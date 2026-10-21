"""Independent exact review of selected 2D subalgebras, not optimality.

The reference basis, bracket table and chart-minor formulas below are
constructed independently of the production membership/adjoint routines.
"""
from __future__ import annotations

import hashlib
from itertools import combinations
import json
from pathlib import Path
import time

import sympy as sp

import algebra_2d as algebra
from main import json_ready
from models_2d import BRANCHES_2D,t,x,y,h,u,v,B,n

HERE=Path(__file__).resolve().parent
COORDS=(t,x,y,h,u,v,B)


def independent_bracket(left,right):
    return sp.Matrix([sp.expand(sum(left[j]*sp.diff(right[i],COORDS[j])
                         -right[j]*sp.diff(left[i],COORDS[j]) for j in range(7)))
                      for i in range(7)])


def coefficient_matrix(vectors):
    """Coefficients against a fixed polynomial monomial list, not point rank."""
    monomials=[(0,)*7]+[tuple(int(i==j) for i in range(7)) for j in range(7)]
    columns=[]
    for vector in vectors:
        entries=[]
        for entry in vector:
            polynomial=sp.Poly(entry,*COORDS)
            if polynomial.total_degree()>1:
                raise ValueError('Non-affine field in reviewed real algebra')
            entries.extend(polynomial.coeff_monomial(power) for power in monomials)
        columns.append(sp.Matrix(entries))
    return sp.Matrix.hstack(*columns)


def chart_simplify(value):
    reduced=sp.simplify(value)
    if reduced==0:
        return reduced
    # The non-polynomial invariant charts explicitly require t>0,x>0.
    # Simplify related real radial powers with a positive placeholder, then
    # restore its defining polynomial. No forced power identity is used.
    radial=sp.Dummy('positive_spatial_radius_squared',positive=True)
    positive_t=sp.Dummy('positive_time',positive=True)
    on_chart=reduced.xreplace({x*x+y*y:radial,t:positive_t})
    combined=sp.factor(sp.simplify(on_chart))
    return sp.simplify(combined.subs({radial:x*x+y*y,positive_t:t},simultaneous=True))


def canonical_basis(cell):
    basis=[sp.eye(7)[:,j] for j in (0,1,2,6)]
    basis.append(sp.Matrix([0,-y,x,0,-v,u,0]))
    def scale(a,b):
        return sp.Matrix([a*t,b*x,b*y,2*(b-a)*h,(b-a)*u,(b-a)*v,2*(b-a)*B])
    if not cell['G']:
        if cell['K'] and cell['m']!=3:
            if cell['coriolis']=='f0':
                basis.append(scale(1,1))
        else:
            if cell['coriolis']=='f0':
                basis.append(scale(1,0))
            basis.append(scale(0,1))
    elif (not cell['K'] or cell['m']==3) and (
            cell['coriolis']=='f0' or cell['n']==2):
        basis.append(scale(sp.sympify(cell['n'])-2,sp.sympify(cell['n'])-1))
    return tuple(basis)


