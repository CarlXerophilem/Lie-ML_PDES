# Priestess Handoff: 21 October 2026

The next remote task is **title, outline and source-question-evidence mapping
for the existing draft/dissertation.tex only**. Follow the
[writing plan](superpowers/plans/2026-10-21-dissertation-writing.md). Do not write
manuscript prose, restart pure PINN, launch a remote agent or copy authentication,
Codex configuration, sessions or unrelated state as part of this handoff.

## Recorded Preflight

The inspected checkout is `/home/carl/research/projects/Lie-ML_PDES`, branch
`astra`, clean at `78ecd5d`, an ancestor of precision-source baseline `11fe2a8`.
These are dated preflight facts, not a claim that the remote already contains
the final cleanup commit. Recheck HEAD, branch and status before updating.

| Component | Inspected state |
|---|---|
| Python | 3.12.14 |
| NumPy / SciPy / SymPy | 2.5.3 / 1.18.1 / 1.14.0 |
| Matplotlib / pytest / mpmath | 3.11.2 / 9.1.1 / 1.3.0 |
| PyTorch | 2.14, CPU only |
| Codex CLI | 0.163.0; inspection only, not permission to launch an agent |
| TeX / privilege | No TeX and no sudo; compile on Windows |
| Four earlier evidence carriers | Already restored, with all recorded hashes matching |

Environment inspection and restoration do not establish a fresh full Linux
numerical campaign. Archived Windows absolute paths remain immutable provenance;
current commands resolve from the Linux repository root.

## Sync Without Overwriting Local Work

Use the existing authorized GitHub remote/SSH setup. Never replace credentials
or remote configuration merely to match this example. From an interactive shell
on Priestess, stop on any dirty status, divergence or failed command:

```bash
set -eu
cd /home/carl/research/projects/Lie-ML_PDES
git status --short
test -z "$(git status --porcelain)" || { echo 'Preserve local work before syncing'; exit 1; }
git remote -v
git fetch origin astra
git switch astra
GIT_LFS_SKIP_SMUDGE=1 git merge --ff-only origin/astra
git lfs pull --include='ref/**,research_artifacts/sve-P-residual-20261021/**' --exclude='' origin
git rev-parse HEAD
git ls-remote origin refs/heads/astra
test "$(git rev-parse HEAD)" = "$(git ls-remote origin refs/heads/astra | cut -f1)"
git status --short
```

The final equality is the publication/synchronization check; a local commit,
successful fetch or clean status alone does not prove equality to GitHub.
If the branch diverged, inspect it and stop rather than resetting or force-pushing.
For a new Ubuntu machine, install Git/LFS/Python by its normal administrator
workflow, clone `astra`, and create a virtual environment as in the root README.
The current handoff does not need sudo or a new environment on Priestess.

## Restore Current Results

Use the inspected Python 3.12+ environment, verify its interpreter, then restore
from the repository root. Requirements are in requirements.txt; PyTorch is not
needed for the active workflow, and no dependency upgrade is required just to read.

```bash
python --version
export PYTHONUTF8=1 PYTHONHASHSEED=0
for archive in \
  research_artifacts/sve-current-20261021/current-build.zip \
  research_artifacts/sve-delivery-20261021/library-evidence.zip \
  research_artifacts/sve-delivery-20261021/printed-P-evidence.zip \
  research_artifacts/sve-delivery-20261021/other-current-evidence.zip
do
  python -X utf8 scripts/build_archive.py verify --archive "$archive"
  python -X utf8 scripts/build_archive.py restore --archive "$archive"
done
python -X utf8 scripts/evidence_archive.py verify --archive research_artifacts/sve-P-residual-20261021/precision-evidence.zip
python -X utf8 scripts/evidence_archive.py restore --archive research_artifacts/sve-P-residual-20261021/precision-evidence.zip --root .
```

