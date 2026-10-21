"""Exact input/reconstruction certificates for the frozen affine graph search.

The graph calculation is deliberately independent of the conditional-invariance
solver.  A correct graph pullback does not admit a failed conditional candidate.
No network, optimizer, learned weight, or training loop is involved.
"""
from functools import lru_cache
import math

import sympy as sp


FIELDS = ('h', 'u', 'v', 'B')
T, RHO, Z = sp.symbols('T rho z', real=True)
F = sp.symbols('H U V Zb', real=True)
P = sp.symbols('H_z U_z V_z Zb_z', real=True)
g, K = sp.symbols('g K', positive=True)


# 1. An affine flow is invertible at every finite real time.
def validate_candidate(candidate):
    a, b = tuple(candidate['a']), tuple(candidate['b'])
    c = candidate['c']
    if len(a) != 4 or len(b) != 4:
        raise ValueError('Exactly four fields are required')
    if any(isinstance(v, bool) or not isinstance(v, int) for v in (*a, *b, c)):
        raise ValueError('This frozen export uses exact integer coefficients')
    return a, b, c


def _dz(expression):
    return sp.expand(sum(sp.diff(expression, f)*p for f, p in zip(F, P)))


def _dt(expression):
    # rho=exp(T), so rho and T are not independent under differentiation.
    return sp.expand(sp.diff(expression, T)+RHO*sp.diff(expression, RHO))


def _time_coefficients(expression):
    """Split real analytic exp-polynomials; preserve all Laurent relations.

    Integral a_i give finite sums T^k exp(j*T).  Distinct (j,k) are linearly
    independent on every time interval.  We never treat exp(T)^2 and exp(2T)
    as unrelated variables. No profile or characteristic factor is divided out.
    """
    groups = {}
    for term in sp.Add.make_args(sp.expand(expression)):
        powers = term.as_powers_dict()
        j, k = powers.get(RHO, sp.S.Zero), powers.get(T, sp.S.Zero)
        if j.is_Integer is not True or k.is_Integer is not True or k < 0:
            raise ValueError('Outside the frozen exponential-polynomial class')
        coefficient = sp.cancel(term/(RHO**j*T**k))
        if coefficient.has(RHO, T):
            raise ValueError('Unsplit time dependence')
        key = (int(j), int(k))
        groups[key] = groups.get(key, 0)+coefficient
    return tuple((j, k, sp.factor(value)) for (j, k), value in sorted(groups.items())
                 if sp.expand(value) != 0)


# 2. Pull the original conservation/momentum equations back to the graph.
@lru_cache(maxsize=64)
def _graph_certificate(a, b, c):
    graph = tuple(RHO**ai*fi + (sp.Rational(bi, ai)*(RHO**ai-1) if ai else bi*T)
                  for ai, bi, fi in zip(a, b, F))
    q = tuple(sp.expand(ai*ui+bi-_dt(ui)) for ai, bi, ui in zip(a, b, graph))
    inverse = tuple(sp.cancel((ui-(sp.Rational(bi, ai)*(RHO**ai-1) if ai else bi*T))
                              /RHO**ai-fi) for ai, bi, ui, fi in zip(a, b, graph, F))
    h, u, v, bed = graph
    derivatives = tuple(_dt(ui)-c*_dz(ui) for ui in graph)
    residual = (
        derivatives[0]+_dz(h*u),
        derivatives[1]+u*_dz(u)+g*_dz(h+bed),
        derivatives[2]+u*_dz(v),
        derivatives[3]+K*_dz((u*u+v*v)*u),
    )
    residual = tuple(sp.expand(e) for e in residual)
    coefficients = tuple(_time_coefficients(e) for e in residual)
    reconstruction = tuple(sp.expand(e-sum(value*RHO**j*T**k for j,k,value in row))
                           for e, row in zip(residual, coefficients))
    # Independent conservation-law chain rule, with no reduced-row templates.
    def dx(e): return sum(sp.diff(e, fi)*pi for fi, pi in zip(F, P))
    def dt(e): return sp.diff(e,T)+RHO*sp.diff(e,RHO)-c*dx(e)
    direct = (dt(h)+dx(h*u), dt(u)+u*dx(u)+g*dx(h+bed),
              dt(v)+u*dx(v), dt(bed)+K*dx((u*u+v*v)*u))
    direct_remainder = tuple(sp.expand(left-right) for left,right in zip(direct,residual))
    initial = tuple(sp.expand(e.subs({RHO:1,T:0})-fi) for e,fi in zip(graph,F))
    matrix = sp.Matrix(graph).jacobian(F)
    return {
        'graph':graph, 'residual':residual, 'coefficient_rows':coefficients,
        'Q_remainders':q, 'inverse_remainders':inverse, 'initial_remainders':initial,
        'reconstruction_remainders':reconstruction,
        'direct_PDE_remainders':direct_remainder,
        'field_jacobian':sp.factor(matrix.det()), 'base_jacobian':sp.S.One,
        'all_identities_zero':all(e==0 for e in (*q,*inverse,*initial,*reconstruction,*direct_remainder)),
    }


