#!/usr/bin/env python3
"""End-to-end verification: hidden strata, (d+1)D quotients, and random PDE -> unparsed ML handoff.

Part A  Manuscript models E1, P, M on complete JetSpace with symbolic parameters (g, K, kappa, m):
        verifies exact pivot-minor + power-resonance jump strata {E1: [0,3], P: [0,1,3], M: [0,3]}.
Part B  Polar E2 and Cartesian planar E2 with symbolic (g, K, G, f, m): discovers basis generators,
        enumerates rank-2 combinations, reduces via 3 constructive first integrals to 1 scalar ODE
        preserving all 9 parameters (C1, C2, C3, G, K, c, f, g, m), and proves quotient equality.
Part C  Randomly formed PDEs across 1+1D, 2+1D, and 3+1D (nonlinear scalar PDEs, coupled multi-field
        conservation systems, and non-diagonal rotational flows) with symbolic parameters preserved
        through reduction and passed directly in-memory (without string parsing or manual edits) into
        the ML layer (_profile_learning.Case.from_reduction -> compare).
"""

import _bootstrap  # historical standalone script path
import argparse
import json
import random
import sympy as sp

from _profile_learning import Case, Settings, compare
from lie_reduce import JetSpace, PDESpec, serial, timed
from lie_reduce.hidden import specialize, strata
from lie_reduce.models import discover_and_enumerate, euler_spec, planar_e2_spec, polar_e2_spec, scalar_spec
from lie_reduce.multid import reduce_nd
from lie_reduce.reduce import reduce


def manuscript_strata():
    m = sp.Symbol('m', real=True)
    out = {}
    for name, spec in (('E1', euler_spec(m)), ('P', scalar_spec('P', m)), ('M', scalar_spec('M', m))):
        r = strata(spec, m, 1, exponent=True)
        out[name] = {
            'generic_dimension': r['generic_kernel_dimension'],
            'preserved_parameters': r['preserved_parameters'],
            'pivot_minor_factors': r['pivot_minor_factors'],
            'resonances': r['resonances'],
            'strata': [
                {k: s[k] for k in ('value', 'kernel_dimension', 'jump', 'extra', 'source') if k in s}
                for s in r['strata']
            ],
        }
    jumps = {k: sorted(s['value'] for s in v['strata'] if s.get('jump')) for k, v in out.items()}
    expected = {'E1': [0, 3], 'P': [0, 1, 3], 'M': [0, 3]}
    out['jumps'] = jumps
    out['match'] = jumps == expected
    return out


def polar_and_planar_E2():
    m = sp.Symbol('m', real=True)
    c = sp.Symbol('c', real=True)
    alpha_1 = sp.Symbol('alpha_1', real=True)

    pol_spec, pol_basis, pol_subs = discover_and_enumerate(polar_e2_spec(m), degree=1, exponent=m)
    pol_sub = next(s for s in pol_subs if 'X2' in s['id'] and 'X1 + alpha_1*X3' in s['id'])
    pol_gens = [tuple(sp.sympify(v).subs(alpha_1, c) for v in g) for g in pol_sub['generators']]
    pol_red = reduce_nd(pol_spec, pol_gens)

    pla_spec, pla_basis, pla_subs = discover_and_enumerate(planar_e2_spec(m), degree=1, exponent=m)
    pla_sub = next(s for s in pla_subs if 'X5' in s['id'] and 'X1 + alpha_1*X4' in s['id'])
    pla_gens = [tuple(sp.sympify(v).subs(alpha_1, c) for v in g) for g in pla_sub['generators']]
    pla_red = reduce_nd(pla_spec, pla_gens)

    z = pla_red.graph.z
    F_pol = pol_red.target_profile
    F_pla = pla_red.target_profile
    ode_pol = pol_red.reduced_equations[0].subs(pol_red.graph.z, z).subs(F_pol, F_pla)
    ode_pla = pla_red.reduced_equations[0]
    diff_scalar = sp.simplify(sp.powsimp(sp.expand(ode_pla - ode_pol)))

    return {
        'polar': {
            'status': pol_red.status,
            'discovered_basis_dim': len(pol_basis),
            'first_integrals': len(pol_red.first_integrals),
            'reduced_equations_count': len(pol_red.reduced_equations),
            'preserved_parameters': [str(p) for p in pol_red.preserved_parameters],
        },
        'planar': {
            'status': pla_red.status,
            'discovered_basis_dim': len(pla_basis),
            'enumerated_subalgebras': len(pla_subs),
            'first_integrals': len(pla_red.first_integrals),
            'reduced_equations_count': len(pla_red.reduced_equations),
            'weight_kind': pla_red.checks.get('weight_kind'),
            'preserved_parameters': [str(p) for p in pla_red.preserved_parameters],
            'scalar_ode': str(ode_pla) + ' = 0',
        },
        'scalar_ode_difference': str(diff_scalar),
        'match': (
            pol_red.status == 'verified'
            and pla_red.status == 'verified'
            and len(pol_red.reduced_equations) == 1
            and len(pla_red.reduced_equations) == 1
            and len(pla_red.preserved_parameters) == 9
            and diff_scalar == 0
        ),
    }


