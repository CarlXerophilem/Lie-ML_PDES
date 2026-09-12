"""Source-specific checks for the printed 2026 Lagrangian master equation.

Run without arguments for stdout JSON, or use --output-dir to generate evidence.
This does not train a PINN or certify equivalence with Eulerian sediment transport.
"""

import argparse
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp


SOURCE_DOI = "10.3390/math14030433"


def coefficients(sigma, r, v, g=1, beta=0.1):
    a = 8 * (1 - g * beta) * sigma**3 * r - 2 * g * sigma / r**2
    b = (
        4 * sigma * (1 - 4 * g * beta) * r**2
        + 8 * sigma**2 * (3 - 5 * g * beta) * r * v
        + (8 * sigma**3 * (1 - g * beta) + 4 * g * sigma / r**3) * v**2
    )
    return a, b


def rhs(sigma, state):
    _, r, v = state
    if r <= 0:
        raise ValueError("Outside the regular positive branch")
    a, b = coefficients(sigma, r, v)
    if abs(a) < 1e-10:
        raise ValueError("Outside the regular positive branch")
    return np.array([r, v, -b / a])


def master(phi, t, s, g, beta, m=3):
    ps, pt = sp.diff(phi, s), sp.diff(phi, t)
    return sp.diff(ps * sp.diff(phi, t, 2) - g * sp.diff(phi, s, 2) / ps**2, t) - g * beta * sp.diff(pt**(m - 1) * sp.diff(phi, t, s) / ps, s)


def symbolic_checks():
    t, s, z, g, beta = sp.symbols("t s z g beta", positive=True)
    F = sp.Function("F")
    phi = F(s * t**2)
    r, v = sp.diff(F(z), z), sp.diff(F(z), z, 2)
    a, b = coefficients(z, r, v, g, beta)
    reduced = a * sp.diff(F(z), z, 3) + b
    pulled = (t * master(phi, t, s, g, beta)).subs(s, z / t**2).doit()
    lift = sp.simplify(pulled - reduced)

    k = sp.symbols("k", positive=True)
    exact = k * z**sp.Rational(1, 3)
    cubic = sp.factor(reduced.subs(F(z), exact).doit())
    cubic = sp.factor(cubic).subs(k**3, 27 * g / (1 - 4 * g * beta))
    cubic = sp.simplify(cubic)

    # This exact wave satisfies the printed pair, but not Eulerian Exner.
    wave = -sp.log(2 - s - t)
    bed = s - 1 / (2 * (2 - s - t)**2)
    ps, pt = sp.diff(wave, s), sp.diff(wave, t)
    momentum = sp.simplify(sp.diff(wave, t, 2) - sp.diff(wave, s, 2) / ps**3 + sp.diff(bed, s) / ps)
    printed_bed = sp.simplify(sp.diff(bed, t) + pt**2 * sp.diff(wave, t, s) / ps)
    physical_bed = sp.factor(printed_bed - pt / ps * sp.diff(bed, s))
    x = sp.symbols("x", real=True)
    h, u, B = sp.exp(-x), sp.exp(x), 2 - t - sp.exp(-x) - sp.exp(2 * x) / 2
    euler = [sp.simplify(sp.diff(h, t) + sp.diff(h * u, x)), sp.simplify(sp.diff(u, t) + u * sp.diff(u, x) + sp.diff(h + B, x)), sp.simplify(sp.diff(B, t) + u**2 * sp.diff(u, x))]
    arbitrary = 2 * t + F(s)
    tests = {
        "cubic_reduction_pullback_zero": lift == 0,
        "cubic_exact_profile_zero": cubic == 0,
        "traveling_wave_master_zero": sp.simplify(master(wave, t, s, 1, 1)) == 0,
        "traveling_wave_printed_momentum_zero": momentum == 0,
        "traveling_wave_printed_bed_zero": printed_bed == 0,
        "eulerian_mass_momentum_zero": euler[:2] == [0, 0],
        "eulerian_exner_counterexample_confirmed": sp.simplify(euler[2] - (sp.exp(3 * x) - 1)) == 0,
        "arbitrary_static_profile_master_zero": sp.simplify(master(arbitrary, t, s, 1, 1)) == 0,
    }
    return {
        "checks": tests,
        "traveling_wave_physical_bed_defect": str(physical_bed),
        "traveling_wave_eulerian_exner_defect": str(euler[2]),
        "regular_leading_coefficient": str(a),
    }


def reference(sigma):
    k = np.cbrt(45.0)
    sigma = np.asarray(sigma)
    return np.array([k * sigma**(1 / 3), k / 3 * sigma**(-2 / 3), -2 * k / 9 * sigma**(-5 / 3)])


def solve(initial, method="DOP853", rtol=1e-11, atol=1e-13, max_step=0.02):
    sol = solve_ivp(rhs, (1.0, 1.5), initial, method=method, rtol=rtol, atol=atol, dense_output=True, max_step=max_step)
    if not sol.success or sol.t[-1] < 1.5:
        raise RuntimeError(sol.message)
    return sol


