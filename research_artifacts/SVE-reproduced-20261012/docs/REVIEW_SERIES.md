# Independent review: local series and manuscript refocus

Date: 2026-10-13. Scope: the printed scalar SVE equation, its corrected
similarity pullbacks, `compute_ode_series()`, saved degree-six series campaign,
and the refocused `draft/main.tex` and `draft/dissertation.tex`. This review
does not extend the result to the advectively corrected scalar or full bed
system. The pre-series archive and the frozen 20261010 package were not edited.

## Claim-level verdicts

| Claim | Verdict | Evidence and boundary |
|---|---|---|
| Regular positive-chart similarity IVPs have analytic local profile germs | **Accepted locally.** | The corrected residual is analytic near a fixed real jet with `g,kappa>0`, `m>=1`, positive original velocity and gradient, and nonzero coefficient of `F'''`. Noninteger powers are analytic on this strictly positive branch. The normal-form analytic ODE theorem gives a unique germ for each specified triple. It gives no global continuation, numerical radius, or arbitrary-data theorem. Teschl section 4.1 is recorded in `results/series-validation/analytic-ode-source.json`. |
| The Taylor recurrence and degree-six corrected-residual checks are exact | **Accepted.** | The triangular recurrence uses only coefficients through `a_(n+2)`. The final polynomial is checked against the undivided corrected residual, not merely its divided normal form. The final JSON has 21/21 regular rows with exact zero coefficients through degree three. Fractional `m=3/2` coefficients remain algebraic and exact. These are finite coefficient identities plus the separate analytic-germ theorem, not a computed error constant or radius. |
| The displayed X4 cubic series is independently consistent | **Accepted.** | From the independent first integral `I=C K`, `K=-z^3 P+gz/P^2+gm kappa z(F-zP)^(m-1)/P`, the stated initial jet gives `K=79/20` and `F'''=-11/395`, hence `a3=-11/2370`. Expanding `I'` one order farther gives `[h]I'=474 a4/5-123111/197500`, hence `a4=41037/6241000`, independently matching the saved coefficient. The exact 3.8 quadratic is a separate terminating branch. |
| Every numbered similarity row has a regular three-jet IVP | **Rejected.** | Rows 3.1, 3.2, 3.3, and 3.7 are respectively outside the positive-velocity chart, undefined at `phi_s=0`, without an invariant graph, and an identity family. The API types these outcomes. `A=0` is `normal_form_singular`, not a nonexistence proof; the checked cubic power law is a singular-branch solution. |
| Saved Taylor-versus-RKF45/DOP853 differences establish a convergence radius or certified remainder | **Rejected.** | The comparisons are finite, floating-grid diagnostics only. The final campaign has 21/21 provenance-matched references and 252 component rows at four nodes per IVP; 118 component comparisons are below the operational resolution threshold. The X4 cubic profile error at offset 0.025 is at floating precision, not an order measurement. |
| The numerical comparison refers to the same IVP and corrected equation | **Accepted for the final saved campaign, qualified as a receipt check.** | Each numerical receipt binds model, exponent, `g`, `kappa`, interval, initial jet, corrected symbolic ODE fingerprint and CSV SHA-256. The series comparison checks these, the first grid node, finite numeric columns, increasing coordinates, and the four requested existing nodes. Mismatched or absent provenance yields no samples. This does not certify the numerical reference's continuous error. |
| The dissertation now reports a learned ODE-order reduction | **Rejected.** | Both manuscripts explicitly propose this as future work. Their `D_z I=0`, nonconstancy, independence and `I_C != 0` gates distinguish a proved order-lowering first integral from a learned profile fit. The SVE first integrals reported here are exact classical calculations, not learned outputs. |
| The narrative follows the requested order and scope | **Accepted.** | Both abstracts and opening chapters lead with replication/corrected solutions, then derive an infinitesimal Lie-point reducer from arbitrary `tau,xi,eta` and the original PDE master equation, then propose ML-assisted ODE order reduction. The implementation claim is SVE-specific; an arbitrary-PDE unrestricted solver is not claimed. Lagrange coordinates, parameter/orbit-rank strata, and task-dependent trivial-symmetry filtration are named and qualified. Hybrid design and conservation analogies are deferred. The main bibliography contracts from 52 to 19 entries without treating the removed citations as deleted sources. |

## Independent checks

- Ran `python -B -m pytest -q -p no:cacheprovider --basetemp build/series-review-pytest research_artifacts/SVE-reproduced-20261012/tests/test_series.py`: **17 passed in 9.17 s** before the final malformed-grid guards were added. The earlier 15-test run also passed but emitted a Windows pytest atexit temp-symlink permission warning; the explicit `--basetemp` run did not.
- Inspected the final added malformed-reference controls for nonnumeric, `nan`, and `inf` payloads even with a recomputed matching CSV hash. Their parser path returns `reference_grid_invalid` with no samples. The director's later focused run is recorded in `build/series-final-focused.log`: **20 passed in 9.39 s**. This final 20-test run was not my own execution.
- Independently evaluated the X4 first-integral coefficients above with SymPy, without calling `compute_ode_series()` or the package's reduced ODE. Also inspected guards for noninteger exponents, negative X4 invariant coordinate, small positive slope, SymPy Float, singular leading factor, identity rows and `alpha3=0` in 3.6.
- Parsed final `results/series/series.json`, `results/series/series_comparison.csv`, and `results/numerical/numerics.json`: 21 exact passed rows, 21 provenance-matched comparisons, 252 comparison component rows, and 21/21 numerical receipts with equation and CSV hashes. The saved source table's five cubic leading factors and first coefficients agree with the corrected pullbacks and the traveling first-integral formula.
- Read the final native logs `build/latex/main.log` and `build/dissertation/dissertation.log`: output PDFs have 33 and 47 pages; no unresolved citation/reference or overfull-box warnings were found. The director visually inspected changed pages; I checked logs, not every rendered page. The director's final `main.py --trace full` campaign exited zero and regenerated the 21 matched receipts; I checked the saved outputs, not a second full campaign.

## Limits and release note

The focused series result is accepted within the declared local printed-scalar
scope. The project audit separately reports 218 pre-existing issues: 146
tracked temporary files, 41 Markdown-link issues, 30 canonical-reference
mismatches and one unavailable external archive. The director's broader
regression run reported 165 passed and one pre-existing Windows CRLF fixture
hash mismatch. Neither negative check is concealed by the 20 passing focused
series tests. The full regression suite was not independently rerun here.
Keep the audit receipt, singular statuses, unresolved sampled comparisons,
and source-formula discrepancies visible in the release.
