"""Ambient distribution equivalence, variable frame changes, and graph collapse."""
import json
from pathlib import Path

import pytest
import sympy as sp

import classification_2d
from models_2d import t,x,y,h,u,v,B
from nonclassical_equivalence import (
    FROZEN_REGISTRY_SHA256,classical_distribution_equivalence,
    evaluate_frozen_registry,special_solution_collapse_control,solution_family_containment)

HERE=Path(__file__).resolve().parents[1]
REGISTRY=json.loads((HERE/'nonclassical_candidates.json').read_text())
CLASSICAL_IDS={'C00','C01','C02','C45','C46','C47','C48','C49','C50'}


def candidate(*,c=0,a=(0,0,0,0),b=(0,0,0,0)):
    return {'id':'explicit_control','c':c,'a':a,'b':b}


@pytest.mark.parametrize('record',REGISTRY['candidates'],ids=lambda row:row['id'])
def test_all_frozen_candidates_use_the_entire_constant_classical_tangent_space(record):
    result=classical_distribution_equivalence(record)
    expected=record['id'] in CLASSICAL_IDS
    assert result['classical_equivalent'] is expected
    assert result['classical_tangent_space_dimension']==(2 if expected else 1)
    assert result['evaluated_classical_rank']==(2 if expected else 1)
    assert result['distribution_rank']==2
    assert result['source_classical_algebra_dimension']==7
    assert result['source_review_gate']['passed'] is True
    assert all(value==0 for row in result['tangency_kernel_residuals'] for value in row)
    assert result['conditional_invariance_claim'] is False
    assert result['point_equivalence_groupoid_claim'] is False


def test_frozen_registry_fingerprint_and_exact_status_counts():
    result=evaluate_frozen_registry()
    assert result['registry_sha256']==FROZEN_REGISTRY_SHA256
    assert result['candidate_count']==64
    assert result['status_counts']=={'verified_classical_distribution':9,
        'no_classical_representative_on_open_ambient_chart':55}
    assert result['frozen_candidate_order']==tuple(row['id'] for row in REGISTRY['candidates'])


def test_point_dependent_frame_change_can_have_a_fixed_classical_representative():
    change=sp.Matrix([[h,t],[0,1/h]])
    result=classical_distribution_equivalence(candidate(c=2,b=(0,0,0,3)),basis_change=change)
    assert result['status']=='verified_classical_distribution'
    assert result['frame_change_determinant']==1
    assert result['frame_change_point_dependent'] is True
    assert result['fixed_subalgebra_basis'][0]==sp.Matrix([0,0,1,0,0,0,0])
    assert result['fixed_subalgebra_basis'][1]==sp.Matrix([1,2,0,0,0,0,3])
    assert result['frame_to_fixed_classical_basis']==change.inv()
    assert result['classical_frame_reconstruction_residual']==sp.zeros(7,2)
    assert result['fixed_subalgebra_bracket']==sp.zeros(7,1)


def test_point_dependent_frame_change_does_not_remove_ambient_obstruction():
    result=classical_distribution_equivalence(candidate(a=(0,1,0,0)),
                                              basis_change=sp.Matrix([[h,t],[0,1/h]]))
    assert result['status']=='no_classical_representative_on_open_ambient_chart'
    assert result['classical_tangent_basis']==(sp.Matrix([0,0,1,0,0,0,0]),)
    assert result['fixed_subalgebra_basis'] is None


def test_special_uniform_solution_collapses_without_ambient_equivalence():
    result=special_solution_collapse_control()
    assert result['ambient_result']['classical_equivalent'] is False
    assert result['graph']==(2,0,1,0)
    assert result['original_PDE_residuals']==(0,0,0,0)
    assert result['restricted_frame_difference']==sp.zeros(7,2)
    assert result['speed_squared']==1
    assert result['special_solution_only'] is True
    assert result['conditional_invariance_claim'] is False


