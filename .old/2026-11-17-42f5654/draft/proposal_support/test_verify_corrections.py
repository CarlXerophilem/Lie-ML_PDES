"""Focused regressions for the proposal's standalone verification program."""

import unittest

import numpy as np

import verify_corrections as vc


class CorrectionChecks(unittest.TestCase):
    def test_symbolic_balances_and_scaling(self):
        self.assertTrue(all(vc.symbolic_checks().values()))

    def test_cubic_control_ode(self):
        for t in (1.0, 1.2, 1.5):
            H, v, C = vc.baseline(t)
            rhs = [-3 * H * v, -v**2 - 2 * vc.G * (H + C), -3 * vc.KAPPA * v**3]
            np.testing.assert_allclose(vc.baseline_derivative(t), rhs, atol=1e-15)

    def test_zero_correction_initial_forcing(self):
        _, _, b, c = vc.correction_matrices(vc.T0)
        np.testing.assert_allclose(vc.correction_rhs(vc.T0, np.zeros(6)), np.r_[b, c])

    def test_exponential_reference_satisfies_correction_ode(self):
        times = np.array([1.0, 1.2, 1.5])
        curve = vc.exponential_reference(times)
        derivative = vc.differentiate_curve(vc.exponential_reference, times, 1e-4)
        rhs = np.stack([vc.correction_rhs(t, w) for t, w in zip(times, curve.T)], axis=1)
        np.testing.assert_allclose(derivative, rhs, atol=1e-10, rtol=0)
        np.testing.assert_array_equal(curve[:, 0], np.zeros(6))

    def test_independent_derivatives_include_endpoints(self):
        def polynomial(t):
            return np.vstack([t**j for j in range(6)])

        times = np.array([1.0, 1.2, 1.5])
        got = vc.differentiate_curve(polynomial, times, 1e-3)
        expected = np.vstack([np.zeros_like(times)] + [j * times**(j - 1) for j in range(1, 6)])
        np.testing.assert_allclose(got, expected, atol=1e-8, rtol=0)

    def test_derivative_stays_inside_interval(self):
        def guarded(t):
            self.assertGreaterEqual(float(min(t)), vc.T0)
            self.assertLessEqual(float(max(t)), vc.T1)
            return np.vstack([t])

        got = vc.differentiate_curve(guarded, [vc.T0, vc.T1], 1e-4)
        np.testing.assert_allclose(got, 1.0, atol=1e-10)

    def test_bad_derivative_step_rejected(self):
        with self.assertRaises(ValueError):
            vc.differentiate_curve(lambda t: t, [1.0], 0)

    def test_large_one_sided_stencil_rejected_before_evaluation(self):
        def must_not_evaluate(t):
            self.fail("An out-of-interval stencil was evaluated")

        with self.assertRaises(ValueError):
            vc.differentiate_curve(must_not_evaluate, [1.19], 0.1)

    def test_log_domain_rejected(self):
        with self.assertRaises(ValueError):
            vc.reconstruct([1.0], [0.0], 0.01, np.zeros((6, 1)), np.zeros((6, 1)))

    def test_reconstruction_time_derivative_detects_wrong_curve(self):
        times, xs = np.array([1.1, 1.4]), np.array([1.0, 2.0])
        def curve(t):
            return np.array([(t - 1)**2, 0 * t, 0 * t, 0 * t, 0 * t, 0 * t])

        step, delta = 1e-5, 0.02
        derivative = vc.differentiate_curve(curve, times, step)
        _, dt, _ = vc.reconstruct(times, xs, delta, curve(times), derivative)
        plus = vc.reconstruct(times + step, xs, delta, curve(times + step), derivative)[0]
        minus = vc.reconstruct(times - step, xs, delta, curve(times - step), derivative)[0]
        np.testing.assert_allclose(dt, (plus - minus) / (2 * step), atol=1e-8, rtol=0)

    def test_reconstruction_space_derivative(self):
        times, xs = np.array([1.0, 1.5]), np.array([1.1, 1.8])
        curve = np.arange(12).reshape(6, 2) * 1e-3
        derivative = np.zeros_like(curve)
        step = 1e-5
        _, _, dx = vc.reconstruct(times, xs, 0.02, curve, derivative)
        plus = vc.reconstruct(times, xs + step, 0.02, curve, derivative)[0]
        minus = vc.reconstruct(times, xs - step, 0.02, curve, derivative)[0]
        np.testing.assert_allclose(dx, (plus - minus) / (2 * step), atol=1e-9, rtol=0)

    def test_two_sided_numeric_orders_and_negative_control(self):
        result = vc.numerical_checks()
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(len(result["records"]), 10)


if __name__ == "__main__":
    unittest.main()
