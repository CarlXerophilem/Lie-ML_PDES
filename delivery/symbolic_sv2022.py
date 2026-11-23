"""Final expressions for 1+1 Eulerian Grass SVE, g,K,h,u>0 and real m>=1."""
import json
from _eulerian_first_order import (branch_generators, flux_matrix, run_verification,
                                  s, t, x, h, u, B, K, m, g)


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
    assert residual.subs(g,1).applyfunc(s.simplify) == s.Matrix([0,0,slope+K*f.diff(x)])
    weights = s.Matrix([[-1,-1,1],[-1,0,1],[0,2,1]])
    assert weights.det() != 0
    return {
        "scope": "Local smooth point symmetries, all real m>=1, K,g,h,u>0",
        "verified_proof_identities": proof["check_count"],
        "coordinate_order": list(map(str, coordinates)),
        "strata": results,
        "optimal_lines_layout": {
            "names": "T=dt; X=dx; Z=dB; D=t*dt+x*dx; S=t*dt-2h*dh-u*du-2B*dB",
            "generic_scaling": "D+cZ, c real",
            "generic_translations": "RP1 in (T,X); Z; Z+cos(theta)T+sin(theta)X",
            "cubic_scaling": "H=aD+bS, projective (a:b). Normalize a=1 if a!=0, else b=1. For every zero weight in (-(a+b),-a,2b), append c times the corresponding T,X,Z with c=0,+1,-1.",
            "cubic_translations": "Each nonempty support of T,X,Z with unit coefficients; signs modulo global sign."
        },
        "m2_bed_drift_quotient": "K*Y' + b = 0; Y=u^2, h=1/u, B=bt+2-Y/2-h, g=1",
        "m2_remaining_residual": str(s.simplify(residual[2].subs(g,1))),
        "classification_proof": "delivery/derivations/eulerian-first-order.md; range extension and orbits in delivery/VERIFICATION.md",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
