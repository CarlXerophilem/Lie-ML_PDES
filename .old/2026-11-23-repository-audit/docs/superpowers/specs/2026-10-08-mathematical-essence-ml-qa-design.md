# Design specification: mathematical machine learning for Lie-reduced PDEs

**Date:** 2026-10-08
**Target document:** `docs/The Mathematical Essence of Machine Learning.md`
**Companion research manuscript:** `draft/main.tex`

## 1. Purpose

Rewrite the target document as a formal, readable, and mathematically careful Q&A for a researcher who understands semi-analytical PDE reduction but has limited familiarity with machine learning and wants to know precisely where a PINN or related learned model belongs in a Lie-symmetry workflow.

The revision is not a sentence-level copyedit. It is a conceptual reconstruction that preserves the useful mathematical content and Q&A format while correcting clear errors, repairing notation, adding the missing Lie–ML interfaces, and imposing an explicit boundary on the global research scope.

The central thesis is:

> Machine learning does not replace Lie symmetry analysis. Lie theory determines whether and how the PDE can be reduced; analysis determines what is already known about the reduced problem; machine learning is then an optional approximation mechanism for the remaining unknown map. The learned object may be a reduced profile, an analytical remainder, or a parameter-to-profile operator. If exact reduction fails, a full-space or softly symmetry-constrained model is a fallback rather than evidence for the core reduction method.

The target document must answer three practical questions throughout:

1. **What is the mathematical object being learned?**
2. **At what stage of PDE reduction is it learned?**
3. **What evidence would establish that learning added value?**

## 2. Intended reader and explanatory standard

The intended reader is a researcher working on semi-analytical PDE reduction who knows differential equations and some Lie-symmetry machinery but does not yet know the conceptual organization of machine learning, PINNs, or equivariant architectures.

Accordingly, the rewrite must:

- introduce an object intuitively before formalizing it;
- distinguish labelled-data learning from residual-based PINN training;
- use one recurring PDE-reduction notation rather than changing symbols between answers;
- explain each advanced construction in terms of its role in the pipeline;
- include concrete small examples where they clarify an otherwise abstract distinction;
- avoid assuming that neural networks, probability distributions, or compact-group representation theory are universal prerequisites;
- state limitations and failed logical implications explicitly;
- preserve enough mathematical detail to support later research use.

The prose should be formal but not compressed. A technical term should not appear merely to signal sophistication: it should either be defined, used in a later argument, or omitted.

## 3. Editorial architecture

The revised Q&A will be cumulative rather than a sequence of four largely independent essays. Its order is deliberately asymmetric: the reader first receives a self-contained mathematical account of machine learning without Lie theory, PDE symmetry, or PINN-specific notation; only afterward does the document construct the ML–Lie interface. Later answers may refer back to the pure-ML objects, but Part I must not presuppose Part II.

### Part I. Machine learning on its own

### Q1. What is the mathematical essence of machine learning?

Define learning broadly as selecting or approximating an unknown function, operator, distribution, parameter, or decision rule from incomplete information under a specified criterion. Introduce population risk and empirical risk as the standard statistical case, but do not claim that all machine learning is literally an ill-posed inverse problem over a probability space.

Separate five sources of difficulty:

- incomplete information;
- restricted representation;
- finite or biased sampling;
- optimization error;
- validation under a declared target distribution.

Explain the approximation–estimation–optimization decomposition only under assumptions for which it is meaningful. State explicitly that the conditional expectation is the Bayes predictor for squared loss, not for every loss.

### Q2. What are the fundamental components of a learning problem?

Use a complete problem specification rather than the current underspecified five-tuple. A suitable organizing object is

\[
\mathfrak L=(\mathcal Z,P,\mathcal H,\ell,\Omega,\mathsf{Alg},\mathsf{Val}),
\]

where:

- \(\mathcal Z\) is the observation or query space;
- \(P\) is a data-generating or sampling measure when one is present;
- \(\mathcal H\) is the hypothesis class;
- \(\ell\) defines the discrepancy or decision cost;
- \(\Omega\) is an explicit regularizer or structural constraint;
- \(\mathsf{Alg}\) is the search or optimization procedure;
- \(\mathsf{Val}\) is the validation or evaluation rule.

