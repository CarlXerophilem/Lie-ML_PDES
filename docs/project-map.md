# Project map — 21 October 2026

The current work is **direct solution of the 2026 printed scalar P reductions**.
The [solution API](../symm/LieSymm/scalar2026/SOLUTIONS.md) reuses the existing
classification and retains exact, series, numerical and unresolved results.
The [accepted plan](superpowers/plans/2026-10-21-sve-printed-solutions.md) governs
this cycle; the older E programme below is comparison material, not its priority.
The [direct-solution delivery](../build/sve-P-solutions-20261021/DELIVERY.md)
includes the independent review, repaired data checks and retained failures.
Its [demo](../build/sve-P-solutions-20261021/campaign-reviewed/index.html) separates
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
| Full Eulerian E | 8 declared 1D / 17 declared 2D maximal local point-algebra cells | Solve the registered 1D profiles, retaining singular strata |
| Printed scalar P | 18 registered families, cubic singular parameter integral, m=1 exact families, series and numerical examples | Resolve the recorded regular scaling/mixed closed forms, singular continuations and numerical diagnostic failure |
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
cost advantage can be tested. No new training ran in this refresh.

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
