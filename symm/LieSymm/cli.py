"""Portable CLI; all generated outputs must be outside this package."""
import argparse
import json
from pathlib import Path

from ._loader import PACKAGE_ROOT
from .core import analyze, json_ready, print_derivation
from .models import branch_model
from .models_2d import branch_model_2d
from .provenance import check_historical_gate, verify_adapter, verify_snapshot


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dimension", type=int, choices=(1, 2), default=1)
    parser.add_argument("--branch", default="grass_generic")
    parser.add_argument("--out", type=Path, help="NEW output directory outside the installed package")
    parser.add_argument("--trace", choices=("full", "summary"), default="summary")
    parser.add_argument("--check-integrity", action="store_true", help="verify snapshot and all historical gates, without symbolic analysis")
    args = parser.parse_args(argv)
    if args.check_integrity:
        report = {"snapshot": verify_snapshot(), "adapter": verify_adapter(),
                  "historical_gates": {str(stage): check_historical_gate(stage) for stage in (1, 2, 3)}}
        print(json.dumps(report, indent=2))
        return 0 if (report["snapshot"]["passed"] and report["adapter"]["passed"]
                     and all(row["passed"] for row in report["historical_gates"].values())) else 1
    if args.out is None:
        parser.error("--out is required unless --check-integrity is selected")
    output = args.out.resolve()
    if output.is_relative_to(PACKAGE_ROOT) or output.exists():
        parser.error("Use a NEW output directory outside the installed LieSymm package")
    builder = branch_model if args.dimension == 1 else branch_model_2d
    try:
        model = builder(args.branch)
    except KeyError:
        parser.error("Unknown branch for the selected dimension: " + args.branch)
    report = analyze(**model)
    output.mkdir(parents=True, exist_ok=False)
    (output / "derivation.json").write_text(json.dumps(json_ready(report), indent=2) + "\n", encoding="utf-8")
    if args.trace == "full":
        print_derivation(report)
    else:
        print(args.branch, report["classification_status"], len(report["determining_equations"]), "determining equations")
    return 1 if report["classification_status"] == "failed" else 0
