# Shared repairs and mathematical effects

Historical source and failure receipts are preserved. The active implementation is `symm/LieSymm/strict.py`; the native runner is `scripts/run_strict_lie.py`.

| Minimal counterexample | Repair | Mathematical effect / evidence |
|---|---|---|
| A native Linux command contains `wsl` | Select native argv and native paths; preserve the WSL path on Windows | Runtime portability, not a new symmetry. Native fixture and live Priestess tests |
| Change a chart guard but keep the PDE | Hash the entire mathematical input, including SymPy assumptions, guards and data | Prevent stale evidence being attached to a different domain |
| `f=0` with f absent from symbolic parameters; `u_t>0` | Bind fixed parameters and first jets explicitly | Unknown conditions are no longer silently confused with fixed equalities |
| Swap two CRACK terminal branches and rename/rescale free constants | Match families by assignments or finite linear span; retain rank minors and reject ambiguity | Conditions are attached to the correct family; coverage remains unproved |
| A remaining budget of 0.15 seconds; backend exits 124 | Allow positive budgets up to 1800 seconds and preserve timeout status | Serial cumulative-budget accounting; timeout never means no solution |
| Direct CRACK input must retain all original function arguments | Serialize the independently split determining equations with explicit dependencies | No polynomial-degree ansatz or supplied generator basis |
| Fixed f and a terminal m−1≠0 condition disappear during reduction | Reuse guard_environment and pull back inherited CRACK/rank guards | Two observed failed tests, then passing regressions; all 29 receipts revalidated |
| Positive-velocity slope transport has an unnormalized symbolic pullback | Expand independent residuals and simplify powers using declared positive bases | Five historical unresolved expressions become exact zeros. Raw expressions retained; derivative-defect negative control retained |
| A CRACK four-list terminal result enters a LIEPDE three-list parser | Select the correct result grammar and retain inequations | Observed missing-adapter test then pass; running controller's original receipt is never rewritten |

The final review also repaired three shared boundaries: supplementary reducers now verify the full mathematical-input and CAS-script fingerprints before replay; they inherit terminal/rank conditions; and serial runners stop immediately after an unconfirmed process cleanup, preserving the failure receipt and running marker. Five failing regressions preceded these fixes.

The native generic result exposed one further counterexample: `eta_B=c/(m-2)` passed residual checks without recording its parameter pole. A failing regression preceded the shared `CAS_assignment_denominator` guard fix. The same guards now propagate into reduction. The direct-CRACK mode of `analyze_strict` uses the same independent verifier as LIEPDE and preserves raw four-list output. Its generic Grass family passes only on the retained chart; separate m=1,2 solves remain incomplete.

Tests live in `scripts/tests/test_strict_completion.py` and `scripts/tests/test_strict_release.py`. This round added twenty tests, alongside existing strict negative controls. The final active suite contains 346 passing tests; the native focused suite contains 49 passing tests. Log hashes and exact commands are retained with the experiment evidence. These are software checks, not a count of fully classified PDEs.

Earlier shared repairs (mixed-shell row ordering, WSL group termination, duplicate assignments, elementary-function parsing, graph substitution, explicit-coordinate pullback and affine characteristic pivots) remain documented in the preserved 26 October independent review. No frozen `_snapshot` implementation was edited.
