# Dissertation integration notes: 2026-10-12 SVE reproduction

The standalone `research_artifacts/SVE-reproduced-20261012/manuscript_section.tex`
is integrated inline immediately before `\section{Related work and research position}`
in `draft/main.tex`. It uses the existing `amsmath`, `booktabs`, `tabularx`,
`natbib`, and `hyperref` setup and prefixes new labels `sve-repro-`. It cites
the existing `ap` item and the added `uddin2016rkf` item (DOI `10.1016/j.aej.2016.05.009`; local reference PDF
has 2016 in-press metadata, so do not invent volume or page numbers).

The section is additive to the earlier example and keeps the printed scalar
model distinct from the advectively corrected physical pullback. Its numeric
claim uses the accepted post-repair 21-run snapshot in
`research_artifacts/SVE-reproduced-20261012/build/numerics-smoke/numerics.json`
and the qualifications in `docs/REVIEW_NUMERICS.md`. The symbolic scope
follows `docs/REVIEW_SYMBOLIC.md`: complete local smooth point algebra only
on the declared positive regular chart, not a full-bed-system or singular
branch classification. Source equations (24)--(34) are individually
qualified/refuted via explicit witnesses; the cubic power solution remains
valid on its singular normal-form stratum.

The director completed native `latexmk`, final citation/reference diagnostics,
rendered-page inspection, and the project and package validation commands.
See `../VALIDATION.md` for the results and retained failures. The standalone
section and the inline manuscript block match exactly. The source PDF, frozen 2026-10-10 package,
manifest, and existing unrelated deletion must remain untouched.
