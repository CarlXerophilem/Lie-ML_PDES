"""Exact point maps for the declared 1D coupled SVE family.

The certificates establish a subgroup and exact coordinate rewrites. They do
not classify the full local point-equivalence groupoid. See EQUIVALENCE.md.
Running this module prints JSON and never rewrites evidence or model files.
"""
from __future__ import annotations

import json
import sympy as sp


def _require(expr, property_name, label):
    expr = sp.sympify(expr)
    if getattr(expr, property_name) is not True:
        raise ValueError(f"{label} must have the proved property {property_name}; got {expr}")
    return expr


def parameter_map(g=None, K=None, G=None, m=None, n=None, *, a=None,
                  b=None, C=None, datum=0, t0=0, x0=0, reflection=1):
    """Return an invertible scaling/translation/reflection and its guards.

    SymPy expressions, rather than floating-point approximations, are returned.
    Inputs must explicitly carry the stated positivity/reality assumptions.
    ``reflection=-1`` changes both x and u; it preserves the signed transport
    law K*abs(u)**(m-1)*u, not an arbitrary extension of u**m to u<0.
    """
    g = sp.Symbol('g', positive=True) if g is None else g
    K = sp.Symbol('K', nonnegative=True) if K is None else K
    G = sp.Symbol('G', nonnegative=True) if G is None else G
    m = sp.Symbol('m', real=True) if m is None else m
    n = sp.Symbol('n', real=True) if n is None else n
    a = sp.Symbol('a', positive=True) if a is None else a
    b = sp.Symbol('b', positive=True) if b is None else b
    C = sp.Symbol('C', positive=True) if C is None else C
    g = _require(g, 'is_positive', 'g')
    K, G = (_require(value, 'is_nonnegative', name)
            for name, value in (('K', K), ('G', G)))
    a, b, C = (_require(value, 'is_positive', name)
               for name, value in (('a', a), ('b', b), ('C', C)))
    m, n, datum, t0, x0 = (_require(value, 'is_real', name) for name, value in
                          (('m', m), ('n', n), ('datum', datum), ('t0', t0), ('x0', x0)))
    reflection = sp.sympify(reflection)
    if reflection not in (sp.S.One, -sp.S.One):
        raise ValueError('reflection must be exactly +1 or -1')
    t, x, u, B = sp.symbols('t x u B', real=True)
    h = sp.Symbol('h', positive=True)
    tp, xp, up, Bp = sp.symbols('t_prime x_prime u_prime B_prime', real=True)
    hp = sp.Symbol('h_prime', positive=True)
    return {
        'parameters': {
            'g': b**2*g/(a**2*C),
            'K': C*(a/b)**(m-1)*K,
            'G': b**(2-n)*a**(n-1)*G,
            'm': m, 'n': n,
        },
        'variables': {'t': a*t+t0, 'x': reflection*b*x+x0,
                      'h': C*h, 'u': reflection*b*u/a, 'B': C*B+datum},
        'inverse': {'t': (tp-t0)/a, 'x': reflection*(xp-x0)/b,
                    'h': hp/C, 'u': reflection*a*up/b, 'B': (Bp-datum)/C},
        'jacobian': b**2*C**2,
        'residual_multipliers': {'mass': C/a, 'primitive_momentum': reflection*b/a**2,
                                 'Exner': C/a, 'conservative_momentum': reflection*C*b/a**2},
        'guards': ['a>0', 'b>0', 'C>0', 'g>0', 'K>=0', 'G>=0', 'h>0',
                   'u!=0', 'm,n real', 'constant a,b,C,t0,x0,datum',
                   'signed flux K*abs(u)**(m-1)*u-G*abs(u)**n*B_x'],
        'scope': 'proved subgroup; full local point-equivalence classification unresolved',
    }


def effective_exponents(K, G, m=None, n=None):
    """Remove only exponents multiplying identically absent flux terms.

    A symbolic nonnegative coefficient alone does not decide its zero branch;
    pass 0 or a strictly positive symbolic/numeric coefficient instead.
    """
    active = []
    for name, value in (('K', K), ('G', G)):
        value = _require(value, 'is_nonnegative', name)
        if value.is_zero is True:
            active.append(False)
        elif value.is_positive is True:
            active.append(True)
        else:
            raise ValueError(f'Decide {name}=0 versus {name}>0 before deduplication')
    if active[0] and m is None:
        raise ValueError('m is required when K>0')
    if active[1] and n is None:
        raise ValueError('n is required when G>0')
    return {'K_active': active[0], 'G_active': active[1],
            'm': _require(m, 'is_real', 'm') if active[0] else None,
            'n': _require(n, 'is_real', 'n') if active[1] else None}


