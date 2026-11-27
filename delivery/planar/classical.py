"""Classical route: Chebyshev collocation of s dw/ds = frak(side*s, w) on one side of the crossing."""
import time

import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import least_squares


def basis(s, smax, N):
    x = 2*s/smax - 1
    T = C.chebvander(x, N - 1)
    dT = np.stack([C.chebval(x, C.chebder(np.eye(N)[k]))*(2/smax) for k in range(N)], axis=1)
    return T, dT


def collocate(model, ell, side, smax, N, c0=None, max_nfev=400):
    """Solve for c in w = s sum c_k T_k; returns coefficients, nfev, seconds, success."""
    k = np.arange(N)
    s = 0.5*smax*(1 - np.cos((2*k + 1)*np.pi/(2*N)))
    T, dT = basis(s, smax, N)

    def resid(c):
        w = s*(T @ c)
        dw = T @ c + s*(dT @ c)
        with np.errstate(all='ignore'):
            r = s*dw - model.frak_undivided(side*s, w, ell)
        return np.where(np.isfinite(r), r, 1e6)
    c0 = np.zeros(N) if c0 is None else c0
    t = time.perf_counter()
    sol = least_squares(resid, c0, method='lm', xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=max_nfev*N)
    dt = time.perf_counter() - t
    return {'coeffs': sol.x, 'nfev': int(sol.nfev), 'seconds': dt,
            'success': bool(sol.success and np.max(np.abs(sol.fun)) < 1e-8), 'max_residual': float(np.max(np.abs(sol.fun)))}


def project(wfun, smax, N):
    """Least-squares Chebyshev coefficients of w(s)/s from samples (warm start)."""
    k = np.arange(4*N)
    s = 0.5*smax*(1 - np.cos((2*k + 1)*np.pi/(8*N)))
    T, _ = basis(s, smax, N)
    return np.linalg.lstsq(T, wfun(s)/s, rcond=None)[0]
