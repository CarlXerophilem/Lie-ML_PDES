"""Concise human report and publication artifacts from measured results only."""
from __future__ import annotations

from pathlib import Path
from statistics import median
from typing import Any

import numpy as np


def groups(results: dict) -> list[dict[str, Any]]:
    rows = []
    for family in (False, True):
        for method in ("PINN", "PIKAN"):
            runs = [r for r in results["neural"] if r["method"] == method and r["conditioned"] == family]
            attempted = [r for r in runs if "validation" in r]
            validations = [v for r in attempted for v in r["validation"]]
            metrics = [v["metrics"] for v in validations if "max_profile_error" in v["metrics"]]
            breaks = [r["costs"]["new_parameter_crossing"]["N_break"] for r in attempted
                      if r["costs"]["new_parameter_crossing"]["status"] == "amortizable"]
            rows.append({"method": method, "family": family, "planned": len(runs), "attempted": len(attempted),
                         "passed": sum(r["accuracy_admissible"] for r in runs),
                         "median_error": median(m["max_profile_error"] for m in metrics) if metrics else None,
                         "median_residual": median(m["original_residual_L2"] for m in metrics) if metrics else None,
                         "median_training": median(r["training_seconds"] for r in attempted) if attempted else None,
                         "median_break": median(breaks) if breaks else None,
                         "amortizable": len(breaks)})
    return rows


