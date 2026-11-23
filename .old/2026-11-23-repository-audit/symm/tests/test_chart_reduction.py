"""Independent chain-rule fixtures and negative cases for chart reduction."""

from dataclasses import replace
import importlib

import pytest
import sympy as sp

from symm.generic import DifferentialSystem, JetSpace, PointGenerator


def api():
    # A missing public operation must fail as an assertion before implementation.
    module = importlib.import_module("symm.generic")
    for name in ("PDEProblem", "DataCondition", "ReductionChart", "reduce_in_chart"):
        assert hasattr(module, name), f"missing chart-reduction API: {name}"
    return module


def transport_case():
    a = api()
    t, x, c = sp.symbols("t x c", real=True)
    u = sp.Symbol("u")
    z, rho, U = sp.symbols("z rho U", real=True)
    source = JetSpace((t, x), (u,), 1)
    reduced = JetSpace((z,), (U,), 1)
    equation = source.jet_symbol(0, (1, 0)) + c * source.jet_symbol(0, (0, 1))
    problem = a.PDEProblem(DifferentialSystem(source, (equation,)), parameters=(c,))
    chart = a.ReductionChart(reduced, (x - c*t,), rho, t, (rho, z + c*rho), (U,), (1,))
    return a, problem, PointGenerator((1, c), (0,)), chart


def test_traveling_coordinate_uses_both_chain_rule_terms():
    a, problem, generator, chart = transport_case()
    result = a.reduce_in_chart(problem, generator, chart)
    assert result.certificate.status == "verified"
    assert result.reduced_system.equations == (0,)
    # Changing to u_t + (c+1)u_x must leave U_z, not the old zero.
    space = problem.system.jet_space
    other = replace(problem, system=replace(problem.system, equations=(
        problem.system.equations[0] + space.jet_symbol(0, (0, 1)),)))
    assert a.reduce_in_chart(other, generator, chart).reduced_system.equations == (
        chart.reduced_space.jet_symbol(0, (1,)),)


def test_multiple_fields_and_more_equations_than_fields():
    a = api()
    t, x, y = sp.symbols("t x y")
    u, v, U, V = sp.symbols("u v U V")
    z, w, rho = sp.symbols("z w rho")
    space = JetSpace((t, x, y), (u, v), 2)
    j = space.jet_symbol
    equations = (j(0, (1,0,0))-j(0, (0,2,0))-j(0, (0,0,2)),
                 j(1, (1,0,0))-j(1, (0,2,0))-j(1, (0,0,2)),
                 j(0, (0,1,0))+j(1, (0,0,1)))
    reduced = JetSpace((z, w), (U, V), 2)
    chart = a.ReductionChart(reduced, (x,y), rho, t, (rho,z,w), (U,V), (1,1,1))
    outcome = a.reduce_in_chart(a.PDEProblem(DifferentialSystem(space, equations)),
                                PointGenerator((1,0,0),(0,0)), chart)
    assert outcome.certificate.status == "verified"
    rj = reduced.jet_symbol
    assert outcome.reduced_system.equations == (
        -rj(0,(2,0))-rj(0,(0,2)), -rj(1,(2,0))-rj(1,(0,2)),
        rj(0,(1,0))+rj(1,(0,1)))


def test_field_scaling_and_mixed_derivatives():
    a = api()
    t, x, u, z, rho, U = sp.symbols("t x u z rho U")
    space = JetSpace((t,x),(u,),2)
    equation = space.jet_symbol(0,(1,1))-space.jet_symbol(0,(0,1))
    chart = a.ReductionChart(JetSpace((z,),(U,),2), (x,), rho, t,
                            (rho,z), (sp.exp(t)*U,), (sp.exp(t),))
    outcome = a.reduce_in_chart(a.PDEProblem(DifferentialSystem(space,(equation,))),
                                PointGenerator((1,0),(u,)), chart,
                                symmetry_multipliers=((1,),))
    assert outcome.certificate.status == "verified"
    assert outcome.reduced_system.equations == (0,)


