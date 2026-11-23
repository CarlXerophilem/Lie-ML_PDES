# Next milestone: certified ML-assisted ODE solution and 2D reconstruction

The local theorem is the mathematical foundation. It does not complete the dissertation's required semi-analytic solver, which must include ML or a comparable learned architecture. The next milestone keeps the exact same two-dimensional PDE and the derived solution class.

## 1. Complete the previously selected regular IVP certificate first

Retain the earlier staged plan: use the same `c=-7` parameter values, with
the proposed regular initial data `r0=1`, `H0=6/5`, `Z0=0`. The proposed
interval `[1,21/20]` is a candidate, not an accepted enclosure. Derive an
explicit tube and positive margins for `r,H,S` and `|D|`, then bound the
continuous residual and propagated state error with validated arithmetic.
Record a shorter interval as a new experiment if the candidate cannot be
certified. The critical point is excluded from this first numerical certificate.

Keep the corrected material M model in its separate adapter and certificate.
Neither an M certificate nor an older radial-swirl adapter certifies this
Coriolis/slope-dependent two-dimensional model.

**Deliverable:** one fixed annular IVP with continuous profile and original-PDE
reconstruction bounds. This is the immediate solver target; a quantified
critical-crossing certificate is the following extension, not a new gate
blocking the regular IVP or the local theorem.

## 2. Use ML primarily on the derived ODE

Use an equation-derived Taylor prefix and a learned finite polynomial or
Chebyshev correction for the remaining profile. Compute all derivatives from
that same profile; preserve the exact currents through reconstruction. Save
actual learned coefficients/weights and raw proposals. A classical fallback
must not be counted as a successful learned output. Accept the learner's
output only through the independent certificate from step 1.

Use the divided ODE only on its certified regular chart. After the fixed-case
milestone, consider held-out nearby parameters within a separately budgeted
study. The later manifold formulation below may extend this architecture
through the crossing. Learned discovery of a new integral is not required to
establish this declared ODE-solving contribution.

**Deliverable:** PDE → derived quotient → ML-assisted profile → continuous
certificate → original 2D fields, with all costs recorded. This file is a
plan; no training has been performed in the theorem package.

## 3. Quantify the critical manifold as a subsequent extension

Derive branch-specific jets from the undivided equation using the exact critical state and one of the two eigenvector slopes. Prove an a posteriori enclosure for a local invariant-manifold graph, with positivity and `G S` bounded away from zero. Establish an explicit radial interval and state tube; do not estimate it by sampled residuals or step-size success. Ordinary Lipschitz estimates for `H'=N/D` are not valid through `D=0`.

A nonzero small residual `D H'-N` near the critical point alone is insufficient for a state-error bound: the leading coefficient vanishes. The certificate must also control the selected branch/tangent, critical-point compatibility, and a well-posed local manifold problem. Auxiliary-time integration cannot start at the exact equilibrium and cross it in finite time.

**Deliverable:** a validated interval for one branch, then the second branch, with an explicit map back to the original Cartesian fields. Keep existence proof, numerical enclosure and sampled diagnostics distinct.

## 4. Compare at matched certified accuracy

After nondimensionalization, report separately:

- Continuous profile/state bounds on the specified radial interval.
- Continuous residual bounds for the original mass, both momentum and Exner equations; include the bed's second spatial derivatives.
- Current/flux errors with the correct annular measure and actual boundaries.
- Cartesian field errors at the same `(t,x,y)` and derivative norms required by the PDE.
- Setup, training, verification, inference/fallback time, memory and amortization assumptions.

Use independent classical Taylor/Chebyshev and guarded ODE/manifold controls. Charge failed candidates and fallback. If the classical method wins, report that result; a verified hybrid method and a neural speedup are different claims. Do not revive a pure-PINN campaign.

## 5. Establish the exact literature boundary

The inspected Chesnokov v1 establishes flat-bottom annular water predecessors, while Berthon et al. supplies a distinct one-dimensional drifting-bed precedent. The present proof establishes a model-specific coupled-bed extension of those inspected results. It does not establish global novelty.

Search next around `rotating Saint-Venant Exner`, `radial transcritical morphodynamics`, `slope-dependent bedload`, and `implicit ODE saddle continuation`, including references and citing papers. Compare exact equations, hypotheses and conclusions, not only abstracts. Record unavailable text and negative searches without interpreting them as nonexistence. The general stable-manifold mechanism must remain credited as classical.

## 6. Dissertation and 8+2 minute defence

Once the quantified/ML milestone is independently checked, prepare a separate proposed manuscript patch. The core explanation should show: the specified PDE; why the solution class was derived rather than assumed; why normal-form division fails; the saddle and the two slopes; how all original PDEs are recovered; and exactly what the learner contributes.

Use English prose and TikZ diagrams. Mathematical fixtures remain clearly separate from real observations. For empirical applicability, inspect historical/government data and closure scales first; if they cannot support this invariant class, report that mismatch rather than relabelling the mathematical example as observed data.

Keep the full classification contract independently open. Its missing arbitrary-function, parameter-stratum and all-dimensional subalgebra obligations do not block this already-defined local theorem, and this local theorem does not discharge them.