def graph_certificate(candidate):
    return _graph_certificate(*validate_candidate(candidate))


# 3. Export equations and masks; admission is provided by the independent solver.
def build_certificate(candidate, *, conditional_admitted, conditional_status,
                      equivalence_status, conditional_evidence):
    allowed = {'verified_conditional_on_declared_chart',
               'verified_conditional_on_regular_subchart', 'failed_conditional_criterion'}
    if (conditional_status not in allowed or not conditional_evidence or
            bool(conditional_admitted) != conditional_status.startswith('verified_conditional_')):
        raise ValueError('Inconsistent conditional admission/status/evidence')
    data = graph_certificate(candidate)
    if not data['all_identities_zero']:
        raise ValueError('Input/reconstruction verification failed')
    a,b,c = validate_candidate(candidate)
    return {
        'schema':'sve-ml-input-v1', 'candidate_id':candidate['id'],
        'model':'2D full SVE: G=f=0,m=3,g>0,K>0',
        'field_order':list(FIELDS), 'affine_coefficients':{'a':list(a),'b':list(b),'c':c},
        'conditional_status':conditional_status,
        'conditional_admitted':bool(conditional_admitted),
        'global_chart_admitted':conditional_status=='verified_conditional_on_declared_chart',
        'use':'certified_conditional_solution_class' if conditional_admitted else 'diagnostic_graph_only',
        'classical_equivalence_status':equivalence_status,
        'invariant_coordinates':{'z':f'x-({c})*t','field_invariants':[
            f'exp(-({ai})*t)*({name}-({bi})*(exp(({ai})*t)-1)/({ai}))' if ai else f'{name}-({bi})*t'
            for name,ai,bi in zip(FIELDS,a,b)]},
        'reduced_unknowns':[str(f)+'(z)' for f in F],
        'profile_derivative_symbols':[str(p) for p in P],
        'reconstruction':{'time_symbol':'T=t','rho':'exp(t)>0',
                          'fields':[str(e) for e in data['graph']]},
        'pullback_PDE':[str(e) for e in data['residual']],
        'profile_equations':[[{'exp_rate':j,'time_power':k,'coefficient_must_vanish':str(value)}
                              for j,k,value in row] for row in data['coefficient_rows']],
        'time_split_proof':'Finite distinct t^k exp(j*t) are independent on an open real interval; rho powers are multiplied before grouping.',
        'valid_domain_mask':['g>0','K>0','all values finite','h(t,z)>0','u(t,z)^2+v(t,z)^2>0']+
            (['u(t,z)!=0'] if conditional_status=='verified_conditional_on_regular_subchart' else []),
        'chart':{'base_determinant':'1','field_determinant':str(data['field_jacobian']),
                 'guards':['rho=exp(t)>0','finite real t'],
                 'divisions':['nonzero constant a_i only in the a_i!=0 flow formula','rho**a_i>0'],
                 'no_profile_or_characteristic_division':True},
        'data_conditions':{
            'initial_time':'t=0','initial_fields':[str(f)+'(x)' for f in F],
            'y_independence_required':True,
            'initial_time_derivative':[str(ai*fi+bi-c*pi) for ai,bi,fi,pi in zip(a,b,F,P)],
            'compatibility':'All exported profile coefficient equations and any additional conditional-system guards must hold; arbitrary profiles are not solutions.',
            'boundary':'Boundary values and fluxes must be restrictions of this reconstructed family; no arbitrary IBVP guarantee.',
            'mass_flux':['h*u','h*v'],
            'sediment_flux':['K*(u*u+v*v)*u','K*(u*u+v*v)*v'],
        },
        'applicable_solution_class':'y-independent local smooth graphs obeying Q and all profile equations on the wet, nonzero-speed domain',
        'singular_compatibility':'Implicit profile equations retain singular characteristic loci; no leading-matrix division is used by this adapter.',
        'certificate':{'input_inverse_verified':True,'Q_verified':True,
                       'PDE_pullback_verified':True,'time_coefficients_reconstruct_PDE':True,
                       'identity_remainders':{key:[str(e) for e in data[key]] for key in
                           ('Q_remainders','inverse_remainders','initial_remainders',
                            'reconstruction_remainders','direct_PDE_remainders')},
                       'conditional_evidence':conditional_evidence},
        'independent_review':'required_before_release',
        'training_performed':False,'learned_error_bound':False,
    }


