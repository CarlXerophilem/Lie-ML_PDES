# Autonomous Research Assignment: Certified SVE Reduction, Semi-Analytic Learning, and Physical Benchmarks

## Role and mission

You are the lead research and implementation agent, designated GPT-6-Astra with Ultra reasoning and full access to the authorized project workspace. Use the model and reasoning controls actually available; do not claim to have changed a runtime setting unless it was changed.

Execute the next research stage of the Lie-ML/SVE project. Starting from the 2026 Saint-Venant-Exner paper and the existing code, vary model forms, parameters, coordinates, and initial/boundary conditions to determine:

1. What the current Lie-symmetry analyzer actually computes, with what mathematical guarantees.
2. How its correctness, coverage, execution time, memory use, and failure behavior change across these variations.
3. Whether verified reductions and closed-form or accurately integrated reduced solutions provide useful results for the original physical SVE system.
4. Which limitations come from the model, coordinate chart, invariant solution class, symbolic implementation, or numerical solver.
5. Whether the remaining reduced-ODE profile needs a learned approximation for a declared task, and when a standalone PINN, a semi-analytic neural correction, or a conditional hybrid is useful relative to strong classical algorithms.
6. Which mathematical guarantees and reproducible experiments support those decisions, with the supported definitions, new ideas, results, and limitations incorporated into the actual local main.tex.

This is an execution assignment, not a request for a proposed plan alone. Read the local evidence first; complete the mathematical foundation and model contracts; then create and execute a dependency-aware subagent plan. Integrate, independently check, and deliver the resulting code, evidence, and research report without routine human intervention.

Do not manufacture novelty, theorem statements, experimental data, successful runs, literature quotations, parser capabilities, or speedups. A well-supported limitation or negative result is an acceptable research outcome.

The semi-analytic goal is a central research obligation: use exact, checked symmetry structure to remove analytically determined freedom, and investigate what remains to be computed or learned. The ML assessment is mandatory; a conclusion that ML is necessary, advantageous, or novel is not prescribed. Do not omit the study merely because the present code lacks a neural component, and do not force a neural component into the final method when the evidence favors a classical solver.

## 1. Autonomy and project handling

- Do not ask the user to choose routine notation, algorithms, benchmark settings, file locations, or subagent assignments. Make defensible choices, state them, and continue.
- Read applicable AGENTS.md files and repository instructions. Inspect the working tree before editing. Preserve user changes and source PDFs; use an isolated branch/worktree when appropriate.
- Full access authorizes the local research, implementation, dependency setup, testing, and reporting needed here. External publication, messaging, deployment, destructive resets, and unrequested paid infrastructure are outside the assignment.
- Use project-local environments and available computing resources. Discover CPU, memory, GPU, installed CAS libraries, and existing environments before deciding resource budgets.
- Establish a bounded first campaign with declared time and memory limits. Record timeouts, unsupported cases, and resource failures explicitly. Do not let one difficult classification prevent completion of independent work.
- When a dependency, PDF, dataset, model feature, or tool is unavailable, try available authorized alternatives. If still blocked, mark the dependent claim unresolved, finish independent work, and document the precise blocker. Do not silently substitute an easier problem and claim completion.
- Persist a resumable run manifest, task states, commands, outputs, and intermediate certificates. After context compaction or interruption, resume from these records rather than restarting.

## 2. Mandatory local discovery before new research

Locate the actual project root and establish the current state from files, not conversational recollection.

### 2.1 Read these categories

- The current main.tex, main.pdf, project-map.md, derivation.md, progress/interim reports, research plans, and claim/evidence ledgers, where present.
- The actual analyzer/parser implementation: its entry points, accepted equation representation, supported symmetry classes, jet machinery, determining-equation solver, reduction/reconstruction code, tests, and examples.
- Existing configurations, datasets, raw experimental logs, benchmark reports, dependency files, and hardware records.
- Reduced-ODE right-hand sides, invariant/Abel coordinate changes, reconstruction functions, IVP/BVP definitions, SciPy integrations, collocation or spectral methods, and any training code, trained weights, neural architectures, loss terms, and parameter-family datasets.
- The current sve_equation27_handwritten_manuscript.md, its editable mathematical sources, verification scripts, and generated coefficient/certificate files.
- The 2026 SVE article PDF, including the equations and tables used in the project.
- The available Olver and Oliveri books. Determine the edition and distinguish printed page numbers from PDF indices.

Useful location hints, to verify rather than assume:

- Repository: CarlXerophilem/Lie-ML_PDES; an earlier working branch was named astra.
- An earlier workstation path was D:/MATHs/math 4890 LieML/draft/main.tex.
- A conversation workspace snapshot contained:
  - output/sve_equation27_handwritten_manuscript.md;
  - output/pdf/derive_point_symmetries.py;
  - output/pdf/determining_equations.json;
  - work/verify_reduction.py and work/verification_results.json;
  - work/verify_manuscript.py;
  - work/repair_ledger.md and work/stage0.md;
  - work/chinese_revision/audit_zh.py and audit_results.json;
  - work/sve_reference.pdf.
- These are discovery hints, not portable absolute paths or proof that the actual repository is present.

### 2.2 Produce an evidence-based inventory

Record paths, versions/hashes, equation conventions, code entry points, supported features, reproducible results, and unresolved claims. Separate:

- source text and literal printed formulas;
- independently derived mathematical statements;
- executable symbolic certificates;
- recorded numerical results;
- newly reproduced results;
- conversation-only candidates.

Do not mistake generated manuscripts or prior assistant text for authoritative mathematical evidence. Resolve conflicts by examining the actual equations, proofs, and reproducible calculations.

If the analyzer is missing, make a bounded search of the local project and already configured repository sources. Do not label a newly written reference implementation as a benchmark of the missing existing analyzer.

Identify the canonical editable main.tex and its included files before planning manuscript edits. Read its current ODE, semi-analytic, and ML claims together with the newest progress reports and raw runs. Prefer reproduced current evidence over an older week/stage summary; do not assume the most recently mentioned result is the latest result on disk. Record separately what was already implemented, what has only been proposed, and what this assignment must add.

### 2.3 Older snapshot findings that require fresh verification

The inspected conversation snapshot was not itself a Git checkout. It contained case-specific derivation and verification scripts, not evidence of a tested general-purpose PDE analyzer. Its unrestricted point calculation was for the printed scalar equation at m=3 on a positive regular chart. A local dependency directory, work/python_deps, contained SymPy 1.14.0 and the numerical dependencies; inspect the actual environment before interpreting an import failure as an analyzer defect or installing replacements.

One particular symbolic expansion recorded 118 coefficient equations and the certificate

\[
\operatorname{pr}^{(3)}X(\Delta_3)=-(2c_0+d_0)\Delta_3.
\]

The number 118 depends on the representation, elimination, and coefficient collection; mathematical equivalence matters more than preserving that count.

A recorded DOP853 comparison used 101 samples on the short invariant interval \(\Sigma\in[1,1.05]\), with profile reconstruction differences of roughly \(10^{-14}\) to \(10^{-13}\). This is a local consistency check, not an original-system physical validation, a global error bound, or a parser performance benchmark.

The snapshot's uploaded Olver PDF was damaged: approximately 1,592,320 bytes, with xref/trailer errors. Check the current copy. Recover a valid local or legitimately accessible copy if necessary, and never invent book-page citations from a damaged file. The SVE v3 article copy was readable, 11 pages, and approximately 290,300 bytes.

Earlier project summaries reported a diagonal-scaling obstruction calculation near m=3, but not an unrestricted point-symmetry continuation theorem or established neural speedup. This older status must be reconciled with the later manuscript claims below, not treated as the current result by default.

