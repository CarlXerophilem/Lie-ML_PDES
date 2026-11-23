import sympy as sp

from symm.generic import (
    DifferentialSystem,
    JetSpace,
    PointGenerator,
    bracket,
    check_lie_closure,
    orbit_rank,
    translation_reduce,
)


def _three_variable_system():
    x, y, t = sp.symbols("x y t")
    u = sp.Symbol("u")
    space = JetSpace((x, y, t), (u,), 1)
    equation = (
        space.jet_symbol(0, (0, 0, 1))
        - space.jet_symbol(0, (1, 0, 0))
        - space.jet_symbol(0, (0, 1, 0))
    )
    return DifferentialSystem(space, (equation,), name="transport-3")


def test_translation_reduction_is_verified_and_lowers_dimension():
    system = _three_variable_system()
    first = PointGenerator((1, 0, 0), (0,))
    result = translation_reduce(system, first)
    assert result.certificate.status == "verified"
    assert result.certificate.all_checks_pass
    assert result.reduced_system is not None
    assert result.reduced_system.jet_space.p == 2
    assert all(value == 0 for value in result.certificate.residuals)


def test_translation_reduction_is_composable():
    system = _three_variable_system()
    first = translation_reduce(system, PointGenerator((1, 0, 0), (0,)))
    assert first.reduced_system is not None
    second = translation_reduce(first.reduced_system, PointGenerator((1, 0), (0,)))
    assert second.certificate.status == "verified"
    assert second.reduced_system is not None
    assert second.reduced_system.jet_space.p == 1


def test_explicit_dependence_and_guard_loss_are_rejected():
    x, t = sp.symbols("x t")
    u = sp.Symbol("u")
    space = JetSpace((x, t), (u,), 1)
    equation = space.jet_symbol(0, (0, 1))
    explicit = DifferentialSystem(space, (x * equation,), name="explicit")
    result = translation_reduce(explicit, PointGenerator((1, 0), (0,)))
    assert result.reduced_system is None
    assert result.certificate.status == "unsupported"

    guarded = DifferentialSystem(
        space, (equation,), inequations=(space.jet_symbol(0, (1, 0)),), name="guarded"
    )
    result = translation_reduce(guarded, PointGenerator((1, 0), (0,)))
    assert result.reduced_system is None
    assert result.certificate.status == "unsupported"


def test_bracket_closure_and_orbit_rank():
    x, t = sp.symbols("x t")
    u = sp.Symbol("u")
    space = JetSpace((x, t), (u,), 1)
    dx = PointGenerator((1, 0), (0,))
    dt = PointGenerator((0, 1), (0,))
    assert bracket(space, dx, dt) == PointGenerator((0, 0), (0,))
    algebra = check_lie_closure(space, (dx, dt))
    assert algebra.closure_status == "closed"
    assert orbit_rank(space, (dx, dt)) == 2


def test_bracket_antisymmetry_and_jacobi_identity():
    x, t = sp.symbols("x t")
    u = sp.Symbol("u")
    space = JetSpace((x, t), (u,), 1)
    scale = PointGenerator((x, 0), (0,))
    shift = PointGenerator((1, 0), (0,))
    time_shift = PointGenerator((0, 1), (0,))
    zero = PointGenerator((0, 0), (0,))
    assert bracket(space, scale, shift) == PointGenerator((-1, 0), (0,))
    assert bracket(space, scale, shift) == PointGenerator(
        tuple(-value for value in bracket(space, shift, scale).xi), (0,)
    )
    jacobi = (
        bracket(space, scale, bracket(space, shift, time_shift)).xi,
        bracket(space, shift, bracket(space, time_shift, scale)).xi,
        bracket(space, time_shift, bracket(space, scale, shift)).xi,
    )
    assert tuple(sum(item[index] for item in jacobi) for index in range(2)) == zero.xi
