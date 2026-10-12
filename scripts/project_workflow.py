"""Replay the manuscript's nine symmetry-analysis stages without training.

``run(root, out)`` writes inspectable JSON, Markdown and offline HTML.  A passing
replay certifies only the declared scalar identities and numerical controls;
undeclared data, full-system classification and historical learning remain
separate, explicit gates.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import html
import importlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time


ARTIFACT = Path("research_artifacts/sve-progress-20261010")
PARAMETERS = Path("draft/proposal_support/verify_parameter_effects.py")
REGULAR_BRANCH = ["t > 0", "phi_s > 0", "phi_t > 0", "g,kappa > 0",
                  "smooth local solutions and a nonzero leading coefficient"]


def _load_file(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@contextmanager
def _replay_modules(root: Path):
    """Keep package-local imports isolated from other archived experiments."""
    prefixes = ("sve_lab", "_lieml_workflow_parameters", "_lieml_workflow_run_all")
    selected = lambda name: any(name == p or name.startswith(p + ".") for p in prefixes)
    saved = {name: module for name, module in sys.modules.items() if selected(name)}
    old_path = list(sys.path)
    for name in saved:
        del sys.modules[name]
    try:
        sys.path.insert(0, str(root / ARTIFACT))
        modules = {
            "parameters": _load_file(prefixes[1], root / PARAMETERS),
            "jets": importlib.import_module("sve_lab.jets"),
            "symbolic": importlib.import_module("sve_lab.symbolic"),
            "tube": importlib.import_module("sve_lab.tube"),
            "runner": _load_file(prefixes[2], root / ARTIFACT / "run_all.py"),
        }
        yield modules
    finally:
        sys.path[:] = old_path
        for name in list(sys.modules):
            if selected(name):
                del sys.modules[name]
        sys.modules.update(saved)


def _json_safe(value):
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _check(report: dict, name: str, operation, evidence: str):
    start = time.perf_counter()
    try:
        value = operation()
        entry = {"name": name, "status": "verified", "evidence": evidence,
                 "result": _json_safe(value)}
    except Exception as exc:
        entry = {"name": name, "status": "failed", "evidence": evidence,
                 "error": f"{type(exc).__name__}: {exc}"}
    entry["elapsed_seconds"] = time.perf_counter() - start
    report["checks"].append(entry)
    return entry


def _zero(sp, expression, label):
    remainder = sp.simplify(expression)
    if remainder != 0:
        raise ValueError(f"{label}: nonzero exact remainder {remainder}")
    return str(remainder)


def _exact_replay(report: dict, modules: dict):
    import sympy as sp

    params, jets, symbolic, tube = (modules[key] for key in
                                  ("parameters", "jets", "symbolic", "tube"))
    for name in ("verify_power_diffusion", "verify_quadratic_reaction",
                 "verify_nonzero_resonance_counterexample"):
        _check(report, name, getattr(params, name), str(PARAMETERS))

    def chart():
        cert = symbolic.common_scaling_certificate()
        for name, value in cert["checks"].items():
            _zero(sp, value, name)
        _zero(sp, cert["characteristic"]["expression"] -
              (jets.u - jets.t * jets.p - jets.s * jets.q), "characteristic")
        if cert["orbit_ranks"] != {"base": 1, "total_space": 1}:
            raise ValueError("Common-scaling rank changed")
        expected = {"()": jets.u-jets.t*jets.p-jets.s*jets.q,
                    "(t)": -jets.t*jets.a-jets.s*jets.b,
                    "(s)": -jets.t*jets.b-jets.s*jets.c,
                    "(t,t)": -jets.a-jets.t*jets.r-jets.s*jets.w,
                    "(t,s)": -jets.b-jets.t*jets.w-jets.s*jets.x,
                    "(s,s)": -jets.c-jets.t*jets.x-jets.s*jets.y}
        for name, value in expected.items():
            _zero(sp, cert["differential_consequences"][name]-value, name)
        y, z, v = sp.symbols("y z v", real=True)
        inverse = {jets.t: sp.exp(y), jets.s: sp.exp(y)*z, jets.u: sp.exp(y)*v}
        for coordinate, target in ((sp.log(jets.t), y), (jets.s/jets.t, z),
                                   (jets.u/jets.t, v)):
            _zero(sp, coordinate.subs(inverse)-target, "chart inverse")
        cert["singleton_bracket"] = "[Xc,Xc] = 0"
        return cert

    _check(report, "common_scaling_chart", chart,
           str(ARTIFACT / "sve_lab/symbolic.py"))

    for physical in (False, True):
        model = "physical_corrected" if physical else "printed"

        def model_checks(physical=physical):
            recursive = symbolic.obstruction(physical)
            principal = symbolic.principal_symbol_obstruction(physical)
            checks = {
                "recursive_witness": _zero(sp, recursive["witness"]-3*jets.g*jets.kappa,
                                           "recursive obstruction witness"),
                "principal_witness": _zero(sp, principal["witness"]-3*jets.g*jets.kappa,
                                           "principal obstruction witness"),
                "independent_obstruction_agreement": _zero(
                    sp, recursive["highest_polynomial"]-principal["highest_polynomial"],
                    "recursive/principal disagreement"),
            }
            E = jets.model_residual(jets.m, physical)
            forcing = jets.g*jets.m*jets.kappa*jets.total(
                jets.p**(jets.m-1)*jets.b/jets.q, 1)
            checks["common_scaling_identity"] = _zero(
                sp, jets.act(E, jets.t, jets.s, jets.u)+2*E, "common scaling")
            checks["exceptional_generator_defect"] = _zero(
                sp, jets.act(E, jets.t, -2*jets.s, 0)+E-(jets.m-3)*forcing,
                "exceptional generator defect")
            velocity = sp.symbols("velocity", positive=True)
            checks["first_integral"] = _zero(
                sp, (symbolic.profile_total(symbolic.first_integral(jets.m, physical))
                     - symbolic.reduced_residual(jets.m, physical)).subs(
                         symbolic.f, velocity+symbolic.z*symbolic.P), "first integral")
            checks["independent_direct_pullbacks"] = {
                str(exponent): _zero(sp, symbolic.direct_pullback(exponent, physical)
                                    -symbolic.reduced_residual(exponent, physical),
                                    f"direct pullback m={exponent}")
                for exponent in (1, 2, 3, 4)
            }
            conservation = symbolic.conservation_pullback_certificate(jets.m, physical)
            for name, value in conservation["checks"].items():
                _zero(sp, value, name)
            rational_tube = tube.tube_certificate(physical)
            for name in ("leading_lower", "velocity_lower", "barrier_slack"):
                if sp.Rational(rational_tube[name]) <= 0:
                    raise ValueError(f"Nonpositive exact reference tube {name}")
            return {"checks": checks, "obstruction_witness": str(recursive["witness"]),
                    "generator_scope": "arbitrary smooth tau(t,s,u), xi(t,s,u), eta(t,s,u)",
                    "conservation": conservation, "reference_tube": rational_tube}

        _check(report, f"scalar_model_{model}", model_checks,
               str(ARTIFACT / "sve_lab/symbolic.py"))

    def physical_reconstruction():
        compatibility, residual = symbolic.physical_audit()
        return {"bed_compatibility_remainder": _zero(sp, compatibility-residual,
                                                   "bed compatibility")}

    _check(report, "local_bed_reconstruction", physical_reconstruction,
           str(ARTIFACT / "sve_lab/symbolic.py"))


def _historical(root: Path):
    path = root / ARTIFACT / "results/experiment_results.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data["cases"]
    return {"status": "historical-not-rerun", "evidence": str(ARTIFACT /
            "results/experiment_results.json"), "case_count": len(cases),
            "budget_exhausted": sum(not row["optimizer_success"] for row in cases),
            "methods": sorted({row["method"] for row in cases}),
            "cases": cases, "scope": data["scope"],
            "limitations": data["protocol"]["comparison_limitations"],
            "training_performed": False}


def _classical_replay(modules: dict, out: Path):
    destination = out / "classical"
    destination.mkdir(parents=True, exist_ok=True)
    rows = modules["runner"].classical(destination)
    if len(rows) != 12:
        raise ValueError(f"Expected 12 classical controls, found {len(rows)}")
    error_keys = ("two_vs_three_order_error", "first_integral_drift", "bed_time_equation_error")
    for row in rows:
        for key in error_keys:
            if not math.isfinite(row[key]) or row[key] > 1e-8:
                raise ValueError(f"Classical control failed: {row['model']} m={row['m']} {key}")
        for key in ("min_phi_s", "min_phi_t", "min_abs_leading"):
            if not math.isfinite(row[key]) or row[key] <= 0:
                raise ValueError(f"Sampled classical guard failed: {key}")
    return {"status": "numerically-replayed", "case_count": len(rows),
            "cases": rows, "consistency_tolerance": 1e-8,
            "maximum_discrepancies": {key: max(row[key] for row in rows) for key in error_keys},
            "evidence": "classical/classical_results.json",
            "scope": "constructed smooth invariant data; numerical agreement is not an absolute error bound",
            "guard_evidence": "sampled; exact reference-family tube is certified separately"}


def _validate_data_report(root: Path, payload: dict):
    """Accept only current, passing evidence for the constructed moving ray."""
    import sympy as sp

    if payload.get("schema_version") != "lieml.data_flux/1" or payload.get("status") != "verified":
        raise ValueError("Data report schema/status is not verified")
    validation = payload.get("validation", {})
    if (validation.get("all_required_checks_passed") is not True
            or validation.get("exact_reference_tubes_passed") is not True
            or validation.get("reference_case_count") != 12):
        raise ValueError("Required data-report validation gates did not pass")
    paths = {root / "scripts/project_data_flux.py"}
    paths.update((root / "symm/generic").glob("*.py"))
    paths.update((root / ARTIFACT / "sve_lab").glob("*.py"))
    hashes = payload.get("source_hashes", {})
    for path in sorted(paths):
        name = path.relative_to(root).as_posix()
        if not path.is_file() or hashes.get(name) != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError(f"Missing or stale data-report source hash: {name}")
    required_checks = {"generic_chart_verified", "normalized_ray_data_compatible",
                       "generic_matches_independent_profile_equation",
                       "all_invariant_graph_derivatives_through_order_two",
                       "old_from_new_jacobian_T", "current_divergence_identity",
                       "density_pullback", "source_zero",
                       "boundary_flux_is_first_integral_over_T",
                       "first_integral_derivative_equals_reduced_equation"}
    models = payload.get("symbolic_models", [])
    if len(models) != 2 or {row["model"] for row in models} != {"printed", "physical_corrected"}:
        raise ValueError("Both scalar models must have data evidence")
    for model in models:
        checks = model.get("checks", {})
        if (model.get("status") != "verified" or model.get("data_status") != "data-compatible"
                or not required_checks.issubset(checks)
                or any(value is not True for value in checks.values())
                or not model.get("data_checks")
                or any(value is not True for value in model["data_checks"].values())
                or model.get("pulled_surface") != "z - 1"
                or model.get("pulled_data") != ["f - 2", "P - 1/2", "C - 1/10"]):
            raise ValueError(f"Exact constructed data checks failed: {model['model']}")
    controls = payload.get("negative_controls", [])
    if len(controls) != 5 or any(row.get("passed") is not True for row in controls):
        raise ValueError("All five incompatible-data/singular-chart controls must pass")
    references = payload.get("reference_cases", [])
    expected = {(model, exponent) for model in ("printed", "physical_corrected")
                for exponent in (1, 2, 2.9, 3, 3.1, 4)}
    if len(references) != 12 or {(row["model"], row["exponent"]) for row in references} != expected:
        raise ValueError("Constructed data report must contain twelve distinct reference cases")
    for row in references:
        if row.get("passed") is not True:
            raise ValueError("A numerical reference control did not pass")
        for name in ("max_profile_crosssolve_absolute_error", "first_integral_max_absolute_drift"):
            value = row[name]
            if isinstance(value, bool) or not math.isfinite(value) or not 0 <= value <= 1e-9:
                raise ValueError(f"Data-report numerical control failed: {name}")
    tubes = payload.get("exact_reference_tubes", [])
    if len(tubes) != 2 or {row["model"] for row in tubes} != {"printed", "physical_corrected"}:
        raise ValueError("Both exact reference-family tubes are required")
    for tube in tubes:
        for name in ("barrier_slack", "leading_lower", "velocity_lower"):
            if sp.Rational(tube[name]) <= 0:
                raise ValueError(f"Nonpositive data-report rational tube: {name}")
    return hashes


def _data_gate(root: Path, out: Path, data_report: Path | None = None):
    gate = {"status": "pending-specific-IBVP", "passed": False, "evidence": [],
            "scope": "constructed normalized three-jet ray s=t only; arbitrary physical IBVPs remain separate"}
    candidates = ([Path(data_report).resolve()] if data_report is not None else
                  [out.parent / "data-flux/data_flux.json", root / "build/data-flux/data_flux.json"])
    # An explicitly selected or colocated failed report must not be bypassed by
    # an older successful report elsewhere.
    path = next((path for path in candidates if path.is_file()), None)
    if path is None:
        gate["reason"] = "No constructed data/flux report is available"
        return gate
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        hashes = _validate_data_report(root, payload)
    except Exception as exc:
        gate["rejected_report"] = {"path": str(path), "reason": f"{type(exc).__name__}: {exc}"}
        return gate
    gate.update(status="verified-constructed-data-flux", passed=True, evidence=[str(path)],
                report_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), source_hashes=hashes)
    return gate


def _stages(report: dict):
    verified = report["checks_passed"]
    exact = "verified" if verified else "failed"
    check_evidence = ["workflow.json#checks", str(ARTIFACT / "docs/THEORY.md")]
    records = [
        ("Freeze the model", exact, "Two declared scalar models; nondimensional fixed g,kappa and positive branch.", check_evidence),
        ("Verify symmetry candidates", exact, "Parameter examples and exact Xc/X5 identities; first-order X5 obstruction. No independent maximal classification.", check_evidence),
        ("Select subgroup and rank", exact, "Singleton Xc is bracket closed; local projected and total rank are one.", check_evidence),
        ("Construct the quotient chart", exact, "y=log(t), z=s/t, v=phi/t; exact inverse and Jacobian checks.", check_evidence),
        ("Pull back jets and data", "partial" if verified else "failed", "Exact invariant-surface consequences through order two; a specific physical IBVP remains a separate gate.", check_evidence),
        ("Certify reduced equations", exact, "Independent direct pullbacks at m=1,2,3,4; arbitrary-m scaling and first-integral identities.", check_evidence),
        ("Approximate the profile", "numerically-replayed" if verified else "blocked", "Twelve classical controls regenerated; 40 stored comparisons are historical, including 16 exhausted budgets. No training.", ["classical/classical_results.json", str(ARTIFACT / "results/experiment_results.json")]),
        ("Reconstruct and validate", "numerically-replayed" if verified else "blocked", "Local bed compatibility, exact reference-family rational tube, and independent second-/third-order controls. Candidate guards remain sampled.", check_evidence+["classical/classical_results.json"]),
        ("Report scope and total cost", "verified" if verified else "failed", "Source hashes, exact/numerical distinctions, failures and historical budgets retained; no measured neural speedup.", ["workflow.json", "workflow.md"]),
    ]
    stages = [{"id": i, "title": title, "status": status, "scope": scope,
               "assumptions": REGULAR_BRANCH, "evidence": list(evidence)}
              for i, (title, status, scope, evidence) in enumerate(records, 1)]
    stages[4]["evidence"] += report["data_compatibility"]["evidence"]
    if verified and report["data_compatibility"]["passed"]:
        stages[4]["status"] = "verified"
        stages[4]["scope"] = ("Exact jet pullbacks and compatible normalized three-jet data on s=t; "
                               "the declared scalar density/source/flux and incompatible controls pass. "
                               "Arbitrary physical IBVPs remain separate.")
    return stages


def _evidence_href(path: str, root: Path, out: Path):
    name, separator, fragment = path.partition("#")
    destination = (out if name.startswith(("workflow.", "classical/")) else root) / name
    return os.path.relpath(destination, out) + (separator + fragment if separator else "")


def _evidence_label(path: str):
    name, _, fragment = path.partition("#")
    filename = Path(name).name
    labels = {"THEORY.md": "Scalar theory", "data_flux.json": "Data and flux checks",
              "classical_results.json": "Classical controls",
              "experiment_results.json": "Historical comparisons",
              "workflow.md": "Readable report", "workflow.json": "Detailed report"}
    return "Exact checks" if filename == "workflow.json" and fragment == "checks" else labels.get(filename, filename)


def _markdown(report: dict, root: Path, out: Path):
    lines = ["# Manuscript symmetry workflow", "", f"Replay: **{report['status']}**. "
             f"Workflow: **{report['workflow_status']}**.", "",
             "A passing replay applies to the declared scalar benchmark and constructed reference family. "
             "It does not establish maximal SVE classification, full physical IBVP equivalence, or neural speedup.", "",
             "| Stage | Status | Evidence and scope |", "|---|---|---|"]
    for stage in report["stages"]:
        links = ", ".join(f"[{_evidence_label(path)}]({_evidence_href(path, root, out)})"
                          for path in stage["evidence"])
        lines.append(f"| {stage['id']}. {stage['title']} | {stage['status']} | {stage['scope']} {links} |")
    lines += ["", "## Replay checks", ""]
    for check in report["checks"]:
        lines.append(f"- {check['name']}: **{check['status']}**" +
                     (f" — {check['error']}" if "error" in check else ""))
    historical = report.get("historical_comparisons", {})
    lines += ["", f"Historical comparisons: {historical.get('case_count', 'unavailable')}; "
              f"budget exhausted: {historical.get('budget_exhausted', 'unavailable')}. "
              "These are stored measurements; no learning was rerun.", "",
              "Specific data/flux compatibility: " + report["data_compatibility"]["status"] + ".", "",
              "Exact and numerical results, source hashes, per-case controls and historical failures are in workflow.json.", ""]
    return "\n".join(lines)


def _html(report: dict, root: Path, out: Path):
    palette = {"verified": "#15735f", "partial": "#9b6500", "pending": "#9b6500",
               "numerically-replayed": "#275c9b", "failed": "#b32936", "blocked": "#737c87"}
    nodes = []
    for stage in report["stages"]:
        idx = stage["id"]-1
        row, column = divmod(idx, 3)
        x, y = 24+column*320, 24+row*152
        color = palette[stage["status"]]
        label = html.escape(f"{stage['id']}. {stage['title']}")
        nodes.append(f'<a href="#stage-{stage["id"]}"><rect x="{x}" y="{y}" width="290" height="112" rx="12" fill="white" stroke="{color}" stroke-width="2"/>'
                     f'<text x="{x+15}" y="{y+35}" fill="#17212e">{label}</text>'
                     f'<text x="{x+15}" y="{y+67}" fill="{color}" font-size="13">{html.escape(stage["status"])}</text></a>')
        if column < 2:
            nodes.append(f'<path d="M{x+292},{y+56} h25" stroke="#788492" marker-end="url(#arrow)"/>')
        elif row < 2:
            nodes.append(f'<path d="M{x+145},{y+114} v19 H12 V{y+152+56} H22" fill="none" stroke="#788492" marker-end="url(#arrow)"/>')
    sections = []
    for stage in report["stages"]:
        evidence = " ".join(f'<a href="{html.escape(_evidence_href(path, root, out), quote=True)}">'
                            f'{html.escape(_evidence_label(path))}</a>' for path in stage["evidence"])
        sections.append(f'<article id="stage-{stage["id"]}"><h2>{stage["id"]}. {html.escape(stage["title"])}</h2>'
                        f'<p><strong>{html.escape(stage["status"])}</strong> — {html.escape(stage["scope"])}</p>'
                        f'<p class="evidence">Evidence: {evidence}</p></article>')
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Manuscript symmetry workflow</title><style>body{margin:0;background:#f3f5f8;color:#17212e;font:16px/1.6 system-ui,sans-serif}'
            'main{max-width:1000px;margin:32px auto;padding:20px}h1{font-size:30px}svg{width:100%;height:auto;font:15px system-ui,sans-serif}'
            'article{background:white;padding:16px 24px;margin:16px 0;border-radius:12px}h2{font-size:20px;margin:0}code{font-size:12px;overflow-wrap:anywhere}'
            '.evidence{color:#475364}a:focus rect{stroke-width:4}</style><main><h1>Manuscript symmetry workflow</h1>'
            f'<p>Replay: <strong>{html.escape(report["status"])}</strong>. Workflow: <strong>{html.escape(report["workflow_status"])}</strong>.</p>'
            '<p>Green: exact scoped identities. Blue: numerical controls. Amber: incomplete data gate. '
            'Historical learning results were read without training. Maximal classification and full physical IBVP claims remain separate.</p>'
            '<svg viewBox="0 0 980 468" role="img" aria-label="Nine manuscript analysis stages with exact and numerical statuses">'
            '<defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#788492"/></marker></defs>'
            +''.join(nodes)+'</svg>'+''.join(sections)+'<p>Assumptions: '+html.escape('; '.join(REGULAR_BRANCH))+
            '. The exact rational tube concerns the reference family; learned-candidate branch checks remain sampled.</p>'
            '<p>See <a href="workflow.json">workflow.json</a> for all checks, numerical controls, historical runs and source hashes.</p></main></html>\n')


def run(root: Path, out: Path, *, data_report: Path | None = None) -> dict:
    """Replay existing mathematical code and write reports under ``out`` only."""
    root, out = Path(root).resolve(), Path(out).resolve()
    if out == root or out == root / ARTIFACT or root / ARTIFACT in out.parents:
        raise ValueError("Choose an output directory outside the frozen experimental artifact")
    if not __debug__:
        raise RuntimeError("Replay requires Python assertions enabled in existing verification scripts")
    out.mkdir(parents=True, exist_ok=True)
    report = {"schema": "lieml.manuscript-workflow.v1", "status": "failed", "checks": [],
              "created_utc": datetime.now(timezone.utc).isoformat(), "manuscript": "draft/main.tex",
              "scope": "two declared scalar SVE models and parameter-position verification examples",
              "assumptions": REGULAR_BRANCH, "training_performed": False}
    sources = [root / "draft/main.tex", root / PARAMETERS, root / "scripts/project_workflow.py"]
    sources += sorted((root / ARTIFACT).glob("sve_lab/*.py"))
    sources += [root / ARTIFACT / name for name in
                ("run_all.py", "MANIFEST.json", "lie-ml-sve-progress-20261010.zip",
                 "results/experiment_results.json", "results/symbolic_certificates.json")]
    report["source_hashes"] = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                               if path.is_file() else None for path in sources}
    try:
        report["historical_comparisons"] = _historical(root)
        with _replay_modules(root) as modules:
            runner = modules["runner"]
            report["environment"] = {"python": sys.version.split()[0],
                                     "numpy": runner.np.__version__,
                                     "scipy": runner.scipy.__version__,
                                     "sympy": runner.sp.__version__}
            _exact_replay(report, modules)
            if all(check["status"] == "verified" for check in report["checks"]):
                control = _check(report, "classical_controls", lambda: _classical_replay(modules, out),
                                 "classical/classical_results.json")
                if control["status"] == "verified":
                    report["classical_controls"] = control["result"]
    except Exception as exc:
        report["checks"].append({"name": "replay_inputs", "status": "failed",
                                 "error": f"{type(exc).__name__}: {exc}", "evidence": str(ARTIFACT)})
    report["checks_passed"] = bool(report["checks"]) and all(
        check["status"] == "verified" for check in report["checks"])
    report["status"] = "passed" if report["checks_passed"] else "failed"
    report["data_compatibility"] = _data_gate(root, out, data_report)
    if not report["checks_passed"]:
        report["workflow_status"] = "failed"
    elif report["data_compatibility"]["passed"]:
        report["workflow_status"] = "scoped-replay-complete"
        report["source_hashes"].update(report["data_compatibility"]["source_hashes"])
    else:
        report["workflow_status"] = "pending-data-compatibility"
    report["stages"] = _stages(report)
    report["outputs"] = {kind: str(out / f"workflow.{kind}") for kind in ("json", "md", "html")}
    (out / "workflow.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    (out / "workflow.md").write_text(_markdown(report, root, out), encoding="utf-8")
    (out / "workflow.html").write_text(_html(report, root, out), encoding="utf-8")
    return report