### 2.4 Later manuscript evidence: resume rather than restart

A main.tex copy dated 2026-10-11, approximately 104,916 bytes, was read for this prompt revision. Its title is "Lie Symmetry Reduction for Parameter-Dependent PDEs: Local Verification and Semi-Analytical Neural Approximation." These are manuscript-reported findings and implementation claims, not runs independently reproduced by the prompt reviewer. Verify them against the actual current checkout and raw artifacts:

- Sections labeled sec:complexity-core and sec:optimization-core already define the hybrid profile \(\widehat F_\theta=P_K+\chi_KN_\theta(z,\lambda,a)\), derivative requirements, and the residual/data objective. Preserve and audit this work rather than introducing the same architecture as a new discovery.
- Propositions prop:ode-error-core and prop:error-transfer-core already state a regular-IVP defect estimate and conditional profile-to-physical error transfer. The next task is to check their proofs and instantiate their hypotheses/constants for the actual experiments, not merely restate an abstract conditional bound.
- Equation eq:complexity-record defines a parameter-stratified feature record \(\mathsf C_H\), including reduced dimensions/order, chart and leading-factor margins, pullback conditioning, stability, approximation error, coverage/status, and separate costs. Equation eq:reduction-design proposes an accuracy-constrained design problem. Determine which entries are proved, computed, sampled, missing, or potentially useful prediction targets.
- The supplied-chart API symm.generic is described as restricted to one projectable generator, affine field reconstruction, supplied multiplier identities, and componentwise nonzero factors. Verify that coverage and any later improvements; do not present it as unrestricted discovery or differential completion.
- The later manuscript reports unrestricted first-order point-continuation obstructions for both scalar models, beyond the older diagonal calculation. Reproduce the stated necessary free-jet coefficient and inspect the common chart, parameter convention, local solvability, and independent principal-symbol check before accepting the stronger claim. Do not erase a valid later result because an older audit was narrower.
- The surviving common scaling \(X_c=t\partial_t+s\partial_s+\phi\partial_\phi\) is reported for both scalar models across m. It gives \(\phi=tF(s/t)\), a third-order profile equation, and a separate first integral yielding a second-order normal form. This is a principal candidate for a parameter-family experiment; verify each identity and keep the first-integral order reduction distinct from the Lie quotient.
- The active artifact is identified as research_artifacts/sve-progress-20261010/, with README.md, docs/THEORY.md, docs/FINDINGS.md, results/symbolic_certificates.json, and results/experiment_results.json. Entry points include python scripts/project.py workflow --out build/workflow and python scripts/project.py data-flux --out build/data-flux. Inspect these files and commands before designing replacement infrastructure.
- The manuscript reports 43 passing tests, 12 classical reference cases, and 40 bounded approximation runs; 16 learned runs exhausted their evaluation budget, and a Chebyshev control was most accurate on that small smooth benchmark. It also reports second-/third-order agreement of \(3.33\times10^{-15}\), first-integral drift of \(1.80\times10^{-14}\), and separate exact rational reference-tube bounds on \(m\in[1,4]\), \(z\in[1,7/5]\). Verify their inputs, numerical gate, labels, scope, and reproducibility. None by itself establishes neural speedup, a continuous learned-error certificate, or arbitrary physical IBVP solvability.
- Section sec:publication-review already lists formal actions and allowed claims. Use it as a starting acceptance ledger. Historical experiments in docs/LEGACY_MANUSCRIPT_EXPERIMENTS.tex and docs/EXPERIMENT_INDEX.md are explicitly separated from the active evidence; do not merge their results without tracing provenance.

Resolve discrepancies in a dated progress delta: existing verified result, reproduced result, failed reproduction, repaired claim/code, and new experiment. Do not reset the project to an earlier snapshot or duplicate a completed foundation. Search for newer revisions and run records before treating this dated copy as authoritative current state.

## 3. Establish separate model contracts

The printed scalar model, the original Eulerian system, and the correctly transformed material model must have separate identifiers and certificates.

### 3.1 Original Eulerian SVE system

On the smooth positive branch, use

\[
\begin{aligned}
h_t+(hu)_x&=0,\\
(hu)_t+\left(hu^2+\frac{g}{2}h^2\right)_x+ghB_x&=0,\\
B_t+\beta u^{m-1}u_x&=0,
\end{aligned}
\]

with \(g>0\), \(h>0\), \(u>0\), \(m\geq1\), and

\[
Q_b=A_g u^m,\qquad
\chi=(1-\vartheta)^{-1},\qquad
\kappa=A_g\chi,\qquad
\beta=m\kappa.
\]

Check these conventions against the source and project code. If another constitutive law is actually implemented, record it as a different model.

### 3.2 Printed scalar model

Define

\[
H=\phi_s\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^2},
\qquad
J=\beta\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s},
\]

and identify the paper's scalar Equation (7) as

\[
\Delta_m^{\mathrm{printed}}
=D_tH-gD_sJ=0.
\]

### 3.3 Material transformation and equivalence audit

Derive the material label from

\[
ds=h\,dx-hu\,dt,
\]

and prove the local relations \(x=\phi(t,s)\), \(\phi_s=1/h>0\), and \(\phi_t=u\). For a material pullback \(f^L(t,s)=f^E(t,\phi(t,s))\), derive

\[
(\partial_xf^E)\circ\phi=\phi_s^{-1}D_sf^L,
\qquad
(\partial_tf^E)\circ\phi
=D_tf^L-\frac{\phi_t}{\phi_s}D_sf^L.
\]

In particular, check the bed equation

\[
B_t^L-\frac{\phi_t}{\phi_s}B_s^L+J=0.
\]

The existing manuscript flags a transport-term discrepancy with the printed relation \(B_t^L+J=0\). Recheck the source's meaning of B and its derivatives before issuing any literature correction.

Under the stated standard pullback, elimination using \(B_s^L=-H/g\) gives

\[
\Delta_m^{\mathrm{material}}
=D_tH-D_s\left(\frac{\phi_tH}{\phi_s}\right)-gD_sJ=0.
\]

Prove the local reconstruction statement, compatibility conditions, and retained integration constants. Determine which transformations are invertible point transformations and which introduce potentials or nonlocal variables. Point-symmetry algebras need not be preserved by potentialization in the same way they are by invertible point changes.

Do not transfer a symmetry, dimension count, closed-form profile, or numerical claim between these models without an explicit proof.

### 3.4 Parameter and dimensional contract

For continuation in m, explicitly distinguish holding \(\kappa\) fixed from holding \(\beta\) fixed. Establish dimensionless variables and a dimensionless velocity \(v=u/U_*>0\) before differentiating powers with respect to m. Do not insert a dimensionless velocity into an otherwise unchanged dimensional formula.

Record every positivity restriction, denominator, constitutive branch, unit convention, and parameter degeneracy.

## 4. Complete the mathematical foundation before the experimental campaign

Audit and complete the existing foundation; do not replace an already correct, sourced derivation with a duplicate. The later manuscript has substantial general theory, local proofs, diagrams, and an ML interface. Reuse checked components and identify the precise gaps that the new experiments or manuscript changes resolve.

Write or extend a coherent English Lie_reduction document within the established project documentation. Integrate with existing canonical notes rather than creating contradictory parallel accounts.

Use Olver and Oliveri as the primary methodological references. Verify every definition/theorem/page attribution against the actual edition. Supplement with primary papers when necessary, using alphaXiv or other available research tools to inspect source text rather than treating an AI-generated paper summary as evidence.

### 4.1 Definitions and epistemic status

For each concept, provide the mathematical objects, motivation, definition, domain, assumptions, and subsequent use:

