# SVE reproduction run contract

Approved by the user on 2026-10-12: implement the preceding reproduction plan.

## Objective and scope

Reproduce and independently audit the mathematical content of Paliathanasis,
Leon and Leach, Mathematics 14 (2026) 433, local v3 PDF, equations (1)--(34),
Tables 1--3 and subsections 3.1--3.9. Produce a runnable `main.py`, visible
stepwise symbolic derivations, numerical SVE IVPs using classic Fehlberg 4(5),
and a reviewed section included in `draft/main.tex`.

Preserve printed formulas. A correction requires the exact source location,
failed check/counterexample, derivation, assumptions, and downstream effects.
The numerical examples are new dimensionless demonstrations, not source data.
Use g=1, kappa=1/30, beta=m*kappa. Default nonlinear initial jet at z=1 is
(F,F',F'')=(2,1/2,1/10), interval [1,1.1]; retain X4 [1,1.4] control.
Traveling alpha=-1, alpha3=1. Linear case 3.8 uses alpha=1 and initial
jet (0,1,1/10) at t=0 on [0,.4]. Generic m tests: 1,3/2,2,3,4.

## Boundaries

Keep printed scalar and advectively corrected physical models distinct.
Default local chart has phi_s>0 and phi_t>0; stationary and singular branches
are separately typed. No full-bed-system, shock, arbitrary-IBVP, global-error,
ML, or novelty claim follows. Maximal classification requires a complete
determining-system proof on its declared branch. Every unproved source claim
must have an explicit conditional/unresolved/refuted status.

All new research files stay here or in build/. Preserve the historical
sve-progress-20261010 package, its ZIP/manifest, and unrelated changes.
Baseline user change: deletion of ref/large-pdfs/application-of-symmetry-methods-to-partial-differential-53fphztrbi.pdf.
No Git commits, external publication, paid API calls, or memory edits requested.
Work in the requested shared directory; additive modules have disjoint owners,
and the director alone integrates main.py and draft/main.tex.

## Roles and checks

All child agents: GPT-6-Sol, high reasoning, isolated context. Up to three
children; CPU-heavy computations serialized with the director. Symbolic
research, numerical implementation, fresh independent review, and writing
remain separate roles. Authors do not approve their own claims. Claim changes
invalidate prior review. Ledger: LEDGER.json; research notes: docs/.
No user deadline, cost cap, or token cap was supplied. Computations use
bounded inputs and per-process limits (600 seconds by default); a timeout is
unresolved, not a theorem. Actual token/cache data are unknown unless exposed.

Required release checks: new package tests and demo; README project audit,
data-flux and workflow; engine/chart regressions and historical 43 tests;
native latexmk, final citation/reference diagnostics, rendered-page inspection.

## Shared interfaces

`sve_reproduce.core` owns t,s,u,p,q,a,b,c,r,w,x,y,g,kappa,m,z,F,P,C,H;
`total(expr,axis)`, `prolongation(tau,xi,eta)`, `act(expr,tau,xi,eta)`,
`master(exponent=m)` use exact SymPy expressions and beta=m*kappa.

`reductions.derive_reduction(case, exponent=3, alpha=-1, alpha3=1,
mix_alpha=1/4)` returns a dict with id, status, coordinate, ansatz,
residual (z,F,P,C,H; g,kappa), leading, rhs, velocity, gradient, ode_order,
steps, guards, source_equations. Cases 3.1--3.9 and table3-mixed.
status: regular_ode, identity, undefined, no_invariant_graph; absent expressions
are None. rhs solves H when order is 3. velocity and gradient are original
phi_t and phi_s at t=1 in profile jets, sufficient for the positive t charts;
case 3.8 uses its actual independent time. Steps are dictionaries with
label and expression (SymPy or str). No string eval for user input.

`symmetries.build_symmetry_report()` and `algebra.build_algebra_report()`
return JSON-serializable dictionaries with claims, formulas, exact checks,
source discrepancies and scope labels. `reductions.build_reduction_report()`
returns JSON-serializable nine-case/comparison/further-reduction evidence.
`numerics.run_campaign(out_dir, rtol=1e-9, atol=1e-11,
selected_reduction='all', selected_case='all')` returns a JSON-serializable
report and writes numerical CSV/figures below out_dir.

All reports distinguish successful audit execution from source agreement.
Numerical gates: scaled solver disagreement and certified integral drift
<=1e-7, independent original-PDE residual <=1e-6 with refinement evidence,
positive sampled branch margins, regular leading coefficient and endpoint
completion. Do not invent an integral for a row without a certificate.

## Required report keys

- [master equation]
- [infinitesimal generator]
- [Symmetries of the SVE Equation]
- [Commutators of the admitted Lie symmetries for the SVE equation]
- [listed Lie symmetries]
- [One-Dimensional Optimal System]
- [Similarity Transformations]
- [One dimensional optimal system and Lie invariants Table]
- [Solution ODE with all 9 reductions]
- [Numeric solutions to the ODEs]
