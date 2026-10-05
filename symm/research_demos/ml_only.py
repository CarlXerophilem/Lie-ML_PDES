"""ML-only ODE baselines: bounded Duffing TM-PINN and logistic PIKAN.

No Lie-reduction module is imported here. The Duffing study is a fixed-IVP,
CPU directional reproduction, not the paper's full parameter-family study.
"""

from __future__ import annotations

import argparse
import csv
import math
import platform
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp
import torch
from torch import nn

from .schema import sha256, utc_now, write_json


def trainable_parameter_count(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


def build_logistic_model(kind: str, seed: int) -> nn.Module:
    torch.manual_seed(seed)
    if kind == "mlp":
        return nn.Sequential(nn.Linear(1, 40), nn.Tanh(), nn.Linear(40, 1)).double()
    if kind == "pikan":
        from kan import KAN

        model = KAN(width=[1, 7, 1], grid=3, k=3, seed=seed,
                    auto_save=False, symbolic_enabled=False).double()
        for name, parameter in model.named_parameters():
            if name.startswith("symbolic_fun"):
                parameter.requires_grad_(False)
        return model
    raise ValueError(f"unknown logistic model: {kind}")


def _grad(value: torch.Tensor, variable: torch.Tensor) -> torch.Tensor:
    return torch.autograd.grad(value.sum(), variable, create_graph=True)[0]


def _relative_l2(predicted: np.ndarray, reference: np.ndarray) -> float:
    return float(np.linalg.norm(predicted - reference) / np.linalg.norm(reference))


def _logistic_exact(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + 9 * np.exp(-x))


def run_logistic_case(kind: str, seed: int, iterations: int = 10_000) -> dict:
    model = build_logistic_model(kind, seed)
    optimizer = torch.optim.Adam((p for p in model.parameters() if p.requires_grad), lr=0.01)
    collocation = torch.linspace(0, 5, 100, dtype=torch.float64).reshape(-1, 1).requires_grad_()
    start = time.perf_counter()
    status, reason = "completed", ""
    final_loss = math.nan
    try:
        for _ in range(iterations):
            optimizer.zero_grad(set_to_none=True)
            values = model(collocation)
            residual = _grad(values, collocation) - values * (1 - values)
            loss = residual.square().mean() + 10 * (values[0, 0] - 0.1).square()
            loss.backward()
            optimizer.step()
        final_loss = float(loss.detach())
    except (RuntimeError, ValueError, FloatingPointError) as exc:
        status, reason = "failed", str(exc)
    training_seconds = time.perf_counter() - start
    if status == "failed":
        return {"method": kind, "seed": seed, "status": status, "reason": reason,
                "iterations": iterations, "training_seconds": training_seconds,
                "parameter_count": trainable_parameter_count(model)}
    grid = torch.linspace(0, 5, 1001, dtype=torch.float64).reshape(-1, 1).requires_grad_()
    inference_start = time.perf_counter()
    values = model(grid)
    derivative = _grad(values, grid)
    inference_seconds = time.perf_counter() - inference_start
    x = grid.detach().numpy().ravel()
    exact = _logistic_exact(x)
    exact_derivative = exact * (1 - exact)
    predicted = values.detach().numpy().ravel()
    predicted_derivative = derivative.detach().numpy().ravel()
    return {
        "method": kind, "seed": seed, "status": "completed", "iterations": iterations,
        "parameter_count": trainable_parameter_count(model), "final_training_loss": final_loss,
        "training_seconds": training_seconds, "inference_seconds": inference_seconds,
        "solution_mae": float(np.mean(np.abs(predicted - exact))),
        "solution_relative_l2": _relative_l2(predicted, exact),
        "derivative_mae": float(np.mean(np.abs(predicted_derivative - exact_derivative))),
        "derivative_relative_l2": _relative_l2(predicted_derivative, exact_derivative),
    }


class _DuffingNet(nn.Module):
    def __init__(self, method: str, seed: int, x0: float, y0: float, delta: float):
        super().__init__()
        torch.manual_seed(seed)
        self.method = method
        self.x0, self.y0, self.delta = x0, y0, delta
        self.net = nn.Sequential(nn.Linear(1, 64), nn.Tanh(), nn.Linear(64, 2)).double()
        f0 = x0 - x0**3 - delta * y0
        y2 = y0 - 3 * x0**2 * y0 - delta * f0
        y3 = f0 - 6 * x0 * y0**2 - 3 * x0**2 * f0 - delta * y2
        self.register_buffer("coeff", torch.tensor(
            [[x0, y0, f0 / 2, y2 / 6], [y0, f0, y2 / 2, y3 / 6]], dtype=torch.float64))

    def forward(self, t: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        raw = self.net(t)
        if self.method in {"vanilla", "higher-order"}:
            state = self.coeff[:, 0] + t * raw
        elif self.method == "tm-pinn":
            p2 = self.coeff[:, 0] + t * self.coeff[:, 1] + t**2 * self.coeff[:, 2]
            state = p2 + t**3 * (self.coeff[:, 3] + t * raw)
        else:
            raise ValueError(f"unknown Duffing method: {self.method}")
        return state[:, 0:1], state[:, 1:2]


def _duffing_residual(model: _DuffingNet, t: torch.Tensor):
    x, y = model(t)
    rx = _grad(x, t) - y
    ry = _grad(y, t) - (x - x**3 - model.delta * y)
    return x, y, rx, ry


def _duffing_reference(t_end: float, x0: float, y0: float, delta: float):
    def rhs(_, state):
        x, y = state
        return y, x - x**3 - delta * y

    result = solve_ivp(rhs, (0, t_end), (x0, y0), method="DOP853", rtol=1e-12,
                       atol=1e-14, dense_output=True, max_step=0.02)
    if not result.success:
        raise RuntimeError(result.message)
    return result


def run_duffing_case(method: str, seed: int, t_end: float, iterations: int = 3_000) -> dict:
    x0, y0, delta = -0.224, -0.269, 0.327
    model = _DuffingNet(method, seed, x0, y0, delta)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)
    t = torch.linspace(0, t_end, 128, dtype=torch.float64).reshape(-1, 1).requires_grad_()
    start = time.perf_counter()
    for _ in range(iterations):
        optimizer.zero_grad(set_to_none=True)
        _, _, rx, ry = _duffing_residual(model, t)
        loss = rx.square().mean() + ry.square().mean()
        if method == "higher-order":
            loss = loss + 0.1 * (_grad(rx, t).square().mean() + _grad(ry, t).square().mean())
        elif method == "tm-pinn":
            scale = torch.clamp(t, min=1e-3) ** 2
            loss = (rx / scale).square().mean() + (ry / scale).square().mean()
        loss.backward()
        optimizer.step()
    training_seconds = time.perf_counter() - start
    grid = torch.linspace(0, t_end, 1001, dtype=torch.float64).reshape(-1, 1).requires_grad_()
    inference_start = time.perf_counter()
    x, y, rx, ry = _duffing_residual(model, grid)
    inference_seconds = time.perf_counter() - inference_start
    predicted = np.vstack((x.detach().numpy().ravel(), y.detach().numpy().ravel()))
    reference = _duffing_reference(t_end, x0, y0, delta).sol(grid.detach().numpy().ravel())
    residual = np.hypot(rx.detach().numpy().ravel(), ry.detach().numpy().ravel())
    return {
        "method": method, "seed": seed, "horizon": t_end, "status": "completed",
        "iterations": iterations, "parameter_count": trainable_parameter_count(model),
        "training_seconds": training_seconds, "inference_seconds": inference_seconds,
        "mae": float(np.mean(np.abs(predicted - reference))),
        "relative_l2": _relative_l2(predicted, reference),
        "residual_rms": float(np.sqrt(np.mean(residual**2))),
        "residual_max": float(np.max(residual)),
    }


def _write_outputs(output_dir: Path, report: dict) -> None:
    rows = []
    for run in report["logistic"]["runs"]:
        rows.append({"problem": "logistic", "method": run["method"], "seed": run["seed"],
                     "horizon": 5, "status": run["status"], "parameter_count": run["parameter_count"],
                     "iterations": run["iterations"], "training_seconds": run["training_seconds"],
                     "inference_seconds": run.get("inference_seconds", ""),
                     "relative_l2": run.get("solution_relative_l2", ""),
                     "derivative_relative_l2": run.get("derivative_relative_l2", ""),
                     "residual_rms": ""})
    for run in report["duffing"]["runs"]:
        rows.append({"problem": "duffing", "method": run["method"], "seed": run["seed"],
                     "horizon": run["horizon"], "status": run["status"],
                     "parameter_count": run["parameter_count"], "iterations": run["iterations"],
                     "training_seconds": run["training_seconds"],
                     "inference_seconds": run.get("inference_seconds", ""),
                     "relative_l2": run.get("relative_l2", ""), "derivative_relative_l2": "",
                     "residual_rms": run.get("residual_rms", "")})
    with (output_dir / "ml_only_runs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    colors = {"mlp": "#275d8c", "pikan": "#b44d34", "vanilla": "#275d8c",
              "higher-order": "#7a6b25", "tm-pinn": "#b44d34"}
    logistic = [row for row in report["logistic"]["runs"] if row["status"] == "completed"]
    for index, method in enumerate(("mlp", "pikan")):
        values = [max(row["solution_relative_l2"], 1e-16) for row in logistic if row["method"] == method]
        axes[0].scatter(np.full(len(values), index), values, color=colors[method], alpha=0.75)
        if values:
            axes[0].plot(index, np.median(values), marker="_", ms=22, mew=3, color="black")
    axes[0].set(xticks=[0, 1], xticklabels=["MLP-PINN", "PIKAN"], yscale="log",
                ylabel="solution relative $L^2$", title="Logistic benchmark (all seeds)")
    duffing = [row for row in report["duffing"]["runs"] if row["status"] == "completed"]
    methods = ("vanilla", "higher-order", "tm-pinn")
    offsets = {-1.0: -0.15, 1.0: -0.15, 3.0: 0.15}
    for index, method in enumerate(methods):
        for horizon in (1.0, 3.0):
            values = [max(row["relative_l2"], 1e-16) for row in duffing
                      if row["method"] == method and row["horizon"] == horizon]
            label = f"T={horizon:g}" if index == 0 else None
            axes[1].scatter(np.full(len(values), index + offsets[horizon]), values,
                            color="#126a5b" if horizon == 1 else "#b44d34", alpha=0.75, label=label)
    axes[1].set(xticks=range(3), xticklabels=["vanilla", "higher-order", "TM-PINN"],
                yscale="log", ylabel="state relative $L^2$",
                title="Bounded Duffing reproduction")
    axes[1].legend(frameon=False)
    fig.savefig(output_dir / "ml_only_comparison.png", dpi=180)
    plt.close(fig)


def run_demo(output_dir: Path, logistic_iterations: int = 10_000,
             duffing_iterations: int = 3_000, seeds=range(3),
             logistic_seeds=range(10)) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    logistic = [run_logistic_case(method, seed, logistic_iterations)
                for method in ("mlp", "pikan") for seed in logistic_seeds]
    duffing = [run_duffing_case(method, seed, horizon, duffing_iterations)
               for horizon in (1.0, 3.0)
               for method in ("vanilla", "higher-order", "tm-pinn") for seed in seeds]
    successful_logistic = [row for row in logistic if row["status"] == "completed"]
    means = {method: float(np.mean([row["solution_relative_l2"] for row in successful_logistic
                                    if row["method"] == method]))
             for method in ("mlp", "pikan")}
    report = {
        "schema": "lieml.three-layer.ml-only.v1", "created_utc": utc_now(),
        "status": "completed" if all(row["status"] == "completed" for row in logistic + duffing) else "partial",
        "scope": {"duffing": "bounded fixed-IVP directional reproduction",
                  "logistic": "configured reproduction of the reported PINN-PIKAN benchmark",
                  "piratenet": "literature-only; no reduced PyTorch implementation is called a reproduction"},
        "versions": {"python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__},
        "source_sha256": sha256(Path(__file__)),
        "configuration": {"logistic_iterations": logistic_iterations,
                          "duffing_iterations": duffing_iterations,
                          "duffing_seeds": list(seeds), "logistic_seeds": list(logistic_seeds)},
        "logistic": {"runs": logistic, "mean_solution_relative_l2": means,
                     "reported_direction_reproduced": means["pikan"] < means["mlp"]},
        "duffing": {"runs": duffing},
    }
    write_json(output_dir / "ml_only_report.json", report)
    _write_outputs(output_dir, report)
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--logistic-iterations", type=int, default=10_000)
    parser.add_argument("--duffing-iterations", type=int, default=3_000)
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args(argv)
    if args.quick:
        report = run_demo(args.output_dir, 20, 20, seeds=range(1), logistic_seeds=range(1))
    else:
        report = run_demo(args.output_dir, args.logistic_iterations, args.duffing_iterations)
    print((args.output_dir / "ml_only_report.json").read_text(encoding="utf-8"))
    return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
