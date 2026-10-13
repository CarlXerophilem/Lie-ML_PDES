# Independent computation review (2026-10-13)

## Verdict

Accepted as an executable, computation-only reproduction of the **printed scalar**
SVE equation on its declared regular charts. The release candidate recomputes
symbolic identities, source counterexamples, constructed IVPs, Taylor recurrences,
and finite numerical diagnostics. It is not automatic discovery of every source
formula or orbit representative, and it is not a full bed-field or arbitrary-data
result. No release-blocking computation defect was found in this review.

## Live checks and negative controls

- The copied `main.py` clean run in `build/computation-portable/results/` finished
  in 20.22 seconds with `symbolic_passed=true`, `numerical_passed=true`, and
  `complete_audit=true`. Its source manifest records local primary-PDF checks.
  The directory has no HTML output.
- Table 2 has 25 entrywise computed adjoint-versus-transcription comparisons.
  An in-memory sign corruption of `Ad(X1)X4` changed its status to `disagrees`;
  the cell difference was `2*eps`.
- The nine subsection cases yield 25 verification rows: 23 direct
  original-master substitutions and two typed no-graph/undefined-chart cases,
  with five numerical exponents where applicable. Scaling checks retain the
  symbolic time multiplier, not only a single section. Three first-integral
  derivatives equal the corrected
  residuals for symbolic `m`. Adding 1 to the case 3.9 reduced residual in
  memory failed all five of its pullbacks and its first-integral check.
- Source equations (24)--(34) have computed witness gates; (32) is qualified,
  and the other ten are refuted as printed for the recorded jets/parameters.
  Flipping `eq25.audit_verified` in a copy of saved evidence made
  `symbolic_certificate_summary` fail with the named path. The report-only CLI
  identifies itself as formatting saved evidence and rejects a mismatched
  `main.py` code hash; it is not presented as fresh computation.
- All 21 numerical rows passed freshly executed Fehlberg, DOP853, branch,
  finite original-coordinate PDE, negative-control, and applicable integral
  gates. The maximum accepted finite-difference PDE residual was
  `7.99e-7` for DOP853 reconstruction and `9.37e-7` for RKF reconstruction,
  under the declared `1e-6` gate. All 21 exact local series recurrences passed
  residual-coefficient checks and matched provenance-bound numerical grids.
  All 21 convergence campaigns completed; 16 had resolved fixed-step pairwise
  orders, while the five exact-quadratic 3.8 cases were correctly marked
  unresolved at the reference roundoff floor.

## Evidence boundary

The paper's equations, Table 2 cells, generator choices, witness jets, and
orbit normal forms are hand-authored mathematical inputs. The program checks
their consequences and labels the orbit classification as hand-derived from
computed adjoint actions; it does not parse the PDF into a theorem prover or
automatically classify every orbit. The unrestricted determining split checks
free-jet coefficient identities; solving those identities by parameter stratum
is a mathematical argument recorded in the report. The 21 IVPs are newly
constructed dimensionless examples, not source-supplied initial data. Sampled
PDE residuals, solver agreement, and Taylor truncations provide finite
diagnostics, not continuous-domain error bounds, global smoothness, shocks,
or equivalence to the advectively corrected/full SVE system.

The broad regression log records `173 passed, 1 failed` after 46.91 seconds.
Its single failure is `scripts/tests/test_project_audit.py::`
`test_missing_expanded_evidence_is_not_a_false_carrier_failure`, a fixture
audit status mismatch, not a reproduction-package computation assertion.
The director's project-wide validation and final release receipts are tracked
separately in `COMPUTATION_VALIDATION.md`.
