# What the reproduction computes

The default `python main.py` performs new calculations. It does not read
`evidence.json` or stored trajectories as substitutes for those calculations.
It writes symbolic traces, exact certificates, numerical CSVs, convergence
experiments and static figures. The HTML template, viewer data packaging,
viewer CLI and generated `solutions.html` have been removed; the previous
viewer is retained only in the pre-edit archive.

| Object | Live calculation | Authored inputs / scope |
|---|---|---|
| Master equation | `total()` differentiates the two currents; `build_model_report()` computes coordinate pullbacks and compatibility differences. | The balances, constitutive law and choice of printed scalar model are mathematical inputs. |
| Infinitesimal symmetries | Recursive third prolongation, arbitrary-function determining coefficients and generator defects are computed with SymPy. | The split sequence and integration of the determining conditions are guided by the documented mathematical derivation. This is not a general autonomous PDE-classification engine. |
| Lie algebra and Table 2 | Coordinate brackets, Jacobi identities and adjoint actions are computed; all 25 Table 2 cells are compared with source transcriptions. | The listed source fields and Table 2 formulas are inputs. Optimal-system representatives and chart arguments are hand-derived from the computed actions, not discovered by an orbit-classification algorithm. |
| Nine reductions | `derive_reduction()` constructs profile jets/residuals. `verify_reduction_pullbacks()` independently differentiates the invariant graphs and substitutes every jet into `master()`. | Nine chosen graphs and the campaign exponents are inputs; the two-variable multiplier identities are checked symbolically, retaining time for scaling/traveling graphs. |
| First integrals | The total derivative of each supplied candidate is compared with the corrected ODE residual for symbolic m. | The candidate integral is supplied analytically; verification is computed. This is not learned integral discovery. |
| Source discrepancies | Source equations are solved/substituted at exact witness jets. A verdict requires an actual nonzero residual or mismatch; zero tests of the printed formulas are also recorded. | Source formulas and witness choices are transcribed inputs. The PDF text is extracted and hashed, not automatically converted into all mathematical formulas. |
| Numerical profiles | The six-stage Fehlberg 4(5) integrator evaluates the generated RHS; DOP853, original-PDE finite differences and first-integral solves give separate checks. | Constants, tolerances and constructed IVP data are explicitly chosen. They are not the source paper's numerical experiments. |
| Series and convergence | Taylor coefficients and undivided residual coefficients are calculated exactly; fresh fixed-step and adaptive sweeps produce endpoint comparisons. | A completed sweep is not automatically a resolved convergence order. A finite polynomial or small measured difference is not a radius/error certificate. |

The direct graph audit contains 25 entries: the 21 regular campaign IVPs
and four distinct nonregular/identity rows. The 3.4 and 3.5 checks retain the
symbolic multipliers T^-2 and T^-1, respectively, on T>0. Traveling checks
use the declared alpha=-1 examples; they do not test every possible group
parameter. Three additional first-integral identities use symbolic m.

Failure of the named model/symmetry checks, Table 2 comparisons, independent
pullbacks, integral identities or source-witness tests makes the symbolic
CLI gate fail. Source disagreement is expected and remains distinct from a
failed calculation. The numerical and series gates are evaluated separately.

`--stage report` only formats saved results: it says so explicitly and
refuses results with a different/missing recorded code hash. It is not a
fresh calculation. `--stage plots` reads hash-matched numerical data and
computes Taylor comparisons and separate second-order solves; use the default
full run when fresh numerical trajectories are required. Missing source PDFs
set `complete_audit=false` even if the computations themselves succeed.

The computation revision was also run from a copied `main.py` with an empty
output directory. Negative controls alter the master equation and an adjoint
sign and require the calculated checks to fail; another control supplies a
new initial jet and checks its newly integrated/derived solution. Receipts
and limitations are in `COMPUTATION_VALIDATION.md`.
