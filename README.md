# Lie symmetry reduction for parameter-dependent PDEs

Start with [the manuscript](draft/main.tex) or [its PDF](draft/main.pdf).
The [dissertation draft](draft/dissertation.tex) develops the synopsis into
fundamentals, boundary/data restrictions, derivations, implementation and results.
The project separates exact symmetry/reduction certificates, constructed
data compatibility, numerical diagnostics, and bounded approximation results.

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

Build the self-contained manuscript with a TeX distribution containing latexmk,
pdfLaTeX, natbib and TikZ:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/latex draft/main.tex
```

The embedded bibliography needs no external `.bib` database. Read the final
LaTeX log for unresolved citations/references and inspect the resulting PDF.
On this machine, the local TeX tools are in
`$HOME/.local/share/.TinyTeX/bin/x86_64-linux`; add that directory to `PATH`.
Git LFS must be installed before checking out the canonical PDF corpus.

## Research priorities

1. **Executable manuscript workflow:** synchronize claims with replayed exact
   evidence and show all nine analysis stages. Subjective urgency 85–95%,
   usefulness 90–95%.
2. **Common-scaling data/flux example:** certify one constructed invariant
   data family and boundary flux for each scalar model. Subjective urgency
   65–80%, usefulness 80–90%.

These ranges are planning judgments, not measured probabilities. Urgency means
deferral is likely to delay manuscript progress; usefulness means completion
is likely to supply manuscript evidence. They reflect the available partial
project chats: analysis first, verified reduction before ML, classical controls,
positivity/error evidence, readable workflows, and low compute cost. Cloud and
Windows ChatGPT memories were not accessible.

## Preserved history

[Archive and evidence integrity](docs/archive.md) explains the external snapshot,
recovery gaps, and frozen-versus-expanded results. Historical experiments and
drafts are available there and in the preceding Git commit. Only the current
SVE evidence package remains in `research_artifacts/`. Existing `symm` package
paths stay stable for regression checks; older demos are secondary entrypoints.
