"""Outward-rounded interval arithmetic and truncated Taylor jets.

Interval endpoints are float64 arrays. Every arithmetic result is widened by one ulp in each
direction (np.nextafter). Elementary functions (exp, log, tanh, sqrt) are widened by four ulps;
this assumes the platform libm is accurate to within four ulps, which the cross-check against
mpmath intervals in verify_parameter_neighborhoods.py tests on sampled cells.
"""
import numpy as np

INF = np.inf
U = np.finfo(float).eps / 2


def _dn(x):
    return np.nextafter(x, -INF)


def _up(x):
    return np.nextafter(x, INF)


def _pdn(x, k=4):
    return x - k*np.spacing(np.abs(x)) - 5e-324


def _pup(x, k=4):
    return x + k*np.spacing(np.abs(x)) + 5e-324


class I:
    """Closed interval [lo, hi], vectorized over numpy arrays."""
    __slots__ = ('lo', 'hi')
    __array_priority__ = 100

    def __init__(self, lo, hi=None):
        self.lo = np.asarray(lo, dtype=float)
        self.hi = self.lo if hi is None else np.asarray(hi, dtype=float)

    @staticmethod
    def of(x):
        return x if isinstance(x, I) else I(x, x)

    @property
    def mid(self):
        return 0.5*(self.lo + self.hi)

    @property
    def rad(self):
        """Upper bound of max(mid - lo, hi - mid), so [mid - rad, mid + rad] contains [lo, hi]."""
        m = self.mid
        return _up(np.maximum(_up(m - self.lo), _up(self.hi - m)))

    def mag(self):
        return np.maximum(np.abs(self.lo), np.abs(self.hi))

    def mig(self):
        return np.where((self.lo <= 0) & (self.hi >= 0), 0.0, np.minimum(np.abs(self.lo), np.abs(self.hi)))

    def __getitem__(self, k):
        return I(self.lo[k], self.hi[k])

    def __add__(self, o):
        if isinstance(o, Jet):
            return NotImplemented
        o = I.of(o)
        return I(_dn(self.lo + o.lo), _up(self.hi + o.hi))

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, o):
        if isinstance(o, Jet):
            return NotImplemented
        o = I.of(o)
        return I(_dn(self.lo - o.hi), _up(self.hi - o.lo))

    def __rsub__(self, o):
        if isinstance(o, Jet):
            return NotImplemented
        return I.of(o) - self

    def __mul__(self, o):
        if isinstance(o, Jet):
            return NotImplemented
        o = I.of(o)
        p = (self.lo*o.lo, self.lo*o.hi, self.hi*o.lo, self.hi*o.hi)
        lo = np.minimum(np.minimum(p[0], p[1]), np.minimum(p[2], p[3]))
        hi = np.maximum(np.maximum(p[0], p[1]), np.maximum(p[2], p[3]))
        lo = np.where(np.isnan(lo), -INF, lo)
        hi = np.where(np.isnan(hi), INF, hi)
        return I(_dn(lo), _up(hi))

    __rmul__ = __mul__

    def recip(self):
        bad = (self.lo <= 0) & (self.hi >= 0)
        with np.errstate(divide='ignore', invalid='ignore'):
            lo, hi = _dn(1/self.hi), _up(1/self.lo)
        return I(np.where(bad, -INF, lo), np.where(bad, INF, hi))

    def __truediv__(self, o):
        if isinstance(o, Jet):
            return NotImplemented
        return self*I.of(o).recip()

    def __rtruediv__(self, o):
        if isinstance(o, Jet):
            return NotImplemented
        return I.of(o)*self.recip()

    def sqr(self):
        a, b = self.lo*self.lo, self.hi*self.hi
        z = (self.lo <= 0) & (self.hi >= 0)
        return I(np.where(z, 0.0, _dn(np.minimum(a, b))), _up(np.maximum(a, b)))

    def exp(self):
        return I(np.maximum(_pdn(np.exp(self.lo)), 0.0), _pup(np.exp(self.hi)))

    def log(self):
        with np.errstate(divide='ignore', invalid='ignore'):
            lo = np.where(self.lo > 0, _pdn(np.log(np.where(self.lo > 0, self.lo, 1.0))), -INF)
            hi = np.where(self.hi > 0, _pup(np.log(np.where(self.hi > 0, self.hi, 1.0))), np.nan)
        return I(lo, hi)

    def tanh(self):
        return I(np.maximum(_pdn(np.tanh(self.lo)), -1.0), np.minimum(_pup(np.tanh(self.hi)), 1.0))

    def sqrt(self):
        return I(np.maximum(_pdn(np.sqrt(np.maximum(self.lo, 0.0))), 0.0), _pup(np.sqrt(self.hi)))

    def powr(self, p):
        """x**p for x>0 via exp(p log x)."""
        return (I.of(p)*self.log()).exp()

    def hull(self, o):
        o = I.of(o)
        return I(np.minimum(self.lo, o.lo), np.maximum(self.hi, o.hi))

    def matvec(self, W, b=None):
        """Point matrix W (k x n) times interval vector with leading axis n; optional point bias b (k,)."""
        W = np.asarray(W, float)
        xm, xr = self.mid, self.rad
        shape = (W.shape[0],) + (1,)*(xm.ndim - 1)
        ym = np.tensordot(W, xm, axes=(1, 0))
        A = np.abs(W)
        n = W.shape[1] + 2
        gam = n*U/(1 - n*U)
        yr = (1 + gam)*np.tensordot(A, xr, axes=(1, 0)) + gam*np.tensordot(A, np.abs(xm) + xr, axes=(1, 0))
        if b is not None:
            bb = np.asarray(b, float).reshape(shape)
            yr = yr + gam*np.abs(bb)
            ym = ym + bb
        yr = _up(_up(yr) + np.spacing(np.abs(ym)))
        return I(_dn(ym - yr), _up(ym + yr))


