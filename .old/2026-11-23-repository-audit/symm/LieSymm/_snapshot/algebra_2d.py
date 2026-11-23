"""Verified 2D line/rank-two representatives, not an optimal-system theorem.

All membership tests use constant coefficients in the solved point algebra.
The differential invariant charts are local. They prove graph-reduction
geometry, not existence of a profile satisfying the reduced PDE.
"""
from functools import lru_cache
from itertools import combinations

import sympy as sp

from models_2d import BRANCHES_2D, t, x, y, h, u, v, B

COORDINATES=(t,x,y,h,u,v,B)


def _clean(value):
    return sp.factor(sp.cancel(sp.sympify(value)))


def bracket(left,right):
    """[left,right] in point coordinates, independently evaluated here."""
    left,right=sp.Matrix(left),sp.Matrix(right)
    return (right.jacobian(COORDINATES)*left-left.jacobian(COORDINATES)*right).applyfunc(_clean)


def _key(basis):
    return tuple(tuple(sp.sympify(e) for e in vector) for vector in basis)


def _affine_coefficients(vector):
    """Formal coefficient extraction; no pointwise numeric rank test."""
    vector=sp.Matrix(vector)
    if vector.shape!=(7,1):
        raise ValueError('Point vectors must have seven components')
    if any(value.has(sp.nan,sp.zoo,sp.oo,-sp.oo) for value in vector):
        raise ValueError('The affine basis requires finite real coefficients')
    derivative=vector.jacobian(COORDINATES)
    if any(entry.has(*COORDINATES) for entry in derivative):
        raise ValueError('The verified adapter requires an affine point basis')
    constant=(vector-derivative*sp.Matrix(COORDINATES)).applyfunc(_clean)
    if any(entry.has(*COORDINATES) for entry in constant):
        raise ValueError('Vector is outside the affine constant span')
    if any(value.is_real is False or value.is_finite is False for value in (*derivative,*constant)):
        raise ValueError('The affine basis requires finite real coefficients')
    # Field rows precede t,x,y rows: a slope dilation has constant h-weight
    # 2, so extracting it never divides by n-1 or n-2.
    return sp.Matrix(list(constant)+[derivative[i,j]
                     for i in (3,4,5,6,0,1,2) for j in range(7)])


@lru_cache(maxsize=128)
def _span_data(basis_key):
    if not basis_key:
        raise ValueError('An empty family has no nonzero constant span')
    matrix=sp.Matrix.hstack(*(_affine_coefficients(q) for q in basis_key))
    rows=matrix.T.rref()[1]
    if len(rows)!=len(basis_key):
        raise ValueError('Basis is dependent in the constant span')
    inverse=matrix[list(rows),:].inv()
    denominators=tuple(sorted({sp.factor(sp.denom(e)) for e in inverse
                                if sp.denom(e).free_symbols},key=str))
    return matrix,rows,inverse,denominators


def constant_coordinates(vector,basis):
    """Unique constant coefficients, or ValueError; functions are rejected."""
    basis_key=_key(basis)
    matrix,rows,inverse,_=_span_data(basis_key)
    target=_affine_coefficients(vector)
    coefficients=(inverse*target[list(rows),:]).applyfunc(_clean)
    if any(_clean(value)!=0 for value in matrix*coefficients-target):
        raise ValueError('Vector is outside the constant span of the supplied basis')
    if any(value.has(*COORDINATES) for value in coefficients):
        raise ValueError('Coordinate functions cannot be constant span coefficients')
    if any(value.is_real is False or value.is_finite is False or value in (sp.nan,sp.zoo)
           for value in coefficients):
        raise ValueError('The point algebra requires finite real constant span coefficients')
    return coefficients


@lru_cache(maxsize=32)
def _structure(basis_key):
    basis=tuple(sp.Matrix(q) for q in basis_key)
    matrices=[sp.zeros(len(basis)) for _ in basis]
    constants={}
    for i,j in combinations(range(len(basis)),2):
        coefficients=constant_coordinates(bracket(basis[i],basis[j]),basis)
        constants[f'{i},{j}']=tuple(coefficients)
        matrices[i][:,j]=coefficients
        matrices[j][:,i]=-coefficients
    return {'status':'verified_bracket_closure','structure_constants':constants,
            'adjoint_matrices':tuple(matrices),
            'convention':'ad_X(Y)=[X,Y]; Ad(exp(epsilon X))=exp(epsilon ad_X)'}


def adjoint_action(report,left,right,epsilon=1):
    """Evaluate a real inner adjoint action using the actual bracket matrix."""
    coefficients=constant_coordinates(left,report['basis'])
    target=constant_coordinates(right,report['basis'])
    epsilon=sp.sympify(epsilon)
    for value in (*coefficients,*target,epsilon):
        if value.has(*COORDINATES) or value.is_real is not True or value.is_finite is not True:
            raise ValueError('A real inner action requires declared finite real constants')
    matrix=sum((c*A for c,A in zip(coefficients,report['structure']['adjoint_matrices'])),
               sp.zeros(len(coefficients)))
    transformed=sp.exp(epsilon*matrix)*target
    return (sp.Matrix.hstack(*report['basis'])*transformed).applyfunc(sp.simplify)


