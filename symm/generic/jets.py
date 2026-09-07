"""Lazy multi-index jets, total derivatives, and point prolongation."""

from __future__ import annotations

from itertools import product
import math
from typing import Iterator, Mapping

import sympy as sp

from .core import DifferentialSystem, JetSpace, PointGenerator


class JetOrderLimitError(ValueError):
    """A requested derivative exceeds the configured finite jet space."""


def iter_multi_indices(
    dimensions: int,
    max_order: int,
    min_order: int = 0,
) -> Iterator[tuple[int, ...]]:
    """Yield multi-indices once, in degree then lexicographic order."""
    dimensions = int(dimensions)
    max_order = int(max_order)
    min_order = int(min_order)
    if dimensions <= 0 or max_order < 0 or min_order < 0 or min_order > max_order:
        raise ValueError("invalid multi-index bounds")
    for order in range(min_order, max_order + 1):
        for index in product(range(order + 1), repeat=dimensions):
            if sum(index) == order:
                yield index


def multi_index_count(dimensions: int, max_order: int, min_order: int = 0) -> int:
    """Return the number of multi-indices without materializing them."""
    if min_order == 0:
        return math.comb(int(dimensions) + int(max_order), int(max_order))
    return sum(math.comb(int(dimensions) + order - 1, order)
               for order in range(int(min_order), int(max_order) + 1))


def jet_coordinates(space: JetSpace, order: int | None = None) -> dict[tuple[int, tuple[int, ...]], sp.Expr]:
    """Materialize the bounded coordinate map for a requested order."""
    limit = space.max_order if order is None else int(order)
    if limit < 0 or limit > space.max_order:
        raise JetOrderLimitError("requested jet coordinate order exceeds budget")
    return {
        (field, index): space.jet_symbol(field, index)
        for field in range(space.q)
        for index in iter_multi_indices(space.p, limit)
    }


def _raise_if_order_exceeded(index: tuple[int, ...], limit: int) -> None:
    if sum(index) > limit:
        raise JetOrderLimitError(
            f"total derivative needs order {sum(index)}, configured order is {limit}"
        )


def total_derivative(
    space: JetSpace,
    expression,
    variable_index: int,
    *,
    order: int | None = None,
    coordinates: Mapping[tuple[int, tuple[int, ...]], sp.Expr] | None = None,
) -> sp.Expr:
    """Apply one total derivative without silently dropping a jet term."""
    index = int(variable_index)
    limit = space.max_order if order is None else int(order)
    if not 0 <= index < space.p:
        raise ValueError("variable index outside jet space")
    if limit < 0 or limit > space.max_order:
        raise JetOrderLimitError("requested derivative order exceeds budget")
    coords = jet_coordinates(space, limit) if coordinates is None else coordinates
    expression = sp.sympify(expression)
    result = sp.diff(expression, space.independent_variables[index])
    for (field, multi_index), symbol in coords.items():
        partial = sp.diff(expression, symbol)
        if partial == 0:
            continue
        next_index = list(multi_index)
        next_index[index] += 1
        next_index = tuple(next_index)
        _raise_if_order_exceeded(next_index, limit)
        result += partial * coords[(field, next_index)]
    return sp.expand(result)


def total_derivative_multi(
    space: JetSpace,
    expression,
    multi_index: tuple[int, ...],
    *,
    order: int | None = None,
) -> sp.Expr:
    """Apply `D_J` in a deterministic order."""
    index = tuple(int(value) for value in multi_index)
    if len(index) != space.p or any(value < 0 for value in index):
        raise ValueError("invalid total-derivative multi-index")
    limit = space.max_order if order is None else int(order)
    result = sp.sympify(expression)
    for variable_index, count in enumerate(index):
        for _ in range(count):
            result = total_derivative(space, result, variable_index, order=limit)
    return result


def _unit(index: int, dimensions: int) -> tuple[int, ...]:
    return tuple(1 if i == index else 0 for i in range(dimensions))


def _subtract_unit(index: tuple[int, ...], variable: int) -> tuple[int, ...]:
    result = list(index)
    result[variable] -= 1
    return tuple(result)


def _validate_generator(space: JetSpace, generator: PointGenerator) -> None:
    if generator.p != space.p or generator.q != space.q:
        raise ValueError("generator dimensions do not match jet space")


def characteristic(space: JetSpace, generator: PointGenerator) -> tuple[sp.Expr, ...]:
    """Return `Q^a = phi^a - xi^i u^a_i`."""
    _validate_generator(space, generator)
    if space.max_order < 1:
        raise JetOrderLimitError("characteristics require first-order jets")
    return tuple(
        sp.expand(
            generator.phi[field]
            - sum(
                generator.xi[index] * space.jet_symbol(field, _unit(index, space.p))
                for index in range(space.p)
            )
        )
        for field in range(space.q)
    )


