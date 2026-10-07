#!/usr/bin/env python3
"""Series-first smooth edge-KAN and damped correction-chain SWE/SVE pilot.

The model is a finite-parameter conditional field solver. No arbitrary-function
operator claim, fixed-point convergence theorem, or KAN superiority is assumed.
The copied baseline_core directory contains the already-reviewed PDE/reference.
"""
import argparse
import csv
import json
import platform
import time
from dataclasses import replace
from pathlib import Path
import numpy as np
import sympy as sp
import torch
from torch import nn
from baseline_core.models import Case,conditional_family,initial_torch,residual_torch,equation_scales
from baseline_core.numerics import ladder,grid


def make_coefficients():
    """P2 = U0 + t*F(U0) + t^2/2 * DF(U0)[F(U0)], fully coupled."""
    tic=time.perf_counter()
    x,y,A,B,u0,v0,g,k,m,f,gamma=sp.symbols('x y A B u0 v0 g k m f gamma',real=True)
    h,u,v,b,hx,hy,ux,uy,vx,vy,bx,by=sp.symbols('h u v b hx hy ux uy vx vy bx by',real=True)
    r2=u*u+v*v
    flux=k*(r2**((m-1)/2)*(ux+vy)+(m-1)*r2**((m-3)/2)*(u*u*ux+u*v*vx+u*v*uy+v*v*vy))
    F=sp.Matrix([-u*hx-v*hy-h*(ux+vy),-u*ux-v*uy-g*(hx+bx)+f*v-gamma*u,
                 -u*vx-v*vy-g*(hy+by)-f*u-gamma*v,-flux])
    U0=sp.Matrix([1+A*sp.cos(x)*sp.cos(y),u0,v0,B*sp.sin(x)*sp.sin(y)])
    z=(h,u,v,b,hx,hy,ux,uy,vx,vy,bx,by)
    initial=(*U0,*(sp.diff(q,coord) for q in U0 for coord in (x,y)))
    rules=dict(zip(z,initial));F0=F.subs(rules,simultaneous=True)
    direction=sp.Matrix([*F0,*(sp.diff(q,coord) for q in F0 for coord in (x,y))])
    second=sp.simplify(F.jacobian(z).subs(rules,simultaneous=True)*direction/2)
    variables=(x,y,A,B,u0,v0,g,k,m,f,gamma)
    fn=sp.lambdify(variables,[*F0,*second],modules=[{'sin':torch.sin,'cos':torch.cos},'math'],cse=True)
    report={'construction':'a1=F(U0); a2=DF(U0)[a1]/2','order':2,'fields':['h','u','v','b'],
            'seconds':time.perf_counter()-tic,'operation_count':sum(int(sp.count_ops(e)) for e in [*F0,*second]),
            'a1':list(map(str,F0)),'a2':list(map(str,second)),
            'scope':'local smooth expansion; not a convergence radius or global solution certificate'}
    return fn,report


COEFFICIENTS=None


def polynomial(points,case,order=2):
    values=COEFFICIENTS(points[:,1]-case.phase_x,points[:,2]-case.phase_y,case.amplitude,
                       case.bed_amplitude,case.u0,case.v0,case.g,case.kappa,case.m,case.coriolis,case.drag)
    tensors=[q if isinstance(q,torch.Tensor) else torch.zeros_like(points[:,0])+q for q in values]
    a1,a2=torch.stack(tensors[:4],1),torch.stack(tensors[4:],1)
    t=points[:,0,None]
    return initial_torch(points,case)+(t*a1 if order>=1 else 0)+(t*t*a2 if order>=2 else 0)


class EdgeKAN(nn.Module):
    """Smooth Gaussian edge functions + linear edge term, followed by node sums.

RBF-KAN architecture is informed by the DeepOKAN authors' implementation.
This is an independently implemented conditional-field variant, not DeepOKAN.
"""
    def __init__(self,nin,nout,centers=8):
        super().__init__()
        self.register_buffer('centers',torch.linspace(-1,1,centers,dtype=torch.float64))
        self.width=2/(centers-1)
        self.coefficients=nn.Parameter(torch.randn(nout,nin,centers,dtype=torch.float64)*.04/np.sqrt(nin))
        self.linear=nn.Parameter(torch.randn(nout,nin,dtype=torch.float64)*.04/np.sqrt(nin))
        self.bias=nn.Parameter(torch.zeros(nout,dtype=torch.float64))
    def forward(self,x):
        basis=torch.exp(-((x[:,:,None]-self.centers)/self.width).square())
        return torch.einsum('nik,oik->no',basis,self.coefficients)+x@self.linear.T+self.bias


