#!/usr/bin/env python3
"""Compatible material equation M: complete-JetSpace generators, scaling integral, and in-memory verifier."""
import json
import sympy as sp

from lie_reduce.algebra import span_equal
from lie_reduce.models import discover_and_enumerate, scalar_spec
from lie_reduce.reduce import reduce
from reproduce_sve2026 import u
from symbolic_sve2026 import classify, material_scaling


def _serialize_reduction(red):
    return {
        'model': red.model,
        'status': red.status,
        'invariant': str(red.graph.invariant) if red.graph else None,
        'reduced_equations': [str(e) + ' = 0' for e in red.reduced_equations],
        'integrated_ode': (str(red.integrated_ode) + ' = 0') if red.integrated_ode is not None else None,
        'preserved_parameters': [str(p) for p in red.preserved_parameters],
    }


def _polynomial_span(classification):
    rows = []
    for exponent, key in ((1, 'm'), (2, 'm'), (3, '3'), (4, 'm')):
        spec, basis, _ = discover_and_enumerate(scalar_spec('M', exponent), degree=1)
        coords = spec.jets.independent + spec.jets.dependent
        derived = [tuple(c.subs(u, coords[2]) for c in gen) for gen in classification['bases'][key]]
        equal = bool(span_equal(list(basis.values()), derived, coords))
        rows.append({'exponent': exponent, 'stratum': key, 'span_equal': equal, 'labels': list(basis)})
        if not equal:
            raise ArithmeticError('degree-1 labels do not span the smooth M basis')
    return rows


def written_verifier(raw_reductions, integral):
    reasons = []
    for name, red in raw_reductions.items():
        if red.status != 'verified' or not red.checks.get('on_shell'):
            reasons.append({'id': name, 'status': red.status})
    if 'V' not in integral.get('bindings', {}) or not integral.get('first_integral'):
        reasons.append('material first integral')
    return {
        'status': 'passed' if not reasons else 'failed',
        'reasons': reasons,
        'checker': 'in-memory complete-JetSpace pullback + variational first-integral verifier (lie_reduce)',
    }


def main():
    classification = classify('M')
    integral = material_scaling()

    m = sp.Symbol('m', real=True)
    spec_m, _, subs_m = discover_and_enumerate(scalar_spec('M', m), degree=1, exponent=m, max_combo_terms=3)
    scale_sub = next(s for s in subs_m if s['id'] == 'Y4')
    tilted_sub = next(s for s in subs_m if s['id'] == 'Y1 + alpha_1*Y2 + alpha_2*Y3')

    spec_3, _, subs_3 = discover_and_enumerate(scalar_spec('M', 3), degree=1)
    cubic_sub = next(s for s in subs_3 if s['id'] == 'Y5')

    raw_reductions = {
        'scaling_symbolic_m': reduce(spec_m, scale_sub['generators']),
        'tilted_traveling_symbolic_m': reduce(spec_m, tilted_sub['generators']),
        'cubic_m3': reduce(spec_3, cubic_sub['generators']),
    }
    verdict = written_verifier(raw_reductions, integral)
    report = {
        'model': 'M',
        'search_class': 'Unrestricted smooth point generators on complete JetSpace (phi_t,phi_s,g,kappa>0, real m>=1).',
        'chart': 'phi_t>0, phi_s>0, g,kappa>0',
        'derived': {
            'exceptional_exponents': [str(v) for v in classification['exceptional_exponents']],
            'smooth_to_affine_proved': classification['smooth_to_affine_proved'],
            'bases': {k: [list(map(str, g_vec)) for g_vec in b] for k, b in classification['bases'].items()},
        },
        'polynomial_labels_span_smooth_basis': _polynomial_span(classification),
        'material_scaling': integral,
        'reductions': {k: _serialize_reduction(v) for k, v in raw_reductions.items()},
        'written_verifier': verdict,
        'not_claimed': 'No continuation from the printed scalar P into M.',
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
