"""Deterministic complete-JetSpace discovery and reduction for planar E2 and rotating exchange."""
import json
import sympy as sp

from lie_reduce.models import discover_and_enumerate, exchange_spec, planar_e2_spec
from lie_reduce.multid import reduce_nd


def _require(condition, stage):
    if not condition:
        raise ArithmeticError(stage)


def discover_planar_e2(exponent=None):
    """Discover the 5D Cartesian E2 algebra and reduce <R, d_t + c d_B> to the scalar ODE."""
    m = sp.Symbol('m', real=True) if exponent is None else sp.sympify(exponent)
    spec = planar_e2_spec(m)
    exp_sym = m if isinstance(m, sp.Symbol) else None
    _, basis, subalgebras = discover_and_enumerate(spec, degree=1, exponent=exp_sym)
    c = sp.Symbol('c', real=True)
    alpha_1 = sp.Symbol('alpha_1', real=True)
    chosen = next(s for s in subalgebras if 'X5' in s['id'] and 'X1 + alpha_1*X4' in s['id'])
    gens = [tuple(sp.sympify(comp).subs(alpha_1, c) for comp in g_vec) for g_vec in chosen['generators']]
    red = reduce_nd(spec, gens)
    _require(red.status == 'verified' and len(red.reduced_equations) == 1,
             'Cartesian E2 reduces deterministically via 3 first integrals to 1 scalar ODE')
    return spec, basis, subalgebras, red


def discover_exchange():
    """Discover the 2D polar exchange point algebra and reduce <d_t, d_theta>."""
    spec, basis, subalgebras = discover_and_enumerate(exchange_spec(), degree=1)
    chosen = next(s for s in subalgebras if s['id'] == 'X1 ; X2')
    red = reduce_nd(spec, chosen['generators'])
    _require(red.status == 'verified' and len(red.first_integrals) == 3,
             'Polar exchange reduces deterministically via 3 first integrals')
    return spec, basis, subalgebras, red


def discover_exchange_swirl_ode():
    """Evaluate the polar exchange JetSpace equations on the swirl invariant submanifold."""
    spec = exchange_spec()
    j = spec.jets
    t, r, th = j.independent
    h, V, W, B, A = j.dependent
    g, K, G, omega, kd, ke, Da = spec.parameters
    b_fn = sp.Function('b')(t)
    bed = sp.Rational(1, 10) / r**2
    lifts = (
        1 + sp.Rational(25, 72) * r**2 - bed,
        sp.S.Zero,
        r / sp.Integer(2),
        bed + b_fn,
        bed / sp.Integer(2) + sp.Rational(9, 20) - b_fn,
    )
    pars = {g: 1, K: 1, G: 1, omega: sp.Rational(1, 3), kd: 2, ke: 1, Da: 0}
    jmap = j.pullback(lifts)
    pulled = [sp.simplify(eq.xreplace(jmap).subs(pars).doit()) for eq in spec.equations]
    _require(pulled[0] == 0 and pulled[1] == 0 and pulled[2] == 0, 'hydrodynamic swirl balances')
    _require(sp.simplify(pulled[3] + pulled[4]) == 0, 'total sediment conservation on swirl')
    return spec, b_fn, t, r, pulled[3], lifts, pars


def run(e2_bundle=None):
    e2_spec, e2_basis, e2_subs, e2_red = e2_bundle or discover_planar_e2()
    ex_spec, ex_basis, ex_subs, ex_red = discover_exchange()
    _, b_fn, t_sym, r_sym, swirl_ode, _, pars = discover_exchange_swirl_ode()

    p_sym = sp.Symbol('p', real=True)
    b_sol = sp.Rational(3, 10) + (p_sym - sp.Rational(3, 10)) * sp.exp(-3 * t_sym)
    swirl_check = sp.simplify(swirl_ode.subs(b_fn, b_sol).doit())
    _require(swirl_check == 0, 'swirl decay residual')

    # Verify r * Q_r == 1/20 on the swirl control
    V_s, W_s, B_r = sp.S.Zero, r_sym / 2, sp.diff(sp.Rational(1, 10) / r_sym**2, r_sym)
    r_Qr = sp.simplify(r_sym * (V_s**2 + W_s**2) * (1 * V_s - 1 * B_r))
    _require(r_Qr == sp.Rational(1, 20), 'swirl radial bedload throughput')

    return {
        'E2_planar': {
            'discovered_basis': {k: list(map(str, v)) for k, v in e2_basis.items()},
            'enumerated_rank2_subalgebras': len(e2_subs),
            'first_integrals_count': len(e2_red.first_integrals),
            'eliminated_profiles': {str(k): str(v) for k, v in e2_red.eliminated.items()},
            'scalar_ode': str(e2_red.reduced_equations[0]) + ' = 0',
            'preserved_parameters': [str(p) for p in e2_red.preserved_parameters],
        },
        'E_exch': {
            'discovered_basis': {k: list(map(str, v)) for k, v in ex_basis.items()},
            'enumerated_rank2_subalgebras': len(ex_subs),
            'first_integrals_count': len(ex_red.first_integrals),
            'reduced_equations': [str(eq) + ' = 0' for eq in ex_red.reduced_equations],
            'preserved_parameters': [str(p) for p in ex_red.preserved_parameters],
        },
        'swirl_ode': str(swirl_ode) + ' = 0',
        'swirl_b': str(b_sol),
        'swirl_residuals': ['0', '0', '0', str(swirl_check), str(-swirl_check)],
        'swirl_r_Qr': str(r_Qr),
        'scope': 'Complete-JetSpace point discovery, combination subalgebra enumeration, and exact multi-integral quotients.',
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
