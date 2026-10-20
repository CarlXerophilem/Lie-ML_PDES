# Build cleanup and restore — 21 October 2026

25 build directories whose latest file predates 19 October were hash-archived.
The archive holds 6,927 files / 1,313,541,529 original bytes; its size is
1,172,045,698 bytes. It is machine-local, outside the active repository:

`D:/MATHs/Lie-ML_PDES-archive/2026-10-21/pre-20261019-build.zip`

SHA256: `8c14e984863d510af42bd67e60d9cfd3c218914c126922efe3fe463854e98530`.
The adjacent `pytest-cache-aliases.json` records 182 optional pytest `current`
symlinks. Their numbered targets were preserved; aliases alone were unlinked
before packing. No junction or outside-target link was followed.
Its SHA256 is `bb645c9ba967e22cbd79048bcfa279b04b6ed5abbb2988f676f0577209711cec`.

The guarded archive utility requires Python 3.12 or later (validated with 3.14.2).

From the repository root:

```powershell
python -X utf8 scripts/build_archive.py verify --archive 'D:/MATHs/Lie-ML_PDES-archive/2026-10-21/pre-20261019-build.zip'
python -X utf8 scripts/build_archive.py restore --archive 'D:/MATHs/Lie-ML_PDES-archive/2026-10-21/pre-20261019-build.zip' --directory sve-equation27-manim-20261017
```

Restore checks every archived hash, rejects traversal and refuses to overwrite
different bytes. Omit `--directory` to restore all old build children. The video
README, PRESENTER_NOTES.md and production/ONLINE_CHECK.md are available after
restoring that named directory. Historical bare paths inside dated records are
retained as execution provenance, rather than presented as currently live links.

`build/week-4` is retained because `draft/dissertation.tex` directly inputs its
measured table and PDF figure. The 19/20 October evidence also remains live.
These inputs are included in the [portable current snapshot](../research_artifacts/sve-current-20261021/README.md).

146 tracked `tmp/` files were removed from Git tracking only. Their current
local bytes remain intact. Their original committed bytes remain recoverable
from commit `84df778685db89100e3debbe27e61e7c897cabb9`; a per-file hash manifest
is included in the refresh receipt package.

This archive is distinct from the absent 11 October hydrated archive referenced
by `cleanup.json`. That older source commit is in Git, but the absent external
manifest cannot be certified. The project audit continues to report this gap.
Frozen ZIPs, release gates and historical failure receipts were not rewritten.