def _minor(matrix,rows,columns):
    return _clean(matrix[list(rows),list(columns)].det(method='domain-ge'))


def _record(name,generators,basis,invariants,base_invariants,rank,columns,guards=()):
    generators=tuple(sp.Matrix(q) for q in generators)
    invariants=tuple(map(sp.sympify,invariants))
    coefficients=tuple(constant_coordinates(q,basis) for q in generators)
    matrix=sp.Matrix.hstack(*basis)
    residuals=tuple(tuple(_clean(e) for e in matrix*c-q)
                    for c,q in zip(coefficients,generators))
    closure={f'{i},{j}':tuple(constant_coordinates(bracket(generators[i],generators[j]),generators))
             for i,j in combinations(range(len(generators)),2)}
    invariant_matrix=sp.Matrix(invariants).jacobian(COORDINATES).applyfunc(_clean)
    invariant_residuals=tuple(tuple(_clean(e) for e in invariant_matrix*q) for q in generators)
    if any(e!=0 for row in invariant_residuals for e in row):
        raise AssertionError('Proposed invariant is not annihilated: '+name)
    witnesses=tuple(_minor(invariant_matrix,range(len(invariants)),cols) for cols in columns)
    if not any(e!=0 for e in witnesses):
        raise AssertionError('No independent-invariant chart: '+name)
    projected=sp.Matrix.hstack(*(q[:3,0] for q in generators))
    projection_witnesses=tuple(_minor(projected,rows,cols)
        for rows in combinations(range(3),rank)
        for cols in combinations(range(len(generators)),rank)) if rank else ()
    if rank and not any(e!=0 for e in projection_witnesses):
        raise AssertionError('Projection rank has no witness: '+name)
    if projected.rank()!=rank:
        raise AssertionError('Projection rank is wrong: '+name)
    return {'name':name,'status':'verified_subalgebra','generators':generators,
            'constant_coordinates':coefficients,'span_residuals':residuals,
            'closure_coefficients':closure,'projection_rank':rank,
            'projection_rank_witnesses':projection_witnesses,
            'invariants':invariants,'invariant_residuals':invariant_residuals,
            'invariant_chart':{'verified':True,'base_invariants':tuple(base_invariants),
                'rank':len(invariants),'rank_witnesses':witnesses,
                'guards':tuple(guards),'interpretation':'at least one displayed minor is nonzero on this chart'},
            'graph_admissible':rank==len(generators),'guards':tuple(guards),
            'profile_solution_claim':False}


@lru_cache(maxsize=32)
def _catalogue(basis_key,scale_key):
    basis=tuple(sp.Matrix(q) for q in basis_key)
    T,X,Y,Z=(sp.eye(7)[:,i] for i in (0,1,2,6))
    R=sp.Matrix([0,-y,x,0,-v,u,0])
    c,a,b=sp.symbols('c a b',real=True)
    radius=sp.sqrt(x*x+y*y)
    radial=(x*u+y*v)/radius
    transverse=(x*v-y*u)/radius
    theta=sp.atan(y/x)
    drop=lambda i:tuple(j for j in range(7) if j!=i)
    lines=[]
    for label,q,skip in (('time_translation',T,0),('space_x_translation',X,1),
                         ('space_y_translation',Y,2),('bed_translation',Z,6)):
        inv=tuple(COORDINATES[j] for j in drop(skip))
        base=tuple(q for q in (t,x,y) if q in inv)
        lines.append(_record(label,(q,),basis,inv,base,0 if skip==6 else 1,(drop(skip),)))
    lines[-1]['graph_obstruction']='Q_B=1'
    lines.append(_record('joint_rotation',(R,),basis,(t,radius,h,radial,transverse,B),
                         (t,radius),1,(drop(2),),('x>0 (local polar chart)',)))
    lines.append(_record('traveling_translation',(T+c*X,),basis,(x-c*t,y,h,u,v,B),
                         (x-c*t,y),1,(drop(0),)))
    lines.append(_record('time_bed_drift',(T+b*Z,),basis,(x,y,h,u,v,B-b*t),
                         (x,y),1,(drop(0),)))
    lines.append(_record('space_bed_drift',(X+b*Z,),basis,(t,y,h,u,v,B-b*x),
                         (t,y),1,(drop(1),)))
    lines.append(_record('rotation_time_bed_screw',(R+a*T+b*Z,),basis,
                         (t-a*theta,radius,h,radial,transverse,B-b*theta),
                         (t-a*theta,radius),1,(drop(2),),('x>0 (local polar chart)',)))
    pairs=[
        _record('plane_wave',(T+c*X,Y),basis,(x-c*t,h,u,v,B),(x-c*t,),2,((1,3,4,5,6),)),
        _record('plane_wave_bed_drift',(T+c*X+a*Z,Y),basis,
                (x-c*t,h,u,v,B-a*t),(x-c*t,),2,((1,3,4,5,6),)),
        _record('spatially_homogeneous',(X,Y),basis,(t,h,u,v,B),(t,),2,((0,3,4,5,6),)),
        _record('stationary_radial',(T,R),basis,(radius,h,radial,transverse,B),(radius,),
                2,((1,3,4,5,6),),('x>0 (local polar chart)',)),
    ]
    named={'T':T,'X':X,'Y':Y,'Z':Z,'R':R}
    for label,raw in scale_key:
        scaling=sp.Matrix(raw)
        aa,bb=sp.diff(scaling[0],t),sp.diff(scaling[1],x)
        expected=sp.Matrix([aa*t,bb*x,bb*y,2*(bb-aa)*h,(bb-aa)*u,(bb-aa)*v,2*(bb-aa)*B])
        if any(_clean(e)!=0 for e in scaling-expected) or (aa==0 and bb==0):
            raise ValueError('Unrecognized scaling in solved algebra')
        named[label]=scaling
        # No division by aa, bb, n-1, or n-2. With t>0, r>0,
        # z=t**bb*r**(-aa) has nonzero gradient whenever (aa,bb)!=(0,0).
        z=t**bb*(x*x+y*y)**(-aa/2)
        fields=(h*t*t/(x*x+y*y),t*(x*u+y*v)/(x*x+y*y),
                t*(x*v-y*u)/(x*x+y*y),B*t*t/(x*x+y*y))
        guards=('t>0','x>0 (local polar chart)',f'({aa},{bb}) != (0,0)')
        line=_record(label,(scaling,),basis,(z,theta,*fields),(z,theta),1,
                     (drop(0),drop(1)),guards)
        line['scaling_weights']=(aa,bb)
        lines.append(line)
        pair=_record('rotation_'+label,(scaling,R),basis,(z,*fields),(z,),2,
                     ((0,3,4,5,6),(1,3,4,5,6)),guards)
        pair['scaling_weights']=(aa,bb)
        pairs.append(pair)
    return {'line_representatives':tuple(lines),'rank_two_representatives':tuple(pairs),
            'named_generators':named,'parameters':{'c':c,'a':a,'b':b}}


