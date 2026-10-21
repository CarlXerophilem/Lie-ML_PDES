"""Specified 2D flow/data controls and explicit field/parameter point maps.

This module does not classify symmetries, infer evolution from an initial
profile, or claim a complete point-equivalence groupoid. It reads the solved
2D coefficient families and checks their tangency to explicitly fixed data.
All stage-1 modules remain read-only.
"""
from __future__ import annotations

import json
import time

import sympy as sp

from main import JetSpace,graph_check,json_ready
from models_2d import BRANCHES_2D,branch_model_2d,t,x,y,h,u,v,B,g,K,G,m,n,f
from data_experiments import _guarded_homogeneous_solve

COORDINATES=(t,x,y,h,u,v,B)


def _fixed(value,label):
    value=sp.sympify(value)
    if value.free_symbols.intersection(COORDINATES) or value.atoms(sp.Function):
        raise ValueError(label+' must be independent of point coordinates')
    if value.is_real is False or value.is_finite is False or value in (sp.nan,sp.zoo):
        raise ValueError(label+' must be a finite real constant')
    return value


def _real_finite_guards(values,label):
    """Keep the real smooth-data domain explicit, including symbolic profiles."""
    guards=[]
    for value in map(sp.sympify,values):
        if value.is_real is False or value.is_finite is False or value.has(sp.nan,sp.zoo):
            raise ValueError(label+' must be finite real values on the declared data domain')
        if value.is_real is None:
            guards.append(sp.Contains(value,sp.S.Reals,evaluate=False))
        if value.is_finite is None:
            guards.append(sp.Q.finite(value))
    return tuple(dict.fromkeys(guards))


def _context(name,substitutions=None):
    name=name.removeprefix('2d__')
    model=branch_model_2d(name)
    cell=BRANCHES_2D[name]
    substitutions={sp.sympify(k):_fixed(value,'physical parameter')
                   for k,value in (substitutions or {}).items()}
    if not set(substitutions).issubset(model['parameters']):
        raise ValueError('Specialize only active parameters of this branch')
    conditions=[sp.Gt(g,0,evaluate=False)]
    if cell['K']:
        mm=sp.sympify(cell['m'])
        conditions += [sp.Gt(K,0,evaluate=False),sp.Ge(mm,1,evaluate=False),sp.Le(mm,4,evaluate=False)]
        if 'generic' in cell['base_cell']:
            conditions.append(sp.Ne(mm,3,evaluate=False))
    if cell['G']:
        conditions.append(sp.Gt(G,0,evaluate=False))
    if not cell['K'] and cell['G']:
        nn=sp.sympify(cell['n'])
        conditions += [sp.Ge(nn,0,evaluate=False),sp.Le(nn,4,evaluate=False)]
        if name=='slope_only_generic_f_nonzero':
            conditions.append(sp.Ne(nn,2,evaluate=False))
    if cell['coriolis']=='f_nonzero':
        conditions.append(sp.Ne(f,0,evaluate=False))
    specialized=[condition.subs(substitutions,simultaneous=True) for condition in conditions]
    if any(value is sp.S.false for value in specialized):
        raise ValueError('Parameter specialization contradicts the registered 2D branch')
    guards=[str(value) for value in specialized if value is not sp.S.true]
    for value in substitutions.values():
        if value.is_real is None:
            guards.append(str(sp.Contains(value,sp.S.Reals,evaluate=False)))
        if value.is_finite is None:
            guards.append(str(sp.Q.finite(value)))
    model['branch_conditions']['guards']=['h>0','u^2+v^2>0']+guards
    model['branch_conditions']['substitutions']=substitutions
    equations=tuple(eq.subs(substitutions,simultaneous=True) for eq in model['equations'])
    space=JetSpace(model['independent_variables'],model['dependent_fields'])
    return name,cell,model,space,equations,substitutions


def _flow_result(name,graph,substitutions=None,extra_guards=()):
    name,_,model,space,equations,substitutions=_context(name,substitutions)
    graph=tuple(sp.sympify(value).subs(substitutions,simultaneous=True) for value in graph)
    data_domain_guards=_real_finite_guards(graph,'Flow profiles')
    checked=graph_check(space,equations,graph)
    speed_squared=sp.expand(graph[1]**2+graph[2]**2)
    outside=graph[0].is_nonpositive is True or speed_squared.is_nonpositive is True
    return {'branch':name,'graph':graph,'equation_residuals':checked['equation_residuals'],
            'status':'outside_declared_chart' if outside else
                     'verified_constructed_solution' if checked['is_solution'] else 'negative_pde_control',
            'chart_guards':(sp.Gt(graph[0],0,evaluate=False),sp.Gt(speed_squared,0,evaluate=False)),
            'extra_data_guards':extra_guards,'data_domain_guards':data_domain_guards,
            'parameter_guards':model['branch_conditions']['guards'],
            'parameter_substitutions':substitutions,
            'scope':'constructed smooth flow on the recorded positive-depth/nonzero-speed chart',
            'arbitrary_data_claim':False}


