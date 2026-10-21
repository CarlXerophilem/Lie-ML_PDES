"""Exact-first solvers and explicit unresolved branches for printed scalar P."""
from __future__ import annotations
import sympy as sp
from .catalog import (t,s,z,F,p,q,h,J,derive_entry,parameter_values)


def profile_derivative(expr):
    return sp.diff(expr,z)+p*sp.diff(expr,F)+q*sp.diff(expr,p)+h*sp.diff(expr,q)


def cubic_autonomous(g=1,kappa=sp.Rational(1,30)):
    """3.5 in log(z): turning of Sigma is permitted; Delta=0 is not divided."""
    G,K=map(sp.sympify,(g,kappa));S,M=sp.symbols('Sigma M', real=True)
    row=derive_entry('paper-3.5',dict(g=G,kappa=K,m=sp.Integer(3)))
    residue=row['residual'].subs({z:1,p:S,q:M},simultaneous=True)
    leading=sp.diff(residue,h);constant=residue.subs(h,0)
    H=sp.factor(-constant/leading)
    delta=4*S**3*(3*G*K-1)+G
    return dict(variables=(S,M),rhs=(2*S/3+M,sp.factor(5*M/3+H)),
                delta=delta,implicit_equation=residue,leading=leading,
                singular_compatibility=constant,coordinate='r=log(z), z>0',
                reconstruction="z=exp(r); dF/dr=Sigma*exp(r/3)",
                guards=['Sigma>0','z>0','Delta!=0 for the explicit vector field'],
                turning_condition=2*S/3+M,
                parameter_strata=['3*g*kappa<1/4','3*g*kappa=1/4','1/4<3*g*kappa<1',
                                  '3*g*kappa=1','3*g*kappa>1'],
                singular_status='Delta=0 requires implicit compatibility and differentiated constraints; continuation unresolved')


def singular_cubic(g,kappa):
    """Cubic L=0 solved by a rational parameter integral; equilibrium retained.

    y=w/rho, D=1-g*beta*(y-1)^2, rho^3=g/D. This is the positive
    branch of w=rho+sqrt((rho^3-g)/(g*beta*rho)), expressed without radicals
    in the differential constraints used by the independent verifier.
    """
    G,K=map(sp.sympify,(g,kappa));gamma=3*G*K
    y=sp.Symbol('y',positive=True);Z,Rho=sp.symbols('Z rho',positive=True)
    y0=sp.Symbol('y0',positive=True);z0=sp.Symbol('z0',positive=True);v=sp.Dummy('v',positive=True)
    D=1-gamma*(y-1)**2
    ell=2*gamma*(y-1)/(3*D)
    rate=sp.factor((1+y*ell)/(1-y/3))
    integral=sp.Integral(rate.subs(y,v),(v,y0,y))
    Zmap=z0*sp.exp(integral);rhomap=(G/D)**sp.Rational(1,3)
    return dict(parameter=y,auxiliaries=(Z,Rho),rates=(Z*rate,Rho*ell),
                coordinate=Z,profile=y*Rho*Z**sp.Rational(1,3),
                coordinate_map=Zmap,profile_map=y*rhomap*Zmap**sp.Rational(1,3),
                algebraic_constraint=Rho**3*D-G,rho_cube=G/D,
                logarithmic_rate=rate,denominator=D,
                rho_form='w=rho+sqrt((rho^3-g)/(g*beta*rho)); f_prime*rho_r=rho-f/3',
                guards=['y>1','D=1-g*beta*(y-1)^2>0','z0>0','y!=3',
                        'path from y0 to y stays in one connected regular interval'],
                equilibrium='y=3 is separate: A^3=27*g/(1-4*g*beta), requiring g*beta<1/4',
                constants=(z0,y0),constant_count=1,
                constant_note='y0 is a reference point; changing it rescales z0, not a second independent constant')


def _quadrature(B, numerator, *, kind, F0=None,p0=None,z0=None):
    r=next(v for v in B.free_symbols if v.name=='r')
    p0=sp.sympify(p0) if p0 is not None else sp.Symbol('p0',positive=True)
    z0=sp.sympify(z0) if z0 is not None else sp.Symbol('z0',real=True)
    F0=sp.sympify(F0) if F0 is not None else sp.Symbol('F0',real=True)
    v=sp.Dummy('v',positive=True);speed=sp.cancel(B/numerator)
    Z=z0+sp.Integral(speed.subs(r,v),(v,p0,r))
    W=F0+sp.Integral((r*speed).subs(r,v),(v,p0,r))
    return dict(kind=kind,parameter=r,coordinate_map=Z,profile_map=W,
                coordinate_rate=speed,profile_rate=r*speed,B=B,numerator=numerator,
                constants=(z0,F0,p0),guards=['B(r)!=0','numerator(r)!=0','r>0',
                'positive original velocity','the integration path stays inside this chart'])


