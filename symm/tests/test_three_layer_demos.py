"""Contract tests for the three independent research demos."""

from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import torch


ROOT = Path(__file__).resolve().parents[2]


def _module(name: str):
    return importlib.import_module(f"symm.research_demos.{name}")


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_demo_modules_preserve_layer_boundaries():
    package = ROOT / "symm" / "research_demos"
    ml_imports = _imports(package / "ml_only.py")
    lie_imports = _imports(package / "lie_only.py")
    assert not any(name == "symm.generic" or name.startswith("symm.generic.") for name in ml_imports)
    assert not any(name == "torch" or name.startswith("torch.") for name in lie_imports)
    assert not any(name == "kan" or name.startswith("kan.") for name in lie_imports)


def test_lie_only_report_verifies_cubic_case_and_rejects_m4(tmp_path):
    lie = _module("lie_only")
    report = lie.run_demo(tmp_path, make_plot=False)
    cubic = report["cases"]["m3"]
    negative = report["cases"]["m4"]
    assert report["schema"] == "lieml.three-layer.lie-only.v1"
    assert cubic["certificate"]["status"] == "verified"
    assert all(cubic["certificate"]["checks"].values())
    assert cubic["invariant_surface_zero"] is True
    assert cubic["lifting_identity_zero"] is True
    assert cubic["exact_control_zero"] is True
    assert cubic["invariant"] == "sigma = s*t**2"
    assert negative["certificate"]["status"] == "unsupported"
    assert negative["symmetry_identity_zero"] is False
    saved = json.loads((tmp_path / "lie_only_report.json").read_text(encoding="utf-8"))
    assert saved["cases"]["m3"]["certificate"]["status"] == "verified"


def test_lie_only_emits_strict_data_compatible_v02_certificate(tmp_path):
    lie = _module("lie_only")
    lie.run_demo(tmp_path, make_plot=False)
    path = tmp_path / "sve_certificate_v02.json"
    assert path.is_file()
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["schema"] == "lieml.sve.reduction-certificate.v0.2"
    assert report["status"] == "verified-regular-data-compatible"
    assert report["fixed_branch"]["m"] == 3
    assert report["fixed_branch"]["delta_m"] == 0
    assert report["structural_classification"] == {
        "independent_variables": 2,
        "dependent_fields": 1,
        "equations": 1,
        "order": 3,
        "jet_structure": ["rational"],
    }
    assert report["data_compatibility"]["surface"] == "sigma - 1"
    assert all(report["data_compatibility"]["checks"].values())
    assert report["data_compatibility"]["status"] == "data-compatible"
    assert report["exact_branch_guards"]["chart_rank"] == "-rho**2"
    assert report["exact_branch_guards"]["orbit_speed"] == "rho"
    assert "F_prime" in report["singular_boundaries"]
    assert "leading_coefficient" in report["singular_boundaries"]
    assert report["claims"]["generic_m_classified"] is False
    assert report["claims"]["m3_delta_continuation_proved"] is False


def test_lifting_label_uses_pullback_identity_not_only_orbit_independence():
    lie = _module("lie_only")
    certificate = SimpleNamespace(
        status="unsupported",
        checks=(("orbit_independent_equations", True), ("pullback_identity", False)),
        residuals=(), covered_guards=(), message="fixture", system_fingerprint="system",
        configuration_fingerprint="configuration",
    )
    outcome = SimpleNamespace(
        certificate=certificate,
        reduced_system=SimpleNamespace(equations=(0,)),
        regularity_conditions=(),
    )
    assert lie._m3_details(outcome)["lifting_identity_zero"] is False


def test_ml_model_parameter_counts_match_declared_logistic_benchmark():
    ml = _module("ml_only")
    mlp = ml.build_logistic_model("mlp", seed=0)
    pikan = ml.build_logistic_model("pikan", seed=0)
    assert ml.trainable_parameter_count(mlp) == 121
    assert ml.trainable_parameter_count(pikan) == 112
    symbolic = [p.requires_grad for n, p in pikan.named_parameters() if n.startswith("symbolic_fun")]
    assert symbolic and not any(symbolic)


def test_fusion_rejects_an_unverified_reduction_certificate(tmp_path):
    fusion = _module("fusion")
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({
        "schema": "lieml.three-layer.lie-only.v1",
        "cases": {"m3": {"certificate": {"status": "unsupported", "checks": {}}}},
    }), encoding="utf-8")
    with pytest.raises(fusion.CertificateError, match="verified"):
        fusion.load_verified_certificate(path)


@pytest.mark.parametrize("order, power", [(2, 3), (4, 5)])
def test_hard_profile_preserves_declared_initial_jets(order, power):
    fusion = _module("fusion")
    initial = fusion.perturbed_initial_state()
    model = fusion.HardProfile(order=order, initial=initial, seed=0)
    assert model.correction_power == power
    sigma = torch.ones((1, 1), dtype=torch.float64, requires_grad=True)
    jets = fusion.profile_jets(model, sigma)
    actual = np.array([value.detach().item() for value in jets[:3]])
    np.testing.assert_allclose(actual, initial, rtol=0, atol=1e-12)


def test_direct_master_and_lifted_reduced_residual_agree():
    fusion = _module("fusion")
    model = fusion.HardProfile(order=2, initial=fusion.perturbed_initial_state(), seed=1)
    check = fusion.original_master_check(model, grid_size=5)
    assert check["direct_vs_lift_max_abs"] < 1e-9


def test_ml_only_smoke_writes_machine_readable_table_and_figure(tmp_path):
    ml = _module("ml_only")
    report = ml.run_demo(tmp_path, logistic_iterations=1, duffing_iterations=1,
                         seeds=range(1), logistic_seeds=range(1))
    assert report["status"] == "completed"
    assert (tmp_path / "ml_only_runs.csv").is_file()
    assert (tmp_path / "ml_only_comparison.png").is_file()


def test_fusion_smoke_writes_table_and_figure_from_verified_certificate(tmp_path):
    lie = _module("lie_only")
    fusion = _module("fusion")
    certificate_dir = tmp_path / "lie"
    lie.run_demo(certificate_dir, make_plot=False)
    output = tmp_path / "fusion"
    report = fusion.run_demo(certificate_dir / "lie_only_report.json", output,
                             steps=1, seeds=range(1))
    assert report["status"] == "completed"
    for name in ("exact_unperturbed", "taylor_p2", "taylor_p4"):
        assert "raw_residual_max_abs" in report["controls"][name]
        assert "normalized_residual_max_abs" in report["controls"][name]
        assert "direct_master_max_abs" in report["controls"][name]
    assert report["reference"]["DOP853_seconds"] >= 0
    assert report["reference"]["Radau_seconds"] >= 0
    ladder = report["reference"]["DOP853_tolerance_ladder"]
    assert [row["name"] for row in ladder] == ["coarse", "medium", "fine"]
    assert ladder[-1]["difference_to_fine_max_abs"] == 0
    assert ladder[0]["difference_to_fine_max_abs"] >= ladder[1]["difference_to_fine_max_abs"]
    assert (output / "fusion_runs.csv").is_file()
    assert (output / "fusion_comparison.png").is_file()
