import sympy as sp
from symm.generic import (
    BackendRequest,
    PointGenerator,
    ResourceLimits,
    bounded_completion,
    determining_equations,
    detect_backend,
    heat_2plus1,
    parameter_branches,
    request_backend,
    verify_off_shell_residuals,
)


def test_bounded_completion_preserves_parameter_guards_without_division():
    a = sp.Symbol("a")
    case = next(item for item in parameter_branches()
                if item.name == "parameter-a-nonzero")
    outcome = bounded_completion(case.system)
    assert outcome.certificate.status == "branch-partial"
    branch = outcome.certificate.branches[0]
    assert branch.inequations == (a,)
    assert branch.equations == case.system.equations
    assert all("divide" not in value for key, value in branch.provenance)


def test_completion_resource_cap_is_explicitly_unsupported():
    system = heat_2plus1().system
    limits = ResourceLimits(max_expression_nodes=1)
    outcome = bounded_completion(system, limits=limits)
    assert outcome.certificate.status == "unsupported"
    assert not dict(outcome.certificate.checks)["resource_budget"]


def test_backend_request_has_structured_unavailable_boundary():
    request = BackendRequest(heat_2plus1().system, "completion", "maple")
    response = request_backend(request)
    expected = "unsupported" if detect_backend("maple").available else "backend-unavailable"
    assert response.status == expected
    assert response.request_fingerprint == request.fingerprint()
    assert response.as_dict()["schema_version"]


def test_raw_determining_equations_are_partial_and_exact_check_is_separate():
    case = heat_2plus1()
    x_translation = PointGenerator((1, 0, 0), (0,))
    partial = determining_equations(case.system, x_translation)
    assert partial.status == "branch-partial"
    assert not dict(partial.checks)["branch_normal_form"]
    exact = verify_off_shell_residuals(case.system, x_translation)
    assert exact.status == "verified"
    assert exact.all_checks_pass
