import sympy as sp
import pytest
import json
from run_all import certificates
from sve_lab.jets import *
from sve_lab.symbolic import (obstruction, direct_pullback, reduced_residual,
                             physical_audit, normal_form, first_integral,
                             profile_total, common_scaling_certificate,
                             principal_symbol_obstruction,
                             conservation_pullback_certificate,
                             z, f, P)

def test_common_scaling_reduction_certificate():
    cert=common_scaling_certificate()
    assert sp.simplify(cert['characteristic']['expression']-(u-t*p-s*q))==0
    expected={
        '()':u-t*p-s*q,
        '(t)':-t*a-s*b,
        '(s)':-t*b-s*c,
        '(t,t)':-a-t*r-s*w,
        '(t,s)':-b-t*w-s*x,
        '(s,s)':-c-t*x-s*y,
    }
    assert set(cert['differential_consequences'])==set(expected)
    for index,expression in expected.items():
        assert sp.simplify(cert['differential_consequences'][index]-expression)==0
    assert cert['differential_consequence_order']==2
    assert cert['orbit_ranks']=={'base':1,'total_space':1}
    assert cert['transversality']['status']=='verified'
    assert cert['transversality']['base_rank']==cert['transversality']['total_space_rank']==1
    assert sp.simplify(cert['coordinates']['old_to_new_jacobian']-t**-2)==0
    assert sp.simplify(cert['coordinates']['new_to_old_jacobian']-t**2)==0
    assert sp.simplify(cert['coordinates']['full_old_to_new_jacobian']-t**-3)==0
    assert all(sp.simplify(value)==0 for value in cert['checks'].values())

@pytest.mark.parametrize('physical',[False,True])
def test_scalar_conservation_pullback_certificate(physical):
    cert=conservation_pullback_certificate(m,physical)
    density=q*a-g*c/q**2
    flux=-g*m*kappa*p**(m-1)*b/q
    if physical:
        flux-=p*density/q
    assert sp.simplify(cert['density']-density)==0
    assert sp.simplify(cert['spatial_flux']-flux)==0
    assert cert['source']==0
    assert cert['constraints']['status']=='not_declared_for_scalar_benchmark'
    assert cert['data']['status']=='not_declared'
    assert sp.simplify(cert['coordinate_map']['jacobian_old_from_new']-t)==0
    assert sp.simplify(cert['transformed_density']-t*density)==0
    assert sp.simplify(cert['transformed_spatial_flux']-(flux-s*density/t))==0
    assert sp.simplify(cert['boundary_normal_flux_pullback']
                       -cert['transformed_spatial_flux'])==0
    assert sp.simplify(cert['checks']['divergence_remainder'])==0
    assert cert['scope']['full_bed_field_system']==False
    assert cert['scope']['noether_or_variational_claim']==False

def test_machine_certificate_exports_reduction_and_conservation(tmp_path):
    certificates(tmp_path)
    payload=json.loads((tmp_path/'symbolic_certificates.json').read_text())
    reduction=payload['common_scaling_reduction']
    assert reduction['status']=='verified'
    assert reduction['characteristic']['expression']=='-p*t - q*s + u'
    assert reduction['orbit_ranks']=={'base':1,'total_space':1}
    assert len(payload['conservation_pullbacks'])==2
    for pullback in payload['conservation_pullbacks']:
        assert pullback['status']=='verified_for_declared_scalar_balance_law'
        assert pullback['checks']['divergence_remainder']=='0'
        assert pullback['constraints']['status']=='not_declared_for_scalar_benchmark'
    for obstruction_cert in payload['certificates']:
        assert obstruction_cert['selected_coefficient_alias']=='const_1'
        assert obstruction_cert['selected_coefficient_definition']=='const_1 := 3*g*kappa'
        assert obstruction_cert['principal_symbol_crosscheck']['remainder']=='0'
        assert obstruction_cert['principal_symbol_crosscheck']['witness']=='3*g*kappa'

@pytest.mark.parametrize('physical',[False,True])
def test_unrestricted_obstruction(physical):
    cert=obstruction(physical)
    assert sp.simplify(cert['witness']-3*g*kappa)==0
    # Off-shell identity supplies the perturbation forcing with its sign.
    E=model_residual(m,physical)
    T=g*m*kappa*total(p**(m-1)*b/q,1)
    assert sp.simplify(act(E,t,-2*s,0)+E-(m-3)*T)==0

@pytest.mark.parametrize('physical',[False,True])
def test_common_scaling_all_exponents(physical):
    E=model_residual(m,physical)
    assert sp.simplify(act(E,t,s,u)+2*E)==0

@pytest.mark.parametrize('physical',[False,True])
@pytest.mark.parametrize('exponent',[1,2,3,4])
def test_ode_against_independent_chain_rule(physical,exponent):
    assert sp.simplify(direct_pullback(exponent,physical)
                       -reduced_residual(exponent,physical))==0

def test_corrected_bed_compatibility():
    compatibility,E=physical_audit()
    assert sp.simplify(compatibility-E)==0
    assert sp.simplify(E-model_residual(m,False)+total(p*(q*a-g*c/q**2)/q,1))==0

@pytest.mark.parametrize('physical',[False,True])
def test_leading_coefficient_not_dropped(physical):
    _,leading=normal_form(m,physical)
    V=f-z*P
    expected=(-z**3*P+g*z/P**2+g*m*kappa*z*V**(m-1)/P)
    if physical:expected=f*(g/P**3-z**2)+g*m*kappa*z*V**(m-1)/P
    assert sp.simplify(leading-expected)==0

@pytest.mark.parametrize('physical',[False,True])
def test_first_integral(physical):
    velocity=sp.symbols('velocity',positive=True)
    difference=profile_total(first_integral(m,physical))-reduced_residual(m,physical)
    # Explicit real-power branch; do not force power identities globally.
    assert sp.simplify(difference.subs(f,velocity+z*P))==0

def test_printed_obstruction_against_principal_symbol_derivation():
    tau=sp.Function('tau')(t,s,u);xi=sp.Function('xi')(t,s,u);eta=sp.Function('eta')(t,s,u)
    A=g/q**2+3*g*kappa*p**2/q
    eta_s=total(eta,1)-p*total(tau,1)-q*total(xi,1)
    eta_t=total(eta,0)-p*total(tau,0)-q*total(xi,0)
    coefficient=(A/q-sp.diff(A,q))*eta_s-sp.diff(A,p)*eta_t
    coefficient+=2*A*(total(xi,1)-total(tau,0))+3*g*kappa*p**2/q
    # This expression follows from the principal symbol q*r-A*x,
    # independently of the recursive full prolongation used by obstruction().
    assert sp.simplify(q**3*coefficient-obstruction(False)['highest_polynomial'])==0

def test_corrected_obstruction_against_independent_principal_symbol_derivation():
    printed=principal_symbol_obstruction(False)
    corrected=principal_symbol_obstruction(True)
    tau=sp.Function('tau')(t,s,u);xi=sp.Function('xi')(t,s,u)
    transport_correction=(
        p*(3*g*kappa*p**2*q-2*g)*(q*sp.diff(tau,u)+sp.diff(tau,s))
        +2*p*q**3*(p*sp.diff(xi,u)+sp.diff(xi,t)))
    assert sp.simplify(corrected['highest_polynomial']
                       -printed['highest_polynomial']-transport_correction)==0
    assert sp.simplify(corrected['highest_polynomial']
                       -obstruction(True)['highest_polynomial'])==0
    assert sp.simplify(corrected['witness']-3*g*kappa)==0