Clarify in ordinary ML terms that these entries are not independent. The observation space and data law constrain which hypotheses are meaningful; the hypothesis class and regularizer determine representational and inductive bias; the loss determines which discrepancies matter; the parameterization and optimizer determine which candidates are reachable in practice; and the validation rule determines what counts as success. Keep this explanation self-contained and illustrate it with an ordinary supervised-learning example.

### Q3. Is a neural network necessary?

Answer no. Within ordinary machine learning, compare neural networks with linear and generalized-linear models, decision trees and ensembles, nearest-neighbor methods, kernel methods, Gaussian processes, splines, and other basis expansions. Explain that these choices encode different assumptions about smoothness, locality, compositionality, invariance, uncertainty, and computational scaling.

Present a neural network as one parameterized hypothesis class. It is justified only if it provides a measurable benefit, such as approximation of a complicated function family, reusable representation learning, differentiation through a surrogate, or useful performance under a matched computational budget.

Close with a general model-selection rule: prefer the simplest hypothesis class and optimization method that meet the declared accuracy, generalization, interpretability, and cost requirements.

### Q4. How do representation, loss, regularization, optimization, and validation interact?

Explain the coupled structure of a learning system through one elementary supervised example. The answer must show that changing one component changes the meaning or behavior of the others: a loss selects a target functional of the conditional distribution; a restricted hypothesis class introduces approximation bias; regularization changes the effective class; the parameterization and optimizer introduce explicit or implicit search bias; and validation estimates only performance under its declared sampling assumptions.

Distinguish population risk, empirical or training objective, validation criterion, and computational optimization error. Introduce the schematic decomposition

\[
\text{total performance gap}
=\text{approximation} + \text{estimation} + \text{optimization}
\]

only with the warning that an exact additive identity requires a specified setup and that the terms may instead be controlled by inequalities. End by showing how these terms jointly explain underfitting, overfitting, and failure to optimize.

### Q5. What can ordinary machine learning establish, and what remains unproved?

Distinguish training fit, held-out predictive performance, distributional generalization, calibration or uncertainty statements, and formal guarantees. Explain distribution shift, identifiability, and the fact that success under one validation distribution need not transfer to another. End Part I with a compact pure-ML decision rule covering target, data, hypothesis class, objective, optimizer, and validation.

### Part II. Machine learning combined with PDEs and Lie reduction

### Q6. What changes when the governing object is a PDE rather than a labelled dataset?

Introduce the full PDE problem

\[
\mathcal P_\lambda=(\mathscr O,\Delta_\lambda,\mathcal B_\lambda,
\mathcal C_\lambda,\mathcal D_\lambda),
\]

where \(\mathscr O\) is the physical domain, \(\Delta_\lambda=0\) the PDE system, \(\mathcal B_\lambda=0\) the initial/boundary/interface/asymptotic data, \(\mathcal C_\lambda\) the admissibility and branch conditions, and \(\mathcal D_\lambda\) the parameter and data family of interest. This notation keeps the ML regularizer \(\Omega\), optimization algorithm \(\mathsf{Alg}\), and PDE-domain/admissibility objects distinct.

Explain that PINN training may use collocation coordinates without labelled solution values. The operator residual and data residual then define the objective. The collocation measure is a numerical design choice, not part of the exact definition of a PDE symmetry.

Compare the resulting PINN with finite-element, spectral, finite-difference, finite-volume, shooting, and direct ODE-solver alternatives as appropriate to the problem. State the key negative decision rule here: if one low-dimensional reduced ODE is solved faster and more accurately by a conventional integrator, a PINN has no demonstrated one-query computational advantage. Repeated parameter queries, inverse estimation, or differentiable amortization require separate evidence.

### Q7. What does Lie symmetry reduction accomplish before machine learning begins?

First define the notation. Let \(x=(x^1,\ldots,x^p)\) denote the independent variables and \(u=(u^1,\ldots,u^q)\) the dependent fields. A point-symmetry generator is

\[
X=\xi^i(x,u)\frac{\partial}{\partial x^i}
 +\eta^\alpha(x,u)\frac{\partial}{\partial u^\alpha},
\]

with summation over the independent-variable index \(i\) and field-component index \(\alpha\). Define

