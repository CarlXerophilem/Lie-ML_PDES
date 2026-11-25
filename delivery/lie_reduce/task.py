"""Regular task export. Critical 0/0 charts cannot silently enter a Picard solver."""
import sympy as sp


def to_task(reduced,traces,domain):
    if reduced.status!='verified': raise ValueError('unverified reduction')
    if len(reduced.equations)!=1 or len(reduced.graph.profiles)!=1:
        raise NotImplementedError('coupled-system task export requires an explicit normal form')
    eq=reduced.equations[0]; z=reduced.graph.z; F=reduced.graph.profiles[0]
    n=max((d.derivative_count for d in eq.atoms(sp.Derivative)),default=0)
    if n==0: raise ValueError('algebraic reduction is not an ODE task')
    highest=sp.diff(F,z,n)
    solutions=sp.solve(eq,highest)
    if len(solutions)!=1: raise ValueError('normal form has multiple or missing branches')
    if len(traces)!=n: raise ValueError('one initial datum per normal-form component is required')
    subs={z:domain[0],**{sp.diff(F,z,i):v for i,v in enumerate(traces)}}
    denominator=sp.denom(sp.cancel(solutions[0]))
    value=sp.simplify(denominator.subs(subs,simultaneous=True))
    if value==0 or value.is_zero is not False:
        raise ValueError('initial normal-form denominator is zero or undecidable')
    return {'schema':'Definition 6.1','scope':reduced.scope,'degree':reduced.degree,
            'status':'local_regular_task','domain':domain,'traces':traces,
            'residual':eq,'picard_rhs':tuple(sp.diff(F,z,i) for i in range(1,n))+(solutions[0],),
            'nonvanishing_denominator':denominator,'conditions':reduced.conditions,
            'domain_certificate':'not supplied; nonvanishing must hold over the solution tube',
            'training_fields':('residual','picard_rhs','domain','traces'),
            'singularity_analysis':'leading coefficient zero set is a candidate locus, not a classified singularity'}
