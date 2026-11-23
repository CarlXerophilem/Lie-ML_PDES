"""Safety and evidence-boundary checks for the manuscript workflow replay."""

import importlib
import json
from pathlib import Path
import sys
from types import ModuleType

import pytest

from scripts import project_workflow as workflow


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def replay(tmp_path_factory):
    out = tmp_path_factory.mktemp("workflow")
    report = workflow.run(ROOT, out, data_report=out / "absent-data-report.json")
    return report, out


def test_actual_replay_preserves_mathematical_scope(replay):
    report, out = replay
    assert report["status"] == "passed", report["checks"]
    assert [stage["id"] for stage in report["stages"]] == list(range(1, 10))
    assert report["workflow_status"] == "pending-data-compatibility"
    assert report["stages"][4]["status"] == "partial"
    assert "No independent maximal classification" in report["stages"][1]["scope"]
    assert report["classical_controls"]["case_count"] == 12
    assert report["historical_comparisons"]["case_count"] == 40
    assert report["historical_comparisons"]["budget_exhausted"] == 16
    assert report["training_performed"] is False
    assert json.loads((out / "workflow.json").read_text())["checks_passed"]
    visual = (out / "workflow.html").read_text()
    assert "<svg" in visual and "<script src=" not in visual
    assert "reference family" in visual and "remain sampled" in visual


def test_nonzero_exact_identity_blocks_classical_controls(monkeypatch, tmp_path):
    import sympy as sp

    load_file = workflow._load_file

    def corrupt_chart(name, path):
        module = load_file(name, path)
        if name == "_lieml_workflow_run_all":
            symbolic = importlib.import_module("sve_lab.symbolic")
            original = symbolic.common_scaling_certificate

            def bad_certificate():
                cert = original()
                cert["checks"]["Xc_z"] = sp.Integer(1)
                return cert

            symbolic.common_scaling_certificate = bad_certificate

            def forbidden_classical(_):
                pytest.fail("Numerical work must not bypass a failed exact gate")

            module.classical = forbidden_classical
        return module

    monkeypatch.setattr(workflow, "_load_file", corrupt_chart)
    report = workflow.run(ROOT, tmp_path)
    assert report["status"] == "failed"
    assert not (tmp_path / "classical").exists()
    chart = next(check for check in report["checks"] if check["name"] == "common_scaling_chart")
    assert "nonzero exact remainder" in chart["error"]
    assert report["stages"][6]["status"] == "blocked"


def test_archive_imports_do_not_replace_callers_modules(tmp_path):
    sentinel = ModuleType("sve_lab")
    old = sys.modules.get("sve_lab")
    old_path = list(sys.path)
    sys.modules["sve_lab"] = sentinel
    try:
        with workflow._replay_modules(ROOT) as modules:
            assert modules["symbolic"].__file__.startswith(str(ROOT / workflow.ARTIFACT))
            assert sys.modules["sve_lab"] is not sentinel
        assert sys.modules["sve_lab"] is sentinel
        assert sys.path == old_path
    finally:
        if old is None:
            sys.modules.pop("sve_lab", None)
        else:
            sys.modules["sve_lab"] = old


def test_output_cannot_overwrite_frozen_experiment():
    with pytest.raises(ValueError, match="outside the frozen"):
        workflow.run(ROOT, ROOT / workflow.ARTIFACT / "results")


@pytest.fixture(scope="module")
def data_evidence(tmp_path_factory):
    from scripts.project_data_flux import run

    out = tmp_path_factory.mktemp("data-gate") / "data-flux"
    return run(ROOT, out), out / "data_flux.json"


def test_current_constructed_data_gate_completes_scoped_workflow(data_evidence, tmp_path):
    _, path = data_evidence
    report = workflow.run(ROOT, tmp_path, data_report=path)
    assert report["status"] == "passed"
    assert report["workflow_status"] == "scoped-replay-complete"
    assert report["data_compatibility"]["passed"]
    assert report["stages"][4]["status"] == "verified"
    assert "Arbitrary physical IBVPs remain separate" in report["stages"][4]["scope"]
    assert str(path) in report["stages"][4]["evidence"]


@pytest.mark.parametrize("corruption", ["failed", "stale", "missing_hash", "false_check", "nan_error"])
def test_failed_or_stale_data_report_never_certifies(data_evidence, tmp_path, corruption):
    original, _ = data_evidence
    payload = json.loads(json.dumps(original))
    if corruption == "failed":
        payload["status"] = "failed"
    elif corruption == "stale":
        payload["source_hashes"]["symm/generic/chart_reduction.py"] = "0" * 64
    elif corruption == "missing_hash":
        del payload["source_hashes"]["scripts/project_data_flux.py"]
    elif corruption == "false_check":
        payload["symbolic_models"][0]["checks"]["normalized_ray_data_compatible"] = False
    else:
        payload["reference_cases"][0]["max_profile_crosssolve_absolute_error"] = float("nan")
    path = tmp_path / "data-flux/data_flux.json"
    path.parent.mkdir()
    path.write_text(json.dumps(payload))
    gate = workflow._data_gate(ROOT, tmp_path / "workflow")
    assert not gate["passed"]
    assert gate["status"] == "pending-specific-IBVP"
    assert gate["evidence"] == []
    assert gate["rejected_report"]["reason"]
