"""Independent high-precision IVP reference and original-coordinate P stencils.

The reference surface, not a float64 interpolant, is differentiated. Agreement
with sampled DOP853/RKF45 states is a separate numerical check, not an error
bound on either interpolant or a continuous PDE certificate.
"""
from functools import lru_cache
import time

import mpmath as mp
import numpy as np
import sympy as sp

from .catalog import t, s, z, F, p, q, h


def _number(value):
    return mp.mpf(str(sp.N(value, mp.mp.dps)))


@lru_cache(maxsize=1)
def _rational_weights():
    return tuple(tuple(sp.finite_diff_weights(order, list(range(-4, 5)), 0)
                       [order][-1]) for order in range(4))


def high_precision_pde_residual(phi, T, S, *, m, step, g=1,
                                kappa=sp.Rational(1, 30), digits=40):
    """Differentiate only phi values; no ODE derivative rules enter this check."""
    if not isinstance(digits, int) or digits < 30:
        raise ValueError('PDE diagnostic requires at least 30 decimal digits')
    with mp.workdps(digits):
        T, S, step, m, g, kappa = map(_number, (T, S, step, m, g, kappa))
        if not all(mp.isfinite(v) for v in (T, S, step, m, g, kappa)):
            raise ValueError('finite parameters and coordinates required')
        if step <= 0 or m < 1 or g <= 0 or kappa <= 0:
            raise ValueError('positive step, g, kappa and m>=1 required')
        weights = [[mp.mpf(int(v.p)) / int(v.q) for v in row]
                   for row in _rational_weights()]
        values = [[phi(T + i * step, S + j * step) for j in range(-4, 5)]
                  for i in range(-4, 5)]
        if not all(mp.isfinite(v) for row in values for v in row):
            raise ValueError('nonfinite reconstructed surface')

        def derivative(i, j):
            return mp.fsum(weights[i][a] * weights[j][b] * values[a][b]
                           for a in range(9) for b in range(9)) / step**(i + j)

        velocity, gradient = derivative(1, 0), derivative(0, 1)
        if velocity <= 0 or gradient <= 0:
            raise ValueError('reconstructed surface left the positive chart')
        tt, ts, ss = derivative(2, 0), derivative(1, 1), derivative(0, 2)
        ttt, tss = derivative(3, 0), derivative(1, 2)
        inertial_t = ts * tt + gradient * ttt - g * (
            tss / gradient**2 - 2 * ss * ts / gradient**3)
        flux_s = m * kappa * (
            (m - 1) * velocity**(m - 2) * ts**2 / gradient
            + velocity**(m - 1) * tss / gradient
            - velocity**(m - 1) * ts * ss / gradient**2)
        return dict(residual=float(inertial_t - g * flux_s),
                    velocity=float(velocity), gradient=float(gradient),
                    step=float(step), precision_digits=digits)


