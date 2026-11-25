from dataclasses import dataclass, field
import sympy as sp
from sympy.core.function import AppliedUndef
from .identities import require_zero, nonzero_record


@dataclass
class Graph:
    z: sp.Symbol
    invariant: sp.Expr
    profiles: tuple
    lifts: tuple
    section: dict
    conditions: tuple = ()
    orbit_coordinates: dict = field(default_factory=dict)


@dataclass
class ReducedODE:
    model: str
    status: str
    reason: str = ''
    graph: Graph | None = None
    equations: tuple = ()
    weights: tuple = ()
    first_integrals: tuple = ()
    leading_coefficients: tuple = ()
    conditions: tuple = ()
    checks: dict = field(default_factory=dict)
    scope: str = 'specified local invariant graph; not exhaustive reduction classification'
    degree: int | None = None


def automatic_graph(spec, X):
    j=spec.jets
    if len(j.independent)!=2:
        raise NotImplementedError('automatic graph currently supports two independent variables; supply section graph')
    t,x=j.independent
    if X[0]==0:
        if X[1]==0: raise ValueError('no invariant graph')
        # Swap independent coordinates only for construction; lifts keep original coordinates.
        t,x=x,t
        base=(X[1],X[0])
    else: base=X[:2]
    a,b=sp.diff(base[0],t),base[0].subs(t,0)
    c,d=sp.diff(base[1],x),base[1].subs(x,0)
    if any(v.has(*j.independent,*j.dependent) for v in (a,b,c,d)):
        raise NotImplementedError('non-diagonal affine base flow needs a supplied section graph')
    z=sp.Symbol('z',real=True)
    t0=sp.S.One if a!=0 and b==0 else sp.S.Zero
    if sp.simplify(a*t0+b)==0: raise ValueError('section is not transverse')
    e=sp.log((a*t+b)/(a*t0+b))/a if a!=0 else (t-t0)/b
    inv=sp.exp(-c*e)*(x+d/c)-d/c if c!=0 else x-d*e
    inv=sp.simplify(sp.expand_power_base(inv))
    profiles=tuple(sp.Function('F'+str(i))(z) for i in range(len(j.dependent)))
    lifts=[]
    v=sp.Symbol('orbit',real=True)
    tflow=(t0+b/a)*sp.exp(a*v)-b/a if a!=0 else t0+b*v
    for u,eta,F in zip(j.dependent,X[2:],profiles):
        rate=sp.diff(eta,u)
        forcing=sp.expand(eta-rate*u)
        if rate.has(*j.independent,*j.dependent) or forcing.has(*j.dependent):
            raise NotImplementedError('coupled vertical flow needs a supplied section graph')
        xflow=(inv+d/c)*sp.exp(c*v)-d/c if c!=0 else inv+d*v
        integral=sp.integrate(sp.exp(-rate*v)*forcing.subs({t:tflow,x:xflow},simultaneous=True),(v,0,e))
        lifts.append(sp.simplify(sp.exp(rate*e)*(F.subs(z,inv)+integral)))
    return Graph(z,inv,profiles,tuple(lifts),{t:t0,x:z},
                 (f'{a*t+b} != 0', 'local flow chart; logarithm arguments positive when used'),
                 {t:tflow,x:(z+d/c)*sp.exp(c*v)-d/c if c!=0 else z+d*v})


def total_1d(expr,z,Y):
    return sp.diff(expr,z)+sum(Y[i+1]*sp.diff(expr,Y[i]) for i in range(len(Y)-1))


def flux_check(expr,F,z):
    """Construct a highest-jet linear flux and check it exactly. No guessed integral accepted."""
    orders=[d.derivative_count for d in expr.atoms(sp.Derivative) if d.expr==F]
    n=max(orders,default=0)
    if n<1: return {'status':'not_found','reason':'no derivative'}
    Y=sp.symbols('v:'+str(2*n+2))
    mapping={sp.diff(F,z,i):Y[i] for i in range(n+1)}
    r=expr.xreplace(mapping)
    euler=sum((-1)**i*__D(sp.diff(r,Y[i]),i,z,Y) for i in range(n+1))
    from .identities import zero_record
    euler_evidence=zero_record(euler)
    if euler_evidence['status']!='proved_zero':
        return {'status':'not_total_derivative' if euler_evidence['status']=='proved_not_identically_zero' else 'undetermined',
                'euler_operator':sp.factor(euler),'evidence':euler_evidence}
    # Repeated integration of the highest jet constructs a local flux when polynomial/elementary.
    remainder=r; flux=sp.S.Zero
    for k in range(n,0,-1):
        candidate=sp.integrate(sp.diff(remainder,Y[k]),Y[k-1])
        flux+=candidate
        remainder=sp.cancel(remainder-total_1d(candidate,z,Y))
    flux+=sp.integrate(remainder,z)
    defect=sp.cancel(r-total_1d(flux,z,Y))
    if defect!=0: return {'status':'not_found','reason':'constructive flux identity failed'}
    inverse={Y[i]:sp.diff(F,z,i) for i in range(n+1)}
    return {'status':'verified','flux':flux.xreplace(inverse),'identity_remainder':0,'constant':'I0','euler_evidence':euler_evidence}