def _exact(result, expression, status, constants=(), guards=()):
    result.update(status=status,expression=expression,free_constants=constants,
                  remaining_equation=None)
    result['guards']+=list(guards)
    if any(sp.diff(expression,x).is_nonpositive is True for x in (s,t)):
        result['status']='outside_positive_chart'
    return result


def _profile_of_expression(result):
    """Recover the exact profile on the registered transversal, before testing data."""
    graph=result['graph'];weight=sp.diff(graph,F)
    profile=(result['expression']-graph.subs(F,0))/weight
    return sp.simplify(profile.subs(result['section'],simultaneous=True))


def _initial_representation_constraints(result,jet,z0):
    """Constraints for the selected exact representation, independent of the ODE."""
    if result.get('expression') is not None:
        profile=_profile_of_expression(result)
        return {f'profile_derivative_{i}':sp.simplify(sp.diff(profile,z,i).subs(z,z0)-value)
                for i,value in enumerate(jet)}
    param=result.get('parametric',{})
    if param.get('kind')=='slope':
        r=param['parameter'];p0=jet[1]
        speed=param['coordinate_rate']
        values=[param['profile_map'],r,1/speed]
        return {f'profile_derivative_{i}':sp.simplify(values[i].subs(r,p0)-value)
                for i,value in enumerate(jet)}
    if param:
        y=param['parameter'];Z,rho=param['auxiliaries']
        rate=param['rates'][0]/Z;ell=param['rates'][1]/rho
        y0=sp.simplify(jet[0]/(z0*jet[1]));rho0=jet[1]*z0**sp.Rational(2,3)
        at={y:y0,Z:z0,rho:rho0}
        checks={'singular_algebraic_relation':sp.simplify(param['algebraic_constraint'].subs(at)),
                'profile_derivative_2':sp.simplify((rho/Z**sp.Rational(5,3)*(ell/rate-sp.Rational(2,3))).subs(at)-jet[2])}
        result['initial_parameter']=y0
        result['initial_parameter_conditions']=[z0>0,y0>1,sp.Ne(y0,3),param['denominator'].subs(y,y0)>0]
        if any(v is sp.false for v in result['initial_parameter_conditions']):
            checks['singular_parameter_chart']=sp.Integer(1)
        return checks
    return {}


