# ML decision for the 1D SVE exact-first ODE programme

**Decision: abandon the pure-PINN route for this programme; do not launch another pure-PINN campaign.** The current ODE is already reduced exactly, has an explicit first integral, and is solved by standard numerical methods. Across the closest existing campaign, 23 neural runs passed **0** complete accuracy/residual gates; the non-neural Chebyshev control passed the two fixed-profile gates. This rejects pure PINNs for the tested workload, not every hybrid or future SVE task.

## What is being decided

The active object is a registered one-dimensional reduction of a named scalar model, followed by an ODE initial-value problem. Keep printed scalar `P`, advectively corrected material scalar `M`, and Eulerian system `E` distinct. Every reduction is conditional on its generator, branch, local chart, invariant graph, data compatibility, and reconstruction having been checked. The 2026-10-10 package derives for its common-scaling graph an exact first integral `I=L(z,F,F';m)F''`, on `L != 0`, reducing the profile equation to a second-order ODE. This is already a structure result, not a learned one.

Two different goals must not be conflated:

| Track | Candidate learned object | What would count as success | Current disposition |
|---|---|---|---|
| Exact structure proposal | A discrete generator, first integral, symmetry, or parameter-branch hypothesis | A candidate passes exact prolongation / determining-equation or total-derivative identity; independence, rank, chart, and data tests also pass | No training. At most a cheap learned/rule-based ranker may be considered after a repeated, nontrivial candidate-search bottleneck is measured. |
| Approximate profile | `F(z)` or a correction for a fixed certified reduced ODE and declared data family | Held-out original ODE and reconstructed-model errors meet frozen thresholds, and end-to-end amortized cost beats DOP853, Taylor/series, and Chebyshev at the same accuracy | Pure PINN no-go for present workload. Keep classical solver and spectral reuse as defaults. A hybrid remains open only for a named unmet task, with exact constraints fixed first. |

“Exact structure” means the final accepted statement is exact; a model prediction is only a proposal. In one independent variable, solving an already certified ODE does not discover a PDE symmetry or automatically lower ODE order. A fit to `F` is approximation, not an integral or order reduction.

## Evidence behind the no-go

1. The current package index records 40 bounded approximation runs, including 16 runs reaching their evaluation budget; for its declared smooth profile benchmark the Chebyshev control was most accurate. The 10 October report gives median fixed-feature wall times of 0.104–0.251 s for the tested tanh variants and 0.286–0.292 s for Chebyshev, with Chebyshev errors near floating-point/reference accuracy. These timings are from that specific implementation and task, not a universal solver ranking.
2. The newer 19 October package is the more relevant comparison: 17 planned and 6 exploratory neural runs, across affine/material tasks, produced **0/23 all-gate passes**. All six derivative-compatible exploratory fits still missed at least one threshold: state max error `1.16e-5`–`2.85e-5` (target `1e-5`) and original scalar residual `5.15e-3`–`1.33e-2` (target `1e-4`). The 21 runs that reached the full L-BFGS evaluation budget did not thereby demonstrate optimizer convergence.
3. In that run, degree-16 Chebyshev reuse passed both fixed-profile state and actual-original-residual gates. Reported setup plus reference-integration time was `0.01030` s and `0.01263` s on the two tasks. This is a fixed-profile numerical control, not a family-wide certificate. The neural campaign's combined wall time was `284.0249` s; a matched-accuracy neural break-even was not established. Do not divide that aggregate by a nominal query count to claim a universal per-query ratio.
4. The active package already supplies a first integral and locally well-posed regular ODE branches. SciPy 1.17.1 documents DOP853 for high-precision nonstiff IVPs and Radau/BDF alternatives for stiff problems; the project also has Taylor and Chebyshev controls. A strong baseline is therefore cheap to obtain and must not be replaced by a weak coarse mesh or an unmatched BVP.
5. PINN literature gives plausible failure mechanisms (optimization/conditioning and gradient pathologies), but only motivates diagnostics. Its results do not predict SVE-ODE performance. Approximation-existence theorems for tanh networks do not establish that a finite optimizer finds those approximants.

Interpretation: this is a **bounded empirical no-go for pure PINNs under the tested model family, accuracy gates, architectures, and budgets**. It is not proof that every neural/hybrid surrogate fails or that no future repeated-query task could amortize training.

## Exact-structure track: gate before learning

Current exact-first sequence:

1. Freeze which equation is under study (`P`, `M`, or `E`), parameters and parameter strata, sign branch, regularity, and state/data domain.
2. Derive or verify the point generator and invariant graph by the determining identity. A finite ansatz search establishes only its declared search-space result, not maximal classification.
3. Check the base-orbit rank and invariant coordinates; pull back the original equation and initial/boundary data.
4. Derive and verify a first integral `D_z I=0` on the ODE. To claim an order drop from order `r` to `r-1`, verify functional nontriviality/independence on the declared chart and reconstruct the integration constant from the same initial jet. A symmetry candidate must satisfy its ODE determining identity and regular order-reduction chart.
5. Solve the resulting ODE classically and check reconstruction into the same original model.