def __D(expr,n,z,Y):
    for _ in range(n): expr=total_1d(expr,z,Y)
    return expr


def reduce(spec,X,section=None):
    X=tuple(map(sp.sympify,X)); j=spec.jets
    if len(X)!=len(j.independent)+len(j.dependent):
        return ReducedODE(spec.name,'rejected',reason='generator dimension mismatch')
    if all(v==0 for v in X):
        return ReducedODE(spec.name,'rejected',reason='zero generator does not define a one-dimensional subalgebra')
    if any(v.has(*j.dependent) for v in X[:len(j.independent)]):
        return ReducedODE(spec.name,'unsupported',reason='base action is not projectable in this chart')
    if all(v==0 for v in X[:len(j.independent)]):
        vertical=X[len(j.independent):]
        if any(nonzero_record(v,spec.positive)['status']=='proved_nonzero' or (not v.has(*j.dependent) and v!=0) for v in vertical):
            return ReducedODE(spec.name,'no invariant graph',reason='a vertical component cannot vanish on this chart')
        return ReducedODE(spec.name,'vertical_fixed_locus',reason='solve eta=0 on the graph; a pure vertical field may have fixed graphs',conditions=tuple(sp.Eq(v,0) for v in vertical))
    try: graph=section or automatic_graph(spec,X)
    except (NotImplementedError,ValueError) as exc:
        return ReducedODE(spec.name,'unsupported',str(exc))
    if sp.simplify(graph.invariant.subs(graph.section,simultaneous=True)-graph.z)!=0:
        return ReducedODE(spec.name,'rejected',reason='section does not invert the quotient coordinate')
    if any(sp.simplify(lift.subs(graph.section,simultaneous=True)-F)!=0 for lift,F in zip(graph.lifts,graph.profiles)):
        return ReducedODE(spec.name,'rejected',reason='section does not recover arbitrary profile data')
    section_curve=sp.Matrix([graph.section.get(x,x) for x in j.independent])
    if len(j.independent)!=2:
        return ReducedODE(spec.name,'unsupported',reason='use reduce_subalgebra for higher-dimensional bases')
    transverse=sp.Matrix.hstack(sp.Matrix(X[:2]).subs(graph.section,simultaneous=True),section_curve.diff(graph.z)).det()
    transverse_record=nonzero_record(transverse,spec.positive)
    if transverse_record['status']=='zero':
        return ReducedODE(spec.name,'rejected',reason='section is tangent to the orbit')
    shell,_=spec.shell()
    if any(sp.cancel(j.act(eq,X).subs(shell,simultaneous=True))!=0 for eq in spec.equations):
        return ReducedODE(spec.name,'rejected',reason='generator fails full on-shell symmetry identity')
    n=len(j.independent)
    mapping=dict(zip(j.dependent,graph.lifts))
    defects=tuple(sp.simplify(eta.subs(mapping,simultaneous=True)-sum(
        xi.subs(mapping,simultaneous=True)*sp.diff(lift,x) for xi,x in zip(X[:n],j.independent)))
        for eta,lift in zip(X[n:],graph.lifts))
    invariant_defect=sp.simplify(sum(v*sp.diff(graph.invariant,x) for v,x in zip(X[:n],j.independent)))
    if any(v!=0 for v in defects) or invariant_defect!=0:
        return ReducedODE(spec.name,'rejected',reason='invariant surface or invariant coordinate identity fails')
    jet_map=j.pullback(graph.lifts)
    positive=tuple(sp.simplify(v.xreplace(jet_map)) for v in spec.positive)
    if any(v.is_nonpositive is True for v in positive):
        return ReducedODE(spec.name,'chart-incompatible',reason='a declared strictly positive quantity is identically nonpositive on this graph',graph=graph)
    pulled=tuple(sp.factor(eq.xreplace(jet_map)) for eq in spec.equations)
    equations=tuple(sp.factor(v.subs(graph.section, simultaneous=True).doit()) for v in pulled)
    weights=[]; weight_evidence=[]
    for raw,red in zip(pulled,equations):
        if graph.orbit_coordinates:
            raw=sp.simplify(raw.subs(graph.orbit_coordinates,simultaneous=True).doit())
            lifted=red
        else:
            lifted=red.subs(graph.z,graph.invariant).doit()
        ratio=sp.simplify(raw/lifted) if red!=0 else sp.S.One
        if red==0 and sp.simplify(raw)!=0:
            return ReducedODE(spec.name,'rejected',reason='zero section equation does not extend off section')
        if ratio.has(*j.dependent) or ratio.atoms(AppliedUndef) or ratio.atoms(sp.Derivative):
            return ReducedODE(spec.name,'unsupported',reason='cannot verify scalar weight off section; need equivariant system section')
        if sp.simplify(raw-ratio*lifted)!=0:
            return ReducedODE(spec.name,'rejected',reason='pullback weight identity fails')
        evidence=nonzero_record(ratio,spec.positive)
        if evidence['status']=='zero':
            return ReducedODE(spec.name,'rejected',reason='zero pullback weight destroys reverse implication')
        weight_evidence.append(evidence)
        weights.append(ratio)
    integrals=tuple(flux_check(eq,graph.profiles[0],graph.z) for eq in equations) if len(graph.profiles)==1 else ()
    leading=[]
    for eq in equations:
        derivatives=eq.atoms(sp.Derivative)
        order=max((d.derivative_count for d in derivatives),default=0)
        leading.append({str(d):sp.factor(eq.diff(d)) for d in derivatives if d.derivative_count==order})
    return ReducedODE(spec.name,'verified',graph=graph,equations=equations,weights=tuple(weights),
                      first_integrals=integrals,leading_coefficients=tuple(leading),conditions=spec.conditions+graph.conditions+tuple(str(v)+' > 0' for v in positive),
                      checks={'on_shell':True,'invariant_surface':True,'pullback':True,
                              'base_orbit_rank':1,'transversality':transverse_record,
                              'weight_nonvanishing':weight_evidence,'section_inverse':True,
                              'verification_level':'local symbolic identities conditional on listed chart and nonvanishing requirements',
                              'chart_admissibility':'conditional: profile inequalities must be checked with data',
                              'closed_form':'not attempted; Lie hint applies to supported first-order scalar ODEs only'})


