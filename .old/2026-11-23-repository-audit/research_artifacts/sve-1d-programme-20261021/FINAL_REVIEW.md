# Independent final review: exact-first 1D SVE programme

Review date: 21 October 2026. This review treats `PLAN.md` as the canonical
programme and checks the bounded mathematical package, its provenance, and its
claim limits. It does not treat duplicate implementation-plan or registry
validation files under `build/` as programme authority.

## Verdict

**Accepted. No mathematical blocker remains for this bounded programme.** The
package supports its stated deliverable: a provenance-bound inventory of 17
emitted Eulerian reductions, exact local identities and controls for selected
E/P/M structures, an exact-first solver programme, and a bounded decision not
to continue pure-PINN training on the current workload. Acceptance does not
mean that every registered profile has been solved or that any global or
maximal result beyond the declared gates has been proved.

## Provenance decision

The authoritative classification input is the reviewed seed-0 evidence bound
by `build/sve-general-symm-20261020/STAGE_1_GATE.json`. That gate has
`passed=true`, names eight declared positive-chart branches, and hashes all
eight `stage1-branches-seed0/*/derivation.json` files. The registry reproduces
17 traveling/scaling E reductions from those files. Every E row carries
`current_gate_status=accepted_exact_version_by_STAGE_1_GATE`; the embedded
`awaiting_necessity_review` value is explicitly identified as historical source
snapshot state, not the current verdict.

The later `stage1-branches-final` receipt is nonauthoritative. Its single
180-second `slope_source_generic` timeout is an execution failure only. It is
neither a mathematical obstruction nor evidence against the accepted seed-0
derivation. The registry records this distinction directly.

P and M entries are not silently promoted to E certificates. They are hashed
discovery pointers marked `discovery_pointer_not_executable_solver_certificate`;
the historical nine P reductions still require model-specific faithful import.
Thus E, printed scalar P, and advectively corrected scalar M remain separate
models throughout the accepted package.

## Mathematical checks

The scalar common-scaling calculation is correctly local. On the declared
positive chart, the P and M residuals satisfy their separate identities

```text
t^2 E_P = D_z(L_P F''),    t^2 E_M = D_z(L_M F'').
```

Consequently `L F'' = I0` lowers a third-order profile equation to second order
only on a connected subinterval where the corresponding model-specific pivot
`L` is nonzero. The package does not use this identity to cross `L=0`, infer
compatible arbitrary data, or transfer a scalar conclusion to E.

For the E traveling reduction, direct differentiation confirms the three
integrals

```text
H(U-c) = q,
(U-c)^2/2 + g(H+Z) = C,
K U^m - G U^n Z' - c Z = j.
```

For `G>0`, `U>0`, `U-c != 0`, positive depth, and
`D=dZ/dU != 0`, solving the third relation gives the stated separable first
order equation and exact local quadrature. Local inversion additionally
requires its numerator `N=K U^m-cZ-j` to be nonzero. The package correctly
keeps `D=0`, `N=0`, `U=c`, and the zero-transport `c=0` cases separate rather
than cancelling them. For `G=0`, the sediment relation remains algebraic; no
division by `G` is made.

The constructed E control is genuinely independent of the traveling-profile
ansatz. Direct substitution gives original-PDE residuals `(0,0,0)` on `x>-2`.
Perturbing only the bed by `epsilon*x` gives `(0,epsilon,0)`, so the negative
control exercises the momentum coupling instead of merely repeating the
positive calculation.

The saved fresh review replay
`build/sve-1d-programme-final-review-replay.json` records all 19 exact checks as
passed: two symbolic-exponent scalar identities, eight integer-exponent scalar
identities, three E traveling residuals, three exact-control residuals, and
three expected perturbation-control outcomes. Its SHA-256 is identical to the
frozen `verification.json` receipt. Before release of the symbolic CPU lease,
an independent SymPy spot recomputation also returned E control `(0,0,0)`,
perturbed control `(0,epsilon,0)`, three zero derivatives of the traveling
integrals, and quadrature inverse derivative `1`.

## Claim boundary

This acceptance does **not** establish any of the following:

- solution of an arbitrary SVE initial-boundary-value problem;
- a global solution or continuation through a singular chart or pivot;
- maximal classification of the printed scalar P or corrected scalar M model;
- completeness over all one-dimensional subalgebras, literature reductions,
  nonclassical reductions, shocks, or wet/dry interfaces;
- a learned first integral, universal neural-method failure, or universal ML
  advantage or disadvantage.

The structural vector in `STRUCTURE_MEASURES.md` correctly separates point
algebra dimension, projected orbit rank, number of usable first integrals,
singular loci, and representation-dependent complexity. The ML decision is
therefore accepted only as a workload-specific stop rule backed by the saved
negative experiments and matched-cost reopening gates.

## Canonical hash ledger

All hashes below were recomputed during this review.

```text
abcc9eaa4f6c8803f6f13a1e2cd97abdac3d1256953af9990395fb1aeeda3cc1  PLAN.md
5f46ba58e86502d0972953eda01ca2f916a29749ffa88fdde5175b712cb240e6  README.md
13533a98001868f052ced5307d8ebdfe4612551ea60e4219ef8aaa219d1e582b  REDUCTION_INVENTORY.md
b6d5a5e4bc3e09449a9753753d515e2c808d0f3ab6c247b144c5a1d54aff28d6  reduction_registry.json
34a62b400fdd2815b30a6ddf24df323666bd5a311068b2fc890e1a55b024b08f  SOLVER_DEMONSTRATION.md
b39ba05a109d94cd84cdb08e359bed4cf9d666a81bff51b8d0e19d7cafdee688  verify_structures.py
498407844923e61a12a45a24abf8f91f5b7f49a8abfc90becc64bef18143eb30  verification.json
66078e91a60a442430b0f1b692ae74ca4bd4675e2f3b912dfa168323842b746d  STRUCTURE_MEASURES.md
956ee51daff87081b00987409e5cb89329150fbe11f6bf76291816d02523f7cf  ML_DECISION.md
cdb10227b3eb88408635d68b93ef3f677a0ff3763ce1e88683c3d019771fd7eb  LITERATURE_1D.md
6cb76ba6a129aaae9508e97a6fcaea73569cc00067d12686c1784d276f696c7f  build/sve-general-symm-20261020/STAGE_1_GATE.json
05b3e734fd694cf5c8bc05afffe2f332faff6081e70dc813dfb22991d1e7f767  build/sve-general-symm-20261020/runs/stage1-branches-final/receipts.json
498407844923e61a12a45a24abf8f91f5b7f49a8abfc90becc64bef18143eb30  build/sve-1d-programme-final-review-replay.json
```

The required project audit, data-flux check, workflow runner, engine/chart
regressions, and active 43-test package are root-owned integration checks and
are not re-run by this independent reviewer. Their outcomes must be reported
separately; they do not alter the bounded mathematical verdict above unless
they expose a contradiction in these bound artifacts.
