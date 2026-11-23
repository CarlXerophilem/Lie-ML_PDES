# Cleanup and workflow validation

## Current Cleanup And Precision Validation, 21 October 2026

The [cleanup delivery](../research_artifacts/archives-20261021/CLEANUP.md)
records 72 library/scalar, 168 scripts/engine/chart/active-package and 410
historical general-symm tests passed on Windows (650 disjoint tests, including
43 active-package and 58 new archive controls). Integrity, data-flux and workflow
pass. The audit retains only the missing external 11 October history archive;
archived historical issues are not relabelled as repaired.

The [precision follow-up](residual-resolution-20261021.md) supersedes the
earlier extended-IVP outcome below: all 11 independent high-precision-reference
checks pass the unchanged 1e-6 gate. The frozen raw float64 campaign still
records 10/11 and its time-resonant 1.177074994e-6 failure. This is not a
continuous residual/error certificate for either float64 interpolant.

Native Windows builds after compaction produced 47-page dissertation and
51-page manuscript PDFs; final logs contain no undefined or multiply defined
citations/references. Existing underfull-box warnings remain. Dissertation
page 26 and manuscript page 40 were rendered and inspected. Sources and
bibliography were not rewritten. Logs, PDFs, render checks, negative receipts
and the independent review are retained in cleanup-evidence.zip in the linked
delivery. Linux synchronization/checks are recorded separately in the
[handoff](priestess-handoff.md), not inferred from these Windows checks.

## Earlier Deliveries On This Host, 21 October 2026

The latest [printed-P solution delivery](../build/sve-P-solutions-20261021/DELIVERY.md)
supersedes the library-only counts below: 66 library/scalar tests, 410 historical
general-symm tests and 110 retained active/engine/chart/script tests passed
(including the 43 active tests). Exact examples are 12/12, seed IVPs 21/21 and
extended IVPs 10/11. The time-resonant original-P sampled residual is
1.177074994e-6 against 1e-6 and remains failed. Integrity, data-flux and workflow
pass; project audit retains the missing 11 October archive. The independent
review found three Important data/chart issues, fixed with recorded regressions.
All runs and failed attempts are included in the
[publication carriers](../research_artifacts/sve-delivery-20261021/README.md).

The subsequent [LieSymm delivery](../symm/LieSymm/docs/DELIVERY.md) records
410 historical general-symm regressions, 32 new library/scalar tests, 43 active
scalar tests, and 66 existing engine/chart/script tests passed under UTF-8.
The new native Windows absolute-link regression also passes (11 focused audit
tests). All 21 constructed scalar IVPs and exact series checks passed;
data-flux and workflow passed. The first GBK-default workflow test failure is
retained in the run log. Project audit still reports the absent 11 October
external archive. Raw receipts: `build/lie-symm-library-20261021/`.

The [refresh report](../research_artifacts/project-refresh-20261021/REPORT.md)
contains current commands and raw receipts. data-flux/workflow pass; 62 engine,
chart and audit tests, 43 active-package tests and 410 general-symm tests pass.
After the final archive-guard repair, all 13 focused archive controls pass.
The project audit has **one failure**: the absent 11 October external archive.
Thirty canonical PDF hashes, active links and frozen evidence pass.
The older records below describe their dated hosts and are not this host's status.
No TeX source or bibliography was changed in this cleanup, so no new manuscript
build or visual PDF acceptance is claimed.

Validated on 2026-10-11, Python 3.12, SymPy 1.14.0, NumPy 2.5.3,
SciPy 1.18.1 and Matplotlib 3.11.2. Optional retained demo checks used
PyTorch and pykan 0.2.8 with their supporting dependencies.

