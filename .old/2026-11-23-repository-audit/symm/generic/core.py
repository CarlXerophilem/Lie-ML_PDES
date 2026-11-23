"""Canonical data model for multi-field, multi-variable PDE systems.

The legacy scalar engine remains separate.  This module owns normalized
metadata, fingerprints, and certificate records used by the generic path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Iterable

import sympy as sp


VALID_STATUSES = frozenset(
    {
        "verified",
        "branch-partial",
        "backend-unavailable",
        "timeout",
        "unsupported",
        "inconsistent",
        "oracle-disagreement",
        "error",
    }
)

LegacyStatus = frozenset({"CERTIFIED", "PARTIAL", "LATENT-ONLY"})
JetKey = tuple[int, tuple[int, ...]]


class GenericValidationError(ValueError):
    """Raised when a canonical object violates its dimensional contract."""


def _expr(value: Any) -> sp.Expr:
    return sp.sympify(value)


def expression_repr(value: Any) -> str:
    return sp.srepr(_expr(value))


def _tuple_expr(values: Iterable[Any]) -> tuple[sp.Expr, ...]:
    return tuple(_expr(value) for value in values)


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.Basic):
        return {"sympy": sp.srepr(value)}
    if isinstance(value, dict):
        return {str(k): _json_value(v) for k, v in sorted(value.items(), key=lambda x: str(x[0]))}
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    if isinstance(value, set):
        return sorted(_json_value(item) for item in value)
    if hasattr(value, "as_dict"):
        return value.as_dict()
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_json_value(value), sort_keys=True, separators=(",", ":"))


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def configuration_fingerprint(value: Any) -> str:
    """Hash a normalized execution configuration separately from a system."""
    return fingerprint({"configuration": value})


@dataclass(frozen=True)
class DifferentialRanking:
    """Deterministic ranking metadata, independent of a CAS syntax."""

    derivative_order: str = "orderly"
    field_order: tuple[int, ...] = ()
    tie_break: str = "lex"
    differentiation_compatible: bool = True

    def __post_init__(self) -> None:
        if self.derivative_order not in {"orderly", "lex", "degree-reverse-lex"}:
            raise GenericValidationError("unsupported derivative ranking")
        if self.tie_break not in {"lex", "reverse-lex"}:
            raise GenericValidationError("unsupported ranking tie-break")
        if any(int(item) < 0 for item in self.field_order):
            raise GenericValidationError("field order must be nonnegative")

    def as_dict(self) -> dict[str, Any]:
        return {
            "derivative_order": self.derivative_order,
            "field_order": list(self.field_order),
            "tie_break": self.tie_break,
            "differentiation_compatible": self.differentiation_compatible,
        }


@dataclass(frozen=True)
class JetSpace:
    independent_variables: tuple[sp.Symbol, ...]
    dependent_fields: tuple[sp.Symbol, ...]
    max_order: int
    ranking: DifferentialRanking = field(default_factory=DifferentialRanking)

    def __post_init__(self) -> None:
        variables = tuple(_expr(item) for item in self.independent_variables)
        fields = tuple(_expr(item) for item in self.dependent_fields)
        if not variables or not fields:
            raise GenericValidationError("a jet space needs variables and fields")
        if len(set(variables)) != len(variables):
            raise GenericValidationError("independent variables must be unique")
        if len(set(fields)) != len(fields):
            raise GenericValidationError("dependent fields must be unique")
        if set(variables) & set(fields):
            raise GenericValidationError("variables and fields must be disjoint")
        if int(self.max_order) < 0:
            raise GenericValidationError("max_order must be nonnegative")
        if self.ranking.field_order and sorted(self.ranking.field_order) != list(range(len(fields))):
            raise GenericValidationError("ranking field_order must be a permutation of fields")
        object.__setattr__(self, "independent_variables", variables)
        object.__setattr__(self, "dependent_fields", fields)
        object.__setattr__(self, "max_order", int(self.max_order))

    @property
    def p(self) -> int:
        return len(self.independent_variables)

    @property
    def q(self) -> int:
        return len(self.dependent_fields)

    def jet_symbol(self, field: int, multi_index: tuple[int, ...]) -> sp.Expr:
        """Return the canonical symbolic coordinate for one jet."""
        if not 0 <= int(field) < self.q:
            raise GenericValidationError("field index outside jet space")
        index = tuple(int(value) for value in multi_index)
        if len(index) != self.p or any(value < 0 for value in index):
            raise GenericValidationError("invalid jet multi-index")
        if sum(index) > self.max_order:
            raise GenericValidationError("jet order exceeds jet space budget")
        base = str(self.dependent_fields[field])
        if not any(index):
            return self.dependent_fields[field]
        suffix = "".join(name * count for name, count in zip(("x", "y", "z", "w"), index))
        if self.p > 4:
            suffix = "_".join(f"x{i}^{value}" for i, value in enumerate(index) if value)
        return sp.Symbol(f"{base}_{suffix}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "independent_variables": [expression_repr(item) for item in self.independent_variables],
            "dependent_fields": [expression_repr(item) for item in self.dependent_fields],
            "max_order": self.max_order,
            "ranking": self.ranking.as_dict(),
        }

    def fingerprint(self) -> str:
        return fingerprint(self.as_dict())


@dataclass(frozen=True)
class DifferentialSystem:
    jet_space: JetSpace
    equations: tuple[sp.Expr, ...]
    inequations: tuple[sp.Expr, ...] = ()
    assumptions: tuple[sp.Expr, ...] = ()
    name: str = "system"

    def __post_init__(self) -> None:
        equations = _tuple_expr(self.equations)
        inequations = _tuple_expr(self.inequations)
        assumptions = _tuple_expr(self.assumptions)
        if not self.name:
            raise GenericValidationError("system name must not be empty")
        object.__setattr__(self, "equations", equations)
        object.__setattr__(self, "inequations", inequations)
        object.__setattr__(self, "assumptions", assumptions)

    @property
    def p(self) -> int:
        return self.jet_space.p

    @property
    def q(self) -> int:
        return self.jet_space.q

    @property
    def r(self) -> int:
        return len(self.equations)

    def as_dict(self) -> dict[str, Any]:
        return {
            "jet_space": self.jet_space.as_dict(),
            "equations": [expression_repr(item) for item in self.equations],
            "inequations": [expression_repr(item) for item in self.inequations],
            "assumptions": [expression_repr(item) for item in self.assumptions],
            "name": self.name,
        }

    def fingerprint(self) -> str:
        return fingerprint(self.as_dict())


@dataclass(frozen=True)
class DifferentialBranch:
    equations: tuple[sp.Expr, ...]
    inequations: tuple[sp.Expr, ...] = ()
    assumptions: tuple[sp.Expr, ...] = ()
    leaders: tuple[JetKey, ...] = ()
    initials: tuple[sp.Expr, ...] = ()
    separants: tuple[sp.Expr, ...] = ()
    parametric_derivatives: tuple[JetKey, ...] = ()
    ranking: DifferentialRanking = field(default_factory=DifferentialRanking)
    branch_id: str = "branch-0"
    status: str = "branch-partial"
    semantic_scope: str = "formal-regular"
    provenance: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise GenericValidationError(f"invalid branch status: {self.status}")
        if not self.branch_id:
            raise GenericValidationError("branch_id must not be empty")
        object.__setattr__(self, "equations", _tuple_expr(self.equations))
        object.__setattr__(self, "inequations", _tuple_expr(self.inequations))
        object.__setattr__(self, "assumptions", _tuple_expr(self.assumptions))
        object.__setattr__(self, "initials", _tuple_expr(self.initials))
        object.__setattr__(self, "separants", _tuple_expr(self.separants))
        object.__setattr__(self, "provenance", tuple((str(k), str(v)) for k, v in self.provenance))

    def as_dict(self) -> dict[str, Any]:
        return {
            "equations": [expression_repr(item) for item in self.equations],
            "inequations": [expression_repr(item) for item in self.inequations],
            "assumptions": [expression_repr(item) for item in self.assumptions],
            "leaders": [[field_index, list(index)] for field_index, index in self.leaders],
            "initials": [expression_repr(item) for item in self.initials],
            "separants": [expression_repr(item) for item in self.separants],
            "parametric_derivatives": [[field_index, list(index)] for field_index, index in self.parametric_derivatives],
            "ranking": self.ranking.as_dict(),
            "branch_id": self.branch_id,
            "status": self.status,
            "semantic_scope": self.semantic_scope,
            "provenance": list(self.provenance),
        }


@dataclass(frozen=True)
class PointGenerator:
    xi: tuple[sp.Expr, ...]
    phi: tuple[sp.Expr, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "xi", _tuple_expr(self.xi))
        object.__setattr__(self, "phi", _tuple_expr(self.phi))
        if not self.xi or not self.phi:
            raise GenericValidationError("a point generator needs xi and phi components")

    @property
    def p(self) -> int:
        return len(self.xi)

    @property
    def q(self) -> int:
        return len(self.phi)

    def as_dict(self) -> dict[str, Any]:
        return {
            "xi": [expression_repr(item) for item in self.xi],
            "phi": [expression_repr(item) for item in self.phi],
        }

    def fingerprint(self) -> str:
        return fingerprint(self.as_dict())


@dataclass(frozen=True)
class LieSubalgebra:
    generators: tuple[PointGenerator, ...]
    structure_constants: tuple[tuple[tuple[sp.Expr, ...], ...], ...] = ()
    closure_status: str = "unverified"

    def __post_init__(self) -> None:
        generators = tuple(self.generators)
        if not generators:
            raise GenericValidationError("a Lie subalgebra needs at least one generator")
        p, q = generators[0].p, generators[0].q
        if any(item.p != p or item.q != q for item in generators):
            raise GenericValidationError("subalgebra generators must have equal dimensions")
        if self.closure_status not in {"closed", "not-closed", "unverified"}:
            raise GenericValidationError("invalid closure status")
        object.__setattr__(self, "generators", generators)

    def as_dict(self) -> dict[str, Any]:
        return {
            "generators": [item.as_dict() for item in self.generators],
            "structure_constants": _json_value(self.structure_constants),
            "closure_status": self.closure_status,
        }


@dataclass(frozen=True)
class ReductionMap:
    source_fingerprint: str
    generator: PointGenerator
    quotient_variables: tuple[sp.Symbol, ...]
    invariant_dependent_coordinates: tuple[sp.Expr, ...]
    invariant_surface_equations: tuple[sp.Expr, ...]
    pullback_rules: tuple[tuple[sp.Expr, sp.Expr], ...]
    reconstruction_rules: tuple[tuple[sp.Expr, sp.Expr], ...] = ()
    rank_guards: tuple[sp.Expr, ...] = ()
    denominator_guards: tuple[sp.Expr, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_fingerprint:
            raise GenericValidationError("source_fingerprint is required")
        object.__setattr__(self, "quotient_variables", tuple(_expr(item) for item in self.quotient_variables))
        object.__setattr__(self, "invariant_dependent_coordinates", _tuple_expr(self.invariant_dependent_coordinates))
        object.__setattr__(self, "invariant_surface_equations", _tuple_expr(self.invariant_surface_equations))
        object.__setattr__(self, "pullback_rules", tuple((_expr(k), _expr(v)) for k, v in self.pullback_rules))
        object.__setattr__(self, "reconstruction_rules", tuple((_expr(k), _expr(v)) for k, v in self.reconstruction_rules))
        object.__setattr__(self, "rank_guards", _tuple_expr(self.rank_guards))
        object.__setattr__(self, "denominator_guards", _tuple_expr(self.denominator_guards))

    def as_dict(self) -> dict[str, Any]:
        pair = lambda values: [[expression_repr(k), expression_repr(v)] for k, v in values]
        return {
            "source_fingerprint": self.source_fingerprint,
            "generator": self.generator.as_dict(),
            "quotient_variables": [expression_repr(item) for item in self.quotient_variables],
            "invariant_dependent_coordinates": [expression_repr(item) for item in self.invariant_dependent_coordinates],
            "invariant_surface_equations": [expression_repr(item) for item in self.invariant_surface_equations],
            "pullback_rules": pair(self.pullback_rules),
            "reconstruction_rules": pair(self.reconstruction_rules),
            "rank_guards": [expression_repr(item) for item in self.rank_guards],
            "denominator_guards": [expression_repr(item) for item in self.denominator_guards],
        }


@dataclass(frozen=True)
class ReducedSystem:
    jet_space: JetSpace
    equations: tuple[sp.Expr, ...]
    inequations: tuple[sp.Expr, ...]
    assumptions: tuple[sp.Expr, ...]
    reduction_map: ReductionMap
    source_branch_id: str = "branch-0"

    def __post_init__(self) -> None:
        object.__setattr__(self, "equations", _tuple_expr(self.equations))
        object.__setattr__(self, "inequations", _tuple_expr(self.inequations))
        object.__setattr__(self, "assumptions", _tuple_expr(self.assumptions))

    def as_dict(self) -> dict[str, Any]:
        return {
            "jet_space": self.jet_space.as_dict(),
            "equations": [expression_repr(item) for item in self.equations],
            "inequations": [expression_repr(item) for item in self.inequations],
            "assumptions": [expression_repr(item) for item in self.assumptions],
            "reduction_map": self.reduction_map.as_dict(),
            "source_branch_id": self.source_branch_id,
        }


@dataclass(frozen=True)
class CompletionCertificate:
    system_fingerprint: str
    status: str
    branches: tuple[DifferentialBranch, ...]
    ranking: DifferentialRanking
    checks: tuple[tuple[str, bool], ...] = ()
    message: str = ""
    backend: str = "python-fallback"
    configuration_fingerprint: str = ""
    schema_version: str = "lieml.generic.certificate/1"

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise GenericValidationError(f"invalid completion status: {self.status}")
        object.__setattr__(self, "branches", tuple(self.branches))
        object.__setattr__(self, "checks", tuple((str(k), bool(v)) for k, v in self.checks))

    def as_dict(self) -> dict[str, Any]:
        return {
            "system_fingerprint": self.system_fingerprint,
            "status": self.status,
            "branches": [item.as_dict() for item in self.branches],
            "ranking": self.ranking.as_dict(),
            "checks": list(self.checks),
            "message": self.message,
            "backend": self.backend,
            "configuration_fingerprint": self.configuration_fingerprint,
            "schema_version": self.schema_version,
        }


@dataclass(frozen=True)
class ReductionCertificate:
    system_fingerprint: str
    status: str
    source_branch_id: str
    checks: tuple[tuple[str, bool], ...]
    residuals: tuple[sp.Expr, ...] = ()
    covered_guards: tuple[sp.Expr, ...] = ()
    uncovered_branches: tuple[str, ...] = ()
    message: str = ""
    configuration_fingerprint: str = ""
    schema_version: str = "lieml.generic.certificate/1"

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise GenericValidationError(f"invalid reduction status: {self.status}")
        object.__setattr__(self, "checks", tuple((str(k), bool(v)) for k, v in self.checks))
        object.__setattr__(self, "residuals", _tuple_expr(self.residuals))
        object.__setattr__(self, "covered_guards", _tuple_expr(self.covered_guards))

    @property
    def all_checks_pass(self) -> bool:
        return bool(self.checks) and all(value for _, value in self.checks)

    def as_dict(self) -> dict[str, Any]:
        return {
            "system_fingerprint": self.system_fingerprint,
            "status": self.status,
            "source_branch_id": self.source_branch_id,
            "checks": list(self.checks),
            "residuals": [expression_repr(item) for item in self.residuals],
            "covered_guards": [expression_repr(item) for item in self.covered_guards],
            "uncovered_branches": list(self.uncovered_branches),
            "message": self.message,
            "configuration_fingerprint": self.configuration_fingerprint,
            "schema_version": self.schema_version,
        }
