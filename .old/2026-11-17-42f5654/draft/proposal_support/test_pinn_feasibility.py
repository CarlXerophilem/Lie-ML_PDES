import unittest

import numpy as np
import torch

from pinn_feasibility import Profile, original_master_check, profile_jets, residuals
from verify_lagrange import reference, taylor_coefficients


class FeasibilityTests(unittest.TestCase):
    def test_initial_jets_are_hard_constraints(self):
        initial = reference(1.0)
        for order in (2, 4):
            model = Profile(order, initial)
            with torch.no_grad():
                model.net[-1].weight.fill_(0.1)
            sigma = torch.ones((1, 1), dtype=torch.float64, requires_grad=True)
            jets = profile_jets(model, sigma)
            np.testing.assert_allclose([v.detach().item() for v in jets[:3]], initial, atol=1e-14)

    def test_zero_remainder_is_taylor(self):
        initial = reference(1.0)
        sigma = torch.tensor([[1.2]], dtype=torch.float64)
        for order in (2, 4):
            value = Profile(order, initial)(sigma).detach().item()
            expected = np.polynomial.polynomial.polyval(0.2, taylor_coefficients(initial)[:order+1])
            self.assertAlmostEqual(value, expected, places=13)

    def test_direct_neural_master_matches_lift(self):
        model = Profile(4, reference(1.0))
        with torch.no_grad():
            model.net[-1].weight.fill_(0.03)
        result = original_master_check(model)
        self.assertLess(result['direct_vs_lift_max_abs'], 1e-10)

    def test_gradients_are_finite(self):
        model = Profile(2, reference(1.0))
        sigma = torch.linspace(1, 1.5, 16, dtype=torch.float64).reshape(-1, 1).requires_grad_()
        loss = residuals(model, sigma)[3].square().mean()
        loss.backward()
        self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all().item() for p in model.parameters()))


if __name__ == '__main__':
    unittest.main()
