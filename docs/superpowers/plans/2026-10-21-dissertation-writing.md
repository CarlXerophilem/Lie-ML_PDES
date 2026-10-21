# Dissertation Writing: Title, Outline And Evidence Map

## Scope And Stop Condition

The next task is a planning pass for the existing
[draft/dissertation.tex](../../../draft/dissertation.tex), not a replacement
manuscript and not permission to write chapter prose. Deliver only a provisional
title, chapter/section outline, and source-question-evidence map. Stop for review
before manuscript or bibliography edits, new experiments, training or agent launch.

**Provisional title:** Verified Lie Symmetry Reduction and Solution Reconstruction
for SVE-Type Models.

The title is deliberately broader than the exceptional m=3 stratum but does not
promise all solutions, global well-posedness, arbitrary-PDE classification or a
demonstrated ML advantage. Do not change the manuscript's title in this task.

## Inputs And Evidence Rules

Read the [root entrypoint](../../../README.md), [current map](../../project-map.md),
[main manuscript](../../../draft/main.tex), existing dissertation and
[retained experiment index](../../../research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md).
Use the [research roadmap](../../research-roadmap-20261021.md) for future scope
and the [Priestess handoff](../../priestess-handoff.md) for portable execution.

- Keep P (2026 printed scalar), E (full Eulerian SV+bed) and M (corrected scalar)
  separate. Any transfer requires an independently checked certificate.
- Distinguish reproduced source formula, independently verified correction,
  constructed exact/IVP extension, numerical diagnostic, negative result and plan.
- State parameter strata, nonzero denominators, positive local chart, data and
  continuation limits. A registered catalogue is not maximal classification.
- Separate variable compression, ODE-order reduction and solution reconstruction.
- Re-open the exact cited source pages before final wording. A DOI, abstract,
  search result or this plan is not evidence that a particular open problem exists.
- Pure PINN remains stopped. The benchmark reference informs prospective protocol
  design only; any hybrid learning component needs a separate unmet-task gate.
- Preserve frozen receipts. The missing 11 October external archive is nonblocking
  history, not a condition for planning or writing the current dissertation.

## Proposed Outline

| Part | Intended contents | Evidence / status |
|---|---|---|
| Title | The provisional title above; state local verified scope | Planning only; no title change yet |
| Introduction | SVE model questions; Lie algebra as variable compression; research questions and precise contributions/non-claims | Named source context plus completed P evidence; later E/2D route explicitly prospective |
| Main sections | First principles: jets, prolongation, determining identities, parameter strata, invariant graphs, charts/data; then distinct P/E/M contracts; printed-versus-verified reductions; reconstruction and first integrals | Standard theory attributed; implemented and certified cases tied to exact source/evidence entries |
| Experiments and algorithms | Reproducible generator/reduction/reconstruction pipeline; exact controls; series/local IVPs; independent residual/reference checks; negative controls, tolerances, budgets and provenance | Current code and receipts, not private calculations or a promised generic solver |
| Results and inspirations | Accepted exact and numerical findings; source discrepancies; unresolved closed forms/singular branches; lessons from negative ML results; controlled E baseline and source-verified 2D questions as future work | Completed/future labels on every proposed subsection; no assumed superiority or unrestricted obstruction |
| Citations | Source edition/page/equation locators; primary SVE papers; standard Lie theory; future-protocol comparator | Verify metadata and final rendered citations before later manuscript delivery |

Preserve the existing dissertation's useful derivations and distinctive teaching
sequence. First inventory what it already contains and what only main.tex or
current artifacts contain; do not assume the two manuscripts are synchronized.
Tables should expose generators, invariants, ansatz, reduced equation, guards,
solution type and original-equation check without copying another model's
source-specific parameters or transformations.

## Source-Question-Evidence Map

These locators bound the next reading pass. They are not declarations that the
suggested future questions remain open in the complete literature.

