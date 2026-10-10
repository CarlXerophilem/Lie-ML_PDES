"""Auditable identities, ODEs, and unrestricted first-order obstruction."""
import sympy as sp
from .jets import (t,s,u,p,q,a,b,c,r,w,x,y,g,kappa,m,
                   total,act,model_residual)

z=sp.symbols('z', positive=True)
f,P,C,H=sp.symbols('f P C H', real=True)

def profile_total(expr):
    return sp.diff(expr,z)+P*sp.diff(expr,f)+C*sp.diff(expr,P)+H*sp.diff(expr,C)

def reduced_residual(exponent=m, physical=False):
    V=f-z*P
    A=C*(z**2*P-g/P**2)
    J=z*V**(exponent-1)*C/P
    R=-A-z*profile_total(A)+g*exponent*kappa*profile_total(J)
    if physical:
        R-=profile_total(V*A/P)
    return sp.expand(R)

def normal_form(exponent=m, physical=False):
    R=reduced_residual(exponent,physical)
    leading=sp.diff(R,H)
    rhs=-R.subs(H,0)/leading
    return rhs,leading

def first_integral(exponent=m,physical=False):
    """R = dI/dz; the bed logarithmic drift is I/g."""
    _,leading=normal_form(exponent,physical)
    return sp.factor(leading*C)

def obstruction(physical=False):
    """Necessary tangency condition with arbitrary smooth point coefficients.

    On q>0 solve the equation for r=phi_ttt. Multiply the x=phi_tss
    coefficient by q**3 to obtain a polynomial in the freely varying p,q.
    Its p**2*q**2 coefficient is a nonzero scalar, independent of ALL
    derivatives of the unrestricted point-generator coefficients.
    """
    tau=sp.Function('tau')(t,s,u)
    xi=sp.Function('xi')(t,s,u)
    eta=sp.Function('eta')(t,s,u)
    E=model_residual(3,physical)
    forcing=3*g*kappa*total(p**2*b/q,1)
    shell=-E.subs(r,0)/q
    tangency=sp.expand((act(E,tau,xi,eta)+forcing).subs(r,shell))
    highest=sp.expand(q**3*sp.diff(tangency,x))
    poly=sp.Poly(highest,p,q)
    witness=sp.factor(poly.coeff_monomial(p**2*q**2))
    return {'model':'physical_corrected' if physical else 'printed',
            'shell':shell,'highest_polynomial':poly.as_expr(),
            'witness':witness,'tangency':tangency}

def direct_pullback(exponent,physical=False):
    """Independent direct chain rule in (t,s), for polynomial equality tests."""
    F=sp.Function('F')
    phi=t*F(s/t)
    A=sp.diff(phi,s)*sp.diff(phi,t,2)-g*sp.diff(phi,s,2)/sp.diff(phi,s)**2
    E=sp.diff(A,t)-g*exponent*kappa*sp.diff(
        sp.diff(phi,t)**(exponent-1)*sp.diff(phi,t,s)/sp.diff(phi,s),s)
    if physical:
        E-=sp.diff(sp.diff(phi,t)*A/sp.diff(phi,s),s)
    pulled=sp.expand((t**2*E).subs(s,t*z).doit())
    return pulled.xreplace({F(z):f,sp.diff(F(z),z):P,
                           sp.diff(F(z),z,2):C,sp.diff(F(z),z,3):H})

def physical_audit():
    """Compatibility of the reconstructed bed derivatives, not a closure guess."""
    A=q*a-g*c/q**2
    bs=-A/g
    bt=p*bs/q-m*kappa*p**(m-1)*b/q
    compatibility=sp.expand(g*(total(bt,1)-total(bs,0)))
    return compatibility, model_residual(m,True)
