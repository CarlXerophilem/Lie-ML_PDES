"""Symbolic checks for Appendix C; no two-dimensional PDE solver is claimed."""

import unittest

import sympy as sp


t, a, b, x, y = sp.symbols("t a b x y", real=True)
g, xi, ag = sp.symbols("g xi A_g", positive=True)
LABELS = (a, b)
SPACE = (x, y)


def grad(value, coordinates=LABELS):
    return sp.Matrix([sp.diff(value, c) for c in coordinates])


def div(vector, coordinates=LABELS):
    return sum(sp.diff(value, c) for value, c in zip(vector, coordinates))


class SVE2DChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Both off-diagonal derivatives and J vary in space on this regular map.
        cls.position = sp.Matrix([(1 + t) * a + b**2 / 5, (1 + 2*t) * b + a**2 / 7])
        cls.M = cls.position.jacobian(LABELS)
        cls.J = sp.factor(cls.M.det())
        cls.inverse = cls.M.inv()
        cls.velocity = cls.position.diff(t)
        cls.w = cls.inverse * cls.velocity
        cls.coflux = (cls.J * cls.inverse).applyfunc(sp.cancel)

    def pull(self, value):
        return value.subs(dict(zip(SPACE, self.position)), simultaneous=True)

    def assertZero(self, value):
        entries = list(value) if isinstance(value, sp.MatrixBase) else [value]
        for entry in entries:
            self.assertEqual(sp.cancel(entry), 0)

    def test_gradient_and_fixed_point_time_chain_rules(self):
        scalar = t*x**2 + x*y + y**3
        pulled = self.pull(scalar)
        self.assertZero(self.inverse.T * grad(pulled) - self.pull(grad(scalar, SPACE)))
        self.assertZero(sp.diff(pulled, t) - self.w.dot(grad(pulled)) - self.pull(sp.diff(scalar, t)))

    def test_piola_divergence_on_nonaffine_map(self):
        flux = sp.Matrix([x**2 + t*y, x*y + t**2])
        self.assertZero(div(self.coflux * self.pull(flux)) - self.J * self.pull(div(flux, SPACE)))
        for column in range(2):
            self.assertZero(div(self.coflux[:, column]))

    def test_jacobian_and_water_mass_identity(self):
        self.assertZero(sp.diff(self.J, t) - div(self.coflux * self.velocity))
        H = 2 + a**2 + b**2 + t*a
        euler_mass_pullback = sp.diff(H, t) - self.w.dot(grad(H)) + div(self.coflux * (H*self.velocity)) / self.J
        self.assertZero(self.J * euler_mass_pullback - sp.diff(self.J * H, t))
        mu = 2 + a**2 + b**2
        self.assertZero(sp.diff(self.J * (mu/self.J), t))

    def test_relative_bed_flux_identity(self):
        bed = t*a + a**2 + a*b + b**3
        flux = sp.Matrix([a**2 + t*b, a*b + t**2])
        nonconservative = sp.diff(bed, t) - self.w.dot(grad(bed)) + xi*div(self.coflux * flux)/self.J
        conservative = sp.diff(self.J * bed, t) + div(self.coflux * (xi*flux - bed*self.velocity))
        self.assertZero(conservative - self.J * nonconservative)

    def test_conservative_primitive_momentum_identity(self):
        h, u, v, bed = [sp.Function(name)(t, x, y) for name in ("h", "u", "v", "B")]
        velocity = sp.Matrix([u, v])
        mass = sp.diff(h, t) + div(h*velocity, SPACE)
        for i, coordinate in enumerate(SPACE):
            conservative = sp.diff(h*velocity[i], t) + div(h*velocity[i]*velocity, SPACE) + g*h*sp.diff(h + bed, coordinate)
            primitive = sp.diff(velocity[i], t) + velocity.dot(grad(velocity[i], SPACE)) + g*sp.diff(h + bed, coordinate)
            self.assertZero(conservative - h*primitive - velocity[i]*mass)

    def test_exact_sloping_bed_example_and_missing_transport(self):
        hc = sp.symbols("h_c", positive=True)
        velocity = sp.Matrix([2 - t, 1 - 2*t])
        bed = x + 2*y
        flux = ag * velocity.dot(velocity) * velocity
        self.assertZero(sp.diff(hc, t) + div(hc*velocity, SPACE))
        self.assertZero(velocity.diff(t) + grad(hc + bed, SPACE))
        self.assertZero(sp.diff(bed, t) + xi*div(flux, SPACE))
        position = sp.Matrix([a + 2*t - t**2/2, b + t - t**2])
        M = position.jacobian(LABELS)
        self.assertEqual(M.det(), 1)
        self.assertZero(position.diff(t) - velocity)
        pulled_bed = bed.subs(dict(zip(SPACE, position)), simultaneous=True)
        self.assertZero(position.diff(t, 2) + M.inv().T * grad(hc + pulled_bed))
        self.assertZero(sp.diff(pulled_bed, t) - velocity.dot(grad(pulled_bed)) + xi*div(flux))
        wrong_residual = sp.diff(pulled_bed, t) + xi*div(flux)
        self.assertEqual(sp.expand(wrong_residual), 4 - 5*t)

    def test_cubic_one_dimensional_limit(self):
        phi, bed = sp.Function("phi")(t, a), sp.Function("Btilde")(t, a)
        position = sp.Matrix([phi, b])
        M = position.jacobian(LABELS)
        J = M.det()
        velocity = position.diff(t)
        w = M.inv() * velocity
        flux = ag * velocity.dot(velocity) * velocity
        momentum = position.diff(t, 2) + g*M.inv().T * grad(1/J + bed)
        A = sp.diff(phi, a)*sp.diff(phi, t, 2) - g*sp.diff(phi, a, 2)/sp.diff(phi, a)**2
        self.assertZero(J * momentum[0] - A - g*sp.diff(bed, a))
        self.assertZero(momentum[1])
        exner = sp.diff(bed, t) - w.dot(grad(bed)) + xi/J*div(J*M.inv()*flux)
        expected = sp.diff(bed, t) - sp.diff(phi, t)/sp.diff(phi, a)*sp.diff(bed, a) + 3*xi*ag*sp.diff(phi, t)**2*sp.diff(phi, t, a)/sp.diff(phi, a)
        self.assertZero(exner - expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
