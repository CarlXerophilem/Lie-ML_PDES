"""Preservation audit catches corrupted carriers and misleading Markdown."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest

from scripts.project import audit, markdown_targets, ROOT


def _hash(raw):
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def small_project(tmp_path, monkeypatch):
    root = tmp_path / "project"
    archive = tmp_path / "archive"
    (root / "docs").mkdir(parents=True)
    (root / "ref/pdfs").mkdir(parents=True)
    archive.mkdir()
    (archive / "history.md").write_text("unique history\n")
    (archive / "ARCHIVE_MANIFEST.json").write_text(json.dumps({"files": {
        "history.md": {"sha256": _hash(b"unique history\n"), "type": "file"}}}))
    (root / "ref/inventory.json").write_text(json.dumps({"records": []}))
    package = root / "research_artifacts/sve-progress-20261010"
    package.mkdir(parents=True)
    raw = b"frozen source\n"
    (package / "MANIFEST.json").write_text(json.dumps({"source.py": {
        "sha256": _hash(raw), "size": len(raw)}}))
    carrier = package / "lie-ml-sve-progress-20261010.zip"
    with zipfile.ZipFile(carrier, "w") as z:
        z.writestr("lie-ml-sve-progress-20261010/source.py", raw)
    (root / "docs/cleanup.json").write_text(json.dumps({
        "archive_relative": "../archive", "original_tracked_count": 10,
        "frozen_zip_sha256": _hash(carrier.read_bytes())}))
    monkeypatch.setattr("scripts.project.active_files", lambda _: ["docs/cleanup.json"])
    return root, archive, carrier


def test_missing_expanded_evidence_is_not_a_false_carrier_failure(small_project, tmp_path):
    root, _, _ = small_project
    result = audit(root, tmp_path / "out")
    assert result["status"] == "passed"
    assert result["frozen_vs_expanded"]["missing_but_in_zip"] == ["source.py"]


def test_archive_corruption_is_reported(small_project, tmp_path):
    root, archive, _ = small_project
    (archive / "history.md").write_text("lost provenance\n")
    result = audit(root, tmp_path / "out")
    assert result["status"] == "failed"
    assert any("available_history_preserved" in item for item in result["issues"])


def test_frozen_zip_corruption_is_reported(small_project, tmp_path):
    root, _, carrier = small_project
    with zipfile.ZipFile(carrier, "w") as z:
        z.writestr("lie-ml-sve-progress-20261010/source.py", b"rewritten evidence")
    result = audit(root, tmp_path / "out")
    assert result["status"] == "failed"
    assert any("frozen_evidence_manifest" in item for item in result["issues"])
    assert any("frozen_carrier_unchanged" in item for item in result["issues"])


def test_math_and_examples_do_not_become_files():
    text = "\\([p^2q^2](q^3\\Omega)\\) `![placeholder](missing)`\n"
    text += "```text\n[example](absent)\n```\n"
    text += "[real](<papers/name (version).pdf>) [nested](paper(v2).pdf)"
    assert list(markdown_targets(text)) == ["papers/name (version).pdf", "paper(v2).pdf"]


@pytest.mark.parametrize("path", ["draft", "ref/pdfs", ".git", "../Lie-ML_PDES-archive/2026-10-11"])
def test_cli_rejects_overwriting_preserved_sources(path):
    result = subprocess.run([sys.executable, str(ROOT / "scripts/project.py"),
                             "audit", "--out", str(ROOT / path)], capture_output=True, text=True)
    assert result.returncode == 2
    assert "outside source/evidence" in result.stderr
