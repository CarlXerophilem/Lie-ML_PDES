# LieML PDE formalization, symmetry reduction and research gates

Updated: 2026-10-07. This checklist replaces conversational knowledge checks.
Current priority: P0 has verified a first-order obstruction only in the
declared diagonal-scaling class at `m = 3 + delta`. The next decision is the
unrestricted response/determining problem, followed by data/flux
compatibility. ML remains a candidate proposer behind exact symbolic gates;
it is not the authority on symmetry or reduction.

## Current evidence status

- [x] The fixed `m=3` regular local certificate is reproducible for
  `X_5=t*d_t-2*s*d_s`, `sigma=s*t^2`, the reduced equation and the declared
  invariant data surface.
- [x] Historical Eulerian near-cubic correction experiments exist, but they
  concern a different three-field formulation and provide sampled perturbative
  evidence rather than a Lagrangian symmetry-continuation theorem.
- [x] The printed reduced equation in the 2026 source conflicts with direct
  substitution into its printed master equation; the project uses the directly
  derived expression and retains the discrepancy as a source audit result.
- [x] P0 has a machine-checkable **scaling** obstruction certificate for
  `X_5=t*d_t-2*s*d_s` at `m=3+delta`, with `beta_tr=m*kappa`, fixed
  dimensionless `kappa`, and the branch `t,s,phi_s,v>0`. Its status is
  `verified` / `obstruction-verified-scaling`; it is not an unrestricted
  point-symmetry result.
- [ ] No unrestricted generic-`m` determining-system solution, maximality
  theorem or equivalence-group classification has been established.
- [ ] No exact or formally completed first-order continuation of `X_5` at
  `m=3+delta` has been established.
- [ ] No structural ML speedup, full Eulerian/Lagrangian equivalence, singular
  branch theorem, global quotient or validated interval error bound is claimed.

## Ordered research branches

### P0 -- near-cubic continuation or obstruction

The declared diagonal-scaling subproblem is complete. The unrestricted
first-order determining problem remains open and is the next analytic gate.

The next bounded mathematical question is not whether a neural network can fit
an `X_1`. It is whether the first-order determining problem is compatible:

`E_delta = E_0 + delta E_1 + O(delta^2)`,
`X_delta = X_5 + delta X_1 + O(delta^2)`,
`A_0 X_1 = -A_1 X_5`.

- [x] Freeze the exact Lagrangian master equation, multiplier convention,
  regular branch, jet order and assumptions such as `phi_s>0`; declare the
  sign branch needed to expand noninteger powers through logarithms.
- [ ] Derive the `O(delta)` determining equations without dividing by
  `delta`, `m-3`, a leading derivative, `phi_s`, `phi_t` or any branch factor.
- [x] Separate two claims: an unrestricted differential determining problem
  and a declared diagonal-scaling calculation. The latter is not a proof
  about all smooth infinitesimals.
- [ ] Fix the gauge freedoms of `X_1` modulo known `m=3` generators so that
  continuation is not confused with a change of basis.
- [x] Compute the exact first-order defect inside the declared diagonal
  scaling class, including the `m*kappa` coefficient perturbation and direct
  third-jet prolongation agreement.
- [x] Emit
  `research_artifacts/p0-near-cubic-20261007/p0_scaling_obstruction_certificate.json`
  with status `verified` / `obstruction-verified-scaling`, source hashes,
  nondimensional units, guards, divisions, multiplier convention and
  two-sided numerical secondary evidence.
- [ ] Compute the exact compatibility/cokernel condition for an unrestricted
  `X_1` before training any neural model. For a differential operator, do not
  replace formal completion by a finite matrix cokernel without labeling the
  restriction.
- [ ] If compatibility holds, recover and verify `X_1` exactly on every
  declared regular branch, including bracket and parameter-stratum checks.
- [ ] Only after `X_1` passes verification, derive approximate invariants and
  an approximate reduced equation; verify the invariant-surface, reduction,
  reconstruction and original-PDE residual identities through `O(delta^2)`.
- [x] Use two-sided numerical `delta` refinement only as secondary evidence.
  A sampled slope near two does not replace the symbolic coefficient check.
- [ ] Do not infer an approximate solution or an error bound merely from an
  approximate generator. Initial/boundary compatibility, existence and error
  control remain separate obligations.

Decision exits:

- `continuation-verified`: proceed to compatible approximate reduction.
- `scaling-obstruction-verified`: retain `m=3` as exceptional within the
  declared diagonal-scaling class and escalate to the unrestricted analytic
  gate; do not infer isolation among all point symmetries.
