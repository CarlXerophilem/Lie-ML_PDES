# Week 4: boundary-aware symmetry certificates and solver comparisons

Date: 2026-10-11. The written specification and single-agent execution were
approved in conversation, and the implementation is complete. Work stays offline until
a paper novelty review requires literature search. CPU computation is permitted.
The suggested directory layout is flexible; reuse the current core and preserve
the frozen evidence package.

## Purpose and success criteria

Make the nine-stage method in [main.tex](../draft/main.tex) executable and easy
to inspect. Separate equation symmetry, invariant boundary/data compatibility,
reduction, analytical order reduction, and approximation accuracy. Produce exact
certificates and reproducible classical/neural comparisons without promising
neural superiority, maximal SVE classification, or arbitrary-IBVP solvability.

| Priority | Goal and Python implementation | Urgency | Usefulness |
|---|---|---|---|
| 1 | Boundary-aware symbolic certificates, parameter strata and genuine spectral/IVP controls, exposed through `run_pipeline.py` | 90-95% | 90-95% |
| 2 | Constrained PyTorch PINN/KAN profiles and a parameter-conditioned cost comparison with held-out validation | 65-80% | 75-90% |

These ranges are subjective planning judgments: urgency concerns manuscript
delay; usefulness concerns obtaining defensible evidence. They are not measured
probabilities. The second goal depends on the first goal's admissibility gates.

## Review findings and mathematical contract

Read [the project map](project-map.md), [the experiment index](../research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md)
and [the current theory](../research_artifacts/sve-progress-20261010/docs/THEORY.md)
with the manuscript. The current package already supplies third-order
prolongation, the common-scaling chart, first integrals, two scalar models, and
43 tests. Its Chebyshev control fits fixed features; its tanh control trains only
output weights. Neither is the proposed spectral collocation/deep-PINN comparison.

1. A finite determining matrix has finite nullity. Certify the nonlinear
   diffusion counts 4 and 5 within a declared sufficiently rich finite ansatz,
   and reaction's count 3 for nonzero coefficient. At the zero coefficients,
   report the finite ansatz result separately from the exact infinite-dimensional
   heat-solution superposition family. Do not infer maximality from matrix tests.
2. Keep `printed` and `physical_corrected` scalar SVE results separate. Declare
   `t>0`, `phi_s>0`, `phi_t>0`, smooth classical solutions, real powers on the
   positive branch, and every leading-factor denominator.
3. The X5 defect is an off-shell identity. Its "only m=3" conclusion assumes
   `g*beta_tr != 0`. On the manuscript path `beta_tr=m*kappa`, `m=0` is an
   additional zero-transport case; vanishing on particular jets is not an identity.
4. The manuscript's `R_0` uses `phi=F(s*t**2)` at `m=3`. The common-scaling
   family uses `phi=t*F(s/t)`. Register both charts with separate initial data,
   residuals, measures and scope labels.
5. Record requested and effective tolerances. In this environment SciPy raises
   `rtol=1e-14` to approximately `2.220446049250313e-14`.

### Exact first integral to export

For the common-scaling chart, put `P=F'`, `V=F-z*P>0`, `beta_tr=m*kappa`.
Direct substitution gives `E=t**(-2)*R`, and

\[
L_{\rm print}=-z^3P+\frac{gz}{P^2}
                 +\frac{g\beta_{\rm tr}zV^{m-1}}{P},
\qquad
L_{\rm corrected}=F\left(\frac g{P^3}-z^2\right)
                 +\frac{g\beta_{\rm tr}zV^{m-1}}{P}.
\]

For each model, `R=(L*F'')'`. On `L!=0`, solve the separate second-order
problem `F''=I0/L`, where `I0=L(z0,F0,P0)*F''0`. Verify by an independent
third-order solve and by substitution into the original scalar PDE.
The Lie quotient reduces independent-variable dimension; the first integral
reduces differential order.

For the corrected momentum/bed equations, exact prolongation verifies `Xc`
with bed unchanged and the bed translation `d_b`. The lifted cubic candidate
`X5-2*b*d_b` is admitted at `m=3` with nonzero transport. This is a verified
subgroup, not a maximal classification. A common-scaling solution with nonzero
`I0` has `b=B(z)+(I0/g)*log(t)` and uses `Xc+(I0/g)*d_b` for its invariant graph.

## Boundary and continuous-space gate

