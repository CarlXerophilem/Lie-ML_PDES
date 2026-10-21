"""Independent data/parent-model review, excluding first-order proof approval.

This reviewer uses direct differential residuals rather than graph_check as
the oracle for constructed flows, and checks parent material identities from
Eulerian derivative operators. It writes only its own review receipt.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time

import sympy as sp

import data_experiments as data
import parent_models as parent
from main import json_ready
from models import BRANCHES,t,x,h,u,B,g,K,G,m,n

HERE=Path(__file__).resolve().parent


def review():
    start=time.perf_counter()
    checks=[]
    qualifications=[]

    def check(name, condition, evidence=None):
        checks.append({'name':name,'passed':bool(condition),'evidence':evidence})

    def zero(name, expression):
        values=list(expression) if isinstance(expression,(tuple,list,sp.MatrixBase)) else [expression]
        simplified=[sp.simplify(v) for v in values]
        check(name,all(v==0 for v in simplified),simplified)

    # Independent original-PDE oracle: differentiate the actual graph without
    # calling the shared jet engine, graph_check, or a generator verifier.
    def original_residual(branch,graph,substitutions=None):
        H,U,Z=graph
        cell=BRANCHES[branch]
        flux=K*U**cell['m'] if cell['K'] else sp.S.Zero
        if cell['G']:
            flux-=G*U**cell['n']*sp.diff(Z,x)
        residual=(sp.diff(H,t)+sp.diff(H*U,x),
                  sp.diff(U,t)+U*sp.diff(U,x)+g*sp.diff(H+Z,x),
                  sp.diff(Z,t)+sp.diff(flux,x))
        return tuple(sp.simplify(v.subs(substitutions or {},simultaneous=True)) for v in residual)

    for branch in BRANCHES:
        for kind,result in (
            ('uniform',data.uniform_flow(branch,depth=5,velocity=7,datum=-2)),
            ('slope',data.constant_slope_flow(branch,depth=5,velocity=7,slope=sp.Rational(-2,3),datum=-2,time0=4))):
            zero(branch+'_'+kind+'_independent_PDE',original_residual(branch,result['graph']))
            check(branch+'_'+kind+'_status_scope',result['status']=='verified_exact_solution'
                  and not result['arbitrary_data_claim'],result['chart_guards'])
        for label,bed,expected in [('flat',1,1 if BRANCHES[branch]['G'] else 2),
                                   ('linear',1-2*x,1),('quadratic',1+3*x*x,0)]:
            result=data.initial_data_stabilizer(branch,(2,3,bed),time0=4)
            check(branch+'_'+label+'_independent_stabilizer_dimension',result.get('dimension')==expected,
                  {'dimension':result.get('dimension'),'status':result['status']})
            tau,xi,H,U,Z=result['stabilized_coefficients']
            at={t:4,h:2,u:3,B:sp.sympify(bed)}
            zero(branch+'_'+label+'_independent_tangency',[
                tau.subs(at,simultaneous=True),H.subs(at,simultaneous=True),
                U.subs(at,simultaneous=True),
                (Z-xi*sp.diff(sp.sympify(bed),x)).subs(at,simultaneous=True)])
            check(branch+'_'+label+'_no_evolution_claim',not result['pde_solution_claim'])
        fixed=data.initial_data_stabilizer(branch,(2,3,1),time0=4,endpoints=(-1,2))
        check(branch+'_two_endpoints_remove_initial_stabilizer',fixed['dimension']==0,
              fixed['stabilized_coefficients'])

    slope=sp.Symbol('review_profile_slope',real=True)
    conditional=data.initial_data_stabilizer('grass_generic',(2,3,1+slope*x))
    check('unknown_profile_slope_retains_rank_branch',
          conditional['status']=='conditional_initial_data_stabilizer'
          and bool(conditional['rank_guards']) and bool(conditional['unresolved_zero_pivot_branches']),
          {k:conditional[k] for k in ('dimension','rank_guards','unresolved_zero_pivot_branches')})
    flat=data.initial_data_stabilizer('grass_generic',(2,3,1))
    check('zero_profile_slope_rank_drop_is_real',flat['dimension']==2 and conditional['dimension']==1)
    exponent_rank=data.initial_data_stabilizer('slope_only',(x*x,x,x*x))
    special=data.initial_data_stabilizer('slope_only',(x*x,x,x*x),substitutions={n:2})
    check('slope_exponent_rank_guard_and_n_two_branch',
          exponent_rank['status']=='conditional_initial_data_stabilizer'
          and bool(exponent_rank['rank_guards']) and special['dimension']==1,
          {'generic_dimension':exponent_rank.get('dimension'),'guards':exponent_rank.get('rank_guards'),
           'n_two_dimension':special.get('dimension')})

    # General projectable scaling weights provide an independent flux oracle.
    T,X,V,W=sp.symbols('review_T review_X review_V review_W',real=True)
    for branch in BRANCHES:
        result=data.sediment_flux_variation(branch,(T*t,X*x,0,V*u,W*B))
        cell=BRANCHES[branch]
        expected=cell['m']*V*K*u**cell['m'] if cell['K'] else sp.S.Zero
        if cell['G']:
            expected-=G*(cell['n']*V+W-X)*u**cell['n']*result['bed_slope_jet']
        zero(branch+'_independent_flux_weight',result['variation']-expected)
        zero(branch+'_independent_slope_weight',result['slope_variation']-(W-X)*result['bed_slope_jet'])
    tilted=data.sediment_flux_variation('slope_attachment_cubic',(x,0,0,0,0))
    bed_t=sp.Symbol('B__1_0',real=True)
    zero('flux_prolongation_retains_B_t_Dx_tau',tilted['variation']-G*u*u*bed_t)

    wrong=data.initial_data_stabilizer('grass_cubic',(2,3,1),sediment_flux=0)
    check('incompatible_flux_rejected',wrong['status']=='incompatible_prescribed_flux',wrong['flux_data'])
    initial_only=data.initial_data_stabilizer('grass_cubic',(2,3,1),time0=4,
                                               sediment_flux={0:27*K+(t-4),1:27*K-(t-4)})
    check('time_dependent_flux_only_initial_trace',initial_only['status']=='verified_initial_data_stabilizer'
          and initial_only['dimension']==0 and 'initial slice' in initial_only['boundary_scope'],
          initial_only['flux_data']['compatibility_residuals'])

    invalid=[('grass_generic',{m:3}),('grass_generic',{m:0}),('grass_generic',{m:5}),
             ('grass_generic',{g:0}),('grass_generic',{g:-1}),
             ('grass_generic',{K:0}),('grass_generic',{K:-1}),('grass_generic',{K:sp.I}),
             ('slope_only',{G:0}),('slope_only',{G:-1}),('slope_only',{G:sp.I}),
             ('slope_only',{n:-1}),('slope_only',{n:5})]
    for branch,substitutions in invalid:
        try:
            result=data.uniform_flow(branch,substitutions=substitutions)
        except (ValueError,TypeError) as error:
            check('reject_invalid_'+branch+'_'+str(substitutions),True,str(error))
        else:
            check('reject_invalid_'+branch+'_'+str(substitutions),False,result)

    # Record rather than hide symbolic/nonreal input behavior at this API boundary.
    r=sp.Symbol('review_parameter',real=True)
    symbolic=data.uniform_flow('grass_generic',substitutions={g:r})
    guards=symbolic.get('parameter_guards',())
    if not any('review_parameter' in str(v) for v in guards):
        qualifications.append({'code':'symbolic_guard_provenance',
            'finding':'A symbolic g replacement is accepted, but reported parameter guards retain g>0 instead of explicitly requiring the replacement positive.',
            'observed_status':symbolic['status'],'observed_guards':guards,
            'scope':'symbolic substitution API; default and valid numeric review cases unaffected'})
    try:
        nonreal=data.uniform_flow('grass_generic',substitutions={g:sp.I})
    except (ValueError,TypeError):
        check('nonreal_positive_parameter_rejected',True)
    else:
        check('nonreal_positive_parameter_rejected',False,nonreal)

    static=data.lake_control('slope_only',bed=x*x,level=5,substitutions={n:0})
    moving=data.lake_control('slope_only',bed=x*x+2*G*t,level=5+2*G*t,substitutions={n:0})
    symbolic_lake=data.lake_control('slope_only',bed=1,level=5,substitutions={n:0,G:r})
    check('zero_speed_report_carries_specialized_parameter_guards',
          any('review_parameter' in str(v) for v in symbolic_lake.get('parameter_guards',()))
          and symbolic_lake.get('parameter_substitutions',{}).get(G)==r,
          {k:symbolic_lake.get(k) for k in ('parameter_guards','parameter_substitutions')})
    zero('static_zero_speed_diffusion_negative_control',
         sp.Matrix(static['check']['equation_residuals'])-sp.Matrix([0,0,-2*G]))
    zero('moving_zero_speed_diffusion_solution',original_residual('slope_only',moving['graph'],{n:0}))
    check('zero_speed_chart_disclaimer',not moving['inside_classified_positive_speed_chart']
          and 'polynomial' in moving['scope'])
    for branch,substitutions in [('grass_generic',{}),('grass_generic',{m:2}),
                                  ('slope_only',{n:1}),('slope_only',{n:3}),
                                  ('slope_source_cubic',{})]:
        result=data.lake_control(branch,bed=1,level=5,substitutions=substitutions)
        check('reject_unapproved_zero_extension_'+branch+'_'+str(substitutions),
              result['status']=='outside_declared_chart' and result['check'] is None)

    # Parent controls from independent Eulerian/material chain rules.
    z=parent.scalar_models()
    tt,ss,phi,bed,q,v,gg,kk,mm=(z[k] for k in ('t','s','phi','bed','q','v','g','K','m'))
    Dx=lambda f:sp.diff(f,ss)/q
    Dt=lambda f:sp.diff(f,tt)-v*sp.diff(f,ss)/q
    depth=1/q
    zero('material_chain_continuity',Dt(depth)+Dx(depth*v))
    original_momentum=Dt(v)+v*Dx(v)+gg*Dx(depth+bed)
    zero('material_chain_momentum_sign',q*original_momentum-z['A']-gg*sp.diff(bed,ss))
    original_bed=Dt(bed)+Dx(kk*v**mm)
    zero('material_chain_Exner_sign',original_bed-(sp.diff(bed,tt)-v*sp.diff(bed,ss)/q+z['C']))
    original_relative=sp.diff(q*bed,tt)+sp.diff(kk*v**mm-v*bed,ss)
    zero('relative_flux_from_original_exner',original_relative-q*original_bed)
    zero('P_is_printed_closedness',sp.diff(z['bed_s'],tt)-sp.diff(z['bed_t_P'],ss)+z['P']/gg)
    zero('M_is_material_closedness',sp.diff(z['bed_s'],tt)-sp.diff(z['bed_t_M'],ss)+z['M']/gg)
    c=sp.Symbol('review_speed',positive=True)
    phi0=ss*ss/2+c*tt
    P=sp.simplify(z['P'].subs(phi,phi0).doit())
    M=sp.simplify(z['M'].subs(phi,phi0).doit())
    zero('printed_counterexample_P',P)
    zero('printed_counterexample_M_defect',M+3*gg*c/ss**4)
    check('printed_counterexample_is_nonzero',M!=0)
    parent_result=parent.verify_scalar_and_material()
    check('parent_report_checks_pass',parent_result['all_passed'])
    check('parent_does_not_claim_point_equivalence',not parent_result['point_algebra_equivalence_claim'])

    source=parent.source_receipt()
    expected_ids={'R01','R02','R03','R04','R07','R08'}
    actual_ids={item['id'] for item in source['sources']}
    check('primary_source_ID_coverage',actual_ids==expected_ids,sorted(actual_ids))
    check('primary_source_bytes_match',source['all_matched'])
    check('source_provenance_not_claimed_as_new_web_retrieval',source['new_web_retrieval'] is False)

    paths=['data_experiments.py','parent_models.py','models.py','main.py',
           'research_first_order.py','research_slope.py','tests/test_data_experiments.py',
           'tests/test_parent_models.py','review_data_parent.py']
    hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in paths}
    passed=all(item['passed'] for item in checks)
    return {'review_status':'accepted_with_qualifications' if passed and qualifications else
                            'accepted' if passed else 'rejected_pending_repairs',
            'all_checks_passed':passed,'check_count':len(checks),'checks':checks,
            'qualifications':qualifications,'reviewed_sha256':hashes,
            'source_ledger_sha256':source['source_ledger_sha256'],
            'elapsed_seconds':time.perf_counter()-start,
            'per_process_timeout_seconds':60,
            'scope':['constructed exact flows','specified initial-data stabilizers',
                     'parameter and profile pivot guards','first-prolonged sediment flux',
                     'signed polynomial zero-speed extensions','P/M separation',
                     'mass-coordinate signs and guards','live source byte hashes'],
            'not_reviewed':['first-order maximality proof authored by this reviewer',
                            'slope maximality proof','2D classification','global well-posedness',
                            'future-time boundary invariance','new web citation retrieval']}


if __name__=='__main__':
    receipt=review()
    target=HERE/'review_data_parent_results.json'
    target.write_text(json.dumps(json_ready(receipt),indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:receipt[key] for key in ('review_status','all_checks_passed','check_count','elapsed_seconds')},indent=2))
    print('receipt:',target)
    raise SystemExit(0 if receipt['all_checks_passed'] else 1)
