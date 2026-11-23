"""2022 Eulerian bed drift at m=2, g=1, K=1/2."""
import numpy as np
from _profile_learning import Case, cli


def exact(x,p):
    return p-x/2,np.full_like(x,-.5),np.zeros_like(x),np.zeros_like(x)


def fields(x,jets):
    Y=jets[0]
    if np.any(Y<=0):
        raise ValueError("Require positive Y=u^2")
    u=np.sqrt(Y)
    h=1/u
    B=.5/4+2-Y/2-h
    return np.stack((h,u,B))


def residual(x,jets,p):
    return .5*jets[1]+.25


CASE=Case("2022 E1",0.,(1.,1.4),1,(0.,.5),
          lambda z,p:-.25,lambda p:(p,),
          lambda n,p,z0,trace:[trace[0],-.5],
          exact,fields,residual)

if __name__=="__main__":
    cli((CASE,))
