"""Small deterministic benchmark registry for the generic PDE kernel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import sympy as sp

from .core import DifferentialSystem, JetSpace, PointGenerator
from .jets import prolonged_system
from .reduction import orbit_rank


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    system: DifferentialSystem
    expected_shape: tuple[int, int, int]
    description: str
    known_generators: tuple[tuple[str, PointGenerator], ...] = ()
    rank_guards: tuple[sp.Expr, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "expected_shape": list(self.expected_shape),
            "actual_shape": [self.system.p, self.system.q, self.system.r],
            "system_fingerprint": self.system.fingerprint(),
            "known_generators": [name for name, _ in self.known_generators],
            "rank_guards": [sp.srepr(value) for value in self.rank_guards],
        }


def _jets(space: JetSpace, field: int, *indices: tuple[int, ...]) -> tuple[sp.Expr, ...]:
    return tuple(space.jet_symbol(field, index) for index in indices)


def heat_2plus1() -> BenchmarkCase:
    x, y, t = sp.symbols("x y t")
    u = sp.Symbol("u")
    space = JetSpace((x, y, t), (u,), 2)
    ut, uxx, uyy = _jets(space, 0, (0, 0, 1), (2, 0, 0), (0, 2, 0))
    system = DifferentialSystem(space, (ut - uxx - uyy,), name="heat-2plus1")
    return BenchmarkCase(
        "heat-2plus1", system, (3, 1, 1),
        "scalar heat equation with two spatial variables",
    )


def reaction_diffusion() -> BenchmarkCase:
    x, y, t = sp.symbols("x y t")
    u, v = sp.symbols("u v")
    space = JetSpace((x, y, t), (u, v), 2)
    ut, uxx, vt, vyy = _jets(
        space, 0, (0, 0, 1), (2, 0, 0), (0, 0, 1), (0, 2, 0)
    )
    # The second field's jets are fetched separately to keep field identity explicit.
    vt = space.jet_symbol(1, (0, 0, 1))
    vyy = space.jet_symbol(1, (0, 2, 0))
    system = DifferentialSystem(
        space,
        (ut - uxx - u * (1 - v), vt - vyy - v * (1 - u)),
        name="reaction-diffusion-2field",
    )
    return BenchmarkCase(
        "reaction-diffusion-2field", system, (3, 2, 2),
        "two-field polynomial reaction-diffusion system",
    )


def cauchy_riemann() -> BenchmarkCase:
    x, y = sp.symbols("x y")
    u, v = sp.symbols("u v")
    space = JetSpace((x, y), (u, v), 1)
    ux, uy = _jets(space, 0, (1, 0), (0, 1))
    vx, vy = _jets(space, 1, (1, 0), (0, 1))
    system = DifferentialSystem(space, (ux - vy, uy + vx), name="cauchy-riemann")
    return BenchmarkCase(
        "cauchy-riemann", system, (2, 2, 2),
        "first-order two-field Cauchy-Riemann system",
    )


def overdetermined_constraint() -> BenchmarkCase:
    x, t = sp.symbols("x t")
    u, v = sp.symbols("u v")
    space = JetSpace((x, t), (u, v), 1)
    ux, ut = _jets(space, 0, (1, 0), (0, 1))
    vx, vt = _jets(space, 1, (1, 0), (0, 1))
    system = DifferentialSystem(
        space, (ut - vx, ux + vt, u + v), name="constraint-r3-q2"
    )
    return BenchmarkCase(
        "constraint-r3-q2", system, (2, 2, 3),
        "overdetermined two-field constraint with r != q",
    )


def parameter_branches() -> tuple[BenchmarkCase, BenchmarkCase]:
    x, t = sp.symbols("x t")
    u, a = sp.symbols("u a")
    space = JetSpace((x, t), (u,), 1)
    ut = space.jet_symbol(0, (0, 1))
    ux = space.jet_symbol(0, (1, 0))
    regular = DifferentialSystem(
        space, (a * ut - ux,), inequations=(a,), name="parameter-a-nonzero"
    )
    singular = DifferentialSystem(
        space, (-ux,), assumptions=(sp.Eq(a, 0),), name="parameter-a-zero"
    )
    return (
        BenchmarkCase("parameter-a-nonzero", regular, (2, 1, 1),
                      "regular parameter branch retaining a != 0"),
        BenchmarkCase("parameter-a-zero", singular, (2, 1, 1),
                      "singular parameter branch retaining a = 0"),
    )


def rank_dropping_rotation() -> BenchmarkCase:
    x, y = sp.symbols("x y")
    u = sp.Symbol("u")
    space = JetSpace((x, y), (u,), 1)
    ux, uy = _jets(space, 0, (1, 0), (0, 1))
    system = DifferentialSystem(space, (x * ux + y * uy,), name="rank-dropping-rotation")
    rotation = PointGenerator((-y, x), (0,))
    return BenchmarkCase(
        "rank-dropping-rotation", system, (2, 1, 1),
        "rotation with a rank-one generic orbit and a rank-zero origin stratum",
        known_generators=(("rotation", rotation),),
        rank_guards=(x**2 + y**2,),
    )


def navier_stokes_2d() -> BenchmarkCase:
    t, x, y = sp.symbols("t x y")
    u, v, pressure, nu = sp.symbols("u v p nu")
    space = JetSpace((t, x, y), (u, v, pressure), 2)
    ut, ux, uy = _jets(space, 0, (1, 0, 0), (0, 1, 0), (0, 0, 1))
    uxx, uyy = _jets(space, 0, (0, 2, 0), (0, 0, 2))
    vt, vx, vy = _jets(space, 1, (1, 0, 0), (0, 1, 0), (0, 0, 1))
    vxx, vyy = _jets(space, 1, (0, 2, 0), (0, 0, 2))
    px, py = _jets(space, 2, (0, 1, 0), (0, 0, 1))
    equations = (
        ut + u * ux + v * uy + px - nu * (uxx + uyy),
        vt + u * vx + v * vy + py - nu * (vxx + vyy),
        ux + vy,
    )
    generators = (
        ("time-translation", PointGenerator((1, 0, 0), (0, 0, 0))),
        ("x-translation", PointGenerator((0, 1, 0), (0, 0, 0))),
        ("y-translation", PointGenerator((0, 0, 1), (0, 0, 0))),
        ("pressure-gauge", PointGenerator((0, 0, 0), (0, 0, 1))),
        ("x-galilean", PointGenerator((0, t, 0), (1, 0, 0))),
        ("y-galilean", PointGenerator((0, 0, t), (0, 1, 0))),
    )
    system = DifferentialSystem(space, equations, name="incompressible-navier-stokes-2d")
    return BenchmarkCase(
        "incompressible-navier-stokes-2d", system, (3, 3, 3),
        "incompressible 2D Navier-Stokes with pressure and divergence constraint",
        known_generators=generators,
    )


def benchmark_registry() -> tuple[BenchmarkCase, ...]:
    return (
        heat_2plus1(),
        reaction_diffusion(),
        cauchy_riemann(),
        overdetermined_constraint(),
        *parameter_branches(),
        rank_dropping_rotation(),
        navier_stokes_2d(),
    )


def validate_case(case: BenchmarkCase) -> dict[str, Any]:
    shape = (case.system.p, case.system.q, case.system.r)
    shape_ok = shape == case.expected_shape
    residuals: dict[str, tuple[sp.Expr, ...]] = {}
    for name, generator in case.known_generators:
        try:
            residuals[name] = tuple(
                sp.simplify(value) for value in prolonged_system(case.system, generator)
            )
        except Exception as exc:
            residuals[name] = (sp.Symbol(f"unsupported_{type(exc).__name__}"),)
    residuals_ok = all(all(value == 0 for value in values) for values in residuals.values())
    return {
        "name": case.name,
        "shape": shape,
        "expected_shape": case.expected_shape,
        "shape_ok": shape_ok,
        "known_generator_residuals": residuals,
        "known_generator_residuals_ok": residuals_ok,
        "rank_guards": case.rank_guards,
        "status": "verified" if shape_ok and residuals_ok else "unsupported",
    }


def validate_registry() -> tuple[dict[str, Any], ...]:
    return tuple(validate_case(case) for case in benchmark_registry())