# 4. Numeric callers get an explicit mask, never an implicit certification.
def encode(candidate, t, x, y, fields, gravity=1.0, transport=1.0, *, regular_u_chart=False):
    a,b,c = validate_candidate(candidate)
    if len(fields)!=4:
        raise ValueError('fields must be (h,u,v,B)')
    values = tuple(float(v) for v in fields)
    if not all(math.isfinite(float(v)) for v in (t,x,y,gravity,transport,*values)):
        return {'valid_domain':False,'reason':'nonfinite_input','z':None,'profiles':None}
    try:
        profiles = tuple(math.exp(-ai*t)*(ui-bi*math.expm1(ai*t)/ai) if ai else ui-bi*t
                         for ai,bi,ui in zip(a,b,values))
    except OverflowError:
        return {'valid_domain':False,'reason':'floating_point_overflow','z':None,'profiles':None}
    valid = gravity>0 and transport>0 and values[0]>0 and (values[1]!=0 or values[2]!=0)
    valid = valid and (not regular_u_chart or values[1]!=0)
    valid = valid and all(math.isfinite(v) for v in profiles)
    return {'valid_domain':bool(valid),'reason':'domain_only_not_PDE_or_data_compatibility',
            'z':x-c*t,'profiles':profiles}


def decode(candidate, t, profiles):
    a,b,_ = validate_candidate(candidate)
    if len(profiles)!=4 or not all(math.isfinite(float(v)) for v in (t,*profiles)):
        raise ValueError('Finite time and four finite profile values required')
    return tuple(math.exp(ai*t)*fi+bi*math.expm1(ai*t)/ai if ai else fi+bi*t
                 for ai,bi,fi in zip(a,b,profiles))


def encode_certificate(certificate, t, x, y, fields, gravity=1.0, transport=1.0):
    """Use this entry for exported inputs: the certificate fixes chart guards.

    Admission is the conditional solver's mathematical finding; final source
    review is checked by the package release gate, not by floating-point input.
    Domain validity still does not assert a profile solves its equations.
    """
    status=certificate['conditional_status']
    if (not certificate['conditional_admitted'] or status not in
            {'verified_conditional_on_declared_chart','verified_conditional_on_regular_subchart'}):
        raise ValueError('Diagnostic-only candidates cannot enter the admitted input adapter')
    params=certificate['affine_coefficients']
    candidate={'id':certificate['candidate_id'],**params}
    return encode(candidate,t,x,y,fields,gravity,transport,
                  regular_u_chart=status=='verified_conditional_on_regular_subchart')
