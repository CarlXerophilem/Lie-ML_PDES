# Verified Lie symmetry reduction for SVE-type models

The **27 October strict follow-up** is indexed in
[the current delivery](research_artifacts/sve-final-20261027/README.md).
Its latest dissertation is [the five-chapter source](<draft/dissertation_2026 (1).tex>)
and [compiled PDF](<draft/dissertation_2026 (1).pdf>), with a total limit of 25 pages.
Read [the failure and acceptance analysis](research_artifacts/sve-final-20261027/FAILURES.md)
before interpreting a passing software test as a mathematical classification.
Strict acceptance remains incomplete; the publication branch is `codex/final`.
This task supersedes the earlier outline-only writing scope below.

Start with the [project map](docs/project-map.md), [manuscript](draft/main.tex)
and [dissertation](draft/dissertation.tex). The 26 October writing cycle now
completes the dissertation, superseding the earlier outline-only task.
Its [run record](build/dissertation-completion-20261026/RUN.md) separates the
scalar source audit, a fresh annular 2D full-E benchmark and prospective ML.

## Dissertation And Fresh 2D Verification: 26 October 2026

The subsequent [strict CAS run](build/sve-strict-lie-20261026/RUN.md) is
**incomplete**. Its [equation-first entry](symm/LieSymm/strict.py) invokes the
official REDUCE LIEPDE/CRACK packages and independently checks returned
families, without registry basis or profile backfilling. Partial translation
reductions are distinguished from exhaustive determining-system closure,
source-subsection reproduction and data-compatible reconstruction. The
[serial runner](scripts/run_strict_lie.py) preserves raw failures and guarded
60/300/1800-second tiers. No universal-reduction claim follows from this run.

The [annular module](symm/LieSymm/annular2d.py) produces six supplied symmetry
profiles, prolonged tangency, an admitted algebra and rank-two reduction to
ODEs for isotropic cubic transport with downslope diffusion and Coriolis
forcing. Three independent integrals further reduce the regular five-state
ODE. This is a constructed smooth full-E reference, not a maximal 2D
classification, physical calibration or an executed 2D ML comparison.
The [delivery and review](build/dissertation-completion-20261026/README.md) retain
exact certificates, sampled reconstruction, source verification and negatives.

```bash
python -B -X utf8 scripts/verify_dissertation_interfaces.py --out build/interfaces-NEW.json
python -B -X utf8 -m symm.LieSymm.annular2d --out build/annular-NEW
python -B -X utf8 -m pytest -q -p no:cacheprovider scripts/tests/test_dissertation_interfaces.py symm/LieSymm/tests/test_annular2d.py
```

The scalar and 2D targets remain separate. No training, SSH work or remote
publication is part of this writing cycle. The older writing plan is historical.

## Current Evidence: 21 October 2026

