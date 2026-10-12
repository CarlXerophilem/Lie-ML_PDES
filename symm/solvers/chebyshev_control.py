"""Square nonlinear Chebyshev collocation with an exact Cauchy-data lift."""
from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
from numpy.polynomial import Chebyshev, Polynomial
from scipy.optimize import root

from .problems import ProfileProblem


@dataclass
class SpectralSolution:
    problem: ProfileProblem
    polynomial: Chebyshev
    degree: int
    setup_seconds: float
    optimizer_success: bool
    collocation_max_residual: float
    evaluations: int

    def jets(self, points: np.ndarray) -> np.ndarray:
        return np.array([self.polynomial.deriv(order)(points) for order in range(4)])

    def profile(self, points: np.ndarray) -> np.ndarray:
        return self.polynomial(points)


def solve_chebyshev(problem: ProfileProblem, degree: int = 16) -> SpectralSolution:
    if degree < 4:
        raise ValueError("spectral degree must be at least four")
    started = perf_counter()
    a, b = problem.interval
    displacement = Polynomial([-a, 1.])
    f0, p0, c0 = problem.initial
    prior = (f0+p0*displacement+c0/2*displacement**2).convert(kind=Chebyshev, domain=(a, b))
    lift = (displacement**3).convert(kind=Chebyshev, domain=(a, b))
    basis = [lift*Chebyshev.basis(i, domain=(a, b)) for i in range(degree-2)]
    # Gauss points: degree-2 unknown remainder coefficients and equations.
    x = np.cos(np.pi*(np.arange(degree-2)+.5)/(degree-2))
    points = (a+b)/2+(b-a)*x/2
    matrices = np.array([[poly.deriv(order)(points) for poly in basis] for order in range(4)])
    priors = np.array([prior.deriv(order)(points) for order in range(4)])

    def values(coefficients: np.ndarray) -> np.ndarray:
        return priors+np.einsum("okn,k->on", matrices, coefficients)

    def residual(coefficients: np.ndarray) -> np.ndarray:
        jets = values(coefficients)
        guards = problem.guards(points, jets)
        if any(not np.isfinite(v) or v <= 1e-10 for v in guards.values()):
            return np.full(len(points), 1e10)+coefficients
        return np.asarray(problem.residual(points, *jets), dtype=float)

    def jacobian(coefficients: np.ndarray) -> np.ndarray:
        jets = values(coefficients)
        partials = np.array([np.broadcast_to(partial, points.shape)
                             for partial in problem.partials(points, *jets)])
        return np.einsum("on,okn->nk", partials, matrices)

    outcome = root(residual, np.zeros(degree-2), jac=jacobian, method="hybr",
                   options={"xtol": 1e-10, "maxfev": 500})
    maximum = float(np.max(np.abs(residual(outcome.x))))
    if not np.isfinite(maximum) or maximum > 1e-6:
        raise RuntimeError(f"Chebyshev collocation did not solve the system: {outcome.message}; residual={maximum}")
    polynomial = prior+sum((c*poly for c, poly in zip(outcome.x, basis)),
                           Chebyshev([0.], domain=(a, b)))
    return SpectralSolution(problem, polynomial, degree, perf_counter()-started,
                            bool(outcome.success), maximum, int(outcome.nfev))
