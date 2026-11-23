"""Build a source/manuscript deployment snapshot without secrets or old runs.

Usage: python -B -m symm.fluid_baselines.package --output release.tar.gz
The archive is a snapshot of working files, not a Git commit or history export.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import tarfile


def package(output):
    root = Path(__file__).resolve().parents[2]
    allowed = {".py",".md",".txt",".tex",".json",".csv",".yaml",".yml",".toml",".ini",".cfg",".sh",".html",".js",".bib",".service"}
    excluded = {"__pycache__",".pytest_cache","node_modules","archive","runs","output","outputs","results"}
    selected = []
    for directory in ("symm","configs","docs","draft"):
        for path in (root/directory).rglob("*"):
            relative = path.relative_to(root)
            if path.is_file() and not path.is_symlink() and not set(relative.parts)&excluded and path.suffix.lower() in allowed:
                if path.stat().st_size <= 20*1024*1024:
                    selected.append(path)
    selected += [p for p in root.iterdir() if p.is_file() and (p.suffix in {".md",".tex"} or p.name in {"plan.txt"})]
    selected += [p for p in (root/"draft/main.pdf",root/"draft/proposal(1).pdf") if p.exists()]
    selected = sorted(set(selected))
    manifest = {"scope":"working source, configs, docs, draft text, main/proposal PDFs",
                "excluded":"Git history, credentials/runtime state, reference library, pdf2md, archived runs, caches, other binaries, files over 20 MiB",
                "sha256":{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in selected}}
    output = Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists():
        raise FileExistsError(output)
    with tarfile.open(output,"w:gz") as archive:
        for path in selected:
            archive.add(path,arcname=path.relative_to(root).as_posix(),recursive=False)
        raw = (json.dumps(manifest,indent=2)+"\n").encode()
        info = tarfile.TarInfo("deployment_manifest.json")
        info.size = len(raw)
        archive.addfile(info,io.BytesIO(raw))
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(json.dumps({"archive":str(output),"sha256":digest,"files":len(selected),"bytes":output.stat().st_size},indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    package(parser.parse_args().output)
