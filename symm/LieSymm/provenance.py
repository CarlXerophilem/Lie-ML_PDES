"""Read-only package integrity and historical gate checks."""
import hashlib
import json
from pathlib import Path

from ._loader import PACKAGE_ROOT, SNAPSHOT_ROOT, load_module, snapshot_path


def verify_snapshot():
    manifest_path = PACKAGE_ROOT / "SOURCE_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    changed = []
    for name, record in manifest["files"].items():
        try:
            path = snapshot_path(name)
            if (not path.is_file() or path.stat().st_size != record["bytes"]
                    or hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]):
                changed.append(name)
        except (ValueError, OSError):
            changed.append(name)
    return {"passed": not changed, "changed": changed,
            "file_count": len(manifest["files"]), "total_bytes": manifest["total_bytes"],
            "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            "scope": "copied historical bytes; not a new mathematical review"}


def check_historical_gate(stage):
    """Check exact copied evidence; do not regenerate or re-sign old gates."""
    if stage not in (1, 2, 3):
        return {"passed": False, "reason": "unknown_stage"}
    if stage == 3:
        result = load_module("stage3_gate").check()
    else:
        result = load_module("gatekeeper").check_gate(stage)
    return {**result, "stage": stage, "evidence_kind": "frozen_historical_gate",
            "runtime_adapter_review": "separate_from_historical_gate"}


def verify_adapter():
    path = PACKAGE_ROOT / "PORT_MANIFEST.json"
    if not path.is_file():
        return {"passed": False, "reason": "port_manifest_missing"}
    manifest = json.loads(path.read_text(encoding="utf-8"))
    changed = []
    for name, expected in manifest["sha256"].items():
        try:
            item = snapshot_path(name, root=PACKAGE_ROOT)
            if not item.is_file() or hashlib.sha256(item.read_bytes()).hexdigest() != expected:
                changed.append(name)
        except (ValueError, OSError):
            changed.append(name)
    return {"passed": not changed, "changed": changed,
            "scope": "adapter release bytes; see fresh validation receipts for behavior"}


def provenance_summary():
    return {"source": "sve-general-symm-20261020", "source_policy": "byte-identical snapshot",
            "import_adapter": "module-local sibling imports; no bare module aliases",
            "gate_adapter": "separator-normalized relative names; unchanged SHA-256 comparison",
            "historical_gate_scope": "copied evidence, not a fresh portability review",
            "mathematical_scope": "declared SVE necessity certificates only; unknown PDE integration unresolved"}
