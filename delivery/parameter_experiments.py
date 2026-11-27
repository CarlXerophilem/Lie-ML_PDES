"""Planar E2 benchmark: five routes on the f=0 river-bend crossing plus drift, bowl and f=1 review controls.

Writes logs/planar_ml/experiments.json, network weights and candidate coefficients. Every number here is
sampled (status local_only); continuous bounds come from parameter_bounds.py.
"""
import json
import os
import subprocess
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
import torch

from planar import bench as B
from planar import drift as DR
from planar.classical import collocate
from planar.ivl import I, Jet
from planar.model import Anchor, reference, reference_w

warnings.filterwarnings('ignore')
torch.set_num_threads(1)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'planar_ml')
GRID = 501


def commit():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    except Exception:
        return 'unknown'


def label(ref, smax):
    return 'boundary_reached' if ref['extent'] >= smax*(1 - 1e-12) else 'obstruction_numerical'


def side_job(args):
    """Reference and cold Chebyshev collocation for one (tuple, f, stage, side, branch)."""
    t, f, stage, side, b = args
    M = Anchor(t['m'], t['kappa'], t['gamma'], f)
    ell, lam, a = M.slopes()[1][b]
    smax = B.STAGES[stage]['sides'][side]
    t0 = time.perf_counter()
    ref = reference(M, ell, a, side, smax)
    t_ref = time.perf_counter() - t0
    dom = smax if ref['reason'] == 'boundary_reached' else 0.999*ref['extent']
    col = collocate(M, ell, side, dom, B.STAGES[stage]['cheb'][side])
    s = np.linspace(0.0, ref['extent'], GRID)
    w_ref = reference_w(ref, s)
    cand = B.chebyshev_candidate(col['coeffs'], dom, side)
    w_c = cand(Jet([I(side*s), 1.0]), 1).c[0].mid
    keep = s <= dom
    return {'stage': stage, 'side': side, 'branch': '-+'[b], 'ell': float(ell), 'a': float(a), 'smax': smax,
            'reference': {'extent': ref['extent'], 'reason': ref['reason'], 'label': label(ref, smax),
                          'seconds': t_ref, 's0': ref['s0'], 'nfev': int(ref['sol'].nfev), 'taylor_order': 16},
            'chebyshev': {'coeffs': col['coeffs'].tolist(), 'domain': dom, 'N': len(col['coeffs']),
                          'nfev': col['nfev'], 'seconds': col['seconds'], 'max_collocation_residual': col['max_residual'],
                          'H_error_sampled': float(np.max(s[keep]*np.abs(w_c[keep] - w_ref[keep])))},
            'grid': {'s': s.tolist(), 'w_ref': w_ref.tolist()}}


def with_branch(t, f=B.F_BEND):
    M, gamma, gs, det, br = B.tuple_model(t, f)
    out = dict(t)
    out.update(gamma=gamma, gamma_star=gs, det=det, ell=float(br[1][0]), ell_minus=float(br[0][0]),
               a_plus=float(br[1][2]), a_minus=float(br[0][2]), C3_over_G=float(M.C3g))
    return out


def run_sides(pool, tuples, f, stages, branches):
    jobs = [(t, f, st, side, b) for t in tuples for st in stages for side in (1, -1) for b in branches]
    res = list(pool.map(side_job, jobs, chunksize=1))
    out = [{} for _ in tuples]
    k = 0
    for i, t in enumerate(tuples):
        for st in stages:
            for side in (1, -1):
                for b in branches:
                    out[i][(st, side, '-+'[b])] = res[k]
                    k += 1
    return out