def uniform_rotating_flow(name,*,depth=2,velocity=(3,4),datum=1,time0=0,substitutions=None):
    """Spatially uniform inertia rotation: W_t=-f R W, h and B constant."""
    depth,datum,time0=(_fixed(value,'flow datum') for value in (depth,datum,time0))
    U,V=(_fixed(value,'initial velocity') for value in velocity)
    ff=sp.S.Zero if name.endswith('_f0') else f
    angle=ff*(t-time0)
    graph=(depth,U*sp.cos(angle)+V*sp.sin(angle),V*sp.cos(angle)-U*sp.sin(angle),datum)
    return _flow_result(name,graph,substitutions,
                        (sp.Gt(U*U+V*V,0,evaluate=False),))


def constant_slope_flow(name,*,depth=2,velocity=(3,4),slope=(sp.Rational(1,5),sp.Rational(-1,7)),
                        datum=1,time0=0,substitutions=None):
    """Exact uniform-velocity acceleration/rotation above a fixed planar bed.

    At f!=0 the geostrophic center is (-g*l/f,g*k/f), and the displacement
    from that center rotates at angular speed -f. Flux is spatially constant.
    """
    depth,datum,time0=(_fixed(value,'flow datum') for value in (depth,datum,time0))
    U,V=(_fixed(value,'initial velocity') for value in velocity)
    k,ell=(_fixed(value,'bed slope') for value in slope)
    elapsed=t-time0
    if name.endswith('_f0'):
        flow_u,flow_v=U-g*k*elapsed,V-g*ell*elapsed
    else:
        center_u,center_v=-g*ell/f,g*k/f
        angle=f*elapsed
        flow_u=center_u+(U-center_u)*sp.cos(angle)+(V-center_v)*sp.sin(angle)
        flow_v=center_v+(V-center_v)*sp.cos(angle)-(U-center_u)*sp.sin(angle)
    return _flow_result(name,(depth,flow_u,flow_v,k*x+ell*y+datum),substitutions,
                        (sp.Gt(U*U+V*V,0,evaluate=False),))


def _solved_coefficients(name,cell,substitutions):
    if cell['G']:
        from research_slope_2d import general_solution
        exponent=sp.sympify(cell['m'] if cell['K'] else cell['n']).subs(substitutions)
        solved=general_solution(name,coordinates=COORDINATES,exponent=exponent)
    else:
        from research_first_order_2d import general_solution
        exponent=sp.sympify(cell['m']).subs(substitutions) if cell['K'] else None
        ff=0 if cell['coriolis']=='f0' else f.subs(substitutions)
        solved=general_solution(name,coordinates=COORDINATES,exponent=exponent,f_value=ff)
    old=tuple(solved['free_constants'])
    constants=tuple(sp.Dummy('data_'+str(c),real=True) for c in old)
    rename=dict(zip(old,constants))
    coefficients=tuple(sp.sympify(z).xreplace(rename).subs(substitutions,simultaneous=True)
                       for z in solved['coefficients'])
    return coefficients,constants,tuple(map(str,old))


