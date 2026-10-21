"""Readable adapters and independent checks of the printed equation (7).

P = D_t(phi_s phi_tt - g phi_ss / phi_s**2)
    - g D_s(m kappa phi_t**(m-1) phi_ts / phi_s).
There is no claim that P is equivalent to the coupled Eulerian SVE system.
"""
from functools import lru_cache
import hashlib
from pathlib import Path

import sympy as sp

SOURCE_SHA256 = '71224cf2e4a3ed456dc0cf9b5bb467fdf484b3ce7b4a7b7d713f649aa9747aa9'


@lru_cache(maxsize=1)
def backend():
    """Load byte-identical recovered source in a private module namespace."""
    source = Path(__file__).with_name('_historical.py')
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise RuntimeError('Historical scalar source hash mismatch')
    from . import _historical
    return _historical


def derive_reduction(case, exponent=3, **kwargs):
    """Derive a source subsection's pullback; exceptional rows retain status.

    For 3.7/3.8 the default translation slope is +1 (positive chart).
    For traveling rows 3.6/3.9 it is -1. This differs deliberately from the
    historical universal alpha=-1 default, which is outside the 3.8 chart.
    """
    kwargs.setdefault('alpha', 1 if str(case) in ('3.7', '3.8') else -1)
    return backend().derive_reduction(case, exponent=exponent, **kwargs)


def compute_ode_series(case, exponent=3, order=6, **kwargs):
    """Exact rational recurrence, with singular and non-ODE status guards."""
    return backend().compute_ode_series(case, exponent=exponent, order=order, **kwargs)


def printed_pde(phi, t, s, exponent=3, g=1, kappa=sp.Rational(1, 30)):
    """Independent original-PDE differentiation, without reduced ODE rules.

    Callers must check phi_s != 0; real fractional powers require phi_t > 0.
    """
    phi = sp.sympify(phi)
    gradient = sp.diff(phi, s)
    if gradient == 0:
        raise ValueError('Printed PDE undefined at phi_s=0')
    velocity = sp.diff(phi, t)
    inertial = gradient * sp.diff(phi, t, 2) - g * sp.diff(phi, s, 2) / gradient**2
    flux = sp.sympify(exponent) * kappa * velocity**(exponent-1) * sp.diff(phi, t, s) / gradient
    return sp.factor(sp.diff(inertial, t) - g * sp.diff(flux, s))


def source_audit():
    """All numbered formula witnesses, not an assertion that the paper agrees."""
    return backend().printed_equation_witnesses()


def exact_solution_checks():
    """Substitute explicit graphs directly in equation (7), including controls."""
    t, s = sp.symbols('t s', positive=True)
    eps = sp.Symbol('epsilon', real=True)
    gv, kv = sp.Integer(1), sp.Rational(1, 30)
    amplitude = sp.real_root(27*gv/(1-12*kv*gv), 3)
    examples = [
        ('3.1', 'stationary_control', s+s**3/6, 's>0,t>0; phi_t=0; m=3 only in this control'),
        ('3.4', 'affine_profile', s+2*t, 's>0,t>0'),
        ('3.4/3.5', 'source_cubic_power', amplitude*s**sp.Rational(1,3)*t**sp.Rational(2,3),
         's>0,t>0; m=3; A^3=45; singular X4 normal form'),
        ('3.6', 'constant_slope_traveling', 2+(s+t)/2, 's>0,t>0'),
        ('3.7', 'arbitrary_profile_example', t+s+s**3/6, 's>0,t>0'),
        ('3.8', 'quadratic_time_profile', s+t+t**2/20, 's>0,t>0'),
        ('3.9', 'constant_slope_mixed_traveling', t+2+(s+t)/2, 's>0,t>0'),
    ]
    rows = []
    for case, label, phi, domain in examples:
        residual = sp.simplify(printed_pde(phi, t, s, 3, gv, kv))
        rows.append(dict(case=case, label=label, phi=phi, domain=domain,
                         velocity=sp.diff(phi,t), gradient=sp.diff(phi,s),
                         model='P', residual=residual, passed=residual == 0))
    perturbed = printed_pde(s+t+t**2/20+eps*t**3, t, s)
    # Original PDE sees the deliberate perturbation exactly, not via ODE RHS.
    negative = dict(phi=s+t+t**2/20+eps*t**3, residual=perturbed,
                    expected=6*eps, passed=sp.simplify(perturbed-6*eps) == 0)
    return dict(examples=rows, negative_control=negative,
                passed=all(row['passed'] for row in rows) and negative['passed'])


def traveling_quadrature(exponent=3, alpha=-1, alpha3=0,
                         g=1, kappa=sp.Rational(1,30)):
    """Exact parametric general solution on the regular nonconstant chart.

    z(r)=z0+(Y(r)-Y(p0))/I0; F(r)=F0+(W(r)-W(p0))/I0,
    Y'=B, W'=r B, r=F'(z), I0 != 0. I0=0 gives affine profiles
    on B!=0. B=0 and zero coordinate speed are separate chart boundaries.
    """
    exponent, alpha, alpha3, g, kappa = map(sp.sympify, (exponent,alpha,alpha3,g,kappa))
    if alpha == 0:
        raise ValueError('alpha=0 is an identity family, not this quadrature')
    r, p0 = sp.symbols('r p0', positive=True)
    I0, z0, F0 = sp.symbols('I0 z0 F0', real=True)
    B = sp.factor(alpha**2*r-g/r**2-g*exponent*kappa*(alpha3-alpha*r)**(exponent-1)/r)
    # Only bounded integer powers are evaluated; all other real powers retain
    # exact integrals instead of invoking unbounded heuristic integration.
    if exponent.is_Integer and 1 <= exponent <= 4:
        Y = sp.integrate(sp.expand(B), r)
        W = sp.integrate(sp.expand(r*B), r)
    else:
        Y, W = sp.Integral(B,r), sp.Integral(r*B,r)
    z_map = z0+(Y-Y.subs(r,p0))/I0
    f_map = F0+(W-W.subs(r,p0))/I0
    dz = sp.diff(z_map,r)
    p = sp.simplify(sp.diff(f_map,r)/dz)
    curvature = sp.simplify(sp.diff(p,r)/dz)
    constant = sp.simplify(B*curvature)
    return dict(B=B, Y=Y, W=W, parameter=r, p0=p0, I0=I0, z0=z0, F0=F0,
                z=z_map, F=f_map, profile_slope=p, profile_curvature=curvature,
                first_integral=constant, passed=(p==r and sp.simplify(constant-I0)==0),
                domain='r>0, alpha3-alpha*r>0, alpha!=0, B(r)!=0, I0!=0',
                zero_integral='F=F0+p0*(z-z0) on B(p0)!=0; also check constant roots B(p0)=0 directly',
                singular_status='B=0 is a failed inverse chart, not a nonexistence proof')
