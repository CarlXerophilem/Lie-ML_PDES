"""Rebuild the 2026 v3 printed SVE scalar, reductions, errata and local series.

Exact routines adapted from the repository's scalar2026/_historical.py.
Use --order to choose the verified regular Taylor degree (3 through 8).
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
import json
import math
from pathlib import Path

import sympy as sp


G = 1.0


KAPPA = 1 / 30


NUMERICAL_CASE_SETTINGS = {
    '3.4': ((1.0, 1.4), (2.0, 0.5, 0.1)),
    '3.5': ((1.0, 1.1), (2.0, 0.5, 0.1)),
    '3.6': ((1.0, 1.1), (2.0, 0.5, 0.1)),
    '3.8': ((0.0, 0.4), (0.0, 1.0, 0.1)),
    '3.9': ((1.0, 1.1), (2.0, 0.5, 0.1)),
}


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


_COORDS = (t, s, u)


_NAMES = ('X1', 'X2', 'X3', 'X4', 'X5')


_M1_NAMES = ('X1', 'X2', 'X3', 'X4', 'X6')


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
                     'evidence_module':owner,'status':'indexed_source_equation'})
    return rows


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
                       alpha=None, alpha3=None, mix_alpha=sp.Rational(1,4)):
    """Exact degree-order Taylor polynomial for a corrected regular profile ODE.

    Coefficient n multiplies (z-z0)**n. Exceptional rows are typed, never
    divided through a singular leading coefficient.
    """
    case = str(case)
    if case not in tuple(f'3.{i}' for i in range(1,10))+("table3-mixed",):
        raise ValueError("case must be 3.1 through 3.9 or table3-mixed")
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
    if (case == '3.5' or (case=='table3-mixed' and mix_alpha!=0)) and exponent != 3:
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
    reduction = derive_reduction(case,exponent=exponent,alpha=alpha,alpha3=alpha3,
                                 mix_alpha=mix_alpha)
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


def cubic_material_laurent(order):
    """Exact coefficients of the convergent M Laurent branch at g beta=3/4."""
    xi = sp.Symbol("xi")
    coefficients = [sp.S.One]
    for n in range(1, order+1):
        Y = sum(c*xi**i for i,c in enumerate(coefficients))
        V = sp.diff(Y,xi)
        # Multiply the differential equation by 8Y^3; use its polynomial jet.
        poly = 24*xi*Y**3*V.diff(xi)+24*xi*Y**2*V**2+8*Y**3*V-2*xi*V+Y
        cn = -sp.series(poly,xi,0,n).removeO().coeff(xi,n-1)/(8*n*(3*n-2))
        coefficients.append(cn)
    assert coefficients[1] == -sp.Rational(1,8)
    if order >= 2:
        assert coefficients[2] == -sp.Rational(7,512)
    return {"Y":coefficients,
            "F_coefficients_in_w_over_sigma": [c/(4*i-1) for i,c in enumerate(coefficients)],
            "xi":"g*sigma^4/w0^3",
            "convergence":"|xi|<1/4 by the dissertation's disk-algebra fixed point"}


def singular_examples():
    """Check the common-scaling critical power solutions without dividing by L."""
    exponent = sp.Rational(1,3)
    amp = sp.Symbol("A0", positive=True)
    profile = amp*z**exponent
    jets = {v:sp.diff(profile,z,i) for i,v in enumerate((F,P,C,H))}
    time = sp.Symbol("T",positive=True)
    aux = time*profile.subs(z,s/time)
    # s>0 in this chart. Replace s by z*T before setting T=1.
    jet_values = {v:sp.diff(aux,time,i,s,j).subs(s,z*time).subs(time,1)
                  for (i,j),v in JETS.items()}
    P3 = master(3)
    M3 = P3-total(p*(q*a-g*c/q**2)/q,1)
    results = {}
    for model, eq, divisor in (("P",P3,12),("M",M3,4)):
        # The pullback's leading coefficient uses all transformed third jets.
        common = derive_reduction("3.4",exponent=3)["residual"]
        if model=="M":
            # D_s(velocity*A/phi_s) on the t=1 common scaling chart.
            term = (F-z*P)*(z*z*C-g*C/P**3)
            common -= profile_total(term)
        k0 = (1-27*g/amp**3)/(divisor*g)
        leading = sp.simplify(common.diff(H).xreplace(jets).subs(kappa,k0))
        direct = sp.simplify(eq.xreplace(jet_values).subs(kappa,k0))
        assert leading == direct == 0, (model, leading, direct)
        results[model] = {"A0_cubed":27*g/(1-divisor*g*kappa),"guard":"denominator > 0"}
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order",type=int,default=6,choices=range(3,9))
    parser.add_argument("--output",type=Path)
    parser.add_argument("--case", choices=tuple(f"3.{n}" for n in range(1,10))+("table3-mixed",),
                        help="Compute one exact regular chart or report a branch guard")
    parser.add_argument("--m", default="3", help="Exact rational exponent for --case")
    parser.add_argument("--initial-jet", nargs=3, metavar=("F","Fp","Fpp"))
    parser.add_argument("--z0", help="Exact rational chart centre for --case")
    parser.add_argument("--mix", default="1/4", help="Scaling mixture for --case table3-mixed")
    opts = parser.parse_args()
    if opts.case:
        data=compute_ode_series(opts.case,sp.Rational(opts.m),opts.order,
                                initial_jet=opts.initial_jet,z0=opts.z0,
                                mix_alpha=sp.Rational(opts.mix))
        emit(data,opts.output)
        return
    evidence = {"models":build_model_report(),"symmetries":build_symmetry_report(),
                "algebra":build_algebra_report(),"reductions":build_reduction_report()}
    assert symbolic_certificate_summary(evidence)["passed"]
    evidence["equations"] = equation_inventory()
    cases = [f"3.{n}" for n in range(1,10)]
    for row in evidence["equations"]:
        if row["equation"] >= 24:
            row["status"] = evidence["reductions"]["source_witnesses"][f'eq{row["equation"]}']["status"]
    evidence["series"] = [compute_ode_series(case,m_value,opts.order)
                          for case in cases
                          for m_value in ((1,sp.Rational(3,2),2,3,4)
                                         if case in ("3.4","3.6","3.8","3.9") else (3,))]
    assert sum(row["status"]=="regular_analytic_germ" for row in evidence["series"])==21
    evidence["mixed_series"] = [
        compute_ode_series("table3-mixed",3,opts.order,mix_alpha=mu)
        for mu in (sp.Rational(1,4),-1)]
    assert all(row["status"]=="regular_analytic_germ" for row in evidence["mixed_series"])
    evidence["critical_examples"] = singular_examples()
    evidence["material_Laurent"] = cubic_material_laurent(opts.order)
    pth = Path(__file__).resolve().parents[1]/"ref/main"
    from hashlib import sha256
    source = next(iter(sorted(pth.glob("*00433-v3.pdf"))),None)
    evidence["primary_pdf_sha256"] = sha256(source.read_bytes()).hexdigest() if source else None
    evidence["scope"] = "All nine printed section entries; exact regular initial-jet examples and selected singular branches"
    emit(evidence,opts.output)
    if opts.output:
        print("Verified 9 sections, 11 displayed equation audits, 23 Taylor jets and the listed critical branches.")


def emit(evidence,destination):
    output=json.dumps(jsonable(evidence),ensure_ascii=False,indent=2,sort_keys=True)
    if destination is None:
        print(output)
    else:
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(output+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
