# Single-script, convergence, and animation validation

The requested revision is complete with the mathematical and numerical scope
qualifications below. The repository-wide checks are not all green.
The earlier release remains in `archive/release-before-animation.zip`;
`VALIDATION.md` and `LEDGER.json` describe that historical release.

## Executed checks

| Check | Measured result |
|---|---|
| Final `main.py --trace full` | Exit 0; symbolic certificates passed; 21/21 regular numerical IVPs passed |
| Separate convergence study | 21/21 cases completed; 147 fixed-step errors, 55 resolved and 92 floor-limited; 39 resolved adjacent orders |
| Combined regression suite | **148 passed, 1 existing failure**, 30.68 seconds |
| Active reproduction tests | **55/55 passed**, included in the combined run |
| Frozen 2026-10-10 tests | **43/43 passed**, included in the combined run |
| Single-script portability | Only `main.py` copied to a separate C-drive directory; exit 0, 21 numerical cases and 21 convergence cases, HTML generated |
| Project data-flux checker | Exit 0, verified |
| Project workflow runner | Exit 0, passed |
| Project audit | Exit 1, 218 existing issues; none names this package |
| Native MiKTeX manuscript build | Exit 0; 33 pages; zero unresolved citations/references and zero overfull boxes |
| PDF visual inspection | Final pages 22, 24, 25 and 31 inspected, including reconstruction, convergence, variational discussion and Noether bibliography entry |
| Browser interaction | All ten equation selections, exponent restrictions, phi/u/h controls, play, pause and reset passed |
| Offline browser | Reloaded the final file with network emulation Offline; zero external resource requests, zero console errors/warnings |
| Responsive layout | Mobile 390 by 844 and desktop 1440 by 1000; no horizontal overflow; final mobile and desktop endpoint tick alignment visually inspected |
| Integrity | Frozen ZIP and manifest hashes unchanged; prior-release archive hash unchanged; inline manuscript section matches its package source |
| Implementation layout | All runtime implementation and HTML template in `main.py`; no local implementation import, source `exec` or `eval` |

The copied-script portability run preceded final axis-label alignment and
default-settings centralization. The final canonical script then passed the
complete demo and regression run. Missing PDFs in the copied-script run were
explicitly marked unavailable, and `complete_audit` was false. A working
calculation without its sources is not a complete source audit.

The final desktop DevTools screenshot timed out. A separate headless Chrome
capture succeeded and was visually inspected; its image is retained as
`results/revision-validation/desktop.png`. Both final desktop and mobile
captures show the corrected endpoint tick alignment. The DevTools timeout is
retained as a capture-tool limitation, not a page failure.

Twenty underfull-box notices remain in manuscript tables. The compiled
`build/latex/main.pdf` was copied to `draft/main.pdf`; their hashes match.

## Commands and durable receipts

Run from the repository root with `$env:PYTHONUTF8='1'`:

```powershell
python -B research_artifacts/SVE-reproduced-20261012/main.py --trace full
python -B -m pytest -q --import-mode=importlib -p no:cacheprovider --basetemp=research_artifacts/SVE-reproduced-20261012/build/pytest-final-revision scripts/tests symm/tests/test_chart_reduction.py symm/tests/test_engine.py research_artifacts/sve-progress-20261010/tests research_artifacts/SVE-reproduced-20261012/tests
python scripts/project.py audit
python scripts/project.py data-flux --out build/data-flux
python scripts/project.py workflow --out build/workflow
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex
```

The actual build used the native MiKTeX `latexmk.exe` under the user's
`AppData/Local/Programs/MiKTeX/miktex/bin/x64` directory. Use a fresh
`--basetemp` when preserving earlier pytest receipts, because pytest clears it.

Machine-readable validation, test output, demo trace, build log, browser
observations, portability receipt and project-audit JSON are retained in
`results/revision-validation/`. `REVISION_LEDGER.json` records this revision's
claims and review, and `RELEASE_MANIFEST.json` hashes the delivered files.

## Retained failures and scope

The one regression failure is the unchanged
`scripts/tests/test_project_audit.py::test_missing_expanded_evidence_is_not_a_false_carrier_failure`.
Its Windows fixture writes CRLF bytes while expecting the hash of LF bytes.
The exact prior diagnosis is retained in `VALIDATION.md`; the audit has not
been weakened to hide this mismatch.

The 218 repository-audit issues comprise 1 missing external archive,
30 canonical-reference integrity mismatches, 41 Markdown-link issues and
146 tracked temporary/build-file entries. Reference moves/deletions and other
unrelated working-tree changes were preserved. All 78 frozen manifest entries
that the audit checks passed, as did the frozen-carrier integrity check.

Fixed-step fifth-order behavior is measured on scaling cases and the exact
non-polynomial control. Traveling rows have only one resolved pair apiece;
their adaptive sweep retains the same two steps and does not demonstrate
tolerance convergence. The quadratic control gives no nontrivial measurable
order. Reference agreement, sampled chart guards, interpolation and finite
endpoint/PDE residual tests are diagnostics, not continuous error certificates.

The HTML uses corrected reductions of the **printed scalar model**, constructed
dimensionless IVPs, and masked local reconstructions. It does not establish
the advectively corrected full bed system, arbitrary data compatibility,
shock behavior or global regularity. Source (24)--(33) includes related
derivative and first-integral representations, not ten independent IVPs.

`docs/REVIEW_REVISION.md` independently accepts the convergence and
reconstruction mathematics within these limits. The director's post-merge
tests and browser checks cover final single-script and HTML integration.
