"""One residual/linearization interface for three separately labelled charts."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any
import sys

import numpy as np
import sympy as sp


def scalar_lab() -> Any:
    path = Path(__file__).resolve().parents[2]/"research_artifacts/sve-progress-20261010"
    # parents[2] is symm's repository parent for symm/solvers/problems.py.
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    from sve_lab import symbolic
    return symbolic


@dataclass(frozen=True)
class ProfileProblem:
    chart: str
    exponent: float = 3.
    eta: float = 0.
    gravity: float = 1.
    kappa: float = 1./30.
    interval: tuple[float, float] = (1., 1.5)

    def __post_init__(self) -> None:
        if self.chart not in ("cubic_X5", "common_printed", "common_corrected"):
            raise ValueError("unknown certified chart")
        if self.chart == "cubic_X5" and self.exponent != 3:
            raise ValueError("the X5 chart is certified only at m=3 with nonzero transport")
        if self.interval[0] != 1 or self.interval[1] <= 1:
            raise ValueError("this constructed benchmark uses z0=1 and positive length")
        if self.gravity <= 0 or self.kappa <= 0 or not np.isfinite(self.eta):
            raise ValueError("invalid benchmark parameters")

    @property
    def initial(self) -> tuple[float, float, float]:
        if self.chart == "cubic_X5":
            denominator = 1-12*self.gravity*self.kappa
            if denominator <= 0:
                raise ValueError("explicit cubic anchor requires 1-12*g*kappa>0")
            amplitude = (27*self.gravity/denominator)**(1/3)
            return 2., amplitude/3, -(1+self.eta)*2*amplitude/9
        return 2., .5, .1*(1+self.eta)

    @property
    def weight(self) -> float:
        return 7/24 if self.chart == "cubic_X5" else 3/8

    @property
    def integral(self) -> float | None:
        if self.chart == "cubic_X5":
            return None
        return float(self.leading(1., *self.initial))*self.initial[2]

    def residual(self, z: Any, *jets: Any, exponent: Any = None) -> Any:
        return compiled(self.chart)[0](z, *jets,
                self.exponent if exponent is None else exponent, self.gravity, self.kappa)

    def partials(self, z: Any, *jets: Any, exponent: Any = None) -> tuple[Any, ...]:
        args = (z, *jets, self.exponent if exponent is None else exponent, self.gravity, self.kappa)
        return tuple(fun(*args) for fun in compiled(self.chart)[1])

    def leading(self, z: Any, f: Any, p: Any, c: Any = 0., exponent: Any = None) -> Any:
        return compiled(self.chart)[2](z, f, p, c, 0.,
                self.exponent if exponent is None else exponent, self.gravity, self.kappa)

    def third_derivative(self, z: Any, f: Any, p: Any, c: Any) -> Any:
        return -self.residual(z, f, p, c, 0.)/self.leading(z, f, p, c)

    def guards(self, z: np.ndarray, jets: np.ndarray) -> dict[str, float]:
        slope = jets[1]
        velocity = 2*z*slope if self.chart == "cubic_X5" else jets[0]-z*slope
        return {"min_slope": float(np.min(slope)), "min_velocity": float(np.min(velocity)),
                "min_abs_leading": float(np.min(np.abs(self.leading(z, *jets[:3]))))}


@lru_cache(maxsize=3)
def expressions(chart: str) -> tuple[tuple[sp.Symbol, ...], sp.Expr, sp.Expr]:
    sy = scalar_lab()
    from sve_lab.jets import m, g, kappa
    z, f, p, c, h = sy.z, sy.f, sy.P, sy.C, sy.H
    if chart == "cubic_X5":
        a = 2*z*p*p+4*z*z*p*c-g*c/p**2
        b = 8*z*z*p*(p+z*c)
        residual = sp.expand(2*z*sy.profile_total(a)-3*g*kappa*sy.profile_total(b))
    else:
        residual = sy.reduced_residual(m, chart == "common_corrected")
    return (z, f, p, c, h, m, g, kappa), residual, sp.diff(residual, h)


@lru_cache(maxsize=3)
def compiled(chart: str) -> tuple[Any, tuple[Any, ...], Any]:
    args, residual, leading = expressions(chart)
    # Algebraic operations also work on PyTorch tensors, preserving their graph.
    return (sp.lambdify(args, residual, cse=True),
            tuple(sp.lambdify(args, sp.diff(residual, value), cse=True) for value in args[1:5]),
            sp.lambdify(args, leading, cse=True))
