from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import zipfile


root = Path("research_artifacts/sve-progress-20261010")
archive_path = root / "lie-ml-sve-progress-20261010.zip"
manifest_path = root / "MANIFEST.json"
archive_tmp = root / "lie-ml-sve-progress-20261010.zip.tmp"
manifest_tmp = root / "MANIFEST.json.tmp"

payloads: dict[str, bytes] = {}
metadata: dict[str, zipfile.ZipInfo] = {}

with zipfile.ZipFile(archive_path) as source:
    assert source.testzip() is None
    names = [item.filename for item in source.infolist()]
    assert len(names) == len(set(names))
    prefix = names[0].split("/", 1)[0] + "/"
    for info in source.infolist():
        assert info.filename.startswith(prefix)
        relative = info.filename[len(prefix) :]
        if not relative or relative == "MANIFEST.json":
            continue
        payloads[relative] = source.read(info)
        metadata[relative] = info
    manifest_info = source.getinfo(prefix + "MANIFEST.json")

# Overlay every locally available packaged file, while retaining candidate
# arrays that intentionally exist only in the prior complete ZIP.
for relative in list(payloads):
    local = root / relative
    if local.is_file():
        payloads[relative] = local.read_bytes()

for relative in (
    "docs/EXPERIMENT_INDEX.md",
    "docs/LEGACY_MANUSCRIPT_EXPERIMENTS.tex",
):
    payloads[relative] = (root / relative).read_bytes()


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


manifest = {
    relative: {"size": len(payloads[relative]), "sha256": digest(payloads[relative])}
    for relative in sorted(payloads)
}
manifest_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode(
    "utf-8"
)
manifest_tmp.write_bytes(manifest_bytes)


def fresh_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(2026, 10, 10, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


with zipfile.ZipFile(archive_tmp, "w") as target:
    for relative in sorted(payloads):
        info = metadata.get(relative)
        if info is None:
            info = fresh_info(prefix + relative)
        target.writestr(info, payloads[relative])
    target.writestr(manifest_info, manifest_bytes)

with zipfile.ZipFile(archive_tmp) as check:
    assert check.testzip() is None
    names = [item.filename for item in check.infolist()]
    assert len(names) == len(set(names))
    assert set(names) == {prefix + name for name in manifest} | {
        prefix + "MANIFEST.json"
    }
    assert check.read(prefix + "MANIFEST.json") == manifest_bytes
    for relative, record in manifest.items():
        data = check.read(prefix + relative)
        assert len(data) == record["size"]
        assert digest(data) == record["sha256"]

os.replace(manifest_tmp, manifest_path)
os.replace(archive_tmp, archive_path)
print(f"manifest_entries={len(manifest)} zip_entries={len(manifest) + 1}")