def net_sampled(net, t, stage, sides):
    """Sampled H error against the reference and sampled defect on the reference-reached part of each side."""
    st = B.STAGES[stage]
    err, dmax, secs = 0.0, 0.0, 0.0
    for side in (1, -1):
        r = sides[(stage, side, '+')]
        s = np.asarray(r['grid']['s'])
        t0 = time.perf_counter()
        w = B.predict(net, t, stage, side*s)
        secs += time.perf_counter() - t0
        err = max(err, float(np.max(s*np.abs(w - np.asarray(r['grid']['w_ref'])))))
        rho = torch.tensor(side*s[s >= 1e-3]).requires_grad_(True)
        nu = torch.tensor([B.nu_hat(t)]*len(rho))
        P = {'m': t['m'], 'kappa': t['kappa'], 'gamma': t['gamma'], 'ell': t['ell'], 'f': B.F_BEND}
        d = B.residuals(net, rho, nu, P, st, 'defect').detach().numpy()
        dmax = max(dmax, float(np.max(np.abs(d))))
    return err, dmax, secs


def bowl_check():
    """Closed-form bowl profiles through the numerical radial residuals (V = 0, W = -fr/2)."""
    f, g, G, c, E = 1.0, 1.0, 1.0, 0.1, 1.0
    r = np.linspace(0.2, 1.5, 261)
    out = {'f': f, 'g': g, 'G': G, 'c': c, 'E': E, 'Z_normalization': 'Z(1)=0', 'profiles': {}}
    for m in (1.0, 1.5, 2.0, 3.0):
        Zp = c*r**(2 - m)/(2*G*(f/2)**(m - 1))
        Z = (c/(2*G*(f/2)**(m - 1)))*(np.log(r) if m == 3 else (r**(3 - m) - 1)/(3 - m))
        H = E - Z - f**2*r**2/(8*g)
        Hp = -Zp - f**2*r/(4*g)
        W = -f*r/2
        radial = -W**2/r - f*W + g*(Hp + Zp)
        Q = np.abs(W)**(m - 1)*(-G*Zp)
        exner = c + np.gradient(r*Q, r, edge_order=2)/r
        out['profiles'][str(m)] = {
            'max_radial_momentum_residual': float(np.max(np.abs(radial))),
            'max_Q_plus_cr_over_2': float(np.max(np.abs(Q + c*r/2))),
            'max_exner_residual_fd': float(np.max(np.abs(exner))), 'H_min': float(H.min()),
            'r': r[::10].tolist(), 'Z': Z[::10].tolist(), 'H_plus_Z': (H + Z)[::10].tolist()}
    return out


def drift_control():
    tr, te = B.sample(DR.BOX, 30, B.SEED_TRAIN), B.sample(DR.BOX, 12, B.SEED_TEST)
    A, info = DR.fit(tr)
    x = np.linspace(0, 1, 1001)
    tests = []
    for p in te:
        t0 = time.perf_counter()
        Uh = DR.U_hat(A, p['m'], p['U0'], x)
        q = time.perf_counter() - t0
        tests.append({'equation_parameters': p, 'field_error_sampled': float(np.max(np.abs(Uh - DR.exact(p['m'], p['U0'], x)))),
                      'defect_sampled': float(np.max(np.abs(DR.defect(A, p['m'], p['U0'], x)))), 'query_seconds': q})
    np.save(os.path.join(OUT, 'drift_readout.npy'), A)
    return {'model': 'E1 uniform drift, exact U=(U0^m-x/2)^(1/m), kappa=1/2, alpha=1/4, g=C=1, E=2',
            'domain': 'x in [0,1], all t', 'box': DR.BOX, 'seed': {'train': B.SEED_TRAIN, 'test': B.SEED_TEST},
            'route': 'rf readout (6 Chebyshev x 15 features), integral defect loss', 'training': info,
            'tests': tests, 'status': 'local_only'}


