"""Exact 2D rank-one PDE and rank-two ODE/DAE graph reductions.

These are independently verified reductions of specified generators. They do
not supply necessity or maximality of the 2D point algebra. The common parent
handles the point prolongation; every reduced equation is pulled back here.
"""
import sympy as sp
from main import JetSpace, characteristic, lie_bracket, verify_generator
from models_2d import branch_model_2d, BRANCHES_2D, g, K, G, m, n, f


def _context(name):
    model=branch_model_2d(name)
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    return model,J


def _jet_mapping(J,equations,graph,operators):
    needed=set().union(*(e.free_symbols for e in equations)) & J.reverse.keys()
    needed.update(J.u)
    needed.update(J.jet(a,J.unit(i)) for a in range(len(J.u)) for i in range(len(J.x)))
    mapping={}
    for symbol in sorted(needed,key=str):
        a,index=J.reverse[symbol]
        value=sp.sympify(graph[a])
        for axis,count in enumerate(index):
            for _ in range(count):
                value=operators[axis](value)
        mapping[symbol]=value
    return mapping


def _invariants_on_graph(J,generators,mapping,base_map,simplify=sp.simplify):
    return tuple(tuple(simplify(value.xreplace(mapping).subs(base_map,simultaneous=True))
                       for value in characteristic(J,vector[:3],vector[3:])) for vector in generators)


def plane_wave(name,speed=None):
    """Two commuting translations give z=x-c*t, with all four field profiles.

    This permits transverse velocity; setting it to zero is generally
    incompatible with nonzero f. The reduced leading system is kept implicit.
    """
    model,J=_context(name)
    t,x,y=J.x;h,u,v,B=J.u
    c=sp.Symbol('c',real=True) if speed is None else sp.sympify(speed)
    if c.has(*(J.x+J.u)):
        raise ValueError('Plane-wave speed is a constant')
    if c.is_real is False or c.is_finite is False or c in (sp.nan,sp.zoo):
        raise ValueError('Plane-wave speed must be finite and real')
    speed_guards=[]
    if c.is_real is None:
        speed_guards.append(sp.Contains(c,sp.S.Reals,evaluate=False))
    if c.is_finite is None:
        speed_guards.append(sp.Q.finite(c))
    z=sp.Symbol('z',real=True)
    profiles=tuple(sp.Function(name)(z) for name in ('H','U','V','Z'))
    operators=(lambda e:-c*sp.diff(e,z),lambda e:sp.diff(e,z),lambda e:sp.S.Zero)
    mapping=_jet_mapping(J,model['equations'],profiles,operators)
    reduced=tuple(sp.simplify(e.xreplace(mapping)) for e in model['equations'])
    generators=((1,c,0,0,0,0,0),(0,0,1,0,0,0,0))
    verification=[verify_generator(J,model['equations'],q[:3],q[3:]) for q in generators]
    Q=_invariants_on_graph(J,generators,mapping,{x:z+c*t})
    # Rebuild Cartesian derivatives directly, without the reduced operators.
    graph=tuple(value.subs(z,x-c*t) for value in profiles)
    direct=_jet_mapping(J,model['equations'],graph,tuple(lambda e,k=k:sp.diff(e,k) for k in J.x))
    remainder=tuple(sp.simplify(e.xreplace(direct)-r.subs(z,x-c*t))
                    for e,r in zip(model['equations'],reduced))
    return {'status':'verified_ode_reduction' if all(v['verified'] for v in verification)
            and all(e==0 for row in Q for e in row) and all(e==0 for e in remainder) else 'unresolved',
            'generators':generators,'projection_rank':2,'reduced_independent_variables':(z,),
            'invariant':x-c*t,'profiles':profiles,'graph':graph,'reduced_equations':reduced,
            'characteristic_residuals':Q,'reconstruction_residuals':remainder,
            'generator_checks':verification,'chart_jacobian':sp.S.One,
            'guards':('H(z)>0','U(z)**2+V(z)**2>0',*speed_guards),
            'leading_system':'implicit ODE/DAE; no division by wave characteristic speeds',
            'order_reduction_claim':False,'maximality_claim':False}


