"""Exact-arithmetic replay of the rotating exchange quotient on 0 <= t <= 1."""

import argparse
import json
from math import comb
from pathlib import Path

import sympy as sp


t = sp.Symbol("t")
DECAY = sp.Integer(3)
SOURCE = sp.Rational(9, 10)
EQUILIBRIUM = SOURCE / DECAY


def rational_input(text):
    """Parse a rational number without evaluating symbolic input."""
    try:
        return sp.Rational(text)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError("expected a fraction or finite decimal") from error


def picard(candidate, initial):
    antiderivative = sp.Poly(SOURCE - DECAY * candidate, t, domain=sp.QQ).integrate()
    return sp.expand(initial + antiderivative.as_expr() - antiderivative.eval(0))


def range_enclosure(polynomial, nodes):
    """Exact sampled maximum and continuous upper bound on [0, 1]."""
    p = sp.Poly(polynomial, t, domain=sp.QQ)
    node_max = max(abs(p.eval(node)) for node in nodes)
    derivative = p.diff()
    # A Bernstein polynomial lies between its extreme coefficients on [0, 1].
    degree = len(derivative.all_coeffs()) - 1
    lipschitz_bound = max(
        abs(sum(derivative.nth(k) * comb(i, k) / comb(degree, k)
                for k in range(i + 1)))
        for i in range(degree + 1)
    )
    return node_max, node_max + lipschitz_bound / (2 * (len(nodes) - 1))


def trial_profile(method, initial, degree, nodes):
    if method == "taylor":
        coefficients = [initial]
        for k in range(degree):
            source = SOURCE if k == 0 else 0
            coefficients.append((source - DECAY * coefficients[-1]) / (k + 1))
        return sum(c * t**k for k, c in enumerate(coefficients))
    if method != "fit":
        raise ValueError("method must be fit or taylor")

    # Fix the trace. The columns are defects of the homogeneous trial directions.
    lift_defect = initial - picard(initial, initial)
    directions = [t**k + DECAY * t**(k + 1) / (k + 1) for k in range(1, degree + 1)]
    matrix = sp.Matrix([[term.subs(t, node) for term in directions] for node in nodes])
    target = sp.Matrix([-lift_defect.subs(t, node) for node in nodes])
    gram = matrix.T * matrix
    coefficients = gram.inv(method="DM") * matrix.T * target
    return initial + sum(c * t**k for k, c in enumerate(coefficients, 1))


def cartesian_balances():
    """Build the original five balances before inserting any time profile."""
    x, y = sp.symbols("x y", real=True)
    b = sp.Function("b")(t)
    radius_squared = x*x + y*y
    omega = sp.Rational(1, 2)
    rotation = sp.Rational(1, 3)
    bed_shape = 1 / (10 * radius_squared)
    depth = 1 + (omega + rotation)**2 * radius_squared / 2 - bed_shape
    bed = bed_shape + b
    load = bed_shape / 2 + sp.Rational(9, 20) - b
    velocity = sp.Matrix([-omega*y, omega*x])
    position = sp.Matrix([x, y])

    def gradient(field):
        return sp.Matrix([field.diff(x), field.diff(y)])

    def divergence(flux):
        return flux[0].diff(x) + flux[1].diff(y)

    momentum = (velocity.diff(t) + velocity.jacobian(position) * velocity
                + gradient(depth + bed) + 2 * rotation * sp.Matrix([-velocity[1], velocity[0]])
                - rotation**2 * position)
    bed_flux = velocity.dot(velocity) * (velocity - gradient(bed))
    exchange = 2 * load - bed
    residuals = [
        depth.diff(t) + divergence(depth * velocity),
        *momentum,
        bed.diff(t) + divergence(bed_flux) - exchange,
        load.diff(t) + divergence(load * velocity) + exchange,
    ]
    return dict(zip(("water_mass", "momentum_x", "momentum_y", "bed", "mobile_load"),
                    map(sp.cancel, residuals)))


def exact_number(value):
    return {"exact": str(value), "decimal": float(value)}


