# LieML agent handoff and research queue

This file is the persistent coordination contract for the research task in
`D:\MATHs\math 4890 LieML`. Read it together with `CLAUDE.md` before acting.

## Objective

Generalize the current scalar `(1+1)` Lie-symmetry engine to a research-grade
PDE-system framework with:

- `p` independent variables `x^1, ..., x^p`;
- `q` dependent fields `u^1, ..., u^q`;
- `r` equations, including implicit, over/underdetermined, constrained, and
  singular polynomial differential systems where the selected CAS supports
  them;
- arbitrary multi-index jets and Lie point prolongation;
- theory for reduction by a `k`-dimensional Lie subalgebra;
- a first implementation of composable one-generator reduction (`p -> p-1`),
  designed so chains can realize higher-dimensional reductions;
- formal completion, branch decomposition, and machine-checkable reduction
  certificates;
- a substantial advanced-research section added to `intro.tex`.

Treat any new theory as a project-local formulation until a literature review
supports a novelty claim. Distinguish classical results, repackaged certificate
conditions, conjectures, and genuinely new propositions.

## Confirmed decisions

1. The target is generic `(p, q, r)`, not merely scalar `n`-dimensional PDEs
   or `n` spatial dimensions plus time.
2. The mathematical theory covers arbitrary `k`-dimensional subalgebras.
   Initial executable reduction is `k=1` and composable.
3. The target is advanced research-level differential elimination, not a
   best-effort call to `sympy.solve`.
4. Primary mature backend: Maple, principally `DifferentialThomas` plus
   `PDEtools`; evaluate `DifferentialAlgebra/RosenfeldGroebner` and GeM where
   each is stronger.
5. Secondary independent backend: REDUCE, principally
   `CRACK`/`LIEPDE`/`APPLYSYM`, with `CDIFF`/CDE considered where relevant.
6. The Python/SymPy engine owns the canonical intermediate representation,
   multi-index jet/prolongation logic, orchestration, verification records,
   and a bounded fallback. A Julia/Python differential-algebra analyzer is an
   acceptable later research track, but not a substitute for a mature oracle.
7. The mathematical support and limitations belong in a new major advanced
   section of the existing `intro.tex`, not a separate paper.
8. No visual companion is needed for the design discussion.

## Current project facts

- Project guidance: `CLAUDE.md`.
- The folder is not a Git repository.
- Maple, REDUCE, Sage, and a working Julia installation were not found on this
  machine. The `julia.exe` WindowsApps shim is inaccessible.
- System Python is 3.14.2; the project uses SymPy 1.14 and pytest.
- The current implementation is hard-coded to one field `u(x,t)`:
  `jet.py`, `determining.py`, `algebra.py`, and `reduce.py` all encode this
  assumption. `engine.py`, serialization, the CLI, corpus generator, and tests
  expose the resulting tuple conventions.
- Preserve `PDE.scalar_1plus1`, `pde.x`, `pde.t`, `pde.u`,
  `jet_sym(a,b)`, generator tuple order `(tau, xi, phi)`, and every existing
  regression unless an approved migration explicitly says otherwise.
- The project is outside the normal writable workspace. Read-only inspection
  is allowed; project writes require the appropriate approval.

## Design gate

The active workflow is design-first. Do not implement, scaffold, or alter the
engine until all of the following have happened:

1. research is synthesized;
2. two or three approaches and their trade-offs are presented;
3. the user approves the design section by section;
4. the approved spec is written and self-reviewed;
5. the user reviews that written spec;
6. a detailed implementation plan is produced.

Creating this coordination file is not approval to modify production code.

## Ordered TODO queue

### A. Complete focused research

- [ ] **R1 — Formal theory and proof obligations**
  - Define the bundle `E -> X`, coordinates, multi-indices, finite/infinite jet
    spaces, contact structure, total derivatives, differential rankings, and
    equation/inequation systems.
  - State point-generator and characteristic-form prolongation for arbitrary
    `(p,q)` and verify equivalence of recursive and characteristic formulas.
  - Model a Thomas/Rosenfeld decomposition as disjoint regular branches with
    principal and parametric derivatives; state precisely which analytic or
    formal solution semantics are certified.
  - Derive determining systems branchwise by normal-form reduction and
    splitting over parametric jets. Specify how branchwise symmetries combine
    into symmetries of the original system.
  - Formalize `k`-subalgebra closure, Frobenius integrability, orbit rank,
    projectability, transversality, rank strata, invariant-surface conditions,
    quotient variables, profile reconstruction, and singular reductions.
  - Investigate whether completion then reduction commutes with reduction then
    completion. Define a computable discrepancy/certificate without presenting
    a classical observation as novel.
  - Formulate a local correctness theorem: on each regular constant-rank
    branch, certified invariant solutions of the original system correspond to
    solutions of the reduced system under explicit hypotheses.
  - Identify counterexamples for non-involutive systems, rank drops,
    incompatible invariant-surface conditions, lost inequation branches, and
    reductions that introduce or divide by zero factors.

