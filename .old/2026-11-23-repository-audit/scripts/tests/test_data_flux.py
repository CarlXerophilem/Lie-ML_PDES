"""Acceptance checks for the declared scalar chart, data and current adapter."""

import json
import hashlib
import xml.etree.ElementTree as ET

import pytest
import sympy as sp

from scripts.project_data_flux import ROOT, _modules, _symbolic_model, check_chart_point, run


@pytest.fixture(scope="module")
def evidence(tmp_path_factory):
    out = tmp_path_factory.mktemp("data-flux")
    return run(ROOT, out), out


def test_both_scalar_models_have_exact_data_and_current_checks(evidence):
    report, _ = evidence
    assert report["status"] == "verified"
    assert {row["model"] for row in report["symbolic_models"]} == {"printed", "physical_corrected"}
    for row in report["symbolic_models"]:
        assert all(row["checks"].values())
        assert row["data_status"] == "data-compatible"
        assert row["pulled_surface"] == "z - 1"
        assert row["pulled_data"] == ["f - 2", "P - 1/2", "C - 1/10"]
        assert set(row["graph_derivative_remainders"].values()) == {"0"}
        assert row["current"]["old_from_new_jacobian"] == "T"
        assert row["current"]["source"] == "0"


def test_all_twelve_crosssolves_and_flux_time_scaling(evidence):
    report, _ = evidence
    cases = report["reference_cases"]
    assert len(cases) == 12
    assert {(row["model"], row["exponent"]) for row in cases} == {
        (model, exponent) for model in ("printed", "physical_corrected")
        for exponent in (1, 2, 2.9, 3, 3.1, 4)
    }
    for row in cases:
        assert row["passed"]
        assert row["max_profile_crosssolve_absolute_error"] <= 1e-9
        assert row["first_integral_max_absolute_drift"] <= 1e-9
        assert row["crosssolve_profile_jets"] == ["F", "Fprime", "Fsecond"]
        assert min(row["sampled_guards"].values()) > 0
        assert row["guard_evidence"] == "401 grid points; sampled"
        flux = {sample["T"]: sample["flux"] for sample in row["boundary_flux_samples"]}
        assert flux[2.] == pytest.approx(row["I0"]/2.)
        assert flux[4.] == pytest.approx(row["I0"]/4.)
        assert flux[2.] != pytest.approx(row["I0"])
    for tube in report["exact_reference_tubes"]:
        assert sp.Rational(tube["barrier_slack"]) > 0
        assert tube["scope"]["m_closed_interval"] == ["1", "4"]
        assert "exact reference family" in tube["applies_to"]


def test_negative_controls_preserve_pde_and_reject_incompatible_data(evidence):
    report, _ = evidence
    controls = report["negative_controls"]
    assert len(controls) == 5 and all(row["passed"] for row in controls)
    for row in controls:
        if row["control"].startswith("constant physical"):
            assert row["pde_status"] == "verified"
            assert row["data_status"] == "pulled-back-only"
            assert row["data_checks"]["constant-physical-phi.surface_invariant"]
            assert not row["data_checks"]["constant-physical-phi.quotient_data"]
        if row["control"] == "zero chart determinant":
            assert row["checks"]["base_rank"] is False


@pytest.mark.parametrize("time", [0, -1, sp.oo, sp.nan])
def test_singular_or_undeclared_chart_points_fail_closed(time):
    with pytest.raises(ValueError, match="t>0"):
        check_chart_point(time)


def test_chart_determinant_is_checked_independently():
    assert check_chart_point(2)["determinant"] == "1/2"
    with pytest.raises(ValueError, match="determinant"):
        check_chart_point(2, determinant=0)


def test_exact_check_rejects_omitted_time_factor_in_boundary_current(monkeypatch):
    api, jets, symbolic, _, _ = _modules(ROOT)
    original = symbolic.conservation_pullback_certificate

    def wrong_current(*args, **kwargs):
        current = original(*args, **kwargs)
        # This reproduces the tempting I0 instead of I0/T mistake.
        current["boundary_normal_flux_pullback"] *= jets.t
        return current

    monkeypatch.setattr(symbolic, "conservation_pullback_certificate", wrong_current)
    record, _ = _symbolic_model(api, jets, symbolic, False)
    assert record["status"] == "failed"
    assert not record["checks"]["boundary_flux_is_first_integral_over_T"]


def test_outputs_are_inspectable_json_markdown_and_svg(evidence):
    report, out = evidence
    assert json.loads((out / "data_flux.json").read_text()) == report
    for name, expected_hash in report["source_hashes"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected_hash
    markdown = (out / "data_flux.md").read_text()
    assert "I0/T" in markdown and "arbitrary IBVP" in markdown
    assert ET.parse(out / "data_flux_workflow.svg").getroot().tag.endswith("svg")
    if report["outputs"]["plot"]["status"] == "written":
        assert ET.parse(out / "data_flux.svg").getroot().tag.endswith("svg")
