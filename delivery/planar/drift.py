"""Whole-domain drift control: U = (U0^m - x/2)^(1/m) on x in [0, 1] (kappa = 1/2, alpha = 1/4).

Candidate U_hat = U0 + x R(x, nu), R = sum_{j<=5} T_j(2x - 1) a_j . [1, nu_hat, tanh(W nu_hat + b)],
with 12 fixed hidden features (seed 27) and the readout a_j fitted to the integral defect
D = (U_hat^m - U0^m)/2 + x/4 without solution labels.
"""
import time

import numpy as np
from scipy.optimize import least_squares

from .ivl import I, Jet, powr

BOX = {'m': (1.0, 4.0), 'U0': (1.0, 1.4)}
J, HIDDEN = 6, 12


def features(m, U0, seed=27):
    g = np.random.default_rng(seed)
    W, b = g.normal(size=(HIDDEN, 2)), g.normal(size=HIDDEN)
    nu = np.array([(m - 2.5)/1.5, (U0 - 1.2)/0.2])
    return np.concatenate([[1.0], nu, np.tanh(W @ nu + b)])


def exact(m, U0, x):
    return (U0**m - x/2)**(1/m)


def U_hat(A, m, U0, x):
    """Works for float arrays, intervals and jets in x (parameters are points)."""
    coef = A @ features(m, U0)
    z = x*2.0 - 1.0
    T0, T1 = 0.0*x + 1.0, z
    R = T0*float(coef[0]) + T1*float(coef[1])
    for j in range(2, J):
        T0, T1 = T1, z*T1*2.0 - T0
        R = R + T1*float(coef[j])
    return x*R + U0


def defect(A, m, U0, x):
    u0m = I.of(U0).powr(I.of(m)) if isinstance(x, (I, Jet)) else U0**m
    return (powr(U_hat(A, m, U0, x), m) - u0m)*0.5 + x*0.25


def fit(pairs, nodes=64):
    x = 0.5*(1 - np.cos((2*np.arange(nodes) + 1)*np.pi/(2*nodes)))

    def res(a):
        A = a.reshape(J, -1)
        with np.errstate(all='ignore'):
            r = np.concatenate([defect(A, p['m'], p['U0'], x) for p in pairs])
        return np.where(np.isfinite(r), r, 1e3)
    t = time.perf_counter()
    sol = least_squares(res, np.zeros(J*(3 + HIDDEN)), method='lm', xtol=1e-15, ftol=1e-15, max_nfev=20000)
    return sol.x.reshape(J, -1), {'seconds': time.perf_counter() - t, 'nfev': int(sol.nfev),
                                  'train_max_defect': float(np.max(np.abs(sol.fun))), 'parameters': int(sol.x.size)}


def certify(A, m, U0, cells=500):
    """Outward-rounded sup|D| over [0,1] (centred form) and min U_hat; error bound 2^m/m sup|D| if U_hat >= 1/2."""
    e = np.linspace(0.0, 1.0, cells + 1)
    xa, xb = e[:-1], e[1:]
    xc = 0.5*(xa + xb)
    cell = I(xa, xb)
    D_c = defect(A, m, U0, I(xc))
    D_cell = defect(A, m, U0, Jet([cell, 1.0]))
    enc = D_c + D_cell.c[1]*I(xa - xc, xb - xc)
    natural = defect(A, m, U0, cell)
    sup = float(np.max(np.minimum(enc.mag(), natural.mag())))
    umin = float(np.min(U_hat(A, m, U0, cell).lo))
    # exact U decreases in x, so its minimum is (U0^m - 1/2)^(1/m) at x = 1
    uex = (I.of(U0).powr(I.of(m)) - 0.5).powr(1/I.of(m))
    xi = min(umin, float(uex.lo))
    ok = xi >= 0.5
    # mean value theorem: |U_hat^m - U^m| >= m xi^(m-1) |U_hat - U|, and D = (U_hat^m - U^m)/2
    factor = (2.0/(I.of(m)*I.of(xi).powr(I.of(m) - 1.0))).hi
    crude = I.of(2.0).powr(I.of(m)).hi/m
    return {'sup_defect': sup, 'U_hat_min': umin, 'U_min': float(uex.lo), 'factor': float(factor),
            'factor_xi_half': float(crude), 'error_bound': float((I.of(factor)*sup).hi) if ok else None,
            'positivity_ok': bool(ok), 'cells': cells}
