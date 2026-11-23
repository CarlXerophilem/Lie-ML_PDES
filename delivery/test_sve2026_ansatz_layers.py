"""Regression tests of the frozen scalar determination stages."""
import unittest
from unittest.mock import DEFAULT, patch

import reproduce_sve2026 as source
from symbolic_sve2026 import (
    classify, compatible, material_slice, material_scaling, _rank_strata,
    sp, t, s, u, p, q, a, b, c, r, w, x, y, m, JETS,
)


def characteristic_action(equation, tau, xi, eta):
    """Independent characteristic prolongation, with fourth jets cancelled."""
    jets = {**JETS, **{(4-j, j): sp.Dummy(real=True) for j in range(5)}}

    def derivative(expression, axis):
        result = expression.diff((t, s)[axis])
        for i, j in JETS:
            result += expression.diff(jets[i, j])*jets[i+(axis == 0), j+(axis == 1)]
        return sp.expand(result)

    characteristic = eta-p*tau-q*xi
    result = tau*equation.diff(t)+xi*equation.diff(s)
    for (i, j), jet in JETS.items():
        prolonged = characteristic
        for axis in [0]*i+[1]*j:
            prolonged = derivative(prolonged, axis)
        coefficient = sp.expand(prolonged+tau*jets[i+1, j]+xi*jets[i, j+1])
        if any(coefficient.has(jets[4-k, k]) for k in range(5)):
            raise ArithmeticError("fourth-order jet did not cancel")
        result += coefficient*equation.diff(jet)
    return sp.expand(result)


def restrict(equation, variation):
    solved, = sp.solve(equation, r)
    return variation.subs(r, solved)


class TestFrozenScalarLayers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The paper's listed generators and printed coefficient receipts may
        # be used for separate historical checks, never for classification.
        with patch.multiple(source, generators=DEFAULT,
                            _determining_split=DEFAULT) as mocks:
            for factory in mocks.values():
                factory.side_effect = AssertionError("read historical fixtures")
            cls.printed = classify("P")
            cls.material = classify("M")

    def test_discovered_strata_and_dimensions(self):
        self.assertEqual(self.printed["exceptional_exponents"], (1, 3))
        self.assertEqual(self.material["exceptional_exponents"], (3,))
        self.assertEqual({k: len(v) for k, v in self.printed["bases"].items()},
                         {"m": 4, "1": 5, "3": 5})
        self.assertEqual({k: len(v) for k, v in self.material["bases"].items()},
                         {"m": 4, "3": 5})

    def test_rank_drop_discovery_uses_matrix_input(self):
        self.assertEqual(_rank_strata(sp.diag(m-5, m-8)), sp.FiniteSet(5, 8))
        self.assertEqual(_rank_strata(sp.Matrix([[m-5, m-8]])), sp.S.EmptySet)

    def test_material_slice_matches_independent_prolongation(self):
        field = tuple(sp.Function(name)(t, s, u) for name in ("tau", "xi", "eta"))
        equation = compatible()
        independent = restrict(equation, characteristic_action(equation, *field))
        zero_second = {a: 0, b: 0, c: 0}
        candidate = material_slice(equation, field)
        for jet in (w, x, y):
            defect = candidate.diff(jet)-independent.diff(jet).subs(zero_second)
            self.assertEqual(sp.simplify(defect), 0)

    def test_derived_bases_on_unsliced_equation(self):
        for derivation, model in ((self.printed, source.master),
                                  (self.material, compatible)):
            for case, basis in derivation["bases"].items():
                equation = model(m if case == "m" else sp.Integer(case))
                for generator in basis:
                    defect = restrict(equation, characteristic_action(equation, *generator))
                    self.assertEqual(sp.simplify(defect), 0)

    def test_negative_controls_on_full_equation(self):
        for equation in (compatible(2), source.master(2)):
            cubic_scaling = (t, -2*s, sp.S.Zero)
            variation = characteristic_action(equation, *cubic_scaling)
            self.assertNotEqual(sp.simplify(restrict(equation, variation)), 0)
        boost = (sp.S.Zero, sp.S.Zero, t)
        for equation, admitted in ((source.master(1), True), (compatible(1), False)):
            defect = sp.simplify(restrict(equation, characteristic_action(equation, *boost)))
            self.assertEqual(defect == 0, admitted)

    def test_frozen_dependency_gate_rejects_empty_slice(self):
        with patch("symbolic_sve2026.material_slice", return_value=sp.S.Zero):
            with self.assertRaisesRegex(ArithmeticError, "projected dependencies"):
                classify("M")

    def test_reduction_requires_invariant_graph(self):
        with self.assertRaisesRegex(ArithmeticError, "invariant-surface"):
            material_scaling((sp.S.Zero, sp.S.Zero, sp.S.One))
        material_scaling(self.material["bases"]["m"][-1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
