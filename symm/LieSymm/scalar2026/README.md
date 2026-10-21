# 2026 printed scalar SVE: equation-first solutions

This subpackage reproduces the **printed scalar model P**, DOI
[10.3390/math14030433](https://doi.org/10.3390/math14030433), v3, equation (7).
The coupled Eulerian E and advectively corrected scalar M are different models.
`phi(t,s)` is particle position, not depth. The material chart has
`phi_s>0`; real powers use `phi_t>0`. A zero-velocity cubic control is labeled
separately. No pure PINN is run.

```python
from symm.LieSymm.scalar2026 import derive_reduction, compute_ode_series
r = derive_reduction('3.4', exponent=3)
print(r['residual'], r['guards'])
germ = compute_ode_series('3.4', exponent=3, order=6)
print(germ['status'], germ['polynomial'])
```

Run the complete minimal demonstration from the project root:

```powershell
python -m symm.LieSymm.scalar2026.demo --out build/sve-scalar-demo-NEW
python -B -m pytest -q symm/LieSymm/scalar2026/tests
```

The new output contains all nine source subsections, all eleven numbered
formulas (24)–(34) with their audit status, exact original-PDE checks,
21 constructed local IVPs, exact degree-six Taylor recurrences, and six
`s,t,phi` surface panels. Open `index.html`; PNG/PDF figures and NPZ grids are
standalone exports. Existing output directories and paths inside the library
are rejected. The historical source's CLI is an archival implementation, not
the safe public entrypoint; use the module command above.

Only five source subsections yield valid regular ODEs: 3.4, 3.5, 3.6, 3.8 and
3.9. The intermediate derivative equations are further reductions of those
same profiles. 3.1 is a zero-velocity identity, 3.2 is outside the PDE domain,
3.3 has no invariant graph, and 3.7 is an arbitrary-profile identity family.

The printed equations contain exact discrepancies; deriving their corrected
pullbacks from P does **not** change P into model M. Traveling cases 3.6/3.9
have an exact general parametric quadrature on `B(F')!=0`; the zero integral
affine branch is retained. 3.8 has the complete quadratic family on its
declared graph. Scaling cases have exact special solutions, local series and
numerical solutions; their general closed forms and singular continuation are
not claimed solved.

`_historical.py` is byte-identical to the recovered 12 October scalar source,
SHA256 `71224cf2e4a3ed456dc0cf9b5bb467fdf484b3ce7b4a7b7d713f649aa9747aa9`.
Source: `build/sve-autonomous-20261019/recovery/package/main.py`, matched to the
frozen original release. The current `research_artifacts/SVE-reproduced-20261012/main.py`
is Eulerian code and was not used. Private namespace imports preserve other
packages' `main` modules. `api.py` adds direct original-equation checks and an
exact parametric traveling solution; `demo.py` keeps generated outputs separate.
The old source hash is provenance, not approval of new wrapper mathematics.

Numerical validation uses the classic six-stage Fehlberg 4(5), independent
DOP853 comparison, first-integral drift, reconstructed-PDE finite differences
at three stencil sizes and a deliberately perturbed negative control.
These are finite diagnostics. Degree-six series are truncations with exact
zero coefficients through the tested residual order, without a radius bound.
Surface interpolation is used only within the solved patch and positive chart.
# Direct solution programme

The additive [solution API](SOLUTIONS.md) registers all existing representative
families and supplies exact, parametric, local-series and numerical results.
Run `python -X utf8 -m symm.LieSymm.scalar2026.solve_demo --out build/sve-P-solutions-NEW`
for the seed-paper-first extended demonstration. The original demo below remains available.

