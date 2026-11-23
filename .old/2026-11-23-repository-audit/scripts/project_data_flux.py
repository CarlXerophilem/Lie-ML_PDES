"""Verify the scalar SVE common-scaling data and current pullback.

Run ``python -B scripts/project_data_flux.py --out tmp/data-flux``.
This adapter reuses the existing generic chart verifier and sve_lab references;
it does not classify the physical bed-field system or prove arbitrary IBVPs.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from html import escape
import hashlib
import importlib
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
EXPONENTS = (1, 2, 2.9, 3, 3.1, 4)
TOLERANCE = 1e-9


def _modules(root: Path):
    lab = root / "research_artifacts/sve-progress-20261010"
    if not (lab / "sve_lab/symbolic.py").is_file():
        raise FileNotFoundError(f"Missing current scalar research package: {lab}")
    for location in (root, lab):
        if str(location) not in sys.path:
            sys.path.insert(0, str(location))
    return tuple(importlib.import_module(name) for name in (
        "symm.generic", "sve_lab.jets", "sve_lab.symbolic",
        "sve_lab.numerics", "sve_lab.tube",
    ))


def _branch_remainder(expression, symbolic):
    """Use the recorded positive velocity branch, never force a power identity."""
    velocity, slope = sp.symbols("V_positive P_positive", positive=True)
    return sp.simplify(expression.xreplace({
        symbolic.f: velocity + symbolic.z*slope,
        symbolic.P: slope,
    }))


def _case(api, jets, physical):
    t, s = sp.symbols("t s", positive=True)
    phi, field = sp.symbols("phi F", real=True)
    zeta, orbit = sp.symbols("zeta orbit", positive=True)
    space = api.JetSpace((t, s), (phi,), 3)
    target = api.JetSpace((zeta,), (field,), 3)
    source_mapping = {
        jets.t: t, jets.s: s, jets.g: sp.Integer(1),
        jets.kappa: sp.Rational(1, 30),
        **{value: space.jet_symbol(0, index) for index, value in jets.JETS.items()},
    }
    residual = jets.model_residual(jets.m, physical).xreplace(source_mapping)
    pt, ps = space.jet_symbol(0, (1, 0)), space.jet_symbol(0, (0, 1))
    data = api.DataCondition("ray-three-jet", s/t-1, (
        phi/t-2, ps-sp.Rational(1, 2),
        t*space.jet_symbol(0, (0, 2))-sp.Rational(1, 10),
    ))
    problem = api.PDEProblem(
        api.DifferentialSystem(space, (residual,), inequations=(t, ps),
                               name="physical-corrected-scalar" if physical else "printed-scalar"),
        parameters=(jets.m,),
        domain=(sp.Gt(t, 0, evaluate=False), ps > 0, pt > 0), data=(data,),
    )
    chart = api.ReductionChart(target, (s/t,), orbit, t,
                              (orbit, orbit*zeta), (t*field,), (t**-2,))
    generator = api.PointGenerator((t, s), (phi,))
    return problem, generator, chart, source_mapping


def check_chart_point(time_value, determinant=None):
    """Reject singular/undeclared points before evaluating the local chart."""
    time_value = sp.sympify(time_value)
    if time_value.is_finite is not True or time_value.is_positive is not True:
        raise ValueError("the declared chart requires finite t>0")
    # The (T,z)=(t,s/t) base chart has det(d(T,z)/d(t,s))=1/t.
    value = 1/time_value if determinant is None else sp.sympify(determinant)
    if value.is_finite is not True or value.is_zero is not False:
        raise ValueError("the chart determinant must be finite and nonzero")
    return {"time": str(time_value), "determinant": str(value), "status": "regular"}


def _symbolic_model(api, jets, symbolic, physical):
    problem, generator, chart, source_mapping = _case(api, jets, physical)
    outcome = api.reduce_in_chart(problem, generator, chart, symmetry_multipliers=((-2,),))
    if outcome.reduced_system is None:
        raise RuntimeError(outcome.certificate.message)
    zeta = chart.reduced_space.independent_variables[0]
    target_jets = {chart.reduced_space.jet_symbol(0, (n,)): value
                   for n, value in enumerate((symbolic.f, symbolic.P, symbolic.C, symbolic.H))}
    time = sp.Symbol("T", positive=True)
    target_mapping = {zeta: symbolic.z, chart.orbit_variable: time, **target_jets}
    rules = dict(outcome.reduced_system.reduction_map.pullback_rules)
    inverse = dict(zip(problem.system.jet_space.independent_variables, chart.inverse_coordinates))

    def pull(expression):
        return sp.simplify(expression.xreplace(source_mapping).xreplace(rules)
                           .subs(inverse, simultaneous=True).xreplace(target_mapping))

    constants = {jets.g: 1, jets.kappa: sp.Rational(1, 30)}
    reduced = symbolic.reduced_residual(jets.m, physical).subs(constants)
    integral = symbolic.first_integral(jets.m, physical).subs(constants)
    current = symbolic.conservation_pullback_certificate(jets.m, physical)
    density = pull(current["transformed_density"])
    flux = pull(current["boundary_normal_flux_pullback"])
    base_density = symbolic.C*(symbolic.z**2*symbolic.P-1/symbolic.P**2)
    old_from_new = sp.Matrix((time, time*symbolic.z)).jacobian((time, symbolic.z)).det()
    graph = symbolic.common_scaling_certificate()
    graph_remainders = {name: _branch_remainder(pull(value), symbolic)
                        for name, value in graph["differential_consequences"].items()}
    reduced_by_generic = outcome.reduced_system.equations[0].xreplace(target_mapping)
    checks = {
        "generic_chart_verified": outcome.certificate.status == "verified",
        "normalized_ray_data_compatible": outcome.data_status == "data-compatible",
        "generic_matches_independent_profile_equation":
            _branch_remainder(reduced_by_generic-reduced, symbolic) == 0,
        "all_invariant_graph_derivatives_through_order_two":
            all(value == 0 for value in graph_remainders.values()),
        "old_from_new_jacobian_T": old_from_new == time,
        "current_divergence_identity": current["checks"]["divergence_remainder"] == 0,
        "density_pullback": _branch_remainder(density-base_density, symbolic) == 0,
        "source_zero": pull(current["source"]) == 0,
        "boundary_flux_is_first_integral_over_T":
            _branch_remainder(flux-integral/time, symbolic) == 0,
        "first_integral_derivative_equals_reduced_equation":
            _branch_remainder(symbolic.profile_total(integral)-reduced, symbolic) == 0,
    }
    pulled_data = outcome.pulled_data[0]
    model = "physical_corrected" if physical else "printed"
    record = {
        "model": model, "exponent": "symbolic real m on F-z*Fprime>0",
        "status": "verified" if all(checks.values()) else "failed", "checks": checks,
        "problem_fingerprint": problem.fingerprint(),
        "generic_certificate": outcome.certificate.as_dict(),
        "data_status": outcome.data_status, "data_checks": dict(outcome.data_checks),
        "normalized_source_data": [str(e) for e in problem.data[0].residuals],
        "pulled_surface": str(pulled_data.surface.xreplace(target_mapping)),
        "pulled_data": [str(e.xreplace(target_mapping)) for e in pulled_data.residuals],
        "graph_derivative_remainders": {name: str(value) for name, value in graph_remainders.items()},
        "regularity_conditions": [str(e) for e in outcome.regularity_conditions],
        "pulled_domain": [str(e) for e in outcome.pulled_domain],
        "current": {
            "old_from_new_jacobian": str(old_from_new), "source": "0",
            "transformed_density": str(density), "transformed_spatial_flux": str(flux),
            "first_integral": str(integral),
            "on_solution_boundary_flux": "I0/T",
            "boundary_covector": "dz on z=constant, positive z orientation",
            "integrated_flux_T1_to_T2": "I0*log(T2/T1), for 0<T1<T2",
            "convention": "vector density; no metric/unit-normal convention",
        },
        "scope": "declared scalar balance law and normalized ray data only",
    }
    return record, (problem, generator, chart)


def _negative_controls(api, cases):
    records = []
    for model, (problem, generator, chart) in cases.items():
        phi = problem.system.jet_space.dependent_fields[0]
        incompatible = api.DataCondition("constant-physical-phi", problem.data[0].surface, (phi-2,))
        outcome = api.reduce_in_chart(replace(problem, data=(incompatible,)), generator, chart,
                                      symmetry_multipliers=((-2,),))
        records.append({
            "model": model, "control": "constant physical phi=2 on moving ray s=t",
            "passed": outcome.data_status == "pulled-back-only"
                      and not all(value for _, value in outcome.data_checks),
            "pde_status": outcome.certificate.status, "data_status": outcome.data_status,
            "data_checks": dict(outcome.data_checks),
            "meaning": "PDE pullback survives; these data cannot be marked compatible",
        })
        singular = api.reduce_in_chart(problem, generator, replace(chart, invariants=(sp.Integer(1),)),
                                       symmetry_multipliers=((-2,),))
        records.append({"model": model, "control": "zero chart determinant",
                        "passed": singular.reduced_system is None
                                  and singular.certificate.status == "unsupported",
                        "checks": dict(singular.certificate.checks)})
    try:
        check_chart_point(0)
    except ValueError as error:
        records.append({"control": "t=0", "passed": True, "reason": str(error)})
    else:
        records.append({"control": "t=0", "passed": False})
    return records


def _numerical(numerics, tube):
    records, curves = [], []
    grid = np.linspace(1, 1.4, 401)
    for physical in (False, True):
        model = "physical_corrected" if physical else "printed"
        _, leading, _ = numerics.functions(physical)
        for exponent in EXPONENTS:
            reference, guards = numerics.reference(exponent, physical)
            integrated, initial_integral = numerics.integrated_reference(exponent, physical)
            values = reference.sol(grid)
            other = integrated.sol(grid)
            curvature = initial_integral/leading(grid, other[0], other[1], 0., exponent, 1., 1./30.)
            independent_jets = np.vstack((other[:2], curvature))
            disagreement = float(np.max(np.abs(values-independent_jets)))
            integral_values = values[2]*leading(grid, *values, exponent, 1., 1./30.)
            drift = float(np.max(np.abs(integral_values-initial_integral)))
            guards_positive = all(np.isfinite(value) and value > 0 for value in guards.values())
            records.append({
                "model": model, "exponent": exponent,
                "max_profile_crosssolve_absolute_error": disagreement,
                "crosssolve_profile_jets": ["F", "Fprime", "Fsecond"],
                "first_integral_max_absolute_drift": drift, "threshold": TOLERANCE,
                "passed": disagreement <= TOLERANCE and drift <= TOLERANCE and guards_positive,
                "sampled_guards": guards, "guard_evidence": "401 grid points; sampled",
                "exact_tube_certificate": model, "I0": initial_integral,
                "boundary_flux_samples": [{"T": time, "flux": initial_integral/time}
                                          for time in (1., 2., 4.)],
                "integrated_flux_T1_to_T2": initial_integral*float(np.log(2.)),
            })
            curves.append((model, exponent, grid, values, initial_integral))
    certificates = [tube.tube_certificate(physical) for physical in (False, True)]
    return records, curves, certificates


def _workflow_svg(path):
    labels = (
        ("Declare scalar equation", "printed / physical corrected; g=1, kappa=1/30"),
        ("Common scaling and chart", "phi=t F(z), z=s/t; t>0, F'>0, F-zF'>0"),
        ("Normalize moving-ray data", "z=1: F=2, F'=1/2, F''=1/10"),
        ("Pull back current and flux", "Jacobian=T; scalar boundary flux=I0/T"),
        ("Cross-check the two ODE solves", "12 cases; error and integral drift <= 1e-9"),
        ("Retain the evidence scope", "exact reference tube; candidate guards stay sampled"),
    )
    pieces = ['<svg xmlns="http://www.w3.org/2000/svg" width="950" height="730" viewBox="0 0 950 730">',
              '<rect width="950" height="730" fill="#f8fafc"/>',
              '<g font-family="sans-serif" text-anchor="middle">',
              '<text x="475" y="34" font-size="24" fill="#0f172a">Scalar symmetry, data and flux verification</text>']
    for index, (title, detail) in enumerate(labels):
        y = 58+index*108
        pieces += [f'<rect x="65" y="{y}" width="820" height="80" rx="12" fill="#e0f2fe" stroke="#0369a1"/>',
                   f'<text x="475" y="{y+29}" font-size="20" fill="#0c4a6e">{escape(title)}</text>',
                   f'<text x="475" y="{y+56}" font-size="16" fill="#334155">{escape(detail)}</text>']
        if index < len(labels)-1:
            pieces += [f'<path d="M475 {y+82} v19 m-6 -6 l6 6 l6 -6" fill="none" stroke="#0369a1" stroke-width="2"/>']
    pieces += ['<text x="475" y="716" font-size="15" fill="#475569">No arbitrary IBVP theorem, neural speedup, or maximal bed-field classification.</text>', '</g></svg>']
    path.write_text("\n".join(pieces), encoding="utf-8")


def _plot(path, curves):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return {"status": "unavailable", "reason": "optional matplotlib is not installed"}
    with plt.rc_context({"svg.fonttype": "none", "font.size": 11}):
        fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
        times = np.linspace(1, 4, 100)
        for row, model in enumerate(("printed", "physical_corrected")):
            for name, exponent, grid, values, initial_integral in curves:
                if name != model:
                    continue
                axes[row, 0].plot(grid, values[0], label=f"m={exponent:g}")
                axes[row, 1].plot(times, initial_integral/times, label=f"m={exponent:g}")
            axes[row, 0].set(title=f"{model.replace('_', ' ')}: reference profile", xlabel="z=s/t", ylabel="F(z)")
            axes[row, 1].set(title="Boundary current paired with dz", xlabel="T=t", ylabel="I0/T")
            for axis in axes[row]:
                axis.grid(alpha=.25)
                axis.legend(ncol=2, fontsize=9)
        fig.suptitle("Declared scalar models: 12 classical references and moving-ray flux", fontsize=14)
        fig.savefig(path, format="svg", metadata={"Date": None})
        plt.close(fig)
    return {"status": "written", "path": path.name}


def run(root: Path, out: Path) -> dict:
    """Write JSON, a compact report, a workflow SVG and an optional plot SVG."""
    root, out = Path(root).resolve(), Path(out).resolve()
    api, jets, symbolic, numerics, tube = _modules(root)
    symbolic_records, cases = [], {}
    for physical in (False, True):
        record, case = _symbolic_model(api, jets, symbolic, physical)
        symbolic_records.append(record)
        cases[record["model"]] = case
    controls = _negative_controls(api, cases)
    numerical_records, curves, tubes = _numerical(numerics, tube)
    tube_passed = all(sp.Rational(cert["barrier_slack"]) > 0
                      and sp.Rational(cert["leading_lower"]) > 0 for cert in tubes)
    passed = all(record["status"] == "verified" for record in symbolic_records)
    passed &= all(record["passed"] for record in controls+numerical_records) and tube_passed
    out.mkdir(parents=True, exist_ok=True)
    _workflow_svg(out / "data_flux_workflow.svg")
    plot = _plot(out / "data_flux.svg", curves)
    sources = [root / "scripts/project_data_flux.py",
               *sorted((root / "symm/generic").glob("*.py")),
               *sorted((root / "research_artifacts/sve-progress-20261010/sve_lab").glob("*.py"))]
    report = {
        "schema_version": "lieml.data_flux/1", "status": "verified" if passed else "failed",
        "source_hashes": {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
        "parameters": {"g": "1", "kappa": "1/30", "z_interval": ["1", "7/5"],
                       "initial_profile_jets": ["2", "1/2", "1/10"],
                       "numerical_exponents": list(EXPONENTS), "threshold": TOLERANCE},
        "symbolic_models": symbolic_records, "negative_controls": controls,
        "reference_cases": numerical_records, "exact_reference_tubes": tubes,
        "validation": {"reference_case_count": len(numerical_records),
                       "exact_reference_tubes_passed": tube_passed,
                       "all_required_checks_passed": bool(passed)},
        "scope": {"data": "normalized three-jet values on moving ray s=t",
                  "flux": "declared scalar balance law; z-oriented current density",
                  "exact_tube": "existing exact reference family on the stated domain",
                  "sampled_guards": "numerical grid evidence, separate from the exact tube",
                  "exclusions": ["arbitrary IBVP existence or uniqueness", "maximal point classification",
                                 "full physical bed-field SVE classification", "weak/shock solutions",
                                 "neural superiority or speedup"]},
        "outputs": {"json": "data_flux.json", "markdown": "data_flux.md",
                    "workflow": "data_flux_workflow.svg", "plot": plot},
    }
    serialized = json.dumps(report, indent=2, ensure_ascii=False)+"\n"
    report = json.loads(serialized)
    (out / "data_flux.json").write_text(serialized, encoding="utf-8")
    max_error = max(row["max_profile_crosssolve_absolute_error"] for row in numerical_records)
    max_drift = max(row["first_integral_max_absolute_drift"] for row in numerical_records)
    lines = ["# Scalar symmetry, data and flux verification", "", f"Status: **{report['status']}**.", "",
             "Both scalar models use common scaling: `phi=t F(s/t)` on `t>0`, `F'>0`, `F-zF'>0`.",
             "The normalized ray `s/t=1` carries `phi/t=2`, `phi_s=1/2`, `t phi_ss=1/10`.", "",
             f"- Exact chart, data and current checks passed for {sum(row['status'] == 'verified' for row in symbolic_records)}/2 model records, with symbolic real `m` on the declared branch.",
             "- The current check uses `(T,z)=(t,s/t)`, Jacobian `T`, source zero, and boundary flux `I0/T`.",
             "- The first integral is an additional reduction of ODE order, separate from the group quotient.",
             f"- {sum(row['passed'] for row in numerical_records)}/12 reference cases passed: maximum cross-solve error `{max_error:.3e}`; integral drift `{max_drift:.3e}`; required `<=1e-9`.",
             f"- {sum(row['passed'] for row in controls)}/{len(controls)} negative controls passed: constant physical `phi=2` on the moving ray, `t=0`, and a zero chart determinant.", "",
             "Exact reference-tube bounds are recorded separately from the 401-point sampled guard checks.",
             "This verifies the declared scalar current and ray data. It supplies no arbitrary IBVP theorem,",
             "maximal physical bed-field classification, weak-solution result, or neural speedup claim.", "",
             "[Detailed evidence](data_flux.json) · [Workflow](data_flux_workflow.svg)"]
    if plot["status"] == "written":
        lines.append(" · [Reference profiles and boundary flux](data_flux.svg)")
    (out / "data_flux.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, default=ROOT / "tmp/data-flux")
    args = parser.parse_args(argv)
    report = run(args.root, args.out)
    print(json.dumps({"status": report["status"], "output": str(args.out.resolve()),
                      "validation": report["validation"]}, indent=2))
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
