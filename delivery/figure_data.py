"""pgfplots tables for the planar figures, read only from logs/planar_ml receipts and saved weights.

Writes draft/figures/planar/{branches_A,profile_B,coverage_B,errors_A,errors_B}.dat.
"""
import json
import os

import numpy as np

from planar import bench as B
from planar.ivl import I, Jet
from planar.model import Anchor

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'logs', 'planar_ml')
FIG = os.path.join(HERE, '..', 'draft', 'figures', 'planar')
ROUTES = ('chebyshev', 'pinn', 'rf', 'gated')


def load(name):
    with open(os.path.join(LOG, name)) as fh:
        return json.load(fh)


def write(name, header, rows):
    with open(os.path.join(FIG, name), 'w') as fh:
        fh.write(' '.join(header) + '\n')
        for r in rows:
            fh.write(' '.join('nan' if v is None else f'{v:.8g}' for v in r) + '\n')


def side_curve(grid, ell, side):
    s = np.asarray(grid['s'])
    rho = side*s
    return 1 + rho, 1 + rho*(ell + np.asarray(grid['w_ref']))


def bed(t, r, H):
    """Z with Z(1) = 0 from Z' = P_Z(r, H) by the trapezoid rule on the plotted samples (illustration only)."""
    M = Anchor(t['m'], t['kappa'], t['gamma'], B.F_BEND)
    PZ = M.parts(r, H)[3]
    Z = np.concatenate([[0.0], np.cumsum(0.5*(PZ[1:] + PZ[:-1])*np.diff(r))])
    return Z - np.interp(1.0, r, Z)


def sci(x, digits=3, up=True):
    """Scientific notation in math mode; bounds round upward, sampled values to nearest."""
    if x is None:
        return r'\text{--}'
    if x == 0:
        return '0'
    e = int(np.floor(np.log10(abs(x))))
    m = (np.ceil if up else np.round)(abs(x)/10**e*10**(digits - 1))/10**(digits - 1)
    if m >= 10:
        m, e = m/10, e + 1
    s = f'{m:.{digits - 1}f}'
    return s if e == 0 else rf'{s}\times10^{{{e}}}'


