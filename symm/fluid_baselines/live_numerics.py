"""Persistent versions of the small periodic CPU controls in ``numerics``.

NS/Oseen store complex Fourier vorticity; SVE stores real conservative (h, hu, B).
Parameters are constant between explicit updates at ``t``. No state is restarted
or clipped. Clone before advancing if a controller needs whole-call rollback:
successful internal steps remain committed when a later stage fails.
Oseen a/b are advection coefficients; its reconstructed velocity mean is always
(.3, -.2), so coefficient changes preserve all physical fields at the update.
Restart needs only state/t/params/steps and n/model/kind; all other data are
deterministically reconstructed by the constructor, including conservation references.

The spectral tail ratio is a resolution indicator, not an error certificate.
SVE retains the original smooth-solution, non-well-balanced Rusanov baseline;
neither long-time accuracy nor shock/positivity certification is implied.
"""
from collections.abc import Mapping
from copy import deepcopy
from numbers import Integral, Real

import numpy as np


_DEFAULTS = {"ns": {"nu": .01}, "oseen": {"nu": .01, "a": .3, "b": -.2},
             "sve": {"m": 3., "kappa": .1, "g": 1.}}
_BOUNDS = {"nu": (.0005, 1.), "a": (-2., 2.), "b": (-2., 2.),
           "m": (.5, 6.), "kappa": (0., 1.), "g": (.1, 10.)}


