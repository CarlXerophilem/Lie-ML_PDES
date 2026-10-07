#!/usr/bin/env python3
"""Unreduced (t,s) PINN baseline for the scalar SVE master equation, m=3.

Run: python base_PINN.py --steps 1000 --lbfgs 100 --out results
Dependencies: numpy scipy sympy torch pytorch-optimizer matplotlib pillow

Default: smooth tanh network, float64, hard Cauchy data (phi,phi_t,phi_tt),
SOAP then deterministic L-BFGS polishing. SOAP evidence:
https://arxiv.org/abs/2502.00604 ; competing 2026 optimizers:
https://arxiv.org/abs/2604.05230 . This is a strong configurable baseline,
NOT a claim that this architecture/optimizer is globally best or PirateNets.
No similarity coordinate enters this network. Exact interior values are used
only for validation; supplied boundary/Cauchy data select a known solution.
"""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from base_LieReduct import (Problem,problem_arguments,problem_from_args,
                           symbolic_model,write_equations,save_result)


def derivative(y,x):
    return torch.autograd.grad(y,x,torch.ones_like(y),create_graph=True)[0]


class Network(nn.Module):
    def __init__(self,dim,width,depth):
        super().__init__()
        layers=[]
        for k in range(depth):
            layers.extend([nn.Linear(dim if k==0 else width,width),nn.Tanh()])
        layers.append(nn.Linear(width,1))
        self.net=nn.Sequential(*layers)
        for layer in self.net:
            if isinstance(layer,nn.Linear):
                nn.init.xavier_normal_(layer.weight); nn.init.zeros_(layer.bias)
        nn.init.zeros_(self.net[-1].weight)

    def forward(self,x):
        return self.net(x)


class DirectField(nn.Module):
    def __init__(self,problem,width,depth):
        super().__init__();self.problem=problem
        self.net=Network(2,width,depth)

    def forward(self,ts):
        p=self.problem;t,s=ts[:,0:1],ts[:,1:2];tau=t-p.t0
        # Only known Cauchy data, not the interior solution, enter this lift.
        a=p.c*s.pow(1/3)*p.t0**(2/3)
        b=(2/3)*a/p.t0; c=(-2/9)*a/p.t0**2
        norm=torch.cat([2*(t-p.t0)/(p.t1-p.t0)-1,
                        2*(s-p.s0)/(p.s1-p.s0)-1],dim=1)
        return a+b*tau+0.5*c*tau*tau+tau**3*self.net(norm)


def pde_residual(model,ts,problem):
    """Differentiate original divergence-form PDE, not a surrogate residual."""
    phi=model(ts);d=derivative(phi,ts);pt,ps=d[:,0:1],d[:,1:2]
    dd_t=derivative(pt,ts);ptt,pts=dd_t[:,0:1],dd_t[:,1:2]
    pss=derivative(ps,ts)[:,1:2]
    A=ps*ptt-problem.g*pss/ps**2
    B=pt**2*pts/ps
    E=derivative(A,ts)[:,0:1]-problem.g*problem.beta*derivative(B,ts)[:,1:2]
    return E,phi,pt,ps


def reduced_residual(model,ts,problem):
    z=(ts[:,1:2]*ts[:,0:1]**2).detach().requires_grad_(True)
    f=model.profile(z);p=derivative(f,z);q=derivative(p,z)
    A=2*z*p*p+4*z*z*p*q-problem.g*q/p**2
    B=8*z*z*p*(p+z*q)
    R=2*z*derivative(A,z)-problem.g*problem.beta*derivative(B,z)
    return R/ts[:,0:1],ts[:,0:1]**2*p


def neural_arguments(parser):
    problem_arguments(parser)
    parser.add_argument('--steps',type=int,default=1000,help='SOAP/Adam iterations; demonstration budget.')
    parser.add_argument('--lbfgs',type=int,default=100,help='Full-batch polishing iterations.')
    parser.add_argument('--points',type=int,default=256)
    parser.add_argument('--width',type=int,default=24)
    parser.add_argument('--depth',type=int,default=3)
    parser.add_argument('--lr',type=float,default=0.003)
    parser.add_argument('--seed',type=int,default=7)
    parser.add_argument('--optimizer',choices=['soap','adam'],default='soap')
    parser.add_argument('--device',default='cpu')
    parser.add_argument('--threads',type=int,default=1)
    parser.add_argument('--resample',type=int,default=100,help='Sobol resampling interval; 0 freezes points.')
    parser.add_argument('--self-test',action='store_true',help='Symbolic and autodiff consistency checks only.')


