"""Guarded continuation with separate float64 and high-precision P diagnostics."""
from pathlib import Path
import json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from .api import backend
from .catalog import t,s,z,F,p,q,h
from .precision import reference_pde_diagnostics


def continue_profile(result,out,*,interval,rtol=1e-10,atol=1e-12):
    """Compare two independent integrators, never continue an implicit singularity."""
    if result.get('data_status')!='compatible' or result.get('leading')==0:
        return dict(status='not_regular',reason=result.get('data_reason','compatible regular initial jet required'))
    start,end=map(float,interval)
    if not np.isfinite([start,end]).all() or end<=start or start!=float(result['data'].get('z0',1)):
        raise ValueError('interval must start at the supplied z0 and increase finitely')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    if (out/'numerics.json').exists():raise FileExistsError('Numerical evidence cannot be overwritten')
    residual=result['residual'];leading=result['leading'];order=result['ode_order']
    highest=(F,p,q,h)[order]
    if sp.diff(residual,highest,2)!=0:return dict(status='not_regular',reason='nonlinear highest derivative requires an implicit solver')
    rhs_expr=sp.cancel(-residual.subs(highest,0)/leading)
    args=(z,)+(F,p,q)[:order]
    funcs=[sp.lambdify(args,e,'numpy') for e in (rhs_expr,leading,result['velocity'],result['gradient'])]
    rhs,lead,vel,grad=funcs
    initial=np.array([float(v) for v in result['data']['jet'][:order]]);grid=np.linspace(start,end,601)
    initial_leading_sign=float(np.sign(lead(start,*initial)))
    stopped=[]
    def guard(x,y):
        try:
            vals=np.array([lead(x,*y),vel(x,*y),grad(x,*y)],float)
            return bool(np.all(np.isfinite(y)) and np.all(np.isfinite(vals)) and initial_leading_sign*vals[0]>1e-10 and vals[1]>1e-9 and vals[2]>1e-9)
        except (ValueError,TypeError,OverflowError,ZeroDivisionError):return False
    def fun(x,y):
        if not guard(x,y):
            stopped.append(float(x));raise ValueError('regular profile guard reached')
        return np.array([*y[1:],rhs(x,*y)],float)
    report=dict(id=result['id'],model='P',interval=[start,end],rtol=rtol,atol=atol,
                initial_jet=initial.tolist(),status='failed',continuous_error_certificate=False,
                initial_leading_sign=initial_leading_sign,
                guard_scope='stage samples retain the initial leading-coefficient sign; not a continuous nonvanishing proof')
    try:
        dop=solve_ivp(fun,(start,end),initial,method='DOP853',rtol=rtol,atol=atol,
                      t_eval=grid,dense_output=True,max_step=(end-start)/80)
        rkf=backend().solve_ivp_rkf45(fun,(start,end),initial,t_eval=grid,rtol=rtol,atol=atol,
                                     guard=guard,max_step=(end-start)/80)
        report.update(dop_status=dop.message,rkf_status=rkf.status)
        report.update(dop_stop=float(dop.t[-1]),rkf_stop=float(rkf.t[-1]))
        np.savetxt(out/'DOP-trajectory.csv',np.column_stack((dop.t,dop.y.T)),delimiter=',')
        np.savetxt(out/'RKF-trajectory.csv',np.column_stack((rkf.t,rkf.y.T)),delimiter=',')
        if not dop.success or rkf.status!='completed' or len(dop.t)!=len(grid) or len(rkf.t)!=len(grid):
            report['reason']='integration stopped before the requested endpoint';return report
        error=float(np.max(np.abs(dop.y-rkf.y)));tolerance=float(1e-7*(1+np.max(np.abs(dop.y))))
        report.update(state_error=error,state_tolerance=tolerance)
        dop_jets=dop.y if order==3 else np.vstack((dop.y,[rhs(x,*y) for x,y in zip(grid,dop.y.T)]))
        rkf_jets=rkf.y if order==3 else np.vstack((rkf.y,[rhs(x,*y) for x,y in zip(grid,rkf.y.T)]))
        np.savetxt(out/'profile.csv',np.column_stack((grid,dop_jets.T,rkf_jets.T)),delimiter=',',
                   header='z,F_DOP,p_DOP,q_DOP,F_RKF,p_RKF,q_RKF',comments='')
        report['csv']=str((out/'profile.csv').resolve())
        report['original_pde_float64']=original_pde_diagnostics(result,dop.sol,backend()._rkf_interpolant(grid,rkf.y),(start,end))
        reference,reference_states=reference_pde_diagnostics(result,grid,dop.y,rkf.y,(start,end))
        report['original_pde']=reference
        if reference_states.shape==dop.y.shape:
            reference_path=out/'reference-profile.csv'
            np.savetxt(reference_path,np.column_stack((grid,reference_states.T)),delimiter=',',
                       header=','.join(('z','F','p','q')[:order+1]),comments='')
            report['reference_csv']=str(reference_path.resolve())
        if 'first_integral' in result:
            integral=sp.lambdify(args,result['first_integral'],'numpy')
            values=np.array([integral(x,*y) for x,y in zip(grid,dop.y.T)])
            drift=float(np.max(abs(values-values[0]))/(1+abs(values[0])))
            report['first_integral_drift']=drift
        else:report['first_integral_drift']=None
        report['status']='passed' if (error<=tolerance and report['original_pde']['passed'] and
             (report['first_integral_drift'] is None or report['first_integral_drift']<=1e-8)) else 'failed'
    except (ValueError,FloatingPointError,OverflowError,ZeroDivisionError) as exc:
        report.update(status='guard_stop' if stopped else 'failed',reason=str(exc),stopped_at=stopped[-1] if stopped else None)
    finally:
        (out/'numerics.json').write_text(json.dumps(report,indent=2,allow_nan=False),encoding='utf-8')
    return report


