# Dissertation title inspection

Date: 2026-10-14. Scope: wording and alignment with the current evidence;
this inspection does not change the dissertation cover or declare new results.

## Supplied title and clarified meaning

> Lie analysis of Processed (2+1)-dimensional parameter-Shallow-water equations
> with Exner-Bed Evolution and analytic solutions through machine learning

The author clarified that "Processed" means transformed or nondimensionalized
equations. The intended research subject remains the parameter-dependent
coupled (2+1)-dimensional shallow-water/Exner system, including general
transport exponents rather than an exclusive m=3 study.

## Recommended title

**Lie Symmetry Analysis of Parameter-Dependent (2+1)-Dimensional
Saint–Venant–Exner Equations: Analytical Reduction and Machine-Learning-Assisted
Solution Construction**

This retains the intended model, dimension, parameter dependence, Lie methods,
analytical work and machine learning. It does not imply that an approximate
neural profile is an exact PDE solution. It is a proposed dissertation target;
the eventual submitted dissertation must substantiate its components.

## Wording findings

1. **Lie analysis:** use "Lie symmetry analysis" to identify the mathematical
   method explicitly.
2. **Processed:** this is not a precise mathematical formulation. If only
   units are rescaled, use "nondimensionalized" in the model description.
   If coordinates or dependent variables change, name the transformation and
   state its domain, invertibility and reconstruction rules. A transformation
   should appear in the title only if it is central to the contribution.
   Routine nondimensionalization can be stated in the abstract and methodology.
3. **Parameter-Shallow-water:** replace the incomplete compound by
   "parameter-dependent shallow-water equations." Define the actual parameter
   family in the dissertation and separate generic and exceptional strata.
   A cubic example alone does not deliver a general-parameter study.
4. **Exner-Bed Evolution:** use "Exner bed evolution" or the established name
   "Saint–Venant–Exner equations" for the coupled model. The Grass closure and
   friction/forcing assumptions should be explicit in the model definition;
   the title is not evidence that all sediment closures have been studied.
5. **Analytic solutions through machine learning:** this can imply that ML
   supplies exact solutions. A fitted neural profile is usually an
   approximation, even if its activation functions and output are analytic.
   Exact formulas or convergent analytic constructions require verification
   against the stated equations and their branch/domain conditions.

If exact symbolic discovery is the intended final contribution, the stronger
subtitle **Machine-Learning-Assisted Discovery of Exact Solutions** is a
clear research objective. To substantiate it, identify the learned object
(for example a symmetry, first integral or explicit solution formula), show
that ML actually proposed it, and verify the resulting identities exactly.
Report failures and classical baselines; the wording does not itself imply
a speedup or novelty claim. If ML only approximates reduced profiles, use
**Analytical Reduction and Machine-Learning Approximation** instead.

## Current evidence and remaining work

- The current dissertation's abstract, lines 64–93, is centered on the scalar
  SVE reproduction and reducer. Lines 82–85 and 255 explicitly state that no
  learned order-reducing object has passed the exact acceptance checks.
- The new 2D package verifies selected generators, a general-m rotational
  quotient, and a completed cubic ODE example. Its report describes a bounded
  initial calculation and leaves a full 2D numerical solver and ML comparison
  as future work.
- The subsequent chat calculation verified the general-m rotation plus common
  space-time scaling substitution with invariant r/t. That branch and its
  singular coefficient cases have not yet been integrated into the saved report.

Consequently the proposed title can guide the final dissertation, but it is
broader than the results currently assembled in the manuscript. The remaining
central deliverables are a substantive general-m 2D analysis and an explicitly
defined, evaluated ML contribution. No full classification or exact learned
solution result is inferred from the existing cubic example.

Inspected sources:

- [Dissertation](<D:/MATHs/math 4890 LieML/draft/dissertation.tex:64>)
- [Main manuscript](<D:/MATHs/math 4890 LieML/draft/main.tex:34>)
- [Project map](<D:/MATHs/math 4890 LieML/docs/project-map.md:1>)
- [Current experiment index](<D:/MATHs/math 4890 LieML/research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md:1>)
- [2D extension report](<D:/MATHs/math 4890 LieML/research_artifacts/SVE-2D-extension-20261014/report.tex:16>)

Verification was a source inspection. No manuscript, bibliography, executable
or scientific claim was changed, so compilation and computational regression
tests were not needed for this title review.
