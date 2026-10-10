import sympy as sp
import pytest
from sve_lab.jets import *
from sve_lab.symbolic import (obstruction, direct_pullback, reduced_residual,
                             physical_audit, normal_form, first_integral,
                             profile_total, z, f, P)

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