class RawNet(nn.Module):
    def __init__(self,kind='kan',zero_output=False):
        super().__init__();self.kind=kind
        if kind=='kan':
            self.layers=nn.ModuleList([EdgeKAN(11,19),EdgeKAN(19,4)])
        else:
            self.layers=nn.ModuleList([nn.Linear(11,32),nn.Linear(32,32),nn.Linear(32,32),nn.Linear(32,4)])
            self.double()
            for layer in self.layers:nn.init.xavier_normal_(layer.weight);nn.init.zeros_(layer.bias)
        if zero_output:
            last=self.layers[-1]
            for parameter in last.parameters():nn.init.zeros_(parameter)
    def forward(self,x):
        for layer in self.layers[:-1]:x=torch.tanh(layer(x))
        return self.layers[-1](x)


def features(points,case,horizon):
    t,x,y=points.unbind(1);x,y=x-case.phase_x,y-case.phase_y
    context=points.new_tensor(case.context()).expand(len(points),-1)
    return torch.cat([torch.stack([2*t/horizon-1,torch.sin(x),torch.cos(x),torch.sin(y),torch.cos(y)],1),context],1)


class Field(nn.Module):
    def __init__(self,kind,horizon,series_order=0):
        super().__init__();self.horizon=horizon;self.series_order=series_order
        self.blocks=nn.ModuleList([RawNet(kind,zero_output=True)])
        self.weights=[1.]
    def forward(self,points,case):
        t=points[:,0,None];z=features(points,case,self.horizon)
        raw=sum(w*block(z) for w,block in zip(self.weights,self.blocks))
        scales=points.new_tensor([.08,.12,.12,.02*case.kappa])
        if self.series_order:
            return polynomial(points,case,self.series_order)+t.pow(self.series_order+1)/self.horizon**self.series_order*raw*scales
        base=initial_torch(points,case)
        return torch.stack([base[:,0]*torch.exp(t[:,0]*scales[0]*raw[:,0]),
                            base[:,1]+t[:,0]*scales[1]*raw[:,1],base[:,2]+t[:,0]*scales[2]*raw[:,2],
                            base[:,3]+t[:,0]*scales[3]*raw[:,3]],1)


def residual(model,points,case):
    points=points.detach().requires_grad_(True);fields=model(points,case)
    derivatives=[torch.autograd.grad(fields[:,i].sum(),points,create_graph=True)[0] for i in range(4)]
    j=torch.cat([points,fields,*derivatives],1)
    return residual_torch(j,case),fields


def pde_loss(model,points,case,components=False):
    equations,fields=residual(model,points,case)
    if fields[:,0].min().detach()<=0 or (case.kappa and (fields[:,1:3].square().sum(1).min().detach()<1e-12)):
        raise FloatingPointError('Left positive-depth / nonzero-speed branch')
    square=(equations/points.new_tensor(equation_scales(case))).square()
    return square.mean(0) if components else square.mean()


def sensitivity_loss(model,points,case,parameter,step):
    """Central-difference proxy for the parameter sensitivity equation d_p R=0.

    Both coefficient and field change with p. No reference sensitivity or test
    cases enter this physics term; it does not certify the exact gradient.
    """
    value=getattr(case,parameter)
    plus=replace(case,**{parameter:value+step});minus=replace(case,**{parameter:value-step})
    rp,_=residual(model,points,plus);rm,_=residual(model,points,minus)
    normalized=(rp-rm)/(2*step*points.new_tensor(equation_scales(case)))
    return normalized.square().mean()


def physics_validation(model,cases,banks):
    return float(np.mean([float(pde_loss(model,banks[c.name],c).detach()) for c in cases]))


def physics_components(model,cases,banks):
    return np.mean([pde_loss(model,banks[c.name],c,components=True).detach().numpy() for c in cases],axis=0)


def predict(model,case,times,n):
    x,y=grid(n)
    points=np.concatenate([np.column_stack([np.full(n*n,t),x.ravel(),y.ravel()]) for t in times])
    with torch.no_grad():return model(torch.tensor(points,dtype=torch.float64),case).numpy().reshape(len(times),n,n,4)


