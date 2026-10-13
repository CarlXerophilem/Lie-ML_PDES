# Executable reproduction of the scalar SVE paper

This package audits Paliathanasis, Leon and Leach, *Mathematics* 14 (2026),
433, DOI `10.3390/math14030433`, using the supplied v3 PDF. It preserves the
printed source, independently derives the mathematics, and records corrections
with explicit witnesses. Source agreement and successful software execution
are different fields in the evidence report.

The default run computes symbolic certificates, numerical solutions, local
series, convergence experiments and static plots.
[docs/COMPUTATION.md](docs/COMPUTATION.md) distinguishes live calculations from
transcribed inputs and hand-derived arguments.
[RESULTS_EXPLAINED.md](RESULTS_EXPLAINED.md) answers the
paper-correctness, reconstruction, and variational-Lagrangian questions.
Local analytic existence and exact Taylor recurrences are explained in
[docs/SERIES.md](docs/SERIES.md). The public `compute_ode_series()` function
returns coefficients, a SymPy polynomial, chart status, and exact residual checks.
All implementation code is ordinary source in **one `main.py`**. The HTML
viewer has been removed. The prior modular release is preserved in
`archive/release-before-animation.zip`.

The revised manuscript follows the exact Boussinesq chapter's table-led
exposition, with direct SVE transformations and a reviewed retain/discard
assessment. See [presentation validation](BOUSSINESQ_STYLE_VALIDATION.md).

## Run

From the repository root, with Python, SymPy, NumPy, SciPy, Matplotlib,
PyMuPDF and pytest installed:

```powershell
python research_artifacts/SVE-reproduced-20261012/main.py
```

The default computes and prints symbolic steps, runs the numerical campaign,
exact Taylor recurrences and independent convergence sweeps, and generates
static figures. Numerical results go
to this package's `results/` directory. Run from the package directory with
`python main.py`; all paths are resolved relative to the script, not the shell.

```powershell
python main.py --stage symbolic
python main.py --stage all --reduction 3.5 --case 3 --trace summary
python main.py --stage all --rtol 1e-10 --atol 1e-12 --out build/tighter
python main.py --stage report
python main.py --stage convergence
python main.py --stage series --series-order 6
python main.py --stage plots
python -B -m pytest -q tests
```

`--case` selects the numerical exponent from `1, 1.5, 2, 3, 4`; `all` is the default.
The displayed profile-jet examples use the cubic case; the symbolic symmetry
classification and general formulas cover the declared parameter strata.
`--reduction` selects the paper subsection `3.1`--`3.9` or `table3-mixed`.
Non-ODE rows receive explicit statuses rather than fabricated IVPs. The mixed
Table 3 calculation is a symbolic companion, separate from the numbered nine.
Top-level
`DEFAULT_RTOL`, `DEFAULT_ATOL`, `G`, `KAPPA`, and
`NUMERICAL_CASE_SETTINGS` locate the main numerical settings for editing.
The source sections remain explicit and searchable. A copied `main.py` can
run without this directory; `--repo-root PATH` locates the reference PDFs.
Missing sources are recorded as unavailable, not silently verified.

## Read the output

- `COMPUTATION_VALIDATION.md`: current computation-only revision, clean-run
  checks, negative controls and known limitations. Earlier validation records
  describe their respective releases.
- `FORMAL_EXPOSITION_VALIDATION.md`: expanded manuscript derivations,
  generator tables, mathematical pseudocode, chapter attribution and review.
- `results/REPORT.md`: all ten requested headings, source inventory, formulas,
  exact checks, detailed derivations, numerical metrics and limitations.
- `results/convergence/`: fixed-step and tolerance-only endpoint experiments,
  including a non-polynomial exact control and explicit error-floor decisions.
- `results/series/`: exact Taylor coefficients and recurrence trace for all
  21 regular IVPs, nine case statuses, and comparisons with verified saved
  numerical grid nodes. `--stage series` runs this fixed campaign; call
  `compute_ode_series('3.4', exponent=3, order=6)` for one profile.
- `SERIES_VALIDATION.md`: series/manuscript revision checks; earlier
  validation records below describe their own releases.
