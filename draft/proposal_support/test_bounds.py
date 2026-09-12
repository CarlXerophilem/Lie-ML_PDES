from fractions import Fraction as Q
import unittest

from verify_bounds import Interval, verify


class BoundsTests(unittest.TestCase):
    def test_sign_crossing_even_power(self):
        interval = Interval(-2, 3)**2
        self.assertEqual((interval.lower, interval.upper), (0, 9))

    def test_negative_quotient(self):
        interval = Interval(2, 3) / Interval(-2, -1)
        self.assertEqual((interval.lower, interval.upper), (-3, -1))

    def test_zero_division_rejected(self):
        with self.assertRaises(ZeroDivisionError):
            Interval(1) / Interval(-1, 1)

    def test_exact_partition_result(self):
        report = verify()
        self.assertTrue(all(report['checks'].values()))
        self.assertEqual(Q(report['joint_derivative_bound_exact']), Q(7150105171934045737, 506087956699582464))
        self.assertEqual(report['covered_subboxes'], 1728)
        self.assertFalse(report['neural_uniform_residual_validated'])


if __name__ == '__main__':
    unittest.main()