\[
Q^\alpha[j^1u]
:=\eta^\alpha(x,u)-\xi^i(x,u)u_i^\alpha,
\qquad
u_i^\alpha:=\frac{\partial u^\alpha}{\partial x^i}.
\]

Call \(Q=(Q^1,\ldots,Q^q)\) the **characteristic** of \(X\). The vertical generalized vector field

\[
\mathbf v_Q=\sum_{\alpha=1}^{q}Q^\alpha\frac{\partial}{\partial u^\alpha}
\]

is the associated **evolutionary representative**. Explain clause by clause: \(\eta^\alpha\) is the direct infinitesimal change of field component \(u^\alpha\); \(\xi^iu_i^\alpha\) is the induced change arising from movement of the independent variables; their difference is the field variation at fixed base coordinates. Include the scalar translation example \(X=\partial_x\), for which \(Q=-u_x\), so \(Q=0\) selects fields independent of \(x\).

Then distinguish equation symmetry from invariance of a particular solution graph:

\[
\left.\operatorname{pr}^{(n)}X(\Delta)\right|_{\Delta=0}=0,
\qquad
Q^\alpha[j^1u]=0\quad(\alpha=1,\ldots,q).
\]

The first condition says that the transformation maps solutions to solutions. The second is the invariant-surface condition selecting solution graphs fixed by the chosen subgroup. Neither replaces the other, and the second must not be described as a general definition of equivariance.

Explain orbit rank, invariant coordinates, the quotient problem, the reduced profile \(F\), and the reconstruction map \(u=\mathcal T_HF\). Emphasize that reduction describes an invariant solution family rather than every solution of the original PDE.

### Q8. Under what conditions does a PDE problem belong to the research program?

Present the research-scope and admissibility contract from Sections 5–8 below. This question must appear early enough that later ML options are not mistaken for universally admissible operations.

### Q9. Where exactly can machine learning enter the Lie-reduction pipeline?

Distinguish four principal sockets:

1. a full-space model \(u_\theta(x)\);
2. a reduced profile model \(F_\theta(z)\);
3. an analytical-remainder model
   \[
   \widehat F_\theta(z)=F_{\mathrm{an}}(z)+\omega(z)N_\theta(z);
   \]
4. a parameter-to-profile model or reduced operator
   \[
   (z,\lambda,a)\longmapsto F_{\lambda,a}(z).
   \]

The reduced profile or analytical remainder is the primary socket for the companion manuscript. A full-space PINN is a baseline or fallback. A learned symmetry or learned closure is a different inverse problem and must not be silently identified with solution approximation.

### Q10. How does Lie reduction transform every component of the learning problem?

This is the principal interaction section. Explain the transformation

\[
(x,u,\Delta,\mathcal B,P,\mathcal H)
\longmapsto
(z,F,\mathcal R,\overline{\mathcal B},\overline P,
\mathcal H_{\mathrm{red}}).
\]

Reduction changes more than input dimension. It changes:

- the independent variables;
- the admissible profile family;
- the differential operator and its order or constraints;
- the initial and boundary data;
- the collocation domain and measure;
- the meaning of regularization;
- the reconstruction map;
- the interpretation of profile and physical-field errors.

Where possible, connect this section explicitly to the sequence used in `draft/main.tex`:

\[
\text{verified symmetry}
\to\text{reduced equation}
\to\text{analytical profile}
\to\text{neural correction}
\to\text{reconstruction}
\to\text{original-PDE check}.
\]

### Q11. How do geometry, data, loss, architecture, and optimization constrain one another?

Make the dependencies explicit rather than listing components independently:

- symmetry and chart determine reduced coordinates;
- reduced differential order determines required network differentiability;
- data geometry determines whether a symmetry reduction is admissible;
- boundary/initial conditions determine whether constraints can be imposed exactly by the trial function;
- residual normalization and term weights influence conditioning;
- architecture and optimizer jointly induce an implicit bias;
- singular orbits and parameter strata restrict where one network may be shared;
- reconstruction may amplify a small profile error;
- a small sampled residual implies a solution-error bound only with stability and norm control.

Include at least one concrete worked comparison between a direct PDE PINN and a reduced-profile PINN.

### Q12. Which components can be tuned, replaced, or generalized?

