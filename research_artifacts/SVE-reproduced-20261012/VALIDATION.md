# Release validation: 2026-10-12

The reproduction and dissertation integration are complete with the scope
qualifications below. The repository-wide audit is **not clean**.

## Executed checks

Commands ran from the repository root with `$env:PYTHONUTF8='1'` on Windows.

| Check | Actual result |
|---|---|
| `python -B research_artifacts/SVE-reproduced-20261012/main.py --trace full` | Exit 0; symbolic certificates passed; 21/21 regular numerical IVPs passed |
| Combined regression command below | 137 passed, 1 failed; 29.52 seconds |
| New reproduction tests within combined run | 44/44 passed |
| Frozen 2026-10-10 package tests within combined run | 43/43 passed |
| `python scripts/project.py data-flux --out build/data-flux` | Exit 0; verified |
| `python scripts/project.py workflow --out build/workflow` | Exit 0; passed |
| `python scripts/project.py audit` | Exit 1; 218 issues, listed below |
| Native MiKTeX `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex` | Exit 0; 32-page PDF; no unresolved citations/references, no overfull boxes |
| Visual inspection | New section on pages 20--24 and new bibliography entry on page 32 checked after final layout changes |
| Frozen ZIP and manifest hashes | Both unchanged; expanded-file audit reports no changed frozen files |
| `git diff --check` | Passed |

The compiled `build/latex/main.pdf` was copied to `draft/main.pdf`. Twenty
underfull-box notices remain in table text across the manuscript; inspected
new-section pages have no clipped or overlapping text.

```powershell
$env:PYTHONUTF8='1'
python -B -m pytest -q --import-mode=importlib -p no:cacheprovider --basetemp=research_artifacts/SVE-reproduced-20261012/build/pytest-release scripts/tests symm/tests/test_chart_reduction.py symm/tests/test_engine.py research_artifacts/sve-progress-20261010/tests research_artifacts/SVE-reproduced-20261012/tests
```

Use a fresh `--basetemp` directory when retaining a previous run's receipts:
pytest clears that directory on reuse. Importlib mode avoids colliding
`test_numerics.py` module names across the two evidence packages. A temporary
directory on drive D avoids the existing workflow's C-to-D relative-path
failure. The initial default collection failed on duplicate module names;
the importlib run with default C-drive temp produced 134 passes, 3 failures
and 1 error. Those negative runs are retained in the receipts.

The remaining failure is the unchanged
`scripts/tests/test_project_audit.py::test_missing_expanded_evidence_is_not_a_false_carrier_failure`.
Its fixture writes `b'unique history\r\n'` through Windows text I/O but
records the SHA-256 of `b'unique history\n'`. Replacing CRLF by LF in those
fixture bytes reproduces the expected hash exactly. The audit correctly
reports the byte mismatch. This is a diagnosed test-fixture portability
issue, not a passed regression or a reason to weaken the audit.

The initial audit invocation without UTF-8 mode raised a GBK decoding error;
the explicit UTF-8 rerun completed and reported the actual issues. The
default-temp pytest run also reported an exit-time Windows cleanup
`PermissionError` for `pytest-current`; no unrelated temp files were deleted.

## Repository audit limitations

The 218 issues comprise:

- 1 unavailable machine-local external archive;
- 30 canonical-reference path/hash mismatches;
- 41 existing Markdown link failures;
- 146 temporary/build-file tracking entries.

No reported issue names the new reproduction package. These checkout/history
conditions are retained, not repaired by rewriting reference inventories or
frozen evidence. The pre-existing deleted reference PDF remains deleted.

## Mathematical and numerical release scope

All ten requested report headings, source equations (1)--(34), Tables 1--3,
and nine numbered reductions have traceable statuses. An inventory entry is
not an assertion that its source claim is true. Several displayed formulas
fail exact substitution; `all_printed_claims_reproduced` remains **false**.

The unrestricted local point-algebra proof applies to the printed scalar
equation on `phi_t>0`, `phi_s>0`, `g,kappa>0`, `m>=1`. The `m=1` boost,
bracket signs, optimal-system omissions and incorrect source reductions are
reported explicitly. No full-bed-system, shock, global, or arbitrary-IBVP
result follows. Cases that are identities, undefined, or admit no invariant
graph have explicit statuses instead of fabricated numerical solutions.

The 21 IVPs use constructed dimensionless data and the genuine six-stage
Fehlberg 4(5) pair. Original-PDE residual gates use a fixed finite-difference
stencil. The tolerance comparison also changes maximum step; it measures
joint finite-step consistency, not an isolated convergence order. Finer PDE
stencils can worsen from roundoff. Positivity and regularity are sampled,
not certified between mesh points.

The final numerical JSON matches the independently accepted smoke snapshot
exactly after excluding the 42 output-path fields (`csv` and `plot`).
The final 3.9 trace correction changes only the displayed ansatz, not the ODE.

Independent reviews are in `docs/REVIEW_SYMBOLIC.md`,
`docs/REVIEW_NUMERICS.md` (including its post-repair acceptance), and
`docs/REVIEW_RELEASE.md`. `LEDGER.json` records the claim decisions;
`RELEASE_MANIFEST.json` records delivered-file hashes and validation receipts.
The machine-readable evidence and full stepwise trace are in `results/`.
