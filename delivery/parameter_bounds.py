"""Interval barrier certificates for every held-out candidate of parameter_experiments.py.

For each (tuple, stage, side, route) the certifier searches a tube |w - w_hat| <= e0 exp(beta s) and
returns the largest contiguous certified prefix s in [0, reach] with outward-rounded chart gates
H >= H_min > 0, S >= S_min > 0, |Delta_c/rho| >= d_min > 0 and strict barrier signs. Each side endpoint is
labelled boundary_reached, obstruction_numerical (DOP853 stopped at Delta_c -> 0 or H -> 0 and the
certificate stops before it) or certification_failed. Writes logs/planar_ml/bounds.json.
"""
import json
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np

from planar import bench as B
from planar import drift as DR
from planar.certify import bed_lipschitz, certify_side
from planar.ivl import I
from planar.model import Anchor

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'logs', 'planar_ml')
# obstruction_numerical requires the certificate to track the reference to within 10% of its extent
OBSTRUCTION_REACH = 0.9


def candidate(route, stage, side, t, srec):
    if route.startswith('chebyshev'):
        ch = srec['chebyshev']
        return B.chebyshev_candidate(ch['coeffs'], ch['domain'], side)
    kind, wt = B.load_weights(os.path.join(OUT, f'weights_{route}_{stage}.npz'))
    return B.as_candidate(kind, wt, t, stage)


def job(args):
    split, i, t, f, stage, side, route, branch, srec = args
    Mi = Anchor(I(t['m']), I(t['kappa']), I(t['gamma']), f)
    det, br = Mi.slopes()
    ell = br[0 if branch == '-' else 1][0]
    cand = candidate(route, stage, side, t, srec)
    smax = srec['smax']
    t0 = time.perf_counter()
    rec = certify_side(Mi, ell, cand, side, smax)
    secs = time.perf_counter() - t0
    reach = rec['reach']
    if reach >= smax*(1 - 1e-12):
        lab = 'boundary_reached'
    elif srec['reference']['label'] == 'obstruction_numerical' and reach >= OBSTRUCTION_REACH*srec['reference']['extent']:
        lab = 'obstruction_numerical'
    else:
        lab = 'certification_failed'
    LZ = bed_lipschitz(Mi, ell, cand, side, reach, rec['e0'], rec['beta'])
    emax = float((rec['e0']*(I.of(float(rec['beta']))*I.of(float(reach))).exp()).hi)
    return {'split': split, 'i': i, 'stage': stage, 'side': side, 'route': route, 'branch': branch, 'smax': smax,
            'reach': reach, 'label': lab, 'reference_extent': srec['reference']['extent'],
            'status': 'certified' if lab == 'boundary_reached' else 'failed',
            'certified_coverage': {'s': [0.0, reach], 'r': sorted([1.0, 1.0 + side*reach])},
            'e0': rec['e0'], 'beta': rec['beta'], 'H_error_bound': rec['H_error_bound'],
            'defect_bound_continuous': rec['defect'], 'H_min': rec['Hmin'], 'S_min': rec['Smin'], 'd_min': rec['dmin'],
            'L_Z': LZ, 'Z_error_bound': None if LZ is None else float((I.of(LZ)*emax*I.of(float(reach)).sqr()*0.5).hi),
            'det_enclosure': [float(det.lo), float(det.hi)], 'cells': rec.get('cells'), 'seconds': secs}


def build_jobs(exp):
    jobs = []
    for split in ('test', 'near_threshold'):
        for i, rec in enumerate(exp['bend'][split]):
            t = rec['equation_parameters']
            for stage in ('A', 'B'):
                sides = rec['stages'][stage]['sides']
                for side in (1, -1):
                    for branch in ('+', '-'):
                        srec = sides[f'{side:+d}{branch}']
                        routes = ['chebyshev'] + (['pinn', 'rf', 'gated'] if branch == '+' else [])
                        for route in routes:
                            jobs.append((split, i, t, B.F_BEND, stage, side, route, branch, srec))
    for i, rec in enumerate(exp['review_control']['tests']):
        t = rec['equation_parameters']
        for side in (1, -1):
            for branch in ('+', '-'):
                jobs.append(('review_control', i, t, 1.0, 'A', side, 'chebyshev', branch, rec['sides'][f'A{side:+d}{branch}']))
    return jobs


