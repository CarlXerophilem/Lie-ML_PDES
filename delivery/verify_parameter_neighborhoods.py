"""Parameter-box certificates around held-out bend tuples, and an mpmath cross-check of the interval engine.

1. Boxes. For each held-out tuple (stage A, branch ell_+) the gated network with interval inputs nu_hat and
   the tuple's fixed Chebyshev candidate are certified for all (m, kappa, gamma) in a box around the tuple.
   gamma_* = 2^((m+1)/2) (kappa(m-2) - 2(m+1))/3 (f = 0) is enclosed in intervals, so delta = gamma_* - gamma
   and det J_* < 0 are enclosed over the whole box. A ladder of box scales is tried; the largest certified
   scale is recorded.
2. Engine. On sampled certified cells, 40-digit mpmath point values of the two barrier functions must lie
   inside the float64 enclosures, and numpy exp/log/tanh/sqrt must be within the 4-ulp padding of ivl.py.
Writes logs/planar_ml/neighborhoods.json.
"""
import json
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

os.environ.setdefault('OMP_NUM_THREADS', '1')
import mpmath as mp
import numpy as np

from planar import bench as B
from planar.certify import SideCertifier, certify_side
from planar.ivl import I
from planar.model import Anchor, cstar

warnings.filterwarnings('ignore')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'planar_ml')
BASE = {'m': 0.03, 'kappa': 0.12, 'gamma': 0.03}
SCALES = (1.0, 1/3, 1/10, 1/30)
mp.mp.dps = 40


def gamma_star_iv(m, kappa):
    return I.of(2.0).powr((m + 1.0)*0.5)*(kappa*(m - 2.0) - (m + 1.0)*2.0)/3.0


def box_job(args):
    i, t, route, srecs, scale = args
    h = {k: v*scale for k, v in BASE.items()}
    m, kap, gam = I(t['m'] - h['m'], t['m'] + h['m']), I(t['kappa'] - h['kappa'], t['kappa'] + h['kappa']), I(t['gamma'] - h['gamma'], t['gamma'] + h['gamma'])
    Mi = Anchor(m, kap, gam, B.F_BEND)
    det, br = Mi.slopes()
    ell = br[1][0]
    delta = gamma_star_iv(m, kap) - gam
    nu = [m - 2.5, (kap - 6.0)*0.25, delta - 2.0]
    corners = [Anchor(a, b, c, B.F_BEND).slopes()[1][1][0] for a in (m.lo, m.hi) for b in (kap.lo, kap.hi) for c in (gam.lo, gam.hi)]
    out = {'i': i, 'route': route, 'scale': scale, 'halfwidths': h, 'det_enclosure': [float(det.lo), float(det.hi)],
           'ell_enclosure_width': float(ell.hi - ell.lo), 'ell_corner_range': float(max(corners) - min(corners)),
           'delta_enclosure': [float(delta.lo), float(delta.hi)], 'sides': {}}
    if not det.hi < 0:
        out['status'] = 'failed'
        out['reason'] = 'det enclosure not negative'
        return out
    t0 = time.perf_counter()
    for side in (1, -1):
        srec = srecs[side]
        if route == 'gated':
            kind, wt = B.load_weights(os.path.join(OUT, 'weights_gated_A.npz'))
            cand = B.as_candidate(kind, wt, t, 'A', nu)
        else:
            cand = B.chebyshev_candidate(srec['chebyshev']['coeffs'], srec['chebyshev']['domain'], side)
        rec = certify_side(Mi, ell, cand, side, srec['smax'])
        out['sides'][side] = {k: rec[k] for k in ('reach', 'e0', 'beta', 'H_error_bound', 'defect', 'Hmin', 'Smin', 'dmin')}
    out['seconds'] = time.perf_counter() - t0
    full = all(out['sides'][s]['reach'] >= srecs[s]['smax']*(1 - 1e-12) for s in (1, -1))
    out['status'] = 'certified' if full else 'failed'
    out['H_error_bound'] = max(out['sides'][s]['H_error_bound'] for s in (1, -1)) if full else None
    return out