def review():
    started=time.perf_counter()
    checks=[]
    def check(name,passed,evidence=None):
        checks.append({'name':name,'passed':bool(passed),'evidence':evidence})
    def zero(name,values):
        if not isinstance(values,(tuple,list,sp.MatrixBase)):
            values=[values]
        reduced=[chart_simplify(z) for z in values]
        check(name,all(z==0 for z in reduced),reduced)
    seen_charts=set()
    for name,cell in BRANCHES_2D.items():
        report=algebra.representative_subalgebras(name)
        reference=canonical_basis(cell)
        actual=tuple(report['basis'])
        expected_matrix=coefficient_matrix(reference)
        actual_matrix=coefficient_matrix(actual)
        check(name+'_constant_real_span',len(actual)==len(reference)
              and actual_matrix.rank()==len(reference)
              and expected_matrix.row_join(actual_matrix).rank()==len(reference))
        check(name+'_bounded_scope',report['status']=='verified_representatives'
              and report['optimality_status']=='not_proved'
              and report['maximal_point_algebra_claim'] is False)
        basis_matrix=sp.Matrix.hstack(*actual)
        for i,j in combinations(range(len(actual)),2):
            expected=independent_bracket(actual[i],actual[j])
            encoded=sp.Matrix(report['structure']['structure_constants'][f'{i},{j}'])
            zero(f'{name}_bracket_{i}_{j}',basis_matrix*encoded-expected)
            zero(f'{name}_adjoint_column_{i}_{j}',
                 report['structure']['adjoint_matrices'][i][:,j]-encoded)
        # Jacobi uses only the reported structure constants/matrices, not the
        # bracket routine that generated them.
        ad=report['structure']['adjoint_matrices']
        for i,j in combinations(range(len(actual)),2):
            encoded=ad[i][:,j]
            expected=sum((encoded[k]*ad[k] for k in range(len(actual))),sp.zeros(len(actual)))
            zero(f'{name}_adjoint_representation_{i}_{j}',ad[i]*ad[j]-ad[j]*ad[i]-expected)
        for family in ('line_representatives','rank_two_representatives'):
            for item in report[family]:
                key=(tuple(tuple(q) for q in item['generators']),tuple(item['invariants']))
                if key in seen_charts:
                    continue
                seen_charts.add(key)
                tag=name+'_'+item['name']
                generators=item['generators']
                for i,j in combinations(range(len(generators)),2):
                    encoded=sp.Matrix(item['closure_coefficients'][f'{i},{j}'])
                    zero(tag+'_closure',sp.Matrix.hstack(*generators)*encoded
                         -independent_bracket(generators[i],generators[j]))
                for index,scalar in enumerate(item['invariants']):
                    zero(tag+f'_invariant_{index}',[sum(q[j]*sp.diff(scalar,COORDS[j])
                         for j in range(7)) for q in generators])
                check(tag+'_no_profile_solution_claim',item['profile_solution_claim'] is False)
                if item['name']=='bed_translation':
                    check(tag+'_vertical_graph_obstruction',item['projection_rank']==0
                          and item['graph_admissible'] is False
                          and item['graph_obstruction']=='Q_B=1')
                else:
                    check(tag+'_projection_and_invariant_counts',
                          item['projection_rank']==len(generators)
                          and len(item['invariants'])==7-len(generators)
                          and len(item['invariant_chart']['base_invariants'])==3-len(generators))
                if 'scaling_weights' in item:
                    a,b=item['scaling_weights']
                    radius2=x*x+y*y
                    z=t**b*radius2**(-a/2)
                    expected=(-a*z*t**6/radius2**4,b*z*x*t**5/radius2**4) if len(generators)==1 else (
                              b*z*t**5/radius2**3,-a*z*x*t**6/radius2**4)
                    zero(tag+'_independent_chart_minor_formulas',
                         [old-new for old,new in zip(item['invariant_chart']['rank_witnesses'],expected)])
                    # These formulas are globally non-simultaneously zero on
                    # t>0, x>0 provided (a,b)!=(0,0). For slope weights the
                    # difference b-a is the constant 1 for every real n.
                    check(tag+'_no_hidden_parameter_rank_drop',
                          sp.simplify(b-a)==1 or (not (a.free_symbols|b.free_symbols) and (a!=0 or b!=0)),
                          {'weights':(a,b),'guards':item['guards']})
                    if a.has(n) or b.has(n):
                        for value in (0,1,2,3,4):
                            check(tag+f'_slope_weight_{value}',
                                  (a.subs(n,value),b.subs(n,value))!=(0,0))
                else:
                    # The simple translation/polar charts have no continuous
                    # exponent; direct Jacobian rank is exact on the stated
                    # nonzero coordinate chart, with minors retained by API.
                    jacobian=sp.Matrix(item['invariants']).jacobian(COORDS)
                    check(tag+'_independent_jacobian_rank',jacobian.rank()==len(item['invariants']))
    report=algebra.representative_subalgebras('grass_cubic_f0')
    named=report['named_generators']
    epsilon=sp.Symbol('epsilon',real=True)
    zero('rotation_adjoint_real_sign',algebra.adjoint_action(report,named['R'],named['X'],epsilon)
         -sp.cos(epsilon)*named['X']+sp.sin(epsilon)*named['Y'])
    original=report['basis']
    for label,basis in [('imaginary_basis',(sp.I*original[0],*original[1:])),
                        ('infinite_basis',(sp.oo*original[0],*original[1:]))]:
        rejected=False
        try:
            algebra.representative_subalgebras('grass_cubic_f0',basis)
        except ValueError:
            rejected=True
        check(label+'_rejected',rejected)
    rejected=False
    try:
        algebra.adjoint_action(report,named['R'],named['X'],sp.I)
    except ValueError:
        rejected=True
    check('imaginary_adjoint_parameter_rejected',rejected)
    all_passed=all(item['passed'] for item in checks)
    paths=('algebra_2d.py','ALGEBRA_2D.md','tests/test_algebra_2d.py',
           'review_algebra_2d.py','ALGEBRA_2D_REVIEW.md',
           'research_first_order_2d.py','research_slope_2d.py','models_2d.py')
    return {'review_status':'accepted' if all_passed else 'changes_required',
            'all_checks_passed':all_passed,'passed_checks':sum(item['passed'] for item in checks),
            'total_checks':len(checks),'elapsed_seconds':time.perf_counter()-started,
            'reviewed_sha256':{path:hashlib.sha256((HERE/path).read_bytes()).hexdigest() for path in paths},
            'checks':checks,'scope':'Independent algebra/span/chart verification of selected representatives.',
            'not_claimed':['optimal system completeness','maximal point classification from representatives',
                           'existence of reduced profiles','full disconnected equivalence groupoid']}


if __name__=='__main__':
    result=review()
    target=HERE/'algebra_2d_review.json'
    target.write_text(json.dumps(json_ready(result),indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('review_status','all_checks_passed',
          'passed_checks','total_checks','elapsed_seconds')},indent=2))
    raise SystemExit(0 if result['all_checks_passed'] else 1)
