# Project map — 21 October 2026

The immediate work is **verified reproduction and extension of the original
SVE paper**. The [printed-P precision repair](residual-resolution-20261021.md)
now passes the independent reference check while preserving the raw failure.
The [research roadmap](research-roadmap-20261021.md) then proceeds to controlled
changes of the full SV+bed model, a frozen LieML baseline, and source-verified
open 2D problems. These later stages are planned, not completed research claims.
The [solution API](../symm/LieSymm/scalar2026/SOLUTIONS.md) reuses the existing
classification and retains exact, series, numerical and unresolved results.
The [accepted plan](superpowers/plans/2026-10-21-sve-printed-solutions.md) governs
the printed-P solution cycle; the E programme below remains a distinct model
and supplies a later experimental starting point, not a replacement for P.
The [new local delivery](../build/sve-P-residual-20261021/DELIVERY.md) and
[fresh demo](../build/sve-P-residual-20261021/campaign-reviewed/index.html) give
12/12 exact, 21/21 seed and 11/11 reference-checked extended IVPs. The
[frozen published delivery](../build/sve-P-solutions-20261021/DELIVERY.md)
keeps the earlier 10/11 result. These demonstrations separate
exact surfaces, truncated series and numerical trajectories.
The [local LieSymm library](../symm/LieSymm/README.md) now preserves and exposes
the general-symm kernel without depending on the original build directory.
The [2026 scalar demo](../symm/LieSymm/scalar2026/README.md) processes all nine
source subsections and their eleven numbered formulas, with 21 verified local
IVPs and `(s,t,phi)` surface exports. Its corrected reductions solve printed
model P; they do not establish equivalence to E or M.

Start with the [1D programme](../research_artifacts/sve-1d-programme-20261021/README.md),
[registered reductions](../research_artifacts/sve-1d-programme-20261021/REDUCTION_INVENTORY.md),
and [implementation plan](../research_artifacts/sve-1d-programme-20261021/PLAN.md).

| Object | Current evidence | Next operation |
|---|---|---|
| Full Eulerian E | 8 declared 1D / 17 declared 2D maximal local point-algebra cells | After the source-paper demo, pose controlled SV+bed modifications and test/freeze the baseline, retaining singular strata |
| Printed scalar P | 18 registered families, exact/series/numerical examples; time-resonant reference residual 2.212490569e-8 at unchanged 1e-6 gate | Finish source-faithful demo and address recorded regular scaling/mixed closed forms and singular continuations |
| Corrected scalar M | Common-scaling first integral and local material reconstruction | Check currents, exceptional branches and additional reductions independently |

The completed [20 October delivery](../build/sve-general-symm-20261020/DELIVERY.md)
contains 64 nonclassical candidate certificates: 11 full-chart passes, 2 requiring
u!=0, and 51 failures. It found no new classically inequivalent solution family.
2D optimal-subalgebra completeness and a full equivalence groupoid remain open.
The eight 1D branch records currently emit 17 traveling/scaling certificates;
this is not every possible invariant reduction or every solution.

Pure PINN training has been abandoned for the current workload, following the
user's decision and existing negative evidence. See the [ML decision](../research_artifacts/sve-1d-programme-20261021/ML_DECISION.md).
Hybrid ML is considered only after a specific unmet task and a matched-accuracy
cost advantage can be tested. No new training campaign is part of this repair.
The user-selected local annotated PINN/KAN benchmark is a prospective protocol
reference in the roadmap; it is not a completed LieML comparison or permission
to restart pure PINN. Future 2D targets must be checked against the selected
papers before calling them unknown or novel.

## Current acceptance boundary

The missing 11 October external archive is a **nonblocking legacy-provenance
note**, not a current research gate. Preserve its old audit receipt without
spending the present research cycle on archive recovery. Current acceptance
depends on source fidelity, explicit model/chart/data assumptions, independent
original-equation reconstruction and appropriately scoped numerical checks.
General closed forms, untreated singular continuations and raw float64 stencil
failures remain explicitly recorded. The independent reference check does not
prove a continuous error bound for double-precision interpolants.

## Evidence and reproduction

- [Published library and P-solution carriers](../research_artifacts/sve-delivery-20261021/README.md); Ubuntu synchronization and restoration commands are in the root README.
- [Portable build snapshot and restore](../research_artifacts/sve-current-20261021/README.md).
- [10 October scalar experiment index](../research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md): 43-test retained benchmark.
- [Source-faithful 12 October reproduction](../research_artifacts/SVE-reproduced-20261012/README.md): use the 19 October scalar recovery adapter for its original scalar code.
- [Archive policy and current cleanup](build-archive-20261021.md).
- [Project checks](validation.md); exact current commands and results are in the refresh report linked from the documentation index.

The [manuscript](../draft/main.tex) and [dissertation](../draft/dissertation.tex)
retain their existing research scope. This cleanup does not rewrite their claims.
The dissertation still reads `build/week-4`, so that directory is retained and
included in the portable snapshot.

For the detailed theory, notation and older workflow diagrams, read the
[preserved methodology map through 19 October](methodology-map-through-20261019.md).
For other documents, use the [documentation index](README.md).