def test_data_and_domain_are_retained_without_claiming_ibvp_symmetry():
    a, problem, generator, chart = transport_case()
    t, x = problem.system.jet_space.independent_variables
    u = problem.system.jet_space.dependent_fields[0]
    data = a.DataCondition("initial", t, (u-x**2,))
    problem = replace(problem, domain=(t >= 0,), data=(data,))
    result = a.reduce_in_chart(problem, generator, chart)
    z = chart.reduced_space.independent_variables[0]
    U = chart.reduced_space.dependent_fields[0]
    c = problem.parameters[0]
    assert result.data_status == "pulled-back-only"
    assert result.data_checks
    assert not all(value for _, value in result.data_checks)
    assert result.pulled_data[0].surface == chart.orbit_variable
    assert sp.expand(result.pulled_data[0].residuals[0] - (U-(z+c*chart.orbit_variable)**2)) == 0
    assert result.pulled_domain == (chart.orbit_variable >= 0,)


def test_sve_invariant_data_surface_and_three_jets_are_strictly_compatible():
    a = api()
    from symm.generic.sve_reduction import sve_data_family_case

    problem, generator, chart, multipliers = sve_data_family_case()
    outcome = a.reduce_in_chart(problem, generator, chart,
                                symmetry_multipliers=multipliers)
    assert outcome.certificate.status == "verified"
    assert outcome.data_status == "data-compatible"
    assert outcome.data_checks
    assert all(value for _, value in outcome.data_checks)
    assert outcome.data_invariance_residuals
    assert all(sp.simplify(value) == 0 for value in outcome.data_invariance_residuals)

    sigma = chart.reduced_space.independent_variables[0]
    rho = chart.orbit_variable
    pulled = outcome.pulled_data[0]
    assert sp.expand(pulled.surface - (sigma - 1)) == 0
    assert all(not residual.has(rho) for residual in pulled.residuals)
    assert len(pulled.residuals) == 3


@pytest.mark.parametrize("defect", ["inverse", "invariant", "zero-factor", "fiber-rank", "symmetry", "guard"])
def test_invalid_inputs_never_emit_a_verified_reduction(defect):
    a, problem, generator, chart = transport_case()
    t, x = problem.system.jet_space.independent_variables
    if defect == "inverse":
        chart = replace(chart, inverse_coordinates=(chart.orbit_variable, chart.reduced_space.independent_variables[0]))
    elif defect == "invariant":
        chart = replace(chart, invariants=(t,))
    elif defect == "zero-factor":
        chart = replace(chart, equation_factors=(0,))
    elif defect == "fiber-rank":
        chart = replace(chart, field_reconstruction=(0,))
    elif defect == "symmetry":
        problem = replace(problem, system=replace(problem.system, equations=(problem.system.equations[0]+t,)))
    elif defect == "guard":
        j = problem.system.jet_space.jet_symbol
        problem = replace(problem, system=replace(problem.system, inequations=(j(0,(1,0))+problem.parameters[0]*j(0,(0,1)),)))
    result = a.reduce_in_chart(problem, generator, chart)
    assert result.reduced_system is None
    assert result.certificate.status == "unsupported"


def test_reconstruction_must_satisfy_invariant_surface_equation():
    a, problem, generator, chart = transport_case()
    t = problem.system.jet_space.independent_variables[0]
    chart = replace(chart, field_reconstruction=(sp.exp(t)*chart.reduced_space.dependent_fields[0],))
    result = a.reduce_in_chart(problem, generator, chart)
    assert result.reduced_system is None
    assert not dict(result.certificate.checks)["invariant_surface"]


def test_orbit_dependent_residual_cannot_be_called_a_reduced_equation():
    a, problem, generator, chart = transport_case()
    t = problem.system.jet_space.independent_variables[0]
    ux = problem.system.jet_space.jet_symbol(0,(0,1))
    problem = replace(problem,system=replace(problem.system,equations=(problem.system.equations[0]+ux,)))
    chart = replace(chart,equation_factors=(t,))
    result = a.reduce_in_chart(problem,generator,chart)
    assert result.reduced_system is None
    assert not dict(result.certificate.checks)["orbit_independent_equations"]


def test_domain_denominators_are_preserved_even_when_pullback_cancels_them():
    a, problem, generator, chart = transport_case()
    ut,ux = [problem.system.jet_space.jet_symbol(0,index) for index in ((1,0),(0,1))]
    problem = replace(problem,domain=(ut/ux > 0,))
    assert ux in problem.denominator_guards
    outcome = a.reduce_in_chart(problem,generator,chart)
    Uz = chart.reduced_space.jet_symbol(0,(1,))
    assert any(condition.has(Uz) for condition in outcome.regularity_conditions)


