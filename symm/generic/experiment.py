"""Auditable corpus, oracle, and CPU ML experiment utilities.

This module is deliberately separate from the mathematical kernel.  It turns
benchmark cases into provenance records, labels candidates with the local
exact residual checker, and trains a small deterministic binary tree used only
for prioritization.  A model score never changes a certificate status.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field, replace
import json
import math
from pathlib import Path
import time
from typing import Any, Iterable, Mapping, Sequence

import sympy as sp

from .backend import ResourceLimits, detect_backend
from .benchmarks import BenchmarkCase, benchmark_registry
from .core import PointGenerator, VALID_STATUSES, fingerprint
from .determining import verify_off_shell_residuals
from .reduction import orbit_rank
from .reductor import FEATURE_SCHEMA, PDEsReductor, translation_candidates
from .resource import memory_snapshot


EXPERIMENT_SCHEMA_VERSION = "lieml.experiment/1"
MODEL_SCHEMA_VERSION = "lieml.experiment.tree/1"
EXPERIMENT_FEATURE_SCHEMA = tuple(FEATURE_SCHEMA) + (
    "candidate_index",
    "candidate_xi_nonzero",
    "candidate_phi_nonzero",
    "candidate_expression_nodes",
    "system_guard_count",
    "system_equation_nodes",
)


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"


def write_json(path: str | Path, value: Any) -> Path:
    """Write a deterministic UTF-8 JSON artifact and return its path."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_json_dump(value), encoding="utf-8")
    return target


