# Active project instructions

Read README.md, draft/main.tex, docs/project-map.md and the current experiment
index before making research claims. The current evidence entries are indexed in docs/project-map.md. The retained
scalar benchmark is research_artifacts/sve-progress-20261010; the portable
19/20 October classification snapshot is research_artifacts/sve-current-20261021;
the current printed-P solution delivery is build/sve-P-solutions-20261021,
published in research_artifacts/sve-delivery-20261021. The E-focused 1D programme
is research_artifacts/sve-1d-programme-20261021 and remains a separate model.
Historical instructions in the
external archive apply to their snapshot, not this working tree.

## Mathematical and evidence boundaries

- Keep printed and advectively corrected scalar SVE models separate.
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

## Validation

Run the project audit, data-flux checker and workflow runner from README.md.
Run relevant engine/chart regression tests and the current package's 43 tests.
For manuscript or bibliography edits, build with native latexmk, inspect final
citation/reference warnings and rendered pages. Regex inventories are navigation
aids, not authoritative citation validation. Report commands and limitations.

Before broad changes inspect Git status, preserve concurrent edits and inspect
path dependencies. The external archive is machine-local; do not assume its
presence in another checkout. Avoid automatically reading or expanding it.