def test_formalization_rejects_nonpredicate_domain():
    _, problem, _, _ = transport_case()
    with pytest.raises(ValueError,match="predicate"):
        replace(problem,domain=(problem.system.jet_space.independent_variables[0],))


def test_supplied_sympy_matrix_has_the_same_checked_meaning():
    a, problem, generator, chart = transport_case()
    outcome = a.reduce_in_chart(problem,generator,chart,symmetry_multipliers=sp.zeros(1))
    assert outcome.certificate.status == "verified"
    assert outcome.reduced_system.equations == (0,)


def test_equations_require_residual_expressions():
    _, problem, _, _ = transport_case()
    with pytest.raises(ValueError,match="residual"):
        replace(problem,system=replace(problem.system,equations=(sp.S.true,)))


def test_formalization_distinguishes_real_parameter_and_jet_structure():
    a, problem, _, _ = transport_case()
    space = problem.system.jet_space
    ut, ux = space.jet_symbol(0,(1,0)), space.jet_symbol(0,(0,1))
    m = sp.Symbol("m", real=True)
    assert problem.jet_structure == ("polynomial",)
    rational = replace(problem, system=replace(problem.system, equations=(ut/ux,)))
    assert rational.jet_structure == ("rational",)
    assert ux in rational.denominator_guards
    nonpoly = replace(problem, parameters=(*problem.parameters,m),
                      system=replace(problem.system, equations=(ut**m/ux,)))
    assert nonpoly.jet_structure == ("nonpolynomial",)
    with pytest.raises(ValueError, match="undeclared"):
        replace(problem, system=replace(problem.system, equations=(ut+m,)))


def test_sve_cubic_matches_independent_third_order_ode():
    a = api()
    from symm.generic.sve_reduction import sve_scaling_case
    problem, generator, chart, multipliers = sve_scaling_case()
    outcome = a.reduce_in_chart(problem,generator,chart,symmetry_multipliers=multipliers)
    assert outcome.certificate.status == "verified"
    z = chart.reduced_space.independent_variables[0]
    r = chart.reduced_space.jet_symbol(0,(1,))
    v = chart.reduced_space.jet_symbol(0,(2,))
    w = chart.reduced_space.jet_symbol(0,(3,))
    g, kappa = problem.parameters
    beta = 3*kappa
    leading = 8*(1-g*beta)*z**3*r-2*g*z/r**2
    remainder = (4*z*(1-4*g*beta)*r**2 + 8*z**2*(3-5*g*beta)*r*v
                 +(8*z**3*(1-g*beta)+4*g*z/r**3)*v**2)
    assert sp.cancel(outcome.reduced_system.equations[0]-leading*w-remainder) == 0
    # An independent direct differentiation of a nonpolynomial profile.
    F = chart.reduced_space.dependent_fields[0]
    concrete = sp.exp(z)
    expected = (leading*w+remainder).subs({r:concrete,v:concrete,w:concrete})
    assert sp.simplify(outcome.reduced_system.equations[0].subs({F:concrete,r:concrete,v:concrete,w:concrete})-expected) == 0
    noncubic = sve_scaling_case(m=4)
    failed = a.reduce_in_chart(*noncubic[:3],symmetry_multipliers=noncubic[3])
    assert failed.reduced_system is None
    assert not dict(failed.certificate.checks)["symmetry_identity"]


def test_sve_lift_agrees_with_direct_differentiation_of_a_field():
    a = api()
    from symm.generic.sve_reduction import sve_scaling_case
    from symm.generic import iter_multi_indices
    problem,generator,chart,matrix = sve_scaling_case()
    result = a.reduce_in_chart(problem,generator,chart,symmetry_multipliers=matrix)
    t,s = problem.system.jet_space.independent_variables
    z = chart.reduced_space.independent_variables[0]
    profile = sp.exp(z)+z**2
    field = profile.subs(z,s*t**2)
    direct = {problem.system.jet_space.jet_symbol(0,index):sp.diff(field,t,index[0],s,index[1])
              for index in iter_multi_indices(2,3)}
    reduced = {chart.reduced_space.jet_symbol(0,(n,)):sp.diff(profile,z,n) for n in range(4)}
    original_residual = problem.system.equations[0].xreplace(direct)
    reduced_residual = result.reduced_system.equations[0].xreplace(reduced).subs(z,s*t**2)/t
    assert sp.simplify(original_residual-reduced_residual) == 0
