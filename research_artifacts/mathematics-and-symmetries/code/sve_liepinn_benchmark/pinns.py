"""Matched PINN architectures, jet-space Lie losses, and paired controls."""
import csv
import time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from models import initial_torch, residual_torch, equation_scales, subgroup_coeff_torch, multiplier
from numerics import grid


class MLP(nn.Module):
    def __init__(self, nin, width, depth, nout):
        super().__init__()
        layers=[]
        for i in range(depth):
            layers.extend([nn.Linear(nin if i == 0 else width,width),nn.Tanh()])
        self.net=nn.Sequential(*layers,nn.Linear(width,nout))
    def forward(self,x):
        return self.net(x)


class ModifiedMLP(nn.Module):
    """Wang et al., equations 43--47: tanh mixing gates, not sigmoid gates."""
    def __init__(self,width):
        super().__init__()
        self.u,self.v,self.first=[nn.Linear(11,width) for _ in range(3)]
        self.gates=nn.ModuleList([nn.Linear(width,width) for _ in range(2)])
        self.out=nn.Linear(width,4)
    def forward(self,x):
        u,v,h=[torch.tanh(layer(x)) for layer in (self.u,self.v,self.first)]
        for layer in self.gates:
            z=torch.tanh(layer(h));h=(1-z)*u+z*v
        return self.out(h)


class OperatorNet(nn.Module):
    """Small branch/trunk dot-product adaptation of the paper's Eq. 9."""
    def __init__(self,width,rank=8):
        super().__init__()
        self.rank=rank
        self.branch=MLP(70,width,2,4*rank)
        self.trunk=MLP(5,width,2,rank)
    def forward(self,features,context):
        b=self.branch(context).reshape(1,4,self.rank)
        return (b*self.trunk(features)[:,None,:]).sum(2)/np.sqrt(self.rank)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters())


class PINN(nn.Module):
    def __init__(self,architecture,horizon,width=32):
        super().__init__()
        self.architecture,self.horizon=architecture,horizon
        target=count_parameters(MLP(11,width,3,4))
        if architecture == 'mlp':
            self.raw=MLP(11,width,3,4);self.width=width
        else:
            factory=ModifiedMLP if architecture == 'modified' else OperatorNet
            if architecture not in ('modified','deeponet'):
                raise ValueError(architecture)
            self.width=min(range(4,129),key=lambda w:abs(count_parameters(factory(w))-target))
            self.raw=factory(self.width)
        self.double()
        for layer in self.modules():
            if isinstance(layer,nn.Linear):
                nn.init.xavier_normal_(layer.weight);nn.init.zeros_(layer.bias)

    def forward(self,points,case):
        t,x,y=points.unbind(1)
        x,y=x-case.phase_x,y-case.phase_y
        features=torch.stack([t/self.horizon,torch.sin(x),torch.cos(x),torch.sin(y),torch.cos(y)],1)
        context=points.new_tensor(case.context()).expand(len(points),-1)
        if self.architecture == 'deeponet':
            sx,sy=grid(4)
            sensors=points.new_tensor(np.column_stack([np.zeros(16),sx.ravel()+case.phase_x,
                                                       sy.ravel()+case.phase_y]))
            branch=torch.cat([initial_torch(sensors,case).reshape(-1),context[0]]).reshape(1,-1)
            raw=self.raw(features,branch)
        else:
            raw=self.raw(torch.cat([features,context],1))
        base=initial_torch(points,case)
        # Identical hard IC, periodicity, positive depth, and frozen-bed ansatz for all methods.
        return torch.stack([base[:,0]*torch.exp(t*.08*raw[:,0]),
                            base[:,1]+t*.12*raw[:,1],base[:,2]+t*.12*raw[:,2],
                            base[:,3]+t*.02*case.kappa*raw[:,3]],1)


def jet(model,points,case):
    points=points.detach().requires_grad_(True)
    fields=model(points,case)
    derivatives=[torch.autograd.grad(fields[:,i].sum(),points,create_graph=True)[0] for i in range(4)]
    return torch.cat([points,fields,*derivatives],1)