def numbers(exp, bnd, nbh, cont, iA, iB):
    """numbers.tex: one macro per quoted receipt number (bounds rounded upward)."""
    N = {}
    sm = bnd['summary']
    names = {'chebyshev': 'Cheb', 'pinn': 'Pinn', 'rf': 'Rf', 'gated': 'Gated'}
    for split, tag in (('test', ''), ('near_threshold', 'Near')):
        for stage in ('A', 'B'):
            for rt, nm in names.items():
                v = sm[f'{split}/{stage}/{rt}/+']
                N[f'Cert{tag}{stage}{nm}'] = v['certified_full_slice'].replace('/', '/')
                N[f'Bound{tag}{stage}{nm}'] = sci(v['max_H_bound_full'])
                N[f'Cov{tag}{stage}{nm}'] = f"{100*v['mean_coverage']:.0f}"
                N[f'CertSec{tag}{stage}{nm}'] = f"{v['median_cert_seconds']:.1f}"
            v = sm[f'{split}/{stage}/chebyshev/-']
            N[f'Cert{tag}{stage}ChebMinus'] = v['certified_full_slice']
            N[f'Cov{tag}{stage}ChebMinus'] = f"{100*v['mean_coverage']:.0f}"
    for stage in ('A', 'B'):
        for rt, nm in names.items():
            errs = [r['stages'][stage]['routes'][rt]['field_error_sampled'] for r in exp['bend']['test']] if rt != 'chebyshev' else \
                [max(r['stages'][stage]['sides'][f'{s:+d}+']['chebyshev']['H_error_sampled'] for s in (1, -1)) for r in exp['bend']['test']]
            N[f'Err{stage}{nm}'] = sci(max(errs), up=False)
        for rt, nm in names.items():
            if rt == 'chebyshev':
                continue
            tr = exp['training']['routes'][f'{rt}/{stage}']
            N[f'Train{stage}{nm}Sec'] = f"{tr['seconds']:.1f}"
            N[f'Train{stage}{nm}Rms'] = sci(tr['final_rms_loss_residual'])
            N[f'Train{stage}{nm}Params'] = str(tr['parameters'])
            N[f'Train{stage}Points'] = str(tr['points'])
    rv = sm['review_control/A/chebyshev/+'], sm['review_control/A/chebyshev/-']
    det = exp['review_control']['det_enclosure_box']
    N['ReviewDetLo'], N['ReviewDetHi'] = f'{det[0]:.3f}', f'{det[1]:.3f}'
    rc = [r for r in bnd['results'] if r['split'] == 'review_control' and r['side'] == -1]
    for br, nm in (('+', 'Plus'), ('-', 'Minus')):
        reach = [r['reach'] for r in rc if r['branch'] == br]
        ref = [r['reference_extent'] for r in rc if r['branch'] == br]
        N[f'ReviewIn{nm}Lo'], N[f'ReviewIn{nm}Hi'] = f'{min(reach):.4f}', f'{max(reach):.4f}'
        N[f'ReviewRef{nm}Lo'], N[f'ReviewRef{nm}Hi'] = f'{min(ref):.4f}', f'{max(ref):.4f}'
    out = [r for r in bnd['results'] if r['split'] == 'review_control' and r['side'] == 1]
    N['ReviewOutCert'] = f"{sum(r['label'] == 'boundary_reached' for r in out)}/{len(out)}"
    dr = bnd['drift']
    N['DriftCert'] = f"{sum(d['status'] == 'certified' for d in dr)}/{len(dr)}"
    N['DriftErr'] = sci(max(t['field_error_sampled'] for t in exp['drift']['tests']), up=False)
    N['DriftBound'] = sci(max(d['error_bound'] for d in dr))
    N['DriftFactorMax'] = f"{max(d['factor'] for d in dr):.2f}"
    N['DriftCrudeMax'] = f"{max(d['factor_xi_half'] for d in dr):.2f}"
    N['BowlResidual'] = sci(max(p['max_radial_momentum_residual'] for p in exp['bowl']['profiles'].values()))
    for rt, nm in (('gated', 'Gated'), ('chebyshev', 'Cheb')):
        for sc, v in nbh['summary'][rt]['per_scale'].items():
            tag = {'1': 'One', '0.3333': 'Third', '0.1': 'Tenth', '0.03333': 'Thirtieth'}[sc]
            N[f'Box{nm}{tag}'] = v['certified']
            N[f'BoxBound{nm}{tag}'] = sci(v['max_H_bound'])
    N['CrossPoints'] = str(nbh['crosscheck_points'])
    N['CrossViol'] = str(nbh['crosscheck_violations'])
    N['UlpMax'] = f"{max(u['max_ulp_error'] for u in nbh['ulp'].values()):.2f}"
    N['EllOver'] = f"{np.median([b['ell_enclosure_width']/b['ell_corner_range'] for b in nbh['boxes']]):.2f}"
    for stage in ('A', 'B'):
        s = cont['summary'][stage]
        N[f'Tol{stage}'] = sci(s['H_tolerance'], 1)
        N[f'ColdNfev{stage}'] = str(s['cold']['nfev_total'])
        N[f'ChebTol{stage}'] = s['chebyshev_accepted_tuples']
        N[f'ClassicalSec{stage}'] = f"{s['classical_seconds_per_tuple']:.2f}"
        for rt, nm in names.items():
            if rt == 'chebyshev':
                continue
            x = s[rt]
            N[f'WarmNfev{stage}{nm}'] = str(x['warm']['nfev_total'])
            N[f'WarmOk{stage}{nm}'] = x['warm']['success']
            N[f'OnlyTol{stage}{nm}'] = x['learned_only_certified_tuples']
            N[f'OnlySec{stage}{nm}'] = '--' if x['learned_only_seconds_per_tuple'] is None else f"{x['learned_only_seconds_per_tuple']:.2f}"
            be = x['break_even_queries_fix']
            N[f'BreakFix{stage}{nm}'] = be.replace('_', ' ') if isinstance(be, str) else f'{be:.0f}'
            be = x['break_even_queries_learned_only']
            N[f'BreakOnly{stage}{nm}'] = '--' if be is None else be.replace('_', ' ') if isinstance(be, str) else f'{be:.0f}'
        N[f'GainFixMax{stage}'] = f"{100*max(s[rt]['relative_gain_fix'] for rt in names if rt != 'chebyshev'):.1f}"
    N['GainMin'] = f"{100*cont['break_even_min_relative_gain']:.0f}"
    with open(os.path.join(FIG, 'numbers.tex'), 'w') as fh:
        fh.write('% Generated by delivery/figure_data.py from logs/planar_ml receipts; do not edit.\n')
        for k, v in N.items():
            fh.write(f'\\newcommand{{\\Num{k}}}{{{v}}}\n')


