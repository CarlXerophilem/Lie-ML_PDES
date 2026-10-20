"""Bounded exact checks for scalar P/M integrals and a positive-u traveling wave.

This is an identity verifier, not a symmetry-classification or solution campaign.
"""
from __future__ import annotations

import argparse
import json
import hashlib
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def _check(expr):
    reduced = sp.simplify(sp.factor(expr))
    return {"pass": reduced == 0, "remainder": str(reduced)}


def _check_profile(expr, V, m):
    # SymPy cannot infer (for symbolic m) that V**m = V*V**(m-1)
    # when V is a composite expression. Apply that real-positive-chart
    # exponent law explicitly, then simplify the polynomial remainder.
    expr = expr.subs(V**m, V * V ** (m - 1), simultaneous=True)
    reduced = sp.simplify(sp.factor(expr))
    return {"pass": reduced == 0, "remainder": str(reduced)}


def _expected_nonzero(expr):
    reduced = sp.simplify(sp.factor(expr))
    return {"pass": reduced != 0, "remainder": str(reduced), "expected": "nonzero"}


def verify_profile_integrals():
    t, s, z = sp.symbols("t s z", positive=True)
    g, kappa = sp.symbols("g kappa", positive=True)
    m = sp.symbols("m", real=True)
    F = sp.Function("F")
    f = F(z)
    P = sp.diff(f, z)
    F2 = sp.diff(f, z, 2)
    V = f - z * P
    A0 = F2 * (z**2 * P - g / P**2)
    J0 = z * V ** (m - 1) * F2 / P

    # Pull back the field jets directly, then apply the total derivatives
    # at fixed s and fixed t. This independently builds the two residuals.
    phi_t = V
    phi_s = P
    phi_tt = z**2 * F2 / t
    phi_ts = -z * F2 / t
    phi_ss = F2 / t
    A = phi_s * phi_tt - g * phi_ss / phi_s**2
    C = phi_t ** (m - 1) * phi_ts / phi_s

    def Dt(expr):
        return sp.diff(expr, t) - z / t * sp.diff(expr, z)

    def Ds(expr):
        return sp.diff(expr, z) / t

    E_print = Dt(A) - g * m * kappa * Ds(C)
    E_corr = E_print - Ds(phi_t * A / phi_s)
    R_print = sp.simplify(t**2 * E_print)
    R_corr = sp.simplify(t**2 * E_corr)

    beta = m * kappa
    L_print = -z**3 * P + g * z / P**2 + g * beta * z * V ** (m - 1) / P
    L_corr = f * (g / P**3 - z**2) + g * beta * z * V ** (m - 1) / P
    p_identity = _check_profile(R_print - sp.diff(L_print * F2, z), V, m)
    m_identity = _check_profile(R_corr - sp.diff(L_corr * F2, z), V, m)
    samples = {}
    for exponent in (1, 2, 3, 4):
        samples[str(exponent)] = {
            "P": _check_profile((R_print - sp.diff(L_print * F2, z)).subs(m, exponent), V, m),
            "M": _check_profile((R_corr - sp.diff(L_corr * F2, z)).subs(m, exponent), V, m),
        }
    return {
        "symbolic_m": {"P": p_identity, "M": m_identity},
        "integer_m_samples": samples,
        "definitions": {
            "P": "t^2 E_print = D_z(L_print F'')",
            "M": "t^2 E_corrected = D_z(L_corrected F'')",
            "chart": "t>0, P=F'>0, V=F-zF'>0, g>0, kappa>0",
            "pivot": "order 3 to 2 only on a subinterval where the relevant L is nonzero",
        },
    }