- `results/presentation/`: manuscript profile/series comparisons and
  first-integral drift/order-reduced-solve figures, with matched-data receipts.
  `--stage plots` regenerates them; the default full run also writes them.
  `PRESENTATION_VALIDATION.md` records the subsequent explanatory/figure revision.
- `REVISION_VALIDATION.md`: checks of the single-file revision and browser,
  alongside the earlier `VALIDATION.md` release record.
- `results/evidence.json`: machine-readable counterpart, including per-claim
  statuses. `source_manifest.json` records source hashes and environment.
- `results/symbolic_steps.txt`: the printed calculation trace, including every
  derivative substitution and reduced equation.
- `results/numerical/`: numerical CSV data, profile plots, and solver receipts.
- `docs/`: detailed mathematical proofs and method explanations.
- `RUN_CONTRACT.md`, `LEDGER.json`: approved scope, task ownership and review.

The jet notation is
`p=phi_t, q=phi_s, a=phi_tt, b=phi_ts, c=phi_ss, r=phi_ttt,
w=phi_tts, x=phi_tss, y=phi_sss`. Here the jet `b` is distinct from a bed
function named `b(t,s)` in the physical-coordinate audit.

For a profile, `F,P,C,H` mean `F,F',F'',F'''`. A Lie generator gives a way to
compress two independent variables into one invariant coordinate. Requiring
the solution graph to follow that symmetry gives a profile ODE; finding a
first integral is a separate step that can lower its order.

## Scope and numerical defaults

The mathematical target is the **printed scalar equation (7)**. Its physically
advected bed counterpart is shown only in the model audit. The local symmetry
classification uses `g,kappa>0`, `m>=1`, and `phi_t,phi_s>0`. Stationary and
singular cases are retained separately; no global or arbitrary-data theorem is
claimed. The corrected classification must account for both `m=1` and `m=3`.

The numerical runs are newly constructed dimensionless IVPs, not data supplied
by either paper. They use `g=1`, `kappa=1/30`, `beta=m*kappa`, with nonlinear
initial jet `(2,.5,.1)` at reduced coordinate 1. Common scaling uses the existing
regular comparison interval `[1,1.4]`; the other nonlinear cases use `[1,1.1]`.
The linear case 3.8 uses `(0,1,.1)` at time 0 on `[0,.4]`.

The default integrator is the **classic six-stage Fehlberg 4(5)** pair, with
fifth-order accepted values, `rtol=1e-9`, `atol=1e-11`. SciPy `RK45` is a
different Dormand--Prince formula and is not used as a Fehlberg substitute.
Uddin et al., DOI `10.1016/j.aej.2016.05.009`, motivate this method but solve
a different boundary-value problem; their shooting data are not SVE data.

State agreement and integral drift target `1e-7`. Independent original-PDE
finite differences target `1e-6` at a declared stencil size and retain their
refinement/roundoff diagnostics. These are sampled numerical checks, not
continuous error bounds. The source's cubic power law lies on a degenerate
normal-form branch and is checked exactly instead of dividing by zero.

## Dissertation and validation

The reviewed section is included in `draft/main.tex`. Run the repository's
README audit, data-flux, workflow, chart/engine and historical-package checks,
then native `latexmk` and inspect the rendered manuscript. Existing frozen
evidence and unrelated working-tree changes are preserved.

The 2026-10-13 manuscripts lead with replication and corrected solutions,
then derive the SVE infinitesimal reducer and describe proposed ML-assisted
ODE order reduction. The refocus shortened the main bibliography from 52 to
19 entries; the formal exposition adds the requested Boussinesq chapter,
giving 20 entries.
The prior manuscripts and complete bibliography are preserved in
`archive/release-before-series-20261013.zip`. Hybrid design and conservation
analogies are deferred; fitting a profile is not claimed to lower ODE order.

## Audit-fixture repair, 2026-10-14

The Windows newline fixture mismatch is fixed. The same combined regression
set now passes all 174 tests, including the 80 reproduction tests. Data-flux
and workflow checks pass; the separate 218 project-audit findings remain.
See [the follow-up validation](results/audit-fixture-validation/VALIDATION.md).
Earlier validation reports preserve their original dated outcomes.