Retain the useful breadth of the current answer, but organize it around mathematically distinct choices: domain/observation geometry, sampling, hypotheses, discrepancy, regularization, optimization, and validation.

Correct the geometry. A group orbit \(G\!\cdot\!x\), a homogeneous space \(G/H\), and an orbit space \(M/G\) are different objects. Quotienting by a symmetry requires suitable regularity, rank, transversality, and data compatibility. Do not describe an observation space as being replaced by “diffeomorphic Lie-group orbits” without specifying the action and quotient construction.

### Q13. What is the difference between invariant reduction, equivariant architecture, and symmetry regularization?

Separate three strategies:

1. **Invariant-solution reduction:** impose \(Q=0\) and solve on a quotient;
2. **Equivariant architecture:** retain the full domain but impose
   \[
   \Phi(\rho_{\mathrm{in}}(g)x)
   =\rho_{\mathrm{out}}(g)\Phi(x);
   \]
3. **Symmetry loss or augmentation:** encourage a transformation law through sampled penalties or transformed data.

State what each strategy guarantees and does not guarantee. Exact reduction and equivariant learning are not interchangeable.

### Q14. What does compact-group representation theory contribute, and where does it not apply?

Retain a corrected, more focused explanation of Peter–Weyl theory, isotypic decomposition, Schur intertwiners, group convolution, and Clebsch–Gordan constructions. Tie each construction to equivariant feature maps rather than presenting it as the universal basis of machine learning.

State prominently that many PDE point-symmetry groups central to reduction—translations, scalings, boosts, and affine groups—are noncompact. Peter–Weyl theory for compact groups therefore cannot be applied indiscriminately to the companion manuscript's symmetry algebra.

### Q15. What can be certified after training?

Distinguish:

\[
\text{training loss},\quad
\text{held-out residual},\quad
\text{profile error},\quad
\text{reconstructed PDE residual},\quad
\text{solution-error bound}.
\]

Explain the missing implications. A deterministic solution-error certificate requires a suitable stability estimate, controlled quadrature or residual norm, admissible data, and a bounded reconstruction map. Training success alone is empirical evidence, not a theorem.

### Q16. What workflow is recommended for the present project?

End with the decision sequence

\[
\boxed{
\text{specify}
\to\text{classify or verify}
\to\text{reduce}
\to\text{analyze}
\to\text{learn only the unresolved part}
\to\text{reconstruct}
\to\text{verify}
}.
\]

Include explicit fallback branches when classification, data compatibility, reduction, certification, or ML value fails.

## 4. Four interacting layers

The answers will repeatedly distinguish four layers.

### 4.1 Exact geometric layer

This layer contains the equation manifold, declared symmetry class, infinitesimal generators, prolongation, group orbits, invariant-surface conditions, quotient variables, reduced equations, and reconstruction map.

No training procedure is allowed to replace an unverified exact identity at this layer while the result is still labelled exact.

### 4.2 Analytical layer

This layer contains well-posedness assumptions, first integrals, local series, asymptotics, semi-analytical approximations, admissible data, regularity, stability, and conventional numerical references.

An analytical approximation must carry a declared domain and error status. A formal local series is not automatically a global approximation.

### 4.3 Learned numerical layer

This layer contains the network or other parameterization, collocation and labelled data, residual and data losses, regularization, normalization, optimization, parameter conditioning, and random-seed variation.

The learned component should be identified precisely: full field, reduced profile, analytical remainder, operator, closure, or symmetry candidate.

### 4.4 Certification layer

This layer contains independent reduced and original-PDE residuals, data mismatch, chart and branch guards, reference-solution errors, held-out parameters, stability estimates, reconstruction-error propagation, and computational-cost comparisons.

The document must not conflate a low training objective with certification.

## 5. Symmetry-classification boundary

The rewrite will classify mathematical constructions by their defining contract.

