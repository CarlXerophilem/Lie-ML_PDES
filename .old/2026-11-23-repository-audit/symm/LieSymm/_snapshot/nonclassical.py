"""Exact finite-candidate conditional-distribution analysis for cubic SVE.

The first-jet conditional criterion is tested before any extra compatibility
constraint is imposed. A compatible graph never changes a failed verdict.
Frozen stage-1/2 sources are read-only inputs. Use serialize_result for JSON.
"""
from __future__ import annotations

from functools import lru_cache
import itertools
import time

import sympy as sp

from models_2d import t,x,y,h,u,v,B,g,K

FIELDS=(h,u,v,B)
COORDINATES=(t,x,y,*FIELDS)
P=sp.Matrix(sp.symbols('h_x u_x v_x B_x',real=True))
R=sp.Matrix(sp.symbols('h_xx u_xx v_xx B_xx',real=True))
UT=sp.Matrix(sp.symbols('h_t u_t v_t B_t',real=True))
UY=sp.Matrix(sp.symbols('h_y u_y v_y B_y',real=True))
A=sp.Matrix([[u,h,0,0],[g,u,0,g],[0,0,u,0],
             [0,K*(3*u*u+v*v),2*K*u*v,0]])
C=sp.Matrix([[v,0,h,0],[0,v,0,0],[g,0,v,g],
             [0,2*K*u*v,K*(u*u+3*v*v),0]])
GUARDS=('g>0','K>0','h>0','u**2+v**2>0','all fields finite and real')


def validate_candidate(candidate):
    a=tuple(sp.sympify(z) for z in candidate['a'])
    b=tuple(sp.sympify(z) for z in candidate['b'])
    c=sp.sympify(candidate['c'])
    if len(a)!=4 or len(b)!=4:
        raise ValueError('Exactly four diagonal coefficients and four shifts are required')
    if any(isinstance(z,bool) for z in (*candidate['a'],*candidate['b'],candidate['c'])):
        raise ValueError('Boolean values are not exact rational coefficients')
    if any(z.is_Rational is not True for z in (*a,*b,c)):
        raise ValueError('This finite proposal class uses fixed exact rational coefficients')
    return c,a,b


def _directional(matrix,direction):
    return matrix.applyfunc(lambda entry:sp.expand(sum(
        direction[j]*sp.diff(entry,FIELDS[j]) for j in range(4))))


@lru_cache(maxsize=3)
def _matrix_data(c):
    matrix=A-c*sp.eye(4)
    w=u-c
    second=g*K*(3*u*u+v*v)*w+c*(w*w-g*h)
    determinant=-w*second
    if sp.expand(matrix.det()-determinant)!=0:
        raise AssertionError('Characteristic determinant mismatch')
    return matrix,sp.factor(determinant),matrix.adjugate(),sp.expand(second)