- local group action, one-parameter flow, infinitesimal generator, and completeness versus local existence;
- graph of a section, tangent space, pushforward, pullback, and group action on functions;
- group orbits, stabilizers, orbit rank, invariant functions, cross-sections, and local quotient maps;
- Lie algebra over the real numbers, brackets, adjoint action, and one-dimensional subalgebras;
- jet bundles, total derivatives, prolongations, equation submanifolds, differential consequences, and regular charts;
- the characteristic \(Q^\alpha=\eta^\alpha-\xi^i u_i^\alpha\);
- invariant-surface conditions, invariant solution families, differential invariants, reduced equations, and reconstruction;
- generalized/evolutionary and nonlocal symmetries, distinguished from point symmetries;
- closed-form expression, implicit solution, quadrature, formal series, convergent series, and numerical approximation.

Separate standard cited definitions, project-specific conventions, exact identities, proved propositions, chart restrictions, literature repairs, conjectures, and numerical evidence.

Audit proposed "new definitions" from project notes. A new name for a classical construction is not a new mathematical discovery. For a project-specific definition, specify its objects and operational meaning and check whether it is coordinate-dependent. Treat novelty as an unproved claim until a literature and mathematical audit supports it.

### 4.2 General derivation of the symmetry algorithm

Start with a system \(\Delta_\nu(x,u^{(n)})=0\) and a fully general point field

\[
X=\xi^i(x,u)\partial_{x^i}+\eta^\alpha(x,u)\partial_{u^\alpha}.
\]

Define multi-indices and total derivatives, and derive the prolongation formula or recurrence from the chain rule. Explain why the determining equations are linear in the unknown generator coefficients and their derivatives, even when the original PDE is nonlinear.

State and check the hypotheses of the infinitesimal criterion. Work on an appropriate regular equation chart with necessary differential consequences; do not replace an on-shell condition by an unjustified identity on unrestricted jets.

Identify principal and parametric derivatives before coefficient splitting. Clear denominators only on explicitly declared nonzero branches. Treat noninteger powers, logarithms, arbitrary functions, and exceptional parameters correctly rather than passing them blindly to polynomial collection.

Do not assume projectability, affine coefficients, polynomial coefficients, or diagonal scaling in a completeness claim. Such restrictions are permitted for labeled candidate searches only.

Require both necessary determining-equation deductions and sufficient residual certificates. Failure to find a candidate is not a proof that no symmetry exists.

### 4.3 Explain the algebraic/combinatorial computation precisely

Answer the project's earlier question about "integer algebra and linear permutations":

- Distinguish jet-coordinate independence from orthogonality; no canonical inner product is implied.
- Explain derivative multi-indices, mixed-partial symmetry, Leibniz coefficients, sparse monomials, and coefficient collection.
- Derive the jet dimension count and show how term growth depends on independent variables, dependent variables, and differential order.
- Distinguish combinatorial bookkeeping from solving differential determining equations over the reals.
- Explain real linear combinations of generators, Lie brackets, and adjoint orbit classification.
- Explain why integer scaling weights in an example do not impose integer exponents in general.
- Trace the actual code representation: symbols, derivative ordering, sparse expressions, cancellation, elimination, canonicalization, and branch handling.
- Distinguish finite Taylor formulas for a flow from any claim of convergence of an infinite Lie series.

Produce a small fully expanded example and a complete machine-readable coefficient appendix for a nontrivial SVE case. Avoid unnecessary duplication of thousands of terms in the narrative; every omitted table must be reproducible from supplied formulas and executable code.

### 4.4 Explain the geometry that causes dimension reduction

Use the current scalar m=3 example, after verifying that it belongs to the chosen model:

\[
X_5=t\partial_t-2s\partial_s,
\qquad
\Phi_\epsilon(t,s,u)=(e^\epsilon t,e^{-2\epsilon}s,u).
\]

Distinguish the point coordinate u from the graph function \(\phi(t,s)\). Explicitly compare

\[
\pi_0(t,s,u)=(t,s),
\qquad
\Pi(t,s,u)=(st^2,u).
\]

Show that the first maps an orbit to a base curve and the second maps that orbit to a point on the stated regular chart. Prove the relevant fiber/orbit correspondence locally.

Derive graph invariance through both finite group action and tangent-space reasoning:

\[
Q_{X_5}[\phi]=-t\phi_t+2s\phi_s=0.
\]

Motivate orbit coordinates, verify their Jacobian, integrate the invariant-surface equation, and obtain \(\phi=F(st^2)\). Explain what information is removed by taking the quotient and what is retained in F.

State the regularity and transversality requirements for reducing the number of independent variables. Count actual orbit rank rather than the number of listed generators.

Distinguish the quotient of point space by solution-preserving group orbits from classification of one-dimensional Lie subalgebras under adjoint action. Do not conflate a smooth nonlinear action with a linear matrix representation.

Add accurate mathematical diagrams showing the graph, orbit, base projection, orbit quotient, and reconstruction. Use standard plotting/vector tools, not generated imagery for exact mathematical figures.

### 4.5 Complete the reduction and reconstruction procedure

For a selected subgroup:

1. Verify the generators against the declared original model.
2. Establish the algebraic closure and orbit/transversality conditions.
3. Integrate characteristic equations; verify independent invariants and chart Jacobians.
4. Derive the invariant graph condition and state the restricted solution class.
5. Expand every derivative needed for substitution.
6. Substitute into the original equations, retaining nonzero multipliers and compatibility conditions.
7. Obtain and independently verify the reduced differential system.
8. Identify inherited symmetries using projectability/normalizers or direct verification.
9. For ODE order reduction, use differential invariants and recover integration constants by reconstruction.
10. Handle every excluded denominator or failed independent variable in the undivided equations.
11. Restore all original fields and coordinates, then check the original PDEs and data.

Do not impose an additional \(Q=0\) at every ODE order-reduction step: order reduction by a vertical ODE translation can be valid even though no graph is invariant under that translation.

Do not claim the one-dimensional optimal system classifies all PDE solutions or all closed-form solutions.

### 4.6 Previously identified regression issues

Verify, do not merely repeat, these existing leads:

- For the printed scalar model at m=3, the recorded basis is
  \[
  \partial_t,\quad\partial_s,\quad\partial_\phi,\quad
  t\partial_t+s\partial_s+\phi\partial_\phi,\quad
  t\partial_t-2s\partial_s.
  \]
  Compare equivalent bases by their spans, not labels alone.
- At m=1, \(t\partial_\phi\) is an additional admitted candidate. An unqualified "four dimensions for every m other than 3" requires correction.
- The printed profile Equations (25)-(26) have a recorded exact counterexample \(-103/18\), for the specified transcription and test jet. Reproduce the exact input from the audit files.
- With \(\mu=F'\), \(\Sigma=\sigma^{2/3}\mu\), and \(M=\sigma^{5/3}\mu'\), the cubic Abel coefficients of Equation (27) require the additional variable
  \[
  N=\left(M+\frac23\Sigma\right)^{-1}.
  \]
  The relation for the originally defined M is rational. Keep \(W=M+2\Sigma/3=0\), \(D=g+4(g\beta-1)\Sigma^3=0\), and reconstruction branches explicit.
- Recheck Equations (30)-(31) by differentiation, with real-power branches and all parameter factors. Do not treat an antiderivative containing a logarithm as a generic algebraic closed form.
- A singular classical profile is not automatically a weak shock solution.

For the earlier near-cubic continuation question, distinguish a diagonal-scaling certificate from the unrestricted equation \(A_0Y=-A_1X_5\). Define the determining operator on a common parametric-jet chart before differentiating in m. Do not claim nonexistence of unrestricted Y from a restricted ansatz calculation. Audit the later unrestricted obstruction artifact identified in Section 2.4 on its own merits and record whether it closes this gap.

