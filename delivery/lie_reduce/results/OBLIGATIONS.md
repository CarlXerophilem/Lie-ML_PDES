# Evidence for the 43 proof obligations

Checked local symbolic reductions within declared charts and a finite point-coefficient search; a separate explicit certificate for the selected annular saddle.

**No global completeness claim.** A successfully executed check is not an independently verified theorem hypothesis outside its stated scope.

| # | Condition | Status | Evidence / limit |
|---|---|---|---|
| 1 | Equation class and parameter domain | declared | Model dimensions, orders and chart inequalities are explicit; parameter ranges are scoped. Evidence: models.py, runs[*].principal_chart |
| 2 | Smoothness / analytic branch | conditional | Fixed integer exponents yield rational analytic PDEs where denominators are nonzero; no arbitrary smooth input theorem is automated. Evidence: models.py |
| 3 | Regular equation submanifold | partial | Principal Jacobian is checked on shell; unresolved nonvanishing conditions remain explicit. Evidence: runs[*].principal_chart |
| 4 | Explicit principal chart | partial | A unique simple principal branch is checked; this is not a PDE existence theorem. Evidence: runs[*].principal_chart |
| 5 | Local solvability / differential compatibility | not_checked | No general involutive completion or analytic Cauchy theorem hypotheses checker. Evidence: none |
| 6 | Equivalent equation presentations | partial | P and M remain separate; no blanket symmetry-preserving elimination claim. Evidence: source_formula_audit |
| 7 | Declared coefficient class | scoped | Degree-two point coefficient search; unrestricted claims rely on separate proofs. Evidence: runs[*].discovery |
| 8 | Free-jet splitting and exclusions | conditional | Algebraic splitting on a regular principal chart; full formal integrability is not established. Evidence: runs[*].discovery, runs[*].principal_chart |
| 9 | Complete determining-system solution | scoped | Exact finite ansatz kernel and frozen P/M proof replay; no general Janet solver. Evidence: runs[*].discovery, frozen_PM |
| 10 | All parameter strata | partial | m=1,2,3,4 replayed; frozen all-real-m proof is separate; no multivariate CAD stratification. Evidence: coverage |
| 11 | Full prolongation sufficiency | machine_checked | Every computed finite-class generator is substituted into the full prolongation. Evidence: runs[*].discovery |
| 12 | Point-symmetry scope | declared | Point symmetries only; contact, generalized and nonclassical symmetries excluded. Evidence: scope |
| 13 | Lie closure and Jacobi | machine_checked | Closure and Jacobi checked at each instantiated stratum. Evidence: runs[*].algebra |
| 14 | Connected adjoint action | partial | Adjoint matrix construction and scaling regression; no discrete group classification. Evidence: algebra.py, test_pipeline.py |
| 15 | Optimal-system coverage and inequivalence | source_proof_only | Catalogue input is not an automatic optimality proof; E2 two-dimensional system absent. Evidence: draft/dissertation_wku_compact.tex Appendix B |
| 16 | Chart-preserving equivalence | conditional | Individual graph conditions are retained; conjugacy is not assumed to preserve the chart. Evidence: runs[*].reductions[*].value.checks |
| 17 | Projectability | conditional | Rank-one projectability is tested; explicit polar E2 action is supplied. Evidence: runs[*].reductions[*].value.checks |
| 18 | Constant orbit/base rank | conditional | Ranks require nonzero section minors; unresolved conditions restrict the local chart. Evidence: runs[*].reductions[*].value.checks |
| 19 | Transverse section | conditional | Section inverse and transverse determinant checked; no global single-intersection claim. Evidence: runs[*].reductions[*].value.checks |
| 20 | Independent complete local invariants | conditional | Local section recovers arbitrary profile data; no global invariant-coordinate theorem. Evidence: runs[*].reductions[*].value.checks |
| 21 | Invariant-surface identities | scoped | Passing reductions satisfy vector invariant-surface identities; exclusions are retained. Evidence: runs[*].reductions, E2 |
| 22 | Bidirectional residual equivalence | conditional | Identity and nonzero-weight evidence are separate; conditional factors are not universal equivalence. Evidence: runs[*].reductions[*].value.checks |
| 23 | Reduced differential-algebraic compatibility | partial | Three exact annular first integrals checked; no arbitrary DAE completion. Evidence: E2 |
| 24 | First-integral identities | scoped | Constructed fluxes must differentiate to the residual; not every equation has an integral. Evidence: runs[*].reductions[*].value.first_integrals, E2 |
| 25 | Inherited normalizer symmetries | not_checked | No machine evidence in this run establishes the full condition. Evidence: none |
| 26 | Classification of leading-coefficient zeros | not_checked | No machine evidence in this run establishes the full condition. Evidence: none |
| 27 | Compatible critical point | scoped_machine_checked | Only the c=-7 annular saddle, with two computed slopes; not a classification of all singularities. Evidence: critical_certificate |
| 28 | Holomorphic desingularization | scoped_machine_checked | Only the c=-7 annular saddle, with two computed slopes; not a classification of all singularities. Evidence: critical_certificate |
| 29 | BB normal form | scoped_machine_checked | Only the c=-7 annular saddle, with two computed slopes; not a classification of all singularities. Evidence: critical_certificate |
| 30 | All-order nonresonance | scoped_machine_checked | Only the c=-7 annular saddle, with two computed slopes; not a classification of all singularities. Evidence: critical_certificate |
| 31 | Hyperbolic saddle with nonvertical directions | scoped_machine_checked | Only the c=-7 annular saddle, with two computed slopes; not a classification of all singularities. Evidence: critical_certificate |
| 32 | Explicit complex contraction disk | scoped_machine_checked | Only the c=-7 annular saddle, with two computed slopes; not a classification of all singularities. Evidence: critical_certificate |
| 33 | Laurent balance, recurrence and convergence | not_checked | No machine evidence in this run establishes the full condition. Evidence: none |
| 34 | Regular Picard bounds | not_checked | No machine evidence in this run establishes the full condition. Evidence: none |
| 35 | Invertible physical lift | conditional | Material invertibility requires phi_s>0; polar chart requires r>0; no global inverse proof. Evidence: models.py, task_exports |
| 36 | Closed bed one-form and periods | source_proof_only | Local bed reconstruction theorem not a global period computation. Evidence: draft/dissertation_wku_compact.tex |
| 37 | All original physical balances | partial | Four E2 quotient balances and source pullbacks checked; no claim of five balances for E1/E2. Evidence: E2, source_formula_audit |
| 38 | Physical admissibility | partial | Positive-chart conditions and saddle disk guards; no added bed-thickness or Froude assumptions. Evidence: runs[*].reductions, critical_certificate |
| 39 | Invariant initial/boundary data | not_applicable | No user-prescribed physical initial/boundary value problem is solved in this stage. Evidence: none |
| 40 | Exact arithmetic | scoped_machine_checked | Exact symbolic/rational proof paths; floating quantities in timings/diagnostics are not proofs. Evidence: identities.py, critical_certificate |
| 41 | Decidable identity checks | partial | Conservative rational/algebraic normal forms and unknown status; legacy graph simplification remains chart-conditioned. Evidence: identities.py |
| 42 | Explicit failures | machine_checked | Timed stages retain explicit failure/unknown conditions; no inference of completeness from successful execution. Evidence: runs |
| 43 | Manuscript and source regressions | partial | Finite-stratum/table regressions and exact source witnesses; not an independent reproof of all manuscript theorems. Evidence: frozen_PM, source_formula_audit, tests.log |
