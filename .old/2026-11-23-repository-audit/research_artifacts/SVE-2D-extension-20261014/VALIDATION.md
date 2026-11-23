# Validation record

Run date: 2026-10-14, Asia/Tokyo. This record distinguishes the new extension
checks from pre-existing repository issues. Exact commands and logs are
retained under `build/sve-2d-extension-20261014/validation/` and copied into
this package's `results/validation/` for release.

## New extension

- `main.py` completes with **68 zero scalar remainders**, covering candidate
  prolongations, primitive/conservative equivalence, the radial quotient,
  cubic Cartesian reconstruction, graph invariance, rank, first integral,
  annular balances and the exact evolving solution. Components of vector
  identities are counted separately; this is not 68 independent theorems.
- Five negative controls return nonzero: Galilean boost, spatial rotation
  without velocity rotation, noncubic amplitude scaling, missing radial
  divergence geometry, and incorrectly using the 1D coefficient in 2D.
- **10 tests pass**, including independent planar restriction, a nonflat
  lake at rest, a stationary swirl solution and negative controls.
- A constructed dimensionless IVP passes its finite numerical gates:
  DOP853/Radau maximum sampled discrepancy `1.7392753903777702e-12`;
  step/tolerance comparison `1.2822916062305012e-9`;
  first-integral drift `2.0816681711721685e-17`; separate exact-family
  numerical error `3.3306690738754696e-16`.
- Centered-difference defects decrease by a factor `3.9548263702416566`
  when the sampling interval is halved. This is a consistency diagnostic,
  not a continuous-domain error bound or a full 2D PDE-solver test.
- Script and CSV hashes match `results/evidence.json`. The source
  manifest's **58 artifact hashes** pass a separate controller check.

Commands from the repository root:

```powershell
python -B research_artifacts/SVE-2D-extension-20261014/main.py --out research_artifacts/SVE-2D-extension-20261014/results
python -B -m pytest -q -p no:cacheprovider research_artifacts/SVE-2D-extension-20261014/tests --basetemp=build/sve-2d-extension-20261014/pytest-extension
```

For a later replay, prefer a new `build/` output directory so the delivered
receipts remain intact. Python 3.14.2, SymPy 1.14.0, NumPy 2.3.5 and SciPy
1.17.1 were used. Computations were serial with BLAS/OpenMP thread caps of
one and 600-second subprocess limits. No random seed, training or paid
provider was needed. Exact token/cache telemetry was unavailable.

## Required existing-project checks

| Command | Observed result |
| --- | --- |
| `python -B scripts/project.py audit --out build/sve-2d-extension-20261014/audit-before` | Failed: 218 existing issues at the beginning of this extension |
| `python -B scripts/project.py data-flux --out build/sve-2d-extension-20261014/data-flux` | `verified`, exit 0 |
| `python -B scripts/project.py workflow --out build/sve-2d-extension-20261014/workflow` | `passed`, exit 0 |
| `python -B -m pytest -q -p no:cacheprovider scripts/tests symm/tests/test_chart_reduction.py symm/tests/test_engine.py` | Initial run: 48 passed, 2 failed, 1 error; Windows cross-drive relative paths |
| Same test selection with `--basetemp=build/sve-2d-extension-20261014/pytest-existing` | **51 passed**, exit 0 |
| `python -B -m pytest -q -p no:cacheprovider research_artifacts/sve-progress-20261010/tests` | **43 passed**, exit 0 |

The initial workflow-test failures arise from `os.path.relpath` between
project files on `D:` and the default pytest directory on `C:`. Moving
only the test temporary directory onto `D:` resolves them. Existing project
source was not edited. The default-temp runs also emit a Windows pytest
cleanup `PermissionError` after the tests; the active-package process still
exits 0. Both original and successful rerun logs are retained.

The existing audit issues include an unavailable external archive, canonical
reference paths/integrity after local reference moves, broken historical
links and registered temporary outputs. The frozen evidence manifest and
ZIP-carrier checks pass. The release audit comparison is recorded in
`results/validation/audit-comparison.json`. The final audit has exactly the
same 218 issues, no added or removed issues, and no issue in this new package.
It must not be described as an entirely green repository audit.

## Report build and visual checks

Working directory: `research_artifacts/SVE-2D-extension-20261014`.

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir="D:/MATHs/math 4890 LieML/build/sve-2d-extension-20261014/latex" report.tex
```

Native MiKTeX/latexmk succeeds and produces **five pages**. The final TeX log
contains no undefined citations/references, LaTeX warnings, or overfull or
underfull boxes. Perl emits a Windows locale fallback warning outside the
TeX log; it does not prevent the build. All five final pages were rendered
with Poppler at 105 dpi and visually inspected: no clipping, overlap or
unreadable tables/figures was found. The rendered report's two references
match the consulted primary metadata. `results/artifact_qa.json` records
the final PDF and artifact checks.

## Development diagnostics retained

The first calculator run completed the algebra and integration but failed
to serialize a NumPy Boolean in a solver receipt. Conversion at the source
to Python `bool` fixed the issue; the subsequent complete run and saved
JSON passed. An initial hand-written expected sign for the rotation-only
negative witness was corrected from +1 to -1 after direct prolongation;
the actual nonzero witness is -1. No passing scientific result is inferred
from either failed or intermediate output.

The independent derivation note retains an intermediate general-exponent
CAS simplification limitation; the successful parent prolongation identities
and reviewer replay govern the released claims. Primary retrieval failures
and PDF extraction warnings remain in `SOURCE_AUDIT.md`.

The fresh reviewer identified a resource-provenance issue: default-setting
thread variables could retain larger incoming values while the receipt said
one thread. `main.py` now sets all three variables to one before importing
numerical libraries. A replay starting with all three set to seven confirms
the enforced values, passes the complete calculation and reproduces identical
CSV, plot and numerical-table hashes. See `results/thread_cap_repair.json`.

## Review and limitations

The fresh reviewer accepted C1-C7 within their stated scopes, replayed the
68 zero remainders and numerical data, and independently constructed 28
additional symbolic checks. No unresolved actionable finding remains. The
review and per-claim verdicts are recorded separately in
`REVIEW.md`, `REVIEW.json`, and `CLAIMS.json`. No maximal 2D point algebra,
novelty, arbitrary-data PDE well-posedness, finite sediment-supply model,
continuous numerical error certificate, or ML result is claimed. The
original uploaded context and existing scalar evidence are preserved.
