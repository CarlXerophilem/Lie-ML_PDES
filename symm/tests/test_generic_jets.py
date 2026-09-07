import sympy as sp
import pytest

from symm.generic import (
    JetOrderLimitError,
    JetSpace,
    PointGenerator,
    iter_multi_indices,
    jet_coordinates,
    multi_index_count,
    prolong_characteristic,
    prolong_recursive,
    prolonged_action,
    total_derivative,
)


def test_multi_index_enumeration_matches_hockey_stick_count():
    indices = list(iter_multi_indices(3, 2))
    assert len(indices) == multi_index_count(3, 2) == 10
    assert len(set(indices)) == 10
    assert indices[0] == (0, 0, 0)
    assert indices[-1] == (2, 0, 0)


def test_total_derivatives_commute_within_order_budget():
    x, y, t = sp.symbols("x y t")
    u, v = sp.symbols("u v")
    space = JetSpace((x, y, t), (u, v), 3)
    coords = jet_coordinates(space)
    f = coords[(0, (1, 0, 0))] + v * coords[(1, (0, 1, 0))] + x * u
    dxy = total_derivative(space, total_derivative(space, f, 0, coordinates=coords), 1, coordinates=coords)
    dyx = total_derivative(space, total_derivative(space, f, 1, coordinates=coords), 0, coordinates=coords)
    assert sp.simplify(dxy - dyx) == 0


def test_recursive_and_characteristic_prolongations_agree():
    x, y, t = sp.symbols("x y t")
    u, v = sp.symbols("u v")
    space = JetSpace((x, y, t), (u, v), 2)
    generator = PointGenerator((x + t, y, 1), (u + x, v + t))
    recursive = prolong_recursive(space, generator, 2)
    characteristic_form = prolong_characteristic(space, generator, 2)
    assert recursive.keys() == characteristic_form.keys()
    for key in recursive:
        assert sp.simplify(recursive[key] - characteristic_form[key]) == 0


def test_translation_prolonged_action_is_zero_on_constant_coefficient_equation():
    x, t = sp.symbols("x t")
    u = sp.Symbol("u")
    space = JetSpace((x, t), (u,), 2)
    generator = PointGenerator((1, 0), (0,))
    equation = space.jet_symbol(0, (0, 1)) - space.jet_symbol(0, (2, 0))
    assert sp.simplify(prolonged_action(space, equation, generator)) == 0


def test_order_budget_never_silently_drops_a_term():
    x, t = sp.symbols("x t")
    u = sp.Symbol("u")
    space = JetSpace((x, t), (u,), 1)
    first_jet = space.jet_symbol(0, (1, 0))
    with pytest.raises(JetOrderLimitError):
        total_derivative(space, first_jet, 0)
    with pytest.raises(JetOrderLimitError):
        prolong_recursive(space, PointGenerator((1, 0), (0,)), 2)

