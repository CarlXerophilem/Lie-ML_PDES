# Novelty audit and baseline claim

Audit date: 2026-09-25. Scope: the supplied-chart Python reductor, original
Eulerian SVE, periodic incompressible 2D NS, and constant-drift Oseen controls.
This is a focused comparison, not an exhaustive proof that no prior work exists.

## Defensible claim

We implement a bounded symbolic verifier for supplied one-generator invariant
reductions of PDE systems. It checks chart inverses, graph invariance, a supplied
symmetry identity and exact jet pullbacks, retains admissibility conditions and
data traces, and exports reproducibility records. We connect this verifier to
independently checked finite-time fluid evolution baselines.

This is an **engineering and reproducibility accomplishment**. The present work
does not establish a new Lie-reduction theorem, a complete symmetry classifier,
a new fluid integrator, or a machine-learning speedup.

## Verified literature comparisons

| Source and evidence anchor | Consequence for our claim |
|---|---|
| P. J. Olver, *Applications of Lie Groups to Differential Equations*, 2nd ed. (1993), [DOI 10.1007/978-1-4612-4350-2](https://doi.org/10.1007/978-1-4612-4350-2); edition checked against [author bibliography](https://www-users.cse.umn.edu/~olver/books.html). | Prolongation and invariant-solution reduction are classical. Full book pages were unavailable in this audit; no page-specific theorem verification is claimed. |
| A. Paliathanasis (2022), [DOI 10.3390/sym14081679](https://doi.org/10.3390/sym14081679), publisher PDF p. 4 Proposition 1; pp. 8–9 §§4.10–4.12. | Eulerian SVE symmetries, exceptional cubic exponent, and similarity reductions predate this project. Independently verifying their coefficients is useful reproduction. |
| Paliathanasis–Leon–Leach (2026), [DOI 10.3390/math14030433](https://doi.org/10.3390/math14030433), publisher `00433-v3.pdf`, p. 2 Eq. (7), p. 4 Proposition 1, p. 6 Table 3, p. 7 §3.5. | The printed scalar master PDE and the generator `t∂t−2s∂s`, invariant `s t²`, and ansatz `φ=F(s t²)` are published. Our older scalar example is verification, not discovery. |
| Kavousanakis et al., *Going with the Flow*, [arXiv:2509.15963v1](https://arxiv.org/abs/2509.15963v1), p. 3 §2 Eqs. (1)–(4), pp. 5–6 §§3–4, p. 15 §6. | Symmetry coordinates, reconstruction and PINNs already appear together in dynamically rescaled PDE–DAE systems. Their evolving profile/rate problem differs from our supplied invariant-family check, but rules out broad novelty claims for “coordinates plus neural solvers.” |
| Wang et al., *Generalized Lie Symmetries in Physics-Informed Neural Operators*, [arXiv:2502.00373v2](https://arxiv.org/abs/2502.00373v2), p. 3 Proposition 2.2 and §3 Eqs. (1)–(4), p. 4 §4/Table 1. | Evolutionary representatives already augment PINO losses. A zero off-shell translation residual in one example is not a general theorem that symmetry losses fail at symmetric points, nor evidence of our approach's ML superiority. |
| Maple [InvariantSolutions](https://www.maplesoft.com/support/help/Maple/view.aspx?path=PDEtools%2FInvariantSolutions), Description/Optional arguments; [SymmetryTest](https://www.maplesoft.com/support/help/Maple/view.aspx?path=PDEtools%2FSymmetryTest), Description. | Supplied infinitesimals/invariants, testing, reduced variables, transformation-only output and sequential reductions already exist. `InvariantSolutions`, rather than `SymmetrySolutions`, is the relevant reduction comparator. |
| REDUCE manual [APPLYSYM/LIEPDE/DETRAFO §§20.1.1–20.1.4](https://reduce-algebra.sourceforge.io/manual/manualse127.html), [CRACK §§20.15.1–20.15.3](https://reduce-algebra.sourceforge.io/manual/manualse141.html). | Prolongation, canonical coordinates, inverse transformations, chain rules, determinant checks, unresolved conditions and nonvanishing assumptions are established computational features. |

Primary PDFs, arXiv metadata, Crossref and official documentation were checked.
MDPI HTML showed access interstitials; supplied publisher PDFs were read and
their identities checked against Crossref. Online Maple/REDUCE documentation
was accessed on the audit date and is not pinned to a locally installed release.
Failure to access a source is not evidence that prior art is absent.

Rusanov fluxes, SSPRK3, Fourier pseudospectral dealiasing, RK4, DOP853,
Taylor–Green decay and Fourier-semigroup Oseen propagation are used explicitly
as standard numerical controls. This audit does not claim originality for any
of them, and makes no numerical-method literature completeness claim.

## What is—and is not—verified

The reductor's exact condition `pr(X)Δ=MΔ` is sufficient within the supplied
regular chart. Its multiplier matrix is restricted to base coordinates and
fixed parameters; failure does not prove that no symmetry exists. Reconstruction
is affine in the profile fields. Guard retention is not a proof of nonempty
solution branches, formal integrability, or compatible initial/boundary data.

`PDEsReductor` ranks cheap candidates using
`2 * 1[pr(X)Δ=0] + 1[projected orbit rank > 0]`. This is deterministic,
untrained prioritization. It does not recognize all relative symmetries with
nonzero `M`, and its score cannot upgrade a reduction certificate. The new
runner executes this ranking as well as the stronger supplied-chart check.
No Maple/REDUCE completion is inferred from a Python result.

The original Eulerian SVE balances are checked directly in the new baseline.
They must not be silently replaced by the 2026 printed scalar equation: for
`b(t,s)=B(t,φ(t,s))`, the ordinary Eulerian Exner pullback includes
`−(φ_t/φ_s)b_s`, absent from the printed intermediate Eq. (6). Verification of
that paper's Eq. (7) alone does not prove equivalence to the original system.

## Candidate research beyond this baseline

1. Compare a completed-branch certificate with Maple/REDUCE on the same
   ranked systems, preserving divisions, inequations and uncovered branches.
   The backend and complete branch coverage are still required.
2. Establish and test a quantitative near-cubic defect/correction result on
   an explicit compact positive domain; compare it to the existing SVE
   similarity literature. This needs a theorem and a targeted novelty search.
3. Define a repeated-query parameter task and compare reduced ODE integration,
   interpolation, and a learned correction at matched accuracy, including
   training cost and break-even query count. A neural speedup is currently
   unmeasured; a negative result remains a valid outcome.

These are research questions, not accomplished novelty claims.