def conditional_system(c,a,b):
    """Original E,Q, their order-two consequences, and exact criterion identity."""
    c,a,b=validate_candidate({'c':c,'a':a,'b':b})
    D=sp.diag(*a)
    phi=D*sp.Matrix(FIELDS)+sp.Matrix(b)
    M,determinant,adjugate,second=_matrix_data(c)
    E=UT+A*P+C*UY
    Qy=-UY
    Qflow=phi-UT-c*P
    joint=M*P+phi
    N=_directional(A,phi)+A*D-D*A
    off_shell_action=D*E+N*P+(_directional(C,phi)+C*D-D*C)*UY
    on_Q_action=D*joint+N*P
    mixed=D*P-c*R
    tt=D*phi-2*c*D*P+c*c*R
    dxE=M*R+_directional(A,P)*P+D*P
    dtE=D*(phi-c*P)+_directional(A,phi-c*P)*P+M*mixed
    compatibility=(dtE+c*dxE-on_Q_action).applyfunc(sp.expand)
    V1=sp.Matrix([0,0,1,0,0,0,0])
    V2=sp.Matrix([1,c,0,*phi])
    bracket=(V2.jacobian(COORDINATES)*V1-V1.jacobian(COORDINATES)*V2).applyfunc(sp.expand)
    projection=sp.Matrix.hstack(V1[:3,0],V2[:3,0])
    return {'model':'grass_cubic_f0','phi':phi,'diagonal_matrix':D,
            'generators':(V1,V2),'projection_matrix':projection,
            'projection_rank':2,'projection_minor_t_y':projection[[0,2],:].det(),
            'involutivity_residual':bracket,'original_PDE':E,
            'Q_y':Qy,'Q_flow':Qflow,'joint_first_order_equations':joint,
            'leading_matrix':M,'determinant':determinant,
            'characteristic_factors':(u-c,second),'adjugate':adjugate,
            'conditional_matrix':N,'prolonged_PDE_before_Q':off_shell_action,
            'prolonged_PDE_on_Q':on_Q_action,'conditional_residual_mod_joint':N*P,
            'differential_consequences':{
                'U_t':phi-c*P,'U_y':sp.zeros(4,1),'U_tx':mixed,'U_tt':tt,
                'U_xy':sp.zeros(4,1),'U_yy':sp.zeros(4,1),'U_ty':sp.zeros(4,1),
                'D_x_E_on_Q_and_DQ':dxE,'D_t_E_on_Q_and_DQ':dtE,
                'D_y_E_on_Q_and_DQ':sp.zeros(4,1),
                'compatibility_identity_remainder':compatibility,
                'meaning':'(D_t+c D_x)E = D*(M*p+phi)+N*p after Q and DQ; adding this compatibility condition cannot prove conditional invariance on the original first-jet locus'},
            'guards':GUARDS}


def _positive_parameter_obstruction(numerators):
    """A nonzero same-sign polynomial coefficient cannot vanish for g,K>0."""
    for row,value in enumerate(numerators):
        for powers,coefficient in sp.Poly(value,*FIELDS).terms():
            if coefficient==0:
                continue
            parameter_polynomial=sp.Poly(coefficient,g,K)
            terms=parameter_polynomial.terms()
            signs={sp.sign(number) for _,number in terms}
            if len(signs)==1 and signs in ({sp.S.One},{sp.S.NegativeOne}):
                return {'row':row,'field_powers':powers,'coefficient':sp.factor(coefficient),
                        'parameter_monomials':terms,
                        'proof':'Every monomial has the same nonzero sign and g,K are strictly positive; this field-polynomial coefficient is nonzero for every admitted parameter pair.'}
    return None


def _regular_witness(system,numerators):
    # A witness illustrates the exact polynomial proof; no finite sampling
    # establishes acceptance or parameter-uniform rejection.
    states=itertools.product((2,1,3),(2,3,-2,1),(1,0,2),(1,0,-1),(1,2),(1,2))
    for values in states:
        at=dict(zip((h,u,v,B,g,K),map(sp.Rational,values)))
        determinant=system['determinant'].subs(at)
        if determinant==0 or at[u]**2+at[v]**2==0:
            continue
        residual=sp.Matrix(numerators).subs(at)/determinant
        if all(z==0 for z in residual):
            continue
        p=(-system['adjugate']*system['phi']).subs(at)/determinant
        joint=(system['leading_matrix'].subs(at)*p+system['phi'].subs(at)).applyfunc(sp.simplify)
        actual=(system['conditional_matrix'].subs(at)*p).applyfunc(sp.simplify)
        if any(z!=0 for z in joint) or actual!=residual:
            raise AssertionError('Conditional-failure witness does not satisfy the joint system')
        return {'state':at,'U_x':p,'U_y':sp.zeros(4,1),
                'U_t':system['phi'].subs(at)-system['generators'][1][1]*p,
                'determinant':determinant,'joint_residual':joint,
                'conditional_residual':actual,'kind':'compatible_first_jet_not_a_claimed_solution'}
    return {'status':'no_small_witness_found','proof_remains':_positive_parameter_obstruction(numerators)}


