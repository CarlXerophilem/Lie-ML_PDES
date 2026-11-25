"""Independent four-balance E2 quotient and exact first-integral elimination."""
import sympy as sp
from .models import annular
from .reduce import reduce_subalgebra


def derive():
    spec,fields,graph,c=annular();red=reduce_subalgebra(spec,fields,graph)
    if red.status!='verified':raise ArithmeticError(red.reason)
    r=graph.z;h,v,w,z=graph.profiles
    g,K,G=sp.symbols('g K G',positive=True);f=sp.Symbol('f',real=True)
    C1,C2,C3=sp.symbols('C1 C2 C3',real=True)
    Q=(v**2+w**2)*(K*v-G*z.diff(r))
    fluxes=(r*h*v,r*w+f*r**2/2,r*Q+c*r**2/2)
    checks=(sp.factor(sp.diff(fluxes[0],r)-r*red.equations[0]),
            sp.factor(v*sp.diff(fluxes[1],r)-r*red.equations[2]),
            sp.factor(sp.diff(fluxes[2],r)-r*red.equations[3]))
    if any(v!=0 for v in checks):raise ArithmeticError('annular flux identity failed')
    vv=C1/(r*h);ww=C2/r-f*r/2;speed=vv**2+ww**2
    PZ=(K*vv-(C3/r-c*r/2)/speed)/G
    D=g*h-vv**2;N=h*(speed/r+f*ww-g*PZ)
    substitutions={v:vv,w:ww}
    residual=red.equations[1].subs(substitutions).doit().subs(z.diff(r),PZ)
    if sp.factor(residual-(D*h.diff(r)-N)/h)!=0:raise ArithmeticError('annular elimination failed')
    return {'reduction':red,'first_integrals':fluxes,'flux_identity_remainders':checks,
            'V':vv,'W':ww,'P_Z':PZ,'D':D,'N':N,'undivided_ode':D*h.diff(r)-N,
            'additional_conditions':('V != 0 for angular integration','H>0','r>0','V**2+W**2>0'),
            'singularity_candidates':{'leading_zero':sp.Eq(D,0),'compatible_critical':(sp.Eq(D,0),sp.Eq(N,0)),
                                       'classification':'saddle requires an additional desingularized Jacobian check'},
            'task_status':'critical N3 requires separate BB normal form; regular N/D export forbidden at D=0'}
