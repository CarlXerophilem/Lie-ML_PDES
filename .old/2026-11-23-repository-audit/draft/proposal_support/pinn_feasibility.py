"""Bounded pre-study CPU feasibility check, not the planned 2027 experiment."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch
from torch import nn

from verify_lagrange import coefficients, reference, solve, taylor_coefficients


def derivative(value, variable):
    return torch.autograd.grad(value.sum(), variable, create_graph=True)[0]


class Profile(nn.Module):
    def __init__(self, order, initial, seed=0):
        super().__init__()
        if order not in (2, 4):
            raise ValueError("Only the declared order-2/order-4 trials are supported")
        torch.manual_seed(seed)
        self.order = order
        self.net = nn.Sequential(nn.Linear(1, 16), nn.Tanh(), nn.Linear(16, 16), nn.Tanh(), nn.Linear(16, 1)).double()
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)
        self.register_buffer("polynomial", torch.tensor(taylor_coefficients(initial)[:order + 1], dtype=torch.float64))

    def forward(self, sigma):
        z = sigma - 1
        p = sum(coefficient * z**k for k, coefficient in enumerate(self.polynomial))
        return p + z**(self.order + 1) * self.net(4 * z - 1)


def profile_jets(model, sigma):
    value = model(sigma)
    r = derivative(value, sigma)
    v = derivative(r, sigma)
    third = derivative(v, sigma)
    return value, r, v, third


def residuals(model, sigma):
    value, r, v, third = profile_jets(model, sigma)
    a, b = coefficients(sigma, r, v)
    if not all(torch.isfinite(x).all().item() for x in (value, r, v, third, a, b)):
        raise ValueError("Nonfinite profile or residual coefficient")
    if (r <= 0).any().item() or (a.abs() < 1e-6).any().item():
        raise ValueError("Sampled regularity check failed")
    return value, r, v, third + b / a, a * third + b, a


def original_master_check(model):
    tgrid, sigmagrid = np.meshgrid(np.linspace(1, 1.25, 11), np.linspace(1, 1.5, 11), indexing="ij")
    t = torch.tensor(tgrid.reshape(-1, 1), dtype=torch.float64, requires_grad=True)
    s = torch.tensor((sigmagrid / tgrid**2).reshape(-1, 1), dtype=torch.float64, requires_grad=True)
    phi = model(s * t**2)
    ps, pt = derivative(phi, s), derivative(phi, t)
    pss, ptt, pts = derivative(ps, s), derivative(pt, t), derivative(pt, s)
    A = ps * ptt - pss / ps**2
    original = derivative(A, t) - 0.1 * derivative(pt**2 * pts / ps, s)
    sigma = torch.tensor(sigmagrid.reshape(-1, 1), dtype=torch.float64, requires_grad=True)
    _, _, _, _, reduced, _ = residuals(model, sigma)
    lifted = reduced / t.detach()
    return {
        "direct_master_max_abs": float(original.detach().abs().max()),
        "direct_vs_lift_max_abs": float((original.detach() - lifted.detach()).abs().max()),
        "grid_shape": [11, 11],
    }


def evaluate(model, initial):
    # Midpoints do not coincide with the 128 uniform training points.
    x = 1 + (np.arange(1001) + 0.5) * 0.5 / 1001
    sigma = torch.tensor(x[:, None], dtype=torch.float64, requires_grad=True)
    value, r, v, normalized, raw, a = residuals(model, sigma)
    target = solve(initial).sol(x)
    predicted = np.stack([x.detach().numpy().ravel() for x in (value, r, v)])
    start = torch.ones((1, 1), dtype=torch.float64, requires_grad=True)
    jets = profile_jets(model, start)[:3]
    result = {
        "max_profile_error": float(np.max(np.abs(predicted[0] - target[0]))),
        "max_state_error": float(np.max(np.abs(predicted - target))),
        "max_normalized_defect": float(normalized.detach().abs().max()),
        "max_raw_reduced_residual": float(raw.detach().abs().max()),
        "sampled_min_r": float(r.detach().min()),
        "sampled_min_abs_a": float(a.detach().abs().min()),
        "initial_jet_max_error": float(np.max(np.abs(np.array([j.detach().item() for j in jets]) - initial))),
    }
    result.update(original_master_check(model))
    return result


def run_case(order, steps):
    initial = reference(1.0).copy()
    initial[2] *= 1.01
    model = Profile(order, initial)
    before = evaluate(model, initial)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    start = time.perf_counter()
    for _ in range(steps):
        optimizer.zero_grad(set_to_none=True)
        sigma = torch.linspace(1, 1.5, 128, dtype=torch.float64).reshape(-1, 1).requires_grad_()
        *_, normalized, raw, a = residuals(model, sigma)
        loss = normalized.square().mean()
        loss.backward()
        if not all(p.grad is None or torch.isfinite(p.grad).all().item() for p in model.parameters()):
            raise ValueError("Nonfinite optimizer gradient")
        optimizer.step()
    runtime = time.perf_counter() - start
    after = evaluate(model, initial)
    return {"order": order, "seed": 0, "adam_steps": steps, "parameter_count": sum(p.numel() for p in model.parameters()), "training_seconds": runtime, "before": before, "after": after, "status": "completed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=400)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be positive")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    cases = []
    for order in (2, 4):
        try:
            cases.append(run_case(order, args.steps))
        except (ValueError, RuntimeError) as exc:
            cases.append({"order": order, "status": "failed", "reason": str(exc)})
    passed = all(c["status"] == "completed" and c["after"]["direct_vs_lift_max_abs"] < 1e-9 for c in cases)
    source = Path(__file__)
    report = {
        "schema": "lieml.pinn-feasibility.v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "feasibility-only" if passed else "failed",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "coefficient_source_sha256": hashlib.sha256(source.with_name("verify_lagrange.py").read_bytes()).hexdigest(),
        "torch_version": torch.__version__,
        "device": "cpu", "dtype": "float64", "threads": 1,
        "training_points": 128, "evaluation_points": 1001,
        "evaluation_grid": "midpoints, separate from training endpoints",
        "formal_2027_study_completed": False,
        "interval_certified": False,
        "cases": cases,
    }
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        if passed:
            rows = []
            for case in cases:
                def tex(value):
                    mantissa, exponent = f"{value:.2e}".split("e")
                    return f"{mantissa}\\times10^{{{int(exponent)}}}"
                rows.append(f"{case['order']} & ${tex(case['before']['max_profile_error'])}$ & ${tex(case['after']['max_profile_error'])}$ & ${tex(case['after']['max_normalized_defect'])}$ & {case['training_seconds']:.2f} \\\\")
            (args.output_dir / "table.tex").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
