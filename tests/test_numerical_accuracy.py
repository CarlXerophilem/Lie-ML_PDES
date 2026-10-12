import numpy as np
import pytest
import torch

from symm.solvers.problems import ProfileProblem
from symm.solvers.classical_integrators import solve_reference
from symm.solvers.chebyshev_control import solve_chebyshev
from symm.solvers.hybrid_profile import HardProfile
from symm.solvers.loss_measures import differential_linearization, profile_jets, quotient_loss, directional_loss
from symm.selection.complexity_selector import cost_crossing, choose_minimum_cost


@pytest.mark.parametrize("chart", ("cubic_X5", "common_printed", "common_corrected"))
def test_classical_accuracy_and_spectral_convergence(chart):
    problem = ProfileProblem(chart, eta=.1)
    grid = np.linspace(1, 1.5, 1001)
    dop = solve_reference(problem)
    rad = solve_reference(problem, "Radau")
    assert np.max(np.abs(dop.state_jets(grid)[:3]-rad.state_jets(grid)[:3])) < 1e-9
    errors = []
    for degree in (8, 12, 16):
        solution = solve_chebyshev(problem, degree)
        errors.append(np.max(np.abs(solution.profile(grid)-dop.profile(grid))))
        assert np.max(np.abs(solution.jets(np.array([1.]))[:3, 0]-problem.initial)) < 1e-12
    assert errors[-1] < 1e-9
    assert errors[-1] <= errors[0]+1e-13
    if chart != "cubic_X5":
        integral = solve_reference(problem, integrated=True)
        assert np.max(np.abs(integral.state_jets(grid)[:3]-dop.state_jets(grid)[:3])) < 1e-9


def test_exact_cubic_and_effective_tolerance():
    problem = ProfileProblem("cubic_X5")
    grid = np.linspace(1, 1.5, 1001)
    solution = solve_reference(problem, rtol=1e-14)
    amplitude = 45**(1/3)
    assert np.max(np.abs(solution.profile(grid)-(2-amplitude+amplitude*grid**(1/3)))) < 1e-12
    assert solution.effective_rtol >= 100*np.finfo(float).eps
    assert solution.warnings
    assert np.max(np.abs(solution.dense_jets(grid)[0]-solution.profile(grid))) < 1e-14


@pytest.mark.parametrize("kind", ("PINN", "PIKAN"))
def test_conditioned_hard_traces_after_parameter_changes(kind):
    problem = ProfileProblem("common_printed")
    model = HardProfile(problem, kind, conditioned=True)
    with torch.no_grad():
        for parameter in model.parameters():
            parameter.add_(.001)
    for eta in (-.1, .05, .1):
        values = model.jets(np.array([1.]), exponent=2.95, eta=eta)
        assert np.max(np.abs(values[:3, 0]-(2., .5, .1*(1+eta)))) < 1e-13


def test_frechet_linearization_and_weight_derivative():
    problem = ProfileProblem("common_corrected")
    z = torch.linspace(1, 1.5, 21, dtype=torch.float64, requires_grad=True)
    profile = 2+.5*(z-1)+.05*(z-1)**2+.01*(z-1)**3
    tangent = .03*(z-1)**3+.01*(z-1)**4
    jets, directions = profile_jets(profile, z), profile_jets(tangent, z)
    q = torch.full_like(z, .5/21)
    metric = 1+jets[0].square()
    derivative = directional_loss(problem, z, jets, directions, q,
                                  metric=metric, metric_direction=2*jets[0]*directions[0])
    epsilon = 1e-5
    plus = tuple(f+epsilon*d for f, d in zip(jets, directions))
    minus = tuple(f-epsilon*d for f, d in zip(jets, directions))
    measure = lambda values: 1+values[0].square()
    numerical = (quotient_loss(problem,z,plus,q,metric=measure)-quotient_loss(problem,z,minus,q,metric=measure))/(2*epsilon)
    assert torch.allclose(derivative, numerical, rtol=1e-8, atol=1e-10)


def test_break_even_arithmetic_and_inadmissibility():
    record = cost_crossing(12., 2., .1, .5)
    count = record["N_break"]
    assert 12+count*.1 <= 2+count*.5
    assert 12+(count-1)*.1 > 2+(count-1)*.5
    assert cost_crossing(12, 2, .5, .1)["N_break"] is None
    assert cost_crossing(1, 2, .5, .1)["last_advantage_query"] == 2
    assert cost_crossing(1,2,.1,.5,admissible=False)["status"] == "accuracy-inadmissible"


def test_cost_selection_rejects_fast_inaccurate_candidates():
    candidates = [dict(id="fast-but-inaccurate", admissible=False, setup_seconds=0., query_seconds=0.),
                  dict(id="cheap-setup", admissible=True, setup_seconds=1., query_seconds=1.),
                  dict(id="cheap-query", admissible=True, setup_seconds=10., query_seconds=.01)]
    assert choose_minimum_cost(candidates,1)["selected"]["id"] == "cheap-setup"
    assert choose_minimum_cost(candidates,1000)["selected"]["id"] == "cheap-query"
    assert choose_minimum_cost(candidates[:1],1000)["selected"] is None
