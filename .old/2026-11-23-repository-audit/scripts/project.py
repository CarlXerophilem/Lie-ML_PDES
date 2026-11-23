"""One entrypoint for the active manuscript, evidence audit and scalar examples."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    raw = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    return hashlib.sha256(raw).hexdigest()


def active_files(root: Path) -> list[str]:
    raw = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=root
    )
    return sorted({name for name in raw.decode().split("\0")
                   if name and ((root / name).is_file() or (root / name).is_symlink())})


def markdown_targets(text: str):
    """Read local link destinations, retaining balanced filename parentheses."""
    text = re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", text)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"(?s)\\\[.*?\\\]|\\\(.*?\\\)", "", text)
    # Mathematical bracket evaluation, e.g. $[X,Y](f)$, is not a file link.
    # Handle display dollars first, and leave escaped currency dollars alone.
    text = re.sub(r"(?s)(?<!\\)\$\$.*?(?<!\\)\$\$", "", text)
    text = re.sub(r"(?s)(?<!\\)\$(?!\$)(?:\\.|[^$])*?(?<!\\)\$", "", text)
    for match in re.finditer(r"\]\(", text):
        start = match.end()
        if text[start:start + 1] == "<":
            end = text.find(">", start)
            if end != -1:
                yield text[start + 1:end]
            continue
        depth, end = 1, start
        while end < len(text) and depth:
            char = text[end]
            if char == "(" and (end == 0 or text[end - 1] != "\\"):
                depth += 1
            elif char == ")" and (end == 0 or text[end - 1] != "\\"):
                depth -= 1
            if depth:
                end += 1
        if depth == 0:
            yield text[start:end].split(' "', 1)[0].strip()


def audit(root: Path, out: Path) -> dict:
    cleanup = json.loads((root / "docs/cleanup.json").read_text(encoding="utf-8"))
    inventory = json.loads((root / "ref/inventory.json").read_text(encoding="utf-8"))
    checks, issues = [], []

    def check(name, failures, **details):
        checks.append({"name": name, "passed": not failures, **details})
        issues.extend(f"{name}: {item}" for item in failures)

    archive = (root / cleanup["archive_relative"]).resolve()
    manifest_path = archive / "ARCHIVE_MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        failures = []
        for rel, item in manifest["files"].items():
            path = archive / rel
            if not (path.is_file() or path.is_symlink()) or digest(path) != item["sha256"]:
                failures.append(rel)
        check("available_history_preserved", failures,
              verified_entries=len(manifest["files"]), archive=str(archive))
    else:
        # Git preserves the source commit; only this machine carries the full
        # hydrated archive. Its absence is explicit, never a false validation.
        check("available_history_preserved", ["local external archive unavailable"], archive=str(archive))

    canonical = [r for r in inventory["records"] if r["availability"] == "canonical"]
    failures = []
    for record in canonical:
        path = root / record["path"]
        if not path.exists() or digest(path) != record["sha256"]:
            failures.append(record["citation_key"])
    check("canonical_reference_integrity", failures, citation_records=len(canonical))
    # The corpus was reorganized into main/, large-pdfs/ and small-pdfs/.
    # Canonical identity comes from the registered path and hash, not a folder.
    registered = {r["path"] for r in canonical}
    pdfs = sorted(root / name for name in registered if (root / name).is_file())
    hashes = [digest(path) for path in pdfs]
    check("unique_canonical_pdfs", ["duplicate SHA-256"] if len(hashes) != len(set(hashes)) else [],
          pdf_count=len(pdfs))
    canonical_folder_pdfs = sorted((root / "ref/pdfs").glob("*.pdf"))
    failures = [p.relative_to(root).as_posix() for p in canonical_folder_pdfs
                if p.relative_to(root).as_posix() not in registered]
    failures += [name for name in registered
                 if not (root / name).resolve().is_relative_to((root / "ref").resolve())]
    check("canonical_reference_inventory", failures)

    files = active_files(root)
    failures = []
    for rel in files:
        if not rel.endswith(".md"):
            continue
        path = root / rel
        for target in markdown_targets(path.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#") or not parsed.path:
                continue
            local_path = unquote(parsed.path)
            # Codex-rendered Windows file links use /D:/... . Preserve frozen
            # Markdown bytes while checking the actual native path, including
            # missing targets; this is not an exemption for archived links.
            if os.name == "nt" and re.match(r"^/[A-Za-z]:[/\\]", local_path):
                local_path = local_path[1:]
            destination = (path.parent / local_path).resolve()
            if not destination.exists():
                failures.append(f"{rel} -> {target}")
    check("active_markdown_links", failures)
    check("temporary_outputs_untracked", [rel for rel in files if rel.startswith(("tmp/", "build/"))])

    package = root / "research_artifacts/sve-progress-20261010"
    frozen = json.loads((package / "MANIFEST.json").read_text(encoding="utf-8"))
    missing, changed, frozen_failures = [], [], []
    with zipfile.ZipFile(package / "lie-ml-sve-progress-20261010.zip") as carrier:
        for rel, item in frozen.items():
            member = "lie-ml-sve-progress-20261010/" + rel
            try:
                raw = carrier.read(member)
                if hashlib.sha256(raw).hexdigest() != item["sha256"] or len(raw) != item["size"]:
                    frozen_failures.append(rel)
            except KeyError:
                frozen_failures.append(rel)
            path = package / rel
            if not path.exists():
                missing.append(rel)
            elif digest(path) != item["sha256"]:
                changed.append(rel)
    check("frozen_evidence_manifest", frozen_failures, verified_entries=len(frozen))
    # Also detect modifications to the carrier itself after the cleanup baseline.
    carrier_rel = "research_artifacts/sve-progress-20261010/lie-ml-sve-progress-20261010.zip"
    check("frozen_carrier_unchanged", [] if digest(root / carrier_rel) == cleanup["frozen_zip_sha256"] else [carrier_rel])
    result = {"status": "passed" if not issues else "failed", "checks": checks, "issues": issues,
              "original_tracked_count": cleanup["original_tracked_count"], "active_file_count": len(files),
              "reduction_percent": round(100 * (1 - len(files) / cleanup["original_tracked_count"]), 1),
              "frozen_vs_expanded": {"missing_but_in_zip": missing, "changed_from_frozen": changed},
              "local_only_references": [r["citation_key"] for r in inventory["records"] if r["availability"] == "local-only"],
              "citation_validation": "Inventory is a navigation aid. Native LaTeX build/logs validate citations and cross-references."}
    out.mkdir(parents=True, exist_ok=True)
    (out / "audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Active project audit", "", f"Status: **{result['status']}**.", "",
             f"Active files: {len(files)}; baseline: {cleanup['original_tracked_count']} ({result['reduction_percent']}% fewer).", "",
             f"Canonical PDFs: {len(pdfs)}. Frozen entries checked: {len(frozen)}.", "",
             f"Expanded evidence: {len(missing)} omitted files recoverable from ZIP; {len(changed)} files differ from frozen versions.", "",
             "| Check | Result |", "|---|---|"]
    lines += [f"| {c['name']} | {'PASS' if c['passed'] else 'FAIL'} |" for c in checks]
    if issues:
        lines += ["", "Issues:", ""] + [f"- {issue}" for issue in issues]
    (out / "audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "workflow", "data-flux"))
    parser.add_argument("--out", type=Path, help="fresh output directory (default: build/<command>)")
    parser.add_argument("--data-report", type=Path,
                        help="verified data_flux.json to link into the workflow")
    args = parser.parse_args(argv)
    out = (args.out or ROOT / "build" / args.command).resolve()
    # Public commands cannot overwrite manuscript source or preserved evidence.
    archive = (ROOT.parent / "Lie-ML_PDES-archive").resolve()
    protected = (ROOT / "draft", ROOT / "ref", ROOT / "research_artifacts", ROOT / "symm", ROOT / "scripts", ROOT / "docs", ROOT / ".git", archive)
    if out == ROOT or any(out == path or path in out.parents for path in protected):
        parser.error("--out must be outside source/evidence directories; use build/<command>")
    if args.data_report is not None and args.command != "workflow":
        parser.error("--data-report applies only to workflow")
    out.mkdir(parents=True, exist_ok=True)
    if args.command == "audit":
        result = audit(ROOT, out)
    elif args.command == "workflow":
        from project_workflow import run
        result = run(ROOT, out, data_report=args.data_report)
    else:
        from project_data_flux import run
        result = run(ROOT, out)
    print(json.dumps({"command": args.command, "status": result["status"], "out": str(out)}, indent=2))
    return 0 if result["status"] in ("passed", "verified") else 1


if __name__ == "__main__":
    sys.exit(main())