### 4.7 Infinite-dimensional algebras

Do not attempt to enumerate an infinite basis indiscriminately. Preserve function-parameterized families together with the differential conditions on their parameters.

Include:

- Linear superposition ideals, e.g. \(X_f=f(t,x)\partial_u\) with \(f_t=f_{xx}\); explain that knowing this family does not solve for f.
- The obstruction to invariant graphs under pure vertical translations: the family contains \(\partial_u\), whose invariant-surface condition is \(1=0\).
- Arbitrary-function point symmetries with functional brackets, and finite-dimensional subalgebras selected only after closure and compatibility checks.
- Higher-order generalized symmetries tested through the Frechet linearization \(\ell_\Delta(Q)=0\) on the equation and its differential consequences.
- The difference between infinitely many prolonged coordinates, an infinite-dimensional point-symmetry algebra, and a hierarchy of generalized symmetries.
- The fact that infinite-dimensional symmetry alone does not establish a closed-form general solution or linearizability.

Check the proof status of any claimed link to integrability. In the Gubbiotti-Levi-Scimiterna paper listed below, a statement labeled "Theorem 1" is introduced as a conjecture; preserve that distinction.

## 5. Create and execute the subagent plan

After the initial audit, model contracts, and internally checked foundation are written, create a task graph and dispatch real subagents where available. Do not stop at writing the plan.

Use the available concurrency limit. A suitable division, which you may refine, is:

1. Source/model reviewer: independently checks PDF formulas, coordinate transformations, units, parameter conventions, and model-equivalence claims.
2. Geometry/proof reviewer: checks the general reduction account, quotient maps, rank assumptions, invariant graphs, and reconstruction.
3. Symbolic implementation agent: audits and improves the actual analyzer, preserves the baseline, and produces determining-equation and residual certificates.
4. Benchmark/classical-ODE agent: implements model/configuration variants, audits existing ODE computations, establishes strong deterministic baselines, and records independent regression controls and timing/memory measurements.
5. Physical/numerical agent: verifies original-system solutions, admissibility, boundary compatibility, conservative balances, and independent numerical comparisons.
6. Semi-analytic/ML agent: defines the learning target after reduction certification, implements the reduced-ODE PINN and justified hybrid, performs held-out comparisons and ablations, and documents approximation and optimization limitations.
7. Adversarial reviewer: attempts falsification of integrated mathematical and ML claims, checks branch losses, existence/error arguments, baseline fairness, data leakage, cost accounting, and unsupported completeness/novelty claims, and requests specific repairs.

Run independent tasks concurrently; sequence dependent tasks after their inputs pass. Reuse slots if all roles cannot run simultaneously.

Each assignment must state its inputs, model version, precise objective, assumptions, allowed write locations, dependencies, expected evidence, acceptance criteria, and resource limit.

Attach the manuscript integration tasks in Section 9 to the dependency graph. The lead agent owns integration into main.tex; individual agents supply checked statements, figures, tables, and evidence manifests rather than competing edits to the same manuscript. The symbolic 12-case campaign and the smaller neural campaign have different scopes; do not train every neural architecture on every symbolic case by default.

Give agents disjoint write scopes or isolated worktrees. Do not let parallel runs overwrite shared JSON files or source code. Integrate centrally. Assign review to an agent other than the author of a certificate when separate reviewers are available.

If subagent execution is unavailable, keep the same task records and execute the tasks sequentially. Use a separately constructed verification method and explicitly record that independent agent review was unavailable; do not describe self-review as a separate reviewer. Report the actual execution mode.

## 6. Benchmark design and implementation

Preserve a runnable baseline of the existing analyzer before changing it. Use model registries and adapters rather than silently replacing it with a new engine.

### 6.1 Minimum bounded campaign

Predeclare a first tranche of at least 12 cases/configurations covering the categories below. Include all three model contracts, both ordinary and exceptional parameter cases, equivalent coordinate/equation presentations, symmetry-breaking cases, and data/physical-condition variations.

Do not demand complete classification of every difficult system as a prerequisite for finishing. Per case, report whether the result is a complete classification, a verified subset, a verified rejection, unsupported, or unresolved.

Cover:

- The printed scalar model at m=3, m=1, representative other integers, and a positive-branch noninteger exponent.
- Near-cubic cases on both sides of m=3, with the held-fixed coefficient convention stated.
- The original Eulerian model and its independently derived material formulation.
- Invertible point-coordinate changes and equivalent conservative/primitive presentations on their nonzero charts.
- A fixed-bed or zero-transport limit as a separately derived branch, not as substitution into a proof that divided by beta.
- At least one physically justified model extension, such as friction or an alternative sediment law, with its units and smooth branch documented.
- Symmetry-compatible and incompatible initial/boundary data, clearly distinguished from symmetries of the PDE alone.
- At least one infinite-dimensional control, such as the heat equation.
- At least one negative control where a previously admitted generator must fail.

For variable exponents, do not confuse dimensional parameter changes with a controlled dimensionless family. For threshold/absolute-value laws, treat smooth branches separately and do not apply smooth-point theory across a nonsmooth interface without justification.

### 6.2 Correctness and robustness

Use independent checks that can detect real implementation defects:

- Mixed-derivative consistency of prolongation recurrences.
- Agreement between independent prolongation constructions on selected nontrivial cases.
- On-shell validation of every returned generator against the original input model.
- Necessary-equation evidence before any completeness claim.
- Invariance under variable renaming, valid point-coordinate changes, and invertible recombination of equations.
- Equivalent-equation multiplication only on the declared nonzero chart.
- Correct branch handling at m=1, m=3, beta=0, and vanishing leading coefficients.
- Failure diagnostics for invalid invariant graphs or noninvertible reconstruction coordinates.
- A generator rejection supported by a nonzero symbolic residual or exact admissible jet witness, not floating-point sampling alone.

Where truth is unknown, do not calculate precision/recall as if a candidate list were complete. Compare Lie algebras up to basis change/pushforward rather than literal coefficient strings.

### 6.3 Performance measurements

Measure relevant stages separately: parsing, jet construction, prolongation, equation restriction, denominator/branch handling, coefficient collection, determining-system solution, certification, invariant construction, reduction, and reconstruction.

Record environment and versions, CPU/wall time, peak memory, expression/term sizes, coefficient counts, caching, tolerances, seeds, timeouts, and failure classifications.

Use repeated timings for inexpensive cases and separate cold/warm runs. Compare baseline and modified code on the same inputs, hardware, mathematical scope, and accuracy requirements. Include failures and preprocessing costs.

Do not call hard-coded SVE formulas a general analyzer, and do not claim a speedup from doing less mathematics.

## 7. Physical evaluation and an original-system exact benchmark

Use original variables \(h,u,B\) for physical conclusions. A scalar residual alone is insufficient.

Verify the following conversation-derived family independently and use it as an exact smooth benchmark if it passes. No novelty claim is attached to it.

For m=3, let

\[
T=t-t_0>0,\qquad z=x-x_0>0,\qquad
\alpha=\frac{2}{1+\sqrt{1+4g\beta}},
\]

and define

\[
h=H_*\left(\frac{T}{T_*}\right)^{-\alpha},
\qquad
u=\frac{\alpha z}{T},
\qquad
B=B_0+\frac{\beta\alpha^3z^2}{2T^2},
\]

with \(H_*,T_*,g,\beta>0\).

The motivating finite-dimensional substitution is \(h=H(T)\), \(u=a(T)z\), \(B=B_0+c(T)z^2\), giving

