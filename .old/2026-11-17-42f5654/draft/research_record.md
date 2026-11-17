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

## Revision 2026-09-25: Formal PDE input and supplied-chart reduction

At the user's request, `main.tex` now formalizes `(p,q,r,n)`, fixed parameters,
jet equations, nonzero guards, real-domain predicates and data hypersurfaces.
Its new methodology sections give the exact chain-rule algorithm, a commuting
residual diagram and a conditional local correctness statement for a supplied
projectable one-generator chart with affine field reconstruction. This is a
bounded implementation step; it does not strengthen the earlier maximality,
physical-equivalence, neural-performance or global-solution claims.

Executable sources are `symm/generic/problem.py`, `chart_reduction.py` and
`sve_reduction.py`; behavior checks are in `symm/tests/test_chart_reduction.py`.
The source remains the printed master Eq. (7) of DOI 10.3390/math14030433,
with independent pullback checks against the known cubic ODE and direct
differentiation of a nonpolynomial reconstructed field. With beta=m*kappa,
the cubic example verifies; reusing its generator at m=4 fails the supplied
symmetry identity. That failure does not exclude other noncubic reductions.

Fresh verification: 130 pytest tests pass with the standalone ML script
excluded from collection; that script separately passes 22 checks, exit 0.
Plain pytest collection encounters its existing module-level SystemExit.
The test runner also emits an existing Windows temporary-cleanup warning.
The 13-page `main.pdf` compiles with resolved references and no overfull boxes;
the new methodology and page flow were visually inspected. Details, remaining
decisions and implementation limits are retained in root `checklist.md` and
`docs/pde_formalization_and_reduction.md`. No publication submission occurred.

### 2026-09-25 — Original-SVE and 2D fluid remote baseline

Deployed 148 hash-verified source/manuscript files to
`priestess:/home/carl/lieml/releases/20260925-fluid-baseline-v1`, activated
`pinn`, and ran 17 parameterized original-Eulerian-SVE, incompressible-2D-NS
and Oseen cases. The original conservative SVE balances are now independently
represented and reduced; they are not identified with the printed 2026 scalar
master equation. Cubic scaling and NS/Oseen x-translation charts pass exact
local pullback checks. The same SVE scaling fails at m=2 and m=4, without
excluding other symmetries. Deterministic `PDEsReductor` rankings are retained.

Remote verification: 139 pytest tests, 22 legacy standalone checks, 21 baseline
gates all passed. Analytic controls, conservation/positivity, dissipation,
incompressibility and refinement were checked. The 48² low-viscosity NS pilot
failed its 1e-5 refinement gate; 64²/128² passed at approximately 8.82e-7.
Both the resolution diagnostic and an initial missing-PyTorch collection
failure are retained. The final run used CPU PyTorch only for existing tests;
no fluid ML advantage was measured.

An SSH-served dashboard shows whole-domain and local time evolution, field
selection, a movable probe and diagnostics. Its plotted values and controls
were checked against the actual saved data. Full-precision arrays, source hashes,
environment versions and test logs were downloaded and archive-hash verified.
`docs/fluid_baseline_accomplishments.md` records equations, methods, parameters,
results and rerun instructions. `docs/fluid_baseline_novelty.md` compares the
implementation with Paliathanasis 2022, Paliathanasis–Leon–Leach 2026, Olver,
Maple/REDUCE, Going with the Flow and generalized-symmetry PINO work. Current
claims are reproducibility/engineering accomplishments; classical reductions,
complete classification, global solvability and future ML novelty are kept
distinct. No external-CAS completion or manuscript submission occurred.

### 2026-09-25 — Persistent paired evolution and parameter perturbations

Hosted `lieml-live.service` on `priestess` using the `pinn` runtime, exposed
locally at port 8879 through an SSH reconnect supervisor. The original static
baseline remains on 8878. Stateful NS, Oseen and original Eulerian SVE solvers
now evolve a fixed-parameter reference and a comparison with recorded
piecewise-constant parameter changes. Coefficient changes preserve the current
field; Oseen's advection drift is explicitly separated from its fixed velocity
mean. Atomic checkpoints and archived frames retain the experiment history.

212 tests passed locally and remotely. A separate nine-check pilot reached
t=100, including an analytic piecewise-viscosity shear, nonlinear NS diagnostics,
128²/256² refinement at t=5 (vorticity RMS discrepancy about 4.43e-7), and
original SVE with m=3 -> 3.02 at t=1. These are finite-time numerical controls,
not uniform error or global-existence proofs. Browser parameter/probe/frame
checks passed across all three models. Bitwise checkpoint recovery, automatic
systemd restart after process termination and local SSH reconnection were
verified. The handed-over default is unperturbed NS, nu=.01, n=128, horizon100,
with horizon extension and perturbation controls available. See
`docs/live_simulation.md` and `research_artifacts/live-simulation-20260925/`.

