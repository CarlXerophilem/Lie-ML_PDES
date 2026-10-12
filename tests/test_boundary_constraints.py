from dataclasses import replace
from pathlib import Path

import sympy as sp

from scripts.project_data_flux import _case, _modules
from symm.generic.boundary import normalize_zero_condition, restrict_to_constraints


def test_equivalent_moving_ray_and_dirichlet_conditions():
    api, jets, *_ = _modules(Path(__file__).resolve().parents[1])
    problem, generator, chart, _ = _case(api, jets, False)
    t, s = problem.system.jet_space.independent_variables
    phi = problem.system.jet_space.dependent_fields[0]
    original = problem.data[0]
    datum = api.DataCondition(original.name, s-t,
                              (phi-2*t, *original.residuals[1:]))
    result = api.reduce_in_chart(replace(problem, data=(datum,)), generator, chart,
                                 symmetry_multipliers=((-2,),))
    assert result.data_status == "data-compatible"
    assert result.pulled_data[0].surface == chart.reduced_space.independent_variables[0]-1
    assert all(value for _, value in result.data_checks)
    assert result.regularity_conditions


def test_boundary_restriction_is_local_and_parameter_safe():
    t, a, k = sp.symbols("t a k")
    assert restrict_to_constraints(t-a, (t-a,)).verified
    assert not restrict_to_constraints(t, (t-a,)).verified
    assert not restrict_to_constraints(t, (k*t,)).verified
    assert not restrict_to_constraints(t, (t, t-1)).verified
    assert not restrict_to_constraints(0, (t, t-1)).verified
    assert not restrict_to_constraints(0, (1,)).verified


def test_unknown_unit_is_preserved():
    rho = sp.Symbol("rho", positive=True)
    x, k = sp.symbols("x k")
    normalized, units = normalize_zero_condition(rho*k*(x-1))
    assert normalized == k*x-k
    assert rho in units and k not in units
    assert normalize_zero_condition(x-sp.Rational(1, 2))[0] == x-sp.Rational(1, 2)


def test_time_caps_and_frozen_flux_fail():
    t, t0 = sp.symbols("t t0", positive=True)
    assert not restrict_to_constraints(t, (t-t0,)).verified
    eta, integral = sp.symbols("eta integral", nonzero=True)
    assert sp.simplify((1+eta)*integral-integral) != 0
