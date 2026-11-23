"""Contracts for the branch-aware SVE certificate v0.2 family demo."""

from __future__ import annotations

import copy
import json

import numpy as np
import pytest
import torch


def test_declared_parameter_split_is_disjoint_and_inside_candidate_interval():
    from symm.research_demos import sve_family

    train = set(sve_family.TRAIN_ETAS)
    heldout = set(sve_family.HELDOUT_ETAS)
    assert train
    assert heldout
    assert train.isdisjoint(heldout)
    assert min(train | heldout) >= -0.02
    assert max(train | heldout) <= 0.02
    assert len(sve_family.BRANCH_PLOT_TICKS) <= 5
    assert sve_family.BRANCH_PLOT_TICKS[0] == -0.02
    assert sve_family.BRANCH_PLOT_TICKS[-1] == 0.02


def test_branch_classifier_preserves_distinct_failure_statuses():
    from symm.research_demos import sve_family

    sigma = np.array([1.0, 1.5])
    regular = np.array([[3.5, 4.0], [1.0, 0.8], [-0.2, -0.1]])
    assert sve_family.classify_branch_samples(sigma, regular, 1e-12)["status"] == "regular"
    assert sve_family.classify_branch_samples(
        sigma, regular, 1e-12, rank_ok=False)["status"] == "rank-drop"

    zero_slope = regular.copy()
    zero_slope[1, 1] = 0.0
    assert sve_family.classify_branch_samples(
        sigma, zero_slope, 1e-12)["status"] == "singular-Fprime"

    root = np.cbrt(2.0 / 7.2)
    zero_leading = np.array([[3.5], [root], [0.0]])
    assert sve_family.classify_branch_samples(
        np.array([1.0]), zero_leading, 1e-12)["status"] == "singular-leading"
    assert sve_family.classify_branch_samples(
        sigma, regular, 1e-4)["status"] == "reference-disagreement"
    assert sve_family.reference_case(float("nan"))["status"] == "solver-failure"


def test_reference_family_records_every_eta_and_cross_solver_agreement(tmp_path):
    from symm.research_demos import lie_only, sve_family

    lie_only.run_demo(tmp_path, make_plot=False)
    certificate = sve_family.load_verified_v02_certificate(
        tmp_path / "sve_certificate_v02.json")
    assert certificate["data_compatibility"]["status"] == "data-compatible"
    etas = (-0.02, -0.005, 0.0, 0.0125, 0.02)
    records, solutions = sve_family.build_reference_family(etas)
    assert [record["eta_ic"] for record in records] == list(etas)
    assert set(solutions) == set(etas)
    assert all(record["status"] == "regular" for record in records)
    assert all(record["cross_solver_max_abs"] < 1e-9 for record in records)
    assert all(record["minimum_F_prime"] > 0 for record in records)
    assert all(record["minimum_abs_leading_coefficient"] > 0 for record in records)

    bad = json.loads((tmp_path / "sve_certificate_v02.json").read_text(encoding="utf-8"))
    bad["data_compatibility"]["status"] = "pulled-back-only"
    bad_path = tmp_path / "bad-v02.json"
    bad_path.write_text(json.dumps(bad), encoding="utf-8")
    try:
        sve_family.load_verified_v02_certificate(bad_path)
    except sve_family.CertificateError as exc:
        assert "data-compatible" in str(exc)
    else:
        raise AssertionError("data-incompatible certificate was accepted")


def test_v02_loader_rejects_a_mislabeled_branch_or_proof_payload(tmp_path):
    from symm.research_demos import lie_only, sve_family

    lie_only.run_demo(tmp_path, make_plot=False)
    source = json.loads(
        (tmp_path / "sve_certificate_v02.json").read_text(encoding="utf-8"))
    defects = (
        ("wrong-m", ("fixed_branch", "m"), 4),
        ("nonzero-delta", ("fixed_branch", "delta_m"), 0.1),
        ("nonzero-data-proof", ("data_compatibility", "invariance_residuals"),
         ["0", "0", "0", "1"]),
        ("zero-rank-guard", ("exact_branch_guards", "chart_rank"), "0"),
        ("wrong-family", ("parameter_family", "name"), "delta_m"),
    )
    for name, path, value in defects:
        bad = copy.deepcopy(source)
        bad[path[0]][path[1]] = value
        bad_path = tmp_path / f"{name}.json"
        bad_path.write_text(json.dumps(bad), encoding="utf-8")
        with pytest.raises(sve_family.CertificateError):
            sve_family.load_verified_v02_certificate(bad_path)


def test_conditional_hard_profile_preserves_three_jets_for_unseen_eta():
    from symm.research_demos import fusion, sve_family

    model = sve_family.ConditionalHardProfile(seed=0)
    for eta_ic in (-0.0125, 0.005, 0.0125):
        sigma = torch.ones((1, 1), dtype=torch.float64, requires_grad=True)
        eta = torch.full_like(sigma, eta_ic)
        jets = sve_family.conditional_profile_jets(model, sigma, eta)[:3]
        actual = np.array([value.detach().item() for value in jets])
        np.testing.assert_allclose(actual, fusion.perturbed_initial_state(eta_ic),
                                   rtol=0, atol=1e-12)


def test_conditional_profile_keeps_direct_and_lifted_residuals_equal():
    from symm.research_demos import fusion, sve_family

    model = sve_family.ConditionalHardProfile(seed=1)
    fixed = sve_family.FixedEtaProfile(model, eta_ic=0.005)
    check = fusion.original_master_check(fixed, grid_size=5)
    assert check["direct_vs_lift_max_abs"] < 1e-9


def test_amortization_break_even_requires_positive_online_advantage():
    from symm.research_demos import sve_family

    assert sve_family.amortization_break_even(10.0, 0.003, 0.001) == 5000
    assert sve_family.amortization_break_even(10.0, 0.003, 0.003) is None
    assert sve_family.amortization_break_even(10.0, 0.003, 0.004) is None


def test_family_smoke_trains_only_on_train_parameters_and_reports_heldout(tmp_path):
    from symm.research_demos import lie_only, sve_family

    certificate_dir = tmp_path / "certificate"
    lie_only.run_demo(certificate_dir, make_plot=False)
    output = tmp_path / "family"
    report = sve_family.run_demo(
        certificate_dir / "sve_certificate_v02.json",
        output,
        steps=1,
        seeds=range(1),
        train_etas=(-0.02, 0.0, 0.02),
        heldout_etas=(-0.005, 0.005),
        collocation_points=8,
    )
    assert report["schema"] == "lieml.sve.parameter-family.v0.2"
    assert report["status"] == "completed"
    assert set(report["split"]["train_eta_ic"]).isdisjoint(report["split"]["heldout_eta_ic"])
    assert len(report["references"]) == 5
    assert len(report["runs"]) == 2
    assert {run["eta_ic"] for run in report["runs"]} == {-0.005, 0.005}
    assert all(run["split"] == "heldout" for run in report["runs"])
    for run in report["runs"]:
        assert "F_max_abs_error" in run["metrics"]
        assert "raw_residual_max_abs" in run["metrics"]
        assert "direct_master_max_abs" in run["metrics"]
        assert "direct_vs_lift_max_abs" in run["metrics"]
    assert report["cost"]["break_even_queries"] is None or report["cost"]["break_even_queries"] > 0
    assert (output / "sve_family_report.json").is_file()
    assert (output / "sve_family_runs.csv").is_file()
    assert (output / "sve_family_comparison.png").is_file()
