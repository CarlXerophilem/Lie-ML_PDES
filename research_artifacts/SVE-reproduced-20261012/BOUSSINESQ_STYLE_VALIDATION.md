# SVE replication presentation revision, 2026-10-14

The revised Section 8 uses the arrangement and table explanations of the exact
Bruzon-Gandarias chapter, not its Boussinesq transformations. The source map is
in [the chapter-style report](docs/BOUSSINESQ_STYLE_MAP.md); its primary anchors
are printed pp. 157-159, Tables 1-3, and pp. 166-169 for the separate
conservation-law/order-reduction discussion.

## What changed

- Added an exponent-stratum classification table, followed by the explicit
  SVE generator table and an explanation of each field and its one-parameter flow.
- Explained how to read a row from generator to invariants to graph. The next
  table gives the original-master pullback and outcome for the same nine cases.
  Case 3.9 explicitly includes its zero-speed identity branch.
- Replaced the general two-exponent scaling presentation with separate,
  complete derivative and current calculations for `phi=t F(s/t)` and
  `phi=F(st^2)`. The mixed cubic family is derived from its own SVE generator.
- Distinguished derivative abbreviations, fixed coefficients selecting a
  subalgebra, the flow parameter, and fixed SVE model parameters. Removed the
  reused `a,b` optimal-system coefficients and `A,B` scaling template.
- Kept the master-equation expansion, characteristic derivation, determining
  equations, chart restrictions, first integrals, exact source witnesses,
  local series, numerical comparisons and mathematical pseudocode.
- Replaced the generic reconstruction template with a table of the actual
  SVE graph families and their velocity/depth expressions.

The earlier template was SVE-derived; the audit found no actual import of the
Boussinesq constitutive constants or transformation formulas. The revision
removes the misleading presentation and makes that provenance inspectable.

## Retain or discard

The section is retained as a paper-specific replication and correction study.
The independent [merit assessment](docs/REPLICATION_MERIT.md) found substantive
results: the source omits the `m=1` boost, exact positive-chart witnesses refute
several displayed reduced equations, corrected first integrals lower ODE order,
and the source's power profile lies on a singularity of the divided common-
scaling ODE. The source (24) witness was independently recomputed from the
master equation as `2367/5000`, rather than inferred from a solver failure.

The standard Taylor/RKF45 constructions support these results; they are not
claimed as new methods or literature-wide new solution families. Priority beyond
the audited source is unestablished. The full physical SVE model, arbitrary data,
global solutions and learned order reduction remain outside the claimed result.
Detailed derivations are retained to meet the requested step-by-step exposition.

Two GPT-6-Sol high researchers examined chapter style and replication merit.
A fresh GPT-6-Sol high reviewer checked the revised claims and independently
substituted the displayed pullbacks. The table's zero-speed omission and a
wording issue were repaired and re-reviewed. The final review is
[recorded here](docs/REVIEW_BOUSSINESQ_STYLE.md).

## Validation

- Combined required regression: **174 passed** in 43.66 seconds, including
  the current evidence package's 43 tests and the reproduction's 80 tests.
- Project data-flux: **verified**. Project workflow: **passed**.
- Project audit: **218 existing issues remain** (146 tracked temporary outputs,
  41 Markdown links, 30 reference-integrity mismatches, one unavailable archive).
- Independent SymPy checks verify all 18 displayed scaling derivatives and the
  common-scaling/cubic current identities exactly. The initial simplify-only
  probe did not reduce one equivalent expression to literal zero; exact
  factorization did, without any mathematical formula change.
- Native MiKTeX latexmk: **46 pages**, no final citation/reference warnings,
  undefined references, or overfull boxes. Underfull diagnostics remain.
  The SVE pages, final tables, formulas, figures and bibliography were rendered
  and inspected. The source, PDF and two manuscript fragments are synchronized.
- The executable `main.py`, numerical evidence, dissertation files and frozen
  20261010 evidence remain byte-identical to the preceding release. Only the
  marked SVE block changes in `draft/main.tex`.

Exact commands, logs, hashes and review records are in
[the validation receipt](results/style-revision-validation/validation.json).
The pre-revision manuscript, PDF, fragments and release manifest are preserved
in `archive/release-before-boussinesq-style-20261014.zip`.