def scores(pred,ref,case):
    err=pred[1:]-ref[1:];evolution=ref[1:]-ref[0]
    rmse=np.sqrt(np.mean(err**2,axis=(0,1,2)));scale=np.sqrt(np.mean(evolution**2,axis=(0,1,2)))
    fields=rmse/np.maximum(scale,1e-14)
    active=[0,1,2]+([3] if case.kappa else [])
    return {'evolution_relative_l2':float(np.linalg.norm(err)/max(np.linalg.norm(evolution),1e-14)),
            'per_field_evolution_error':dict(zip(['h','u','v','b'],map(float,fields))),
            'max_field_evolution_error':float(fields[active].max()),'mass_drift':float(np.max(abs(pred[...,0].mean((1,2))-ref[0,...,0].mean()))),
            'bed_mean_drift':float(np.max(abs(pred[...,3].mean((1,2))-ref[0,...,3].mean()))),'min_depth':float(pred[...,0].min())}


def run_model(method,seed,train,test,refs,args,out):
    torch.manual_seed(seed);start=time.perf_counter()
    is_chain=method.startswith('chain');kind='mlp' if method.endswith('mlp') else 'kan'
    order=2 if method.startswith('series') or is_chain else 0
    model=Field(kind,args.horizon,order)
    rng=np.random.default_rng(seed+1123)
    banks={c.name:torch.tensor(rng.random((args.points,3))*[args.horizon,2*np.pi,2*np.pi],dtype=torch.float64) for c in train}
    valrng=np.random.default_rng(seed+3141)
    validation={c.name:torch.tensor(valrng.random((args.points,3))*[args.horizon,2*np.pi,2*np.pi],dtype=torch.float64) for c in train}
    history=[];stages=[];train_seconds=0.
    stage_count=args.stages if is_chain else 1
    budget=args.steps//stage_count if is_chain else args.steps
    for stage in range(stage_count):
        if stage:
            for parameter in model.parameters():parameter.requires_grad_(False)
            model.blocks.append(RawNet(kind,zero_output=True));model.weights.append(1.)
        before=physics_validation(model,train,validation)
        before_components=physics_components(model,train,validation) if args.acceptance=='per_equation' else None
        optimizer=torch.optim.Adam([p for p in model.parameters() if p.requires_grad],lr=args.lr)
        for step in range(1,budget+1):
            case=train[(step-1)%len(train)];tic=time.perf_counter()
            optimizer.zero_grad(set_to_none=True);loss=pde_loss(model,banks[case.name],case)
            if args.sensitivity_weight:
                parameter='m' if args.family=='sve' else 'coriolis'
                loss=loss+args.sensitivity_weight*sensitivity_loss(model,banks[case.name],case,parameter,args.sensitivity_step)
            if not torch.isfinite(loss):raise FloatingPointError('Nonfinite training loss')
            loss.backward();optimizer.step();train_seconds+=time.perf_counter()-tic
            if step in set(np.linspace(1,budget,8,dtype=int)):
                val=physics_validation(model,train,validation)
                times,ref,_=refs[test[0].name];measure=scores(predict(model,test[0],times,args.n),ref,test[0])
                history.append({'stage':stage,'step':stage*budget+step,'training_seconds':train_seconds,
                                'training_loss':float(loss.detach()),'physics_validation':val,
                                'heldout_evolution_error':measure['evolution_relative_l2'],
                                'heldout_max_field_error':measure['max_field_evolution_error']})
        # Backtracking is based ONLY on unseen physics points of training cases.
        # Test-reference errors never select a stage weight.
        candidates=[]
        if is_chain:
            for alpha in [1.,.5,.25,.125,0.]:
                model.weights[-1]=alpha
                try:
                    val=physics_validation(model,train,validation)
                    if before_components is not None:
                        vector=physics_components(model,train,validation)
                        if np.any(vector>before_components*(1+1e-10)+1e-14):val=float('inf')
                except FloatingPointError:val=float('inf')
                candidates.append((alpha,val))
            alpha,after=min(candidates,key=lambda v:v[1]);model.weights[-1]=alpha
            if after>before*(1+1e-12):raise AssertionError('Backtracking failed to preserve validation loss')
        else:alpha,after=1.,physics_validation(model,train,validation)
        times,ref,_=refs[test[0].name];measure=scores(predict(model,test[0],times,args.n),ref,test[0])
        stages.append({'stage':stage,'before_physics_validation':before,'after_physics_validation':after,
                       'before_components':before_components.tolist() if before_components is not None else None,
                       'after_components':physics_components(model,train,validation).tolist() if before_components is not None else None,
                       'accepted_weight':alpha,'backtracking_trials':[{'weight':a,'loss':v if np.isfinite(v) else None} for a,v in candidates],
                       'test_diagnostic_only':measure,'compute_seconds_cumulative':train_seconds})
    training_wall=time.perf_counter()-start;tests={};directory=out/method/f'seed{seed}';directory.mkdir(parents=True,exist_ok=True)
    for case in test:
        times,ref,diag=refs[case.name];pred=predict(model,case,times,args.n);metric=scores(pred,ref,case)
        active=[0,1,2]+([3] if case.kappa else [])
        scale=max(float(np.sqrt(np.mean((ref[1:]-ref[0])**2,axis=(0,1,2)))[active].min()),1e-14)
        reference_ok=diag['estimated_reference_uncertainty']/scale<.005 and diag['tight']['sampled_max_eigenvalue_imag']<1e-10
        metric['reference_guard_passed']=bool(reference_ok)
        metric['matched_5percent']=bool(reference_ok and metric['min_depth']>0 and metric['max_field_evolution_error']<=.05)
        durations=[]
        for _ in range(5):
            tic=time.perf_counter();predict(model,case,times,args.n);durations.append(time.perf_counter()-tic)
        metric['inference_seconds']=float(np.median(durations));tests[case.name]=metric
        np.savez_compressed(directory/(case.name+'.npz'),prediction=pred,reference=ref,times=times)
    with (directory/'history.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=history[0]);writer.writeheader();writer.writerows(history)
    checkpoint={'state_dict':model.state_dict(),'weights':model.weights,'method':method,'horizon':args.horizon,
                'series_order':order,'blocks':len(model.blocks),'kind':kind,'train_cases':[c.metadata() for c in train]}
    torch.save(checkpoint,directory/'model.pt')
    return {'method':method,'seed':seed,'parameters':sum(p.numel() for p in model.parameters()),
            'parameters_per_block':sum(p.numel() for p in model.blocks[0].parameters()),
            'steps':budget*stage_count,'training_compute_seconds':train_seconds,'training_wall_seconds':training_wall,
            'test_metrics':tests,'stages':stages,'directory':str(directory),
            'selection':'fixed checkpoint; chain alpha chosen only by training-family physics validation'}


def verify():
    torch.manual_seed(73);case=Case('verify',m=3.1)
    p=torch.rand(8,3,dtype=torch.float64)*torch.tensor([.25,6.28,6.28],dtype=torch.float64);p[:,0]=0
    # Independent autograd differentiation of PDE F, versus symbolic coefficients.
    base=initial_torch(p.requires_grad_(True),case)
    d=[torch.autograd.grad(base[:,i].sum(),p,create_graph=True)[0] for i in range(4)]
    j=torch.cat([p,base,*d],1);F0=-residual_torch(j,case)
    a1_expected=F0.detach()
    tangent=torch.stack([torch.autograd.grad(F0[:,i].sum(),p,create_graph=True)[0] for i in range(4)],1)
    independent=torch.cat([j[:,:3].detach(),j[:,3:].detach()],1).requires_grad_(True)
    F=-residual_torch(independent,case)
    # F(U)=-spatial residual: independent temporal jets are zero in this check.
    direction=torch.cat([torch.zeros_like(p),F0,*[tangent[:,i] for i in range(4)]],1)
    expected=[]
    for i in range(4):expected.append((torch.autograd.grad(F[:,i].sum(),independent,retain_graph=True)[0]*direction).sum(1)/2)
    values=COEFFICIENTS(p[:,1],p[:,2],case.amplitude,case.bed_amplitude,case.u0,case.v0,case.g,case.kappa,case.m,case.coriolis,case.drag)
    values=torch.stack([q if isinstance(q,torch.Tensor) else p[:,0]*0+q for q in values],1)
    a1err=float((values[:,:4]-a1_expected).abs().max().detach());a2err=float((values[:,4:]-torch.stack(expected,1)).abs().max().detach())
    assert a1err<1e-12 and a2err<1e-12,(a1err,a2err)
    layer=EdgeKAN(2,2);inputs=torch.tensor([[.13,-.29],[.27,.36]],dtype=torch.float64,requires_grad=True)
    assert torch.autograd.gradcheck(layer,(inputs,),eps=1e-6,atol=1e-5,rtol=1e-4)
    assert torch.autograd.gradgradcheck(layer,(inputs,),eps=1e-6,atol=1e-5,rtol=1e-4)
    q=layer(inputs).sum();g1=torch.autograd.grad(q,inputs,create_graph=True)[0]
    g2=torch.autograd.grad(g1.sum(),inputs,create_graph=True)[0];g3=torch.autograd.grad(g2.sum(),inputs)[0]
    assert torch.isfinite(g3).all()
    model=Field('kan',.25,2);e,fields=residual(model,p.detach(),case)
    assert float((fields-initial_torch(p,case)).abs().max().detach())==0
    assert float(e.abs().max().detach())<1e-12
    # Independent exact uniform Coriolis/drag control checks series derivatives.
    uniform=Case('uniform',amplitude=0,bed_amplitude=0,kappa=0,coriolis=.2,drag=.05)
    q=polynomial(p,uniform);dt=[torch.autograd.grad(q[:,i].sum(),p,create_graph=True,retain_graph=True)[0][:,0] for i in range(4)]
    assert abs(float(dt[1][0].detach())-(-uniform.drag*uniform.u0+uniform.coriolis*uniform.v0))<1e-12
    class ExactUniform(nn.Module):
        def forward(self,points,case):
            t=points[:,0];decay=torch.exp(-case.drag*t);c=torch.cos(case.coriolis*t);s=torch.sin(case.coriolis*t)
            return torch.stack([t*0+1,decay*(case.u0*c+case.v0*s),decay*(case.v0*c-case.u0*s),t*0],1)
    exact_sensitivity=float(sensitivity_loss(ExactUniform(),p.detach(),uniform,'coriolis',.01).detach())
    assert exact_sensitivity<1e-20
    # Test preserved derivatives with an actually nonzero correction block.
    last=model.blocks[0].layers[-1]
    for parameter in last.parameters():nn.init.normal_(parameter,mean=.1,std=.03)
    q=p.detach().requires_grad_(True);corrected=model(q,case)
    first=torch.stack([torch.autograd.grad(corrected[:,i].sum(),q,create_graph=True,retain_graph=True)[0][:,0] for i in range(4)],1)
    second=torch.stack([torch.autograd.grad(first[:,i].sum(),q,retain_graph=True)[0][:,0] for i in range(4)],1)
    first_error=float((first-values[:,:4].detach()).abs().max().detach())
    second_error=float((second-2*values[:,4:].detach()).abs().max().detach())
    assert first_error<1e-12 and second_error<1e-12
    return {'status':'passed','symbolic_vs_autograd_a1_max':a1err,'symbolic_vs_autograd_a2_max':a2err,
            'RBF_KAN_gradcheck':True,'RBF_KAN_gradgradcheck':True,'finite_third_derivative':True,
            'initial_PDE_residual_exact':True,'uniform_source_series_checked':True,
            'nonzero_correction_initial_first_derivative_error':first_error,
            'nonzero_correction_initial_second_derivative_error':second_error,
            'exact_uniform_parameter_sensitivity_residual':exact_sensitivity}


def render(out,payload):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(14,4))
    methods=payload['arguments']['methods'];colors=dict(zip(methods,plt.cm.tab10.colors))
    for run in payload['runs']:
        with (Path(run['directory'])/'history.csv').open() as f:rows=list(csv.DictReader(f))
        x=[float(r['training_seconds']) for r in rows];p=[float(r['physics_validation']) for r in rows]
        e=[float(r['heldout_evolution_error']) for r in rows]
        axes[0].semilogy(x,p,color=colors[run['method']],alpha=.6)
        axes[1].semilogy(x,e,color=colors[run['method']],alpha=.6)
        for stage in run['stages']:
            axes[2].scatter(stage['after_physics_validation'],stage['test_diagnostic_only']['evolution_relative_l2'],
                            color=colors[run['method']],alpha=.7)
    axes[0].set(xlabel='Training compute (s)',ylabel='Physics-validation MSE',title='Residual reduction')
    axes[1].set(xlabel='Training compute (s)',ylabel='Held-out evolution error',title='Prediction accuracy')
    axes[2].set(xlabel='Accepted-stage physics loss',ylabel='Held-out evolution error',xscale='log',yscale='log',title='A smaller residual need not rank error')
    from matplotlib.lines import Line2D
    axes[0].legend(handles=[Line2D([0],[0],color=colors[m],label=m) for m in methods],fontsize=8)
    fig.tight_layout();fig.savefig(out/'halfway_process.png',dpi=160);plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify-only',action='store_true');p.add_argument('--steps',type=int,default=600)
    p.add_argument('--stages',type=int,default=2);p.add_argument('--points',type=int,default=128)
    p.add_argument('--seeds',nargs='+',type=int,default=[0,1,2]);p.add_argument('--horizon',type=float,default=.25)
    p.add_argument('--n',type=int,default=16);p.add_argument('--lr',type=float,default=.001)
    p.add_argument('--family',choices=['flat','sve'],default='flat')
    p.add_argument('--acceptance',choices=['total','per_equation'],default='total',
                   help='For chains: preserve total validation loss or every equation component')
    p.add_argument('--sensitivity-weight',type=float,default=0,
                   help='Optional weight for a finite-difference parameter-sensitivity PDE residual')
    p.add_argument('--sensitivity-step',type=float,default=.01)
    p.add_argument('--methods',nargs='+',choices=['direct_mlp','direct_kan','series_mlp','series_kan','chain_kan','chain_mlp'],
                   default=['direct_mlp','direct_kan','series_mlp','series_kan','chain_mlp','chain_kan'])
    p.add_argument('--out',default='results/series_kan_pilot');args=p.parse_args()
    if args.steps<args.stages or args.stages<1 or args.points<8 or args.horizon<=0:p.error('Invalid budget, stages, points, or horizon')
    if args.sensitivity_weight<0 or args.sensitivity_step<=0:p.error('Invalid sensitivity weight or step')
    torch.set_num_threads(1);torch.set_num_interop_threads(1)
    global COEFFICIENTS
    COEFFICIENTS,construction=make_coefficients();out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'series_construction.json').write_text(json.dumps(construction,indent=2))
    check=verify();(out/'verification.json').write_text(json.dumps(check,indent=2));print('Series and KAN derivative verification passed.',flush=True)
    if args.verify_only:return
    if args.family=='sve':
        train,test=conditional_family();test=[c for c in test if c.name!='test_translated']
    else:
        train=[Case(f'train_f{f:g}_a{a:g}',coriolis=f,amplitude=a,kappa=0,bed_amplitude=0)
               for f in [0,.1,.2] for a in [.02,.04]]
        test=[Case(f'test_f{f:g}_a0.03',coriolis=f,amplitude=.03,kappa=0,bed_amplitude=0) for f in [.05,.15]]
    refs={};reference_start=time.perf_counter()
    for case in test:refs[case.name]=ladder(case,[12,18,24],args.horizon,args.n)
    baselines={}
    for order in [0,1,2]:
        class Taylor(nn.Module):
            def forward(self,points,case):return polynomial(points,case,order)
        baselines[f'P{order}']={c.name:scores(predict(Taylor(),c,refs[c.name][0],args.n),refs[c.name][1],c) for c in test}
    payload={'arguments':vars(args),'series':construction,'references':{n:r[2] for n,r in refs.items()},
             'reference_wall_seconds':time.perf_counter()-reference_start,'Taylor_controls':baselines,
             'train_cases':[c.metadata() for c in train],'test_cases':[c.metadata() for c in test],
             'environment':{'python':platform.python_version(),'torch':torch.__version__,'sympy':sp.__version__,'device':'CPU','threads':1,'dtype':'float64'},
             'protocol':'parameter-conditioned field solver; exact P2, smooth edge functions, damped frozen-block chain; no function-space operator claim',
             'runs':[]}
    for seed in args.seeds:
        for method in args.methods:
            run=run_model(method,seed,train,test,refs,args,out);payload['runs'].append(run)
            (out/'results.json').write_text(json.dumps(payload,indent=2,allow_nan=False))
            print(method,seed,round(run['training_compute_seconds'],3),[round(v['evolution_relative_l2'],5) for v in run['test_metrics'].values()],flush=True)
    render(out,payload)


if __name__=='__main__':main()
