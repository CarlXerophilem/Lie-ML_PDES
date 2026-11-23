"""Original-equation and exceptional-branch controls for the P solution programme."""
import sympy as sp
import pytest
from symm.LieSymm import scalar2026 as api


def test_solution_interfaces_and_coverage():
    assert hasattr(api, 'solution_catalog'), 'the direct-solving API is missing'
    rows = api.solution_catalog()
    assert {f'3.{i}' for i in range(1, 10)} <= {a for r in rows for a in r['aliases']}
    assert {'generic', 'm1', 'm3'} == {m for r in rows for m in r['algebra_strata']}
    assert all(r['model'] == 'P' and 'generator' in r for r in rows)


@pytest.mark.parametrize('name', ['m1-boost-travel', 'm1-boost-space', 'paper-3.7', 'paper-3.8'])
def test_exact_graphs_have_independent_P_and_Q_certificates(name):
    result = api.solve_reduction(name, parameters={'m': 1, 'a': 0})
    check = api.verify_solution(result)
    assert check['exact_passed'], check


def test_rejected_parameters_and_distinct_non_odes():
    for parameters in ({'m': 0}, {'g': 0}, {'kappa': -1}):
        with pytest.raises(ValueError):
            api.solve_reduction('paper-3.4', parameters=parameters)
    assert api.solve_reduction('paper-3.2', parameters={})['status'] == 'undefined_pde'
    assert api.solve_reduction('paper-3.3', parameters={})['status'] == 'no_invariant_graph'
    with pytest.raises(ValueError, match='m=3'):
        api.solve_reduction('paper-3.5', parameters={'m': 2})


def test_zero_speed_and_zero_integral_are_not_divided():
    identity = api.solve_reduction('paper-3.9', parameters={'alpha': 0, 'alpha3': 2})
    assert identity['status'] == 'exact_arbitrary_function'
    affine = api.solve_reduction('paper-3.6', parameters={}, data={'I0': 0})
    assert affine['status'] == 'exact_affine'
    assert api.verify_solution(affine)['exact_passed']


def test_m1_accelerating_travel_quadrature():
    result = api.solve_reduction('m1-boost-travel', parameters={'m': 1, 'a': -1, 'sigma': 1})
    assert result['status'] == 'exact_parametric_quadrature'
    assert api.verify_solution(result)['exact_passed']


def test_cubic_singular_quadrature_and_equilibrium():
    result = api.solve_reduction('paper-3.4', parameters={'m': 3}, data={'branch': 'singular'})
    assert result['status'] == 'exact_parametric_quadrature'
    assert api.verify_solution(result)['exact_passed']
    power = api.solve_reduction('paper-3.4', parameters={'m': 3}, data={'branch': 'power'})
    assert api.verify_solution(power)['exact_passed']
    with pytest.raises(ValueError, match='positive'):
        api.solve_reduction('paper-3.4', parameters={'m': 3, 'g': 1, 'kappa': sp.Rational(1, 12)}, data={'branch': 'power'})


def test_autonomous_turning_point_is_not_original_singularity():
    from symm.LieSymm.scalar2026.solving import cubic_autonomous
    r = cubic_autonomous(1, sp.Rational(1, 30))
    S, M = r['variables']
    at = {S: 1, M: -sp.Rational(2, 3)}
    assert r['rhs'][0].subs(at) == 0
    assert r['delta'].subs(at) != 0
    assert r['rhs'][1].subs(at).is_finite


def test_mixed_resonant_graphs_and_reduction_certificates():
    for name, parameters in [('cubic-mixed', {'a': 1, 'b': -1}),
                             ('cubic-resonant-time', {'c': 1}),
                             ('cubic-resonant-space', {'c': -1}),
                             ('cubic-resonant-vertical', {'c': 1}),
                             ('m1-scale-boost', {'m': 1, 'alpha': 2})]:
        result = api.solve_reduction(name, parameters=parameters)
        check = api.verify_solution(result)
        assert check['reduction_passed'], (name, check)
        assert result['remaining_equation'] is not None


def test_incompatible_jet_and_perturbed_graph_rejected():
    result = api.solve_reduction('paper-3.8', parameters={}, data={'z0': 1, 'jet': (2, -1, 0)})
    assert result['data_status'] == 'incompatible'
    exact = api.solve_reduction('paper-3.8', parameters={})
    t = exact['variables'][0]
    exact['expression'] += t**3
    assert not api.verify_solution(exact)['exact_passed']


