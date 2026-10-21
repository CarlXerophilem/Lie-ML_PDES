# Printed P: direct solution API

The seed is Paliathanasis, Leon and Leach, *Mathematics* 14 (2026), 433,
DOI 10.3390/math14030433, v3. Printed reduced formulas are audited separately.
Every new reduction starts from printed PDE (7); E and corrected M remain
different models. The existing classification is reused, not recomputed.

```python
from symm.LieSymm.scalar2026 import solution_catalog, solve_reduction, verify_solution

catalog = solution_catalog()  # continuous symbolic parameters, 18 registry records
solution = solve_reduction('paper-3.4', parameters={'m': 3},
                           data={'branch': 'singular'})
certificate = verify_solution(solution)
assert certificate['exact_passed']
```

`catalog` owns representatives, invariant graphs, all jets and undivided
residuals. `solving` owns exact formulas, parameter integrals, first integrals,
exceptional branches, initial-data checks and exact local recurrences.
`validation` independently differentiates graphs in the original PDE;
`continuation` compares DOP853 and classic Fehlberg 4(5), then differentiates
reconstructed position samples without inserting an ODE right-hand side.

### Precision-resolved numerical checks

The old time-resonant float64 check has a confirmed h^-3 amplified
evaluation/interpolation noise floor. It is retained as `original_pde_float64`,
including its original failures. It is not silently relabelled as passing.

`precision` constructs an independent mpmath Taylor IVP reference at 40 decimal
digits (`tol=1e-30`, degree 20), with the same model, parameters and initial
jet. `original_pde` now differentiates that reference's original-coordinate
position values using exact rational 9x9 stencil weights. All three fixed
steps .003, .002, .001 must satisfy the unchanged 1e-6 residual threshold,
positive-chart checks and the perturbed-surface negative control.

Acceptance additionally requires every integrated state component of DOP853
and RKF45 to agree with the reference on the output grid within
1e-7*(1+max_abs_reference_state). `reference-profile.csv` stores reference
states rounded to double for inspection, not for the high-precision stencil.
Reference failure, timeout or disagreement cannot count as acceptance.

This checks the reference reconstruction and sampled solver agreement. It
does not certify the PDE residual of either float64 interpolant or prove a
continuous error bound. The demo's interpolated numerical surfaces remain
visualizations. The frozen seed-paper numerical engine remains byte-identical
and retains its separately reported historical diagnostics.

## Inputs and statuses

Use `parameters={'g': ..., 'kappa': ..., 'm': ...}` and the representative's
parameters shown by the catalog. Defaults are g=1, kappa=1/30, m=3; m1
representatives default to m=1. Symbolic parameters require the displayed
real/positive branch assumptions. sigma has the connected-orbit signs +/-1.

`data` accepts `branch`, `I0`, `F0`, `p0`, `z0`, `jet`, `order`, `bed_datum`,
and `bed_profile`. Default branch is `regular`. Traveling families also
accept `affine`; common scaling accepts `affine`, cubic `singular`, and
cubic `power`. Unsupported selections raise an error.

An initial jet contains (F,F',F'') for a third-order ODE and (F,F') for a
second-order ODE. Supplying three entries to a second-order ODE additionally
requires that its residual vanish. An initial jet binds the quadrature's
reference values and determines I0; inconsistent supplied constants fail.
Exact affine/logarithmic profiles bind their constants to that jet. Cubic
singular/power branches require I0=0; their initial derivatives are checked
against the selected representation independently of the reduced ODE.
Ordinary Taylor and numerical solvers do not accept zero-leading-coefficient
data. Initial derivatives do not impose arbitrary initial or boundary functions.

For an explicit graph, `bed_datum=(t0,s0,b0)` and `bed_profile` (a SymPy
expression in the catalog's s symbol at t=t0) can check the printed bed
trace and additive constant. Bed reconstruction requires a simply connected
local chart or zero periods. Parametric bed reconstruction remains specified
by the closed differential form; explicit bed traces for those representations
are not automatically solved.
Supplied parametric bed data therefore return `data_status='unsupported'`
and cannot yield `exact_passed=True`. Explicit bed anchors must satisfy the
positive chart. Symbolically undecided initial constraints remain conditional.

Results distinguish `exact_arbitrary_function`, `exact_affine`,
`exact_quadratic`, `exact_logarithmic`, `exact_power`,
`exact_parametric_quadrature`, `first_integral_reduced`,
`autonomous_order_reduction`, `unresolved_ode`, `undefined_pde`,
`outside_positive_chart`, and `no_invariant_graph`. A reduction certificate
is not an exact solution certificate. `exact_passed` is conditional on the
listed domain; `reduction_passed` certifies the invariant graph and residual.

## Reproduce

```powershell
python -B -X utf8 -m symm.LieSymm.scalar2026.solve_demo --out build/sve-P-solutions-NEW
python -B -X utf8 -m pytest -q -p no:cacheprovider symm/LieSymm/scalar2026/tests
```

Use a new output directory. The demonstration starts with the nine source
subsections, then adds m=1 and cubic mixed/resonant families. All numerical
initial data are constructed. Failed longer continuations are retained
even when a shorter local interval passes. The method does not infer that
a numerical failure proves nonexistence or a shock.

The 3.4 cubic singular family has an exact parameter integral and a separate
power equilibrium. General regular scaling closed forms, mixed/resonant
closed forms and general singular continuation remain unresolved. Numerical
residuals and plots are finite diagnostics, not continuous error bounds.
Numerical stage guards retain the initial sign of the highest coefficient;
this detects the tested sign-changing crossing, without proving continuous
nonvanishing between every finite sample.
The surfaces have axes s,t,phi: material label, time and particle position.

All historical entrypoints and byte-pinned backend files are preserved.
