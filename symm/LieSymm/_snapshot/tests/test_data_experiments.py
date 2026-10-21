"""Data tangency and original-PDE controls, independent of a solver ansatz."""
import importlib

import pytest
import sympy as sp

from models import BRANCHES, t, x, h, u, B, g, K, G, m, n


def module():
    assert importlib.util.find_spec('data_experiments') is not None, 'data controls are not implemented'
    return importlib.import_module('data_experiments')


@pytest.mark.parametrize('value',[sp.I,sp.oo,sp.nan,t])
def test_parameter_specialization_rejects_nonphysical_constants(value):
    with pytest.raises(ValueError):
        module().uniform_flow('grass_generic',substitutions={g:value})


def test_symbolic_parameter_guard_is_pulled_back_with_substitution():
    r=sp.Symbol('r',real=True)
    result=module().uniform_flow('grass_generic',substitutions={g:r})
    assert 'r > 0' in result['parameter_guards']
    assert result['parameter_substitutions']=={g:r}


@pytest.mark.parametrize('branch', tuple(BRANCHES))
def test_uniform_and_accelerating_flow_satisfy_original_coupled_rows(branch):
    data = module()
    uniform = data.uniform_flow(branch, depth=2, velocity=3, datum=5)
    accelerating = data.constant_slope_flow(branch, depth=2, velocity=3,
                                            slope=sp.Rational(1,5), datum=5, time0=2)
    for result in (uniform, accelerating):
        assert result['status'] == 'verified_exact_solution'
        assert result['check']['equation_residuals'] == [0, 0, 0]
        assert result['scope'] == 'constructed smooth solution on recorded chart'
    assert sp.diff(accelerating['graph'][1],t) == -g/5
    assert accelerating['graph'][1].subs(t,2) == 3
    assert any(condition.has(t) for condition in accelerating['chart_guards'])


@pytest.mark.parametrize('branch', tuple(BRANCHES))
@pytest.mark.parametrize('bed,expected_no_slope,expected_slope',[(1,2,1),(1+x,1,1),(1+x**2,0,0)])
def test_concrete_flat_linear_quadratic_initial_stabilizers(branch,bed,expected_no_slope,expected_slope):
    result = module().initial_data_stabilizer(branch,(2,3,bed),time0=0)
    assert result['status'] == 'verified_initial_data_stabilizer', result
    assert result['dimension'] == (expected_slope if BRANCHES[branch]['G'] else expected_no_slope)
    assert all(v==0 for v in result['verification_residuals'])
    assert result['pde_solution_claim'] is False
    if bed != 1:
        assert result['frozen_profile_diagnostic']['is_solution'] is False


def test_nonzero_initial_time_and_two_fixed_endpoints_remove_base_dilations():
    data = module()
    free = data.initial_data_stabilizer('grass_cubic',(2,3,5),time0=2)
    assert free['dimension'] == 2
    assert free['stabilized_coefficients'][0].subs(t,2) == 0
    fixed = data.initial_data_stabilizer('grass_cubic',(2,3,5),time0=2,endpoints=(0,1))
    assert fixed['dimension'] == 0
    assert fixed['stabilized_coefficients'] == (0,0,0,0,0)


def test_sediment_flux_uses_prolonged_slope_not_just_velocity():
    # m=3,n=2 dilation: prX(B_x)=B_x, so every term in J has weight three.
    variation = module().sediment_flux_variation('slope_attachment_cubic',(0,x,2*h,u,2*B))
    assert sp.simplify(variation['variation']-3*variation['flux']) == 0
    assert variation['slope_variation'] == variation['bed_slope_jet']
    wrong = 3*K*u**3-4*G*u**2*variation['bed_slope_jet']
    assert sp.simplify(variation['variation']-wrong) == G*u**2*variation['bed_slope_jet']