\[
H'+aH=0,\qquad
a'+a^2+2gc=0,\qquad
c'+\beta a^3=0.
\]

The parameter satisfies \(g\beta\alpha^2+\alpha-1=0\). The handoff preparation also checked the three conservative original-system residuals symbolically: mass and Exner vanished identically; momentum factored into the stated quadratic constraint. Repeat the verification in your own environment before using the fixture.

For a bounded numerical domain, impose initial and boundary traces from the exact solution and account for boundary fluxes. Do not demand constant total mass on an open domain with nonzero boundary flux.

Evaluate:

- original-system residuals and independent field errors;
- positivity and constitutive admissibility;
- water and sediment balance, including boundary fluxes;
- invertibility of the material map and reconstruction;
- finite-time chart failures and any approach to dry states or singular gradients;
- sensitivity to parameter and initial/boundary perturbations;
- the approximation restriction imposed by the chosen invariant/finite-dimensional class.

Use suitable baselines: high-accuracy ODE methods for reduced ODEs, and a verified appropriate original-system PDE method when comparison is needed. Document hyperbolicity, numerical flux/source treatment, time step restrictions, and grid-convergence checks. Do not treat a reduced ODE solver as an original-PDE solver.

If experimental/field data exist locally, document provenance, units, parameter fitting, and validation separation. If no such data exist, report mathematical verification and numerical physical-model experiments; do not claim empirical physical validation.

Carry out the reduced-ODE learning assessment in Section 8. Keep symmetry discovery, certification, reduction, reference generation, solver, and training costs separate. Restrict physical conclusions to the model whose equivalence and reconstruction were actually checked.

## 8. Mandatory semi-analytic and reduced-ODE learning study

### 8.1 Recover the current computation and define the task

Audit the existing ODE computation before redesigning it. Reproduce its equations, normalizations, independent variable, state representation, initial/boundary data, integration constants, tolerances, Jacobians, stopping events, singular branches, and reconstruction. Check that the implemented right-hand side agrees with the mathematically verified reduction. An integration in an Abel coordinate and an integration of the unreduced profile ODE are distinct implementations and can provide a useful cross-check.

Start from the actual classical and approximation runs identified in Section 2.4, including the existing Chebyshev control and failed learned runs. Determine what those learned runs actually trained: basis coefficients, a neural remainder, a standalone PINN, or another approximation. Do not relabel a non-neural coefficient fit as a trained deep network. When comparing second- and third-order formulations, reconstruct the first-integral constant from the same data and check that the solution problems agree.

State which computational task is being studied:

- one admissible IVP or BVP;
- repeated evaluations of the same solution;
- many solves over a specified finite-dimensional parameter/initial-data family;
- parameter inference or calibration from a declared observation model;
- an optional approximation outside an invariant class, which requires its own PDE-level argument.

These tasks have different costs and mathematical obligations. Fitting one profile does not demonstrate a solution operator over arbitrary data. Learning a residual profile does not discover a symmetry, and learning the reduced vector field is not the same problem as approximating solutions of a known vector field. Do not learn an already known right-hand side merely to call the method hybrid; identify the computational or modeling benefit first.

Treat "workflow-certified symmetry profile" as a proposed project convention, not an established term or a novel theorem. Define a reduction record containing the model/version, admitted generator or subgroup, exact invariance certificate, regular chart, invariant ansatz, reduced equation, reconstruction, integration constants, admissible data, and domain guards. Distinguish three statuses: a certified reduction structure, a numerically validated profile with a stated error assessment, and a rigorously enclosed profile when an actual rigorous enclosure has been computed. Ordinary solver tolerances and sampled residuals do not confer the third status.

Reconcile this record with the existing \(\mathsf C_H\) complexity/status record rather than introducing an incompatible parallel definition. Explicitly distinguish learning F or its correction from learning a predictor based on \(\mathsf C_H\). Exact algebraic facts, admissibility decisions, and certificate status are verified inputs, not facts made true by a predictor. A prospective learned selector may rank already certified reductions or estimate cost/error, but needs enough independently labeled tasks, held-out regimes, calibration, and a deterministic acceptance check. Assess whether such a dataset and task justify learning a selector at all; do not infer it from a handful of SVE cases. Keep selector learning optional and separate from the mandatory reduced-ODE profile study.

Choose a learning target only after constructing that record: for example, the profile F, its slope \(\mu=F'\), a regular Abel variable N, or a compatible first-order state \(z=(F,F',F'')\) for a third-order profile equation. Explain conditioning, derivative requirements, excluded branches, and reconstruction for the chosen target. Do not force a reciprocal Abel variable onto its excluded \(W=0\) branch.

For a family, specify its finite parameter vector \(\lambda\), permitted initial data, branch labels, compact evaluation domains, and dimensionless conventions. Verify the reduction at every parameter value used. In particular, an exact m=3 invariant ansatz cannot silently be reused at \(m=3\pm\delta\) if its generator is no longer admitted. A perturbative or approximately invariant method needs separately derived equations, a stated approximation order, and a validity test.

### 8.2 Establish appropriate deterministic baselines

Read the documentation for the installed SciPy version and inspect the actual local environment. For regular nonstiff IVPs, assess methods such as RK45 and DOP853; for demonstrated stiffness, assess suitable implicit methods such as Radau or BDF, or LSODA when appropriate. Justify method choice through the equation, Jacobian, conditioning, and observed solver behavior. Do not interpret failure at a coordinate singularity as evidence that ordinary ODE integration is intrinsically inadequate. Log events before inadmissible denominators, loss of positivity, or chart failure.

Use solve_bvp only for a correctly posed BVP with the appropriate number of independent boundary conditions and an assessed local solvability/conditioning argument. Do not replace an IVP by an easier BVP and compare timings as though the tasks were identical. Reproduce any existing spectral, Chebyshev, sparse-collocation, quadrature, or interpolation code; assess it where relevant. For many-query work, include nonlearned reuse such as interpolation or a classical reduced surrogate, not only repeated independent IVP solves.

Generate reference values and the needed derivatives using independently checked high-accuracy computations or exact formulas. Check tolerance/refinement sensitivity and use a second formulation or algorithm on representative cases. A single SciPy run is a numerical reference, not an exact oracle or an existence proof. Charge reference-data generation to any method that uses those data for training or tuning.

### 8.3 Compare standalone and hybrid approaches progressively

Use the following comparison structure, adapting implementation details to the audited problem:

| Stage | Method | Required question |
| --- | --- | --- |
| C0 | Exact formula/quadrature where available; appropriate accurate ODE integration otherwise | What accuracy and cost are already attainable for this task? |
| C1 | Classical reuse, interpolation, spectral approximation, or parameter surrogate | Does a nonlearned reusable representation already meet the many-query goal? |
| N0 | Standalone PINN applied to the same reduced ODE and admissible data | Can direct physics-informed profile learning compete, and where does training fail? |
| H1 | Semi-analytic base plus a neural profile/defect correction | Does explicit structure improve accuracy, conditioning, or cost over N0 and classical alternatives? |
| H2 | Conditional hybrid over a declared admissible parameter/data family | Is any benefit retained on held-out whole profiles, rather than just new points on training profiles? |
| H3 | Optional learned warm start or solver assistance with a deterministic corrector and fallback | Does assistance improve total cost at matched verified accuracy? |

The core bounded study must attempt C0, an appropriate C1 comparison when reuse is claimed, N0, and at least one justified hybrid. Assess H2 when many-query usefulness is the motivation; H3 is optional. If the local project lacks ML code, implement a minimal reproducible N0 and hybrid in the project environment when feasible. Record precise resource/infrastructure blockers if execution is impossible; absence of old code alone is not a scientific reason to skip the assessment. Unexecuted comparisons remain unresolved.

