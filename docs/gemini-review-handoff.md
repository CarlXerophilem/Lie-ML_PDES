# Gemini-4-carbon dissertation review handoff

## Review target and frozen scope

Review `draft/dissertation_wku.tex` against its 51-page PDF, its embedded bibliography and the evidence carriers. This branch prepares the files for review; it does not send them to an external model. The supplied WKU/MATH 4890 cover, unsigned declaration, recorded submission date, frozen research questions, multi-parameter SVE definitions and analytical claims remain unchanged. Start with the research motivations and unresolved obstacles in the root README and follow `AGENTS.md`.

The priority is analytical validity: continuous extension and exceptional parameter strata; finite versus infinite-dimensional symmetry; transverse subalgebra families and local reconstruction; singular crossings, analytic representations and parameter-dependent error control. Challenge unsupported implications and identify precise missing assumptions. Do not substitute a different model, introduce an unproved Hopf interpretation, or claim a physical classification for every noninteger dimension.

## Source matching and restored resources

- `ref/dissertation-sources.json` covers all 23 embedded bibliography keys and their in-text occurrences. `evidence/CITATION_MAP.md` provides the claim-level review route. Legacy 47-key inventories are explicitly historical.
- The project-supplied Fernández-Nieto and Bluman–Cheviakov PDFs are added under `ref/dissertation/` with byte hashes. Existing aliases for Deng–Reid, Noether, Wang and the 2022 SVE paper are mapped, not needlessly duplicated.
- `research_artifacts/annular-transcritical-theorem-20261101/` is copied as an exact Git subtree from the manuscript's cited commit `c48d9994e4bfaf69a91913c73a59e7ef8f1e1bf7`. No proofs or validation records inside it were rewritten.
- The three Chapter 5 prototype scripts are supplied under `research_artifacts/sve-regular-correction-20261117/`; their import README states their restricted model and provenance limitations.
- Both navigation paths mentioned in LaTeX comments now resolve: `docs/dissertation-figure-workflow.md` and `evidence/CITATION_MAP.md`.

## Remaining resource limitations

Bibliography-only entries are Exner, Anderson–Fels–Torre, Druzhkov–Cheviakov, Chesnokov, Berthon et al., Teschl, Mishra–Molinaro, Trefethen, Güngör et al., and Westreich–Podolak. Their bibliography records and available source URLs are retained; this cleanup does not claim to have retrieved or revalidated those PDFs. Inspect their exact editions before accepting cited theorem/page locators.

The Olver PDF and the theorem package's evidence ZIP are Git LFS pointers in the Git tree. After cloning, use Git LFS to retrieve available objects, and verify successful hydration before inspection. The theorem package's plain-text proof, replay scripts and rendered PDF are present independently of its ZIP. Failure to hydrate an object is a resource limitation, not a mathematical disproof.

## Cleanup and validation

The obsolete root `checklist.md` is removed and its exact prior blob is archived with the old `AGENTS.md` and reference guide under `.old/2026-11-17-review-cleanup/`. Obsolete `draft/tmp/` QA screenshots are removed from the active tree; they remain in the earlier full-draft snapshot `.old/2026-11-17-42f5654/draft/tmp/`. Historical proposal support, reports, figures, solver code and evidence are retained because their research dependencies differ from current LaTeX inputs.

Run `python tools/audit_dissertation_sources.py` from the root. It checks literal labels/references, bibliography/citation matching, external cover assets, wrappers and mapped resource paths. The recorded result is `docs/dissertation-source-audit.json`. The cleanup does not alter the canonical TeX/PDF bytes, so the previous build/layout records remain applicable; it does not claim a new TeX build or a new theorem/experiment validation. Python syntax checking of the three imported scripts does not verify numerical correctness.

## Requested reviewer deliverable

Return a theorem-by-theorem and proposition-by-proposition report with manuscript locators, hypotheses, proof dependencies, source locators, gaps and severity. Separate blocking mathematical issues from missing resources and presentation improvements. For example, a claim of uniform tail bounds needs a specified parameter set and a uniform majorant; a collection of per-parameter convergent series is insufficient. Propose minimal edits without applying a wholesale rewrite. End with a feasible eight-minute defence narrative using only established results.
