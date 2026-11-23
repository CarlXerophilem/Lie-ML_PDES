"""Actual 2D brackets, constant spans, local invariant charts, and nonclaims."""
import pytest
import sympy as sp

from models_2d import BRANCHES_2D, t, x, y, h, u, v, B, n
from algebra_2d import (representative_subalgebras, constant_coordinates,
                        adjoint_action, bracket)

COORDINATES=(t,x,y,h,u,v,B)


@pytest.mark.parametrize('name',tuple(BRANCHES_2D))
def test_all_cells_have_verified_representatives_without_optimality_claim(name):
    report=representative_subalgebras(name)
    assert report['status']=='verified_representatives'
    assert report['optimality_status']=='not_proved'
    assert report['maximal_point_algebra_claim'] is False
    assert report['structure']['status']=='verified_bracket_closure'
    for family in ('line_representatives','rank_two_representatives'):
        for record in report[family]:
            assert record['status']=='verified_subalgebra'
            assert all(value==0 for row in record['invariant_residuals'] for value in row)
            assert all(value==0 for row in record['span_residuals'] for value in row)
            assert record['invariant_chart']['verified']


def test_plane_wave_contains_transverse_velocity_and_has_one_base_invariant():
    report=representative_subalgebras('slope_source_generic_f_nonzero')
    record=next(r for r in report['rank_two_representatives'] if r['name']=='plane_wave')
    c=report['parameters']['c']
    assert record['projection_rank']==2
    assert record['invariants']==(x-c*t,h,u,v,B)
    assert record['invariant_chart']['base_invariants']==(x-c*t,)
    assert record['closure_coefficients']=={'0,1':(0,0)}


def test_bed_translation_is_a_valid_line_but_has_no_invariant_graph():
    record=next(r for r in representative_subalgebras('grass_generic_f0')['line_representatives']
                if r['name']=='bed_translation')
    assert record['projection_rank']==0
    assert record['graph_admissible'] is False
    assert record['graph_obstruction']=='Q_B=1'


def test_rotation_uses_actual_bracket_sign_and_rotates_both_spaces():
    report=representative_subalgebras('grass_generic_f0')
    fields=report['named_generators']
    assert bracket(fields['R'],fields['X'])==-fields['Y']
    assert bracket(fields['R'],fields['Y'])==fields['X']
    angle=sp.Symbol('angle',real=True)
    actual=adjoint_action(report,fields['R'],fields['X'],angle)
    expected=sp.cos(angle)*fields['X']-sp.sin(angle)*fields['Y']
    assert all(sp.simplify(a-b)==0 for a,b in zip(actual,expected))
    assert fields['R'][4:6]==[-v,u]


def test_span_uses_constant_coefficients_and_rejects_pointwise_multipliers():
    X=sp.Matrix([0,1,0,0,0,0,0])
    with pytest.raises(ValueError,match='constant span'):
        constant_coordinates(x*X,(X,))


def test_catalogue_accepts_mixed_reordered_basis_and_rejects_incomplete_one():
    original=representative_subalgebras('slope_attachment_cubic_f_nonzero')
    basis=original['basis']
    mixed=(basis[-1]+basis[0],*basis[1:-1],basis[0])
    report=representative_subalgebras('slope_attachment_cubic_f_nonzero',mixed)
    assert report['status']=='verified_representatives'
    assert report['basis']==tuple(sp.Matrix(q) for q in mixed)
    with pytest.raises(ValueError,match='same constant span'):
        representative_subalgebras('slope_attachment_cubic_f_nonzero',basis[:-1])


@pytest.mark.parametrize('exponent',(0,1,2,3,4))
def test_slope_scaling_rotation_chart_keeps_every_resonant_exponent(exponent):
    report=representative_subalgebras('slope_only_f0')
    record=next(r for r in report['rank_two_representatives'] if r['name']=='rotation_scaling_d')
    a,b=record['scaling_weights']
    assert (a.subs(n,exponent),b.subs(n,exponent))==(exponent-2,exponent-1)
    assert record['invariant_chart']['base_invariants']==(t**(n-1)*(x*x+y*y)**((2-n)/2),)
    point={n:exponent,t:2,x:3,y:1,h:5,u:2,v:1,B:7}
    assert any(sp.simplify(w.subs(point))!=0 for w in record['projection_rank_witnesses'])
    assert any(sp.simplify(w.subs(point))!=0 for w in record['invariant_chart']['rank_witnesses'])
    assert all(not sp.denom(sp.together(I)).has(n) for I in record['invariants'])


def test_fixed_rotation_forbids_unadmitted_dilation():
    a=representative_subalgebras('slope_source_cubic_f_nonzero')
    b=representative_subalgebras('slope_only_n2_f_nonzero')
    assert not any(r['name'].startswith('scaling_') for r in a['line_representatives'])
    assert any(r['name'].startswith('scaling_') for r in b['line_representatives'])


def test_bracket_closure_of_rotation_with_one_translation_is_not_falsified():
    report=representative_subalgebras('slope_attachment_generic_f0')
    R,X=report['named_generators']['R'],report['named_generators']['X']
    with pytest.raises(ValueError,match='constant span'):
        constant_coordinates(bracket(R,X),(R,X))


def test_name_prefix_is_supported_and_unsplit_rotating_slope_rejected():
    assert representative_subalgebras('2d__grass_cubic_f0')['status']=='verified_representatives'
    with pytest.raises(ValueError,match='refined'):
        representative_subalgebras('slope_only_f_nonzero')


def test_real_algebra_rejects_complex_basis_and_complex_adjoint_parameter():
    report=representative_subalgebras('grass_generic_f0')
    with pytest.raises(ValueError,match='finite real'):
        representative_subalgebras('grass_generic_f0',(sp.I*report['basis'][0],*report['basis'][1:]))
    with pytest.raises(ValueError,match='finite real'):
        representative_subalgebras('grass_generic_f0',(sp.oo*report['basis'][0],*report['basis'][1:]))
    with pytest.raises(ValueError,match='finite real'):
        adjoint_action(report,report['named_generators']['R'],report['named_generators']['X'],sp.I)
    with pytest.raises(ValueError,match='finite real'):
        adjoint_action(report,report['named_generators']['R'],report['named_generators']['X'],t)