def run(method, initial, degree, fit_nodes, check_cells, gamma):
    if not sp.Rational(2, 25) <= initial <= sp.Rational(1, 5):
        raise ValueError("initial must be in [0.08, 0.20] for this tank case")
    if degree < 1 or fit_nodes < degree + 2 or check_cells < 1:
        raise ValueError("require degree >= 1, fit_nodes >= degree + 2, check_cells >= 1")
    if gamma <= DECAY:
        raise ValueError("gamma must exceed 3")

    train = [sp.Rational(i, fit_nodes - 1) for i in range(fit_nodes)]
    check = [sp.Rational(i, check_cells) for i in range(check_cells + 1)]
    candidate = sp.expand(trial_profile(method, initial, degree, train))
    defect = sp.expand(candidate - picard(candidate, initial))
    sampled, upper = range_enclosure(defect, check)
    _, from_center = range_enclosure(candidate - EQUILIBRIUM, check)
    contraction = DECAY / gamma
    radius = abs(initial - EQUILIBRIUM) / (1 - contraction)
    if from_center > radius:
        raise ValueError("the continuous enclosure does not verify ball membership")

    # Decimal evaluation of the analytic solution is a check only.
    oracle_max = max(abs(sp.N(candidate.subs(t, node) - EQUILIBRIUM
                              - (initial - EQUILIBRIUM) * sp.exp(-DECAY * node), 25))
                     for node in check)
    upper_error = upper / (1 - contraction)
    # Gronwall gives exp(3) times the unweighted defect. Use exp(3) < 21.
    unweighted_error = 21 * upper
    positive_lift_certified = unweighted_error < min(initial + sp.Rational(2, 45),
                                                       sp.Rational(9, 20) - EQUILIBRIUM)
    b = sp.Function("b")(t)
    pde_residuals = {key: sp.expand(expr.subs(b, candidate).doit())
                     for key, expr in cartesian_balances().items()}
    return {
        "schema_version": 1,
        "sympy_version": sp.__version__,
        "input": {
            "model": "dimensionless rotating exchange swirl",
            "ode": "b'(t) + 3 b(t) = 9/10",
            "interval": ["0", "1"],
            "initial": str(initial),
            "method": method,
            "degree": degree,
            "fit_nodes": fit_nodes,
            "check_cells": check_cells,
            "gamma": str(gamma),
        },
        "trial_coefficients_ascending": [
            str(sp.Poly(candidate, t).nth(k)) for k in range(degree + 1)],
        "trace_exact": candidate.subs(t, 0) == initial,
        "certificate": {
            "norm": "sup_[0,1] exp(-gamma * t) * abs(error(t))",
            "contraction_upper": exact_number(contraction),
            "ball_radius": exact_number(radius),
            "candidate_ball_upper": exact_number(from_center),
            "sampled_defect_max_unweighted": exact_number(sampled),
            "continuous_defect_upper_unweighted": exact_number(upper),
            "continuous_error_upper_weighted": exact_number(upper_error),
            "continuous_error_upper_unweighted": exact_number(unweighted_error),
            "positive_lift_certified": bool(positive_lift_certified),
        },
        "diagnostic_sampled_oracle_error_unweighted": float(oracle_max),
        "cartesian_original_residuals_of_trial": {
            key: {
                "polynomial": str(expr),
                "continuous_abs_upper": exact_number(range_enclosure(expr, check)[1]),
            } for key, expr in pde_residuals.items()
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method", choices=("fit", "taylor"), default="fit")
    parser.add_argument("--initial", type=rational_input, default=sp.Rational(3, 20))
    parser.add_argument("--degree", type=int, default=10)
    parser.add_argument("--fit-nodes", type=int, default=17)
    parser.add_argument("--check-cells", type=int, default=128)
    parser.add_argument("--gamma", type=rational_input, default=sp.Integer(4))
    parser.add_argument("--output", type=Path, help="JSON file path; default: stdout")
    args = parser.parse_args()
    try:
        report = run(args.method, args.initial, args.degree, args.fit_nodes,
                     args.check_cells, args.gamma)
    except ValueError as error:
        parser.error(str(error))
    result = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(result, end="")
    else:
        args.output.write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()
