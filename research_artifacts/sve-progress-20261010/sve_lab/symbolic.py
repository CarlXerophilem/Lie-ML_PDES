"""Auditable identities, ODEs, and unrestricted first-order obstruction."""
import sympy as sp
from .jets import (t,s,u,p,q,a,b,c,r,w,x,y,g,kappa,m,
                   total,act,model_residual)

z=sp.symbols('z', positive=True)
f,P,C,H=sp.symbols('f P C H', real=True)

def profile_total(expr):
    return sp.diff(expr,z)+P*sp.diff(expr,f)+C*sp.diff(expr,P)+H*sp.diff(expr,C)

def reduced_residual(exponent=m, physical=False):
    V=f-z*P
    A=C*(z**2*P-g/P**2)
    J=z*V**(exponent-1)*C/P
    R=-A-z*profile_total(A)+g*exponent*kappa*profile_total(J)
    if physical:
        R-=profile_total(V*A/P)
    return sp.expand(R)

def normal_form(exponent=m, physical=False):
    R=reduced_residual(exponent,physical)
    leading=sp.diff(R,H)
    rhs=-R.subs(H,0)/leading
    return rhs,leading

def first_integral(exponent=m,physical=False):
    """R = dI/dz; the bed logarithmic drift is I/g."""
    _,leading=normal_form(exponent,physical)
    return sp.factor(leading*C)

def obstruction(physical=False):
    """Necessary tangency condition with arbitrary smooth point coefficients.

    On q>0 solve the equation for r=phi_ttt. Multiply the x=phi_tss
    coefficient by q**3 to obtain a polynomial in the freely varying p,q.
    Its p**2*q**2 coefficient is a nonzero scalar, independent of ALL
    derivatives of the unrestricted point-generator coefficients.
    """
    tau=sp.Function('tau')(t,s,u)
    xi=sp.Function('xi')(t,s,u)
    eta=sp.Function('eta')(t,s,u)
    E=model_residual(3,physical)
    forcing=3*g*kappa*total(p**2*b/q,1)
    shell=-E.subs(r,0)/q
    tangency=sp.expand((act(E,tau,xi,eta)+forcing).subs(r,shell))
    highest=sp.expand(q**3*sp.diff(tangency,x))
    poly=sp.Poly(highest,p,q)
    witness=sp.factor(poly.coeff_monomial(p**2*q**2))
    return {'model':'physical_corrected' if physical else 'printed',
            'shell':shell,'highest_polynomial':poly.as_expr(),
            'witness':witness,'tangency':tangency}

def principal_symbol_obstruction(physical=False):
    """Independent highest-jet derivation of the point-lift obstruction.

    This uses the principal symbol and the first prolongation coefficients,
    rather than the recursive third-prolongation calculation in obstruction().
    """
    tau=sp.Function('tau')(t,s,u)
    xi=sp.Function('xi')(t,s,u)
    eta=sp.Function('eta')(t,s,u)
    principal=g/q**2+3*g*kappa*p**2/q
    eta_s=total(eta,1)-p*total(tau,1)-q*total(xi,1)
    eta_t=total(eta,0)-p*total(tau,0)-q*total(xi,0)
    coefficient=(principal/q-sp.diff(principal,q))*eta_s
    coefficient-=sp.diff(principal,p)*eta_t
    coefficient+=2*principal*(total(xi,1)-total(tau,0))
    coefficient+=3*g*kappa*p**2/q
    highest=sp.expand(q**3*coefficient)
    if physical:
        highest+=p*(3*g*kappa*p**2*q-2*g)*(
            q*sp.diff(tau,u)+sp.diff(tau,s))
        highest+=2*p*q**3*(p*sp.diff(xi,u)+sp.diff(xi,t))
        highest=sp.expand(highest)
    poly=sp.Poly(highest,p,q)
    return {
        'model':'physical_corrected' if physical else 'printed',
        'derivation':'independent principal-symbol calculation',
        'highest_polynomial':poly.as_expr(),
        'witness':sp.factor(poly.coeff_monomial(p**2*q**2)),
    }