def _time_split(expression):
    groups={}
    for term in sp.Add.make_args(sp.expand(expression)):
        rate=sp.S.Zero
        coefficient=sp.S.One
        power=0
        for factor in sp.Mul.make_args(term):
            if factor.func==sp.exp:
                factor_rate=sp.diff(factor.args[0],t)
                if factor_rate.has(t) or sp.expand(factor.args[0]-factor_rate*t)!=0:
                    raise ValueError('Nonlinear exponential time argument')
                rate+=factor_rate
            elif factor==t:
                power+=1
            elif isinstance(factor,sp.Pow) and factor.base==t and factor.exp.is_Integer and factor.exp>=0:
                power+=int(factor.exp)
            else:
                coefficient*=factor
        if coefficient.has(t):
            raise ValueError('Unsplit time-dependent coefficient')
        groups[(rate,power)]=groups.get((rate,power),0)+coefficient
    return tuple({'exp_rate':rate,'time_power':power,'equation':sp.factor(value)}
                 for (rate,power),value in sorted(groups.items()) if sp.expand(value)!=0)


def invariant_graph(c,a,b):
    """Integrate Q and pull back E, retaining every time-split implicit DAE."""
    c,a,b=validate_candidate({'c':c,'a':a,'b':b})
    z=sp.Symbol('z',real=True)
    F=sp.Matrix(sp.symbols('H U V Z',real=True))
    dF=sp.Matrix(sp.symbols('H_z U_z V_z Z_z',real=True))
    graph=sp.Matrix([sp.exp(ai*t)*fi+bi*(sp.exp(ai*t)-1)/ai if ai else fi+bi*t
                     for ai,bi,fi in zip(a,b,F)])
    inverse=sp.Matrix([sp.exp(-ai*t)*(field-bi*(sp.exp(ai*t)-1)/ai) if ai else field-bi*t
                       for ai,bi,field in zip(a,b,FIELDS)])
    Dz=lambda expression:sp.expand(sum(sp.diff(expression,fi)*pi for fi,pi in zip(F,dF)))
    Dt=lambda expression:sp.diff(expression,t)-c*Dz(expression)
    H,U,V,Z=graph
    original_pullback=sp.Matrix([Dt(H)+Dz(H*U),Dt(U)+U*Dz(U)+g*Dz(H+Z),
                                Dt(V)+U*Dz(V),Dt(Z)+K*Dz((U*U+V*V)*U)]).applyfunc(sp.expand)
    from_matrix=(graph.diff(t)+(A-c*sp.eye(4)).subs(dict(zip(FIELDS,graph)),simultaneous=True)
                 *graph.jacobian(F)*dF).applyfunc(sp.expand)
    reconstruction=(original_pullback-from_matrix).applyfunc(sp.expand)
    split=tuple(_time_split(row) for row in original_pullback)
    time_remainders=tuple(sp.expand(row-sum(term['equation']*t**term['time_power']
                           *sp.exp(term['exp_rate']*t) for term in terms))
                          for row,terms in zip(original_pullback,split))
    Q=(sp.diag(*a)*graph+sp.Matrix(b)-graph.diff(t)).applyfunc(sp.expand)
    inverse_remainders=(inverse.subs(dict(zip(FIELDS,graph)),simultaneous=True)-F).applyfunc(sp.simplify)
    jacobian=sp.exp(sum(a)*t)
    return {'status':'verified_graph_pullback' if all(value==0 for value in
             (*reconstruction,*time_remainders,*Q,*inverse_remainders)) else 'failed_graph_pullback',
            'remaining_variable':z,'base_invariant':x-c*t,'field_invariants':inverse,
            'profile_symbols':F,'profile_derivative_symbols':dF,'graph':graph,
            'base_coordinate_map':(t,x-c*t,y),'base_jacobian':sp.S.One,
            'field_jacobian':jacobian,'Q_residuals':Q,'inverse_residuals':inverse_remainders,
            'original_PDE_pullback':original_pullback,'matrix_pullback':from_matrix,
            'original_PDE_reconstruction_residuals':reconstruction,
            'profile_DAE_time_coefficients':split,'time_reconstruction_residuals':time_remainders,
            'time_split_basis':'Distinct finite t^k*exp(r*t), rational r and nonnegative integer k, are independent on every open time interval.',
            'formal_DAE_status':'exact_implicit_profile_conditions; global formal integrability not inferred',
            'profile_or_characteristic_divisions':(),
            'guards':('finite real t','h(t,z)>0','u(t,z)**2+v(t,z)**2>0'),
            'conditional_invariance_inferred_from_graph':False}