def prolong_recursive(
    space: JetSpace,
    generator: PointGenerator,
    order: int | None = None,
) -> dict[tuple[int, tuple[int, ...]], sp.Expr]:
    """Compute point prolongation coefficients by the recurrence formula."""
    _validate_generator(space, generator)
    limit = space.max_order if order is None else int(order)
    if limit < 0 or limit > space.max_order:
        raise JetOrderLimitError("requested prolongation order exceeds budget")
    coordinates = jet_coordinates(space, limit)
    coefficients: dict[tuple[int, tuple[int, ...]], sp.Expr] = {
        (field, (0,) * space.p): generator.phi[field]
        for field in range(space.q)
    }
    for degree in range(1, limit + 1):
        for index in iter_multi_indices(space.p, degree, degree):
            variable = next(i for i, value in enumerate(index) if value)
            previous = _subtract_unit(index, variable)
            for field in range(space.q):
                value = total_derivative(
                    space,
                    coefficients[(field, previous)],
                    variable,
                    order=limit,
                    coordinates=coordinates,
                )
                for independent_index in range(space.p):
                    shifted = list(previous)
                    shifted[independent_index] += 1
                    value -= (
                        coordinates[(field, tuple(shifted))]
                        * total_derivative(
                            space,
                            generator.xi[independent_index],
                            variable,
                            order=limit,
                            coordinates=coordinates,
                        )
                    )
                coefficients[(field, index)] = sp.expand(value)
    return coefficients


def prolong_characteristic(
    space: JetSpace,
    generator: PointGenerator,
    order: int | None = None,
) -> dict[tuple[int, tuple[int, ...]], sp.Expr]:
    """Compute point prolongation coefficients from the characteristic form."""
    _validate_generator(space, generator)
    limit = space.max_order if order is None else int(order)
    if limit < 0 or limit > space.max_order:
        raise JetOrderLimitError("requested prolongation order exceeds budget")
    # Q contains first jets. Forming D_J(Q) for |J|=n temporarily needs
    # order n+1 coordinates; the highest-order terms cancel against the
    # xi^i*u_(J+e_i) term for a point generator.
    working_space = JetSpace(
        space.independent_variables,
        space.dependent_fields,
        limit + 1,
        ranking=space.ranking,
    )
    coordinates = jet_coordinates(working_space, limit + 1)
    qualities = characteristic(working_space, generator) if limit >= 1 else generator.phi
    coefficients: dict[tuple[int, tuple[int, ...]], sp.Expr] = {}
    zero = (0,) * space.p
    for field in range(space.q):
        coefficients[(field, zero)] = generator.phi[field]
        for degree in range(1, limit + 1):
            for index in iter_multi_indices(space.p, degree, degree):
                value = total_derivative_multi(
                    working_space, qualities[field], index, order=limit + 1
                )
                value += sum(
                    generator.xi[variable]
                    * coordinates[(field, tuple(
                        index[j] + (1 if j == variable else 0)
                        for j in range(space.p)
                    ))]
                    for variable in range(space.p)
                )
                value = sp.expand(value)
                if any(
                    value.has(symbol)
                    for (candidate_field, candidate_index), symbol in coordinates.items()
                    if sum(candidate_index) > limit
                ):
                    raise JetOrderLimitError(
                        "characteristic prolongation retained an out-of-budget jet"
                    )
                coefficients[(field, index)] = value
    return coefficients


def prolongation(
    space: JetSpace,
    generator: PointGenerator,
    order: int | None = None,
    *,
    form: str = "recursive",
) -> dict[tuple[int, tuple[int, ...]], sp.Expr]:
    """Dispatch to one of the two equivalent prolongation implementations."""
    if form == "recursive":
        return prolong_recursive(space, generator, order)
    if form == "characteristic":
        return prolong_characteristic(space, generator, order)
    raise ValueError("form must be 'recursive' or 'characteristic'")


def prolonged_action(
    space: JetSpace,
    expression,
    generator: PointGenerator,
    order: int | None = None,
    *,
    form: str = "recursive",
) -> sp.Expr:
    """Apply `pr(X)` to one jet-space expression."""
    limit = space.max_order if order is None else int(order)
    coordinates = jet_coordinates(space, limit)
    coefficients = prolongation(space, generator, limit, form=form)
    expression = sp.sympify(expression)
    result = sum(
        generator.xi[index] * sp.diff(expression, space.independent_variables[index])
        for index in range(space.p)
    )
    result += sum(
        generator.phi[field] * sp.diff(expression, space.dependent_fields[field])
        for field in range(space.q)
    )
    for key, symbol in coordinates.items():
        # The zero-order field coefficient is already included above.
        if not any(key[1]):
            continue
        partial = sp.diff(expression, symbol)
        if partial != 0:
            result += coefficients[key] * partial
    return sp.expand(result)


def prolonged_system(
    system: DifferentialSystem,
    generator: PointGenerator,
    *,
    form: str = "recursive",
) -> tuple[sp.Expr, ...]:
    """Apply a point generator to every equation in a system."""
    return tuple(
        prolonged_action(system.jet_space, equation, generator, form=form)
        for equation in system.equations
    )
