#!/usr/bin/env python3
"""Symbolic SVE-informed reduction and non-neural ODE reference.

Run: python base_LieReduct.py --out results
Install: python -m pip install numpy scipy sympy matplotlib pillow

Scope: the scalar master equation in main.tex, NOT a verified elimination of
the full Eulerian Saint--Venant--Exner system. Coordinate transformation and
Lie reduction are different operations. The full-system coordinate identities
are exported for inspection, but only the scalar benchmark is solved here.
No universal 'best' Lie classifier exists; X5 is verified, not guessed.
Reference: https://doi.org/10.3390/math14030433
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path
import json
import time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


@dataclass
class Problem:
    # Dimensionless verification fixture. beta=1/8 makes 1-4*g*beta positive.
    # These are exposed benchmark choices, not calibrated physical constants.
    g: float = 1.0
    beta: float = 0.125
    t0: float = 1.0
    t1: float = 1.2
    s0: float = 1.0
    s1: float = 1.2
    nt: int = 25
    ns: int = 65

    def validate(self):
        if not (self.g > 0 and 0 < self.beta < 1 / (4*self.g)):
            raise ValueError('Exact positive branch requires g>0 and 0<g*beta<1/4.')
        if not (0 < self.t0 < self.t1 and 0 < self.s0 < self.s1):
            raise ValueError('Require positive, increasing time and label intervals.')
        if self.nt < 3 or self.ns < 3:
            raise ValueError('At least three grid points per axis are needed.')
        return self

    @property
    def c(self):
        return (27*self.g / (1-4*self.g*self.beta))**(1/3)

    @property
    def sigma0(self):
        return self.s0*self.t0**2

    @property
    def sigma1(self):
        return self.s1*self.t1**2

    def grid(self):
        return np.meshgrid(np.linspace(self.t0,self.t1,self.nt),
                           np.linspace(self.s0,self.s1,self.ns), indexing='ij')


def problem_arguments(parser):
    for key in ('g','beta','t0','t1','s0','s1'):
        parser.add_argument('--'+key, type=float, default=getattr(Problem(),key))
    parser.add_argument('--nt',type=int,default=25)
    parser.add_argument('--ns',type=int,default=65)
    parser.add_argument('--out',type=Path,default=Path('results'))
    parser.add_argument('--coordinates',choices=['lagrangian','eulerian'],default='lagrangian')
    parser.add_argument('--no-scene',action='store_true',help='Save arrays but skip HTML/PNG.')


def problem_from_args(args):
    return Problem(**{k:getattr(args,k) for k in asdict(Problem())}).validate()


@lru_cache(maxsize=1)
def symbolic_model():
    t,s,z,g,b=sp.symbols('t s sigma g beta', positive=True)
    F=sp.Function('F')(z)
    p,q,r=[sp.diff(F,z,k) for k in (1,2,3)]
    A=2*z*p**2+4*z**2*p*q-g*q/p**2
    B=8*z**2*p*(p+z*q)
    R=sp.expand(2*z*sp.diff(A,z)-g*b*sp.diff(B,z))
    rhs=sp.solve(R,r)[0]
    phi=sp.Function('F')(s*t**2)
    def equation(v):
        return sp.diff(sp.diff(v,s)*sp.diff(v,t,2)-g*sp.diff(v,s,2)/sp.diff(v,s)**2,t)-g*b*sp.diff(sp.diff(v,t)**2*sp.diff(v,t,s)/sp.diff(v,s),s)
    assert sp.simplify(equation(phi)-R.subs(z,s*t**2)/t)==0
    # Independent exact solution check with symbolic amplitude.
    c=sp.symbols('c',positive=True)
    exact=c*(s*t**2)**sp.Rational(1,3)
    defect=sp.simplify(equation(exact))
    assert sp.simplify(defect.subs(b,(1-27*g/c**3)/(4*g)))==0
    # Infinitesimal criterion for X5: derivative weights under t->e^a t,
    # s->e^-2a s. All terms must have weight -1.
    jets=sp.symbols('ps pt pss pts ptt psst ptts pttt')
    ps,pt,pss,pts,ptt,psst,ptts,pttt=jets
    E=pts*ptt+ps*pttt-g*(psst/ps**2-2*pss*pts/ps**3)-g*b*(2*pt*pts**2/ps+pt**2*psst/ps-pt**2*pts*pss/ps**2)
    weights=(2,-1,4,1,-2,3,0,-3)
    assert sp.simplify(sum(w*j*sp.diff(E,j) for w,j in zip(weights,jets))+E)==0
    assert sp.simplify(t*sp.diff(s*t*t,t)-2*s*sp.diff(s*t*t,s))==0
    # The material-coordinate map solves Eulerian mass conservation identically.
    position=sp.Function('phi')(t,s)
    jac=sp.diff(position,s);velocity=sp.diff(position,t);depth=1/jac
    mass=sp.diff(depth,t)-velocity/jac*sp.diff(depth,s)+sp.diff(depth*velocity,s)/jac
    assert sp.simplify(mass)==0
    pp,qq=sp.symbols('p q')
    rhs_numeric=sp.lambdify((z,pp,qq,g,b),rhs.subs({p:pp,q:qq}),'numpy')
    return {'R':R,'rhs':rhs,'rhs_numeric':rhs_numeric,'F':F,'sigma':z,
            'g':g,'beta':b,'E_jets':E,'verified':True}


def write_equations(out,problem):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    m=symbolic_model()
    content = '''SCALAR BENCHMARK (m=3)
E = Dt(phi_s phi_tt - g phi_ss/phi_s^2) - g beta Ds(phi_t^2 phi_ts/phi_s) = 0
X5 = t d/dt - 2s d/ds
S5(a): (t,s,phi) -> (exp(a)t,exp(-2a)s,phi)
Invariant sigma=s*t^2; invariant field phi=F(sigma); E=R[F]/t.

FULL SVE COORDINATE TRANSFORM (identities, not the solved scalar model)
Eulerian: h_t+(h*v)_x=0; v_t+v*v_x+g*(h+b)_x=0;
           b_t+beta*v^(m-1)*v_x=0.
Lagrangian: x=phi(t,s), y=phi_s, h=1/y, v=phi_t;
           y_t-v_s=0; v_t+(g/y)*(1/y+b)_s=0;
           b_t-(v/y)*b_s+(beta/y)*v^(m-1)*v_s=0.
Operators: d_x=(1/phi_s)*D_s; d_t|x=D_t-(phi_t/phi_s)*D_s.
The convective bed term cannot be omitted silently. No bed is reconstructed.

R[F] = '''+str(m['R'])+'\nFthird = '+str(m['rhs'])
    (out/'equations.txt').write_text(content,encoding='utf-8')
    (out/'equations.tex').write_text('\\[ '+sp.latex(m['R'])+'=0 \\]\n',encoding='utf-8')
    (out/'problem.json').write_text(json.dumps(asdict(problem),indent=2))


def exact_fields(problem,T,S):
    phi=problem.c*(S*T**2)**(1/3)
    return phi,2*phi/(3*T),3*S/phi


def save_result(out,name,problem,phi,v,h,residual,metrics,history=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    T,S=problem.grid(); exact,ev,eh=exact_fields(problem,T,S)
    arrays=[phi,v,h,residual]
    if any(np.shape(a)!=T.shape or not np.all(np.isfinite(a)) for a in arrays):
        raise ValueError('Result contains nonfinite values or incompatible grids.')
    metrics=dict(metrics,method=name,scope='scalar master equation only',m=3,
                 relative_phi_l2=float(np.linalg.norm(phi-exact)/np.linalg.norm(exact)),
                 relative_v_l2=float(np.linalg.norm(v-ev)/np.linalg.norm(ev)),
                 relative_h_l2=float(np.linalg.norm(h-eh)/np.linalg.norm(eh)),
                 pde_residual_rms=float(np.sqrt(np.mean(residual**2))),
                 minimum_phi_s=float(np.min(1/h)),problem=asdict(problem))
    path=out/(name+'.npz')
    np.savez_compressed(path,t=T[:,0],s=S[0],phi=phi,v=v,h=h,residual=residual,
                        exact_phi=exact,exact_v=ev,exact_h=eh,
                        metrics=json.dumps(metrics),history=np.array(history or []))
    (out/(name+'_metrics.json')).write_text(json.dumps(metrics,indent=2))
    print(json.dumps(metrics,indent=2),flush=True)
    return path


def run(args):
    problem=problem_from_args(args);start=time.perf_counter()
    write_equations(args.out,problem)
    model=symbolic_model(); z0=problem.sigma0
    initial=[problem.c*z0**(1/3),problem.c/3*z0**(-2/3),-2*problem.c/9*z0**(-5/3)]
    def fun(z,y):
        if y[1]<=0: raise ValueError('Lost positive Jacobian; stop before singular branch.')
        return [y[1],y[2],float(model['rhs_numeric'](z,y[1],y[2],problem.g,problem.beta))]
    sol=solve_ivp(fun,(z0,problem.sigma1),initial,method='DOP853',
                  rtol=args.rtol,atol=args.rtol*0.01,dense_output=True)
    if not sol.success: raise RuntimeError(sol.message)
    T,S=problem.grid();z=S*T*T; F,p,q=sol.sol(z.ravel()).reshape(3,*T.shape)
    r=model['rhs_numeric'](z,p,q,problem.g,problem.beta)
    # Evaluate the expanded original residual after reconstruction.
    ps=T*T*p;pt=2*z*p/T;pss=T**4*q;pts=2*T*(p+z*q)
    ptt=(2*z*p+4*z*z*q)/T**2
    pttt=(12*z*z*q+8*z**3*r)/T**3
    psst=T**3*(4*q+2*z*r);ptts=2*p+10*z*q+4*z*z*r
    E=pts*ptt+ps*pttt-problem.g*(psst/ps**2-2*pss*pts/ps**3)-problem.g*problem.beta*(2*pt*pts**2/ps+pt**2*psst/ps-pt**2*pts*pss/ps**2)
    save_result(args.out,'LieReduct',problem,F,pt,1/ps,E,
                {'seconds':time.perf_counter()-start,'rtol':args.rtol,
                 'reference':'DOP853 reduced IVP; residual uses the ODE derivative',
                 'symbolic_reduction_verified':True})
    if not args.no_scene:
        from pde_scene import render
        render(args.out,coordinates=args.coordinates)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    problem_arguments(parser)
    parser.add_argument('--rtol',type=float,default=1e-10)
    args=parser.parse_args()
    if args.rtol<=0: parser.error('--rtol must be positive')
    run(args)
