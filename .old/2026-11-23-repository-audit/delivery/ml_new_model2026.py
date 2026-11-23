"""Depth-averaged rotating exchange tank on its exact swirl family."""
from math import factorial
import numpy as np
from _profile_learning import Case, cli


def exact(t,p):
    y=(p-.3)*np.exp(-3*t)
    return .3+y,-3*y,9*y,-27*y


def taylor(n,p,z0,trace):
    return [trace[0]]+[(trace[0]-.3)*(-3)**k/factorial(k) for k in range(1,n+1)]


def fields(t,jets):
    r=1.25
    bed=.1/r**2
    b=jets[0]
    B=bed+b
    A=bed/2+.45-b
    if np.any(B<=0) or np.any(A<=0):
        raise ValueError("Require positive bed and areal load on this test")
    return np.stack((np.full_like(t,1+25*r*r/72-bed),np.full_like(t,r/2),B,A))


CASE=Case("2026 rotating tank",0.,(.08,.20),1,(3.,1.),
          lambda z,p:.9,lambda p:(p,),taylor,exact,fields,
          lambda z,jets,p:jets[1]+3*jets[0]-.9)

if __name__=="__main__":
    cli((CASE,))
