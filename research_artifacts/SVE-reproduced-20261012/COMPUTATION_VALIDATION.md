# Computation-only revision validation, 2026-10-13

The requested HTML removal is complete. The default `main.py` executes fresh
symbolic and numerical calculations and writes traces, JSON, CSV and static
scientific figures. The HTML template, viewer-data packaging, viewer-only map,
`--stage html`, `--html-out` and active `solutions.html` are removed. Mathematical
profile reconstruction remains available. The previous viewer and pre-edit
files are preserved in `archive/release-before-computation-only-20261013.zip`.

## What changed in the calculations

- All 25 printed Table 2 cells are now compared with computed adjoint actions;
  agreement is no longer an assigned status.
- Independent differentiation of invariant graphs and substitution into the
  original master equation checks the compact reduction formulas: 23 direct
  substitutions and two explicit undefined/no-graph outcomes cover all nine
  cases, including all 21 regular campaign IVPs. Scaling checks retain symbolic
  positive time, with multipliers `T**-2` and `T**-1`; traveling checks use the
  declared `alpha=-1`, `alpha3=0/1` examples.
- Three first-integral derivatives are compared with ODE residuals for symbolic
  `m`. Printed-equation and translated-ansatz witnesses now calculate their
  derivatives and nonzero defects. The CLI certificate gate requires these
  outcomes as well as the existing model and prolongation checks.
- `--stage report` explicitly identifies itself as saved-evidence formatting
  and rejects missing or mismatched source-code hashes. Use the default run for
  fresh computations.

The [computation map](docs/COMPUTATION.md) distinguishes these calculations from
source transcriptions, chosen graphs/generators and hand-derived orbit arguments.
There is no claim of automatic source-formula extraction or arbitrary-PDE
symmetry classification.

## Fresh-run evidence

A copy of the single script was run from `build/computation-portable/` after
checking that its output directory did not exist. It needed no local runtime
implementation package or saved result data. Primary PDFs were found through
the ancestor-path search. The copied source, canonical source, recorded code
manifest and current plot provenance have the same SHA-256 hash.

| Check | Observed result |
|---|---|
| Copied-script full run | Exit 0, 20.22 seconds |
| Canonical full run | Exit 0, 19.58 seconds |
| Symbolic checks and source-audit coverage | Passed / complete |
| Source agreement | `all_printed_claims_reproduced=false`, intentionally retained |
| RKF45 numerical IVPs | 21 passed; 10,080 primary-solve RHS evaluations |
| Exact Taylor recurrences | 21 verified; degree-six residual checks through degree three |
| Convergence campaigns | 21 completed; 16 with resolved fixed-step orders |
| Quadratic convergence cases | Five unresolved at the reference roundoff floor |
| Largest sampled original-PDE residual, DOP853 reconstruction | `7.984503500590989e-7` |
| Largest sampled original-PDE residual, RKF reconstruction | `9.361751006145558e-7` |
| Current HTML outputs | None |

Both sampled PDE maxima meet the declared `1e-6` gate. These finite diagnostics
are not continuous-domain error bounds. The 21 IVPs are constructed dimensionless
examples for the printed scalar model, not numerical data supplied by the paper.
Local analytic existence and finite Taylor calculations do not prove global
continuation or a convergence radius. The advectively corrected scalar and full
bed-field models remain distinct.

## Negative controls and independent review

The focused regression run passed 10 tests in 5.89 seconds. Tests perturb the
master equation by `+q`, corrupt an adjoint sign, and change the initial jet.
The first two changes invalidate their respective symbolic gates. For initial
jet `(3,2,2/5)`, the fresh quadratic series is `3+2*h+h**2/5`; numerical integration
at offset `.3` returns `(3.618,2.12,.4)`. Removed HTML flags and stale report hashes
are rejected.

A fresh GPT-6-Sol high reviewer independently perturbed the case 3.9 residual,
the adjoint sign and a saved source-witness flag; all affected gates failed.
The [review](docs/REVIEW_COMPUTATION.md) accepts the implementation within its
declared local printed-scalar scope, with no blocking computation defect.

## Regression and manuscript validation

The required combined suite finished with **173 passed and one failed** in
46.91 seconds. Its log contains all **80 current-package tests passing**; this
is a count within the combined run, not a separate package-only invocation.
The failure is the existing Windows fixture/hash mismatch in
`scripts/tests/test_project_audit.py::test_missing_expanded_evidence_is_not_a_false_carrier_failure`.
The fixture's audit returned `failed` instead of `passed`; no gate was weakened.

The required project commands returned:

- Audit: failed, 218 existing issues (146 tracked temporary outputs, 41 Markdown
  links, 30 canonical-reference integrity mismatches, one unavailable archive).
- Data-flux: verified, exit 0.
- Workflow: passed, exit 0.

Native MiKTeX `latexmk` built the updated manuscript successfully: 36 pages,
19 bibliography entries, no final citation/reference warnings or overfull
boxes. Underfull-box diagnostics remain. The changed runtime paragraph was
rendered and visually inspected. The final PDF is synchronized to
`draft/main.pdf`, and the inline reproduction and series blocks remain matched
to the package fragments. The dissertation files and frozen 20261010 evidence
are unchanged by this revision.

## Commands and receipts

Commands were run from the repository root with UTF-8 Python output:

```powershell
python -B research_artifacts/SVE-reproduced-20261012/build/computation-portable/main.py --trace full
python -B research_artifacts/SVE-reproduced-20261012/main.py --trace full
python -B -m pytest -vv --import-mode=importlib -o faulthandler_timeout=30 -p no:cacheprovider --basetemp=research_artifacts/SVE-reproduced-20261012/build/pytest-computation-full scripts/tests symm/tests/test_chart_reduction.py symm/tests/test_engine.py research_artifacts/sve-progress-20261010/tests research_artifacts/SVE-reproduced-20261012/tests
python scripts/project.py audit
python scripts/project.py data-flux --out build/data-flux
python scripts/project.py workflow --out build/workflow
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex
python -B research_artifacts/SVE-reproduced-20261012/main.py --stage report
git diff --check -- README.md docs/project-map.md draft/main.tex draft/dissertation.tex
```

The `latexmk` command used the native executable under
`C:/Users/Administrator/AppData/Local/Programs/MiKTeX/miktex/bin/x64/`.
[validation.json](results/computation-validation/validation.json) records exact
hashes, measured run summaries, project-check JSONs and normalized UTF-8 logs.
`RELEASE_MANIFEST.json` binds the final artifacts; earlier validation records
remain historical evidence for their own releases.
