"""Exact graph controls independent of the conditional criterion implementation."""
import math
from pathlib import Path
import sys

import pytest
import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ml_adapter import (T,RHO,F,P,g,K,_time_coefficients,graph_certificate,
                        build_certificate,encode,decode,encode_certificate)


def candidate(a=(0,0,0,0),b=(0,0,0,0),c=0):
    return {'id':'test','a':list(a),'b':list(b),'c':c}


@pytest.mark.parametrize('case',[
    candidate(c=-1),candidate(b=(1,0,0,0)),candidate(b=(0,1,0,0)),
    candidate(a=(2,1,1,2),b=(0,0,0,1)),candidate(a=(-2,-1,-1,-2)),
])
def test_graph_input_and_reconstruction(case):
    result=graph_certificate(case)
    assert result['all_identities_zero']
    assert result['field_jacobian']==RHO**sum(case['a'])
    original=(2.5,1.2,-0.4,0.8)
    full=decode(case,0.2,original)
    encoded=encode(case,0.2,1.0,3.0,full)
    assert encoded['valid_domain']
    assert encoded['profiles']==pytest.approx(original)
    assert encoded['z']==pytest.approx(1.0-case['c']*0.2)


def test_signed_exponent_grouping_preserves_multiplicative_relations():
    assert _time_coefficients((RHO**2+1)/RHO-RHO)==((-1,0,sp.S.One),)
    assert _time_coefficients(T*(RHO+1)-T*RHO)==((0,1,sp.S.One),)


def test_real_exponents_not_silently_accepted_as_frozen_integers():
    with pytest.raises(ValueError):
        _time_coefficients(RHO**sp.Rational(1,2))


def test_correct_graph_does_not_admit_failed_conditional_candidate():
    export=build_certificate(candidate(a=(1,0,0,0)),conditional_admitted=False,
                             conditional_status='failed_conditional_criterion',
                             equivalence_status='not_classical',conditional_evidence='test')
    assert export['certificate']['PDE_pullback_verified']
    assert export['use']=='diagnostic_graph_only'
    assert export['conditional_admitted'] is False
    assert export['training_performed'] is False
    with pytest.raises(ValueError):
        encode_certificate(export,0,0,0,(1,1,1,0))


def test_contradictory_admission_is_rejected():
    with pytest.raises(ValueError):
        build_certificate(candidate(),conditional_admitted=True,
                          conditional_status='failed_conditional_criterion',
                          equivalence_status='classical',conditional_evidence='test')


def test_restricted_mask_keeps_zero_velocity_characteristic_out():
    case=candidate(b=(0,1,0,0))
    export=build_certificate(case,conditional_admitted=True,
                             conditional_status='verified_conditional_on_regular_subchart',
                             equivalence_status='not_classical',conditional_evidence='test')
    assert 'u(t,z)!=0' in export['valid_domain_mask']
    assert export['global_chart_admitted'] is False
    assert encode(case,0,0,0,(1,0,1,0))['valid_domain']
    assert not encode(case,0,0,0,(1,0,1,0),regular_u_chart=True)['valid_domain']
    assert not encode_certificate(export,0,0,0,(1,0,1,0))['valid_domain']


@pytest.mark.parametrize('fields,gvalue,kvalue',[
    ((0,1,0,0),1,1),((1,0,0,0),1,1),((1,1,0,0),0,1),
    ((1,1,0,0),1,0),((1,math.nan,0,0),1,1),
])
def test_domain_rejects_invalid_inputs(fields,gvalue,kvalue):
    assert not encode(candidate(),0,0,0,fields,gvalue,kvalue)['valid_domain']


def test_depth_shift_constructed_solution_has_zero_original_pde_pullback():
    b=1
    result=graph_certificate(candidate(b=(b,0,0,0)))
    substitutions={F[0]:2-sp.Symbol('z')/2,F[1]:2,F[2]:1,F[3]:sp.Symbol('z')/2,
                   P[0]:-sp.Rational(1,2),P[1]:0,P[2]:0,P[3]:sp.Rational(1,2)}
    assert all(sp.expand(e.subs(substitutions))==0 for e in result['residual'])


def test_velocity_shift_constructed_solution_and_wrong_slope_negative_control():
    result=graph_certificate(candidate(b=(0,1,0,0)))
    substitutions={F[0]:2,F[1]:1,F[2]:1,F[3]:0,P[0]:0,P[1]:0,P[2]:0,P[3]:-1/g}
    assert all(sp.expand(e.subs(substitutions))==0 for e in result['residual'])
    substitutions[P[3]]=1/g
    assert sp.expand(result['residual'][1].subs(substitutions))==2
