"""Anchored radial crossing of the planar model E2 with g=C1=C2=1 at (r,H)=(1,1).

The reduced profile depends on (m, kappa=K/G, gamma=c/G) and the rotation rate f.
All functions accept floats, intervals (I) or jets, so the same formulas serve training,
reference integration and interval certification.
"""
import numpy as np
from scipy.integrate import solve_ivp

from .ivl import I, Jet, powr, F


class Anchor:
    def __init__(self, m, kappa, gamma, f):
        self.m, self.kappa, self.gamma, self.f = m, kappa, gamma, f
        self.a = (m - 1)*0.5
        W0 = 1 - f*0.5
        self.W0 = W0
        self.S0 = W0*W0 + 1
        self.P = self.S0 + f*W0
        self.Qg0 = powr(self.S0, self.a)*(kappa - self.P)
        self.C3g = gamma*0.5 + self.Qg0

    # undivided functions of (r, H)
    def parts(self, r, H):
        V = 1/(r*H)
        W = 1/r - self.f*0.5*r
        S = V*V + W*W
        Qg = self.C3g/r - self.gamma*0.5*r
        PZ = self.kappa*V - Qg*powr(S, -self.a)
        return V, W, S, PZ

    def DN(self, r, H):
        V, W, S, PZ = self.parts(r, H)
        return H - V*V, H*(S/r + self.f*W - PZ), PZ

    def frak_undivided(self, rho, w, ell):
        """f(rho,w) = N/Delta_c - ell - w with H = 1 + rho(ell+w)."""
        r = 1 + rho
        H = 1 + rho*(ell + w)
        Dc, N, _ = self.DN(r, H)
        return N/Dc - ell - w

    def divided(self, rho, w, ell):
        """Cancellation-free d = Delta_c/rho and n = N/rho on intervals (rho may contain 0)."""
        Y = ell + w
        r = 1 + rho
        H = 1 + rho*Y
        B = H*H*H
        d = ((2 + rho)*B + Y*(3 + 3*rho*Y + rho*rho*Y*Y))/(r*r*H*H)
        V = 1/(r*H)
        W = 1/r - self.f*0.5*r
        vd = -(1 + Y + rho*Y)/(r*H)
        wd = -1/r - self.f*0.5
        sd = vd*(V + 1) + wd*(W + self.W0)
        S = V*V + W*W
        qd = -self.C3g/r - self.gamma*0.5
        Sa = powr(S, -self.a)
        xi = I.of(self.S0).hull(S) if isinstance(S, I) else S
        M = -self.a*powr(xi, -self.a - 1) if isinstance(S, I) else _mean_power(self.S0, S, self.a)
        pd = self.kappa*vd - qd*Sa - self.Qg0*sd*M
        n = H*((sd - self.S0)/r + self.f*wd - pd)
        return d, n, H, S

    def frak_divided(self, rho, w, ell):
        d, n, _, _ = self.divided(rho, w, ell)
        return n/d - ell - w

    def jacobian(self):
        """Entries of D_(r,H)(Delta_c, N) at the anchor, by first-order jets."""
        one = I.of(1.0) if isinstance(self.kappa, I) else 1.0
        Dr, Nr, _ = self.DN(Jet.var(one, 1), Jet.const(one, 1))
        DH, NH, _ = self.DN(Jet.const(one, 1), Jet.var(one, 1))
        return Dr.c[1], DH.c[1], Nr.c[1], NH.c[1]

    def slopes(self):
        """(det J, [(ell, lambda, a)] for the two branches, minus first)."""
        Dr, DH, Nr, NH = self.jacobian()
        det = Dr*NH - DH*Nr
        p = Dr - NH
        disc = p*p + 4*DH*Nr
        root = F('sqrt', disc)
        out = []
        for sgn in (-1, 1):
            ell = (-p + sgn*root)/(2*DH)
            lam = Dr + DH*ell
            lam_o = (Dr + NH) - lam
            out.append((ell, lam, lam_o/lam - 1))
        return det, out


def _mean_power(S0, S, a):
    """(S^-a - S0^-a)/(S - S0) for floats, with the limit at S=S0."""
    S = np.asarray(S, float)
    dS = S - S0
    small = np.abs(dS) < 1e-12
    safe = np.where(small, 1.0, dS)
    val = (S**-a - S0**-a)/safe
    return np.where(small, -a*S0**(-a - 1), val)


def cstar(m, kappa, f, lo=-400.0, hi=400.0):
    """gamma at which det J changes sign (det is increasing in gamma)."""
    from scipy.optimize import brentq
    return brentq(lambda g: Anchor(m, kappa, g, f).slopes()[0], lo, hi, xtol=1e-14)


def taylor(model, ell, a, K=16):
    """Taylor coefficients w_1..w_K of the analytic germ, from (k - a) w_k = [frak]_k."""
    w = np.zeros(K + 1)
    for k in range(1, K + 1):
        rho = Jet.var(0.0, k + 1)
        wj = Jet(list(w[:k + 1]) + [0.0])
        Y = ell + wj
        r, H = 1 + rho, 1 + rho*Y
        Dc, N, _ = model.DN(r, H)
        n, d = Jet(N.c[1:]), Jet(Dc.c[1:])
        fr = n/d - ell - Jet(list(w[:k + 1]))
        w[k] = fr.c[k]/(k - a)
    return w


def taylor_eval(w, rho):
    return np.polyval(w[::-1], rho)


def reference(model, ell, a, side, smax, s0=1e-3, K=16, rtol=1e-12, atol=1e-13):
    """DOP853 integration of s dw/ds = frak(side*s, w) from the Taylor germ outward to smax."""
    w = taylor(model, ell, a, K)
    w0 = taylor_eval(w, side*s0)
    sgn0 = np.sign(model.DN(1 + side*s0, 1 + side*s0*(ell + w0))[0])

    def rhs(s, y):
        return [model.frak_undivided(side*s, y[0], ell)/s]

    def crit(s, y):
        rho = side*s
        Dc = model.DN(1 + rho, 1 + rho*(ell + y[0]))[0]
        return sgn0*Dc/s - 1e-6
    crit.terminal = True

    def dry(s, y):
        return 1 + side*s*(ell + y[0]) - 1e-3
    dry.terminal = True
    sol = solve_ivp(rhs, (s0, smax), [w0], method='DOP853', rtol=rtol, atol=atol,
                    dense_output=True, events=[crit, dry])
    reason = 'boundary_reached' if sol.status == 0 else (
        'critical_point' if len(sol.t_events[0]) else 'dry_bed' if len(sol.t_events[1]) else 'solver_failure')
    return {'taylor': w, 'sol': sol, 'extent': float(sol.t[-1]), 'reason': reason, 's0': s0, 'side': side}


def reference_w(ref, s):
    """Reference w(s) on [0, extent]: Taylor germ below s0, dense DOP853 output above."""
    s = np.asarray(s, float)
    dense = ref['sol'].sol(np.clip(s, ref['s0'], ref['extent']))[0]
    return np.where(s <= ref['s0'], taylor_eval(ref['taylor'], ref['side']*s), dense)
