"""Single-parameter 1D Chebyshev spectral collocation on each side of the crossing.

Solves s * dw/ds = frak(side * s, w; nu_0) on s in (0, smax] using the crossing-exact
ansatz w_C(s) = s * sum_{k=0}^{N-1} c_k T_k(2 s / smax - 1), which enforces w(0) = 0
and H(1) = 1, H'(1) = ell(nu_0) identically.
"""
import time
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import least_squares


def basis(s, smax, N):
    x = 2.0 * np.asarray(s, dtype=float) / smax - 1.0
    T = C.chebvander(x, N - 1)
    dT = np.stack([C.chebval(x, C.chebder(np.eye(N)[k])) * (2.0 / smax) for k in range(N)], axis=1)
    return T, dT


def eval_cheb_side(coeffs, smax, side, rho):
    """Return (w, dw_drho, H, dH_dr) at rho = side * s for s >= 0."""
    rho_a = np.asarray(rho, dtype=float)
    s = side * rho_a
    T, dT = basis(s, smax, len(coeffs))
    q = T @ coeffs
    dq_ds = dT @ coeffs
    w = s * q
    dw_ds = q + s * dq_ds
    dw_drho = side * dw_ds
    return w, dw_drho


def collocate(model, ell, side, smax, N, max_nfev=400):
    """Solve for Chebyshev coefficients c in w(s) = s * sum c_k T_k(2 s / smax - 1) for one fixed tuple."""
    k = np.arange(N)
    s = 0.5 * smax * (1.0 - np.cos((2.0 * k + 1.0) * np.pi / (2.0 * N)))
    T, dT = basis(s, smax, N)

    def resid(c):
        w = s * (T @ c)
        dw_ds = (T @ c) + s * (dT @ c)
        with np.errstate(all='ignore'):
            r = s * dw_ds - model.frak_undivided(side * s, w, ell)
        return np.where(np.isfinite(r), r, 1e6)

    t0 = time.perf_counter()
    sol = least_squares(
        resid, np.zeros(N), method='lm',
        xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=max_nfev * N,
    )
    secs = time.perf_counter() - t0
    max_res = float(np.max(np.abs(sol.fun)))
    return {
        'coeffs': sol.x,
        'N': int(N),
        'domain': float(smax),
        'nfev': int(sol.nfev),
        'seconds': float(secs),
        'success': bool(sol.success and max_res < 1e-8),
        'max_collocation_residual': max_res,
    }