def _finite_scalar(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number")
    try:
        value = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not np.isfinite(value):
        raise ValueError(f"{name} must be a finite real number")
    return value


def _check_finite(state):
    if not np.all(np.isfinite(state)):
        raise RuntimeError("Evolution became nonfinite; run rejected")


def _tail_ratio(spectrum, tail):
    # Rescale before squaring so the diagnostic also handles tiny decayed fields.
    magnitude = np.abs(spectrum)
    scale = float(magnitude.max())
    if scale == 0:
        return 0.
    power = (magnitude / scale)**2
    return float(power[..., tail].sum() / power.sum())


class _Stepper:
    def __init__(self, model, n, parameters, kind):
        self.model, self.n, self.kind = model, n, kind
        self.t, self.steps = 0., 0
        self._params = _DEFAULTS[model].copy()
        if parameters is not None:
            self.set_parameters(parameters)
        self.dx = 2 * np.pi / n

    @property
    def params(self):
        """A dictionary snapshot; use set_parameters for validated changes."""
        return self._params.copy()

    def set_parameters(self, updates):
        """Validate the entire update before changing any coefficient."""
        if not isinstance(updates, Mapping):
            raise ValueError("parameter updates must be a mapping")
        unknown = [name for name in updates if name not in self._params]
        if unknown:
            raise ValueError(f"unknown parameters for {self.model}: {unknown}")
        validated = {}
        for name, value in updates.items():
            value = _finite_scalar(value, name)
            lower, upper = _BOUNDS[name]
            if not lower <= value <= upper:
                raise ValueError(f"{name} must satisfy {lower} <= {name} <= {upper}")
            validated[name] = value
        self._params.update(validated)

    def clone(self):
        return deepcopy(self)

    def advance_to(self, target):
        """Advance existing state to a finite, nondecreasing exact time boundary."""
        target = _finite_scalar(target, "target")
        if target < self.t:
            raise ValueError("target must be at or after the current time")
        try:
            with np.errstate(over="raise", invalid="raise", divide="raise"):
                while self.t < target:
                    _check_finite(self.state)
                    remaining = target - self.t
                    dt = min(self._time_step(), remaining)
                    if not np.isfinite(dt) or dt <= 0:
                        raise RuntimeError("No finite positive stable timestep")
                    next_t = target if dt == remaining else self.t + dt
                    if next_t <= self.t:
                        raise RuntimeError("Stable timestep is below clock precision")
                    state = self._step(dt)
                    _check_finite(state)
                    self.state, self.t = state, next_t
                    self.steps += 1
        except FloatingPointError as exc:
            raise RuntimeError("Nonfinite arithmetic in evolution; run rejected") from exc
        return self

    def diagnostics(self):
        result = {"time": self.t, "steps": self.steps, **self._diagnostics()}
        if not all(np.isfinite(value) for value in result.values()):
            raise RuntimeError("Nonfinite diagnostic; run rejected")
        return result


class _VorticityStepper(_Stepper):
    dimension = 2

    def __init__(self, model, n, parameters, kind):
        super().__init__(model, n, parameters, kind)
        self.x = np.arange(n) * 2 * np.pi / n
        self.y = self.x.copy()
        X, Y = np.meshgrid(self.x, self.y, indexing="xy")
        k = np.fft.fftfreq(n, 1 / n)
        self._kx, self._ky = np.meshgrid(k, k, indexing="xy")
        self._k2 = self._kx**2 + self._ky**2
        self._invk2 = np.zeros_like(self._k2)
        self._invk2[self._k2 > 0] = 1 / self._k2[self._k2 > 0]
        radius = np.maximum(abs(self._kx), abs(self._ky))
        self._mask = radius < n / 3  # strict 2/3 square, including at n divisible by 3
        self._max_k2 = float(self._k2[self._mask].max())
        self._tail = self._mask & (radius > (2 / 3) * radius[self._mask].max())
        w = np.sin(Y) if kind == "shear" else 2 * np.sin(X) * np.sin(Y)
        if kind == "interacting":
            w += np.cos(2 * X) * np.cos(Y) + .75 * np.sin(X) * np.cos(2 * Y)
        self.state = np.fft.fft2(w) * self._mask

    @staticmethod
    def _real(spectrum):
        return np.fft.ifft2(spectrum).real

    def _mean(self):
        return (.3, -.2) if self.model == "oseen" else (0., 0.)

    def _velocity(self, w):
        a, b = self._mean()
        psi = w * self._invk2
        return a + self._real(1j * self._ky * psi), b - self._real(1j * self._kx * psi)

    def _time_step(self):
        u, v = self._velocity(self.state)
        speed = max(np.max(abs(u) + abs(v)), 1e-12)
        if self.model == "oseen":
            speed = max(speed, abs(self._params["a"]) + abs(self._params["b"]))
        return min(.01, .2 * self.dx / speed,
                   .5 / (self._params["nu"] * self._max_k2))

    def _rhs(self, w):
        _check_finite(w)
        nu = self._params["nu"]
        if self.model == "oseen":
            a, b = self._params["a"], self._params["b"]
            return (-nu * self._k2 - 1j * (a * self._kx + b * self._ky)) * w
        u, v = self._velocity(w)
        advection = u * self._real(1j * self._kx * w) + v * self._real(1j * self._ky * w)
        return -np.fft.fft2(advection) * self._mask - nu * self._k2 * w

    def _step(self, dt):
        w = self.state
        a = self._rhs(w)
        b = self._rhs(w + dt * a / 2)
        c = self._rhs(w + dt * b / 2)
        d = self._rhs(w + dt * c)
        return (w + dt * (a + 2 * b + 2 * c + d) / 6) * self._mask

    def fields(self):
        _check_finite(self.state)
        u, v = self._velocity(self.state)
        return {"u": u, "v": v, "vorticity": self._real(self.state),
                "speed": np.sqrt(u * u + v * v)}

    def _diagnostics(self):
        fields = self.fields()
        u, v, w = fields["u"], fields["v"], fields["vorticity"]
        divergence = self._real(1j * self._kx * np.fft.fft2(u) +
                                1j * self._ky * np.fft.fft2(v))
        # Fraction of vorticity power in the outer third of the retained square.
        return {"kinetic_energy": float(.5 * (u * u + v * v).mean()),
                "enstrophy": float(.5 * (w * w).mean()),
                "divergence_max": float(abs(divergence).max()),
                "vorticity_mean": float(w.mean()),
                "spectral_tail_ratio": _tail_ratio(self.state * self._mask, self._tail)}


class _SVEStepper(_Stepper):
    dimension = 1

    def __init__(self, model, n, parameters, kind):
        super().__init__(model, n, parameters, kind)
        self.x, self.y = (np.arange(n) + .5) * self.dx, None
        h = 1 + .03 * np.cos(self.x) * np.sinc(self.dx / (2 * np.pi))
        u = .4 + .02 * np.sin(self.x) * np.sinc(self.dx / (2 * np.pi))
        bed = .015 * np.cos(2 * self.x) * np.sinc(self.dx / np.pi)
        self.state = np.array([h, h * u, bed])
        self._initial_depth, self._initial_bed = h.mean(), bed.mean()
        self._tail = abs(np.fft.fftfreq(n, 1 / n)) > (2 / 3) * (n / 2)

    @staticmethod
    def _primitives(U):
        _check_finite(U)
        if U[0].min() <= 0:
            raise RuntimeError("SVE lost finite positive depth; run rejected")
        velocity = U[1] / U[0]
        if not np.all(np.isfinite(velocity)) or velocity.min() <= 0:
            raise RuntimeError("SVE left the declared positive-velocity power branch")
        return U[0], velocity, U[2]

    def _speed_bound(self, U):
        h, u, _ = self._primitives(U)
        m, kappa, g = (self._params[key] for key in ("m", "kappa", "g"))
        # Infinity norm of the primitive quasilinear matrix, as in the baseline.
        return float(max(np.max(abs(u) + h), np.max(abs(u) + 2 * g),
                         np.max(kappa * m * u**(m - 1))))

    def _time_step(self):
        return .25 * self.dx / self._speed_bound(self.state)

    def _rhs(self, U):
        h, u, bed = self._primitives(U)
        m, kappa, g = (self._params[key] for key in ("m", "kappa", "g"))
        flux = np.array([U[1], U[1] * u + .5 * g * h**2, kappa * u**m])
        face = (.5 * (flux + np.roll(flux, -1, axis=1)) -
                .5 * self._speed_bound(U) * (np.roll(U, -1, axis=1) - U))
        rate = -(face - np.roll(face, 1, axis=1)) / self.dx
        rate[1] -= g * h * (np.roll(bed, -1) - np.roll(bed, 1)) / (2 * self.dx)
        return rate

    def _step(self, dt):
        U = self.state
        a = U + dt * self._rhs(U)
        b = .75 * U + .25 * (a + dt * self._rhs(a))
        result = U / 3 + 2 * (b + dt * self._rhs(b)) / 3
        self._primitives(result)
        return result

    def fields(self):
        h, u, bed = self._primitives(self.state)
        return {"h": h.copy(), "u": u, "bed": bed.copy(), "surface": h + bed}

    def _diagnostics(self):
        h, u, bed = self._primitives(self.state)
        spectrum = np.fft.fft(self.state, axis=1)
        spectrum[:, 0] = 0  # Fluctuation power; conserved constant modes excluded.
        return {"mean_depth": float(h.mean()), "mean_bed": float(bed.mean()),
                "minimum_depth": float(h.min()), "minimum_velocity": float(u.min()),
                "mass_relative_drift": float(abs(h.mean() - self._initial_depth) / self._initial_depth),
                "bed_mean_absolute_drift": float(abs(bed.mean() - self._initial_bed)),
                "spectral_tail_ratio": _tail_ratio(spectrum, self._tail)}


def make_stepper(model="ns", n=64, parameters=None, kind="interacting"):
    """Create a persistent periodic solver; grid size is a multiple of 8, 24..256.

    Oseen's advection coefficients (a, b) default to (.3, -.2). Its reconstructed
    velocity mean is fixed at (.3, -.2); NS has zero means. SVE supports only the original
    periodic initial condition (kind='interacting'). Fields are detached float64
    snapshots; x/y are one-dimensional grid coordinates on [0, 2*pi).
    """
    if not isinstance(model, str) or model not in _DEFAULTS:
        raise ValueError("model must be 'ns', 'oseen', or 'sve'")
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, Integral) or not 24 <= n <= 256 or n % 8:
        raise ValueError("n must be an integer multiple of 8 between 24 and 256")
    if kind not in ("interacting", "shear", "taylor_green") or (model == "sve" and kind != "interacting"):
        raise ValueError("unknown initial field for this model")
    cls = _SVEStepper if model == "sve" else _VorticityStepper
    return cls(model, int(n), parameters, kind)
