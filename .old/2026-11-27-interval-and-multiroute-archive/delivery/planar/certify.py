"""Interval barrier certificates for the desingularized crossing equation s dw/ds = frak(side*s, w).

Tube |w - w_hat| <= e(s) = e0 exp(beta s). The tube is invariant on a cell when
    frak(rho, w_hat + e) - rho w_hat' - beta s e < 0   and   frak(rho, w_hat - e) - rho w_hat' + beta s e > 0,
and the closed tube stays in the chart (H > 0, S > 0, Delta_c/rho != 0). Starting from the analytic germ
(w(0) = w_hat(0) = 0), a first exit would contradict these signs, so the germ extends over every
contiguous certified prefix with |H - H_hat| <= |rho| e(|rho|).
"""
import numpy as np

from .ivl import I, Jet


def h_bound(reach, e0, beta):
    """Outward upper bound of reach * e0 * exp(beta * reach)."""
    r = I.of(float(reach))
    return float((r*float(e0)*(I.of(float(beta))*r).exp()).hi)
from .model import Anchor


def cells(smax, s_switch=1e-9, n_near=1, ratio=1.002):
    near = np.linspace(0.0, min(s_switch, smax), n_near + 1)
    edges = [near]
    if smax > s_switch:
        n = int(np.ceil(np.log(smax/s_switch)/np.log(ratio)))
        edges.append(s_switch*np.exp(np.linspace(0, np.log(smax/s_switch), n + 1))[1:])
    e = np.concatenate(edges)
    e[-1] = smax
    return e


def _sub(x, idx):
    return I(x.lo[idx], x.hi[idx])