| Class | Defining condition or question | Status in the project |
|---|---|---|
| Exact point symmetry | Does \(\operatorname{pr}^{(n)}X(\Delta)|_{\Delta=0}=0\)? | Primary classification and reduction class. |
| Symmetry of the full data problem | Does the action also preserve the domain, data surfaces, and data residuals? | Required before claiming a reduction of the stated initial-boundary-value problem. |
| Invariant solution | Does a particular graph satisfy \(Q=0\)? | Defines the reduced family; it is not equivalent to equation symmetry. |
| Approximate symmetry | Can \(X_0\) be continued order by order for a genuinely small perturbation? | Conditional branch with explicit defect, order, and validity region. |
| Nonclassical symmetry | Is invariance imposed jointly with \(Q=0\) and its differential consequences? | Secondary branch when classical point symmetries do not yield a useful reduction. |
| Variational symmetry | Is an action preserved up to a divergence? | Used only when Noether currents or conservation laws are relevant. |
| Equivalence transformation | Does the transformation move parameters or constitutive functions within an equation family? | Used in parameter classification, not counted as a symmetry of one fixed PDE. |
| Discrete/global symmetry | Does a finite transformation outside or beyond the identity component preserve the problem? | Tested separately; not inferred from the infinitesimal algebra alone. |
| Generalized/contact/nonlocal symmetry | Does the generator depend on derivatives or nonlocal variables? | Outside the core workflow unless admitted by a separate research gate. |
| Learned or numerical near-symmetry | Does sampled data suggest a candidate generator or low-rank structure? | Discovery aid only until exact or tolerance-explicit verification. |

The phrase **complete classification** may be used only when all of the following are declared:

- transformation class;
- fixed-parameter stratum or equivalence problem;
- regular jet chart and singular branches;
- smoothness class;
- unrestricted determining system and its solution or involutive completion;
- direct verification of the final generators.

A finite polynomial ansatz, numerical SVD, or list recovered at one parameter value is a candidate search, not a maximal classification.

## 6. Reduction-admissibility gates

A verified generator or subgroup enters the core reduction pipeline only after the following gates pass.

1. **Equation-symmetry gate:** every governing equation satisfies the declared infinitesimal invariance condition.
2. **Lie-closure gate:** selected generators close under commutators when a multi-generator subgroup is used.
3. **Regular-orbit gate:** the projected orbit distribution has locally constant rank on the declared stratum.
4. **Transversality gate:** base and total-space orbit ranks permit invariant graphs with the intended number of reduced fields.
5. **Quotient-chart gate:** independent invariants and a locally invertible reconstruction exist; singular orbits and chart boundaries are recorded.
6. **Data-compatibility gate:** the domain and initial, boundary, interface, or asymptotic data descend consistently to the quotient.
7. **Reduced-equation closure gate:** after substitution and the chain rule, orbit-coordinate dependence factors out on the declared nonzero branch:
   \[
   \Delta[\mathcal T_HF]=a(x)\,\mathcal R_H[F],
   \qquad a(x)\neq0.
   \]
8. **Reconstruction gate:** a reduced profile reconstructs an admissible physical field satisfying all sign, branch, regularity, and data conditions.

Failure must have an explicit result: choose another subgroup or chart, retain a higher-dimensional reduced PDE, or use an unreduced conventional or learned solver. The exposition must never force an ODE reduction where the geometry does not support one.

## 7. Classification by quotient dimension

For \(p\) independent variables and projected orbit rank \(\ell\), the regular quotient dimension is

\[
d=p-\ell.
\]

Classify the generic reduced problem as follows:

- \(d=0\): algebraic or consistency conditions;
- \(d=1\): an ODE or differential-algebraic profile problem;
- \(d\ge2\): a reduced PDE, possibly with constraints;
- rank-changing or singular cases: separate local strata outside the regular-chart claim.

The core semi-analytical and reduced-ODE certification program is strongest for \(d=1\). A lower-dimensional PDE may still be valuable but belongs to a different analytical and certification regime.

## 8. Global research classes

Every candidate problem should be assigned to one of four classes.

### Class I: core admissible problem

All essential gates pass:

- an exact or rigorously controlled approximate subgroup is verified;
- the subgroup is compatible with the physical domain and data;
- a regular quotient gives a low-dimensional profile problem, preferably an ODE;
- the reduced family is well posed on a declared parameter/data set;
- an exact profile or independently converged reference is available for validation;
- reconstruction and original-equation checks are possible.

This class enters the principal **reduce–close–certify–correct** pipeline.

### Class II: conditional extension

The problem may enter a secondary branch if one of the following is justified:

- approximate symmetry for a controlled small parameter;
- nonclassical reduction with a compatible invariant-surface system;
- a useful reduced PDE rather than an ODE;
- a reduced operator learned for repeated parameter or forcing queries;
- several local quotient charts patched across a regular family.

Each extension must state its additional assumptions, truncation order where applicable, validity region, and failure criterion.

### Class III: baseline or fallback problem

The construction is retained for comparison rather than claimed as the core method. Examples include:

- a conventional reduced ODE solver;
- a full-space PINN;
- a reduced PINN without an analytical prior;
- an analytical approximation without neural correction;
- a symmetry-loss or augmentation method;
- a finite-element, spectral, finite-difference, or finite-volume reference method.

A learned method is promoted only if it improves a declared quantity at a matched standard: accuracy, repeated-query cost, robustness, access to a parameterized family, or another predeclared objective.

### Class IV: outside the present scope

The core method makes no general coverage claim for problems with:

- no useful symmetry compatible with the actual data and geometry;
- turbulent or fully three-dimensional dynamics without a justified reduction;
- shocks or discontinuities treated only by pointwise strong-form residuals;
- stiffness or multiscale structure that fails the declared analytical and training gates;
- free boundaries or topology changes absent from the reduction model;
- strongly broken symmetry presented as a small perturbation;
- singular orbit strata hidden by division or an invalid quotient;
- only a small sampled residual and no independent stability, solution, or reconstruction evidence.

These may motivate later research but are not successes of the core framework.

## 9. Classification of the machine-learning role

The revised document will label the learned object explicitly.

| ML role | Learned object | Project classification |
|---|---|---|
| Reduced-profile approximation | \(F(z)\) | Primary admissible socket. |
| Analytical-remainder correction | \(C_\theta\) in \(F_{\mathrm{an}}+\omega C_\theta\) | Preferred when a useful analytical prior exists. |
| Reduced solution operator | \((z,\lambda,a)\mapsto F_{\lambda,a}(z)\) | Admissible for repeated parameter/data queries. |
| Full-space PINN | \(u(x)\) | Baseline or fallback. |
| Equivariant full-space model | A map satisfying a group-intertwining law | Conditional alternative when quotient reduction is undesirable or unavailable. |
| Symmetry discovery | Candidate generators or algebraic structure | Exploratory until exact verification. |
| Closure learning | An unresolved constitutive or reduced term | Separate inverse problem requiring identifiability and data assumptions. |

The prose must not confuse learning a solution, learning an analytical remainder, learning an operator, learning a closure, and learning a symmetry.

## 10. Evidence-status vocabulary

Use the following labels consistently:

- **Exact:** proved symbolically or analytically under stated assumptions;
- **Certified:** accompanied by a valid quantitative enclosure or error argument;
- **Conditional:** valid only under explicitly listed regularity, stability, perturbation, or branch assumptions;
- **Numerically verified:** checked independently or against a converged reference without a theorem-level bound;
- **Empirical:** supported by training/validation experiments and seed variation;
- **Candidate:** generated by an ansatz, numerical rank test, or learning procedure but not fully verified;
- **Unsupported/out of scope:** missing a necessary gate.

The document must preserve the implication warning

\[
\text{small training loss}
\not\Rightarrow
\text{small profile error}
\not\Rightarrow
\text{small physical-field error}
\]

without additional stability and reconstruction control.

## 11. Mathematical corrections required in the source

The rewrite must correct, not merely rephrase, the following issues.