def lie_dots(equations,jets,generators):
    # Differentiating equations with respect to independent jet coordinates.
    jac=torch.stack([torch.autograd.grad(equations[:,i].sum(),jets,create_graph=True,
                                       retain_graph=True)[0] for i in range(4)],1)
    return torch.stack([(jac*subgroup_coeff_torch(jets,g)[:,None,:]).sum(2)
                        for g in generators],1)


def objective(model,points,case,method,generators,weight=1.,return_tensors=False):
    jets=jet(model,points,case)
    equations=residual_torch(jets,case)
    scales=jets.new_tensor(equation_scales(case))
    pde=(equations/scales).square().mean()
    extra=pde*0
    if method in ('lie','cosine') and generators:
        dots=lie_dots(equations,jets,generators)
        if method == 'lie':
            extra=(dots/scales).square().mean()
        else:
            # Scale each equation consistently before measuring jet-space angles.
            jac=torch.stack([torch.autograd.grad((equations[:,i]/scales[i]).sum(),jets,
                       create_graph=True,retain_graph=True)[0] for i in range(4)],1)
            coeff=torch.stack([subgroup_coeff_torch(jets,g) for g in generators],1)
            denom=jac.square().sum(2).sqrt()[:,None,:]*coeff.square().sum(2).sqrt()[:,:,None]
            extra=((dots/scales)/(denom+1e-12)).square().mean()
    elif method == 'reweighted' and generators:
        matrices=jets.new_tensor(np.array([multiplier(g) for g in generators]))
        extra=(torch.einsum('gab,nb->nga',matrices,equations)/scales).square().mean()
    elif method == 'conservation':
        x,y=grid(8)
        times=points.new_tensor([.5*model.horizon,model.horizon])
        quadrature=torch.cat([torch.stack([torch.full_like(points.new_tensor(x.ravel()),t),
                      points.new_tensor(x.ravel()),points.new_tensor(y.ravel())],1) for t in times])
        fields=model(quadrature,case).reshape(2,64,4)
        ic=initial_torch(quadrature[:64]*quadrature.new_tensor([0.,1.,1.]),case)
        drift=fields.mean(1)-ic.mean(0)
        extra=(drift[:,0]/(.08*model.horizon)).square().mean()
        if case.kappa:
            extra=extra+(drift[:,3]/(.02*case.kappa*model.horizon)).square().mean()
    elif method not in ('vanilla','lie','reweighted','cosine'):
        raise ValueError(method)
    loss=pde+weight*extra
    return loss,({'pde':pde,'extra':extra} if return_tensors else
                 {'pde':float(pde.detach()),'extra':float(extra.detach())})


def gradient_diagnostics(model,points,case,method,generators,weight):
    _,parts=objective(model,points,case,method,generators,weight,return_tensors=True)
    parameters=tuple(model.parameters())
    gp=torch.autograd.grad(parts['pde'],parameters,retain_graph=True)
    ge=torch.autograd.grad(weight*parts['extra'],parameters)
    gp=torch.cat([g.reshape(-1) for g in gp]).detach()
    ge=torch.cat([g.reshape(-1) for g in ge]).detach()
    npde,nextra=float(gp.norm()),float(ge.norm())
    return {'pde_gradient_norm':npde,'weighted_extra_gradient_norm':nextra,
            'extra_to_pde_norm_ratio':nextra/max(npde,1e-30),
            'gradient_cosine':float(torch.dot(gp,ge)/(gp.norm()*ge.norm())) if nextra>1e-20 else None,
            'case':case.name,'point_count':len(points),
            'interpretation':'local diagnostic; negative cosine means conflicting gradient directions'}


def points_for_grid(times,n):
    x,y=grid(n)
    return np.concatenate([np.column_stack([np.full(n*n,t),x.ravel(),y.ravel()]) for t in times])