# ---------------------------------------------------------------- mpmath cross-check
def mp_net(kind, wt, t, stage):
    st = B.STAGES[stage]
    nu = [mp.mpf(v) for v in B.nu_hat(t)]

    def lin(W, b, x):
        return [sum(mp.mpf(float(W[r, c]))*x[c] for c in range(len(x))) + (mp.mpf(float(b[r])) if b is not None else 0) for r in range(W.shape[0])]

    def R(rh):
        x = [rh] + nu
        if kind == 'mlp':
            h = x
            for W, b in wt['layers'][:-1]:
                h = [mp.tanh(v) for v in lin(W, b, h)]
            W, b = wt['layers'][-1]
            return lin(W, b, h)[0]
        if kind == 'gated':
            v0 = [mp.tanh(v) for v in lin(wt['A'], wt['b'], x)]
            u = [mp.tanh(v) for v in lin(wt['W'], None, v0)]
            v1 = [v0[k] + mp.tanh(mp.mpf(float(wt['d'][k])))*u[k] for k in range(len(v0))]
            nu1 = [mp.mpf(1)] + nu
            coef = [sum(nu1[k]*mp.mpf(float(wt['Theta'][k, i])) for k in range(len(nu1))) for i in range(len(v1))]
            return sum(v1[k]*coef[k] for k in range(len(v1)))
        raise ValueError(kind)
    return lambda rho: rho*R((rho - st['rc'])/st['rs'])


def mp_cheb(coeffs, dom, side):
    c = [mp.mpf(float(v)) for v in coeffs]

    def w(rho):
        s = rho*side
        x = s*2/mp.mpf(dom) - 1
        b1 = b2 = mp.mpf(0)
        for ck in c[:0:-1]:
            b1, b2 = 2*x*b1 - b2 + ck, b1
        return s*(x*b1 - b2 + c[0])
    return w


def mp_ell(t, f):
    M = Anchor(mp.mpf(t['m']), mp.mpf(t['kappa']), mp.mpf(t['gamma']), mp.mpf(f))
    Dr = mp.diff(lambda r: M.DN(r, mp.mpf(1))[0], 1)
    DH = mp.diff(lambda H: M.DN(mp.mpf(1), H)[0], 1)
    Nr = mp.diff(lambda r: M.DN(r, mp.mpf(1))[1], 1)
    NH = mp.diff(lambda H: M.DN(mp.mpf(1), H)[1], 1)
    p = Dr - NH
    return M, (-p + mp.sqrt(p*p + 4*DH*Nr))/(2*DH)


def crosscheck_job(args):
    i, t, route, side, srec, cert_rec, nsamp = args
    Mi = Anchor(I(t['m']), I(t['kappa']), I(t['gamma']), B.F_BEND)
    ell_i = Mi.slopes()[1][1][0]
    if route == 'chebyshev':
        cand = B.chebyshev_candidate(srec['chebyshev']['coeffs'], srec['chebyshev']['domain'], side)
        wmp = mp_cheb(srec['chebyshev']['coeffs'], srec['chebyshev']['domain'], side)
    else:
        kind, wt = B.load_weights(os.path.join(OUT, f'weights_{route}_A.npz'))
        cand = B.as_candidate(kind, wt, t, 'A')
        wmp = mp_net(kind, wt, t, 'A')
    cert = SideCertifier(Mi, ell_i, cand, side, srec['smax'])
    e0, beta = cert_rec['e0'], cert_rec['beta']
    edges = cert.edges_for(e0)
    res = cert.check(edges[:-1], edges[1:], e0, beta)
    good = np.nonzero(res['ok'])[0]
    rng = np.random.default_rng(1000 + i)
    pick = rng.choice(good, size=min(nsamp, len(good)), replace=False) if len(good) else []
    Mmp, ell = mp_ell(t, B.F_BEND)
    bad, checked, margin = [], 0, mp.inf
    for k in pick:
        for u in (0.1, 0.5, 0.9):
            s = mp.mpf(edges[k]) + u*(mp.mpf(edges[k + 1]) - mp.mpf(edges[k]))
            rho = side*s
            w = wmp(rho)
            dw = mp.diff(wmp, rho)
            e = e0*mp.exp(beta*s)
            up = Mmp.frak_undivided(rho, w + e, ell) - rho*dw - beta*s*e
            lo = Mmp.frak_undivided(rho, w - e, ell) - rho*dw + beta*s*e
            checked += 1
            margin = min(margin, res['up_hi'][k] - up, lo - res['lo_lo'][k])
            if not (up <= res['up_hi'][k] and lo >= res['lo_lo'][k] and up < 0 and lo > 0):
                bad.append([float(s), float(up), float(res['up_hi'][k]), float(lo), float(res['lo_lo'][k])])
    return {'i': i, 'route': route, 'side': side, 'e0': e0, 'beta': beta, 'cells_total': int(len(edges) - 1),
            'cells_passing_unrefined': int(len(good)), 'points_checked': checked, 'violations': bad,
            'min_enclosure_margin': float(margin)}