### 2026-09-27 -- Three-layer baselines and certificate-gated fusion

Implemented three independent demos under `symm/research_demos`. Static tests
enforce that ML-only imports no generic Lie module and Lie-only imports no
neural library. The fusion entry point consumes the exact JSON certificate
from Lie-only and rejects missing, unsupported or incomplete `m=3` evidence.

The Lie-only run verifies the supplied cubic chart, multiplier identity,
invariant-surface condition, reduced equation, lifting identity and exact
power-law control. The same supplied identity returns `unsupported` at `m=4`.
This remains a local supplied-chart certificate, not maximal classification.

The logistic MLP/PIKAN experiment ran the declared ten seeds and 10,000 Adam
iterations. PIKAN's mean relative L2 error was about `1.148e-3`, versus
`6.895e-1` for MLP, but several MLP seeds converged to wrong low-residual
branches. The literature's direction reproduced; its absolute values did not.
The bounded fixed-IVP Duffing experiment found a short-time TM-PINN median
`7.585e-5`, but at `T=3` its median rose to `1.756` with range
`8.678e-2--8.894`, preserving the negative long-horizon result.

For the SVE fusion, DOP853 and Radau differed by `3.281e-13`. Across three
seeds, `P2+z^3 N` had the lowest median profile error (`2.670e-6`), while
`P4+z^5 N` had the lowest raw residual (`5.354e-2`). Direct original-PDE and
lifted residuals agreed to about `1e-14`. The DOP853 tolerance ladder used
92/197/377 evaluations, with coarse/medium differences from fine of about
`2.03e-11/2.07e-14`; Radau agreed to `3.28e-13`. Fine DOP853 took about
`0.0034 s`; neural training took about 3.6--4.2 s per seed. No speedup or universal superiority is
claimed. JSON, CSV and figures are retained under
`research_artifacts/three-layer-baselines-20260927/`.

Final verification for this revision: the focused demo contract passes 10 tests;
the repository regression passes 222 tests; and the standalone historical ML
script passes 22 checks. Pytest retains its existing post-result Windows temp
cleanup warning. The manuscript compiles to 14 pages with resolved references
and no overfull boxes. All manuscript pages, three result figures, and both
pages of the week-2 interim report were visually inspected. Source hashes in
all three full-run reports match the current demo sources.

A bounded arXiv search recovered the expected Lie-PINN, LieSolver, symmetry
enforcement/domain-decomposition, TM-PINN, PIKAN, PirateNet and Saint-Venant
PINN neighbors, but no exact match for this SVE certificate-to-correction-to-
lifting combination. This supports a scoped research gap, not a priority claim.

### 2026-09-28 -- SVE reduction certificate v0.2 stage goal

The stage goal was narrowed to one falsifiable local result: fixed `m=3`, the
supplied `X_5=t*d_t-2*s*d_s` chart, and an invariant three-jet data family on
`Sigma_0={s*t^2=1}`. The generic reducer now checks strict off-shell invariance
of the data surface and each jet residual, plus absence of the orbit coordinate
after pullback. Incompatible data remain `pulled-back-only`; they do not turn a
valid PDE reduction into a false negative.

The v0.2 artifact records exact chart-rank, orbit-speed, fiber-rank, positivity,
`F'=0`, and leading-coefficient guards. This is a regular local certificate,
not a solution of its singular exits. The chosen data pull back to
`F(1)=K`, `F'(1)=K/3`, and
`F''(1)=-(2K/9)(1+eta_ic)`, with `eta_ic` a data parameter and
`delta_m=m-3=0` throughout.

A 697-parameter conditional model `P2+(sigma-1)^3*N(sigma,eta_ic)` was trained
at seven eta values and tested at four disjoint values for seeds 0--2. The
11 DOP853/Radau references were all regular on the 1001-point diagnostic grid;
their maximum cross-solver discrepancy was `3.312e-13`. All 12 held-out runs
completed. Their profile errors range from `2.636e-5` to `1.670e-4`, hard-data
jet errors are at most `1.111e-16`, and direct-versus-lifted residual differences
are at most `1.616e-14`. Taylor `P2` and `P4` errors are about `2.05e-2` and
`2.4e-3`, respectively, on the same held-out values.

Median training, DOP853 query and neural query times were 4.625 s, 0.00326 s
and 0.00262 s. The resulting arithmetic break-even estimate is 7,170 queries;
it is reported as a cost diagnostic, not an ML-speedup result. Generic-`m`
determining systems, maximality, equivalence groups, real-data subgroup choice,
singular branches, global topology, Eulerian/Lagrangian equivalence, and
`m=3+delta` symmetry continuation remain open.
