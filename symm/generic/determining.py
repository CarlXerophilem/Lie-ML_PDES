"""Bounded determining-equation construction for the generic kernel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from .backend import ResourceLimits
from .core import DifferentialSystem, PointGenerator, VALID_STATUSES
from .completion import expression_node_count
from .jets import prolonged_system


@dataclass(frozen=True)
class DeterminingOutcome:
    system_fingerprint: str
    generator: PointGenerator
    equations: tuple[sp.Expr, ...]
    status: str
    checks: tuple[tuple[str, bool], ...]
    branch_id: str = "branch-0"
    message: str = ""

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"invalid determining status: {self.status}")
        object.__setattr__(self, "equations", tuple(sp.sympify(value) for value in self.equations))
        object.__setattr__(self, "checks", tuple((str(k), bool(v)) for k, v in self.checks))

    @property
    def all_checks_pass(self) -> bool:
        return bool(self.checks) and all(value for _, value in self.checks)

    def as_dict(self) -> dict[str, Any]:
        return {
            "system_fingerprint": self.system_fingerprint,
            "generator": self.generator.as_dict(),
            "equations": [sp.srepr(value) for value in self.equations],
            "status": self.status,
            "checks": list(self.checks),
            "branch_id": self.branch_id,
            "message": self.message,
        }


def determining_equations(
    system: DifferentialSystem,
    generator: PointGenerator,
    *,
    limits: ResourceLimits | None = None,
    branch_id: str = "branch-0",
) -> DeterminingOutcome:
    """Apply the prolonged generator to each equation.

    This returns raw bounded residuals.  Branch normal-form reduction and
    splitting over parametric jets are deliberately marked partial until a
    differential-algebra backend provides those operations.
    """
    limits = limits or ResourceLimits()
    if generator.p != system.p or generator.q != system.q:
        return DeterminingOutcome(
            system.fingerprint(), generator, (), "unsupported",
            (("generator_dimensions", False),), branch_id,
            "generator dimensions do not match system",
        )
    try:
        equations = prolonged_system(system, generator)
    except Exception as exc:
        return DeterminingOutcome(
            system.fingerprint(), generator, (), "unsupported",
            (("prolongation", False),), branch_id,
            f"prolongation failed: {type(exc).__name__}: {exc}",
        )
    within_budget = expression_node_count(equations) <= limits.max_expression_nodes
    checks = (
        ("generator_dimensions", True),
        ("prolongation", True),
        ("expression_budget", within_budget),
        ("branch_normal_form", False),
        ("parametric_jet_split", False),
    )
    return DeterminingOutcome(
        system.fingerprint(), generator, equations if within_budget else (),
        "branch-partial" if within_budget else "unsupported",
        checks, branch_id,
        "raw prolonged residuals; differential normal-form splitting is unavailable",
    )


def verify_off_shell_residuals(
    system: DifferentialSystem,
    generator: PointGenerator,
) -> DeterminingOutcome:
    """Verify the stronger exact off-shell identity for a candidate generator."""
    outcome = determining_equations(system, generator)
    if outcome.status == "unsupported":
        return outcome
    residuals_zero = all(sp.simplify(value) == 0 for value in outcome.equations)
    checks = (
        ("generator_dimensions", True),
        ("prolongation", True),
        ("expression_budget", True),
        ("off_shell_residuals", residuals_zero),
    )
    return DeterminingOutcome(
        outcome.system_fingerprint,
        outcome.generator,
        outcome.equations,
        "verified" if residuals_zero else "unsupported",
        checks,
        outcome.branch_id,
        "exact off-shell prolongation residual check",
    )