def original_pde_diagnostics(result,dop_dense,rkf_dense,interval):
    """Retain the raw float64 stencil, including its interpolation/noise floor."""
    b=backend();coord=sp.lambdify((t,s),result['coordinate'],'numpy')
    graph=sp.lambdify((t,s,F),result['graph'],'numpy')
    section={key:sp.lambdify(z,value,'numpy') for key,value in result['section'].items()}
    G,K,N=[float(result['parameters'][key]) for key in ('g','kappa','m')]
    samples=[];negative=[]
    for label,dense in [('DOP853',dop_dense),('RKF45',rkf_dense)]:
        def phi(T,S):
            zz=float(coord(T,S))
            if zz<interval[0] or zz>interval[1]:raise ValueError('PDE stencil outside solved interval')
            return float(graph(T,S,float(dense(zz)[0])))
        for frac in (.45,.5,.55):
            zz=interval[0]+frac*(interval[1]-interval[0]);T=float(section[t](zz));S=float(section[s](zz))
            for step in (.003,.002,.001):
                d=b.original_pde_residual(phi,T,S,m=N,h=step,g=G,kappa=K)
                samples.append(dict(solver=label,z=zz,step=step,residual=d['residual']))
            base=b.original_pde_residual(phi,T,S,m=N,h=.003,g=G,kappa=K)['residual']
            changed=b.original_pde_residual(lambda T,S:phi(T,S)+.001*T**3,T,S,m=N,h=.003,g=G,kappa=K)['residual']
            negative.append(float(abs(changed-base)))
    maximum=max(abs(r['residual']) for r in samples if r['step']==.003)
    return dict(samples=samples,acceptance_max_abs_residual=maximum,acceptance_threshold=1e-6,
                negative_control_differences=negative,negative_control_passed=min(negative)>1e-4,
                passed=bool(maximum<=1e-6 and min(negative)>1e-4),
                method='9x9 differences of reconstructed phi at three step sizes and three locations',
                continuous_certificate=False)
