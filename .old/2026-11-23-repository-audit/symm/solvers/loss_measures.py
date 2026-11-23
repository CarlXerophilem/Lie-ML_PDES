"""Quotient measures, exact differential linearization, and directional losses."""
from __future__ import annotations

from typing import Callable
import numpy as np
import torch

from .problems import ProfileProblem


def quotient_metric(multiplier: np.ndarray, jacobian: np.ndarray, orbit_weights: np.ndarray) -> np.ndarray:
    """Integrate M^T M |J| along the first (orbit) axis."""
    multiplier = np.asarray(multiplier)
    if multiplier.ndim < 3 or len(multiplier) != len(orbit_weights):
        raise ValueError("M must have shape (orbit, ..., original residual, reduced residual)")
    if np.any(orbit_weights < 0) or np.any(~np.isfinite(jacobian)):
        raise ValueError("invalid orbit quadrature")
    gram = np.einsum("...ai,...aj->...ij", multiplier, multiplier)
    weight = np.asarray(orbit_weights).reshape((-1,)+(1,)*(gram.ndim-1))
    return np.sum(gram*np.abs(np.asarray(jacobian))[..., None, None]*weight, axis=0)


def profile_jets(profile: torch.Tensor, z: torch.Tensor) -> tuple[torch.Tensor, ...]:
    values = [profile]
    for _ in range(3):
        values.append(torch.autograd.grad(values[-1].sum(), z, create_graph=True)[0])
    return tuple(values)


def differential_linearization(problem: ProfileProblem, z: torch.Tensor,
                              jets: tuple[torch.Tensor, ...], tangents: tuple[torch.Tensor, ...],
                              exponent: torch.Tensor | None = None) -> torch.Tensor:
    return sum(partial*tangent for partial, tangent in zip(
        problem.partials(z, *jets, exponent=exponent), tangents))


def quotient_loss(problem: ProfileProblem, z: torch.Tensor, jets: tuple[torch.Tensor, ...],
                  quadrature: torch.Tensor, *, exponent: torch.Tensor | None = None,
                  metric: Callable[[tuple[torch.Tensor, ...]], torch.Tensor] | None = None) -> torch.Tensor:
    residual = problem.residual(z, *jets, exponent=exponent)
    weight = problem.weight if metric is None else metric(jets)
    return (quadrature*weight*residual.square()).sum()


def directional_loss(problem: ProfileProblem, z: torch.Tensor, jets: tuple[torch.Tensor, ...],
                     tangents: tuple[torch.Tensor, ...], quadrature: torch.Tensor,
                     *, metric: torch.Tensor | float | None = None,
                     metric_direction: torch.Tensor | float = 0.) -> torch.Tensor:
    residual = problem.residual(z, *jets)
    linearized = differential_linearization(problem, z, jets, tangents)
    weight = problem.weight if metric is None else metric
    return (quadrature*(2*weight*residual*linearized+metric_direction*residual.square())).sum()


def parameter_directional_loss(model: torch.nn.Module, z: torch.Tensor,
                               quadrature: torch.Tensor, directions: tuple[torch.Tensor, ...]) -> torch.Tensor:
    """D_theta L from D_F R and an AD Jacobian-vector product of the network."""
    parameters = tuple(model.named_parameters())
    if len(directions) != len(parameters):
        raise ValueError("one tangent is needed for each named network parameter")
    from torch.func import functional_call

    def evaluate(*values: torch.Tensor) -> torch.Tensor:
        return functional_call(model, dict(zip((name for name, _ in parameters), values)), (z,))

    profile, tangent = torch.autograd.functional.jvp(
        evaluate, tuple(p for _, p in parameters), directions, create_graph=True)
    return directional_loss(model.problem, z, profile_jets(profile, z),
                            profile_jets(tangent, z), quadrature)