def verify_traveling_reduction():
    u = sp.symbols("U", positive=True)
    c, q, C0, g, K, G, j = sp.symbols("c q C g K G j", real=True)
    m, n = sp.symbols("m n", real=True)
    w = u - c
    H = q / w
    Z = C0 / g - w**2 / (2 * g) - q / w
    D = sp.diff(Z, u)
    f = (K * u**m - c * Z - j) / (G * u**n * D)
    D_u = sp.diff(D, u)
    f_u = sp.diff(f, u)
    Zp = D * f
    Zpp = D_u * f**2 + D * f_u * f

    # These are the original three PDE residuals pulled back to z=x-c*t,
    # after U'=f(U), U''=f_U*f. The bed row includes the U'' term.
    r_mass = -c * sp.diff(H, u) * f + sp.diff(H * u, u) * f
    r_momentum = (u - c) * f + g * (sp.diff(H, u) + D) * f
    r_bed = (
        -c * Zp
        + K * m * u ** (m - 1) * f
        - G * (n * u ** (n - 1) * f * Zp + u**n * Zpp)
    )
    checks = {
        "mass": _check(r_mass),
        "momentum": _check(r_momentum),
        "bed_including_second_derivative": _check(r_bed),
    }
    return {
        "checks": checks,
        "reduction": {
            "H": str(H),
            "Z": str(Z),
            "D=dZ/dU": str(sp.simplify(D)),
            "Uprime": str(f),
            "Usecond": "f_U*f",
            "Zsecond": "D_U*f^2 + D*f_U*f",
            "quadrature": "z-z0=integral[G*U^n*D/(K*U^m-c*Z-j)] dU; requires numerator != 0",
            "guards": [
                "U>0",
                "w=U-c != 0",
                "G>0",
                "D=dZ/dU != 0",
                "g > 0",
                "H=q/(U-c)>0",
                "K>=0",
            ],
            "generic_exponents": "m,n are real symbols; U>0 defines real powers",
            "G_zero": "not divided by; sediment law is algebraic in the traveling profile",
        },
    }


def verify_exact_control():
    x, t, eps = sp.symbols("x t eps", real=True)
    U = sp.sqrt(x + 2)
    q = sp.Integer(1)
    H = q / U
    alpha, beta = sp.Integer(1), sp.Integer(2)
    bed_constant = sp.Integer(3)
    B = bed_constant - H - U**2 / 2 - alpha * t
    g = K = sp.Integer(1)

    mass = sp.diff(H, t) + sp.diff(H * U, x)
    momentum = sp.diff(U, t) + U * sp.diff(U, x) + g * sp.diff(H + B, x)
    bed = sp.diff(B, t) + sp.diff(K * U**2, x)
    B_bad = B + eps * x
    momentum_bad = sp.diff(U, t) + U * sp.diff(U, x) + g * sp.diff(H + B_bad, x)
    bed_bad = sp.diff(B_bad, t) + sp.diff(K * U**2, x)
    return {
        "parameters": {
            "m": 2,
            "g": 1,
            "K": 1,
            "q": 1,
            "alpha": 1,
            "beta": 2,
            "G": 0,
            "bed_constant_C_over_g": 3,
            "parameter_role": "K*U^2 = alpha*x + beta and B_t = -alpha; bed_constant_C/g=3 is independent",
        },
        "fields": {
            "U": str(U),
            "H": str(H),
            "B": str(B),
        },
        "domain": "x>-2; all t; U>0 and H>0",
        "original_residuals": {
            "continuity": _check(mass),
            "momentum": _check(momentum),
            "sediment": _check(bed),
        },
        "perturbation_B_plus_eps_x": {
            "continuity": _check(mass),
            "momentum": _expected_nonzero(momentum_bad),
            "sediment": _check(bed_bad),
            "interpretation": "for eps != 0 the momentum residual is eps, so this perturbed bed is not a solution",
        },
        "scope": "Exact local field solution of the stated G=0 original PDE; no blanket initial/boundary compatibility claim.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True, help="New JSON receipt; existing files are never overwritten")
    args = parser.parse_args()
    if args.out.exists():
        parser.error("Preserve existing evidence; choose a new --out file")
    receipt = {
        "status": "completed",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version,
        "sympy": sp.__version__,
        "checks": {
            "scalar_profile_integrals": verify_profile_integrals(),
            "positive_u_traveling_reduction": verify_traveling_reduction(),
            "constant_discharge_evolving_bed_control": verify_exact_control(),
        },
        "claim_boundary": [
            "No symmetry classification was run.",
            "G=0 was not divided through in the traveling reduction.",
            "The exact control is a constructed solution, not a general initial-boundary compatibility result.",
        ],
    }
    def collect_passes(value):
        if not isinstance(value, dict):
            return []
        if "pass" in value:
            return [value["pass"]]
        return [flag for child in value.values() for flag in collect_passes(child)]

    all_checks = [
        flag for group in receipt["checks"].values() for flag in collect_passes(group)
    ]
    receipt["all_exact_checks_passed"] = all(all_checks)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": str(args.out), "all_exact_checks_passed": receipt["all_exact_checks_passed"], "check_count": len(all_checks)}, indent=2))
    if not receipt["all_exact_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