[Hijazi's thesis](../ref/main/application-of-symmetry-methods-to-partial-differential-53fphztrbi.pdf),
section 2.3.4, printed page 28 (PDF page 39), separates finding equation
symmetries, preserving boundary surfaces, and preserving conditions on those
surfaces. The following implementation requirements apply that distinction;
they are project deductions, not a continuous-space theorem attributed to Hijazi.

For a regular boundary `Gamma_j={G_j(x)=0}` and data operator `B_j` of order
`r_j`, check

\[
XG_j\big|_{G_j=0}=0,\qquad
\operatorname{pr}^{(r_j)}X B_j
 \big|_{G_j=0,\ B=0,\ \text{declared compatible jets}}=0.
\]

Retain boundary regularity, corners/intersections, applicable differential
consequences and branch restrictions. Tangency is local; any global-domain
claim needs a finite-flow check. Normal/flux operators require the transformed
geometry and current convention, not merely an unchanged coordinate label.

| Common-scaling example | Exact check | Required conclusion |
|---|---|---|
| Moving ray `s-z0*t=0` | `Xc(G)=G` | Boundary invariant on its zero set |
| Fixed time `t=T0>0` | `Xc(G)` restricts to `T0` | Fixed initial slice is not preserved |
| Fixed wall `s=S0!=0` | Restriction is `S0` | Fixed wall is not preserved |
| `s=0` | Restriction is zero | Geometry passes; outside the current positive-z chart contract |
| `phi/t=F0` | Generator action is zero | Normalized Dirichlet data pass |
| Nonzero constant physical `phi=F0` | Restriction is `F0` | These data fail |
| Bed trace `b=b0+(I0/g)*log(t)` | Action vanishes for `Xc+(I0/g)*d_b` | Lift and trace must agree |

The finite strip `1<=t<=2` is an evaluation/quadrature window. Its time caps
are moved by scaling, so this strip is not a scaling-invariant IBVP domain.
The underlying wedge `t>0, z_left<s/t<z_right` has invariant ray boundaries.
The chart `log(t)` does not cover `t=0`; tangency there does not extend this chart.
An invariant solution satisfying selected data does not by itself make the
entire fixed-data problem invariant.

**Concrete review finding:** `symm/generic/chart_reduction.py` currently demands
off-shell zero generator actions and literal orbit-independent data expressions.
This is sufficient for its normalized examples but unnecessarily restrictive.
The same ray written as `s-t=0`, instead of `s/t-1=0`, is reported
`pulled-back-only`; likewise `phi-2*t=0` versus `phi/t-2=0`. The new boundary
gate must certify vanishing on the boundary/data manifold and normalize only
factors proved nonzero on the chart. Preserve raw expressions, unit-factor
guards and restriction witnesses. If that restriction cannot be certified,
return `unresolved`, without discarding the condition. Keep the existing exact
PDE certificate distinct from boundary/data/domain status.

For the common-scaling curvature family with fixed `F0,P0`, changing
`F''0` to `(1+eta_ic)*F''0` changes `I0` by the same factor. Update the scalar
boundary flux `I0/T` and compatible logarithmic bed trace together. Keeping the
old nonzero flux produces the exact mismatch `eta_ic*I0`; reject that combined
data specification. Do not reinterpret scalar-current flux as every physical
SVE flux without deriving the corresponding pullback.

Use `C^3([1,1.5])` profiles for the third-order strong residual and report the
`C^0` profile error separately from derivative errors. Trace compatibility,
nonempty solution families, uniform regularity and stability constants are
separate prerequisites for continuous-family/error claims. The existing exact
tube covers fixed common-scaling data, `m in [1,4]`, `z in [1,1.4]` only.
New perturbed data and the extension to `1.5` initially receive sampled guards,
not that theorem. Finite grids and small training loss are not continuous norms.

## Architecture and nine-stage evidence flow

Keep `symm/generic` as the jet/prolongation/chart authority. Add focused
parameter-model/rank-strata and boundary-certificate modules there; reuse the
current scalar evidence routines without editing their frozen package.
Add `symm/solvers/` for hybrid profiles, transformed loss, Chebyshev collocation
and classical integrators, and `symm/selection/` for admissibility and total cost.
`run_pipeline.py` is the single orchestration entrypoint. A separate `src/` core
is unnecessary for this design.
New Python interfaces are typed and modular; structured records separate
symbolic expressions, numerical callables, solver outcomes and evidence scope.
Use installed dependencies only and record their versions.

| Stage | Evidence or fail-closed output |
|---|---|
| 1. Specify the problem | Model/parameter fingerprint, branches, domain, data surfaces, operators and spaces |
| 2. Verify generators | Original prolonged residual, declared finite ansatz, exact matrices/minors and parameter cells |
| 3. Choose the subgroup | Brackets, independence, orbit ranks, boundary/data/domain restrictions |
| 4. Construct the chart | Invariants, inverses, Jacobians, positive/nonzero guards |
| 5. Pull back the problem | All required jets, equations, data, current/flux and integration measure |
| 6. Certify reduction | Nonzero factorization, reverse zero-set implication and separately qualified data status |
| 7. Analyze the profile | First integral, actual order, initial data, leading margins and classical controls |
| 8. Approximate | Hard Taylor/data lift, PyTorch residual/loss, differential linearization and parameter gradients |
| 9. Validate and select | Held-out original residuals, empirical errors, budgets, full-query timings and feasible cost choices |

Every certificate carries `exact`, `numerical`, `restricted` or `unresolved`
scope, assumptions and source/configuration hashes. An unavailable backend,
singular branch, failed boundary gate or training budget exhaustion remains
explicit. Rank-drop enumeration must retain pivot/denominator strata; a sampled
rank or a determinant of one guessed matrix is insufficient.

## Reproducible CPU benchmark contract

| Item | Default |
|---|---|
| Evaluation | 1001 points on `z in [1,1.5]`; independent training nodes and validation quadrature |
| Cubic anchor | Printed X5 reduction; `g=1`, `beta_tr=0.1`, `K=45**(1/3)`, `F0=2`, `P0=K/3`, `F''0=-2*K/9` |
| Common scaling | Both scalar models; `g=1`, `kappa=1/30`, `(F0,P0,F''0)=(2,0.5,0.1)` |
| Curvature perturbations | `eta_ic in {-0.1,0,0.1}`, with compatible constants/flux/bed data |
| Reference strata | Common-scaling `m in {1,2,2.9,3,3.1,4}`; positive-branch and leading-factor checks per case |
| Classical convergence | Chebyshev degrees `8,12,16,24`; DOP853 and Radau tolerances `1e-11,1e-12,1e-13,1e-14` with effective values/warnings |
| Neural seeds | `17,23,41`; float64 CPU; recorded parameter counts, node counts and optimizer evaluations |
| Hard profile | `P_2(z)+(z-1)**3*N_theta`; an optional order-4 prior is a labelled ablation |
| Neural architecture | Trainable tanh MLP and smooth polynomial-edge KAN; retain third-order differentiability |
| Empirical acceptance | Profile maximum error `<=1e-6` and unnormalized original-coordinate residual L2 `<=1e-4`, with sampled guards passing |

First compare fixed profiles for the cubic anchor and common-scaling `m=3` at
all three perturbations. Train conditioned common-scaling networks on
`m in {2.9,3.1}` and the three perturbations; validate without training on
`(m,eta_ic)=(3,-0.05),(3,0.05),(2.95,-0.075),(3.05,0.075)` for both models.
Keep new-parameter interpolation separate from repeated evaluation of a cached
profile. No reference values enter the physics-loss training objective.

Use explicit budgets: at most 500 Adam updates followed by 250 L-BFGS closure
evaluations, at most 120 CPU wall seconds per neural run and 30 minutes for the
default neural campaign. Budget exits retain their frozen candidate and final
validation when a run has started; unstarted runs have an explicit
`campaign-budget-not-run` record. Interleave methods and seeds in matched blocks
so the campaign cap does not silently favor the first method. Larger campaigns
are configuration choices, not silent reruns to replace failures. Accuracy
thresholds are empirical gates, not error theorems.

For the scalar residual over `1<=t<=2`, the quotient weights are `7/24` for the
cubic X5 chart and `3/8` for common scaling. Independently verify the original
integral. Include the derivative of a profile-dependent weight when such a
weight is used. Check differential-linearization gradients against an independent
directional derivative. These scalar weights do not automatically apply to the
two-field momentum/bed residual vector.

Record profile/derivative errors, raw reduced and original residuals,
first-integral drift where applicable, branch margins, setup/reference/training
time, warmed evaluation latency and full-query latency. Preserve every seed.
Do not assert hardware timing thresholds in unit tests.

For accuracy-admissible alternatives, compare
`T=C_setup+C_reference+C_train+N*C_full_query`. Define the break-even integer
as the smallest nonnegative `N` where the neural total is no larger than the
classical total. If the neural per-query cost is higher, or accuracy fails,
report no asymptotic speedup; handle ties and finite cost crossings explicitly.
Include reconstruction, required derivatives, guard checks and fallbacks in
full-query cost. Warmed forward-pass timing alone does not establish a speedup.

## Outputs, verification and week-four milestones

`python3 run_pipeline.py` will write under `build/week-4/`:
`symbolic_certificates.json`, `experiment_results.json`, `METHODOLOGY_REPORT.md`,
configuration/environment records, frozen candidates and compact scientific
plots. Reports retain failure records and link evidence to all nine stages.
The methodology report states the first integrals, scoped coupled-generator
results, boundary constraints and the measured domain of classical/neural use.
Required symbolic/classical verification failures produce a nonzero exit.
Neural accuracy and budget failures remain benchmark outcomes; they must not be
promoted to admissible solutions or successful speedup claims.

| Milestone | Reviewable result |
|---|---|
| Day 1 | Equivalent-boundary representations, positive/negative data cases, scoped rank strata and lifted generators |
| Day 2 | Both registered charts, genuine spectral collocation, tolerance ladders and original-residual checks |
| Day 3 | Hard constrained PINN/KAN profiles, correct loss measures and gradient cross-checks |
| Day 4 | Held-out conditioned families and honest total-cost/break-even records |
| Day 5 | Pipeline replay, claim/evidence review and concise manuscript-ready report; online novelty review only if needed |

Add focused tests for the mathematical distinctions above, including
equivalent boundary defining functions, moved time caps, incompatible fixed
flux, heat superposition, third-order jet limits, exact/conditioned hard traces,
collocation convergence and gradient agreement. Preserve and run the existing
engine/chart regressions and the evidence package's 43 tests.

Required validation remains:

```bash
python scripts/project.py audit
python scripts/project.py data-flux --out build/data-flux
python scripts/project.py workflow --out build/workflow
python -B -m pytest -q -p no:cacheprovider symm/tests/test_engine.py symm/tests/test_chart_reduction.py research_artifacts/sve-progress-20261010/tests
```

The approved addition is [dissertation.tex](../draft/dissertation.tex), with a
standard dissertation structure, selected manuscript bibliography and explicit
local Olver/Oliveri edition locators. Changes to TeX or bibliography require
native `latexmk`, final citation/reference warning review and rendered-page
inspection. Do not claim novelty or an advantage
over peer submissions from an offline inventory alone.

Review evidence on 2026-10-11: 66 existing tests passed; 18 common-scaling
sampled cases stayed regular through `z=1.5`; three perturbed cubic cases agreed
between DOP853/Radau to at most `1.75e-13` in profile jets, and the unperturbed
DOP853 profile matched the exact anchor to `1.78e-15`. These exploratory checks
are not the future benchmark campaign or an extension of the interval theorem.

Written-spec validation: project audit passed, data-flux verification passed,
workflow replay passed with the freshly generated data report, and the 66
engine/chart/current-package tests passed in 4.12 seconds. Commands used the
`build/week-4-review/` output directories; no frozen evidence or manuscript was
modified. The cited PDF page was extracted and visually inspected offline.

## Implementation review and measured outcome

`python3 run_pipeline.py` implements the approved scope in the existing `symm`
engine and new `symm/solvers` and `symm/selection` packages. New outputs are in
`build/week-4/`; the first campaign is also retained in
`build/week-4-initial-campaign/`. The frozen artifact package is unchanged.

- Exact certificates recover the finite diffusion nullities 4/5, reaction
  nullity 3 away from zero, and a separately proved infinite heat family.
- Both common-scaling first integrals and the selected corrected coupled
  generators pass exact checks. The equivalent moving-ray boundary test passes;
  fixed time/wall and incompatible-data controls fail as intended.
- All 39 classical cases pass the 312 tolerance comparisons. Independently
  integrated second-order common profiles agree with the third-order references.
- 138/156 spectral degree/case combinations pass both accuracy gates. Every
  case has an admissible spectral control. DOP853's scalar dense polynomial
  passes in 39/39 cases; Radau's state converges but its scalar dense third-
  derivative residual fails the specified gate in 39/39 cases.
- All 66 neural runs are retained. Two fixed PINNs pass; all conditioned models
  fail at least one held-out accuracy gate. The two admitted fixed networks
  have slower full-query cost than their cached spectral controls. No admissible
  neural amortization is demonstrated within this campaign.
- The selector records actual differential order, sampled leading margins,
  unknown stability/error constants and measured cost minima. It rejects fast
  accuracy-inadmissible candidates before computing a crossing.

The post-implementation research priorities are continuous regular-tube/error
certification (subjective urgency 85–95%, usefulness 90–95%), then a complete
corrected coupled determining-system audit with a specified boundary/data
problem (65–80%, 80–90%). The dissertation describes Python implementation
directions. Larger learning budgets remain an alternative experiment; they do
not resolve the continuous-space evidence gap. Novelty review is deferred until
a precise new claim requires online comparison.
