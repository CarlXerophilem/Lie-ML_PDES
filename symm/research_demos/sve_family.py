"""Branch-aware parameter-family extension of the certificate-gated SVE demo."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
import torch
from torch import nn

from .fusion import (PolynomialProfile, coefficients, derivative, evaluate,
                     original_master_check, perturbed_initial_state, solve_reference,
                     taylor_coefficients)
from .schema import sha256, utc_now, write_json


TRAIN_ETAS = (-0.02, -0.015, -0.01, 0.0, 0.01, 0.015, 0.02)
HELDOUT_ETAS = (-0.0125, -0.005, 0.005, 0.0125)
BRANCH_PLOT_TICKS = (-0.02, -0.01, 0.0, 0.01, 0.02)
BRANCH_STATUSES = (
    "regular",
    "rank-drop",
    "singular-Fprime",
    "singular-leading",
    "reference-disagreement",
    "solver-failure",
)


class CertificateError(ValueError):
    """Raised when the family demo is not given the strict v0.2 certificate."""


def load_verified_v02_certificate(path: Path) -> dict:
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    if report.get("schema") != "lieml.sve.reduction-certificate.v0.2":
        raise CertificateError("expected the SVE reduction certificate v0.2")
    if report.get("status") != "verified-regular-data-compatible":
        raise CertificateError("certificate is not verified on the regular data-compatible branch")
    branch = report.get("fixed_branch", {})
    expected_branch = {
        "m": 3,
        "delta_m": 0,
        "generator": "X_5 = t*d_t - 2*s*d_s",
        "invariant": "sigma = s*t**2",
        "orbit_coordinate": "rho = t",
        "parameter_relation": "beta_tr = 3*kappa",
    }
    if any(branch.get(name) != value for name, value in expected_branch.items()):
        raise CertificateError("certificate does not describe the fixed cubic reduction branch")
    reduction = report.get("reduction_certificate", {})
    if (reduction.get("status") != "verified" or not reduction.get("checks")
            or not all(reduction["checks"].values())):
        raise CertificateError("certificate lacks a verified exact reduction")
    data = report.get("data_compatibility", {})
    if (data.get("status") != "data-compatible" or not data.get("checks")
            or not all(data["checks"].values())):
        raise CertificateError("certificate lacks strict data-compatible evidence")
    if data.get("invariance_residuals") != ["0", "0", "0", "0"]:
        raise CertificateError("certificate lacks four exact zero data-invariance residuals")
    guards = report.get("exact_branch_guards", {})
    if any(guards.get(name) in (None, "", "missing", "0", 0)
           for name in ("chart_rank", "orbit_speed", "fiber_rank")):
        raise CertificateError("certificate lacks exact rank guards")
    singular = report.get("singular_boundaries", {})
    if any(singular.get(name) in (None, "", "missing")
           for name in ("rank_drop", "F_prime", "leading_coefficient")):
        raise CertificateError("certificate lacks singular-boundary declarations")
    family = report.get("parameter_family", {})
    if (family.get("name") != "eta_ic"
            or family.get("candidate_interval") != [-0.02, 0.02]
            or len(family.get("data", ())) != 3):
        raise CertificateError("certificate does not declare the required initial-curvature family")
    return report


def classify_branch_samples(sigma, state, cross_solver_max_abs: float, *,
                            rank_ok: bool = True, leading_tolerance: float = 1e-8,
                            reference_tolerance: float = 1e-9) -> dict:
    """Classify sampled numerical evidence without upgrading it to an exact proof."""
    sigma = np.asarray(sigma, dtype=float)
    state = np.asarray(state, dtype=float)
    result = {
        "status": "regular",
        "evidence_scope": "sampled-grid",
        "sample_count": int(sigma.size),
        "minimum_F_prime": math.nan,
        "minimum_abs_leading_coefficient": math.nan,
        "cross_solver_max_abs": float(cross_solver_max_abs),
    }
    if not rank_ok:
        result["status"] = "rank-drop"
        return result
    if state.shape != (3, sigma.size) or not np.isfinite(state).all() or not np.isfinite(sigma).all():
        result["status"] = "solver-failure"
        return result
    first = state[1]
    result["minimum_F_prime"] = float(np.min(first))
    if np.any(first <= 0):
        result["status"] = "singular-Fprime"
        return result
    leading, _ = coefficients(sigma, first, state[2])
    result["minimum_abs_leading_coefficient"] = float(np.min(np.abs(leading)))
    if (not np.isfinite(leading).all()
            or result["minimum_abs_leading_coefficient"] <= leading_tolerance):
        result["status"] = "singular-leading"
        return result
    if (not math.isfinite(cross_solver_max_abs)
            or cross_solver_max_abs > reference_tolerance):
        result["status"] = "reference-disagreement"
    return result


def _reference_case(eta_ic: float, grid_size: int = 1001):
    eta_ic = float(eta_ic)
    if not math.isfinite(eta_ic):
        return ({"eta_ic": eta_ic, "status": "solver-failure",
                 "reason": "eta_ic must be finite", "evidence_scope": "input-validation"}, None)
    try:
        initial = perturbed_initial_state(eta_ic)
        started = time.perf_counter()
        dop853 = solve_reference(initial, method="DOP853", rtol=1e-11,
                                 atol=1e-13, max_step=0.02)
        dop853_seconds = time.perf_counter()-started
        started = time.perf_counter()
        radau = solve_reference(initial, method="Radau", rtol=2e-12,
                                atol=2e-14, max_step=0.02)
        radau_seconds = time.perf_counter()-started
        sigma = np.linspace(1.0, 1.5, grid_size)
        state = dop853.sol(sigma)
        cross_solver = float(np.max(np.abs(state-radau.sol(sigma))))
        record = classify_branch_samples(sigma, state, cross_solver)
        record.update({
            "eta_ic": eta_ic,
            "reason": "",
            "DOP853_nfev": int(dop853.nfev),
            "Radau_nfev": int(radau.nfev),
            "DOP853_seconds": dop853_seconds,
            "Radau_seconds": radau_seconds,
        })
        return record, dop853 if record["status"] == "regular" else None
    except (RuntimeError, ValueError, FloatingPointError) as exc:
        return ({"eta_ic": eta_ic, "status": "solver-failure", "reason": str(exc),
                 "evidence_scope": "solver"}, None)


def reference_case(eta_ic: float, grid_size: int = 1001) -> dict:
    return _reference_case(eta_ic, grid_size)[0]


def build_reference_family(etas, grid_size: int = 1001):
    records = []
    solutions = {}
    for eta_ic in etas:
        record, solution = _reference_case(eta_ic, grid_size)
        records.append(record)
        if solution is not None:
            solutions[float(eta_ic)] = solution
    return records, solutions


class ConditionalHardProfile(nn.Module):
    """P2(sigma, eta) plus a correction that preserves three initial jets."""

    def __init__(self, seed: int):
        super().__init__()
        torch.manual_seed(seed)
        self.net = nn.Sequential(
            nn.Linear(2, 24), nn.Tanh(),
            nn.Linear(24, 24), nn.Tanh(),
            nn.Linear(24, 1),
        ).double()
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)
        self.register_buffer("k", torch.tensor(np.cbrt(45.0), dtype=torch.float64))

    def forward(self, sigma, eta_ic):
        eta_ic = torch.broadcast_to(eta_ic, sigma.shape)
        z = sigma-1
        second = -2*self.k*(1+eta_ic)/9
        p2 = self.k + z*self.k/3 + z**2*second/2
        inputs = torch.cat((4*z-1, eta_ic/0.02), dim=1)
        return p2 + z**3*self.net(inputs)


class FixedEtaProfile(nn.Module):
    """Bind one data parameter for generic profile and lifting evaluators."""

    def __init__(self, model: ConditionalHardProfile, eta_ic: float):
        super().__init__()
        self.model = model
        self.eta_ic = float(eta_ic)

    def forward(self, sigma):
        return self.model(sigma, torch.full_like(sigma, self.eta_ic))


def conditional_profile_jets(model, sigma, eta_ic):
    value = model(sigma, eta_ic)
    first = derivative(value, sigma)
    second = derivative(first, sigma)
    third = derivative(second, sigma)
    return value, first, second, third


def conditional_residuals(model, sigma, eta_ic):
    value, first, second, third = conditional_profile_jets(model, sigma, eta_ic)
    leading, remainder = coefficients(sigma, first, second)
    raw = leading*third+remainder
    normalized = third+remainder/leading
    return value, first, second, normalized, raw, leading


def amortization_break_even(training_seconds: float, solver_query_seconds: float,
                            inference_query_seconds: float) -> int | None:
    advantage = float(solver_query_seconds)-float(inference_query_seconds)
    if advantage <= 0:
        return None
    return int(math.ceil(float(training_seconds)/advantage))


def _validate_split(train_etas, heldout_etas):
    train = tuple(map(float, train_etas))
    heldout = tuple(map(float, heldout_etas))
    if not train or not heldout or set(train) & set(heldout):
        raise ValueError("training and held-out eta sets must be nonempty and disjoint")
    if any(not math.isfinite(value) or value < -0.02 or value > 0.02
           for value in (*train, *heldout)):
        raise ValueError("eta values must be finite and inside [-0.02, 0.02]")
    return train, heldout


def _train(seed: int, train_etas, steps: int, collocation_points: int):
    if steps < 1 or collocation_points < 4:
        raise ValueError("require at least one step and four collocation points")
    model = ConditionalHardProfile(seed)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    started = time.perf_counter()
    status, reason, final_loss = "completed", "", math.nan
    try:
        for _ in range(steps):
            optimizer.zero_grad(set_to_none=True)
            sigma_line = torch.linspace(1, 1.5, collocation_points, dtype=torch.float64)
            sigma = sigma_line.repeat(len(train_etas)).reshape(-1, 1).requires_grad_()
            eta = torch.tensor(train_etas, dtype=torch.float64).repeat_interleave(
                collocation_points).reshape(-1, 1)
            *_, normalized, _, leading = conditional_residuals(model, sigma, eta)
            if (leading.abs() < 1e-6).any() or not torch.isfinite(normalized).all():
                raise ValueError("sampled training branch left the regular finite region")
            loss = normalized.square().mean()
            loss.backward()
            optimizer.step()
        final_loss = float(loss.detach())
    except (RuntimeError, ValueError, FloatingPointError) as exc:
        status, reason = "failed", str(exc)
    return model, {
        "seed": int(seed),
        "status": status,
        "reason": reason,
        "steps": int(steps),
        "collocation_points_per_eta": int(collocation_points),
        "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "final_training_loss": final_loss,
        "training_seconds": time.perf_counter()-started,
    }


def _evaluate_conditional(model, eta_ic: float, reference) -> tuple[dict, float]:
    fixed = FixedEtaProfile(model, eta_ic)
    grid_np = 1+(np.arange(1001)+0.5)*0.5/1001
    grid = torch.tensor(grid_np[:, None], dtype=torch.float64, requires_grad=True)
    started = time.perf_counter()
    value, first, second, normalized, raw, leading = conditional_residuals(
        model, grid, torch.full_like(grid, eta_ic))
    query_seconds = time.perf_counter()-started
    predicted = np.vstack([item.detach().numpy().ravel()
                           for item in (value, first, second)])
    target = reference.sol(grid_np)
    initial = perturbed_initial_state(eta_ic)
    origin = torch.ones((1, 1), dtype=torch.float64, requires_grad=True)
    origin_eta = torch.full_like(origin, eta_ic)
    initial_jets = conditional_profile_jets(model, origin, origin_eta)[:3]
    metrics = {
        "F_max_abs_error": float(np.max(np.abs(predicted[0]-target[0]))),
        "F_prime_max_abs_error": float(np.max(np.abs(predicted[1]-target[1]))),
        "F_second_max_abs_error": float(np.max(np.abs(predicted[2]-target[2]))),
        "state_relative_l2": float(np.linalg.norm(predicted-target)/np.linalg.norm(target)),
        "raw_residual_max_abs": float(raw.detach().abs().max()),
        "normalized_residual_max_abs": float(normalized.detach().abs().max()),
        "minimum_F_prime": float(first.detach().min()),
        "minimum_abs_leading_coefficient": float(leading.detach().abs().min()),
        "initial_jet_max_abs_error": float(np.max(np.abs(
            np.array([item.detach().item() for item in initial_jets])-initial))),
    }
    metrics.update(original_master_check(fixed))
    return metrics, query_seconds


def _controls(heldout_etas, solutions):
    result = {}
    for eta_ic in heldout_etas:
        if eta_ic not in solutions:
            continue
        initial = perturbed_initial_state(eta_ic)
        polynomial = taylor_coefficients(initial)
        result[str(eta_ic)] = {
            "taylor_p2": evaluate(PolynomialProfile(polynomial[:3]), solutions[eta_ic], initial),
            "taylor_p4": evaluate(PolynomialProfile(polynomial), solutions[eta_ic], initial),
        }
    return result


def _write_outputs(output_dir: Path, report: dict):
    fields = [
        "seed", "eta_ic", "split", "status", "reason", "steps", "parameter_count",
        "training_seconds", "inference_seconds", "F_max_abs_error",
        "F_prime_max_abs_error", "F_second_max_abs_error", "state_relative_l2",
        "raw_residual_max_abs", "normalized_residual_max_abs", "direct_master_max_abs",
        "direct_vs_lift_max_abs", "minimum_F_prime",
        "minimum_abs_leading_coefficient", "initial_jet_max_abs_error",
    ]
    with (output_dir/"sve_family_runs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for run in report["runs"]:
            metrics = run.get("metrics", {})
            writer.writerow({name: run.get(name, metrics.get(name, "")) for name in fields})

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    completed = [run for run in report["runs"] if run["status"] == "completed"]
    for seed in sorted({run["seed"] for run in completed}):
        rows = sorted((run for run in completed if run["seed"] == seed),
                      key=lambda item: item["eta_ic"])
        axes[0].plot([run["eta_ic"] for run in rows],
                     [max(run["metrics"]["F_max_abs_error"], 1e-16) for run in rows],
                     marker="o", label=f"seed {seed}")
    axes[0].set(xlabel=r"held-out $\eta_{ic}$", ylabel=r"max $|F-F_{ref}|$",
                yscale="log", title="Conditional profile error")
    axes[0].legend(frameon=False)
    regular = [row for row in report["references"] if row["status"] == "regular"]
    axes[1].plot([row["eta_ic"] for row in regular],
                 [row["minimum_F_prime"] for row in regular], marker="o", label="min F'")
    axes[1].plot([row["eta_ic"] for row in regular],
                 [row["minimum_abs_leading_coefficient"] for row in regular],
                 marker="s", label="min |a|")
    axes[1].set(xlabel=r"$\eta_{ic}$", ylabel="sampled branch margin",
                title="Regular-branch diagnostics")
    axes[1].set_xticks(BRANCH_PLOT_TICKS)
    axes[1].legend(frameon=False)
    fig.savefig(output_dir/"sve_family_comparison.png", dpi=180)
    plt.close(fig)


def run_demo(certificate_path: Path, output_dir: Path, *, steps: int = 1_000,
             seeds=range(3), train_etas=TRAIN_ETAS, heldout_etas=HELDOUT_ETAS,
             collocation_points: int = 64) -> dict:
    certificate = load_verified_v02_certificate(certificate_path)
    train_etas, heldout_etas = _validate_split(train_etas, heldout_etas)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)

    all_etas = tuple(dict.fromkeys((*train_etas, *heldout_etas)))
    references, solutions = build_reference_family(all_etas)
    controls = _controls(heldout_etas, solutions)
    runs = []
    training_records = []
    for seed in seeds:
        model, training = _train(int(seed), train_etas, steps, collocation_points)
        training_records.append(training)
        for eta_ic in heldout_etas:
            base = {
                "seed": int(seed), "eta_ic": eta_ic, "split": "heldout",
                "status": training["status"], "reason": training["reason"],
                "steps": int(steps), "parameter_count": training["parameter_count"],
                "training_seconds": training["training_seconds"],
            }
            if training["status"] == "completed" and eta_ic in solutions:
                metrics, inference_seconds = _evaluate_conditional(
                    model, eta_ic, solutions[eta_ic])
                base.update(status="completed", metrics=metrics,
                            inference_seconds=inference_seconds)
            elif eta_ic not in solutions:
                status = next(row["status"] for row in references
                              if row["eta_ic"] == eta_ic)
                base.update(status=status, reason="held-out reference is not regular")
            runs.append(base)

    completed = [run for run in runs if run["status"] == "completed"]
    regular_references = [row for row in references if row["status"] == "regular"]
    median_training = float(np.median([row["training_seconds"] for row in training_records]))
    median_solver = float(np.median([row["DOP853_seconds"] for row in regular_references]))
    median_inference = (float(np.median([row["inference_seconds"] for row in completed]))
                        if completed else math.nan)
    break_even = (amortization_break_even(median_training, median_solver, median_inference)
                  if completed else None)
    status = ("completed" if len(completed) == len(runs)
              and len(regular_references) == len(references) else "partial")
    report = {
        "schema": "lieml.sve.parameter-family.v0.2",
        "created_utc": utc_now(),
        "status": status,
        "scope": "fixed m=3 regular branch and initial-curvature family; sampled numerical margins",
        "certificate_source": str(Path(certificate_path).resolve()),
        "certificate_fingerprint": certificate["reduction_certificate"]["configuration_fingerprint"],
        "source_sha256": sha256(Path(__file__)),
        "versions": {"python": platform.python_version(), "torch": torch.__version__,
                     "numpy": np.__version__},
        "parameters": {"g": 1, "beta_tr": 0.1, "m": 3, "delta_m": 0,
                       "sigma": [1, 1.5], "eta_ic_interval": [-0.02, 0.02]},
        "split": {"train_eta_ic": list(train_etas),
                  "heldout_eta_ic": list(heldout_etas)},
        "references": references,
        "controls": controls,
        "training": training_records,
        "runs": runs,
        "cost": {
            "median_training_seconds": median_training,
            "median_DOP853_query_seconds": median_solver,
            "median_neural_query_seconds": median_inference,
            "break_even_queries": break_even,
            "break_even_rule": "ceil(training/(DOP853-neural)) only for a positive online advantage",
        },
        "claims": {
            "solution_family": True,
            "interval_certified": False,
            "singular_branches_solved": False,
            "m3_delta_continuation_proved": False,
            "ml_speedup_proved": False,
        },
    }
    write_json(output_dir/"sve_family_report.json", report)
    _write_outputs(output_dir, report)
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=1_000)
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args(argv)
    if args.quick:
        report = run_demo(args.certificate, args.output_dir, steps=10, seeds=range(1),
                          train_etas=(-0.02, 0.0, 0.02), heldout_etas=(-0.005, 0.005),
                          collocation_points=16)
    else:
        report = run_demo(args.certificate, args.output_dir, steps=args.steps)
    print((args.output_dir/"sve_family_report.json").read_text(encoding="utf-8"))
    return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
