"""Bounded, serial, read-only verification of the reviewed release.

Writes only to a fresh --out directory. No CAS solver is executed. A successful
check is never promoted to mathematical classification acceptance.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DELIVERY = ROOT / "research_artifacts/sve-final-20261027"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((DELIVERY / "archive-receipt.json").read_text(encoding="utf-8"))
    archive = DELIVERY / "evidence.zip"
    bad = []
    with zipfile.ZipFile(archive) as zipped:
        for name, row in manifest["files"].items():
            content = zipped.read(name)
            if len(content) != row["bytes"] or hashlib.sha256(content).hexdigest() != row["sha256"]:
                bad.append(name)
        members = [v for v in zipped.namelist() if not v.endswith("/")]
        extra_members = sorted(set(members) - set(manifest["files"]))
    pins = json.loads((DELIVERY / "published-source-hashes.json").read_text(encoding="utf-8"))
    changed_sources = [name for name, sha in pins.items() if digest(ROOT / name) != sha]
    thesis = ROOT / "draft/dissertation_2026 (1).pdf"
    thesis_tex = thesis.with_suffix(".tex")
    expected = json.loads((DELIVERY / "data/dissertation-validation.json").read_text(encoding="utf-8"))
    import fitz
    with fitz.open(thesis) as doc:
        pages = len(doc)
        text = "\n".join(page.get_text() for page in doc)
    coverage = json.loads((DELIVERY / "data/delivery-analysis.json").read_text(encoding="utf-8"))
    remote = json.loads((DELIVERY / "data/remote-summary.json").read_text(encoding="utf-8"))
    inventory = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "reviewed_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "archive_sha256": digest(archive),
        "archive_hash_matches": digest(archive) == manifest["archive_sha256"],
        "archive_manifest_files": len(manifest["files"]),
        "archive_bad_files": bad,
        "archive_extra_members": extra_members,
        "source_pins_checked": len(pins),
        "source_pin_mismatches": changed_sources,
        "pdf_sha256": digest(thesis),
        "pdf_matches_receipt": digest(thesis) == expected["pdf_sha256"],
        "tex_matches_receipt": digest(thesis_tex) == expected["source_sha256"],
        "pdf_pages": pages,
        "main_chapters": expected["main_chapters"],
        "pdf_claims_text_checked": "complete parameter classification" in text.lower(),
        "total_inputs": len(coverage["coverage"]),
        "strict_pass_inputs": sum(row["strict_pass"] for row in coverage["coverage"]),
        "determining_completeness": dict(Counter(row["determining_completeness"] for row in coverage["coverage"])),
        "data_status": dict(Counter(row["data_status"] for row in coverage["coverage"])),
        "recorded_cas_seconds_sum": sum(row["elapsed_seconds"] for row in remote["jobs"]),
        "recorded_cas_seconds_claimed": remote["charged_seconds"],
        "fresh_cas_seconds": 0,
        "mathematical_acceptance": "incomplete",
    }
    save(out / "inventory.json", inventory)
    py = [sys.executable, "-B", "-X", "utf8"]
    pytest = ["-m", "pytest", "-q", "-p", "no:cacheprovider"]
    active = ["symm/LieSymm/tests", "symm/LieSymm/scalar2026/tests", "scripts/tests",
              "symm/tests/test_engine.py", "symm/tests/test_chart_reduction.py",
              "research_artifacts/sve-progress-20261010/tests"]
    active += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "symm/tests").glob("test_generic_*.py"))]
    jobs = [
        ("active-regression", pytest + active),
        ("historical-regression", pytest + ["symm/LieSymm/_snapshot/tests"]),
        ("integrity", ["-m", "symm.LieSymm", "--check-integrity"]),
        ("audit", ["scripts/project.py", "audit", "--out", str(out / "audit")]),
        ("data-flux", ["scripts/project.py", "data-flux", "--out", str(out / "data-flux")]),
        ("workflow", ["scripts/project.py", "workflow", "--out", str(out / "workflow"),
                      "--data-report", str(out / "data-flux/data_flux.json")]),
        ("generic-revalidation", ["scripts/analyze_strict_remote.py", "--out", str(out / "generic")]),
    ]
    rows = []
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONHASHSEED": "0",
           "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"}
    for name, arguments in jobs:
        started = time.monotonic()
        utc = datetime.now(timezone.utc).isoformat()
        log = out / (name + ".log")
        with log.open("wb") as stream:
            try:
                result = subprocess.run(py + arguments, cwd=ROOT, env=env,
                                        stdout=stream, stderr=subprocess.STDOUT, timeout=300)
                status, code = "finished", result.returncode
            except subprocess.TimeoutExpired:
                status, code = "timeout", None
        rows.append({"name": name, "command": py + arguments, "cwd": str(ROOT),
                     "started_utc": utc, "elapsed_seconds": time.monotonic() - started,
                     "timeout_seconds": 300, "status": status, "returncode": code,
                     "log_sha256": digest(log)})
        save(out / "commands.json", rows)
        print(name, status, code, flush=True)
        if status == "timeout":
            print("Stopped serial checks after timeout; descendant cleanup not certified.", flush=True)
            break
    # Review checks are recorded individually; inherited failures remain nonzero.
    return int(bool(bad or changed_sources) or any(row["returncode"] != 0 for row in rows))


if __name__ == "__main__":
    raise SystemExit(main())
