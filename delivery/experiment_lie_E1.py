#!/usr/bin/env python3
"""E1 experiment: complete-JetSpace smooth classification, combination quotients, and in-memory verifier."""
import json
import sympy as sp

from lie_reduce.models import discover_and_enumerate, euler_spec
from lie_reduce.reduce import reduce
from symbolic_sv2022 import run as smooth_run


def _serialize_reduction(red):
    return {
        'model': red.model,
        'status': red.status,
        'invariant': str(red.graph.invariant) if red.graph else None,
        'section': {str(k): str(v) for k, v in red.graph.section.items()} if red.graph else {},
        'equations': [str(e) + ' = 0' for e in red.equations],
        'reduced_equations': [str(e) + ' = 0' for e in red.reduced_equations],
        'first_integrals': [
            {'constant': str(fi['constant']), 'flux': str(fi['flux']), 'multiplier': str(fi['multiplier'])}
            for fi in red.first_integrals
        ],
        'eliminated': {str(k): str(v) for k, v in red.eliminated.items()},
        'preserved_parameters': [str(p) for p in red.preserved_parameters],
        'checks': {str(k): str(v) for k, v in red.checks.items()},
    }


def written_verifier(raw_reductions):
    reasons = []
    for name, red in raw_reductions.items():
        if red.status != 'verified' or not red.checks.get('on_shell'):
            reasons.append({'id': name, 'status': red.status})
    return {
        'status': 'passed' if not reasons else 'failed',
        'reasons': reasons,
        'checker': 'in-memory complete-JetSpace pullback + variational first-integral verifier (lie_reduce)',
    }


def main():
    bases = {}
    for exponent in (1, 2, 3, 4):
        _, basis, _ = discover_and_enumerate(euler_spec(exponent), degree=1)
        bases[str(exponent)] = {
            'search_class': 'polynomial point coefficients of degree <= 1 with symbolic (g, K)',
            'dimension': len(basis),
            'generators': {name: [str(c) for c in vec] for name, vec in basis.items()},
        }

    m = sp.Symbol('m', real=True)
    spec_m, _, subs_m = discover_and_enumerate(euler_spec(m), degree=1, exponent=m)
    bed_sub = next(s for s in subs_m if s['id'] == 'X1 + alpha_1*X3')

    spec_3, _, subs_3 = discover_and_enumerate(euler_spec(3), degree=1)
    scale_sub = next(s for s in subs_3 if s['id'] == 'X5')

    raw_reductions = {
        'bed_drift_symbolic_m': reduce(spec_m, bed_sub['generators']),
        'cubic_scaling_m3': reduce(spec_3, scale_sub['generators']),
    }
    verdict = written_verifier(raw_reductions)
    report = {
        'model': 'E1',
        'search_class': 'Unrestricted smooth point symmetries for all real m>=1 on complete JetSpace, with symbolic (g, K, m) preserved.',
        'chart': 'h,u,g,K>0',
        'smooth_classification': smooth_run(),
        'polynomial_bases': bases,
        'reductions': {k: _serialize_reduction(v) for k, v in raw_reductions.items()},
        'written_verifier': verdict,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
