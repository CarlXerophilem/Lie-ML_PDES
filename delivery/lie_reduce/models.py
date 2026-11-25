"""PDE definitions from balances; independent of frozen prolongation implementation."""
import sympy as sp
from .spec import PDESpec
from .jets import JetSpace


def scalar(model, exponent=2):
    t,s,u=sp.symbols('t s phi',real=True)
    g,k=sp.symbols('g kappa',positive=True)
    j=JetSpace((t,s),(u,),3)
    p,q=j.jet(0,1,0),j.jet(0,0,1)
    a,b,c=j.jet(0,2,0),j.jet(0,1,1),j.jet(0,0,2)
    A=q*a-g*c/q**2
    eq=j.D(A,0)-g*j.D(exponent*k*p**(exponent-1)*b/q,1)
    if model=='M': eq-=j.D(p*A/q,1)
    elif model!='P': raise ValueError(model)
    spec=PDESpec(model,j,(sp.expand(eq),),(j.jet(0,3,0),),(),('phi_t>0','phi_s>0','g,kappa>0',f'm={exponent}'),positive=(p,q,g,k))
    fields={'Y1':(1,0,0),'Y2':(0,0,1),'Y3':(0,1,0),'Y4':(t,s,u)}
    if exponent==3: fields['Y5']=(t,-2*s,0)
    if model=='P' and exponent==1: fields['Y6']=(0,0,t)
    return spec,{k:tuple(map(sp.sympify,v)) for k,v in fields.items()}


def euler(exponent=2):
    t,x,h,u,B=sp.symbols('t x h u B',real=True)
    g,k=sp.symbols('g kappa',positive=True)
    j=JetSpace((t,x),(h,u,B),1)
    equations=(j.D(h,0)+j.D(h*u,1),j.D(u,0)+u*j.D(u,1)+g*j.D(h+B,1),
               j.D(B,0)+k*j.D(u**exponent,1))
    spec=PDESpec('E1',j,equations,tuple(j.jet(a,1,0) for a in range(3)),(),('h,u,g,kappa>0',f'm={exponent}'),positive=(h,u,g,k))
    fields={'X1':(1,0,0,0,0),'X2':(0,1,0,0,0),'X3':(0,0,0,0,1),'X4':(t,x,0,0,0)}
    if exponent==3: fields['X5']=(t,0,-2*h,-u,-2*B)
    return spec,{k:tuple(map(sp.sympify,v)) for k,v in fields.items()}


def annular():
    """E2 in a regular polar chart; NOT the rotating-exchange five-balance model."""
    t,r,theta=sp.symbols('t r theta',real=True)
    h,V,W,B=sp.symbols('h V W B',real=True)
    g,K,G=sp.symbols('g K G',positive=True);f,c=sp.symbols('f c',real=True)
    j=JetSpace((t,r,theta),(h,V,W,B),2)
    S=V**2+W**2;Dr=lambda e:j.D(e,1);Dt=lambda e:j.D(e,0);Da=lambda e:j.D(e,2)
    equations=(Dt(h)+Dr(r*h*V)/r+Da(h*W)/r,
               Dt(V)+V*Dr(V)+W*Da(V)/r-W**2/r+g*Dr(h+B)-f*W,
               Dt(W)+V*Dr(W)+W*Da(W)/r+V*W/r+g*Da(h+B)/r+f*V,
               Dt(B)+Dr(r*S*(K*V-G*Dr(B)))/r+Da(S*(K*W-G*Da(B)/r))/r)
    spec=PDESpec('E2',j,equations,tuple(j.jet(a,1,0,0) for a in range(4)),(),('r>0','h>0','g,K,G>0'),positive=(r,h,g,K,G))
    from .reduce import Graph
    z=sp.Symbol('z',real=True);profiles=tuple(sp.Function(n)(z) for n in ('H','V','W','Z'))
    lifts=tuple(F.subs(z,r) for F in profiles[:3])+(profiles[3].subs(z,r)+c*t,)
    return spec,((0,0,1,0,0,0,0),(1,0,0,0,0,0,c)),Graph(z,r,profiles,lifts,{t:0,theta:0,r:z}),c
