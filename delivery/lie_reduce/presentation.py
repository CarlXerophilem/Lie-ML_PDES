"""Explicit square-free presentation changes; never silently select a PDE component."""
from dataclasses import replace
from itertools import product
from math import prod
import sympy as sp
from .identities import require_zero, nonzero_record


def square_free_presentation(spec, max_components=32):
    """Preserve the zero set of each rational equation on its original domain.

    This removes repeated polynomial factors, not arbitrary real-radical ideals.
    Component coverage is pointwise in jet space, not a global decomposition of
    smooth solutions (which may meet component intersections).
    """
    equations=[];proofs=[];factors=[];exclusions=list(spec.domain_exclusions)
    for eq in spec.equations:
        eq=sp.sympify(eq)
        if eq.has(sp.Float):raise ValueError('presentation normalization requires exact input')
        numerator,denominator=eq.as_numer_denom()
        variables=sorted(numerator.free_symbols,key=sp.default_sort_key)
        if not variables:
            if numerator==0:raise ValueError('identically zero equation: remove redundant rows explicitly')
            raise ValueError('nonzero constant equation has no solutions on its domain')
        try:
            polynomial=sp.Poly(numerator,*variables,domain=sp.QQ)
        except (sp.PolynomialError,sp.CoercionFailed) as exc:
            raise ValueError('square-free normalization supports rational coefficients and polynomial numerators only') from exc
        unit,fac=sp.factor_list(polynomial.as_expr(),*variables)
        if not fac:raise ValueError('empty polynomial factorization')
        require_zero(numerator-unit*prod(f**n for f,n in fac),'factorization reconstruction')
        kept=[];removed=[]
        for f,n in fac:
            evidence=nonzero_record(f,spec.positive)
            if evidence['status']=='proved_nonzero':removed.append({'factor':f,'multiplicity':n,'evidence':evidence})
            else:kept.append(f)
        if not kept:raise ValueError('all factors are nonzero on the declared chart: no solutions')
        new=prod(kept)
        equations.append(new);factors.append(tuple(kept))
        if denominator!=1:exclusions.append(denominator)
        proofs.append({'original':eq,'numerator':numerator,'denominator':denominator,
                       'factorization_unit':unit,'factors_with_multiplicity':fac,'removed_nonzero_factors':removed,
                       'square_free_equation':new,'identity_check':'exact polynomial reconstruction',
                       'zero_set_equivalence':'both directions on the original nonzero-denominator chart'})
    exclusions=tuple(dict.fromkeys(exclusions))
    normalized=replace(spec,name=spec.name+' [square-free]',equations=tuple(equations),domain_exclusions=exclusions)
    count=prod(len(v) for v in factors)
    components=[]
    if count<=max_components:
        for i,choice in enumerate(product(*factors)):
            component=replace(normalized,name=spec.name+f' [component {i}]',equations=tuple(choice))
            try:chart={'status':'available','certificate':component.shell_certificate()}
            except (ValueError,ArithmeticError) as exc:chart={'status':'unavailable','reason':str(exc)}
            components.append({'spec':component,'principal_chart':chart})
    return {'schema':'Definition 6.1 symbolic provenance extension','scope':'rational polynomial presentation on declared chart',
            'status':'zero_set_equivalence_verified','original_spec':spec,'normalized_spec':normalized,
            'equation_certificates':proofs,'domain_exclusions':exclusions,'components':components,
            'component_enumeration':'enumerated' if count<=max_components else 'not_computed',
            'component_count':count,'component_cap':max_components,
            'component_scope':'pointwise union; intersections, branch switching and formal integrability are not classified',
            'symmetry_scope':'symmetries of the full zero set are preserved by equivalence; an individual component may have more symmetries'}