def _apply_data(result,data):
    """Initial-jet compatibility precedes division or numerical integration."""
    result['data']=data;result['data_status']='not_supplied' if not data else 'conditional'
    if 'I0' in data and 'required_I0' in result:
        defect=sp.simplify(sp.sympify(data['I0'])-result['required_I0'])
        if defect.is_zero is False:
            result['data_status']='incompatible';result['data_reason']='I0 contradicts the selected exact branch'
            return result
    if 'jet' not in data:return result
    jet=tuple(map(sp.sympify,data['jet']))
    order=result.get('ode_order',3)
    expected=order if order else 3
    if len(jet) not in (expected,3):raise ValueError(f'jet must contain {expected} initial derivatives for this ODE')
    if any(v.is_real is False or v.has(sp.nan,sp.zoo,sp.oo,-sp.oo) for v in jet):raise ValueError('initial data must be finite real')
    z0=sp.sympify(data.get('z0',1))
    if z0.is_real is False or z0.has(sp.nan,sp.zoo,sp.oo,-sp.oo):raise ValueError('z0 must be finite real')
    at={z:z0,**dict(zip(J,jet))}
    if order==2 and len(jet)==2:
        at[q]=sp.cancel(-result['residual'].subs(q,0)/result['leading']).subs(at)
    result['resolved_initial_jet']=tuple(at[j] for j in (F,p,q))
    trace={key:sp.simplify(result[key].subs(at)) for key in ('velocity','gradient') if key in result}
    result['initial_trace']=trace
    if any(v.is_positive is False for v in trace.values()):
        result['data_status']='incompatible';result['data_reason']='initial velocity or gradient is not positive'
        return result
    if 'first_integral' in result:
        initial_I=sp.simplify(result['first_integral'].subs(at))
        result['initial_integral']=initial_I
        if 'I0' in data and sp.simplify(initial_I-sp.sympify(data['I0']))!=0:
            result['data_status']='incompatible';result['data_reason']='I0 contradicts the initial jet'
            return result
        if 'required_I0' in result and sp.simplify(initial_I-result['required_I0'])!=0:
            result['data_status']='incompatible';result['data_reason']='initial jet contradicts the selected branch integral'
            return result
    constraints=_initial_representation_constraints(result,tuple(at[j] for j in (F,p,q)),z0)
    result['initial_representation_residuals']=constraints
    if any(v.is_zero is False or v.has(sp.nan,sp.zoo,sp.oo,-sp.oo) for v in constraints.values()):
        result['data_status']='incompatible';result['data_reason']='initial jet does not belong to the selected exact representation'
        return result
    if result.get('expression') is not None or 'parametric' in result:
        result['data_status']='compatible' if (all(v==0 for v in constraints.values()) and
            all(v.is_positive is True for v in trace.values())) else 'conditional'
        return result
    if result.get('leading') is not None:
        leading=sp.simplify(result['leading'].subs(at))
        result['initial_leading']=leading
        if leading==0:
            result['data_status']='singular_implicit';result['data_reason']='highest coefficient vanishes; no regular Taylor or numerical solve'
            result['initial_implicit_constraint']=sp.simplify(result['residual'].subs(at).subs(h,0))
            return result
    if order==2 and len(jet)==3 and sp.simplify(result['residual'].subs(at))!=0:
        result['data_status']='incompatible';result['data_reason']='supplied second derivative contradicts the second-order ODE'
        return result
    result['data_status']='compatible' if all(v.is_positive is True for v in trace.values()) else 'conditional'
    return result