- `ansatz-inconclusive`: escalate to P2 rather than claiming persistence.
- `regularity-failed`: split the singular branch; do not divide it away.

### P1 -- data/flux-compatible reduction

- [ ] Fix the v1 target to smooth `1+1` or `2+1` balance-law systems with a
  distinguished time axis, optional differential constraints, branch guards,
  data surfaces and boundary fluxes. Shocks remain outside v1.
- [ ] Given an exact algebra, determine subalgebras that are bracket closed,
  have the required projected orbit rank and preserve the declared data.
- [ ] Verify density, flux, source, constraint, coordinate-Jacobian weight and
  boundary-flux pullbacks in a separate `conservation_status` record.
- [ ] Treat a result with only the trivial data-compatible subgroup as a valid
  negative result and retain the unreduced numerical route.
- [ ] Do not equate data-surface invariance with IBVP well-posedness, physical
  admissibility, a Noether current or conservation across shocks.

### P2 -- branch-aware differential completion

- [ ] Model equations and inequations as regular differential branches and
  preserve rankings, assumptions, divisions and uncovered branches.
- [ ] Compare the bounded Python result with Maple DifferentialThomas/PDEtools
  and REDUCE CRACK/LIEPDE when those backends are actually available.
- [ ] Record `verified`, `branch-partial`, `timeout`, `backend-unavailable` and
  `unsupported`; backend absence must not be simulated as a proof.
- [ ] Use completion to revisit generic `m`, maximality, equivalence classes,
  rank drops and the singular exits `F'=0` and `a=0`.

### P3 -- exact-gated structural ML

- [ ] Run P3 only if repeated determining problems are large enough that an
  exact baseline exposes a measurable cost worth amortizing.
- [ ] Predict a nullity/support/preconditioner or a fixed-rank candidate
  subspace, never a basis-dependent generator list or a certificate.
- [ ] Recover the candidate kernel exactly, verify all declared branches and
  fall back to the full solve on rejection, low confidence or OOD input.
- [ ] Preserve exceptional strata in family-level splits. The earlier
  dimension tree's zero high-symmetry recall is a safety negative baseline.
- [ ] Compare against exact sparse linear algebra, symbolic reuse, RRQR/SVD and
  randomized/recycled baselines at identical final-kernel accuracy.
- [ ] Include training, proposal, recovery, verification and fallback in total
  cost. Stop the ML route when its per-query denominator is nonpositive.

P3 is downstream of P0/P2 ground truth and P1 semantics. A neural approximation
to `X_1` may be explored only as a candidate after the exact obstruction problem
is defined; exact prolongation and compatibility checks decide acceptance.

## Working contract

- [x] Reuse the approved generic `(p,q,r)` architecture in `symm/generic`.
- [x] Read the existing specification and approved implementation plan.
- [x] Establish the baseline: 15 core, jet and translation-reduction tests pass.
- [x] Represent fixed parameters, domain conditions and data surfaces explicitly.
- [x] Distinguish polynomial, rational and nonpolynomial dependence on jets.
- [x] Implement reduction in a supplied local chart for one projectable generator.
- [x] Verify a supplied off-shell symmetry identity, chart inverse and graph invariance.
- [x] Generate derivative substitutions by the chain rule for every field and equation.
- [x] Retain denominator, rank and branch conditions; never silently discard data.
- [x] Verify the SVE cubic reduction against an independently derived ODE.
- [x] Reject the cubic generator at a noncubic exponent when its identity fails.
- [x] Test multiple fields, `r != q`, remaining PDE variables and invalid charts.
- [x] Add the formalization and algorithm contract to `draft/main.tex`.
- [x] Run regression tests and compile the manuscript.

## Implementation sequence

1. Add mathematical behavior tests before implementation.
2. Add `PDEProblem` and `DataCondition` around the existing `DifferentialSystem`.
3. Add `ReductionChart` and `reduce_in_chart`; preserve the scalar API.
4. Supply an executable SVE example and explain inputs, outputs and limits.
5. Record fresh verification results here.

The reduction input includes a generator, invariant coordinates, an inverse
base-coordinate map, an affine field reconstruction and nonzero residual
factors. The algorithm checks these supplied objects; it does not claim to
discover every generator or integrate arbitrary characteristic systems.
It checks `pr(X) Delta = M Delta` for a supplied regular multiplier matrix.
Failure of that sufficient test does not prove that no symmetry exists.

## Mathematical practice and decisions

