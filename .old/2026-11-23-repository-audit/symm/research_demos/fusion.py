"""Lie--ML SVE prototype gated by a verified Lie-only certificate."""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp
import torch
from torch import nn

from .schema import sha256, utc_now, write_json


class CertificateError(ValueError):
    """Raised when the fusion demo is not given the verified Lie reduction."""


def load_verified_certificate(path: Path) -> dict:
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    if report.get("schema") != "lieml.three-layer.lie-only.v1":
        raise CertificateError("expected a lie-only v1 reduction certificate")
    cubic = report.get("cases", {}).get("m3", {})
    certificate = cubic.get("certificate", {})
    if certificate.get("status") != "verified" or not certificate.get("checks") or not all(certificate["checks"].values()):
        raise CertificateError("fusion requires a verified m=3 reduction certificate with passing checks")
    if not cubic.get("lifting_identity_zero") or not cubic.get("exact_control_zero"):
        raise CertificateError("verified certificate is missing lifting or exact-control checks")
    return report


def coefficients(sigma, r, v, g=1.0, beta_tr=0.1):
    a = 8 * (1 - g * beta_tr) * sigma**3 * r - 2 * g * sigma / r**2
    b = (4 * sigma * (1 - 4 * g * beta_tr) * r**2
         + 8 * sigma**2 * (3 - 5 * g * beta_tr) * r * v
         + (8 * sigma**3 * (1 - g * beta_tr) + 4 * g * sigma / r**3) * v**2)
    return a, b


def exact_state(sigma):
    sigma = np.asarray(sigma)
    k = np.cbrt(45.0)
    return np.array([k * sigma**(1 / 3), k / 3 * sigma**(-2 / 3),
                     -2 * k / 9 * sigma**(-5 / 3)])


def perturbed_initial_state(eta_ic: float = 0.01) -> np.ndarray:
    initial = exact_state(1.0).astype(float)
    initial[2] *= 1 + eta_ic
    return initial


def reduced_rhs(sigma, state):
    _, r, v = state
    a, b = coefficients(sigma, r, v)
    if r <= 0 or abs(a) < 1e-10:
        raise ValueError("outside the sampled regular branch")
    return np.array([r, v, -b / a])


def solve_reference(initial, method="DOP853", rtol=1e-11, atol=1e-13, max_step=0.02):
    result = solve_ivp(reduced_rhs, (1, 1.5), initial, method=method, rtol=rtol,
                       atol=atol, max_step=max_step, dense_output=True)
    if not result.success or result.t[-1] < 1.5:
        raise RuntimeError(result.message)
    return result


def taylor_coefficients(initial) -> np.ndarray:
    sigma, r, v = sp.symbols("sigma r v")
    a, b = coefficients(sigma, r, v, sp.Integer(1), sp.Rational(1, 10))
    third = -b / a
    fourth = sp.diff(third, sigma) + sp.diff(third, r) * v + sp.diff(third, v) * third
    evaluate = sp.lambdify((sigma, r, v), (third, fourth), "numpy")
    d3, d4 = evaluate(1.0, initial[1], initial[2])
    return np.array([initial[0], initial[1], initial[2] / 2, d3 / 6, d4 / 24], dtype=float)


def derivative(value, variable):
    return torch.autograd.grad(value.sum(), variable, create_graph=True)[0]


class HardProfile(nn.Module):
    def __init__(self, order: int, initial, seed: int):
        super().__init__()
        if order not in (2, 4):
            raise ValueError("order must be 2 or 4")
        torch.manual_seed(seed)
        self.order = order
        self.correction_power = order + 1
        self.net = nn.Sequential(nn.Linear(1, 24), nn.Tanh(), nn.Linear(24, 24),
                                 nn.Tanh(), nn.Linear(24, 1)).double()
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)
        coefficients_ = taylor_coefficients(initial)[:order + 1]
        self.register_buffer("polynomial", torch.tensor(coefficients_, dtype=torch.float64))

    def forward(self, sigma):
        z = sigma - 1
        polynomial = sum(coefficient * z**degree
                         for degree, coefficient in enumerate(self.polynomial))
        return polynomial + z**self.correction_power * self.net(4 * z - 1)