class SideCertifier:
    """Barrier certificate for one candidate on one side of the crossing."""

    def __init__(self, model, ell, cand, side, smax, s_switch=1e-9, ratio=1.002):
        self.model, self.ell, self.cand, self.side, self.smax = model, ell, cand, side, smax
        self.s_switch, self.ratio = s_switch, ratio

    # candidate enclosures
    def _cand_cell(self, sa, sb, order):
        lo, hi = np.minimum(self.side*sa, self.side*sb), np.maximum(self.side*sa, self.side*sb)
        rho = I(lo, hi)
        return rho, self.cand(Jet([rho, 1.0] + [0.0]*(order - 1)), order)

    def _tube(self, s, e0, beta):
        return e0*(I.of(beta)*s).exp()

    def check(self, sa, sb, e0, beta, need_gates=True):
        """Boolean pass mask per cell [sa, sb] plus diagnostics."""
        sa, sb = np.asarray(sa, float), np.asarray(sb, float)
        M, ell, side = self.model, self.ell, self.side
        s = I(sa, sb)
        e = self._tube(s, e0, beta)
        ok = np.ones(sa.shape, bool)
        near = sb <= self.s_switch*(1 + 1e-12)
        out = {}
        rho, wj = self._cand_cell(sa, sb, 2)
        w, wp = wj.c[0], wj.c[1]
        rwp = rho*wp
        # chart gates on the whole tube (natural)
        tube = I(w.lo - e.hi, w.hi + e.hi)
        tube = I(np.nextafter(tube.lo, -np.inf), np.nextafter(tube.hi, np.inf))
        d, n, H, S = M.divided(rho, tube, ell)
        dmig = np.where(d.lo > 0, d.lo, np.where(d.hi < 0, -d.hi, 0.0))
        gate = (H.lo > 0) & (S.lo > 0) & (dmig > 0)
        out.update(Hmin=H.lo, Smin=S.lo, dmin=dmig)
        ok &= gate
        # barrier signs
        se = I.of(beta)*s*e
        up_n = M.frak_divided(rho, w + e, ell) - rwp - se
        lo_n = M.frak_divided(rho, w - e, ell) - rwp + se
        defect_n = M.frak_divided(rho, w, ell) - rwp
        far = ~near
        up_hi, lo_lo = up_n.hi.copy(), lo_n.lo.copy()
        dsup = defect_n.mag().copy()
        if far.any():
            idx = np.nonzero(far)[0]
            ra, rb = rho.lo[idx], rho.hi[idx]
            rc = 0.5*(ra + rb)
            # centre values
            rcI = I(rc)
            wc = self.cand(Jet([rcI, 1.0]), 1)
            wc0, wc1 = wc.c[0], wc.c[1]
            # derivative enclosures over cells
            rcell = I(ra, rb)
            wcell = Jet([_sub(w, idx), _sub(wp, idx)])
            rw_cell = Jet([rcell*_sub(wp, idx), _sub(wp, idx) + 2*rcell*_sub(wj.c[2], idx)])
            rw_c = Jet([rcI*wc1, wc1])
            for sgn, store in ((1, 'up'), (-1, 'lo'), (0, 'def')):
                vals = []
                for rr, ww, rw in ((rcI, Jet([wc0, wc1]), rw_c), (rcell, wcell, rw_cell)):
                    rj = Jet([rr, 1.0])
                    sj = rj*side
                    ej = (sj*beta).exp()*e0
                    g = M.frak_undivided(rj, ww + ej*sgn, ell) - rw - (sj*ej*beta)*sgn
                    vals.append(g)
                gc, gcell = vals[0].c[0], vals[1].c[1]
                enc = gc + gcell*(I(ra, rb) - I(rc))
                if store == 'up':
                    up_hi[idx] = np.minimum(up_hi[idx], enc.hi)
                elif store == 'lo':
                    lo_lo[idx] = np.maximum(lo_lo[idx], enc.lo)
                else:
                    dsup[idx] = np.minimum(dsup[idx], enc.mag())
        ok &= (up_hi < 0) & (lo_lo > 0)
        out.update(defect=dsup, ok=ok, up_hi=up_hi, lo_lo=lo_lo)
        return out

    def edges_for(self, e0):
        """Cells matched to the tube: natural cells of width ~e0/20 below s_switch, then geometric cells."""
        q = float(np.clip(np.sqrt(e0/20), 2e-4, 2e-3))
        s_switch = float(np.clip(1e-10/e0, 1e-9, 1e-3))
        n_near = int(np.clip(np.ceil(s_switch*20/e0), 1, 20000))
        return cells(self.smax, min(s_switch, self.smax), n_near, 1 + q)

    def run(self, e0, beta, depth=3, keep=400):
        """Largest certified prefix [0, reach]; failing cells are split in four up to `depth` times."""
        edges = self.edges_for(e0)
        sa, sb = edges[:-1], edges[1:]
        for level in range(depth + 1):
            res = self.check(sa, sb, e0, beta)
            bad = np.nonzero(~res['ok'])[0]
            if len(bad) == 0 or level == depth:
                break
            bad = bad[:keep]
            last = bad[-1]
            sa, sb, mask = sa[:last + 1], sb[:last + 1], np.zeros(last + 1, bool)
            mask[bad] = True
            pieces_a, pieces_b = [], []
            for k in range(last + 1):
                if mask[k]:
                    g = np.linspace(sa[k], sb[k], 5)
                    pieces_a.append(g[:-1]); pieces_b.append(g[1:])
                else:
                    pieces_a.append(sa[k:k + 1]); pieces_b.append(sb[k:k + 1])
            sa, sb = np.concatenate(pieces_a), np.concatenate(pieces_b)
        bad = np.nonzero(~res['ok'])[0]
        upto = len(sa) if len(bad) == 0 else bad[0]
        sl = slice(0, upto)
        stats = {}
        for k in ('Hmin', 'Smin', 'dmin'):
            stats[k] = float(np.min(res[k][sl])) if upto else None
        stats['defect'] = float(np.max(res['defect'][sl])) if upto else None
        stats['reach'] = float(sb[upto - 1]) if upto else 0.0
        stats['cells'] = int(len(sa))
        return stats


def sampled_tube_ok(cert, e0, beta, s):
    """Fast floating check of the barrier signs at sample points (screening only)."""
    M, ell, side = cert.model, float(np.asarray(I.of(cert.ell).mid)), cert.side
    rho = side*s
    wj = cert.cand(Jet([I(rho), 1.0]), 1)
    w, wp = wj.c[0].mid, wj.c[1].mid
    e = e0*np.exp(beta*s)
    fm = lambda ww: _float_frak(M, rho, ww, ell)
    up = fm(w + e) - rho*wp - beta*s*e
    lo = fm(w - e) - rho*wp + beta*s*e
    good = (up < 0) & (lo > 0)
    bad = np.nonzero(~good)[0]
    return s[bad[0] - 1] if len(bad) and bad[0] > 0 else (0.0 if len(bad) else s[-1])


