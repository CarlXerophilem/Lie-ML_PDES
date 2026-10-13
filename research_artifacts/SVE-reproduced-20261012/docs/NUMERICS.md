# Numerical SVE reproduction

## Scope and interface

Run from this package directory:

```powershell
python -B -c "from sve_reproduce.numerics import run_campaign; print(run_campaign('build/numerics')['all_passed'])"
python -B -m pytest -q -p no:cacheprovider tests/test_rkf45.py tests/test_numerics.py
```

`run_campaign(out_dir, rtol=1e-9, atol=1e-11, selected_reduction='all',
selected_case='all')` writes `numerics.json`, one CSV and one PNG per regular
run. `selected_reduction` names a section (`3.1` to `3.9`, or `table3-mixed`);
`selected_case` is the exponent `m` in `1, 1.5, 2, 3, 4`. The default contains
21 regular IVPs: five exponents each for 3.4, 3.6, 3.8 and 3.9, plus cubic
3.5. It also records nonnumerical rows and incompatible parameter
combinations separately. A requested unsupported name is an input error.

These are new dimensionless initial-value demonstrations for the **printed
scalar** equation, not measured flow data and not arbitrary boundary-value
solutions. Set `g=1`, `kappa=1/30`, `beta=m*kappa`. The nonlinear initial jet
is `(F,F',F'')=(2,0.5,0.1)` at `z=1`; 3.4 uses `[1,1.4]`, the others
`[1,1.1]`. Traveling rows use `alpha=-1`; 3.9 also uses `alpha3=1`. The
linear 3.8 rows use `alpha=1`, `(0,1,0.1)` at `t=0`, and `[0,0.4]`.

## Integrator and checks

`rkf45.py` declares the rational six-stage classic Fehlberg tableau. Its
fifth-order state is accepted, while the fourth/fifth difference gives a
weighted RMS local error with scale `atol + rtol*max(|y_n|,|y_{n+1}|)`.
The controller uses safety `0.9`, exponent `-1/5`, and factor clamp
`[0.2,5]`. Defaults are `rtol=1e-9`, `atol=1e-11`. It bounds accepted steps,
rejections and minimum steps; checks finite stage/state values and branch
guards at every stage and accepted endpoint. The solver returns typed stop
statuses. `scipy.integrate.RK45` is not used or identified as Fehlberg;
SciPy `DOP853` is a separate tight-reference comparator.

Every run records endpoint completion, regular leading coefficient and
positive velocity/gradient at all 81 sampled RKF states. A separate
coarse-versus-tight RKF endpoint integration uses distinct half-interval and
quarter-interval maximum steps and retains both accepted time histories.
Roundoff-level differences are labeled controls, not observed convergence
orders. The exponential IVP test separately checks fifth-order global error.
The 3.8 rows also compare against the exact quadratic
`F(t)=F0+P0*t+C0*t^2/2`. Certified first integrals are checked only
for 3.4, 3.6 and 3.9; the other rows report
`no_certified_integral`. For 3.4, the certified X4 integral is additionally
used to solve an independent two-state system and compare it with the
three-state profile. These tests establish consistency of the declared
local IVP, not global existence or a continuous error certificate.

The PDE check reconstructs `phi(t,s)` from the symbolic ansatz and samples
the original two-dimensional coordinates. A nine-point tensor finite
difference stencil estimates the derivatives of `phi` directly, including
third derivatives, and evaluates the printed divergence-form scalar PDE.
It never substitutes the reduced residual or RHS for the PDE residual.
One check reconstructs from the DOP853 dense profile; a second uses local
degree-11 barycentric interpolation of a tight RKF profile. Each trajectory
is labeled in JSON; the barycentric weight-order seed is fixed at `0` for
repeatable third-derivative diagnostics. The predeclared acceptance stencil
is `h=0.003` at three interior points, with `h=0.002` and `h=0.001` retained
as resolution diagnostics, not monotone convergence evidence.
The pass threshold is `1e-6` at **the fixed acceptance stencil**, not the
minimum of the three. Smaller stencils can worsen through cancellation of
third derivatives: the reported `error_floor` is an observed finite-grid
minimum, not proof of asymptotic convergence. An added `0.001*t^3` field
perturbation must change the PDE residual by more than `1e-4`; this is a
negative control that detects a vacuous residual checker.

The remaining pass thresholds are `1e-7` for scaled RKF/DOP853 state
disagreement, RKF joint tolerance/maximum-step disagreement, certified-integral drift,
and the 3.4 two-state/three-state comparison. Failure or unavailable
branches remain explicit rows; they are not omitted to make `all_passed`
true. This finite sampling does not certify positivity between samples.

## Bounded run evidence

The 2026-10-12 smoke run at `build/numerics-smoke/numerics.json` finished
21/21 regular rows under the listed gates. The largest scaled RKF/DOP853
state disagreement was `1.09e-13`. The largest fixed-stencil original-PDE
residual was `7.98e-7` on the DOP853 reconstruction and `9.36e-7` on
the tight-RKF reconstruction. The largest certified-integral drift was
`7.33e-15`; the largest X4 two-state/three-state disagreement was
`2.44e-15`. The independent coarse/tight RKF endpoint ladder differed by
at most `2.53e-10`; all histories differed, while five exact-quadratic 3.8
rows were roundoff-level controls. The maximum exact-quadratic error was
`4.44e-15`. Minimum sampled velocity and gradient were both `0.5`, and
the minimum absolute leading coefficient was `1`. The smallest
negative-control residual change was `0.00241`. These figures are measured
on the finite grid, not rigorous error bounds. The run JSON retains every
stencil value; for many rows the finest `h=0.001` value is worse than the
acceptance value due to numerical differentiation roundoff.

The cited reference PDF, *Two parameters Liegroup analysis and numerical
solution of unsteady free convective flow of non-Newtonian fluid* in `ref/`,
reports Runge-Kutta-Fehlberg fourth/fifth order **with shooting** for a
different boundary-value fluid problem. Its abstract does not specify
tolerances for these SVE IVPs and supplies no SVE boundary data. The method
name motivates an integrator choice only; this package does not reproduce
that paper's BVP or infer its numerical accuracy.