def random_scalar_pde(seed, space_dim):
    """Random nonlinear scalar PDE in (space_dim + 1) independent variables with symbolic parameters."""
    rng = random.Random(seed * 31 + space_dim)
    t = sp.Symbol('t', real=True)
    xs = tuple(sp.Symbol(f'x{i+1}', real=True) for i in range(space_dim))
    u = sp.Symbol('u', positive=True)
    nu_sym = sp.Symbol('nu', positive=True)
    mu_sym = sp.Symbol('mu', real=True)
    j = JetSpace((t, *xs), (u,), 2)
    e = lambda idx: tuple(int(k == idx) for k in range(space_dim + 1))
    ee = lambda idx: tuple(2 * int(k == idx) for k in range(space_dim + 1))

    diff_weights = [rng.choice((1, 2)) for _ in xs]
    adv_weights = [rng.choice((1, -1, 2)) for _ in xs]
    kind = ('damping', 'quadratic_source', 'drift')[seed % 3]

    rhs = nu_sym * sum(w * j.jets[0, ee(i + 1)] for i, w in enumerate(diff_weights))
    rhs += u * sum(a * j.jets[0, e(i + 1)] for i, a in enumerate(adv_weights))
    if kind == 'damping':
        rhs -= mu_sym * u
    elif kind == 'quadratic_source':
        rhs -= mu_sym * u ** 2
    else:
        rhs += mu_sym * j.jets[0, e(1)]

    eq = sp.expand(j.jets[0, e(0)] - rhs)
    spec = PDESpec(
        f'random_{space_dim}p1D_scalar_s{seed}', j, (eq,), (j.jets[0, e(0)],),
        (nu_sym, mu_sym), ('u>0', 'nu>0'), positive=(u, nu_sym),
    )
    return spec, {'nu': nu_sym, 'mu': mu_sym}


def random_coupled_pde(seed, space_dim):
    """Random coupled 2-field conservation + dispersive/diffusive PDE system with symbolic parameters."""
    rng = random.Random(seed * 97 + space_dim)
    t = sp.Symbol('t', real=True)
    xs = tuple(sp.Symbol(f'x{i+1}', real=True) for i in range(space_dim))
    u, v = sp.symbols('u v', positive=True)
    alpha_s, beta_s = sp.symbols('alpha_p beta_p', positive=True)
    j = JetSpace((t, *xs), (u, v), 2)
    Dt = lambda expr: j.D(expr, 0)
    Dx1 = lambda expr: j.D(expr, 1)
    c_flux = rng.choice((1, 2))
    # Eq 1: exact conservation law Dt(v) + c_flux * Dx1(u * v) (+ sum_{i>=2} Dxi(v)) == 0
    eq1 = Dt(v) + c_flux * Dx1(u * v) + sum(j.D(v, i) for i in range(2, space_dim + 1))
    # Eq 2: nonlinear diffusive-advective balance coupled to v
    lap_u = sum(j.D(j.D(u, i), i) for i in range(1, space_dim + 1))
    eq2 = Dt(u) - alpha_s * lap_u + beta_s * Dx1(v) + rng.choice((0, 1)) * u * Dx1(u)
    spec = PDESpec(
        f'random_{space_dim}p1D_coupled_s{seed}', j, (sp.expand(eq1), sp.expand(eq2)),
        (j.jet(0, *(1, *(0,) * space_dim)), j.jet(1, *(1, *(0,) * space_dim))),
        (alpha_s, beta_s), ('u>0', 'v>0', 'alpha_p,beta_p>0'), positive=(u, v, alpha_s, beta_s),
    )
    return spec, {'alpha_p': alpha_s, 'beta_p': beta_s}