- [x] Separate a dependent coordinate, a field, its graph and its jet.
- [x] Separate the group-flow parameter epsilon from the model perturbation delta.
- [x] Use `p` for independent variables, `q` for fields, `r` for equations and `n` for order.
- [x] Treat PDE coefficients as fixed parameters during a symmetry action.
- [x] Use exact identities before statistical or sampled loss checks.
- [ ] Review the implemented formalization and worked SVE output when convenient.
- [ ] Select physical initial/boundary data after inspecting their pulled-back constraints.
- [ ] Extend beyond supplied charts and supplied symmetry multiplier identities.
- [x] Reproduce the exact cubic branch before opening the `m = 3 + delta` study.
- [x] Execute the P0 diagonal-scaling obstruction experiment without
  conflating it with the fixed-`m=3` initial-curvature family.
- [ ] Resolve the unrestricted P0 continuation/obstruction problem without
  promoting the diagonal-scaling exit to a full classification claim.
- [x] Define structural ML as an exact-gated candidate task rather than a
  solution or certificate generator.
- [ ] Train structural ML only after P0/P2 produce exact labels and timing
  shows a plausible repeated-query benefit.

## Evidence boundaries

A verified result means a local, conditional identity for invariant fields in
the supplied chart. It does not prove a maximal Lie algebra, differential
completion, existence of solutions, global topology, or compatibility of an
arbitrary initial-boundary value problem. Data are pulled back as constraints
and retain a separate status. Nonpolynomial powers require a declared smooth
real branch. Numerical sampling is not part of exact symmetry verification.

## Verification on 2026-09-25

- Added 19 chart/formalization tests. Initial API and later guard-validation
  failures were observed before implementing the corresponding changes.
- `python -B -m pytest -q -p no:cacheprovider --ignore=symm/test_ml_pde_solver.py`:
  **130 passed**, exit 0. An existing Windows pytest temporary-directory
  cleanup emitted `PermissionError` after the successful test result.
- `python -B symm/test_ml_pde_solver.py`: **22 internal checks passed**, exit 0.
  Plain repository-wide pytest initially stopped in collection because this
  standalone script calls `sys.exit()` when imported. It was run separately,
  not omitted from verification. No test-runner repair was included here.
- SVE CLI: `m=3` gives `verified`, exit 0; `m=4` gives `unsupported`, exit 2,
  with the failed supplied symmetry identity retained in the output.
- `draft/main.tex` compiled twice with pdflatex. The 13-page PDF has resolved
  references and no overfull boxes; the existing bibliography has one underfull
  line warning. New methodology pages and final page flow were visually checked.
- `git diff --check` passed. Unrelated existing manuscript changes/deletions
  were preserved. Nothing was committed or submitted.

Read `docs/pde_formalization_and_reduction.md` for the executable interface,
positional jet-name convention and exact scope of the result.

## Remote fluid baselines — 2026-09-25

- [x] Deploy a hash-verified source/manuscript snapshot to `ssh priestess`.
- [x] Activate `pinn`; install scientific dependencies and CPU PyTorch for regressions.
- [x] Formalize and verify the original three-field Eulerian SVE balances.
- [x] Verify cubic scaling; record rejection of that supplied generator at m=2,4.
- [x] Run `PDEsReductor` candidate ranking and supplied-chart checks on SVE, NS and Oseen.
- [x] Run 17 parameterized finite-time evolution cases, with 41 frames per case.
- [x] Check analytic controls, SVE conservation/positivity and grid refinement.
- [x] Preserve the failed 48² low-viscosity pilot; pass the same gate at 64²/128².
- [x] Pass 139 pytest tests, 22 standalone checks and all 21 fluid-baseline gates remotely.
- [x] Serve whole-domain/local evolution, probe histories and diagnostics through SSH.
- [x] Verify actual dashboard data, field/time switching, playback and probe behavior.
- [x] Review named primary literature and classify these as reproducibility baselines.
- [x] Download and hash-check numerical evidence; record versions and source hashes.
- [ ] Establish a fluid ML task with matched-accuracy traditional controls and total-cost accounting.
- [ ] Run a mature CAS completion/parity study before strengthening certificate claims.

Results: `docs/fluid_baseline_accomplishments.md`; literature:
`docs/fluid_baseline_novelty.md`; evidence:
`research_artifacts/fluid-baseline-20260925/`.
The dashboard uses `http://127.0.0.1:8878/` while its SSH tunnel and server run.
No novel algorithm, general fluid solver theorem, or fluid-ML speedup is claimed.

## Persistent perturbation-ready simulation — 2026-09-25

