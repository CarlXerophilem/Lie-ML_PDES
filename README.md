# Lie symmetry reduction for parameter-dependent PDEs

Start with [the manuscript](draft/main.tex) or [its PDF](draft/main.pdf).
The [dissertation draft](draft/dissertation.tex) develops the synopsis into
fundamentals, boundary/data restrictions, derivations, implementation and results.
The project separates exact symmetry/reduction certificates, constructed
data compatibility, numerical diagnostics, and bounded approximation results.

## Current cycle: 21 October 2026

The publication branch is **`astra`** on
[GitHub](https://github.com/CarlXerophilem/Lie-ML_PDES/tree/astra).
The delivered printed-P programme contains **18 registered reduction families**:
13 ODE records, one arbitrary-profile identity, two cases without an invariant
graph, one undefined PDE and one case outside the positive-velocity chart.
Fourteen symbolic pullbacks pass, including the identity case.

| Evidence | Current result |
|---|---|
| Exact solution demonstrations | 12/12 verified in original P and Q=0, on their stated domains |
| Constructed seed IVPs | 21/21 passed |
| Extended IVPs | Local precision-resolved check: 11/11 passed; frozen raw float64 campaign remains 10/11, with its original failure preserved |
| Regression suites | 72 library/scalar, 410 historical tests in their original build location, and 110 retained active/engine/chart/script tests passed; the 43 active tests are included in 110 |
| Integrity, data-flux and workflow | Passed |
| Legacy provenance audit | Missing 11 October external historical archive; retained as a nonblocking historical note, not a current research acceptance gate |

The [local precision repair](docs/residual-resolution-20261021.md) resolves the
time-resonant finite-difference noise floor without changing the 1e-6 threshold.
An independent 40-digit IVP reference has original-P residual 2.212490569e-8
at h=.003, decreasing to 2.976602120e-11 at h=.001; every integrated DOP853/RKF45
state component agrees with that reference on the output grid. Raw float64
stencil failures remain in the receipts. This is not a continuous PDE
certificate for either float interpolant. The whole repository is not labelled
all-green: broad test collection has separately recorded legacy defects.
Every registered family has a processing status; general closed forms and
singular continuation remain open where recorded. The historical archive does not
block the current research programme; the archived audit result is preserved,
not retroactively rewritten as a pass.

The current implementation is the [printed-P direct solution programme](symm/LieSymm/scalar2026/SOLUTIONS.md).
It reuses the established classification, adds exact accelerating and singular
solution families, and treats regular series, numerical continuation and
unresolved singular strata separately. E and M remain comparison models.
The [execution plan](docs/superpowers/plans/2026-10-21-sve-printed-solutions.md)
fixes the original solution scope. The [new local delivery](build/sve-P-residual-20261021/DELIVERY.md)
and [fresh demo](build/sve-P-residual-20261021/campaign-reviewed/index.html)
record the precision repair. The [frozen published solution delivery](build/sve-P-solutions-20261021/DELIVERY.md)
retains the earlier 10/11 result and its unresolved branches. The local follow-up
has not been committed or pushed as a new release.

The verified general-symm implementation is now available as the local
[LieSymm library](symm/LieSymm/README.md), preserving the existing `symm` APIs.
Its [2026 printed-scalar demo](symm/LieSymm/scalar2026/README.md) audits all nine
paper subsections, separates invalid printed formulas from corrected PDE
pullbacks, and reconstructs exact/series/numerical examples in `(s,t,phi)`.
Run `python -m symm.LieSymm.scalar2026.demo --out build/sve-demo-NEW` for a fresh
21-IVP demonstration. General closed forms for the two scaling families and
singular continuation remain open.

The [project map](docs/project-map.md) now leads with the completed 20 October
classification and the [one-dimensional exact-first programme](research_artifacts/sve-1d-programme-20261021/README.md).
Eight declared 1D branches currently supply **17 registered traveling/scaling
reductions**. Their equations, domains and pending solve status are explicit;
classification coverage is not a claim to have solved all SVE solutions.

Read the [solver plan](research_artifacts/sve-1d-programme-20261021/PLAN.md),
[bounded literature review](research_artifacts/sve-1d-programme-20261021/LITERATURE_1D.md)
and [ML decision](research_artifacts/sve-1d-programme-20261021/ML_DECISION.md).
Pure PINN training is stopped for this workload. Exact structure and classical
solvers remain primary; conditional hybrid ideas require measured added value.

Generated evidence is shipped as a [verified portable snapshot](research_artifacts/sve-current-20261021/README.md).
The [21 October delivery carriers](research_artifacts/sve-delivery-20261021/README.md)
add the library audit and complete current P-solving results, including earlier
failed campaigns, logs, raw trajectories, series, certificates and PNG/PDF/HTML.
Restore it on a fresh checkout before opening build-linked reports. The
[cleanup/restore guide](docs/build-archive-20261021.md) records older local archives,
retained dissertation inputs, and the unresolved 11 October external-archive gap.

## Project goal and research route

The research goal is a reproducible route from a parameter-dependent PDE to
its symmetry generators, invariant reductions and solutions that reconstruct
the original equation. The [research roadmap](docs/research-roadmap-20261021.md)
fixes the following order; it is a research programme, not a claim that its
later stages have already been completed.

1. **Reproduce the original SVE paper, then extend it.** Audit every declared
   source formula and build a verified demonstration for the dissertation.
   Label corrected formulas, constructed data and additional solutions as
   extensions rather than reproduced source results. The immediate target is
   one-dimensional printed P, with g,kappa>0, m>=1 and phi_s,phi_t>0; numeric
   demonstrations mainly use 1<=m<=4.
2. **Vary the original full SV+bed system and build a baseline.** Test the
   existing LieML solver on explicitly posed changes of equation, parameters,
   closure, data and geometry. Use benchmark protocols to separate mathematical,
   implementation and approximation failures, improve the method's principles,
   then freeze a reproducible baseline. The local annotated
   [Unified Benchmark of PINNs and KANs](<ref/A Unified Benchmark of Physics-Informed Neural Networks and Kolmogorov-Arnold Networks for Ordinary and Partial Differential Equations-with-annotations.pdf>)
   is a prospective protocol reference, not evidence of a completed comparison.
3. **Test the improved method on source-verified open 2D SV+bed problems.**
   Select explicit future-work problems from checked local/online papers,
   establish what remains unsolved, and compare against the frozen baseline.
   Retain errors, failures and useful structures to motivate concrete
   geometric/algebraic refinements for the dissertation's future work and
   conclusion. An untested equation is not automatically a novel or open problem.

Throughout, keep three objects separate: the fully coupled Eulerian SVE system
E, the 2026 printed scalar P, and the advectively corrected scalar M. Results
do not transfer between them without a verified transformation certificate.

The time-resonant numerical PDE diagnostic is now precision-resolved, with
its raw failure retained. Next, seek exact integrals or validated continuations
for the unresolved 3.4/3.5 and mixed/resonant equations. Every accepted result
must identify its parameter stratum, nonzero denominators, data constraints,
solution type and independent original-P certificate. A processed catalog is
not a proof that all possible reductions or all nonlinear solutions are solved.

The broader E classification and M control experiments remain independent
evidence. No new 2D/nonclassical campaign is part of the immediate residual
repair; 2D is a later gated stage of the route above. Pure PINN remains stopped.
Studying a PINN/KAN benchmark does not restart that route: ML is considered
only for a concrete unmet task with an exactly checked output or a measured
accuracy/cost benefit over classical methods. Historical archive recovery is
outside the current research acceptance gates.

## Ubuntu: clone, sync astra and restore computational results

Use Ubuntu 24.04+ (Python 3.12+) for the archive utility. The core library also
supports older Python, but the guarded restore script requires Python 3.12.
Private-repository access requires your GitHub account to have repository access;
use your normal Git credential manager or an authorized SSH remote.

```bash
sudo apt-get update
sudo apt-get install -y git git-lfs python3 python3-venv python3-pip
git lfs install
git clone --branch astra --single-branch https://github.com/CarlXerophilem/Lie-ML_PDES.git
cd Lie-ML_PDES
git lfs pull origin astra
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export PYTHONUTF8=1 PYTHONHASHSEED=0
```

For an existing clone, run the following from the repository root. The clean
working-tree check prevents the update from absorbing unrelated local edits.
Commit or deliberately stash your work before rerunning it if the check fails.

```bash
test -z "$(git status --porcelain)" || { echo 'Save local edits before syncing'; exit 1; }
git fetch origin astra
git switch astra
git pull --ff-only origin astra
git lfs pull origin astra
git rev-parse HEAD
git ls-remote origin refs/heads/astra
# The two commit hashes above must match.
```

After cloning or syncing, restore all current computational evidence. The old
carrier is immutable; the three new carriers supplement it without replacing
its files. Restoration verifies hashes and refuses to overwrite different bytes.

```bash
for archive in \
  research_artifacts/sve-current-20261021/current-build.zip \
  research_artifacts/sve-delivery-20261021/library-evidence.zip \
  research_artifacts/sve-delivery-20261021/printed-P-evidence.zip \
  research_artifacts/sve-delivery-20261021/other-current-evidence.zip
do
  python -X utf8 scripts/build_archive.py verify --archive "$archive" || exit 1
  python -X utf8 scripts/build_archive.py restore --archive "$archive" || exit 1
done
python -B -X utf8 -m symm.LieSymm --check-integrity
python -B -X utf8 -m pytest -q -p no:cacheprovider symm/LieSymm/tests symm/LieSymm/scalar2026/tests
python -B -X utf8 -m pytest -q -p no:cacheprovider scripts/tests symm/tests/test_engine.py symm/tests/test_chart_reduction.py research_artifacts/sve-progress-20261010/tests
```

Open `build/sve-P-residual-20261021/campaign-reviewed/index.html` for the local
follow-up; the frozen published demo remains under `build/sve-P-solutions-20261021`.
To generate a separate run, use a new output directory:

```bash
python -B -X utf8 -m symm.LieSymm.scalar2026.solve_demo --out "build/sve-P-local-$(date +%Y%m%d-%H%M%S)"
```

The frozen published demo retains exit code 1 for its 10/11 numerical result.
The current local source returns 0 for the 12/12 exact, 21/21 seed and 11/11
reference-checked extension run; it retains the raw float64 failure separately.
The new local evidence is not added to the older immutable carriers. Archived
Windows paths are provenance; restore preserves their bytes. This release is
validated on Windows, and Ubuntu commands are provided without claiming a full
Linux campaign. The older pre19 video/intermediate archive and missing 11 October
archive remain machine-local/unavailable as documented in the archive guide.

To publish your later Ubuntu changes, inspect and stage explicit paths, then
push without force. Add any new computational evidence carrier alongside its
hash manifest before committing.

```bash
git status --short
git add -- README.md  # Add the other intended source/evidence paths explicitly.
git diff --cached --stat
git commit -m "Describe the verified research update"
git fetch origin astra
git merge --ff-only origin/astra  # Stops on divergence; inspect before resolving.
git push origin HEAD:refs/heads/astra
git rev-parse HEAD
git ls-remote origin refs/heads/astra
```

## Dated research extension: 19 October 2026

The [run report](build/sve-autonomous-20261019/REPORT.md) records 29 symbolic
configurations, an independently evolved original-system affine benchmark,
and 17 planned plus six exploratory neural runs. None of the neural runs
passed every accuracy/residual gate; both single-profile Chebyshev reuse
controls passed. The supported results are integrated into `draft/main.tex`.
The [Lie reduction account](docs/Lie_reduction.md) connects definitions,
geometry, model contracts and the remaining approximation problem.

The reproduction package's current `main.py` is a different Eulerian analysis
from its manifest-matching scalar release. Its scalar tests have six collection
errors. Use the explicit [recovery adapter and instructions](build/sve-autonomous-20261019/recovery/README.md)
for the historical scalar source: all 80 original tests passed in that
separate replay. The frozen package and current entrypoint are preserved.
This is not a fresh full historical numerical campaign.

The [2026-10-12 SVE reproduction](research_artifacts/SVE-reproduced-20261012/README.md)
audits all nine source reductions, records verified corrections, and runs
classic Fehlberg 4(5) numerical examples, exact local series, convergence
checks and static scientific plots. Its
[computation map](research_artifacts/SVE-reproduced-20261012/docs/COMPUTATION.md)
distinguishes live calculations from transcribed source inputs.
Its reviewed section is included in `draft/main.tex`; see its
[revision validation](research_artifacts/SVE-reproduced-20261012/BOUSSINESQ_STYLE_VALIDATION.md)
for passed checks and remaining repository-wide failures.

## Read in this order

1. [Workflow and current status](docs/project-map.md).
2. [Evidence index](research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md).
3. [Theory and assumptions](research_artifacts/sve-progress-20261010/docs/THEORY.md).
4. [Reference guide](ref/README.md); [interface guide](docs/pde_formalization_and_reduction.md) for implementation.

## Reproduce

Python 3.10+ with SymPy, NumPy, SciPy, Matplotlib and pytest:

```bash
python -m pip install -r requirements.txt
python scripts/project.py audit
python scripts/project.py data-flux --out build/data-flux
python scripts/project.py workflow --out build/workflow
python -B -m pytest -q scripts/tests symm/tests/test_chart_reduction.py symm/tests/test_engine.py
python -B -m pytest -q research_artifacts/sve-progress-20261010/tests
```

Open `build/workflow/workflow.html` for the complete, evidence-linked analysis.
JSON and Markdown reports sit beside it. Reports write only to their output
directory; frozen evidence is never regenerated in place. The workflow replays
classical controls, without starting a new learning campaign.
The completed checks and exact commands are in [validation.md](docs/validation.md).

For the full retained regression suite, including older ML demos, install
`symm/research_demos/requirements.txt` and run `python -B -m pytest -q symm/tests`.
Those optional dependencies are unnecessary for the active workflow.

The implemented [week-four plan](docs/week-4_plan.md) adds an offline CPU campaign
using PyTorch 2+ alongside the packages above:

```bash
python3 run_pipeline.py
python -B -m pytest -q -p no:cacheprovider tests
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/dissertation draft/dissertation.tex
```

It writes exact certificates, 39 classical cases, 312 tolerance comparisons,
66 neural runs across three seeds, learned coefficients and a methodology report
to `build/week-4/`. All negative outcomes are retained. In the completed run,
two fixed PINNs passed both accuracy gates; no conditioned candidate passed.
The extended perturbed interval uses sampled guards, without a continuous
error certificate. The dissertation build reads its measured table and figure
from that directory; run it from the repository root. Its bibliography includes
selected manuscript entries; both manuscripts now identify the consulted
1986 Olver edition. A smaller independent campaign uses
`python3 run_pipeline.py --quick --seeds 17 --out build/week-4-quick`.

Build the manuscript with a TeX distribution containing latexmk,
pdfLaTeX, natbib and TikZ:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex
```

The embedded bibliography needs no external `.bib` database. Read the final
LaTeX log for unresolved citations/references and inspect the resulting PDF.
The two ODE comparison figures are included under the reproduction package's
`results/presentation/`. Historical scalar execution requires the dated
recovery adapter above and a separate output directory. The 19 October
Windows build uses native MiKTeX `latexmk`/pdfLaTeX available on `PATH`;
the older Linux checkout used TinyTeX.
Git LFS must be installed before checking out the canonical PDF corpus.

## Research priorities

1. **Replication and ODE solutions:** present the source audit, corrected
   reductions, local existence, Taylor series and numerical evidence first.
2. **Infinitesimal reduction:** derive point generators from the master
   equation's determining system. The implemented SVE calculation is distinct
   from the proposed reusable generic-PDE reducer.
3. **ML-assisted ODE order reduction:** propose a nontrivial first integral
   or admitted ODE generator, then verify it and its order-reduction chart.
   This is a future experiment; profile fitting alone does not lower order.

The three research interests are the Lagrange coordinate option, parameter
and distribution of symmetry-breaking, and trivial-symmetry filtration.
Equation-derived Taylor and derivative-compatible profile architectures were
tested in the dated extension above, with no demonstrated neural benefit.
Learned order-reducing objects and conservation analogies remain prospective. The dated
[revision plan](research_artifacts/SVE-reproduced-20261012/SERIES_PLAN.md)
records this instructor-directed scope.

## Preserved history

[Archive and evidence integrity](docs/archive.md) explains the external snapshot,
recovery gaps, and frozen-versus-expanded results. Historical experiments and
drafts are available there and in the preceding Git commit. Dated evidence packages remain in `research_artifacts/`; the documentation index distinguishes them. Existing `symm` package
paths stay stable for regression checks; older demos are secondary entrypoints.
