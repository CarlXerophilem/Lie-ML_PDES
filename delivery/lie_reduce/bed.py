"""PDE->ODE reducer for 1+1 shallow water with a user-supplied bed balance.

    python -m lie_reduce.bed --flux "kappa*u**3"            # B_t + D_x(q) = 0
    python -m lie_reduce.bed --flux "Q(u)"                  # arbitrary C^2 flux
    python -m lie_reduce.bed --rhs "D_x(u**2 - G*B_x)"      # B_t + R = 0

Water balances are those of E1. Generators are found in the degree-1 polynomial
class when the on-shell residual is polynomial in the free jets; otherwise the
search falls back to the translations, which are then tested individually.
Each one-dimensional candidate is reduced on an automatic section and the
pullback is checked by lie_reduce.reduce.
"""
import argparse
import itertools
import json
import re
import sympy as sp
from .jets import JetSpace
from .spec import PDESpec
from .reduce import reduce
from .run import serial, timed


def bed_spec(flux=None, rhs=None):
    t, x, h, u, B = sp.symbols('t x h u B', real=True)
    g = sp.Symbol('g', positive=True)
    j = JetSpace((t, x), (h, u, B), 2)
    names = {'t': t, 'x': x, 'h': h, 'u': u, 'B': B, 'g': g,
             'h_x': j.jet(0, 0, 1), 'u_x': j.jet(1, 0, 1), 'B_x': j.jet(2, 0, 1),
             'h_xx': j.jet(0, 0, 2), 'u_xx': j.jet(1, 0, 2), 'B_xx': j.jet(2, 0, 2),
             'D_x': lambda e: j.D(e, 1)}
    text = flux if flux is not None else rhs
    for name in re.findall(r'\b([A-Za-z]\w*)\s*\(', text):
        if name not in names and not hasattr(sp, name):
            names[name] = sp.Function(name)
    names.setdefault('Q', sp.Function('Q'))
    expr = sp.sympify(text, locals=names)
    reserved = set(names.values()) | set(j.jets.values())
    params = {v: sp.Symbol(v.name, positive=True) for v in expr.free_symbols - reserved}
    expr = expr.xreplace(params)
    bed = j.jet(2, 1, 0) + (j.D(expr, 1) if flux is not None else expr)
    if bed.has(j.jet(0, 1, 0), j.jet(1, 1, 0)):
        raise ValueError('bed balance may not contain h_t or u_t; eliminate them with the water balances first')
    equations = (j.D(h, 0) + j.D(h*u, 1),
                 j.D(u, 0) + u*j.D(u, 1) + g*j.D(h + B, 1),
                 sp.expand(bed))
    spec = PDESpec('E1[bed]', j, equations, tuple(j.jet(i, 1, 0) for i in range(3)),
                   tuple(params.values()), ('h,u>0', 'g>0', 'parameters>0'),
                   positive=(h, u, g, *params.values()))
    return spec, str(expr)


def translations(spec):
    n = len(spec.jets.independent) + len(spec.jets.dependent)
    unit = lambda i: tuple(sp.S.One if k == i else sp.S.Zero for k in range(n))
    return {'d_t': unit(0), 'd_x': unit(1), 'd_B': unit(4)}


def admitted(spec, field):
    shell, _ = spec.shell()
    return all(sp.simplify(spec.jets.act(eq, field).subs(shell, simultaneous=True)) == 0
               for eq in spec.equations)


def discover(spec):
    from .determining import symmetries
    try:
        found = symmetries(spec, 1)
        basis = {f'G{i+1}': X for i, X in enumerate(found['basis'])}
        return basis, 'degree-1 polynomial determining kernel (complete in that class)'
    except ValueError as exc:
        basis = {k: X for k, X in translations(spec).items() if admitted(spec, X)}
        return basis, f'translations only ({exc}); larger algebras for special laws are not searched'


def candidates(basis):
    c = sp.Symbol('c', real=True)
    rows = [(name, X) for name, X in basis.items()]
    for (a, X), (b, Y) in itertools.combinations(basis.items(), 2):
        rows.append((f'{a}+c*{b}', tuple(sp.expand(p + c*q) for p, q in zip(X, Y))))
    return rows


def run(flux=None, rhs=None, seconds=60):
    spec, law = bed_spec(flux, rhs)
    basis, search = discover(spec)
    names = ('t', 'x', 'h', 'u', 'B')
    out = {'bed_balance': str(spec.equations[2]) + ' = 0', 'law': law, 'search_class': search,
           'generators': {k: ' + '.join(f'({v})*d_{n}' for v, n in zip(X, names) if v != 0) for k, X in basis.items()},
           'reductions': []}
    for label, X in candidates(basis):
        stage = timed(lambda: reduce(spec, X), seconds)
        result = stage['value']
        row = {'generator': label, 'status': result.status if result else stage['status']}
        if result is not None and result.status == 'verified':
            row.update(invariant=str(result.graph.invariant),
                       ansatz={str(v): str(L) for v, L in zip(spec.jets.dependent, result.graph.lifts)},
                       odes=[str(e) + ' = 0' for e in result.equations],
                       weights=[str(w) for w in result.weights])
        else:
            row['reason'] = result.reason if result else stage['reason']
        out['reductions'].append(row)
    out['summary'] = {'ode_reductions': sum(r['status'] == 'verified' for r in out['reductions']),
                      'candidates': len(out['reductions'])}
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--flux', help='q in B_t + D_x(q) = 0; may use h,u,B,h_x,u_x,B_x, parameters, undefined Q(.)')
    group.add_argument('--rhs', help='R in B_t + R = 0; D_x(.) is the total x-derivative')
    parser.add_argument('--stage-seconds', type=int, default=60)
    args = parser.parse_args()
    print(json.dumps(serial(run(args.flux, args.rhs, args.stage_seconds)), indent=2))


if __name__ == '__main__':
    main()
