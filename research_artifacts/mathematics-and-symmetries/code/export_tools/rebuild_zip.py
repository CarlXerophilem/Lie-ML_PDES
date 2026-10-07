#!/usr/bin/env python3
"""Rebuild a portable export after changes; refresh manifest before creating ZIP."""
from pathlib import Path
import argparse, hashlib, json, zipfile

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[2]
out=args.out.resolve()
if out.is_relative_to(root):
    raise SystemExit('Choose an output path outside the project folder')

def eligible(p):
    rel=p.relative_to(root)
    return p.is_file() and not any(x in rel.parts for x in ['.git','__pycache__','.pytest_cache','build'])

paths=sorted(p for p in root.rglob('*') if eligible(p) and p.name!='FILE_MANIFEST.json')
records=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,
          'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
(root/'FILE_MANIFEST.json').write_text(json.dumps({'schema_version':1,'files':records},indent=2,ensure_ascii=False)+'\n')
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(p for p in root.rglob('*') if eligible(p)):
        z.write(p,root.name+'/'+p.relative_to(root).as_posix())
with zipfile.ZipFile(out) as z:
    bad=z.testzip()
    if bad:raise SystemExit('ZIP integrity failure: '+bad)
print(json.dumps({'zip':str(out),'bytes':out.stat().st_size,'files':len(records)+1}))
