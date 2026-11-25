"""Fixed graphs of vertical point fields; no orbit-dimension reduction is claimed."""
import sympy as sp
from .identities import zero_record,nonzero_record,require_zero


def vertical_fixed_graphs(spec,field):
    j=spec.jets;n=len(j.independent);field=tuple(map(sp.sympify,field))
    if len(field)!=n+len(j.dependent) or any(v!=0 for v in field[:n]):
        raise ValueError('a vertical field with the correct dimension is required')
    eta=field[n:]
    if all(v==0 for v in eta):return {'status':'rejected','reason':'zero generator'}
    # Fixed graphs can be studied for any field, but a Lie-reduction claim requires symmetry.
    try:
        principal_chart=spec.shell_certificate()
        shell=principal_chart['solution']
        checks=[zero_record(j.act(eq,field).subs(shell,simultaneous=True)) for eq in spec.equations]
    except (ValueError,ArithmeticError) as exc:
        return {'status':'unsupported','reason':'PDE regularity not secured: '+str(exc)}
    if any(v['status']!='proved_zero' for v in checks):
        return {'status':'rejected','reason':'vertical field is not a verified point symmetry','prolongation':checks}
    constraints=tuple(v for v in eta if v!=0)
    if any(nonzero_record(v,spec.positive)['status']=='proved_nonzero' for v in constraints):
        return {'status':'no invariant graph','reason':'fixed-locus constraint cannot vanish on declared chart'}
    # Only polynomial constraints are solved automatically. A nonpolynomial
    # coefficient may vanish on an open patch; nonidentity alone cannot exclude it.
    try:
        for v in constraints:sp.Poly(v,*(j.independent+j.dependent))
    except sp.PolynomialError:
        return {'status':'unsupported','reason':'nonpolynomial fixed-locus equations require a separate local analysis'}
    try:solutions=sp.solve(constraints,j.dependent,dict=True)
    except NotImplementedError as exc:return {'status':'unsupported','reason':str(exc)}
    if not solutions:
        # solve()==[] is not a completeness certificate in a parametric system.
        if any(v.free_symbols <= set(j.independent) and zero_record(v)['status']=='proved_not_identically_zero' for v in constraints):
            return {'status':'no invariant graph','reason':'polynomial base constraint cannot hold on an open base patch; parameter specializations must be checked separately'}
        return {'status':'undetermined','reason':'no fixed graphs returned; no real-algebraic emptiness proof','constraints':constraints}
    records=[]
    for solution in solutions:
        free=tuple(u for u in j.dependent if u not in solution)
        free_graphs={u:sp.Function('free_'+str(u),real=True)(*j.independent) for u in free}
        lifts=tuple(solution.get(u,u).subs(free_graphs,simultaneous=True) for u in j.dependent)
        for v in constraints:require_zero(v.subs(dict(zip(j.dependent,lifts)),simultaneous=True),'fixed graph constraint')
        if any(v.is_real is False for v in lifts):
            records.append({'status':'nonreal','lifts':lifts});continue
        jets=j.pullback(lifts)
        positives=tuple(sp.factor(v.xreplace(jets)) for v in spec.positive)
        denominators=tuple(dict.fromkeys((*spec.domain_exclusions,*(sp.denom(v) for v in spec.equations),*(sp.denom(v) for v in lifts),*(sp.denom(v) for v in jets.values()))))
        guards=tuple(sp.factor(v.xreplace(jets)) for v in denominators)
        if any(v.is_nonpositive is True for v in positives) or any(v==0 for v in guards):
            records.append({'status':'chart-incompatible','lifts':lifts,'positive_quantities':positives,'denominators':guards});continue
        residuals=tuple(sp.cancel(eq.xreplace(jets)) for eq in spec.equations)
        evidence=tuple(zero_record(eq) for eq in residuals)
        if all(v['status']=='proved_zero' for v in evidence):status='verified_fixed_solution'
        elif free:status='constrained_PDE'
        elif any(v['status']=='proved_not_identically_zero' for v in evidence):status='PDE_incompatible'
        else:status='undetermined'
        records.append({'status':status,'lifts':lifts,'free_dependent_variables':free,'PDE_residuals':residuals,
                        'residual_evidence':evidence,'positive_quantities':positives,'nonzero_denominators':guards,
                        'real_valuedness_conditions':tuple(sp.Q.real(v) for v in lifts if v.is_real is not True),
                        'interpretation':'symbolic result conditional on real smooth lifts and the displayed chart requirements'})
    return {'schema':'Definition 6.1 symbolic provenance extension','status':'fixed_graph_analysis',
            'scope':'candidate fixed graphs on regular PDE chart; no complete real parametric stratification',
            'constraints':constraints,'prolongation':checks,'branches':records,
            'principal_chart':principal_chart,'declared_conditions':spec.conditions,
            'base_orbit_rank':0,'independent_variables_remaining':len(j.independent),
            'is_ODE_reduction':False,'completeness':'not claimed for solve() candidates or parameter specializations'}