No learned module belongs in steps 1–4 for the current fixed problem: the exact generator, quotient and first integral already exist, while current symbolic checks run cheaply. The 19 October analyzer exercised 29 configurations in about 39.6 s subprocess wall across mixed models and controls; this is not a direct fair timing of a new ODE-discovery algorithm, but it is a warning that training overhead has no demonstrated target to amortize. A possible future proposal model may rank a finite set of exact symbolic candidates across many model/parameter instances. It must not supply accepted coefficients or certificates. Compare against (a) direct determining-equation/nullspace solving, (b) exact first-integral/ODE tests, and (c) a simple feature or frequency baseline. Stop if the exact baseline remains below 60 s per instance and no repeated workload of at least 100 distinct instances is documented, unless a separate measured bottleneck justifies a smaller pilot.

## Approximation track: PINN stop rule and any later test

Do not restart pure-PINN/PIKAN training on the current fixed profile or the already tested one-parameter perturbations, including by indefinitely swapping seeds or optimizers. A hybrid is not authorized merely by renaming a PINN: first name a task that exact structure plus the classical solver does not already meet. Re-open an ML pilot only if at least one condition changes materially: a verified ODE family with many genuinely distinct parameter/data queries; an accepted reduced ODE whose classical solve is measured to be expensive; or a new target with a credible approximation gap after series and spectral controls. Preserve verified reductions, first integrals, initial jets, domain and denominator guards exactly; any ML component may approximate only the remaining object.

If reopened, run one small, pre-registered feasibility pilot only (not a broad campaign):

| Gate | Required protocol |
|---|---|
| Freeze task | One named model (`P`, `M`, or `E` reconstruction), reduced ODE, branch/chart, parameter/data distribution, interval, initial data, and physical outputs. Split whole parameter/data profiles before any fitting. |
| Baselines | Adaptive Taylor/local series where analytic; SciPy DOP853 at tight tolerances for nonstiff IVP or Radau/BDF if stiffness is evidenced; degree-refined Chebyshev/collocation on the same IVP. Add a compiled/reused classical surrogate for repeated queries. Do not compare IVP learning with a differently posed BVP. |
| Cost accounting | Wall and CPU time, setup, training, validation, fallback, derivative evaluation, original-model reconstruction, and inference; include offline cost. For `Q` queries report `C_ML(Q)=C_train+Q(C_infer+C_check+C_fallback)` against `C_classical(Q)=C_setup+Q C_solve`, using the same accepted outputs and tolerances. |
| Accuracy gates | Hold out entire profiles and seeds; enforce initial-jet error, state error, derivative error needed by the highest ODE order, reduced ODE residual, and the actual original scalar/system residual after reconstruction. Check branch/denominator margins and positivity on a dense independent grid; use interval/validated bounds if making a continuous claim. Sampled residuals alone are not continuous certificates. |
| Pass | At least 3 independent seeds, every held-out case passes all frozen numerical gates, and the lower-confidence cost comparison shows end-to-end break-even by `Q <= 100` while matched-accuracy quality is no worse than the classical control. Require useful headroom (target at least 2x end-to-end speedup) to justify model maintenance. |
| Stop | Stop the pilot at 30 minutes wall, 2 CPU cores, 2 GiB RSS, or 3 seeds, whichever comes first. Stop immediately if no seed reaches every gate by 10 minutes, if domain/chart guards fail, or if an exact/classical control is already within tolerance at lower total cost. Do not expand to more architectures to rescue a failed pilot. |

The 2x and `Q <= 100` values are proposed decision thresholds, not literature constants. They are deliberately stricter than merely tying: noisy timings and code complexity make a marginal offline win unpersuasive. The user did not authorize a new training run in this assignment; no pilot is started here.

## What PINN applicability means here

Pure PINNs are mathematically **applicable** in the limited sense that a differentiable trial network can be trained against the already known ODE residual and initial data. The original 2D PDE PINN formulation is also possible before reduction. This does not mean they are **useful**: the classical IVP is low-dimensional, has an exact first integral, and has efficient adaptive and spectral solvers; prior directly relevant neural runs failed the combined gates and did not break even. For this task “PINN” describes a residual-training formulation, not a guarantee, method of exact symmetry classification, or certificate. A hybrid may be considered only if exact structure is preserved and it solves a named unmet task with matched-cost held-out evidence.

## Gaps before any future ML claim

- No neural method has demonstrated a matched-accuracy break-even against repeated classical solves or a reusable classical family surrogate.
- Existing 23-run negatives are limited to two constructed smooth tasks/families and stated architectures, thresholds, and budgets; discontinuities, shocks, stiff regimes, wider parameter ranges, and measured physical data were not tested.
- The learned structure track has no verified success case and no dataset of independent SVE equation mechanisms. Current finite symmetry checks are not a maximal classification and do not define a supervised corpus.
- A sampled network residual does not prove a uniform residual, branch preservation, or a continuous error bound. Any such claim needs independent validated numerics or an analytic a posteriori argument.
- External literature supports methods and known risks, not this project's speedup or novelty. The source set below is intentionally bounded (10 primary identities; citation depth 0), not an exhaustive novelty search.

## Provenance

Local evidence inspected: `README.md`; `draft/main.tex`; `docs/project-map.md`; `research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md`, `THEORY.md`, and `FINDINGS.md`; `build/sve-autonomous-20261019/REPORT.md`; `build/sve-autonomous-20261019/learning/{summary.json,costs.json,scalar_followup.json,FINAL_SUMMARY.json}`; and read-only `build/sve-general-symm-20261020/ML_INPUTS.md`. Exact local source paths, versions, retrieval state and source anchors are in `ml_sources.json`; direct retrieval receipts and section anchors are under `sources_ml/`.