| Command | Result |
|---|---|
| `python scripts/project.py audit` | PASS: 1,502 archived entries preserved; 30 unique canonical PDFs; zero broken active Markdown links; all 78 frozen entries match the ZIP |
| `python -B scripts/project.py data-flux --out build/data-flux` | VERIFIED: both scalar models, exact symbolic chart/data/current checks, five negative controls and 12 reference cases |
| `python -B scripts/project.py workflow --out build/workflow` | PASS: nine stages; constructed data gate complete with current source hashes; 12 regenerated classical controls; historical 40 comparisons and 16 exhausted budgets retained |
| `python -B -m pytest -q -p no:cacheprovider symm/tests scripts/tests research_artifacts/sve-progress-20261010/tests` | 274 passed, including all 43 current package tests |
| `python -B draft/proposal_support/verify_parameter_effects.py` | PASS |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex` | PASS: 26-page PDF; no unresolved citations/references, multiply defined labels or overfull lines in final log |
| `git diff --check` | PASS |

The native build used the local TeX installation documented in README.md.
The rebuilt PDF is copied to `draft/main.pdf`. Rendered pages, including the
new constructed-data/Jacobian/current statements and bibliography, were inspected.
Some table paragraphs retain nonfatal underfull spacing diagnostics.

The offline workflow was inspected at 1280px and 390px widths: nine linked
stages, 30 resolving evidence/navigation links, no horizontal page overflow,
and working stage navigation. The generated reference/flux plot was inspected.
Browser QA used local Playwright Chromium; it is not a project runtime dependency.

The data/flux three-jet cross-solver error is at most `3.33e-15`; first-integral
drift is at most `1.80e-14`, both below the `1e-9` threshold. These are numerical
diagnostics. Exact rational tube bounds, exact identities and sampled guards
remain explicitly separate. The obstruction witness is `3*g*kappa` in both
independent calculations for each declared scalar model.

Frozen-versus-expanded evidence differences and unavailable original history
are documented in archive.md. Cloud and Windows ChatGPT memories were not
available; recommendations use the accessible partial project history. No
maximal full-SVE classification or arbitrary-IBVP theorem is claimed.

## Week-four implementation and dissertation

Validated offline on 2026-10-11 with the versions above and PyTorch
2.14.0+cpu. The reviewed implementation extends the existing engine and keeps
both scalar model interpretations separate.

| Command | Result |
|---|---|
| `python3 -B run_pipeline.py` | PASS: exact rank/jet/scalar/coupled-generator/boundary certificates; maintained data-flux and nine-stage workflow replay; 39 classical cases, 312 tolerance comparisons, 36 independent first-integral comparisons and 66 neural runs |
| `python -B -m pytest -q -p no:cacheprovider tests symm/tests scripts/tests research_artifacts/sve-progress-20261010/tests` | 293 passed in 39.90 seconds, including all 43 current evidence tests |
| `python scripts/project.py audit` | PASS: preserved archive/frozen evidence, reference integrity and active links |
| `python scripts/project.py data-flux --out build/data-flux` | VERIFIED |
| `python scripts/project.py workflow --out build/workflow` | PASS |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/dissertation draft/dissertation.tex` | PASS: 39-page dissertation PDF; no unresolved citations/references, multiply defined labels or overfull boxes |
| `git diff --check` | PASS |

The final dissertation PDF is `build/dissertation/dissertation.pdf`. It has a
title page, abstract, roman-numbered front matter, nine chapters, appendices
and 12 selected bibliography entries. Eleven entries come from the manuscript;
the consulted 1986 Olver edition is added with its own key and locators.
The 1993 manuscript entry remains distinct. The local Olver/Oliveri fundamentals
and Hijazi boundary page were extracted and relevant rendered pages inspected.
The final dissertation's rendered pages, first-integral/lift formulas, boundary
section, measured table/figure and bibliography were inspected. One nonfatal
underfull table paragraph remains.

`build/week-4/` stores exact/numerical JSON, source hashes, configuration,
learned coefficients, cost selections and the methodology report. Its numerical
source hashes match the reviewed implementation. Earlier campaigns and their
negative outcomes are retained in `build/week-4-initial-campaign/` and
`build/week-4-reviewed-campaign/`.

Maximum tolerance-ladder state discrepancy: `1.75e-12`. Maximum independent
second/third-order state discrepancy: `2.63e-14`. Spectral admission: 138/156
degree/case combinations, with a passing control in every case. Two fixed
PINNs pass the profile/residual gates; no conditioned model passes all four
held-out cases. Both admitted fixed networks have slower full-query cost than
their cached spectral controls. No admissible neural amortization is observed.
Radau's accurate state output is distinguished from its third-derivative scalar
dense-interpolant residual, which fails this campaign's residual gate.

The perturbed interval through `z=1.5` has sampled guards, without a uniform
continuous tube/error certificate. Coupled generators are verified without
maximal classification. No online novelty review or remote Git synchronization
was performed during the authorized offline work. The post-implementation
brainstorming ranks continuous tube/error certification before a complete
corrected coupled determining-system/boundary audit.
