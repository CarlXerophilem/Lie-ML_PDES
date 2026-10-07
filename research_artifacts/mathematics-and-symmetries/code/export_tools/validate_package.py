#!/usr/bin/env python3
"""Validate archive identity and bibliography/file coverage without ML dependencies."""
from pathlib import Path
import ast
import hashlib
import json
import re

root = Path(__file__).resolve().parents[2]
manifest_path = root / 'FILE_MANIFEST.json'
if not manifest_path.is_file():
    raise SystemExit('FILE_MANIFEST.json is missing; run after export assembly')
manifest = json.loads(manifest_path.read_text())
failures = []
for record in manifest['files']:
    p = root / record['path']
    if not p.is_file(): failures.append('missing: ' + record['path']); continue
    if p.stat().st_size != record['bytes']: failures.append('size: ' + record['path'])
    if hashlib.sha256(p.read_bytes()).hexdigest() != record['sha256']:
        failures.append('hash: ' + record['path'])

py_count = 0
for p in (root / 'code').rglob('*.py'):
    try: ast.parse(p.read_text(), filename=str(p))
    except (SyntaxError, UnicodeError) as e: failures.append(str(e))
    py_count += 1

bib_text = (root/'references.bib').read_text() + '\n' + (root/'references/archived_sources.bib').read_text()
keys = set(re.findall(r'@\w+\s*\{\s*([^,\s]+)', bib_text))
tex = (root/'main(1).tex').read_text()
cited = {k.strip() for block in re.findall(r'\\(?:cite\w*|nocite)(?:\[[^\]]*\])?\{([^}]+)\}', tex)
         for k in block.split(',') if k.strip() != '*'}
for key in cited - keys: failures.append('unresolved citation: ' + key)

pdf_index = json.loads((root/'references/pdf-citations.json').read_text())
for record in pdf_index:
    if record['bibtex_key'] not in keys: failures.append('PDF key: ' + record['path'])
    if not (root/record['path']).is_file(): failures.append('PDF absent: ' + record['path'])
links = json.loads((root/'references/link-inventory.json').read_text())
for record in links:
    if record['bibtex_key'] not in keys: failures.append('link key: ' + record['url'])

result={'status':'failed' if failures else 'passed', 'manifest_files':len(manifest['files']),
        'python_sources':py_count, 'manuscript_citation_keys':len(cited),
        'indexed_source_pdfs':len(pdf_index), 'indexed_http_links':len(links), 'failures':failures}
print(json.dumps(result,indent=2))
raise SystemExit(bool(failures))
