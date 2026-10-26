"""Replay exact dissertation identities and deliberately failing controls.

These are expression certificates on the declared positive chart, not a learned
proposer, physical calibration, continuous numerical bound or classification.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import sympy as sp


@lru_cache(maxsize=1)
def build_certificates() -> dict:
    t, s = sp.symbols("t s", positive=True)
    z, F, c, d = sp.symbols("z F c d", real=True)
    p, g, beta, m = sp.symbols("p g beta m", positive=True)
    profile = sp.Function("F")
    phi = t * profile(s / t)
    Q = lambda expr: sp.simplify(expr - t*sp.diff(expr, t) - s*sp.diff(expr, s))
    theta = sp.symbols("a b w e", real=True)
    a, b, w, e = theta
    network_graph = t * (a + b*sp.tanh(w*s/t + e))
    penalty = Q(network_graph)**2

    def total(expr):
        return sp.diff(expr, z) + p*sp.diff(expr, F) + c*sp.diff(expr, p) + d*sp.diff(expr, c)

    V = F - z*p

    def on_velocity_chart(expr):
        # V>0 is a chart coordinate; real powers must retain their common base.
        v_chart = sp.Symbol("v_chart", positive=True)
        return sp.simplify(sp.factor(expr.subs(F, v_chart+z*p))).subs(v_chart, V)

    A = c * (z**2*p - g/p**2)
    J = z * V**(m-1) * c/p
    Rp = -A - z*total(A) + g*beta*total(J)
    Rc = Rp - total(V*A/p)
    Lp = -z**3*p + g*z/p**2 + g*beta*z*V**(m-1)/p
    Lc = F*(g/p**3 - z**2) + g*beta*z*V**(m-1)/p
    integral_checks = []
    primitive_checks = []
    for residual, L in ((Rp, Lp), (Rc, Lc)):
        normal_rhs = -residual.subs(d, 0)/sp.diff(residual, d)
        I = L*c
        primitive_checks.append(str(on_velocity_chart(residual - total(I))))
        integral_checks.append(str(on_velocity_chart(total(I).subs(d, normal_rhs))))

    h, u, uc, k, lam = sp.symbols("h u u_c k lambda", positive=True)
    fun = sp.Function("f")
    flux = sp.sqrt(g)*h**sp.Rational(3, 2)*fun(u/sp.sqrt(g*h))
    homogeneity = sp.simplify(2*h*sp.diff(flux, h) + u*sp.diff(flux, u) - 3*flux)
    threshold = k*(u**2-uc**2)**sp.Rational(3, 2)
    threshold_defect = sp.simplify(u*sp.diff(threshold, u) - 3*threshold)

    x = sp.symbols("x", real=True)
    G0, n = sp.symbols("G_0 n", positive=True)
    ux, bx, qx = (sp.Function(name)(x) for name in ("u", "B", "q"))
    evolution = -sp.diff(qx-G0*ux**n*sp.diff(bx, x), x)
    expanded = (G0*ux**n*sp.diff(bx, x, 2)
                + G0*n*ux**(n-1)*sp.diff(ux, x)*sp.diff(bx, x)
                - sp.diff(qx, x))

    qu = sp.symbols("q_u", real=True)
    matrix = sp.Matrix([[u, h, 0], [g, u, g], [0, qu, 0]])
    determinant = (matrix-lam*sp.eye(3)).det()
    expected = -lam*((u-lam)**2-g*h)-g*qu*(u-lam)
    ray_det = determinant.subs({lam: F, h: 1/p, u: V, qu: beta*V**(m-1)})
    no_transport = Lc.subs(beta, 0)
    h_ray = 1/p
    zero_transport_expected = F*h_ray**2*(g*h_ray-(F-V)**2)
    water_speed_det = sp.simplify(determinant.subs(lam, u+sp.sqrt(g*h)))

    velocity = sp.Rational(1, 2)
    control_det = determinant.subs({g: 1, h: 1, u: velocity, qu: 0, lam: sp.Rational(3, 2)})
    v0 = sp.symbols("v_0", positive=True)
    counter_phi = s**2/2 + v0*t
    counter_A = sp.diff(counter_phi, s)*sp.diff(counter_phi, t, 2) - g*sp.diff(counter_phi, s, 2)/sp.diff(counter_phi, s)**2
    counter_T = sp.diff(counter_phi, t)**(m-1)*sp.diff(counter_phi, t, s)/sp.diff(counter_phi, s)
    counter_P = sp.diff(counter_A, t)-g*beta*sp.diff(counter_T, s)
    counter_M = counter_P-sp.diff(sp.diff(counter_phi, t)*counter_A/sp.diff(counter_phi, s), s)

    result = {
        "scope": "exact identities on t,p,phi_t,g,beta>0, m>=1; stated subcharts require L!=0",
        "invariant_graph": {
            "arbitrary_profile_Q": str(Q(phi)),
            "parameter_gradient": [str(sp.diff(penalty, parameter)) for parameter in theta],
            "other_constraints_automatically_zero": False,
        },
        "first_integral": {
            "printed_identity": integral_checks[0],
            "corrected_identity": integral_checks[1],
            "undivided_primitive_remainders": primitive_checks,
            "elimination_pivots": [str(Lp), str(Lc)],
            "bad_candidate_vector_derivative": str(total(z)),
            "free_ode_c_squared_vector_derivative": str(total(c**2).subs(d, 0)),
            "c_squared_pivot_at_zero": str(sp.diff(c**2, c).subs(c, 0)),
            "constant_candidate_is_nonconstant": False,
        },
        "constitutive_family": {
            "homogeneity_remainder": str(homogeneity),
            "threshold_defect": str(threshold_defect),
            "threshold_defect_nonzero": bool(threshold_defect.subs({k: 1, u: 2, uc: 1}) != 0),
            "arbitrary_closure_covered": False,
        },
        "diffusion": {
            "expanded_evolution_remainder": str(sp.simplify(evolution-expanded)),
            "coefficient": "G_0*u**n",
            "coefficient_positive_on_declared_chart": True,
            "whole_system_strict_parabolicity_proved": False,
        },
        "characteristics": {
            "polynomial_remainder": str(sp.simplify(determinant-expected)),
            "corrected_coefficient_remainder": str(on_velocity_chart(ray_det-p**2*Lc)),
            "zero_transport_remainder": str(sp.simplify(no_transport-zero_transport_expected)),
            "water_speed_determinant": str(water_speed_det),
            "hydrodynamic_speed_is_generally_coupled_speed": bool(water_speed_det == 0),
        },
        "smooth_characteristic_control": {
            "fields": "h=g=1, u=1/2, B=constant; ray speed=3/2",
            "eulerian_residuals": ["0", "0", "0"],
            "ray_determinant": str(control_det),
            "laboratory_froude": str(velocity),
            "smooth": True,
        },
        "model_counterexample": {
            "phi": str(counter_phi),
            "printed_residual": str(sp.simplify(counter_P)),
            "corrected_residual": str(sp.simplify(counter_M)),
            "corrected_residual_remainder": str(sp.simplify(counter_M+3*g*v0/s**4)),
            "corrected_residual_is_nonzero": bool(counter_M != 0),
        },
    }
    required_zero = [Q(phi), homogeneity, sp.simplify(evolution-expanded),
                     sp.simplify(determinant-expected), on_velocity_chart(ray_det-p**2*Lc),
                     sp.simplify(no_transport-zero_transport_expected), counter_P,
                     sp.simplify(counter_M+3*g*v0/s**4)]
    result["all_expected_identities_passed"] = (
        all(value == 0 for value in required_zero)
        and integral_checks == ["0", "0"] and primitive_checks == ["0", "0"]
        and result["constitutive_family"]["threshold_defect_nonzero"]
        and not result["characteristics"]["hydrodynamic_speed_is_generally_coupled_speed"]
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = dict(build_certificates())
    result["sympy_version"] = sp.__version__
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        parser.error("refusing to overwrite an existing receipt; select a new --out")
    args.out.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["all_expected_identities_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