def reference_pde_diagnostics(result, grid, dop_states, rkf_states, interval,
                              *, digits=40, budget_seconds=30):
    """Check an independent Taylor IVP surface and all sampled solver states.

    All three predeclared stencil sizes must pass the unchanged 1e-6 gate.
    Raw float64 stencil results are retained by the caller, not reclassified.
    """
    report = dict(model='P', passed=False, precision_digits=digits,
                  acceptance_threshold=1e-6, reference_agreement_passed=False,
                  negative_control_passed=False, continuous_certificate=False,
                  reference_tolerance='1e-30', reference_taylor_degree=20,
                  method='mpmath Taylor IVP; exact-weight 9x9 original-coordinate differences',
                  certificate_surface='independent high-precision IVP reconstruction',
                  scope='sampled reference-P residual and all-state grid agreement; '
                        'not a PDE certificate for float64 interpolants',
                  budget_seconds=budget_seconds)
    started = time.perf_counter()
    reference_states = np.empty((result['ode_order'], 0))

    def check_deadline():
        if time.perf_counter() - started > budget_seconds:
            raise TimeoutError('high-precision reference budget exhausted')

    try:
        with mp.workdps(digits):
            order = result['ode_order']
            highest = (F, p, q, h)[order]
            args = (z,) + (F, p, q)[:order]
            rhs = sp.lambdify(args, sp.cancel(
                -result['residual'].subs(highest, 0) / result['leading']), 'mpmath')
            leading, velocity, gradient = [sp.lambdify(args, result[key], 'mpmath')
                                          for key in ('leading', 'velocity', 'gradient')]
            start, end = map(_number, interval)
            initial = list(map(_number, result['data']['jet'][:order]))
            initial_sign = mp.sign(leading(start, *initial))
            check_deadline()

            def fun(x, y):
                check_deadline()
                guard_values = (leading(x, *y), velocity(x, *y), gradient(x, *y))
                if (not all(mp.isfinite(v) for v in (*y, *guard_values))
                        or initial_sign * guard_values[0] <= mp.mpf('1e-10')
                        or min(guard_values[1:]) <= mp.mpf('1e-9')):
                    raise ValueError('high-precision reference regular-chart guard reached')
                return [*y[1:], rhs(x, *y)]

            dense = mp.odefun(fun, start, initial, tol=mp.mpf('1e-30'), degree=20)
            states = []
            for x in grid:
                check_deadline()
                states.append(dense(_number(str(float(x)))))
            check_deadline()
            reference_states = np.array([[float(v) for v in row] for row in states]).T
            tolerance = float(1e-7 * (1 + np.max(np.abs(reference_states))))
            errors = {}
            for name, values in (('DOP853', dop_states), ('RKF45', rkf_states)):
                values = np.asarray(values)
                if values.shape != reference_states.shape or not np.isfinite(values).all():
                    raise ValueError('invalid solver-state grid for reference comparison')
                errors[name] = float(max(abs(mp.mpf(float(values[j, i])) - states[i][j])
                                         for i in range(len(grid)) for j in range(order)))
            report.update(reference_state_errors=errors, reference_state_tolerance=tolerance,
                          reference_grid_points=len(grid), integrated_state_components=order,
                          reference_agreement_passed=all(v <= tolerance for v in errors.values()))
            coordinate = sp.lambdify((t, s), result['coordinate'], 'mpmath')
            graph = sp.lambdify((t, s, F), result['graph'], 'mpmath')
            section = {key: sp.lambdify(z, value, 'mpmath')
                       for key, value in result['section'].items()}

            def phi(T, S):
                zz = coordinate(T, S)
                if zz < start or zz > end:
                    raise ValueError('high-precision PDE stencil outside solved interval')
                return graph(T, S, dense(zz)[0])

            params = {key: result['parameters'][key] for key in ('m', 'g', 'kappa')}
            samples, negatives = [], []
            for fraction in ('0.45', '0.5', '0.55'):
                zz = start + mp.mpf(fraction) * (end - start)
                T, S = section[t](zz), section[s](zz)
                for step in ('.003', '.002', '.001'):
                    check = high_precision_pde_residual(phi, T, S, **params,
                                                        step=step, digits=digits)
                    check_deadline()
                    changed = high_precision_pde_residual(
                        lambda T, S: phi(T, S) + T**3 / 1000, T, S, **params,
                        step=step, digits=digits)
                    check_deadline()
                    samples.append(dict(solver='mpmath-reference', z=float(zz), **check))
                    negatives.append(abs(changed['residual'] - check['residual']))
            maximum = max(abs(row['residual']) for row in samples)
            finite = all(np.isfinite(row['residual']) for row in samples)
            negative_passed = all(np.isfinite(v) and v > 1e-4 for v in negatives)
            check_deadline()
            report.update(samples=samples, acceptance_max_abs_residual=maximum,
                          acceptance_steps=[.003, .002, .001],
                          negative_control_differences=negatives,
                          negative_control_passed=negative_passed,
                          passed=bool(finite and maximum <= 1e-6 and negative_passed
                                      and report['reference_agreement_passed']))
    except (ValueError, TypeError, OverflowError, ZeroDivisionError, TimeoutError) as exc:
        report.update(passed=False, reason=str(exc), status='inconclusive_reference')
    report['elapsed_seconds'] = time.perf_counter() - started
    if report['elapsed_seconds'] > budget_seconds:
        report.update(passed=False, reason='high-precision reference budget exhausted',
                      status='inconclusive_reference')
    return report, reference_states
