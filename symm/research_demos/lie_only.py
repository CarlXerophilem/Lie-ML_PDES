"""Pure symbolic Lie-reduction baseline for the printed Lagrangian SVE PDE.

Run with ``python -B -m symm.research_demos.lie_only --output-dir PATH``.
This module intentionally does not import a neural-network library.
"""

from __future__ import annotations

import argparse
import platform
from pathlib import Path

import numpy as np
import sympy as sp

from symm.generic.chart_reduction import reduce_in_chart
from symm.generic.sve_reduction import sve_data_family_case, sve_scaling_case

from .schema import sha256, utc_now, write_json


def _certificate(outcome) -> dict:
    certificate = outcome.certificate
    return {
        "status": certificate.status,
        "checks": dict(certificate.checks),
        "residuals": [str(item) for item in certificate.residuals],
        "covered_guards": [str(item) for item in certificate.covered_guards],
        "message": certificate.message,
        "system_fingerprint": certificate.system_fingerprint,
        "configuration_fingerprint": certificate.configuration_fingerprint,
    }


def _reduced_expressions():
    sigma, g, beta_tr = sp.symbols("sigma g beta_tr", positive=True)
    F = sp.Function("F")
    r = sp.diff(F(sigma), sigma)
    v = sp.diff(F(sigma), sigma, 2)
    a = 8 * (1 - g * beta_tr) * sigma**3 * r - 2 * g * sigma / r**2
    b = (
        4 * sigma * (1 - 4 * g * beta_tr) * r**2
        + 8 * sigma**2 * (3 - 5 * g * beta_tr) * r * v
        + (8 * sigma**3 * (1 - g * beta_tr) + 4 * g * sigma / r**3) * v**2
    )
    return sigma, g, beta_tr, F, a, b, sp.expand(a * sp.diff(F(sigma), sigma, 3) + b)


def _m3_details(outcome) -> dict:
    t, s = sp.symbols("t s", positive=True)
    sigma, g, beta_tr, F, a, _, reduced = _reduced_expressions()
    profile = F(s * t**2)
    invariant_surface = sp.simplify(-t * sp.diff(profile, t) + 2 * s * sp.diff(profile, s))
    k = sp.symbols("K", positive=True)
    exact = k * sigma ** sp.Rational(1, 3)
    exact_residual = sp.factor(reduced.subs(F(sigma), exact).doit())
    exact_residual = sp.simplify(exact_residual.subs(k**3, 27 * g / (1 - 4 * g * beta_tr)))
    reduced_equation = str(outcome.reduced_system.equations[0])
    return {
        "certificate": _certificate(outcome),
        "generator": "X_5 = t*d_t - 2*s*d_s",
        "flow": {"t": "exp(epsilon)*t", "s": "exp(-2*epsilon)*s", "phi": "phi"},
        "invariant": "sigma = s*t**2",
        "reconstruction": "phi(t,s) = F(s*t**2)",
        "invariant_surface_equation": "Q = -t*phi_t + 2*s*phi_s = 0",
        "invariant_surface_zero": invariant_surface == 0,
        "reduced_equation": reduced_equation,
        "leading_coefficient": str(a),
        "regularity_conditions": [str(item) for item in outcome.regularity_conditions],
        "lifting_identity": "E_3[F(s*t**2)] = R_0[F](s*t**2)/t",
        "lifting_identity_zero": dict(outcome.certificate.checks).get("pullback_identity", False),
        "exact_control": "F_0 = C + K*sigma**(1/3), K**3 = 27*g/(1-4*g*beta_tr)",
        "exact_control_zero": exact_residual == 0,
    }


def _case(m: int) -> tuple[object, object]:
    problem, generator, chart, multiplier = sve_scaling_case(m)
    return reduce_in_chart(problem, generator, chart, symmetry_multipliers=multiplier), problem