def solve_reduction(reduction_id, *, parameters, data=None):
    """Solve a known reduction, retaining exact, conditional and unresolved states."""
    name,values=parameter_values(reduction_id,parameters)
    data=dict(data or {})
    allowed={'branch','I0','F0','p0','z0','jet','order','bed_datum','bed_profile'}
    if set(data)-allowed:raise ValueError('Unknown data keys: '+str(sorted(set(data)-allowed)))
    result=derive_entry(name,values)
    branch=data.get('branch','regular')
    branches={'regular'}
    if name in ('paper-3.6','paper-3.9','m1-boost-travel'):branches.add('affine')
    if name in ('paper-3.4','m1-scale-boost'):branches.update(('affine','singular','power'))
    if branch not in branches:raise ValueError('Unsupported branch for '+name+': '+str(branch))
    if 'jet' in data:
        jet=tuple(map(sp.sympify,data['jet']))
        if len(jet)<2:raise ValueError('initial jet must contain at least F and F_prime')
        for key,value in (('F0',jet[0]),('p0',jet[1])):
            if key in data and sp.simplify(sp.sympify(data[key])-value)!=0:
                raise ValueError(key+' contradicts initial jet')
            data[key]=value
        data.setdefault('z0',1)
    result.update(expression=None,free_constants=(),arbitrary_functions=(),
                  remaining_equation=result['residual'],unresolved=[],solution_scope='local on declared chart',
                  method_attempts=['reuse classified generator','derive graph and undivided pullback'])
    if result['status']!='reduction':return _apply_data(result,data)
    G,K,N=values['g'],values['kappa'],values['m'];beta=N*K
    A=values.get('alpha',1);U=values.get('alpha3',1)
    av=values.get('a',-1);sig=values.get('sigma',1)
    f=sp.Function('f');c0,c1,c2=sp.symbols('c0 c1 c2',real=True)
    p0=sp.sympify(data.get('p0',sp.Symbol('p0',positive=True)))
    F0=sp.sympify(data.get('F0',sp.Symbol('F0',real=True)))
    z0=sp.sympify(data.get('z0',sp.Symbol('z0',real=True)))
    I0=sp.sympify(data.get('I0',sp.Symbol('I0',real=True)))
    if name=='paper-3.7' or (name in ('paper-3.6','paper-3.9') and A==0):
        v=A if name=='paper-3.7' else (0 if name=='paper-3.6' else U)
        _exact(result,v*t+f(s),'exact_arbitrary_function',guards=['f_prime(s)>0',f'{v}>0'])
        result['arbitrary_functions']=(f(s),)
        if sp.sympify(v).is_positive is False:result['status']='outside_positive_chart'
    elif name=='paper-3.8':
        expr=A*s+c0+c1*t+c2*t**2/2
        if 'jet' in data:
            f0,v0,a0=map(sp.sympify,data['jet']);base=sp.sympify(data.get('z0',1))
            expr=A*s+f0+v0*(t-base)+a0*(t-base)**2/2
        _exact(result,expr,'exact_quadratic',(c0,c1,c2),[f'{A}>0','c1+c2*t>0'])
    elif name=='m1-boost-space':
        _exact(result,t*s/sig+c2*(t*sp.log(sig*t)-t)+c1*t+c0,
               'exact_logarithmic',(c0,c1,c2),['sigma*t>0','s/sigma+c2*log(sigma*t)+c1>0'])
        if 'jet' in data:
            profile=_profile_of_expression(result);base=sp.sympify(data['z0'])
            equations=[sp.diff(profile,z,i).subs(z,base)-value for i,value in enumerate(data['jet'])]
            constants=sp.solve(equations,(c0,c1,c2),dict=True)
            if constants:
                result['expression']=sp.simplify(result['expression'].subs(constants[0]))
                result['free_constants']=()
    elif name=='m1-boost-travel' and av==0:
        _exact(result,t**2/(2*sig)+f(s),'exact_arbitrary_function',guards=['t/sigma>0','f_prime(s)>0'])
        result['arbitrary_functions']=(f(s),)
    elif name in ('paper-3.6','paper-3.9','m1-boost-travel'):
        r=sp.Symbol('r',positive=True)
        if name=='m1-boost-travel':
            B=av**2*r/sig**2-G/r**2-G*K/r;numerator=I0-r/sig
            result['first_integral']=p/sig+B.subs(r,p)*q
            result['first_integral_multiplier']=-av/sig
        else:
            velocity=(0 if name=='paper-3.6' else U)-A*r
            B=A**2*r-G/r**2-G*beta*velocity**(N-1)/r;numerator=I0
            result['first_integral']=B.subs(r,p)*q
            result['first_integral_multiplier']=-A
        if 'jet' in data and 'I0' not in data:
            I0=sp.simplify(result['first_integral'].subs({z:sp.sympify(data['z0']),**dict(zip(J,map(sp.sympify,data['jet'])))},simultaneous=True))
            data['I0']=I0
            numerator=I0-r/sig if name=='m1-boost-travel' else I0
        if (I0==0 and name!='m1-boost-travel') or branch=='affine':
            profile=F0+p0*(result['coordinate']-z0)
            _exact(result,result['graph'].subs(F,profile),'exact_affine',(F0,p0,z0))
            result['required_I0']=p0/sig if name=='m1-boost-travel' else sp.Integer(0)
            if name=='m1-boost-travel':result['constant_branch_constraint']=sp.Eq(I0,p0/sig)
        else:
            result.update(status='exact_parametric_quadrature',parametric=_quadrature(B,numerator,kind='slope',
                          F0=data.get('F0'),p0=data.get('p0'),z0=data.get('z0')),
                          remaining_equation=sp.Eq(result['first_integral'],I0),free_constants=(I0,F0,p0,z0))
            result['unresolved']+=['B=0 and numerator=0: use the implicit equation; crossing is not asserted'] if name=='m1-boost-travel' else []
        result['exceptional_branches']=['zero translation speed: arbitrary-profile identity',
            'constant slope is checked directly, including roots of B',
            'B=0 with nonzero numerator cannot be crossed by a finite-curvature classical profile']
        result['independent_constant_count']=3 if result['status']=='exact_parametric_quadrature' else 2
        result['reference_constant_note']='p0 is the reference slope; shifting it can be absorbed into z0,F0'
        result['method_attempts']+=['exact first integral','autonomous slope equation','exact parametric quadrature']
    elif name in ('paper-3.4','m1-scale-boost'):
        boost=A if name=='m1-scale-boost' else sp.Integer(0)
        L=-z**3*p+G*z/p**2+G*beta*z*(F-z*p)**(N-1)/p
        I=sp.factor(L*q-boost*z*p)
        result.update(first_integral=I,first_integral_multiplier=sp.Integer(1),
                      status='first_integral_reduced',remaining_equation=sp.Eq(I,I0),
                      reduced_order=1 if N==1 else 2,
                      exceptional_branches=['I0=0: product branches must be kept','L=0: implicit singular branch',
                                            'z=0 is outside the logarithmic parameter chart'])
        if branch=='affine':
            base=sp.sympify(data.get('z0',0))
            _exact(result,result['graph'].subs(F,F0+p0*(result['coordinate']-base)),'exact_affine',(F0,p0))
            result['required_I0']=sp.Integer(0)
            # A nonzero boost is not generally affine-profile invariant P.
            if boost!=0:raise ValueError('Affine profile is not a solution for nonzero scale boost')
        elif branch=='singular':
            if N!=3 or boost!=0:raise ValueError('Implemented singular parameter quadrature requires m=3 and zero boost')
            result.update(status='exact_parametric_quadrature',parametric=singular_cubic(G,K),
                          remaining_equation=None,required_I0=sp.Integer(0))
            if 'jet' in data:
                par=result['parametric'];Z0,Y0=par['constants']
                initial_y=sp.simplify(data['F0']/(data['z0']*data['p0']))
                for key in ('coordinate_map','profile_map'):
                    par[key]=par[key].subs({Z0:sp.sympify(data['z0']),Y0:initial_y},simultaneous=True)
        elif branch=='power':
            if N!=3:raise ValueError('This power family requires m=3')
            amp_cube=27*G/(1-4*G*beta)
            if amp_cube.is_positive is False or amp_cube.has(sp.zoo):
                raise ValueError('No finite positive amplitude at g*beta>=1/4')
            amp=amp_cube**sp.Rational(1,3)
            _exact(result,amp*s**sp.Rational(1,3)*t**sp.Rational(2,3),'exact_power',
                   guards=['s>0','t>0','g*beta<1/4'])
            result['required_I0']=sp.Integer(0)
        else:result['unresolved']+=['General explicit solution of the remaining first-integral equation is unresolved']
        result['method_attempts']+=['exact first integral','zero-integral product split','cubic singular parameter chart']
    elif name=='paper-3.5':
        result.update(status='autonomous_order_reduction',autonomous=cubic_autonomous(G,K),reduced_order=1)
        result['unresolved']+=['General phase-curve quadrature and Delta=0 continuation unresolved']
        result['method_attempts']+=['mu=F_prime','inherited scaling invariants','log-coordinate autonomous system']
    else:
        result['status']='unresolved_ode'
        result['unresolved']+=['No additional exact first integral certified; regular local series and numerical continuation available',
                               'Zero-leading-coefficient continuation unresolved']
        result['method_attempts']+=['inherited scaling is already used in the graph',
                                   'no autonomous or absent-profile-variable shortcut certified for this representative']
    _apply_data(result,data)
    if 'jet' in data and result['data_status']=='compatible' and result['expression'] is None:
        result['series']=local_series(result,order=int(data.get('order',6)))
    return result


