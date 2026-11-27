"""Candidate profiles w_hat(rho) evaluated on floats, intervals or jets.

Each candidate is a callable cand(rho_jet, order) returning a Jet of w_hat. The networks receive
point or interval parameters nu_hat and fixed float weights, so the certified object is the exact
real function defined by those weights.
"""
import numpy as np

from .ivl import I, Jet, tanh


def _clenshaw(coeffs, x):
    b1 = b2 = 0.0
    for c in coeffs[:0:-1]:
        b1, b2 = x*b1*2 - b2 + float(c), b1
    return x*b1 - b2 + float(coeffs[0])


def poly_rho(coeffs):
    """w_hat = sum_k coeffs[k] rho^k (monomial; used for the Taylor germ)."""
    def cand(rho, order=None):
        acc = 0.0*rho + float(coeffs[-1])
        for c in coeffs[-2::-1]:
            acc = acc*rho + float(c)
        return acc
    return cand


def cheb_side(coeffs, smax, side):
    """w_hat = s * sum_k c_k T_k(2 s/smax - 1), s = side*rho (one side of the crossing)."""
    def cand(rho, order=None):
        s = rho*side
        return s*_clenshaw(coeffs, s*2.0/smax - 1.0)
    return cand


def _vector_input(rho_hat, nu_hat):
    """Stack the scalar jet rho_hat with constant parameters nu_hat (point floats or I) as a vector jet."""
    c0 = rho_hat.c[0]
    shape = np.shape(I.of(c0).lo)
    los = [np.broadcast_to(I.of(c0).lo, shape)]
    his = [np.broadcast_to(I.of(c0).hi, shape)]
    for v in nu_hat:
        v = I.of(v)
        los.append(np.broadcast_to(v.lo, shape))
        his.append(np.broadcast_to(v.hi, shape))
    out = [I(np.stack(los), np.stack(his))]
    for ck in rho_hat.c[1:]:
        z = np.zeros((len(nu_hat) + 1,) + shape)
        ck = I.of(ck)
        z_lo, z_hi = z.copy(), z.copy()
        z_lo[0], z_hi[0] = np.broadcast_to(ck.lo, shape), np.broadcast_to(ck.hi, shape)
        out.append(I(z_lo, z_hi))
    return Jet(out)


def _row(jet, k=0):
    return Jet([I(c.lo[k], c.hi[k]) for c in jet.c])


class Net:
    """w_hat = rho * R(rho_hat, nu_hat), rho_hat = (rho - rc)/rs, with R one of three architectures."""

    def __init__(self, kind, weights, rc, rs, nu_hat):
        self.kind, self.wt, self.rc, self.rs, self.nu = kind, weights, rc, rs, nu_hat

    def R(self, rho_hat):
        wt = self.wt
        if self.kind == 'rf':
            # sum_j T_j(rho_hat) * (A_j . phi(nu)), phi = [1, nu, tanh(Wf nu + bf)]
            phi = self.phi()
            coeffs = [sum((phi[k]*float(wt['A'][j, k]) for k in range(len(phi))), 0.0) for j in range(wt['A'].shape[0])]
            b1 = b2 = 0.0
            for c in coeffs[:0:-1]:
                b1, b2 = rho_hat*b1*2 - b2 + c, b1
            return rho_hat*b1 - b2 + coeffs[0]
        x = _vector_input(rho_hat, self.nu)
        if self.kind == 'mlp':
            h = x
            for W, b in wt['layers'][:-1]:
                h = h.matvec(W, b).tanh()
            W, b = wt['layers'][-1]
            return _row(h.matvec(W, b))
        if self.kind == 'gated':
            v0 = x.matvec(wt['A'], wt['b']).tanh()
            t = I(np.asarray(wt['d'], float)).tanh()
            u = v0.matvec(wt['W']).tanh()
            nd = np.ndim(I.of(u.c[0]).lo) - 1
            gate = I(t.lo.reshape(t.lo.shape + (1,)*nd), t.hi.reshape(t.hi.shape + (1,)*nd))
            v1 = v0 + u*gate
            nu1 = [1.0] + list(self.nu)
            coef = [sum((I.of(nu1[k])*float(wt['Theta'][k, i]) for k in range(len(nu1))), 0.0) for i in range(wt['Theta'].shape[1])]
            out = 0.0
            for i, ci in enumerate(coef):
                out = _row(v1, i)*ci + out
            return out
        raise ValueError(self.kind)

    def phi(self):
        wt = self.wt
        nu = [I.of(v) for v in self.nu]
        feats = [I.of(1.0)] + nu
        for i in range(wt['Wf'].shape[0]):
            z = sum((nu[k]*float(wt['Wf'][i, k]) for k in range(len(nu))), 0.0) + float(wt['bf'][i])
            feats.append(I.of(z).tanh())
        return feats

    def __call__(self, rho, order=None):
        rho_hat = (rho - self.rc)/self.rs
        return rho*self.R(rho_hat)