class VanillaHardProfile(nn.Module):
    """Hard-IVP PINN using jet subtraction rather than an explicit Taylor prior."""

    def __init__(self, initial, seed: int):
        super().__init__()
        torch.manual_seed(seed)
        self.initial = torch.tensor(initial, dtype=torch.float64)
        self.net = nn.Sequential(nn.Linear(1, 24), nn.Tanh(), nn.Linear(24, 24),
                                 nn.Tanh(), nn.Linear(24, 1)).double()

    def forward(self, sigma):
        z = sigma - 1
        origin = torch.ones((1, 1), dtype=sigma.dtype, device=sigma.device, requires_grad=True)
        n0 = self.net(origin)
        n1 = derivative(n0, origin)
        n2 = derivative(n1, origin)
        correction = self.net(sigma) - n0 - z * n1 - z**2 * n2 / 2
        return self.initial[0] + z * self.initial[1] + z**2 * self.initial[2] / 2 + correction


class PolynomialProfile(nn.Module):
    def __init__(self, polynomial):
        super().__init__()
        self.register_buffer("polynomial", torch.tensor(polynomial, dtype=torch.float64))

    def forward(self, sigma):
        z = sigma - 1
        return sum(coefficient * z**degree
                   for degree, coefficient in enumerate(self.polynomial))


class ExactProfile(nn.Module):
    def forward(self, sigma):
        return np.cbrt(45.0) * sigma ** (1 / 3)


def profile_jets(model, sigma):
    value = model(sigma)
    first = derivative(value, sigma)
    second = derivative(first, sigma)
    third = derivative(second, sigma)
    return value, first, second, third


def residuals(model, sigma):
    value, first, second, third = profile_jets(model, sigma)
    a, b = coefficients(sigma, first, second)
    raw = a * third + b
    normalized = third + b / a
    return value, first, second, normalized, raw, a


def original_master_check(model, grid_size=11):
    tgrid, sigmagrid = np.meshgrid(np.linspace(1, 1.25, grid_size),
                                   np.linspace(1, 1.5, grid_size), indexing="ij")
    t = torch.tensor(tgrid.reshape(-1, 1), dtype=torch.float64, requires_grad=True)
    s = torch.tensor((sigmagrid / tgrid**2).reshape(-1, 1), dtype=torch.float64, requires_grad=True)
    phi = model(s * t**2)
    ps, pt = derivative(phi, s), derivative(phi, t)
    pss, ptt, pts = derivative(ps, s), derivative(pt, t), derivative(pt, s)
    flux = ps * ptt - pss / ps**2
    original = derivative(flux, t) - 0.1 * derivative(pt**2 * pts / ps, s)
    sigma = torch.tensor(sigmagrid.reshape(-1, 1), dtype=torch.float64, requires_grad=True)
    *_, reduced, _ = residuals(model, sigma)
    lifted = reduced / t.detach()
    return {"direct_master_max_abs": float(original.detach().abs().max()),
            "direct_vs_lift_max_abs": float((original.detach() - lifted.detach()).abs().max()),
            "grid_shape": [grid_size, grid_size]}


def evaluate(model, reference, initial) -> dict:
    grid_np = 1 + (np.arange(1001) + 0.5) * 0.5 / 1001
    grid = torch.tensor(grid_np[:, None], dtype=torch.float64, requires_grad=True)
    value, first, second, normalized, raw, a = residuals(model, grid)
    predicted = np.vstack([item.detach().numpy().ravel() for item in (value, first, second)])
    target = reference.sol(grid_np)
    start = torch.ones((1, 1), dtype=torch.float64, requires_grad=True)
    initial_jets = profile_jets(model, start)[:3]
    result = {
        "F_max_abs_error": float(np.max(np.abs(predicted[0] - target[0]))),
        "F_prime_max_abs_error": float(np.max(np.abs(predicted[1] - target[1]))),
        "F_second_max_abs_error": float(np.max(np.abs(predicted[2] - target[2]))),
        "state_relative_l2": float(np.linalg.norm(predicted - target) / np.linalg.norm(target)),
        "raw_residual_max_abs": float(raw.detach().abs().max()),
        "normalized_residual_max_abs": float(normalized.detach().abs().max()),
        "min_F_prime": float(first.detach().min()), "min_abs_a": float(a.detach().abs().min()),
        "initial_jet_max_abs_error": float(np.max(np.abs(
            np.array([item.detach().item() for item in initial_jets]) - initial))),
    }
    result.update(original_master_check(model))
    return result