def _float_frak(M, rho, w, ell):
    small = np.abs(rho) < 1e-3
    with np.errstate(all='ignore'):
        und = M.frak_undivided(rho, w, ell)
        d, n, _, _ = M.divided(rho, w, ell)
    return np.where(small, n/d - ell - w, und)


def certify_side(model, ell, cand, side, smax, e0_grid=None, beta_grid=(0, 1, 3, 10, 30), tries=3, e0_cap=1.0, ratio=1.002):
    """Search the tube parameters (screened tries, then e0 x3 up to e0_cap); return the best certificate record."""
    e0_grid = np.geomspace(1e-7, 3e-1, 23) if e0_grid is None else e0_grid
    cert = SideCertifier(model, ell, cand, side, smax, ratio=ratio)
    s = np.concatenate([np.linspace(1e-5, 1e-3, 30), np.geomspace(1e-3, smax, 400)]) if smax > 1e-3 else np.linspace(1e-6, smax, 200)
    # screening only: midpoint float model and slope
    mid = lambda v: float(np.asarray(I.of(v).mid))
    screen = SideCertifier(Anchor(mid(model.m), mid(model.kappa), mid(model.gamma), model.f), mid(ell), cand, side, smax)
    screened = []
    for beta in beta_grid:
        for e0 in e0_grid:
            with np.errstate(all='ignore'):
                reach = sampled_tube_ok(screen, e0, beta, s)
            bound = reach*e0*np.exp(beta*reach)
            screened.append((-reach, bound, e0, beta))
    screened.sort()
    best = None

    def attempt(e0, beta):
        nonlocal best
        st = cert.run(e0, beta)
        st.update(e0=float(e0), beta=float(beta))
        st['H_error_bound'] = h_bound(st['reach'], e0, beta)
        if best is None or st['reach'] > best['reach'] + 1e-12 or (
                abs(st['reach'] - best['reach']) <= 1e-12 and st['H_error_bound'] < best['H_error_bound']):
            best = st
        return st['reach'] >= smax
    for _, _, e0, beta in screened[:tries]:
        if attempt(e0, beta):
            return best
    e0, beta = best['e0'], best['beta']
    while e0*3 <= e0_cap:
        lo, e0 = e0, e0*3
        if attempt(e0, beta):
            # geometric bisection between the last failing and the first passing e0, for beta and for 0
            for b in sorted({0.0, float(beta)}):
                a_, c_ = lo, e0
                if b != beta and not attempt(c_, b):
                    continue
                for _ in range(3):
                    mid = np.sqrt(a_*c_)
                    if attempt(mid, b):
                        c_ = mid
                    else:
                        a_ = mid
            break
    return best


def certify_at_tolerance(model, ell, cand, side, smax, H_tol):
    """Single certificate attempt with the tube e = H_tol/smax (beta = 0), so |H - H_hat| <= H_tol on the slice."""
    cert = SideCertifier(model, ell, cand, side, smax)
    e0 = H_tol/smax
    st = cert.run(e0, 0.0)
    st.update(e0=e0, beta=0.0, H_error_bound=h_bound(st['reach'], e0, 0.0), accepted=bool(st['reach'] >= smax*(1 - 1e-12)))
    return st


def bed_lipschitz(model, ell, cand, side, reach, e0, beta, ncell=400):
    """Outward enclosure of sup |(P_Z)_H| over the certified tube on [0, reach] (natural cells)."""
    if reach <= 0:
        return None
    e = np.linspace(0.0, reach, ncell + 1)
    sa, sb = e[:-1], e[1:]
    rho = I(np.minimum(side*sa, side*sb), np.maximum(side*sa, side*sb))
    w = cand(Jet([rho, 1.0]), 1).c[0]
    tube = e0*(I.of(beta)*I(sa, sb)).exp()
    H = 1 + rho*(ell + (I(w.lo, w.hi) + I(-tube.hi, tube.hi)))
    _, _, _, PZ = model.parts(1 + rho, Jet([H, 1.0]))
    return float(np.max(PZ.c[1].mag()))
