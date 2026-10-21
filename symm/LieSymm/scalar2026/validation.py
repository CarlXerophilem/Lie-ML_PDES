"""Independent original-P differentiation and local reconstruction certificates."""
import sympy as sp
from .catalog import t,s,z,F,p,q,h,J,PHI,alpha,alpha3
from .api import printed_pde


def direct_reduced_residual(result):
    """Differentiate an actual f(coordinate), then restrict to the transversal.

    This does not use the formal-jet total-derivative routine or its expanded
    PDE implementation. Both sides start from the undivided printed PDE.
    """
    f=sp.Function('profile');phi=result['graph'].subs(F,f(result['coordinate']))
    values=result['parameters'];N=values['m'];G=values['g'];K=values['kappa']
    v=sp.diff(phi,t);gradient=sp.diff(phi,s)
    A=gradient*sp.diff(phi,t,2)-G*sp.diff(phi,s,2)/gradient**2
    C=N*K*v**(N-1)*sp.diff(phi,t,s)/gradient
    raw=sp.diff(A,t)-G*sp.diff(C,s)
    sliced=raw.subs(result['section'],simultaneous=True).doit()
    replacements={sp.diff(f(z),z,i):J[i] for i in range(4)}
    return sp.factor(sliced.subs(replacements,simultaneous=True))


def positive_chart_simplify(expr,velocity):
    """Normalize actual real powers using an invertible positive-velocity chart.

    V replaces F, alpha3 or alpha, with Jacobian 1 or -p (p>0).
    No independent power symbols and no force=True power identities are used.
    """
    expr=sp.factor(expr)
    if expr==0:return expr
    V=sp.Symbol('V_positive',positive=True)
    for variable in (F,alpha3,alpha):
        coefficient=sp.diff(velocity,variable)
        if coefficient in (1,-1,p,-p):
            inverse=sp.cancel((V-(velocity-coefficient*variable))/coefficient)
            changed=expr.subs(variable,inverse)
            simplified=sp.simplify(sp.powsimp(sp.factor(changed)))
            return simplified.subs(V,velocity)
    return sp.simplify(expr)


def _algebraic_zero(expr,rho,rho_cube):
    """Exact quotient-ring test; the relation and denominator guards are exposed."""
    numerator=sp.fraction(sp.cancel(expr))[0]
    remainder=sp.rem(numerator,rho**3-rho_cube,rho)
    return sp.factor(remainder)


def _parametric_check(result,direct):
    data=result['parametric']
    if data.get('kind')=='slope':
        r=data['parameter'];Z=data['coordinate_map'];W=data['profile_map']
        dz=sp.diff(Z,r);slope=sp.simplify(sp.diff(W,r)/dz)
        curvature=sp.simplify(sp.diff(slope,r)/dz)
        third=sp.diff(curvature,r)/dz
        residual=sp.factor(direct.subs({z:Z,F:W,p:slope,q:curvature,h:third},simultaneous=True))
        residual=sp.simplify(residual)
        return dict(passed=residual==0 and sp.simplify(slope-r)==0,
                    original_P_residual=residual,slope_identity=sp.simplify(slope-r),
                    guard='nonzero coordinate derivative and the declared positive chart')
    y=data['parameter'];Z,rho=data['auxiliaries'];Zdot,rhodot=data['rates']
    expected=data['profile'].subs({Z:data['coordinate_map'],rho:data['rho_cube']**sp.Rational(1,3)},simultaneous=True)
    map_defect=sp.simplify(data['profile_map']-expected)
    coordinate_defect=sp.simplify(sp.diff(data['coordinate_map'],y)-data['coordinate_map']*Zdot/Z)
    def D(expr):return sp.diff(expr,y)+Zdot*sp.diff(expr,Z)+rhodot*sp.diff(expr,rho)
    slope=sp.factor(D(data['profile'])/Zdot)
    curvature=sp.factor(D(slope)/Zdot);third=sp.factor(D(curvature)/Zdot)
    raw=direct.subs({z:Z,F:data['profile'],p:slope,q:curvature,h:third},simultaneous=True)
    residual=_algebraic_zero(raw,rho,data['rho_cube'])
    constraint_derivative=sp.factor(D(data['algebraic_constraint']))
    slope_check=sp.factor(slope-rho/Z**sp.Rational(2,3))
    return dict(passed=residual==0 and constraint_derivative==0 and slope_check==0 and map_defect==0 and coordinate_defect==0,
                original_P_residual=residual,slope_identity=slope_check,
                profile_map_defect=map_defect,coordinate_map_defect=coordinate_defect,
                constraint_derivative=constraint_derivative,
                algebraic_relation=data['algebraic_constraint'],
                method='direct original P, then exact polynomial remainder modulo the declared positive algebraic branch',
                guard='D>0, y>1, y!=3, Z>0; integration constants respect the same branch')


