import sympy as sp

from symm.generic.parameter_models import diffusion_search, heat_polynomial, reaction_search


def test_diffusion_counts_and_determinants():
    case = diffusion_search()
    strata = case.strata
    assert strata.nullity(2) == 4
    assert strata.nullity(-sp.Rational(4, 3)) == 5
    assert strata.exceptional_values == (-sp.Rational(4, 3),)
    for vector in strata.matrix.subs(strata.parameter, -sp.Rational(4, 3)).nullspace():
        residual = case.shell_residual.subs(dict(zip(strata.coefficients, vector))).subs(
            strata.parameter, -sp.Rational(4, 3))
        assert sp.simplify(residual) == 0
    assert strata.nullity(0) < sp.oo


def test_reaction_counts_and_linear_stratum():
    case = reaction_search()
    assert all(case.strata.nullity(value) == 3 for value in (-2, 1, 2))
    assert case.strata.exceptional_values == (0,)
    assert case.strata.nullity(0) > 3


def test_arbitrarily_high_independent_heat_polynomials():
    t, x = sp.symbols("t x")
    for order in range(15):
        polynomial = heat_polynomial(order, t, x)
        assert sp.expand(sp.diff(polynomial, t)-sp.diff(polynomial, x, 2)) == 0
        assert polynomial.subs(t, 0) == x**order
