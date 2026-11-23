# 2D Saint--Venant--Exner extension, 2026-10-14

This starts the requested extension from a verified primary reference. It
contains an independently checked calculation for the coupled, frictionless
2D Eulerian equations with an isotropic Grass sediment law. The evolving
bed-slope force is retained.

Read [the calculation](report.pdf) or its [LaTeX source](report.tex), then
[the reference audit](SOURCE_AUDIT.md). The [uploaded context](inputs/uploaded-context.txt)
is preserved verbatim as a research lead, not treated as a verified citation.

## First results

- The source model is equation (1.1), p.116, of Fernández-Nieto et al.
  (2017), DOI [10.1051/m2an/2016018](https://doi.org/10.1051/m2an/2016018).
  Its porosity-normalized Grass coefficient maps to `K = kappa/(1-p)`.
- Translations, bed-datum shift, planar rotation, and common space-time
  scaling pass exact first-prolongation checks.
- The diagonal-scaling determining condition is `(3-m)c = 0`. Cubic
  transport admits an additional amplitude/spatial scaling. This is a
  restricted scaling result, not a maximal symmetry classification.
- Rotation leaves a radial PDE with swirl. At `m=3`, combining rotation
  and the extra scaling gives `h=r²H(t)`, radial velocity `rA(t)`, swirl
  `rW(t)` and bed `r²B(t)`:

  ```text
  H' = -4 A H
  A' = W² - A² - 2 g (H+B)
  W' = -2 A W
  B' = -4 K A (A²+W²)
  ```

- Direct Cartesian substitution verifies these ODEs, `W²/H` is a first
  integral for `H>0`, and an explicit evolving swirling family supplies an
  exact control. Independent numerical solvers check a constructed IVP.

The source states `1 <= m <= 4`; statements for other real exponents are
mathematical extensions on nonzero speed. The polar quotient requires
`r>0`. Wet solutions require `h>0`. For a constant bed offset, use the
correspondingly shifted scaling generator, as explained in the report.

## Reproduce

From the repository root, with SymPy, NumPy, SciPy, Matplotlib and pytest:

```powershell
python -B research_artifacts/SVE-2D-extension-20261014/main.py --out build/sve-2d-replay
python -B -m pytest -q -p no:cacheprovider research_artifacts/SVE-2D-extension-20261014/tests --basetemp=build/sve-2d-tests
```

The first command prints each exact residual, detects five deliberately
incorrect candidates/formulas, and writes JSON evidence, a CSV and a plot.
`--symbolic-only` omits numerical integration. Default output is this package's
`results/`; use a new `build/` path to preserve the delivered receipts.
The default run takes seconds on this machine and performs no ML training.

The delivered run has 68 zero scalar remainders, five detected negative
controls and 10 passing extension tests. The required project checks pass
51 engine/chart/workflow tests and the active package's 43 tests. The global
repository audit still has its existing 218 issues; see the validation
record for the Windows test-path workaround and exact audit comparison.

The report build command and repository validation outcomes are in
[VALIDATION.md](VALIDATION.md). See [results/evidence.json](results/evidence.json)
for exact certificates and numerical settings, [REVIEW.md](REVIEW.md) for
independent claim review, and [RESEARCH_LEDGER.json](RESEARCH_LEDGER.json)
for claim status and task provenance.
The fresh reviewer accepted claims C1-C7 within their declared assumptions,
including a separate check of the original conservative Cartesian equations.

## Evidence boundary and next calculation

This is a source-grounded initial calculation. It does not transfer the old
printed scalar Lagrangian classification to the full 2D system. The annular
example uses compatible solution traces; spatial scaling does not preserve
fixed annular radii. No arbitrary-data well-posedness, maximal algebra,
general 2D stability, shock, continuous numerical-error or ML claim follows.
The literature check is bounded and does not establish novelty.

Next: solve the unrestricted 2D determining equations, retaining exceptional
parameter branches; then assess perturbations of the invariant family and
the exact model's well-posedness before a full 2D solver or ML comparison.