1. Do not define all machine learning as an ill-posed inverse problem on a probability space.
2. Qualify empirical-risk consistency by the assumptions needed for uniform convergence, approximation, and optimization.
3. State that \(\mathbb E[Y\mid X=x]\) is the Bayes predictor for squared loss, not for arbitrary loss.
4. State the conditions behind any approximation–estimation–optimization decomposition.
5. Do not assert that every finite-sample evaluation problem is discontinuous. Continuity depends on the function-space topology; point evaluation is bounded in an RKHS but not in spaces such as \(L^2\) without added regularity.
6. Do not call an arbitrary Euclidean parameter set a manifold without qualification, or an empirical Fisher matrix a nondegenerate Riemannian metric when it may be singular.
7. Distinguish deterministic mean-field continuity equations from Fokker–Planck equations, which include diffusion.
8. Replace unsupported quantitative claims that equivariance reduces sample complexity “by the volume of the symmetry group” with theorem-specific or qualitative statements.
9. Correct the claim that symplectic preservation alone enforces energy conservation. Hamiltonian structure, the chosen Hamiltonian, and time symmetry must be distinguished.
10. State the hypotheses for the Kantorovich–Rubinstein dual formula and for any Wasserstein claim.
11. Specify the sign convention when relating Dirichlet energy to the Laplace–Beltrami operator.
12. Invoke Banach's fixed-point theorem only for a self-map of a complete metric space with contraction constant strictly below one.
13. Correct nonlinear infinitesimal equivariance to
    \[
    d\Phi_x\bigl(d\rho_{\mathrm{in}}(X)x\bigr)
    =d\rho_{\mathrm{out}}(X)\Phi(x),
    \]
    with the linear intertwiner equation stated as a special case.
14. Use \(\widehat G\) for the unitary dual in Peter–Weyl theory rather than reusing \(G\).
15. Correct Schur's lemma: inequivalent irreducibles have zero intertwiner space; equivalent complex irreducibles have scalar intertwiners.
16. Qualify the group-convolution characterization by the function spaces and operator class. Not every bounded equivariant operator is convolution against an \(L^2\) function.
17. Fix Fourier-transform convention and multiplication order consistently.
18. Do not claim that pointwise nonlinearities always destroy equivariance. They are equivariant for scalar channels under suitable regular actions but generally not for arbitrary nontrivial irreducible feature types.
19. Replace the universal factorization claim for every continuous, polynomial, or analytic equivariant map with the narrower statement that equivariant architectures can be constructed from intertwiners, tensor products, Clebsch–Gordan projections, invariant scalars, and suitable nonlinearities.
20. Explain the compactness limitation before applying Peter–Weyl theory to PDE symmetries.
21. Remove unresolved placeholders such as `[cite: 1, 3]` and `[cite: 2]`. Any retained external claim must receive a verified source or be rewritten as a definition/derivation not requiring that citation.
22. Repair all malformed copied mathematics using standard Markdown display or inline LaTeX.
23. Correct spelling, inconsistent capitalization, undefined symbols, and abrupt transitions.

## 12. Notation and formatting policy

Use standard Markdown with LaTeX delimiters:

- inline mathematics: `$...$`;
- displayed mathematics: `$$...$$` or the repository's renderer-compatible equivalent;
- no copied Unicode artifacts or broken subscript ordering;
- define every symbol before first use;
- use \(\mathcal H\) consistently for the hypothesis class and \(H\) for a Lie subgroup only when both occur in the same discussion;
- use \(\mathsf{Alg}\) for the ML search/optimization algorithm, \(\mathsf{Val}\) for its validation rule, \(\mathscr O\) for the physical PDE domain, and \(\mathcal C_\lambda\) for PDE admissibility conditions;
- distinguish the true distribution \(P\), empirical measure \(P_n\), and numerical collocation measure;
- distinguish physical parameters \(\lambda\), group parameters, network parameters \(\theta\), and integration/data parameters \(a\);
- use “neural network,” “PINN,” “equivariant model,” and “neural operator” only for their specific meanings.

Each Q&A entry should have:

1. the question as a heading;
2. a one-paragraph direct answer;
3. the necessary mathematical development;
4. a limitation or decision rule when the construction is conditional;
5. in Part II only, a short “Implication for Lie-reduced PDEs” paragraph or callout where useful.

Part I must stand independently as a pure-ML primer. It must not interrupt each foundational answer with Lie terminology or foreshadowing that requires the reader to understand Part II.

## 13. Citation policy

This editorial task is not a new literature review. Use only sources already verified in the companion manuscript or project corpus unless a new claim genuinely requires external checking.

For all literature-dependent claims in the rewritten Q&A:

- verify the cited source before treating it as final;
- mark citations according to the project's verified/unverified convention during drafting;
- prefer named results with narrow claims over broad historical assertions;
- do not invent bibliographic metadata;
- remove citation placeholders that cannot be resolved;
- distinguish a standard theorem used in a derivation from an empirical performance claim requiring a paper.

