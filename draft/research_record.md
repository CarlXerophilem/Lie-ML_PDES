# Research Record: Fixed Core and Evidence History

## Preservation Contract

Requested 2026-09-12: retain established core narratives, theorem statements,
method structure and evidence. Subsequent work must append a dated change
entry and a source/proof/computation link before strengthening or superseding
a claim. A change of notation, title or layout is not stronger evidence.
Keep prior versions inspectable; do not erase a negative result or replace a
conditional statement with an unconditional one. Unsupported historical
claims remain archived, not silently promoted into the active manuscript.

## Fixed Project Identity

Title: **Lie-Symmetry Reduction and Taylor-PINN Approximation of a Lagrangian
Shallow-Water Equation**.

Level and duration: MATH 4890 undergraduate research, eight weeks in 2027
(a two-month project; calendar dates not yet specified). The present
computations are preparatory evidence dated 2026-09-12, not completed 2027
research. The proposal has four main sections plus References. The detailed
submission-style write-up is `draft.tex`; it is a pre-study manuscript, not
a claim of completed formal experiments or accepted publication.

Primary source: Paliathanasis, Leon and Leach (2026), DOI
10.3390/math14030433. Approved model: its printed master Eq. (7).
Retain the coordinate-conversion audit. Physical-model correction is not
the main task. No new maximal symmetry classification or universal solver.

## Stable Claim Register

| ID | Retained core statement | Status and evidence |
| --- | --- | --- |
| C01 | Study printed E_3[phi]=0, phi(t,s)=F(s*t^2), g=1,beta=0.1, sigma in [1,1.5] | User-approved scope; primary Eq.(7), Prop.1, Table3; manuscript problem section |
| C02 | The usual bed pullback adds -(phi_t/phi_s)*Btilde_s to Exner | Exact chain rule and symbolic counterexample; not a claim about unprovided alternative bed definitions |
| C03 | X5=t*d_t-2s*d_s is an admitted cubic scaling with invariant sigma=s*t^2 | Classical source claim independently checked by scaling weights; no maximality claim |
| C04 | E_3[F(s*t^2)]=R[F]/t, R=aF'''+b | Arbitrary-profile symbolic verification in verify_lagrange.py; full proof in draft.tex |
| C05 | F=C+K*sigma^(1/3), K^3=27g/(1-4g beta), is regular for positive sigma when g beta<1/4 | Source power-law family checked; stronger explicit a=2K*sigma^(7/3)>0 proved in manuscript |
| C06 | A uniform normalized residual and Lipschitz constant imply a conditional reduced-IVP error bound | Classical Gronwall proof retained; first-exit version adds validated tube and continuation premises |
| C07 | L=15 is valid on sigma in [1,3/2], r in [17/20,5/4], v in [-17/20,-7/20] | Exact rational arithmetic over 1728 subboxes; verify_bounds.py and feasibility_20260912/bounds.json; NOT a trained-network certificate |
| C08 | Compare P2/P4, DOP853, and P_N+z^(N+1)*NN for N=2,4 | Established Taylor/PINN ingredients; order and envelope both change, so no isolated Taylor-order causal claim |
| C09 | The classical control and perturbed-IVP pilot reproduce with independent checks | lagrange_evidence/report.json; sampled results, not interval enclosures |
| C10 | Both small CPU neural trials can train; profile-error and residual rankings disagree | feasibility_20260912/report.json; one seed,400 Adam steps; preparatory smoke, no multi-seed or speed superiority claim |
| C11 | Eight-week study will run a defined multi-seed comparison and report all failures/costs | Planned 2027 protocol, not completed evidence; rigorous neural residual validation is a stretch outcome |
| C12 | The smooth two-horizontal-dimensional physical SVE system transforms by HJ=mu, material momentum and Exner with retained transport and Piola divergence | Appendix C, locally proved coordinate equivalence; seven symbolic checks in test_sve2d.py; source audit sve2d_source_audit.md; contextual addition, not a change to the main model or a new solver |

## Historical Narratives Preserved

- The Eulerian near-cubic logarithmic correction construction remains in
  `proposal_support/derivation.md`, `references.md`, `verify_corrections.py`
  and `evidence/`. It is not refuted by switching models and is not used as
  proof for the Lagrangian master equation.
- The former engine/reducibility-index manuscript is retained verbatim at
  `proposal_support/archive/before_2027_submit_writeup/draft.tex` and `.pdf`.
  Its reduction-before-learning theme informs the current scope. Its claims
  of universal ML bottlenecks, invariant bounded-ansatz dimensions, and a
  closed-form-only rule attributed to McGreivy/Hakim are not adopted as
  verified claims. They require separate evidence; the last attribution is
  contradicted by the source's actual baseline guidance.
- The previous source-specific proposal is retained in the same archive.
  No established reduction, theorem, model caveat or classical pilot was
  discarded in the current revision.

## Revision 2026-09-12: Submission-Style Foundation

The proposal's mostly verbal opening is replaced by an explicit PDE,
profile IVP, domain, data and evaluation objective. Its title is fixed as
above and the old 12-week plan becomes eight weeks in 2027. The full
manuscript records proofs, method equations, source-attribution limits,
verification results and the prospective protocol.

New evidence permits two scoped additions: C05 gains an analytic leading-
coefficient formula, and C06 gains the computable conditional C07 constant.
The earlier statement that no PINN had been trained is accurate for the
historical classical pilot; C10 records new, separately dated smoke runs.
Their mixed results do not justify a performance claim.

Snapshot SHA-256 values (files preserved byte-for-byte):

| Snapshot file | SHA-256 |
| --- | --- |
| draft.tex | 4d95d5c52a9a6615dbb8a180cec11c7fbc8378fb33bc56f24d81ea212f27b7ff |
| draft.pdf | be468176cce33b8bed6915f6e8894bb6df93fb1afc85ba1edf92ef215e578b36 |
| proposal.tex | db3bb9810f9e656c8f87cf198868ed9817a9e00274b027728fa77f3258ade452 |
| proposal.pdf | ac8694c7b9798532844b4b6efddd405c393a3506b2b1d014d2482f464df8f67b |

## Revision 2026-09-12: Combined Publication Verification

The current combined report is `proposal_support/publication_check_2027.json`,
reproduced by `proposal_support/check_publication.py` after compilation.
It records both PDFs, citation resolution, body typography and text bounds,
source/evidence hashes, a fresh exact-box calculation and the support tests.
The preceding `lagrange_evidence/publication_check.json` remains unchanged;
its hashes identify the archived proposal, not the current revision.
This report checks artifact consistency, not novelty or uniform neural
certification. Claims C01--C11 and their limitations are unchanged.

## Revision 2026-09-13: Two-Dimensional Coordinate Context

At the user's request, Appendix C now states the physical two-horizontal-
dimensional SVE system in Eulerian and water-particle Lagrangian coordinates.
It includes explicit component equations, cubic Grass closure, the area
Jacobian and label density, a smooth-coordinate equivalence proposition,
an exact sloping-bed example, and the one-dimensional consistency limit.
The standard Eulerian source is independently verified through Crossref
and the University of Seville manuscript; the Lagrangian transformation
is derived locally, not attributed as an unverified author result.

The previous `draft.tex`, `draft.pdf`, shared bibliography and combined QA
report are preserved byte-for-byte in
`proposal_support/archive/before_sve2d_20260913/`. Existing core prose,
formulas, theorems and findings are retained; C12 adds context only.
The title, 2027 schedule, main printed-equation scope and proposal content
are unchanged. The refreshed combined QA includes the new appendix and tests.
