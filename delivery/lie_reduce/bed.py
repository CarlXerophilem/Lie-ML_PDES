"""PDE->ODE reducer for 1+1 shallow water with a user-supplied bed balance."""
import argparse
import json
import re
import sympy as sp

from . import serial, timed
from .algebra import canonical_basis_dict, enumerate_subalgebras
from .determining import symmetries
from .jets import JetSpace
from .reduce import reduce
from .spec import PDESpec


def bed_spec(flux=None, rhs=None):
    t, x, h, u, B = sp.symbols('t x h u B', real=True)
    g = sp.Symbol('g', positive=True)
    j = JetSpace((t, x), (h, u, B), 2)
    names = {
        't': t, 'x': x, 'h': h, 'u': u, 'B': B, 'g': g,
        'h_x': j.jet(0, 0, 1), 'u_x': j.jet(1, 0, 1), 'B_x': j.jet(2, 0, 1),
        'h_xx': j.jet(0, 0, 2), 'u_xx': j.jet(1, 0, 2), 'B_xx': j.jet(2, 0, 2),
        'D_x': lambda e: j.D(e, 1),
    }
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
    equations = (
        j.D(h, 0) + j.D(h * u, 1),
        j.D(u, 0) + u * j.D(u, 1) + g * j.D(h + B, 1),
        sp.expand(bed),
    )
    spec = PDESpec('E1[bed]', j, equations, tuple(j.jet(i, 1, 0) for i in range(3)),
                   (g, *params.values()), ('h,u>0', 'g>0', 'parameters>0'),
                   positive=(h, u, g, *params.values()))
    return spec, str(expr)


def _admitted(spec, field):
    shell, _ = spec.shell()
    return all(sp.simplify(spec.jets.act(eq, field).subs(shell, simultaneous=True)) == 0
               for eq in spec.equations)


def discover(spec):
    coords = spec.jets.independent + spec.jets.dependent
    try:
        found = symmetries(spec, 1)
        basis = canonical_basis_dict(found['basis'], coords, prefix='G')
        return basis, 'degree-1 polynomial determining kernel on complete JetSpace'
    except (ValueError, sp.PolynomialError) as exc:
        n = len(coords)
        unit = lambda i: tuple(sp.S.One if k == i else sp.S.Zero for k in range(n))
        trans = [unit(i) for i in range(n) if _admitted(spec, unit(i))]
        basis = canonical_basis_dict(trans, coords, prefix='G')
        return basis, f'coordinate translations verified on complete JetSpace ({exc})'


def run(flux=None, rhs=None, seconds=60):
    spec, law = bed_spec(flux, rhs)
    basis, search = discover(spec)
    coords = spec.jets.independent + spec.jets.dependent
    names = ('t', 'x', 'h', 'u', 'B')
    subalgebras = enumerate_subalgebras(basis, coords, len(spec.jets.independent), max_combo_terms=2)
    out = {
        'bed_balance': str(spec.equations[2]) + ' = 0',
        'law': law,
        'search_class': search,
        'preserved_parameters': [str(p) for p in spec.parameters],
        'generators': {k: ' + '.join(f'({v})*d_{n}' for v, n in zip(X, names) if v != 0)
                       for k, X in basis.items()},
        'reductions': [],
    }
    for sub in subalgebras:
        X = sub['generators'][0]
        stage = timed(lambda X=X: reduce(spec, X), seconds)
        result = stage['value']
        row = {'generator': sub['id'], 'status': result.status if result else stage['status']}
        if result is not None and result.status == 'verified':
            row.update(
                invariant=str(result.graph.invariant),
                ansatz={str(v): str(L) for v, L in zip(spec.jets.dependent, result.reconstructed_lifts or result.graph.lifts)},
                odes=[str(e) + ' = 0' for e in result.reduced_equations],
                first_integrals=[f"{fi['flux']} = {fi['constant']}" for fi in result.first_integrals],
                weights=[str(w) for w in result.weights],
            )
        else:
            row['reason'] = result.reason if result else stage['reason']
        out['reductions'].append(row)
    out['summary'] = {
        'ode_reductions': sum(r['status'] == 'verified' for r in out['reductions']),
        'candidates': len(out['reductions']),
    }
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--flux', help='q in B_t + D_x(q) = 0')
    group.add_argument('--rhs', help='R in B_t + R = 0; D_x(.) is the total x-derivative')
    parser.add_argument('--stage-seconds', type=int, default=60)
    args = parser.parse_args()
    print(json.dumps(serial(run(args.flux, args.rhs, args.stage_seconds)), indent=2))


if __name__ == '__main__':
    main()