def metrics(pred,reference,case):
    error=pred-reference
    evolution=reference[1:]-reference[0]
    evolution_error=error[1:]
    per_rmse=np.sqrt(np.mean(evolution_error**2,axis=(0,1,2)))
    per_scale=np.sqrt(np.mean(evolution**2,axis=(0,1,2)))
    active=[0,1,2]+([3] if case.kappa else [])
    rel_fields={name:float(per_rmse[i]/max(per_scale[i],1e-14)) if i in active else None
                for i,name in enumerate(['h','u','v','b'])}
    return {'relative_l2':float(np.linalg.norm(error)/np.linalg.norm(reference)),
            'evolution_relative_l2':float(np.linalg.norm(evolution_error)/max(np.linalg.norm(evolution),1e-14)),
            'max_active_field_evolution_error':max(rel_fields[name] for name in ['h','u','v','b']
                                                  if rel_fields[name] is not None),
            'field_evolution_relative_l2':rel_fields,'field_rmse':dict(zip(['h','u','v','b'],map(float,per_rmse))),
            'mass_drift':float(np.max(np.abs(pred[...,0].mean((1,2))-reference[0,...,0].mean()))),
            'bed_mean_drift':float(np.max(np.abs(pred[...,3].mean((1,2))-reference[0,...,3].mean()))),
            'min_depth':float(pred[...,0].min()),
            'min_speed':float(np.sqrt(pred[...,1]**2+pred[...,2]**2).min())}


def predict(model,case,times,n):
    with torch.no_grad():
        return model(torch.tensor(points_for_grid(times,n),dtype=torch.float64),case).numpy().reshape(len(times),n,n,4)