def representative_subalgebras(name,basis=None):
    """Return verified representatives for one refined 2D model cell.

    A supplied basis can be reordered or mixed by an invertible constant
    matrix, but must span the entire solved algebra. Extra parameter-dependent
    inverse denominators are made explicit as basis guards. Neither the sample
    line families nor the rank-two families claim adjoint-orbit completeness.
    """
    name=name.removeprefix('2d__')
    if name not in BRANCHES_2D:
        raise ValueError('Choose an explicit refined 2D branch, including its Coriolis stratum')
    cell=BRANCHES_2D[name]
    if cell['G']:
        from research_slope_2d import general_solution
    else:
        from research_first_order_2d import general_solution
    solved=general_solution(name,COORDINATES)
    original=tuple(sp.Matrix(q) for q in solved['basis'])
    if basis is None:
        basis=original
    elif isinstance(basis,dict):
        basis=tuple(basis.values())
    else:
        basis=tuple(sp.Matrix(q) for q in basis)
    if len(basis)!=len(original):
        raise ValueError('Supplied basis must have the same constant span as the solved algebra')
    coefficient_guards=[]
    try:
        for vector in original:
            values=constant_coordinates(vector,basis)
            coefficient_guards.extend(sp.Contains(z,sp.S.Reals,evaluate=False) for z in values if z.is_real is None)
            coefficient_guards.extend(sp.Q.finite(z) for z in values if z.is_finite is None)
        for vector in basis:
            values=constant_coordinates(vector,original)
            coefficient_guards.extend(sp.Contains(z,sp.S.Reals,evaluate=False) for z in values if z.is_real is None)
            coefficient_guards.extend(sp.Q.finite(z) for z in values if z.is_finite is None)
    except ValueError as error:
        raise ValueError('Supplied basis must have the same constant span over finite real coefficients as the solved algebra') from error
    scale_key=[]
    for constant,vector in zip(solved['free_constants'],original):
        if all(_clean(value-sp.diff(value,coordinate)*coordinate)==0
               for value,coordinate in zip(vector,COORDINATES)) and any(vector):
            scale_key.append(('scaling_'+str(constant),tuple(vector)))
    basis_key=_key(basis)
    report=dict(_catalogue(basis_key,tuple(scale_key)))
    report.update(status='verified_representatives',branch=name,basis=tuple(sp.Matrix(q) for q in basis),
                  structure=_structure(basis_key),guards=tuple(solved['guards']),
                  basis_denominator_guards=tuple(sp.Ne(e,0,evaluate=False) for e in _span_data(basis_key)[3]),
                  basis_reality_guards=tuple(dict.fromkeys(coefficient_guards)),
                  optimality_status='not_proved',maximal_point_algebra_claim=False,
                  algebra_source_review_status=solved['review_status'],
                  equivalence='connected inner adjoint action only; no parameter or reflection quotient',
                  slope_parameter_note='n=1,2,3,4 retained; no n-dependent denominator in invariant charts')
    return report
