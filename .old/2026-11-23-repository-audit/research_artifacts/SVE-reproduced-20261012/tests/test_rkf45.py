import math
from fractions import Fraction

import numpy as np
import pytest

from main import FEHLBERG_A, FEHLBERG_B4, FEHLBERG_B5, rkf45_step, solve_ivp_rkf45


def test_classic_six_stage_tableau_and_local_order():
    assert len(FEHLBERG_A) == len(FEHLBERG_B4) == len(FEHLBERG_B5) == 6
    assert FEHLBERG_A[5][0] == Fraction(-8, 27)
    assert FEHLBERG_B5[-1] == Fraction(2, 55)
    errors = []
    for h in (0.4, 0.2):
        _, y5, _ = rkf45_step(lambda t, y: y, 0.0, np.array([1.0]), h)
        errors.append(abs(y5[0] - math.exp(h)))
    assert errors[0] / errors[1] > 40


def test_exponential_endpoint_and_sampled_grid():
    grid = np.linspace(0, 2, 21)
    result = solve_ivp_rkf45(lambda t, y: y, (0, 2), [1], t_eval=grid)
    assert result.status == 'completed'
    assert np.array_equal(result.t, grid)
    assert np.max(abs(result.y[0] - np.exp(grid))) < 2e-8


def test_oscillator_rejects_steps_and_keeps_endpoint():
    result = solve_ivp_rkf45(
        lambda t, y: np.array([y[1], -y[0]]),
        (0, 2 * math.pi), [1, 0], first_step=2 * math.pi,
        rtol=1e-11, atol=1e-13,
    )
    assert result.status == 'completed'
    assert result.n_rejected > 0
    assert result.t[-1] == 2 * math.pi
    assert np.linalg.norm(result.y[:, -1] - [1, 0]) < 1e-9


def test_guard_and_rejection_limits_stop_with_explicit_status():
    stopped = solve_ivp_rkf45(lambda t, y: [1], (0, 1), [0],
                               guard=lambda t, y: t < 0.3, first_step=0.1)
    assert stopped.status == 'guard_stop'
    assert stopped.t[-1] < 1
    limited = solve_ivp_rkf45(lambda t, y: y, (0, 1), [1],
                              first_step=1, rtol=1e-14, atol=1e-16,
                              max_rejections=0)
    assert limited.status == 'rejection_limit'


def test_nonfinite_rhs_stops():
    result = solve_ivp_rkf45(lambda t, y: [float('nan')], (0, 1), [1])
    assert result.status == 'nonfinite_stage'
    assert result.nfev == 1


def test_partial_stage_failure_counts_actual_rhs_calls():
    calls = 0
    def rhs(t, y):
        nonlocal calls
        calls += 1
        return [float('nan') if calls == 3 else 1.0]
    result = solve_ivp_rkf45(rhs, (0, 1), [1])
    assert result.status == 'nonfinite_stage'
    assert result.nfev == calls == 3


def test_guard_before_stage_rhs_does_not_count_blocked_call():
    calls = 0
    def rhs(t, y):
        nonlocal calls
        calls += 1
        return [1.0]
    result = solve_ivp_rkf45(rhs, (0, 1), [0], first_step=0.1,
                             guard=lambda t, y: t < 0.01)
    assert result.status == 'guard_stop'
    assert result.nfev == calls == 1


def test_fixed_step_global_order_on_exponential():
    errors = []
    for h in (0.4, 0.2):
        result = solve_ivp_rkf45(lambda t, y: y, (0, 2), [1],
            rtol=1, atol=1, first_step=h, max_step=h)
        assert result.status == 'completed'
        errors.append(abs(result.y[0, -1]-math.exp(2)))
    assert errors[0] / errors[1] > 25
