"""Independent first-jet, differential-constraint, chart and graph controls."""
import json
from pathlib import Path

import pytest
import sympy as sp

import nonclassical as nc
from main import JetSpace,point_action,prolongation_coefficients
from models_2d import branch_model_2d,t,x,y,h,u,v,B,g,K

HERE=Path(__file__).resolve().parents[1]
REGISTRY=json.loads((HERE/'nonclassical_candidates.json').read_text(encoding='utf-8'))['candidates']


def candidate(profile,c):
    return next(row for row in REGISTRY if row['profile']==profile and row['c']==c)


def test_conditional_matrix_matches_original_pde_prolongation_without_solver_oracle():
    c,a,b=1,(1,-2,3,4),(2,1,-1,5)
    system=nc.conditional_system(c,a,b)
    model=branch_model_2d('grass_cubic_f0')
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    phi=tuple(ai*field+bi for ai,bi,field in zip(a,b,J.u))
    prolonged=prolongation_coefficients(J,(1,c,0),phi,1)
    substitution={}
    for index,field in enumerate(J.u):
        substitution[J.jet(index,(0,1,0))]=nc.P[index]
        substitution[J.jet(index,(0,0,1))]=0
        substitution[J.jet(index,(1,0,0))]=phi[index]-c*nc.P[index]
    actual=sp.Matrix([point_action(J,E,(1,c,0),phi,1,coefficients=prolonged)
                      .xreplace(substitution) for E in model['equations']])
    assert all(sp.expand(z)==0 for z in actual-system['prolonged_PDE_on_Q'])
    assert tuple(system['involutivity_residual'])==(0,)*7
    assert abs(system['projection_minor_t_y'])==1


def test_differentiated_constraints_retain_the_obstruction_instead_of_assuming_it_zero():
    system=nc.conditional_system(1,(1,0,0,0),(0,0,0,0))
    assert any(z!=0 for z in system['conditional_residual_mod_joint'])
    assert all(z==0 for z in system['differential_consequences']['compatibility_identity_remainder'])
    matrix=system['leading_matrix']
    phi=system['phi']
    Dx=lambda e:sum(sp.diff(e,field)*p for field,p in zip(nc.FIELDS,nc.P))
    expected=(matrix*nc.R+sp.Matrix([Dx(e) for e in matrix*nc.P+phi])).applyfunc(sp.expand)
    assert all(sp.expand(z)==0 for z in expected-system['differential_consequences']['D_x_E_on_Q_and_DQ'])


def test_characteristic_factorization_includes_zero_longitudinal_nonzero_transverse_speed():
    system=nc.conditional_system(0,(0,)*4,(0,)*4)
    expected=-g*K*u*u*(3*u*u+v*v)
    assert sp.expand(system['determinant']-expected)==0
    assert system['determinant'].subs({u:0,v:1})==0
    assert system['leading_matrix'].subs({u:0,v:1}).rank()==2


@pytest.mark.parametrize('sign',(-1,1))
def test_depth_shift_has_empty_singular_joint_stratum_and_a_reconstructed_solution(sign):
    row=candidate(f'b_h_{sign}',0)
    result=nc.analyze_candidate(row,require_gate=False)
    assert result['conditional_status']=='verified_conditional_on_declared_chart'
    assert result['singular_status']=='no_compatible_jets'
    assert result['singular_analysis']['contradiction']==K*v*v*sign
    assert result['global_chart_admitted'] is True
    assert all(z==0 for z in result['regular_chart']['Frobenius_commutator'])
    family=result['compatible_families']['explicit_families'][0]
    assert family['name']=='h_shift'
    assert family['PDE_residuals']==family['Q_residuals']==(0,)*4


@pytest.mark.parametrize('sign',(-1,1))
def test_velocity_shift_requires_regular_subchart_despite_exact_acceleration_family(sign):
    result=nc.analyze_candidate(candidate(f'b_u_{sign}',0),require_gate=False)
    assert result['conditional_status']=='verified_conditional_on_regular_subchart'
    assert result['global_chart_admitted'] is False
    assert result['additional_conditional_guards']==('u!=0',)
    witness=result['singular_analysis']['witness']
    assert tuple(witness['joint_residual'])==(0,)*4
    assert witness['conditional_residual'][0]==sign
    assert any(z!=0 for z in witness['conditional_residual'])
    family=result['compatible_families']['explicit_families'][0]
    assert family['PDE_residuals']==family['Q_residuals']==(0,)*4