def bed_reconstruction(expression,parameters,datum=None,initial_bed=None):
    """Printed bed, as an exact local path integral with one additive datum."""
    G,K,N=parameters['g'],parameters['kappa'],parameters['m']
    grad=sp.diff(expression,s);vel=sp.diff(expression,t)
    A=grad*sp.diff(expression,t,2)-G*sp.diff(expression,s,2)/grad**2
    C=N*K*vel**(N-1)*sp.diff(expression,t,s)/grad
    ds=-A/G;dt=-C
    closure=sp.simplify(sp.diff(ds,t)-sp.diff(dt,s))
    t0,s0,b0=sp.symbols('t0 s0 b0',real=True);T,S=sp.symbols('T S',real=True)
    data_residuals={};anchor_values={};anchor_conditions=[]
    if datum is not None:
        if len(datum)!=3:raise ValueError('bed_datum must be (t0,s0,b0)')
        t0,s0,b0=map(sp.sympify,datum)
        if any(v.is_real is False or v.has(sp.nan,sp.zoo,sp.oo,-sp.oo) for v in (t0,s0,b0)):
            raise ValueError('bed datum must be finite real')
        anchor={t:t0,s:s0}
        anchor_values={name:sp.simplify(value.subs(anchor,simultaneous=True)) for name,value in
                       [('phi',expression),('phi_s',grad),('phi_t',vel),('bed_s',ds),('bed_t',dt)]}
        anchor_conditions=[sp.Gt(anchor_values['phi_s'],0),sp.Gt(anchor_values['phi_t'],0)]
        anchor_conditions += [sp.Gt(log.args[0].subs(anchor,simultaneous=True),0) for log in expression.atoms(sp.log)]
        anchor_conditions += [sp.Gt(power.base.subs(anchor,simultaneous=True),0) for power in expression.atoms(sp.Pow)
                              if power.exp.is_integer is False]
    if initial_bed is not None:
        if datum is None:raise ValueError('bed_profile requires bed_datum')
        initial_bed=sp.sympify(initial_bed)
        data_residuals=dict(slope=sp.simplify(sp.diff(initial_bed,s)-ds.subs(t,t0)),
                            datum=sp.simplify(initial_bed.subs(s,s0)-b0))
    primitive=b0+sp.Integral(ds.subs({t:t0,s:S},simultaneous=True),(S,s0,s))+sp.Integral(dt.subs(t,T),(T,t0,t))
    invalid_anchor=(any(v is sp.false for v in anchor_conditions) or
                    any(v.is_real is False or v.has(sp.nan,sp.zoo,sp.oo,-sp.oo) for v in anchor_values.values()))
    data_passed=all(v==0 for v in data_residuals.values()) and all(v is sp.true for v in anchor_conditions) and not invalid_anchor
    data_status=('not_supplied' if datum is None else 'incompatible' if invalid_anchor or any(v.is_zero is False for v in data_residuals.values())
                 else 'compatible' if data_passed else 'conditional')
    return dict(model='P',bed_s=ds,bed_t=dt,closure_residual=closure,
                primitive=primitive,additive_datum=b0,passed=closure==0,
                data_residuals=data_residuals,data_passed=data_passed,data_status=data_status,
                anchor_values=anchor_values,anchor_conditions=anchor_conditions,
                conditions=['simply connected regular local chart or vanishing periods',
                            'one specified b(t0,s0)=b0','supplied bed traces must equal this primitive'],
                physical_E_equivalence=False)


