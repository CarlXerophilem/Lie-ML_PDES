"""No fitted data: derive prospective benchmark residuals from verified reductions."""
from dataclasses import replace
import sympy as sp
from .models import scalar,euler
from .reduce import reduce,Graph,ReducedODE
from .algebra import add
from .annular import derive
from .task import to_task


def export():
    spec,b=euler(2);alpha=sp.Symbol('alpha',real=True)
    red=reduce(spec,add((1,b['X1']),(alpha,b['X3'])))
    if red.status!='verified':raise ArithmeticError(red.reason)
    z=red.graph.z;H,U,B=red.graph.profiles;g,k=sp.symbols('g kappa',positive=True)
    # The water equations have fluxes HU and U²/2+g(H+B).
    for eq,flux in zip(red.equations[:2],(H*U,U**2/2+g*(H+B))):
        if sp.simplify(sp.diff(flux,z)-eq)!=0:raise ArithmeticError('Eulerian first integral failed')
    ode=red.equations[2].subs({k:1,alpha:1})
    n1=ReducedODE('N1','verified',graph=Graph(z,z,(U,),(U,),{}),equations=(ode,),
                  conditions=('U>0','h=1/U','g=kappa=alpha=1','m=2'),degree=2)
    record1=to_task(n1,(1,),(0,sp.Rational(4,5)))
    record1['lift']={'h':1/U,'u':U,'B':'t+3/2-U**2/2-1/U'}
    record1['provenance']='E1 bed-drift pullback plus two checked first integrals'
    spec,b=scalar('M',2);c,gamma=sp.symbols('c gamma',real=True)
    red=reduce(spec,add((1,b['Y1']),(c,b['Y3']),(gamma,b['Y2'])))
    flux=red.first_integrals[0]
    if flux['status']!='verified':raise ArithmeticError('material first integral missing')
    F=red.graph.profiles[0];z=red.graph.z;p=sp.Function('p')(z)
    eq=(flux['flux']-1).xreplace({sp.diff(F,z,2):p.diff(z),sp.diff(F,z):p})
    eq=sp.factor(eq.subs({c:-1,gamma:sp.Rational(1,2),g:1,k:sp.Rational(1,20)})) # beta=m*kappa=1/10
    n2=ReducedODE('N2','verified',graph=Graph(z,z,(p,),(p,),{}),equations=(eq,),degree=2,
                  conditions=('p>0','1/2+p>0','L != 0','m=2,beta=1/10'))
    record2=to_task(n2,(sp.Rational(1,2),),(0,sp.Rational(1,64)))
    record2['domain_note']='local interface smoke test, not the proposed fold-distance benchmark domain'
    record2['provenance']='compatible M tilted reduction, checked flux, beta=m*kappa conversion'
    ann=derive();r=ann['reduction'].graph.z;H=ann['reduction'].graph.profiles[0]
    f,c=sp.symbols('f c',real=True);K,G=sp.symbols('K G',positive=True);C1,C2,C3=sp.symbols('C1 C2 C3',real=True)
    pars={g:1,K:1,G:1,f:1,c:-7,C1:1,C2:1,C3:-sp.Rational(71,16)}
    D,N=ann['D'].subs(pars),ann['N'].subs(pars)
    h=sp.Symbol('h',real=True);D=D.subs(H,h);N=N.subs(H,h)
    point={r:1,h:1}
    if sp.simplify(D.subs(point))!=0 or sp.simplify(N.subs(point))!=0:raise ArithmeticError('not a compatible critical point')
    ell=sp.Symbol('ell',real=True)
    slope_equation=sp.factor((D.diff(r)+D.diff(h)*ell).subs(point)*ell-(N.diff(r)+N.diff(h)*ell).subs(point))
    slopes=sp.solve(slope_equation,ell)
    return {'N1':record1,'N2':record2,'N3':{'schema':'Definition 6.1 symbolic provenance extension','scope':ann['reduction'].scope,
             'degree':None,'status':'implicit_critical_task','residual':D*sp.Symbol('H_prime')-N,
             'traces':point,'slope_equation':slope_equation,'branch_slopes':slopes,'picard_rhs':None,
             'reason':'D=N=0 at initial point: a separately verified BB operator is required before numerical training',
             'source':'generic vector pullback of manual rank-two E2 section'}}