def reduce_subalgebra(spec,generators,graph):
    """Explicit multi-generator section, with rank and vector ISC checks."""
    j=spec.jets;n=len(j.independent)
    fields=[tuple(map(sp.sympify,X)) for X in generators]
    base=sp.Matrix([X[:n] for X in fields]);point=sp.Matrix(fields)
    rank=base.rank()
    if rank!=point.rank() or rank!=n-1:
        return ReducedODE(spec.name,'rejected',reason='orbit/base rank mismatch or quotient is not one-dimensional')
    shell,_=spec.shell();mapping=dict(zip(j.dependent,graph.lifts))
    for X in fields:
        if any(sp.cancel(j.act(eq,X).subs(shell,simultaneous=True))!=0 for eq in spec.equations):
            return ReducedODE(spec.name,'rejected',reason='subalgebra generator fails on-shell identity')
        if sp.simplify(sum(v*graph.invariant.diff(x) for v,x in zip(X[:n],j.independent)))!=0:
            return ReducedODE(spec.name,'rejected',reason='quotient coordinate not invariant')
        for eta,lift in zip(X[n:],graph.lifts):
            if sp.simplify(eta.subs(mapping,simultaneous=True)-sum(v*lift.diff(x) for v,x in zip(X[:n],j.independent)))!=0:
                return ReducedODE(spec.name,'rejected',reason='vector invariant-surface condition fails')
    equations=tuple(sp.factor(eq.xreplace(j.pullback(graph.lifts))) for eq in spec.equations)
    equations=tuple(eq.subs(graph.section,simultaneous=True).doit() for eq in equations)
    for raw,eq in zip(spec.equations,equations):
        if sp.simplify(raw.xreplace(j.pullback(graph.lifts))-eq.subs(graph.z,graph.invariant))!=0:
            return ReducedODE(spec.name,'unsupported',reason='manual graph quotient is not invariant without a weight matrix')
    return ReducedODE(spec.name,'verified',graph=graph,equations=equations,conditions=spec.conditions,
                      checks={'base_orbit_rank':rank,'point_orbit_rank':point.rank(),'on_shell':True,
                              'invariant_surface':True,'pullback':True},
                      scope='manual two-dimensional subalgebra; two-dimensional optimal system not computed')
