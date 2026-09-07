"""Deterministic symmetry-aware prioritization for generic PDE systems."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import sympy as sp

from .core import DifferentialSystem, PointGenerator, ReductionCertificate, VALID_STATUSES
from .jets import prolonged_system
from .reduction import orbit_rank


SCHEMA_VERSION = "lieml.generic.reductor/1"
FEATURE_SCHEMA = (
    "independent_count",
    "field_count",
    "equation_count",
    "max_jet_order",
    "inequation_count",
    "assumption_count",
    "expression_nodes",
    "candidate_orbit_rank",
    "candidate_invariant",
)


def _expression_nodes(system: DifferentialSystem) -> int:
    expressions = (*system.equations, *system.inequations, *system.assumptions)
    return sum(int(sp.count_ops(expression, visual=False)) + 1 for expression in expressions)


def translation_candidates(system: DifferentialSystem) -> tuple[PointGenerator, ...]:
    """Return the canonical independent-coordinate translation family."""
    candidates = []
    for index in range(system.p):
        xi = tuple(sp.Integer(1) if item == index else sp.Integer(0)
                   for item in range(system.p))
        candidates.append(PointGenerator(xi, (sp.Integer(0),) * system.q))
    return tuple(candidates)


@dataclass(frozen=True)
class CandidateReduction:
    generator: PointGenerator
    score: float
    invariant: bool
    residuals: tuple[sp.Expr, ...]
    rationale: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "generator": self.generator.as_dict(),
            "score": self.score,
            "invariant": self.invariant,
            "residuals": [sp.srepr(value) for value in self.residuals],
            "rationale": list(self.rationale),
        }


@dataclass(frozen=True)
class ReductorRecord:
    system_fingerprint: str
    status: str
    feature_schema: tuple[str, ...]
    features: tuple[tuple[str, float], ...]
    candidates: tuple[CandidateReduction, ...]
    evidence: tuple[tuple[str, str], ...] = ()
    model: str = "deterministic-structure-v1"

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"invalid reductor status: {self.status}")
        object.__setattr__(self, "feature_schema", tuple(self.feature_schema))
        object.__setattr__(self, "features", tuple((str(k), float(v)) for k, v in self.features))
        object.__setattr__(self, "candidates", tuple(self.candidates))
        object.__setattr__(self, "evidence", tuple((str(k), str(v)) for k, v in self.evidence))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "system_fingerprint": self.system_fingerprint,
            "status": self.status,
            "feature_schema": list(self.feature_schema),
            "features": list(self.features),
            "candidates": [candidate.as_dict() for candidate in self.candidates],
            "evidence": list(self.evidence),
            "model": self.model,
        }


class PDEsReductor:
    """Rank cheap candidate reductions without changing certificate evidence."""

    def __init__(self, *, model: str = "deterministic-structure-v1") -> None:
        self.model = str(model)

    @staticmethod
    def _candidate_residuals(
        system: DifferentialSystem,
        generator: PointGenerator,
    ) -> tuple[sp.Expr, ...]:
        try:
            return tuple(sp.simplify(value) for value in prolonged_system(system, generator))
        except Exception as exc:
            return (sp.Symbol(f"unsupported_{type(exc).__name__}"),)

    def features(
        self,
        system: DifferentialSystem,
        generator: PointGenerator | None = None,
    ) -> tuple[tuple[str, float], ...]:
        candidate_rank = 0
        candidate_invariant = 0
        if generator is not None:
            candidate_rank = orbit_rank(system.jet_space, (generator,))
            candidate_invariant = int(all(
                value == 0 for value in self._candidate_residuals(system, generator)
            ))
        values = {
            "independent_count": float(system.p),
            "field_count": float(system.q),
            "equation_count": float(system.r),
            "max_jet_order": float(system.jet_space.max_order),
            "inequation_count": float(len(system.inequations)),
            "assumption_count": float(len(system.assumptions)),
            "expression_nodes": float(_expression_nodes(system)),
            "candidate_orbit_rank": float(candidate_rank),
            "candidate_invariant": float(candidate_invariant),
        }
        return tuple((name, values[name]) for name in FEATURE_SCHEMA)

    def rank(
        self,
        system: DifferentialSystem,
        candidates: Sequence[PointGenerator] | None = None,
        *,
        certificate: ReductionCertificate | None = None,
    ) -> ReductorRecord:
        """Rank candidates and preserve any supplied certificate status."""
        candidates = tuple(candidates or translation_candidates(system))
        base_features = self.features(system)
        ranked = []
        for generator in candidates:
            residuals = self._candidate_residuals(system, generator)
            invariant = bool(residuals) and all(value == 0 for value in residuals)
            rank = orbit_rank(system.jet_space, (generator,))
            score = float(2 * int(invariant) + int(rank > 0))
            rationale = (
                "prolonged residuals vanish" if invariant else "prolonged residuals not zero",
                "projected orbit has positive rank" if rank > 0 else "projected orbit rank is zero",
            )
            ranked.append(CandidateReduction(generator, score, invariant, residuals, rationale))
        ranked.sort(key=lambda item: (-item.score, item.generator.as_dict().__repr__()))
        status = certificate.status if certificate is not None else "unsupported"
        evidence = (
            ("certificate_status", status),
            ("certificate_upgrade_by_score", "forbidden"),
        )
        return ReductorRecord(
            system.fingerprint(),
            status,
            FEATURE_SCHEMA,
            base_features,
            tuple(ranked),
            evidence=evidence,
            model=self.model,
        )


def reductor_features(system: DifferentialSystem) -> dict[str, float]:
    """Small functional facade for callers that only need feature values."""
    return dict(PDEsReductor().features(system))
