"""2026 printed m=1 scalar and compatible m=2 material travelling wave."""
import numpy as np
from _profile_learning import Case, cli


def printed_exact(t,p):
    return (.5*(t-1)+p*(t*np.log(t)-t+1), .5+p*np.log(t),p/t,-p/t**2)


def printed_taylor(n,p,z0,trace):
    return [trace[0],trace[1]]+[p*(-1)**k/(z0**(k-1)*k*(k-1)) for k in range(2,n+1)]


PRINTED=Case("2026 P at m=1",1.,(.6,1.),2,(0.,0.,lambda t:t),
             lambda z,p:p,lambda p:(0.,.5),printed_taylor,printed_exact,
             lambda z,jets:np.stack((1.25*z+jets[0],)),
             lambda z,jets,p:jets[2]+z*jets[3])


def material_exact(z,p):
    return p+.2*z,np.full_like(z,.2),np.zeros_like(z),np.zeros_like(z)


def material_fields(z,jets):
    # c=-1, m=2, beta=1/10, g=1, t=1/2, b0=3.
    velocity=jets[0]
    if np.any(velocity<=0):
        raise ValueError("Require positive material gradient")
    depth=1/velocity
    bed=3-depth-velocity**2/2-.01
    return np.stack((depth,velocity,bed))


def material_residual(z,jets,p):
    # General lift uses bed drift -beta*k. Its bed residual is beta*(u_z-k).
    return .1*(jets[1]-.2)


MATERIAL=Case("2026 M to E1 at m=2",0.,(1.,1.4),1,(0.,1.),
              lambda z,p:.2,lambda p:(p,),
              lambda n,p,z0,trace:[trace[0],.2],material_exact,
              material_fields,material_residual)

def material_laurent_profile(sigma, w0, g, offset=0., degree=6):
    """Evaluate the proven m=3, g*beta=3/4 branch and its analytic tail."""
    from reproduce_sve2026 import cubic_material_laurent
    from numpy.polynomial.polynomial import polyval

    sigma=np.asarray(sigma,dtype=float)
    if not (np.all(np.isfinite(sigma)) and np.all(sigma>0) and
            np.isfinite(w0) and w0>0 and np.isfinite(g) and g>0 and
            np.isfinite(offset) and type(degree) is int and 1<=degree<=8):
        raise ValueError("Require a positive finite chart and 1<=degree<=8")
    xi=g*sigma**4/w0**3
    q=4*xi
    if np.any(q>=1):
        raise ValueError("No convergence certificate on this chart")
    coeff=cubic_material_laurent(degree)
    position=polyval(xi,np.array(coeff["F_coefficients_in_w_over_sigma"],float))
    gradient=polyval(xi,np.array(coeff["Y"],float))
    magnitude=17*q**(degree+1)/(16*(1-q))
    return {
        "position":offset+w0*position/sigma,
        "gradient":w0*gradient/sigma**2,
        "position_tail":w0*magnitude/(sigma*(4*degree+3)),
        "gradient_tail":w0*magnitude/sigma**2,
    }


if __name__=="__main__":
    cli((PRINTED,MATERIAL))
