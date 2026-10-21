# Independent review of the Stage 2 algebra representatives

The review concerns `algebra_2d.py`, its notes, and its tests. The reviewer
did not author those artifacts. The separate coefficient classifications
remain the source of the admitted algebra; this review does not infer
classification completeness from a finite list of generators.

## Findings and scope

The constant-span extraction compares formal affine coefficients, avoiding
the false enlargement that pointwise evaluation or coordinate-dependent
linear combinations can cause. The selected real bases have the expected
dimension in every one of the 17 refined cells. The bracket convention is
`[A,C]=A(C)-C(A)`, with `ad_A(C)=[A,C]` and the matching exponential. In
particular `[R,X]=-Y`, `[R,Y]=X`; both velocity components rotate jointly
with the spatial plane. The independently reconstructed bracket matrices
are also checked against the adjoint representation identity, which
contains the Jacobi identities.

Every displayed line or pair is checked against its own invariant
functions and closure relation. Pure bed translation is an algebraic line
but has the graph obstruction `Q_B=1`. The rank-two cases have one base
invariant and five full-space invariants on their explicit charts; this
proves invariant-graph dimension reduction only. No profile existence,
first integral, boundary compatibility, or optimal-system coverage follows.

For scaling weights `(a,b)`, let `s=x^2+y^2` and `z=t^b s^(-a/2)`. The
review independently obtains the line-chart minors
`(-a*z*t^6/s^4, b*z*x*t^5/s^4)` and the rotation/scaling pair minors
`(b*z*t^5/s^3, -a*z*x*t^6/s^4)`. On `t>0,x>0`, they cannot vanish
simultaneously when `(a,b)!=(0,0)`. Slope weights `(n-2,n-1)` differ by
one, so the argument includes `n=0,1,2,3,4` without dividing by `n-1` or
`n-2`. The local angular chart does not exclude either velocity axis.

The API preserves `optimality_status='not_proved'`, does not quotient by
parameter reflections, and does not claim an invariant chart is already
a PDE solution. Optional bases and adjoint parameters must remain in the
real finite domain. The initial static review flagged acceptance of
complex basis changes and imaginary adjoint parameters; the independent
script contains regressions for those cases.

## Exact-version evidence

`review_algebra_2d.py` performs independent symbolic checks and writes
`algebra_2d_review.json`, containing every check, elapsed time, acceptance
status, and SHA-256 hashes of the reviewed implementation, tests, notes,
this report, and the reviewer script. Acceptance is asserted only by a
fresh receipt with `review_status='accepted'` and `all_checks_passed=true`.
Until that receipt exists, this document records a review in progress.

The first independent run passed 959 of 961 checks in 6.80 seconds. Its
two negative checks were both the slope scaling invariant `z`: the
reviewer's generic simplifier did not combine neighboring real powers of
`x^2+y^2`. The unchanged production expressions satisfy the exact identity.
The reviewer now uses positive time/radius placeholders on the declared
chart, combines powers without `force=True`, and restores the defining
radius polynomial. The original negative receipt is preserved as
`runs/algebra2d-review-initial-failure.json`, with the initial command log
and process receipt alongside it.

Run within the shared symbolic CPU lease:

```powershell
python -B build/sve-general-symm-20261020/review_algebra_2d.py
```

The reviewer treats the 17-cell registry and the previously reviewed
coefficient-family implementations as inputs, whose hashes are retained.
No frozen Stage 1 file is modified.
