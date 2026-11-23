"""Exact rational interval verification of a local Lipschitz bound; no NN certificate."""

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path

import sympy as sp

from verify_lagrange import coefficients


class Interval:
    def __init__(self, lower, upper=None):
        self.lower = Q(lower)
        self.upper = Q(lower if upper is None else upper)
        if self.lower > self.upper:
            raise ValueError("Reversed interval")

    @staticmethod
    def convert(value):
        return value if isinstance(value, Interval) else Interval(value)

    def __add__(self, other):
        other = self.convert(other)
        return Interval(self.lower + other.lower, self.upper + other.upper)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.upper, -self.lower)

    def __sub__(self, other):
        return self + -self.convert(other)

    def __rsub__(self, other):
        return self.convert(other) + -self

    def __mul__(self, other):
        other = self.convert(other)
        endpoints = [a * b for a in (self.lower, self.upper) for b in (other.lower, other.upper)]
        return Interval(min(endpoints), max(endpoints))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.convert(other)
        if other.lower <= 0 <= other.upper:
            raise ZeroDivisionError("Interval denominator contains zero")
        return self * Interval(1 / other.upper, 1 / other.lower)

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError("Only nonnegative integer powers are supported")
        if power == 0:
            return Interval(1)
        if power % 2:
            return Interval(self.lower**power, self.upper**power)
        endpoints = [self.lower**power, self.upper**power]
        return Interval(0 if self.lower <= 0 <= self.upper else min(endpoints), max(endpoints))

    def absmax(self):
        return max(abs(self.lower), abs(self.upper))


def partials(x, r, v):
    D = 18 * r**3 * x**2 - 5
    fr = 2 * (-54 * r**8 * x**2 + 162 * r**6 * v**2 * x**4 + 60 * r**5 + 375 * r**4 * v * x + 450 * r**3 * v**2 * x**2 - 25 * v**2) / (r**2 * D**2)
    fv = -2 * (25 * r**4 * x + 18 * r**3 * v * x**2 + 10 * v) / (r * D)
    return fr, fv


def verify():
    x, r, v = sp.symbols("x r v")
    a, b = coefficients(x, r, v, sp.Integer(1), sp.Rational(1, 10))
    fr, fv = partials(x, r, v)
    symbolic = sp.cancel(sp.diff(-b/a, r) - fr) == 0 and sp.cancel(sp.diff(-b/a, v) - fv) == 0
    a_lower = coefficients(Q(1), Q(17, 20), Q(0), Q(1), Q(1, 10))[0]
    a_upper = coefficients(Q(3, 2), Q(5, 4), Q(0), Q(1), Q(1, 10))[0]
    a_sigma_lower = 24 * Q(9, 10) * Q(17, 20) - 2 / Q(17, 20)**2
    best = Q(0)
    min_denominator = Q(18) * Q(17, 20)**3 - 5
    for i, j, k in product(range(12), repeat=3):
        xi = Interval(1 + Q(i, 24), 1 + Q(i + 1, 24))
        ri = Interval(Q(17, 20) + Q(j, 30), Q(17, 20) + Q(j + 1, 30))
        vi = Interval(-Q(17, 20) + Q(k, 24), -Q(17, 20) + Q(k + 1, 24))
        fri, fvi = partials(xi, ri, vi)
        best = max(best, fri.absmax() + fvi.absmax())
    report = {
        "schema": "lieml.exact-box-bound.v1",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "coefficient_source_sha256": hashlib.sha256(Path(__file__).with_name("verify_lagrange.py").read_bytes()).hexdigest(),
        "arithmetic": "fractions.Fraction; exact endpoint operations",
        "box": {"sigma": ["1", "3/2"], "r": ["17/20", "5/4"], "v": ["-17/20", "-7/20"]},
        "subdivisions_per_axis": 12, "covered_subboxes": 12**3,
        "denominator_D_lower": str(min_denominator),
        "a_lower": str(a_lower), "a_upper": str(a_upper),
        "a_sigma_lower": str(a_sigma_lower),
        "joint_derivative_bound_exact": str(best),
        "joint_derivative_bound_decimal": float(best),
        "lipschitz_constant": 15,
        "checks": {"derivatives_match_reduced_rhs": symbolic, "denominators_positive": min_denominator > 0, "a_bounds_positive_and_ordered": 0 < a_lower < a_upper and a_sigma_lower > 0, "joint_bound_below_15": best < 15},
        "neural_uniform_residual_validated": False,
        "perturbed_trajectory_containment_certified": False,
    }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    report = verify()
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "bounds.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not all(report["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
