# Printed-P numerical residual: resolved precision floor

This is a local follow-up to the frozen 21 October publication, not a rewrite
of its receipts or a new GitHub release. The research route is recorded in
[the roadmap](research-roadmap-20261021.md).

## What failed and why

For `cubic-resonant-time`, c=1, g=1, kappa=1/30, m=3, initial jet
(F,F',F'')=(2,1,1/10) at z=1, the raw float64 checker on [1,1.083] is exactly
reproduced: 1.177074994140881e-6 against the unchanged 1e-6 threshold.
The two original integrators differ by only 6.106226635438361e-15.

The diagnosis isolates surface-evaluation, interpolation and state-rounding
noise amplified by h^-3 in third derivatives. A smaller h makes that floor
worse. Merely changing summation order or interpolation can give a passing
number without resolving the underlying precision problem.

## Repair and fresh measurements

An independent 40-decimal-digit mpmath Taylor IVP reference uses the same
reduced equation, parameters, initial jet and valid interval. Exact rational
nine-point tensor weights differentiate its reconstructed position values
in the original (s,t) coordinates. No ODE RHS is substituted into the PDE
derivatives. All three predeclared h values must pass, not the most favourable
one. The perturbed reference surface must fail as a negative control.

| h | Maximum absolute original-P residual at the three sample locations |
|---|---:|
| .003 | 2.212490569e-8 |
| .002 | 1.918933563e-9 |
| .001 | 2.976602120e-11 |

These exhibit the expected sixth-order leading stencil truncation trend.
DOP853 and RKF45 agree with the reference on all three state components at
601 output nodes: respective max differences 5.635132026e-15 and
3.169096380e-15. The original tolerance remains 1e-7*(1+max_abs_reference_state).

The raw double-precision receipt is retained as `original_pde_float64` and
still says false. `original_pde` explicitly checks the independent reference
surface. This does not certify either float64 interpolant between grid points
or establish a continuous error bound. The plotted double-precision
interpolants are visualizations. General closed forms and untreated singular
continuations remain open.

## Delivery and validation

The [new delivery](../build/sve-P-residual-20261021/DELIVERY.md),
[fresh demo](../build/sve-P-residual-20261021/campaign-reviewed/index.html),
[machine-readable receipts](../build/sve-P-residual-20261021/VALIDATION.json)
and [independent review](../build/sve-P-residual-20261021/INDEPENDENT_REVIEW.md)
preserve both the failure and repair.

The fresh campaign passes 12/12 exact demonstrations, 21/21 seed IVPs and
11/11 precision-resolved extended IVPs. The six new regressions cover the
original failure, a perturbed graph, exact/negative original-P controls,
disagreeing solver states, invalid chart/nonfinite data, and reference timeout.
The independent reviewer found one budget-enforcement defect; it was
reproduced RED, fixed, and independently rechecked with no open code findings.

The missing 11 October archive is only nonblocking provenance under the
current route. The old audit is not rewritten. Broad bare pytest remains
separately limited by legacy imports and an import-time SystemExit; neither
this repair nor passing selected suites implies the whole repository is green.

Reproduce into a new directory:

```bash
export PYTHONUTF8=1 PYTHONHASHSEED=0
python -B -X utf8 -m symm.LieSymm.scalar2026.solve_demo --out build/sve-P-precision-NEW
python -B -X utf8 -m pytest -q -p no:cacheprovider symm/LieSymm/tests symm/LieSymm/scalar2026/tests
```

No manuscript or bibliography was edited, no new training campaign was run,
and no new commit or push is part of this follow-up.
