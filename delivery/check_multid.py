#!/usr/bin/env python3
"""Hidden-parameter strata and automatic PDE->ODE quotients in 1+1, 2+1 and 3+1 dimensions.

Part A  the three manuscript models E1, P, M with symbolic exponent m: the
        degree-1 determining matrix is built for the general generator and the
        strata with extra symmetry are found from the pivot minor and the power
        resonances, then decided by exact specialization.
Part B  E2 in polar (t, r, theta) and planar E2 in Cartesian (t, x, y): the rank-2
        quotient is built automatically and compared with the supplied graph.
Part C  seeded random scalar models in 2+1 and 3+1 dimensions with a hidden
        parameter. Each stratum is reduced to an ODE through a subalgebra that
        contains one of its extra generators.
"""
import argparse
import json
import random
from itertools import combinations, islice
import sympy as sp
from lie_reduce.jets import JetSpace
from lie_reduce.spec import PDESpec
from lie_reduce.hidden import strata, specialize
from lie_reduce.multid import reduce_nd, affine, closed
from lie_reduce.hidden import special_kernel as symmetries
from lie_reduce.run import serial, timed


def manuscript_strata():
    from lie_reduce.models import _euler_spec, _scalar_spec
    m = sp.Symbol('m', real=True)
    out = {}
    for name, spec in (('E1', _euler_spec(m)), ('P', _scalar_spec('P', m)), ('M', _scalar_spec('M', m))):
        r = strata(spec, m, 1, exponent=True)
        out[name] = {'generic_dimension': r['generic_kernel_dimension'], 'pivot_minor_factors': r['pivot_minor_factors'],
                     'resonances': r['resonances'],
                     'strata': [{k: s[k] for k in ('value', 'kernel_dimension', 'jump', 'extra', 'source') if k in s}
                                for s in r['strata']]}
    jumps = {k: sorted(s['value'] for s in v['strata'] if s.get('jump')) for k, v in out.items()}
    expected = {'E1': [0, 3], 'P': [0, 1, 3], 'M': [0, 3]}
    out['jumps'] = jumps
    out['match'] = jumps == expected
    out['reading'] = ('m=3: dilation X5/Y5 in all three; m=1: Galilean boost in P only (obstructed in M); '
                      'm=0: transport switched off (degenerate). Resonant m=2,4 decided with no jump.')
    return out


def polar_E2():
    from lie_reduce.models import annular
    from lie_reduce.reduce import reduce_subalgebra
    spec, fields, graph, _ = annular()
    auto = reduce_nd(spec, fields)
    manual = reduce_subalgebra(spec, fields, graph)
    z = auto.graph.z
    to = {F: G.subs(graph.z, z) for F, G in zip(auto.graph.profiles, graph.profiles)}
    diff = [sp.simplify(a.subs(to).doit() - b.subs(graph.z, z)) for a, b in zip(auto.equations, manual.equations)]
    return {'model': 'E2 polar (t,r,theta)', 'generators': 'd_theta, d_t + c d_B', 'status': auto.status,
            'weights': auto.weights, 'odes': auto.equations, 'difference_to_supplied_graph': diff,
            'match': auto.status == 'verified' and all(d == 0 for d in diff)}


def planar_E2():
    t, x, y = sp.symbols('t x y', real=True)
    h, u, v, B = sp.symbols('h u v B', real=True)
    g, K, G = sp.symbols('g K G', positive=True)
    f, c = sp.symbols('f c', real=True)
    j = JetSpace((t, x, y), (h, u, v, B), 2)
    Dt, Dx, Dy = (lambda e, i=i: j.D(e, i) for i in range(3))
    S = u**2 + v**2
    eqs = (Dt(h) + Dx(h*u) + Dy(h*v),
           Dt(u) + u*Dx(u) + v*Dy(u) + g*Dx(h + B) - f*v,
           Dt(v) + u*Dx(v) + v*Dy(v) + g*Dy(h + B) + f*u,
           Dt(B) + Dx(S*(K*u - G*Dx(B))) + Dy(S*(K*v - G*Dy(B))))
    spec = PDESpec('E2 planar', j, tuple(map(sp.expand, eqs)), tuple(j.jet(a, 1, 0, 0) for a in range(4)), (),
                   ('h>0', 'g,K,G>0'), positive=(h, g, K, G))
    R = (0, -y, x, 0, -v, u, 0)
    T = (1, 0, 0, 0, 0, 0, c)
    red = reduce_nd(spec, (R, T))
    if red.status != 'verified':
        return {'model': 'E2 planar', 'status': red.status, 'reason': red.reason, 'match': False}
    same = [sp.simplify(a - b) == 0 for a, b in zip(red.equations, polar_E2()['odes'])]
    return {'model': 'E2 planar Cartesian (t,x,y)', 'generators': 'rotation (-y d_x + x d_y - v d_u + u d_v), d_t + c d_B',
            'status': red.status, 'weight_kind': red.checks.get('weight_kind'), 'weights': red.weights,
            'ansatz': red.graph.lifts, 'base': red.graph.base, 'odes': red.equations,
            'equal_to_polar_quotient': same, 'match': all(same)}


LIBRARY = ('damping', 'power', 'drift')


