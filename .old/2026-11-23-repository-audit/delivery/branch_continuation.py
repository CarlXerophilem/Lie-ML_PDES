"""LieSolver-inspired research control on the common P–M scaling chart.

Uses a verified reduced solution as a continuation seed. It integrates a
tangent IVP in the correction weight and compares the predictor with a direct
solve for the target. The weight is an equation parameter, never a symmetry
parameter. This routine is confined to a regular positive branch.
"""
import argparse
import json

import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp


def build_fields():
    z,F,p,m,lam=sp.symbols("z F p m lambda", real=True)
    U=F-z*p
    base=-z**3*p+z/p**2+(m/30)*z*U**(m-1)/p
    delta=U*(1/p**3-z**2)
    L=base+lam*delta
    state=sp.Matrix([p, sp.Rational(1,40)/L])
    args=(z,F,p,m,lam)
    return tuple(sp.lambdify(args,f,"numpy") for f in
                 (state,state.jacobian([F,p]),state.diff(lam),L))


def run(exponent, step):
    if not np.isfinite(exponent) or exponent<1 or not 0<step<=1:
        raise ValueError("Require finite m>=1 and a continuation step in (0,1]")
    fun,jac,weight,leading=build_fields()
    grid=np.linspace(.8,.9,101)
    initial=[2.,1.]
    def check(z,values,lam):
        if values[1]<=0 or values[0]-z*values[1]<=0:
            raise ArithmeticError("Positive material chart boundary")
        if not np.isfinite(leading(z,*values,exponent,lam)) or abs(
                leading(z,*values,exponent,lam))<1e-5:
            raise ArithmeticError("Leading coefficient too small for this chart")
    def solve(lam,with_tangent):
        def rhs(z,Y):
            values=Y[:2]
            check(z,values,lam)
            args=(z,*values,exponent,lam)
            slope=fun(*args).ravel()
            if not with_tangent:
                return slope
            return np.r_[slope,jac(*args)@Y[2:]+weight(*args).ravel()]
        sol=solve_ivp(rhs,(grid[0],grid[-1]),initial+([0.,0.] if with_tangent else []),
                      method="DOP853",t_eval=grid,rtol=2e-12,atol=2e-14)
        if not sol.success:
            raise ArithmeticError(sol.message)
        return sol.y
    ref=solve(0.,True)
    target=solve(step,False)
    coarse=ref[:2]+step*ref[2:]
    half=solve(step/2,False)
    fine=ref[:2]+step/2*ref[2:]
    err=lambda a,b:float(np.max(np.abs(a-b)))
    return {
        "m":exponent,"weight":step,"frozen_first_integral":.025,
        "direct_seed_error":err(ref[:2],target),
        "tangent_predictor_error":err(coarse,target),
        "half_weight_predictor_error":err(fine,half),
        "sample_min_abs_target_leading":float(np.min(np.abs(
            leading(grid,*target,exponent,step)))),
        "claim":"Numerical regular-chart sensitivity check for fixed traces"
    }


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m",type=float,nargs="+",default=[1.,2.,3.,4.])
    parser.add_argument("--step",type=float,default=.25)
    args=parser.parse_args()
    print(json.dumps([run(m,args.step) for m in args.m],indent=2))
