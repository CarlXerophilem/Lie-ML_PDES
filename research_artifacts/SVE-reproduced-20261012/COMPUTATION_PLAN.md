# Computation-only revision, 2026-10-13

User scope: remove HTML from main.py and verify that the reproduction computes
its claims. Remove viewer template, data packaging and CLI generation paths;
retain mathematical reconstruction, static plots, numerical data and traces.
Archive the old generated viewer before removing it from active outputs.

Director authors code/tests/documentation. Fresh GPT-6-Sol high reviewer audits
live computation versus transcribed inputs and narrated mathematical arguments.
Add runtime checks where a success label lacks a direct comparison, and verify
all nine pullbacks independently from the original master equation. Validate
with a clean output directory and inputs/negative controls that could not be
satisfied by replaying a saved report. Do not claim automatic discovery of
every manually selected source formula, orbit representative or proof argument.

One heavy CPU job at a time, each bounded to 600 seconds; one repair/retry for
an anomalous run before recording a narrower result. No external mutation or
training, no imposed token cap. Preserve frozen evidence and unrelated edits.
Review: docs/REVIEW_COMPUTATION.md. Receipts and scope: COMPUTATION_VALIDATION.md
and results/computation-validation/. Refresh current documentation, rebuild
main.tex if its obsolete viewer paragraph changes, and hash the final release.
