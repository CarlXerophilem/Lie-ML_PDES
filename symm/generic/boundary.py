"""Sufficient local boundary certificates; never a general IBVP theorem."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import sympy as sp


@dataclass(frozen=True)
class BoundaryRestriction:
    expression: sp.Expr
    constraints: tuple[sp.Expr, ...]
    remainder: sp.Expr
    verified: bool
    method: str
    denominator_guards: tuple[sp.Expr, ...]


def normalize_zero_condition(expression: sp.Expr) -> tuple[sp.Expr, tuple[sp.Expr, ...]]:
    """Remove only factors known nonzero by SymPy's declared assumptions.

    Denominators remain explicit regular-chart guards. A factor with unknown
    sign/nonvanishing is retained, including a parameter that could be zero.
    """
    expression = sp.sympify(expression)
    numerator, denominator = sp.fraction(sp.together(expression))
    guards = [] if denominator in (1, -1) else [denominator]
    if numerator == 0:
        return sp.S.Zero, tuple(guards)
    try:
        coefficient, factors = sp.factor_list(numerator)
    except sp.PolynomialError:
        return expression, tuple(guards)
    retained = coefficient
    for factor, exponent in factors:
        if factor.is_nonzero is True:
            guards.append(factor)
        else:
            retained *= factor**exponent
    return sp.expand(retained/denominator), tuple(dict.fromkeys(guards))


def restrict_to_constraints(expression: sp.Expr, constraints: Iterable[sp.Expr]) -> BoundaryRestriction:
    """Certify ideal membership after recording denominator guards.

    All free symbols, including parameters, are polynomial generators. This
    avoids silently dividing by a parameter. Nonpolynomial cases remain
    unresolved unless direct simplification proves zero. The ideal test is
    sufficient and does not assert regularity or completeness of boundary jets.
    """
    expression = sp.simplify(expression)
    raw = tuple(map(sp.sympify, constraints))
    guards: list[sp.Expr] = []
    polynomials: list[sp.Expr] = []
    for item in (expression, *raw):
        numerator, denominator = sp.fraction(sp.together(item))
        polynomials.append(sp.expand(numerator))
        if denominator not in (1, -1):
            guards.append(denominator)
    variables = tuple(sorted(set().union(*(p.free_symbols for p in polynomials)), key=str))
    if not variables:
        consistent = all(p == 0 for p in polynomials[1:])
        return BoundaryRestriction(expression, raw, expression, expression == 0 and consistent,
                                   "constant-test" if consistent else "inconsistent-constraints", tuple(guards))
    try:
        basis = [p for p in polynomials[1:] if p != 0]
        # A unit ideal signals inconsistent data, not boundary compatibility.
        groebner = sp.groebner(basis, *variables) if basis else None
        if groebner is not None and any(p.as_expr() == 1 for p in groebner.polys):
            return BoundaryRestriction(expression, raw, expression, False, "inconsistent-constraints", tuple(guards))
        remainder = groebner.reduce(polynomials[0])[1] if groebner else polynomials[0]
        return BoundaryRestriction(expression, raw, remainder, remainder == 0,
                                   "polynomial-ideal", tuple(dict.fromkeys(guards)))
    except (sp.PolynomialError, ValueError, TypeError, sp.CoercionFailed):
        if expression == 0:
            return BoundaryRestriction(expression, raw, sp.S.Zero, True,
                                       "direct-zero; constraint-consistency-unresolved", tuple(guards))
        return BoundaryRestriction(expression, raw, expression, False,
                                   "unresolved-nonpolynomial", tuple(dict.fromkeys(guards)))
