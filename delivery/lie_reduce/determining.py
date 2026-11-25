"""Discovery in a declared polynomial coefficient class; never a smooth-class theorem."""
import sympy as sp
from .strata import rank_locus
from .identities import require_zero


def symmetries(spec, degree=2):
    j = spec.jets
    base = j.independent+j.dependent
    monomials = sorted(sp.itermonomials(base,degree),key=sp.default_sort_key)
    constants = sp.symbols('a:'+str(len(base)*len(monomials)))
    field = tuple(sum(c*v for c,v in zip(constants[i*len(monomials):(i+1)*len(monomials)],monomials))
                  for i in range(len(base)))
    shell, denominators = spec.shell()
    free = tuple(v for v in j.jets.values() if v not in shell and v not in j.dependent)
    rows = []
    for eq in spec.equations:
        tangent = j.act(eq,field).subs(shell, simultaneous=True)
        numerator = sp.cancel(tangent).as_numer_denom()[0]
        # Polynomial splitting is exact on an open chart. Nonpolynomial jets are
        # explicitly unsupported, rather than sampled at convenient parameter values.
        try:
            rows.extend(sp.Poly(numerator,*(free+base)).coeffs())
        except sp.PolynomialError as exc:
            raise ValueError('nonpolynomial jet dependence: specialize exponent or supply a proved split') from exc
    matrix,rhs = sp.linear_eq_to_matrix(rows,constants)
    if rhs != sp.zeros(matrix.rows,1):
        raise ValueError('inhomogeneous determining equations')
    basis = [tuple(sp.expand(v.subs(dict(zip(constants,k)))) for v in field) for k in matrix.nullspace()]
    for generator in basis:
        for equation in spec.equations:
            require_zero(j.act(equation,generator).subs(shell,simultaneous=True),'full prolongation sufficiency')
    return dict(full_prolongation_verified=True,symmetry_type='point only',scope='polynomial point coefficients on specified principal chart',degree=degree,
                basis=basis,matrix=matrix,rank=matrix.rank(),denominators=denominators,
                strata=rank_locus(matrix,spec.parameters))
