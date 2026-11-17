# Proposal Support: Current Lagrangian Basis

The September proposal (its former `draft/proposal.pdf` is absent from this checkout) was based on Paliathanasis,
Leon and Leach (2026), DOI `10.3390/math14030433`, as requested.
It studies the paper's **printed master Eq. (7)**, with a separately
documented failed equivalence check against Eulerian sediment transport.

**Confirmed scope (2026-09-12):** the user selected study of the printed
master equation with a model audit. Correcting the physical model is
outside the current proposal and would require a separate scope decision.
The audit remains an explicit limitation, not a prerequisite to beginning
the printed-equation reduction and approximation study.

- [../draft.tex](../draft.tex) and [../draft.pdf](../draft.pdf): full
  submission-style pre-study manuscript, with proofs and detailed method.
- [../research_record.md](../research_record.md): fixed title, eight-week
  undergraduate 2027 scope, stable claims, evidence history and preservation rules.
- [submission_source_audit.md](submission_source_audit.md): current primary-source
  integrity, claim-level literature checks and feasibility limitations.
- [sve2d_source_audit.md](sve2d_source_audit.md) and
  [test_sve2d.py](test_sve2d.py): Appendix C's two-horizontal-dimensional
  Eulerian/Lagrangian equations, primary-source checks and seven symbolic tests.
  This is coordinate context, not a change to the principal one-dimensional study.
- [publication_check_2027.json](publication_check_2027.json): combined current
  PDF, citation, formatting, evidence-hash, exact-bound and unit-test checks.
  Reproduce with [check_publication.py](check_publication.py) after building.
  This explicitly supersedes `lagrange_evidence/publication_check.json`,
  which remains unchanged as evidence for the archived preceding proposal.
  The pre-Appendix-C combined check and manuscript are preserved in
  `archive/before_sve2d_20260913/`.
- [lagrange_derivation.md](lagrange_derivation.md): beginner bridge,
  coordinate audit, cubic reduction, conditional error estimate and protocol.
- [lagrange_references.md](lagrange_references.md): current source map and
  bounded literature/novelty audit.
- [verify_lagrange.py](verify_lagrange.py) and
  [test_verify_lagrange.py](test_verify_lagrange.py): source-specific checks.
- `lagrange_evidence/`: preserved classical pilot and manuscript macros.
- `feasibility_20260912/`: exact rational box bound and two short one-seed
  CPU PINN trials. These are preparatory evidence, not the formal 2027 study.

From the repository root:

```powershell
python -B draft/proposal_support/verify_lagrange.py --output-dir draft/proposal_support/lagrange_evidence
python -B draft/proposal_support/verify_bounds.py
python -B draft/proposal_support/pinn_feasibility.py --steps 400
python -B -m unittest discover -s draft/proposal_support -p 'test_*.py' -v
python -B draft/proposal_support/check_publication.py --output draft/proposal_support/publication_check_2027.json
```

Build twice with XeLaTeX from `draft`. The prior proposal source/PDF are
preserved as `archive/proposal_before_lagrange_basis.*`; the supplied
reference PDF and production symmetry engine are untouched.
The older engine manuscript and immediately preceding proposal are preserved
byte-for-byte in `archive/before_2027_submit_writeup/`. Build both `draft.tex`
and `proposal.tex`; their shared bibliography is `references_2027.tex`.
The stdout-only feasibility command does not overwrite stored evidence.

## Historical Eulerian Near-Cubic Package

The files described below apply only to the previous proposal/model.
Their results and `evidence/publication_check.json` must not be used as
current Lagrangian validation. The old reproduction commands remain valid
for historical evidence, not the active manuscript's numeric inputs.

Start with [derivation.md](derivation.md) for the generator-to-ansatz explanation,
six correction equations, detailed proof, evidence boundaries, and oral-defense
questions. [references.md](references.md) records the bounded source audit.

The historical proposal is `archive/proposal_before_lagrange_basis.pdf`,
with its source alongside it. The earlier annotated source and PDF are
preserved byte-for-byte in `archive/`; the alternative `proposal (1).tex` is
untouched. The production symmetry engine is not used or modified.

## Reproduce

From the repository root, using Python with NumPy, SciPy, SymPy and Matplotlib:

```powershell
python -B draft/proposal_support/verify_corrections.py --output-dir draft/proposal_support/evidence
python -B -m unittest discover -s draft/proposal_support -p test_verify_corrections.py -v
```

From the `draft` directory, using XeLaTeX with Times New Roman installed:

```powershell
xelatex -interaction=nonstopmode -halt-on-error proposal.tex
xelatex -interaction=nonstopmode -halt-on-error proposal.tex
```

The verification command defaults to stdout only when `--output-dir` is omitted.
The output option regenerates `report.json`, the manuscript's numeric table
and macros, and PDF/PNG residual-scaling plots. These are generated evidence,
not hand-edited results. The report includes package versions and the source
SHA-256. Run evidence generation before rebuilding the manuscript after changes.

## Evidence Boundaries

- The proof is a local residual-order result with explicit positivity and
  compactness hypotheses, not a full-PDE solution-error theorem.
- The pilot verifies coefficient identities, a classical correction trajectory,
  derivative consistency, sampled positivity and two-sided residual order.
- A constant-matrix exponential independently checks this particular trajectory.
- Neither solver tolerances nor grid samples are interval-arithmetic certificates.
- No PINN was trained, and no neural advantage or verified novelty is claimed.