def rotating_radial(name):
    """The joint rotation has projection rank one and leaves a (t,r) PDE."""
    model,J=_context(name)
    t,x,y=J.x;h,u,v,B=J.u
    r=sp.Symbol('r',positive=True)
    theta=sp.Symbol('theta',real=True)
    H,U,V,Z=(sp.Function(q)(t,r) for q in ('H','U','V','Z'))
    co,si=sp.cos(theta),sp.sin(theta)
    graph=(H,co*U-si*V,si*U+co*V,Z)
    operators=(lambda e:sp.diff(e,t),
               lambda e:co*sp.diff(e,r)-si/r*sp.diff(e,theta),
               lambda e:si*sp.diff(e,r)+co/r*sp.diff(e,theta))
    mapping=_jet_mapping(J,model['equations'],graph,operators)
    speed=U*U+V*V
    norm_check=sp.trigsimp(graph[1]**2+graph[2]**2-speed)
    # Replace the exact squared-norm identity before expanding real powers.
    raw=tuple(sp.trigsimp(e.subs(u*u+v*v,speed).xreplace(mapping)) for e in model['equations'])
    polar=(raw[0],sp.trigsimp(co*raw[1]+si*raw[2]),sp.trigsimp(-si*raw[1]+co*raw[2]),raw[3])
    cell=BRANCHES_2D[name]
    fv=0 if cell['coriolis']=='f0' else f
    flux=K*speed**((sp.sympify(cell['m'])-1)/2)*U if cell['K'] else sp.S.Zero
    if cell['G']:
        flux-=G*speed**(sp.sympify(cell['n'])/2)*sp.diff(Z,r)
    expected=(sp.diff(H,t)+sp.diff(r*H*U,r)/r,
              sp.diff(U,t)+U*sp.diff(U,r)-V*V/r+g*sp.diff(H+Z,r)-fv*V,
              sp.diff(V,t)+U*sp.diff(V,r)+U*V/r+fv*U,
              sp.diff(Z,t)+sp.diff(r*flux,r)/r)
    remainder=tuple(sp.simplify(sp.trigsimp(value-target)) for value,target in zip(polar,expected))
    rotation=(0,-y,x,0,-v,u,0)
    Q=_invariants_on_graph(J,(rotation,),mapping,{x:r*co,y:r*si},sp.trigsimp)
    verification=verify_generator(J,model['equations'],rotation[:3],rotation[3:])
    return {'status':'verified_pde_reduction' if norm_check==0 and all(e==0 for e in remainder)
            and all(e==0 for row in Q for e in row) and verification['verified'] else 'unresolved',
            'generator':rotation,'projection_rank':1,'reduced_independent_variables':(t,r),
            'profiles':(H,U,V,Z),'reduced_equations':expected,'graph_in_polar_coordinates':graph,
            'base_map':(t,r*co,r*si),'base_jacobian':r,'velocity_rotation_determinant':1,
            'guards':('r>0','H(t,r)>0','U(t,r)**2+V(t,r)**2>0','local angle chart'),
            'norm_residual':norm_check,'characteristic_residuals':Q,
            'reconstruction_residuals':remainder,'generator_check':verification,
            'inverse_row_map':'E_x=cos(theta)*E_radial-sin(theta)*E_azimuthal; E_y=sin(theta)*E_radial+cos(theta)*E_azimuthal',
            'ode_claim':False,'maximality_claim':False}


def rotation_scaling_time_ode(name,diffusion_exponent=None):
    """Commuting spatial scaling and joint rotation leave only time.

    The actual PDE decides whether the scaling is admitted. This rejects,
    for example, active source-slope m=n=3, rather than suppressing its r term.
    """
    model,J=_context(name)
    specialization={}
    if diffusion_exponent is not None:
        value=sp.sympify(diffusion_exponent)
        if name!='slope_only_f0' or not value.is_number or value.is_real is not True or not 0<=value<=4:
            raise ValueError('This specialization is a real exponent in [0,4] inside slope_only_f0')
        specialization={n:value}
        model['equations']=tuple(e.subs(specialization) for e in model['equations'])
    t,x,y=J.x;h,u,v,B=J.u
    rotation=(0,-y,x,0,-v,u,0)
    scaling=(0,x,y,2*h,u,v,2*B)
    checks=[verify_generator(J,model['equations'],q[:3],q[3:]) for q in (rotation,scaling)]
    if not all(value['verified'] for value in checks):
        return {'status':'generator_not_admitted','generator_checks':checks,
                'parameter_specialization':specialization,
                'scope':'not admitted uniformly on the supplied symbolic cell; residuals retain exceptional parameter slices',
                'available_specialization':'slope_only_f0 permits diffusion_exponent=2'}
    H,A,W,Z=(sp.Function(q)(t) for q in ('H','A','W','Z'))
    r2=x*x+y*y
    graph=(r2*H,A*x-W*y,W*x+A*y,r2*Z)
    mapping=_jet_mapping(J,model['equations'],graph,tuple(lambda e,k=k:sp.diff(e,k) for k in J.x))
    raw=tuple(sp.expand(e.xreplace(mapping)) for e in model['equations'])
    reduced=(sp.cancel(raw[0]/r2),sp.cancel((x*raw[1]+y*raw[2])/r2),
             sp.cancel((-y*raw[1]+x*raw[2])/r2),sp.cancel(raw[3]/r2))
    if any(value.has(x,y) for value in reduced):
        return {'status':'unresolved_orbit_dependence','pulled_equations':raw,'reduced_attempt':reduced}
    reconstruction=(sp.simplify(raw[0]-r2*reduced[0]),
                    sp.simplify(raw[1]-x*reduced[1]+y*reduced[2]),
                    sp.simplify(raw[2]-y*reduced[1]-x*reduced[2]),
                    sp.simplify(raw[3]-r2*reduced[3]))
    Q=_invariants_on_graph(J,(rotation,scaling),mapping,{})
    bracket=lie_bracket(J.x+J.u,rotation,scaling)
    return {'status':'verified_ode_reduction' if all(e==0 for e in reconstruction+bracket)
            and all(e==0 for row in Q for e in row) else 'unresolved',
            'generators':(rotation,scaling),'generator_checks':checks,'bracket':bracket,
            'projection_rank':2,'projection_minor':-r2,'reduced_independent_variables':(t,),
            'profiles':(H,A,W,Z),'graph':graph,'reduced_equations':reduced,
            'parameter_specialization':specialization,
            'characteristic_residuals':Q,'reconstruction_residuals':reconstruction,
            'guards':('x**2+y**2>0','H(t)>0','A(t)**2+W(t)**2>0'),
            'divisors':(r2,),'maximality_claim':False,'order_reduction_claim':False}
