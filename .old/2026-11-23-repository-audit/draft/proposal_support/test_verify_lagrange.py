import unittest

import numpy as np

from verify_lagrange import coefficients, numerical_pilot, reference, rhs, symbolic_checks, taylor_coefficients


class LagrangeChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.symbolic = symbolic_checks()
        cls.pilot = numerical_pilot()

    def test_arbitrary_profile_pullback(self):
        self.assertTrue(self.symbolic["checks"]["cubic_reduction_pullback_zero"])

    def test_exact_cubic_control(self):
        self.assertTrue(self.symbolic["checks"]["cubic_exact_profile_zero"])

    def test_printed_traveling_wave(self):
        for key in ("traveling_wave_master_zero", "traveling_wave_printed_momentum_zero", "traveling_wave_printed_bed_zero"):
            self.assertTrue(self.symbolic["checks"][key], key)

    def test_physical_equivalence_counterexample(self):
        self.assertTrue(self.symbolic["checks"]["eulerian_mass_momentum_zero"])
        self.assertTrue(self.symbolic["checks"]["eulerian_exner_counterexample_confirmed"])

    def test_static_profile_source_check(self):
        self.assertTrue(self.symbolic["checks"]["arbitrary_static_profile_master_zero"])

    def test_numerical_gates(self):
        self.assertTrue(all(self.pilot["checks"].values()), self.pilot["checks"])

    def test_analytic_initial_derivatives(self):
        y = reference(1.0)
        np.testing.assert_allclose(rhs(1.0, y), [y[1], y[2], 10 * np.cbrt(45) / 27], atol=1e-13)
        c = taylor_coefficients(y)
        np.testing.assert_allclose(c, np.cbrt(45) * np.array([1, 1/3, -1/9, 5/81, -10/243]), atol=1e-13)

    def test_regular_domain_rejects_nonpositive_r(self):
        for r in (0.0, -1.0):
            with self.assertRaises(ValueError):
                rhs(1.0, [1.0, r, 0.0])

    def test_leading_coefficient_rank_drop(self):
        r = np.cbrt(1 / 3.6)
        a, _ = coefficients(1.0, r, 0.0)
        self.assertLess(abs(a), 1e-13)
        with self.assertRaises(ValueError):
            rhs(1.0, [1.0, r, 0.0])

    def test_evidence_boundaries(self):
        self.assertFalse(self.pilot["interval_certified"])
        self.assertFalse(self.pilot["pinn_trained"])


if __name__ == "__main__":
    unittest.main()
