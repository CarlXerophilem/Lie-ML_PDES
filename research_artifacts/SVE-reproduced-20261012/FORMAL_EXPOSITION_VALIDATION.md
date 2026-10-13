# Formal manuscript exposition, 2026-10-13

The manuscript's Section 8 is expanded into a step-by-step replication.
This revision changes exposition and attribution; `main.py`, the numerical
trajectories and their computation evidence remain unchanged.

## Reader-facing changes

- Replaced prompt-highlighted bracket headings with numbered mathematical
  subsections. A table now lists all six generator fields, their parameter
  conditions and finite flows, including the additional `m=1` boost.
- Derived the master equation from the printed bed/momentum compatibility
  relation and expanded both currents by product and quotient rules.
- Derived `Q=eta-tau*phi_t-xi*phi_s` from a transformed graph. Explained why
  graph invariance and equation symmetry impose different conditions.
- Displayed total derivatives, recursive and expanded prolongations, all
  partial derivatives needed in the prolonged master residual, and each
  free-derivative coefficient split. Integrated the determining equations
  separately for generic `m`, `m=3`, and `m=1`, before proving sufficiency.
- Added full cubic commutator and generic optimal-system tables, with
  worked adjoint actions and parameter/line-equivalence qualifications.
- Tabulated the nine source cases with invariants, graphs and exceptional
  outcomes. Showed complete scaling/traveling derivative substitutions,
  time factors, currents, first integrals, quadratures and lost-branch guards.
- Made the cubic further reduction explicit, including its first-order
  rational equation and chain-rule denominator. Kept the source-error table
  and exact singular power profile distinct from regular numerical IVPs.
- Explained the Taylor recurrence through the next coefficient and displayed
  the full Fehlberg tableau, stage equations, error indicator and step control.
- Added mathematical pseudocode for the actual symbolic/numerical workflow.
  Authored orbit arguments and candidate integrals are identified as such.
- Removed visible file paths and executable commands from the manuscript,
  keeping operational details in companion documentation. TeX figure-asset
  paths are retained as compilation dependencies, not rendered instructions.

## Reference and mathematical review

The requested example is M. S. Bruzón and M. L. Gandarias, *Symmetry Analysis
and Conservation Laws of a Family of Boussinesq Equations*, a chapter in
*Symmetries and Applications of Differential Equations* (Springer Singapore,
2021), pp. 153–171, DOI `10.1007/978-981-16-4683-6_5`.
The local primary PDF and Crossref metadata were checked. Section 2,
pp. 157–159, supports the exposition pattern; Section 4, pp. 166–169,
supports the separate conservation-law/first-integral step. Its equation,
generators and conservation laws are not transferred to SVE. The bibliography
now has 20 entries.

Two GPT-6-Sol high researchers independently examined the SVE derivations and
the chapter. A fresh GPT-6-Sol high reviewer checked all five manuscript claims:
derivation, reductions, reference use, exposition and numerical methodology.
The review accepts them within their declared scope, with no blocking
mathematical finding. A final visual pass corrected the functional-derivative
notation in the variational-Lagrangian explanation; this changes no SVE result.

The assumptions remain explicit: the printed scalar model, fixed positive
`g,kappa`, `m>=1`, and positive local velocity/gradient, with all divisions
guarded. The completed local point classification is not a full-bed,
generalized-symmetry, singular-chart or global classification. Constructed
IVPs, sampled residuals and series truncations remain finite diagnostics.
Lagrangian coordinates do not establish a variational action. A reconstructed
field on `(t,s)` has time and one material coordinate, not two spatial dimensions.

## Validation

Native MiKTeX `latexmk` builds the manuscript successfully. The final
citation/reference log has no unresolved references, citation warnings or
overfull boxes. Underfull-box diagnostics remain. The expanded section,
generator/invariant tables, long formulas, algorithm and bibliography were
rendered with Poppler and visually inspected. `draft/main.pdf` is synchronized
with the compiled result; the reproduction and series fragments are synchronized
with `draft/main.tex`.

The required combined regression finished with **173 passed, one failed**
in **44.85 seconds** (46.71 seconds process wall time). All **80 reproduction
package tests** passed within that run. The one failure is the existing
Windows audit-fixture/hash mismatch:
`scripts/tests/test_project_audit.py::test_missing_expanded_evidence_is_not_a_false_carrier_failure`.

Project data-flux verification and the workflow runner passed. The project
audit retains **218 existing issues**: 146 tracked temporary outputs,
41 Markdown links, 30 canonical-reference integrity mismatches and one
unavailable external archive. These failures were not suppressed or repaired
by changing the research checks. Source-only whitespace checks passed.

The frozen 20261010 evidence, both dissertation files, executable `main.py`
and canonical numerical evidence are unchanged. The previous manuscript
and synchronized fragments are preserved in the pre-edit archive.

Exact artifact hashes, commands, build/test logs, review, reference note and
source checks are recorded in
[the validation receipt](results/formal-exposition-validation/validation.json).
The current `RELEASE_MANIFEST.json` binds the final manuscript and its companion
evidence. Earlier validation documents describe their respective releases.