def test_a_compatible_special_solution_does_not_certify_a_failed_distribution():
    result=nc.analyze_candidate(candidate('a_u_1',0),require_gate=False)
    assert result['conditional_status']=='failed_conditional_criterion'
    assert not result['conditional_admitted']
    # h=2,u=0,v=1,B=0 is a solution and is invariant under dt+u du,
    # yet the candidate fails on other compatible first jets.
    at={h:2,u:0,v:1,B:0}
    assert tuple(result['joint_system']['phi'].subs(at))==(0,)*4
    assert result['invariant_graph']['status']=='verified_graph_pullback'
    witness=result['regular_chart']['rejection_witness']
    assert tuple(witness['joint_residual'])==(0,)*4
    assert any(z!=0 for z in witness['conditional_residual'])
    assert result['regular_chart']['positive_parameter_obstruction']


@pytest.mark.parametrize('c',(-1,0,1))
def test_classical_controls_retain_singular_solution_branches(c):
    result=nc.analyze_candidate(candidate('zero',c),require_gate=False)
    assert result['conditional_status']=='verified_conditional_on_declared_chart'
    assert result['singular_status']=='all_compatible_jets_verified'
    families=result['compatible_families']['explicit_families']
    singular=next(row for row in families if row['name'].startswith('singular_'))
    assert singular['status']=='verified_constructed_solution'
    assert singular['PDE_residuals']==singular['Q_residuals']==(0,)*4
    assert result['singular_analysis']['implicit_DAE']['discarded'] is False


def test_bed_drift_first_integrals_reconstruct_all_regular_equations():
    c=sp.Rational(1)
    q=sp.Rational(-1)
    system=nc.conditional_system(c,(0,)*4,(0,0,0,q))
    z=sp.Symbol('z',real=True)
    first=(h*(u-c),(u-c)**2/2+g*(h+B),K*(u*u+v*v)*u-c*B+q*z)
    derivative=lambda e:sp.diff(e,z)+sum(sp.diff(e,field)*p for field,p in zip(nc.FIELDS,nc.P))
    assert sp.expand(derivative(first[0])-system['joint_first_order_equations'][0])==0
    assert sp.expand(derivative(first[1])-system['joint_first_order_equations'][1])==0
    assert sp.expand(derivative(first[2])-system['joint_first_order_equations'][3])==0


def test_graph_reconstruction_and_time_split_with_rational_exponents_are_exact():
    graph=nc.invariant_graph(1,(sp.Rational(1,2),-1,0,2),(1,0,2,1))
    assert graph['status']=='verified_graph_pullback'
    assert graph['profile_or_characteristic_divisions']==()
    assert graph['field_jacobian']==sp.exp(sp.Rational(3,2)*t)
    assert graph['conditional_invariance_inferred_from_graph'] is False
    assert all(z==0 for z in graph['time_reconstruction_residuals'])


@pytest.mark.parametrize('bad',(sp.I,sp.oo,sp.nan,0.2,t,True))
def test_nonrational_nonfinite_coordinate_or_boolean_coefficients_are_rejected(bad):
    with pytest.raises(ValueError):
        nc.analyze_candidate({'id':'invalid','c':bad,'a':[0]*4,'b':[0]*4},require_gate=False)


def test_stage2_gate_cannot_be_skipped_by_default(monkeypatch):
    import gatekeeper
    monkeypatch.setattr(gatekeeper,'check_gate',lambda stage:{'passed':False,'reason':'test missing gate'})
    with pytest.raises(ValueError,match='Stage 2 gate'):
        nc.analyze_candidate(candidate('zero',0))


def test_full_frozen_registry_has_only_certified_or_parameter_uniform_rejected_statuses():
    results=[nc.analyze_candidate(row,require_gate=False) for row in REGISTRY]
    assert len(results)==64
    accepted={result['candidate_id'] for result in results if result['conditional_admitted']}
    expected={f'C{number:02}' for number in (0,1,2,28,31,34,37,45,46,47,48,49,50)}
    assert accepted==expected
    assert sum(result['global_chart_admitted'] for result in results)==11
    assert all(result['conditional_status'] in ('verified_conditional_on_declared_chart',
               'verified_conditional_on_regular_subchart','failed_conditional_criterion') for result in results)
    for result in results:
        if not result['conditional_admitted']:
            assert result['regular_chart']['positive_parameter_obstruction']
            assert any(z!=0 for z in result['regular_chart']['rejection_witness']['conditional_residual'])
        assert result['invariant_graph']['status']=='verified_graph_pullback'
        json.dumps(nc.serialize_result(result))
