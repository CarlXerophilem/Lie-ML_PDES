"""Offline exact certification and reproducible CPU solver comparison."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter

from symm.generic.pipeline_certificates import exact_certificates
from symm.solvers.benchmark import run_benchmarks, write_json
from symm.solvers.reporting import write_report

ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT/"build/week-4")
    parser.add_argument("--quick", action="store_true", help="smaller neural campaign; all classical controls remain")
    parser.add_argument("--seeds", type=int, nargs="+", default=[17, 23, 41])
    parser.add_argument("--adam-steps", type=int, default=500)
    parser.add_argument("--lbfgs-evaluations", type=int, default=250)
    parser.add_argument("--campaign-seconds", type=float, default=1800.)
    args = parser.parse_args()
    out = args.out.resolve()
    protected = [ROOT/name for name in ("draft", "ref", "research_artifacts", "symm", "scripts", "docs", "tests", ".git")]
    protected.append(ROOT.parent/"Lie-ML_PDES-archive")
    if out == ROOT or any(path == out or path in out.parents for path in protected):
        parser.error("outputs must be outside source/evidence directories; use build/week-4")
    if min(args.adam_steps, args.lbfgs_evaluations, args.campaign_seconds) <= 0:
        parser.error("training budgets must be positive")
    out.mkdir(parents=True, exist_ok=True)
    config = {"seeds": args.seeds, "quick": args.quick, "adam_steps": args.adam_steps,
              "lbfgs_evaluations": args.lbfgs_evaluations, "campaign_seconds": args.campaign_seconds,
              "per_model_seconds": 120., "dtype": "float64", "device": "cpu",
              "grid_points": 1001, "interval": [1., 1.5], "time_window": [1., 2.],
              "parameter_domain": {"m": [2.9, 3.1], "eta": [-.1, .1]},
              "family_training": [[m, a] for m in (2.9, 3.1) for a in (-.1, 0., .1)],
              "family_validation": [[3., -.05], [3., .05], [2.95, -.075], [3.05, .075]]}
    write_json(out/"config.json", config)
    sources = [ROOT/"run_pipeline.py", *sorted((ROOT/"symm/generic").glob("*.py")),
               *sorted((ROOT/"symm/solvers").glob("*.py")), *sorted((ROOT/"symm/selection").glob("*.py")),
               *sorted((ROOT/"research_artifacts/sve-progress-20261010/sve_lab").glob("*.py"))]
    environment = {"utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
                   "platform": platform.platform(), "cpu_threads_training": 1,
                   "packages": {name: importlib.metadata.version(name) for name in
                                ("numpy", "scipy", "sympy", "torch", "matplotlib")},
                   "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                   "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                     for path in sources}}
    write_json(out/"environment.json", environment)
    started = perf_counter()
    certificates = exact_certificates()
    certificates["elapsed_seconds"] = perf_counter()-started
    write_json(out/"symbolic_certificates.json", certificates)
    print("Exact scalar, coupled-generator, boundary and rank certificates verified", flush=True)
    # Reuse the maintained original-coordinate data/flux and nine-stage workflow.
    for command in ("data-flux", "workflow"):
        subprocess.run([sys.executable, "scripts/project.py", command, "--out", str(out/command)],
                       cwd=ROOT, check=True)
    results = run_benchmarks(out, seeds=tuple(args.seeds), quick=args.quick,
                            adam_steps=args.adam_steps, lbfgs_evaluations=args.lbfgs_evaluations,
                            campaign_seconds=args.campaign_seconds)
    write_report(out, certificates, results, config)
    print(f"Completed: {out}; neural failures retained as measured outcomes", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