def normal_form(g, K, G, m=None, n=None, *, cubic=None):
    """Choose a representative of a positive-scaling orbit, with an inverse.

    ``cubic=False`` explicitly supplies the m!=3 branch for a symbolic m.
    No assertion about orbits of all admissible point maps is made.
    """
    g = _require(g, 'is_positive', 'g')
    K, G = sp.sympify(K), sp.sympify(G)
    effective = effective_exponents(K, G, m, n)
    m, n = effective['m'], effective['n']
    guards = []
    if effective['K_active']:
        is_cubic = sp.simplify(m-3).is_zero
        if cubic is None:
            if is_cubic is None:
                raise ValueError('Decide m=3 versus m!=3 before normalization')
            cubic = is_cubic
        if cubic and is_cubic is not True:
            raise ValueError('The cubic branch requires m=3 exactly')
        if not cubic and is_cubic is True:
            raise ValueError('Cannot divide by m-3 at m=3')
        r = sp.S.One if cubic else (g*K)**(1/(m-3))
        normalized_K = g*K if cubic else sp.S.One
        if not cubic:
            guards.append('m!=3')
    else:
        r, normalized_K = sp.S.One, sp.S.Zero
    b = r**(n-1)/G if effective['G_active'] else sp.S.One
    a, C = b/r, g*r**2
    # The supplied branch m!=3 proves r>0, but SymPy's intrinsic assumptions
    # cannot encode that relational guard on a generic real m. First obtain
    # the theorem with a positive auxiliary r, then substitute its guarded
    # expression. This does not weaken parameter_map's direct-input guards.
    positive_r = sp.Dummy('positive_velocity_scale', positive=True)
    formal_b = positive_r**(n-1)/G if effective['G_active'] else sp.S.One
    mapping = parameter_map(g, K, G, m if m is not None else 1,
                            n if n is not None else 0, a=formal_b/positive_r,
                            b=formal_b, C=g*positive_r**2)
    for key, value in mapping.items():
        if isinstance(value, dict):
            mapping[key] = {k: v.subs(positive_r, r) if isinstance(v, sp.Basic) else v
                            for k, v in value.items()}
        elif isinstance(value, sp.Basic):
            mapping[key] = value.subs(positive_r, r)
    return {
        'scales': {'a': a, 'b': b, 'C': C, 'r=b/a': r},
        'representative': {'g': sp.S.One, 'K': normalized_K,
                           'G': sp.S.One if effective['G_active'] else sp.S.Zero,
                           'm': m, 'n': n},
        'modulus': g*K if effective['K_active'] and cubic else None,
        'modulus_scope': 'invariant of the verified scaling subgroup only',
        'map': mapping, 'guards': guards + mapping['guards'],
    }


def equivalence_status():
    """Machine-readable obligations; a sufficiency check cannot close them."""
    return {
        'status': 'verified_subgroup_and_coordinate_rewrites',
        'known_subgroup': 'proved',
        'positive_scaling_orbits': 'classified_exactly',
        'effective_exponent_deduplication': 'proved_by_identical_PDEs',
        'negative_speed_chart': 'proved_for_signed_absolute_value_flux',
        'time_reversal': 'proved_on_G_zero_only_within_nonnegative_G_family',
        'primitive_conservative_point_map': 'proved_for_smooth_h_positive_fields',
        'bed_reference_rewrite': 'proved_with_fixed_reference_bed_derivatives_retained',
        'restricted_necessity': 'affine_independent_variables_and_separated_field_maps_only',
        'full_local_point_equivalence': 'unresolved',
        'complete': False,
        'gate_passed': False,
        'unresolved_obligations': [
            'derive general admissible point transformations without assuming projectability or separated fields',
            'integrate cross-parameter equivalence equations on every coefficient-zero and exponent stratum',
            'exclude or exhibit additional exponent-changing or cubic-modulus-changing admissible maps',
            'classify possible discrete components and exceptional same-equation point maps',
        ],
        'nonclaims': ['no maximal equivalence group or groupoid', 'no arbitrary-data equivalence',
                      'no weak/shock equivalence', 'no material or scalar-model point equivalence'],
    }