def _singular_analysis(system,a,b,c,regular_passed):
    zero=(sp.S.Zero,)*4
    implicit={'equations':system['joint_first_order_equations'],
              'characteristic_equation':system['determinant'],
              'discarded':False,'extra_compatibility_must_not_relabel_failed_candidate':True}
    if system['conditional_matrix']==sp.zeros(4):
        result={'status':'all_compatible_jets_verified','proof':'N=0 identically, including both characteristic factors.',
                'implicit_DAE':implicit}
        if a==zero and b[:3]==zero[:3]:
            q=b[3]
            result['u_equals_c_branch']={'conditions':('u=c','p_u=0','p_B=-p_h'),
                'remaining_equation':c*(P[0]+2*K*v*P[2])+q,
                'compatibility':'if c=0, b_B must vanish; if c!=0 this is an exact implicit relation with p_v free'}
            result['second_characteristic_branch']={
                'guards':('u-c!=0','second characteristic factor = 0'),
                'remaining_equations':(P[2],(u-c)*P[0]+h*P[1],g*(P[0]+P[3])+(u-c)*P[1],q),
                'compatibility':'b_B!=0 gives no jets; b_B=0 retains this singular implicit DAE and its differentiated constraints; no full singular-profile classification claimed'}
        return result
    if regular_passed and c==0 and a==zero and b[0]!=0 and b[1:]==zero[1:]:
        q=b[0]
        return {'status':'no_compatible_jets','stratum':'u=0,v!=0',
                'contradiction_combination':'K*v^2*(mass joint row)-h*(bed joint row)',
                'contradiction':K*v*v*q,
                'proof':'K*v^2>0 and b_h!=0; all compatible first jets lie on u!=0.',
                'implicit_DAE':implicit}
    if regular_passed and c==0 and a==zero and b[1]!=0 and b[0]==b[2]==b[3]==0:
        q=b[1]
        at={h:sp.S.One,u:sp.S.Zero,v:sp.S.One,B:sp.S.Zero,g:sp.S.One,K:sp.S.One}
        p=sp.Matrix([1,0,0,-q-1])
        joint=(system['leading_matrix'].subs(at)*p+system['phi'].subs(at)).applyfunc(sp.expand)
        obstruction=(system['conditional_matrix'].subs(at)*p).applyfunc(sp.expand)
        return {'status':'failed_on_compatible_jets','stratum':'u=0,v!=0',
                'joint_constraints':('p_u=0','g*(p_h+p_B)=-b_u','p_h and p_v free'),
                'witness':{'state':at,'U_x':p,'U_y':sp.zeros(4,1),'U_t':system['phi'].subs(at),
                           'joint_residual':joint,'conditional_residual':obstruction},
                'failure_scope':'First-jet conditional invariance fails here; a particular smooth solution may still cross this locus.',
                'implicit_DAE':implicit}
    return {'status':'not_resolved_for_rejected_candidate' if not regular_passed else 'unresolved',
            'implicit_DAE':implicit,
            'scope':'No claim excluding compatible solutions or singular conditional subbranches is inferred from the rejected ambient candidate.'}