Select at least two representative regular ODE tasks from certified reductions or independently verified finite-dimensional substitutions, preferably including an analytic control and a genuinely nonlinear profile. To support a family-level claim, also use a held-out admissible parameter/initial-data family. Confirm that at least one tested reconstruction solves the original SVE model when physical applicability is claimed. A printed-scalar-only experiment has that narrower scope. Do not choose artificial singular windows merely to make a classical baseline fail.

Use at least three independent random seeds for each core neural comparison where feasible within the declared budget. Preserve all seeds and failures; disclose a smaller completed sample. Do not extrapolate broad statistical conclusions from three runs. Keep a full original-PDE PINN as a separately budgeted optional control, rather than treating an ODE PINN as an arbitrary-data PDE solver.

### 8.4 Derive the architectures and losses from the mathematics

Separate exact structure from numerical approximation. For example, once the chosen model admits the verified X5 reduction, the reconstruction

\[
\widehat\phi_\theta(t,s)=\widehat F_\theta(st^2)
\]

has the required invariant graph structure for every sufficiently smooth choice of \(\widehat F_\theta\) on the stated chart. Show the chain-rule calculation. This does not imply that \(\widehat\phi_\theta\) satisfies the PDE: that depends on the profile equation, reconstruction compatibility, and accuracy of the learned profile.

For H1, motivate and derive a representation such as

\[
\widehat F_\theta(\sigma;\lambda)
=F_{\mathrm{base}}(\sigma;\lambda)
+a_{\mathrm{bc}}(\sigma;\lambda)\,N_\theta(\sigma;\lambda).
\]

Define the deterministic base, neural correction, boundary/initial-data lifting factor, normalization, and parameter domain before using the expression. The base may be an analytic branch, a justified local series, or a deliberately coarse deterministic solve. Charge its construction cost and identify its accuracy; hiding a full accurate solve in the base invalidates a claimed learning speedup.

For the existing Taylor/series prior P_K, distinguish coefficients fixed by prescribed data from additional coefficients derived from the ODE. Derive the recurrence explicitly, check ordinary-point/analyticity hypotheses, and state any convergence radius or derivative-aware remainder bound that is actually available. A formal recurrence alone is not an accuracy certificate. Compare data lifting alone with additional equation-derived orders K, and assess classical series continuation, Padé/rational approximation, or patching when appropriate. Explain which part remains for the neural correction to learn and why that residual task should be easier in the norm relevant to reconstruction; test the claim rather than assuming it.

Derive the lifting factor for the actual conditions. For a third-order IVP, a smooth correction multiplied by \((\sigma-\sigma_0)^3\) preserves the prescribed F, F', and F'' at \(\sigma_0\) when the base already matches them; verify all three derivative traces explicitly and maintain consistent units. Other orders or BVP conditions require their own construction. Do not copy that factor into a different problem without checking its conditions.

If a positive slope is required, assess a representation such as \(\widehat\mu=\exp(S_\theta)\), including data matching, chain rules, conditioning, and reconstruction. Positivity of one represented quantity alone does not establish all physical admissibility conditions. Use smooth activations with enough classical derivatives for the selected residual; a piecewise-linear ReLU profile does not supply a generic classical third-order residual. A weak residual formulation is permissible only after its own definition and justification.

For a first-order state formulation, include compatibility residuals such as \(\widehat z_1'-\widehat z_2\) and \(\widehat z_2'-\widehat z_3\), not just the highest-order equation. Define every loss term, scaling, norm, weight, collocation rule, data term, and stopping criterion. Audit eq:neural and eq:optimization-gradient-core in the existing manuscript, retaining the derivative of the residual weight when that weight depends on the learned profile. Measure unweighted physical residuals as well as any optimized weighted loss. A hard invariant ansatz, hard data constraints, and soft differential-equation penalties have different guarantees.

Derive any reconstruction-aware weighting from the actual pullback identities and conditioning, not an unexplained heuristic. Track nonzero multipliers: equality of two residual zeros does not make their numerical magnitudes interchangeable. Never change the SVE equation to absorb neural error without identifying a distinct learned model and validating that model separately.

### 8.5 Establish existence, approximation, and error implications separately

Provide a precise chain of reasoning rather than using "PINN existence" ambiguously:

1. Determine whether the selected ODE IVP/BVP has a solution, whether it is locally unique, and how far it can be continued on the admissible chart. For an explicit first-order IVP, verify the relevant continuity and local Lipschitz hypotheses. Treat implicit or singular branches separately.
2. State the regularity and domain needed for the neural approximation class. Any approximation theorem used must control the derivative order appearing in the residual, through an appropriate \(C^k\) or Sobolev statement. Approximation in function values alone does not imply small high-order differential residuals.
3. Distinguish existence of an approximating network from convergence of the chosen optimizer to it. Training success is an experimental claim unless a relevant convergence theorem with checked hypotheses applies.
4. Distinguish finite collocation loss from a continuous-domain residual bound. Dense independent sampling is useful evidence, but is not a rigorous supremum certificate. Use interval/enclosure methods or justified derivative/covering bounds if a rigorous certificate is claimed.
5. Establish the stability estimate needed to convert residual and data errors into solution error. Parameter inference additionally requires an identifiability/sensitivity analysis; forward accuracy does not supply it.

