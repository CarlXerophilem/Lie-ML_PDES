#!/usr/bin/env python3
"""Planar E2 and rotating exchange: complete-JetSpace discovery, combination enumeration, and 3-integral reduction."""

import _bootstrap  # historical standalone script path
import json

from symbolic_new_model2026 import discover_planar_e2, run as exchange_and_e2_run


def written_verifier(e2_red, bundle):
    reasons = []
    if e2_red.status != 'verified' or len(e2_red.reduced_equations) != 1 or len(e2_red.first_integrals) != 3:
        reasons.append({'id': 'E2_planar_rank2', 'status': e2_red.status})
    if bundle.get('swirl_residuals') != ['0', '0', '0', '0', '0']:
        reasons.append({'id': 'exchange_swirl', 'residuals': bundle.get('swirl_residuals')})
    if bundle.get('swirl_r_Qr') != '1/20':
        reasons.append('exchange throughput')
    return {
        'status': 'passed' if not reasons else 'failed',
        'reasons': reasons,
        'checker': 'in-memory complete-JetSpace prolongation + matrix-exponential orbit quotient + 3-integral eliminator',
    }


def main():
    e2_bundle = discover_planar_e2()
    e2_red = e2_bundle[3]
    bundle = exchange_and_e2_run(e2_bundle=e2_bundle)
    verdict = written_verifier(e2_red, bundle)
    report = {
        'models': ['E_exch', 'E2_planar'],
        'search_class': 'Complete-JetSpace degree-1 point algebra discovery and combination subalgebra enumeration with symbolic parameters preserved.',
        'exchange_chart': 'r>0 and swirl invariant family V=0, W=Omega*r, D_a=0',
        'planar_e2_chart': 'r>0, h>0, u^2+v^2>0, g,K,G>0',
        'bundle': bundle,
        'written_verifier': verdict,
        'not_claimed': 'E2 and the rotating-exchange tank are distinct balance systems.',
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
