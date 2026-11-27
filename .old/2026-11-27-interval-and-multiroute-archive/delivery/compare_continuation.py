"""Cold versus learned warm starts for Chebyshev collocation, and the total-cost break-even.

For every held-out bend tuple, stage and side (branch ell_+), the same collocation problem is solved from a
zero coefficient vector and from the projection of each network prediction. Every candidate is then certified
at the same declared tolerance |H - H_hat| <= H_TOL[stage] on the full slice (tube e = H_TOL/smax, beta = 0).
Per-query costs per tuple (both sides):
  classical      = cold collocation + tolerance certificate of the Chebyshev candidate
  learned+fix    = network query + projection + warm collocation + tolerance certificate of the Chebyshev candidate
  learned only   = network query + tolerance certificate of the network (only tuples it passes)
The break-even query count is training time / (classical - learned) when that difference exceeds 5% of the classical cost.
Writes logs/planar_ml/continuation.json; reads experiments.json.
"""
import json
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
import torch

from planar import bench as B
from planar.certify import certify_at_tolerance
from planar.classical import collocate, project
from planar.ivl import I
from planar.model import Anchor

warnings.filterwarnings('ignore')
torch.set_num_threads(1)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'planar_ml')
NETS = ('pinn', 'rf', 'gated')
H_TOL = {'A': 5e-3, 'B': 5e-2}


def solve(args):
    key, t, stage, side, dom, N, c0 = args
    M = Anchor(t['m'], t['kappa'], t['gamma'], B.F_BEND)
    ell = M.slopes()[1][1][0]
    col = collocate(M, ell, side, dom, N, None if c0 is None else np.asarray(c0))
    return key, {k: col[k] for k in ('nfev', 'seconds', 'success', 'max_residual')}, col['coeffs'].tolist()


def tol_job(args):
    key, t, stage, side, route, spec = args
    Mi = Anchor(I(t['m']), I(t['kappa']), I(t['gamma']), B.F_BEND)
    ell = Mi.slopes()[1][1][0]
    if route == 'chebyshev':
        cand = B.chebyshev_candidate(spec['coeffs'], spec['domain'], side)
    else:
        kind, wt = B.load_weights(os.path.join(OUT, f'weights_{route}_{stage}.npz'))
        cand = B.as_candidate(kind, wt, t, stage)
    t0 = time.perf_counter()
    st = certify_at_tolerance(Mi, ell, cand, side, B.STAGES[stage]['sides'][side], H_TOL[stage])
    st['seconds'] = time.perf_counter() - t0
    return key, st


MIN_RELATIVE_GAIN = 0.05


def break_even(T, gain, per_classical):
    """Training time over per-tuple saving; 'not_resolved' if |saving| is below MIN_RELATIVE_GAIN of the
    classical per-tuple wall time (timing noise with parallel certification workers), 'never' if it is a loss."""
    if abs(gain) < MIN_RELATIVE_GAIN*per_classical:
        return 'not_resolved'
    if gain < 0:
        return 'never'
    return T/gain


