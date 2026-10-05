#!/usr/bin/env bash
# Smoke test for the pdf2md app (../../pdf2md/pdf2md.py).
# Runs the offline (no-API) path end to end and asserts the artifacts
# exist and are non-trivial. Exits non-zero on any failure.
#
# Usage:  bash .claude/skills/run-pdf-extractor/smoke.sh [PDF]
# Run from the unit root (D:/MATHs/math 4890 LieML).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
APP="$ROOT/pdf2md/pdf2md.py"
PDF="${1:-$ROOT/ref/Generalized Lie Symmetries in Physics-Informed Neural Operators.pdf}"
OUT="$(mktemp -d)/smoke_out"
STEM="$(basename "$PDF" .pdf)"

echo "== probe =="
python "$APP" --probe

echo "== convert (local, 2 pages) =="
python "$APP" "$PDF" "$OUT" --max-pages 2 --dpi 100

echo "== assert artifacts =="
DOC="$OUT/$STEM/document.md"
test -f "$DOC"                         || { echo "FAIL: no document.md"; exit 1; }
test -f "$OUT/$STEM/manifest.json"     || { echo "FAIL: no manifest.json"; exit 1; }
test -f "$OUT/$STEM/pages/page-001.png"|| { echo "FAIL: no page-001.png"; exit 1; }
test -f "$OUT/index.md"                || { echo "FAIL: no index.md"; exit 1; }
chars=$(wc -c < "$DOC")
test "$chars" -gt 500 || { echo "FAIL: document.md too small ($chars bytes)"; exit 1; }

echo "PASS: smoke ok ($chars bytes of markdown) -> $DOC"
rm -rf "$(dirname "$OUT")"