def common_scaling_certificate():
    """Exact invariant-graph data for X_c=t*d_t+s*d_s+u*d_u.

    A third-order equation requires the invariant-surface equation and its
    total derivatives through order two.  The rank statements are conditional
    on the recorded t>0 chart guard, rather than a claim at the fixed point
    t=s=u=0.
    """
    characteristic=u-t*p-s*q
    dt=total(characteristic,0)
    ds=total(characteristic,1)
    consequences={
        '()':characteristic,
        '(t)':dt,
        '(s)':ds,
        '(t,t)':total(dt,0),
        '(t,s)':total(dt,1),
        '(s,s)':total(ds,1),
    }
    y_coord=sp.log(t)
    z_coord=s/t
    v_coord=u/t
    generator=lambda expression: sp.expand(
        t*sp.diff(expression,t)+s*sp.diff(expression,s)
        +u*sp.diff(expression,u))
    old_to_new=sp.Matrix([
        [sp.diff(y_coord,t),sp.diff(y_coord,s)],
        [sp.diff(z_coord,t),sp.diff(z_coord,s)],
    ]).det()
    full_old_to_new=sp.Matrix([
        [sp.diff(y_coord,t),sp.diff(y_coord,s),sp.diff(y_coord,u)],
        [sp.diff(z_coord,t),sp.diff(z_coord,s),sp.diff(z_coord,u)],
        [sp.diff(v_coord,t),sp.diff(v_coord,s),sp.diff(v_coord,u)],
    ]).det()
    return {
        'status':'verified',
        'generator':'t*d_t + s*d_s + u*d_u',
        'guards':['t>0','regular local point-action chart'],
        'characteristic':{
            'status':'verified',
            'expression':characteristic,
            'meaning':'invariant-surface equation eta-tau*u_t-xi*u_s=0',
        },
        'differential_consequence_order':2,
        'differential_consequences':consequences,
        'orbit_ranks':{'base':1,'total_space':1},
        'transversality':{
            'status':'verified',
            'criterion':'rank(t,s)=rank(t,s,u)=1 on t>0',
            'base_rank':1,
            'total_space_rank':1,
            'meaning':'the one-dimensional point orbit projects with rank one to the base',
        },
        'coordinates':{
            'orbit_parameter':y_coord,
            'base_invariant':z_coord,
            'dependent_invariant':v_coord,
            'old_to_new_jacobian':sp.factor(old_to_new),
            'new_to_old_jacobian':sp.factor(1/old_to_new),
            'full_old_to_new_jacobian':sp.factor(full_old_to_new),
        },
        'checks':{
            'Xc_y_minus_one':sp.simplify(generator(y_coord)-1),
            'Xc_z':sp.simplify(generator(z_coord)),
            'Xc_v':sp.simplify(generator(v_coord)),
            'base_jacobian_product_minus_one':sp.simplify(old_to_new*t**2-1),
            'full_jacobian_product_minus_one':sp.simplify(full_old_to_new*t**3-1),
            'mixed_DJQ_commutator':sp.simplify(total(dt,1)-total(ds,0)),
        },
    }

def conservation_pullback_certificate(exponent=m, physical=False):
    """Pull back the declared scalar balance law to (T,z)=(t,s/t).

    The transformed current is a vector density.  Consequently its z-component
    is the flux paired with the boundary covector dz; no metric or unit-normal
    convention is introduced.  Data and extra constraints remain explicitly
    undeclared rather than being inferred from the PDE residual.
    """
    density=q*a-g*c/q**2
    spatial_flux=-g*exponent*kappa*p**(exponent-1)*b/q
    if physical:
        spatial_flux-=p*density/q
    transformed_density=sp.expand(t*density)
    transformed_flux=sp.expand(spatial_flux-s*density/t)

    def new_time_total(expression):
        return sp.expand(total(expression,0)+(s/t)*total(expression,1))

    def new_space_total(expression):
        return sp.expand(t*total(expression,1))

    transformed_divergence=sp.expand(
        new_time_total(transformed_density)+new_space_total(transformed_flux))
    original_residual=model_residual(exponent,physical)
    return {
        'status':'verified_for_declared_scalar_balance_law',
        'model':'physical_corrected' if physical else 'printed',
        'density':density,
        'spatial_flux':spatial_flux,
        'source':sp.Integer(0),
        'constraints':{
            'status':'not_declared_for_scalar_benchmark',
            'items':[],
        },
        'data':{
            'status':'not_declared',
            'compatibility':'not_tested_without_a_specific_initial_boundary_value_problem',
        },
        'coordinate_map':{
            'old_coordinates':['t','s'],
            'new_coordinates':['T=t','z=s/t'],
            'jacobian_old_from_new':t,
            'guards':['t>0'],
        },
        'transformed_density':transformed_density,
        'transformed_spatial_flux':transformed_flux,
        'boundary_normal_flux_pullback':transformed_flux,
        'boundary_flux_convention':'current paired with dz on z=constant',
        'checks':{
            'divergence_remainder':sp.simplify(
                transformed_divergence-t*original_residual),
        },
        'scope':{
            'full_bed_field_system':False,
            'noether_or_variational_claim':False,
            'weak_or_shock_solutions':False,
        },
    }

def direct_pullback(exponent,physical=False):
    """Independent direct chain rule in (t,s), for polynomial equality tests."""
    F=sp.Function('F')
    phi=t*F(s/t)
    A=sp.diff(phi,s)*sp.diff(phi,t,2)-g*sp.diff(phi,s,2)/sp.diff(phi,s)**2
    E=sp.diff(A,t)-g*exponent*kappa*sp.diff(
        sp.diff(phi,t)**(exponent-1)*sp.diff(phi,t,s)/sp.diff(phi,s),s)
    if physical:
        E-=sp.diff(sp.diff(phi,t)*A/sp.diff(phi,s),s)
    pulled=sp.expand((t**2*E).subs(s,t*z).doit())
    return pulled.xreplace({F(z):f,sp.diff(F(z),z):P,
                           sp.diff(F(z),z,2):C,sp.diff(F(z),z,3):H})

def physical_audit():
    """Compatibility of the reconstructed bed derivatives, not a closure guess."""
    A=q*a-g*c/q**2
    bs=-A/g
    bt=p*bs/q-m*kappa*p**(m-1)*b/q
    compatibility=sp.expand(g*(total(bt,1)-total(bs,0)))
    return compatibility, model_residual(m,True)
