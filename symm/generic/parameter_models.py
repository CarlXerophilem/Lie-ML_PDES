"""Declared finite polynomial searches, directly derived by prolongation."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from .core import JetSpace, PointGenerator
from .jets import prolonged_action
from .rank_strata import RankStrata, coefficient_matrix, determinantal_strata


@dataclass(frozen=True)
class ParameterSearch:
    name: str
    space: JetSpace
    generator: PointGenerator
    residual: sp.Expr
    shell_residual: sp.Expr
    strata: RankStrata
    scope: str


@lru_cache(maxsize=2)
def diffusion_search() -> ParameterSearch:
    t, x = sp.symbols("t x")
    u = sp.Symbol("u", positive=True)
    alpha = sp.Symbol("alpha", real=True)
    space = JetSpace((t, x), (u,), 2)
    ut, ux, uxx = (space.jet_symbol(0, ij) for ij in ((1, 0), (0, 1), (0, 2)))
    cs = sp.symbols("c0:9")
    tau = cs[0]+cs[1]*t+cs[2]*t*t
    xi = cs[3]+cs[4]*x+cs[5]*x*x
    eta = u*(cs[6]+cs[7]*x+cs[8]*t)
    generator = PointGenerator((tau, xi), (eta,))
    rhs = u**alpha*uxx+alpha*u**(alpha-1)*ux**2
    residual = ut-rhs
    shell = sp.expand(prolonged_action(space, residual, generator).subs(ut, rhs))
    # Split free spatial jets before cancelling positive powers of u. The
    # remaining zero-jet equation is c8*u=0 and has the recorded u>0 guard.
    spatial = sp.Poly(sp.expand(shell/u**alpha), ux, uxx)
    equations = []
    for monomial, expression in spatial.terms():
        if monomial == (0, 0):
            expression = sp.simplify(expression*u**alpha/u)
        else:
            expression = sp.cancel(expression*u if monomial == (2, 0) else expression)
        equations.append(expression)
    matrix = coefficient_matrix(equations, cs, (t, x, u))
    strata = determinantal_strata(matrix, cs, alpha)
    return ParameterSearch("nonlinear_diffusion", space, generator, residual, shell, strata,
                           "tau quadratic in t; xi quadratic in x; eta/u affine in (t,x); u>0; finite scope")


@lru_cache(maxsize=2)
def reaction_search() -> ParameterSearch:
    t, x, u = sp.symbols("t x u")
    kappa = sp.Symbol("kappa", real=True)
    space = JetSpace((t, x), (u,), 2)
    ut, ux, uxx = (space.jet_symbol(0, ij) for ij in ((1, 0), (0, 1), (0, 2)))
    cs = sp.symbols("c0:11")
    tau = cs[0]+cs[1]*t+cs[2]*t*t
    xi = sp.diff(tau, t)*x/2+cs[3]+cs[4]*t
    eta = (cs[5]+cs[6]*x+cs[7]*t)*u+cs[8]+cs[9]*x+cs[10]*t
    generator = PointGenerator((tau, xi), (eta,))
    rhs = uxx+kappa*u*u
    residual = ut-rhs
    shell = sp.expand(prolonged_action(space, residual, generator).subs(ut, rhs))
    matrix = coefficient_matrix((shell,), cs, (t, x, u, ux, uxx))
    strata = determinantal_strata(matrix, cs, kappa)
    return ParameterSearch("quadratic_reaction", space, generator, residual, shell, strata,
                           "tau quadratic; xi=tau_t*x/2+affine(t); eta affine(t,x)*u+affine(t,x); finite scope")


def heat_polynomial(order: int, t: sp.Symbol, x: sp.Symbol) -> sp.Expr:
    if order < 0:
        raise ValueError("heat polynomial order must be nonnegative")
    return sum(sp.factorial(order)*t**j*x**(order-2*j)
               /(sp.factorial(j)*sp.factorial(order-2*j)) for j in range(order//2+1))