def summarize(results, exp):
    summary = {}
    for split in ('test', 'near_threshold', 'review_control'):
        rows = [r for r in results if r['split'] == split]
        for stage in ('A', 'B'):
            for route in ('chebyshev', 'pinn', 'rf', 'gated'):
                for branch in ('+', '-'):
                    sel = [r for r in rows if r['stage'] == stage and r['route'] == route and r['branch'] == branch]
                    if not sel:
                        continue
                    by_tuple = {}
                    for r in sel:
                        by_tuple.setdefault(r['i'], {})[r['side']] = r
                    full = [i for i, d in by_tuple.items() if all(d[s]['label'] == 'boundary_reached' for s in (1, -1))]
                    hb = [max(d[1]['H_error_bound'], d[-1]['H_error_bound']) for i, d in by_tuple.items() if i in full]
                    cov = [(d[1]['reach'] + d[-1]['reach'])/(d[1]['smax'] + d[-1]['smax']) for d in by_tuple.values()]
                    summary[f'{split}/{stage}/{route}/{branch}'] = {
                        'certified_full_slice': f'{len(full)}/{len(by_tuple)}',
                        'max_H_bound_full': max(hb) if hb else None,
                        'mean_coverage': float(np.mean(cov)), 'min_coverage': float(np.min(cov)),
                        'labels': sorted({f"{r['side']:+d}:{r['label']}" for r in sel}),
                        'median_cert_seconds': float(np.median([r['seconds'] for r in sel]))}
    return summary


def drift_bounds(exp):
    A = np.load(os.path.join(OUT, 'drift_readout.npy'))
    out = []
    for t in exp['drift']['tests']:
        p = t['equation_parameters']
        t0 = time.perf_counter()
        c = DR.certify(A, p['m'], p['U0'])
        c.update(equation_parameters=p, field_error_sampled=t['field_error_sampled'], seconds=time.perf_counter() - t0,
                 status='certified' if c['error_bound'] is not None and c['error_bound'] >= t['field_error_sampled'] else 'failed')
        out.append(c)
    return out


def main():
    with open(os.path.join(OUT, 'experiments.json')) as fh:
        exp = json.load(fh)
    t_all = time.perf_counter()
    jobs = build_jobs(exp)
    with ProcessPoolExecutor(max_workers=min(16, os.cpu_count() or 1)) as pool:
        results = list(pool.map(job, jobs, chunksize=1))
    drift = drift_bounds(exp)
    # sampled field error must lie inside the continuous bound wherever the slice is certified
    viol = []
    for r in results:
        if r['split'] == 'review_control':
            continue
        srec = exp['bend'][r['split']][r['i']]['stages'][r['stage']]
        sampled = srec['sides'][f"{r['side']:+d}{r['branch']}"]['chebyshev']['H_error_sampled'] if r['route'] == 'chebyshev' else None
        if sampled is not None and r['label'] == 'boundary_reached' and sampled > r['H_error_bound']*(1 + 1e-9) + 1e-14:
            viol.append((r['split'], r['i'], r['stage'], r['side'], r['route']))
    pairs = {}
    for r in results:
        if r['route'] in ('pinn', 'rf', 'gated'):
            pairs.setdefault((r['split'], r['i'], r['stage'], r['route']), {})[r['side']] = r
    for (split, i, stage, route), d in pairs.items():
        if all(d[s]['label'] == 'boundary_reached' for s in (1, -1)):
            sampled = exp['bend'][split][i]['stages'][stage]['routes'][route]['field_error_sampled']
            if sampled > max(d[1]['H_error_bound'], d[-1]['H_error_bound'])*(1 + 1e-9) + 1e-14:
                viol.append((split, i, stage, 'both', route))
    receipt = {'commit': exp['commit'], 'engine': 'outward-rounded float64 intervals (1 ulp arithmetic, 4 ulp elementary functions), centred Taylor-jet forms',
               'results': results, 'drift': drift, 'summary': summarize(results, exp),
               'sampled_inside_bound_violations': viol, 'seconds': time.perf_counter() - t_all}
    with open(os.path.join(OUT, 'bounds.json'), 'w') as fh:
        json.dump(receipt, fh, indent=1)
    print(json.dumps({'summary': receipt['summary'], 'drift_max_bound': max(d['error_bound'] for d in drift),
                      'drift_status': sorted({d['status'] for d in drift}), 'violations': viol,
                      'seconds': round(receipt['seconds'], 1)}, indent=1))
    sys.exit(1 if viol or any(d['status'] != 'certified' for d in drift) else 0)


if __name__ == '__main__':
    main()