def compatible_families(c,a,b):
    """Constructed solutions are separate evidence, never a criterion shortcut."""
    zero=(sp.S.Zero,)*4
    H0=sp.Symbol('H0',positive=True)
    U0,V0,B0=sp.symbols('U0 V0 B0',real=True)
    graphs=[]
    if a==zero and c==0 and b[0]!=0 and b[1:]==zero[1:]:
        q=b[0]
        graphs.append(('h_shift',(H0+q*t-q*x/U0,U0,V0,B0+q*x/U0),
                       ('U0!=0','H0+b_h*t-b_h*x/U0>0')))
    elif a==zero and c==0 and b[1]!=0 and b[0]==b[2]==b[3]==0:
        q=b[1]
        graphs.append(('u_shift',(H0,U0+q*t,V0,B0-q*x/g),
                       ('U0+b_u*t!=0 for conditional certification','h>0','u^2+v^2>0')))
    elif a==zero and b[:3]==zero[:3]:
        q=b[3]
        if c!=0:
            z=x-c*t
            W=sp.Function('W')(z)
            depth=H0-K*W*W-q*z/c
            graphs.append(('singular_u_equals_c',(depth,c,W,q*t+B0-depth),
                           ('h>0','u=c!=0','arbitrary smooth W(z)')))
        elif q==0:
            depth=sp.Function('H')(x)
            W=sp.Function('W')(x)
            graphs.append(('singular_stationary_transverse_shear',(depth,0,W,B0-depth),
                           ('H(x)>0','W(x)!=0')))
        if q==0:
            graphs.append(('uniform_flow',(H0,U0,V0,B0),('U0^2+V0^2>0',)))
    results=[]
    for label,raw,guards in graphs:
        H,U,V,Z=map(sp.sympify,raw)
        E=(sp.diff(H,t)+sp.diff(H*U,x)+sp.diff(H*V,y),
           sp.diff(U,t)+U*sp.diff(U,x)+V*sp.diff(U,y)+g*sp.diff(H+Z,x),
           sp.diff(V,t)+U*sp.diff(V,x)+V*sp.diff(V,y)+g*sp.diff(H+Z,y),
           sp.diff(Z,t)+K*(sp.diff((U*U+V*V)*U,x)+sp.diff((U*U+V*V)*V,y)))
        Q=tuple(ai*field+bi-sp.diff(field,t)-c*sp.diff(field,x)
                for ai,bi,field in zip(a,b,(H,U,V,Z)))
        residuals=tuple(sp.simplify(value) for value in (*E,*Q))
        results.append({'name':label,'graph':(H,U,V,Z),'guards':guards,
                        'PDE_residuals':residuals[:4],'Q_residuals':residuals[4:],
                        'status':'verified_constructed_solution' if all(z==0 for z in residuals) else 'failed_reconstruction',
                        'initial_profiles':tuple(field.subs(t,0) for field in (H,U,V,Z)),
                        'conditional_symmetry_inferred':False})
    implicit=None
    if a==zero and b[:3]==zero[:3]:
        q=b[3]
        z=sp.Symbol('z',real=True)
        J,E0,S0=sp.symbols('J E0 S0',real=True)
        w=u-c
        depth=J/w
        bed=E0/g-w*w/(2*g)-depth
        relation=K*(u*u+V0*V0)*u-c*bed+q*z-S0
        implicit={'name':'regular_traveling_bed_drift_first_integrals',
                  'velocity_profile_equation':sp.Eq(relation,0),
                  'profiles':(depth,u,V0,bed),'bed_reconstruction':'B(t,x)=b_B*t+bed(x-c*t)',
                  'regularity_factor':sp.factor(sp.diff(relation,u)),
                  'guards':('u-c!=0','J/(u-c)>0','u^2+V0^2>0','d(implicit relation)/du!=0'),
                  'existence':'At any real initial root with these strict guards, the implicit function theorem gives a unique local smooth u(z); the three exact first integrals reconstruct E=Q=0.',
                  'first_integrals':(h*(u-c),(u-c)**2/2+g*(h+B),K*(u*u+v*v)*u-c*B+q*z),
                  'conditional_symmetry_inferred':False}
    return {'explicit_families':results,'implicit_regular_family':implicit,
            'scope':'Specified local solution branches only; no general DAE or arbitrary data theorem.'}