The four original carriers are immutable. Repeated same-byte restoration is
allowed; a different-byte conflict must stop for inspection, not be overwritten.
The new precision carrier contains 401 files and supplements the frozen result:
12/12 exact, 21/21 seed and 11/11 high-precision-reference extended IVPs, while
the older raw float64 campaign still records 10/11. See the
[precision boundary](residual-resolution-20261021.md). No continuous PDE-error
certificate or general closed-form completion follows.

If a historical package is actually needed, first read its ARCHIVED.md stub
and verify only its named ZIP under research_artifacts/archives-20261021:

```bash
python -X utf8 scripts/evidence_archive.py verify --archive research_artifacts/archives-20261021/pilot.zip
python -X utf8 scripts/evidence_archive.py restore --archive research_artifacts/archives-20261021/pilot.zip --root .
```

Do not expand every archive. The missing external 11 October archive is a
nonblocking historical-provenance gap; its recovery is not this task.
The machine-local `build/publish-astra-20261021` staging tree is deliberately
retained outside publication/default search because it contains linked aliases
and nested checkout metadata; it is not a portable evidence carrier.

## Publish Later Ubuntu Changes

Stage only reviewed paths, never all local research or restored history:

```bash
git status --short
git add -- docs/superpowers/plans/2026-10-21-dissertation-writing.md
git diff --cached --stat
git commit -m "Update verified dissertation outline"
git fetch origin astra
git merge --ff-only origin/astra
git push origin HEAD:refs/heads/astra
test "$(git rev-parse HEAD)" = "$(git ls-remote origin refs/heads/astra | cut -f1)"
```

Stop on divergence. Do not force-push or stage unrelated files to make a sync pass.

## Focused Verification And Writing Boundary

After any source change, run the relevant checks, recording commands, exit codes
and limitations rather than relabelling old Windows receipts as Linux results:

```bash
python -B -X utf8 -m symm.LieSymm --check-integrity
python -B -X utf8 -m pytest -q -p no:cacheprovider symm/LieSymm/tests symm/LieSymm/scalar2026/tests
python -B -X utf8 -m pytest -q -p no:cacheprovider scripts/tests symm/tests/test_engine.py symm/tests/test_chart_reduction.py research_artifacts/sve-progress-20261010/tests
audit_exit=0
python -X utf8 scripts/project.py audit --out build/audit-priestess-NEW || audit_exit=$?
printf 'Audit exit: %s; inspect build/audit-priestess-NEW/audit.json\n' "$audit_exit"
test "$audit_exit" -le 1
python -X utf8 scripts/project.py data-flux --out build/data-flux-priestess-NEW
python -X utf8 scripts/project.py workflow --out build/workflow-priestess-NEW
```

The audit is expected to remain failed, not silently skipped: Windows has the
missing external archive; ordinary Linux also reports four frozen `/D:/...`
links in SUMMARY_1D.md because the existing audit normalizes them only on
Windows. Inspect the actual issue list for any additional regression. Capturing
exit 1 above lets the remaining independent checks run under `set -e`; it does
not turn the audit into a pass or authorize editing frozen source evidence.

The root README has native Windows latexmk commands. Restore build/week-4 before
building draft/dissertation.tex there, inspect citation/reference warnings and
rendered pages, and do not install remote TeX as an implicit handoff step.

For this next task, read README.md, docs/project-map.md, draft/main.tex,
draft/dissertation.tex, the current evidence index and the writing plan. Open
the cited source pages, map each question to a source/evidence/unknown status,
and return the bounded planning artifact. Do not silently synchronize dissertation
prose with main.tex or claim that later E/2D work is already complete.

`.ignore` only changes default ripgrep discovery. For deliberate evidence reads:

```bash
rg --no-ignore --files ref
rg --no-ignore -n --glob '*.md' 'failed|unresolved' research_artifacts/sve-1d-programme-20261021
rg --no-ignore --files symm/LieSymm/_snapshot/cases
```
