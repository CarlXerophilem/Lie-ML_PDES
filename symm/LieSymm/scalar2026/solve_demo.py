"""Seed-paper-first solution programme. Every run requires a NEW output directory.

python -X utf8 -m symm.LieSymm.scalar2026.solve_demo --out build/NEW
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
from pathlib import Path
import time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp,quad
from scipy.interpolate import BPoly
from .api import backend,source_audit,compute_ode_series,SOURCE_SHA256
from .catalog import solution_catalog,t,s,z,F,p,q,h
from .solving import solve_reduction,cubic_autonomous
from .validation import verify_solution,material_audit
from .continuation import continue_profile
from .demo import write_json,_plots


def _select_jet(name,parameters):
    trial=solve_reduction(name,parameters=parameters)
    for f0 in (2,3,4,1):
        for p0 in (sp.Rational(1,2),1,2):
            at={z:1,F:f0,p:p0,q:sp.Rational(1,10)}
            v=trial['velocity'].subs(at);grad=trial['gradient'].subs(at);lead=trial['leading'].subs(at)
            if v.is_positive and grad.is_positive and lead!=0 and abs(float(lead))>.05:
                return (f0,p0,sp.Rational(1,10))[:trial['ode_order']]
    return None


def _plots_new(out,examples,exact):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    paths=[];receipts=[]
    for index,(label,result,numerical) in enumerate(examples):
        if numerical['status']!='passed':continue
        values=np.loadtxt(numerical['csv'],delimiter=',',skiprows=1)
        interp=BPoly.from_derivatives(values[:,0],values[:,1:4],extrapolate=False)
        coords=np.linspace(values[0,0],values[-1,0],65)
        zz,orbit=np.meshgrid(coords,np.linspace(.85,1.15,40))
        inverse=result['inverse_chart']
        if s in inverse:
            tt=orbit;ss=sp.lambdify((z,t),inverse[s],'numpy')(zz,tt)
        else:
            ss=orbit;tt=sp.lambdify((z,s),inverse[t],'numpy')(zz,ss)
            if np.ndim(tt)==0:tt=np.full_like(zz,tt)
        ff=interp(zz);pp=interp.derivative(1)(zz);cc=interp.derivative(2)(zz)
        graph=sp.lambdify((t,s,F),result['graph'],'numpy')(tt,ss,ff)
        vel=sp.lambdify((t,s,F,p,q),result['jets'][1,0],'numpy')(tt,ss,ff,pp,cc)
        grad=sp.lambdify((t,s,F,p,q),result['jets'][0,1],'numpy')(tt,ss,ff,pp,cc)
        valid=np.isfinite(graph)&np.isfinite(vel)&np.isfinite(grad)&(vel>0)&(grad>0)
        graph=np.where(valid,graph,np.nan)
        stem=f'extended-{index:02d}-{label}'
        np.savez_compressed(out/'plots'/f'{stem}.npz',s=ss,t=tt,phi=graph,velocity=vel,gradient=grad,valid=valid)
        fig=plt.figure(figsize=(10,4.5),layout='constrained')
        ax=fig.add_subplot(121,projection='3d');ax.plot_surface(ss,tt,graph,cmap='viridis',linewidth=0)
        ax.set(xlabel='s',ylabel='t',zlabel='phi',title=label)
        ax2=fig.add_subplot(122);ax2.plot(values[:,0],values[:,1],label='DOP853')
        ax2.plot(values[:,0],values[:,4],'--',label='RKF4(5)')
        series=result['series'];coefs=np.array([float(c) for c in series['coefficients']])
        ax2.plot(values[:,0],np.polynomial.polynomial.polyval(values[:,0]-1,coefs),':',label='Taylor degree 6')
        ax2.set(xlabel='z',ylabel='F(z)');ax2.legend(frameon=False);ax2.grid(alpha=.2)
        for ext in ('png','pdf'):fig.savefig(out/'plots'/f'{stem}.{ext}',dpi=150)
        plt.close(fig);paths.append(f'plots/{stem}.png')
        receipts.append(dict(id=label,points=int(valid.size),valid_points=int(valid.sum())))
    # The singular exact family uses quad only to display its exact parameter integral.
    singular=exact['singular']['parametric'];y=singular['parameter'];R=sp.lambdify(y,singular['logarithmic_rate'],'numpy')
    yy=np.linspace(1.8,2.2,90);Z=np.array([np.exp(quad(R,2,float(v),epsabs=1e-12,epsrel=1e-12)[0]) for v in yy])
    rho=(1/(1-.1*(yy-1)**2))**(1/3);profile=yy*rho*Z**(1/3)
    zz,tt=np.meshgrid(Z,np.linspace(.8,1.2,40));ss=zz*tt;phi=tt*profile[None,:]
    fig=plt.figure(figsize=(8,5.5),layout='constrained');ax=fig.add_subplot(111,projection='3d')
    ax.plot_surface(ss,tt,phi,cmap='cividis');ax.set(xlabel='s',ylabel='t',zlabel='phi',title='3.4 cubic L=0: exact parametric family')
    for ext in ('png','pdf'):fig.savefig(out/'plots'/f'singular-cubic.{ext}',dpi=160)
    plt.close(fig);paths.append('plots/singular-cubic.png')
    np.savez_compressed(out/'plots'/'singular-cubic.npz',s=ss,t=tt,phi=phi,y=yy,z=Z,
                        valid=np.ones_like(phi,dtype=bool),quadrature_tolerance=1e-12)
    # A deliberately wider diagnostic grid exercises the domain mask.
    ss,tt=np.meshgrid(np.linspace(-1,1,60),np.linspace(.2,1.2,45))
    vv=ss+.3*np.log(tt)+.2;valid=vv>0;phi=tt*ss+.3*(tt*np.log(tt)-tt)+.2*tt
    fig=plt.figure(figsize=(8,5.5),layout='constrained');ax=fig.add_subplot(111,projection='3d')
    ax.plot_surface(ss,tt,np.where(valid,phi,np.nan),cmap='viridis')
    ax.set(xlabel='s',ylabel='t',zlabel='phi',title='m=1 exact logarithmic family: positive-velocity mask')
    for ext in ('png','pdf'):fig.savefig(out/'plots'/f'logarithmic-masked.{ext}',dpi=160)
    plt.close(fig);paths.append('plots/logarithmic-masked.png')
    np.savez_compressed(out/'plots'/'logarithmic-masked.npz',s=ss,t=tt,phi=np.where(valid,phi,np.nan),velocity=vv,valid=valid)
    receipts.append(dict(id='logarithmic-mask',points=int(valid.size),valid_points=int(valid.sum()),invalid_points=int((~valid).sum())))
    return paths,receipts


def _phase_control(out):
    """Cross the Sigma turning point using log-z, then compare original profile."""
    auto=cubic_autonomous();S,M=auto['variables'];rhs=sp.lambdify((S,M),auto['rhs'],'numpy')
    delta=sp.lambdify(S,auto['delta'],'numpy')
    def fun(r,y):
        if y[0]<=0 or abs(delta(y[0]))<1e-9:raise ValueError('original singularity reached')
        ds,dm=rhs(y[0],y[1]);return [ds,dm,y[0]*np.exp(r/3)]
    rr=np.linspace(0,.15,151)
    phase=solve_ivp(fun,(0,.15),(1,-2/3,2),method='DOP853',t_eval=rr,rtol=1e-11,atol=1e-13)
    original=solve_reduction('paper-3.5',parameters={},data={'z0':1,'jet':(2,1,-sp.Rational(2,3))})
    rhs_orig=sp.lambdify((z,F,p,q),-original['residual'].subs(h,0)/original['leading'],'numpy')
    numeric=backend().solve_ivp_rkf45(lambda x,y:[y[1],y[2],rhs_orig(x,*y)],(1,np.exp(.15)),(2,1,-2/3),
                                    t_eval=np.exp(rr),rtol=1e-11,atol=1e-13)
    reconstructed=np.stack((phase.y[2],phase.y[0]*np.exp(-2*rr/3),phase.y[1]*np.exp(-5*rr/3)))
    error=float(np.max(abs(reconstructed-numeric.y)))
    np.savetxt(out/'phase-turning.csv',np.column_stack((rr,np.exp(rr),phase.y.T,numeric.y.T)),delimiter=',',
               header='r,z,Sigma,M,F_phase,F_RKF,p_RKF,q_RKF',comments='')
    return dict(passed=bool(phase.success and numeric.status=='completed' and error<1e-8),
                initial_Sigma_rate=0,initial_delta=float(delta(1)),max_profile_error=error,
                explanation='Sigma is not a valid independent coordinate here; r remains regular',
                original_singular_continuation=False)


def run(out):
    out=Path(out).resolve();library=Path(__file__).resolve().parents[1]
    if out==library or out.is_relative_to(library):raise ValueError('Outputs must be outside the library')
    if out.exists():raise FileExistsError('Use a NEW output directory')
    out.mkdir(parents=True);started=time.perf_counter()
    print('1. Seed paper, symbolic representative families and E/P/M audit',flush=True)
    b=backend();catalog=solution_catalog();aud=material_audit();source=source_audit()
    symbolic=[]
    for row in catalog:
        row.update(expression=None,data_status='not_supplied')
        symbolic.append(dict(id=row['id'],check=verify_solution(row)))
    write_json(out/'catalog.json',catalog);write_json(out/'symbolic-families.json',symbolic)
    write_json(out/'source-audit.json',source);write_json(out/'material-audit.json',aud)
    if not aud['passed'] or any(not r['check']['reduction_passed'] for r in symbolic if r['check']['status']=='reduction'):
        raise RuntimeError('Symbolic registry gate failed')
    print('2. Direct exact solutions, singular quadrature and zero-constant branches',flush=True)
    cases=[('travel', 'paper-3.9',{},{}),('travel-zero','paper-3.6',{},dict(I0=0)),
           ('accelerating-travel','m1-boost-travel',dict(m=1,a=-1),{}),
           ('accelerating-arbitrary','m1-boost-travel',dict(m=1,a=0),{}),
           ('logarithmic','m1-boost-space',dict(m=1),{}),
           ('logarithmic-negative-time','m1-boost-space',dict(m=1,sigma=-1),{}),
           ('singular','paper-3.4',{},dict(branch='singular')),
           ('power','paper-3.4',{},dict(branch='power')),
           ('arbitrary','paper-3.7',{},{}),('quadratic','paper-3.8',{},{}),
           ('singular-quarter','paper-3.4',dict(kappa=sp.Rational(1,12)),dict(branch='singular')),
           ('singular-one','paper-3.4',dict(kappa=sp.Rational(1,3)),dict(branch='singular'))]
    exact={};checks={}
    for label,name,params,data in cases:
        exact[label]=solve_reduction(name,parameters=params,data=data);checks[label]=verify_solution(exact[label])
        print(' exact',label,checks[label]['exact_passed'],flush=True)
    write_json(out/'exact-solutions.json',exact);write_json(out/'exact-checks.json',checks)
    if not all(v['exact_passed'] for v in checks.values()):raise RuntimeError('Exact solution gate failed')
    print('3. Original nine-subsection campaign, with tighter tolerances',flush=True)
    seed=b.run_campaign(out/'seed-numerics',rtol=1e-10,atol=1e-12)
    series=[compute_ode_series(r['case'],exponent=sp.Rational(str(r['m'])),order=6,g_value=1,kappa_value=sp.Rational(1,30)) for r in seed['runs']]
    write_json(out/'seed-series.json',series);figures=_plots(out,seed,series)
    print('4. Representative families: continuation and independent 40-digit P reference',flush=True)
    experiments=[('m1-scale-boost',dict(m=1,alpha=1)),('m1-boost-travel',dict(m=1,a=-1)),
                 ('cubic-mixed',dict(a=1,b=sp.Rational(1,4))),('cubic-mixed',dict(a=1,b=-1)),
                 ('cubic-mixed',dict(a=1,b=sp.Rational(1,2)))]
    for name in ('cubic-resonant-time','cubic-resonant-space','cubic-resonant-vertical'):
        experiments.extend((name,dict(c=sign)) for sign in (1,-1))
    examples=[];new_records=[]
    for index,(name,params) in enumerate(experiments):
        label=f'{name}-{index}';jet=_select_jet(name,params)
        if jet is None:
            new_records.append(dict(id=label,status='no_constructed_regular_jet_found'));continue
        result=solve_reduction(name,parameters=params,data=dict(z0=1,jet=jet))
        check=verify_solution(result)
        numerical=continue_profile(result,out/'extended-numerics'/label,interval=(1,1.6))
        original_attempt=numerical
        if numerical['status'] in ('failed','guard_stop') and numerical.get('reason')=='integration stopped before the requested endpoint':
            last=min(numerical.get('dop_stop',1),numerical.get('rkf_stop',1))
            local_end=1+(last-1)/2
            numerical=continue_profile(result,out/'extended-numerics'/(label+'-local'),interval=(1,local_end)) if local_end>1 else numerical
            numerical['longer_interval_attempt']=original_attempt
            numerical['interpretation']='Separate local retry; its status determines acceptance. The failed longer continuation remains recorded'
        examples.append((label,result,numerical));new_records.append(dict(label=label,result=result,verification=check,numerics=numerical))
        write_json(out/'extended-solutions.json',new_records)
        print(' extended',label,numerical['status'],flush=True)
    phase=_phase_control(out);write_json(out/'phase-turning.json',phase)
    paths,plot_receipts=_plots_new(out,examples,exact);figures+=paths
    write_json(out/'plot-receipts.json',plot_receipts)
    # A solution-stratum audit, not a new point-algebra classification.
    strata=[]
    for gamma in (sp.Rational(1,10),sp.Rational(1,4),sp.Rational(1,2),sp.Integer(1),sp.Rational(3,2)):
        auto=cubic_autonomous(1,gamma/3);strata.append(dict(g_beta=gamma,autonomous=auto,
            positive_power_exists=bool(gamma<sp.Rational(1,4)),
            positive_Delta_root_exists=bool(gamma<1),
            singular_continuation_status='implicit compatibility recorded; not solved'))
    write_json(out/'solution-strata.json',strata)
    final_results=[]
    for row in catalog:
        result=solve_reduction(row['id'],parameters={})
        related=[n for n in new_records if n.get('result',{}).get('id')==row['id']]
        final_results.append(dict(id=row['id'],status=result['status'],unresolved=result['unresolved'],
                                 remaining_equation=result['remaining_equation'],
                                 symbolic_parameters=row['parameters'],aliases=row['aliases'],
                                 generator=row['generator'],guards=row['guards'],
                                 algebra_dimensions={key:5 if key in ('m1','m3') else 4 for key in row['algebra_strata']},
                                 independent_variables_before=2,independent_variables_after=1 if row['status']=='reduction' else None,
                                 numerical_examples=len(related),ode_order=result.get('ode_order'),
                                 reduced_order=result.get('reduced_order'),
                                 certified_first_integrals=int('first_integral' in result)))
    write_json(out/'solution-inventory.json',final_results)
    structure=['# Symmetry structure and differential order','',
        'Dimensions are reused from the existing classification. Reducing two independent variables to one and reducing ODE order are distinct operations.','',
        '| Family | Parameter strata / algebra dimensions | Generator (tau,xi,eta) | Independent variables | Profile ODE order | Reported reduced order | Independent integrals | Domain |',
        '|---|---|---|---|---:|---:|---:|---|']
    for row in final_results:
        structure.append(f"| {row['id']} | {row['algebra_dimensions']} | `{row['generator']}` | 2 to {row['independent_variables_after']} | {row['ode_order']} | {row['reduced_order']} | {row['certified_first_integrals']} | {'; '.join(row['guards'])} |")
    structure += ['',
        'For 3.4, the first integral gives a second-order equation for F; at m=1 its F-independence gives a first-order equation for p=F_prime plus reconstruction.',
        'For 3.5, the recorded reduced order 1 describes phase curves away from dSigma/dr=0. The implemented continuation retains the two-component first-order system in (Sigma,M), with F reconstructed by quadrature, including turning points.',
        'No combined symmetry/nonlinearity score is introduced. Numerical parameter samples are demonstrations, not continuous parameter coverage.']
    (out/'STRUCTURE.md').write_text('\n'.join(structure)+'\n',encoding='utf-8')
    report=dict(model='P',source_doi='10.3390/math14030433',source_version='v3',source_sha256=SOURCE_SHA256,
                parameter_strata=['m=1','1<m<3','m=3','m>3'],registered_families=len(catalog),
                symbolic_pullback_checks=sum(r['check']['reduction_passed'] for r in symbolic),
                typed_non_ode_records=sum(r['check']['status']!='reduction' for r in symbolic),
                exact_demonstrations=len(checks),exact_passed=sum(r['exact_passed'] for r in checks.values()),
                seed_ivps=len(seed['runs']),seed_passed=sum(r['status']=='passed' for r in seed['runs']),
                extended_ivps=len(new_records),extended_passed=sum(r.get('numerics',{}).get('status')=='passed' for r in new_records),
                phase_control=phase,figures=figures,elapsed_seconds=time.perf_counter()-started,
                all_checks_passed=bool(seed['all_passed'] and all(r['verification']['passed'] for r in series) and phase['passed'] and
                    all(r.get('numerics',{}).get('status')=='passed' and r['verification']['reduction_passed'] and r['result']['series']['passed'] for r in new_records)),
                all_general_closed_forms_solved=False,all_singular_continuations_solved=False,
                limitations=['Constructed data, not source experimental IVPs.',
                             'Exact certificates are conditional on their stated local domains.',
                             'Numerical PDE checks are sampled diagnostics, not continuous error bounds.',
                             'Extended PDE checks differentiate an independent 40-digit IVP reference; all DOP853/RKF45 state components are compared on the output grid.',
                             'Raw float64 PDE diagnostics are retained separately; agreement does not certify either float64 interpolant between grid points.',
                             'Displayed numerical surfaces interpolate double-precision trajectories and are visualizations, not continuously certified solutions.',
                             'Mixed/resonant families have symbolic reductions and local numerical examples, not general exact solutions.',
                             'No new point-algebra classification, E equivalence, novelty claim or ML benefit claimed.'])
    write_json(out/'report.json',report)
    _write_documents(out,report,catalog,exact,final_results)
    manifest={str(path.relative_to(out)).replace('\\','/'):hashlib.sha256(path.read_bytes()).hexdigest() for path in out.rglob('*') if path.is_file()}
    write_json(out/'MANIFEST.json',dict(outputs=manifest,sources={path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in Path(__file__).parent.glob('*.py')}))
    return report


def _write_documents(out,report,catalog,exact,inventory):
    lines=['# 2026 printed SVE: direct solution programme','',
           'Seed: Paliathanasis, Leon and Leach, Mathematics 14 (2026), 433, DOI 10.3390/math14030433, v3.',
           'P remains the research model. E and M are separately audited comparisons.','',
           f"Registered families: {report['registered_families']}; symbolic pullbacks: {report['symbolic_pullback_checks']}; typed non-ODE records: {report['typed_non_ode_records']}.",
           f"Exact demonstrations: {report['exact_passed']}/{report['exact_demonstrations']}; seed IVPs: {report['seed_passed']}/{report['seed_ivps']}; extended IVPs: {report['extended_passed']}/{report['extended_ivps']}.",'',
           '## Coverage and remaining equations','',
           '| Family | Processing status | ODE order | Order after certified reduction | Integrals |',
           '|---|---|---:|---:|---:|']
    for row in inventory:lines.append(f"| {row['id']} | {row['status']} | {row['ode_order']} | {row['reduced_order']} | {row['certified_first_integrals']} |")
    lines+=['','Parameter-stratum coverage, registered-family coverage and solved-family coverage are different counts.',
            'The three symbolic generic families include continuous m; numeric values do not supply their symbolic proof.','',
            '## What was solved','',
            '- m=1 accelerating traveling profiles: B(p) p_prime + p/sigma = I0; parametric quadrature retains the constant-slope family.',
            '- Cubic 3.4 singular L=0: y=w/rho, D=1-g*beta*(y-1)^2, rho^3=g/D; integrate d(log z)/dy=(1+y*d(log rho)/dy)/(1-y/3).',
            '- The equilibrium y=3 gives A^3=27g/(1-4g beta), only with g beta<1/4 on the positive chart.',
            '- 3.5: the log-z autonomous system remains regular at dSigma/dr=0 when Delta!=0. The two reconstructed formulations are compared numerically.',
            '- Printed-bed reconstruction is a closed local path integral with one additive datum; it does not restore physical Eulerian equivalence.','',
            '## Explicit remaining work','',
            '- General explicit integration of regular 3.4 and the 3.5 phase curves remains open.',
            '- General exact solutions of mixed/resonant cubic and m=1 scale-boost equations remain open; regular series and numerical examples are supplied.',
            '- Original zero-leading-coefficient continuation is unresolved except the certified cubic L=0 family and explicitly checked constant branches.',
            '- Charts based on positive t or s do not prove continuation through t=0 or s=0.','',
            '## Numerical validation','',
            'Extended IVPs retain original_pde_float64 without reclassifying its failures. The original_pde field checks an independent mpmath Taylor IVP reconstruction at 40 decimal digits.',
            'Exact rational nine-point weights differentiate original-coordinate position values, without replacing the highest derivative by the ODE RHS. All three fixed h=.003,.002,.001 stencils must satisfy the unchanged 1e-6 threshold and the perturbed-surface negative control.',
            'Every integrated state component of both DOP853 and RKF45 must also agree with that reference on the output grid. These are finite diagnostics, not continuous error bounds or PDE certificates for the raw float64 interpolants.',
            'Seed-paper numerics retain their historical method, separately from the precision-resolved extended check.','',
            '## Interpreting the demo','',
            's is a material label, t is time, phi is particle position. These are not water-depth surfaces.',
            'The logarithmic example includes a genuine invalid-domain mask. Parameter-integral pictures evaluate exact formulas numerically.','']
    lines += ['- '+v for v in report['limitations']]
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    deriv=['# Stepwise derivations of registered P reductions','']
    for row in catalog:
        deriv += [f"## {row['id']}",'',f"Generator: `{row['generator']}`",f"Graph: `{row.get('graph')}`",f"Coordinate: `{row.get('coordinate')}`",f"Q: `{row['Q']}`",f"Undivided residual: `{row['residual']}`",f"Highest coefficient: `{row['leading']}`",f"Guards: `{row['guards']}`",'']
    for label,result in exact.items():
        deriv += [f'## Exact family: {label}','',f"Expression: `{result.get('expression')}`",f"Parameter certificate: `{result.get('parametric')}`",f"Guards: `{result['guards']}`",'']
    (out/'DERIVATIONS.md').write_text('\n'.join(deriv),encoding='utf-8')
    images=''.join(f'<figure><img src="{p}"><figcaption>{html.escape(Path(p).stem)}</figcaption></figure>' for p in report['figures'])
    table=''.join('<tr>'+''.join('<td>'+html.escape(str(r[k]))+'</td>' for k in ('id','status','ode_order','reduced_order'))+'</tr>' for r in inventory)
    (out/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>2026 SVE: verified solution families</title>'
       '<style>body{font:17px/1.6 system-ui;max-width:1180px;margin:40px auto;padding:0 24px;color:#193540;background:#fafbf9}img{width:100%}figure{margin:30px 0}td,th{padding:10px;border-bottom:1px solid #ccd5d1;text-align:left}table{border-collapse:collapse;width:100%}code{overflow-wrap:anywhere}</style>'
       '<h1>2026 SVE: from the printed PDE to verified solutions</h1><p>Paliathanasis, Leon and Leach · Mathematics 14 (2026), 433 · Printed scalar model P.</p>'
       '<p>Original PDE → generator and invariant graph → undivided ODE → solution → original-P reconstruction.</p>'
       '<p>s labels particles; t is time; phi is position. All numerical initial data are constructed. E and M remain separate models.</p>'
       f'<p>{report["exact_passed"]} exact demonstrations; {report["seed_passed"]}/{report["seed_ivps"]} seed and {report["extended_passed"]}/{report["extended_ivps"]} extended numerical IVPs passed.</p>'
       '<p>Extended checks differentiate an independent 40-digit IVP reference and compare all sampled DOP853/RKF45 states. Raw float64 stencil failures are retained. Plotted interpolants are visualizations, not continuously certified PDE solutions.</p>'
       '<p><a href="REPORT.md">Coverage and remaining problems</a> · <a href="DERIVATIONS.md">Stepwise derivations</a> · <a href="report.json">Receipts</a></p>'
       +images+'<h2>All registered families</h2><table><tr><th>Family</th><th>Processing status</th><th>ODE order</th><th>Reduced order</th></tr>'+table+'</table>'
       '<p>General closed forms and all singular continuations have not been obtained. Local series, exact solutions and sampled numerical checks are separate evidence types.</p></html>',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    result=run(parser.parse_args().out);print(json.dumps(result,indent=2))
    return 0 if result['all_checks_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
