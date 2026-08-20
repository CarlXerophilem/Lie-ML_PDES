# LieML Project Map

This file is the navigation sheet for the LieML workspace. It does not
replace the project contracts or authorize implementation work.

## 1. Authority order

When documents disagree, use this order:

1. The current user request.
2. `LIEML_AGENTS_INIT.md` (identical to `AGENTS.md` at present): active
   research objective, design gate, compatibility rules, and ordered queue.
3. `CLAUDE.md`: project purpose, conventions, environment, and run commands.
4. `PROJECT_MAP.md`: repository navigation and status summary.
5. `ADVISORY.md`, `CURRICULUM.md`, and `PAPER_TODO_20DAYS.md`: research,
   curriculum, and paper-planning context.
6. `docs/superpowers/specs/` and `docs/superpowers/plans/`: approved or
   historical design artifacts, subject to the active handoff contract.
7. `.sdd/`: execution ledger and review history for the scalar v1 track.

The active handoff contract takes precedence over older v1 plans. A plan is
not approval to execute if the handoff design gate has not been satisfied.

## 2. Repository areas

| Area | Role | Status |
|---|---|---|
| `symm/sym_engine/` | Scalar `(1+1)` Lie engine | v1 complete; preserve regressions |
| `symm/tests/` | Engine, benchmark, and ML regression tests | Existing suite is the baseline |
| `symm/reductor/` | Deterministic corpus and symmetry-prioritization experiments | v1.1 research complete enough for review |
| `symm/sacno/` | Symmetry-aware neural-operator experiments | Companion research track |
| `symm/bench/` | Planned measurement and benchmark harness | Specification exists; implementation is separate |
| `symm/runs/` | Reproducibility traces and engine outputs | Generated artifacts; do not treat as source |
| `ref/` | Source PDFs and research references | Literature corpus |
| `pdf2md/` | Extracted reference text and extraction tooling | Research support |
| `intro.tex` | Beginner-to-advanced mathematical exposition | Advanced section is pending |
| `draft/` | Thesis/paper draft | Paper assembly track |
| `docs/superpowers/specs/` | Reviewed design specifications | Add the new generic-PDE spec only after approval |
| `docs/superpowers/plans/` | Implementation plans | Existing plan is scalar v1 history |
| `.sdd/` | Scalar v1 task reports and completion ledger | Historical execution record |

Top-level generated TeX files (`*.aux`, `*.log`, `*.out`, `*.toc`, `*.pdf`,
and `*.synctex.gz`) are build outputs. They remain untouched for now because
the workspace is not under Git and cleanup has not been authorized.

## 3. Completed baseline

The scalar v1 baseline consists of:

- `PDE.scalar_1plus1` and the legacy `(tau, xi, phi)` generator convention;
- jet/prolongation, determining equations, bounded elimination, algebra
  operations, one-generator reduction, checkpointing, cross-checking,
  reporting, and CLI layers;
- textbook validation and the deterministic reductor experiments;
- the existing scalar regression suite, recorded in `.sdd/progress.md`.

Any generic implementation must preserve `pde.x`, `pde.t`, `pde.u`,
`jet_sym(a,b)`, legacy tuple ordering, and all current regression behavior
through an explicit compatibility adapter.

## 4. Active program: generic PDE systems

The target is a research-grade framework for `p` independent variables, `q`
dependent fields, and `r` differential equations. The mathematical scope
includes arbitrary multi-index jets, point prolongations, differential
completion and branch semantics, and reductions by arbitrary `k`-dimensional
Lie subalgebras. The first executable reduction remains composable
one-generator reduction.

The intended architecture is backend-neutral Python/SymPy orchestration with:

- Maple/DifferentialThomas and PDEtools as the primary mature backend;
- REDUCE/CRACK/LIEPDE/APPLYSYM as an independent secondary route;
- bounded Python fallback and independent certificate checking;
- explicit statuses such as `verified`, `branch-partial`,
  `backend-unavailable`, `timeout`, and `unsupported`.

No novelty claim is valid until the relevant literature has been checked.

## 5. Required execution gates

Work proceeds in this order:

1. **Research synthesis:** complete focused formal-theory and backend studies;
   inventory scalar assumptions and validation requirements.
2. **Architecture review:** present two or three approaches and compare their
   risks; review the mathematical contract, APIs, backend protocol,
   certificates, statuses, migration, tests, and paper structure section by
   section.
3. **User approval:** obtain explicit approval of the design sections.
4. **Persisted specification:** write and self-review
   `docs/superpowers/specs/2026-07-30-nd-pde-system-lie-reduction-design.md`,
   then wait for review of that file.
5. **Implementation plan:** produce a test-first, small-task plan.
6. **Implementation:** migrate the compatibility layer first, then generic
   jets/prolongation, determining/algebra logic, backend interchange,
   reduction/certificates, consumers, benchmarks, and exposition.
7. **Verification:** run the complete legacy and generic suite, compile
   `intro.tex`, inspect logs and layout, and report unsupported branches.

## 6. Immediate next work item

The next active deliverable is a research synthesis, not code. It should
return:

- formal definitions and proof obligations for R1;
- evidence-based Maple/REDUCE capability and reproducibility matrix for R2;
- scalar-assumption inventory and migration/data-flow map for R3;
- validation corpus, negative controls, and `intro.tex` insertion plan for
  R4--R5;
- two or three architecture options with a recommendation.

The three previously attempted research-agent fan-outs failed with HTTP 429
and produced no findings. They must be retried before their outputs are
treated as evidence.

## 7. Working rules

- Keep backend syntax out of the mathematical core.
- Treat polynomial-ansatz stabilization as evidence of a bounded result, not
  proof of a complete Lie algebra.
- Do not call a reduction certified merely because orbit variables disappear;
  require substitution/pullback and completed-branch normal-form checks.
- Record rankings, inequations, divisions, assumptions, backend versions,
  timeouts, and branch coverage in reproducibility artifacts.
- Preserve negative results and unsupported cases explicitly.
- Do not initialize Git, delete build artifacts, or modify production code
  without a separately authorized step.