- [x] Add stateful NS/Oseen/SVE stepping without changing the earlier batch solvers.
- [x] Keep a reference and comparison field at the same time; coefficient updates preserve the current fields.
- [x] Separate Oseen advection coefficients from its conserved velocity mean.
- [x] Save atomic checkpoints, archived frames and timestamped parameter events.
- [x] Host `lieml-live.service` in conda `pinn` on `priestess`, with user lingering and automatic restart.
- [x] Expose the service at `http://127.0.0.1:8879/` using an automatically reconnecting local SSH supervisor.
- [x] Show whole-domain fields/differences, local crop/probe, diagnostics and archived frames.
- [x] Pass 212 local and remote tests; pass the separate 9-check t=100 numerical pilot.
- [x] Verify full-precision checkpoint recovery, automatic process restart and tunnel reconnection.
- [x] Exercise actual browser perturbations for all three models, then leave a fresh unperturbed NS run advancing.

## Three-layer baselines and fused prototype -- 2026-09-27

- [x] Add an ML-only CLI with no import from `symm.generic`.
- [x] Run logistic MLP-PINN/PIKAN at 10 seeds and 10,000 Adam iterations.
- [x] Preserve all logistic seeds; record directional success but numerical mismatch.
- [x] Run bounded Duffing vanilla/higher-order/TM-PINN at `T=1,3`, seeds 0--2.
- [x] Record short-time TM advantage and the severe long-time instability.
- [x] Add a Lie-only CLI with no Torch/PyKAN import.
- [x] Verify `m=3`, the group flow, invariant, invariant-surface equation,
  reduced ODE, lifting identity and exact profile.
- [x] Retain `m=4` as an `unsupported` supplied-identity negative control.
- [x] Require the verified Lie-only JSON certificate at the fusion boundary.
- [x] Compare exact, Taylor `P2/P4`, DOP853/Radau, hard-IVP PINN,
  `P2+z^3 N` and `P4+z^5 N`.
- [x] Run every neural SVE method at seeds 0--2 and keep every result.
- [x] Report profile/derivative errors, raw/normalized residuals, direct PDE
  residuals, lifting differences, regularity, parameters and timings.
- [x] Generate JSON, CSV and PNG evidence for all three demos.
- [x] Keep cubic PIKAN out of the third-order SVE residual pending a smoothness gate.
- [x] Complete a bounded arXiv novelty check without converting no hits into proof.
- [x] Pass 222 repository tests and the separate 22-check historical ML script.
- [x] Compile and visually inspect the 14-page manuscript with resolved references.
- [x] Generate and visually inspect the two-page week-2 interim report.
- [x] Extend the fused experiment to a declared initial-curvature family at
  fixed `m=3`, with seven training values, four disjoint held-out values and
  seeds 0--2.
- [x] Emit a strict v0.2 certificate for the invariant data surface
  `Sigma_0={s*t^2=1}` and the three quotient jet data.
- [x] Keep exact rank guards separate from sampled `F'` and leading-coefficient
  margins; retain explicit singular/failure statuses.
- [x] Verify every held-out reconstruction in the original master PDE and
  preserve the distinction `eta_ic != delta_m`.
- [ ] Repeat the family experiment for a physically sourced data-compatible
  subgroup and real initial/boundary data.
- [ ] Test whether higher-order KAN splines provide stable third derivatives before transfer.
- [ ] Add validated interval residual bounds if the project needs a certified neural error.

Results and commands: `docs/three_layer_baselines.md`. Evidence:
`research_artifacts/three-layer-baselines-20260927/`. The conventional DOP853
solve remains faster for the single fused IVP, so no ML speedup is claimed.
The conditional-family run also does not prove speedup: its measured
amortization estimate is about 7,170 queries and excludes deployment costs.

Operations and interpretation: `docs/live_simulation.md`. Evidence:
`research_artifacts/live-simulation-20260925/`. The default horizon is 100,
extendable to 1000. The service remains ready when evolution reaches the horizon.

## Astra archive verification -- 2026-10-05

- [x] With bytecode and pytest cache writes disabled, the repository regression
  completed with **232 passed** in 73.28 seconds.
- [x] The independent historical ML script completed with **22 passed, 0 failed**.
- [x] The staged snapshot includes `draft/proposal(1).tex`, its PDF and the
  fluid, live-simulation and three-layer experimental evidence directories.
- [x] The staged tree differs from withdrawn commit `3911334` only in this
  updated checklist; line-ending and Windows symlink churn were excluded.
- [x] No archived file is 100 MB or larger; the largest blob is 66,347,904
  bytes. Three unrelated multi-agent planning files remain untracked.
