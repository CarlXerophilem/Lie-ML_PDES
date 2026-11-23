# Independent numerical review (2026-10-12)

Scope: read-only audit of `RUN_CONTRACT.md`, `rkf45.py`, `numerics.py`,
`reductions.py`, `source_formulas.py`, numerical tests, `docs/NUMERICS.md`,
and the 17-row `build/numerics-smoke/numerics.json`. This review predates
any subsequent integration or repair.

## Findings

1. **High, coverage rejected:** `numerics.py:246` excludes reduction 3.8 at
   every `m != 3`, despite `derive_reduction('3.8', exponent=m)` yielding
   `regular_ode`, `rhs=0` for each declared `m=1,3/2,2,3,4`. The graph
   `phi=alpha*s+F(t)` and residual `alpha*F'''` are independent of `m`.
   Therefore 17/17 is not all regular numbered reduction/exponent pairs;
   the declared set contains 21. Remove the 3.8 restriction and run all five
   values, or explicitly narrow the coverage claim. `table3-mixed` is a
   separate symbolic-only companion under the approved scope.

2. **Medium-high, refinement claim rejected for short rows:**
   `numerics.py:283-294` fixes `first_step=interval/2` for both tolerance
   ladder solves. Every 3.6 and 3.9 row and 3.8 has identical `[2,2]`
   accepted step counts and exactly zero endpoint disagreement in the smoke
   JSON (11/17). The two tolerances generate the same path in these rows,
   so this cannot be called a nonvacuous tolerance refinement. Use distinct
   fixed step caps or force a coarse error regime, record step histories,
   and require a distinct trajectory before claiming refinement evidence.
   The smooth exact-quadratic 3.8 case may reasonably be labeled a control.

3. **Medium, PDE refinement qualified:** `numerics.py:149-186` computes the
   original-coordinate residual by independent nine-point tensor finite
   differences; the formula agrees with `core.master`. The fixed `h=.003`
   gate is honestly stated, but `h=.002,.001` usually make the residual
   larger; these data are not convergence evidence. For 3.4, `m=3`, at
   `z=1.2`, an independent DOP853 reconstruction gave residuals
   `-4.34e-9` at `h=.01`, `-4.84e-8` at `.003`, and `-4.70e-6` at `.001`.
   State a roundoff-limited resolution diagnostic, not a convergent PDE
   residual estimate. The predeclared absolute gate still passed at `.003`.

4. **Low, diagnostics:** `rkf45.py:103-108` increments `nfev` only after all
   six stage evaluations succeed; a guard or nonfinite failure after one or
   more RHS calls undercounts actual evaluations. This does not alter states
   or completion status, but `nfev` is not reliable for failed runs.

## Claims assessed

- **Accepted:** Rational coefficients are the classical six-stage Fehlberg
  4(5) tableau; the fifth-order estimate is propagated with embedded
  fourth/fifth weighted-RMS error and a fifth-order controller. Explicit
  reject, guard, nonfinite, minimum-step and endpoint statuses exist. A
  two-dimensional reconstructed-phi finite-difference residual is genuinely
  separate from substituting the reduced RHS. DOP853 is an independent
  integrator; `rkf_pde` is explicitly labeled as a tight-RKF reconstruction.
- **Accepted on tested values:** For reductions 3.4, 3.6, 3.9 and
  `m=1,3/2,3`, the recorded first-integral density differentiates exactly
  to the reduced residual at the configured `alpha=-1`. The 3.4 two-state
  comparison is an additional, structurally distinct check.
- **Qualified:** 17 recorded local IVPs meet their implemented fixed-grid
  gates, including positive sampled margins and endpoint completion; this
  is finite-grid consistency, not continuous branch or global error proof.
  The single `phi+0.001*t^3` negative control validates sensitivity to one
  nonzero perturbation, not every derivative term. Default RKF is compared
  against DOP853; the PDE residual on an RKF trajectory uses the *tighter*
  RKF solution, which is labeled correctly.