def write_jsonl(path: str | Path, rows: Iterable[Mapping[str, Any]]) -> Path:
    """Write one deterministic JSON object per line."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(dict(row), ensure_ascii=True, sort_keys=True) for row in rows]
    target.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return target


@dataclass(frozen=True)
class CloudRunConfig:
    """The selected CPU VM policy used for a reproducible pilot run."""

    instance_type: str = "SA9.8XLARGE64"
    vcpus: int = 32
    memory_gib: int = 64
    exact_workers: int = 4
    ml_vcpus: int = 12
    reserved_vcpus: int = 8
    disk_gib: int = 200
    budget_hours: int = 10
    gpu_required: bool = False
    rss_hard_limit_bytes: int = 1_800_000_000

    def __post_init__(self) -> None:
        if not self.instance_type:
            raise ValueError("instance_type must not be empty")
        if any(int(value) <= 0 for value in (
            self.vcpus, self.memory_gib, self.exact_workers, self.ml_vcpus,
            self.disk_gib, self.budget_hours, self.rss_hard_limit_bytes,
        )):
            raise ValueError("cloud resource values must be positive")
        if int(self.reserved_vcpus) < 0:
            raise ValueError("reserved_vcpus must be nonnegative")
        if self.ml_vcpus + self.reserved_vcpus > self.vcpus:
            raise ValueError("ML and reserved vCPUs exceed the instance")
        object.__setattr__(self, "vcpus", int(self.vcpus))
        object.__setattr__(self, "memory_gib", int(self.memory_gib))
        object.__setattr__(self, "exact_workers", int(self.exact_workers))
        object.__setattr__(self, "ml_vcpus", int(self.ml_vcpus))
        object.__setattr__(self, "reserved_vcpus", int(self.reserved_vcpus))
        object.__setattr__(self, "disk_gib", int(self.disk_gib))
        object.__setattr__(self, "budget_hours", int(self.budget_hours))
        object.__setattr__(self, "rss_hard_limit_bytes", int(self.rss_hard_limit_bytes))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": EXPERIMENT_SCHEMA_VERSION,
            "instance_type": self.instance_type,
            "vcpus": self.vcpus,
            "memory_gib": self.memory_gib,
            "exact_workers": self.exact_workers,
            "ml_vcpus": self.ml_vcpus,
            "reserved_vcpus": self.reserved_vcpus,
            "disk_gib": self.disk_gib,
            "budget_hours": self.budget_hours,
            "gpu_required": self.gpu_required,
            "rss_hard_limit_bytes": self.rss_hard_limit_bytes,
        }

    def fingerprint(self) -> str:
        return fingerprint(self.as_dict())


@dataclass(frozen=True)
class CorpusManifestEntry:
    """Provenance and shape metadata for one benchmark system."""

    case_id: str
    description: str
    domain: str
    source: str
    source_url: str
    license: str
    boundary_initial_provenance: str
    tags: tuple[str, ...]
    p: int
    q: int
    r: int
    system_fingerprint: str
    system: Mapping[str, Any]
    known_generators: tuple[str, ...] = ()
    rank_guards: tuple[str, ...] = ()
    structural_only: bool = True
    schema_version: str = EXPERIMENT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.case_id or not self.system_fingerprint:
            raise ValueError("case_id and system_fingerprint are required")
        if any(int(value) < 0 for value in (self.p, self.q, self.r)):
            raise ValueError("system dimensions must be nonnegative")
        object.__setattr__(self, "tags", tuple(str(item) for item in self.tags))
        object.__setattr__(self, "known_generators", tuple(str(item) for item in self.known_generators))
        object.__setattr__(self, "rank_guards", tuple(str(item) for item in self.rank_guards))
        object.__setattr__(self, "p", int(self.p))
        object.__setattr__(self, "q", int(self.q))
        object.__setattr__(self, "r", int(self.r))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "case_id": self.case_id,
            "description": self.description,
            "domain": self.domain,
            "source": self.source,
            "source_url": self.source_url,
            "license": self.license,
            "boundary_initial_provenance": self.boundary_initial_provenance,
            "tags": list(self.tags),
            "shape": {"p": self.p, "q": self.q, "r": self.r},
            "system_fingerprint": self.system_fingerprint,
            "system": dict(self.system),
            "known_generators": list(self.known_generators),
            "rank_guards": list(self.rank_guards),
            "structural_only": self.structural_only,
        }


_DOMAIN_BY_CASE = {
    "heat-2plus1": "mathematical-physics",
    "reaction-diffusion-2field": "catalyst-chemistry",
    "cauchy-riemann": "pure-mathematics",
    "constraint-r3-q2": "mathematical-physics",
    "parameter-a-nonzero": "engineering",
    "parameter-a-zero": "engineering",
    "rank-dropping-rotation": "pure-mathematics",
    "incompressible-navier-stokes-2d": "engineering",
}


def build_manifest(
    cases: Iterable[BenchmarkCase] | None = None,
) -> tuple[CorpusManifestEntry, ...]:
    """Build a provenance manifest from the checked-in structural registry."""
    entries = []
    for case in tuple(cases or benchmark_registry()):
        entries.append(CorpusManifestEntry(
            case_id=case.name,
            description=case.description,
            domain=_DOMAIN_BY_CASE.get(case.name, "unclassified"),
            source="LieML project benchmark registry",
            source_url="",
            license="project-local benchmark; external provenance required before publication",
            boundary_initial_provenance=(
                "not-provided; structural benchmark only"
            ),
            tags=(
                "generic-pqr",
                "structural-validation",
                "no-analytic-solution-claim",
            ),
            p=case.system.p,
            q=case.system.q,
            r=case.system.r,
            system_fingerprint=case.system.fingerprint(),
            system=case.system.as_dict(),
            known_generators=tuple(name for name, _ in case.known_generators),
            rank_guards=tuple(sp.srepr(value) for value in case.rank_guards),
        ))
    return tuple(entries)


@dataclass(frozen=True)
class OracleRecord:
    """One exact candidate outcome used as an ML training/evaluation row."""

    case_id: str
    candidate_id: str
    system_fingerprint: str
    candidate: Mapping[str, Any]
    features: tuple[tuple[str, float], ...]
    status: str
    backend: str
    verified: bool
    checks: tuple[tuple[str, bool], ...]
    branch_ids: tuple[str, ...]
    runtime_ms: float
    rss_bytes: int | None
    orbit_rank: int
    split: str = "unassigned"
    message: str = ""
    schema_version: str = EXPERIMENT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"invalid oracle status: {self.status}")
        if self.verified != (self.status == "verified"):
            raise ValueError("verified must agree with exact status")
        object.__setattr__(self, "features", tuple((str(k), float(v)) for k, v in self.features))
        object.__setattr__(self, "checks", tuple((str(k), bool(v)) for k, v in self.checks))
        object.__setattr__(self, "branch_ids", tuple(str(item) for item in self.branch_ids))
        object.__setattr__(self, "runtime_ms", float(self.runtime_ms))
        object.__setattr__(self, "orbit_rank", int(self.orbit_rank))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "case_id": self.case_id,
            "candidate_id": self.candidate_id,
            "system_fingerprint": self.system_fingerprint,
            "candidate": dict(self.candidate),
            "features": list(self.features),
            "status": self.status,
            "backend": self.backend,
            "verified": self.verified,
            "checks": list(self.checks),
            "branch_ids": list(self.branch_ids),
            "runtime_ms": self.runtime_ms,
            "rss_bytes": self.rss_bytes,
            "orbit_rank": self.orbit_rank,
            "split": self.split,
            "message": self.message,
        }


def _candidate_pairs(case: BenchmarkCase) -> tuple[tuple[str, PointGenerator], ...]:
    """Combine known and translation candidates without duplicate generators."""
    pairs: list[tuple[str, PointGenerator]] = list(case.known_generators)
    known = {fingerprint(generator.as_dict()) for _, generator in pairs}
    for index, generator in enumerate(translation_candidates(case.system)):
        if fingerprint(generator.as_dict()) not in known:
            pairs.append((f"translation-x{index}", generator))
    return tuple(pairs)


def _candidate_features(
    system,
    generator: PointGenerator,
    candidate_index: int,
) -> tuple[tuple[str, float], ...]:
    reductor = PDEsReductor()
    base = dict(reductor.features(system, generator))
    generator_components = generator.xi + generator.phi
    candidate_nodes = sum(int(sp.count_ops(value, visual=False)) + 1 for value in generator_components)
    equation_nodes = sum(int(sp.count_ops(value, visual=False)) + 1 for value in system.equations)
    values = {
        **base,
        "candidate_index": float(candidate_index),
        "candidate_xi_nonzero": float(sum(value != 0 for value in generator.xi)),
        "candidate_phi_nonzero": float(sum(value != 0 for value in generator.phi)),
        "candidate_expression_nodes": float(candidate_nodes),
        "system_guard_count": float(len(system.inequations) + len(system.assumptions)),
        "system_equation_nodes": float(equation_nodes),
    }
    return tuple((name, float(values[name])) for name in EXPERIMENT_FEATURE_SCHEMA)


def _split_case_ids(case_ids: Sequence[str], held_out_case_ids: Iterable[str] | None) -> set[str]:
    if held_out_case_ids is not None:
        return {str(item) for item in held_out_case_ids}
    ordered = sorted(set(case_ids))
    # Deterministic group holdout: every fifth case, never split candidates.
    return {case_id for index, case_id in enumerate(ordered) if index % 5 == 0}


def generate_oracle_records(
    cases: Iterable[BenchmarkCase] | None = None,
    *,
    held_out_case_ids: Iterable[str] | None = None,
    limits: ResourceLimits | None = None,
) -> tuple[OracleRecord, ...]:
    """Label known/translation candidates with exact local residual checks."""
    cases = tuple(cases or benchmark_registry())
    limits = limits or ResourceLimits()
    records: list[OracleRecord] = []
    for case in cases:
        for candidate_index, (name, generator) in enumerate(_candidate_pairs(case)):
            started = time.perf_counter()
            rss = None
            try:
                outcome = verify_off_shell_residuals(case.system, generator)
                status = outcome.status
                checks = outcome.checks
                branch_ids = (outcome.branch_id,)
                message = outcome.message
                verified = status == "verified" and outcome.all_checks_pass
            except Exception as exc:
                status = "error"
                checks = (("oracle_execution", False),)
                branch_ids = ()
                message = f"{type(exc).__name__}: {exc}"
                verified = False
            rss = memory_snapshot(limits).rss_bytes
            records.append(OracleRecord(
                case_id=case.name,
                candidate_id=f"{case.name}:{name}",
                system_fingerprint=case.system.fingerprint(),
                candidate=generator.as_dict(),
                features=_candidate_features(case.system, generator, candidate_index),
                status=status,
                backend="python-off-shell",
                verified=verified,
                checks=checks,
                branch_ids=branch_ids,
                runtime_ms=(time.perf_counter() - started) * 1000.0,
                rss_bytes=rss,
                orbit_rank=orbit_rank(case.system.jet_space, (generator,)),
                message=message,
            ))
    held_out = _split_case_ids([record.case_id for record in records], held_out_case_ids)
    return tuple(
        replace(record, split="held-out" if record.case_id in held_out else "train")
        for record in records
    )


def _record_values(record: OracleRecord) -> tuple[float, ...]:
    values = dict(record.features)
    return tuple(values[name] for name in EXPERIMENT_FEATURE_SCHEMA)


def _gini(labels: Sequence[int]) -> float:
    if not labels:
        return 0.0
    counts = Counter(labels)
    total = float(len(labels))
    return 1.0 - sum((count / total) ** 2 for count in counts.values())


def _leaf(labels: Sequence[int]) -> dict[str, Any]:
    positives = int(sum(labels))
    total = len(labels)
    return {
        "kind": "leaf",
        "probability": positives / total if total else 0.0,
        "count": total,
        "positive": positives,
    }


def _fit_tree(
    rows: Sequence[tuple[tuple[float, ...], int]],
    feature_schema: Sequence[str],
    *,
    max_depth: int,
    min_leaf: int,
) -> dict[str, Any]:
    def build(indices: tuple[int, ...], depth: int) -> dict[str, Any]:
        labels = [rows[index][1] for index in indices]
        node = _leaf(labels)
        if depth >= max_depth or len(set(labels)) <= 1 or len(indices) < 2 * min_leaf:
            return node
        base = _gini(labels)
        best: tuple[float, int, float, tuple[int, ...], tuple[int, ...]] | None = None
        for feature_index in range(len(feature_schema)):
            values = sorted({rows[index][0][feature_index] for index in indices})
            thresholds = tuple(
                (left + right) / 2.0
                for left, right in zip(values, values[1:])
                if left != right
            )
            for threshold in thresholds:
                left = tuple(index for index in indices if rows[index][0][feature_index] <= threshold)
                right = tuple(index for index in indices if rows[index][0][feature_index] > threshold)
                if len(left) < min_leaf or len(right) < min_leaf:
                    continue
                weighted = (
                    len(left) * _gini([rows[index][1] for index in left])
                    + len(right) * _gini([rows[index][1] for index in right])
                ) / len(indices)
                key = (weighted, feature_index, threshold, left, right)
                if best is None or key[:3] < best[:3]:
                    best = key
        if best is None or best[0] >= base - 1e-12:
            return node
        _, feature_index, threshold, left, right = best
        return {
            "kind": "split",
            "feature": feature_schema[feature_index],
            "threshold": threshold,
            "left": build(left, depth + 1),
            "right": build(right, depth + 1),
        }

    return build(tuple(range(len(rows))), 0)


@dataclass(frozen=True)
class TreeModel:
    """JSON-safe probability tree for candidate prioritization."""

    feature_schema: tuple[str, ...]
    tree: Mapping[str, Any]
    model_name: str = "empirical-probability-depth-limited-tree-v1"
    training_rows: int = 0
    positive_rows: int = 0
    schema_version: str = MODEL_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if tuple(self.feature_schema) != EXPERIMENT_FEATURE_SCHEMA:
            raise ValueError("tree feature schema does not match experiment schema")
        object.__setattr__(self, "feature_schema", tuple(self.feature_schema))
        object.__setattr__(self, "training_rows", int(self.training_rows))
        object.__setattr__(self, "positive_rows", int(self.positive_rows))

    def predict_probability(self, features: Mapping[str, float] | Sequence[float]) -> float:
        if isinstance(features, Mapping):
            values = {name: float(features[name]) for name in self.feature_schema}
        else:
            values = dict(zip(self.feature_schema, (float(item) for item in features)))
        node = self.tree
        while node.get("kind") == "split":
            node = node["left"] if values[node["feature"]] <= float(node["threshold"]) else node["right"]
        return float(node.get("probability", 0.0))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "model_name": self.model_name,
            "feature_schema": list(self.feature_schema),
            "training_rows": self.training_rows,
            "positive_rows": self.positive_rows,
            "tree": self.tree,
            "model_fingerprint": fingerprint({"feature_schema": self.feature_schema, "tree": self.tree}),
        }


def fit_tree_model(
    records: Iterable[OracleRecord],
    *,
    max_depth: int = 3,
    min_leaf: int = 2,
    train_split: str = "train",
) -> TreeModel:
    """Fit a deterministic tree on exact statuses from one split."""
    if max_depth < 0 or min_leaf <= 0:
        raise ValueError("invalid tree limits")
    selected = tuple(record for record in records if record.split == train_split)
    if not selected:
        raise ValueError(f"no records in split {train_split!r}")
    rows = tuple((_record_values(record), int(record.verified)) for record in selected)
    tree = _fit_tree(rows, EXPERIMENT_FEATURE_SCHEMA, max_depth=max_depth, min_leaf=min_leaf)
    return TreeModel(
        EXPERIMENT_FEATURE_SCHEMA,
        tree,
        training_rows=len(rows),
        positive_rows=sum(label for _, label in rows),
    )


def evaluate_tree_model(
    model: TreeModel,
    records: Iterable[OracleRecord],
    *,
    split: str = "held-out",
    top_k: int = 5,
    abstain_threshold: float = 0.75,
) -> dict[str, Any]:
    """Evaluate ranking and abstention without changing exact statuses."""
    if top_k <= 0 or not 0.0 <= abstain_threshold <= 1.0:
        raise ValueError("invalid evaluation limits")
    selected = tuple(record for record in records if record.split == split)
    grouped: dict[str, list[tuple[OracleRecord, float]]] = defaultdict(list)
    for record in selected:
        grouped[record.case_id].append((record, model.predict_probability(dict(record.features))))
    cases_with_target = 0
    recall_hits = 0
    confident = 0
    confident_correct = 0
    abstained = 0
    predictions = []
    for case_id in sorted(grouped):
        scored = sorted(
            grouped[case_id],
            key=lambda pair: (-pair[1], pair[0].candidate_id),
        )
        if any(record.verified for record, _ in scored):
            cases_with_target += 1
            recall_hits += int(any(record.verified for record, _ in scored[:top_k]))
        for record, probability in scored:
            is_confident = probability >= abstain_threshold
            confident += int(is_confident)
            confident_correct += int(is_confident and record.verified)
            abstained += int(not is_confident)
            predictions.append({
                "case_id": case_id,
                "candidate_id": record.candidate_id,
                "probability": probability,
                "exact_status": record.status,
                "recommendation": "rank" if is_confident else "abstain",
            })
    total = len(selected)
    return {
        "schema_version": EXPERIMENT_SCHEMA_VERSION,
        "split": split,
        "top_k": top_k,
        "abstain_threshold": abstain_threshold,
        "n_records": total,
        "n_cases": len(grouped),
        "n_cases_with_verified_candidate": cases_with_target,
        "recall_at_k": (recall_hits / cases_with_target if cases_with_target else None),
        "confident_records": confident,
        "confident_precision": (confident_correct / confident if confident else None),
        "abstention_rate": (abstained / total if total else None),
        "false_confident_records": confident - confident_correct,
        "certificate_status_mutation": False,
        "predictions": predictions,
    }


def run_pilot(
    output_dir: str | Path,
    *,
    cases: Iterable[BenchmarkCase] | None = None,
    held_out_case_ids: Iterable[str] | None = None,
    cloud: CloudRunConfig | None = None,
    limits: ResourceLimits | None = None,
    max_depth: int = 3,
    min_leaf: int = 2,
) -> dict[str, Any]:
    """Run the local, backend-neutral pilot and write all audit artifacts."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    cloud = cloud or CloudRunConfig()
    limits = limits or ResourceLimits(hard_memory_bytes=cloud.rss_hard_limit_bytes)
    cases = tuple(cases or benchmark_registry())
    manifest = build_manifest(cases)
    records = generate_oracle_records(
        cases,
        held_out_case_ids=held_out_case_ids,
        limits=limits,
    )
    model = fit_tree_model(records, max_depth=max_depth, min_leaf=min_leaf)
    evaluation = evaluate_tree_model(model, records)
    write_jsonl(output / "corpus_manifest.jsonl", (entry.as_dict() for entry in manifest))
    write_jsonl(output / "oracle_records.jsonl", (record.as_dict() for record in records))
    write_json(output / "model.json", model.as_dict())
    write_json(output / "evaluation.json", evaluation)
    statuses = Counter(record.status for record in records)
    metadata = {
        "schema_version": EXPERIMENT_SCHEMA_VERSION,
        "cloud": cloud.as_dict(),
        "cloud_fingerprint": cloud.fingerprint(),
        "resource_limits": limits.as_dict(),
        "system_count": len(cases),
        "oracle_record_count": len(records),
        "status_counts": dict(sorted(statuses.items())),
        "system_fingerprints": [case.system.fingerprint() for case in cases],
        "model_fingerprint": model.as_dict()["model_fingerprint"],
        "external_backend_policy": "Maple/REDUCE are not simulated; unavailable status is preserved",
        "backend_preflight": {
            name: detect_backend(name).as_dict() for name in ("maple", "reduce")
        },
    }
    write_json(output / "run_metadata.json", metadata)
    report = (
        "# LieML local experiment pilot\n\n"
        f"Systems: {len(cases)}\n\n"
        f"Oracle records: {len(records)}\n\n"
        f"Status counts: {dict(sorted(statuses.items()))}\n\n"
        f"Held-out recall@{evaluation['top_k']}: {evaluation['recall_at_k']}\n\n"
        "The tree ranks candidates only. Exact statuses and certificates are immutable.\n"
    )
    (output / "REPORT.md").write_text(report, encoding="utf-8")
    return {
        "metadata": metadata,
        "model": model.as_dict(),
        "evaluation": evaluation,
    }


__all__ = [
    "EXPERIMENT_FEATURE_SCHEMA",
    "EXPERIMENT_SCHEMA_VERSION",
    "MODEL_SCHEMA_VERSION",
    "CloudRunConfig",
    "CorpusManifestEntry",
    "OracleRecord",
    "TreeModel",
    "build_manifest",
    "evaluate_tree_model",
    "fit_tree_model",
    "generate_oracle_records",
    "run_pilot",
    "write_json",
    "write_jsonl",
]
