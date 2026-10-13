# Manuscript refocus handoff (2026-10-13)

## Scope and preservation

- Edited `draft/main.tex` and `draft/dissertation.tex` outside the existing
  `% BEGIN/END SVE REPRODUCTION 20261012` span. The director owns insertion of
  the verified series result there and synchronization with
  `manuscript_section.tex`.
- The dissertation has `% BEGIN/END VERIFIED SVE SERIES INSERTION 20261013`
  comments after its existing scalar SVE analysis. Only the verified
  recurrence, coefficient checks, numerical comparison, and exclusion
  statuses should be inserted there. No series metric is asserted here.
- The pre-series manuscript and bibliography are preserved in
  `archive/release-before-series-20261013.zip` (presence checked). No reference
  PDF or reference corpus was deleted by this refocus.

## Narrative changes

- Both title/abstract/introduction paths lead with the printed scalar SVE
  source audit, corrected local ODE solutions, existing exact first integrals,
  and finite numerical evidence. Refuted source formulas and unresolved
  branches remain part of the result.
- The next step begins with unrestricted `tau(t,s,phi)`, `xi(t,s,phi)`, and
  `eta(t,s,phi)`, their prolongation, and the original-PDE master determining
  equation. The active package's `build_symmetry_report` is SVE-specific;
  `derive_reduction` verifies selected generators downstream. A reusable
  unrestricted arbitrary-PDE determining solver is proposed, not claimed as
  implemented.
- The proposed ML target is a nonconstant, independent first integral
  `I(z,F,P,C)` satisfying `I_z + P I_F + C I_P + R I_C = 0` on an open regular
  chart, with `I_C != 0` when solving locally for `C` to reduce order; an
  admitted reduced-ODE generator is an alternative. Exact verification,
  compatible data, and matched-cost classical controls are required. The
  older learned-profile campaign remains secondary and does not demonstrate
  learned ODE order reduction.
- Three named interests are the Lagrange-coordinate option (not a variational
  action), exact exceptional parameter and orbit-rank strata (not a
  probability distribution without a sampling law), and task-dependent
  trivial-symmetry filtration (not automatically a chain of subalgebras or an
  ideal quotient). Valid translations and valid but task-unhelpful symmetries
  are not mislabelled invalid. Hybrid architectures and conservation analogies
  are deferred.
- The main related-work survey and unrelated quantum/decoherence appendix
  were removed from the active narrative. Their prior text remains in the
  archived release. The dissertation's prior profile-fitting chapters retain
  their negative outcomes but are explicitly labeled historical.

## Bibliography inventory

`draft/main.tex`: **52 -> 19** embedded entries. Retained keys, all currently
cited: `olver`, `oliveri2026`, `anderson2000`, `ap`, `otto`, `kovalev`,
`approxalg`, `tarayrah2023`, `teschl2012`, `lagaris`, `cohen2015`,
`mishra2023`, `koval2023`, `levi2015`, `sympinn`, `sveold`, `noether`,
`fernandez2017`, `uddin2016rkf`.

`draft/dissertation.tex`: **12 -> 12** selected entries; all currently cited.
Keys: `olver`, `olver1986`, `oliveri2026`, `anderson2000`, `ap`,
`tarayrah2023`, `teschl2012`, `lagaris`, `cohen2015`, `mishra2023`,
`sympinn`, `hijazi`. `teschl2012` is retained for the local analytic-ODE
existence statement and the director's series subsection. No new online
bibliographic claim was introduced by this edit.

The source-level citation-key inventory found no missing or uncited keys in
either manuscript. This regex inventory is navigation only, **not** native
LaTeX citation validation. Both manuscripts are **unbuilt at this handoff**:
the director will insert the checked series material, run `latexmk`, inspect
the final citation/reference warnings, and render changed pages. Broader
project audits and regression tests are also outside this writing handoff.