def test_supplied_integral_cannot_contradict_affine_branch():
    result=api.solve_reduction('m1-boost-travel',parameters={'m':1,'a':-1},
                               data={'branch':'affine','I0':3,'p0':1})
    assert result['data_status']=='incompatible'
    assert not api.verify_solution(result)['exact_passed']
    result=api.solve_reduction('paper-3.8',parameters={'alpha':-1})
    assert result['status']=='outside_positive_chart'


def test_series_and_numerical_crosscheck_reconstruct_original_P(tmp_path):
    from symm.LieSymm.scalar2026.continuation import continue_profile
    r=api.solve_reduction('m1-scale-boost',parameters={'m':1,'alpha':1},
                          data={'z0':1,'jet':(2,sp.Rational(1,2),sp.Rational(1,10))})
    assert r['series']['passed']
    assert len(r['series']['coefficients'])==7
    n=continue_profile(r,tmp_path,interval=(1,1.6))
    assert n['status']=='passed',n
    assert n['state_error']<=n['state_tolerance']
    assert n['original_pde']['negative_control_passed']


def test_singular_data_and_invalid_interval_never_integrated(tmp_path):
    from symm.LieSymm.scalar2026.continuation import continue_profile
    r=api.solve_reduction('paper-3.4',parameters={'g':sp.Rational(1,2),'kappa':sp.Rational(1,12)},
                          data={'z0':1,'jet':(3,1,-sp.Rational(2,3))})
    assert r['data_status']=='singular_implicit'
    assert continue_profile(r,tmp_path,interval=(1,2))['status']=='not_regular'


def test_singular_parameter_chart_respects_both_integrated_maps():
    r=api.solve_reduction('paper-3.4',parameters={},data={'branch':'singular'})
    r['parametric']['profile_map']+=r['parametric']['parameter']
    assert not api.verify_solution(r)['exact_passed']


def test_continuous_exponents_have_symbolic_pullback_certificate():
    for row in api.solution_catalog():
        if row['id'] in ('paper-3.4','paper-3.6','paper-3.9'):
            row.update(expression=None,data_status='not_supplied')
            assert api.verify_solution(row)['reduction_passed'],row['id']


def test_parametric_solution_binds_the_supplied_initial_jet():
    r=api.solve_reduction('m1-boost-travel',parameters={'m':1,'a':-1},
                          data={'z0':1,'jet':(2,sp.Rational(1,2),sp.Rational(1,10))})
    param=r['parametric'];rr=param['parameter']
    assert sp.simplify(param['coordinate_map'].subs(rr,sp.Rational(1,2)))==1
    assert sp.simplify(param['profile_map'].subs(rr,sp.Rational(1,2)))==2
    assert r['data']['I0']==r['initial_integral']


def test_verifier_recomputes_invariance_away_from_transversal():
    r=api.solve_reduction('paper-3.4',parameters={},data={'branch':'singular'})
    T=r['variables'][0]
    r['graph']+=(T-1)**4
    assert not api.verify_solution(r)['reduction_passed']


def test_unsupported_branches_and_nonfinite_parameters_rejected():
    with pytest.raises(ValueError,match='branch'):
        api.solve_reduction('paper-3.5',parameters={},data={'branch':'typo'})
    with pytest.raises(ValueError):
        api.solve_reduction('cubic-mixed',parameters={'a':sp.I})


def test_spatial_resonance_has_second_order_initial_data(tmp_path):
    from symm.LieSymm.scalar2026.continuation import continue_profile
    r=api.solve_reduction('cubic-mixed',parameters={'a':1,'b':sp.Rational(1,2)},
                          data={'z0':1,'jet':(2,sp.Rational(1,2))})
    assert r['ode_order']==2
    assert r['data_status']=='compatible'
    assert r['series']['passed']
    n=continue_profile(r,tmp_path,interval=(1,1.6))
    assert n['status']=='passed',n


def test_printed_bed_trace_and_additive_datum_are_checked():
    from symm.LieSymm.scalar2026.catalog import s
    data={'z0':1,'jet':(2,sp.Rational(1,2),sp.Rational(1,10)),
          'bed_datum':(1,0,2),'bed_profile':2-s/10}
    r=api.solve_reduction('paper-3.8',parameters={},data=data)
    check=api.verify_solution(r)
    assert check['exact_passed'] and check['bed']['data_passed']
    data['bed_profile']=2+s/10
    r=api.solve_reduction('paper-3.8',parameters={},data=data)
    check=api.verify_solution(r)
    assert not check['exact_passed']
    assert check['bed']['data_residuals']['slope']!=0