def taylor_coefficients(initial):
    z, r, v = sp.symbols("z r v")
    a, b = coefficients(z, r, v, sp.Integer(1), sp.Rational(1, 10))
    f = -b / a
    fourth = sp.diff(f, z) + sp.diff(f, r) * v + sp.diff(f, v) * f
    evaluate = sp.lambdify((z, r, v), (f, fourth), "numpy")
    third, fourth = evaluate(1.0, initial[1], initial[2])
    return np.array([initial[0], initial[1], initial[2] / 2, third / 6, fourth / 24])


def numerical_pilot():
    grid = np.linspace(1, 1.5, 501)
    initial = reference(1.0)
    baseline = solve(initial)
    baseline_error = float(np.max(np.abs(baseline.sol(grid) - reference(grid))))
    perturbed = initial.copy()
    perturbed[2] *= 1.01
    coarse = solve(perturbed, rtol=1e-9, atol=1e-11, max_step=0.08)
    fine = solve(perturbed)
    independent = solve(perturbed, method="Radau", rtol=2e-12, atol=2e-14)
    state = fine.sol(grid)
    aval, _ = coefficients(grid, state[1], state[2])
    refinement = float(np.max(np.abs(coarse.sol(grid) - state)))
    cross_solver = float(np.max(np.abs(independent.sol(grid) - state)))
    # Differentiate the computed curve, not an ODE RHS substituted as a derivative.
    inner = np.linspace(1.01, 1.49, 301)
    defects = {}
    for step in (1e-3, 5e-4):
        derivative = (fine.sol(inner - 2 * step) - 8 * fine.sol(inner - step) + 8 * fine.sol(inner + step) - fine.sol(inner + 2 * step)) / (12 * step)
        target = np.column_stack([rhs(z, y) for z, y in zip(inner, fine.sol(inner).T)])
        defects[str(step)] = float(np.max(np.abs(derivative - target)))
    coefficients4 = taylor_coefficients(perturbed)
    p2 = np.polynomial.polynomial.polyval(grid - 1, coefficients4[:3])
    p4 = np.polynomial.polynomial.polyval(grid - 1, coefficients4)
    checks = {
        "exact_control_state_error_below_1e-8": baseline_error < 1e-8,
        "refinement_difference_below_1e-8": refinement < 1e-8,
        "independent_solver_difference_below_1e-8": cross_solver < 1e-8,
        "sampled_positive_profile_derivative": bool(np.min(state[1]) > 0),
        "sampled_regular_leading_coefficient": bool(np.min(np.abs(aval)) > 1),
        "finite_difference_state_defect_below_1e-6": max(defects.values()) < 1e-6,
    }
    return {
        "parameters": {"g": 1, "beta": 0.1, "m": 3, "sigma_interval": [1, 1.5], "grid_points": 501, "perturbed_initial_curvature_factor": 1.01},
        "checks": checks,
        "baseline_max_state_error": baseline_error,
        "perturbed_max_refinement_difference": refinement,
        "perturbed_max_independent_solver_difference": cross_solver,
        "perturbed_sampled_min_r": float(np.min(state[1])),
        "perturbed_sampled_min_abs_a": float(np.min(np.abs(aval))),
        "finite_difference_state_defects": defects,
        "taylor_p2_max_profile_error": float(np.max(np.abs(p2 - state[0]))),
        "taylor_p4_max_profile_error": float(np.max(np.abs(p4 - state[0]))),
        "initial_state": perturbed.tolist(),
        "taylor_coefficients": coefficients4.tolist(),
        "interval_certified": False,
        "pinn_trained": False,
    }


def generate_report():
    report = {
        "schema": "lieml.lagrange-proposal-pilot.v1",
        "source_doi": SOURCE_DOI,
        "model": "Printed Eq. (7), not a certified Eulerian-equivalent SVE model",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "sympy": sp.__version__},
        "symbolic": symbolic_checks(),
        "numerical": numerical_pilot(),
    }
    report["all_checks_passed"] = all(report["symbolic"]["checks"].values()) and all(report["numerical"]["checks"].values())
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    report = generate_report()
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        macros = {"LagrangeControlError": "baseline_max_state_error", "LagrangeRefinement": "perturbed_max_refinement_difference", "LagrangeOracle": "perturbed_max_independent_solver_difference", "LagrangeMinR": "perturbed_sampled_min_r", "LagrangeMinA": "perturbed_sampled_min_abs_a", "LagrangeTaylorTwo": "taylor_p2_max_profile_error", "LagrangeTaylorFour": "taylor_p4_max_profile_error"}
        lines = []
        for name, key in macros.items():
            mantissa, exponent = f"{report['numerical'][key]:.3e}".split("e")
            lines.append(f"\\newcommand{{\\{name}}}{{{mantissa}\\times10^{{{int(exponent)}}}}}")
        (args.output_dir / "pilot_values.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["all_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
