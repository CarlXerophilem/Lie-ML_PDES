"""Exact checks for the parameter-position examples in draft/main.tex."""

from __future__ import annotations

import sympy as sp


t, x, u = sp.symbols("t x u")
u_t, u_x, u_tx, u_xx = sp.symbols("u_t u_x u_tx u_xx")
alpha, kappa = sp.symbols("alpha kappa", real=True, nonzero=True)


def total_t(expr: sp.Expr) -> sp.Expr:
    """Total t derivative needed for first prolongation coefficients."""
    return sp.diff(expr, t) + u_t * sp.diff(expr, u) + u_tx * sp.diff(expr, u_x)


def total_x(expr: sp.Expr) -> sp.Expr:
    """Total x derivative needed through the second x prolongation."""
    return (
        sp.diff(expr, x)
        + u_x * sp.diff(expr, u)
        + u_tx * sp.diff(expr, u_t)
        + u_xx * sp.diff(expr, u_x)
    )


def prolonged_residual(
    residual: sp.Expr, tau: sp.Expr, xi: sp.Expr, eta: sp.Expr
) -> sp.Expr:
    """Apply the second point prolongation to a scalar residual."""
    dt_tau = total_t(tau)
    dt_xi = total_t(xi)
    dx_tau = total_x(tau)
    dx_xi = total_x(xi)
    eta_t = total_t(eta) - u_t * dt_tau - u_x * dt_xi
    eta_x = total_x(eta) - u_t * dx_tau - u_x * dx_xi
    eta_xx = total_x(eta_x) - u_tx * dx_tau - u_xx * dx_xi
    return sp.expand(
        tau * sp.diff(residual, t)
        + xi * sp.diff(residual, x)
        + eta * sp.diff(residual, u)
        + eta_t * sp.diff(residual, u_t)
        + eta_x * sp.diff(residual, u_x)
        + eta_xx * sp.diff(residual, u_xx)
    )


def verify_power_diffusion() -> None:
    flux_x = u**alpha * u_xx + alpha * u ** (alpha - 1) * u_x**2
    residual = u_t - flux_x
    on_shell = {u_t: flux_x}

    generators = (
        (1, 0, 0),
        (0, 1, 0),
        (2 * t, x, 0),
        (alpha * t, 0, -u),
    )
    for generator in generators:
        value = prolonged_residual(residual, *generator).subs(on_shell)
        assert sp.simplify(value) == 0

    extra = prolonged_residual(residual, 0, x**2, -3 * x * u).subs(on_shell)
    expected = (3 * alpha + 4) * (x * flux_x + 2 * u**alpha * u_x)
    assert sp.simplify(extra - expected) == 0
    assert sp.simplify(extra.subs(alpha, sp.Rational(-4, 3))) == 0


def verify_quadratic_reaction() -> None:
    residual = u_t - u_xx - kappa * u**2
    on_shell = {u_t: u_xx + kappa * u**2}
    generators = (
        (1, 0, 0),
        (0, 1, 0),
        (2 * t, x, -2 * u),
    )
    for generator in generators:
        value = prolonged_residual(residual, *generator).subs(on_shell)
        assert sp.simplify(value) == 0

    c = sp.symbols("c", real=True, nonzero=True)
    transformed_coefficient = sp.simplify(kappa / c)
    assert sp.simplify(transformed_coefficient.subs(c, kappa)) == 1
    assert sp.simplify(transformed_coefficient.subs(c, -1)) == -kappa

    kappa_positive = sp.symbols("kappa_positive", positive=True)
    positive_scale = (kappa_positive / c).subs(c, kappa_positive)
    negative_scale = (-kappa_positive / c).subs(c, kappa_positive)
    assert sp.simplify(positive_scale) == 1
    assert sp.simplify(negative_scale) == -1


def verify_nonzero_resonance_counterexample() -> None:
    rho = sp.symbols("rho", nonzero=True)
    b11, b12, b21, b22 = sp.symbols("b11 b12 b21 b22")
    matrix_b = sp.Matrix([[b11, b12], [b21, b22]])
    matrix_k = sp.diag(1, rho)
    commutator = sp.simplify(matrix_b * matrix_k - matrix_k * matrix_b)
    assert commutator == sp.Matrix(
        [[0, (rho - 1) * b12], [(1 - rho) * b21, 0]]
    )


if __name__ == "__main__":
    verify_power_diffusion()
    verify_quadratic_reaction()
    verify_nonzero_resonance_counterexample()
    print("parameter-effect symbolic checks: PASS")