The Q&A should remain intelligible without turning into an annotated bibliography.

## 14. Relationship to `draft/main.tex`

The Q&A is an explanatory companion, not a duplicate of the manuscript. It should align with these manuscript commitments:

- exact geometry precedes learning;
- equation symmetry and invariant graphs are distinct;
- boundary and initial data compatibility is a separate gate;
- the primary learned object is a reduced profile or analytical remainder;
- reconstruction returns the approximation to the original variables;
- independent original-equation checks are mandatory;
- profile error and residual ranking may disagree;
- a conventional ODE integrator may outperform neural training for a single query;
- parameter-family amortization is a more plausible ML benefit than one-shot solution speed;
- near-exceptional parameter continuation requires a symmetry-defect calculation rather than an assumed invariant ansatz.

The Q&A may cite sections or equations from `draft/main.tex` informally, but it must be self-contained enough to read first.

## 15. Scope statement to appear in the rewritten document

The final Q&A will contain a polished version of this statement near the beginning and return to it in the concluding decision table:

> The global research program concerns automated and verifiable semi-analytical approximation for parameter-dependent PDE problems that admit a useful, data-compatible symmetry reduction on a declared regular stratum. Its primary object is the reduced profile family, not an arbitrary black-box approximation of the original PDE. Machine learning is introduced only where analysis leaves a quantitatively identified unresolved component or where repeated queries justify amortizing the reduced solver. Problems without an admissible reduction remain legitimate baselines or future extensions, but they are not evidence for the core method.

## 16. Verification criteria for the rewrite

The revision is complete only if all of the following checks pass.

### Structural checks

- The document remains a Q&A.
- All sixteen questions form a progressive argument: Q1–Q5 establish pure ML before Q6–Q16 introduce PDEs, Lie reduction, and their interactions.
- Part I contains no unexplained Lie, symmetry-reduction, PINN, collocation, or PDE-residual concepts.
- The research-scope contract appears before the detailed list of ML–Lie sockets.
- The conclusion gives a concrete decision workflow and fallback paths.

### Mathematical checks

- Every formula is syntactically readable in Markdown.
- The generator coefficients, index ranges, jet notation, characteristic \(Q^\alpha\), and associated evolutionary representative \(\mathbf v_Q\) are defined before the invariant-surface condition is used.
- The error list in Section 11 has been addressed.
- Compact and noncompact group cases are not conflated.
- Equation symmetry, invariant solutions, equivariant architectures, and soft symmetry penalties are distinguished.
- Boundary/data compatibility and quotient regularity are explicit gates.
- No small-residual-to-small-error implication is asserted without stability assumptions.

### Audience checks

- A PDE researcher can locate exactly where a PINN enters the pipeline.
- The reader can distinguish what is exact, analytical, learned, and certified.
- The reader can tell when not to use a neural method.
- New advanced terms are motivated and defined.

### Consistency checks against the manuscript

- Symbols do not contradict the established manuscript notation without explanation.
- The reduced-profile and analytical-remainder sockets agree with the construction in `draft/main.tex`.
- The scope does not exceed the manuscript's stated regular-chart, data-compatible, certificate-gated claims.
- Negative results and fallback branches remain explicit.

### File checks

- Search finds no unfinished-work markers, unresolved citation placeholders, malformed copied equations, or misspellings of “necessary.”
- Markdown headings and tables render coherently.
- The final diff is confined to the target Q&A and any separately approved supporting citation changes.

## 17. Non-goals

This revision will not:

- claim a new theorem about all machine learning;
- provide a maximal classification of the SVE equation;
- prove general PINN convergence;
- claim that Peter–Weyl theory handles noncompact PDE symmetry groups without additional machinery;
- turn the Q&A into a full literature survey;
- duplicate the implementation record or all numerical tables from `draft/main.tex`;
- claim ML speedup where the existing evidence does not support it;
- broaden the project into a general nonlinear PDE solver.

## 18. Deliverable

The implementation phase will replace the current target document with a formal, self-contained Q&A following this specification. The resulting file should function as a conceptual entry point to the LieML research program and as a precise map of where machine learning can—and cannot—be inserted into symmetry-based semi-analytical PDE reduction.