def _run_random_pde_to_ml(spec):
    """Discover symmetries, pick first combination reducing to a scalar ODE >= order 1, and run ML compare."""
    _, basis, subalgebras = discover_and_enumerate(spec, degree=1, max_combo_terms=2)
    red_chosen = None
    sub_chosen = None
    # Prefer combinations with nonzero traveling wave coupling (alpha_1 != 0) so time/space derivatives both survive
    ordered_subs = sorted(subalgebras, key=lambda s: ('alpha_1' not in s['id'], s['id']))
    for sub in ordered_subs:
        stage = timed(lambda g=sub['generators']: reduce(spec, g), 15)
        red = stage['value']
        if red is None or red.status != 'verified' or len(red.reduced_equations) != 1:
            continue
        ode_expr = red.reduced_equations[0]
        F_target = red.target_profile or red.graph.profiles[0]
        z_sym = red.graph.z
        orders = [d.derivative_count for d in ode_expr.atoms(sp.Derivative) if d.expr == F_target]
        max_ord = int(max(orders, default=0))
        if max_ord < 1 or max_ord > 3:
            continue
        lead_coeff = sp.simplify(sp.diff(ode_expr, sp.diff(F_target, z_sym, max_ord)))
        if lead_coeff == 0:
            continue
        red_chosen = red
        sub_chosen = sub
        break

    if red_chosen is None:
        raise ArithmeticError(f'{spec.name}: no scalar ODE quotient found among enumerated subalgebras')

    # Assign concrete positive parameter values ONLY at the ML numeric stage (symbolic ODE retains all symbols!)
    p_sym = sp.Symbol('p_trace', real=True)
    param_vals = {}
    for idx_s, sym in enumerate(red_chosen.preserved_parameters):
        nm = str(sym)
        if nm.startswith('alpha_') and nm[-1].isdigit():
            param_vals[sym] = -sp.Rational(3, 2) - sp.Rational(idx_s, 5)
        elif nm.startswith('C'):
            param_vals[sym] = sp.Rational(1, 2)
        else:
            param_vals[sym] = sp.Rational(1, 1) + sp.Rational(idx_s, 5)

    ode_test = sp.together(red_chosen.reduced_equations[0].subs(param_vals).doit())
    F_target = red_chosen.target_profile or red_chosen.graph.profiles[0]
    z_sym = red_chosen.graph.z
    order = int(max(d.derivative_count for d in ode_test.atoms(sp.Derivative) if d.expr == F_target))
    trace_exprs = (p_sym,) + tuple(sp.Rational(1, 10) for _ in range(order - 1))

    ml_case = Case.from_reduction(
        spec.name,
        red_chosen,
        left=0.2,
        trace_interval=(0.8, 1.1),
        trace_exprs=trace_exprs,
        parameter_symbol=p_sym,
        parameter_values=param_vals,
    )
    fast_settings = Settings(seed=27, width=5, chebyshev_degree=22, taylor_degree=24,
                             train_coordinates=18, test_coordinates=101, max_nfev=80)
    ml_record = compare(ml_case, fast_settings)
    return {
        'model': spec.name,
        'basis_dimension': len(basis),
        'selected_subalgebra': sub_chosen['id'],
        'preserved_symbolic_parameters': [str(p) for p in red_chosen.preserved_parameters],
        'first_integrals_eliminated': len(red_chosen.first_integrals),
        'symbolic_ode': str(red_chosen.reduced_equations[0]) + ' = 0',
        'is_linear_ode': ml_case.is_linear,
        'ml_handoff_mode': ml_record['handoff_mode'],
        'ml_selected_method': ml_record['selection']['selected'],
        'ml_selected_field_max_error': ml_record['selection']['selected_field_maximum'],
        'ml_chebyshev_residual_max': ml_record['metrics']['Chebyshev']['original_residual_maximum'],
        'ml_lnn_field_max_error': ml_record['metrics']['LNN-PINN']['field_maximum'],
        'passed': (
            len(red_chosen.preserved_parameters) >= len(spec.parameters)
            and ml_record['selection']['selected'] is not None
            and ml_record['selection']['selected_field_maximum'] < 1e-6
        ),
    }


