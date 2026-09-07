"""Adapters preserving the scalar engine's public conventions."""

from __future__ import annotations

import sympy as sp

from .core import DifferentialSystem, JetSpace, PointGenerator


def legacy_system(pde) -> DifferentialSystem:
    """Convert a scalar legacy PDE into canonical `(x,t)` ordering."""
    equation = sp.sympify(pde.Delta)
    used = equation.free_symbols
    used_order = max(
        (sum(key) for key, symbol in pde.jet.items() if symbol in used),
        default=0,
    )
    jet_space = JetSpace((pde.x, pde.t), (pde.u,), max(pde.order, used_order))
    substitutions = {}
    for (a, b), old_symbol in pde.jet.items():
        if old_symbol in used:
            substitutions[old_symbol] = jet_space.jet_symbol(0, (a, b))
    equation = equation.xreplace(substitutions)
    return DifferentialSystem(jet_space, (equation,), name=pde.name)


def legacy_generator_to_point(pde, generator) -> PointGenerator:
    """Map `(tau, xi, phi)` to canonical `(xi^1, xi^2, phi)` ordering."""
    tau, xi, phi = map(sp.sympify, generator)
    return PointGenerator((xi, tau), (phi,))


def point_to_legacy(generator: PointGenerator):
    """Map canonical `(xi, tau, phi)` back to `(tau, xi, phi)`."""
    if generator.p != 2 or generator.q != 1:
        raise ValueError("legacy generators must have p=2 and q=1")
    return (generator.xi[1], generator.xi[0], generator.phi[0])