def write_report(out: Path, certificates: dict, results: dict, config: dict) -> None:
    summary = groups(results)
    rows = results["classical"]
    cheb = [r for r in rows if r["method"] == "Chebyshev"]
    passed = sum(r["metrics"]["accuracy_admissible"] for r in cheb)
    lines = ["# Methodology and measured outcomes", "", "All computation is offline, float64 CPU. Exact algebra, numerical validation and unresolved questions remain separate.", "",
             "## Exact reductions", "", "Write P=F', C=F'', V=F-zP, beta_tr=m*kappa. On t>0, P>0, V>0:", "",
             "- Printed scalar model: `L_m = -z^3 P + g z/P^2 + g m kappa z V^(m-1)/P`.",
             "- Advectively corrected scalar model: `L_m = F (g/P^3-z^2) + g m kappa z V^(m-1)/P`.",
             "- For each model, `R_m = (L_m F'')' = 0`, so `F''=I0/L_m` wherever `L_m != 0`. The initial curvature fixes `I0=L_m(1,F0,P0) C0`.", "",
             "Common scaling is verified for arbitrary m. The X5 defect is proportional to (m-3) times the transport divergence. It vanishes identically only at m=3 when transport is nonzero; beta_tr=m*kappa also has the m=0 zero-transport stratum. Individual solutions/jets can have zero defect at other m.", "",
             "The corrected coupled momentum/bed system admits the verified lift `Xc=t*d_t+s*d_s+phi*d_phi` with zero bed coefficient for every m, and `X5=t*d_t-2s*d_s-2b*d_b` at m=3. Bare X5 has momentum defect `2g*b_s`. Bed translation is admitted. These checks are not a maximal classification.", "",
             "## Boundary and continuous-space limits", "",
             "PDE symmetry, boundary tangency and data-manifold tangency are separate gates. Moving rays s=z0*t pass common scaling; fixed t=T0>0 and fixed s=S0!=0 fail. The t in [1,2] interval is an evaluation window, not an invariant capped domain. Data are constructed compatibly. Curvature perturbations change I0 and the reconstructed bed/flux data.", "",
             "The retained unperturbed continuous tube reaches z=1.4. This campaign reaches z=1.5 with perturbed data using sampled positivity/leading-factor guards. It supplies neither a uniform tube certificate nor a learned continuous-error theorem. Local jet solvability alone does not establish a PDE initial/boundary value theorem.", "",
             "## Numerical protocol", "",
             f"There are {results['classical_cases']} classical cases and {len(results['tolerance_ladder'])} tolerance-ladder comparisons on a {results['grid_points']}-point grid. Requested rtol=1e-14 is clipped by SciPy to its recorded machine floor. Second- and third-order common-scaling references are independently compared.", "",
             "Chebyshev degrees 8,12,16,24 use square nonlinear collocation and an exact residual Jacobian. The dense IVP residual differentiates the actual returned scalar interpolation polynomial: high-order state convergence does not imply third-derivative convergence. Neural trials enforce all three Cauchy traces exactly and use the original-coordinate residual measure (7/24 for cubic X5, 3/8 for common scaling). The PIKAN uses smooth polynomial edges, without spline knots.", "",
             f"Seeds: {config['seeds']}. Budgets: {config['adam_steps']} Adam updates, {config['lbfgs_evaluations']} L-BFGS closures, 120 seconds/model, {config['campaign_seconds']:g} seconds/campaign. Accuracy gates: profile Linf <=1e-6 and original residual L2 <=1e-4. All attempted and unstarted outcomes are retained.", "",
             f"Chebyshev accuracy-admissible runs: {passed}/{len(cheb)}; failed control attempts: {len(results['failed_controls'])}.", "",
             "| Model | Workload | Passed / planned | Median profile error | Median residual L2 | Median training (s) | Family amortizable runs |", "|---|---|---:|---:|---:|---:|---:|"]
    def number(value: float | None) -> str:
        return "unavailable" if value is None else f"{value:.3g}"
    for row in summary:
        lines.append(f"| {row['method']} | {'conditioned' if row['family'] else 'fixed'} | {row['passed']}/{row['planned']} | {number(row['median_error'])} | {number(row['median_residual'])} | {number(row['median_training'])} | {row['amortizable']} |")
    lines += ["", "Medians include unsuccessful attempted runs; passing a conditioned run means passing all four held-out parameter pairs. Timing varies with hardware and scheduling.", "",
              "## Selection and costs", "",
              "Cost comparisons require matched validation gates. For admissible candidates with positive per-query saving, `N_break = max(0, ceil((neural_setup-classical_setup)/(classical_query-neural_query)))`. Equal or slower neural queries have no asymptotic amortization. Each recorded crossing checks the actual arithmetic inequality.", "",
              "Cached fixed profiles compare against cached spectral evaluation. New parameter queries compare against a fresh spectral solve. Neural cost includes training, validation reference generation, derivatives through third order, sampled guards, physical reconstruction and classical fallback when rejected. An observed finite held-out advantage remains conditional on the same accuracy and cost assumptions for later queries. It is not a parameter-uniform certification or a production speedup guarantee.", "",
              "## Artifacts and replay", "",
              "- `symbolic_certificates.json`: exact checks, matrices, maximal minors, selected commutators and assumptions.",
              "- `experiment_results.json`: every classical and neural run, actual residuals, guards, times, fallback costs and crossings.",
              "- `config.json`, `environment.json`, `candidates/`: seeds, budgets, source SHA-256, package versions and frozen learned coefficients.",
              "- `data-flux/`, `workflow/`: maintained original-coordinate compatibility/flux checks and all nine analysis stages.",
              "- `benchmark_summary.pdf`, `benchmark_table.tex`: measured standalone scientific artifacts.", "",
              "Replay from the repository root with `python3 run_pipeline.py`. For a smaller independent campaign use `--quick --seeds 17 --out build/week-4-quick`. Frozen evidence and manifests are unchanged.", ""]
    (out/"METHODOLOGY_REPORT.md").write_text("\n".join(lines))
    tex = [r"\begin{tabular}{llrrrr}", r"\toprule", r"Model & Workload & Passed & Error & Residual & Train (s) \\", r"\midrule"]
    for row in summary:
        tex.append(f"{row['method']} & {'family' if row['family'] else 'fixed'} & {row['passed']}/{row['planned']} & {number(row['median_error'])} & {number(row['median_residual'])} & {number(row['median_training'])} " + r"\\")
    tex += [r"\bottomrule", r"\end{tabular}"]
    (out/"benchmark_table.tex").write_text("\n".join(tex)+"\n")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    for method, marker in (("Chebyshev", "o"), ("DOP853", "s"), ("Radau", "^")):
        selected = [r for r in rows if r["method"] == method]
        axes[0].scatter([r["setup_seconds"] for r in selected],
                        [max(r["metrics"]["max_profile_error"], 1e-16) for r in selected],
                        s=14, marker=marker, alpha=.6, label=method)
    for method, marker in (("PINN", "o"), ("PIKAN", "s")):
        selected = [r for r in results["neural"] if r["method"] == method and "validation" in r]
        axes[1].scatter([r["training_seconds"] for r in selected],
                        [max(1e-16, max(v["metrics"].get("max_profile_error", 1.) for v in r["validation"])) for r in selected],
                        s=20, marker=marker, label=method)
    for ax in axes:
        ax.set(xscale="log", yscale="log", ylabel="Maximum profile error")
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.axhline(1e-6, color="grey", ls="--", lw=1)
        ax.legend(fontsize=8)
    axes[0].set(xlabel="Classical setup time (s)", title="Classical controls (all charts)")
    axes[1].set(xlabel="Training time (s)", title="Neural candidates (seed/parameter variation)")
    axes[1].set_xscale("linear")
    fig.savefig(out/"benchmark_summary.pdf")
    fig.savefig(out/"benchmark_summary.png", dpi=160)
    plt.close(fig)