def test_prescribed_flux_compatibility_is_checked_before_a_stabilizer_is_certified():
    data = module()
    compatible = data.initial_data_stabilizer('slope_attachment_cubic',(2,3,1+x),
                                              sediment_flux=27*K-9*G)
    assert compatible['status'] == 'verified_initial_data_stabilizer'
    assert compatible['flux_data']['compatibility_residuals'] == (0,)
    wrong = data.initial_data_stabilizer('grass_cubic',(2,3,1),sediment_flux=0)
    assert wrong['status'] == 'incompatible_prescribed_flux'
    assert wrong['flux_data']['compatibility_residuals'] == (27*K,)


def test_flux_at_fixed_endpoints_keeps_initial_time_scope_and_endpoints():
    result = module().initial_data_stabilizer('grass_cubic',(2,3,1),
                                              sediment_flux={0:27*K,1:27*K})
    assert result['status'] == 'verified_initial_data_stabilizer'
    assert result['dimension'] == 0
    assert result['boundary_scope'] == 'fixed endpoint tangency; flux values only on the initial slice'


def test_unknown_profile_parameter_rank_drop_is_not_silently_discarded():
    slope = sp.Symbol('profile_slope',real=True)
    result = module().initial_data_stabilizer('grass_generic',(2,3,1+slope*x))
    assert result['status'] == 'conditional_initial_data_stabilizer'
    assert result['rank_guards']
    assert result['unresolved_zero_pivot_branches']
    flat = module().initial_data_stabilizer('grass_generic',(2,3,1))
    assert flat['dimension'] == 2


def test_nonpolynomial_initial_data_retains_functional_constraints():
    result = module().initial_data_stabilizer('grass_generic',(2,3,sp.sin(x)))
    assert result['status'] == 'unresolved_functional_splitting'
    assert result['tangency_identities']
    assert result['pde_solution_claim'] is False


@pytest.mark.parametrize('branch,substitutions',[
    ('grass_generic',{m:1}),('grass_cubic',{}),
    ('slope_attachment_generic',{m:1}),('slope_attachment_cubic',{}),
    ('slope_only',{n:0}),('slope_only',{n:2}),('slope_only',{n:4}),
    ('zero_transport',{}),
])
def test_flat_lake_only_on_explicit_polynomial_extension(branch,substitutions):
    result = module().lake_control(branch,bed=1,level=3,substitutions=substitutions)
    assert result['status'] == 'verified_polynomial_zero_speed_solution',result
    assert result['check']['equation_residuals'] == [0,0,0]
    assert result['inside_classified_positive_speed_chart'] is False


@pytest.mark.parametrize('branch,substitutions',[
    ('grass_generic',{}),('grass_generic',{m:sp.Rational(3,2)}),
    ('slope_source_generic',{m:1}),('slope_source_cubic',{}),
    ('slope_only',{}),('slope_only',{n:1}),
])
def test_unapproved_zero_speed_extensions_remain_outside_chart(branch,substitutions):
    result = module().lake_control(branch,bed=1,level=3,substitutions=substitutions)
    assert result['status'] == 'outside_declared_chart'
    assert result['check'] is None


def test_constant_diffusivity_quadratic_static_lake_fails_but_coupled_level_motion_passes():
    data = module()
    static = data.lake_control('slope_only',bed=x**2,level=3,substitutions={n:0})
    assert static['status'] == 'negative_pde_control'
    assert static['check']['equation_residuals'] == [0,0,-2*G]
    moving = data.lake_control('slope_only',bed=x**2+2*G*t,level=3+2*G*t,substitutions={n:0})
    assert moving['status'] == 'verified_polynomial_zero_speed_solution'
    assert moving['graph'][0] == 3-x**2
    assert moving['check']['equation_residuals'] == [0,0,0]
    unsupported = data.lake_control('slope_only',bed=x**2,level=3+2*G*t,substitutions={n:0})
    assert unsupported['check']['equation_residuals'] == [2*G,0,-2*G]


def test_full_data_report_covers_each_registered_branch_without_claiming_flat_bed_uniqueness():
    result = module().run_data_experiments()
    assert set(result['branches']) == set(BRANCHES)
    assert result['all_exact_flow_controls_passed'] is True
    assert result['all_concrete_initial_stabilizers_verified'] is True
    assert result['claim_scope'] == 'constructed controls and specified initial-data stabilizers only'
