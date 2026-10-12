"""Tolerance-qualified IVP references and exact dense-polynomial derivatives."""
from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
import warnings
from typing import Any

import numpy as np
from numpy.polynomial import Polynomial
from scipy.integrate import solve_ivp

from .problems import ProfileProblem


@dataclass
class ReferenceSolution:
    problem: ProfileProblem
    solution: Any
    method: str
    requested_rtol: float
    effective_rtol: float
    warnings: tuple[str, ...]
    setup_seconds: float
    integrated: bool

    def state_jets(self, points: np.ndarray) -> np.ndarray:
        state = self.solution.sol(points)
        if self.integrated:
            curvature = self.problem.integral/self.problem.leading(points, state[0], state[1])
            state = np.vstack((state, curvature))
        h = self.problem.third_derivative(points, *state[:3])
        return np.vstack((state[:3], h))

    def profile(self, points: np.ndarray) -> np.ndarray:
        return self.solution.sol(points)[0]

    def dense_jets(self, points: np.ndarray) -> np.ndarray:
        """Differentiate the actual SciPy scalar dense interpolant.

        DOP853 is degree seven and Radau degree three. Their third derivatives
        need not have the accuracy of the integrated state. Internal structure
        is checked explicitly and covered by regression tests; no finite
        difference or substitution of the RHS is called an interpolant defect.
        """
        dense = self.solution.sol
        indices = np.clip(np.searchsorted(dense.ts, points, side="left")-1, 0,
                          len(dense.interpolants)-1)
        result = np.empty((4, len(points)))
        for index in np.unique(indices):
            interpolant = dense.interpolants[int(index)]
            if hasattr(interpolant, "F"):
                polynomial = Polynomial([0.])
                for i, values in enumerate(reversed(interpolant.F)):
                    polynomial += values[0]
                    polynomial *= Polynomial([0., 1.]) if i % 2 == 0 else Polynomial([1., -1.])
                polynomial += interpolant.y_old[0]
            elif hasattr(interpolant, "Q"):
                polynomial = Polynomial([interpolant.y_old[0], *interpolant.Q[0]])
            else:
                raise NotImplementedError("unsupported SciPy dense interpolant structure")
            mask = indices == index
            x = (points[mask]-interpolant.t_old)/interpolant.h
            for order in range(4):
                result[order, mask] = polynomial.deriv(order)(x)/interpolant.h**order
        return result


def solve_reference(problem: ProfileProblem, method: str = "DOP853", *, rtol: float = 1e-12,
                    atol: float = 1e-14, integrated: bool = False) -> ReferenceSolution:
    if method not in ("DOP853", "Radau"):
        raise ValueError("reference method must be DOP853 or Radau")
    if integrated and problem.integral is None:
        raise ValueError("the cubic X5 chart does not use the common-scaling integral")
    effective = max(rtol, 100*np.finfo(float).eps)

    def rhs(z: float, state: np.ndarray) -> list[float]:
        f, p = state[:2]
        velocity = 2*z*p if problem.chart == "cubic_X5" else f-z*p
        lead = float(problem.leading(z, f, p))
        if p <= 0 or velocity <= 0 or abs(lead) < 1e-9:
            raise ValueError("reference left the declared regular positive branch")
        if integrated:
            return [p, float(problem.integral/lead)]
        return [p, state[2], float(problem.third_derivative(z, f, p, state[2]))]

    started = perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        solution = solve_ivp(rhs, problem.interval, problem.initial[:2] if integrated else problem.initial,
                             method=method, rtol=rtol, atol=atol, dense_output=True, max_step=.02)
    if not solution.success:
        raise RuntimeError(solution.message)
    return ReferenceSolution(problem, solution, method, rtol, effective,
                             tuple(str(w.message) for w in caught), perf_counter()-started, integrated)
