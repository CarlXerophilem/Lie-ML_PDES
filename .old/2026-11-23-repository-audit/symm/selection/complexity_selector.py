"""Measured cost crossings; unknown mathematical quantities stay unknown."""
from __future__ import annotations
from dataclasses import dataclass
from math import ceil, floor, isfinite
from typing import Any


@dataclass(frozen=True)
class ComplexityRecord:
    independent_variables: int
    profile_fields: int
    actual_order: int
    residual_count: int
    chart_margin: float | None
    leading_margin: float | None
    stability_constant: float | None = None
    approximation_bound: float | None = None
    evidence_scope: str = "sampled margins; conditional accuracy"


def choose_minimum_cost(candidates: list[dict[str, Any]], queries: int) -> dict[str, Any]:
    """Minimize measured total work after the caller's accuracy/model gates."""
    if not isinstance(queries, int) or queries < 0:
        raise ValueError("query count must be a nonnegative integer")
    admissible = []
    for candidate in candidates:
        if not candidate["admissible"]:
            continue
        setup, query = candidate["setup_seconds"], candidate["query_seconds"]
        if not all(isfinite(v) and v >= 0 for v in (setup, query)):
            raise ValueError("candidate costs must be finite and nonnegative")
        admissible.append({**candidate, "total_seconds": setup+queries*query})
    ranked = sorted(admissible, key=lambda row: (row["total_seconds"], row["id"]))
    return {"queries": queries, "status": "selected" if ranked else "no-admissible-candidate",
            "selected": ranked[0] if ranked else None, "ranked": ranked,
            "scope": "measured costs and caller-supplied admissibility; no stability theorem"}


def cost_crossing(neural_setup: float, classical_setup: float, neural_query: float,
                  classical_query: float, *, admissible: bool = True) -> dict:
    if not all(isfinite(v) for v in (neural_setup,classical_setup,neural_query,classical_query)) or min(neural_setup, classical_setup, neural_query, classical_query) < 0:
        raise ValueError("costs must be nonnegative")
    if not admissible:
        return {"status": "accuracy-inadmissible", "N_break": None, "asymptotic_speedup": False}
    difference = classical_query-neural_query
    overhead = neural_setup-classical_setup
    if difference > 0:
        count = max(0, ceil(overhead/difference))
        # Correct floating-rounding at an integer boundary using the cost inequality.
        while neural_setup+count*neural_query > classical_setup+count*classical_query:
            count += 1
        return {"status": "amortizable", "N_break": count, "asymptotic_speedup": True}
    if difference == 0:
        return {"status": "equal-query-cost", "N_break": 0 if overhead <= 0 else None,
                "asymptotic_speedup": False}
    last = floor(overhead/difference) if overhead <= 0 else None
    return {"status": "finite-advantage-only" if last is not None else "classical-dominates",
            "N_break": 0 if last is not None else None, "last_advantage_query": last,
            "asymptotic_speedup": False}