For a regular IVP written as \(z'=f(\sigma,z;\lambda)\), derive a conditional residual-to-error proposition. If f has a stated Lipschitz constant L on a suitable common region, the exact and approximate trajectories remain in that region, \(e_0=\|\widehat z(\sigma_0)-z(\sigma_0)\|\), and

\[
r(\sigma)=\widehat z'(\sigma)-f(\sigma,\widehat z(\sigma);\lambda),
\]

establish, for forward \(\sigma\geq\sigma_0\),

\[
\|\widehat z(\sigma)-z(\sigma)\|
\leq e^{L(\sigma-\sigma_0)}e_0
+\int_{\sigma_0}^{\sigma}e^{L(\sigma-\rho)}\|r(\rho)\|\,d\rho.
\]

Show the integral subtraction, norm inequality, and Gronwall step. State how L is bounded, prove or explicitly assume the necessary trajectory containment, and derive the uniform-residual special case including L=0. Do not present this conditional estimate as a new theorem or as an unconditional global guarantee. If the bound is too pessimistic to be useful, report that fact and investigate a justified sharper stability estimate. A BVP requires its own stability/invertible-linearization or Green-operator argument; the IVP estimate does not apply automatically.

Derive reconstruction error implications using the actual coordinate maps, required derivative norms, positive Jacobian bounds, and denominator lower bounds. Distinguish errors at matched material coordinates from errors at matched physical coordinates. For example, controlling \(h=1/\phi_s\) needs a lower bound on the relevant derivatives, and inversion of \(x=\phi(t,s)\) introduces additional conditioning. Do not infer original-PDE solution error from a scalar residual without checked model equivalence, data compatibility, and the necessary stability reasoning.

Locate and cite primary mathematical sources for each existence/approximation/stability result actually invoked. State a proved project-specific lemma with its proof when needed. Do not add a theorem solely to make the manuscript appear rigorous; its hypotheses and conclusion must support a reported claim.

For the existing prop:ode-error-core and prop:error-transfer-core, produce a hypothesis-by-hypothesis applicability table for each reported task. Distinguish the exact reference-trajectory tube bounds already claimed in the manuscript from containment and residual bounds for a trained approximant. A reference tube does not automatically contain that approximant. Supply the missing margins or retain an explicitly conditional/empirical conclusion. Extend the existing propositions only where the new argument is necessary and checked.

### 8.6 Fair benchmarking, information accounting, and acceptance gates

Predeclare domains, admissible parameter/data ranges, accuracy targets, norms, hold-outs, compute limits, and failure criteria before the comparison. Match the mathematical task, model, data, precision requirements, and evaluation domain. Record hardware separately and include end-to-end costs when comparing CPU classical methods with GPU learning. Use reasonable tuning for both; a weakly trained PINN and a deliberately poor ODE configuration are both invalid representatives.

Keep training, validation, and test information separate. For a conditional model, hold out entire parameter/initial-data profiles, not only collocation points from profiles already seen in training. Use validation for architecture and hyperparameter choices, then freeze the comparison before testing. Reference test solutions must not enter the learned base, training labels, stopping rule, or model selection. Use separate training and final evaluation points.

Report state and derivative errors, independent residuals, initial/boundary mismatches, reconstructed field errors, admissibility/branch failures, conservation defects where applicable, and success rates. State whether an error is absolute or relative and handle near-zero references explicitly. Distinguish solver failure, coordinate failure, invalid input, training failure, and failure to meet the accuracy target. Include every completed run and declared timeout rather than selecting the best seed.

Record architecture, activation, initialization, optimizer/schedule, loss scaling, collocation/adaptation strategy, sample counts, label provenance, epochs/iterations, random seeds, package versions, precision, compilation/warm-up, automatic differentiation, and peak memory. Separate observations, reference-generated labels, and physics collocation points when claiming reduced data requirements. Unlabeled physics residuals still provide information and incur computation.

Measure time to a matched accuracy target and an accuracy/cost curve, not inference latency alone. Include symbolic certification, reference generation, preprocessing, base construction, tuning, training, inference, residual checks, deterministic corrections, and fallback. Report relevant stage costs even when a shared stage cancels in a particular comparison.

For amortization over \(N_q\) queries, use a declared cost model such as

\[
\begin{aligned}
C_{\mathrm{class}}(N_q)&=C_{\mathrm{sym}}+N_qC_{\mathrm{solve}},\\
C_{\mathrm{learn}}(N_q)&=C_{\mathrm{sym}}+C_{\mathrm{offline}}
+N_q\bigl(C_{\mathrm{infer}}+C_{\mathrm{check}}
+p_{\mathrm{fb}}C_{\mathrm{fallback}}\bigr),
\end{aligned}
\]

where \(C_{\mathrm{offline}}\) includes the actual data, base, tuning, training, and validation costs, and \(p_{\mathrm{fb}}\) is the measured fallback frequency on the declared query distribution. Add any omitted correction stage explicitly. Compare a classical reusable surrogate using its own offline/online costs. Cancel \(C_{\mathrm{sym}}\) only when the stages really are shared. Derive a break-even query count only when the denominator is positive and the methods meet the same accuracy/failure requirements; explain the distributional and timing uncertainty.

Use primary PINN benchmarking studies to inform protocols, not to establish SVE-specific performance or mathematical existence. Disambiguate any locally named "PINN-benchmark" or "PINNBench" by its actual paper, repository, version, and scope. PINNacle is a PDE benchmark; adaptation to a reduced ODE requires an explicit protocol. Do not conflate it with PDEBench or another similarly named resource. Read relevant failure-mode and hybrid/SciML primary sources, verify their assumptions, and document the difference from this project.

### 8.7 New ideas, ablations, and the decision to use ML

Investigate at least three concrete candidate improvements before choosing the hybrid implementation. Suitable directions, subject to the local audit, include:

- an analytic/coarse deterministic base with a small learned defect correction;
- residual and reconstruction conditioning used to select coordinates, scale losses, or place collocation points;
- guard-aware chart/domain decomposition with proved matching conditions, rather than learning through a singular coordinate;
- a conditional surrogate restricted to certified admissible parameter/data families;
- learned warm starts with a deterministic accuracy check, correction, and tested fallback.

For each candidate, state the hypothesized mechanism, prior art, assumptions, predicted benefit, falsifiable experiment, and added cost. Distinguish a change of representation from a new learning algorithm. Classify it as established technique, project adaptation, untested hypothesis, implemented proposal, or supported new result. A conventional method acquiring a new project name is not evidence of novelty. Implement and test at least the strongest feasible justified hybrid, rather than leaving all ideas as a list.

Audit the existing Kolmogorov-width and neural representation-error definitions in sec:complexity-core. If claiming that tighter analysis makes learning easier, specify the profile family, norm, analytical remainder, derivative budget, and resulting approximation target, then compare prior order K, neural capacity P, collocation budget N, and measured optimization cost. A smaller input dimension, fewer ambient jets, or a smaller linear approximation width does not alone prove reduced neural capacity, sample complexity, or training time. Report which links in the proposed reasoning are proved and which are only empirically supported.

Use targeted ablations to test the claimed mechanism: for example, no analytic base, no hard invariant/data constraint, alternative regular coordinates, no special residual weighting, or no deterministic correction. Keep scope and compute budgets explicit. Only compare alternatives that solve the same stated problem; an off-invariant correction changes the approximation class. If pursuing departure from an invariant class, derive the appropriate PDE correction and validity conditions separately instead of pretending the same reduced ODE covers it.

Move from standalone N0 to H1/H2 by a written diagnosis of what the preceding stage cannot do. Do not equate a more complicated architecture with stronger reasoning. A simpler classical method meeting the actual task is a valid result, but the conclusion must follow from the audit and completed comparisons. Report one of: demonstrated single-solve benefit, demonstrated many-query benefit, demonstrated inference benefit for a specified inverse task, no demonstrated benefit in the tested regime, or unresolved under the recorded budget. None of these alone proves that ML is universally necessary or unnecessary.

## 9. Integrate supported results into the actual main.tex

Updating main.tex is an execution requirement, not a suggestion to write a separate future-work note. Inspect the current manuscript and its included sources; preserve unrelated text and user edits. Integrate into the existing argument rather than appending disconnected research logs. Start from the existing sec:complexity-core, sec:selection-core, sec:optimization-core, sec:publication-review, and sec:experiment-artifact, recording a precise delta instead of duplicating their definitions, diagrams, propositions, or reported experiments.

Include the following, to the extent supported by completed derivations and runs:

1. A precise semi-analytic objective and a labeled project definition of the certified reduction record, separating exact symmetry structure from learned numerical profiles.
2. The full reduction-to-computation workflow, geometric motivation, scope of the invariant class, model contracts, and data/chart restrictions.
3. The actual ODE formulation, existing computation audit, classical baseline choices, and the operational criterion for considering learning.
4. The standalone and selected hybrid architectures, all transformations, chain rules, data liftings, residuals, derivative requirements, and training/evaluation algorithms.
5. Checked existence/local uniqueness and continuation assumptions, any relevant approximation result, the conditional residual-to-error argument with proof, and reconstruction conditioning. Mark limitations where a stronger bound is unavailable.
6. New ideas with prior-art comparisons, falsifiable hypotheses, implementation status, and ablation evidence. Reserve novelty claims for the parts actually supported.
7. Reproducible accuracy/cost tables and figures, seeds and hold-out design, failures and excluded branches, matched-accuracy comparisons, and any measured amortization threshold.
8. Original-system verification, physical admissibility, and the distinction between numerical model experiments and field validation.
9. A clear limitations discussion and conclusions consistent with the evidence, including an explicitly negative or inconclusive ML result if that is what the study establishes.

Make the manuscript ready for public technical review through a claim-to-evidence ledger. For each major mathematical or empirical claim, record its main.tex label/location, assumptions, source page/equation or proof, model ID, relevant code path, configuration, input/seed, certificate or raw run, figure/table data, and reproduction command. Record commit/hash information where available. Provide a compact table that lets a reviewer tell whether each claim is proved, symbolically checked, numerically supported, or still hypothetical. State exactly which statements are proposed by this project and which are cited definitions/results.

Use actual measured values and checked statements. Do not insert invented tables, predicted speedups presented as results, unverified theorem environments, or placeholders suggesting completed work. Unexecuted ideas belong in a clearly identified research-directions passage. Update the abstract, contributions, and conclusion only to reflect established results. Include enough derivation detail for manual reproduction, with long symbolic expansions and raw numerical configurations in reproducible appendices/artifacts.

Keep the bibliography manually formatted in GB/T 7714 and verify the primary references actually used. Build the manuscript using its real toolchain, fix introduced undefined references/citations and mathematical/typesetting defects, and inspect changed equations, figures, tables, and PDF pages. Deliver the source diff and build log. A successful LaTeX build checks document production; it is not a mathematical or experimental certificate.

If the canonical manuscript remains unavailable after bounded authorized discovery, record the exact blocker and prepare a clearly identified insertion patch/source fragment with its evidence ledger. Do not fabricate a substitute and claim the real main.tex was updated. Finish independent work and report that manuscript integration is incomplete.

## 10. Deliverables and completion criteria

Follow the repository layout where possible. Deliver at least:

1. A current-state/evidence audit with source and code manifests, unresolved issues, and claim status.
2. The completed general Lie_reduction account, a notation/definition table, precise diagrams, full worked SVE traces, and page-specific primary references.
3. Separate model specifications and executable equivalence/reconstruction checks.
4. Reviewed analyzer changes where justified and feasible, meaningful regression checks, and a preserved baseline where available; otherwise an evidence-backed report of the missing implementation or specific blocker. Do not change correct code merely to claim an implementation contribution.
5. A configurable benchmark runner, case registry, raw machine-readable results, and reproducible summaries.
6. At least one verified original-system closed-form family and a completed numerical verification experiment, or a precise falsification report if a proposed family fails.
7. A reduced-ODE/SciPy audit, explicit learning-target/reduction records, runnable classical and neural baselines, at least one implemented justified hybrid where feasible, raw seeded/held-out results, targeted ablations, and a cost/benefit decision with its limitations or precise execution blockers.
8. The actual updated main.tex and included sources, supported mathematical/empirical additions, generated figures/tables, a claim-to-evidence ledger, source diff, and build log; if blocked, a clearly labeled insertion patch and an explicit incomplete-integration status.
9. An integrated research report separating mathematical correctness, algorithmic performance, representational restrictions, learning usefulness, and physical usefulness.
10. A task/subagent ledger, reproduction commands, environment specification, and resumable status file.
11. A concise final handoff: what changed, what was proved, what ran, measured results, manuscript changes, limitations, and the next three justified research actions.

Classify every important result as exact identity, proved theorem/proposition with assumptions, verified candidate, ansatz-restricted result, numerical evidence, conjecture, or unresolved.

Completion means producing and checking these concrete artifacts, not promising to produce them later. A bounded campaign may finish with documented unknown classifications or resource failures, but these must not be counted as passes.

For the learning study, distinguish assessment completed from a successful neural method: documented negative results can complete the assessment, while unrun core comparisons remain blocked or incomplete. Neither a favorable narrative nor an untested architecture satisfies the empirical obligations.

Do not claim:
- all SVE solutions have been classified;
- a symmetry dimension jump proves discontinuity of PDE solutions;
- a diagonal-scaling obstruction proves unrestricted point-symmetry obstruction;
- small PDE residual proves small solution error;
- an invariant solver handles arbitrary initial data;
- infinitely many symmetries guarantee closed-form general solvability;
- numerical verification constitutes experimental physical validation;
- a repaired printed formula was necessarily the authors' intended formula;
- a small collocation loss proves continuous-domain accuracy, ODE existence, or optimizer convergence;
- an exactly invariant neural ansatz is an exact PDE solution or a closed-form solution;
- a few successful seeds establish generalization to arbitrary PDE data;
- fast inference alone proves an end-to-end speedup;
- a negative bounded comparison proves ML is never useful.

## 11. Writing and bibliography requirements

Write in formal academic English with explicit definitions, motivation, domain guards, and justified transitions. Eliminate flattery and conversational filler.

For every operator, transformation, ansatz, or quotient used in a derivation, define it before performing the algebra. Give all intermediate steps needed to reconstruct the result; make lengthy symbolic collections available as executable/machine-readable appendices.

Cite primary sources manually using GB/T 7714. Check author order, edition, year, page/equation numbers, DOI, and whether a result is actually proved. Read PDF pages containing delicate formulas visually when extraction is ambiguous.

Reference starting points, to verify against available copies:

[1] OLVER P J. Applications of Lie groups to differential equations[M]. New York: Springer-Verlag, 1986.

[2] OLIVERI F. Lie symmetries of differential equations: theory, applications, and symbolic computation[M]. Cham: Birkhäuser, 2026. DOI: 10.1007/978-3-032-12791-4.

[3] PALIATHANASIS A, LEON G, LEACH P G L. Lie symmetries and similarity solutions for a shallow-water model with bed elevation in Lagrange variables[J]. Mathematics, 2026, 14(3): 433. DOI: 10.3390/math14030433.

[4] GUBBIOTTI G, LEVI D, SCIMITERNA C. On partial differential and difference equations with symmetries depending on arbitrary functions[J]. Acta Polytechnica, 2016, 56(3): 193-201. DOI: 10.14311/AP.2016.56.0193. arXiv:1512.01967.

[5] BLUMAN G W, DE LA ROSA R. The natural extension to PDEs of Lie's reduction of order algorithm for ODEs[EB/OL]. (2024-07-12)[2026-10-19]. https://arxiv.org/pdf/2407.09063.

[6] SCIPY DEVELOPERS. scipy.integrate.solve_ivp[EB/OL]. [2026-10-19]. https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html.

[7] SCIPY DEVELOPERS. scipy.integrate.solve_bvp[EB/OL]. [2026-10-19]. https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_bvp.html.

[8] HAO Z, YAO J, SU C, et al. PINNacle: a comprehensive benchmark of physics-informed neural networks for solving PDEs[EB/OL]. (2023-10-05)[2026-10-19]. https://arxiv.org/abs/2306.08827v2. DOI: 10.48550/arXiv.2306.08827.

[9] KRISHNAPRIYAN A, GHOLAMI A, ZHE S, et al. Characterizing possible failure modes in physics-informed neural networks[EB/OL]. (2021)[2026-10-19]. https://proceedings.nips.cc/paper_files/paper/2021/hash/df438e5206f31600e6ae4af72f2725f1-Abstract.html.

[10] RACKAUCKAS C, MA Y, MARTENSEN J, et al. Universal differential equations for scientific machine learning[EB/OL]. (2021-11-02)[2026-10-19]. https://arxiv.org/abs/2001.04385v4. DOI: 10.48550/arXiv.2001.04385.

The online SciPy pages can change; cite documentation corresponding to the installed version in the final manuscript. Reference [8] identifies the checked arXiv version; the work also has a NeurIPS 2024 proceedings version. Reference [9] is the official NeurIPS 2021 proceedings landing page. Inspect the versions actually used and cite the appropriate published form, with verified metadata, in main.tex. Add primary approximation/stability and architecture sources needed by the final argument; these starting points are not a substitute for that literature audit.

Begin with the local inventory and current-progress audit. Continue through the foundation, autonomous task allocation, analyzer and ODE audit, staged classical/PINN/hybrid experiments, independent review, actual main.tex integration, and final evidence-backed handoff. The requested output is completed local research and a review-ready manuscript, not a plan awaiting routine user intervention.