def review_control(pool):
    """f=1 review box (m, K, G, c); normalized to (m, kappa=K/G, gamma=c/G)."""
    raw = B.sample(B.REVIEW_BOX, B.N_TEST, B.SEED_TEST)
    tuples = []
    for p in raw:
        M = Anchor(p['m'], p['K']/p['G'], p['c']/p['G'], 1.0)
        det, br = M.slopes()
        tuples.append({'m': p['m'], 'kappa': p['K']/p['G'], 'gamma': p['c']/p['G'], 'K': p['K'], 'G': p['G'], 'c': p['c'],
                       'det': float(det), 'C3_over_G': float(M.C3g)})
    sides = run_sides(pool, tuples, 1.0, ['A'], (0, 1))
    box = B.REVIEW_BOX
    # hull of interval determinants over 4^4 sub-boxes of (m, K, G, c)
    edges = {k: np.linspace(*box[k], 5) for k in ('m', 'K', 'G', 'c')}
    lo, hi = np.inf, -np.inf
    for a in range(4):
        for b in range(4):
            for g in range(4):
                for d in range(4):
                    m_, K_, G_, c_ = (I(edges[k][j], edges[k][j + 1]) for k, j in zip(('m', 'K', 'G', 'c'), (a, b, g, d)))
                    det_s = Anchor(m_, K_/G_, c_/G_, 1.0).slopes()[0]
                    lo, hi = min(lo, float(det_s.lo)), max(hi, float(det_s.hi))
    det_i = I(lo, hi)
    recs = []
    for t, sd in zip(tuples, sides):
        recs.append({'equation_parameters': t, 'sides': {f'{k[0]}{k[1]:+d}{k[2]}': {kk: v[kk] for kk in ('ell', 'a', 'smax', 'reference', 'chebyshev')}
                                                         for k, v in sd.items()}})
    return {'model': 'E2 planar, f=1 (review control)', 'box': box, 'det_enclosure_box': [float(det_i.lo), float(det_i.hi)],
            'tests': recs, 'status': 'local_only'}, sides


