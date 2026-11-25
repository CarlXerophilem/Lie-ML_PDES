#!/usr/bin/env python3
"""Compatible material equation M: derived generators, first integral, written verifier.

P and M stay separate. The scaling generator passed to the first-integral
check is the extra vector in the derived generic basis, after the three translations.
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


def _polynomial_span(classification):
    from reproduce_sve2026 import u
    from lie_reduce.models import scalar
    from lie_reduce.run import span_equal

    rows = []
    for exponent, key in ((1, "m"), (2, "m"), (3, "3"), (4, "m")):
        spec, basis = scalar("M", exponent)
        coords = spec.jets.independent + spec.jets.dependent
        derived = [tuple(component.subs(u, coords[2]) for component in generator)
                   for generator in classification["bases"][key]]
        equal = bool(span_equal(list(basis.values()), derived, coords))
        rows.append({"exponent": exponent, "stratum": key, "span_equal": equal, "labels": list(basis)})
        if not equal:
            raise ArithmeticError("degree-1 labels do not span the smooth M basis")
    return rows


def written_verifier(reductions, integral):
    reasons = []
    for name, record in reductions.items():
        verdict = (record.get("verification") or {}).get("status")
        if record.get("status") != "computed" or verdict != "verified_local_identities":
            reasons.append({"id": name, "status": record.get("status"), "verifier": verdict})
    if "V" not in integral.get("bindings", {}) or not integral.get("first_integral"):
        reasons.append("material first integral")
    return {
        "status": "passed" if not reasons else "failed",
        "reasons": reasons,
        "checker": "delivery/independent_verifier.py through lie_pde_reducer.verifier; first integral from symbolic_sve2026.material_scaling",
    }


def main():
    from lie_pde_reducer import reduction
    from symbolic_sve2026 import classify, material_scaling

    classification = classify("M")
    scaling, = classification["bases"]["m"][3:]
    integral = material_scaling(scaling)
    reductions = {
        "scaling_m2": reduction("M", 2, "Y4"),
        "tilted_m2": reduction("M", 2, "tilted"),
        "cubic_m3": reduction("M", 3, "Y5"),
    }
    verdict = written_verifier(reductions, integral)
    report = {
        "model": "M",
        "search_class": "Unrestricted smooth point generators on phi_t, phi_s, g, kappa>0, real m>=1. Degree-1 polynomial labels are an integer audit.",
        "chart": "phi_t>0, phi_s>0, g,kappa>0",
        "derived": _publish(classification),
        "polynomial_labels_span_smooth_basis": _polynomial_span(classification),
        "material_scaling": integral,
        "reductions": reductions,
        "written_verifier": verdict,
        "not_claimed": "No continuation from the printed scalar P into M.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
