"""Classical references and analytical Taylor front end on a regular chart."""
from functools import lru_cache
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from .jets import g,kappa,m
from .symbolic import z,f,P,C,normal_form

@lru_cache(maxsize=2)
def functions(physical=False):
    G,L=normal_form(m,physical)
    G4=sp.diff(G,z)+P*sp.diff(G,f)+C*sp.diff(G,P)+G*sp.diff(G,C)
    args=(z,f,P,C,m,g,kappa)
    return tuple(sp.lambdify(args,e,'numpy',cse=True) for e in (G,L,G4))

def reference(exponent,physical=False,initial=(2.,.5,.1),interval=(1.,1.4),
              gravity=1.,transport=1./30.,rtol=1e-11,atol=1e-13):
    G,L,_=functions(physical)
    def rhs(x,v):
        if v[1]<=0 or v[0]-x*v[1]<=0:
            raise ValueError('Reference left the positive real branch')
        leading=L(x,*v,exponent,gravity,transport)
        if abs(leading)<1e-9:
            raise ValueError('Reference approached a singular leading coefficient')
        return [v[1],v[2],G(x,*v,exponent,gravity,transport)]
    sol=solve_ivp(rhs,interval,initial,method='DOP853',rtol=rtol,atol=atol,
                  dense_output=True,max_step=.02)
    if not sol.success: raise RuntimeError(sol.message)
    grid=np.linspace(*interval,401)
    vals=sol.sol(grid)
    guards={'min_phi_s':float(vals[1].min()),
            'min_phi_t':float((vals[0]-grid*vals[1]).min()),
            'min_abs_leading':float(np.abs(L(grid,*vals,exponent,gravity,transport)).min())}
    return sol,guards

def taylor(exponent,physical=False,order=4,initial=(2.,.5,.1),z0=1.,
           gravity=1.,transport=1./30.):
    G,_,G4=functions(physical)
    derivatives=list(initial)
    if order>=3: derivatives.append(float(G(z0,*initial,exponent,gravity,transport)))
    if order>=4: derivatives.append(float(G4(z0,*initial,exponent,gravity,transport)))
    if order not in (2,3,4):raise ValueError('Implemented Taylor orders: 2,3,4')
    from math import factorial
    return np.array([v/factorial(i) for i,v in enumerate(derivatives[:order+1])])

def integrated_reference(exponent,physical=False,initial=(2.,.5,.1),
                         interval=(1.,1.4),gravity=1.,transport=1./30.):
    """Independent second-order solve plus local bed reconstruction."""
    _,L,_=functions(physical)
    I0=float(initial[2]*L(interval[0],*initial,exponent,gravity,transport))
    def rhs(x,v):
        F,fp,bed=v
        leading=L(x,F,fp,0.,exponent,gravity,transport)
        fpp=I0/leading
        A=fpp*(x*x*fp-gravity/fp**2)
        return [fp,fpp,-A/gravity]
    sol=solve_ivp(rhs,interval,[initial[0],initial[1],0.],method='DOP853',
                  rtol=1e-11,atol=1e-13,dense_output=True,max_step=.02)
    if not sol.success:raise RuntimeError(sol.message)
    return sol,I0
