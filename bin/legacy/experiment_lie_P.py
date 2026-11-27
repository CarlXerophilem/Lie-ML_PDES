#!/usr/bin/env python3
"""Printed scalar P: complete-JetSpace generators, paper-list span check, and in-memory verifier."""

import _bootstrap  # historical standalone script path
import json
import sympy as sp

from lie_reduce.algebra import span_equal
from lie_reduce.models import discover_and_enumerate, scalar_spec
from lie_reduce.reduce import reduce
from reproduce_sve2026 import generators, s, t, u
from symbolic_sve2026 import classify


def _serialize_reduction(red):
    return {
        'model': red.model,
        'status': red.status,
        'reason': red.reason,
        'invariant': str(red.graph.invariant) if red.graph else None,
        'reduced_equations': [str(e) + ' = 0' for e in red.reduced_equations],
        'integrated_ode': (str(red.integrated_ode) + ' = 0') if red.integrated_ode is not None else None,
        'preserved_parameters': [str(p) for p in red.preserved_parameters],
    }


def _paper_span(classification):
    listed = generators()
    coords = (t, s, u)
    groups = {
        'm': ('X1', 'X2', 'X3', 'X4'),
        '1': ('X1', 'X2', 'X3', 'X4', 'X6'),
        '3': ('X1', 'X2', 'X3', 'X4', 'X5'),
    }
    rows = []
    for key, names in groups.items():
        equal = bool(span_equal(classification['bases'][key], [listed[name] for name in names], coords))
        rows.append({'stratum': key, 'printed_names': list(names), 'span_equal': equal})
        if not equal:
            raise ArithmeticError('printed P list does not span the derived basis at ' + key)
    return rows


def _polynomial_span(classification):
    rows = []
    for exponent, key in ((1, '1'), (2, 'm'), (3, '3'), (4, 'm')):
        spec, basis, _ = discover_and_enumerate(scalar_spec('P', exponent), degree=1)
        coords = spec.jets.independent + spec.jets.dependent
        derived = [tuple(c.subs(u, coords[2]) for c in gen) for gen in classification['bases'][key]]
        equal = bool(span_equal(list(basis.values()), derived, coords))
        rows.append({'exponent': exponent, 'stratum': key, 'span_equal': equal, 'labels': list(basis)})
        if not equal:
            raise ArithmeticError('degree-1 labels do not span the smooth P basis')
    return rows


def written_verifier(raw_reductions):
    reasons = []
    for name in ('scaling_symbolic_m', 'cubic_m3'):
        red = raw_reductions[name]
        if red.status != 'verified' or not red.checks.get('on_shell'):
            reasons.append({'id': name, 'status': red.status})
    if raw_reductions['vertical_time_shift_m1'].status != 'no invariant graph':
        reasons.append({'id': 'vertical_time_shift_m1', 'status': raw_reductions['vertical_time_shift_m1'].status})
    return {
        'status': 'passed' if not reasons else 'failed',
        'reasons': reasons,
        'checker': 'in-memory complete-JetSpace pullback + variational first-integral verifier (lie_reduce)',
    }


def main():
    classification = classify('P')
    m = sp.Symbol('m', real=True)
    spec_m, _, subs_m = discover_and_enumerate(scalar_spec('P', m), degree=1, exponent=m)
    scale_sub = next(sub for sub in subs_m if sub['id'] == 'Y4')

    spec_3, _, subs_3 = discover_and_enumerate(scalar_spec('P', 3), degree=1)
    cubic_sub = next(sub for sub in subs_3 if sub['id'] == 'Y5')

    spec_1, basis_1, _ = discover_and_enumerate(scalar_spec('P', 1), degree=1)
    # Vertical generator t * d_phi is rejected from projectable base quotients
    vert_gen = next(vec for vec in basis_1.values() if vec[0] == 0 and vec[1] == 0 and vec[2] != 1)

    raw_reductions = {
        'scaling_symbolic_m': reduce(spec_m, scale_sub['generators']),
        'cubic_m3': reduce(spec_3, cubic_sub['generators']),
        'vertical_time_shift_m1': reduce(spec_1, (vert_gen,)),
    }
    verdict = written_verifier(raw_reductions)
    report = {
        'model': 'P',
        'search_class': 'Unrestricted smooth point generators on complete JetSpace (phi_t,phi_s,g,kappa>0, real m>=1).',
        'chart': 'phi_t>0, phi_s>0, g,kappa>0',
        'derived': {
            'exceptional_exponents': [str(v) for v in classification['exceptional_exponents']],
            'smooth_to_affine_proved': classification['smooth_to_affine_proved'],
            'bases': {k: [list(map(str, g_vec)) for g_vec in b] for k, b in classification['bases'].items()},
        },
        'printed_list_spans_derived_basis': _paper_span(classification),
        'polynomial_labels_span_smooth_basis': _polynomial_span(classification),
        'reductions': {k: _serialize_reduction(v) for k, v in raw_reductions.items()},
        'written_verifier': verdict,
        'not_claimed': 'No continuation from P to the compatible material equation M.',
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