def _v02_certificate() -> dict:
    problem, generator, chart, multiplier = sve_data_family_case()
    outcome = reduce_in_chart(problem, generator, chart, symmetry_multipliers=multiplier)
    sigma, g, beta_tr, _, leading, _, reduced = _reduced_expressions()
    rank_guards = outcome.reduced_system.reduction_map.rank_guards if outcome.reduced_system else ()
    pulled = outcome.pulled_data[0] if outcome.pulled_data else None
    exact = outcome.certificate.status == "verified" and outcome.data_status == "data-compatible"
    return {
        "schema": "lieml.sve.reduction-certificate.v0.2",
        "created_utc": utc_now(),
        "status": "verified-regular-data-compatible" if exact else "unsupported",
        "scope": "fixed m=3 supplied chart; strict invariant data; no maximality or singular-branch solution",
        "source_sha256": sha256(Path(__file__)),
        "structural_classification": {
            "independent_variables": problem.system.p,
            "dependent_fields": problem.system.q,
            "equations": problem.system.r,
            "order": problem.system.jet_space.max_order,
            "jet_structure": list(problem.jet_structure),
        },
        "fixed_branch": {
            "m": 3,
            "delta_m": 0,
            "generator": "X_5 = t*d_t - 2*s*d_s",
            "invariant": "sigma = s*t**2",
            "orbit_coordinate": "rho = t",
            "parameter_relation": "beta_tr = 3*kappa",
        },
        "reduction_certificate": _certificate(outcome),
        "exact_branch_guards": {
            "chart_rank": str(rank_guards[0]) if len(rank_guards) > 0 else "missing",
            "orbit_speed": str(rank_guards[1]) if len(rank_guards) > 1 else "missing",
            "fiber_rank": str(rank_guards[2]) if len(rank_guards) > 2 else "missing",
            "source_positivity": [str(value) for value in problem.domain],
        },
        "data_compatibility": {
            "status": outcome.data_status,
            "surface": str(pulled.surface) if pulled else "missing",
            "pulled_residuals": [str(value) for value in pulled.residuals] if pulled else [],
            "checks": dict(outcome.data_checks),
            "invariance_residuals": [str(value) for value in outcome.data_invariance_residuals],
            "meaning": "strict off-shell invariance of the supplied surface and jet residuals",
        },
        "reduced_equation": str(reduced),
        "singular_boundaries": {
            "rank_drop": "rho = 0",
            "F_prime": "Derivative(F(sigma), sigma) = 0",
            "leading_coefficient": str(leading),
        },
        "parameter_family": {
            "name": "eta_ic",
            "candidate_interval": [-0.02, 0.02],
            "data": ["F(1)=K", "F'(1)=K/3", "F''(1)=-(2*K/9)*(1+eta_ic)"],
            "K": "cuberoot(45) for g=1, beta_tr=0.1",
        },
        "claims": {
            "generic_m_classified": False,
            "maximal_point_algebra_proved": False,
            "equivalence_group_completed": False,
            "m3_delta_continuation_proved": False,
            "singular_branches_solved": False,
            "global_topology_proved": False,
            "ml_speedup_proved": False,
        },
    }


def _plot(output_dir: Path) -> None:
    import matplotlib.pyplot as plt

    beta_tr = 0.1
    k = np.cbrt(27 / (1 - 4 * beta_tr))
    sigma = np.linspace(1, 1.5, 250)
    t = np.linspace(0.8, 1.3, 120)
    s = np.linspace(0.6, 1.8, 140)
    tt, ss = np.meshgrid(t, s, indexing="ij")
    field = k * (ss * tt**2) ** (1 / 3)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    axes[0].plot(sigma, k * sigma ** (1 / 3), color="#126a5b", lw=2)
    axes[0].set(xlabel=r"$\sigma$", ylabel=r"$F_0(\sigma)$", title="Exact reduced profile")
    image = axes[1].pcolormesh(s, t, field, shading="auto", cmap="viridis")
    axes[1].set(xlabel=r"$s$", ylabel=r"$t$", title=r"Reconstruction $\phi(t,s)$")
    fig.colorbar(image, ax=axes[1], label=r"$\phi$")
    fig.savefig(output_dir / "lie_only_control.png", dpi=180)
    plt.close(fig)


def run_demo(output_dir: Path, make_plot: bool = True) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    m3, problem3 = _case(3)
    m4, _ = _case(4)
    report = {
        "schema": "lieml.three-layer.lie-only.v1",
        "created_utc": utc_now(),
        "status": "verified-baseline" if m3.certificate.status == "verified" else "failed",
        "scope": "supplied local chart and supplied symmetry multiplier; not maximal classification",
        "model": problem3.system.name,
        "parameter_convention": {"beta_tr": "m*kappa", "group_parameter": "epsilon"},
        "versions": {"python": platform.python_version(), "sympy": sp.__version__, "numpy": np.__version__},
        "source_sha256": sha256(Path(__file__)),
        "cases": {
            "m3": _m3_details(m3),
            "m4": {
                "certificate": _certificate(m4),
                "generator_tested": "X_5 = t*d_t - 2*s*d_s",
                "symmetry_identity_zero": m4.certificate.status == "verified",
                "interpretation": "failure of this supplied identity, not proof that m=4 has no symmetries",
            },
        },
    }
    write_json(output_dir / "lie_only_report.json", report)
    write_json(output_dir / "sve_certificate_v02.json", _v02_certificate())
    if make_plot:
        _plot(output_dir)
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args(argv)
    report = run_demo(args.output_dir, make_plot=not args.no_plot)
    print((args.output_dir / "lie_only_report.json").read_text(encoding="utf-8"))
    return 0 if report["status"] == "verified-baseline" else 1


if __name__ == "__main__":
    raise SystemExit(main())