def setup(args):
    if min(args.width,args.depth,args.points,args.threads)<=0 or min(args.steps,args.lbfgs,args.resample)<0 or args.lr<=0:
        raise ValueError('Invalid positive size or nonnegative iteration setting.')
    torch.set_default_dtype(torch.float64);torch.set_num_threads(args.threads)
    torch.manual_seed(args.seed);np.random.seed(args.seed)
    return problem_from_args(args)


def checks(problem):
    assert symbolic_model()['verified']
    class Exact(nn.Module):
        def forward(self,ts):
            return problem.c*(ts[:,1:2]*ts[:,0:1]**2).pow(1/3)
    ts=torch.tensor([[1.03,1.04],[1.15,1.12]],requires_grad=True)
    E,*_=pde_residual(Exact(),ts,problem)
    assert E.abs().max().item()<1e-9, E
    class Polynomial(nn.Module):
        def profile(self,z):return 1+z+z*z/7+z**3/23
        def forward(self,ts):return self.profile(ts[:,1:2]*ts[:,0:1]**2)
    direct,*_=pde_residual(Polynomial(),ts,problem)
    reduced,_=reduced_residual(Polynomial(),ts,problem)
    torch.testing.assert_close(direct,reduced,rtol=1e-10,atol=1e-10)
    print('PASS: exact solution, X5, invariant, symbolic reduction and off-solution AD identity.')


def train(model,problem,args,reduced=False):
    device=torch.device(args.device);model=model.to(device)
    sobol=torch.quasirandom.SobolEngine(2,scramble=True,seed=args.seed)
    lo=torch.tensor([problem.t0,problem.s0],device=device)
    span=torch.tensor([problem.t1-problem.t0,problem.s1-problem.s0],device=device)
    def points():return (lo+sobol.draw(args.points).to(device=device,dtype=torch.float64)*span).requires_grad_(True)
    ts=points()
    # Same boundary data for both methods; no interior exact labels.
    bt=torch.linspace(problem.t0,problem.t1,33,device=device).reshape(-1,1)
    boundary=torch.cat([torch.cat([bt,torch.full_like(bt,edge)],1)
                        for edge in (problem.s0,problem.s1)],0)
    target=problem.c*(boundary[:,1:2]*boundary[:,0:1]**2).pow(1/3)
    initial_s=torch.linspace(problem.s0,problem.s1,33,device=device).reshape(-1,1)
    initial=torch.cat([torch.full_like(initial_s,problem.t0),initial_s],1).requires_grad_(True)
    initial_phi=problem.c*initial_s.pow(1/3)*problem.t0**(2/3)
    initial_v=2*initial_phi/(3*problem.t0)
    initial_acc=-2*initial_phi/(9*problem.t0**2)
    # A common dimensionless equation scale, not fitted from exact residuals.
    equation_scale=problem.c**2/problem.t0
    weights={'boundary':1.0}
    def losses():
        if reduced:E,ps=reduced_residual(model,ts,problem)
        else:E,_,_,ps=pde_residual(model,ts,problem)
        physics=(E/equation_scale).square().mean()
        data=((model(boundary)-target)/problem.c).square().mean()
        # Both solvers receive the same Cauchy functions. The direct lift
        # satisfies them exactly; the reduced model enforces them softly
        # except for its three hard anchor coefficients.
        ip=model(initial);iv=derivative(ip,initial)[:,0:1]
        ia=derivative(iv,initial)[:,0:1]
        data=data+((ip-initial_phi)/problem.c).square().mean()
        data=data+((iv-initial_v)*problem.t0/problem.c).square().mean()
        data=data+((ia-initial_acc)*problem.t0**2/problem.c).square().mean()
        positivity=torch.relu(0.05-ps).square().mean()
        return physics,data,positivity
    if args.optimizer=='soap':
        try:from pytorch_optimizer import SOAP
        except ImportError as exc:raise RuntimeError('Install pytorch-optimizer for SOAP, or explicitly use --optimizer adam.') from exc
        opt=SOAP(model.parameters(),lr=args.lr,weight_decay=0,precondition_frequency=10)
    else:opt=torch.optim.Adam(model.parameters(),lr=args.lr)
    history=[];start=time.perf_counter()
    for step in range(args.steps):
        if step and args.resample and step%args.resample==0:ts=points()
        opt.zero_grad(set_to_none=True);ts.grad=None;initial.grad=None
        physics,data,positive=losses()
        # Gradient-norm balancing applies to soft boundary data. Freeze for LBFGS.
        if step%50==0:
            params=list(model.parameters())
            norms=[]
            for term in (physics,data):
                grad=torch.autograd.grad(term,params,retain_graph=True,allow_unused=True)
                norms.append(torch.sqrt(sum((v*v).sum() for v in grad if v is not None)).detach().item())
            if norms[1]>1e-14:
                proposed=float(np.clip(norms[0]/norms[1],0.1,100))
                weights['boundary']=0.9*weights['boundary']+0.1*proposed
        loss=physics+weights['boundary']*data+positive
        if not torch.isfinite(loss):raise FloatingPointError('Nonfinite loss; inspect domain/Jacobian and learning rate.')
        loss.backward();opt.step()
        history.append([step,float(loss.detach()),float(physics.detach()),float(data.detach())])
        if step%100==0:print(f'step {step}: physics={float(physics.detach()):.3e}, boundary={float(data.detach()):.3e}',flush=True)
    if args.lbfgs:
        opt2=torch.optim.LBFGS(model.parameters(),max_iter=args.lbfgs,
                              tolerance_grad=1e-12,tolerance_change=1e-14,line_search_fn='strong_wolfe')
        def closure():
            opt2.zero_grad(set_to_none=True);ts.grad=None;initial.grad=None
            a,b,c=losses();loss=a+weights['boundary']*b+c
            if not torch.isfinite(loss):raise FloatingPointError('LBFGS encountered nonfinite residual.')
            loss.backward();return loss
        opt2.step(closure)
    seconds=time.perf_counter()-start
    final=[float(x.detach()) for x in losses()]
    metrics={'training_seconds':seconds,'optimizer':args.optimizer+' + L-BFGS',
             'steps':args.steps,'lbfgs_max_iterations':args.lbfgs,'seed':args.seed,
             'parameter_count':sum(p.numel() for p in model.parameters()),
             'points':args.points,'width':args.width,'depth':args.depth,'lr':args.lr,
             'final_scaled_losses':final,'boundary_weight':weights['boundary'],
             'torch_version':torch.__version__,'device':str(device),
             'architecture':'tanh MLP; not a reproduction of PirateNets',
             'training_labels':'boundary/Cauchy only; no interior solution labels'}
    return model,metrics,history