def train_run(train_cases,test_cases,references,audits,architecture,method,seed,args,output):
    directory=Path(output);directory.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter();torch.manual_seed(seed)
    model=PINN(architecture,args.horizon,args.width)
    init_seconds=time.perf_counter()-start
    optimizer=torch.optim.Adam(model.parameters(),lr=args.lr)
    rng=np.random.default_rng(seed+1123)
    banks={c.name:torch.tensor(rng.random((args.collocation,3))*[args.horizon,2*np.pi,2*np.pi],
                                     dtype=torch.float64) for c in train_cases}
    histories=[];snapshots=[];train_seconds=0.;monitor_seconds=0.
    sample=test_cases[0];times,reference,_=references[sample.name]
    monitor_points=torch.tensor(np.random.default_rng(seed+5678).random((args.collocation,3))*
                                [args.horizon,2*np.pi,2*np.pi],dtype=torch.float64)
    status='ok';message=''
    steps_to_monitor=set(np.linspace(0,args.steps,9,dtype=int))
    def monitor(step,loss=np.nan,pde=np.nan,extra=np.nan):
        nonlocal monitor_seconds
        tic=time.perf_counter();pred=predict(model,sample,times,args.eval_grid)
        scores=metrics(pred,reference,sample)
        monitor_pde=float((residual_torch(jet(model,monitor_points,sample),sample)/
                           monitor_points.new_tensor(equation_scales(sample))).square().mean().detach())
        histories.append({'step':step,'train_seconds':train_seconds,'loss':loss,'pde':pde,'extra':extra,
                          'monitor_pde':monitor_pde,
                          'validation_evolution_error':scores['evolution_relative_l2'],
                          'validation_max_field_error':scores['max_active_field_evolution_error']})
        snapshots.append(pred[-1]);monitor_seconds+=time.perf_counter()-tic
    monitor(0)
    for step in range(1,args.steps+1):
        case=train_cases[(step-1)%len(train_cases)]
        generators=audits[case.name]['useful_generators']
        if args.generators is not None:
            verified={r['generator'] for r in audits[case.name]['generators'] if r['verified']}
            generators=[g for g in args.generators if g in verified]
            if set(generators)!=set(args.generators):
                raise ValueError(f'Unverified generator requested for {case.name}')
        tic=time.perf_counter();optimizer.zero_grad(set_to_none=True)
        try:
            loss,parts=objective(model,banks[case.name],case,method,generators,args.sym_weight)
            if not torch.isfinite(loss):
                raise FloatingPointError('nonfinite training loss')
            loss.backward();optimizer.step()
            train_seconds+=time.perf_counter()-tic
        except (FloatingPointError,RuntimeError) as exc:
            status='failed';message=str(exc);train_seconds+=time.perf_counter()-tic;break
        if step in steps_to_monitor:
            monitor(step,float(loss.detach()),parts['pde'],parts['extra'])
    training_wall_seconds=time.perf_counter()-start
    tests={};inference=[]
    for case in test_cases:
        times,reference,diagnostic=references[case.name]
        # Warm-up and median time for a full grid query; reference is cached too.
        prediction=predict(model,case,times,args.eval_grid)
        durations=[]
        for _ in range(7):
            tic=time.perf_counter();predict(model,case,times,args.eval_grid);durations.append(time.perf_counter()-tic)
        duration=float(np.median(durations));inference.append(duration)
        scores=metrics(prediction,reference,case)
        evaluation=torch.tensor(rng.random((args.collocation,3))*[args.horizon,2*np.pi,2*np.pi],dtype=torch.float64)
        independent=(residual_torch(jet(model,evaluation,case),case)/torch.tensor(equation_scales(case))).square().mean()
        scores['independent_pde_mse']=float(independent.detach())
        scores['inference_seconds']=duration
        uncertainty=diagnostic['estimated_reference_uncertainty']
        active=[0,1,2]+([3] if case.kappa else [])
        evolution_scale=max(float(np.sqrt(np.mean((reference[1:]-reference[0])**2,axis=(0,1,2)))[active].min()),1e-14)
        reference_ok=(uncertainty is not None and uncertainty/evolution_scale < args.accuracy/10
                      and diagnostic['tight']['min_depth']>0 and diagnostic['tight']['sampled_max_eigenvalue_imag']<1e-10)
        scores['reference_accuracy_guard_passed']=bool(reference_ok)
        branch_ok=scores['min_depth']>0 and (not case.kappa or scores['min_speed']>1e-6)
        scores['sampled_physical_branch_passed']=bool(branch_ok)
        matched=status=='ok' and branch_ok and reference_ok and scores['max_active_field_evolution_error']<=args.accuracy
        scores['matched_accuracy']=bool(matched)
        classical=diagnostic['ladder'][-1]['solve_seconds']
        eligible=len(train_cases)>1 and matched and classical>duration
        scores['new_parameter_query_break_even']=int(np.ceil(training_wall_seconds/(classical-duration))) if eligible else None
        scores['break_even_reason']='matched new-parameter solves' if eligible else (
            'accuracy threshold not reached' if not matched else 'single-PDE solution is cached or no measured inference advantage')
        tests[case.name]=scores
        np.savez_compressed(directory/(case.name+'.npz'),prediction=prediction,reference=reference,times=times)
    diagnostic_case=train_cases[0]
    diagnostic_generators=args.generators if args.generators is not None else audits[diagnostic_case.name]['useful_generators']
    gradients=gradient_diagnostics(model,banks[diagnostic_case.name],diagnostic_case,method,diagnostic_generators,args.sym_weight)
    with (directory/'history.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=histories[0]);writer.writeheader();writer.writerows(histories)
    np.savez_compressed(directory/'snapshots.npz',fields=np.array(snapshots),steps=np.array([h['step'] for h in histories]))
    torch.save({'state_dict':model.state_dict(),'architecture':architecture,'width':args.width,
                'horizon':args.horizon,'train_cases':[c.metadata() for c in train_cases]},directory/'model.pt')
    return {'architecture':architecture,'method':method,'seed':seed,'status':status,'message':message,
            'parameters':count_parameters(model),'hidden_width':model.width,
            'init_seconds':init_seconds,'train_seconds':train_seconds,'monitor_seconds':monitor_seconds,
            'training_wall_seconds':training_wall_seconds,
            'total_seconds':time.perf_counter()-start,'steps_completed':step,
            'distinct_collocation_points':len(train_cases)*args.collocation,
            'test_metrics':tests,'gradient_diagnostics':gradients,'directory':str(directory)}


def identity_check(case,generators,horizon=.25):
    torch.manual_seed(992);model=PINN('mlp',horizon)
    points=torch.rand(16,3,dtype=torch.float64)*torch.tensor([horizon,6.28,6.28])
    results=[]
    for method in ('lie','reweighted'):
        model.zero_grad(set_to_none=True)
        loss,_=objective(model,points,case,method,generators)
        grads=torch.autograd.grad(loss,tuple(model.parameters()))
        results.append((float(loss.detach()),torch.cat([g.reshape(-1) for g in grads]).detach()))
    return {'loss_difference':abs(results[0][0]-results[1][0]),
            'max_parameter_gradient_difference':float((results[0][1]-results[1][1]).abs().max())}
