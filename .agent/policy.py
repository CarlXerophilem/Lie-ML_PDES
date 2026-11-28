"""Promotion and admission rules for the Cartan-DEC-MiAE research loop.

Scores enter only as observations. The functions below are the gates in
``.agent/WORKFLOW.md``. They return decisions and never read model prose.
"""

from __future__ import annotations

import re

_NUMBER = re.compile(r"-?\d+\.\d+")


def relative_improvement(baseline: float, candidate: float, direction: str) -> float:
    """Fractional improvement of ``candidate`` over ``baseline``.

    ``direction`` is ``min`` when a smaller value is better and ``max`` when
    a larger value is better. A zero baseline has no defined relative gain.
    """
    if baseline == 0:
        raise ValueError("relative gain is undefined for a zero baseline")
    if direction == "min":
        return (baseline - candidate) / baseline
    if direction == "max":
        return (candidate - baseline) / baseline
    raise ValueError(f"unknown direction: {direction}")


def promote(metric, seed_rows, *, primary_metric, direction, min_relative_gain, forbidden_primary):
    """Decide whether a screened idea clears the primary endpoint.

    ``seed_rows`` is a list of ``{"seed", "baseline", "candidate"}`` records.
    Every seed must improve by at least ``min_relative_gain``.
    """
    if metric in forbidden_primary:
        return {"status": "reject", "reason": "forbidden_primary", "gains": []}
    if metric != primary_metric:
        return {"status": "reject", "reason": "not_primary_endpoint", "gains": []}
    if len(seed_rows) < 2:
        return {"status": "reject", "reason": "need_two_seeds", "gains": []}
    gains = []
    seeds = []
    for row in seed_rows:
        seeds.append(row["seed"])
        gains.append(relative_improvement(row["baseline"], row["candidate"], direction))
    if len(set(seeds)) != len(seeds):
        return {"status": "reject", "reason": "duplicate_seed", "gains": gains}
    if all(gain >= min_relative_gain for gain in gains):
        return {"status": "promote", "reason": "seeds_agree", "gains": gains}
    return {"status": "reject", "reason": "seeds_disagree_or_small_gain", "gains": gains}


def ablation_status(relative_drops, *, min_gain, clean_fraction):
    """Label a one-factor ablation suite.

    ``relative_drops`` are fractional worsenings of the primary metric after
    removing one component. A positive drop means the component was helping.
    """
    if not relative_drops:
        return {"status": "partial", "reason": "no_ablations", "helping": 0, "total": 0}
    helping = sum(1 for drop in relative_drops if drop >= min_gain)
    total = len(relative_drops)
    if helping / total >= clean_fraction:
        return {"status": "clean", "reason": "fraction_met", "helping": helping, "total": total}
    return {"status": "partial", "reason": "fraction_missed", "helping": helping, "total": total}


def admit_claim(claim, observations, *, open_reading_ids):
    """Admit a claim only when its numbers point at stored observations."""
    by_id = {item["id"]: item for item in observations}
    missing = [item for item in claim.get("observation_ids", []) if item not in by_id]
    if not claim.get("observation_ids") or missing:
        return {"status": "reject", "reason": "missing_observation"}
    kind = claim["kind"]
    tier = claim["tier"]
    used = [by_id[item] for item in claim["observation_ids"]]
    if kind == "measurement" and any(item["tier"] != tier for item in used):
        return {"status": "reject", "reason": "tier_mismatch"}
    if kind == "quotation" and any(item["tier"] != "quote" for item in used):
        return {"status": "reject", "reason": "quotation_needs_quote_tier"}
    if kind == "mechanism":
        needed = claim.get("requires_open_reading")
        if needed:
            if needed not in open_reading_ids:
                return {"status": "reject", "reason": "unknown_open_reading"}
            resolved = [
                item
                for item in used
                if item.get("resolves") == needed and item["tier"] == tier
            ]
            if not resolved:
                return {"status": "reject", "reason": "open_reading_unresolved"}
    return {"status": "admit", "reason": "observations_present"}


def unbacked_numbers(text, observations):
    """Return decimals in ``text`` that match no observation value."""
    allowed = set()
    for item in observations:
        value = item["value"]
        if isinstance(value, float):
            allowed.add(f"{value:.2f}")
            allowed.add(str(value))
        elif isinstance(value, int):
            allowed.add(str(value))
    return [token for token in _NUMBER.findall(text) if token not in allowed]


def authorize_training(tier, compute_authorization):
    """Return whether a training command may start for this tier."""
    if tier == "quote":
        return {"status": "reject", "reason": "quote_tier_does_not_train"}
    if tier == "smoke" and compute_authorization == "smoke-only":
        return {"status": "allow", "reason": "smoke_budget"}
    if tier == "paper" and compute_authorization == "paper-authorized":
        return {"status": "allow", "reason": "paper_authorized"}
    if tier == "paper" and compute_authorization == "smoke-only":
        return {"status": "reject", "reason": "paper_tier_needs_authorization"}
    return {"status": "reject", "reason": "unknown_authorization"}