def evaluate(model,problem,args,name,metrics,history):
    T,S=problem.grid();coords=np.column_stack([T.ravel(),S.ravel()])
    outputs=[[],[],[],[]]
    # Full original PDE evaluation, including for the reduced network.
    for start in range(0,len(coords),128):
        ts=torch.tensor(coords[start:start+128],device=args.device,requires_grad=True)
        E,phi,v,ps=pde_residual(model,ts,problem)
        if ps.min().item()<=0:raise ValueError('Jacobian lost positivity on validation grid.')
        for target,x in zip(outputs,[phi,v,1/ps,E]):target.append(x.detach().cpu().numpy().ravel())
    arrays=[np.concatenate(x).reshape(T.shape) for x in outputs]
    # Independent validation of all Cauchy data, including acceleration.
    initial=torch.tensor(np.column_stack([T[0],S[0]]),device=args.device,requires_grad=True)
    ip=model(initial);iv=derivative(ip,initial)[:,0:1];ia=derivative(iv,initial)[:,0:1]
    exact_ip=problem.c*(initial[:,1:2]*problem.t0**2).pow(1/3)
    mismatch=torch.cat([(ip-exact_ip)/problem.c,
                        (iv-2*exact_ip/(3*problem.t0))*problem.t0/problem.c,
                        (ia+2*exact_ip/(9*problem.t0**2))*problem.t0**2/problem.c],1)
    metrics['max_scaled_cauchy_mismatch']=float(mismatch.detach().abs().max())
    save_result(args.out,name,problem,*arrays,metrics,history)
    checkpoint={'state_dict':model.state_dict(),'args':{k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},'method':name}
    torch.save(checkpoint,Path(args.out)/(name+'.pt'))
    if not args.no_scene:
        from pde_scene import render
        render(args.out,coordinates=args.coordinates)


def run(args):
    problem=setup(args)
    if args.self_test:return checks(problem)
    write_equations(args.out,problem)
    model=DirectField(problem,args.width,args.depth)
    model,metrics,history=train(model,problem,args)
    evaluate(model,problem,args,'PINN',metrics,history)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);neural_arguments(parser)
    run(parser.parse_args())