def main():
    os.makedirs(FIG, exist_ok=True)
    exp, bnd, grids = load('experiments.json'), load('bounds.json'), load('grids.json')
    cert = {(r['split'], r['i'], r['stage'], r['side'], r['route'], r['branch']): r for r in bnd['results']}
    # stage A: both branches for a tuple whose ell_- side stops at a second critical point
    iA = next(i for i, rec in enumerate(exp['bend']['test'])
              if rec['stages']['A']['sides']['-1-']['reference']['label'] == 'obstruction_numerical')
    rec, g = exp['bend']['test'][iA], grids['test'][iA]
    t = rec['equation_parameters']
    cols, rows = [], []
    for br, ell in (('+', t['ell']), ('-', t['ell_minus'])):
        r_in, H_in = side_curve(g[f'A-1{br}'], ell, -1)
        r_out, H_out = side_curve(g[f'A+1{br}'], ell, 1)
        r = np.concatenate([r_in[::-1], r_out[1:]])
        H = np.concatenate([H_in[::-1], H_out[1:]])
        cols.append((r[::4], H[::4]))
    n = max(len(c[0]) for c in cols)
    pad = lambda a: np.concatenate([a, np.full(n - len(a), np.nan)])
    write('branches_A.dat', ['r_plus', 'H_plus', 'r_minus', 'H_minus'],
          zip(pad(cols[0][0]), pad(cols[0][1]), pad(cols[1][0]), pad(cols[1][1])))
    # stage B: ell_+ profile, routes and certified coverage for the first held-out tuple certified by all of cheb and gated
    iB = next(i for i in range(len(exp['bend']['test']))
              if all(cert[('test', i, 'B', s, rt, '+')]['label'] == 'boundary_reached' for s in (1, -1) for rt in ('chebyshev', 'gated')))
    rec, g = exp['bend']['test'][iB], grids['test'][iB]
    t = rec['equation_parameters']
    r_in, H_in = side_curve(g['B-1+'], t['ell'], -1)
    r_out, H_out = side_curve(g['B+1+'], t['ell'], 1)
    r = np.concatenate([r_in[::-1], r_out[1:]])
    H = np.concatenate([H_in[::-1], H_out[1:]])
    Z = bed(t, r, H)
    preds = {}
    for route in ('pinn', 'rf', 'gated'):
        kind, wt = B.load_weights(os.path.join(LOG, f'weights_{route}_B.npz'))
        cand = B.as_candidate(kind, wt, t, 'B')
        rho = r - 1
        preds[route] = 1 + rho*(t['ell'] + cand(Jet([I(rho), 1.0]), 1).c[0].mid)
    k = slice(None, None, 5)
    write('profile_B.dat', ['r', 'H_ref', 'Z_ref', 'HZ_ref', 'H_pinn', 'H_rf', 'H_gated'],
          zip(r[k], H[k], Z[k], (H + Z)[k], preds['pinn'][k], preds['rf'][k], preds['gated'][k]))
    write('coverage_B.dat', ['route_index', 'r_lo', 'r_hi', 'H_bound'],
          [(j, 1 - cert[('test', iB, 'B', -1, rt, '+')]['reach'], 1 + cert[('test', iB, 'B', 1, rt, '+')]['reach'],
            max(cert[('test', iB, 'B', s, rt, '+')]['H_error_bound'] for s in (1, -1))) for j, rt in enumerate(ROUTES)])
    # sampled error and certified bound per held-out tuple
    for stage in ('A', 'B'):
        rows = []
        for i, rec in enumerate(exp['bend']['test']):
            row = [i, rec['equation_parameters']['delta']]
            for rt in ROUTES:
                if rt == 'chebyshev':
                    sampled = max(rec['stages'][stage]['sides'][f'{s:+d}+']['chebyshev']['H_error_sampled'] for s in (1, -1))
                else:
                    sampled = rec['stages'][stage]['routes'][rt]['field_error_sampled']
                cs = [cert[('test', i, stage, s, rt, '+')] for s in (1, -1)]
                bound = max(c['H_error_bound'] for c in cs) if all(c['label'] == 'boundary_reached' for c in cs) else None
                row += [max(sampled, 1e-16), bound]
            rows.append(row)
        write(f'errors_{stage}.dat', ['i', 'delta'] + [f'{rt}_{q}' for rt in ROUTES for q in ('sampled', 'bound')], rows)
    numbers(exp, bnd, load('neighborhoods.json'), load('continuation.json'), iA, iB)
    print(json.dumps({'branches_A_tuple': iA, 'profile_B_tuple': iB,
                      'params_A': exp['bend']['test'][iA]['equation_parameters'], 'params_B': t}, indent=1))


if __name__ == '__main__':
    main()