def initial_data_stabilizer(name,profiles,*,time0=0,substitutions=None):
    """Stabilize a specified fixed-time initial graph, without evolving it."""
    name,cell,model,space,equations,substitutions=_context(name,substitutions)
    if len(profiles)!=4:
        raise ValueError('Provide initial profiles (h,u,v,B)')
    profiles=tuple(sp.sympify(z).subs(substitutions,simultaneous=True) for z in profiles)
    if any(z.has(t,h,u,v,B) for z in profiles):
        raise ValueError('Initial profiles may depend only on x,y and fixed data parameters')
    data_domain_guards=_real_finite_guards(profiles,'Initial profiles')
    time0=_fixed(time0,'initial time')
    coefficients,constants,source_names=_solved_coefficients(name,cell,substitutions)
    tau,xi,chi,*eta=coefficients
    substitution={t:time0,**dict(zip((h,u,v,B),profiles))}
    identities=[tau.subs(substitution,simultaneous=True)]
    identities += [(vertical-xi*sp.diff(profile,x)-chi*sp.diff(profile,y)).subs(substitution,simultaneous=True)
                   for vertical,profile in zip(eta,profiles)]
    identities=tuple(sp.simplify(z) for z in identities)
    equations_linear=[];denominator_guards=[]
    speed_squared=sp.expand(profiles[1]**2+profiles[2]**2)
    base={'branch':name,'profiles':profiles,'fixed_time':time0,
          'general_coefficients':coefficients,'source_constant_names':source_names,
          'tangency_identities':identities,
          'chart_guards':(sp.Gt(profiles[0],0,evaluate=False),sp.Gt(speed_squared,0,evaluate=False)),
          'data_domain_guards':data_domain_guards,
          'parameter_guards':model['branch_conditions']['guards'],'parameter_substitutions':substitutions,
          'frozen_profile_diagnostic':graph_check(space,equations,profiles),
          'pde_solution_claim':False,'scope':'specified fixed-time initial graph only; no future boundary or existence theorem'}
    for identity in identities:
        numerator,denominator=sp.fraction(sp.cancel(identity))
        if denominator!=1:
            denominator_guards.append(sp.Ne(denominator,0,evaluate=False))
        try:
            equations_linear.extend(sp.Poly(numerator,x,y).coeffs())
        except sp.PolynomialError:
            return {**base,'status':'unresolved_functional_splitting',
                    'denominator_guards':tuple(denominator_guards)}
    equations_linear=tuple(dict.fromkeys(sp.simplify(z) for z in equations_linear if z!=0))
    solution,rank_guards,zero_branches,free=_guarded_homogeneous_solve(
        equations_linear,constants,cell['base_cell'],substitutions)
    replacement=dict(zip(constants,solution))
    residuals=tuple(sp.simplify(z.subs(replacement,simultaneous=True)) for z in identities)
    stabilized=tuple(sp.simplify(z.subs(replacement,simultaneous=True)) for z in coefficients)
    outside=profiles[0].is_nonpositive is True or speed_squared.is_nonpositive is True
    status=('outside_declared_chart' if outside else 'unresolved_tangency_verification' if any(z!=0 for z in residuals)
            else 'conditional_initial_data_stabilizer' if rank_guards else 'verified_initial_data_stabilizer')
    return {**base,'status':status,'dimension':len(free),'free_constants':free,
            'constant_constraints':equations_linear,'coefficient_solution':solution,
            'stabilized_coefficients':stabilized,'verification_residuals':residuals,
            'rank_guards':rank_guards,'unresolved_zero_pivot_branches':zero_branches,
            'denominator_guards':tuple(denominator_guards)}


def conservative_point_map(name,substitutions=None):
    """Explicit invertible field map (h,u,v,B) -> (h,hu,hv,B), h>0."""
    name,cell,model,old,equations,substitutions=_context(name,substitutions)
    momentum_x,momentum_y=sp.symbols('momentum_x momentum_y',real=True)
    new=JetSpace((t,x,y),(h,momentum_x,momentum_y,B))
    inverse=(h,momentum_x/h,momentum_y/h,B)
    used=set().union(*(e.free_symbols for e in equations))
    mapping={symbol:new.D_multi(inverse[a],index)
             for symbol,(a,index) in old.reverse.items() if symbol in used}
    pulled=tuple(sp.expand(e.xreplace(mapping)) for e in equations)
    ff=sp.S.Zero if cell['coriolis']=='f0' else f
    mass=new.D(h,0)+new.D(momentum_x,1)+new.D(momentum_y,2)
    mx=(new.D(momentum_x,0)+new.D(momentum_x**2/h+g*h*h/2,1)
        +new.D(momentum_x*momentum_y/h,2)+g*h*new.D(B,1)-ff*momentum_y)
    my=(new.D(momentum_y,0)+new.D(momentum_x*momentum_y/h,1)
        +new.D(momentum_y**2/h+g*h*h/2,2)+g*h*new.D(B,2)+ff*momentum_x)
    speed_squared=inverse[1]**2+inverse[2]**2
    flux=[]
    for axis,velocity in enumerate(inverse[1:3],1):
        value=K*speed_squared**((sp.sympify(cell['m'])-1)/2)*velocity if cell['K'] else sp.S.Zero
        if cell['G']:
            value-=G*speed_squared**(sp.sympify(cell['n'])/2)*new.D(B,axis)
        flux.append(value)
    bed=new.D(B,0)+new.D(flux[0],1)+new.D(flux[1],2)
    conservative=tuple(sp.expand(z.subs(substitutions,simultaneous=True)) for z in (mass,mx,my,bed))
    multiplier=sp.Matrix([[1,0,0,0],[inverse[1],h,0,0],[inverse[2],0,h,0],[0,0,0,1]])
    residuals=tuple(sp.simplify(z) for z in sp.Matrix(conservative)-multiplier*sp.Matrix(pulled))
    forward=sp.Matrix([h,h*u,h*v,B])
    jacobian=sp.factor(forward.jacobian((h,u,v,B)).det())
    return {'branch':name,'status':'verified_field_point_equivalence' if all(z==0 for z in residuals)
            and jacobian==h*h else 'unresolved_field_map_verification',
            'forward':tuple(forward),'inverse':inverse,'jacobian':jacobian,
            'row_multiplier':multiplier,'equivalence_residuals':residuals,
            'conservative_fields':new.u,'conservative_equations':conservative,
            'sediment_flux_in_conservative_fields':tuple(value.subs(substitutions,simultaneous=True) for value in flux),
            'guards':('h>0','momentum_x^2+momentum_y^2>0'),
            'parameter_guards':model['branch_conditions']['guards'],'parameter_substitutions':substitutions,
            'scope':'explicit field point equivalence; no material-coordinate or scalar-model equivalence'}


