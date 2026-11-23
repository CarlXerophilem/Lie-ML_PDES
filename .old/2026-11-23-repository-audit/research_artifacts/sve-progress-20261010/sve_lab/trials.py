"""Hard-IVP tanh trial functions and independent original-coordinate residuals.

Hidden-layer features are fixed; scipy optimizes output weights only. This
small experiment must not be described as a general deep-PINN comparison.
"""
from math import comb, factorial
import numpy as np

def tanh_derivative(h,n):
    v=np.tanh(h)
    return (v,1-v*v,-2*v+2*v**3,-2+8*v*v-6*v**4)[n]

class Trial:
    def __init__(self,prior,kind='reduced_tanh',seed=17,n_features=12,
                 z0=1.,length=.4):
        self.prior=np.asarray(prior)
        self.kind=kind;self.z0=z0;self.length=length
        self.lift_order=len(prior)
        rng=np.random.default_rng(seed)
        self.az=rng.uniform(-3,3,n_features)
        self.ay=(rng.uniform(-2,2,n_features)/np.log(2)
                 if kind=='direct_tanh' else np.zeros(n_features))
        self.bias=rng.uniform(-1,1,n_features)
        self.n_features=n_features

    def derivative(self,y,z,weights,ny=0,nz=0):
        y,z=np.broadcast_arrays(np.asarray(y),np.asarray(z))
        xx=(z-self.z0)/self.length
        out=np.zeros_like(xx,dtype=float)
        if ny==0:
            for i in range(nz,len(self.prior)):
                out += self.prior[i]*factorial(i)/factorial(i-nz)*(z-self.z0)**(i-nz)
        basis=np.zeros(xx.shape+(self.n_features,))
        if self.kind=='reduced_chebyshev':
            if ny:return out
            from numpy.polynomial import Polynomial,Chebyshev
            lift=Polynomial([0]*self.lift_order+[1])
            for j in range(self.n_features):
                pol=Chebyshev.basis(j).convert(kind=Polynomial)(Polynomial([-1,2]))*lift
                basis[...,j]=pol.deriv(nz)(xx)/self.length**nz
        else:
            h=xx[...,None]*self.az+y[...,None]*self.ay+self.bias
            for l in range(min(nz,self.lift_order)+1):
                power=self.lift_order-l
                factor=comb(nz,l)*factorial(self.lift_order)/factorial(power)
                basis += (factor*xx[...,None]**power
                   *tanh_derivative(h,ny+nz-l)*self.az**(nz-l)
                   *self.ay**ny/self.length**nz)
        return out+np.einsum('...j,j->...',basis,np.asarray(weights))

    def jets(self,y,z,weights):
        return {(i,j):self.derivative(y,z,weights,i,j)
                for n in range(4) for i in range(n+1) for j in [n-i]}

def original_residual(jets,z,exponent,physical=False,gravity=1.,transport=1./30.,
                      safe_optimization=False):
    """Return t**2 E[phi] for phi=t U(log(t),s/t).

    Derivative formulas here use the original PDE rather than the reduced
    normal form. Only exploratory optimizer iterates can use clipped powers;
    final validation must use the true positive-branch values.
    """
    U=lambda i,j:jets[(i,j)]
    z=np.asarray(z)
    p=U(0,0)+U(1,0)-z*U(0,1)
    q=U(0,1)
    a=U(2,0)+U(1,0)-2*z*U(1,1)+z*z*U(0,2)
    b=U(1,1)-z*U(0,2);c=U(0,2)
    r=(U(3,0)-U(1,0)-3*z*U(2,1)+3*z*U(1,1)
       +3*z*z*U(1,2)-3*z*z*U(0,2)-z**3*U(0,3))
    w=U(2,1)-U(1,1)-2*z*U(1,2)+2*z*U(0,2)+z*z*U(0,3)
    x=U(1,2)-U(0,2)-z*U(0,3);y=U(0,3)
    if safe_optimization:
        pe=np.maximum(p,.05);qe=np.maximum(q,.05)
    else:
        if np.any(p<=0) or np.any(q<=0):raise ValueError('Invalid frozen candidate branch')
        pe,qe=p,q
    flux=gravity*exponent*transport*((exponent-1)*pe**(exponent-2)*b*b/qe
              +pe**(exponent-1)*x/qe-pe**(exponent-1)*b*c/qe**2)
    E=q*r+b*a-gravity*(x/qe**2-2*c*b/qe**3)-flux
    if physical:
        E-=p*w+b*a-gravity*(b*c/qe**3+p*y/qe**3-3*p*c*c/qe**4)
    return E,p,q
