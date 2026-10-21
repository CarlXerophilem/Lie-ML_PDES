# Active project instructions

Read README.md, draft/main.tex, docs/project-map.md and the current experiment
index before making research claims. The current map distinguishes the new
precision follow-up (build/sve-P-residual-20261021, source baseline 11fe2a8)
from the frozen printed-P delivery (build/sve-P-solutions-20261021).
The new precision carrier is research_artifacts/sve-P-residual-20261021;
the four immutable earlier carriers remain in sve-current-20261021 and
sve-delivery-20261021. The retained 43-test scalar benchmark is
research_artifacts/sve-progress-20261010. The E-focused 1D programme is
research_artifacts/sve-1d-programme-20261021 and remains a separate model.
Historical archive instructions apply to their snapshot, not this working tree.

## Mathematical and evidence boundaries

- Keep printed scalar P, full Eulerian SV+bed E and corrected scalar M separate.
- Record positive-branch/chart assumptions, denominators, parameter strata,
  and whether a result is exact, numerical, restricted, or unresolved.
- A verified generator or finite search does not prove maximal classification.
  An unavailable backend or exhausted budget is not an obstruction proof.
- Reduction of independent-variable dimension and reduction of ODE order by
  a first integral are separate results. Data and current compatibility are
  additional checks. No arbitrary-IBVP, full-bed-system or learned-error theorem
  follows from the constructed scalar example.
- Preserve frozen ZIP/manifest files and negative experiment records. Write
  new outputs to build/ or a separate user-selected directory.
- Current checks are 12/12 exact, 21/21 seed and 11/11 high-precision-reference
  extended IVPs; the frozen raw float64 campaign remains 10/11. Neither a finite
  residual nor agreement at output nodes certifies a continuous PDE error bound.
- Pure PINN is stopped. The missing 11 October external archive is nonblocking
  historical provenance; do not rewrite its failed audit or make recovery a gate.

## Navigation and next task

The next task is ONLY a title, outline and source-question-evidence map for
the existing draft/dissertation.tex, following
docs/superpowers/plans/2026-10-21-dissertation-writing.md. Do not write manuscript
prose, start training, launch agents remotely or copy authentication/config.

`.ignore` reduces default ripgrep file discovery; it does not prevent direct
reads or control every agent/tool. References, evidence and frozen JSON remain
available through explicit scoped searches. Python implementation under
symm/LieSymm/_snapshot stays visible; its run output and JSON do not. Examples:

```bash
rg --no-ignore --files ref
rg --no-ignore -n --glob '*.md' 'current|failed|unresolved' research_artifacts/sve-progress-20261010
rg --no-ignore -n 'source_sha256' symm/LieSymm/_snapshot/cases
rg --no-ignore --files research_artifacts/archives-20261021
```

Eight historical packages retain ARCHIVED.md stubs pointing to verified ZIPs;
restore only when needed. Do not automatically expand them or the machine-local
external archive. Follow docs/priestess-handoff.md for portable remote work.

## Validation

Run the project audit, data-flux checker and workflow runner from README.md.
Run relevant engine/chart regression tests and the current package's 43 tests.
For manuscript or bibliography edits, build with native latexmk, inspect final
citation/reference warnings and rendered pages. Regex inventories are navigation
aids, not authoritative citation validation. Report commands and limitations.

Before broad changes inspect Git status, preserve concurrent edits and inspect
path dependencies. The external archive is machine-local; do not assume its
presence in another checkout. Avoid automatically reading or expanding it.