- **Rejected until repair:** "all regular source reduction/exponent runs"
  and "nonvacuous tolerance ladder on every run".

## Evidence probes

Commands ran from the package directory in under a few seconds. Exact
symbolic differences `reduced_residual - d(first_integral)/dz` returned zero
for `m=1,3/2,3` on 3.4, 3.6 and 3.9. `derive_reduction('3.8', exponent=m)`
returned `regular_ode` and `rhs=0` for all five declared exponents. A direct
SciPy DOP853 reconstruction at 3.4, `m=3`, produced the residual-versus-`h`
values listed above. The 17-row smoke JSON showed the stated identical
two-step ladder trajectories; no source solver code was modified.

## Post-repair acceptance (2026-10-12)

The four findings above describe the *pre-repair* version. Targeted re-review
of the repaired code and regenerated `build/numerics-smoke/numerics.json`
supports **acceptance of the local numerical reproduction**, subject to the
scope qualifications below.

- **Coverage repaired:** 21/21 numbered regular case/exponent IVPs passed:
  five each for 3.4, 3.6, 3.8, 3.9, and one cubic 3.5. All five 3.8 rows
  compare to the exact quadratic solution, with maximum absolute error
  `4.440892098500626e-15`. The mixed Table 3 companion remains explicitly
  symbolic-only under the approved scope.
- **Distinct-grid check repaired:** All 21 coarse/fine Fehlberg integrations
  now have distinct accepted time histories. The traveling rows use `[2,4]`
  accepted steps and have nonzero endpoint differences of roughly
  `1.6e-13` to `7.5e-13`. The five exact-quadratic 3.8 differences are
  roundoff-level controls, not observed convergence orders. The comparison
  changes both tolerance and maximum step; it is a finite-step consistency
  comparison, **not an isolated tolerance-convergence experiment**. The
  phrase "tolerance-ladder disagreement" in `docs/NUMERICS.md` should be
  read with this qualification or renamed before publication.
- **PDE evidence remains qualified:** The largest fixed `h=.003` residuals
  are `7.984503500590989e-7` (DOP853) and `9.361751006145558e-7`
  (tight-RKF reconstruction), both below the predeclared `1e-6` gate.
  `h=.002,.001` are explicitly documented as resolution diagnostics, not
  convergence evidence. The review accepts the finite-grid pass only.
- **Diagnostics repaired:** A guard-stop probe with three actual RHS calls
  reports `nfev=3`; the failed-stage counter is now accurate for this case.
  Focused `test_rkf45.py` and `test_numerics.py` run: **13 passed**. Pytest
  then emitted a Windows temporary-directory symlink cleanup warning at
  process exit; it did not affect the test result.

SHA-256 acceptance snapshot (code and smoke JSON, in listed order):

| Artifact | SHA-256 |
| --- | --- |
| `sve_reproduce/rkf45.py` | `8B379D40AC9DE517103461C2D3A92841C629C9F39B284E46BFC25DDFD1883580` |
| `sve_reproduce/numerics.py` | `74645D4CD7FE07508828961A86A3C2E0A950694C8D2FAE57A976F206CBD24494` |
| `sve_reproduce/reductions.py` | `8D9E0F8737F83538CDD9203FAD03FA4F214D441BEC4439CEFD98AE53A931A542` |
| `sve_reproduce/source_formulas.py` | `33AF5671A39E12FE4BA3904A0B37B325CA8904CC9BCE6D1960D2BA65590B1139` |
| `build/numerics-smoke/numerics.json` | `E4EEFD6B04713BE396909B66F493F5373F9D56BC1C4D9EACBBCCC1C593B21188` |

This acceptance does not cover the source-paper equation audit or manuscript
citations, which require their separate reviews. It is not a proof of
continuous positivity, a guaranteed numerical error bound, an arbitrary
initial-boundary-value result, or a physical-data validation.
