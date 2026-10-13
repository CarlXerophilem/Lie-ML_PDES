# Series and manuscript revision validation — 2026-10-13

Status: completed with qualifications. The new local analytic-series result
and manuscript refocus passed independent review in
[docs/REVIEW_SERIES.md](docs/REVIEW_SERIES.md). This is a successful audit and
corrected reproduction, not a declaration that all source-paper formulas are
correct. The canonical evidence explicitly records
`all_printed_claims_reproduced=false`.

## Mathematical result and implementation

`compute_ode_series()` is ordinary editable code in `main.py`. For a corrected
profile residual `A F''' + B = 0`, it checks the initial chart and `A != 0`,
constructs exact Taylor coefficients of the normal form, then independently
checks the coefficient residual of the undivided equation. On the strictly
positive real branch the normal form is analytic, so the analytic ODE theorem
gives a unique local analytic germ. This applies to the regular IVPs in rows
3.4, 3.5, 3.6, 3.8 and 3.9, with the recorded parameter restrictions.

The final degree-six campaign verifies **21/21** regular IVPs, including
fractional `m=3/2`. All residual coefficients through degree three vanish
exactly. The nine rows retain their separate regular, identity, undefined,
outside-chart and no-invariant-graph statuses. A singular leading coefficient
is inconclusive for existence; the exact cubic power-law branch demonstrates
why it must not be called nonexistence. The 3.8 quadratic terminates exactly.

All 21 numerical comparisons match the recorded equation fingerprint, model,
parameters, initial jet, interval and CSV hash. They use four existing nodes
without interpolation, producing 252 component comparisons. Of these, 118
fall below the operational resolution threshold and do not measure an order.
Malformed/nonfinite grids and stale/missing provenance return explicit
statuses. No convergence radius, numerical remainder bound, global solution,
arbitrary-data solution or full-bed-system theorem is claimed.

The analytic theorem source was checked in the author-hosted Teschl book;
metadata and locators are in
`results/series-validation/analytic-ode-source.json`. The book itself is not
redistributed. Detailed recurrence and examples are in [docs/SERIES.md](docs/SERIES.md).

## Executed checks

Commands below were run from the repository root, with `PYTHONUTF8=1`.

| Check | Observed result |
|---|---|
| `python -B research_artifacts/SVE-reproduced-20261012/main.py --trace full` | Exit 0; 18.64 s; symbolic audit passed, 21 numerical IVPs, 21 series and convergence campaign regenerated |
| `python -B -m pytest -q --import-mode=importlib -p no:cacheprovider --basetemp=research_artifacts/SVE-reproduced-20261012/build/pytest-series-package-final research_artifacts/SVE-reproduced-20261012/tests` | **75 passed**, 15.30 s, final code |
| Final focused `tests/test_series.py`, using the same options and `build/pytest-series-malformed` | **20 passed**, 9.39 s; includes hash-bound malformed/nan/inf CSV controls |
| Combined `scripts/tests`, chart/engine regressions, frozen-package tests and active-package tests, before the last three malformed-grid controls | **165 passed, 1 failed**, 42.05 s; pre-existing Windows CRLF fixture hash failure |
| Independent review's focused run before the last controls | **17 passed**, 9.17 s; final controls separately inspected and director receipt checked |
| `python scripts/project.py data-flux --out build/data-flux` | Exit 0, verified |
| `python scripts/project.py workflow --out build/workflow` | Exit 0, passed |
| `python scripts/project.py audit` | Exit 1; **218 existing issues**, none names this reproduction package |
| Native MiKTeX `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex` | Exit 0; 33 pages; no final warning, undefined citation/reference or overfull-box matches |
| Native MiKTeX `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/dissertation draft/dissertation.tex` | Exit 0; 47 pages; same clean final log checks |

The failed regression is
`scripts/tests/test_project_audit.py::test_missing_expanded_evidence_is_not_a_false_carrier_failure`:
the Windows fixture writes CRLF while the expected hash assumes LF. The
separate project audit records 146 tracked temporary outputs, 41 Markdown-link
issues, 30 canonical-reference integrity mismatches and one unavailable
external archive. These failures are retained; they were not suppressed to
make this revision appear globally green.

The director rendered and visually inspected main PDF pages 1–3, 27–28,
30–33, and dissertation PDF pages 2, 9–11, 28–30, 46–47. The formulas, tables,
new narrative and bibliographies are legible and unclipped. Final PDFs were
copied to `draft/main.pdf` and `draft/dissertation.pdf`. This is targeted
changed-page inspection, not a claim that every page was newly inspected.

## Manuscripts and preservation

The main bibliography is shortened from **52 to 19** entries; the dissertation
retains 12. Both final LaTeX builds resolve citations and references. Source
inventories find no missing or unused bibliography keys, as a supplemental
check rather than a substitute for the builds. The retained sources were not
all newly re-read; the new analytic-existence source was checked directly.

Both manuscripts lead with corrected replication and actual ODE solutions,
then explain the infinitesimal reducer from arbitrary `tau,xi,eta` and the
prolonged master equation. ML-assisted ODE order reduction is proposed, with
exact first-integral or ODE-symmetry acceptance gates; historical profile fits
are not presented as learned order reduction. All three requested interests
are included. Hybrid structure design and conservation analogies are deferred.

The main inline reproduction block equals `manuscript_section.tex`, and
`series_section.tex` is embedded in both manuscripts. All original ten report
headings are retained. The regenerated offline `solutions.html` keeps the
previous animation interface; its JavaScript was not changed or newly
browser-certified in this series revision. Earlier browser receipts remain
in `REVISION_VALIDATION.md`.

The pre-revision archive is `archive/release-before-series-20261013.zip`,
SHA-256 `9a5237ce7bf4a894ec8aec5a478a4aab9f2f6e9a27e74ceb50dc4bb1ba7c36bc`.
The frozen 20261010 manifest and ZIP retain their recorded hashes. Existing
unrelated reference moves/deletions were preserved. Final machine-readable
receipts are in `results/series-validation/validation.json`; the release
manifest hashes the deliverables after report generation.

Source-only `git diff --check` passes. The unrestricted command also checks
the generated dissertation PDF as text in this checkout and reports PDF
stream/xref whitespace; the PDF was validated by native compilation, opening
and rendering instead. No binary content was rewritten to silence this.
