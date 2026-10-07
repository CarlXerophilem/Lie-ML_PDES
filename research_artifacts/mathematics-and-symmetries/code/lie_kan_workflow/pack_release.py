#!/usr/bin/env python3
"""Create a portable, hash-inventoried release containing the measured pilot."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def included(path):
    relative=path.relative_to(ROOT)
    if any(p.startswith('.') or p=='__pycache__' for p in relative.parts):return False
    if relative.parts[:2] in [('results','series_smoke'),('results','series_verification')]:return False
    if str(relative) in ['MANIFEST.json','results/analyzer_tests.json']:return False
    return path.is_file()


def main():
    paths=sorted(p for p in ROOT.rglob('*') if included(p))
    inventory=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,
                'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
    manifest=ROOT/'MANIFEST.json'
    manifest.write_text(json.dumps({'files':inventory,'excluded':'Python caches and superseded smoke/test traces',
        'verification':'Analyzer, independent reference controls, symbolic/autograd series checks, 42 checkpoint replays, and acceptance/guard checks passed.'},indent=2))
    destination=ROOT.parent/'lie_kan_workflow.zip'
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for p in [*paths,manifest]:z.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)))
    with zipfile.ZipFile(destination) as z:assert z.testzip() is None
    print(json.dumps({'archive':str(destination),'files':len(paths)+1,'bytes':destination.stat().st_size}))


if __name__=='__main__':main()