- [ ] **R2 — Mature backend capability and reproducibility study**
  - Verify exact roles and limits of Maple
    `DifferentialThomas:-ThomasDecomposition`, `NormalForm`, `ReducedForm`,
    `PDEtools:-DeterminingPDE`, `Infinitesimals`, `SymmetrySolutions`,
    `casesplit`, `DifferentialAlgebra:-RosenfeldGroebner`, and GeM.
  - Determine which Maple operations can emit a replayable proof/provenance
    artifact and which require independent checking in Python.
  - Verify REDUCE `LIEPDE` completeness assumptions, CRACK solving behavior,
    APPLYSYM invariant computation, and whether CDIFF/CDE supplies useful
    differential-consequence machinery.
  - Record license, installation, headless execution, version pinning, timeout,
    deterministic ranking, CI, and redistribution constraints.
  - Define backend parity benchmarks and honest outcomes: `verified`,
    `branch-partial`, `backend-unavailable`, `timeout`, and `unsupported`.
  - Evaluate Sage/Python/Julia differential-algebra projects only as future
    analyzers. The July 2026 `DifferentialThomas-sage` repository reports only
    phase 1, so it is not currently a production backend.

- [ ] **R3 — Existing-code migration analysis**
  - Inventory every scalar/`1+1` assumption and every public or serialized
    representation that depends on it.
  - Design stable types for `JetSpace`, `DifferentialSystem`,
    `DifferentialBranch`, `PointGenerator`, `LieSubalgebra`,
    `CompletionCertificate`, `ReductionMap`, `ReducedSystem`, and
    `ReductionCertificate`.
  - Specify the canonical generator ordering:
    `(xi^1,...,xi^p,phi^1,...,phi^q)`, with a legacy adapter for
    `(tau,xi,phi)`.
  - Split responsibilities among jet enumeration/naming, total derivatives,
    prolongation, normal forms, determining equations, ansatz windows,
    Lie-algebra operations, invariants, substitution/pullback, external CAS
    adapters, orchestration, reporting, and serialization.
  - Plan checkpoint/result schema versioning and cache invalidation using a
    mathematical-system fingerprint, backend/version, ranking, and assumptions.
  - Identify expression-growth controls, lazy jet generation, degree/order
    budgets, cancellation/timeouts, and branch limits.

- [ ] **R4 — Validation corpus and falsifiable gates**
  - Keep the complete current scalar `(1+1)` test suite green.
  - Add low-cost formula/property tests for multi-index enumeration, commuting
    total derivatives, prolongation recurrences, bracket antisymmetry/Jacobi,
    renaming/permutation covariance, and legacy API equivalence.
  - Use at least one scalar `2+1` equation, one two-field system, one system
    with `r != q`, one implicit differential constraint, one parameter-induced
    singular branch, and one rank-dropping reduction.
  - Candidate escalating benchmarks: decoupled heat/advection fields;
    reaction-diffusion systems; Cauchy--Riemann or Maxwell-type first-order
    systems; incompressible `2D` Navier--Stokes with pressure and divergence
    constraint; a manufactured Thomas-decomposition branch example.
  - Pin published symmetry algebras/reductions only after locating primary or
    standard references. Do not infer truth from agreement between two wrappers
    around the same CAS.
  - Require substitution/pullback and normal-form-zero checks for every emitted
    reduction; retain counterexamples as negative tests.

