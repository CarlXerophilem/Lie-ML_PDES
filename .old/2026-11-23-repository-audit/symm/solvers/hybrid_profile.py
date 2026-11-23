"""Float64 CPU hard-data PINN and smooth polynomial-edge KAN remainders."""
from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any
import copy

import numpy as np
import torch
from torch import nn

from .loss_measures import profile_jets, quotient_loss
from .problems import ProfileProblem


class PolynomialEdge(nn.Module):
    """Trainable sums of Chebyshev-polynomial edge functions, without knots."""
    def __init__(self, inputs: int, outputs: int, degree: int = 5) -> None:
        super().__init__()
        self.degree = degree
        self.coefficients = nn.Parameter(.02*torch.randn(outputs, inputs, degree+1, dtype=torch.float64))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        terms = [torch.ones_like(x), x]
        for _ in range(2, self.degree+1):
            terms.append(2*x*terms[-1]-terms[-2])
        return torch.einsum("nid,oid->no", torch.stack(terms, dim=-1), self.coefficients)


class HardProfile(nn.Module):
    def __init__(self, problem: ProfileProblem, kind: str = "PINN", *, conditioned: bool = False,
                 seed: int = 17) -> None:
        super().__init__()
        torch.manual_seed(seed)
        self.problem, self.kind, self.conditioned = problem, kind, conditioned
        inputs = 3 if conditioned else 1
        if kind == "PINN":
            self.network = nn.Sequential(nn.Linear(inputs, 12), nn.Tanh(), nn.Linear(12, 12),
                                         nn.Tanh(), nn.Linear(12, 1)).double()
            nn.init.zeros_(self.network[-1].weight)
            nn.init.zeros_(self.network[-1].bias)
        elif kind == "PIKAN":
            self.network = nn.Sequential(PolynomialEdge(inputs, 8 if conditioned else 16),
                                         PolynomialEdge(8 if conditioned else 16, 1))
            nn.init.zeros_(self.network[-1].coefficients)
        else:
            raise ValueError("kind must be PINN or PIKAN")

    def forward(self, z: torch.Tensor, exponent: torch.Tensor | None = None,
                eta: torch.Tensor | None = None) -> torch.Tensor:
        m = torch.full_like(z, self.problem.exponent) if exponent is None else exponent
        perturbation = torch.full_like(z, self.problem.eta) if eta is None else eta
        f0, p0, c0 = self.problem.initial
        if self.conditioned:
            if self.problem.chart == "cubic_X5":
                raise ValueError("the parameter-conditioned experiment uses common scaling")
            c0 = .1*(1+perturbation)
        displacement = z-1
        x = 2*displacement/(self.problem.interval[1]-1)-1
        features = torch.stack((x, (m-3)/.1, perturbation/.1), dim=1) if self.conditioned else x[:, None]
        prior = f0+p0*displacement+c0/2*displacement.square()
        return prior+displacement**3*self.network(features).squeeze(1)

    def jets(self, points: np.ndarray, *, exponent: float | None = None,
             eta: float | None = None) -> np.ndarray:
        z = torch.tensor(points, dtype=torch.float64, requires_grad=True)
        m = None if exponent is None else torch.full_like(z, exponent)
        a = None if eta is None else torch.full_like(z, eta)
        values = profile_jets(self(z, m, a), z)
        return np.array([value.detach().numpy() for value in values])

    def profile(self, points: np.ndarray, *, exponent: float | None = None,
                eta: float | None = None) -> np.ndarray:
        with torch.no_grad():
            z = torch.tensor(points, dtype=torch.float64)
            m = None if exponent is None else torch.full_like(z, exponent)
            a = None if eta is None else torch.full_like(z, eta)
            return self(z, m, a).numpy()


@dataclass
class TrainingOutcome:
    model: HardProfile
    seconds: float
    adam_updates: int
    lbfgs_evaluations: int
    status: str
    best_loss: float
    parameter_count: int


class _BudgetStop(Exception):
    pass


