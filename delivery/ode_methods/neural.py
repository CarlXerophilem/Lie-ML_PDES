"""Three complete recipes. Training has no reference/verification callback."""
import time
import torch
import numpy as np


class Network(torch.nn.Module):
    def __init__(self,liquid=False,width=64):
        super().__init__();self.liquid=liquid
        self.hidden=torch.nn.ModuleList([torch.nn.Linear(1 if i==0 else width,width) for i in range(4)])
        if liquid:
            self.core=torch.nn.ModuleList([torch.nn.Linear(width,width) for _ in range(4)])
            self.alpha=torch.nn.ParameterList([torch.nn.Parameter(torch.full((width,),.5)) for _ in range(4)])
        self.output=torch.nn.Linear(width,1)
    def forward(self,x):
        for i,layer in enumerate(self.hidden):
            x=torch.tanh(layer(x))
            if self.liquid:x=x+self.alpha[i]*torch.tanh(self.core[i](x))
        return self.output(x)
    def record(self):
        def layer(v,kind):return {'kind':kind,'weight':v.weight.detach().tolist(),'bias':v.bias.detach().tolist()}
        layers=[]
        for i,v in enumerate(self.hidden):
            layers.append(layer(v,'tanh'))
            if self.liquid:layers.append({**layer(self.core[i],'residual'),'alpha':self.alpha[i].detach().tolist()})
        layers.append(layer(self.output,'linear'));return layers


def fit(task,method,steps=8000,cpu_seconds=150,seed=27,prefix=None):
    torch.set_num_threads(1);torch.set_default_dtype(torch.float64);torch.use_deterministic_algorithms(True);torch.manual_seed(seed)
    net=Network(liquid=method=='lnn');optimizer=torch.optim.Adam(net.parameters(),lr=1e-3)
    lo,hi=task.interval;nodes=torch.linspace(lo,hi,128).reshape(-1,1)
    from symbolic_input import Expressions
    reader=Expressions()
    residual=task.torch_function();coeff=None if prefix is None else [float(reader.read(v)) for v in prefix]
    def model(x):
        y=net(x)
        if coeff is not None:
            yy=torch.zeros_like(x)
            for v in reversed(coeff):yy=yy*x+v
            y=yy+x**len(coeff)*y
        return y
    quad,weight=np.polynomial.legendre.leggauss(16)
    u=torch.tensor((quad+1)/2).reshape(1,-1);weight=torch.tensor(weight/2).reshape(1,-1)
    start=time.process_time();termination='step_budget';last_loss=None
    for step in range(steps):
        if time.process_time()-start>=cpu_seconds:termination='cpu_budget';break
        optimizer.zero_grad()
        if method=='prefix':
            at=nodes*u;flat=at.reshape(-1,1);yy=model(flat).reshape(at.shape)
            # R=A(s,y)*y_s+B(s,y). Derive f=-B/A without accessing an oracle.
            R0=residual(at,yy,torch.zeros_like(yy));R1=residual(at,yy,torch.ones_like(yy))
            if task.critical:
                b=float(task.data['b']);psi_over_X=b*yy-R0
                integral=torch.sum(weight*u**(b-1)*psi_over_X,dim=1,keepdim=True)
                error=model(nodes)-integral
            else:
                rhs=-R0/(R1-R0)
                error=model(nodes)-task.trace-nodes*torch.sum(weight*rhs,dim=1,keepdim=True)
            loss=torch.mean(error**2)
        else:
            x=nodes.clone().requires_grad_(True);y=model(x)
            dy=torch.autograd.grad(y,x,torch.ones_like(y),create_graph=True)[0]
            error=residual(x,y,dy)
            loss=torch.mean(error**2)+(model(torch.zeros((1,1)))-task.trace).square().mean()
        if not torch.isfinite(loss):termination='nonfinite_loss';break
        loss.backward();optimizer.step();last_loss=float(loss.detach())
    else:step=steps
    probes=[]
    probe_coordinates=(lo,(lo+hi)/2,hi)
    for coordinate in probe_coordinates:
        x=torch.tensor([[coordinate]],requires_grad=True);value=model(x)
        derivative=torch.autograd.grad(value,x,torch.ones_like(value))[0]
        probes.append({'coordinate':str(coordinate),'value':float(value.detach()),'derivative':float(derivative.detach())})
    return {'autograd_probes':probes,'representation':'network','layers':net.record(),'prefix':None if prefix is None else list(prefix),
            'parameter_count':sum(v.numel() for v in net.parameters()),'steps_completed':step,
            'status':'fixed_budget_approximation','termination':termination,'loss':last_loss,'seed':seed,
            'optimizer':'Adam','learning_rate':1e-3,'residual_points':128,'quadrature_nodes':16 if method=='prefix' else None,
            'verification_points':list(map(str,probe_coordinates)),'cpu_seconds':time.process_time()-start}