def verify_solution(result):
    """Recompute certificates; never trust a cached pass flag supplied by a caller."""
    if result.get('model')!='P':raise ValueError('This verifier accepts only printed model P')
    # Re-evaluate supplied-data constraints against the actual returned expression.
    from .solving import _apply_data
    result=dict(result)
    if result.get('data'):_apply_data(result,dict(result['data']))
    out=dict(model='P',status=result['status'],exact_passed=False,reduction_passed=False,
             domain_scope='conditional on explicitly recorded local guards')
    if result['status'] in ('no_invariant_graph','undefined_pde','outside_positive_chart'):
        out['typed_outcome']=result['status'];return out
    direct=direct_reduced_residual(result)
    f=sp.Function('profile');phi=result['graph'].subs(F,f(result['coordinate']))
    tau,xi,eta=result['generator']
    recomputed_Q=sp.simplify(eta.subs(PHI,phi)-tau*sp.diff(phi,t)-xi*sp.diff(phi,s))
    difference=positive_chart_simplify(direct-result['residual'],result['velocity'])
    out.update(direct_residual=direct,reduction_difference=difference,Q=recomputed_Q,
               reduction_passed=difference==0 and recomputed_Q==0)
    if 'first_integral' in result:
        from .solving import profile_derivative
        defect=positive_chart_simplify(direct-result['first_integral_multiplier']*profile_derivative(result['first_integral']),result['velocity'])
        out['first_integral_defect']=defect
        out['reduction_passed']=out['reduction_passed'] and defect==0
    if result.get('expression') is not None:
        phi=result['expression'];values=result['parameters']
        tau,xi,eta=result['generator']
        Q=sp.simplify(eta.subs(PHI,phi)-tau*sp.diff(phi,t)-xi*sp.diff(phi,s))
        # Power simplification is only used inside the explicitly positive s,t chart.
        residue=printed_pde(phi,t,s,values['m'],values['g'],values['kappa'])
        residue=sp.simplify(residue)
        out.update(original_P_residual=residue,exact_Q=Q,
                   exact_passed=residue==0 and Q==0)
        out['bed']=bed_reconstruction(phi,values,result.get('data',{}).get('bed_datum'),result.get('data',{}).get('bed_profile'))
        out['exact_passed']=out['exact_passed'] and out['bed']['data_passed']
    elif 'parametric' in result:
        out['parametric']=_parametric_check(result,direct)
        out['exact_passed']=out['parametric']['passed']
        if any(key in result.get('data',{}) for key in ('bed_datum','bed_profile')):
            out['bed']=dict(model='P',data_status='unsupported',data_passed=False,
                            reason='bed data on parametric graphs require a separately verified local inverse chart')
            out['exact_passed']=False
    if result.get('data_status') in ('incompatible','singular_implicit'):
        out['exact_passed']=False
        out['data_rejection']=result.get('data_reason')
    if 'jet' in result.get('data',{}) and result.get('data_status')!='compatible':
        out['exact_passed']=False
    out['data_status']=result.get('data_status','not_supplied')
    out['initial_representation_residuals']=result.get('initial_representation_residuals',{})
    out['exact_passed']=bool(out['exact_passed'] and out['reduction_passed'])
    return out


def material_audit():
    """Replay E->material calculus without importing any build-directory code."""
    phi=sp.Function('phi')(t,s);bed=sp.Function('b')(t,s)
    G,K,N=sp.symbols('g kappa m',positive=True)
    Q=sp.diff(phi,s);v=sp.diff(phi,t);depth=1/Q
    Dx=lambda expr:sp.diff(expr,s)/Q
    Dt=lambda expr:sp.diff(expr,t)-v*sp.diff(expr,s)/Q
    mass=sp.simplify(Dt(depth)+Dx(depth*v))
    momentum=Dt(v)+v*Dx(v)+G*Dx(depth+bed)
    A=Q*sp.diff(phi,t,2)-G*sp.diff(phi,s,2)/Q**2
    C=N*K*v**(N-1)*sp.diff(phi,t,s)/Q
    momentum_defect=sp.simplify(Q*momentum-A-G*sp.diff(bed,s))
    exner=Dt(bed)+N*K*v**(N-1)*Dx(v)
    exner_defect=sp.simplify(exner-(sp.diff(bed,t)-v*sp.diff(bed,s)/Q+C))
    P=sp.diff(A,t)-G*sp.diff(C,s);M=P-sp.diff(v*A/Q,s)
    speed=sp.Symbol('c',positive=True);witness=s**2/2+speed*t
    WP=printed_pde(witness,t,s,3,G,K)
    WQ=sp.diff(witness,s);WA=WQ*sp.diff(witness,t,2)-G*sp.diff(witness,s,2)/WQ**2
    WM=sp.simplify(WP-sp.diff(sp.diff(witness,t)*WA/WQ,s))
    return dict(model='separate E/P/M audit',mass=mass,momentum=momentum_defect,exner=exner_defect,
                P=P,M=M,witness=witness,witness_P=WP,witness_M=WM,
                passed=mass==0 and momentum_defect==0 and exner_defect==0 and WP==0 and sp.simplify(WM+3*G*speed/s**4)==0,
                interpretation='solution-dependent reciprocal transformation, not an ordinary Eulerian point transformation')
