# Lie symmetry reduction for parameter-dependent PDEs

Start with [the manuscript](draft/main.tex) or [its PDF](draft/main.pdf).
The [dissertation draft](draft/dissertation.tex) develops the synopsis into
fundamentals, boundary/data restrictions, derivations, implementation and results.
The project separates exact symmetry/reduction certificates, constructed
data compatibility, numerical diagnostics, and bounded approximation results.

The [2026-10-12 SVE reproduction](research_artifacts/SVE-reproduced-20261012/README.md)
audits all nine source reductions, records verified corrections, and runs
classic Fehlberg 4(5) numerical examples, exact local series, convergence
checks and static scientific plots. Its
[computation map](research_artifacts/SVE-reproduced-20261012/docs/COMPUTATION.md)
distinguishes live calculations from transcribed source inputs.
Its reviewed section is included in `draft/main.tex`; see its
[revision validation](research_artifacts/SVE-reproduced-20261012/FORMAL_EXPOSITION_VALIDATION.md)
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
selected manuscript entries and distinguishes the consulted 1986 Olver edition
from the manuscript's 1993 entry. A smaller independent campaign uses
`python3 run_pipeline.py --quick --seeds 17 --out build/week-4-quick`.

Build the manuscript with a TeX distribution containing latexmk,
pdfLaTeX, natbib and TikZ:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex
```

The embedded bibliography needs no external `.bib` database. Read the final
LaTeX log for unresolved citations/references and inspect the resulting PDF.
The two ODE comparison figures are included under the reproduction package's
`results/presentation/`; regenerate them with its `main.py --stage plots`
after generating the matching numerical data, or run its default full demo.
On this machine, the local TeX tools are in
`$HOME/.local/share/.TinyTeX/bin/x86_64-linux`; add that directory to `PATH`.
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
Hybrid structure design and conservation analogies are deferred. The dated
[revision plan](research_artifacts/SVE-reproduced-20261012/SERIES_PLAN.md)
records this instructor-directed scope.

## Preserved history

[Archive and evidence integrity](docs/archive.md) explains the external snapshot,
recovery gaps, and frozen-versus-expanded results. Historical experiments and
drafts are available there and in the preceding Git commit. Only the current
SVE evidence package remains in `research_artifacts/`. Existing `symm` package
paths stay stable for regression checks; older demos are secondary entrypoints.