def train_profile(problem: ProfileProblem, kind: str = "PINN", *, seed: int = 17,
                  conditioned: bool = False, adam_steps: int = 500, lbfgs_evaluations: int = 250,
                  seconds_limit: float = 120., nodes: int = 32) -> TrainingOutcome:
    torch.set_num_threads(1)
    model = HardProfile(problem, kind, conditioned=conditioned, seed=seed)
    abscissae, weights = np.polynomial.legendre.leggauss(nodes)
    a, b = problem.interval
    grid = a+(abscissae+1)*(b-a)/2
    weights = weights*(b-a)/2
    parameter_pairs = [(m, eta) for m in (2.9, 3.1) for eta in (-.1, 0., .1)] if conditioned else [(problem.exponent, problem.eta)]
    z = torch.tensor(np.tile(grid, len(parameter_pairs)), dtype=torch.float64, requires_grad=True)
    quadrature = torch.tensor(np.tile(weights, len(parameter_pairs))/len(parameter_pairs), dtype=torch.float64)
    m = torch.tensor(np.repeat([p[0] for p in parameter_pairs], nodes), dtype=torch.float64)
    eta = torch.tensor(np.repeat([p[1] for p in parameter_pairs], nodes), dtype=torch.float64)
    started = perf_counter()
    best_loss, best_state = float("inf"), copy.deepcopy(model.state_dict())
    adam_done, closures = 0, 0
    status = "optimizer-budget-exhausted"

    def evaluate() -> torch.Tensor:
        nonlocal best_loss, best_state
        if perf_counter()-started >= seconds_limit:
            raise _BudgetStop("wall-time-budget-exhausted")
        jets = profile_jets(model(z, m, eta), z)
        slope, velocity = jets[1], jets[0]-z*jets[1]
        if problem.chart == "cubic_X5":
            velocity = 2*z*slope
        if bool((slope <= 0).any()) or bool((velocity <= 0).any()):
            raise _BudgetStop("invalid-iterate-restored")
        leading = problem.leading(z, *jets[:3], exponent=m)
        if bool((leading.abs() <= 1e-9).any()):
            raise _BudgetStop("singular-iterate-restored")
        value = quotient_loss(problem, z, jets, quadrature, exponent=m)
        number = float(value.detach())
        if not np.isfinite(number):
            raise _BudgetStop("nonfinite-iterate-restored")
        if number < best_loss:
            best_loss, best_state = number, copy.deepcopy(model.state_dict())
        return value

    try:
        adam = torch.optim.Adam(model.parameters(), lr=1e-3)
        for _ in range(adam_steps):
            adam.zero_grad()
            loss = evaluate()
            loss.backward()
            adam.step()
            adam_done += 1
        optimizer = torch.optim.LBFGS(model.parameters(), max_iter=lbfgs_evaluations,
                        max_eval=lbfgs_evaluations, line_search_fn="strong_wolfe",
                        tolerance_grad=1e-11, tolerance_change=1e-15)

        def closure() -> torch.Tensor:
            nonlocal closures
            if closures >= lbfgs_evaluations:
                raise _BudgetStop("optimizer-budget-exhausted")
            closures += 1
            optimizer.zero_grad()
            loss = evaluate()
            loss.backward()
            return loss

        optimizer.step(closure)
        # A loss target is distinguished from a solver convergence theorem.
        status = "loss-target-met" if best_loss <= 1e-12 else "optimizer-stopped"
    except _BudgetStop as error:
        status = str(error)
    model.load_state_dict(best_state)
    return TrainingOutcome(model, perf_counter()-started, adam_done, closures, status,
                           best_loss, sum(p.numel() for p in model.parameters()))


def frozen_state(outcome: TrainingOutcome) -> dict[str, Any]:
    return {"kind": outcome.model.kind, "conditioned": outcome.model.conditioned,
            "parameters": {key: value.tolist() for key, value in outcome.model.state_dict().items()},
            "parameter_count": outcome.parameter_count, "best_loss": outcome.best_loss,
            "optimizer_status": outcome.status}
