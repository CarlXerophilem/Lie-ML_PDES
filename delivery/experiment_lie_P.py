#!/usr/bin/env python3
"""Printed scalar P: derived generators, paper-list span check, written verifier.

reproduce_sve2026.generators is the printed v3 list. This script does not use
that list as the solver. It checks that the list spans the bases derived by
symbolic_sve2026.classify.
"""
import json


def _publish(result):
    return {
        "exceptional_exponents": [str(value) for value in result["exceptional_exponents"]],
        "affine_coordinates": list(result["affine_coordinates"]),
        "determining_splits": result["determining_splits"],
        "bases": {
            key: [[str(component) for component in generator] for generator in basis]
            for key, basis in result["bases"].items()
        },
    }


def _paper_span(classification):
    from reproduce_sve2026 import generators, t, s, u
    from lie_reduce.run import span_equal

    listed = generators()
    coords = (t, s, u)
    groups = {
        "m": ("X1", "X2", "X3", "X4"),
        "1": ("X1", "X2", "X3", "X4", "X6"),
        "3": ("X1", "X2", "X3", "X4", "X5"),
    }
    rows = []
    for key, names in groups.items():
        equal = bool(span_equal(classification["bases"][key], [listed[name] for name in names], coords))
        rows.append({"stratum": key, "printed_names": list(names), "span_equal": equal})
        if not equal:
            raise ArithmeticError("printed P list does not span the derived basis at " + key)
    return rows


def _polynomial_span(classification):
    from reproduce_sve2026 import u
    from lie_reduce.models import scalar
    from lie_reduce.run import span_equal

    rows = []
    for exponent, key in ((1, "1"), (2, "m"), (3, "3"), (4, "m")):
        spec, basis = scalar("P", exponent)
        coords = spec.jets.independent + spec.jets.dependent
        derived = [tuple(component.subs(u, coords[2]) for component in generator)
                   for generator in classification["bases"][key]]
        equal = bool(span_equal(list(basis.values()), derived, coords))
        rows.append({"exponent": exponent, "stratum": key, "span_equal": equal, "labels": list(basis)})
        if not equal:
            raise ArithmeticError("degree-1 labels do not span the smooth P basis")
    return rows


def written_verifier(reductions):
    reasons = []
    required = ("scaling_m2", "cubic_m3")
    for name in required:
        record = reductions[name]
        verdict = (record.get("verification") or {}).get("status")
        if record.get("status") != "computed" or verdict != "verified_local_identities":
            reasons.append({"id": name, "status": record.get("status"), "verifier": verdict})
    rejected = reductions["vertical_time_shift_m1"]
    if rejected.get("status") != "no invariant graph":
        reasons.append({"id": "vertical_time_shift_m1", "status": rejected.get("status")})
    return {
        "status": "passed" if not reasons else "failed",
        "reasons": reasons,
        "checker": "delivery/independent_verifier.py through lie_pde_reducer.verifier",
    }


def main():
    from lie_pde_reducer import reduction
    from symbolic_sve2026 import classify

    classification = classify("P")
    reductions = {
        "scaling_m2": reduction("P", 2, "Y4"),
        "cubic_m3": reduction("P", 3, "Y5"),
        "vertical_time_shift_m1": reduction("P", 1, "Y6"),
    }
    verdict = written_verifier(reductions)
    report = {
        "model": "P",
        "search_class": "Unrestricted smooth point generators on phi_t, phi_s, g, kappa>0, real m>=1. Degree-1 polynomial labels are an integer audit.",
        "chart": "phi_t>0, phi_s>0, g,kappa>0",
        "derived": _publish(classification),
        "printed_list_spans_derived_basis": _paper_span(classification),
        "polynomial_labels_span_smooth_basis": _polynomial_span(classification),
        "reductions": reductions,
        "written_verifier": verdict,
        "not_claimed": "No continuation from P to the compatible material equation M.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
