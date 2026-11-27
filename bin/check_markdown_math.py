#!/usr/bin/env python3
"""Check current Markdown formulas; optionally parse them with a local KaTeX module.

Usage: python bin/check_markdown_math.py [--katex-module /path/to/katex.mjs]
Without the optional renderer only delimiter and known portability checks run.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {".old", ".agents", ".claude", ".git", "build", ".venv", "dist"}


def formulas():
    for path in sorted(ROOT.rglob("*.md")):
        if EXCLUDE.intersection(path.relative_to(ROOT).parts):
            continue
        text = path.read_text()
        # Mask code, including embedded shell/TeX examples, without changing line offsets.
        def mask(match):
            return re.sub(r"[^\n]", " ", match.group())
        text = re.sub(r"(?ms)^[ \t]*(?:```+|~~~+)[^\n]*\n.*?^[ \t]*(?:```+|~~~+)[^\n]*(?:\n|$)", mask, text)
        text = re.sub(r"`+[^`\n]+`+", mask, text)
        text = re.sub(r"<!--.*?-->", mask, text, flags=re.S)
        pattern = re.compile(r"(?<!\\)\$\$(.*?)\$\$|(?<![\\$])\$(?!\$)([^$\n]+?)\$(?!\$)", re.S)
        for m in pattern.finditer(text):
            value = m.group(1) if m.group(1) is not None else m.group(2)
            yield {"path": str(path.relative_to(ROOT)), "line": text.count("\n", 0, m.start()) + 1,
                   "tex": value.strip(), "display": m.group(1) is not None}
        uncovered = pattern.sub(mask, text)
        for m in re.finditer(r"(?<!\\)\$|\\[\[\]()]", uncovered):
            yield {"path": str(path.relative_to(ROOT)), "line": text.count("\n", 0, m.start()) + 1,
                   "invalid": "unpaired or nonportable math delimiter", "tex": m.group()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--katex-module")
    args = parser.parse_args()
    rows = list(formulas())
    failures = [r for r in rows if "invalid" in r or re.search(r"\\(?:operatorname|degree)(?![a-zA-Z])", r["tex"])]
    good = [r for r in rows if "invalid" not in r]
    if args.katex_module:
        js = """
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
const katex = (await import(pathToFileURL(process.argv[1]).href)).default;
const rows = JSON.parse(fs.readFileSync(0, 'utf8'));
const errors = [];
for (const row of rows) {
  try { katex.renderToString(row.tex, {throwOnError:true, displayMode:row.display, strict:'ignore'}); }
  catch (e) { errors.push({...row, invalid:String(e.message)}); }
}
console.log(JSON.stringify(errors));
"""
        result = subprocess.run(["node", "--input-type=module", "-e", js, str(Path(args.katex_module).resolve())],
                                input=json.dumps(good), text=True, capture_output=True, check=True)
        failures += json.loads(result.stdout)
    print(json.dumps({"formulas": len(good), "rendered": bool(args.katex_module), "failures": failures},
                     indent=2, ensure_ascii=False))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
