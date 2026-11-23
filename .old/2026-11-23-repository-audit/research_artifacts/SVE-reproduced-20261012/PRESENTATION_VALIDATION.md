# Traveling reductions, series and numerical figures — 2026-10-13

The three requested purposes are now explicit in `draft/main.tex`.

| Purpose | Before this revision | Final presentation |
|---|---|---|
| Completeness for source (28)--(31),(33) | The original-PDE counterexamples and corrected traveling integral were present, but their equation-by-equation correspondence was implicit. | The new paragraph **What replaces source (28)--(31) and (33)** maps the third-order F equation, second-order P equation, first-order M equation, integrated M formula and vertically shifted traveling family. It retains positive-chart, nonzero-B and nonzero-I0 restrictions and the separate affine branch. |
| Clear PDE-to-ODE compression | The invariant graph was stated without a worked explanation. | **How the traveling symmetry compresses the PDE** gives the finite transformation, its two invariants, the ansatz, graph condition, pulled-back derivatives and reduction of two independent variables to one. It distinguishes that step from lowering differential order. |
| Verification and order reduction | First-integral formulas and aggregate drift metrics were present. | The manuscript displays the two-state IVP with its initial integral constant, explains independent evaluation along the three-state solver, and plots drift plus disagreement with a separately integrated second-order system. |

The existing **[Numeric solutions to the ODEs]** subsection is reorganized as
one account: common IVP data, local analytic existence and Taylor recurrence,
series/numerical comparison, numerical method, first-integral checks,
reconstruction and convergence diagnostics. The original required heading is
retained. The source paper's disputed formulas remain disputed; correction
does not mean agreement with them.

## Figures and reproducibility

- Figure 3 (PDF page 28): `results/presentation/series-numerical.pdf` overlays
  cubic common-scaling and traveling RKF45/DOP853/Taylor profiles, then shows
  separate F, F', F'' differences at four saved nodes. Hollow markers denote
  unresolved differences under the existing operational screen; zero values
  are omitted on logarithmic axes.
- Figure 4 (PDF page 30): `results/presentation/first-integral-checks.pdf`
  displays signed integral drift and two-state/three-state differences for
  cubic cases 3.4, 3.6 and 3.9. The constants are respectively 79/200,
  -71/200 and -79/200. The largest plotted scaled drift is 3.72e-15; the
  largest scaled two-state disagreement is 1.53e-15 (rounded upward).

The lower-order solves use DOP853 with rtol=1e-12, atol=1e-14 and max_step=.01.
They solve a different differential formulation from the three-state RKF45
trajectory. Matching this finite solution does not bound its continuous error.
No variational Lagrangian, learned integral, new global solution theorem or
computed series convergence radius is assumed or asserted.

All plot implementation remains in `main.py`, function
`write_manuscript_plots()`. From the repository root:

```powershell
python -B research_artifacts/SVE-reproduced-20261012/main.py --stage plots
```

The default full demo also generates the figures. The plot function requires
matching numerical receipts, IVP data, equation fingerprints and CSV hashes.
It writes PNG/PDF figures, three diagnostic CSVs, and `plots.json` with source,
input and output hashes. The TeX source now documents its two external figure
assets; its bibliography remains embedded with 19 cited entries.

## Executed validation

- Full `main.py --trace full`: exit 0, 18.96 seconds; symbolic audit, all
  21 numerical IVPs, all 21 degree-six series and all convergence cases pass;
  the two figure sets are generated and their hashes verified.
- Final active-package pytest: **76 passed in 16.60 seconds**, including
  the new figure integration test. It independently evaluates the three
  cubic integrals using NumPy formulas and confirms refusal of a modified CSV.
- Focused plot integration: **1 passed in 3.47 seconds**.
- Broader script, engine/chart, frozen-package and active-package suite
  before the new integration test: **168 passed, 1 failed in 38.76 seconds**.
  The failure is the existing Windows CRLF fixture/hash mismatch in
  `scripts/tests/test_project_audit.py`.
- One initial quiet active-package rerun stalled after 41 tests and was
  stopped after roughly three minutes of CPU use. Its incomplete log is
  retained. A focused diagnostic run and one full verbose retry with
  faulthandler enabled passed. The stall's cause is unresolved; it is not
  counted as a successful run.
- Required `scripts/project.py data-flux --out build/data-flux`: verified,
  exit 0; `workflow --out build/workflow`: passed, exit 0.
- Required `scripts/project.py audit`: exit 1, the same **218 existing
  issues** (146 tracked temporary outputs, 41 Markdown links, 30 reference
  integrity mismatches, one unavailable external archive). None names the
  active reproduction package. These are not hidden by the focused passes.
- Native MiKTeX `latexmk -pdf -interaction=nonstopmode -halt-on-error
  -outdir=build/latex draft/main.tex`: exit 0, **36 pages**, no final
  warnings, overfull boxes or undefined citation/reference matches.
  Nonfatal underfull-box spacing diagnostics remain in the log; the rendered
  changed pages have no clipping or overlapping labels.
  Rendered PDF pages 25--31 and 34--36 and both standalone figures were
  visually inspected. Final PDF is copied to `draft/main.pdf`.

Independent mathematical, provenance and figure review is recorded in
`docs/REVIEW_ODE_PRESENTATION.md`. The main reproduction fragment is
synchronized with `manuscript_section.tex`; the unchanged `series_section.tex`
is still embedded. `draft/dissertation.tex` and its PDF retain their previous
revision. Frozen 20261010 hashes, prior archives and unrelated reference edits
are preserved. A focused pre-edit snapshot is
`archive/release-before-presentation-20261013.zip`.

Machine-readable receipts and normalized command logs are in
`results/presentation-validation/`; `RELEASE_MANIFEST.json` identifies this
revision and hashes the final files. Earlier validation documents remain
records of their own releases.
