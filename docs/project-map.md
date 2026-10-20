# Project map — 21 October 2026

The current work is **one-dimensional SVE reduction and exact-first ODE solving**.
Start with the [1D programme](../research_artifacts/sve-1d-programme-20261021/README.md),
[registered reductions](../research_artifacts/sve-1d-programme-20261021/REDUCTION_INVENTORY.md),
and [implementation plan](../research_artifacts/sve-1d-programme-20261021/PLAN.md).

| Object | Current evidence | Next operation |
|---|---|---|
| Full Eulerian E | 8 declared 1D / 17 declared 2D maximal local point-algebra cells | Solve the registered 1D profiles, retaining singular strata |
| Printed scalar P | Source-formula audit, separate historical scalar replay | Import and check its nine source reductions before solving |
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