def pushforward_generator(coefficients):
    """Push a point generator through the field map, without reclassifying it."""
    if len(coefficients)!=7:
        raise ValueError('Expected (tau,xi,chi,H,U,V,Z)')
    tau,xi,chi,H,U,V,Z=map(sp.sympify,coefficients)
    momentum_x,momentum_y=sp.symbols('momentum_x momentum_y',real=True)
    image=sp.Matrix([tau,xi,chi,H,u*H+h*U,v*H+h*V,Z])
    return image.subs({u:momentum_x/h,v:momentum_y/h},simultaneous=True).applyfunc(sp.simplify)


def signed_coriolis_reflection(name):
    """Verify y -> -y, v -> -v, f -> -f, with all other parameters fixed."""
    name,_,model,space,equations,_=_context(name)
    used=set().union(*(e.free_symbols for e in equations))
    mapping={symbol:(-1)**(index[2]+int(a==2))*symbol
             for symbol,(a,index) in space.reverse.items() if symbol in used}
    mapping[f]=-f
    reflected=tuple(sp.expand(e.xreplace(mapping)) for e in equations)
    parity=(1,1,-1,1)
    residuals=tuple(sp.simplify(new-sign*old) for new,sign,old in zip(reflected,parity,equations))
    return {'branch':name,'status':'verified_parameter_reflection' if all(z==0 for z in residuals)
            else 'unresolved_parameter_reflection','equivalence_residuals':residuals,
            'map':{'t':'t','x':'x','y':'-y','h':'h','u':'u','v':'-v','B':'B','f':'-f'},
            'guards':model['branch_conditions']['guards'],
            'fixed_parameter_symmetry':name.endswith('_f0'),
            'scope':'one verified discrete equivalence between signed f parameters; not the full equivalence groupoid'}


def run_data_controls(name):
    """Per-branch entry point for the stage-2 wrapper, with bounded claims."""
    started=time.perf_counter()
    name=name.removeprefix('2d__')
    flows={'uniform_inertia_rotation':uniform_rotating_flow(name),
           'planar_bed_acceleration_rotation':constant_slope_flow(name)}
    initial={label:initial_data_stabilizer(name,(2,3,4,bed),time0=1)
             for label,bed in (('flat',sp.S.One),('linear',1+x-2*y),('quadratic',1+x*x+y*y))}
    conservative=conservative_point_map(name)
    reflection=signed_coriolis_reflection(name)
    passed=(all(result['status']=='verified_constructed_solution' for result in flows.values())
            and all(result['status']=='verified_initial_data_stabilizer' for result in initial.values())
            and conservative['status']=='verified_field_point_equivalence'
            and reflection['status']=='verified_parameter_reflection')
    return {'branch':name,'status':'verified_specified_data_controls' if passed else 'unresolved_specified_data_controls',
            'all_declared_checks_passed':passed,'flows':flows,'initial_data':initial,
            'primitive_conservative_map':conservative,'signed_coriolis_reflection':reflection,
            'elapsed_seconds':time.perf_counter()-started,
            'scope':'two constructed flows, three specified initial graphs, one field point map, and one parameter reflection',
            'not_claimed':['arbitrary data compatibility','global solutions','future boundary preservation',
                           'zero-speed classification','full equivalence groupoid']}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--branch',required=True,choices=tuple(BRANCHES_2D))
    args=parser.parse_args()
    result=run_data_controls(args.branch)
    print(json.dumps(json_ready(result),indent=2))
    raise SystemExit(0 if result['all_declared_checks_passed'] else 1)
