"""Independent original-equation/data/map regressions for the 2D controls."""
import pytest
import sympy as sp

from data_experiments_2d import (run_data_controls,uniform_rotating_flow,constant_slope_flow,
    initial_data_stabilizer,conservative_point_map,pushforward_generator,signed_coriolis_reflection)
from models_2d import BRANCHES_2D,t,x,y,h,u,v,B,g,K,G,m,n,f


@pytest.mark.parametrize('name',tuple(BRANCHES_2D))
def test_all_declared_controls_and_independent_data_dimensions(name):
    result=run_data_controls(name)
    assert result['status']=='verified_specified_data_controls',result
    for flow in result['flows'].values():
        assert flow['equation_residuals']==[0,0,0,0]
        assert flow['chart_guards']
        assert flow['arbitrary_data_claim'] is False
    cell=BRANCHES_2D[name]
    expected_flat=3 if not cell['G'] and cell['coriolis']=='f0' else 2
    for label,expected in [('flat',expected_flat),('linear',2),('quadratic',0)]:
        data=result['initial_data'][label]
        assert data['dimension']==expected
        assert all(z==0 for z in data['verification_residuals'])
        assert data['pde_solution_claim'] is False
    point_map=result['primitive_conservative_map']
    assert point_map['equivalence_residuals']==(0,0,0,0)
    assert point_map['jacobian']==h*h
    assert point_map['row_multiplier'].det()==h*h
    assert result['signed_coriolis_reflection']['equivalence_residuals']==(0,0,0,0)


def test_uniform_rotation_and_planar_slope_solve_the_original_ODEs_with_correct_sign():
    uniform=uniform_rotating_flow('grass_cubic_f_nonzero',velocity=(2,5),time0=3)
    _,U,V,_=uniform['graph']
    assert sp.simplify(sp.diff(U,t)-f*V)==0
    assert sp.simplify(sp.diff(V,t)+f*U)==0
    assert sp.trigsimp(U*U+V*V-29)==0
    assert (U.subs(t,3),V.subs(t,3))==(2,5)
    sloped=constant_slope_flow('slope_source_cubic_f_nonzero',velocity=(2,5),
                              slope=(sp.Rational(2,3),sp.Rational(-1,4)),time0=3)
    _,U,V,Z=sloped['graph']
    assert sp.simplify(sp.diff(U,t)+g*sp.diff(Z,x)-f*V)==0
    assert sp.simplify(sp.diff(V,t)+g*sp.diff(Z,y)+f*U)==0
    assert (sp.simplify(U.subs(t,3)),sp.simplify(V.subs(t,3)))==(2,5)


def test_unknown_initial_bed_slope_keeps_rank_drop_branch():
    k=sp.Symbol('profile_slope',real=True)
    result=initial_data_stabilizer('grass_generic_f0',(2,3,4,1+k*x))
    assert result['status']=='conditional_initial_data_stabilizer'
    assert result['rank_guards'] and result['unresolved_zero_pivot_branches']
    assert result['dimension']==2
    assert initial_data_stabilizer('grass_generic_f0',(2,3,4,1))['dimension']==3


def test_nonpolynomial_data_is_not_certified_from_samples():
    result=initial_data_stabilizer('grass_cubic_f0',(2,3,4,sp.sin(x*y)))
    assert result['status']=='unresolved_functional_splitting'
    assert result['tangency_identities']


def test_point_map_pushforward_contains_both_product_rule_terms():
    momentum_x,momentum_y=sp.symbols('momentum_x momentum_y',real=True)
    image=pushforward_generator((0,x,y,2*h,u,v,2*B))
    assert image==sp.Matrix([0,x,y,2*h,3*momentum_x,3*momentum_y,2*B])
    reflected=signed_coriolis_reflection('zero_transport_f_nonzero')
    assert reflected['status']=='verified_parameter_reflection'
    assert reflected['fixed_parameter_symmetry'] is False


@pytest.mark.parametrize('name,substitutions',[
    ('grass_generic_f0',{m:3}),('grass_generic_f0',{g:sp.I}),
    ('grass_generic_f0',{K:0}),('slope_only_f0',{G:-1}),
    ('grass_cubic_f_nonzero',{f:0}),('grass_cubic_f_nonzero',{f:x}),
    ('slope_only_generic_f_nonzero',{n:2}),
])
def test_invalid_parameter_domains_are_rejected(name,substitutions):
    with pytest.raises(ValueError):
        uniform_rotating_flow(name,substitutions=substitutions)


def test_symbolic_parameter_guards_and_zero_speed_status_are_explicit():
    gravity=sp.Symbol('gravity',real=True)
    result=uniform_rotating_flow('grass_generic_f0',substitutions={g:gravity})
    assert any('gravity' in str(z) for z in result['parameter_guards'])
    assert result['parameter_substitutions']=={g:gravity}
    stopped=uniform_rotating_flow('zero_transport_f0',velocity=(0,0))
    assert stopped['status']=='outside_declared_chart'


@pytest.mark.parametrize('invalid',(sp.I,sp.oo,sp.nan,sp.zoo))
def test_nonreal_or_nonfinite_initial_profiles_are_rejected(invalid):
    with pytest.raises(ValueError,match='finite real'):
        initial_data_stabilizer('grass_cubic_f0',(2,3,4,invalid))


def test_unknown_profile_reality_and_finiteness_are_recorded_as_domain_guards():
    datum=sp.Symbol('unknown_real_datum')
    result=initial_data_stabilizer('grass_cubic_f0',(2,3,4,datum))
    assert sp.Contains(datum,sp.S.Reals,evaluate=False) in result['data_domain_guards']
    assert sp.Q.finite(datum) in result['data_domain_guards']
