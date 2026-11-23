"""Exact 2D SVE checks and a constructed cubic rotating-flow IVP.

Run from any directory: python -B main.py --out results
No source paper's numerical experiment is reproduced by this script.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_name] = "1"

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

HERE = Path(__file__).resolve().parent


def clean(expr):
    return s.factor(s.simplify(s.expand(expr)))


def zero_list(expressions):
    return [clean(expr) for expr in expressions]


def jet_model(exponent=None):
    """First jets are independent; K already includes inverse solid fraction."""
    t, x, y = s.symbols("t x y", real=True)
    h, u, v, b = s.symbols("h u v b", real=True)
    g, K = s.symbols("g K", positive=True)
    m = s.Symbol("m", real=True) if exponent is None else s.sympify(exponent)
    base, fields = (t, x, y), (h, u, v, b)
    jets = {(f, z): s.Symbol(f"{f}_{z}", real=True) for f in fields for z in base}

    def total(expr, z):
        return s.diff(expr, z) + sum(s.diff(expr, f) * jets[f, z] for f in fields)

    speed_factor = (u*u + v*v)**((m-1)/2)
    flux = (speed_factor*u, speed_factor*v)
    divq = total(flux[0], x) + total(flux[1], y)
    E = s.Matrix([
        jets[h,t] + total(h*u,x) + total(h*v,y),
        jets[u,t] + u*jets[u,x] + v*jets[u,y] + g*(jets[h,x]+jets[b,x]),
        jets[v,t] + u*jets[v,x] + v*jets[v,y] + g*(jets[h,y]+jets[b,y]),
        jets[b,t] + K*divq,
    ])
    conservative = s.Matrix([
        E[0],
        total(h*u,t) + total(h*u*u+g*h*h/2,x) + total(h*u*v,y) + g*h*jets[b,x],
        total(h*v,t) + total(h*u*v,x) + total(h*v*v+g*h*h/2,y) + g*h*jets[b,y],
        E[3],
    ])
    return dict(base=base, fields=fields, jets=jets, g=g, K=K, m=m,
                total=total, E=E, conservative=conservative, divq=divq)


def prolong(model, xi, eta):
    """First point prolongation, with every jet coefficient from the chain rule."""
    fields, base, jets, total = (model[k] for k in ("fields","base","jets","total"))
    prolonged = {}
    for f, ef in zip(fields, eta):
        for z in base:
            prolonged[jets[f,z]] = total(ef,z) - sum(
                jets[f,q]*total(xq,z) for q,xq in zip(base,xi))
    values = []
    for E in model["E"]:
        values.append(sum(a*s.diff(E,z) for a,z in zip(xi,base))
                      + sum(a*s.diff(E,f) for a,f in zip(eta,fields))
                      + sum(a*s.diff(E,j) for j,a in prolonged.items()))
    return s.Matrix(values)


def symmetry_checks():
    model = jet_model()
    t,x,y = model["base"]
    h,u,v,b = model["fields"]
    E,K,m = model["E"],model["K"],model["m"]
    Z = (0,0,0,0)
    checks = {}
    for label,xi,eta,target in [
        ("time_translation",(1,0,0),Z,s.zeros(4,1)),
        ("x_translation",(0,1,0),Z,s.zeros(4,1)),
        ("y_translation",(0,0,1),Z,s.zeros(4,1)),
        ("bed_datum_shift",(0,0,0),(0,0,0,1),s.zeros(4,1)),
        ("rotation",(0,-y,x),(0,-v,u,0),s.Matrix([0,-E[2],E[1],0])),
        ("common_spacetime_scaling",(t,x,y),Z,-E),
    ]:
        checks[label] = zero_list(prolong(model,xi,eta)-target)
    Dpr = prolong(model,(0,x,y),(2*h,u,v,2*b))
    Ddefect = Dpr-s.diag(2,1,1,2)*E
    checks["cubic_scaling_defect_formula"] = zero_list(
        Ddefect-s.Matrix([0,0,0,(m-3)*K*model["divq"]]))
    checks["cubic_scaling_at_m3"] = zero_list(Ddefect.subs(m,3))
    checks["conservative_primitive_equivalence"] = zero_list(
        model["conservative"]-s.Matrix([E[0],u*E[0]+h*E[1],v*E[0]+h*E[2],E[3]]))

    # Restricted diagonal determining equations. They are not a full classification.
    a,c,d,e,k = s.symbols("a c d e k", real=True)
    weights = [c-k+a, d-2*c, e-d, d-a-m*c+k]
    reduced = clean(weights[-1].subs({d:2*c,k:c+a}))
    checks["diagonal_scaling_stratum"] = [clean(reduced-(3-m)*c)]

    cubic = jet_model(3)
    tc,xc,yc = cubic["base"]
    hc,uc,vc,bc = cubic["fields"]
    jets = cubic["jets"]
    zero_jets = {j:0 for j in jets.values()}
    boost = prolong(cubic,(0,tc,0),(0,1,0,0))[3]
    boost_witness = clean(boost.subs({**zero_jets,jets[bc,xc]:1}))
    rotation_without_velocity = prolong(cubic,(0,-yc,xc),Z)
    rotation_witness = clean(rotation_without_velocity[0].subs(
        {**zero_jets,hc:1,uc:1,vc:0,jets[hc,yc]:1}))
    noncubic = clean(Ddefect[3].subs(m,2).subs(
        {**{j:0 for j in model["jets"].values()},u:1,v:0,model["jets"][u,x]:1,K:1}))
    return dict(
        exact_checks=checks,
        diagonal_weights=weights,
        diagonal_solution="c=k-a, d=e=2*(k-a), (3-m)*(k-a)=0",
        cubic_scaling_defect=(m-3)*K*model["divq"],
        negative_controls=dict(galilean_boost=boost_witness,
            rotation_without_velocity=rotation_witness,noncubic_scaling_m2=noncubic),
    )


def radial_checks():
    """Pull back Cartesian differential operators; retain angular velocity."""
    t,r,theta = s.symbols("t r theta", real=True, positive=True)
    g,K = s.symbols("g K", positive=True)
    h,a,w,b,f = [s.Function(n)(t,r) for n in ("h","a","w","b","f")]
    c,ss = s.cos(theta),s.sin(theta)
    u,v = c*a-ss*w,ss*a+c*w
    Dx = lambda z: c*s.diff(z,r)-ss*s.diff(z,theta)/r
    Dy = lambda z: ss*s.diff(z,r)+c*s.diff(z,theta)/r
    div = lambda qx,qy: s.trigsimp(s.expand(Dx(qx)+Dy(qy)))
    Eu = s.diff(u,t)+u*Dx(u)+v*Dy(u)+g*Dx(h+b)
    Ev = s.diff(v,t)+u*Dx(v)+v*Dy(v)+g*Dy(h+b)
    radial = [
        s.diff(h,t)+s.diff(r*h*a,r)/r,
        s.diff(a,t)+a*s.diff(a,r)-w*w/r+g*s.diff(h+b,r),
        s.diff(w,t)+a*s.diff(w,r)+a*w/r,
        s.diff(b,t)+K*s.diff(r*f*a,r)/r,
    ]
    pulled = [s.diff(h,t)+div(h*u,h*v),s.trigsimp(s.expand(c*Eu+ss*Ev)),
              s.trigsimp(s.expand(-ss*Eu+c*Ev)),s.diff(b,t)+K*div(f*u,f*v)]
    checks = {"radial_pullback":zero_list(s.Matrix(pulled)-s.Matrix(radial)),
              "speed_is_rotation_invariant":[s.trigsimp(u*u+v*v-a*a-w*w)]}
    # f is arbitrary here, so this identity includes f=(a²+w²)^((m-1)/2).
    return dict(exact_checks=checks,radial_equations=radial,
                sediment_factor="f=(a(t,r)**2+w(t,r)**2)**((m-1)/2)",
                missing_geometry_witness=clean((radial[0]-s.diff(h,t)-s.diff(h*a,r)).subs({h:1,a:1,r:1})))


def cubic_checks():
    t,x,y = s.symbols("t x y", real=True)
    r = s.Symbol("r", positive=True)
    g,K = s.symbols("g K", positive=True)
    b0 = s.Symbol("b0", real=True)
    H,A,W,B = [s.Function(n)(t) for n in ("H","A","W","B")]
    r2 = x*x+y*y
    h,u,v,b = H*r2,A*x-W*y,W*x+A*y,B*r2+b0
    speed2 = s.expand(u*u+v*v)
    E = [s.diff(h,t)+s.diff(h*u,x)+s.diff(h*v,y),
         s.diff(u,t)+u*s.diff(u,x)+v*s.diff(u,y)+g*s.diff(h+b,x),
         s.diff(v,t)+u*s.diff(v,x)+v*s.diff(v,y)+g*s.diff(h+b,y),
         s.diff(b,t)+K*(s.diff(speed2*u,x)+s.diff(speed2*v,y))]
    profile = s.Matrix([s.diff(H,t)+4*A*H,
         s.diff(A,t)+A*A-W*W+2*g*(H+B),s.diff(W,t)+2*A*W,
         s.diff(B,t)+4*K*A*(A*A+W*W)])
    targets = [r2*profile[0],x*profile[1]-y*profile[2],
               y*profile[1]+x*profile[2],r2*profile[3]]
    derivatives = dict(zip([s.diff(z,t) for z in (H,A,W,B)],
                           [-4*A*H,W*W-A*A-2*g*(H+B),-2*A*W,-4*K*A*(A*A+W*W)]))
    invariant = W*W/H
    Rxy,Dxy = s.Matrix([-y,x]),s.Matrix([x,y])
    bracket = Dxy.jacobian([x,y])*Rxy-Rxy.jacobian([x,y])*Dxy
    checks = {"cartesian_cubic_factorization":zero_list(s.Matrix(E)-s.Matrix(targets)),
              "cartesian_cubic_on_ode":zero_list(s.Matrix(E).subs(derivatives)),
              "swirl_first_integral":[clean(s.diff(invariant,t).subs(derivatives))],
              "rotation_scaling_base_bracket":zero_list(bracket),
              "projected_rank_determinant":[clean(s.Matrix.hstack(Rxy,Dxy).det()+r2)]}
    # Annular mass/solid-bed balance, exact for boundary traces of this solution.
    ri,ro,p = s.symbols("ri ro p", real=True, positive=True)
    water_mass = s.pi*(ro**4-ri**4)*H/2
    water_net = 2*s.pi*A*H*(ro**4-ri**4)
    solid_bed = (1-p)*s.pi*(ro**4-ri**4)*B/2
    sediment_net = 2*s.pi*(1-p)*K*A*(A*A+W*W)*(ro**4-ri**4)
    checks["annular_water_balance"]=[clean((s.diff(water_mass,t)+water_net).subs(derivatives))]
    checks["annular_solid_bed_balance"]=[clean((s.diff(solid_bed,t)+sediment_net).subs(derivatives))]
    rotation_Q=[-y*s.diff(z,x)+x*s.diff(z,y) for z in (h,u,v,b)]
    checks["rotation_graph_invariance"]=zero_list(s.Matrix([0,-v,u,0])-s.Matrix(rotation_Q))
    scaling_Q=[x*s.diff(z,x)+y*s.diff(z,y) for z in (h,u,v,b)]
    checks["shifted_scaling_graph_invariance"]=zero_list(
        s.Matrix([2*h,u,v,2*(b-b0)])-s.Matrix(scaling_Q))
    omega=s.Symbol('omega',real=True)
    cstar=omega**2+s.Rational(1,4)
    exact_values={H:cstar*(1/(2*g)-K)/t**2,A:1/(2*t),W:omega/t,B:K*cstar/t**2}
    exact_derivatives={s.diff(z,t):s.diff(expr,t) for z,expr in exact_values.items()}
    checks["exact_evolving_swirl_cartesian"]=zero_list(
        s.Matrix(E).subs(exact_derivatives).subs(exact_values))
    # The 2D factor 4 must not silently become the 1D factor 3.
    wrong = dict(derivatives)
    wrong[s.diff(H,t)]=-3*A*H
    missing_factor_witness=clean(E[0].subs(wrong).subs({x:1,y:0,H:1,A:1}))
    return dict(exact_checks=checks,profile_residuals=list(profile),
                cartesian_fields=[h,u,v,b],first_integral=invariant,
                exact_time_family={str(z):expr for z,expr in exact_values.items()},
                exact_time_family_guards=['t>0','r>0','2*g*K<1','g,K>0','omega real'],
                missing_factor_witness=missing_factor_witness,
                noncubic_bed_residual="r**2*Bprime + K*(m+1)*A*(A**2+W**2)**((m-1)/2)*r**(m-1)")


def numerical_example(out):
    """Dimensionless IVP; two solver implementations and sampled diagnostics."""
    g,kappa,p = 1.0,0.03,0.4
    K = kappa/(1-p)
    initial = np.array([1.0,0.15,0.2,0.05])
    def rhs(t,z):
        H,A,W,B=z
        return [-4*A*H,W*W-A*A-2*g*(H+B),-2*A*W,-4*K*A*(A*A+W*W)]
    def depth_guard(t,z):
        return z[0]-0.1
    depth_guard.terminal=True
    depth_guard.direction=-1
    def magnitude_guard(t,z):
        return 10.0-np.max(np.abs(z))
    magnitude_guard.terminal=True
    magnitude_guard.direction=-1
    grid=np.linspace(0.0,0.2,201)
    settings=[("DOP853",1e-8,1e-10,0.1),("DOP853",1e-12,1e-14,0.01),
              ("Radau",1e-11,1e-13,0.01)]
    solutions=[]
    runs=[]
    for method,rtol,atol,max_step in settings:
        start=time.perf_counter()
        sol=solve_ivp(rhs,(grid[0],grid[-1]),initial,method=method,rtol=rtol,
                      atol=atol,t_eval=grid,events=[depth_guard,magnitude_guard],max_step=max_step)
        full=bool(sol.success and sol.t.size==grid.size and sol.t[-1]==grid[-1])
        if not full or not np.isfinite(sol.y).all():
            raise RuntimeError(f"IVP guard/failure: {method}: {sol.message}")
        solutions.append(sol.y)
        runs.append(dict(method=method,rtol=rtol,atol=atol,max_step=max_step,nfev=sol.nfev,
                         seconds=time.perf_counter()-start,success=full))
    reference=solutions[1]
    csv_path=out/'profiles.csv'
    with csv_path.open('w',newline='',encoding='utf-8') as stream:
        writer=csv.writer(stream)
        writer.writerow(['t','H','A','W','B'])
        writer.writerows(zip(grid,*reference))
    H,A,W,B=reference
    invariant=W*W/H
    # Time derivatives here use independent finite differences of solver samples,
    # not substitution of the same RHS used by the integrator.
    def fd_defect(step):
        zz=reference[:,::step]
        tt=grid[::step]
        dz=(zz[:,2:]-zz[:,:-2])/(tt[2:]-tt[:-2])
        f=np.array([rhs(0,z) for z in zz[:,1:-1].T]).T
        return float(np.max(np.abs(dz-f)))
    fine,coarse=fd_defect(1),fd_defect(2)
    # A separate integration starts on an exactly known evolving solution.
    exact_grid=np.linspace(1.0,1.2,101)
    exact_amplitude=np.array([1.25*(1/(2*g)-K),0.5,1.0,1.25*K])
    exact_target=exact_amplitude[:,None]/exact_grid[None,:]**np.array([2,1,1,2])[:,None]
    exact_sol=solve_ivp(rhs,(1.0,1.2),exact_amplitude,method='DOP853',
                        rtol=1e-12,atol=1e-14,t_eval=exact_grid,max_step=0.01)
    if not exact_sol.success or exact_sol.y.shape!=exact_target.shape:
        raise RuntimeError('Exact-control integration failed')
    exact_error=float(np.max(np.abs(exact_sol.y-exact_target)))
    summary=dict(label='constructed dimensionless rotating cubic IVP',g=g,kappa=kappa,p=p,K=K,m=3,
        initial=dict(zip(['H','A','W','B'],initial.tolist())),interval=[0.0,0.2],samples=len(grid),
        spatial_chart='1 <= r <= 2; periodic theta; boundary values/fluxes are solution traces',
        runs=runs,refinement_max_abs=float(np.max(np.abs(solutions[0]-reference))),
        cross_solver_max_abs=float(np.max(np.abs(solutions[2]-reference))),
        first_integral_max_abs_drift=float(np.max(np.abs(invariant-invariant[0]))),
        H_min=float(H.min()),speed_on_r1_min=float(np.sqrt(A*A+W*W).min()),
        finite_difference_defect_fine=fine,finite_difference_defect_coarse=coarse,
        finite_difference_ratio=coarse/fine,final_state=reference[:,-1].tolist(),
        exact_control=dict(interval=[1.0,1.2],omega=1.0,initial=exact_amplitude.tolist(),
                           max_abs_error=exact_error,method='DOP853',rtol=1e-12,atol=1e-14),
        thresholds=dict(cross_solver=1e-8,refinement=1e-8,first_integral=1e-9,exact_control=1e-9),
        sample_sha256=hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        limitations=['sampled numerical consistency, not a continuous error certificate',
            'constructed data, not measured or source-paper data',
            'ODE reference, not a full 2D PDE-solver comparison'])
    summary['passed']=bool(summary['cross_solver_max_abs']<1e-8 and
        summary['refinement_max_abs']<1e-8 and summary['first_integral_max_abs_drift']<1e-9
        and summary['H_min']>0 and summary['speed_on_r1_min']>0 and exact_error<1e-9)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,2,figsize=(8,5),layout='constrained')
    for ax,label,values in zip(axes.flat,['H: depth coefficient','A: radial coefficient',
                                        'W: swirl coefficient','B: bed coefficient'],reference):
        ax.plot(grid,values,color='#246b8e',lw=1.8)
        ax.set(xlabel='dimensionless time',ylabel=label)
        ax.grid(alpha=.2)
    fig.suptitle('Constructed cubic 2D SVE invariant family')
    fig.savefig(out/'profiles.png',dpi=180)
    plt.close(fig)
    def tex_number(value):
        mantissa,exponent=f'{value:.3e}'.split('e')
        return rf'${mantissa}\times10^{{{int(exponent)}}}$'
    rows=[('DOP853/Radau maximum difference',summary['cross_solver_max_abs']),
          ('DOP853 step/tolerance comparison',summary['refinement_max_abs']),
          ('Maximum drift of $W^2/H$',summary['first_integral_max_abs_drift']),
          ('Exact-family numerical error',exact_error),
          ('Minimum sampled $H$',summary['H_min']),
          ('Minimum sampled speed at $r=1$',summary['speed_on_r1_min']),
          ('Fine centered-difference ODE defect',fine),
          ('Coarse/fine defect ratio',coarse/fine)]
    table=['\\begin{center}','\\begin{tabular}{ll}','\\toprule',
           'Diagnostic & Measured value \\\\', '\\midrule']
    table.extend(label+' & '+tex_number(value)+r' \\' for label,value in rows)
    table.extend(['\\bottomrule','\\end{tabular}','\\end{center}'])
    (out/'numerical_table.tex').write_text('\n'.join(table)+'\n',encoding='utf-8')
    return summary


def serialize(obj):
    if isinstance(obj,s.Basic):
        return str(obj)
    raise TypeError(type(obj).__name__)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=HERE/'results')
    parser.add_argument('--symbolic-only',action='store_true')
    args=parser.parse_args(argv)
    out=args.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    groups=dict(symmetry=symmetry_checks(),radial=radial_checks(),cubic=cubic_checks())
    failures=[]
    exact_count=0
    for group,records in groups.items():
        for name,residuals in records['exact_checks'].items():
            exact_count+=len(residuals)
            if any(z!=0 for z in residuals):
                failures.append(f'{group}.{name}')
            print(f'{group}.{name}: {residuals}',flush=True)
    negatives={**groups['symmetry']['negative_controls'],
               'missing_radial_geometry':groups['radial']['missing_geometry_witness'],
               'using_1d_factor_in_2d':groups['cubic']['missing_factor_witness']}
    if any(clean(z)==0 for z in negatives.values()):
        failures.append('negative_control_not_detected')
    print('Negative controls (must be nonzero):',negatives,flush=True)
    numerical=None if args.symbolic_only else numerical_example(out)
    if numerical is not None and not numerical['passed']:
        failures.append('numerical_gate')
    evidence=dict(schema_version=1,status='passed' if not failures else 'failed',
        created_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        environment=dict(python=platform.python_version(),sympy=s.__version__,numpy=np.__version__,
                         scipy=scipy.__version__,thread_cap=1),
        assumptions=['smooth classical fields','h>0','g>0','kappa>0','0<=p<1',
          'K=kappa/(1-p)','speed>0 for arbitrary real m','polar chart r>0',
          'source Grass range 1<=m<=4; other real exponents are mathematical extensions',
          'g,kappa,p fixed under symmetry transformations','no friction or external forcing'],
        exact_zero_count=exact_count,groups=groups,negative_controls=negatives,
        numerical=numerical,failures=failures,elapsed_seconds=time.perf_counter()-start,
        claim_scope='verified candidates and diagonal-scaling stratum, not maximal classification')
    (out/'evidence.json').write_text(json.dumps(evidence,indent=2,default=serialize)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=evidence['status'],exact_zero_count=exact_count,
                         numerical=numerical,seconds=evidence['elapsed_seconds']),indent=2))
    return int(bool(failures))


if __name__=='__main__':
    raise SystemExit(main())