def ulp_check(n=20000, seed=7):
    rng = np.random.default_rng(seed)
    tests = {'exp': (np.exp, mp.exp, rng.uniform(-30, 30, n)), 'log': (np.log, mp.log, np.exp(rng.uniform(-30, 30, n))),
             'tanh': (np.tanh, mp.tanh, rng.uniform(-20, 20, n)), 'sqrt': (np.sqrt, mp.sqrt, np.exp(rng.uniform(-30, 30, n)))}
    out = {}
    for name, (fn, fm, x) in tests.items():
        y = fn(x)
        err = max(float(abs(mp.mpf(float(yy)) - fm(mp.mpf(float(xx))))/np.spacing(abs(yy))) for xx, yy in zip(x, y) if yy != 0)
        out[name] = {'max_ulp_error': err, 'points': n, 'within_padding_4': err <= 4}
    return out


def main():
    with open(os.path.join(OUT, 'experiments.json')) as fh:
        exp = json.load(fh)
    with open(os.path.join(OUT, 'bounds.json')) as fh:
        bounds = json.load(fh)
    t_all = time.perf_counter()
    tests = exp['bend']['test']
    for t in tests:
        p = t['equation_parameters']
        g = float((gamma_star_iv(I(p['m']), I(p['kappa']))).mid)
        assert abs(g - cstar(p['m'], p['kappa'], 0.0)) < 1e-9, 'closed-form gamma_* disagrees with the determinant root'
    jobs = []
    for i, rec in enumerate(tests):
        srecs = {side: rec['stages']['A']['sides'][f'{side:+d}+'] for side in (1, -1)}
        for route in ('gated', 'chebyshev'):
            for sc in SCALES:
                jobs.append((i, rec['equation_parameters'], route, srecs, sc))
    cert_lookup = {(r['i'], r['route'], r['side']): r for r in bounds['results']
                   if r['split'] == 'test' and r['stage'] == 'A' and r['branch'] == '+'}
    cjobs = []
    for i in range(3):
        rec = tests[i]
        for route in ('chebyshev', 'gated', 'pinn'):
            for side in (1, -1):
                cr = cert_lookup[(i, route, side)]
                if cr['label'] == 'boundary_reached':
                    cjobs.append((i, rec['equation_parameters'], route, side, rec['stages']['A']['sides'][f'{side:+d}+'], cr, 12))
    with ProcessPoolExecutor(max_workers=min(16, os.cpu_count() or 1)) as pool:
        boxes = list(pool.map(box_job, jobs, chunksize=1))
        cross = list(pool.map(crosscheck_job, cjobs, chunksize=1))
    largest = {}
    for b in boxes:
        key = f"{b['i']}/{b['route']}"
        if b['status'] == 'certified' and (key not in largest or b['scale'] > largest[key]['scale']):
            largest[key] = {'scale': b['scale'], 'halfwidths': b['halfwidths'], 'H_error_bound': b['H_error_bound'],
                            'det_enclosure': b['det_enclosure'], 'delta_enclosure': b['delta_enclosure']}
    ulps = ulp_check()
    summary = {}
    for route in ('gated', 'chebyshev'):
        per_scale = {}
        for sc in SCALES:
            sel = [b for b in boxes if b['route'] == route and b['scale'] == sc]
            ok = [b for b in sel if b['status'] == 'certified']
            per_scale[f'{sc:.4g}'] = {'halfwidths': {k: v*sc for k, v in BASE.items()}, 'certified': f'{len(ok)}/{len(sel)}',
                                      'max_H_bound': max([b['H_error_bound'] for b in ok], default=None)}
        summary[route] = {'tuples_with_certified_box': sum(1 for i in range(len(tests)) if f'{i}/{route}' in largest),
                          'per_scale': per_scale}
    viol = sum(len(c['violations']) for c in cross)
    receipt = {'commit': exp['commit'], 'base_halfwidths': BASE, 'scales': SCALES, 'boxes': boxes, 'largest': largest,
               'summary': summary, 'crosscheck': cross, 'crosscheck_points': sum(c['points_checked'] for c in cross),
               'crosscheck_violations': viol, 'ulp': ulps, 'mp_dps': mp.mp.dps, 'seconds': time.perf_counter() - t_all}
    with open(os.path.join(OUT, 'neighborhoods.json'), 'w') as fh:
        json.dump(receipt, fh, indent=1)
    print(json.dumps({'summary': summary, 'crosscheck_points': receipt['crosscheck_points'], 'crosscheck_violations': viol,
                      'ulp': ulps, 'seconds': round(receipt['seconds'], 1)}, indent=1))
    sys.exit(1 if viol or not all(u['within_padding_4'] for u in ulps.values()) else 0)


if __name__ == '__main__':
    main()
