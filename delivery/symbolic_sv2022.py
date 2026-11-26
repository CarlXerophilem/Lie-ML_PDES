"""Final expressions for 1+1 Eulerian Grass SVE, g,K,h,u>0 and real m>=1."""
import json
from _eulerian_first_order import (branch_generators, flux_matrix, run_verification,
                                  s, t, x, h, u, B, K, m, g)


def _require(condition, stage):
    if not condition:
        raise ArithmeticError(stage)


def run():
    proof = run_verification()
    coordinates = (t, x, h, u, B)
    results = {}
    for stratum in ("positive_generic", "positive_cubic"):
        basis = branch_generators(stratum)
        bracket = {}
        for left, v in basis.items():
            for right, w in basis.items():
                value = w.jacobian(coordinates)*v - v.jacobian(coordinates)*w
                if value != s.zeros(5, 1):
                    bracket[f"[{left},{right}]"] = list(map(str, value))
        results[stratum] = {"basis": proof["generators"][stratum], "brackets": bracket}
    f = s.Function("Y")(x)
    slope = s.Symbol("b", real=True)
    profile = (1/s.sqrt(f), s.sqrt(f), slope*t+2-f/2-1/s.sqrt(f))
    residual = s.Matrix(profile).diff(t)+flux_matrix(2*K*s.sqrt(f)).subs(
        {h:profile[0],u:profile[1]})*s.Matrix(profile).diff(x)
    reduced = residual.subs(g, 1).applyfunc(s.simplify)
    _require(reduced[0] == 0 and reduced[1] == 0, "Cartesian bed-drift substitution")
    _require(not reduced[2].has(t), "bed-drift quotient is autonomous")
    weights = s.Matrix([[-1,-1,1],[-1,0,1],[0,2,1]])
    _require(weights.det() != 0, "cubic determining weights")
    return {
        "scope": "Local smooth point symmetries, all real m>=1, K,g,h,u>0",
        "verified_proof_identities": proof["check_count"],
        "coordinate_order": list(map(str, coordinates)),
        "strata": results,
        "m2_bed_drift_profile": {"h": str(profile[0]), "u": str(profile[1]), "B": str(profile[2]), "g": "1"},
        "m2_bed_drift_quotient": str(reduced[2]) + " = 0",
        "classification_proof": "delivery/derivations/eulerian-first-order.md; range extension and orbits in delivery/VERIFICATION.md",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
