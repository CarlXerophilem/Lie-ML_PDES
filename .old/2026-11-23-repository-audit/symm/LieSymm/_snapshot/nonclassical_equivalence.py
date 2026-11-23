"""Classical distribution equivalence for the frozen Stage 3 affine family.

A distribution can have a classical representative even when a chosen
variable-coefficient frame does not consist of classical generators. This
module computes the ENTIRE constant classical algebra tangent to the
distribution, then tests its evaluated rank. Conditional invariance of the
PDE is a different calculation and is never inferred here.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

import sympy as sp

import classification_2d
from models_2d import t,x,y,h,u,v,B,g,K
from research_first_order_2d import general_solution

HERE=Path(__file__).resolve().parent
COORDINATES=(t,x,y,h,u,v,B)
FIELDS=(h,u,v,B)
FROZEN_REGISTRY_SHA256='2409ee048ab8ed66bdf4d0840a34a95b6ea380fdb72c2aedc29ce84382b3b764'
CLASSICAL='verified_classical_distribution'
NONCLASSICAL='no_classical_representative_on_open_ambient_chart'


def _clean(value):
    return sp.factor(sp.cancel(sp.sympify(value)))


def _constant(value):
    value=sp.sympify(value)
    if value.free_symbols.intersection(COORDINATES) or value.atoms(sp.Function):
        raise ValueError('Candidate coefficients must be independent of point coordinates')
    if value.has(sp.Float):
        raise ValueError('Supply exact constants, such as Rational(1,2), rather than floats')
    if value.is_real is not True or value.is_finite is not True:
        raise ValueError('Candidate coefficients must be declared finite real constants')
    return value


def _candidate(candidate):
    if len(candidate.get('a',()))!=4 or len(candidate.get('b',()))!=4:
        raise ValueError('Each of a,b must have four entries in order h,u,v,B')
    return (_constant(candidate['c']),tuple(map(_constant,candidate['a'])),
            tuple(map(_constant,candidate['b'])))


def _source():
    review=classification_2d.review_gate()
    stage_path=HERE/'STAGE_2_GATE.json'
    stage=json.loads(stage_path.read_text(encoding='utf-8')) if stage_path.exists() else {}
    review={**review,'stage_2_passed':stage.get('passed') is True}
    review['passed']=review.get('passed') is True and review['stage_2_passed']
    solved=general_solution('grass_cubic_f0',COORDINATES)
    basis=tuple(sp.Matrix(q) for q in solved['basis'])
    if len(basis)!=7:
        raise AssertionError('The reviewed cubic G=f=0 source algebra must have dimension seven')
    return review,solved,basis


def _frame(c,a,b,basis_change):
    Y=sp.Matrix([0,0,1,0,0,0,0])
    Q=sp.Matrix([1,c,0,*(aa*field+bb for aa,field,bb in zip(a,FIELDS,b))])
    canonical=sp.Matrix.hstack(Y,Q)
    change=sp.eye(2) if basis_change is None else sp.Matrix(basis_change)
    if change.shape!=(2,2):
        raise ValueError('A distribution basis change must be a 2 by 2 matrix')
    guards=[]
    for value in change:
        if value.has(sp.nan,sp.zoo,sp.oo,-sp.oo,sp.Float):
            raise ValueError('Frame coefficients must be exact finite real functions on their chart')
        numerator,denominator=sp.fraction(sp.cancel(value))
        if numerator.is_real is not True or denominator.is_real is not True:
            raise ValueError('Declare real frame coefficients and their point coordinates')
        if denominator.is_nonzero is not True:
            guards.append(sp.Ne(denominator,0,evaluate=False))
    determinant=_clean(change.det())
    if determinant==0:
        raise ValueError('A change of distribution basis must be invertible')
    if determinant.is_nonzero is not True:
        guards.append(sp.Ne(determinant,0,evaluate=False))
    inverse=change.inv().applyfunc(_clean)
    if (change*inverse-sp.eye(2)).applyfunc(_clean)!=sp.zeros(2):
        raise AssertionError('Frame inverse failed')
    return canonical,change,inverse,tuple(dict.fromkeys(guards))


def _polynomial_equations(identities):
    equations=[]
    for identity in identities:
        equations.extend(sp.Poly(sp.expand(identity),*COORDINATES).coeffs())
    return tuple(dict.fromkeys(value for value in equations if value!=0))


def _constant_classical_coordinates(vector,basis):
    constants=sp.symbols('classical_coordinate_0:7',real=True)
    difference=sp.Matrix.hstack(*basis)*sp.Matrix(constants)-sp.Matrix(vector)
    equations=_polynomial_equations(difference)
    solutions=tuple(sp.linsolve(equations,constants))
    if len(solutions)!=1 or any(value.has(*constants,*COORDINATES) for value in solutions[0]):
        raise AssertionError('Claimed fixed generator has no unique constant classical coefficients')
    return sp.Matrix(solutions[0])


def _bracket(left,right):
    return (right.jacobian(COORDINATES)*left-left.jacobian(COORDINATES)*right).applyfunc(_clean)


def _characteristics(vector,graph):
    substitution=dict(zip(FIELDS,graph))
    vector=sp.Matrix(vector).subs(substitution,simultaneous=True)
    return tuple(_clean(vector[3+i]-sum(vector[j]*sp.diff(profile,coordinate)
                 for j,coordinate in enumerate((t,x,y)))) for i,profile in enumerate(graph))


def _pde_on_graph(graph):
    H,U,V,Z=map(sp.sympify,graph)
    speed=U*U+V*V
    return tuple(_clean(value) for value in (
        sp.diff(H,t)+sp.diff(H*U,x)+sp.diff(H*V,y),
        sp.diff(U,t)+U*sp.diff(U,x)+V*sp.diff(U,y)+g*sp.diff(H+Z,x),
        sp.diff(V,t)+U*sp.diff(V,x)+V*sp.diff(V,y)+g*sp.diff(H+Z,y),
        sp.diff(Z,t)+sp.diff(K*speed*U,x)+sp.diff(K*speed*V,y)))


def solution_family_containment(candidate):
    """Four pure c=0 shift cases: complete local families are classically invariant.

    The proof uses the t coefficient in the mass identity after integrating
    the candidate invariant-surface equations. This does not establish the
    nonclassical criterion at arbitrary first jets, including singular jets.
    """
    c,a,b=_candidate(candidate)
    unavailable={'status':'not_analyzed_for_this_candidate','classical_solution_family_containment':None,
                 'conditional_invariance_claim':False,'novel_solution_family_claim':False}
    if c!=0 or any(value!=0 for value in a):
        return unavailable
    if b[0].is_zero is False and all(b[i]==0 for i in (1,2,3)):
        kind='depth_shift';beta=b[0]
    elif b[1].is_zero is False and all(b[i]==0 for i in (0,2,3)):
        kind='longitudinal_velocity_shift';beta=b[1]
    else:
        return unavailable
    # For a depth-shift graph, positivity is local in (t,x) and does not
    # force its intercept H0 positive. A constant-depth family does.
    H0=sp.Symbol('H0',real=True) if kind=='depth_shift' else sp.Symbol('H0',positive=True)
    U0=sp.Symbol('U0',real=True,nonzero=True) if kind=='depth_shift' else sp.Symbol('U0',real=True)
    V0,B0=sp.symbols('V0 B0',real=True)
    Y=sp.Matrix([0,0,1,0,0,0,0])
    if kind=='depth_shift':
        graph=(H0+beta*t-beta*x/U0,U0,V0,B0+beta*x/U0)
        classical=sp.Matrix([1,U0,0,0,0,0,beta])
        guards=('h=H0+beta*t-beta*x/U0>0','U0!=0','g>0','K>0','beta!=0')
        projection_witness=U0
        deduction=(
            'ISC gives h=beta*t+H(x), u=U(x), v=V(x), B=Z(x).',
            'The mass coefficient of t is beta*Uprime; beta!=0 forces Uprime=0.',
            'Mass becomes beta+U0*Hprime=0, so U0 cannot be zero.',
            'Momentum gives Hprime+Zprime=0 and U0*Vprime=0.',
            'Integrating yields the displayed four-constant family; the bed row then vanishes.')
        time_coefficient=beta*sp.diff(sp.Function('U')(x),x)
    else:
        graph=(H0,U0+beta*t,V0,B0-beta*x/g)
        classical=sp.Matrix([0,1,0,0,0,0,-beta/g])
        guards=('H0>0','U0+beta*t!=0 (regular conditional-invariance chart)',
                '(U0+beta*t)^2+V0^2>0','g>0','K>0','beta!=0')
        projection_witness=sp.S.One
        deduction=(
            'ISC gives h=H(x), u=beta*t+U(x), v=V(x), B=Z(x).',
            'The mass coefficient of t is beta*Hprime; beta!=0 forces Hprime=0.',
            'With H0>0, mass forces Uprime=0; the transverse t coefficient forces Vprime=0.',
            'Longitudinal momentum is beta+g*Zprime=0.',
            'Integrating yields the displayed four-constant family; the bed row then vanishes.')
        time_coefficient=beta*sp.diff(sp.Function('H')(x),x)
    canonical,_,_,_=_frame(c,a,b,None)
    combined=sp.Matrix.hstack(canonical[:3,0],canonical[:3,1],classical[:3,0])
    if _clean(combined.det()-projection_witness)!=0 or projection_witness.is_zero is not False:
        raise AssertionError('Distinct-plane projection witness failed')
    candidate_residuals=tuple(_characteristics(canonical[:,j],graph) for j in range(2))
    classical_residuals=tuple(_characteristics(vector,graph) for vector in (Y,classical))
    pde=_pde_on_graph(graph)
    if any(value!=0 for value in pde) or any(value!=0 for row in (*candidate_residuals,*classical_residuals) for value in row):
        raise AssertionError('Constructed family or classical containment failed direct substitution')
    _,_,basis=_source()
    coordinates=tuple(_constant_classical_coordinates(vector,basis) for vector in (Y,classical))
    return {'status':'verified_classical_invariant_solution_family','kind':kind,
            'classical_solution_family_containment':True,'graph':tuple(graph),
            'parameters':(H0,U0,V0,B0),'beta':beta,'guards':guards,
            'fixed_classical_subalgebra':(Y,classical),'constant_classical_coordinates':coordinates,
            'fixed_classical_bracket':_bracket(Y,classical),
            'original_PDE_residuals':pde,'candidate_characteristic_residuals':candidate_residuals,
            'classical_characteristic_residuals':classical_residuals,
            'time_coefficient_in_mass':time_coefficient,'completeness_derivation':deduction,
            'full_local_candidate_solution_family_on_stated_chart':True,
            'combined_projection_rank':3,'combined_projection_rank_witness':projection_witness,
            'distribution_equality_on_these_graphs':False,
            'conditional_invariance_claim':False,'novel_solution_family_claim':False,
            'singular_jet_scope':('The displayed exact family can extend to u=0 when v!=0; this does not repair '
                'failure of the candidate conditional-invariance criterion at other singular first jets.'
                if kind=='longitudinal_velocity_shift' else 'The consistent family forces U0!=0.'),
            'meaning':'Every graph in this local family is invariant under a fixed classical rank-two subalgebra; '
                      'the subalgebra may depend on its fixed profile parameters. Candidate and classical '
                      'rank-two tangent distributions remain different.'}


def classical_distribution_equivalence(candidate,basis_change=None,require_gate=True):
    """Solve constant classical tangency, including invertible variable frames.

    Ambient equivalence means equality on a nonempty open subset of
    (t,x,y,h,u,v,B) with h>0 and u^2+v^2>0. It is not equality after imposing
    a particular solution graph. Unknown coefficient zero strata are retained.
    """
    c,a,b=_candidate(candidate)
    canonical,change,inverse,frame_guards=_frame(c,a,b,basis_change)
    review,solved,basis=_source()
    bad=(*a,*b[:3])
    condition=sp.And(*(sp.Eq(value,0) for value in bad))
    base={'candidate_id':candidate.get('id'),'c':c,'a':a,'b':b,
          'canonical_distribution_frame':canonical,'distribution_frame':canonical*change,
          'frame_change':change,'frame_change_inverse':inverse,
          'frame_change_determinant':_clean(change.det()),
          'frame_change_point_dependent':any(value.has(*COORDINATES) for value in change),
          'frame_chart_guards':frame_guards,'distribution_rank':2,
          'distribution_rank_minor':-sp.S.One,'source_review_gate':review,
          'source_classical_algebra_dimension':len(basis),'source_classical_basis':basis,
          'classical_condition':condition,'ambient_chart':('h>0','u^2+v^2>0','open point-coordinate domain'),
          'conditional_invariance_claim':False,'point_equivalence_groupoid_claim':False,
          'novel_solution_family_claim':False,
          'equivalence_scope':'same distribution in the fixed PDE coordinates; arbitrary invertible point-dependent changes of its frame',
          'unproved_equivalences':('all point equivalences of PDE systems','classification of arbitrary nonclassical distributions')}
    if require_gate and not review['passed']:
        return {**base,'status':'unresolved_classical_algebra_gate','classical_equivalent':None}
    vector=sp.Matrix(solved['coefficients'])
    tau=vector[0]
    identities=(vector[1]-c*tau,*(vector[3+i]-tau*(a[i]*FIELDS[i]+b[i]) for i in range(4)))
    equations=_polynomial_equations(identities)
    matrix,rhs=sp.linear_eq_to_matrix(equations,solved['free_constants'])
    if any(value!=0 for value in rhs):
        raise AssertionError('Classical tangency system must be homogeneous')
    base.update(tangency_identities=identities,tangency_matrix=matrix,
                source_classical_constants=tuple(solved['free_constants']))
    Y=canonical[:,0]
    fixed_Q=sp.Matrix([1,c,0,0,0,0,b[3]])
    if condition not in (sp.S.true,sp.S.false):
        return {**base,'status':'conditional_parameter_stratum' if review['passed'] else 'candidate_algebra_parameter_strata_only','classical_equivalent':None,
                'classical_tangent_space_dimension':None,'evaluated_classical_rank':None,
                'parameter_strata':(
                    {'condition':condition,'status':CLASSICAL if review['passed'] else 'candidate_algebra_rank_two','classical_tangent_space_dimension':2,
                     'classical_tangent_basis':(Y,fixed_Q),'evaluated_classical_rank':2},
                    {'condition':sp.Not(condition),'status':NONCLASSICAL if review['passed'] else 'candidate_algebra_rank_one','classical_tangent_space_dimension':1,
                     'classical_tangent_basis':(Y,),'evaluated_classical_rank':1}),
                'solution_family_containment':solution_family_containment(candidate)}
    equivalent=condition is sp.S.true
    kernel=tuple(matrix.nullspace())
    actual_vectors=tuple((sp.Matrix.hstack(*basis)*coefficients).applyfunc(_clean) for coefficients in kernel)
    dimension=len(kernel)
    rank=sp.Matrix.hstack(*actual_vectors).rank()
    expected_dimension=2 if equivalent else 1
    if dimension!=expected_dimension or rank!=expected_dimension:
        raise AssertionError('Raw constant tangency solve disagrees with the all-parameter theorem')
    residuals=tuple(tuple(_clean(value) for value in matrix*coefficients) for coefficients in kernel)
    if any(value!=0 for row in residuals for value in row):
        raise AssertionError('Constant tangency nullspace failed reconstruction')
    fixed=(Y,fixed_Q) if equivalent else None
    reconstruction=((canonical*change*inverse-sp.Matrix.hstack(*fixed)).applyfunc(_clean)
                    if equivalent else None)
    if equivalent and reconstruction!=sp.zeros(7,2):
        raise AssertionError('Variable-frame classical witness failed')
    status=CLASSICAL if equivalent else NONCLASSICAL
    if not require_gate and not review['passed']:
        status='candidate_algebra_distribution_test_only'
    return {**base,'status':status,'classical_equivalent':equivalent if review['passed'] else None,
            'classical_tangent_space_dimension':dimension,'evaluated_classical_rank':rank,
            'classical_coefficient_nullspace':kernel,'raw_classical_tangent_basis':actual_vectors,
            'classical_tangent_basis':(Y,fixed_Q) if equivalent else (Y,),
            'tangency_kernel_residuals':residuals,'fixed_subalgebra_basis':fixed,
            'fixed_subalgebra_constant_coordinates':tuple(_constant_classical_coordinates(q,basis) for q in fixed) if fixed else None,
            'fixed_subalgebra_bracket':_bracket(*fixed) if fixed else None,
            'frame_to_fixed_classical_basis':inverse if equivalent else None,
            'classical_frame_reconstruction_residual':reconstruction,
            'ambient_obstruction':None if equivalent else 'All fixed classical tangent fields are constant multiples of partial_y; their evaluated rank is only one.',
            'solution_family_containment':solution_family_containment(candidate)}


def special_solution_collapse_control():
    """An inequivalent ambient distribution can coincide on one uniform graph."""
    candidate={'id':'special_solution_control','c':0,'a':(0,1,0,0),'b':(0,0,0,0)}
    result=classical_distribution_equivalence(candidate)
    graph=(2,0,1,0)
    frame=result['canonical_distribution_frame'].subs(dict(zip(FIELDS,graph)),simultaneous=True)
    classical=sp.Matrix.hstack(sp.Matrix([0,0,1,0,0,0,0]),sp.Matrix([1,0,0,0,0,0,0]))
    return {'ambient_result':result,'graph':graph,'original_PDE_residuals':_pde_on_graph(graph),
            'restricted_frame_difference':frame-classical,'speed_squared':1,
            'classical_frame_on_graph':classical,'special_solution_only':True,
            'conditional_invariance_claim':False,
            'meaning':'Coincidence on one codimension-four solution graph does not establish ambient distribution equivalence or the conditional-invariance criterion.'}


def evaluate_frozen_registry(path=None):
    path=Path(path) if path is not None else HERE/'nonclassical_candidates.json'
    raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if digest!=FROZEN_REGISTRY_SHA256:
        raise ValueError('The frozen 64-candidate registry fingerprint changed')
    registry=json.loads(raw)
    if registry['preceding_gate_sha256']!=hashlib.sha256((HERE/'STAGE_2_GATE.json').read_bytes()).hexdigest():
        raise ValueError('The candidate registry is not bound to the current Stage 2 gate')
    if len(registry['candidates'])!=64 or registry['model']!='grass_cubic_f0':
        raise ValueError('Unexpected frozen candidate scope')
    results=tuple(classical_distribution_equivalence(candidate) for candidate in registry['candidates'])
    return {'registry_sha256':digest,'candidate_count':len(results),
            'frozen_candidate_order':tuple(candidate['id'] for candidate in registry['candidates']),
            'status_counts':dict(Counter(result['status'] for result in results)),
            'results':results,'special_solution_collapse_control':special_solution_collapse_control(),
            'scope':'classical distribution equivalence only; independent of conditional-invariance acceptance',
            'conditional_invariance_claim':False,'novel_solution_family_claim':False}


if __name__=='__main__':
    from main import json_ready
    result=evaluate_frozen_registry()
    print(json.dumps(json_ready(result),indent=2))
