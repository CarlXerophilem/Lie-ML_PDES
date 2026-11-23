# Validation record — 1 November 2026

Publication note: this is the recorded local theorem-package audit. Its original source PDFs, extracted text and raw alphaXiv page bodies remain local; consult SOURCE_AUDIT.json for versions, hashes and public URLs. Detailed validation paths are available after restoring theorem-evidence.zip.

The mathematical proof is in the note. This record documents executable algebra, regression checks, source/version bindings and rendering. Tests and hashes do not replace the theorem's argument.

| Check | Observed result | Scope / limitation |
|---|---|---|
| Fresh reviewed chain | Four serial stages exited successfully | Original PDE determining solve → derived invariants → derived closure/reduction → independent Cartesian checker |
| Determining computation | 84 distinct constraints, rank 50, six directions | Exact rational shared affine class only; unsplit identities checked |
| Invariant pivot coverage | Time/bed row `[1,c]` with unit pivot | Includes `c=0` without parameter division |
| Cartesian identities | Original mass, both momentum and Exner identities passed; bed-slope fault detected | Independent implementation using the same SymPy 1.14.0 backend |
| Focused regressions | **66 passed** in 4.06 seconds reported by pytest | Includes the retained 43-test scalar benchmark plus relevant engine/chart tests; not a full repository pass |
| Library integrity | Passed | Snapshot/adapter byte integrity, not a new review of historical mathematical gates |
| Data/flux | Verified | Existing two-model scalar current/data regression; does not certify this 2D theorem |
| Workflow | Passed, scoped replay complete | Existing scalar/classical controls; no training |
| Project audit | **Failed: one pre-existing issue** | `build/dissertation-print-20261031/pdf/dissertation_reviewed_20261028.pdf` is tracked; left intact |
| TeX | Native latexmk succeeded; final log has no warnings | 8 pages; no unresolved citations/references or box warnings |
| Visual inspection | All 8 rendered pages inspected | Equations, theorem, bibliography and TikZ tangent schematic readable and unclipped |
| Preservation | 1,375 tracked baseline entries unchanged; original HEAD unchanged | Concurrent dirty checkout and frozen evidence preserved |
| Source binding | All three source PDFs and copied text/alphaXiv records match their hashes | Not all sources were indexed by alphaXiv; see source audit |

The campaign began at 08:12:23 UTC. Every production computation ran serially through the copied/native Linux runner, with per-node limits at most 1,200 seconds (below the 30-minute ceiling); the reviewed replay nodes used 300-second limits. The runner enforces the 110/115-minute stop rules. All nodes finished well before those cutoffs.

Native receipts use `wait4` and `/proc` and explicitly disclose incomplete observation of short-lived thread lifetimes, waited-descendant limits, and sampled/shared RSS. `thread_accounting_complete` and `mathematical_acceptance` are false. There is no psutil substitute and no parallel production campaign.

Preserved failures include the first invariant JSON serialization error. The corrected pipeline was executed afresh; no failed receipt or partial result was relabelled as successful. The first TeX build's `\over` warning was fixed in the separate proof source; the final log is clean. The project-audit failure remains visible.

## Commands actually used

The native wrapper form was:

```bash
python -B scripts/native_proof_run.py \
  --campaign build/annular-transcritical-theorem-20261101/campaign \
  --name UNIQUE_NODE --timeout 300 -- COMMAND
```

The reviewed discovery/reconstruction replay runs its own four serial native nodes:

```bash
python -B build/annular-transcritical-theorem-20261101/replay.py \
  --out build/annular-transcritical-theorem-20261101/replay-reviewed \
  --campaign build/annular-transcritical-theorem-20261101/campaign \
  --prefix reviewed
```

The existing output path is preserved. Choose a fresh path/name for an independent repeat and respect the current campaign budget.

Commands executed inside native nodes:

```bash
python -B -X utf8 -m pytest -q -p no:cacheprovider \
  symm/tests/test_engine.py symm/tests/test_chart_reduction.py \
  research_artifacts/sve-progress-20261010/tests
python -B -X utf8 -m symm.LieSymm --check-integrity
python -B -X utf8 scripts/project.py audit \
  --out build/annular-transcritical-theorem-20261101/validation/project-audit
python -B -X utf8 scripts/project.py data-flux \
  --out build/annular-transcritical-theorem-20261101/validation/data-flux
python -B -X utf8 scripts/project.py workflow \
  --out build/annular-transcritical-theorem-20261101/validation/workflow
env PATH="/home/carl/research/projects/Lie-ML_PDES/build/dissertation-print-20261031/toolchain/.TinyTeX/bin/x86_64-linux:$PATH" \
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=build/annular-transcritical-theorem-20261101/pdf \
  build/annular-transcritical-theorem-20261101/document/local-continuation.tex
pdftoppm -scale-to 1300 -png \
  build/annular-transcritical-theorem-20261101/pdf/local-continuation.pdf \
  build/annular-transcritical-theorem-20261101/rendered/page
python -B build/annular-transcritical-theorem-20261101/support/check_package.py
```

See [package integrity](validation/package-integrity.json), [project checks](validation/project-checks.json), [native receipts in the evidence carrier](theorem-evidence.zip), and [claim ledger](CLAIMS.json). The source and result files are all included for review; the package does not claim that a reviewer must trust a test count or a stored zero.