The publication branch is [GitHub `astra`](https://github.com/CarlXerophilem/Lie-ML_PDES/tree/astra).
The precision follow-up's source baseline is `11fe2a8`; frozen earlier receipts
are not rewritten. Exact certificates, numerical diagnostics and future work
are separate evidence classes.

| Result | Scope |
|---|---|
| Printed P: 12/12 exact demonstrations | Original P and invariant condition Q=0, on stated domains |
| Printed P: 21/21 seed IVPs | Constructed local data, not arbitrary-IBVP existence |
| Extended IVPs: 11/11 high-precision-reference checks | Frozen raw float64 campaign remains 10/11; unchanged 1e-6 gate |
| P catalogue: 18 registered families | Exact, series, numerical, undefined/no-graph/out-of-chart statuses are explicit |
| Historical 11 October archive | Missing external provenance is nonblocking; its failed receipt remains |

Read the [precision explanation](docs/residual-resolution-20261021.md),
[current delivery](build/sve-P-residual-20261021/DELIVERY.md),
[interactive result](build/sve-P-residual-20261021/campaign-reviewed/index.html)
and [solution API](symm/LieSymm/scalar2026/SOLUTIONS.md). The independent
40-digit reference resolves a third-derivative noise floor; it does not certify
either float64 interpolant continuously. Closed forms and singular continuation
remain open where recorded. Selected passing suites do not make bare pytest green.

## Research Route And Model Boundaries

1. Reproduce the 2026 printed scalar paper faithfully, then label independently
   verified corrections and extensions as such.
2. Pose controlled changes of the full SV+bed system, test the existing LieML
   method against named controls, and freeze a reproducible baseline.
3. Select source-verified open 2D SV+bed questions, then test the frozen baseline.

**P** is the 2026 printed scalar equation; **E** is the full Eulerian SV+bed
system; **M** is the advectively corrected scalar equation. No result transfers
between them without a verified transformation/reconstruction certificate.
Charts, nonzero denominators, parameter strata and compatible data are part of
each result. Registered families are not all solutions, and finite searches
are not maximal/global classification proofs. Variable reduction and ODE-order
reduction are distinct. Pure PINN is stopped; hybrid ML needs a concrete unmet
task and exact verification or measured matched-accuracy/cost benefit.
See the [three-stage roadmap](docs/research-roadmap-20261021.md) and
[separate E-focused 1D programme](research_artifacts/sve-1d-programme-20261021/README.md).

## Reproduce And Validate

Python 3.12+ is required for portable archive utilities. Install dependencies,
restore the evidence below, and run from the repository root into new outputs:

```bash
python -m pip install -r requirements.txt
python -B -X utf8 -m symm.LieSymm --check-integrity
python -B -X utf8 -m pytest -q -p no:cacheprovider symm/LieSymm/tests symm/LieSymm/scalar2026/tests
python -B -X utf8 -m pytest -q -p no:cacheprovider scripts/tests symm/tests/test_engine.py symm/tests/test_chart_reduction.py research_artifacts/sve-progress-20261010/tests
python -X utf8 scripts/project.py audit
python -X utf8 scripts/project.py data-flux --out build/data-flux-NEW
python -X utf8 scripts/project.py workflow --out build/workflow-NEW
python -B -X utf8 -m symm.LieSymm.scalar2026.solve_demo --out build/sve-P-NEW
```

The retained scalar package has 43 tests. Detailed receipts and legacy test
limitations are indexed in [validation](docs/validation.md). The workflow
replays classical controls, not a training campaign. Preserve frozen evidence.

On Windows use native MiKTeX `latexmk` from the repository root, then inspect
the final citation/reference warnings and rendered PDFs:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/dissertation draft/dissertation.tex
```

The completed dissertation uses the retained scalar precision surface and the
fresh annular profile in `build/dissertation-completion-20261026`. Older
`build/week-4` inputs remain for historical dependants. Compilation remains on
Windows for the current Priestess handoff, which has neither TeX nor sudo.

## Ubuntu Sync And Evidence Restore

Use an authorized GitHub SSH/credential-manager configuration and Git LFS;
do not copy authentication or agent configuration. For a fresh checkout:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --branch astra --single-branch git@github.com:CarlXerophilem/Lie-ML_PDES.git
cd Lie-ML_PDES
git lfs install
git lfs pull --include='ref/**,research_artifacts/sve-P-residual-20261021/**' --exclude='' origin
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export PYTHONUTF8=1 PYTHONHASHSEED=0
```

For an existing checkout, use the clean-tree, fast-forward-only sync and remote
hash check and later push commands in the [Priestess handoff](docs/priestess-handoff.md). Restore the four
immutable earlier carriers, then the new 401-file precision carrier:

```bash
for archive in research_artifacts/sve-current-20261021/current-build.zip research_artifacts/sve-delivery-20261021/library-evidence.zip research_artifacts/sve-delivery-20261021/printed-P-evidence.zip research_artifacts/sve-delivery-20261021/other-current-evidence.zip; do
  python -X utf8 scripts/build_archive.py verify --archive "$archive" || exit 1
  python -X utf8 scripts/build_archive.py restore --archive "$archive" || exit 1
done
python -X utf8 scripts/evidence_archive.py verify --archive research_artifacts/sve-P-residual-20261021/precision-evidence.zip
python -X utf8 scripts/evidence_archive.py restore --archive research_artifacts/sve-P-residual-20261021/precision-evidence.zip --root .
```

Restore verifies hashes and refuses different-byte overwrites. Archived Windows
paths are provenance, not Linux execution paths. No full Linux campaign is
implied by carrier restoration or environment inspection.

## Navigation And Preserved History

- [Documentation index](docs/README.md) and [current evidence map](docs/project-map.md).
- [Scalar experiment index](research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md), [source reproduction](research_artifacts/SVE-reproduced-20261012/README.md), [reference guide](ref/README.md).
- [Current snapshot](research_artifacts/sve-current-20261021/README.md), [frozen delivery](research_artifacts/sve-delivery-20261021/README.md), [archive policy](docs/archive.md), [build restore guide](docs/build-archive-20261021.md).

`.ignore` limits default ripgrep discovery, not direct reads or every agent/tool.
Use scoped `rg --no-ignore` commands in [AGENTS.md](AGENTS.md) to inspect excluded
evidence and references. Historical package stubs link to verified archives in
`research_artifacts/archives-20261021`; `root-history.zip` preserves moved root history.
