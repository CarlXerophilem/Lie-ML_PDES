"""Lie brackets and a certified first reduction slice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import sympy as sp

from .core import (
    DifferentialSystem,
    LieSubalgebra,
    PointGenerator,
    ReducedSystem,
    ReductionCertificate,
    ReductionMap,
    fingerprint,
)
from .jets import characteristic, iter_multi_indices, jet_coordinates
from .core import JetSpace


@dataclass(frozen=True)
class ReductionOutcome:
    reduced_system: ReducedSystem | None
    certificate: ReductionCertificate


def bracket(space: JetSpace, first: PointGenerator, second: PointGenerator) -> PointGenerator:
    """Compute the point-vector-field bracket in canonical component order."""
    if first.p != space.p or second.p != space.p or first.q != space.q or second.q != space.q:
        raise ValueError("generator dimensions do not match jet space")
    coordinates = space.independent_variables + space.dependent_fields
    first_components = first.xi + first.phi
    second_components = second.xi + second.phi
    result = tuple(
        sp.expand(
            sum(
                first_components[index] * sp.diff(second_components[component], coordinates[index])
                - second_components[index] * sp.diff(first_components[component], coordinates[index])
                for index in range(len(coordinates))
            )
        )
        for component in range(len(coordinates))
    )
    return PointGenerator(result[:space.p], result[space.p:])


def orbit_rank(space: JetSpace, generators: Sequence[PointGenerator]) -> int:
    """Return the projected orbit rank of a generator list."""
    if not generators:
        return 0
    if any(item.p != space.p for item in generators):
        raise ValueError("generator dimensions do not match jet space")
    return int(sp.Matrix([item.xi for item in generators]).rank())


def invariant_surface_equations(space: JetSpace, generator: PointGenerator) -> tuple[sp.Expr, ...]:
    """Return the invariant-surface equations `Q^a=0`."""
    return characteristic(space, generator)


def _linear_coordinates(
    target: Sequence[sp.Expr],
    basis: Sequence[PointGenerator],
    variables: Sequence[sp.Expr],
) -> tuple[sp.Expr, ...] | None:
    coefficients = sp.symbols(f"c0:{len(basis)}")
    equations = []
    for component_index, component in enumerate(target):
        difference = sp.expand(
            sum(coefficients[index] * (basis[index].xi + basis[index].phi)[component_index]
                for index in range(len(basis)))
            - component
        )
        if difference == 0:
            continue
        try:
            equations.extend(sp.Poly(difference, *variables).coeffs())
        except sp.PolynomialError:
            equations.append(difference)
    if not equations:
        return tuple(sp.Integer(0) for _ in basis)
    solution = sp.linsolve(equations, *coefficients)
    if solution == sp.EmptySet:
        return None
    values = tuple(next(iter(solution)))
    if any(value.free_symbols & set(coefficients) for value in values):
        return None
    return tuple(sp.simplify(value) for value in values)


def check_lie_closure(space: JetSpace, generators: Sequence[PointGenerator]) -> LieSubalgebra:
    """Check closure and return structure coordinates when polynomially solvable."""
    generators = tuple(generators)
    if not generators:
        raise ValueError("closure requires at least one generator")
    variables = space.independent_variables + space.dependent_fields
    rows = []
    closed = True
    for first_index, first in enumerate(generators):
        row = []
        for second_index, second in enumerate(generators):
            value = bracket(space, first, second)
            coordinates = _linear_coordinates(value.xi + value.phi, generators, variables)
            if coordinates is None:
                closed = False
                coordinates = tuple(sp.nan for _ in generators)
            row.append(coordinates)
        rows.append(tuple(row))
    return LieSubalgebra(
        generators,
        structure_constants=tuple(rows),
        closure_status="closed" if closed else "not-closed",
    )


def _parts(system):
    if isinstance(system, DifferentialSystem):
        return (
            system.jet_space,
            system.equations,
            system.inequations,
            system.assumptions,
            system.fingerprint(),
            "branch-0",
        )
    if isinstance(system, ReducedSystem):
        return (
            system.jet_space,
            system.equations,
            system.inequations,
            system.assumptions,
            fingerprint(system.as_dict()),
            system.source_branch_id,
        )
    raise TypeError("expected DifferentialSystem or ReducedSystem")


def _failure(source_fingerprint: str, branch_id: str, message: str) -> ReductionOutcome:
    return ReductionOutcome(
        None,
        ReductionCertificate(
            source_fingerprint,
            "unsupported",
            branch_id,
            checks=(("reduction", False),),
            message=message,
            configuration_fingerprint=fingerprint({
                "operation": "translation_reduce",
                "source_fingerprint": source_fingerprint,
                "message": message,
            }),
        ),
    )


def translation_reduce(system, generator: PointGenerator) -> ReductionOutcome:
    """Reduce a system by one unit independent-variable translation.

    This first executable reduction intentionally handles only a unit
    translation with zero dependent-field component.  It is composable because
    the result carries its reduced JetSpace and the same operation can be
    applied again.
    """
    space, equations, inequations, assumptions, source_fingerprint, branch_id = _parts(system)
    if generator.p != space.p or generator.q != space.q:
        return _failure(source_fingerprint, branch_id, "generator dimensions do not match system")
    variables = space.independent_variables + space.dependent_fields
    if any(component.free_symbols & set(variables) for component in generator.xi):
        return _failure(source_fingerprint, branch_id, "translation coefficients must be constant")
    if any(component != 0 for component in generator.phi):
        return _failure(source_fingerprint, branch_id, "dependent-field translations are not in the first slice")
    nonzero = [index for index, component in enumerate(generator.xi) if sp.simplify(component) != 0]
    if len(nonzero) != 1 or sp.simplify(abs(generator.xi[nonzero[0]]) - 1) != 0:
        return _failure(source_fingerprint, branch_id, "only one unit translation is supported")
    removed = nonzero[0]
    removed_variable = space.independent_variables[removed]
    if any(expression.has(removed_variable) for expression in (*equations, *inequations, *assumptions)):
        return _failure(source_fingerprint, branch_id, "explicit dependence breaks translation reduction")

    reduced_variables = tuple(
        value for index, value in enumerate(space.independent_variables) if index != removed
    )
    reduced_space = JetSpace(reduced_variables, space.dependent_fields, space.max_order, ranking=space.ranking)
    full_coordinates = jet_coordinates(space)
    reduced_coordinates = jet_coordinates(reduced_space)
    pullback = {removed_variable: sp.Integer(0)}
    for field in range(space.q):
        for index in iter_multi_indices(space.p, space.max_order):
            full_key = (field, index)
            if index[removed] > 0:
                pullback[full_coordinates[full_key]] = sp.Integer(0)
            else:
                reduced_index = tuple(value for position, value in enumerate(index) if position != removed)
                pullback[full_coordinates[full_key]] = reduced_coordinates[(field, reduced_index)]

    reduced_equations = tuple(sp.expand(expression.xreplace(pullback)) for expression in equations)
    reduced_inequations = tuple(sp.expand(expression.xreplace(pullback)) for expression in inequations)
    reduced_assumptions = tuple(sp.expand(expression.xreplace(pullback)) for expression in assumptions)
    guards_ok = all(value != 0 for value in reduced_inequations)
    residuals = tuple(
        sp.simplify(reduced - sp.expand(original.xreplace(pullback)))
        for original, reduced in zip(equations, reduced_equations)
    )
    residuals += tuple(
        sp.simplify(value) for value in reduced_inequations if value == 0
    )
    surface = invariant_surface_equations(space, generator)
    reduction_map = ReductionMap(
        source_fingerprint=source_fingerprint,
        generator=generator,
        quotient_variables=reduced_variables,
        invariant_dependent_coordinates=reduced_space.dependent_fields,
        invariant_surface_equations=surface,
        pullback_rules=tuple(pullback.items()),
        rank_guards=(sp.Integer(1),),
        denominator_guards=(),
    )
    reduced_system = ReducedSystem(
        reduced_space,
        reduced_equations,
        reduced_inequations,
        reduced_assumptions,
        reduction_map,
        source_branch_id=branch_id,
    )
    checks = (
        ("generator_dimensions", True),
        ("pure_unit_translation", True),
        ("explicit_invariance", True),
        ("invariant_surface", bool(surface)),
        ("guard_preservation", guards_ok),
        ("pullback_exact", all(value == 0 for value in residuals)),
    )
    status = "verified" if all(value for _, value in checks) else "unsupported"
    certificate = ReductionCertificate(
        source_fingerprint,
        status,
        branch_id,
        checks=checks,
        residuals=residuals,
        covered_guards=reduced_inequations,
        message="unit independent-variable translation reduction",
        configuration_fingerprint=fingerprint({
            "operation": "translation_reduce",
            "generator": generator.as_dict(),
            "source_fingerprint": source_fingerprint,
        }),
    )
    if status != "verified":
        return ReductionOutcome(None, certificate)
    return ReductionOutcome(reduced_system, certificate)