- [ ] **R5 — `intro.tex` research section**
  - Add a layered section after the existing jet/diffiety foundations and
    before the glossary, with a short bridge from the beginner material.
  - Cover `(p,q,r)` notation, multi-index jets, differential completion and
    branch semantics, general prolongation, determining systems, `k`-orbit
    reduction, rank/transversality, invariant-surface equations, quotient and
    reconstruction, the certificate, algorithm/backend architecture,
    complexity, benchmark gates, and limitations.
  - Include theorem/lemma/proof sketches and one worked multi-field,
    multi-dimensional example.
  - Cite Olver/Bluman--Kumei for Lie reduction; Bächler--Gerdt--
    Lange-Hegermann--Robertz for differential Thomas decomposition; and
    authoritative Maple/REDUCE documentation. Verify every stronger claim.
  - Compile with XeLaTeX or the project-supported TeX engine and inspect the
    resulting PDF/log for errors and overfull boxes.

### B. Synthesize and approve the architecture

- [ ] Present two or three viable architectures with costs and risks.
- [ ] Recommend a backend-neutral Python core with Maple as the proof-producing
  primary backend and REDUCE as an independent secondary path.
- [ ] Review design sections separately: mathematical contract; components and
  APIs; backend protocol; reduction/certificate flow; errors/statuses;
  migration; tests/benchmarks; paper structure.
- [ ] Obtain explicit user approval.

### C. Persist the approved design

- [ ] Write `docs/superpowers/specs/2026-07-30-nd-pde-system-lie-reduction-design.md`
  unless the user selects another name/location.
- [ ] Self-review for placeholders, contradictions, scope creep, ambiguous
  semantics, and unsupported novelty claims.
- [ ] Because this folder is not a Git repository, ask whether to initialize
  Git or record the spec without the brainstorming workflow's normal commit.
- [ ] Ask the user to review the written spec.

### D. Plan and implement only after approval

- [ ] Produce a test-first implementation plan with small, reviewable tasks.
- [ ] Establish a clean baseline with bytecode/cache writes disabled or routed
  to an approved temporary directory.
- [ ] Implement canonical data types and the legacy facade first.
- [ ] Implement generic jets, total derivatives, and prolongation second.
- [ ] Implement determining/algebra generalization third.
- [ ] Implement CAS interchange and completion adapters fourth.
- [ ] Implement composable one-generator reduction and certificates fifth.
- [ ] Migrate engine/report/checkpoint/CLI/corpus consumers sixth.
- [ ] Add oracle integrations and escalating benchmarks last.
- [ ] Update and compile `intro.tex`, then run the complete verification suite.

## Saved subagent fan-out configuration

Retry these as three independent research agents when capacity is available.
They must not edit files.

Common settings:

- `fork_turns: "none"`
- inherit the parent model and reasoning effort; no model override
- run concurrently when service capacity permits
- scope is research and task decomposition only
- inspect the project read-only
- return structured evidence, risks, open questions, and a task DAG
- never claim implementation success

### Agent `formal_theory`

Goal: produce the mathematical framework described in R1.

Required return:

1. core definitions;
2. candidate theorem and lemma statements;
3. certificate schema;
4. proof/research task DAG;
5. benchmarks and counterexamples;
6. references requiring verification.

### Agent `backend_research`

Goal: produce the capability and integration study described in R2.

Required return:

1. evidence-based capability matrix;
2. primary/secondary/fallback recommendation;
3. backend adapter and serialization contract;
4. install/license/CI risks;
5. oracle/parity tests;
6. staged research and implementation task DAG.

### Agent `migration_validation`

Goal: produce the module/API migration and validation plan described in
R3--R5.

Required return:

1. scalar-assumption inventory;
2. public types and compatibility layer;
3. module/data-flow migration map;
4. error/status and checkpoint migration;
5. benchmark and test matrix;
6. risk-ordered task DAG with acceptance criteria;
7. exact `intro.tex` insertion and content plan.

### Last fan-out result

On 2026-07-30, all three agents failed before producing research because the
service returned HTTP `429 Too Many Requests` and exhausted retries. Their
tasks remain pending. Retry later; do not treat the failed calls as findings.

## Working principles

- Explain the beginner-facing layer clearly, but make the mathematics and
  certificates precise enough for research review.
- Preserve negative results and unsupported branches explicitly.
- Never equate polynomial-ansatz stabilization with proof of a complete Lie
  algebra.
- Never label a reduction certified solely because orbit variables disappear;
  verify it against completed branches by normal form or an equivalent oracle.
- Record all rankings, inequations, divisions, assumptions, backend versions,
  timeouts, and branch coverage in reproducibility artifacts.
- Keep backend-specific syntax outside the mathematical core.
