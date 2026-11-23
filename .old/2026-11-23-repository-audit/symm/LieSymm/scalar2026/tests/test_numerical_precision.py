"""Regressions for independent original-P checks above the float64 noise floor."""
import sympy as sp

from symm.LieSymm.scalar2026 import solve_reduction
from symm.LieSymm.scalar2026.continuation import continue_profile


def test_time_resonance_has_an_independent_precision_resolved_P_check(tmp_path):
    result = solve_reduction('cubic-resonant-time', parameters={'c': 1},
                             data={'z0': 1, 'jet': (2, 1, sp.Rational(1, 10))})
    numerical = continue_profile(result, tmp_path, interval=(1, 1.083))
    assert numerical['status'] == 'passed', numerical
    check = numerical['original_pde']
    assert check['acceptance_threshold'] == 1e-6
    assert check['precision_digits'] >= 40
    assert check['reference_agreement_passed']
    assert check['negative_control_passed']
    assert check['acceptance_max_abs_residual'] < 3e-8
    assert max(abs(row['residual']) for row in check['samples']
               if row['step'] == .001) < 5e-11
    assert 'original_pde_float64' in numerical
    assert not check['continuous_certificate']


def test_precision_resolved_check_rejects_a_perturbed_reconstruction(tmp_path):
    from symm.LieSymm.scalar2026.catalog import t
    result = solve_reduction('cubic-resonant-time', parameters={'c': 1},
                             data={'z0': 1, 'jet': (2, 1, sp.Rational(1, 10))})
    result['graph'] += t**3 / 1000
    numerical = continue_profile(result, tmp_path, interval=(1, 1.083))
    assert numerical['status'] == 'failed'
    assert not numerical['original_pde']['passed']
    assert numerical['original_pde']['acceptance_max_abs_residual'] > 1e-4


def test_high_precision_stencil_checks_original_P_and_not_an_ODE():
    from symm.LieSymm.scalar2026.precision import high_precision_pde_residual
    import mpmath as mp
    with mp.workdps(40):
        exact = high_precision_pde_residual(
            lambda T, S: S + T + T**2 / 20,
            '1.0415', 1, m=3, step='.001')
        perturbed = high_precision_pde_residual(
            lambda T, S: S + T + T**2 / 20 + T**3 / 1000,
            '1.0415', 1, m=3, step='.001')
    assert abs(exact['residual']) < 1e-25
    assert abs(perturbed['residual'] - .006) < 1e-14


def test_high_precision_reference_cannot_accept_disagreeing_integrators():
    from symm.LieSymm.scalar2026.precision import reference_pde_diagnostics
    import numpy as np
    result = solve_reduction('paper-3.8', parameters={},
                             data={'z0': 1, 'jet': (2, 1, sp.Rational(1, 10))})
    grid = np.linspace(1, 1.1, 21)
    wrong_states = np.zeros((3, len(grid)))
    check, _ = reference_pde_diagnostics(
        result, grid, wrong_states, wrong_states, (1, 1.1))
    assert not check['reference_agreement_passed']
    assert not check['passed']


def test_high_precision_stencil_rejects_nonfinite_or_invalid_chart():
    from symm.LieSymm.scalar2026.precision import high_precision_pde_residual
    import pytest
    import mpmath as mp
    for graph in (lambda T, S: mp.nan, lambda T, S: T - S):
        with pytest.raises(ValueError):
            high_precision_pde_residual(graph, 1, 1, m=3, step='.003')


def test_reference_budget_also_covers_cached_stencil_evaluation(monkeypatch):
    from symm.LieSymm.scalar2026 import precision
    import numpy as np
    import time
    result = solve_reduction('paper-3.8', parameters={},
                             data={'z0': 1, 'jet': (2, 1, sp.Rational(1, 10))})
    grid = np.linspace(1, 1.1, 21)
    offset = grid - 1
    states = np.vstack((2 + offset + offset**2 / 20,
                        1 + offset / 10, np.full_like(grid, .1)))
    original = precision.high_precision_pde_residual

    def slow_stencil(*args, **kwargs):
        time.sleep(.1)
        return original(*args, **kwargs)

    monkeypatch.setattr(precision, 'high_precision_pde_residual', slow_stencil)
    check, _ = precision.reference_pde_diagnostics(
        result, grid, states, states, (1, 1.1), budget_seconds=1)
    assert not check['passed'], check
    assert 'budget' in check['reason']