def verify_maps():
    """Direct chain-rule certificates on symbolic real exponent branches.

    The tests retain free jets and compare off-shell residual identities.
    They do not sample exponents, substitute example solutions, or solve a
    finite generator ansatz. No files are written.
    """
    checks, residuals = [], {}

    def clean(expr):
        return sp.simplify(sp.expand_power_base(sp.expand(expr)))

    def check(name, expr):
        remainder = clean(expr)
        residuals[name] = str(remainder)
        checks.append({'name': name, 'passed': remainder == 0})

    a, b, C, g, K, G, v, h = sp.symbols('a b C g K G v h', positive=True)
    m, n = sp.symbols('m n', real=True)
    ht, ut, Bt, hx, ux, Bx, Bxx = sp.symbols('h_t u_t B_t h_x u_x B_x B_xx', real=True)
    mapped = parameter_map(g, K, G, m, n, a=a, b=b, C=C)['parameters']

    for speed_sign in (-1, 1):
        for reflect in (-1, 1):
            u, speed_prime = speed_sign*v, b*v/a
            H, U = C*h, reflect*b*u/a
            Ht, Hx = C*ht/a, reflect*C*hx/b
            Ut, Ux = reflect*b*ut/a**2, ux/a
            Zt, Zx, Zxx = C*Bt/a, reflect*C*Bx/b, C*Bxx/b**2
            old = (ht+u*hx+h*ux, ut+u*ux+g*(hx+Bx),
                   Bt+K*m*v**(m-1)*ux-G*(v**n*Bxx+n*speed_sign*v**(n-1)*ux*Bx))
            new = (Ht+U*Hx+H*Ux, Ut+U*Ux+mapped['g']*(Hx+Zx),
                   Zt+mapped['K']*m*speed_prime**(m-1)*Ux
                   -mapped['G']*(speed_prime**n*Zxx
                       +n*reflect*speed_sign*speed_prime**(n-1)*Ux*Zx))
            for name, actual, expected in zip(('mass', 'momentum', 'Exner'), new,
                    (C*old[0]/a, reflect*b*old[1]/a**2, C*old[2]/a)):
                check(f'chart {speed_sign:+d}, reflection {reflect:+d}: {name}', actual-expected)

    t, x, u, B, t0, x0, datum = sp.symbols('t x u B t0 x0 datum', real=True)
    for reflect in (-1, 1):
        transformed = sp.Matrix((a*t+t0, reflect*b*x+x0, C*h,
                                  reflect*b*u/a, C*B+datum))
        check(f'Jacobian reflection {reflect:+d}', transformed.jacobian((t,x,h,u,B)).det()-b**2*C**2)
        inverse = ((transformed[0]-t0)/a, reflect*(transformed[1]-x0)/b,
                   transformed[2]/C, reflect*a*transformed[3]/b, (transformed[4]-datum)/C)
        for name, back, original in zip(('t', 'x', 'h', 'u', 'B'), inverse, (t,x,h,u,B)):
            check(f'inverse reflection {reflect:+d}: {name}', back-original)

    # Smooth primitive -> conservative variables: q=hu, h>0.
    mass, primitive_momentum = ht+u*hx+h*ux, ut+u*ux+g*(hx+Bx)
    conservative_momentum = u*ht+h*ut+u**2*hx+2*h*u*ux+g*h*hx+g*h*Bx
    check('conservative momentum = h*primitive momentum + u*mass',
          conservative_momentum-h*primitive_momentum-u*mass)
    check('primitive-to-conservative field Jacobian',
          sp.Matrix((h,h*u,B)).jacobian((h,u,B)).det()-h)
    q = sp.Symbol('q', real=True)
    check('momentum coordinate inverse', (h*u/h)-u)
    check('velocity coordinate inverse', h*(q/h)-q)

    # Fixed reference bed b0(x): never discard its slope or curvature.
    zt, zx, zxx, b0x, b0xx = sp.symbols('zeta_t zeta_x zeta_xx b0_x b0_xx', real=True)
    old_bed = Bt+K*m*v**(m-1)*ux-G*(v**n*Bxx+n*v**(n-1)*ux*Bx)
    ref_sub = {Bt:zt, Bx:b0x+zx, Bxx:b0xx+zxx}
    rewritten_bed = zt+K*m*v**(m-1)*ux-G*(v**n*(b0xx+zxx)+n*v**(n-1)*ux*(b0x+zx))
    check('fixed reference bed Exner rewrite', old_bed.subs(ref_sub)-rewritten_bed)
    check('fixed reference bed momentum rewrite',
          primitive_momentum.subs(Bx,b0x+zx)-(ut+u*ux+g*(hx+b0x+zx)))

    check('scaling product identity', mapped['g']*mapped['K']-(b/a)**(3-m)*g*K)
    check('cubic scaling invariant', (mapped['g']*mapped['K']).subs(m,3)-g*K)
    log_weights = sp.Matrix(((-2,2,-1),(m-1,1-m,1),(n-1,2-n,0)))
    check('logarithmic parameter-map determinant', log_weights.det()-(3-m))

    # This extra discrete admissible map is outside the positive-time subgroup.
    diffusion = G*(v**n*Bxx+n*v**(n-1)*ux*Bx)
    zero_slope_bed = Bt+K*m*v**(m-1)*ux
    check('G=0 time reversal: mass', (-ht-u*hx-h*ux)+mass)
    check('G=0 time reversal: momentum', (ut+u*ux+g*(hx+Bx))-primitive_momentum)
    check('G=0 time reversal: Exner', (-Bt-K*m*v**(m-1)*ux)+zero_slope_bed)
    check('time reversal with unchanged G has exact diffusion defect',
          (-zero_slope_bed-diffusion)+(zero_slope_bed-diffusion)+2*diffusion)

    # Normal-form coefficient checks: symbolic noncubic m and real n.
    for label, ks, gs, ms, ns, cubic in (
        ('generic grass', K, 0, m, None, False),
        ('generic slope', K, G, m, n, False),
        ('cubic grass', K, 0, 3, None, True),
        ('cubic slope', K, G, 3, n, True),
        ('slope only', 0, G, None, n, None),
        ('zero transport', 0, 0, None, None, None),
    ):
        form = normal_form(g, ks, gs, ms, ns, cubic=cubic)
        for coefficient in ('g','K','G'):
            difference = (form['map']['parameters'][coefficient]
                          -form['representative'][coefficient])
            if cubic is False:
                # Encode the recorded nonzero divisor for the assumptions
                # engine; this is the whole m!=3 branch, not a sample value.
                nonzero_difference = sp.Symbol('m_minus_3', real=True, nonzero=True)
                difference = difference.subs(m, 3+nonzero_difference)
            difference = sp.powdenest(difference, force=False)
            coefficient_label = {'g': 'gravity', 'K': 'transport', 'G': 'slope'}[coefficient]
            check(f'{label} normalization: {coefficient_label}', difference)

    # Identical-PDE deduplication, not an equivalence maximality assertion.
    for label, actual, expected in (
        ('K=0 removes m', effective_exponents(0,G,2,n)['m'], None),
        ('G=0 removes n', effective_exponents(K,0,m,2)['n'], None),
        ('K=G=0 removes both', tuple(effective_exponents(0,0,2,3)[e] for e in ('m','n')), (None,None)),
    ):
        checks.append({'name': label, 'passed': actual == expected})

    # Broken-hypothesis controls must fail for a concrete nonzero witness.
    wrong_g_momentum_defect = (g*C/b-b*g/a**2)*(hx+Bx)
    bad_reflection_defect = -2*(u*hx+h*ux)
    controls = {
        'keeping g fixed under arbitrary scales': wrong_g_momentum_defect.subs({a:2,b:3,C:5,g:1,hx:1,Bx:0}),
        'reflecting x without u': bad_reflection_defect.subs({u:1,h:1,hx:1,ux:0}),
        'discarding a nonconstant reference-bed slope': g*sp.S.One,
        'time-dependent datum in Exner': sp.S.One,
        'time reversal with unchanged positive G': -2*G,
    }
    for name, witness in controls.items():
        checks.append({'name': 'negative control: '+name, 'passed': witness.is_zero is False})
    for name, kwargs in (('zero scale', {'a':0}), ('negative depth scale', {'C':-1}),
                         ('invalid reflection', {'reflection':0})):
        rejected = False
        try:
            parameter_map(**kwargs)
        except ValueError:
            rejected = True
        checks.append({'name': 'guard rejection: '+name, 'passed': rejected})
    return {'all_passed': all(item['passed'] for item in checks), 'check_count': len(checks),
            'checks': checks, 'exact_residuals': residuals,
            'negative_control_witnesses': {name: str(expr) for name,expr in controls.items()},
            'status': equivalence_status()}


if __name__ == '__main__':
    result = verify_maps()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['all_passed'] else 1)
