"""Verify the near-cubic SVE proposal without importing the production engine.

Default: print a JSON evidence record. --output-dir also publishes that record,
the proposal's generated table/macros, and a residual-scaling plot.
Numerical time derivatives are finite differences of the dense interpolant,
never replacements by the right-hand side being tested.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import expm
import sympy as sp


G, KAPPA = 1.0, 0.1
T0, T1 = 1.0, 1.5
DELTAS = (0.08, 0.04, 0.02, 0.01, 0.005)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def baseline(t):
    t = np.asarray(t, dtype=float)
    return np.array([1 / (15 * t**2), 2 / (3 * t), 2 / (45 * t**2)])


def baseline_derivative(t):
    t = np.asarray(t, dtype=float)
    return np.array([-2 / (15 * t**3), -2 / (3 * t**2), -4 / (45 * t**3)])


def correction_matrices(t):
    H, v, _ = baseline(t)
    J = np.array([
        [-3 * v, -3 * H, 0],
        [-2 * G, -2 * v, -2 * G],
        [0, -9 * KAPPA * v**2, 0],
    ])
    K = np.array([
        [-v, -H, 0],
        [-G, -v, -G],
        [0, -3 * KAPPA * v**2, 0],
    ])
    b = np.array([0, 0, -3 * KAPPA * v**3])
    c = np.array([0, 0, -KAPPA * v**3 * (1 + 3 * np.log(v))])
    return J, K, b, c


def correction_rhs(t, w):
    # State order: logarithmic correction q, then constant correction p.
    q, p = w[:3], w[3:]
    J, K, b, c = correction_matrices(t)
    return np.concatenate((J @ q + b, J @ p + K @ q + c))


def exponential_reference(times):
    """Independent constant-matrix reference for this exact baseline only."""
    M = np.array([[0, -1 / 5, 0], [-2, -1 / 3, -2], [0, -2 / 5, 2]])
    N = np.array([[-2 / 3, -1 / 15, 0], [-1, -2 / 3, -1], [0, -2 / 15, 0]])
    A = np.zeros((8, 8))
    A[:3, :3], A[3:6, :3], A[3:6, 3:6] = M, N, M
    A[2, 7] = -4 / 45
    A[5, 7] = -4 / 135 * (1 + 3 * np.log(2 / 3))
    A[5, 6], A[6, 7] = 4 / 45, 1
    initial = np.zeros(8)
    initial[-1] = 1
    result = []
    for t in times:
        if t <= 0:
            raise ValueError("The exponential reference requires t>0")
        scaled = expm(A * np.log(t)) @ initial
        result.append(scaled[:6] / np.array([t**2, t, t**2] * 2))
    return np.stack(result, axis=1)


def symbolic_checks():
    t, x, g, k = sp.symbols("t x g k", positive=True)
    delta = sp.Symbol("delta", real=True)
    H, v, C = [sp.Function(n)(t) for n in ("H", "v", "C")]
    p = sp.Matrix([sp.Function(n)(t) for n in ("pH", "pv", "pC")])
    q = sp.Matrix([sp.Function(n)(t) for n in ("qH", "qv", "qC")])
    y = sp.Matrix([H, v, C])
    f = sp.Matrix([-3 * H * v, -v**2 - 2 * g * (H + C), -3 * k * v**3])
    J = f.jacobian(y)
    K = sp.Matrix([[-v, -H, 0], [-g, -v, -g], [0, -3 * k * v**2, 0]])
    b = sp.Matrix([0, 0, -3 * k * v**3])
    c = sp.Matrix([0, 0, -k * v**3 * (1 + 3 * sp.log(v))])
    rhs = dict(zip(sp.diff(y, t), f))
    rhs.update(zip(sp.diff(q, t), J * q + b))
    rhs.update(zip(sp.diff(p, t), J * p + K * q + c))
    shape = sp.diag(x**2, x, x**2)
    h, u, B = shape * (y + delta * (p + sp.log(x) * q))
    original = sp.Matrix([
        sp.diff(h, t) + sp.diff(h * u, x),
        sp.diff(u, t) + u * sp.diff(u, x) + g * sp.diff(h + B, x),
        sp.diff(B, t) + k * sp.diff(u**(3 + delta), x),
    ])
    # Only the delta=0 and first-delta derivatives are reduced; the original
    # flux is differentiated before any truncated flux formula is introduced.
    zero = original.subs(delta, 0)
    first = sp.diff(original, delta).subs(delta, 0)
    clean = lambda expr: sp.simplify(sp.expand_log(expr, force=True))
    # force=True uses the explicitly stated x>0 and v>0 baseline branch.
    checks = {
        "zeroth_order_original_balances": all(clean(r.subs(rhs)) == 0 for r in zero),
        "first_order_original_balances": all(clean(r.subs(rhs)) == 0 for r in first),
    }
    rq, rp = sp.diff(q, t) - J * q - b, sp.diff(p, t) - J * p - K * q - c
    checks["coefficient_defect_transfer_identity"] = all(
        clean(r) == 0 for r in first - shape * (rp + sp.log(x) * rq)
    )
    control = {H: 1 / (15 * t**2), v: sp.Rational(2, 3) / t,
               C: sp.Rational(2, 45) / t**2, g: 1, k: sp.Rational(1, 10)}
    checks["exact_cubic_control"] = all(
        clean(r.subs(control).doit()) == 0 for r in zero
    )
    zeta = sp.Symbol("zeta", positive=True)
    corrected_source = {
        H: (3 - 4 * g * zeta) / (27 * g * t**2),
        v: sp.Rational(2, 3) / t, C: 4 * zeta / (27 * t**2), k: zeta / 3,
    }
    printed_source = dict(corrected_source)
    printed_source[H], printed_source[C] = corrected_source[C], corrected_source[H]
    checks["source_control_coefficients_independently_rederived"] = all(
        clean(r.subs(corrected_source).doit()) == 0 for r in zero
    )
    checks["source_printed_bed_defect_checked"] = clean(
        zero[2].subs(printed_source).doit() - 2 * x**2 * (8 * g * zeta - 3) / (27 * g * t**3)
    ) == 0
    logjet = sp.Symbol("ell")
    split = (shape.inv() * first).applyfunc(
        lambda r: sp.expand(sp.expand_log(r, force=True)).subs(sp.log(x), logjet)
    )
    coeff = sp.Matrix([r.coeff(logjet, 1) for r in split] +
                      [r.coeff(logjet, 0) for r in split])
    derivatives = sp.Matrix(list(sp.diff(q, t)) + list(sp.diff(p, t)))
    checks["correction_derivative_matrix_identity"] = coeff.jacobian(derivatives) == sp.eye(6)

    a, bweight, cweight, dweight, eweight, m = sp.symbols("a b c d e m")
    conditions = [a - bweight + cweight, a - bweight - cweight + dweight,
                  a - bweight - cweight + eweight,
                  a - bweight + m * cweight - eweight]
    substitution = {bweight: a + cweight, dweight: 2 * cweight, eweight: 2 * cweight}
    reduced = [sp.factor(e.subs(substitution)) for e in conditions]
    checks["diagonal_scaling_condition"] = reduced == [0, 0, 0, cweight * (m - 3)]
    checks["generic_spacetime_dilation_retained"] = all(
        e.subs({bweight: a, cweight: 0, dweight: 0, eweight: 0}) == 0
        for e in conditions
    )
    uncorrected = k * sp.diff((x * v)**(3 + delta), x)
    defect1 = clean(sp.diff(uncorrected, delta).subs(delta, 0))
    expected = k * x**2 * v**3 * (1 + 3 * sp.log(x * v))
    checks["uncorrected_first_order_defect"] = clean(defect1 - expected) == 0
    hh, uu = sp.symbols("h u", positive=True)
    A = sp.Matrix([[uu, hh, 0], [g, uu, g], [0, k * m * uu**(m - 1), 0]])
    S = sp.diag(g / hh, 1, g / (k * m * uu**(m - 1)))
    checks["algebraic_symmetrizer_identity_only"] = sp.simplify(S * A - (S * A).T) == sp.zeros(3)
    require(all(checks.values()), f"Symbolic checks failed: {checks}")
    return checks


def differentiate_curve(evaluate, times, step, interval=(T0, T1)):
    """Fourth-order five-point differences, including one-sided endpoints."""
    times = np.asarray(times, dtype=float)
    lo, hi = interval
    if step <= 0 or 4 * step >= hi - lo:
        raise ValueError("Finite-difference step must fit inside the time interval")
    if np.any(times < lo) or np.any(times > hi):
        raise ValueError("Derivative sample outside the time interval")
    result = []
    for t in times:
        if t - 2 * step < lo:
            offsets, weights = np.arange(5), np.array([-25, 48, -36, 16, -3])
        elif t + 2 * step > hi:
            offsets, weights = np.arange(-4, 1), np.array([3, -16, 36, -48, 25])
        else:
            offsets, weights = np.arange(-2, 3), np.array([1, -8, 0, 8, -1])
        stencil = t + step * offsets
        if np.any(stencil < lo) or np.any(stencil > hi):
            raise ValueError("Selected derivative stencil leaves the time interval")
        result.append(evaluate(stencil) @ weights / (12 * step))
    return np.stack(result, axis=1)


def reconstruct(times, xs, delta, curve, curve_derivative):
    """Return fields and their independent time/space derivatives on a grid."""
    times, xs = np.asarray(times), np.asarray(xs)
    if np.any(xs <= 0):
        raise ValueError("The logarithmic ansatz requires x>0")
    q, p = curve[:3], curve[3:]
    qd, pd = curve_derivative[:3], curve_derivative[3:]
    ell = np.log(xs)[None, None, :]
    y = baseline(times)[:, :, None]
    yd = baseline_derivative(times)[:, :, None]
    profiles = y + delta * (p[:, :, None] + ell * q[:, :, None])
    profile_dt = yd + delta * (pd[:, :, None] + ell * qd[:, :, None])
    powers = np.array([2, 1, 2])[:, None, None]
    factor = xs[None, None, :]**powers
    values = factor * profiles
    dt = factor * profile_dt
    dx = factor / xs[None, None, :] * (powers * profiles + delta * q[:, :, None])
    return values, dt, dx


def pde_residual(values, dt, dx, delta):
    h, u, _ = values
    ht, ut, Bt = dt
    hx, ux, Bx = dx
    if np.any(u <= 0) or 3 + delta <= 0:
        raise ValueError("The tested model requires u>0 and m=3+delta>0")
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        return np.array([
            ht + hx * u + h * ux,
            ut + u * ux + G * (hx + Bx),
            Bt + KAPPA * (3 + delta) * u**(2 + delta) * ux,
        ])


def numerical_checks():
    times, xs = np.linspace(T0, T1, 101), np.linspace(1.0, 2.0, 61)
    options = dict(method="DOP853", dense_output=True)
    coarse = solve_ivp(correction_rhs, (T0, T1), np.zeros(6),
                       rtol=1e-11, atol=1e-13, **options)
    fine = solve_ivp(correction_rhs, (T0, T1), np.zeros(6),
                     rtol=1e-12, atol=1e-14, **options)
    require(coarse.success and fine.success, "Correction integration failed")
    curve = fine.sol(times)
    refinement = float(np.max(np.abs(curve - coarse.sol(times))))
    oracle_difference = float(np.max(np.abs(curve - exponential_reference(times))))
    steps = (1e-4, 5e-5, 2.5e-5)
    derivatives = [differentiate_curve(fine.sol, times, h) for h in steps]
    derivative = derivatives[-1]
    derivative_difference = float(np.max(np.abs(derivatives[-1] - derivatives[-2])))
    ode_rhs = np.stack([correction_rhs(t, w) for t, w in zip(times, curve.T)], axis=1)
    ode_defect = float(np.max(np.abs(derivative - ode_rhs)))
    records = []
    zeros = np.zeros_like(curve)
    for sign in (1, -1):
        previous = previous_uncorrected = None
        for magnitude in DELTAS:
            delta = sign * magnitude
            fields = reconstruct(times, xs, delta, curve, derivative)
            residual = pde_residual(*fields, delta)
            maximum = float(np.max(np.abs(residual)))
            uncorrected = pde_residual(*reconstruct(times, xs, delta, zeros, zeros), delta)
            maximum_uncorrected = float(np.max(np.abs(uncorrected)))
            records.append({
                "delta": delta,
                "max_sampled_pde_residual": maximum,
                "component_max_sampled_residuals": np.max(np.abs(residual), axis=(1, 2)).tolist(),
                "uncorrected_max_sampled_residual": maximum_uncorrected,
                "halving_ratio": None if previous is None else previous / maximum,
                "observed_order": None if previous is None else float(np.log2(previous / maximum)),
                "uncorrected_observed_order": None if previous_uncorrected is None else
                    float(np.log2(previous_uncorrected / maximum_uncorrected)),
                "min_sampled_depth": float(fields[0][0].min()),
                "min_sampled_velocity": float(fields[0][1].min()),
            })
            previous, previous_uncorrected = maximum, maximum_uncorrected

    def wrong_curve(t):
        values = fine.sol(t).copy()
        values[0] += 1e-3 * (np.asarray(t) - T0)
        return values

    wrong_derivative = differentiate_curve(wrong_curve, times, steps[-1])
    wrong_rhs = np.stack([correction_rhs(t, w) for t, w in zip(times, wrong_curve(times).T)], axis=1)
    wrong_defect = float(np.max(np.abs(wrong_derivative - wrong_rhs)))
    cubic = pde_residual(*reconstruct(times, xs, 0.0, curve, derivative), 0.0)
    checks = {
        "two_successful_reference_solves": bool(coarse.success and fine.success),
        "profile_tolerance_refinement_below_1e_minus_10": refinement < 1e-10,
        "independent_exponential_reference_below_1e_minus_10": oracle_difference < 1e-10,
        "derivative_step_refinement_below_1e_minus_8": derivative_difference < 1e-8,
        "independent_sampled_ode_defect_below_1e_minus_8": ode_defect < 1e-8,
        "exact_cubic_numeric_residual_below_1e_minus_12": bool(np.max(np.abs(cubic)) < 1e-12),
        "corrected_order_near_two_both_signs": all(
            1.9 < r["observed_order"] < 2.1 for r in records if r["observed_order"] is not None),
        "uncorrected_order_near_one_both_signs": all(
            0.9 < r["uncorrected_observed_order"] < 1.1 for r in records
            if r["uncorrected_observed_order"] is not None),
        "positive_sampled_fields": all(
            r["min_sampled_depth"] > 0 and r["min_sampled_velocity"] > 0 for r in records),
        "independent_derivatives_detect_wrong_curve": wrong_defect > 1e-4,
    }
    require(all(checks.values()), f"Numerical checks failed: {checks}")
    return {
        "checks": checks,
        "configuration": {
            "g": G, "kappa": KAPPA, "time_interval": [T0, T1], "space_interval": [1, 2],
            "time_points": len(times), "space_points": len(xs), "method": "DOP853",
            "reference_tolerances": [[1e-11, 1e-13], [1e-12, 1e-14]],
            "independent_derivative_steps": list(steps),
            "state_order": ["q_H", "q_v", "q_C", "p_H", "p_v", "p_C"],
            "initial_corrections": [0] * 6,
        },
        "max_profile_refinement_difference": refinement,
        "max_exponential_reference_difference": oracle_difference,
        "max_derivative_step_difference": derivative_difference,
        "max_independently_differentiated_ode_defect": ode_defect,
        "wrong_curve_detected_defect": wrong_defect,
        "reference_function_evaluations": [coarse.nfev, fine.nfev],
        "records": records,
    }


def tex_scientific(value):
    mantissa, exponent = f"{value:.3e}".split("e")
    return rf"{mantissa}\times10^{{{int(exponent)}}}"


def publish(report, directory):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    directory.mkdir(parents=True, exist_ok=True)
    (directory / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    numerical = report["numerical"]
    lines = [r"% Generated by verify_corrections.py; do not hand-edit.",
             r"\begin{tabular}{c r r}",
             r"\hline", r"$\delta$ & Corrected defect & Uncorrected defect \\", r"\hline"]
    for row in numerical["records"]:
        if row["delta"] in (0.04, 0.02, 0.01):
            lines.append(f"{row['delta']:.2f} & ${tex_scientific(row['max_sampled_pde_residual'])}$ & "
                         f"${tex_scientific(row['uncorrected_max_sampled_residual'])}$ " + r"\\")
    lines.extend([r"\hline", r"\end{tabular}"])
    (directory / "pilot_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    macros = {
        "PilotRefinement": numerical["max_profile_refinement_difference"],
        "PilotDerivativeDifference": numerical["max_derivative_step_difference"],
        "PilotODEDefect": numerical["max_independently_differentiated_ode_defect"],
        "PilotOracleDifference": numerical["max_exponential_reference_difference"],
    }
    (directory / "pilot_values.tex").write_text(
        "% Generated by verify_corrections.py; do not hand-edit.\n" +
        "\n".join(rf"\newcommand{{\{name}}}{{{tex_scientific(value)}}}" for name, value in macros.items()) + "\n",
        encoding="utf-8")
    fig, ax = plt.subplots(figsize=(7.4, 4.8), layout="constrained")
    for sign, marker, style in ((1, "o", "-"), (-1, "s", "--")):
        rows = [r for r in numerical["records"] if r["delta"] * sign > 0]
        magnitudes = [abs(r["delta"]) for r in rows]
        label = "+" if sign > 0 else "-"
        ax.loglog(magnitudes, [r["max_sampled_pde_residual"] for r in rows],
                  marker=marker, linestyle=style, color="#16765e", label=f"Corrected, delta {label}")
        ax.loglog(magnitudes, [r["uncorrected_max_sampled_residual"] for r in rows],
                  marker=marker, linestyle=style, color="#a73a49", label=f"Uncorrected, delta {label}")
    ax.set(xlabel="Absolute exponent perturbation |delta|", ylabel="Maximum sampled PDE residual",
           title="Residual order, not a PDE solution-error certificate")
    ax.grid(True, which="both", alpha=0.22)
    ax.legend(fontsize=9)
    fig.savefig(directory / "residual_scaling.pdf", metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(directory / "residual_scaling.png", dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Publish generated evidence here in addition to stdout")
    args = parser.parse_args()
    report = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__, "sympy": sp.__version__},
        "status": "local-symbolic-and-numerical-checks-passed",
        "evidence_boundary": "No PINN trained; no validated numerical supremum; no full-PDE solution-error theorem; novelty unconfirmed.",
        "symbolic": symbolic_checks(),
        "numerical": numerical_checks(),
    }
    if args.output_dir:
        publish(report, args.output_dir)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
