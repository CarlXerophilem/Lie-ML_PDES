"""Small process-memory guard used by bounded generic phases."""

from __future__ import annotations

from dataclasses import dataclass
import os

from .backend import ResourceLimits


class ResourceLimitError(RuntimeError):
    """Raised when the current process exceeds a configured hard limit."""


@dataclass(frozen=True)
class MemorySnapshot:
    rss_bytes: int | None
    soft_exceeded: bool
    hard_exceeded: bool
    source: str

    def as_dict(self) -> dict[str, int | bool | str | None]:
        return {
            "rss_bytes": self.rss_bytes,
            "soft_exceeded": self.soft_exceeded,
            "hard_exceeded": self.hard_exceeded,
            "source": self.source,
        }


def current_rss_bytes() -> tuple[int | None, str]:
    """Read RSS through psutil when present, with a standard-library fallback."""
    try:
        import psutil
        return int(psutil.Process(os.getpid()).memory_info().rss), "psutil"
    except Exception:
        pass
    try:
        import resource
        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        # Linux reports KiB; Windows builds generally do not expose resource.
        if os.name != "nt":
            value *= 1024
        return value, "resource"
    except Exception:
        return None, "unavailable"


def memory_snapshot(limits: ResourceLimits | None = None) -> MemorySnapshot:
    limits = limits or ResourceLimits()
    rss, source = current_rss_bytes()
    return MemorySnapshot(
        rss,
        rss is not None and rss > limits.soft_memory_bytes,
        rss is not None and rss > limits.hard_memory_bytes,
        source,
    )


def enforce_memory_limit(limits: ResourceLimits | None = None) -> MemorySnapshot:
    """Fail closed at a phase boundary when RSS is already above the hard cap."""
    snapshot = memory_snapshot(limits)
    if snapshot.hard_exceeded:
        raise ResourceLimitError(
            f"RSS {snapshot.rss_bytes} exceeds hard limit "
            f"{(limits or ResourceLimits()).hard_memory_bytes}"
        )
    return snapshot