def analyze_candidate(candidate,require_gate=True):
    """Evaluate one exact recorded affine candidate; no finite-class maximality."""
    start=time.perf_counter()
    if require_gate:
        from gatekeeper import check_gate
        gate=check_gate(2)
        if not gate['passed']:
            raise ValueError('Current Stage 2 gate required before conditional evaluation: '+str(gate))
    else:
        gate={'passed':None,'reason':'explicit mathematical unit-test mode; not release evidence'}
    c,a,b=validate_candidate(candidate)
    system=conditional_system(c,a,b)
    numerators=(-system['conditional_matrix']*system['adjugate']*system['phi']).applyfunc(sp.expand)
    regular_passed=all(value==0 for value in numerators)
    positive_obstruction=None if regular_passed else _positive_parameter_obstruction(numerators)
    singular=_singular_analysis(system,a,b,c,regular_passed)
    if regular_passed:
        regular_status='verified'
        if singular['status'] in ('all_compatible_jets_verified','no_compatible_jets'):
            status='verified_conditional_on_declared_chart'
        elif singular['status']=='failed_on_compatible_jets':
            status='verified_conditional_on_regular_subchart'
        else:
            status='unresolved_singular_conditional_strata'
    else:
        regular_status='failed' if positive_obstruction else 'unresolved_parameter_stratum'
        status='failed_conditional_criterion' if positive_obstruction else 'unresolved_conditional_parameter_stratum'
    F=(-system['adjugate']*system['phi']/system['determinant']).applyfunc(sp.cancel)
    if regular_passed:
        commutator=(F.jacobian(FIELDS)*system['phi']-system['diagonal_matrix']*F).applyfunc(sp.cancel)
        if any(value!=0 for value in commutator):
            raise AssertionError('Accepted regular candidate failed Frobenius compatibility')
    else:
        commutator=None
    graph=invariant_graph(c,a,b)
    if graph['status']!='verified_graph_pullback':
        raise AssertionError('Graph pullback verification failed')
    families=compatible_families(c,a,b)
    if any(row['status']!='verified_constructed_solution' for row in families['explicit_families']):
        raise AssertionError('Constructed family failed direct reconstruction')
    return {'candidate_id':candidate.get('id'),'candidate':dict(candidate),'model':'grass_cubic_f0',
            'conditional_status':status,'regular_chart_status':regular_status,
            'singular_status':singular['status'],'conditional_admitted':regular_passed,
            'global_chart_admitted':status=='verified_conditional_on_declared_chart',
            'independent_review_status':'pending_fresh_review','preceding_gate':gate,
            'distribution':{'generators':system['generators'],'projection_rank':2,
                            'projection_minor_t_y':system['projection_minor_t_y'],
                            'involutivity_residual':system['involutivity_residual']},
            'joint_system':system,'regular_chart':{
                'guard':sp.Ne(system['determinant'],0,evaluate=False),
                'profile_vector_field':F,'conditional_numerators':numerators,
                'positive_parameter_obstruction':positive_obstruction,
                'Frobenius_commutator':commutator,
                'Frobenius_identity':'M*[phi,F]=-N*F, with F=-M^{-1}phi; acceptance checks this is zero.',
                'rejection_witness':None if regular_passed else _regular_witness(system,numerators)},
            'singular_analysis':singular,'implicit_DAE':graph['profile_DAE_time_coefficients'],
            'invariant_graph':graph,'compatible_families':families,
            'additional_conditional_guards':('u!=0',) if status=='verified_conditional_on_regular_subchart' else (),
            'not_claimed':['unrestricted nonclassical classification','novelty','classical distribution inequivalence',
                           'complete singular-profile classification','arbitrary data compatibility','ML training'],
            'elapsed_seconds':time.perf_counter()-start}


def serialize_result(result):
    from main import json_ready
    return json_ready(result)
