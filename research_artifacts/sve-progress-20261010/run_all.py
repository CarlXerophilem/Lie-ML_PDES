"""Reproduce symbolic certificates, classical references and CPU experiments."""
import argparse
import csv
import json
import platform
import time
from pathlib import Path
import numpy as np
import scipy
import sympy as sp
from scipy.optimize import least_squares
from scipy.stats import qmc
from scipy.integrate import simpson
from sve_lab.jets import g,kappa,m,t,s,u,act,model_residual,total,p,q,b
from sve_lab.symbolic import obstruction,first_integral,reduced_residual,z,f,P,C,H
from sve_lab.numerics import reference,integrated_reference,taylor,functions
from sve_lab.trials import Trial,original_residual
from sve_lab.tube import tube_certificate

def write_json(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def certificates(out):
    data=[]
    for physical in [False,True]:
        cert=obstruction(physical)
        assert sp.simplify(cert['witness']-3*g*kappa)==0
        E=model_residual(m,physical)
        T=g*m*kappa*total(p**(m-1)*b/q,1)
        common=sp.simplify(act(E,t,s,u)+2*E)
        defect=sp.simplify(act(E,t,-2*s,0)+E-(m-3)*T)
        assert common==0 and defect==0
        data.append({
            'model':cert['model'],
            'status':'first_order_point_continuation_obstructed',
            'generator_scope':'arbitrary smooth tau(t,s,u), xi(t,s,u), eta(t,s,u)',
            'base_generator':'t*d_t - 2*s*d_s',
            'parameter_path':'m=3+delta; fixed nondimensional g,kappa>0; U*=1',
            'guards':['g>0','kappa>0','p=phi_t>0','q=phi_s>0',
                      'regular local jet chart; connected open base domain',
                      'C^1 parameter dependence and enough point-coefficient regularity'],
            'on_shell_phi_ttt':str(cert['shell']),
            'highest_jet':'x=phi_tss',
            'cleared_highest_coefficient':str(cert['highest_polynomial']),
            'polynomial_variables':['p','q'],
            'selected_monomial':'p**2*q**2',
            'selected_coefficient':str(cert['witness']),
            'reason':'An identity on the positive open p,q branch must have every polynomial coefficient zero.',
            'common_scaling_identity_remainder':str(common),
            'X5_defect_identity_remainder':str(defect),
            'first_integral':str(first_integral(m,physical)),
            'excluded_claims':['maximal point classification','contact/generalized/nonlocal symmetries',
                               'singular parameter continuations','novelty','global existence',
                               'shock/weak solutions','data-independent invariant coverage']})
    write_json(out/'symbolic_certificates.json',{'certificates':data})
    write_json(out/'reference_tube_certificates.json',{
        'certificates':[tube_certificate(False),tube_certificate(True)]})

def classical(out):
    rows=[]
    for physical in [False,True]:
        for exponent in [1.,2.,2.9,3.,3.1,4.]:
            started=time.perf_counter()
            ref,guards=reference(exponent,physical)
            integrated,I0=integrated_reference(exponent,physical)
            grid=np.linspace(1,1.4,401)
            F=ref.sol(grid)
            other=integrated.sol(grid)
            _,leading,_=functions(physical)
            drift=float(np.max(np.abs(F[2]*leading(grid,*F,exponent,1.,1/30)-I0)))
            row={'model':'physical_corrected' if physical else 'printed','m':exponent,
                 **guards,'two_vs_three_order_error':float(np.max(np.abs(F[:2]-other[:2]))),
                 'first_integral_drift':drift,'I0':I0,'bed_log_coefficient':I0,
                 'elapsed_seconds':time.perf_counter()-started,'guard_evidence':'sampled, not interval-certified'}
            # Reconstruct b=B(z)+I0/g*log(t); verify its two derivatives.
            fpp=I0/leading(grid,*other[:2],0.,exponent,1.,1/30)
            A=fpp*(grid**2*other[1]-1/other[1]**2)
            bs=-A;bt=I0-grid*bs
            flux=exponent/30*grid*(other[0]-grid*other[1])**(exponent-1)*fpp/other[1]
            expected_bt=flux+(other[0]-grid*other[1])/other[1]*bs if physical else flux
            row['bed_time_equation_error']=float(np.max(np.abs(bt-expected_bt)))
            np.savez(out/f"reference_{row['model']}_m{exponent:g}.npz",
                     z=grid,F=F[0],Fp=F[1],Fpp=F[2],bed_profile=other[2],I0=I0)
            rows.append(row)
    write_json(out/'classical_results.json',{'cases':rows})
    return rows

def affine_jets(trial,y,z):
    zero=np.zeros(trial.n_features)
    base=trial.jets(y,z,zero)
    columns=[trial.jets(y,z,np.eye(trial.n_features)[i]) for i in range(trial.n_features)]
    basis={key:np.stack([v[key]-base[key] for v in columns],axis=-1) for key in base}
    return lambda weights:{key:base[key]+np.einsum('...j,j->...',basis[key],weights) for key in base}

def fit_case(exponent,physical,method,seed,out):
    started=time.perf_counter()
    kind={'hard_ivp_tanh':'reduced_tanh','taylor4_tanh':'reduced_tanh',
          'hard_ivp_chebyshev':'reduced_chebyshev','direct_2d_tanh':'direct_tanh'}[method]
    order=4 if method=='taylor4_tanh' else 2
    prior=taylor(exponent,physical,order)
    trial=Trial(prior,kind,seed)
    if kind=='direct_tanh':
        sample=qmc.Sobol(2,scramble=True,seed=100).random_base2(6)
        ys=sample[:,0]*np.log(2);zs=1+.4*sample[:,1]
        measure=np.exp(-ys)*np.sqrt(.4*np.log(2)/64)
    else:
        ys=np.zeros(64);zs=1+.4*(np.arange(64)+.5)/64
        measure=np.full(64,np.sqrt(.4*3/8/64))
    cached=affine_jets(trial,ys,zs)
    def objective(weights):
        E,pv,qv=original_residual(cached(weights),zs,exponent,physical,
                                 safe_optimization=True)
        return np.concatenate([measure*E,100*np.minimum(pv-.05,0),100*np.minimum(qv-.05,0)])
    fitted=least_squares(objective,np.zeros(12),bounds=(-10.,10.),max_nfev=150,
                         ftol=1e-11,xtol=1e-11,gtol=1e-11)
    training_seconds=time.perf_counter()-started
    # Final evidence uses new quadrature and untouched reference information.
    ref,reference_guards=reference(exponent,physical)
    yy=np.linspace(0,np.log(2),25);zz=np.linspace(1,1.4,161)
    Y,Z=np.meshgrid(yy,zz,indexing='ij')
    jets=trial.jets(Y,Z,fitted.x)
    E,pv,qv=original_residual(jets,Z,exponent,physical)
    err=jets[(0,0)]-ref.sol(zz)[0][None,:]
    residual_squared=simpson(simpson(E**2*np.exp(-2*Y),x=zz,axis=1),x=yy)
    lead=-Z**3*qv+Z/qv**2+exponent/30*Z*pv**(exponent-1)/qv
    if physical:lead+=-pv*Z**2+pv/qv**3
    data_errors=[np.max(np.abs(trial.derivative(yy,1.,fitted.x,0,j)-val))
                 for j,val in enumerate([2.,.5,.1])]
    row={'model':'physical_corrected' if physical else 'printed','m':exponent,
         'method':method,'seed':seed,'trainable_parameters':12,'collocation_points':64,
         'nfev':int(fitted.nfev),'optimizer_success':bool(fitted.success),
         'optimizer_message':fitted.message,'training_seconds':training_seconds,
         'validation_seconds':time.perf_counter()-started-training_seconds,
         'max_U_error':float(np.max(np.abs(err))),
         'max_original_phi_error':float(np.max(np.abs(np.exp(Y)*err))),
         'original_residual_L2':float(np.sqrt(residual_squared)),
         'max_data_error':float(max(data_errors)),
         'max_graph_invariance_defect_Uy':float(np.max(np.abs(jets[(1,0)]))),
         'min_phi_s':float(qv.min()),'min_phi_t':float(pv.min()),
         'min_abs_z_leading':float(np.min(np.abs(lead))),
         'branch_guard_evidence':'sampled, not interval-certified'}
    tag=f"{row['model']}_m{exponent:g}_{method}_seed{seed}"
    np.savez(out/f'candidate_{tag}.npz',weights=fitted.x,az=trial.az,ay=trial.ay,
             bias=trial.bias,prior=prior,z=zz,y=yy,U=jets[(0,0)],original_E_scaled=E)
    print(json.dumps({key:row[key] for key in ('model','m','method','seed',
          'max_U_error','original_residual_L2','training_seconds') }),flush=True)
    return row

def experiments(out,quick=False):
    rows=[]
    for physical in [False,True]:
        for exponent in ([3.1] if quick else [2.9,3.1]):
            for method in ['hard_ivp_tanh','taylor4_tanh','hard_ivp_chebyshev','direct_2d_tanh']:
                for seed in ([17] if quick or method=='hard_ivp_chebyshev' else [17,23,41]):
                    rows.append(fit_case(exponent,physical,method,seed,out))
    write_json(out/'experiment_results.json',{
        'scope':'small CPU fixed-feature tanh trial experiment on constructed smooth invariant data',
        'protocol':{'initial':[2.,.5,.1],'g':1.,'kappa':1/30,'z_interval':[1.,1.4],
                    't_interval':[1.,2.],'optimizer':'scipy least_squares',
                    'max_nfev':150,'features':12,'final_validation_grid':[25,161],
                    'output_weight_bounds':[-10.,10.],
                    'optimizer_branch_floor':.05,
                    'hidden_layer':'fixed random features; only output weights optimized',
                    'comparison_limitations':['fixed hidden-layer features, not deep-network training',
                        'equal parameters and nfev cap; wall times measured rather than equalized',
                        'direct method has a genuinely two-variable correction',
                        'constructed data rather than a canal data set',
                        'sampled guards and quadrature rather than rigorous interval bounds',
                        'no statistical significance or general speedup theorem']},'cases':rows})
    with (out/'experiment_results.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--quick',action='store_true',help='one seed at m=3.1')
    parser.add_argument('--skip-learning',action='store_true')
    parser.add_argument('--out',type=Path,default=Path('results'))
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    started=time.perf_counter()
    write_json(args.out/'environment.json',{'python':platform.python_version(),
         'platform':platform.platform(),'numpy':np.__version__,'scipy':scipy.__version__,
         'sympy':sp.__version__,'timestamp_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
         'learning_scope':'CPU scipy output-weight optimization; no GPU used'})
    certificates(args.out);classical_rows=classical(args.out)
    experiment_rows=[] if args.skip_learning else experiments(args.out,args.quick)
    write_json(args.out/'run_summary.json',{'classical_cases':len(classical_rows),
        'learning_cases':len(experiment_rows),'elapsed_seconds':time.perf_counter()-started,
        'symbolic_status':'both unrestricted obstructions and both first integrals verified'})

if __name__=='__main__':main()