def train_case(method: str, seed: int, initial, reference, steps: int) -> dict:
    if method == "vanilla-hard":
        model = VanillaHardProfile(initial, seed)
    elif method == "p2-corrected":
        model = HardProfile(2, initial, seed)
    elif method == "p4-corrected":
        model = HardProfile(4, initial, seed)
    else:
        raise ValueError(method)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    start = time.perf_counter()
    status, reason = "completed", ""
    try:
        for _ in range(steps):
            optimizer.zero_grad(set_to_none=True)
            sigma = torch.linspace(1, 1.5, 128, dtype=torch.float64).reshape(-1, 1).requires_grad_()
            *_, normalized, raw, a = residuals(model, sigma)
            if (a.abs() < 1e-6).any() or not torch.isfinite(normalized).all():
                raise ValueError("sampled regularity or finiteness gate failed")
            loss = normalized.square().mean()
            loss.backward()
            optimizer.step()
    except (RuntimeError, ValueError, FloatingPointError) as exc:
        status, reason = "failed", str(exc)
    training_seconds = time.perf_counter() - start
    base = {"method": method, "seed": seed, "status": status, "reason": reason,
            "steps": steps, "parameter_count": sum(p.numel() for p in model.parameters()),
            "training_seconds": training_seconds}
    if status == "completed":
        inference_start = time.perf_counter()
        base["metrics"] = evaluate(model, reference, initial)
        base["inference_seconds"] = time.perf_counter() - inference_start
    return base


