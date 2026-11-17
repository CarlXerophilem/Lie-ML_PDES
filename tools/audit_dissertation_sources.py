#!/usr/bin/env python3
"""Static checks for this manuscript's literal LaTeX and resource map.

No TeX expansion, source-claim validation, numerical replay or proof checking.
Optional --tree-json accepts a Git tree inventory for connector-based staging;
resource existence is then metadata-based and cannot establish LFS hydration.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


def audit(root, remote_paths=None):
    remote_paths = remote_paths or set()
    source = root / 'draft/dissertation_wku.tex'
    raw = source.read_bytes()
    text = re.sub(r'(?<!\\)%[^\n]*', '', raw.decode())
    manifest = json.loads((root / 'ref/dissertation-sources.json').read_text())
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    refs = re.findall(r'\\(?:ref|eqref|pageref|autoref|cref|Cref)\*?\{([^}]+)\}', text)
    refs = [k.strip() for group in refs for k in group.split(',')]
    bib = re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', text)
    cites = re.findall(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}', text)
    cites = [k.strip() for group in cites for k in group.split(',')]
    entries = manifest['entries']
    mapped = [e['key'] for e in entries]
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    def exists(path):
        return (root / path).exists() or path in remote_paths
    require(hashlib.sha256(raw).hexdigest() == manifest['source_sha256'], 'Source hash differs from citation inventory')
    for label, n in Counter(labels).items():
        require(n == 1, 'Duplicate label: ' + label)
    for key, n in Counter(bib).items():
        require(n == 1, 'Duplicate bibliography key: ' + key)
    require(not set(refs) - set(labels), 'Undefined references: ' + str(sorted(set(refs) - set(labels))))
    require(not set(cites) - set(bib), 'Undefined citations: ' + str(sorted(set(cites) - set(bib))))
    require(set(mapped) == set(bib) and len(mapped) == len(set(mapped)), 'Citation inventory keys differ from bibliography')
    graphics = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', text)
    for asset in graphics:
        require(exists('draft/' + asset), 'Missing graphic: ' + asset)
    inputs = re.findall(r'\\(?:input|include)\{([^}]+)\}', text)
    for name in inputs:
        require(exists('draft/' + name) or exists('draft/' + name + '.tex'), 'Missing TeX input: ' + name)
    for wrapper in ['main.tex', 'dissertation.tex']:
        p = root / 'draft' / wrapper
        require(p.exists(), 'Missing local wrapper: ' + wrapper)
        if p.exists():
            require(bool(re.search(r'\\input\{dissertation_wku(?:\.tex)?\}', p.read_text())), 'Unexpected wrapper target: ' + wrapper)
    for entry in entries:
        path = entry['path']
        if path:
            require(exists(path), 'Missing mapped resource: ' + path)
        if path and entry.get('sha256') and (root / path).is_file():
            require(hashlib.sha256((root / path).read_bytes()).hexdigest() == entry['sha256'], 'Resource hash mismatch: ' + path)
    return {
        'scope': 'Literal LaTeX cross-references and resource paths only; not claim/proof validation.',
        'resource_check_mode': 'local files plus Git tree metadata' if remote_paths else 'local files',
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'label_count': len(labels), 'reference_occurrences': len(refs),
        'bibliography_count': len(bib), 'citation_occurrences': len(cites),
        'uncited_bibliography_keys': sorted(set(bib) - set(cites)),
        'external_graphics': graphics,
        'bibliography_only': [e['key'] for e in entries if e['status'] == 'bibliography-only'],
        'lfs_resources': [e['path'] for e in entries if e['status'] == 'git-lfs-pointer'] + ['research_artifacts/annular-transcritical-theorem-20261101/theorem-evidence.zip'],
        'errors': errors, 'passed': not errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--tree-json', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    paths = set()
    if args.tree_json:
        obj = json.loads(args.tree_json.read_text())
        paths = {e['path'] for e in obj['tree']}
    result = audit(args.root, paths)
    rendered = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end='')
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