def main():
    with open(os.path.join(OUT, 'experiments.json')) as fh:
        exp = json.load(fh)
    nets = {}
    for route in NETS:
        for stage in ('A', 'B'):
            kind, wt = B.load_weights(os.path.join(OUT, f'weights_{route}_{stage}.npz'))
            net = B.make_net(route, stage)
            if kind == 'mlp':
                for lin, (W, b) in zip((net.l1, net.l2, net.l3), wt['layers']):
                    lin.weight.data, lin.bias.data = torch.tensor(W), torch.tensor(b)
            elif kind == 'rf':
                net.A.data, net.Wf, net.bf = torch.tensor(wt['A']), torch.tensor(wt['Wf']), torch.tensor(wt['bf'])
            else:
                net.inp.weight.data, net.inp.bias.data = torch.tensor(wt['A']), torch.tensor(wt['b'])
                net.W.data, net.d.data, net.Theta.data = torch.tensor(wt['W']), torch.tensor(wt['d']), torch.tensor(wt['Theta'])
            nets[(route, stage)] = net
    jobs, prep, query = [], {}, {}
    for i, rec in enumerate(exp['bend']['test']):
        t = rec['equation_parameters']
        for stage in ('A', 'B'):
            for side in (1, -1):
                ch = rec['stages'][stage]['sides'][f'{side:+d}+']['chebyshev']
                dom, N = ch['domain'], ch['N']
                jobs.append(((i, stage, side, 'cold'), t, stage, side, dom, N, None))
                for route in NETS:
                    t0 = time.perf_counter()
                    c0 = project(lambda s: B.predict(nets[(route, stage)], t, stage, side*s), dom, N)
                    prep[(i, stage, side, route)] = time.perf_counter() - t0
                    xs = 0.5*dom*(1 - np.cos((2*np.arange(4*N) + 1)*np.pi/(8*N)))
                    t0 = time.perf_counter()
                    B.predict(nets[(route, stage)], t, stage, side*xs)
                    query[(i, stage, side, route)] = time.perf_counter() - t0
                    jobs.append(((i, stage, side, route), t, stage, side, dom, N, c0.tolist()))
    with ProcessPoolExecutor(max_workers=min(16, os.cpu_count() or 1)) as pool:
        out = {k: (v, c) for k, v, c in pool.map(solve, jobs, chunksize=1)}
    tjobs = []
    for (i, stage, side, kind), (v, c) in out.items():
        t = exp['bend']['test'][i]['equation_parameters']
        if kind == 'cold':
            dom = exp['bend']['test'][i]['stages'][stage]['sides'][f'{side:+d}+']['chebyshev']['domain']
            tjobs.append(((i, stage, side, 'chebyshev'), t, stage, side, 'chebyshev', {'coeffs': c, 'domain': dom}))
        else:
            tjobs.append(((i, stage, side, kind), t, stage, side, kind, None))
    with ProcessPoolExecutor(max_workers=8) as pool:
        cert = dict(pool.map(tol_job, tjobs, chunksize=1))
    rows = []
    for (i, stage, side, kind), (v, c) in out.items():
        row = {'i': i, 'stage': stage, 'side': side, 'start': kind, **v}
        if kind != 'cold':
            row['query_and_projection_seconds'] = prep[(i, stage, side, kind)]
            row['query_seconds'] = query[(i, stage, side, kind)]
            row['max_coeff_difference_to_cold'] = float(np.max(np.abs(np.asarray(c) - np.asarray(out[(i, stage, side, 'cold')][1]))))
        rows.append(row)
    training = exp['training']['routes']
    summary = {}
    for stage in ('A', 'B'):
        sel = lambda k: [r for r in rows if r['stage'] == stage and r['start'] == k]
        cold = sel('cold')
        cheb_cert = [cert[(r['i'], stage, r['side'], 'chebyshev')]['seconds'] for r in cold]
        cheb_ok = [all(cert[(i, stage, s, 'chebyshev')]['accepted'] for s in (1, -1)) for i in sorted({r['i'] for r in cold})]
        per_classical = (sum(r['seconds'] for r in cold) + sum(cheb_cert))/len(cold)*2
        st = {'cold': {'nfev_total': sum(r['nfev'] for r in cold), 'seconds_total': sum(r['seconds'] for r in cold),
                       'success': f"{sum(r['success'] for r in cold)}/{len(cold)}"},
              'H_tolerance': H_TOL[stage], 'chebyshev_accepted_tuples': f'{sum(cheb_ok)}/{len(cheb_ok)}',
              'classical_seconds_per_tuple': per_classical, 'chebyshev_cert_seconds_total': sum(cheb_cert)}
        for route in NETS:
            w = sel(route)
            T = training[f'{route}/{stage}']['seconds']
            fix = (sum(r['seconds'] + r['query_and_projection_seconds'] for r in w) + sum(cheb_cert))/len(w)*2
            tuples = sorted({r['i'] for r in w})
            own = [all(cert[(i, stage, s, route)]['accepted'] for s in (1, -1)) for i in tuples]
            only = [sum(cert[(i, stage, s, route)]['seconds'] for s in (1, -1)) +
                    sum(r['query_seconds'] for r in w if r['i'] == i) for i in tuples]
            only_ok = [x for x, ok in zip(only, own) if ok]
            per_only = float(np.mean(only_ok)) if only_ok else None
            gain_fix = per_classical - fix
            gain_only = None if per_only is None else per_classical - per_only
            st[route] = {'warm': {'nfev_total': sum(r['nfev'] for r in w), 'seconds_total': sum(r['seconds'] for r in w),
                                  'success': f"{sum(r['success'] for r in w)}/{len(w)}",
                                  'max_coeff_difference_to_cold': max(r['max_coeff_difference_to_cold'] for r in w)},
                         'training_seconds': T, 'learned_fix_seconds_per_tuple': fix,
                         'learned_only_seconds_per_tuple': per_only, 'learned_only_certified_tuples': f'{sum(own)}/{len(own)}',
                         'relative_gain_fix': gain_fix/per_classical,
                         'relative_gain_learned_only': None if gain_only is None else gain_only/per_classical,
                         'break_even_queries_fix': break_even(T, gain_fix, per_classical),
                         'break_even_queries_learned_only': None if gain_only is None else break_even(T, gain_only, per_classical)}
        summary[stage] = st
    certs = [{'i': k[0], 'stage': k[1], 'side': k[2], 'route': k[3], **v} for k, v in cert.items()]
    receipt = {'commit': exp['commit'], 'H_tolerance': H_TOL, 'break_even_min_relative_gain': MIN_RELATIVE_GAIN, 'rows': rows, 'tolerance_certificates': certs, 'summary': summary,
               'note': 'seconds are single-process wall times on the recording machine (8 certification workers in parallel)'}
    with open(os.path.join(OUT, 'continuation.json'), 'w') as fh:
        json.dump(receipt, fh, indent=1)
    print(json.dumps(summary, indent=1))
    sys.exit(0)


if __name__ == '__main__':
    main()