def nondiagonal_rotational_check():
    """Verify non-diagonal rotational field reduction on coupled 1+1D Cauchy-Riemann-type system."""
    t, x, u, v = sp.symbols('t x u v', real=True)
    j = JetSpace((t, x), (u, v), 1)
    spec = PDESpec('coupled_rotational_1p1D', j,
                   (j.D(u, 0) + j.D(v, 1), j.D(v, 0) - j.D(u, 1)),
                   (j.jet(0, 1, 0), j.jet(1, 1, 0)))
    red = reduce(spec, (-x, t, -v, u))
    return {
        'model': spec.name,
        'status': red.status,
        'weight_kind': red.checks.get('weight_kind'),
        'equations': [str(e) + ' = 0' for e in red.equations],
        'passed': red.status == 'verified',
    }


def random_end_to_end_suite(seeds):
    rows = []
    for seed in seeds:
        # 1+1D, 2+1D, and 3+1D random nonlinear scalar PDEs with symbolic parameters
        for space_dim in (1, 2, 3) if seed == seeds[0] else (2,):
            spec_s, _ = random_scalar_pde(seed, space_dim)
            rows.append(_run_random_pde_to_ml(spec_s))
        # Coupled 2-component PDEs (1+1D and 2+1D) with first-integral elimination + ML handoff
        spec_c, _ = random_coupled_pde(seed, 1 if seed % 2 == 0 else 2)
        rows.append(_run_random_pde_to_ml(spec_c))
    return rows


def random_strata_suite(seeds):
    """Verify hidden-parameter stratum detection on seeded 2+1D and 3+1D random PDEs."""
    rows = []
    for seed in seeds[:2]:
        for space in (2, 3):
            rng = random.Random(seed)
            t = sp.Symbol('t', real=True)
            xs = sp.symbols(' '.join(f'x{i+1}' for i in range(space)), real=True)
            u = sp.Symbol('u', positive=True)
            j = JetSpace((t, *xs), (u,), 2)
            e = lambda idx: tuple(int(k == idx) for k in range(space + 1))
            ee = lambda idx: tuple(2 * int(k == idx) for k in range(space + 1))
            kind = ('damping', 'power')[seed % 2]
            mu = sp.Symbol('m' if kind == 'power' else 'mu', real=True)
            rhs = sum((i + 1) * j.jets[0, ee(i + 1)] for i in range(space)) + u * j.jets[0, e(1)]
            rhs += (u ** mu if kind == 'power' else mu * u)
            eq = sp.expand(j.jets[0, e(0)] - rhs)
            spec = PDESpec(f'strata_{space+1}D_s{seed}', j, (eq,), (j.jets[0, e(0)],), (mu,), ('u>0',), positive=(u,))
            r = strata(spec, mu, 1, exponent=(kind == 'power'))
            jumps = [s for s in r['strata'] if s.get('jump')]
            rows.append({
                'model': spec.name,
                'generic_dimension': r['generic_kernel_dimension'],
                'jump_strata_count': len(jumps),
                'decided': all(s['status'] == 'decided' for s in r['strata']),
            })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--seeds', type=int, nargs='*', default=[0, 1, 2])
    args = parser.parse_args()

    part_a = manuscript_strata()
    part_b = polar_and_planar_E2()
    rot_check = nondiagonal_rotational_check()
    rand_strata = random_strata_suite(args.seeds)
    rand_ml = random_end_to_end_suite(args.seeds)

    summary = {
        'manuscript_strata_match': part_a['match'],
        'E2_polar_and_planar_match': part_b['match'],
        'nondiagonal_rotational_verified': rot_check['passed'],
        'random_strata_all_decided': all(r['decided'] and r['jump_strata_count'] >= 1 for r in rand_strata),
        'random_pde_to_ml_total': len(rand_ml),
        'random_pde_to_ml_passed': sum(bool(r['passed']) for r in rand_ml),
    }
    report = {
        'manuscript_strata': part_a,
        'E2_polar_and_planar': part_b,
        'nondiagonal_rotational': rot_check,
        'random_strata': rand_strata,
        'random_pde_to_ml': rand_ml,
        'summary': summary,
    }
    print(json.dumps(serial(report), indent=2, default=str))
    ok = (
        summary['manuscript_strata_match']
        and summary['E2_polar_and_planar_match']
        and summary['nondiagonal_rotational_verified']
        and summary['random_strata_all_decided']
        and summary['random_pde_to_ml_passed'] == summary['random_pde_to_ml_total']
    )
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
