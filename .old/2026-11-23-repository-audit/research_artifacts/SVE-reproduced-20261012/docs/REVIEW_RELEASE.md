# Independent manuscript-section release review (2026-10-12)

## Verdict

**Qualified acceptance of `manuscript_section.tex` as a local, printed-scalar
SVE reproduction section.** No load-bearing mathematical or numerical
discrepancy was found against the reviewed package and current generated
evidence. This is not approval of the full dissertation build, rendered pages,
or every unnumbered assertion in the source paper. The package inventory says
`all_printed_claims_reproduced=false`; that negative must remain visible.

## Checks and findings

- All ten headings required by `RUN_CONTRACT.md` occur exactly once. The Table 3
  rows 3.1--3.9 each have an explicit outcome: 3.1 is an identity outside the
  `p>0` chart, 3.2 is undefined at `q=0`, 3.3 has no invariant graph, 3.4--3.6
  and 3.9 have local regular ODEs subject to leading-coefficient/parameter
  guards, 3.7 is an identity, and 3.8 is `E=alpha*F'''`. The separate mixed
  cubic chart is not falsely counted as a tenth numbered case.
- The master equation, local unrestricted point-algebra dimensions `4,5,5`
  for `m!=1,3`, `m=3`, `m=1`, extra `m=1` boost, bracket corrections,
  connected-inner-adjoint equivalence, scaling pullback, exact 3.4 first
  integral, traveling first integral, and singular cubic profile match
  `docs/REVIEW_SYMBOLIC.md` and `docs/REDUCTIONS.md`. The section preserves
  `p,q,g,kappa>0`, `m>=1`, the printed-scalar/advectively-corrected distinction,
  and the local rather than global/full-system scope.
- The source-error witnesses for (24)--(31), (33)--(34), and the qualified
  status of (32) match the exact fractions in `results/evidence.json` and
  `results/REPORT.md`. The text correctly says these refute universal printed
  formulas, not every special solution. The primary SVE paper is cited as
  `ap`; the distinct RKF/shooting paper is cited as `uddin2016rkf`, with both
  keys present in the currently integrated `draft/main.tex` bibliography.
- The current `results/numerical/numerics.json` has 21 passed runs: five each
  for 3.4, 3.6, 3.8, 3.9, plus cubic 3.5. Recomputed maxima/minima agree with
  the section: solver disagreement `1.08663e-13`, certified integral drift
  `7.32747e-15`, two-state disagreement `2.44249e-15`, exact-quadratic error
  `4.44089e-15`, coarse/fine endpoint difference `2.53052e-10`, original-PDE
  residuals `7.98450e-7` (DOP853) and `9.36175e-7` (tight RKF), sampled
  velocity/gradient minima `0.5`, and minimum absolute leading coefficient
  `1`. The code indeed uses a 9-by-9 tensor stencil of reconstructed `phi`.
  The post-repair acceptance in `docs/REVIEW_NUMERICS.md` supersedes that
  note's initial 17-run and vacuous-ladder findings.
- The section accurately qualifies the numerical evidence as fixed-stencil,
  finite-step and sampled-chart checks. Its warning that smaller stencil
  widths often worsen from roundoff, and that changing both tolerance and
  maximum step is not isolated tolerance convergence, is important and should
  stay. It makes no claim of global accuracy, arbitrary-IBVP solvability,
  shock certification, or transfer to the physical/full-bed model.
- After the director's display, table-width, and citation integration edits,
  the section copied into `draft/main.tex` exactly matches the current
  `manuscript_section.tex` content (surrounding whitespace excluded). The
  subsequent explicit `z>0` guard for the 3.5 fractional invariants and the
  table's definition of `L` as the `F'''` coefficient preserve the reviewed
  scope. Latest reviewed artifact SHA-256:
  `ACEA7A56147FE85C60BA920539D057AA5FC89FEF84DE2917B3FCC86682A30750`.

## Remaining release conditions

The director must still run the complete project and package checks, native
`latexmk`, citation/reference diagnostics, and rendered-page inspection after
the final integration. This review did not rerun the full symbolic derivation
or the numerical campaign; it cross-checked the section against their current
artifacts, reviewed code, and independently recomputed numerical aggregates.
The `m=3` fractional-power invariant formula is used locally; keep its
nonzero/positive `z` chart guard explicit in any expanded discussion.
