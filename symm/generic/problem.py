"""A PDE problem separates equations, fixed parameters, domain and data.

All expressions are symbolic; no sampling distribution is part of this
mathematical input. Inequations in DifferentialSystem mean nonzero, whereas
domain predicates retain signs and real-branch conditions.
"""

from dataclasses import dataclass

import sympy as sp
from sympy.core.relational import Relational
from sympy.logic.boolalg import Boolean

from .core import DifferentialSystem, GenericValidationError, fingerprint
from .jets import jet_coordinates


@dataclass(frozen=True)
class DataCondition:
    """Residuals vanish on a supplied base hypersurface `surface = 0`."""

    name: str
    surface: sp.Expr
    residuals: tuple[sp.Expr, ...]

    def __post_init__(self):
        if not self.name or not self.residuals:
            raise GenericValidationError("data need a name and at least one residual")
        object.__setattr__(self, "surface", sp.sympify(self.surface))
        object.__setattr__(self, "residuals", tuple(map(sp.sympify, self.residuals)))
        if any(not isinstance(e, sp.Expr) for e in (self.surface, *self.residuals)):
            raise GenericValidationError("data surface and residuals must be expressions")

    def as_dict(self):
        return {"name": self.name, "surface": sp.srepr(self.surface),
                "residuals": list(map(sp.srepr, self.residuals))}


@dataclass(frozen=True)
class PDEProblem:
    system: DifferentialSystem
    parameters: tuple[sp.Symbol, ...] = ()
    domain: tuple[sp.Basic, ...] = ()
    data: tuple[DataCondition, ...] = ()

    def __post_init__(self):
        parameters = tuple(map(sp.sympify, self.parameters))
        domain = tuple(map(sp.sympify, self.domain))
        data = tuple(self.data)
        space = self.system.jet_space
        # Prevent a large implicit coordinate allocation at the formalization boundary.
        from .jets import multi_index_count
        if space.q * multi_index_count(space.p, space.max_order) > 1000:
            raise GenericValidationError("jet coordinate budget exceeds 1000")
        coordinates = set(jet_coordinates(space).values())
        base = set(space.independent_variables)
        if not all(isinstance(s, sp.Symbol) for s in (*base, *coordinates, *parameters)):
            raise GenericValidationError("coordinates and parameters must be symbols")
        if len(parameters) != len(set(parameters)) or set(parameters) & (base | coordinates):
            raise GenericValidationError("parameters must be unique and disjoint from coordinates")
        if len(coordinates) != space.q * multi_index_count(space.p, space.max_order) or base & coordinates:
            raise GenericValidationError("canonical jet names collide with coordinates")
        allowed = base | coordinates | set(parameters)
        expressions = (*self.system.equations, *self.system.inequations,
                       *self.system.assumptions, *domain)
        if any(not isinstance(e, sp.Expr) for e in (*self.system.equations, *self.system.inequations)):
            raise GenericValidationError("equations and inequations must be residual expressions")
        if any(not isinstance(e, Boolean) or isinstance(e, sp.Expr)
               for e in (*domain, *self.system.assumptions)):
            raise GenericValidationError("domain and assumptions must be Boolean predicates")
        for condition in data:
            if condition.surface.free_symbols - base - set(parameters):
                raise GenericValidationError("data surfaces must depend only on base coordinates and parameters")
            expressions += (condition.surface, *condition.residuals)
        for expression in expressions:
            unknown = expression.free_symbols - allowed
            if unknown:
                raise GenericValidationError(f"undeclared symbols or out-of-order jets: {unknown}")
            if expression.has(sp.Derivative):
                raise GenericValidationError("use canonical jet symbols instead of unevaluated derivatives")
        if len({condition.name for condition in data}) != len(data):
            raise GenericValidationError("data names must be unique")
        object.__setattr__(self, "parameters", parameters)
        object.__setattr__(self, "domain", domain)
        object.__setattr__(self, "data", data)

    @property
    def jet_structure(self) -> tuple[str, ...]:
        jets = tuple(jet_coordinates(self.system.jet_space).values())
        result = []
        for equation in self.system.equations:
            if equation.is_polynomial(*jets):
                result.append("polynomial")
            else:
                numerator, denominator = sp.together(equation).as_numer_denom()
                rational = numerator.is_polynomial(*jets) and denominator.is_polynomial(*jets)
                result.append("rational" if rational else "nonpolynomial")
        return tuple(result)

    @property
    def denominator_guards(self) -> tuple[sp.Expr, ...]:
        expressions = (*self.system.equations, *self.system.inequations,
                       *(e for d in self.data for e in (d.surface, *d.residuals)))
        expressions += tuple(side for condition in (*self.domain, *self.system.assumptions)
                             for relation in condition.atoms(Relational)
                             for side in (relation.lhs, relation.rhs))
        return tuple(dict.fromkeys(sp.denom(sp.together(e)) for e in expressions
                                   if sp.denom(sp.together(e)) != 1))

    def as_dict(self):
        return {"system": self.system.as_dict(),
                "parameters": list(map(sp.srepr, self.parameters)),
                "domain": list(map(sp.srepr, self.domain)),
                "data": [item.as_dict() for item in self.data]}

    def fingerprint(self):
        return fingerprint(self.as_dict())
