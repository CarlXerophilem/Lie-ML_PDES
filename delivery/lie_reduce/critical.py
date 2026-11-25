"""Exact algebraic BB form with rational complex-polydisk majorants. No ML/float bounds."""
import sympy as sp
from functools import lru_cache
from .annular import derive
from .identities import require_zero

ROOT=sp.sqrt(141)
FIELD=sp.QQ.algebraic_field(ROOT)
# Exact rational enclosure, proved by integer squaring.
LO=sp.Rational(11874342087037,10**12)
HI=sp.Rational(11874342087038,10**12)
assert LO**2<141<HI**2


@lru_cache(maxsize=4096)
def interval(c):
    c=FIELD.to_sympy(FIELD.from_sympy(c))
    b=c.coeff(ROOT);a=sp.simplify(c-b*ROOT)
    if not a.is_Rational or not b.is_Rational:raise ValueError('coefficient outside Q(sqrt(141))')
    return (a+b*LO,a+b*HI) if b>=0 else (a+b*HI,a+b*LO)


def upper_abs(c):
    lo,hi=interval(c);return max(abs(lo),abs(hi))


def lower_abs(c):
    lo,hi=interval(c)
    return 0 if lo<=0<=hi else min(abs(lo),abs(hi))


def terms(expr,x,w):return sp.Poly(expr,x,w,extension=ROOT).terms()


def norm(poly,R,W):return sum(upper_abs(c)*R**i*W**j for (i,j),c in poly)


def lower(poly,R,W):
    return sum(lower_abs(c) for (i,j),c in poly if (i,j)==(0,0))-sum(
        upper_abs(c)*R**i*W**j for (i,j),c in poly if (i,j)!=(0,0))


def derivative(poly):return [((i,j-1),j*c) for (i,j),c in poly if j]


def certify():
    ann=derive();r=ann['reduction'].graph.z;H=ann['reduction'].graph.profiles[0]
    h=sp.Symbol('h',real=True);rho,w=sp.symbols('rho w',real=True)
    pars={sp.Symbol('g',positive=True):1,sp.Symbol('K',positive=True):1,sp.Symbol('G',positive=True):1,
          sp.Symbol('f',real=True):1,sp.Symbol('c',real=True):-7,sp.Symbol('C1',real=True):1,
          sp.Symbol('C2',real=True):1,sp.Symbol('C3',real=True):-sp.Rational(71,16)}
    D=ann['D'].subs(pars).subs(H,h);N=ann['N'].subs(pars).subs(H,h)
    origin={r:1,h:1};require_zero(D.subs(origin),'critical D');require_zero(N.subs(origin),'critical N')
    J=sp.Matrix([D,N]).jacobian((r,h)).subs(origin)
    if not J.det()<0:raise ArithmeticError('not a saddle')
    ell=sp.Symbol('ell');slope_eq=sp.factor((D.diff(r)+ell*D.diff(h)).subs(origin)*ell-(N.diff(r)+ell*N.diff(h)).subs(origin))
    branches=[]
    for slope in sp.solve(slope_eq,ell):
        graph=1+rho*(slope+w);sub={r:1+rho,h:graph}
        d=sp.cancel(D.subs(sub)/rho,extension=ROOT);n=sp.cancel(N.subs(sub)/rho,extension=ROOT)
        d0=sp.simplify(d.subs({rho:0,w:0}));require_zero(n.subs({rho:0,w:0})-slope*d0,'critical direction')
        dn,dd=sp.fraction(d);nn,nd=sp.fraction(n)
        # Work in Q(sqrt(141))[rho,w]; avoid repeated expression-tree cancel().
        poly=lambda e:sp.Poly(e,rho,w,extension=ROOT)
        denominator=poly(nd)*poly(dn)
        numerator=poly(nn)*poly(dd)-poly(slope+w)*denominator
        c0=denominator.coeff_monomial(1)
        a=FIELD.to_sympy(FIELD.from_sympy(numerator.coeff_monomial(w)/c0));b=-a
        if not interval(b)[0]>1:raise ArithmeticError('b>1 not certified')
        numerator=numerator-poly(a*w)*denominator
        require_zero(numerator.coeff_monomial(1),'Psi origin')
        require_zero(numerator.coeff_monomial(w),'Psi_w origin')
        pn,pd=numerator.as_expr(),denominator.as_expr();psi=pn/pd
        P,Q=numerator.terms(),denominator.terms()
        # Preserve original chart factors, including the desingularized leading numerator.
        dn,_=sp.fraction(d)
        speed_num=sp.expand(1+graph**2*(1-(1+rho)**2/2)**2)
        factors={'r':terms(1+rho,rho,w),'H':terms(graph,rho,w),
                 'speed_numerator':terms(speed_num,rho,w),'d_numerator':terms(dn,rho,w)}
        accepted=None
        for k in range(4,25):
            R=sp.Rational(1,2**k)
            for j in range(4,13):
                W=sp.Rational(1,2**j);qlo=lower(Q,R,W)
                guards={name:lower(poly,R,W) for name,poly in factors.items()}
                if qlo<=0 or min(guards.values())<=0:continue
                L=norm(derivative(P),R,W)/qlo+norm(P,R,W)*norm(derivative(Q),R,W)/qlo**2
                pzero=[((i-1,0),c) for (i,j),c in P if j==0 and i>=1]
                K=norm(pzero,R,0)/lower(Q,R,0);blo=interval(b)[0]
                contraction=L/blo;image=K*R/(blo+1)+contraction*W
                if contraction<sp.Rational(1,2) and image<W:
                    accepted={'R':R,'R_w':W,'K_Psi_upper':K,'L_Psi_upper':L,'Lambda_upper':contraction,
                              'image_upper':image,'denominator_lower':qlo,'original_chart_modulus_lowers':guards,
                              'norm':'supremum on complex polydisk; coefficient triangle majorants',
                              'arithmetic':'exact rational outward enclosure of Q(sqrt(141)); no sampled bounds',
                              'status':'verified'}
                    break
            if accepted:break
        if not accepted:raise ArithmeticError('no disk accepted on fixed radius search')
        branches.append({'slope':slope,'d_origin':d0,'a':a,'b':b,'Psi':psi,
                         'nonresonance':'a < -1, hence n-a>0 for every integer n>=1',
                         'disk':accepted,
                         'tail_bound':'For H truncated after degree d>=1, |tail| <= R*R_w*q**(d+1)/(1-q), |rho|<=qR<R',
                         'tail_status':'analytic bound only; no truncated polynomial was generated in this stage'})
    return {'status':'verified','critical_point':origin,'desingularized_jacobian':J,'determinant':J.det(),
            'eigenvalues':tuple(J.eigenvals()),'slope_equation':slope_eq,'branches':branches,
            'shared_halfwidth':min(v['disk']['R'] for v in branches)/2,
            'scope':'specific c=-7 annular saddle; not all singular branches',
            'root_enclosure':(LO,HI)}
