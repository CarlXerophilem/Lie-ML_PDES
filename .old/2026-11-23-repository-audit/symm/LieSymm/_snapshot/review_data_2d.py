"""Independent 2D data review: direct derivatives, kernel ranks, point maps.

Run each phase under a 60-second external process timeout, then --phase merge.
No phase imports the source adapter's tangency solver or accepts its success
boolean in place of the independent mathematical checks below.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time

import sympy as sp

import data_experiments_2d as adapter
from models_2d import BRANCHES_2D,t,x,y,h,u,v,B,g,K,G,m,n,f

HERE=Path(__file__).resolve().parent
COORDINATES=(t,x,y,h,u,v,B)
PHASES=('flows','initial','maps')
INPUTS=('data_experiments_2d.py','tests/test_data_experiments_2d.py','DATA_CONTROLS_2D.md','models_2d.py',
        'models.py','main.py','data_experiments.py','research_slope_2d.py',
        'research_first_order_2d.py','review_data_2d.py')
CHECKS=[]


def hashes():
    return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in INPUTS}


def check(label,condition):
    if condition is not True:
        raise AssertionError(label)
    CHECKS.append(label)


def zero(label,expression):
    check(label,sp.simplify(sp.trigsimp(expression))==0)


def physical_rows(name,fields,derivative):
    """PDE specification rebuilt directly, independently of JetSpace.D."""
    H,U,V,Z=fields
    cell=BRANCHES_2D[name]
    ff=0 if cell['coriolis']=='f0' else f
    speed=U*U+V*V
    def flux(W,axis):
        value=K*speed**((sp.sympify(cell['m'])-1)/2)*W if cell['K'] else sp.S.Zero
        if cell['G']:
            value-=G*speed**(sp.sympify(cell['n'])/2)*derivative(Z,axis)
        return value
    return (derivative(H,0)+derivative(H*U,1)+derivative(H*V,2),
            derivative(U,0)+U*derivative(U,1)+V*derivative(U,2)+g*derivative(H+Z,1)-ff*V,
            derivative(V,0)+U*derivative(V,1)+V*derivative(V,2)+g*derivative(H+Z,2)+ff*U,
            derivative(Z,0)+derivative(flux(U,1),1)+derivative(flux(V,2),2))


def review_flows():
    for name in BRANCHES_2D:
        for label,flow in (('uniform',adapter.uniform_rotating_flow(name)),
                           ('slope',adapter.constant_slope_flow(name))):
            graph=flow['graph']
            for row,value in enumerate(physical_rows(name,graph,lambda q,i:sp.diff(q,(t,x,y)[i]))):
                zero(f'{name}/{label}/direct_PDE_{row}',value)
            for i,value in enumerate(graph[1:3]):
                zero(f'{name}/{label}/initial_velocity_{i}',value.subs(t,0)-(3,4)[i])
            check(f'{name}/{label}/chart_not_global',len(flow['chart_guards'])==2
                  and flow['arbitrary_data_claim'] is False)
        if name.endswith('_f_nonzero'):
            flow=adapter.uniform_rotating_flow(name)
            zero(name+'/uniform/speed',flow['graph'][1]**2+flow['graph'][2]**2-25)
    stopped=adapter.uniform_rotating_flow('zero_transport_f0',velocity=(0,0))
    check('zero_speed_is_outside_chart',stopped['status']=='outside_declared_chart')
    bad_depth=adapter.uniform_rotating_flow('grass_generic_f0',depth=-1)
    check('negative_depth_is_outside_chart',bad_depth['status']=='outside_declared_chart')


def solved_basis(name):
    if BRANCHES_2D[name]['G']:
        from research_slope_2d import general_solution
    else:
        from research_first_order_2d import general_solution
    return tuple(sp.Matrix(q) for q in general_solution(name,COORDINATES)['basis'])


def tangent(vector,profiles):
    substitution={t:sp.S.One,**dict(zip((h,u,v,B),profiles))}
    return sp.Matrix([vector[0],*(vector[3+i]-vector[1]*sp.diff(profile,x)
                     -vector[2]*sp.diff(profile,y) for i,profile in enumerate(profiles))]
                     ).subs(substitution,simultaneous=True).applyfunc(sp.expand)


def tangent_matrix(basis,profiles):
    columns=[tangent(vector,profiles) for vector in basis]
    result=[]
    for component in range(5):
        polys=[sp.Poly(column[component],x,y) for column in columns]
        monomials=set().union(*(set(poly.monoms()) for poly in polys))
        result.extend([poly.coeff_monomial(monomial) for poly in polys] for monomial in sorted(monomials))
    return sp.Matrix(result)


def independent_affine_rank(vectors):
    if not vectors:
        return 0
    columns=[]
    for vector in vectors:
        vector=sp.Matrix(vector)
        jacobian=vector.jacobian(COORDINATES)
        remainder=vector-jacobian*sp.Matrix(COORDINATES)
        check('stabilized_family_affine',not any(q.has(*COORDINATES) for q in (*jacobian,*remainder)))
        columns.append(sp.Matrix([*remainder,*jacobian]))
    return sp.Matrix.hstack(*columns).rank()


def review_initial():
    for name in BRANCHES_2D:
        basis=solved_basis(name)
        for label,bed in (('flat',sp.S.One),('linear',1+x-2*y),('quadratic',1+x*x+y*y)):
            profiles=(sp.Integer(2),sp.Integer(3),sp.Integer(4),bed)
            result=adapter.initial_data_stabilizer(name,profiles,time0=1)
            independent_dimension=len(basis)-tangent_matrix(basis,profiles).rank()
            check(f'{name}/{label}/independent_kernel_dimension',result['dimension']==independent_dimension)
            vector=sp.Matrix(result['stabilized_coefficients'])
            for i,value in enumerate(tangent(vector,profiles)):
                zero(f'{name}/{label}/independent_tangency_{i}',value)
            directions=[vector.diff(constant) for constant in result['free_constants']]
            check(f'{name}/{label}/entire_kernel_spanned',independent_affine_rank(directions)==independent_dimension)
            check(f'{name}/{label}/initial_only',result['pde_solution_claim'] is False)
    parameter=sp.Symbol('unknown_bed_slope',real=True)
    conditional=adapter.initial_data_stabilizer('grass_generic_f0',(2,3,4,1+parameter*x))
    check('unknown_profile_parameter_retains_rank_guard',
          conditional['status']=='conditional_initial_data_stabilizer' and bool(conditional['rank_guards'])
          and bool(conditional['unresolved_zero_pivot_branches']))
    nonpolynomial=adapter.initial_data_stabilizer('grass_cubic_f0',(2,3,4,sp.sin(x*y)))
    check('nonpolynomial_profiles_remain_unresolved',nonpolynomial['status']=='unresolved_functional_splitting')
    for label,profiles in (('complex',(2,3,4,sp.I)),('nonfinite',(2,3,4,sp.oo))):
        try:
            adapter.initial_data_stabilizer('grass_generic_f0',profiles)
        except ValueError:
            CHECKS.append(label+'_profile_rejected')
        else:
            raise AssertionError(label+'_profile_was_not_rejected')


def direct_jet_derivative(fields):
    """A small independent order-two jet algebra, with shared symbol spelling."""
    jets={}
    for a,field in enumerate(fields):
        for index in itertools.product(range(3),repeat=3):
            if sum(index)<=2:
                jets[a,index]=field if not any(index) else sp.Symbol(
                    str(field)+'__'+'_'.join(map(str,index)),real=True)
    reverse={value:key for key,value in jets.items()}
    def derivative(expression,axis):
        expression=sp.sympify(expression)
        value=sp.diff(expression,(t,x,y)[axis])
        for symbol in expression.free_symbols.intersection(reverse):
            a,index=reverse[symbol]
            shifted=list(index);shifted[axis]+=1
            value+=sp.diff(expression,symbol)*jets[a,tuple(shifted)]
        return sp.expand(value)
    return derivative,reverse


def review_maps():
    P,Q=sp.symbols('momentum_x momentum_y',real=True)
    fields=(h,P,Q,B)
    derivative,_=direct_jet_derivative(fields)
    inverse=(h,P/h,Q/h,B)
    primitive_D,reverse=direct_jet_derivative((h,u,v,B))
    for name in BRANCHES_2D:
        result=adapter.conservative_point_map(name)
        rows=physical_rows(name,inverse,derivative)
        independently_transformed=(rows[0],h*rows[1]+inverse[1]*rows[0],
                                   h*rows[2]+inverse[2]*rows[0],rows[3])
        for i,(actual,expected) in enumerate(zip(result['conservative_equations'],independently_transformed)):
            zero(f'{name}/conservative/direct_chain_rule_{i}',sp.expand(actual-expected))
        forward=sp.Matrix(result['forward'])
        zero(name+'/field_jacobian',forward.jacobian((h,u,v,B)).det()-h*h)
        zero(name+'/row_multiplier_determinant',result['row_multiplier'].det()-h*h)
        for i,value in enumerate(forward.subs({u:P/h,v:Q/h},simultaneous=True)):
            zero(f'{name}/inverse_composition_{i}',value-fields[i])
        original=physical_rows(name,(h,u,v,B),primitive_D)
        reflection={symbol:(-1)**(index[2]+int(a==2))*symbol
                    for symbol,(a,index) in reverse.items()}
        reflection[f]=-f
        for i,(equation,parity) in enumerate(zip(original,(1,1,-1,1))):
            zero(f'{name}/independent_signed_reflection_{i}',equation.xreplace(reflection)-parity*equation)
        source=adapter.signed_coriolis_reflection(name)
        check(name+'/fixed_parameter_reflection_flag',source['fixed_parameter_symmetry']==name.endswith('_f0'))
        if name.endswith('_f_nonzero'):
            reflection.pop(f)
            zero(name+'/reflection_without_f_flip_is_broken_x',original[1].xreplace(reflection)-original[1]-2*f*v)
            zero(name+'/reflection_without_f_flip_is_broken_y',original[2].xreplace(reflection)+original[2]-2*f*u)


def merge():
    current=hashes()
    results=[json.loads((HERE/'runs'/f'data-2d-review-{phase}.json').read_text()) for phase in PHASES]
    passed=all(result['all_checks_passed'] and result['inputs_sha256']==current for result in results)
    count=sum(result['check_count'] for result in results)
    report=(
        '# Independent review of the 2D data controls\n\n'
        f'Review status: **{"accepted" if passed else "not accepted"}**. '
        f'The three bounded phases contain {count} independently checked identities and conditions. '
        'The exact source hashes and individual phase receipts are bound in `data_2d_review.json`.\n\n'
        'The reviewer did not author `data_experiments_2d.py`. The review reconstructs all four PDE '
        'rows with ordinary partial derivatives for the two returned flow graphs in all 17 refined '
        'branches. Initial-data dimensions are recomputed as nullities of independently assembled '
        'polynomial tangency matrices; returned stabilizer directions are checked to span the entire '
        'kernel for the three specified profiles. A separate order-two jet derivative checks the '
        'primitive/conservative chain rule, invertible field and equation-row maps, and signed-f reflection.\n\n'
        'The field map is `(h,u,v,B) -> (h,hu,hv,B)` and both its Jacobian determinant and the '
        'equation-row multiplier determinant equal `h^2`. Hence the equivalence is restricted to '
        '`h>0`. The reflection `(y,v,f) -> (-y,-v,-f)` preserves the parameterized equations; '
        'at fixed nonzero f, omitting the parameter flip leaves the checked nonzero momentum '
        'residuals `(2fv,2fu)`. No complete equivalence groupoid is inferred.\n\n'
        'The review identified a real-domain gap for complex/nonfinite initial profiles. The author '
        'was asked to reject those profiles; the independent initial-data phase includes both '
        'regressions. Unknown profile rank pivots retain explicit guards and unresolved zero-pivot '
        'branches. Nonpolynomial profile splitting is explicitly unresolved.\n\n'
        'Acceptance covers two constructed smooth flows, three fixed-time data profiles per branch, '
        'and the two explicit maps. Positivity and nonzero-speed conditions restrict the charts; '
        'the planar-bed flow is not claimed global. A fixed initial graph is not a future evolution '
        'or boundary-compatibility theorem. Classification maximality and any conditional-symmetry '
        'or learned stage are outside this review.\n')
    (HERE/'DATA_2D_REVIEW.md').write_text(report,encoding='utf-8')
    current['DATA_2D_REVIEW.md']=hashlib.sha256((HERE/'DATA_2D_REVIEW.md').read_bytes()).hexdigest()
    receipt={'review_status':'accepted' if passed else 'not_accepted','all_checks_passed':passed,
             'reviewer':'slope_classification; independent of data adapter author',
             'inputs_sha256':current,'reviewed_sha256':current,
             'check_count':count,'phase_receipts':[f'runs/data-2d-review-{phase}.json' for phase in PHASES],
             'phase_check_counts':{r['phase']:r['check_count'] for r in results},
             'maximality_claim':False,'arbitrary_data_claim':False}
    (HERE/'data_2d_review.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=(*PHASES,'merge'),required=True)
    arguments=parser.parse_args()
    if arguments.phase=='merge':
        result=merge()
    else:
        started=time.perf_counter();initial=hashes()
        error=None
        try:
            globals()['review_'+arguments.phase]()
        except Exception as exception:
            error=repr(exception)
        unchanged=hashes()==initial
        result={'phase':arguments.phase,'all_checks_passed':error is None and unchanged,
                'check_count':len(CHECKS),'checks':CHECKS,'error':error,
                'inputs_sha256':initial,'input_hashes_unchanged':unchanged,
                'elapsed_seconds':time.perf_counter()-started}
        (HERE/'runs').mkdir(exist_ok=True)
        (HERE/'runs'/f'data-2d-review-{arguments.phase}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('checks','inputs_sha256','reviewed_sha256')},indent=2))
    raise SystemExit(0 if result['all_checks_passed'] else 1)
