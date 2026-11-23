"""Standalone, source-audited scalar SVE reproduction.

Edit the defaults below, or override them with command-line options. The
printed scalar equation and the advectively corrected model remain distinct.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import sys
import time
from contextlib import redirect_stdout
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path

# Set BLAS thread limits before importing NumPy/SciPy.
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_name, '1')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import BarycentricInterpolator
import sympy as sp

# Edit settings here; command-line flags take precedence.
DEFAULT_RTOL = 1e-9
DEFAULT_ATOL = 1e-11
DEFAULT_TRACE = 'full'
G = 1.0
KAPPA = 1 / 30
CASES = ('3.4', '3.5', '3.6', '3.8', '3.9')
EXPONENTS = (1, 1.5, 2, 3, 4)
# Each value is (ODE interval, initial (F, F', F'') jet).
NUMERICAL_CASE_SETTINGS = {
    '3.4': ((1.0, 1.4), (2.0, 0.5, 0.1)),
    '3.5': ((1.0, 1.1), (2.0, 0.5, 0.1)),
    '3.6': ((1.0, 1.1), (2.0, 0.5, 0.1)),
    '3.8': ((0.0, 0.4), (0.0, 1.0, 0.1)),
    '3.9': ((1.0, 1.1), (2.0, 0.5, 0.1)),
}


# ========================================================================
# Core
# ========================================================================
t, s, u = sp.symbols('t s u', real=True)

p, q = sp.symbols('p q', positive=True)

a, b, c, r, w, x, y = sp.symbols('a b c r w x y', real=True)

JETS = {(0,0):u,(1,0):p,(0,1):q,(2,0):a,(1,1):b,(0,2):c,
        (3,0):r,(2,1):w,(1,2):x,(0,3):y}

g, kappa = sp.symbols('g kappa', positive=True)

m = sp.symbols('m', real=True)

z = sp.symbols('z', positive=True)

F, P, C, H = sp.symbols('F P C H', real=True)

def total(expr, axis):
    expr = sp.sympify(expr)
    if axis not in (0, 1):
        raise ValueError('axis must be 0 or 1')
    result = sp.diff(expr, (t,s)[axis])
    for ij, jet in JETS.items():
        d = sp.diff(expr, jet)
        if d == 0:
            continue
        nxt = (ij[0]+int(axis==0), ij[1]+int(axis==1))
        if nxt not in JETS:
            raise ValueError('total derivative exceeds available jet order 3')
        result += JETS[nxt]*d
    return sp.expand(result)

def prolongation(tau, xi, eta):
    coeff = {(0,0):sp.sympify(eta)}
    dtau = [total(tau,i) for i in (0,1)]
    dxi = [total(xi,i) for i in (0,1)]
    for n in range(1,4):
        for i in range(n,-1,-1):
            j = n-i
            axis = 0 if i else 1
            prev = (i-1,j) if i else (i,j-1)
            coeff[(i,j)] = sp.expand(total(coeff[prev],axis)
                -JETS[(prev[0]+1,prev[1])]*dtau[axis]
                -JETS[(prev[0],prev[1]+1)]*dxi[axis])
    return coeff

def act(expr, tau, xi, eta):
    coeff = prolongation(tau,xi,eta)
    result = tau*sp.diff(expr,t)+xi*sp.diff(expr,s)
    result += sum(coeff[ij]*sp.diff(expr,jet) for ij,jet in JETS.items())
    return sp.expand(result)

def master(exponent=m):
    exponent = sp.sympify(exponent)
    A = q*a-g*c/q**2
    flux = exponent*kappa*p**(exponent-1)*b/q
    return total(A,0)-g*total(flux,1)

def profile_total(expr):
    return sp.diff(expr,z)+P*sp.diff(expr,F)+C*sp.diff(expr,P)+H*sp.diff(expr,C)

def jsonable(value):
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, dict):
        return {str(k):jsonable(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)):
        return [jsonable(v) for v in value]
    return value


# ========================================================================
# Models
# ========================================================================
def build_model_report():
    k = kappa
    bs,bt=sp.symbols('b_s b_t',real=True)
    A=q*a-g*c/q**2
    transport=m*k*p**(m-1)*b/q
    # Eulerian derivatives at fixed spatial position, expressed on material jets.
    h_T=-b/q**2+p*c/q**3
    h_x=-c/q**3
    u_T=a-p*b/q
    u_x=b/q
    mass=sp.expand(h_T+p*h_x+u_x/q)
    momentum=sp.expand(u_T+p*u_x+g*(h_x+bs/q))
    printed_b_s=-A/g
    printed_b_t=-transport
    physical_b_t=-p*A/(g*q)-transport
    printed_closure=sp.expand(total(printed_b_s,0)-total(printed_b_t,1))
    physical_closure=sp.expand(total(printed_b_s,0)-total(physical_b_t,1))
    E=master()
    Ephys=sp.expand(E-total(p*A/q,1))
    checks={
        'mass_pullback_zero':mass==0,
        'momentum_pullback_zero':sp.expand(momentum-(a-g*c/q**3+g*bs/q))==0,
        'printed_compatibility_zero':sp.expand(printed_closure+E/g)==0,
        'physical_compatibility_zero':sp.expand(physical_closure+Ephys/g)==0,
    }
    steps=[
        ('Coordinate definitions','x=phi(t,s), h=1/phi_s, u=phi_t, b(t,s)=B(t,phi(t,s))'),
        ('Eulerian derivative operators','D_x=(1/q)D_s; D_T=D_t-(p/q)D_s'),
        ('Continuity pullback',mass),
        ('Momentum pullback',momentum),
        ('Exner pullback',bt-p*bs/q+transport),
        ('Printed Exner expression',bt+transport),
        ('Missing term under the pullback interpretation',-p*bs/q),
        ('Define A',A),
        ('Printed b_s',printed_b_s),
        ('Printed b_t',printed_b_t),
        ('Compatibility b_st-b_ts',printed_closure),
        ('Printed master equation E=0',E),
        ('Advectively corrected compatibility equation',Ephys),
    ]
    return jsonable({
        'model':'printed_scalar',
        'scope':'Local smooth material chart q>0; noninteger powers on p>0; g,kappa>0; m>=1.',
        'master':E,'master_latex':sp.latex(E),'beta':'m*kappa',
        'checks':checks,'steps':[{'label':a,'expression':b} for a,b in steps],
        'physical_equals_printed':sp.expand(E-Ephys)==0,
        'discrepancies':[{
            'id':'D-MODEL-06','source':'p.2 equation (6)',
            'printed':'b_t + beta*phi_t**(m-1)*phi_ts/phi_s = 0',
            'derived':'b_t - (phi_t/phi_s)*b_s + beta*phi_t**(m-1)*phi_ts/phi_s = 0',
            'witness':'D_T B = b_t - (p/q)b_s; the missing contribution is -p*b_s/q.',
            'status':'corrected_under_declared_bed_pullback',
            'qualification':'No inference about an alternative undefined bed variable; source equation (7) is retained as the mathematical reproduction target.'}],
        'reconstruction':'On a simply connected regular patch, E=0 closes omega=b_t dt+b_s ds and reconstructs the printed bed b up to a constant. This does not repair the Eulerian physical pullback.',
        'lagrangian_statement':'Lagrange coordinates describe material labels. The source says it could not find a variational Lagrangian; this is not a proof of nonexistence and no Noether argument is used.'})


# ========================================================================
# Symmetries
# ========================================================================
def generators():
    """Source v3 PDF p. 4, in (t,s,phi) coordinate order."""
    return {
        'X1': (sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        'X2': (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
        'X3': (sp.Integer(0), sp.Integer(0), sp.Integer(1)),
        'X4': (t, s, u),
        'X5': (t, -2*s, sp.Integer(0)),
        'X6': (sp.Integer(0), sp.Integer(0), t),
    }

def split_weight_identity():
    """pr X5(E_m)+E_m; only the bedload-flux term has wrong weight."""
    flux_part = -g*total(m*kappa*p**(m-1)*b/q, 1)
    return sp.expand((3-m)*flux_part)

def _determining_split():
    """Necessary free-jet coefficients, checked against unrestricted prolongation.

    At each stage earlier coefficients have set xi=xi(s), tau=tau(t), eta_s=0.
    The last residual verifies sufficiency for the only remaining m=1 function.
    """
    E = master()
    r_rhs = sp.solve(E, r)[0]
    tau = sp.Function('tau')(t,s,u)
    xi = sp.Function('xi')(t,s,u)
    eta = sp.Function('eta')(t,s,u)
    omega = act(E,tau,xi,eta).subs(r,r_rhs)
    factor = g*(kappa*m*p**m*q+p)/(p*q**2)
    y_expected = factor*(sp.diff(xi,t)+p*sp.diff(xi,u))
    y_ok = sp.simplify(sp.diff(omega,y)-y_expected) == 0

    xi_s = sp.Function('xi')(s)
    omega = act(E,tau,xi_s,eta).subs(r,r_rhs)
    w_expected = 2*factor*(sp.diff(tau,s)+q*sp.diff(tau,u))
    w_ok = sp.simplify(sp.diff(omega,w)-w_expected) == 0

    tau_t = sp.Function('tau')(t)
    omega = act(E,tau_t,xi_s,eta).subs(r,r_rhs)
    ab_expected = -sp.diff(eta,s)/q
    ab_ok = sp.simplify(sp.diff(omega,a,b)-ab_expected) == 0

    eta_tu = sp.Function('eta')(t,u)
    omega = act(E,tau_t,xi_s,eta_tu).subs(r,r_rhs)
    a_expected = q*(4*p*sp.diff(eta_tu,u,2)
                      -3*sp.diff(tau_t,t,2)+4*sp.diff(eta_tu,t,u))
    a_ok = sp.simplify(sp.diff(omega,a)-a_expected) == 0

    A = sp.Function('A')(t)
    B = sp.Function('B')(t)
    omega = act(E,tau_t,xi_s,A*u+B).subs(r,r_rhs)
    x_expected = -g/(p**2*q**2)*(
        kappa*m*p**m*q*((m-3)*p*(A-sp.diff(tau_t,t))
                            +(m-1)*(sp.diff(A,t)*u+sp.diff(B,t)))
        +p**2*(2*sp.diff(tau_t,t)+sp.diff(xi_s,s)-3*A))
    x_ok = sp.simplify(sp.diff(omega,x)-x_expected) == 0

    lam, t0, s0 = sp.symbols('lam t0 s0', real=True)
    E1 = master(1)
    rem = sp.factor(act(E1,lam*t+t0,lam*s+s0,lam*u+B)+2*lam*E1)
    rem_expected = b*sp.diff(B,t,2)+q*sp.diff(B,t,3)
    rem_ok = sp.simplify(rem-rem_expected) == 0
    return {
        'passed': all((y_ok,w_ok,ab_ok,a_ok,x_ok,rem_ok)),
        'free_y': {'coefficient':str(y_expected),'checked':y_ok,
                   'consequence':'xi_t=xi_u=0; common factor is positive on the branch'},
        'free_w': {'coefficient':str(w_expected),'checked':w_ok,
                   'consequence':'tau_s=tau_u=0'},
        'free_a_b': {'coefficient':str(ab_expected),'checked':ab_ok,
                     'consequence':'eta_s=0'},
        'free_a': {'coefficient':str(a_expected),'checked':a_ok,
                   'consequence':'eta=A(t)*u+B(t), 4*A_prime=3*tau_double_prime'},
        'free_x': {'coefficient':str(x_expected),'checked':x_ok,
                   'consequence':'2*tau_prime+xi_prime-3*A=0; (m-3)*p*(A-tau_prime)+(m-1)*(A_prime*u+B_prime)=0'},
        'm1_remaining_residual': {'expression':str(rem_expected),'checked':rem_ok,
                                   'consequence':'B_double_prime=0 by free b,q splitting'},
        'normal_form':str(r_rhs),
    }

def build_symmetry_report():
    E = master()
    X = generators()
    checks = {}
    for name, multiplier in [('X1', 0), ('X2', 0), ('X3', 0), ('X4', -2)]:
        difference = sp.simplify(act(E, *X[name])-multiplier*E)
        checks[name] = {'multiplier': str(multiplier), 'remainder': str(difference),
                        'passed': difference == 0, 'status': 'exact_off_shell'}
    difference = sp.simplify(act(E, *X['X5'])+E-split_weight_identity())
    checks['X5'] = {'identity_remainder': str(difference), 'passed': difference == 0,
                    'm3_defect': str(sp.simplify(split_weight_identity().subs(m, 3))),
                    'm4_defect_nonzero': sp.simplify(split_weight_identity().subs(m, 4)) != 0,
                    'status': 'exact_off_shell_weight_identity'}
    boost_1 = sp.simplify(act(master(1),*X['X6']))
    boost_2 = sp.simplify(act(master(2),*X['X6']))
    checks['X6_m1'] = {'remainder':str(boost_1),'passed':boost_1 == 0,
                       'm2_nonzero':boost_2 != 0, 'status':'exact_off_shell'}
    checks['unrestricted_determining_split'] = _determining_split()
    # On source p. 4, this printed determining equation gives 3+1+2=6 for X4.
    printed_witness = sp.Integer(3)*sp.Integer(1)+sp.diff(s,s)+2*sp.diff(t,t)
    return {
        'scope': {'equation': 'printed scalar equation (7), not advectively corrected/full bed system',
                  'branch': 'p=phi_t>0, q=phi_s>0, g>0, kappa>0, m>=1',
                  'category': 'local smooth point generators; direct third-jet prolongation',
                  'source': 'Paliathanasis, Leon, Leach, Mathematics 14 (2026) 433, v3 PDF pp. 4-5'},
        'claims': {
            'listed_generators': {'status': 'proved_direct_identity',
                                  'generic': ['X1','X2','X3','X4'], 'm3_extra': 'X5',
                                  'm1_extra_not_in_source':'X6=t*d_phi'},
            'maximal_classification': {'status': 'proved_on_declared_branch' if checks['unrestricted_determining_split']['passed'] else 'unresolved',
                                       'dimensions': {'m=1':5,'m=3':5,'m>=1,m!=1,3':4},
                                       'category':'unrestricted smooth local point generators on p,q>0; no singular p=0/q=0 branch'}},
        'formulas': {'E_m': str(E), 'X5_defect': str(split_weight_identity()),
                     'X5_weight_identity': 'pr3(X5)(E_m)+E_m=(3-m)*E_bedload',
                     'E_bedload': str(-g*total(m*kappa*p**(m-1)*b/q, 1))},
        'checks': checks,
        'discrepancies': {
            'printed_determining_X4_witness': {
                'source': 'v3 PDF p. 4, displayed determining system: 3 eta1 + xi2_s + 2 xi1_t = 0',
                'substitution': 'X4: eta1=1, xi2_s=1, xi1_t=1',
                'value': str(printed_witness), 'status': 'refuted_as_printed',
                'effect': 'The printed determining system cannot establish its Proposition 1 or maximality.'},
            'missing_m1_generator': {
                'source':'v3 PDF p. 4 Proposition 1: four for arbitrary m, fifth only m=3',
                'counterexample':'X6=t*d_phi at m=1; pr3(X6)(E_1)=0',
                'status':'refutes_source_maximal_count_at_m1',
                'corrected_dimension':'5 on the declared positive branch'}}}


# ========================================================================
# Algebra
# ========================================================================
_NAMES = ('X1', 'X2', 'X3', 'X4', 'X5')

_M1_NAMES = ('X1', 'X2', 'X3', 'X4', 'X6')

_COORDS = (t, s, u)

def bracket(left, right):
    """[left,right]=left(right)-right(left), as coordinate vector fields."""
    return tuple(sp.simplify(sum(left[k]*sp.diff(right[i], _COORDS[k])
                                 -right[k]*sp.diff(left[i], _COORDS[k])
                                 for k in range(3))) for i in range(3))

def _coordinates(vector, names=_NAMES):
    basis = generators()
    coefficients = sp.symbols('c1:6')
    equations = [sum(coefficients[k]*basis[names[k]][i] for k in range(5))-vector[i]
                 for i in range(3)]
    equations = [coefficient for expression in equations
                 for coefficient in sp.Poly(expression, t, s, u).coeffs()]
    answer = sp.solve(equations, coefficients, dict=True)
    if not answer:
        raise ValueError('vector is outside the declared Lie span')
    return {name: sp.simplify(answer[0][coefficient]) for name, coefficient in zip(names, coefficients)
            if answer[0].get(coefficient, 0) != 0}

def adjoint(actor, target, epsilon, stratum='m3'):
    """Source convention Ad(exp(eps A))B=exp(-eps ad_A)B."""
    names = _M1_NAMES if stratum == 'm1' else _NAMES
    if actor not in names or target not in names:
        raise ValueError('unknown generator')
    X = generators()
    if actor in ('X1','X2','X3','X6'):
        first = _coordinates(bracket(X[actor], X[target]), names)
        result = {target: sp.Integer(1)}
        for name, value in first.items():
            result[name] = sp.simplify(result.get(name, 0)-epsilon*value)
    else:
        first = _coordinates(bracket(X[actor], X[target]), names)
        if not first:
            result = {target: sp.Integer(1)}
        else:
            eigenvalue = first.get(target)
            if eigenvalue is None or len(first) != 1:
                raise ValueError('unexpected non-diagonal dilation')
            result = {target: sp.exp(-epsilon*eigenvalue)}
    return {name: value for name, value in result.items() if value != 0}

def orbit_invariants():
    """Orbit data, not a claim that the source list is an optimal system."""
    return {
        'generic': {
            'translation_projective_dimension': 2,
            'reason': 'Ad(X4) rescales all X1,X2,X3 equally, hence fixes each translation line.',
            'translation_representatives': ['X1+a*X2+b*X3 (a,b real)',
                                            'X2+a*X3 (a real)', 'X3'],
            'missing_source_family': 'X2+a*X3 (a nonzero), with projective parameter a',
            'nontranslation_line': 'X4 (translation terms removable)'},
        'exceptional': {
            'diagonal_weights_of_ad_aX4_bX5': {'X1':'-(a+b)', 'X2':'-(a-2b)', 'X3':'-a'},
            'resonant_directions': [
                {'H':'X5', 'survivor':'X3', 'family':'X5+c*X3'},
                {'H':'X4-X5', 'survivor':'X1', 'family':'X4-X5+c*X1'},
                {'H':'X4+(1/2)*X5', 'survivor':'X2', 'family':'X4+(1/2)*X5+c*X2'}],
            'resonant_c_connected_normal_forms': ['0','+1','-1'],
            'translation_line_invariant': 'I=a1**2*a2/a3**3 when a3!=0',
            'translation_invariant_scope': 'Ad(X5) and nonzero line rescaling; support and relative signs require separate strata',
            'translation_representatives': [
                'X1', 'X2', 'X3', 'X1+sigma*X2',
                'X3+sigma*X1', 'X3+sigma*X2',
                'X3+sigma*X1+K*X2'],
            'translation_parameters': 'sigma in {+1,-1}; K real nonzero; use only terms with their stated nonzero support',
            'nontranslation_representatives': 'H=aX4+bX5, (a:b) in RP1; at the three resonance directions add c*survivor, c=+1 or -1',
            'equivalence_test': 'For translation coefficients v,w: w=lambda*(exp(eps)*v1, exp(-2eps)*v2, v3), lambda real nonzero; for H+v, H projective fixed and nonresonant v removed by translations.',
            'source_optimality_status': 'refuted_incomplete'},
        'm1': {
            'basis':['X1','X2','X3','X4','X6'],
            'adjoint_elementary_actions': [
                'Ad(exp(eps X1)): v1->v1-eps*h, v3->v3-eps*c',
                'Ad(exp(eps X2)): v2->v2-eps*h',
                'Ad(exp(eps X3)): v3->v3-eps*h',
                'Ad(exp(eps X4)): (v1,v2,v3)->exp(eps)*(v1,v2,v3)',
                'Ad(exp(eps X6)): v3->v3+eps*v1'],
            'coordinates':'Z=v1*X1+v2*X2+v3*X3+h*X4+c*X6',
            'representatives': [
                'X4+alpha*X6 (alpha real)',
                'X6', 'X6+sigma*X1+a*X2 (sigma=+1 or -1, a real)',
                'X6+sigma*X2 (sigma=+1 or -1)',
                'X1+a*X2 (a real)', 'X2+a*X3 (a real)', 'X3'],
            'normalization': 'When c normalized to 1, X4 permits only positive common scaling of (v1,v2), so signs survive.',
            'classification_status':'connected-adjoint orbit representatives on the m=1 five-generator algebra'}}

def build_algebra_report():
    X = generators()
    zero = (sp.Integer(0),)*3
    brackets = {}
    anti = 0
    for a,b in product(_NAMES, repeat=2):
        ab = bracket(X[a], X[b])
        brackets[f'[{a},{b}]'] = {k:str(v) for k,v in _coordinates(ab).items()}
        anti += int(tuple(sp.simplify(v+w) for v,w in zip(ab,bracket(X[b],X[a]))) == zero)
    jacobi = 0
    for a,b,c in product(_NAMES, repeat=3):
        terms = [bracket(X[a],bracket(X[b],X[c])),
                 bracket(X[b],bracket(X[c],X[a])),
                 bracket(X[c],bracket(X[a],X[b]))]
        jacobi += int(all(sp.simplify(sum(term[i] for term in terms)) == 0 for i in range(3)))
    eps = sp.symbols('eps', real=True)
    adjoints = {f'Ad({a}){b}': {k:str(v) for k,v in adjoint(a,b,eps).items()}
                for a,b in product(_NAMES, repeat=2)}
    m1_brackets = {f'[{a},{b}]':{k:str(v) for k,v in _coordinates(bracket(X[a],X[b]), _M1_NAMES).items()}
                   for a,b in product(_M1_NAMES, repeat=2)}
    m1_jacobi = 0
    for a,b,c in product(_M1_NAMES, repeat=3):
        terms = [bracket(X[a],bracket(X[b],X[c])),
                 bracket(X[b],bracket(X[c],X[a])),
                 bracket(X[c],bracket(X[a],X[b]))]
        m1_jacobi += int(all(sp.simplify(sum(term[i] for term in terms)) == 0 for i in range(3)))
    m1_adjoints = {f'Ad({a}){b}':{k:str(v) for k,v in adjoint(a,b,eps,'m1').items()}
                   for a,b in product(_M1_NAMES, repeat=2)}
    # Literal source Table 2 inputs, independently compared with computed ad.
    expected = {(a,b):{b:sp.Integer(1)} for a,b in product(_NAMES,repeat=2)}
    expected.update({('X1','X4'):{'X4':1,'X1':-eps},
                     ('X1','X5'):{'X5':1,'X1':-eps},
                     ('X2','X4'):{'X4':1,'X2':-eps},
                     ('X2','X5'):{'X5':1,'X2':2*eps},
                     ('X3','X4'):{'X4':1,'X3':-eps}})
    for target in ('X1','X2','X3'):
        expected['X4',target]={target:sp.exp(eps)}
    expected['X5','X1']={'X1':sp.exp(eps)}
    expected['X5','X2']={'X2':sp.exp(-2*eps)}
    table2 = {}
    for actor,target in product(_NAMES,repeat=2):
        actual=adjoint(actor,target,eps)
        differences={key:sp.simplify(actual.get(key,0)-expected[actor,target].get(key,0))
                     for key in _NAMES}
        table2[f'Ad({actor}){target}']={
            'passed':all(value==0 for value in differences.values()),
            'difference':{key:str(value) for key,value in differences.items() if value!=0}}
    table2_passed=all(row['passed'] for row in table2.values())
    return {
        'scope': {'source': 'v3 PDF pp. 4-6, Tables 1-2 and displayed one-dimensional system',
                  'convention': '[A,B]=A(B)-B(A); Ad(exp(eps A))B=exp(-eps ad_A)B',
                  'generic_basis':'X1-X4 for m!=1,3', 'm3_basis':'X1-X5', 'm1_basis':'X1-X4 plus X6',
                  'equivalence': 'connected inner adjoint plus nonzero line rescaling'},
        'claims': {'lie_algebra': {'status':'verified_for_listed_generators_only'},
                   'source_optimal_system': {'status':'refuted_incomplete'},
                   'complete_1d_classification': {'status':'derived_connected_inner_adjoint_with_line_scaling_on_each_declared_stratum'}},
        'formulas': {'brackets':brackets, 'adjoints':adjoints, 'm1_brackets':m1_brackets,
                     'm1_adjoints':m1_adjoints, 'orbits':orbit_invariants(),
                     'orbit_evidence_kind':'hand-derived classification using computed adjoint actions; not an automatic orbit-classification algorithm'},
        'checks': {'antisymmetry':{'passed':anti,'total':25},
                   'jacobi':{'passed':jacobi,'total':125},
                   'm1_jacobi':{'passed':m1_jacobi,'total':125},
                   'table_2':{'status':'agrees' if table2_passed else 'disagrees',
                              'convention':'negative ad','comparisons':table2}},
        'discrepancies': {
            'table_1': {'wrong_cells':['[X5,X1]','[X5,X2]'],
                        'source_values':['+X1','-2X2'], 'correct_values':['-X1','+2X2'],
                        'proof':'antisymmetry and direct coordinate-vector bracket'},
            'one_dimensional_list': {
                'status':'refuted_incomplete',
                'generic_missing':'X2+aX3 for a!=0; X4 acts only by common rescaling on translation lines',
                'm3_missing':['X5+cX3','X4-X5+cX1','X4+(1/2)X5+cX2'],
                'qualification':'c!=0 witnesses cannot be removed by connected inner adjoint; sign and support strata require explicit tracking'},
            'm1_missing_generator': {
                'source':'v3 PDF p. 4 Proposition 1 and pp. 5-6 Tables 1-2/list, all omitting m=1 stratum',
                'generator':'X6=t*d_phi', 'new_bracket':'[X1,X6]=X3',
                'effect':'At m=1 the listed four-dimensional algebra is a proper subalgebra; its optimal list cannot be complete.'}}}


# ========================================================================
# Reductions
# ========================================================================
def _D(expr):
    return profile_total(expr)

def _reductions_step(label, expression):
    return {'label': label, 'expression': expression}

def _result(case, status, coordinate, ansatz, residual=None, velocity=None,
            gradient=None, steps=(), guards=(), source_equations=()):
    if residual is not None:
        residual = sp.factor(residual)
        leading = sp.factor(sp.diff(residual, H))
        order = 3 if leading != 0 else (2 if residual.has(C) else 0)
        rhs = sp.cancel(-(residual - leading*H)/leading) if order == 3 else None
    else:
        leading, rhs, order = None, None, None
    return dict(id=case, status=status, coordinate=coordinate, ansatz=ansatz,
                residual=residual, leading=leading, rhs=rhs, velocity=velocity,
                gradient=gradient, ode_order=order, steps=list(steps),
                guards=list(guards), source_equations=list(source_equations))

def _scale(case, A, B, exponent, coordinate, ansatz, source_equations):
    # t^d Y(z) differentiates to t^(d-1)[dY+BzY']; s differentiation
    # adds B to the t exponent and differentiates Y with respect to z.
    V = A*F+B*z*P
    q = P
    a = (A-1)*V+B*z*_D(V)
    b = _D(V)
    c = C
    r = (A-2)*a+B*z*_D(a)
    w = _D(a)
    x = _D(b)
    y = H
    inertial = q*a-g*c/q**2
    flux = exponent*kappa*V**(exponent-1)*b/q
    residual = sp.factor(-A*inertial+B*z*_D(inertial)-g*_D(flux))
    steps = [_reductions_step('generator', f'X=t d_t + ({-B}) s d_s + ({A}) phi d_phi (rescaled)'),
             _reductions_step('invariant graph equation Q', A*F-((A*F+B*z*P)-B*z*P)),
             _reductions_step('invariant coordinate', coordinate),
             _reductions_step('invariant graph Q=0', ansatz),
             _reductions_step('phi_t at t=1', V), _reductions_step('phi_s at t=1', q),
             _reductions_step('phi_tt at t=1', a), _reductions_step('phi_ts at t=1', b),
             _reductions_step('phi_ss at t=1', c), _reductions_step('phi_ttt at t=1', r),
             _reductions_step('phi_tts at t=1', w), _reductions_step('phi_tss at t=1', x),
             _reductions_step('phi_sss at t=1', y),
             _reductions_step('inertial current profile', inertial),
             _reductions_step('sediment flux profile', flux),
             _reductions_step('PDE pullback multiplier', sp.Symbol('t')**(-A-1)),
             _reductions_step('reduced residual', residual)]
    if case == '3.4':
        integral = C*(-z**3*P+g*z/P**2+
                        g*exponent*kappa*z*V**(exponent-1)/P)
        steps.append(_reductions_step('first-integral density', sp.factor(integral)))
    guards = ['t>0', 'profile gradient P>0', 'profile velocity A*F+B*z*P>0',
              'highest-derivative coefficient nonzero']
    return _result(case, 'regular_ode', coordinate, ansatz, residual, V, q,
                   steps, guards, source_equations)

def _travel(case, exponent, alpha, alpha3):
    zc = s-alpha*t
    v = alpha3-alpha*P
    A = (alpha**2*P-g/P**2)*C
    flux = -alpha*exponent*kappa*v**(exponent-1)*C/P
    integral = sp.factor(A-g*exponent*kappa*v**(exponent-1)*C/P)
    residual = -alpha*_D(integral)
    ansatz = alpha3*t+F
    jets = [ansatz, v, P, alpha**2*C, -alpha*C, C,
            -alpha**3*H, alpha**2*H, -alpha*H, H]
    names = ['phi', 'phi_t', 'phi_s', 'phi_tt', 'phi_ts', 'phi_ss',
             'phi_ttt', 'phi_tts', 'phi_tss', 'phi_sss']
    steps = [_reductions_step('generator', f'd_t+({alpha})d_s+({alpha3})d_phi'),
             _reductions_step('invariant coordinate', zc),
             _reductions_step('invariant graph Q=0', ansatz)]
    steps += [_reductions_step(name, value) for name, value in zip(names,jets)]
    steps += [_reductions_step('inertial current', A), _reductions_step('sediment flux', flux),
              _reductions_step('PDE pullback multiplier', sp.Integer(1)),
              _reductions_step('first-integral density', integral),
              _reductions_step('reduced residual', residual)]
    if alpha == 0:
        return _result(case, 'identity', s, ansatz, sp.Integer(0), v, P,
                       steps, ['P>0', 'alpha3>0 for positive velocity'],
                       ['Table 3', '3.7' if alpha3 != 0 else '3.1'])
    return _result(case, 'regular_ode', zc, ansatz, residual, v, P, steps,
                   ['P>0', 'alpha3-alpha*P>0', 'alpha!=0',
                    'highest-derivative coefficient nonzero'],
                   ['(28)' if alpha3 == 0 else '(33)', '(29)-(31)' if alpha3 == 0 else '(34)'])

@lru_cache(maxsize=128)
def derive_reduction(case, exponent=3, alpha=-1, alpha3=1, mix_alpha=sp.Rational(1,4)):
    """Return exact local pullback; inputs are numbers, never evaluated strings."""
    case = str(case)
    exponent, alpha, alpha3, mix_alpha = map(sp.sympify,
                                             (exponent,alpha,alpha3,mix_alpha))
    if case == '3.1':
        return _result(case, 'identity', s, F, sp.Integer(0), 0, P,
                       [_reductions_step('generator', 'd_t'), _reductions_step('Q=0', 'phi_t=0'),
                        _reductions_step('jets', 'phi=F(s), phi_t=phi_ts=phi_tt=0; phi_s=P, phi_ss=C, phi_sss=H'),
                        _reductions_step('PDE pullback', sp.Integer(0))],
                       ['P>0', 'velocity=0 is outside the positive-velocity chart'], ['Table 3', '3.1'])
    if case == '3.2':
        return _result(case, 'undefined', t, F, None, P, 0,
                       [_reductions_step('generator','d_s'), _reductions_step('Q=0','phi_s=0'),
                        _reductions_step('jets','phi=F(t), phi_t=P, phi_tt=C, phi_ttt=H; phi_s=phi_ts=phi_ss=0'),
                        _reductions_step('denominator','phi_s^2=0')],
                       ['phi_s=0 violates the PDE domain'], ['Table 3','3.2'])
    if case == '3.3':
        return _result(case, 'no_invariant_graph', (t,s), None,
                       steps=[_reductions_step('generator','d_phi'), _reductions_step('Q=0','1=0')],
                       guards=['vertical orbit has no invariant graph'], source_equations=['Table 3','3.3'])
    if case == '3.4':
        return _scale(case, sp.Integer(1), sp.Integer(-1), exponent,
                      s/t, t*F, ['(24)'])
    if case == '3.5':
        if exponent != 3:
            raise ValueError('X5 is a symmetry only at exponent 3')
        return _scale(case, sp.Integer(0), sp.Integer(2), exponent,
                      s*t**2, F, ['(25)-(27)'])
    if case == '3.6':
        return _travel(case, exponent, alpha, sp.Integer(0))
    if case == '3.7':
        return _result(case, 'identity', s, alpha*t+F,
                       sp.Integer(0), alpha, P,
                       [_reductions_step('generator',f'd_t+({alpha})d_phi'),
                        _reductions_step('Q=0','phi_t=alpha'),
                        _reductions_step('jets','phi_t=alpha, phi_s=P, phi_ss=C; all mixed and higher time jets vanish'),
                        _reductions_step('PDE pullback',sp.Integer(0))],
                       ['P>0', 'alpha>0 for positive-velocity chart'], ['3.7'])
    if case == '3.8':
        residual = alpha*H
        return _result(case, 'regular_ode', t, alpha*s+F,
                       residual, P, alpha,
                       [_reductions_step('generator',f'd_s+({alpha})d_phi'),
                        _reductions_step('Q=0','phi_s=alpha'),
                        _reductions_step('jets','phi_t=P, phi_s=alpha, phi_tt=C, phi_ttt=H; all s-derivatives of order >=2 and mixed jets vanish'),
                        _reductions_step('PDE pullback',residual)],
                       ['alpha>0', 'P>0', 'alpha!=0'], ['(32)'])
    if case == '3.9':
        return _travel(case, exponent, alpha, alpha3)
    if case == 'table3-mixed':
        if exponent != 3 and mix_alpha != 0:
            raise ValueError('mixed X4+alpha*X5 is a symmetry only at exponent 3 unless alpha=0')
        if mix_alpha == -1:
            # X4-X5=3s*d_s+phi*d_phi; use s>0 as the transverse chart.
            A = sp.Rational(1,3)
            ansatz = s**A*F
            v, q = s**A*P, A*s**(A-1)*F
            # Substitute the complete original jet, then set s=1,t=z.
            f = sp.Function('f')(t)
            phi = s**A*f
            subs = {jet:sp.diff(phi,t,i,s,k).subs(s,1)
                    for (i,k),jet in JETS.items()}
            subs = {key: val.subs({f:F,sp.diff(f,t):P,
                    sp.diff(f,t,2):C,sp.diff(f,t,3):H})
                    for key,val in subs.items()}
            residual = sp.factor(master(3).subs(subs, simultaneous=True))
            steps = [_reductions_step('generator','3s*d_s+phi*d_phi'),
                     _reductions_step('invariants','t, phi*s^(-1/3)'),
                     _reductions_step('Q=0',ansatz)] + [
                     _reductions_step('jet '+str(ij), subs[jet]) for ij,jet in JETS.items()]
            steps += [_reductions_step('PDE pullback multiplier',s**(-A)),
                      _reductions_step('reduced residual at s=1',residual)]
            return _result(case,'regular_ode',t,ansatz,residual,v.subs(s,1),
                           q.subs(s,1),steps,['s>0','F>0','P>0',
                           'highest-derivative coefficient nonzero'],['Table 3'])
        A = sp.cancel(1/(1+mix_alpha))
        B = sp.cancel((2*mix_alpha-1)/(1+mix_alpha))
        return _scale(case,A,B,exponent,s*t**B,t**A*F,['Table 3'])
    raise ValueError(f'unknown reduction case: {case}')

def verify_reduction_pullbacks():
    """Differentiate the invariant graphs and substitute into master() directly.

    This route does not reuse _scale/_travel differentiation rules. It checks
    the cubic nine-case table and the other declared numerical exponents.
    """
    profile=sp.Function('profile')
    graphs={'3.1':profile(s),'3.2':profile(t),'3.4':t*profile(s/t),
            '3.5':profile(s*t**2),'3.6':profile(s+t),'3.7':t+profile(s),
            '3.8':s+profile(t),'3.9':t+profile(s+t)}
    fields={'3.1':(1,0,0),'3.2':(0,1,0),'3.3':(0,0,1),
            '3.4':(t,s,u),'3.5':(t,-2*s,0),'3.6':(1,-1,0),
            '3.7':(1,0,1),'3.8':(0,1,1),'3.9':(1,-1,1)}
    chart_time=sp.Symbol('T',positive=True)
    chart_space=sp.Symbol('S',real=True)
    at={'3.1':{t:chart_time,s:z},'3.2':{t:z,s:chart_space},
        '3.4':{t:chart_time,s:z*chart_time},
        '3.5':{t:chart_time,s:z/chart_time**2},
        '3.6':{t:chart_time,s:z-chart_time},'3.7':{t:chart_time,s:z},
        '3.8':{t:z,s:chart_space},'3.9':{t:chart_time,s:z-chart_time}}
    replacements={sp.diff(profile(z),z,i):value for i,value in enumerate((F,P,C,H))}
    rows=[]
    for case in (f'3.{i}' for i in range(1,10)):
        if case=='3.3':
            graph_condition=sp.sympify(fields[case][2])
            rows.append({'case':case,'m':3,'status':'no_invariant_graph',
                         'graph_condition':graph_condition,'passed':graph_condition!=0})
            continue
        graph=graphs[case];tau,xi,eta=map(sp.sympify,fields[case])
        graph_condition=sp.simplify(eta.subs(u,graph)-tau*sp.diff(graph,t)-xi*sp.diff(graph,s))
        raw_jets={jet:sp.diff(graph,t,i,s,k) for (i,k),jet in JETS.items()}
        if case=='3.2':
            rows.append({'case':case,'m':3,'status':'undefined_chart',
                         'gradient':raw_jets[q],'graph_condition':graph_condition,
                         'passed':raw_jets[q]==0 and graph_condition==0})
            continue
        jets={key:value.subs(at[case],simultaneous=True).doit().subs(replacements,simultaneous=True)
              for key,value in raw_jets.items()}
        exponents=(1,sp.Rational(3,2),2,3,4) if case in ('3.4','3.6','3.8','3.9') else (3,)
        for exponent in exponents:
            original=sp.factor(master(exponent).subs(jets,simultaneous=True))
            reduced=derive_reduction(case,exponent=exponent,alpha=1 if case in ('3.7','3.8') else -1)
            multiplier=chart_time**(-2 if case=='3.4' else -1) if case in ('3.4','3.5') else sp.Integer(1)
            difference=sp.simplify(original-multiplier*reduced['residual'])
            rows.append({'case':case,'m':exponent,'status':reduced['status'],
                         'graph_condition':graph_condition,'direct_pullback':original,
                         'pullback_multiplier':multiplier,
                         'difference':difference,'passed':graph_condition==0 and difference==0})
    integrals={}
    for case,data in [('3.4',common_scaling_first_integral(m)),
                      ('3.6',traveling_first_integral(m,-1,0)),
                      ('3.9',traveling_first_integral(m,-1,1))]:
        difference=sp.simplify(data['dI']-derive_reduction(case,exponent=m)['residual'])
        integrals[case]={'difference':difference,'passed':difference==0,
                         'scope':'symbolic m; traveling alpha=-1 and declared alpha3'}
    return {'passed':all(row['passed'] for row in rows) and all(row['passed'] for row in integrals.values()),
            'direct_graph_checks':rows,'first_integral_checks':integrals}


def build_reduction_report():
    """JSON-safe evidence; exact certificates remain available from derive_reduction."""
    rows = [derive_reduction(f'3.{i}', alpha=1 if i in (7,8) else -1)
            for i in range(1,10)]
    mixed = derive_reduction('table3-mixed')
    return jsonable({'cases':rows, 'table3_mixed':mixed,
        'checks':verify_reduction_pullbacks(),
        'exact_certificates': {
            'common_scaling':common_scaling_first_integral(m),
            'traveling_3_6':traveling_first_integral(3,-1,0),
            'traveling_3_9':traveling_first_integral(3,-1,1),
            'cubic_power_law':cubic_power_law_audit()},
        'source_witnesses':printed_equation_witnesses(),
        'translation_witnesses':translated_ansatz_witnesses(),
        'further_reduction': {
            'common_scaling': 'I=C*(-z^3*P+g*z/P^2+g*m*kappa*z*(F-z*P)^(m-1)/P); dI/dz equals the third-order residual for symbolic m',
            'traveling_3.6_3.9': 'I=C*(alpha^2*P-g/P^2-g*m*kappa*(alpha3-alpha*P)^(m-1)/P); I is constant; for I!=0, dz/dP=B(P)/I',
            '3.8': 'H=0, so F(t)=c0+c1*t+c2*t^2/2',
            '3.5': 'translation in F permits mu=P, a second-order equation; additional scaling gives a rational first-order equation on 2*Sigma/3+M!=0'},
        'printed_comparison': {
            '3.1_3.2': 'Source subsection prose reverses Table 3: X1 gives F(s), X2 gives F(t); X2 is outside q>0 domain.',
            '3.7_3.8': 'Source subsection ansatzes are reversed. Correct 3.7: alpha*t+F(s), identity; correct 3.8: alpha*s+F(t), alpha*F_ttt=0.',
            '3.4': 'Printed cubic power profile and amplitude condition agree exactly, but the normal-form leading coefficient vanishes there; phi grows like t^(2/3) at fixed s>0.',
            '3.5': 'Printed (25)--(27) fail exact rational witnesses; source power profile is exact and (27) should have an additional 2*Sigma/3+M denominator.',
            '3.6_3.9': 'Printed (29), (31), (33) fail exact rational witnesses. Correct traveling residual is -alpha*dI/dz. Free-particle linearization is valid locally where B(P)!=0; (34) selects I=-1, not the general family.'}})


# ========================================================================
# Source Formulas
# ========================================================================
def cubic_power_law_audit():
    """Equations (24)--(26): exact profile, condition, and ODE-chart type."""
    A = sp.symbols('A', positive=True)
    jets = {F:A*z**sp.Rational(1,3),
            P:A*z**sp.Rational(-2,3)/3,
            C:-2*A*z**sp.Rational(-5,3)/9,
            H:10*A*z**sp.Rational(-8,3)/27}
    beta = 3*kappa
    condition = sp.expand((4*beta*g-1)*A**3+27*g)
    x4 = derive_reduction('3.4')
    x5 = derive_reduction('3.5')
    return {'profile':jets[F], 'condition_printed':condition,
            'x4_residual':sp.factor(x4['residual'].subs(jets)),
            'x5_residual':sp.factor(x5['residual'].subs(jets)),
            'x4_leading':sp.factor(x4['leading'].subs(jets)),
            'x5_leading':sp.factor(x5['leading'].subs(jets)),
            'domain':'z>0, A>0, g>0, kappa>0; x4 normal-form coefficient vanishes on the printed condition'}

def translated_ansatz_witnesses():
    """Table 3 versus subsections 3.1--3.2 and 3.7--3.8."""
    # At alpha=1, F'=2, source 3.7/3.8 displayed graphs fail Q=0.
    # The source 3.8 graph alpha*t+F(s) actually has zero PDE residual
    # for any F(s), including an F with nonzero third derivative.
    def graph_condition(graph,tau,xi,eta):
        return sp.simplify(eta-tau*sp.diff(graph,t)-xi*sp.diff(graph,s))
    phi=t+s+s**3/6
    jets={jet:sp.diff(phi,t,i,s,k) for (i,k),jet in JETS.items()}
    return {'3.1_source_graph_Q_at_Fprime_2':graph_condition(2*t,1,0,0),
            '3.2_source_graph_Q_at_Fprime_2':graph_condition(2*s,0,1,0),
            '3.7_source_graph_Q_at_alpha_1_Fprime_2':graph_condition(s+2*t,1,0,1),
            '3.8_source_graph_Q_at_alpha_1_Fprime_2':graph_condition(t+2*s,0,1,1),
            '3.8_wrong_graph_counterexample': {
                'phi':phi,
                'phi_s':jets[q],
                'phi_t':jets[p],
                'F_sss':jets[y],
                'original_PDE':sp.simplify(master().subs(jets,simultaneous=True)),
                'note':'For any real s this is q>0 and p>0; it violates the printed F_sss=0 requirement while solving the printed scalar PDE.'}}

def traveling_first_integral(exponent=3, alpha=-1, alpha3=1):
    """Exact first integral of (28)/(33) with its free integration constant."""
    exponent,alpha,alpha3 = map(sp.sympify,(exponent,alpha,alpha3))
    v = alpha3-alpha*P
    B = sp.factor(alpha**2*P-g/P**2
                  -g*exponent*kappa*v**(exponent-1)/P)
    I = B*C
    # Y(P)=integral B(P)dP locally. A second derivative of Y(P(z))
    # is B*H+B'*C^2, so the reduced equation is -alpha*Y''=0.
    return {'B':B, 'I':I, 'dI':sp.factor(profile_total(I)),
            'linearization':'Y(P)=Integral(B(P),dP); Y(z) is affine if B(P)!=0',
            'quadrature':'z-z0=(Integral(B(P),dP)-Y0)/I0 for I0!=0; I0=0 implies P constant on B!=0 chart',
            'domain':'P>0, alpha3-alpha*P>0, alpha!=0, B(P)!=0'}

def common_scaling_first_integral(exponent=3):
    """Exact X4 certificate for all real exponents on the positive chart."""
    exponent = sp.sympify(exponent)
    velocity = F-z*P
    I = C*(-z**3*P+g*z/P**2+
             g*exponent*kappa*z*velocity**(exponent-1)/P)
    return {'I':sp.factor(I), 'dI':sp.factor(profile_total(I)),
            'domain':'z>0, P>0, F-z*P>0; all real m; I is constant on reduced solutions'}

def printed_equation_witnesses():
    """Page-image-checked equations (25),(27),(29)--(31),(33), cubic slice.

    Source expressions are transcribed on their displayed normalization. A
    zero of a source formula with nonzero original pullback disproves even
    equivalence up to a nonvanishing multiplier.
    """
    Z,G,K = z,g,kappa
    beta = 3*K
    point = {Z:1,P:sp.Rational(1,2),C:sp.Rational(1,10),
             G:1,K:sp.Rational(1,30)}
    V = F-Z*P
    source24 = (-Z**2*P**3*(Z*profile_total(P*C)+3*P*C)
                +G*P*profile_total(Z*C)-2*G*Z*C**2
                +G*beta*Z*P*V*2*Z**2*C**2
                -V**2*P*((Z*H+2*C**2)*P-Z*C**2))
    point24 = {**point, F:2}
    h24 = sp.solve(source24.subs(point24),H)[0]
    source25 = (4*Z*P**3*C*(Z*C+3*P)+2*G*C**2+
                beta*Z*((Z*C+5*P)*Z*C+(2*P+Z**2*H)*P))
    h25 = sp.solve(source25.subs(point),H)[0]
    source29 = (P*((P*C)**2+H*(P**3-G))-
                beta*G*P**3*(C+P*H))  # alpha=-1, m=3
    h29 = sp.solve(source29.subs(point),H)[0]
    source28 = source29-beta*G*P**4*H
    h28 = sp.solve(source28.subs(point),H)[0]
    v = 1+P
    source33 = (P*((P*C)**2+H*(P**3-G))-
                beta*G*(v**3*P*(C+P*H)-v*H))
    h33 = sp.solve(source33.subs(point),H)[0]
    sigma, M = sp.symbols('Sigma M', positive=True)
    den27 = 4*sigma**3*(beta*G-1)+G
    source27 = (2*(G+(4*beta*G-1)*sigma**3)*sigma*M**3/(9*den27)
                +(8*sigma**3*(1+2*beta*G)+G)*M**2/(3*den27)
                +2*(2*sigma**3*(beta*G-1)-G)*M/(sigma*den27))
    x5 = derive_reduction('3.5')
    transformed_h = x5['rhs'].subs({P:sigma*Z**sp.Rational(-2,3),
                                     C:M*Z**sp.Rational(-5,3)})
    exact27 = sp.factor((sp.Rational(5,3)*M+Z**sp.Rational(8,3)*transformed_h)
                         /(sp.Rational(2,3)*sigma+M))
    sample27 = {sigma:1,M:1,G:1,K:sp.Rational(1,30),Z:1}
    B = traveling_first_integral(3,-1,0)['B']
    source30_slope = (P**3+beta*P**2+2*G)/(P*(G-P**2+P**3))
    correct30_slope = -sp.diff(B,P)/B
    source31 = beta*G*P**2/((1+beta*G)*P**3+G)  # M0=1, exp(-2*pi*i)=1
    # Literal (34), with lower integration limit P0=1. The displayed
    # integrand contains the coordinate z rather than dummy variable tau.
    D34 = G/P**2-Z+beta*G*(1+P)**2/P
    c34 = sp.factor((1+(P-1))/D34).subs(point)
    h34 = sp.factor((2*c34-sp.diff(D34,P).subs(point)*c34**2)
                    /D34.subs(point))
    data = {
        'eq24':{'printed_H_zero':h24,
                'original_residual_at_zero':sp.factor(derive_reduction('3.4')['residual'].subs(point24).subs(H,h24))},
        'eq25':{'printed_H_zero':h25,
                'original_residual_at_zero':sp.factor(x5['residual'].subs(point).subs(H,h25))},
        'eq26':{'printed_mu_second_zero':h25,
                'correct_mu_equation_at_zero':sp.factor(x5['residual'].subs(point).subs(H,h25))},
        'eq27':{'printed_Mprime_at_sample':sp.factor(source27.subs(sample27)),
                'correct_Mprime_at_sample':sp.factor(exact27.subs(sample27)),
                'correct_rhs':exact27},
        'eq28':{'printed_H_zero':h28,
                'original_residual_at_zero':sp.factor(derive_reduction('3.6')['residual'].subs(point).subs(H,h28))},
        'eq29':{'printed_H_zero':h29,
                'original_residual_at_zero':sp.factor(derive_reduction('3.6')['residual'].subs(point).subs(H,h29))},
        'eq30':{'printed_Mprime_over_M_at_sample':sp.factor(source30_slope.subs(point)),
                'correct_Mprime_over_M_at_sample':sp.factor(correct30_slope.subs(point))},
        'eq31':{'printed_M':source31,
                'd_of_correct_integral_dP_at_sample':sp.factor(sp.diff(B*source31,P).subs(point))},
        'eq33':{'printed_H_zero':h33,
                'original_residual_at_zero':sp.factor(derive_reduction('3.9')['residual'].subs(point).subs(H,h33))},
        'eq32':{
                'not_necessary_witness':'phi=t+s+s^3/6 has p=1, q=1+s^2/2>0, E=0, but F_sss=1'},
        'eq34':{'literal_implicit_first_derivative':'D(z,P)*C-(P-1)-1=0, D=g/P^2-z+beta*g*(1+P)^2/P',
                'literal_implied_C':c34,'literal_implied_H':h34,
                'original_residual_at_implied_jet':sp.factor(derive_reduction('3.9')['residual'].subs({Z:1,P:sp.Rational(1,2),G:1,K:sp.Rational(1,30),C:c34,H:h34}, simultaneous=True)),
                'correct_integrand':'g/tau^2-alpha^2*tau+beta*g*(alpha3-alpha*tau)^(m-1)/tau',
                'note':'Even corrected integrand with coefficient 1 fixes first-integral constant I=-1; general I0 must be retained.'},
        'sample':{'m':3,'alpha':-1,'alpha3':1,'g':1,'kappa':'1/30',
                  'z':1,'P':'1/2','C':'1/10','Sigma':1,'M':1}}
    metadata = {
      'eq24':('refuted_as_printed','p.7 eq(24)','Literal displayed expanded beta terms; positive jet F=2,P=1/2,C=1/10'),
      'eq25':('refuted_as_printed','p.7 eq(25)','Displayed X5 third-order equation'),
      'eq26':('refuted_as_printed','p.7 eq(26)','Equation (25) with mu=phi_sigma, hence same failed zero'),
      'eq27':('refuted_as_printed','p.7 eq(27)','Displayed Abel-type polynomial RHS for M_Sigma'),
      'eq28':('refuted_as_printed','p.7 eq(28)','Traveling expanded equation with alpha=-1,m=3'),
      'eq29':('refuted_as_printed','p.8 eq(29)','Displayed mu second-order equation, alpha=-1,m=3'),
      'eq30':('refuted_as_printed','p.8 eq(30)','Displayed M_Xi/M logarithmic derivative'),
      'eq31':('refuted_as_printed','p.8 eq(31)','Displayed complex-form M(Xi), real cubic slice M0=1'),
      'eq32':('qualified','p.8 eq(32)','Quadratic F(s) is sufficient but not necessary for printed wrong 3.8 graph'),
      'eq33':('refuted_as_printed','p.8 eq(33)','Mixed traveling expanded equation alpha=-1,alpha3=1,m=3'),
      'eq34':('refuted_as_printed','p.9 eq(34)','Literal -alpha^2*kappa in integrand; lower limit P0=1')}
    for key,(status,source,printed) in metadata.items():
        data[key].update(source=source,printed=printed,
                         domain='g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample')
    nonzero = {'eq24':'original_residual_at_zero','eq25':'original_residual_at_zero',
               'eq26':'correct_mu_equation_at_zero','eq28':'original_residual_at_zero',
               'eq29':'original_residual_at_zero','eq31':'d_of_correct_integral_dP_at_sample',
               'eq33':'original_residual_at_zero','eq34':'original_residual_at_implied_jet'}
    for key,field in nonzero.items():
        data[key]['audit_verified']=sp.simplify(data[key][field]).is_zero is False
    for key,left,right in [('eq27','printed_Mprime_at_sample','correct_Mprime_at_sample'),
                           ('eq30','printed_Mprime_over_M_at_sample','correct_Mprime_over_M_at_sample')]:
        data[key]['audit_verified']=sp.simplify(data[key][left]-data[key][right]).is_zero is False
    # For witness jets chosen by solving a printed equation, check that zero too.
    for key,expression,point_here,hvalue in [
            ('eq24',source24,point24,h24),('eq25',source25,point,h25),
            ('eq26',source25,point,h25),('eq28',source28,point,h28),
            ('eq29',source29,point,h29),('eq33',source33,point,h33)]:
        zero=sp.simplify(expression.subs(point_here).subs(H,hvalue))
        data[key]['printed_residual_at_witness']=zero
        data[key]['audit_verified'] &= zero==0
    c0,c1,c2=sp.symbols('c0 c1 c2',real=True)
    quadratic=t+c0+c1*s+c2*s**2/2
    quadratic_jets={jet:sp.diff(quadratic,t,i,s,k) for (i,k),jet in JETS.items()}
    quadratic_residual=sp.simplify(master().subs(quadratic_jets,simultaneous=True))
    witness=translated_ansatz_witnesses()['3.8_wrong_graph_counterexample']
    data['eq32'].update(printed_quadratic_is_solution=quadratic_residual==0,
                        quadratic_residual=quadratic_residual,
                        audit_verified=(quadratic_residual==0 and witness['original_PDE']==0
                                        and witness['F_sss']!=0))
    for key in metadata:
        data[key]['status']=('qualified' if key=='eq32' else 'refuted_as_printed') if data[key]['audit_verified'] else 'unresolved'
    return data


# ========================================================================
# Sources
# ========================================================================
PACKAGE_ROOT = Path(__file__).resolve().parent

SOURCE_REL=Path('ref/main/Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables-mathematics-14-00433-v3.pdf')

METHOD_REL=Path('ref/Two parameters Liegroup analysis and numerical solution of unsteady free convective flow of non-Newtonian fluid.pdf')

REQUIRED_KEYS=[
    '[master equation]', '[infinitesimal generator]',
    '[Symmetries of the SVE Equation]',
    '[Commutators of the admitted Lie symmetries for the SVE equation]',
    '[listed Lie symmetries]', '[One-Dimensional Optimal System]',
    '[Similarity Transformations]',
    '[One dimensional optimal system and Lie invariants Table]',
    '[Solution ODE with all 9 reductions]', '[Numeric solutions to the ODEs]']

def equation_inventory():
    descriptions={
        1:'Eulerian mass balance',2:'Eulerian conservative momentum balance',
        3:'Exner bed balance',4:'Power-law sediment closure',
        5:'Lagrange momentum equation',6:'Printed Lagrange bed equation',
        7:'Printed third-order scalar master equation',
        8:'General PDE notation',9:'Infinitesimal time transformation',
        10:'Infinitesimal label transformation',11:'Infinitesimal field transformation',
        12:'General point infinitesimal generator',13:'Finite-to-infinitesimal invariance limit',
        14:'Prolonged infinitesimal criterion (on the equation manifold)',
        15:'Lie derivative of a scalar function',16:'First prolongation recursion',
        17:'Ellipsis in the displayed prolongation sequence',18:'Higher prolongation recursion',
        19:'Linear combinations of algebra basis elements',20:'Adjoint equivalence',
        21:'Nonzero generator rescaling',22:'Invariant characteristic equation',
        23:'Functions of invariants',24:'X4 reduced ODE',25:'X5 reduced ODE',
        26:'Derivative reduction of X5 ODE',27:'Claimed Abel equation',
        28:'Traveling-wave third-order ODE',29:'Traveling-wave derivative ODE',
        30:'Autonomous order reduction',31:'Claimed explicit reduced solution',
        32:'Claimed quadratic profile in subsection 3.8',
        33:'Shifted traveling-wave ODE',34:'Claimed implicit quadrature'}
    rows=[]
    for n in range(1,35):
        page=2 if n<=7 else 3 if n<=15 else 4 if n<=18 else 5 if n<=21 else 6 if n<=23 else 7 if n<=28 else 8 if n<=33 else 9
        owner='models' if n<=7 else 'symmetries' if n<=18 else 'algebra' if n<=21 else 'reductions'
        rows.append({'equation':n,'page':page,'description':descriptions[n],
                     'evidence_module':owner,'status':'pending_evidence'})
    return rows

def source_manifest(out_dir, repo_root=None):
    """Hash and extract available primary PDFs; record missing sources plainly."""
    try:
        import pymupdf
    except ImportError:
        pymupdf = None
    out_dir=Path(out_dir)
    dest=out_dir/'sources'
    dest.mkdir(parents=True,exist_ok=True)
    sources=[]
    roots = [Path(repo_root).resolve()] if repo_root is not None else [PACKAGE_ROOT, *PACKAGE_ROOT.parents]
    for source_id,rel,doi in [('SVE',SOURCE_REL,'10.3390/math14030433'),
                              ('RKF-reference',METHOD_REL,'10.1016/j.aej.2016.05.009')]:
        path=next((root/rel for root in roots if (root/rel).is_file()),None)
        record={'id':source_id,'path':rel.as_posix(),'doi':doi,
                'sha256':None,'pages':None,'verification':'source_unavailable',
                'accessed':datetime.now(timezone.utc).date().isoformat()}
        if path is not None:
            record['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            if pymupdf is not None:
                try:
                    with pymupdf.open(path) as doc:
                        extracted='\n\n'.join(f'=== PDF PAGE {i+1} ===\n'+page.get_text()
                                              for i,page in enumerate(doc))
                        record['pages']=len(doc)
                    (dest/f'{source_id}.txt').write_text(extracted,encoding='utf-8')
                    record['verification']='local_primary_pdf_checked'
                except Exception as exc:
                    record['verification']='pdf_extraction_failed'
                    record['error']=f'{type(exc).__name__}: {exc}'
            else:
                record['verification']='pdf_extractor_unavailable'
        sources.append(record)
    versions={}
    for name in ['sympy','numpy','scipy','matplotlib','pytest','pymupdf']:
        try: versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: versions[name]=None
    return {'sources':sources,
            'source_verification_complete':all(row['verification']=='local_primary_pdf_checked' for row in sources),
            'environment':{'python':sys.version,'platform':platform.platform(),'packages':versions},
            'method_scope':'Uddin et al. use RKF fourth-fifth order plus shooting for a different BVP; SVE initial data and algorithm tolerances here are newly specified.',
            'equations':equation_inventory(),'tables':[{'table':1,'page':5,'owner':'algebra'}, {'table':2,'page':5,'owner':'algebra'}, {'table':3,'page':6,'owner':'reductions'}]}


# ========================================================================
# Coverage
# ========================================================================
def build_coverage(evidence):
    rows=equation_inventory()
    witnesses=evidence.get('reductions',{}).get('source_witnesses',{})
    for row in rows:
        n=row['equation']
        if n<=4:
            row.update(status='model_assumption', evidence='models: coordinate pullback; the Eulerian balances and power closure are input assumptions, not empirical validation.')
        elif n==5:
            row.update(status='verified',evidence='models.checks.momentum_pullback_zero')
        elif n==6:
            row.update(status='corrected_under_declared_bed_pullback',evidence='models.discrepancies.D-MODEL-06; missing -(phi_t/phi_s)b_s')
        elif n==7:
            row.update(status='verified_for_printed_pair',evidence='models.checks.printed_compatibility_zero; source equation retained')
        elif n in (8,9,10,11,12,15,17,19,20,21):
            row.update(status='definition_reproduced',evidence=('symmetries and core.prolongation' if n<19 else 'algebra.formulas.adjoints and orbits'))
        elif n in (13,14):
            row.update(status='qualified',evidence='Use pr(X)E=0 ON E=0, or pr(X)E=lambda E off shell; the literal unconditional zero condition rejects scaling.')
        elif n in (16,18):
            row.update(status='verified',evidence='core.prolongation recursive formula; unrestricted determining split and direct polynomial substitution tests')
        elif n in (22,23):
            row.update(status='verified_on_recorded_charts',evidence='reductions.cases and table3_mixed: Q, invariant coordinates and complete jet pullbacks')
        else:
            witness=witnesses.get(f'eq{n}')
            if witness is None:
                row.update(status='unresolved',evidence=f'No source_witnesses.eq{n} result exists in this run.')
            else:
                row.update(status=witness.get('status','unresolved'),evidence=f'reductions.source_witnesses.eq{n}',detail=witness)
    extra=[
        {'source':'p.4 Proposition 1','status':'corrected','evidence':'symmetries.claims.maximal_classification; the m=1 stratum has X6=t*d_phi'},
        {'source':'p.4 printed determining system','status':'refuted_as_printed','evidence':'symmetries.discrepancies.printed_determining_X4_witness'},
        {'source':'pp.5-6 optimal system','status':'corrected','evidence':'algebra.formulas.orbits; missing projective/resonant families'},
        {'source':'p.7 reduced generators after (25) and (26)','status':'corrected',
         'printed':'3*sigma*d_sigma+phi*d_sigma and 3*sigma*d_sigma-2*mu*d_sigma',
         'derived':'3*sigma*d_sigma+phi*d_phi and 3*sigma*d_sigma-2*mu*d_mu',
         'evidence':'X4(s*t^2)=3*s*t^2 and X4(phi)=phi; prolongation to mu=phi_sigma gives mu-3*mu=-2*mu.'},
        {'source':'p.8 eight-generator/free-particle statement','status':'qualified','evidence':'corrected traveling derivative ODE has invertible Y(P)=Integral(B(P),dP) on B!=0, giving Y_second=0'},
        {'source':'pp.7-8 shock/nonsingular descriptions','status':'unsupported_as_global_claim','evidence':'local smooth-profile checks do not establish weak shock balances or global absence of singularities'},
        {'source':'p.9 variational Lagrangian','status':'author_reported_negative','evidence':'authors report not finding a formulation; no nonexistence proof follows'},
        {'source':'p.9 initial-value discussion','status':'source_text_inconsistent','evidence':'conclusion both says IVP was examined and later says it was not discussed; paper supplies no numerical initial data'}]
    return {'equations':rows,
            'tables':[{'table':1,'page':5,'status':'corrected','evidence':'algebra.formulas.brackets; two source sign errors'},
                      {'table':2,'page':5,'status':'verified','evidence':'algebra.formulas.adjoints; convention exp(-epsilon ad)'},
                      {'table':3,'page':6,'status':'qualified','evidence':'recorded invariants verified; alpha=-1 requires a separate chart and the list omits other orbit families'}],
            'unnumbered_claims':extra,
            'inventory_complete':len(rows)==34 and all(row['status']!='pending_evidence' for row in rows),
            'all_printed_claims_reproduced':False}


# ========================================================================
# Rkf45
# ========================================================================
FEHLBERG_C = (Q(0), Q(1, 4), Q(3, 8), Q(12, 13), Q(1), Q(1, 2))

FEHLBERG_A = (
    (), (Q(1, 4),), (Q(3, 32), Q(9, 32)),
    (Q(1932, 2197), Q(-7200, 2197), Q(7296, 2197)),
    (Q(439, 216), Q(-8), Q(3680, 513), Q(-845, 4104)),
    (Q(-8, 27), Q(2), Q(-3544, 2565), Q(1859, 4104), Q(-11, 40)),
)

FEHLBERG_B4 = (Q(25, 216), Q(0), Q(1408, 2565), Q(2197, 4104), Q(-1, 5), Q(0))

FEHLBERG_B5 = (Q(16, 135), Q(0), Q(6656, 12825), Q(28561, 56430), Q(-9, 50), Q(2, 55))

class _StageFailure(Exception):
    def __init__(self, status):
        self.status = status

@dataclass
class RKFResult:
    t: np.ndarray
    y: np.ndarray
    status: str
    n_steps: int
    n_rejected: int
    nfev: int
    message: str

def _stage(fun, t, y, guard):
    if not np.all(np.isfinite(y)) or not np.isfinite(t):
        raise _StageFailure('nonfinite_stage')
    if guard is not None and not guard(t, y):
        raise _StageFailure('guard_stop')
    value = np.asarray(fun(t, y), dtype=float)
    if value.shape != y.shape or not np.all(np.isfinite(value)):
        raise _StageFailure('nonfinite_stage')
    return value

def _rkf45_step(fun, t, y, h, guard=None):
    stages = []
    for i in range(6):
        trial = y + h * sum((float(a) * stages[j] for j, a in enumerate(FEHLBERG_A[i])), np.zeros_like(y))
        stages.append(_stage(fun, t + float(FEHLBERG_C[i]) * h, trial, guard))
    y4 = y + h * sum((float(b) * stages[i] for i, b in enumerate(FEHLBERG_B4)), np.zeros_like(y))
    y5 = y + h * sum((float(b) * stages[i] for i, b in enumerate(FEHLBERG_B5)), np.zeros_like(y))
    return y4, y5, y5 - y4

def rkf45_step(fun, t, y, h):
    """Return fourth estimate, accepted fifth estimate, and embedded difference."""
    return _rkf45_step(fun, float(t), np.asarray(y, dtype=float), float(h))

def solve_ivp_rkf45(fun, t_span, y0, *, t_eval=None, rtol=1e-9, atol=1e-11,
                    first_step=None, min_step=1e-14, max_step=np.inf,
                    max_steps=100000, max_rejections=10000, guard=None):
    t0, end = map(float, t_span)
    y = np.atleast_1d(np.asarray(y0, dtype=float)).copy()
    if y.ndim != 1 or not np.all(np.isfinite(y)) or not np.isfinite([t0, end]).all():
        raise ValueError('finite scalar interval and finite one-dimensional initial state required')
    if end <= t0 or rtol <= 0 or atol <= 0 or min_step <= 0 or max_step <= 0:
        raise ValueError('positive forward interval, tolerances and step bounds required')
    if max_steps < 1 or max_rejections < 0:
        raise ValueError('invalid iteration limits')
    targets = None if t_eval is None else np.asarray(t_eval, dtype=float)
    if targets is not None and (targets.ndim != 1 or len(targets) == 0 or
            targets[0] < t0 or targets[-1] > end or np.any(np.diff(targets) <= 0)):
        raise ValueError('t_eval must be strictly increasing within t_span')
    h = min(float(first_step) if first_step is not None else (end - t0) / 20,
            max_step, end - t0)
    if h <= 0:
        raise ValueError('first_step must be positive')
    ts, ys = [t0], [y.copy()]
    t, steps, rejected, nfev = t0, 0, 0, 0

    def counted_rhs(stage_t, stage_y):
        nonlocal nfev
        nfev += 1
        return fun(stage_t, stage_y)

    next_target = 0
    if targets is not None and targets[0] == t0:
        next_target = 1
    status = 'completed'
    while t < end:
        if steps >= max_steps:
            status = 'step_limit'
            break
        target = end if targets is None or next_target >= len(targets) else targets[next_target]
        if target <= t:
            next_target += 1
            continue
        trial_h = min(h, target - t, end - t)
        if trial_h < min_step and target - t > 16 * np.spacing(t):
            status = 'step_underflow'
            break
        if t + trial_h == t:
            status = 'step_underflow'
            break
        try:
            y4, y5, diff = _rkf45_step(counted_rhs, t, y, trial_h, guard)
            if not np.all(np.isfinite(y5)) or not np.all(np.isfinite(diff)):
                raise _StageFailure('nonfinite_stage')
            if guard is not None and not guard(t + trial_h, y5):
                raise _StageFailure('guard_stop')
        except _StageFailure as failure:
            status = failure.status
            break
        scale = atol + rtol * np.maximum(np.abs(y), np.abs(y5))
        error = float(np.sqrt(np.mean((diff / scale) ** 2)))
        factor = 5.0 if error == 0 else float(np.clip(0.9 * error ** (-1 / 5), 0.2, 5.0))
        if error <= 1:
            t = target if abs((t + trial_h) - target) <= 8 * np.spacing(target) else t + trial_h
            y = y5
            steps += 1
            if targets is None or t == target:
                ts.append(t)
                ys.append(y.copy())
            if targets is not None and t == target:
                next_target += 1
        else:
            rejected += 1
            if rejected > max_rejections:
                status = 'rejection_limit'
                break
        h = min(max_step, trial_h * factor)
    if targets is not None and status == 'completed' and next_target != len(targets):
        status = 'incomplete_grid'
    return RKFResult(np.asarray(ts), np.stack(ys, axis=1), status, steps, rejected,
                     nfev, status)


# ========================================================================
# Numerics
# ========================================================================


NON_NUMERICAL = ('3.1', '3.2', '3.3', '3.7', 'table3-mixed')


_OFFSETS = np.arange(-4, 5, dtype=float)

def _weights(order):
    powers = np.arange(9)
    matrix = _OFFSETS[None, :] ** powers[:, None]
    target = np.zeros(9)
    target[order] = float(sp.factorial(order))
    return np.linalg.solve(matrix, target)

_W = {degree: _weights(degree) for degree in range(4)}

def original_pde_residual(phi, t, s, *, m, h, g=G, kappa=KAPPA):
    """Differentiate reconstructed phi in both original coordinates.

    The 9-by-9 tensor stencil differentiates phi itself; no reduced ODE
    residual or formula for F''' is inserted in this diagnostic.
    """
    if h <= 0:
        raise ValueError('h must be positive')
    values = np.array([[phi(t + i*h, s + k*h) for k in _OFFSETS]
                       for i in _OFFSETS], dtype=float)
    if not np.all(np.isfinite(values)):
        return {'residual': float('nan'), 'velocity': float('nan'),
                'gradient': float('nan'), 'h': h}

    def d(i, k):
        return float(_W[i] @ values @ _W[k] / h**(i+k))

    p, q = d(1, 0), d(0, 1)
    a, b, c = d(2, 0), d(1, 1), d(0, 2)
    r, x = d(3, 0), d(1, 2)
    if p <= 0 or q <= 0:
        return {'residual': float('nan'), 'velocity': p,
                'gradient': q, 'h': h}
    inertial_t = b*a + q*r - g*(x/q**2 - 2*c*b/q**3)
    flux_s = m*kappa*((m-1)*p**(m-2)*b*b/q +
                       p**(m-1)*x/q - p**(m-1)*b*c/q**2)
    return {'residual': float(inertial_t-g*flux_s),
            'velocity': p, 'gradient': q, 'h': h}

def _selection(value, choices, name):
    if value == 'all':
        return choices
    if name == 'selected_case':
        try:
            selected = float(value)
        except (ValueError, TypeError) as exc:
            raise ValueError('selected_case must be one of 1, 1.5, 2, 3, 4 or all') from exc
        if selected not in choices:
            raise ValueError('unsupported exponent')
        return (selected,)
    if str(value) not in choices:
        raise ValueError('unsupported reduction')
    return (str(value),)

def _functions(reduction, exponent):
    substitutions = {g: G, kappa: KAPPA, m: exponent}
    args = (z, F, P, C)
    rhs_expr = reduction['rhs'].subs(substitutions)
    lead_expr = reduction['leading'].subs(substitutions)
    vel_expr = reduction['velocity'].subs(substitutions)
    grad_expr = reduction['gradient'].subs(substitutions)
    return tuple(sp.lambdify(args, expr, modules='numpy') for expr in
                 (rhs_expr, lead_expr, vel_expr, grad_expr))

def _coordinate_and_ansatz(reduction):
    coord = sp.lambdify((t, s), reduction['coordinate'], modules='numpy')
    ansatz = sp.lambdify((t, s, F), reduction['ansatz'], modules='numpy')
    return coord, ansatz

def _profile_guard(functions, deadline):
    _, lead, vel, grad = functions

    def check(z, y):
        if time.monotonic() > deadline or not np.all(np.isfinite(y)):
            return False
        try:
            v, q, coeff = float(vel(z, *y)), float(grad(z, *y)), float(lead(z, *y))
            return np.isfinite([v, q, coeff]).all() and v > 1e-9 and q > 1e-9 and abs(coeff) > 1e-10
        except (ValueError, FloatingPointError, OverflowError):
            return False
    return check

def _geometry(case, z):
    if case == '3.8':
        return z, 1.0
    if case in ('3.6', '3.9'):
        return 1.0, z - 1.0
    return 1.0, z

def _integral_drift(reduction, grid, states, exponent):
    step = next((entry for entry in reduction['steps']
                 if entry['label'] == 'first-integral density'), None)
    if step is None:
        return {'status': 'no_certified_integral', 'scaled_drift': None}
    expr = step['expression'].subs({g: G, kappa: KAPPA, m: exponent})
    f = sp.lambdify((z, F, P, C), expr, modules='numpy')
    values = np.array([f(zi, *state) for zi, state in zip(grid, states.T)], dtype=float)
    drift = float(np.max(np.abs(values-values[0])) / max(1.0, abs(values[0])))
    return {'status': 'passed' if drift <= 1e-7 else 'failed',
            'scaled_drift': drift, 'initial': float(values[0])}

def _rkf_interpolant(grid, states):
    width = min(12, len(grid))
    interpolators = [BarycentricInterpolator(grid[i:i+width], states[0, i:i+width], rng=0)
                     for i in range(len(grid)-width+1)]

    def evaluate(z):
        start = int(np.clip(np.searchsorted(grid, z)-width//2, 0,
                            len(interpolators)-1))
        return np.array([float(interpolators[start](z))])
    return evaluate

def _pde_check(reduction, dense, interval, case, exponent):
    coord, ansatz = _coordinate_and_ansatz(reduction)

    def phi(t, s):
        z = float(coord(t, s))
        if z < interval[0]-1e-12 or z > interval[1]+1e-12:
            raise ValueError('stencil left integrated profile interval')
        return float(ansatz(t, s, float(dense(z)[0])))

    points = np.linspace(interval[0]+0.45*(interval[1]-interval[0]),
                         interval[1]-0.45*(interval[1]-interval[0]), 3)
    refinements = []
    for h in (0.003, 0.002, 0.001):
        samples = [original_pde_residual(phi, *_geometry(case, z), m=exponent, h=h)
                   for z in points]
        refinements.append({'h': h,
                            'max_abs_residual': float(max(abs(x['residual']) for x in samples)),
                            'min_velocity': float(min(x['velocity'] for x in samples)),
                            'min_gradient': float(min(x['gradient'] for x in samples))})
    floor = min(x['max_abs_residual'] for x in refinements)
    acceptance = refinements[0]['max_abs_residual']
    min_v = min(x['min_velocity'] for x in refinements)
    min_q = min(x['min_gradient'] for x in refinements)
    z = (interval[0]+interval[1])/2
    t0, s0 = _geometry(case, z)
    baseline = original_pde_residual(phi, t0, s0, m=exponent, h=0.003)['residual']
    perturbed = original_pde_residual(lambda t, s: phi(t, s)+0.001*t**3,
                                      t0, s0, m=exponent, h=0.003)['residual']
    negative = {'baseline': baseline, 'perturbed': perturbed,
                'absolute_change': abs(perturbed-baseline),
                'passed': bool(np.isfinite(perturbed) and abs(perturbed-baseline) > 1e-4),
                'perturbation': 'phi + 0.001*t^3'}
    result = {'status': 'passed' if np.isfinite(acceptance) and acceptance <= 1e-6 and
            min_v > 0 and min_q > 0 else 'failed',
            'acceptance_h': 0.003, 'acceptance_max_abs_residual': acceptance,
            'error_floor': floor, 'refinements': refinements,
            'min_velocity': min_v, 'min_gradient': min_q,
            'stencil': 'nine-point tensor finite differences of reconstructed phi'}
    return result, negative

def _second_order_check(reduction, grid, third_order, y0, exponent):
    step = next((entry for entry in reduction['steps']
                 if entry['label'] == 'first-integral density'), None)
    if reduction['id'] != '3.4' or step is None:
        return {'status': 'not_applicable', 'scaled_disagreement': None}
    expr = step['expression'].subs({g: G, kappa: KAPPA, m: exponent})
    coefficient = sp.diff(expr, C)
    coefficient_fn = sp.lambdify((z, F, P), coefficient, modules='numpy')
    integral0 = float(sp.lambdify((z,F,P,C),expr,modules='numpy')(grid[0],*y0))
    def second(z, state):
        coeff = float(coefficient_fn(z, *state))
        if not np.isfinite(coeff) or abs(coeff) <= 1e-10:
            raise ValueError('second-order first-integral denominator crossed zero')
        return [state[1], integral0/coeff]
    solution = solve_ivp(second, (grid[0],grid[-1]), y0[:2], method='DOP853',
                         t_eval=grid, rtol=1e-12, atol=1e-14, max_step=0.01)
    if not solution.success:
        return {'status': 'failed', 'message': solution.message,
                'scaled_disagreement': None}
    error = float(np.max(np.abs(solution.y-third_order[:2])/
                         np.maximum(1, np.abs(third_order[:2]))))
    return {'status': 'passed' if error <= 1e-7 else 'failed',
            'scaled_disagreement': error, 'integral_constant': integral0}

def _write_plot(path, z, states, case, exponent):
    fig, ax = plt.subplots(figsize=(7.2, 4.0), layout='constrained')
    for values, label, color in zip(states, ('F', "F'", "F''"),
                                    ('#175a79', '#ba5a37', '#36855c')):
        ax.plot(z, values, lw=2, label=label, color=color)
    ax.set(xlabel='reduced coordinate', ylabel='profile / jet',
           title=f'Reduction {case} | m = {exponent:g}')
    ax.grid(alpha=.18)
    ax.legend(frameon=False, ncol=3)
    fig.savefig(path, dpi=160)
    plt.close(fig)

def run_campaign(out_dir, rtol=1e-9, atol=1e-11,
                 selected_reduction='all', selected_case='all'):
    """Run dimensionless IVPs; every failed gate remains explicit in the report."""
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    selected = _selection(selected_reduction, CASES+NON_NUMERICAL, 'selected_reduction')
    exponents = _selection(selected_case, EXPONENTS, 'selected_case')
    runs = []
    non_numerical = []
    campaign_deadline = time.monotonic() + 600
    for case in selected:
        if case in NON_NUMERICAL:
            item = derive_reduction(case, exponent=3)
            non_numerical.append({'case': case, 'status':
                'symbolic_only_companion' if case == 'table3-mixed' else item['status'],
                'reason': 'no regular positive-branch IVP in this campaign'})
            continue
        for exponent in exponents:
            if case == '3.5' and exponent != 3:
                non_numerical.append({'case': case, 'm': exponent,
                    'status': 'incompatible_exponent',
                    'reason': 'X5 is a symmetry only at m=3'})
                continue
            row = {'case': case, 'm': exponent, 'model': 'printed scalar',
                   'g': G, 'kappa': KAPPA, 'beta': exponent*KAPPA}
            runs.append(row)
            if time.monotonic() > campaign_deadline:
                row['status'] = 'campaign_time_limit'
                continue
            try:
                reduction = derive_reduction(case, exponent=sp.Rational(str(exponent)),
                                             alpha=-1 if case != '3.8' else 1, alpha3=1)
                row['equation_sha256'] = _ode_fingerprint(reduction)
                interval, y0 = NUMERICAL_CASE_SETTINGS[case]
                row['interval'], row['initial_jet'] = interval, y0
                functions = _functions(reduction, exponent)
                guard = _profile_guard(functions, min(campaign_deadline, time.monotonic()+25))
                rhs = lambda z, state: np.array([state[1], state[2],
                                                 float(functions[0](z, *state))], dtype=float)
                grid = np.linspace(*interval, 81)
                rkf = solve_ivp_rkf45(rhs, interval, y0, t_eval=grid,
                                      rtol=rtol, atol=atol, max_steps=20000,
                                      max_rejections=2000, guard=guard)
                row['solver'] = {'status': rkf.status, 'steps': rkf.n_steps,
                                 'rejected': rkf.n_rejected, 'nfev': rkf.nfev}
                if rkf.status != 'completed':
                    row['status'] = 'solver_failed'
                    continue
                tighter = solve_ivp_rkf45(rhs, interval, y0, t_eval=grid,
                    rtol=rtol/10, atol=atol/10, max_steps=30000,
                    max_rejections=3000, guard=guard)
                if tighter.status != 'completed':
                    row['status'] = 'tight_solver_failed'
                    row['solver']['tight_status'] = tighter.status
                    continue
                length = interval[1]-interval[0]
                ladder = [solve_ivp_rkf45(rhs, interval, y0,
                    first_step=cap, max_step=cap,
                    rtol=tol, atol=absolute, max_steps=30000,
                    max_rejections=3000, guard=guard)
                    for tol, absolute, cap in ((rtol, atol, length/2),
                                               (rtol/10, atol/10, length/4))]
                if any(item.status != 'completed' for item in ladder):
                    row['status'] = 'ladder_solver_failed'
                    row['solver']['ladder_statuses'] = [item.status for item in ladder]
                    continue
                tight_disagreement = float(np.max(np.abs(ladder[0].y[:,-1]-ladder[1].y[:,-1])/
                    np.maximum(1, np.abs(ladder[1].y[:,-1]))))
                row['solver']['tight_ladder_disagreement'] = tight_disagreement
                row['solver']['ladder_steps'] = [item.n_steps for item in ladder]
                row['solver']['ladder_times'] = [item.t.tolist() for item in ladder]
                distinct = not np.array_equal(ladder[0].t, ladder[1].t)
                row['solver']['ladder_distinct_history'] = bool(distinct)
                row['solver']['ladder_interpretation'] = (
                    'roundoff_level_control' if tight_disagreement <= 1e-13 else
                    'finite_step_comparison')
                reference = solve_ivp(rhs, interval, y0, method='DOP853',
                                      t_eval=grid, dense_output=True,
                                      rtol=min(rtol/100, 1e-12),
                                      atol=min(atol/100, 1e-14), max_step=0.01)
                if not reference.success:
                    row['status'] = 'reference_failed'
                    row['reference_message'] = reference.message
                    continue
                disagreement = float(np.max(np.abs(rkf.y-reference.y)/
                                            np.maximum(1, np.abs(reference.y))))
                row['solver']['scaled_disagreement'] = disagreement
                if case == '3.8':
                    dt = grid-interval[0]
                    expected = np.vstack((y0[0]+y0[1]*dt+0.5*y0[2]*dt**2,
                                          y0[1]+y0[2]*dt,
                                          np.full_like(grid, y0[2])))
                    quadratic_error = float(np.max(np.abs(rkf.y-expected)))
                    row['exact_quadratic'] = {
                        'status': 'passed' if quadratic_error <= 1e-10 else 'failed',
                        'max_abs_error': quadratic_error,
                        'formula': 'F=F0+P0*(t-t0)+C0*(t-t0)^2/2'}
                else:
                    row['exact_quadratic'] = {'status': 'not_applicable',
                                               'max_abs_error': None}
                row['integral'] = _integral_drift(reduction, rkf.t, rkf.y, exponent)
                row['second_order'] = _second_order_check(reduction, grid, rkf.y, y0, exponent)
                row['pde'], row['negative_control'] = _pde_check(
                    reduction, reference.sol, interval, case, exponent)
                row['pde']['trajectory'] = 'DOP853 reference reconstruction'
                rkf_pde, _ = _pde_check(reduction, _rkf_interpolant(grid, tighter.y),
                                       interval, case, exponent)
                rkf_pde['trajectory'] = 'tight RKF45 local degree-11 interpolation'
                row['rkf_pde'] = rkf_pde
                margins = np.array([[float(fn(z, *state)) for z, state in zip(grid, rkf.y.T)]
                                    for fn in functions[1:]], dtype=float)
                row['branch'] = {'min_velocity': float(np.min(margins[1])),
                                 'min_gradient': float(np.min(margins[2])),
                                 'min_abs_leading': float(np.min(np.abs(margins[0]))),
                                 'sample_count': len(grid)}
                stem = f"{case.replace('.', '-')}-m{str(exponent).replace('.', 'p')}"
                csv_path, plot_path = output / f'{stem}.csv', output / f'{stem}.png'
                with csv_path.open('w', newline='', encoding='utf-8') as handle:
                    writer = csv.writer(handle)
                    writer.writerow(('z', 'F_rkf45', 'P_rkf45', 'C_rkf45',
                                     'F_dop853', 'P_dop853', 'C_dop853'))
                    writer.writerows(zip(grid, *rkf.y, *reference.y))
                _write_plot(plot_path, grid, rkf.y, case, exponent)
                row['csv'], row['plot'] = str(csv_path), str(plot_path)
                row['csv_sha256'] = hashlib.sha256(csv_path.read_bytes()).hexdigest()
                gates = (disagreement <= 1e-7, tight_disagreement <= 1e-7,
                         distinct, row['exact_quadratic']['status'] != 'failed',
                         row['pde']['status'] == 'passed',
                         row['rkf_pde']['status'] == 'passed',
                         row['negative_control']['passed'],
                         row['integral']['status'] != 'failed',
                         row['second_order']['status'] != 'failed',
                         row['branch']['min_abs_leading'] > 1e-10,
                         row['branch']['min_velocity'] > 0,
                         row['branch']['min_gradient'] > 0)
                row['status'] = 'passed' if all(gates) else 'failed_gate'
            except (ValueError, ZeroDivisionError, OverflowError, FloatingPointError) as exc:
                row['status'] = 'unresolved_exception'
                row['error'] = f'{type(exc).__name__}: {exc}'
    report = {'settings': {'rtol': rtol, 'atol': atol,
                           'rkf_tableau': 'classic six-stage Fehlberg 4(5)',
                           'reference': 'SciPy DOP853, independent comparator',
                           'pde_gate': 1e-6, 'solver_and_integral_gate': 1e-7},
              'runs': runs, 'non_numerical': non_numerical,
              'all_passed': bool(runs) and all(r['status'] == 'passed' for r in runs)}
    (output / 'numerics.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    return report


# ========================================================================
# Reporting
# ========================================================================
def _bracket_table(brackets,names):
    parts=['| [row, column] | '+' | '.join(names)+' |',
           '|---|'+'---|'*len(names)]
    for a in names:
        cells=[]
        for b in names:
            terms=brackets.get(f'[{a},{b}]',{})
            cells.append(' + '.join(f'{v} {k}' for k,v in terms.items()) or '0')
        parts.append('| '+a+' | '+' | '.join(cells)+' |')
    return '\n'.join(parts)+'\n'

def _invariant_table(reductions):
    parts=['| Source row | Invariant coordinate | Invariant graph (F is evaluated at that coordinate) | Outcome |',
           '|---|---|---|---|']
    rows=list(reductions.get('cases',[]))
    if reductions.get('table3_mixed'):rows.append(reductions['table3_mixed'])
    for row in rows:
        parts.append(f'| {row["id"]} | `{row.get("coordinate")}` | `{row.get("ansatz")}` | {row["status"]} |')
    return '\n'.join(parts)+'\n'

def _render(value, level=3):
    if isinstance(value,dict):
        parts=[]
        for key,item in value.items():
            parts.append(f'{"#"*min(level,6)} {key.replace("_"," ")}\n')
            parts.append(_render(item,level+1))
        return '\n'.join(parts)
    if isinstance(value,list):
        if not value:
            return '(none)\n'
        return '\n'.join(_render(item,level) for item in value)
    if value is None:
        return 'Not applicable / not supplied.\n'
    text=str(value)
    if '\n' in text or len(text)>140 or any(x in text for x in ['**','Derivative(','Subs(']):
        return f'```text\n{text}\n```\n'
    return f'{text}\n'

def write_report(evidence,out_dir):
    out_dir=Path(out_dir)
    out_dir.mkdir(parents=True,exist_ok=True)
    evidence=jsonable(evidence)
    (out_dir/'evidence.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding='utf-8')
    model=evidence.get('models',{})
    sym=evidence.get('symmetries',{})
    algebra=evidence.get('algebra',{})
    reductions=evidence.get('reductions',{})
    numerical=evidence.get('numerics',{})
    sections=[model,
        {'general_point_generator':'X=tau(t,s,phi)*d_t+xi(t,s,phi)*d_s+eta(t,s,phi)*d_phi',
         'invariant_graph_characteristic':'Q=eta-tau*phi_t-xi*phi_s',
         'prolongation_recursion':'eta_(J,i)=D_i eta_J-phi_(J,t)D_i tau-phi_(J,s)D_i xi',
         'criterion':'pr^(3)X(E)=0 on E=0; a nonzero multiple of E is permitted off-shell.'},
        sym,algebra.get('formulas',{}).get('brackets',{}),
        {'source_four':'X1=d_t; X2=d_s; X3=d_phi; X4=t*d_t+s*d_s+phi*d_phi',
         'source_cubic_extra':'X5=t*d_t-2*s*d_s (m=3)',
         'additional_verified_endpoint':'X6=t*d_phi (m=1)',
         'classification':sym.get('claims',{}),
         'scope':sym.get('scope',sym.get('classification_status','See symmetry evidence above.'))},
        algebra,
        {'lagrangian_statement':model.get('lagrangian_statement',''),
         'method':'Solve Q=0, verify invariant chart, substitute every jet into original E. Dimension reduction and subsequent ODE order reduction are distinct.',
         'details':'See the per-case steps and further-reduction evidence below.'},
        reductions.get('invariants',reductions.get('invariant_table',{})),
        reductions,numerical]
    parts=['# Reproduction and independent audit of the scalar SVE paper\n',
           'This report distinguishes paper statements, exact checks, corrected results, and unresolved claims. '
           'Numerical IVPs are new constructed dimensionless examples. A successful execution does not certify every source claim.\n',
           '## Run status\n',_render(evidence.get('run',{})),
           '## Sources and complete equation inventory\n',_render(evidence.get('source_manifest',{}))]
    for index,(title,content) in enumerate(zip(REQUIRED_KEYS,sections)):
        parts.append(f'## {title}\n')
        if index==3:
            formulas=algebra.get('formulas',{})
            parts.extend(['Cubic stratum (the generic algebra is the X1--X4 block):\n',
                          _bracket_table(formulas.get('brackets',{}),['X1','X2','X3','X4','X5']),
                          'Endpoint m=1:\n',
                          _bracket_table(formulas.get('m1_brackets',{}),['X1','X2','X3','X4','X6'])])
        elif index==7:
            parts.append(_invariant_table(reductions))
        else:
            parts.append(_render(content))
    if 'series' in evidence:
        parts.extend(['## Local analytic existence and ODE series\n',
                      _render(evidence['series'])])
    parts.append('## Detailed derivations and discrepancy explanations\n')
    docs=PACKAGE_ROOT/'docs'
    if docs.exists():
        for path in sorted(docs.glob('*.md')):
            if 'REVIEW' in path.name.upper():
                continue
            parts.extend([f'### {path.name}\n',path.read_text(encoding='utf-8')])
    (out_dir/'REPORT.md').write_text('\n'.join(parts),encoding='utf-8')
    script_path=Path(__file__).resolve()
    code_hashes={script_path.name:hashlib.sha256(script_path.read_bytes()).hexdigest()}
    (out_dir/'code_manifest.json').write_text(json.dumps(code_hashes,indent=2),encoding='utf-8')
    return out_dir/'REPORT.md'

def print_steps(label,steps,stream):
    stream.write(f'\n{label}\n')
    for i,step in enumerate(steps,1):
        if isinstance(step,dict):
            text=step.get('expression',step.get('result',step))
            stream.write(f'  {i:02d}. {step.get("label",step.get("step","calculation"))}\n      {text}\n')
        else:
            stream.write(f'  {i:02d}. {step}\n')
    stream.flush()


# Local Taylor series of corrected similarity ODEs
def _series_rational(value):
    """Recover exact small rational inputs from the declared decimal IVP data."""
    if isinstance(value, (float,sp.Float)):
        original = float(value)
        if not math.isfinite(original):
            raise ValueError('series parameters and initial jets must be finite')
        decimal = sp.Rational(str(value))
        candidate = decimal.limit_denominator(1_000_000)
        return candidate if float(candidate) == original else decimal
    result = sp.sympify(value)
    if result.is_Rational:
        return result
    raise ValueError('series parameters and initial jets must be rational numbers')


def _series_coefficients(expr, jets, degree):
    """Truncated exact Taylor arithmetic for rational-power expressions."""
    zeros = (sp.Integer(0),)*(degree+1)
    one = (sp.Integer(1),)+zeros[1:]

    def multiply(left,right):
        return tuple(sum((left[k]*right[n-k] for k in range(n+1)),
                         sp.Integer(0)) for n in range(degree+1))

    @lru_cache(maxsize=None)
    def evaluate(node):
        if node in jets:
            return tuple(jets[node][:degree+1]) + zeros[:max(0,degree+1-len(jets[node]))]
        if node.is_Number:
            return (node,)+zeros[1:]
        if node.is_Add:
            terms = [evaluate(arg) for arg in node.args]
            return tuple(sum((term[n] for term in terms),sp.Integer(0))
                         for n in range(degree+1))
        if node.is_Mul:
            result = one
            for arg in node.args:
                result = multiply(result,evaluate(arg))
            return result
        if node.is_Pow and node.exp.is_Rational:
            base = evaluate(node.base)
            power = node.exp
            if power.is_Integer and power >= 0:
                result = one
                for _ in range(int(power)):
                    result = multiply(result,base)
                return result
            if base[0] == 0:
                raise ValueError('series expression has a singular power at its center')
            normalized = (sp.Integer(0),)+tuple(base[i]/base[0]
                                                  for i in range(1,degree+1))
            result, term = one, one
            for k in range(1,degree+1):
                term = multiply(term,normalized)
                result = tuple(result[i]+sp.binomial(power,k)*term[i]
                               for i in range(degree+1))
            return tuple(base[0]**power*value for value in result)
        raise ValueError(f'unsupported series expression node: {node}')

    return tuple(sp.simplify(value) for value in evaluate(sp.sympify(expr)))


def compute_ode_series(case, exponent=3, order=6, *, z0=None,
                       initial_jet=None, g_value=None, kappa_value=None,
                       alpha=None, alpha3=None):
    """Exact degree-order Taylor polynomial for a corrected regular profile ODE.

    Coefficient n multiplies (z-z0)**n. Exceptional rows are typed, never
    divided through a singular leading coefficient.
    """
    case = str(case)
    if case not in tuple(f'3.{i}' for i in range(1,10)):
        raise ValueError('case must be one of 3.1 through 3.9')
    if type(order) is not int or not 3 <= order <= 8:
        raise ValueError('series order must be an integer from 3 through 8')
    exponent = _series_rational(exponent)
    alpha = _series_rational((1 if case in ('3.7','3.8') else -1)
                             if alpha is None else alpha)
    alpha3 = _series_rational((0 if case=='3.6' else 1)
                              if alpha3 is None else alpha3)
    gv = _series_rational(G if g_value is None else g_value)
    kv = _series_rational(KAPPA if kappa_value is None else kappa_value)
    default_interval, default_jet = NUMERICAL_CASE_SETTINGS.get(
        case, ((1.0, 1.1), (2.0, 0.5, 0.1)))
    z0 = _series_rational(default_interval[0] if z0 is None else z0)
    if initial_jet is None:
        initial_jet = default_jet
    if len(initial_jet) != 3:
        raise ValueError('initial_jet must contain F, F_prime, F_double_prime')
    f0,p0,c0 = map(_series_rational, initial_jet)
    result = {'case':case,'m':exponent,'order':order,'z0':z0,
              'initial_jet':(f0,p0,c0),'g':gv,'kappa':kv,
              'alpha':alpha,'alpha3':alpha3,'polynomial':None,
              'coefficients':[],'verification':None,'leading_at_initial':None,
              'assumptions':['printed scalar equation','real local chart'],
              'local_existence':None}
    if exponent < 1 or gv <= 0 or kv <= 0:
        return dict(result,status='incompatible_parameter',
                    reason='requires m>=1, g>0, kappa>0')
    if case == '3.5' and exponent != 3:
        return dict(result,status='incompatible_parameter',
                    reason='X5 reduces the fixed-m equation only at m=3')
    if case == '3.6' and alpha3 != 0:
        return dict(result,status='incompatible_parameter',
                    reason='3.6 has alpha3=0; nonzero alpha3 is row 3.9')
    if case == '3.1':
        return dict(result,status='outside_positive_chart',
                    reason='stationary phi=F(s) has phi_t=0; arbitrary stationary profiles form an identity family outside p>0')
    if case == '3.2':
        return dict(result,status='undefined_chart',
                    reason='phi_s=0 makes the printed scalar PDE undefined')
    if case == '3.3':
        return dict(result,status='no_invariant_graph',
                    reason='vertical translation requires the impossible graph equation 1=0')
    if case in ('3.6','3.9') and alpha == 0:
        if case == '3.6' or alpha3 <= 0 or p0 <= 0:
            return dict(result,status='outside_positive_chart',
                        reason='alpha=0 is an identity family but positive velocity and gradient are not both satisfied')
        return dict(result,status='identity_family',
                    reason='alpha=0 gives phi=alpha3*t+F(s); arbitrary analytic F with F_prime>0 is allowed')
    if case == '3.7':
        if alpha > 0 and p0 > 0:
            return dict(result,status='identity_family',
                        reason='phi=alpha*t+F(s) is an identity; any local analytic F with F_prime>0 is allowed, not a unique recurrence')
        return dict(result,status='outside_positive_chart',
                    reason='identity graph requires alpha>0 and F_prime>0')
    if case == '3.8' and alpha == 0:
        return dict(result,status='undefined_chart',
                    reason='phi_s=alpha=0 makes the printed scalar PDE undefined')
    reduction = derive_reduction(case,exponent=exponent,alpha=alpha,alpha3=alpha3)
    at = {z:z0,F:f0,P:p0,C:c0,g:gv,kappa:kv}
    velocity = sp.simplify(reduction['velocity'].subs(at))
    gradient = sp.simplify(reduction['gradient'].subs(at))
    leading = sp.simplify(reduction['leading'].subs(at))
    result.update(velocity_at_initial=velocity,gradient_at_initial=gradient,
                  leading_at_initial=leading)
    if velocity <= 0 or gradient <= 0:
        return dict(result,status='outside_positive_chart',
                    reason='initial jet violates phi_t>0 or phi_s>0')
    if leading == 0:
        return dict(result,status='normal_form_singular',
                    reason='F_triple_prime coefficient vanishes; no division or nonexistence claim')
    h = sp.Symbol('h',real=True)
    rhs = sp.cancel(reduction['rhs'].subs({g:gv,kappa:kv}))
    coefficients = [f0,p0,c0/2]
    recurrence = []
    for n in range(order-2):
        jets = {z:(z0,sp.Integer(1)),F:tuple(coefficients),
                P:tuple(i*coefficients[i] for i in range(1,len(coefficients))),
                C:tuple(i*(i-1)*coefficients[i] for i in range(2,len(coefficients)))}
        rhs_coefficient = _series_coefficients(rhs,jets,n)[n]
        degree = n+3
        coefficient = sp.factor(rhs_coefficient/(degree*(degree-1)*(degree-2)))
        coefficients.append(coefficient)
        recurrence.append({'degree':degree,'rhs_coefficient':rhs_coefficient,
                           'coefficient':coefficient})
    polynomial = sp.expand(sum(coefficients[i]*h**i for i in range(order+1)))
    residual = reduction['residual'].subs({g:gv,kappa:kv})
    jets = {z:(z0,sp.Integer(1)),F:tuple(coefficients),
            P:tuple(i*coefficients[i] for i in range(1,len(coefficients))),
            C:tuple(i*(i-1)*coefficients[i] for i in range(2,len(coefficients))),
            H:tuple(i*(i-1)*(i-2)*coefficients[i]
                    for i in range(3,len(coefficients)))}
    residual_coefficients = list(_series_coefficients(residual,jets,order-3))
    passed = all(value == 0 for value in residual_coefficients)
    result.update(status='regular_analytic_germ' if passed else 'verification_failed',
        polynomial=polynomial,coefficients=coefficients,recurrence=recurrence,
        verification={'passed':passed,'through_degree':order-3,
                      'residual_coefficients':residual_coefficients,
                      'residual_remainder_order':order-2},
        assumptions=['g>0','kappa>0','m>=1','positive real velocity and gradient',
                     'nonzero third-derivative coefficient at initial jet',
                     'scaling rows additionally require t>0'],
        local_existence=('The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) '
                         'is real analytic near this regular jet. Analytic ODE local existence and '
                         'uniqueness give a unique local analytic profile germ. The degree-N polynomial '
                         'is a formal truncation, not an exact solution or a radius bound.'),
        formal_remainders={'F':order+1,'F_prime':order,'F_double_prime':order-1})
    return result


def _ode_fingerprint(reduction):
    """Bind a numerical receipt to the exact corrected symbolic ODE."""
    return hashlib.sha256(sp.srepr(reduction['residual']).encode('utf-8')).hexdigest()


def _series_grid_comparison(row, csv_path):
    if row['status'] != 'regular_analytic_germ' or not csv_path.exists():
        return {'status':'existing_numerical_grid_unavailable','samples':[]}
    metadata_path = csv_path.parent/'numerics.json'
    if not metadata_path.exists():
        return {'status':'reference_provenance_unavailable','samples':[]}
    try:
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
        record = next((item for item in metadata.get('runs',[])
                       if item.get('case') == row['case']
                       and float(item.get('m',float('nan'))) == float(row['m'])),None)
        if record is None or not all(record.get(key) for key in
                                     ('csv_sha256','equation_sha256')):
            return {'status':'reference_provenance_unavailable','samples':[]}
        reduction = derive_reduction(row['case'],exponent=row['m'],
                                     alpha=row['alpha'],alpha3=row['alpha3'])
        interval = NUMERICAL_CASE_SETTINGS[row['case']][0]
        checks = {
            'passed_reference':record.get('status') == 'passed',
            'model':record.get('model') == 'printed scalar',
            'g':float(record['g']) == float(row['g']),
            'kappa':float(record['kappa']) == float(row['kappa']),
            'interval':list(map(float,record['interval'])) == list(map(float,interval)),
            'center':float(record['interval'][0]) == float(row['z0']),
            'initial_jet':list(map(float,record['initial_jet'])) ==
                          list(map(float,row['initial_jet'])),
            'equation':record['equation_sha256'] == _ode_fingerprint(reduction),
            'csv_bytes':record['csv_sha256'] == hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        }
        if not all(checks.values()):
            return {'status':'reference_metadata_mismatch','samples':[],
                    'failed_checks':[key for key,passed in checks.items() if not passed]}
    except (ValueError,TypeError,KeyError,OSError) as exc:
        return {'status':'reference_provenance_unavailable','samples':[],
                'reason':str(exc)}
    try:
        columns = ('z','F_rkf45','P_rkf45','C_rkf45',
                   'F_dop853','P_dop853','C_dop853')
        with csv_path.open(newline='',encoding='utf-8') as handle:
            grid = [{name:float(item[name]) for name in columns}
                    for item in csv.DictReader(handle)]
        if any(not np.isfinite(value) for item in grid for value in item.values()):
            return {'status':'reference_grid_invalid','samples':[]}
    except (ValueError,TypeError,KeyError,OSError,csv.Error) as exc:
        return {'status':'reference_grid_invalid','samples':[],
                'reason':str(exc)}
    if not grid or any(float(grid[0][name]) != float(value)
                       for names in (('F_rkf45','P_rkf45','C_rkf45'),
                                     ('F_dop853','P_dop853','C_dop853'))
                       for name,value in zip(names,row['initial_jet'])):
        return {'status':'reference_initial_node_mismatch','samples':[]}
    coordinates = np.array([float(item['z']) for item in grid])
    if (not np.all(np.isfinite(coordinates)) or np.any(np.diff(coordinates) <= 0)
            or coordinates[0] != float(row['z0'])):
        return {'status':'reference_grid_invalid','samples':[]}
    h = sp.Symbol('h',real=True)
    evaluators = [sp.lambdify(h,sp.diff(row['polynomial'],h,i),'numpy')
                  for i in range(3)]
    interval = NUMERICAL_CASE_SETTINGS[row['case']][0]
    length = interval[1]-interval[0]
    samples = []
    for k in range(1,5):
        offset = length/(2**k)
        target = float(row['z0'])+offset
        index = int(np.argmin(np.abs(coordinates-target)))
        tolerance = 8*np.finfo(float).eps*max(1,abs(target))
        if abs(coordinates[index]-target) > tolerance:
            return {'status':'existing_grid_node_missing','samples':samples}
        match = grid[index]
        target = float(match['z'])
        offset = target-float(row['z0'])
        approx = [float(fn(offset)) for fn in evaluators]
        rkf = [float(match[name]) for name in ('F_rkf45','P_rkf45','C_rkf45')]
        dop = [float(match[name]) for name in ('F_dop853','P_dop853','C_dop853')]
        disagreement = [abs(a-b) for a,b in zip(rkf,dop)]
        error = [abs(a-b) for a,b in zip(approx,dop)]
        threshold = [float(max(10*d,32*np.finfo(float).eps*max(1,abs(ref))))
                     for d,ref in zip(disagreement,dop)]
        samples.append({'offset':offset,'z':target,'polynomial':approx,
                        'rkf45':rkf,'dop853':dop,
                        'abs_error_vs_dop853':error,
                        'abs_error_vs_rkf45':[abs(a-b) for a,b in zip(approx,rkf)],
                        'rkf_dop_disagreement':disagreement,
                        'diagnostic_resolution_threshold':threshold,
                        'resolved_vs_reference':[bool(e>q) for e,q in zip(error,threshold)]})
    return {'status':'existing_grid_nodes_only','samples':samples,
            'provenance':{'metadata':metadata_path.name,'checks':checks,
                          'csv_sha256':record['csv_sha256'],
                          'equation_sha256':record['equation_sha256']},
            'interpretation':'finite endpoint diagnostics; no interpolation, radius, or certified remainder'}


def run_series_campaign(out_dir, order=6, compare_dir=None):
    """Write exact recurrence receipts and optional existing-grid comparisons."""
    output = Path(out_dir)
    output.mkdir(parents=True,exist_ok=True)
    compare_dir = None if compare_dir is None else Path(compare_dir)
    regular_runs,nine_rows,trace = [],{},[]
    started = time.monotonic()
    deadline = started+600
    for case in tuple(f'3.{i}' for i in range(1,10)):
        exponents = ((1,sp.Rational(3,2),2,3,4)
                     if case in ('3.4','3.6','3.8','3.9') else (3,))
        for exponent in exponents:
            if time.monotonic() >= deadline:
                row = {'case':case,'m':exponent,'status':'campaign_time_limit'}
            else:
                try:
                    row = compute_ode_series(case,exponent=exponent,order=order)
                except (ValueError,ArithmeticError) as exc:
                    row = {'case':case,'m':exponent,'status':'unresolved_exception',
                           'reason':f'{type(exc).__name__}: {exc}'}
            if exponent == 3:
                nine_rows[case] = row
            if case not in CASES:
                continue
            if compare_dir is not None and row['status']=='regular_analytic_germ':
                suffix = ('1p5' if exponent==sp.Rational(3,2)
                          else str(exponent).replace('.','p'))
                stem = f"{case.replace('.','-')}-m{suffix}"
                row['comparison'] = _series_grid_comparison(row,compare_dir/f'{stem}.csv')
            regular_runs.append(row)
            trace.append(f"{case}, m={exponent}: {row['status']}, "
                         f"z0={row.get('z0')}, jet={row.get('initial_jet')}")
            if row.get('recurrence'):
                for term in row['recurrence']:
                    degree = term['degree']
                    trace.append(f"  a_{degree} = [h^{degree-3}]R / "
                        f"({degree}*{degree-1}*{degree-2}) = {term['coefficient']}")
                trace.append(f"  corrected residual coefficients 0..{order-3}: "
                             f"{row['verification']['residual_coefficients']}")
    for case,row in nine_rows.items():
        if case not in CASES:
            trace.append(f"{case}: {row['status']}; {row.get('reason')}")
    report = {'order':order,'model':'printed scalar SVE, corrected reductions',
              'regular_runs':regular_runs,'nine_rows':nine_rows,
              'regular_count':sum(r['status']=='regular_analytic_germ' for r in regular_runs),
              'all_verified':all(r['status']=='regular_analytic_germ' for r in regular_runs),
              'elapsed_seconds':time.monotonic()-started,
              'scope':'local analytic germs on regular positive chart; no radius or global PDE claim'}
    (output/'series.json').write_text(json.dumps(jsonable(report),indent=2,
        ensure_ascii=False,allow_nan=False),encoding='utf-8')
    (output/'series_trace.txt').write_text('\n'.join(trace)+'\n',encoding='utf-8')
    with (output/'series_comparison.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.writer(handle)
        writer.writerow(('case','m','offset','component','series_abs_error_vs_dop853',
                         'series_abs_error_vs_rkf45','rkf_dop_disagreement',
                         'diagnostic_resolution_threshold','resolved_vs_reference'))
        for row in regular_runs:
            for item in row.get('comparison',{}).get('samples',[]):
                for i,name in enumerate(('F','F_prime','F_double_prime')):
                    writer.writerow((row['case'],row['m'],item['offset'],name,
                        item['abs_error_vs_dop853'][i],
                        item['abs_error_vs_rkf45'][i],
                        item['rkf_dop_disagreement'][i],
                        item['diagnostic_resolution_threshold'][i],
                        item['resolved_vs_reference'][i]))
    return report


# Convergence
def _conv_scaled_error(actual, reference):
    return float(np.max(np.abs(np.asarray(actual)-np.asarray(reference)) /
                        np.maximum(1.0, np.abs(reference))))


def _conv_fixed(rhs, interval, y0, n, guard):
    """Take exactly n classical Fehlberg fifth-order steps, without adaptivity."""
    a, b = interval
    h = (b-a)/n
    y = np.asarray(y0, dtype=float).copy()
    for k in range(n):
        t = a+k*h
        if not guard(t, y):
            raise ValueError(f'branch guard failed before fixed step {k}')
        with np.errstate(all='raise'):
            _, y, _ = rkf45_step(rhs, t, y, h)
        if not np.all(np.isfinite(y)) or not guard(t+h, y):
            raise ValueError(f'branch guard failed after fixed step {k}')
    return y


def _conv_order(rows, coordinate):
    """Pairwise empirical orders only above a declared resolution threshold."""
    for previous, current in zip(rows, rows[1:]):
        e0, e1 = previous.get('error'), current.get('error')
        if e0 is None or e1 is None or not (previous['resolved'] and current['resolved']):
            current['pairwise_order'] = None
            continue
        ratio = previous[coordinate]/current[coordinate]
        current['pairwise_order'] = (float(math.log(e0/e1)/math.log(ratio))
                                     if e0 > 0 and e1 > 0 and ratio > 1 else None)


def _conv_one(case, exponent, deadline):
    reduction = derive_reduction(case, exponent=sp.Rational(str(exponent)),
                                 alpha=1 if case == '3.8' else -1, alpha3=1)
    interval, y0 = NUMERICAL_CASE_SETTINGS[case]
    fns = _functions(reduction, exponent)
    guard = _profile_guard(fns, deadline)

    def rhs(z, state):
        if not guard(z, state):
            raise ValueError('regular positive-branch guard failed at solver stage')
        return np.array([state[1], state[2], float(fns[0](z, *state))])

    length = interval[1]-interval[0]
    result = {'case':case, 'm':exponent, 'interval':interval, 'initial_jet':y0,
              'status':'started'}
    if case == '3.8':
        z = interval[1]-interval[0]
        reference = np.array([y0[0]+y0[1]*z+y0[2]*z*z/2,
                              y0[1]+y0[2]*z, y0[2]])
        result['reference'] = {'type':'exact_quadratic', 'endpoint':reference.tolist(),
                               'disagreement':0.0}
    else:
        opts = ((1e-12, 1e-14, length/8), (1e-13, 1e-15, length/16))
        refs = [solve_ivp(rhs, interval, y0, method='DOP853', rtol=rtol,
                          atol=atol, max_step=maxstep)
                for rtol, atol, maxstep in opts]
        result['reference'] = {'type':'independent_DOP853_pair',
            'policies':[{'rtol':r,'atol':a,'max_step':h} for r,a,h in opts],
            'statuses':[bool(ref.success) for ref in refs],
            'nfev':[int(ref.nfev) for ref in refs],
            'messages':[ref.message for ref in refs]}
        if not all(ref.success and abs(ref.t[-1]-interval[1]) < 1e-12 for ref in refs):
            result['status'] = 'reference_failed'
            return result
        reference = refs[1].y[:, -1]
        disagreement = _conv_scaled_error(refs[0].y[:, -1], reference)
        result['reference'].update(endpoint=reference.tolist(), disagreement=disagreement)
    # Endpoint error is scaled componentwise. The factor 32 accounts for several
    # floating-point operations per step; 10x comparator disagreement prevents
    # DOP853 reference uncertainty from masquerading as Fehlberg truncation.
    floor = max(32*np.finfo(float).eps, 10*result['reference']['disagreement'])
    threshold = 10*floor
    result['resolution'] = {'scaled_floor':floor, 'resolved_if_error_gt':threshold,
        'rule':'error > 10*max(32*machine_epsilon, 10*DOP853_pair_disagreement)'}
    fixed = []
    for n in (1, 2, 4, 8, 16, 32, 64):
        row = {'n_steps':n, 'h':length/n, 'nfev':6*n}
        try:
            endpoint = _conv_fixed(rhs, interval, y0, n, guard)
            error = _conv_scaled_error(endpoint, reference)
            row.update(status='completed', endpoint=endpoint.tolist(), error=error,
                       resolved=bool(error > threshold))
        except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError) as exc:
            row.update(status='failed', error=None, resolved=False,
                       message=f'{type(exc).__name__}: {exc}')
        fixed.append(row)
    _conv_order(fixed, 'h')
    adaptive = []
    for rtol in (1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10):
        atol = rtol*1e-2
        row = {'rtol':rtol, 'atol':atol, 'first_step':length/2,
               'max_step':length, 't_eval':None}
        try:
            sol = solve_ivp_rkf45(rhs, interval, y0, rtol=rtol, atol=atol,
                 first_step=length/2, max_step=length, max_steps=20000,
                 max_rejections=2000, guard=guard)
            row.update(status=sol.status, n_steps=sol.n_steps,
                       n_rejected=sol.n_rejected, nfev=sol.nfev,
                       endpoint=sol.y[:, -1].tolist())
            error = (_conv_scaled_error(sol.y[:, -1], reference)
                     if sol.status == 'completed' else None)
            row.update(error=error, resolved=bool(error is not None and error > threshold))
        except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError) as exc:
            row.update(status='failed', error=None, resolved=False,
                       message=f'{type(exc).__name__}: {exc}')
        adaptive.append(row)
    resolved_orders = [r['pairwise_order'] for r in fixed
                       if r.get('pairwise_order') is not None]
    result.update(fixed=fixed, adaptive=adaptive,
                  resolved_fixed_pair_orders=resolved_orders,
                  fixed_order_status=('measured_pairwise' if resolved_orders else
                                      'unresolved_at_reference_roundoff_floor'),
                  adaptive_distinct_step_counts=len({r.get('n_steps') for r in adaptive
                     if r['status']=='completed'}),
                  status=('completed' if all(r['status']=='completed' for r in fixed+adaptive)
                          else 'partial_failure'))
    return result


def _conv_exp_control():
    """Exact non-polynomial control on an interval that exposes fifth order."""
    interval = (0.0, 2.0)
    exact = np.array([math.exp(2.0)])
    rows = []
    for n in (2, 4, 8, 16, 32, 64):
        endpoint = _conv_fixed(lambda t,y:y, interval, [1.0], n,
                               lambda t,y:np.all(np.isfinite(y)))
        error = _conv_scaled_error(endpoint, exact)
        rows.append({'n_steps':n, 'h':2/n, 'nfev':6*n,
                     'error':error, 'resolved':bool(error>10*32*np.finfo(float).eps),
                     'status':'completed'})
    _conv_order(rows, 'h')
    return {'equation':"y'=y", 'interval':interval, 'initial':1.0,
            'exact_endpoint':float(exact[0]), 'fixed':rows}


def _conv_write_plot(rows, control, path):
    colors = {'3.4':'#155e75','3.5':'#b45309','3.6':'#377c55',
              '3.8':'#666666','3.9':'#a63a52'}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), layout='constrained')
    selected = [r for r in rows if r['m']==3 and r['status'] in ('completed','partial_failure')]
    for r in selected:
        case = r['case']
        fixed = [x for x in r['fixed'] if x['status']=='completed' and x['error']>0]
        resolved = [x for x in fixed if x['resolved']]
        unresolved = [x for x in fixed if not x['resolved']]
        if resolved:
            axes[0].loglog([x['h'] for x in resolved], [x['error'] for x in resolved],
                           'o-', color=colors[case], label=case)
        if unresolved:
            axes[0].loglog([x['h'] for x in unresolved], [x['error'] for x in unresolved],
                           'x', color=colors[case], label=case if not resolved else None)
        adaptive = [x for x in r['adaptive'] if x['status']=='completed' and x['error']>0]
        axes[1].loglog([x['rtol'] for x in adaptive], [x['error'] for x in adaptive],
                       'o-', color=colors[case], label=case)
    axes[0].loglog([x['h'] for x in control['fixed']],
                   [x['error'] for x in control['fixed']], 'k--', label="y'=y")
    axes[0].set(xlabel='Fixed step h', ylabel='Scaled endpoint error',
                title='Fehlberg fifth-order fixed steps (x: unresolved)')
    axes[1].set(xlabel='Relative tolerance', ylabel='Scaled endpoint error',
                title='Adaptive tolerance sweep (no output grid)')
    axes[1].invert_xaxis()
    axes[1].text(.03, .50, '3.8: exact zero; omitted on log axis',
                 transform=axes[1].transAxes, fontsize=8, color='#555555')
    for ax in axes:
        ax.grid(alpha=.2, which='both')
        ax.legend(frameon=False, ncol=2, fontsize=8)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def run_convergence(out_dir):
    """Run and save bounded endpoint convergence checks for all 21 regular IVPs."""
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    deadline = started+600
    runs = []
    for case in ('3.4','3.5','3.6','3.8','3.9'):
        for exponent in ((3,) if case=='3.5' else (1,1.5,2,3,4)):
            if time.monotonic() >= deadline:
                runs.append({'case':case,'m':exponent,'status':'campaign_time_limit'})
                continue
            try:
                runs.append(_conv_one(case, exponent, min(deadline,time.monotonic()+25)))
            except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError) as exc:
                runs.append({'case':case,'m':exponent,'status':'unresolved_exception',
                             'message':f'{type(exc).__name__}: {exc}'})
    control = _conv_exp_control()
    report = {'method':'classic six-stage Fehlberg fifth-order accepted state',
              'model':'printed scalar SVE, constructed dimensionless local IVPs',
              'error':'maximum componentwise endpoint error divided by max(1, abs(reference))',
              'fixed_steps':[1,2,4,8,16,32,64],
              'adaptive_rtol':[1e-3,1e-4,1e-5,1e-6,1e-7,1e-8,1e-9,1e-10],
              'runs':runs, 'exact_exponential_control':control,
              'elapsed_seconds':time.monotonic()-started,
              'complete_count':sum(r['status']=='completed' for r in runs)}
    with (output/'convergence.json').open('w',encoding='utf-8') as handle:
        json.dump(report,handle,indent=2,allow_nan=False)
    with (output/'convergence.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.writer(handle)
        writer.writerow(('case','m','method','parameter','step_size','n_steps','nfev',
                         'error','resolved','pairwise_order','status'))
        for r in runs:
            for x in r.get('fixed',[]):
                writer.writerow((r['case'],r['m'],'fixed',x['n_steps'],x['h'],
                    x['n_steps'],x['nfev'],x['error'],x['resolved'],
                    x.get('pairwise_order'),x['status']))
            for x in r.get('adaptive',[]):
                writer.writerow((r['case'],r['m'],'adaptive',x['rtol'],'',
                    x.get('n_steps'),x.get('nfev'),x['error'],x['resolved'],'',x['status']))
        for x in control['fixed']:
            writer.writerow(('exp', '', 'fixed',x['n_steps'],x['h'],x['n_steps'],
                             x['nfev'],x['error'],x['resolved'],x.get('pairwise_order'),x['status']))
    _conv_write_plot(runs,control,output/'convergence.png')
    return report


# Reconstruction


def reconstruct_profile_fields(case, interpolant, interval, times, space):
    """Reconstruct phi, velocity and depth from one consistent interpolant.

    x=phi(t,s) is the particle-position map. u=phi_t and h=1/phi_s
    use the normalized mass coordinate. These kinematic quantities do not
    upgrade the printed scalar equation to the corrected full bed system.
    NaN entries mark unsolved coordinates and must never be extrapolated.
    """
    tt, ss = np.meshgrid(times, space, indexing='ij')
    if case == '3.4':
        zz = ss/tt
    elif case == '3.5':
        zz = ss*tt**2
    elif case in ('3.6', '3.9'):
        zz = ss+tt
    elif case == '3.8':
        zz = tt
    else:
        raise ValueError('No regular reconstructed profile for this case')
    valid = (zz >= interval[0]) & (zz <= interval[1])
    ff = interpolant(zz)
    pp = interpolant.derivative(1)(zz)
    if case == '3.4':
        phi, vel, grad = tt*ff, ff-zz*pp, pp
    elif case == '3.5':
        phi, vel, grad = ff, 2*zz*pp/tt, tt**2*pp
    elif case == '3.6':
        phi, vel, grad = ff, pp, pp
    elif case == '3.9':
        phi, vel, grad = tt+ff, 1+pp, pp
    else:
        phi, vel, grad = ss+ff, pp, np.ones_like(pp)
    valid &= np.isfinite(phi) & np.isfinite(vel) & np.isfinite(grad)
    valid &= (vel > 0) & (grad > 0)
    fields = {'phi': np.where(valid, phi, np.nan),
              'u': np.where(valid, vel, np.nan),
              'h': np.where(valid, 1/grad, np.nan)}
    return fields, valid


# ========================================================================
# Main
# ========================================================================
class Tee:
    def __init__(self,*streams): self.streams=streams
    def write(self,text):
        for stream in self.streams: stream.write(text)
        return len(text)
    def flush(self):
        for stream in self.streams: stream.flush()

def symbolic_certificate_summary(evidence):
    """Fail closed on the named calculations, not on paper disagreements."""
    failures=[]

    def get(*path):
        value=evidence
        for part in path:
            if not isinstance(value,dict) or part not in value:
                return None
            value=value[part]
        return value

    def require_true(*path):
        if get(*path) is not True:
            failures.append('.'.join(path))

    for name in ('mass_pullback_zero','momentum_pullback_zero',
                 'printed_compatibility_zero','physical_compatibility_zero'):
        require_true('models','checks',name)
    if get('models','physical_equals_printed') is not False:
        failures.append('models.physical_equals_printed')
    for name in ('X1','X2','X3','X4','X5','X6_m1',
                 'unrestricted_determining_split'):
        require_true('symmetries','checks',name,'passed')
    require_true('symmetries','checks','X5','m4_defect_nonzero')
    if get('symmetries','checks','X5','m3_defect') != '0':
        failures.append('symmetries.checks.X5.m3_defect')
    require_true('symmetries','checks','X6_m1','m2_nonzero')
    for name in ('free_y','free_w','free_a_b','free_a','free_x',
                 'm1_remaining_residual'):
        require_true('symmetries','checks','unrestricted_determining_split',name,'checked')
    for name in ('antisymmetry','jacobi','m1_jacobi'):
        passed=get('algebra','checks',name,'passed')
        total=get('algebra','checks',name,'total')
        if (type(passed) is not int or type(total) is not int
                or total <= 0 or passed != total):
            failures.append(f'algebra.checks.{name}')
    if get('algebra','checks','table_2','status') != 'agrees':
        failures.append('algebra.checks.table_2.status')
    table2=get('algebra','checks','table_2','comparisons')
    if (not isinstance(table2,dict) or len(table2)!=25
            or not all(row.get('passed') is True for row in table2.values())):
        failures.append('algebra.checks.table_2.comparisons')
    require_true('reductions','checks','passed')
    for number in range(24,35):
        require_true('reductions','source_witnesses',f'eq{number}','audit_verified')
    return {'passed':not failures,'failures':failures}

def write_manuscript_plots(out_dir):
    """Plot matched cubic IVPs and re-solve their certified second-order ODEs.

    Uses existing numerical receipts; refuses stale or mismatched data. The
    figures are finite diagnostics, not error certificates or radius estimates.
    """
    output = Path(out_dir)
    destination = output/'presentation'
    destination.mkdir(parents=True,exist_ok=True)
    profiles = {}
    receipt = {'scope':'printed scalar, cubic constructed IVPs; finite diagnostics',
               'cases':{},'files':[],
               'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    for case in ('3.4','3.6','3.9'):
        row = compute_ode_series(case,exponent=3,order=6)
        path = output/'numerical'/f"{case.replace('.','-')}-m3.csv"
        comparison = _series_grid_comparison(row,path)
        if comparison['status'] != 'existing_grid_nodes_only':
            raise ValueError(f"Cannot plot {case}: {comparison['status']}")
        data = np.genfromtxt(path,delimiter=',',names=True)
        grid = data['z']
        states = np.vstack([data[name+'_rkf45'] for name in ('F','P','C')])
        reference = np.vstack([data[name+'_dop853'] for name in ('F','P','C')])
        reduction = derive_reduction(case,exponent=3,alpha=-1,alpha3=row['alpha3'])
        integral = next(x['expression'] for x in reduction['steps']
                        if x['label']=='first-integral density')
        integral = integral.subs({g:row['g'],kappa:row['kappa'],m:3})
        initial = dict(zip((z,F,P,C),(row['z0'],*row['initial_jet'])))
        integral0 = float(integral.subs(initial))
        density = sp.lambdify((z,F,P,C),integral,'numpy')
        drift = np.asarray(density(grid,*states),dtype=float)-integral0
        drift /= max(1,abs(integral0))
        coefficient = sp.lambdify((z,F,P),sp.diff(integral,C),'numpy')
        def second_order(coordinate,state):
            f,p = state
            a = float(coefficient(coordinate,f,p))
            velocity = f-coordinate*p if case=='3.4' else float(row['alpha3'])+p
            if p<=0 or velocity<=0 or not np.isfinite(a) or abs(a)<=1e-10:
                raise ValueError(f'First-integral chart failed for {case}')
            return [p,integral0/a]
        # Different differential formulation, same initial integral constant.
        second = solve_ivp(second_order,(grid[0],grid[-1]),states[:2,0],
                           method='DOP853',t_eval=grid,rtol=1e-12,atol=1e-14,
                           max_step=.01)
        if not second.success:
            raise ValueError(f'Second-order solve failed for {case}: {second.message}')
        disagreement = np.max(np.abs(second.y-states[:2])/
                              np.maximum(1,np.abs(states[:2])),axis=0)
        if max(np.max(np.abs(drift)),np.max(disagreement))>1e-7:
            raise ValueError(f'First-integral diagnostic failed for {case}')
        receipt['cases'][case] = {
            'm':3,'z0':float(row['z0']),'initial_jet':list(map(float,row['initial_jet'])),
            'provenance':comparison['provenance'],'integral_constant':integral0,
            'max_scaled_drift':float(np.max(np.abs(drift))),
            'max_two_state_disagreement':float(np.max(disagreement)),
            'second_order_method':'DOP853; rtol=1e-12, atol=1e-14, max_step=0.01',
            'series_samples':comparison['samples']}
        with (destination/f"checks-{case.replace('.','-')}.csv").open('w',newline='',encoding='utf-8') as handle:
            writer = csv.writer(handle)
            writer.writerow(('z','scaled_integral_drift','scaled_two_state_disagreement'))
            writer.writerows(zip(grid,drift,disagreement))
        profiles[case]=(row,grid,states,reference,comparison,drift,disagreement)
    colors = ('#1a6584','#c05a30','#347c4c')
    with plt.rc_context({'font.size':10,'axes.titlesize':11,'legend.fontsize':8}):
        fig,axes = plt.subplots(2,2,figsize=(10,6.4),layout='constrained')
        for column,case in enumerate(('3.4','3.6')):
            row,grid,states,reference,comparison,_,_ = profiles[case]
            offsets = grid-float(row['z0'])
            h = sp.Symbol('h',real=True)
            polynomial = sp.lambdify(h,row['polynomial'],'numpy')
            ax=axes[0,column]
            ax.plot(offsets,states[0],color=colors[0],lw=2,label='RKF45')
            ax.plot(offsets[::8],reference[0,::8],'o',mfc='none',ms=4,color='black',label='DOP853 nodes')
            ax.plot(offsets,polynomial(offsets),'--',color=colors[1],lw=1.5,label='Degree-six Taylor')
            ax.set(title=f"{'Common scaling' if case=='3.4' else 'Traveling'} ({case}), m = 3",
                   xlabel=r'$h=z-z_0$',ylabel=r'$F(z_0+h)$')
            ax.legend(frameon=False)
            ax=axes[1,column]
            samples=sorted(comparison['samples'],key=lambda x:x['offset'])
            for j,(label,color) in enumerate(zip((r'$F$',r"$F'$",r"$F''$"),colors)):
                x=np.array([s['offset'] for s in samples])
                error=np.array([s['abs_error_vs_dop853'][j] for s in samples])
                resolved=np.array([s['resolved_vs_reference'][j] for s in samples])
                positive=error>0
                ax.loglog(x[positive],error[positive],'-',color=color,lw=1,label=label)
                for mask,fill in ((resolved,color),(~resolved,'none')):
                    use=positive & mask
                    ax.scatter(x[use],error[use],s=30,edgecolors=color,facecolors=fill,zorder=3)
            ax.set(xlabel=r'$h=z-z_0$',ylabel='Absolute Taylor minus DOP853',
                   title='Filled: resolved; hollow: below screen')
            ax.set_xticks(x,labels=[f'{value:g}' for value in x])
            ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
            ax.legend(frameon=False,ncol=3)
        for ax in axes.flat: ax.grid(alpha=.18)
        for extension in ('pdf','png'):
            name=f'series-numerical.{extension}';fig.savefig(destination/name,dpi=180)
            receipt['files'].append(name)
        plt.close(fig)
        fig,axes = plt.subplots(1,2,figsize=(10,3.6),layout='constrained')
        for (case,values),color in zip(profiles.items(),colors):
            _,grid,_,_,_,drift,disagreement=values
            coordinate=(grid-grid[0])/(grid[-1]-grid[0])
            axes[0].plot(coordinate,drift,lw=1.2,color=color,label=f'Case {case}')
            axes[1].plot(coordinate,disagreement,lw=1.2,color=color,label=f'Case {case}')
        axes[0].set(title='Independent integral evaluation',ylabel=r'$(I-I_0)/\max(1,|I_0|)$')
        axes[1].set(title='Second-order vs third-order solves',ylabel='Scaled difference in (F, P)')
        for ax in axes:
            ax.set_xlabel('Fraction of each solved interval')
            ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
            ax.grid(alpha=.18);ax.legend(frameon=False)
        for extension in ('pdf','png'):
            name=f'first-integral-checks.{extension}';fig.savefig(destination/name,dpi=180)
            receipt['files'].append(name)
        plt.close(fig)
    receipt['status']='passed'
    receipt['figure_sha256']={name:hashlib.sha256((destination/name).read_bytes()).hexdigest()
                              for name in receipt['files']}
    (destination/'plots.json').write_text(json.dumps(jsonable(receipt),indent=2),encoding='utf-8')
    return receipt


def parse_args(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage',choices=['all','symbolic','numerical','report','convergence','series','plots'],default='all')
    p.add_argument('--reduction',choices=['all']+[f'3.{i}' for i in range(1,10)]+['table3-mixed'],default='all')
    p.add_argument('--case',default='all',help='Numerical exponent/case selector, or all. Displayed reduction traces use cubic defaults; symbolic classification covers m>=1.')
    p.add_argument('--rtol',type=float,default=DEFAULT_RTOL)
    p.add_argument('--atol',type=float,default=DEFAULT_ATOL)
    p.add_argument('--series-order',type=int,default=6,
                   help='Degree of the local Taylor polynomial, from 3 through 8.')
    p.add_argument('--out',type=Path,default=PACKAGE_ROOT/'results')
    p.add_argument('--repo-root',type=Path,default=None,
                   help='Optional repository containing ref/ primary PDFs.')
    p.add_argument('--trace',choices=['full','summary'],default=DEFAULT_TRACE)
    return p.parse_args(argv)

def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8',errors='backslashreplace')
    args=parse_args(argv)
    if not (0<args.rtol<1 and 0<args.atol<1):
        raise SystemExit('rtol and atol must be between zero and one')
    if not 3 <= args.series_order <= 8:
        raise SystemExit('series order must be between 3 and 8')
    args.out=args.out.resolve()
    args.out.mkdir(parents=True,exist_ok=True)
    if args.stage=='plots':
        result=write_manuscript_plots(args.out)
        print('Manuscript plots:',result['status'],args.out/'presentation')
        return 0
    if args.stage=='series':
        series=run_series_campaign(args.out/'series',order=args.series_order,
                                   compare_dir=args.out/'numerical')
        print('Regular analytic series:',series['regular_count'],'/ 21 verified.')
        print('Recurrence trace:',args.out/'series'/'series_trace.txt')
        if args.trace=='full':
            print((args.out/'series'/'series_trace.txt').read_text(encoding='utf-8'))
        return 0 if series['all_verified'] else 1
    if args.stage=='convergence':
        convergence=run_convergence(args.out/'convergence')
        print('Convergence checks:',convergence['complete_count'],'/ 21 completed.')
        return 0 if convergence['complete_count']==21 else 1
    if args.stage=='report':
        path=args.out/'evidence.json'
        if not path.exists(): raise SystemExit('No evidence.json: run symbolic or all first.')
        code_path=args.out/'code_manifest.json'
        if (not code_path.exists() or json.loads(code_path.read_text(encoding='utf-8')).get('main.py')
                != hashlib.sha256(Path(__file__).read_bytes()).hexdigest()):
            raise SystemExit('Saved evidence belongs to different or unrecorded code; rerun all or symbolic before report.')
        print('Report-only: formatting saved evidence; no mathematical recomputation.')
        evidence=json.loads(path.read_text(encoding='utf-8'))
        summary=symbolic_certificate_summary(evidence)
        evidence.setdefault('run',{}).update(symbolic_passed=summary['passed'],
                                              symbolic_failures=summary['failures'])
        report=write_report(evidence,args.out)
        print(report)
        failed = (not summary['passed'] or evidence['run'].get('numerical_passed') is False
                  or ('series' in evidence and not evidence['series'].get('all_verified',False)))
        return 1 if failed else 0
    started=time.perf_counter()
    evidence={'source_manifest':source_manifest(args.out,args.repo_root),'models':build_model_report(),
              'numerics':{'status':'not_run'},'run':{
                  'started_utc':datetime.now(timezone.utc).isoformat(),
                  'stage':args.stage,'selection':args.reduction,'case':args.case,
                  'calculation_mode':'fresh symbolic derivation and requested numerical stages',
                  'complete_audit':False,'source_agreement':'assessed_per_claim',
                  'numerical_scope':'constructed dimensionless local IVPs'}}
    with (args.out/'symbolic_steps.txt').open('w',encoding='utf-8') as log:
        stream=Tee(sys.stdout,log)
        with redirect_stdout(stream):
            print('SVE reproduction: source formulas are checked against independent calculations.',flush=True)
            print_steps('[master equation]',evidence['models']['steps'],stream)
            print('\nComputing point-symmetry and Lie-algebra certificates...',flush=True)
            evidence['symmetries']=build_symmetry_report()
            evidence['algebra']=build_algebra_report()
            for label,key in [('[Symmetries of the SVE Equation]','symmetries'),('[One-Dimensional Optimal System]','algebra')]:
                report=evidence[key]
                if args.trace=='full':
                    print(label,flush=True)
                    print(json.dumps(jsonable(report),indent=2,ensure_ascii=False),flush=True)
                else: print(label,'computed; full formulas saved in evidence.json',flush=True)
            print('\nDeriving the nine source reductions and Table 3 companion...',flush=True)
            ids=[f'3.{i}' for i in range(1,10)]+['table3-mixed']
            for case in ids:
                if args.reduction not in ('all',case): continue
                row=derive_reduction(case,alpha=1 if case in ('3.7','3.8') else -1)
                print(f'\nReduction {case}: {row["status"]}',flush=True)
                if args.trace=='full': print_steps('Symbolic computation',row.get('steps',[]),stream)
                else: print('  residual:',row.get('residual'),' guards:',row.get('guards'),flush=True)
            evidence['reductions']=build_reduction_report()
            if args.stage in ('all','numerical'):
                print('\nRunning true Fehlberg RKF 4(5) and independent numerical checks...',flush=True)
                evidence['numerics']=run_campaign(args.out/'numerical',rtol=args.rtol,atol=args.atol,
                    selected_reduction=args.reduction,selected_case=args.case)
            if args.stage=='all':
                print('Computing exact local series of corrected regular ODEs...',flush=True)
                evidence['series']=run_series_campaign(args.out/'series',order=args.series_order,
                                                       compare_dir=args.out/'numerical')
                print('Regular analytic series verified:',evidence['series']['regular_count'],
                      '/ 21; recurrence trace:',args.out/'series'/'series_trace.txt',flush=True)
                if args.trace=='full':
                    print((args.out/'series'/'series_trace.txt').read_text(encoding='utf-8'),flush=True)
                print('Checking fixed-step order and adaptive-tolerance convergence...',flush=True)
                evidence['convergence']=run_convergence(args.out/'convergence')
                print('Convergence cases completed:',evidence['convergence']['complete_count'],flush=True)
                if args.reduction=='all' and args.case=='all':
                    evidence['presentation']=write_manuscript_plots(args.out)
                    print('Series/numerical and first-integral figures written.',flush=True)
            evidence['run']['elapsed_seconds']=time.perf_counter()-started
            # Coverage and theorem status are finalized below without interpreting
            # a successfully executed source counterexample as source agreement.
            evidence['run']['execution_status']='finished'
            coverage=build_coverage(evidence)
            evidence['source_manifest'].update(coverage)
            evidence['run']['complete_audit']=(coverage['inventory_complete']
                and evidence['source_manifest']['source_verification_complete'])
            evidence['run']['all_printed_claims_reproduced']=False
            summary=symbolic_certificate_summary(evidence)
            evidence['run']['symbolic_passed']=summary['passed']
            evidence['run']['symbolic_failures']=summary['failures']
            evidence['run']['numerical_passed']=evidence['numerics'].get('all_passed')
            (args.out/'source_manifest.json').write_text(json.dumps(jsonable(evidence['source_manifest']),indent=2,ensure_ascii=False),encoding='utf-8')
            report_path=write_report(evidence,args.out)
            print('\nEvidence report:',report_path,flush=True)
            print('Read per-claim statuses; source discrepancies are retained.',flush=True)
    failed=(not evidence['run']['symbolic_passed'] or evidence['run']['numerical_passed'] is False
            or ('convergence' in evidence and evidence['convergence']['complete_count']!=21)
            or ('series' in evidence and not evidence['series']['all_verified']))
    return 1 if failed else 0


if __name__=='__main__':
    raise SystemExit(main())
