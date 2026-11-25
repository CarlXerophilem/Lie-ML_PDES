#!/usr/bin/env python3
"""E1 experiment: smooth classification, derived X_i, and the written verifier.

The named generators come from the degree-1 determining kernel. That finite
search does not replace the unrestricted smooth proof for every real m>=1.
"""
import json


def written_verifier(reductions):
    """Require the independent checker to accept each emitted quotient."""
    reasons = []
    for name, record in reductions.items():
        verdict = (record.get("verification") or {}).get("status")
        if record.get("status") != "computed" or verdict != "verified_local_identities":
            reasons.append({"id": name, "status": record.get("status"), "verifier": verdict})
    return {
        "status": "passed" if not reasons else "failed",
        "reasons": reasons,
        "checker": "delivery/independent_verifier.py through lie_pde_reducer.verifier",
    }


def main():
    from symbolic_sv2022 import run as smooth_run
    from lie_pde_reducer import reduction
    from lie_reduce.models import euler

    bases = {}
    for exponent in (1, 2, 3, 4):
        _spec, basis = euler(exponent)
        bases[str(exponent)] = {
            "search_class": "polynomial point coefficients of degree at most 1",
            "dimension": len(basis),
            "generators": {name: [str(component) for component in vector] for name, vector in basis.items()},
        }
    reductions = {
        "bed_drift_m2": reduction("E1", 2, "bed_drift"),
        "cubic_scaling_m3": reduction("E1", 3, "X5"),
    }
    verdict = written_verifier(reductions)
    report = {
        "model": "E1",
        "search_class": "Unrestricted smooth point symmetries for all real m>=1, plus a separate degree-1 polynomial audit at m=1,2,3,4.",
        "chart": "h,u,g,K>0",
        "smooth_classification": smooth_run(),
        "polynomial_bases": bases,
        "reductions": reductions,
        "written_verifier": verdict,
        "not_claimed": "The integer polynomial audit is not the all-real-m classification.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
