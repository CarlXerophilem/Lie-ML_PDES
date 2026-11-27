#!/usr/bin/env python3
"""ML experiment on the material travelling wave, with a written verifier."""

import _bootstrap  # historical standalone script path
import json
import math


def written_verifier(record):
    reasons = []
    if record["fit"].get("interpretation") != "fixed-budget approximation; no convergence claim":
        reasons.append("missing fixed-budget interpretation")
    if record["fit"].get("status") not in ("budget_exhausted", "optimizer_terminated"):
        reasons.append("unexpected optimizer status")
    for method, metrics in record["metrics"].items():
        for key, value in metrics.items():
            if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                reasons.append(f"{method} {key}")
        if method in ("Chebyshev", "Taylor") and metrics["trace_error_maximum"] > 1e-8:
            reasons.append(f"{method} trace error")
    return {
        "status": "passed" if not reasons else "failed",
        "reasons": reasons,
        "checker": "written check of field, residual and trace metrics on the held-out grid",
    }


def main():
    from _profile_learning import compare
    from ml_sve2026 import MATERIAL

    record = compare(MATERIAL)
    verdict = written_verifier(record)
    report = {
        "model": "M",
        "task": MATERIAL.name,
        "search_class": "Reduced travelling wave lifted from compatible M to E1. Printed P is a separate experiment.",
        "record": record,
        "written_verifier": verdict,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
