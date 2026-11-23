# Research route: reproduction, controlled variation, open 2D problems

Updated 21 October 2026 from the user's research direction. This document
records scope and future acceptance conditions, not new experimental results.
The [immediate precision repair](residual-resolution-20261021.md) is delivered
without relaxing the original-P threshold. The next work remains completing
the source-faithful reproduction/extension demonstration, not starting a new
2D or training campaign prematurely.

## 1. Reproduce the source paper and make an extension demo

The starting point is Paliathanasis, Leon and Leach, *Mathematics* 14 (2026),
433, DOI `10.3390/math14030433`, as pinned in the current source audit.
The goal is complete accounting of its declared formulas and reduction
families, not a claim that all nonlinear solutions have closed forms.

- Keep printed source equations visible, including non-reproducing formulas.
- Distinguish faithful reproduction, independently verified correction and
  extension: new exact solutions, locally constructed IVPs, series and numerics.
- For each accepted result retain the generator, invariant condition,
  reduction, solution type, parameter/chart/data conditions and independent
  reconstruction in the original equation.
- Demonstrate particle-position surfaces in `(s,t,phi)` with valid-domain masks.
  A finite numerical residual is a diagnostic, not an exact proof or a
  continuous error theorem.
- Integrate accepted explanations and figures into the dissertation only in a
  separately requested manuscript revision; this roadmap does not edit it.

The current evidence is the [printed-P delivery](../build/sve-P-solutions-20261021/DELIVERY.md)
and [solution interface](../symm/LieSymm/scalar2026/SOLUTIONS.md).
Full Eulerian SV+bed E and advectively corrected scalar M remain separate
objects. Neither is silently substituted for the source's printed scalar P.

## 2. Controlled SV+bed changes and a frozen baseline

After the source-paper demonstration, define each experiment from the full
original SV+bed system and change explicitly declared aspects: parameter
strata, constitutive transport/bed closures, variables, initial or boundary
data, geometry and dimension. State which changes are point-equivalent,
which genuinely change the model, and which comparison remains unresolved.

Use the existing LieML implementation as the starting method; do not invent
a replacement generic engine before a concrete failure justifies it. Record
the solver version and the exact change to the model before measuring outcomes.

The local annotated reference
[A Unified Benchmark of Physics-Informed Neural Networks and Kolmogorov-Arnold Networks for Ordinary and Partial Differential Equations](<../ref/A Unified Benchmark of Physics-Informed Neural Networks and Kolmogorov-Arnold Networks for Ordinary and Partial Differential Equations-with-annotations.pdf>)
is selected for **future protocol review**. Its local presence has been checked;
its detailed methods, citation metadata and external results are not established
by this roadmap and must be read/source-checked before adoption.

Benchmark design must distinguish at least:

| Layer | What to test and retain |
|---|---|
| Mathematical structure | Determining identities, invariant rank, parameter strata, first-integral independence and singular branches |
| Representation | Inverse chart, reconstruction, nonzero denominators and compatible data |
| Implementation | Correct/incorrect controls, reproducible failure inputs and supported versus unsupported cases |
| Approximation | Solution error against an independent reference, original-PDE residual, discretization sensitivity and valid interval |
| Cost | CPU time, tolerances, budgets, seeds and repeated-query cost where relevant |

Separate independent-variable reduction from ODE-order reduction. Do not rank
methods with an unproved composite symmetry/nonlinearity score. A timeout or
an unsupported input is not a mathematical obstruction; low residual alone is
not solution accuracy, and fitting a profile is not discovering a first integral.

Use failures to propose falsifiable changes of the method's principles, test
those changes against both positive and negative controls, then freeze the
baseline source, environments, cases, metrics and evidence before the 2D test.
Report the old and improved method side by side rather than comparing against
a moving baseline. No ML benefit or superiority is assumed in advance.

Pure PINN remains stopped. Benchmark study may inform error analysis without
training a PINN. Any later ML component needs a specific unmet task and either
an exactly verifiable structural output or a measured accuracy/cost advantage
over the classical baseline.

## 3. Source-verified open 2D SV+bed targets

Select explicit future-work questions from local and online journal papers.
Before execution, register the source/version, the proposed equation and
closure, geometry, chart, data, parameter domain, known reductions/solutions,
and the precise unresolved question. Re-check the literature before using
"open", "unknown" or "novel" as a research claim. Existing local 2D
classification evidence does not establish that every proposed 2D problem is new.

Apply the frozen baseline and the proposed improvement to the same tasks,
domains, accuracy requirements and CPU budgets. Retain invalid candidates,
no-improvement cases, approximation failures and unresolved singular behaviour
alongside accepted reductions or solutions. A finite search cannot establish
maximal classification or nonexistence.

Only demonstrated recurring structures should motivate geometric/algebraic
iteration: for example orbit-rank changes, distributions and their integrability,
stabilizers of compatible data, quotient charts and independent conservation
identities. State each proposed principle with an explicit domain, falsifiable
prediction and counterexample/control, rather than claiming that numerical
patterns already form an abstract theory. These results and limits feed the
dissertation's future-work and conclusion sections.

## Acceptance and provenance

The unavailable 11 October external archive is a nonblocking historical
provenance gap. Preserve its existing receipt; archive recovery is not a task
or acceptance gate for this route. Do not rewrite old failed audits as passes.

Current research acceptance still requires its own available sources, code,
data, exact certificates where claimed, independent reconstruction checks,
negative controls and fresh run receipts. Historical evidence is never mixed
with new results to turn a failed check green. Registered-family coverage,
model-branch coverage and actual-solution coverage remain separate quantities.
