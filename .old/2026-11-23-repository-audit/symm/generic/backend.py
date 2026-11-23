"""Backend-neutral requests, resource limits, and vendor-runtime discovery.

The local package never imports Maple or REDUCE syntax.  A request can still
be serialized and audited when a vendor runtime is absent, which keeps an
unavailable oracle distinct from a verified Python calculation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import shutil
from typing import Any

from .core import (
    DifferentialRanking,
    DifferentialSystem,
    GenericValidationError,
    VALID_STATUSES,
    configuration_fingerprint,
    fingerprint,
)


SCHEMA_VERSION = "lieml.generic.backend/1"


@dataclass(frozen=True)
class ResourceLimits:
    """Deterministic limits for local and subprocess phases."""

    soft_memory_bytes: int = 1_200_000_000
    hard_memory_bytes: int = 1_800_000_000
    timeout_seconds: float = 30.0
    max_jet_order: int = 6
    max_branches: int = 32
    max_expression_nodes: int = 250_000
    max_serialized_bytes: int = 8_000_000

    def __post_init__(self) -> None:
        if self.soft_memory_bytes <= 0 or self.hard_memory_bytes <= 0:
            raise GenericValidationError("memory limits must be positive")
        if self.soft_memory_bytes >= self.hard_memory_bytes:
            raise GenericValidationError("soft memory limit must be below hard limit")
        if self.timeout_seconds <= 0:
            raise GenericValidationError("timeout must be positive")
        if any(
            int(value) <= 0
            for value in (self.max_jet_order, self.max_branches,
                          self.max_expression_nodes, self.max_serialized_bytes)
        ):
            raise GenericValidationError("resource caps must be positive")
        object.__setattr__(self, "soft_memory_bytes", int(self.soft_memory_bytes))
        object.__setattr__(self, "hard_memory_bytes", int(self.hard_memory_bytes))
        object.__setattr__(self, "timeout_seconds", float(self.timeout_seconds))
        object.__setattr__(self, "max_jet_order", int(self.max_jet_order))
        object.__setattr__(self, "max_branches", int(self.max_branches))
        object.__setattr__(self, "max_expression_nodes", int(self.max_expression_nodes))
        object.__setattr__(self, "max_serialized_bytes", int(self.max_serialized_bytes))

    def as_dict(self) -> dict[str, Any]:
        return {
            "soft_memory_bytes": self.soft_memory_bytes,
            "hard_memory_bytes": self.hard_memory_bytes,
            "timeout_seconds": self.timeout_seconds,
            "max_jet_order": self.max_jet_order,
            "max_branches": self.max_branches,
            "max_expression_nodes": self.max_expression_nodes,
            "max_serialized_bytes": self.max_serialized_bytes,
        }

    def fingerprint(self) -> str:
        return configuration_fingerprint(self.as_dict())


@dataclass(frozen=True)
class BackendAvailability:
    name: str
    available: bool
    executable: str | None = None
    reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "available": self.available,
            "executable": self.executable,
            "reason": self.reason,
        }


_EXECUTABLE_NAMES = {
    "maple": ("maple", "maple.exe"),
    "reduce": ("redps", "reduce", "reduce.exe", "redps.exe"),
}


def detect_backend(name: str) -> BackendAvailability:
    """Discover an executable without importing or invoking vendor code."""
    normalized = str(name).strip().lower()
    candidates = _EXECUTABLE_NAMES.get(normalized)
    if candidates is None:
        return BackendAvailability(normalized, False, reason="unknown backend")
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return BackendAvailability(normalized, True, path, "executable found")
    return BackendAvailability(
        normalized,
        False,
        reason="no supported executable found on PATH",
    )


@dataclass(frozen=True)
class BackendRequest:
    system: DifferentialSystem
    task: str
    backend: str
    ranking: DifferentialRanking | None = None
    version_constraint: str = ""
    limits: ResourceLimits = field(default_factory=ResourceLimits)
    options: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if self.task not in {"completion", "determining", "normal_form", "reduction"}:
            raise GenericValidationError("unsupported backend task")
        if not self.backend:
            raise GenericValidationError("backend name is required")
        object.__setattr__(self, "ranking", self.ranking or self.system.jet_space.ranking)
        object.__setattr__(self, "options", tuple((str(k), str(v)) for k, v in self.options))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "system": self.system.as_dict(),
            "system_fingerprint": self.system.fingerprint(),
            "task": self.task,
            "backend": self.backend,
            "ranking": self.ranking.as_dict(),
            "version_constraint": self.version_constraint,
            "limits": self.limits.as_dict(),
            "options": list(self.options),
        }

    def fingerprint(self) -> str:
        return fingerprint(self.as_dict())


@dataclass(frozen=True)
class BackendResponse:
    request_fingerprint: str
    backend: str
    status: str
    branches: tuple[dict[str, Any], ...] = ()
    diagnostics: tuple[str, ...] = ()
    divisions: tuple[str, ...] = ()
    verification: tuple[tuple[str, bool], ...] = ()
    version: str = "unknown"
    output_fingerprint: str = ""

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise GenericValidationError(f"invalid backend status: {self.status}")
        object.__setattr__(self, "branches", tuple(self.branches))
        object.__setattr__(self, "diagnostics", tuple(str(item) for item in self.diagnostics))
        object.__setattr__(self, "divisions", tuple(str(item) for item in self.divisions))
        object.__setattr__(self, "verification", tuple(
            (str(key), bool(value)) for key, value in self.verification
        ))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "request_fingerprint": self.request_fingerprint,
            "backend": self.backend,
            "status": self.status,
            "branches": list(self.branches),
            "diagnostics": list(self.diagnostics),
            "divisions": list(self.divisions),
            "verification": list(self.verification),
            "version": self.version,
            "output_fingerprint": self.output_fingerprint,
        }


def request_backend(request: BackendRequest) -> BackendResponse:
    """Return an auditable response for the installed-backend boundary.

    Executable discovery is intentionally separate from adapter execution.  A
    found executable therefore yields ``unsupported`` until a version-pinned
    adapter is supplied, rather than an unverified success claim.
    """
    availability = detect_backend(request.backend)
    if request.backend.lower() not in _EXECUTABLE_NAMES:
        status = "unsupported"
        diagnostics = (availability.reason,)
    elif not availability.available:
        status = "backend-unavailable"
        diagnostics = (availability.reason,)
    else:
        status = "unsupported"
        diagnostics = ("runtime found but no version-pinned adapter is enabled",)
    response = BackendResponse(
        request_fingerprint=request.fingerprint(),
        backend=request.backend,
        status=status,
        diagnostics=diagnostics,
        verification=(("independent_python_check", False),),
        version="unknown",
    )
    return BackendResponse(
        **{**response.__dict__, "output_fingerprint": fingerprint(response.as_dict())}
    )