| Source and locator | Question to map | Available project evidence | Status / required next check |
|---|---|---|---|
| Paliathanasis, Leon and Leach (2026), DOI [10.3390/math14030433](https://doi.org/10.3390/math14030433), p. 9, section 4; master PDE and reduction tables elsewhere in the same source | What is printed, what actually reconstructs P, and what do the variational/Lagrangian and IVP statements establish? | [source reproduction](../../../research_artifacts/SVE-reproduced-20261012/README.md), [current P API](../../../symm/LieSymm/scalar2026/SOLUTIONS.md), [precision explanation](../../residual-resolution-20261021.md) | Source discrepancies and constructed IVPs must remain explicit; clarify variational-action versus material-coordinate language and missing/ambiguous IVP specification, not silently repair it |
| Paliathanasis (2022), DOI [10.3390/sym14081679](https://doi.org/10.3390/sym14081679), p. 10, section 5 | Which extensions to general Q(u,h), conservation currents and model classes does the paper propose? | [1D literature audit](../../../research_artifacts/sve-1d-programme-20261021/LITERATURE_1D.md), [E programme](../../../research_artifacts/sve-1d-programme-20261021/README.md) | E, not P; re-read exact future-work/current statements and test any proposed closure separately |
| Fernandez-Nieto et al. (2017), DOI [10.1051/m2an/2016018](https://doi.org/10.1051/m2an/2016018) | What 2D energy/closure structure already exists, and which model would a proposed extension actually change? | Existing model-provenance distinctions and source literature ledger | Prior art already includes 2D energy work; do not present dimensional extension or an energy law alone as novel |
| 2019 JFM source, DOI [10.1017/jfm.2019.166](https://doi.org/10.1017/jfm.2019.166), pp. 486-488 | Which closure or well-posedness questions are precisely posed, under what assumptions, and are they still unresolved? | Source locator for a bounded reading/literature pass; no new accepted result in this cleanup | Future candidate only; present open status is unverified and must be checked against later literature before selecting an experiment |
| Unified PINN/KAN benchmark, [arXiv:2602.15068v1](https://arxiv.org/abs/2602.15068v1), local annotated PDF under ref/ | Which accuracy/cost, baseline, budget and reproducibility rules should a later comparison adopt? | [three-stage roadmap](../../research-roadmap-20261021.md), stopped-PINN decision and retained negative approximation evidence | Protocol reference only, not an SVE result or evidence of LieML superiority; does not restart training |

For each row in the delivered map, record source version, page/section/equation,
literal source question, P/E/M contract, completed evidence path, exact versus
numerical status, missing step and a falsifiable next test. Mark unsupported,
unavailable, contradicted, implementation-limited and genuinely unresolved
questions separately. Search failure alone never proves absence or novelty.

## Completed Versus Future Evidence

| Completed / retained | Not established by these results |
|---|---|
| P source audit and 18-family processing catalogue; exact/series/numerical/no-graph/undefined/out-of-chart statuses | All nonlinear P solutions, complete closed forms or singular continuation |
| 12/12 exact demonstrations and 21/21 constructed seed IVPs | Arbitrary initial/boundary-data or global PDE existence |
| 11/11 high-precision-reference extended checks at unchanged 1e-6 gate; frozen raw float64 campaign remains 10/11 | A continuous error theorem for the float64 interpolants |
| Declared E 1D/2D local algebra cells and registered reductions; separate M controls | Automatic maximal classification for arbitrary PDEs or P/E/M equivalence |
| Negative bounded neural evidence and successful classical controls on their recorded tasks | ML speedup, a learned first integral or neural superiority |
| A research route from P reproduction to controlled E baseline to verified 2D targets | Completion of the later baseline campaign or proof that a selected 2D question is still open |

The new precision evidence is the 401-file carrier
research_artifacts/sve-P-residual-20261021/precision-evidence.zip, with source
baseline 11fe2a8. Older current/delivery carriers and failed receipts stay frozen.
Historical package stubs and restoration instructions are in the project map;
archive expansion is not required for this planning pass.

## Acceptance Checklist

- [ ] Inspect existing dissertation structure and list only necessary changes.
- [ ] Deliver the title, outline and source-question-evidence map, with no chapter prose.
- [ ] Re-open source locators and verify citation metadata before accepting source claims.
- [ ] Tag every proposed result as completed, exact, numerical, negative, restricted or future.
- [ ] Preserve P/E/M, chart/data/parameter and reduction/order distinctions.
- [ ] Identify any unverified open-problem status without filling it with speculation.
- [ ] Stop for user review before manuscript edits or new execution.

Later approved manuscript work must build with native Windows latexmk, inspect
final citation/reference warnings and rendered pages, and retain build/week-4
inputs used by the existing dissertation. No remote TeX installation or sudo
assumption is part of this next task.
