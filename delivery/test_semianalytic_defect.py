"""Check the continuous-certificate and independent Cartesian replay contracts."""

import unittest

import sympy as sp

from semianalytic_defect import EQUILIBRIUM, cartesian_balances, run, t


class FixedPointReplay(unittest.TestCase):
    def test_both_methods_enclose_oracle_on_independent_nodes(self):
        initial = sp.Rational(3, 20)
        for method in ("fit", "taylor"):
            with self.subTest(method=method):
                report = run(method, initial, 10, 17, 128, sp.Integer(4))
                self.assertTrue(report["trace_exact"])
                cert = report["certificate"]
                self.assertTrue(cert["positive_lift_certified"])
                self.assertEqual(cert["contraction_upper"]["exact"], "3/4")

                coefficients = list(map(sp.Rational, report["trial_coefficients_ascending"]))
                profile = sp.Poly(sum(c * t**k for k, c in enumerate(coefficients)), t)
                bound = sp.Rational(cert["continuous_error_upper_weighted"]["exact"])
                for i in range(33):
                    point = sp.Rational(i, 32)
                    oracle = EQUILIBRIUM + (initial - EQUILIBRIUM)*sp.exp(-3*point)
                    weighted_error = sp.exp(-4*point)*abs(profile.eval(point)-oracle)
                    self.assertLess(weighted_error.evalf(35), bound)

    def test_cartesian_balances_with_unconstrained_time_profile(self):
        offset = sp.Function("b")(t)
        residual = offset.diff(t) + 3*offset - sp.Rational(9, 10)
        self.assertEqual(cartesian_balances(), {
            "water_mass": 0, "momentum_x": 0, "momentum_y": 0,
            "bed": residual, "mobile_load": -residual,
        })

    def test_invalid_contraction_configuration_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "gamma"):
            run("fit", sp.Rational(3, 20), 10, 17, 128, sp.Integer(3))


if __name__ == "__main__":
    unittest.main()