def random_model(seed, space):
    rng = random.Random(seed)
    t = sp.Symbol('t', real=True)
    xs = sp.symbols(' '.join(f'x{i+1}' for i in range(space)), real=True)
    u = sp.Symbol('u', positive=True)
    j = JetSpace((t, *xs), (u,), 2)
    e = lambda i: tuple(int(k == i) for k in range(space + 1))
    ee = lambda i: tuple(2*int(k == i) for k in range(space + 1))
    nu = [rng.choice((1, 2, 3)) for _ in xs]
    adv = [rng.choice((0, 1, -1, 2)) for _ in xs]
    kind = LIBRARY[seed % len(LIBRARY)]
    mu = sp.Symbol('m' if kind == 'power' else 'mu', real=True)
    rhs = sum(n*j.jets[0, ee(i+1)] for i, n in enumerate(nu)) + u*sum(a*j.jets[0, e(i+1)] for i, a in enumerate(adv))
    if kind == 'damping':
        rhs += mu*u
    elif kind == 'power':
        rhs += rng.choice((1, -1, 2))*u**mu
    else:
        rhs += mu*xs[0]*j.jets[0, e(1)]
    eq = sp.expand(j.jets[0, e(0)] - rhs)
    spec = PDESpec(f'random{space+1}D#{seed}', j, (eq,), (j.jets[0, e(0)],), (mu,), ('u>0',), positive=(u,))
    return spec, mu, kind == 'power', str(eq) + ' = 0'


def _pool(basis, extra, coords, n):
    """Rank n-1 sets of affine fields and two-term combinations; sets using an extra generator first."""
    c = sp.Symbol('c', real=True)
    same = lambda X, Y: all(sp.expand(a - b) == 0 for a, b in zip(X, Y))
    fields = []
    for X in [*extra, *(X for X in basis if not any(same(X, Y) for Y in extra))]:
        try:
            affine(X, coords)
            fields.append((tuple(X), any(same(X, Y) for Y in extra)))
        except NotImplementedError:
            pass
    pool = fields + [(tuple(sp.expand(p + c*q) for p, q in zip(X, Y)), a or b)
                     for (X, a), (Y, b) in combinations(fields, 2)]
    sets = sorted(combinations(pool, n - 1), key=lambda S: not any(e for _, e in S))
    for S in sets:
        fields = [X for X, _ in S]
        if sp.Matrix([X[:n] for X in fields]).rank() == n - 1 and closed(fields, coords):
            yield S


def reduce_stratum(spec, basis, extra, attempts, seconds):
    j = spec.jets
    n = len(j.independent)
    coords = j.independent + j.dependent
    tried = []
    for S in islice(_pool(basis, extra, coords, n), attempts):
        stage = timed(lambda S=S: reduce_nd(spec, [X for X, _ in S]), seconds)
        red = stage['value']
        tried.append(red.status if red else stage['status'])
        if red is not None and red.status == 'verified':
            return {'subalgebra': [str(X) for X, _ in S], 'uses_extra': any(e for _, e in S),
                    'base': red.graph.base, 'ansatz': red.graph.lifts, 'ode': red.equations,
                    'weights': red.weights, 'tried': tried}
    return {'status': 'no verified quotient in the attempted subalgebras', 'tried': tried}


def random_suite(seeds, attempts=12, seconds=60):
    rows = []
    for seed in seeds:
        for space in (2, 3):
            spec, mu, exponent, text = random_model(seed, space)
            r = strata(spec, mu, 1, exponent=exponent)
            row = {'model': spec.name, 'pde': text, 'hidden_parameter': str(mu),
                   'generic_dimension': r['generic_kernel_dimension'],
                   'pivot_minor_factors': r['pivot_minor_factors'], 'resonances': r['resonances'], 'strata': []}
            for s in r['strata']:
                entry = {k: s[k] for k in ('value', 'kernel_dimension', 'jump', 'extra', 'source', 'status', 'reason') if k in s}
                if s.get('jump'):
                    entry['reduction'] = reduce_stratum(specialize(spec, {mu: s['value']}), s['basis'], s['extra'],
                                                        attempts, seconds)
                row['strata'].append(entry)
            generic_value = next(v for v in range(5, 50) if all(v != s['value'] for s in r['strata']))
            row['generic_reduction'] = reduce_stratum(specialize(spec, {mu: generic_value}),
                                                      symmetries(specialize(spec, {mu: generic_value}), 1)['basis'],
                                                      [], attempts, seconds)
            row['generic_reduction']['sample_value'] = generic_value
            rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--seeds', type=int, nargs='*', default=[0, 1, 2])
    args = parser.parse_args()
    report = {'manuscript_strata': manuscript_strata(), 'E2_polar': polar_E2(), 'E2_planar': planar_E2(),
              'random': random_suite(args.seeds)}
    jumps = [s for row in report['random'] for s in row['strata'] if s.get('jump')]
    report['summary'] = {
        'manuscript_strata_match': report['manuscript_strata']['match'],
        'E2_polar_match': report['E2_polar']['match'], 'E2_planar_verified': report['E2_planar']['match'],
        'random_models': len(report['random']), 'random_jump_strata': len(jumps),
        'jump_strata_reduced_with_extra_generator': sum(bool(s['reduction'].get('uses_extra')) for s in jumps),
        'generic_strata_reduced': sum('ode' in row['generic_reduction'] for row in report['random'])}
    print(json.dumps(serial(report), indent=2, default=str))
    s = report['summary']
    ok = (s['manuscript_strata_match'] and s['E2_polar_match'] and s['E2_planar_verified']
          and s['generic_strata_reduced'] == s['random_models']
          and s['jump_strata_reduced_with_extra_generator'] == s['random_jump_strata'])
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