def _write_outputs(output_dir: Path, report: dict) -> None:
    rows = []
    for run in report["runs"]:
        metrics = run.get("metrics", {})
        rows.append({"method": run["method"], "seed": run["seed"], "status": run["status"],
                     "steps": run["steps"], "parameter_count": run["parameter_count"],
                     "training_seconds": run["training_seconds"],
                     "inference_seconds": run.get("inference_seconds", ""),
                     "F_max_abs_error": metrics.get("F_max_abs_error", ""),
                     "F_prime_max_abs_error": metrics.get("F_prime_max_abs_error", ""),
                     "F_second_max_abs_error": metrics.get("F_second_max_abs_error", ""),
                     "raw_residual_max_abs": metrics.get("raw_residual_max_abs", ""),
                     "normalized_residual_max_abs": metrics.get("normalized_residual_max_abs", ""),
                     "direct_master_max_abs": metrics.get("direct_master_max_abs", ""),
                     "lifting_residual_difference": metrics.get("direct_vs_lift_max_abs", ""),
                     "min_F_prime": metrics.get("min_F_prime", ""),
                     "min_abs_a": metrics.get("min_abs_a", "")})
    with (output_dir / "fusion_runs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    import matplotlib.pyplot as plt

    completed = [row for row in report["runs"] if row["status"] == "completed"]
    methods = ("vanilla-hard", "p2-corrected", "p4-corrected")
    labels = ("hard-IVP", "$P_2+z^3N$", "$P_4+z^5N$")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    for index, method in enumerate(methods):
        errors = [max(row["metrics"]["F_max_abs_error"], 1e-16) for row in completed
                  if row["method"] == method]
        residuals_ = [max(row["metrics"]["raw_residual_max_abs"], 1e-16) for row in completed
                      if row["method"] == method]
        axes[0].scatter(np.full(len(errors), index), errors, color="#126a5b", alpha=0.75)
        axes[1].scatter(np.full(len(residuals_), index), residuals_, color="#b44d34", alpha=0.75)
    axes[0].axhline(report["controls"]["taylor_p2"]["F_max_abs_error"], color="#666", ls="--", label="$P_2$")
    axes[0].axhline(report["controls"]["taylor_p4"]["F_max_abs_error"], color="#111", ls=":", label="$P_4$")
    axes[0].set(xticks=range(3), xticklabels=labels, yscale="log", ylabel="max $|F-F_{ref}|$",
                title="Profile error (all seeds)")
    axes[0].legend(frameon=False)
    axes[1].set(xticks=range(3), xticklabels=labels, yscale="log",
                ylabel="max raw reduced residual", title="Reduced-equation defect")
    fig.savefig(output_dir / "fusion_comparison.png", dpi=180)
    plt.close(fig)


def run_demo(certificate_path: Path, output_dir: Path, steps: int = 1_000, seeds=range(3)) -> dict:
    certificate = load_verified_certificate(certificate_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    initial = perturbed_initial_state()
    ladder_specs = (
        ("coarse", 1e-7, 1e-9, 0.10),
        ("medium", 1e-9, 1e-11, 0.04),
        ("fine", 1e-11, 1e-13, 0.02),
    )
    ladder_solutions = []
    for name, rtol, atol, max_step in ladder_specs:
        started = time.perf_counter()
        solution = solve_reference(initial, rtol=rtol, atol=atol, max_step=max_step)
        ladder_solutions.append((name, rtol, atol, max_step, solution,
                                 time.perf_counter() - started))
    dop853 = ladder_solutions[-1][4]
    dop853_seconds = ladder_solutions[-1][5]
    started = time.perf_counter()
    radau = solve_reference(initial, method="Radau", rtol=2e-12, atol=2e-14)
    radau_seconds = time.perf_counter() - started
    grid = np.linspace(1, 1.5, 1001)
    ladder = [{
        "name": name, "rtol": rtol, "atol": atol, "max_step": max_step,
        "nfev": solution.nfev, "seconds": seconds,
        "difference_to_fine_max_abs": float(np.max(np.abs(solution.sol(grid) - dop853.sol(grid)))),
    } for name, rtol, atol, max_step, solution, seconds in ladder_solutions]
    cross_solver = float(np.max(np.abs(dop853.sol(grid) - radau.sol(grid))))
    coeff = taylor_coefficients(initial)
    exact_initial = exact_state(1.0).astype(float)
    exact_reference = solve_reference(exact_initial)
    controls = {
        "exact_unperturbed": evaluate(ExactProfile(), exact_reference, exact_initial),
        "taylor_p2": evaluate(PolynomialProfile(coeff[:3]), dop853, initial),
        "taylor_p4": evaluate(PolynomialProfile(coeff), dop853, initial),
    }
    runs = [train_case(method, seed, initial, dop853, steps)
            for method in ("vanilla-hard", "p2-corrected", "p4-corrected") for seed in seeds]
    report = {
        "schema": "lieml.three-layer.fusion.v1", "created_utc": utc_now(),
        "status": "completed" if all(row["status"] == "completed" for row in runs) else "partial",
        "certificate_source": str(Path(certificate_path).resolve()),
        "certificate_fingerprint": certificate["cases"]["m3"]["certificate"]["configuration_fingerprint"],
        "parameters": {"g": 1, "beta_tr": 0.1, "m": 3, "sigma": [1, 1.5],
                       "eta_ic": 0.01, "delta_m": 0},
        "versions": {"python": platform.python_version(), "torch": torch.__version__,
                     "numpy": np.__version__}, "source_sha256": sha256(Path(__file__)),
        "reference": {"DOP853_nfev": dop853.nfev, "Radau_nfev": radau.nfev,
                      "DOP853_seconds": dop853_seconds, "Radau_seconds": radau_seconds,
                      "DOP853_tolerance_ladder": ladder,
                      "cross_solver_max_abs": cross_solver},
        "controls": controls,
        "runs": runs,
        "claims": {"ml_faster_than_numerical_solver": False,
                   "interval_certified": False,
                   "cubic_pikan_transferred": False},
    }
    write_json(output_dir / "fusion_report.json", report)
    _write_outputs(output_dir, report)
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=1_000)
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args(argv)
    report = run_demo(args.certificate, args.output_dir, steps=10 if args.quick else args.steps,
                      seeds=range(1) if args.quick else range(3))
    print((args.output_dir / "fusion_report.json").read_text(encoding="utf-8"))
    return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