def local_series(result,order=6):
    """Exact implicit recurrence, retaining the original undivided equation."""
    if result['data_status']!='compatible':return dict(status='data_not_regular')
    differential_order=result['ode_order']
    if not result['leading']:return dict(status='not_regular_ode')
    if order<differential_order:raise ValueError('series order is below the differential order')
    data=result['data'];z0=sp.sympify(data.get('z0',1));jet=list(map(sp.sympify,data['jet']))
    x=sp.Symbol('x',real=True);coeff=[jet[i]/sp.factorial(i) for i in range(differential_order)]
    residual=result['residual'];equations=[]
    for n in range(differential_order,order+1):
        u=sp.Symbol('u');poly=sum(v*x**i for i,v in enumerate(coeff))+u*x**n
        pull=residual.subs({z:z0+x,F:poly,p:sp.diff(poly,x),q:sp.diff(poly,x,2),h:sp.diff(poly,x,3)},simultaneous=True)
        eq=sp.simplify(sp.diff(pull,x,n-differential_order).subs(x,0)/sp.factorial(n-differential_order))
        lead=sp.diff(eq,u)
        if lead==0:return dict(status='singular_recurrence',equation=eq,coefficients=coeff)
        value=sp.cancel(-eq.subs(u,0)/lead);coeff.append(value);equations.append(sp.simplify(eq.subs(u,value)))
    poly=sum(v*x**i for i,v in enumerate(coeff))
    return dict(status='exact_local_series',order=order,z0=z0,coefficients=coeff,
                polynomial=poly.subs(x,z-z0),residual_coefficients=equations,
                passed=all(v==0 for v in equations),scope=f'truncated series; residual vanishes through degree {order-differential_order}')
