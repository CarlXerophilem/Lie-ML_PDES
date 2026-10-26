"""Exact controls for the dissertation's mathematical interfaces."""


def certificates():
    from scripts.verify_dissertation_interfaces import build_certificates

    return build_certificates()


def test_reduced_graph_and_same_generator_penalty_are_identically_redundant():
    result = certificates()["invariant_graph"]
    assert result["arbitrary_profile_Q"] == "0"
    assert result["parameter_gradient"] == ["0", "0", "0", "0"]
    assert result["other_constraints_automatically_zero"] is False


def test_first_integral_identity_is_separate_from_elimination_pivot():
    result = certificates()["first_integral"]
    assert result["printed_identity"] == "0"
    assert result["corrected_identity"] == "0"
    assert result["bad_candidate_vector_derivative"] == "1"
    assert result["free_ode_c_squared_vector_derivative"] == "0"
    assert result["c_squared_pivot_at_zero"] == "0"
    assert result["constant_candidate_is_nonconstant"] is False


def test_scale_compatible_flux_is_a_restricted_exact_family():
    result = certificates()["constitutive_family"]
    assert result["homogeneity_remainder"] == "0"
    assert result["threshold_defect_nonzero"] is True
    assert result["arbitrary_closure_covered"] is False


def test_bed_evolution_has_positive_not_negative_diffusion():
    result = certificates()["diffusion"]
    assert result["expanded_evolution_remainder"] == "0"
    assert result["coefficient_positive_on_declared_chart"] is True
    assert result["whole_system_strict_parabolicity_proved"] is False


def test_characteristic_identity_uses_the_full_coupled_matrix():
    result = certificates()["characteristics"]
    assert result["polynomial_remainder"] == "0"
    assert result["corrected_coefficient_remainder"] == "0"
    assert result["zero_transport_remainder"] == "0"
    assert result["hydrodynamic_speed_is_generally_coupled_speed"] is False


def test_characteristic_smooth_flow_is_a_negative_shock_control():
    result = certificates()["smooth_characteristic_control"]
    assert result["eulerian_residuals"] == ["0", "0", "0"]
    assert result["ray_determinant"] == "0"
    assert result["laboratory_froude"] == "1/2"
    assert result["smooth"] is True


def test_printed_and_corrected_scalar_models_are_not_conflated():
    result = certificates()["model_counterexample"]
    assert result["printed_residual"] == "0"
    assert result["corrected_residual_remainder"] == "0"
    assert result["corrected_residual_is_nonzero"] is True