def F(name, x):
    """Elementary function on an interval or a float array."""
    if isinstance(x, I):
        return getattr(x, name)()
    return getattr(np, name)(x)


class Jet:
    """Truncated Taylor series c0 + c1 h + ... + cK h^K in one variable; coefficients are I or floats."""
    __slots__ = ('c',)

    def __init__(self, c):
        self.c = list(c)

    @property
    def K(self):
        return len(self.c) - 1

    @staticmethod
    def var(x, K):
        return Jet([x, 1.0] + [0.0]*(K - 1))

    @staticmethod
    def const(x, K):
        return Jet([x] + [0.0]*K)

    def _lift(self, o):
        return o if isinstance(o, Jet) else Jet.const(o, self.K)

    def __add__(self, o):
        o = self._lift(o)
        return Jet([a + b for a, b in zip(self.c, o.c)])

    __radd__ = __add__

    def __neg__(self):
        return Jet([-a for a in self.c])

    def __sub__(self, o):
        return self + (-self._lift(o))

    def __rsub__(self, o):
        return self._lift(o) - self

    def __mul__(self, o):
        if not isinstance(o, Jet):
            return Jet([a*o for a in self.c])
        return Jet([sum((self.c[i]*o.c[k - i] for i in range(k + 1)), 0.0) for k in range(self.K + 1)])

    def __rmul__(self, o):
        return self*o

    def __truediv__(self, o):
        if not isinstance(o, Jet):
            if isinstance(o, I) or any(isinstance(c, I) for c in self.c):
                return self*I.of(o).recip()
            return self*(1.0/o)
        inv0 = o.c[0].recip() if isinstance(o.c[0], I) else 1.0/o.c[0]
        q = []
        for k in range(self.K + 1):
            acc = self.c[k]
            for i in range(1, k + 1):
                acc = acc - o.c[i]*q[k - i]
            q.append(acc*inv0)
        return Jet(q)

    def __rtruediv__(self, o):
        return self._lift(o)/self

    def exp(self):
        e = [F('exp', self.c[0])]
        for k in range(1, self.K + 1):
            e.append(sum((i*self.c[i]*e[k - i] for i in range(1, k + 1)), 0.0)*(1.0/k))
        return Jet(e)

    def log(self):
        a0 = self.c[0]
        inv0 = a0.recip() if isinstance(a0, I) else 1.0/a0
        l = [F('log', a0)]
        for k in range(1, self.K + 1):
            acc = self.c[k]
            for i in range(1, k):
                acc = acc - (i/k)*l[i]*self.c[k - i]
            l.append(acc*inv0)
        return Jet(l)

    def tanh(self):
        t0 = F('tanh', self.c[0])
        if self.K == 0:
            return Jet([t0])
        s = 1.0 - (t0.sqr() if isinstance(t0, I) else t0*t0)
        t1 = s*self.c[1]
        if self.K == 1:
            return Jet([t0, t1])
        if self.K == 2:
            return Jet([t0, t1, s*self.c[2] - t0*t1*self.c[1]])
        raise NotImplementedError('tanh jets beyond order 2')

    def matvec(self, W, b=None):
        """Linear map on a vector jet whose coefficients all carry the vector axis first."""
        return Jet([I.of(ck).matvec(W, b if k == 0 else None) for k, ck in enumerate(self.c)])


def powr(x, p):
    """x**p for positive x on floats, intervals or jets."""
    if isinstance(x, Jet):
        return (x.log()*p).exp()
    if isinstance(x, I):
        return x.powr(p)
    if isinstance(p, I):
        return I.of(x).powr(p)
    return x**p


def tanh(x):
    if isinstance(x, (Jet, I)):
        return x.tanh()
    return np.tanh(x)
