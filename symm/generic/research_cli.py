"""Command-line entry point for the auditable generic-PDE pilot."""

from __future__ import annotations

import argparse
from pathlib import Path

from .experiment import run_pilot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the backend-neutral LieML oracle and CPU ranking pilot."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research_artifacts") / "pilot",
        help="directory for JSONL, model, evaluation, and report artifacts",
    )
    parser.add_argument(
        "--held-out",
        default="",
        help="comma-separated case IDs for the group-held-out split",
    )
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--min-leaf", type=int, default=2)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    held_out = tuple(item.strip() for item in args.held_out.split(",") if item.strip()) or None
    result = run_pilot(
        args.output,
        held_out_case_ids=held_out,
        max_depth=args.max_depth,
        min_leaf=args.min_leaf,
    )
    evaluation = result["evaluation"]
    print(f"artifacts: {args.output}")
    print(f"records: {result['metadata']['oracle_record_count']}")
    print(f"status_counts: {result['metadata']['status_counts']}")
    print(f"held_out_recall_at_{evaluation['top_k']}: {evaluation['recall_at_k']}")
    print(f"abstention_rate: {evaluation['abstention_rate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
