# Independent review: convergence and reconstruction additions

**Verdict: accepted within the stated local, numerical scope.** Reviewed
`build/convergence_addition.py`, `docs/CONVERGENCE.md`, the saved convergence
JSON, `build/reconstruction_addition.py`, the core reduction/solver definitions,
and the extracted paper's equations (24)--(33). This does not review the final
HTML/browser integration or the consolidated `main.py`; those require separate
post-integration checks.

## Convergence

- The fixed ladder calls the classic six-stage Fehlberg fifth-order accepted
  state exactly `N=1,2,4,8,16,32,64` times, without an output grid or an
  adaptive controller. The adaptive sweep uses `t_eval=None`, fixed
  `first_step=L/2` and `max_step=L` at every tolerance. Stage RHS calls and
  accepted endpoints use the positive-branch guard.
- Recomputed from `convergence.json`: 21/21 rows completed, 147 fixed runs,
  55 resolved errors, 39 eligible adjacent orders, and maximum DOP853-pair
  disagreement `1.887379141862766e-15`. The five 3.4 final eligible slopes
  are `4.9675`--`4.9755`; 3.5 is `4.9338`. Each 3.6/3.9 row has only one
  eligible pair; none of the exact-quadratic 3.8 rows has one. These agree
  with `docs/CONVERGENCE.md` and do not justify a stronger asymptotic claim.
- Independently checked the exact traveling first integral at `m=3` against
  saved DOP853 endpoints: `B(P)C` changes by `2.78e-16` for 3.6 and
  `1.67e-16` for 3.9. The exact `y'=y` control supplies a non-polynomial
  fifth-order check. Reference-pair agreement and the operational error floor
  are diagnostics, **not** a rigorous bound on reference error; the document
  correctly says so. Adaptive plateaus with unchanged step counts cannot be
  interpreted as tolerance convergence.

## Reconstruction and source provenance

- Differentiating the five declared ansatzes independently gives precisely
  the implemented `(phi,u,h)=(phi,phi_t,1/phi_s)`: 3.4 has
  `(tF,F-zP,1/P)`, 3.5 `(F,2zP/t,1/(t^2P))`, 3.6
  `(F,P,1/P)`, 3.8 `(s+F,P,1)`, and 3.9 `(t+F,1+P,1/P)`.
  Here `z` is respectively `s/t,st^2,s+t,t,s+t`; animation time is `t`,
  not generally the ODE coordinate. The normalized-depth identity does not
  establish the corrected full physical model.
- Independently tested the saved `m=3` initial jets. The reconstructed
  `(phi,u,h)` values for cases 3.4, 3.5, 3.6, 3.8, 3.9 were respectively
  `(2,1.5,2)`, `(2,1,2)`, `(2,0.5,2)`, `(0.2,1,1)` at `s=0.2`, and
  `(2,1.5,2)`, with maximum numerical discrepancy below `3e-12`.
  One coordinate beyond each of the five solved intervals returned an
  invalid mask and three `NaN` fields, not extrapolated values.
- `BPoly.from_derivatives` constructs piecewise quintic Hermite segments
  from the stored `F,P,C` jets with extrapolation disabled. Data construction
  succeeded for all 21 passed runs; the maximum stored-node derivative
  discrepancy was `4.86e-9`, below its `1e-7` sanity gate. Sampling positivity
  and masking provide a plotted local patch, not a continuous between-node
  regularity or interpolation-error certificate.
- The equation map matches the paper's sequence: (24) 3.4, (25)--(27) 3.5,
  (28)--(31) 3.6, (32) 3.8, and (33) 3.9. It correctly identifies (26)/(29)
  as derivative reductions, (27)/(30)/(31) as further/first-integral
  representations rather than independent IVPs, and (32) as a qualified
  source statement with a corrected time profile. The parametric
  `(Sigma,M)` and `(P,C)` curves must not be represented as single-valued
  graphs without the stated nonzero-coordinate-derivative chart guards.

**Remaining integration gate:** run the consolidated one-file CLI and inspect
the final offline HTML in a browser after the new definitions are merged.
The build fragment intentionally relies on imports supplied by `main.py`,
so this review does not claim that it is independently executable.