@pytest.mark.parametrize('branch', ['affine', 'singular', 'power'])
def test_review_exact_branch_rejects_incompatible_initial_jet(branch):
    r=api.solve_reduction('paper-3.4',parameters={},data={
        'branch':branch,'z0':1,'jet':(2,sp.Rational(1,2),sp.Rational(1,10))})
    assert r['data_status']=='incompatible'
    assert not api.verify_solution(r)['exact_passed']


@pytest.mark.parametrize('branch', ['singular', 'power'])
def test_review_zero_integral_is_required_without_a_jet(branch):
    r=api.solve_reduction('paper-3.4',parameters={},data={'branch':branch,'I0':1})
    assert r['data_status']=='incompatible'


def test_review_affine_anchor_and_independent_initial_jet_check():
    from symm.LieSymm.scalar2026.catalog import t,s
    r=api.solve_reduction('paper-3.4',parameters={},data={
        'branch':'affine','z0':1,'jet':(2,sp.Rational(1,2),0)})
    assert sp.simplify(r['expression']-(3*t/2+s/2))==0
    assert r['data_status']=='compatible'
    assert api.verify_solution(r)['exact_passed']
    r['expression']+=t
    assert not api.verify_solution(r)['exact_passed']


def test_review_singular_parameter_family_binds_jet_and_keeps_singular_solution():
    rho=(sp.Rational(10,9))**sp.Rational(1,3)
    r=api.solve_reduction('paper-3.4',parameters={},data={
        'branch':'singular','z0':1,'jet':(2*rho,rho,-20*rho/31)})
    assert r['data_status']=='compatible',r
    par=r['parametric'];y=par['parameter']
    assert sp.simplify(par['coordinate_map'].subs(y,2))==1
    assert sp.simplify(par['profile_map'].subs(y,2)-2*rho)==0
    assert api.verify_solution(r)['exact_passed']


def test_review_regular_solver_stops_at_leading_coefficient_sign_change(tmp_path):
    from symm.LieSymm.scalar2026.continuation import continue_profile
    r=api.solve_reduction('paper-3.4',parameters={},data={'z0':1,'jet':(2,1,0)})
    n=continue_profile(r,tmp_path,interval=(1,1.2))
    assert n['status']=='guard_stop',n
    assert n['stopped_at']<1.06


def test_review_bed_anchor_outside_positive_chart_is_rejected():
    r=api.solve_reduction('m1-boost-space',parameters={'sigma':-1},
                          data={'bed_datum':(1,0,0)})
    check=api.verify_solution(r)
    assert not check['bed']['data_passed']
    assert not check['exact_passed']
    assert check['bed']['data_status']=='incompatible'


def test_review_parametric_bed_data_is_explicitly_unchecked():
    r=api.solve_reduction('paper-3.9',parameters={},
                          data={'bed_datum':(1,0,0),'bed_profile':0})
    check=api.verify_solution(r)
    assert check['bed']['data_status']=='unsupported'
    assert not check['exact_passed']
    assert check['parametric']['passed']


def test_review_logarithmic_constants_realize_supplied_jet():
    from symm.LieSymm.scalar2026.solving import _profile_of_expression
    from symm.LieSymm.scalar2026.catalog import z
    jet=(2,sp.Rational(1,2),sp.Rational(1,10))
    r=api.solve_reduction('m1-boost-space',parameters={},data={'z0':1,'jet':jet})
    profile=_profile_of_expression(r)
    assert all(sp.simplify(sp.diff(profile,z,i).subs(z,1)-value)==0 for i,value in enumerate(jet))
    assert api.verify_solution(r)['exact_passed']


def test_review_power_branch_accepts_its_own_singular_initial_jet():
    amp=sp.Integer(45)**sp.Rational(1,3)
    r=api.solve_reduction('paper-3.4',parameters={},data={
        'branch':'power','z0':1,'jet':(amp,amp/3,-2*amp/9)})
    assert r['data_status']=='compatible'
    assert api.verify_solution(r)['exact_passed']
