"""Behavioral contracts for the near-cubic SVE obstruction certificate."""

from __future__ import annotations

import sympy as sp


def test_transport_expansion_keeps_the_exponent_and_coefficient_perturbations():
    """Dropping the m*kappa perturbation must change the certified E1 term."""
    from symm.generic.sve_near_cubic import transport_factor_expansion

    v = sp.Symbol("v", positive=True)
    expansion = transport_factor_expansion(v)

    assert sp.simplify(expansion.leading - 3 * v**2) == 0
    assert sp.simplify(expansion.first_order - v**2 * (1 + 3 * sp.log(v))) == 0


def test_certificate_declares_the_nondimensional_logarithm_and_unit_convention():
    """The P0 record must not present a logarithm of a dimensional velocity."""
    from symm.generic.sve_near_cubic import build_scaling_obstruction_certificate

    certificate = build_scaling_obstruction_certificate()

    convention = certificate["nondimensional_chart"]
    assert convention["velocity"] == (
        "v = d(phi_bar)/d(t_bar) = d(phi_phys)/d(t_phys)/U_star > 0"
    )
    assert certificate["model_contract"]["dimensionless_velocity"] == convention["velocity"]
    assert convention["logarithm_argument"] == "v"
    assert convention["family_status"] == "dimensionless-formal-parameter-family"
    assert certificate["equation_expansion"]["E1_canonical"] == (
        "-g*kappa*D_s(H*(1 + 3*log(v)))"
    )
    assert certificate["units_and_divisions"]["division_records"]


def test_scaling_certificate_reports_the_first_order_obstruction():
    """Replacing the -delta defect by zero must make this certificate fail."""
    from symm.generic.sve_near_cubic import build_scaling_obstruction_certificate

    certificate = build_scaling_obstruction_certificate()

    assert certificate["status"] == "verified"
    assert certificate["outcome"] == "obstruction-verified-scaling"
    assert certificate["checks"]["cubic_multiplier_identity"] is True
    assert certificate["checks"]["generic_x4_multiplier_identity"] is True
    assert certificate["checks"]["prolonged_residual_agrees"] is True
    assert certificate["scaling_constraints"]["inner"] == "3*c - b - 2*a"
    assert certificate["scaling_constraints"]["outer"] == "(m - 3)*(c - a)"
    assert certificate["first_order_defect"] == "-1"


def test_cubic_generator_has_the_reviewed_first_order_defect_identity():
    """A sign error in pr(X5)E1 + E1 must be observable at a regular jet."""
    from symm.generic.sve_near_cubic import cubic_generator_first_order_defect

    identity = cubic_generator_first_order_defect()

    assert sp.simplify(identity.lhs - identity.rhs) == 0
    assert identity.regular_sample_value == sp.Rational(186, 125)


def test_certificate_keeps_the_full_point_statement_source_conditioned():
    """A published generator list must not be promoted to an independent proof."""
    from symm.generic.sve_near_cubic import build_scaling_obstruction_certificate

    corollary = build_scaling_obstruction_certificate()["source_conditioned_corollary"]

    assert corollary["status"] == "qualified"
    assert corollary["requires_published_exhaustiveness"] is True
    assert corollary["independent_classification_claim"] is False


def test_certificate_reports_regularity_failed_without_a_positive_velocity_branch():
    """A missing log(v) branch guard must produce a replayable failure status."""
    from symm.generic.sve_near_cubic import (
        P0ModelContract,
        build_scaling_obstruction_certificate,
    )

    certificate = build_scaling_obstruction_certificate(
        P0ModelContract(positive_velocity=False)
    )

    assert certificate["status"] == "regularity-failed"
    assert certificate["outcome"] == "regularity-failed"
    assert any(
        "positive dimensionless velocity" in failure
        for failure in certificate["guard_failures"]
    )


def test_secondary_delta_check_has_linear_not_quadratic_defect_scaling():
    """A mistaken O(delta**2) label is caught by the independent numeric check."""
    from symm.generic.sve_near_cubic import two_sided_delta_check

    check = two_sided_delta_check()

    assert check["classification"] == "linear-defect-secondary-evidence"
    assert abs(check["absolute_ratio_h_over_half_h"] - 2.0) < 1e-10


def test_certificate_writer_preserves_scope_and_contract_in_json(tmp_path):
    """A downstream report must receive the qualified, branch-aware record."""
    from symm.generic.sve_near_cubic import write_scaling_obstruction_certificate

    path = tmp_path / "p0_certificate.json"
    written = write_scaling_obstruction_certificate(path)

    assert path.is_file()
    import json
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded == written
    assert loaded["model_contract"]["beta_rule"] == "beta_tr = m*kappa"
    assert loaded["scope"]["unrestricted_determining_system"] == "not-solved"
    assert "ML training is intentionally excluded from P0" in loaded["nonclaims"]
