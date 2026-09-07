"""Bounded local completion boundary.

SymPy is useful for exact local identities, but it is not treated as a
differential Thomas/Rosenfeld oracle.  This module records the input as a
partial formal branch and exposes the resource checks needed before invoking a
licensed external backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from .backend import ResourceLimits
from .core import (
    CompletionCertificate,
    DifferentialBranch,
    DifferentialSystem,
    configuration_fingerprint,
)


def expression_node_count(expressions: tuple[sp.Expr, ...] | list[sp.Expr]) -> int:
    """Return a conservative deterministic expression-size estimate."""
    return sum(int(sp.count_ops(sp.sympify(expression), visual=False)) + 1
               for expression in expressions)


@dataclass(frozen=True)
class CompletionOutcome:
    certificate: CompletionCertificate
    configuration_fingerprint: str


def bounded_completion(
    system: DifferentialSystem,
    *,
    limits: ResourceLimits | None = None,
    backend: str = "python-fallback",
) -> CompletionOutcome:
    """Record a bounded fallback branch without claiming completion.

    The original equations, inequations, assumptions, and ranking all survive
    unchanged.  In particular, a parameter equation such as ``a*u_t-u_x`` is
    never divided by ``a`` and therefore does not lose its singular branch.
    """
    limits = limits or ResourceLimits()
    configuration = {
        "backend": backend,
        "limits": limits.as_dict(),
        "system_fingerprint": system.fingerprint(),
    }
    expressions = (*system.equations, *system.inequations, *system.assumptions)
    node_count = expression_node_count(expressions)
    within_budget = system.jet_space.max_order <= limits.max_jet_order
    within_budget = within_budget and node_count <= limits.max_expression_nodes
    branch = DifferentialBranch(
        equations=system.equations,
        inequations=system.inequations,
        assumptions=system.assumptions,
        ranking=system.jet_space.ranking,
        branch_id="fallback-input",
        status="branch-partial",
        semantic_scope="formal-input-preserving; not-completed",
        provenance=(
            ("backend", backend),
            ("configuration_fingerprint", configuration_fingerprint(configuration)),
            ("expression_nodes", str(node_count)),
        ),
    )
    checks = (
        ("input_equations_preserved", branch.equations == system.equations),
        ("input_inequations_preserved", branch.inequations == system.inequations),
        ("input_assumptions_preserved", branch.assumptions == system.assumptions),
        ("resource_budget", within_budget),
        ("completion_proved", False),
    )
    status = "branch-partial" if within_budget else "unsupported"
    message = (
        "local fallback preserves one input branch; differential completion "
        "requires a proof-producing backend"
        if within_budget else
        "local fallback refused the input because a configured resource cap was exceeded"
    )
    certificate = CompletionCertificate(
        system.fingerprint(),
        status,
        (branch,),
        system.jet_space.ranking,
        checks=checks,
        message=message,
        backend=backend,
        configuration_fingerprint=configuration_fingerprint(configuration),
    )
    return CompletionOutcome(certificate, configuration_fingerprint(configuration))


local_completion = bounded_completion