def main():
    os.makedirs(OUT, exist_ok=True)
    t_all = time.perf_counter()
    receipt = {'commit': commit(), 'design': {'box': B.BOX, 'near_box': B.NEAR_BOX, 'stages': {k: {kk: v[kk] for kk in ('r', 'sides', 'rc', 'rs', 'nodes', 'cheb')} for k, v in B.STAGES.items()},
                                              'seeds': {'train': B.SEED_TRAIN, 'test': B.SEED_TEST}, 'n_train': B.N_TRAIN, 'n_test': B.N_TEST,
                                              'routes': B.ROUTES, 'lbfgs_iterations': B.LBFGS_ITERS,
                                              'nu_hat': '((m-2.5)/1, (kappa-6)/4, (delta-2)/1)',
                                              'reduction_constants': 'g=C1=C2=1, anchor (r,H)=(1,1), C3/G fixed by the anchor',
                                              'stratum': 'generic: R and T_c admitted for every (m,K,G,f,g,c); rank-two orbits'}}
    receipt['bowl'] = bowl_check()
    receipt['drift'] = drift_control()
    train = [with_branch(t) for t in B.sample(B.BOX, B.N_TRAIN, B.SEED_TRAIN)]
    test = [with_branch(t) for t in B.sample(B.BOX, B.N_TEST, B.SEED_TEST)]
    near = [with_branch(t) for t in B.sample(B.NEAR_BOX, B.N_TEST, B.SEED_TEST)]
    with ProcessPoolExecutor(max_workers=min(16, os.cpu_count() or 1)) as pool:
        t0 = time.perf_counter()
        train_sides = run_sides(pool, train, B.F_BEND, ['A', 'B'], (1,))
        t_train_refs = time.perf_counter() - t0
        test_sides = run_sides(pool, test, B.F_BEND, ['A', 'B'], (0, 1))
        near_sides = run_sides(pool, near, B.F_BEND, ['A', 'B'], (0, 1))
        receipt['review_control'], review_sides = review_control(pool)
    nets, training = {}, {}
    for stage in ('A', 'B'):
        nodes = B.radial_nodes(stage)
        masks = []
        for sd in train_sides:
            ext = {side: sd[(stage, side, '+')]['reference']['extent'] for side in (1, -1)}
            masks.append(np.array([abs(x) <= 0.999*ext[1 if x > 0 else -1] for x in nodes]))
        for route in ('pinn', 'rf', 'gated'):
            net, info = B.train(route, stage, train, masks)
            info['masked_points_dropped'] = int(sum((~mk).sum() for mk in masks))
            nets[(route, stage)] = net
            training[f'{route}/{stage}'] = info
            B.save_weights(os.path.join(OUT, f'weights_{route}_{stage}.npz'), net.kind, net.export())
            # interval export reproduces the torch forward pass
            cand = B.as_candidate(net.kind, net.export(), test[0], stage)
            rho = np.linspace(-B.STAGES[stage]['sides'][-1], B.STAGES[stage]['sides'][1], 7)
            info['export_mismatch'] = float(np.max(np.abs(cand(Jet([I(rho), 1.0]), 1).c[0].mid - B.predict(net, test[0], stage, rho))))
    receipt['training'] = {'reference_seconds_training_tuples': t_train_refs, 'domain_oracle': 'training nodes beyond the DOP853 reach of each training tuple are dropped (no profile labels)', 'routes': training}

    def records(tuples, sides_list, split):
        recs = []
        for t, sd in zip(tuples, sides_list):
            rec = {'model': 'E2 planar, f=0 free-vortex bend', 'split': split, 'equation_parameters': t,
                   'stratum': receipt['design']['stratum'], 'trace': 'H(1)=1, H\'(1)=ell', 'seed': B.SEED_TEST,
                   'defect_bound_continuous': 'not_run', 'certified_coverage': 'not_run', 'status': 'local_only', 'stages': {}}
            for stage in ('A', 'B'):
                srec = {'domain': {'r': B.STAGES[stage]['r']}, 'sides': {}}
                for (st, side, br), v in sd.items():
                    if st == stage:
                        srec['sides'][f'{side:+d}{br}'] = {k: v[k] for k in ('ell', 'a', 'smax', 'reference', 'chebyshev')}
                srec['routes'] = {}
                for route in ('pinn', 'rf', 'gated'):
                    err, dmax, q = net_sampled(nets[(route, stage)], t, stage, sd)
                    srec['routes'][route] = {'branch': '+', 'field_error_sampled': err, 'reconstruction_residual': dmax, 'query_seconds': q}
                rec['stages'][stage] = srec
            recs.append(rec)
        return recs
    receipt['bend'] = {'test': records(test, test_sides, 'test'), 'near_threshold': records(near, near_sides, 'near_threshold'),
                       'train_reach': [{f'{st}{side:+d}': sd[(st, side, '+')]['reference']['label'] for st in ('A', 'B') for side in (1, -1)} for sd in train_sides]}
    receipt['seconds'] = time.perf_counter() - t_all
    with open(os.path.join(OUT, 'grids.json'), 'w') as fh:
        json.dump({'test': [{f'{k[0]}{k[1]:+d}{k[2]}': v['grid'] for k, v in sd.items()} for sd in test_sides],
                   'review': [{f'{k[0]}{k[1]:+d}{k[2]}': v['grid'] for k, v in sd.items()} for sd in review_sides]}, fh)
    with open(os.path.join(OUT, 'experiments.json'), 'w') as fh:
        json.dump(receipt, fh, indent=1)
    summary = {'seconds': round(receipt['seconds'], 1), 'training': {k: {kk: v[kk] for kk in ('final_rms_loss_residual', 'train_max_defect', 'seconds', 'export_mismatch')} for k, v in training.items()}}
    for stage in ('A', 'B'):
        for route in ('pinn', 'rf', 'gated'):
            errs = [r['stages'][stage]['routes'][route]['field_error_sampled'] for r in receipt['bend']['test']]
            summary[f'test {stage} {route} max H err'] = max(errs)
        summary[f'test {stage} chebyshev max H err'] = max(v['chebyshev']['H_error_sampled'] for r in receipt['bend']['test'] for v in r['stages'][stage]['sides'].values())
        summary[f'test {stage} labels'] = sorted({f"{k}:{v['reference']['label']}" for r in receipt['bend']['test'] for k, v in r['stages'][stage]['sides'].items()})
    print(json.dumps(summary, indent=1))
    ok = all(v['export_mismatch'] < 1e-12 for v in training.values()) and all(
        p['max_radial_momentum_residual'] < 1e-12 for p in receipt['bowl']['profiles'].values())
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
