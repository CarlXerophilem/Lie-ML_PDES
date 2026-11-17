# Dissertation review instructions

This branch is prepared for **gemini-4-carbon** review. Review the existing dissertation; do not replace its frozen research questions or model definitions. No external reviewer has been invoked by this handoff.

## Read first

1. `README.md`: research motivation, frozen questions, obstacles and scope.
2. `docs/gemini-review-handoff.md`: review contract, resource gaps and validation limits.
3. `draft/dissertation_wku.tex` and its PDF: canonical manuscript and supplied WKU/MATH 4890 cover. `draft/main.tex` and `draft/dissertation.tex` are wrappers, not independent drafts.
4. `ref/README.md`, `ref/dissertation-sources.json`, and `evidence/CITATION_MAP.md`: current 23-entry bibliography and source locations.
5. Relevant version-bound evidence packages, including `research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md` and `research_artifacts/annular-transcritical-theorem-20261101/`.

## Frozen mathematical boundaries

- Multi-parameter SVE is the setting. Do not silently replace it by a single-exponent model or a different closure.
- Keep printed scalar P, corrected scalar M, and Eulerian systems E1/E2 separate. State the actual equation, parameter stratum, domain, branch and closure before using a result.
- Distinguish invariant PDE reduction, ODE order reduction, conservation laws, and reconstruction. A Lie symmetry alone is not a Noether conservation law.
- A finite ansatz or verified generator list is not maximal classification. Continuous parameter indexing is not proof of infinite-dimensional symmetry.
- State transversality, graph conditions, regularity, nonvanishing denominators, critical compatibility, recursion solvability and convergence hypotheses explicitly.
- Separate theorem/proof, symbolic identity, numerical evidence, conjecture and open problem. Sampled residuals and discrete corrector tolerances do not certify continuous PDE error.
- Hopf interpretations, noninteger spatial dimension and function-space projections remain exploratory unless the manuscript supplies precise definitions and proofs. Do not promote them into frozen results.
- Preserve negative results, ZIPs, manifests and existing experiment bytes. New outputs belong in `build/` or a new explicitly named artifact directory. No training, remote agents, or new experiments are needed for this review.

## Review output

Provide file/line or theorem/equation locators, the exact mathematical issue, severity, assumptions needed, and the smallest proposed correction. Audit the analytical propositions and proofs before stylistic edits. Identify missing proof steps without inventing replacements. Keep the eight-minute defence constraint in view; propose a concise narrative without changing the dissertation's research questions.

## Validation and navigation

Run `python tools/audit_dissertation_sources.py` for static reference/resource checks. This is not a proof check or a substitute for LaTeX compilation. If manuscript text changes, build from `draft/` using `latexmk -pdf dissertation_wku.tex`, inspect undefined-reference/citation warnings, and review affected PDF pages. Use relevant solver tests only when solver code changes; report commands and limitations accurately.

Use scoped `rg --no-ignore` searches when the repository ignore rules hide references/evidence. Historical instructions inside `.old/` apply to those snapshots only. `docs/project-map.md` and the legacy reference inventories describe earlier research states; the current handoff takes precedence for manuscript navigation. Preserve concurrent changes and use a guarded normal push.