@pytest.mark.parametrize('identifier',('C28','C31','C34','C37'))
def test_four_shift_families_have_classical_solution_containment_without_distribution_equality(identifier):
    record=next(row for row in REGISTRY['candidates'] if row['id']==identifier)
    result=classical_distribution_equivalence(record)
    assert result['status']=='no_classical_representative_on_open_ambient_chart'
    containment=result['solution_family_containment']
    assert containment['status']=='verified_classical_invariant_solution_family'
    assert containment['classical_solution_family_containment'] is True
    assert containment['original_PDE_residuals']==(0,0,0,0)
    assert containment['candidate_characteristic_residuals']==((0,0,0,0),(0,0,0,0))
    assert containment['classical_characteristic_residuals']==((0,0,0,0),(0,0,0,0))
    assert containment['fixed_classical_bracket']==sp.zeros(7,1)
    assert containment['combined_projection_rank']==3
    assert containment['distribution_equality_on_these_graphs'] is False
    assert containment['full_local_candidate_solution_family_on_stated_chart'] is True
    assert containment['novel_solution_family_claim'] is False


def test_velocity_shift_formula_extension_does_not_repair_singular_jet_criterion():
    result=solution_family_containment(candidate(b=(0,1,0,0)))
    assert 'does not repair' in result['singular_jet_scope']
    assert any('regular conditional-invariance chart' in guard for guard in result['guards'])
    assert result['conditional_invariance_claim'] is False


def test_depth_shift_positivity_is_local_and_does_not_exclude_negative_intercepts():
    result=solution_family_containment(candidate(b=(1,0,0,0)))
    H0,U0,V0,B0=result['parameters']
    assert H0.is_positive is None
    assert result['graph'][0].subs({H0:-1,U0:1,t:2,x:0})==1
    assert any('H0+beta*t-beta*x/U0>0' in guard for guard in result['guards'])


def test_unknown_candidate_parameter_preserves_both_equivalence_strata():
    alpha=sp.Symbol('alpha',real=True)
    result=classical_distribution_equivalence(candidate(a=(0,alpha,0,0)))
    assert result['status']=='conditional_parameter_stratum'
    assert result['classical_equivalent'] is None
    assert result['classical_condition']==sp.Eq(alpha,0)
    assert {row['classical_tangent_space_dimension'] for row in result['parameter_strata']}=={1,2}
    assert classical_distribution_equivalence(candidate(a=(0,0,0,0)))['classical_equivalent'] is True
    assert classical_distribution_equivalence(candidate(a=(0,1,0,0)))['classical_equivalent'] is False


def test_unreviewed_source_algebra_never_certifies_ambient_absence(monkeypatch):
    monkeypatch.setattr(classification_2d,'review_gate',lambda:{'passed':False,'reason':'control'})
    result=classical_distribution_equivalence(candidate(a=(1,0,0,0)))
    assert result['status']=='unresolved_classical_algebra_gate'
    assert result['classical_equivalent'] is None


@pytest.mark.parametrize('record',[
    candidate(c=t),candidate(a=(sp.I,0,0,0)),candidate(b=(0,0,sp.oo,0)),
    candidate(a=(0,0,0)),candidate(c=sp.Float('0.5')),
])
def test_nonconstant_nonreal_nonfinite_inexact_or_malformed_candidate_is_rejected(record):
    with pytest.raises(ValueError):
        classical_distribution_equivalence(record)


def test_singular_frame_change_is_rejected_and_regular_subchart_is_explicit():
    with pytest.raises(ValueError,match='invertible'):
        classical_distribution_equivalence(candidate(),basis_change=sp.Matrix([[1,1],[1,1]]))
    result=classical_distribution_equivalence(candidate(),basis_change=sp.diag(u,1))
    assert sp.Ne(u,0,evaluate=False) in result['frame_chart_guards']
    assert result['classical_equivalent'] is True
