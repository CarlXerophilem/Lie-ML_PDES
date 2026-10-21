# Independent review of the declared 1D local point algebras

Review date: 20 October 2026. Reviewer: a fresh agent separated from the two
derivation authors and the root implementation author. Review scope is the
eight cells in `models.py`, on an open positive chart `h>0,u>0,g>0`, with fixed
parameters. No desired verdict was supplied. Only this review, its independent
verification script, and its JSON receipt are reviewer-owned outputs.

## Verdict

**First-order family: accepted.** The displayed necessary-and-sufficient
classification covers `G=0,K>0,1<=m<=4` and `G=K=0` without a coefficient
ansatz. The maximal local smooth point dimensions are respectively 4 for
`m!=3`, 5 for `m=3`, and 5 when `K=0` (where `m` is absent).

**Slope family: accepted.** The displayed necessary-and-sufficient
classification covers `G>0,K>0,n=m-1` and `n=m`, `1<=m<=4`, and
`G>0,K=0,0<=n<=4`. The dimensions are 3 for positive `K,m!=3` and 4 for
positive `K,m=3` or zero `K`. No extra branch occurs at `n=0,1,2`.

**Root analyzer: accepted for unrestricted determining-equation construction
on these eight declared cells; qualified as a general classification tool.**
The arbitrary-function input, prolongation, equation-shell reduction, and free
jet split agree with a separate explicit calculation. Its model-specific
integration adapter may use the reviewed proofs and solved coefficient
families. That is not an algorithm for integrating an arbitrary PDE's
determining equations. Unknown systems must retain an unresolved integration
status. Exact substitution alone is a sufficiency check; the necessity proof
remains the analytical integration reviewed below.

These are mathematical scope verdicts. The computational receipt and hashes
in `classification_review.json` identify the exact checked version. The full
point-equivalence groupoid is **not adjudicated** here. Retaining potentially
equivalent redundant branches is compatible with coverage; removing branches
using an unproved equivalence would not be.

## First-order necessity audit

1. **The equation manifold and unrestricted identity are legitimate.** All
   three first time derivatives are solved with unit coefficient, so the
   three spatial first jets are independent. A general field depends on all
   five coordinates. Direct prolongation gives exactly `C+M p+Q(p)` in
   equations (6)--(7). Splitting constant, linear, and quadratic jet degree is
   therefore both necessary and sufficient. The independent verifier checks
   the full identity, not merely its value at the final generators.

2. **Projectability is proved rather than assumed.** In an eigenbasis the
   mixed quadratic coefficient is
   `(lambda_i-lambda_j)*(lambda_i*tau_wj-xi_wj)`. With three distinct
   eigenvalues, fixing `j` leaves two distinct values of `lambda_i`, forcing
   both derivatives to vanish. For `K>0`, `q=m*K*u^(m-1)>0` and the positive
   symmetrizer produces an irreducible symmetric tridiagonal matrix.
   Its eigenvector recurrence gives a one-dimensional eigenspace for each
   eigenvalue, and symmetry identifies geometric and algebraic multiplicity.
   Thus every state in this chart has a simple spectrum. This pointwise
   algebra argument does not differentiate the eigenvectors.

3. **The zero-transport degeneracy is handled correctly.** For `K=0`, the
   discriminant is `4*g*h*(u^2-g*h)^2`. The nonsimple locus is a hypersurface
   with empty interior. Smooth coefficient derivatives which vanish on the
   dense complement vanish on that hypersurface too. This does not discard an
   open-domain point symmetry. A separately imposed constraint `u^2=g*h`
   would define a different PDE problem, outside this claim.

4. **Trace elimination does not replace the full matrix criterion.** The
   first two traces solve uniquely for `U,H`, using only nonzero `g` and the
   positive-chart rewriting by `u`. The adjugate trace is valid even when the
   flux matrix is singular: no inverse of that matrix is used. Its free-`h`
   coefficient is `g*(b*g*m*q+c)`. For `m>1,K>0`, differentiating in `u`
   forces `b=c=0` because `q'>0`; the remainder is precisely
   `a*g*q*u*(m-3)`. The separate `m=1` remainder is
   `g*q*(-4*a*u+3*b*g*q)/2`, which again forces `a=b=c=0` by free-`u`
   splitting. Thus no endpoint is lost by division by `m-1`.

5. **The static-bed branch has an essential extra check.** At `q=0`, the
   determinant equation forces `c=0` but leaves `b` undetermined. Substituting
   the trace solutions in the actual `M11` equation gives `3*g*h*b=0`.
   Hence `b=0`; relying on traces alone would have been insufficient.

6. **The residual equations force constants, not just affine trial fields.**
   The actual `M21,M31,M23` equations force `Z_h=Z_u=0` and `Z_B=-2*a`.
   Therefore `Z=-2*a(t,x)*B+d(t,x)`. The first zero-jet equation is
   `-h*(2*a_t+3*u*a_x)=0`. Independent `u` and positive `h` force
   `a_t=a_x=0`; the next two rows force `d_t=d_x=0`. Finally
   `tau_x=xi_t=0` and constant `tau_t-xi_x` force affine `tau(t),xi(x)`.
   No alternative functional coefficient remains. The final independent
   prolonged residual vanishes exactly under the stated `K*(m-3)*a=0`
   condition.

This reasoning establishes necessity before sufficiency is checked. A finite
search over affine or scaling generators is not being used as its substitute.

## Slope-family necessity audit

1. **The mixed-order shell is appropriate.** In `J2`, include the original
   three equations and the two first derivatives of each hydrodynamic row.
   They solve `h_t,u_t,B_t,h_tx,u_tx,h_tt,u_tt`; their leading coefficients
   are one. The momentum time consequence solves `u_tt` and leaves `B_tx`
   free. `B_tt` is also free. Differentiating the order-two bed equation is
   a `J3` operation, so it cannot be imposed as an additional equation on
   the stated `J2` chart. There is no hidden order-two relation eliminating
   `B_tx`: at `J3`, `B_tx=D_x f3` solves `B_xxx` with nonzero coefficient
   `D=G*u^n`.

2. **All projectability steps use independently free jets.** The `B_tx`
   coefficient is `2*D*D_x(tau)`, so `tau=tau(t)`. The `h_xx,u_xx`
   coefficients then force `Z_h=Z_u=xi_h=xi_u=0` by splitting in `B_x`.
   The `B_xx` coefficient has a `2*D*B_x*xi_B` term, forcing `xi_B=0`.
   The first two rows' `B_xx` coefficients force `H_B=U_B=0`, and the water
   row's `B_x` coefficient forces `H_u=0`. The independent calculation
   checks every one of these coefficients. None uses `D'!=0` or `n!=0`.

3. **The seven hydrodynamic equations integrate exhaustively.** Subtracting
   the two equations containing `h*U_h` gives `2*h*U_h=0`. Their sum fixes
   `U=xi_t+(xi_x-tau')*u`. The `h` and `B` derivatives of the remaining
   field coefficients both equal `2*(xi_x-tau')`; the water `u_x`
   coefficient removes the additive `H(t,x)` term. The constant water
   coefficient yields `xi_xx=0` and `3*xi_tx-2*tau''=0`. Writing
   `xi=L(t)*x+R(t)`, the momentum constant coefficient separately gives
   `2*L'-tau''=0`. These independent relations force `L'=tau''=0`.
   The remaining equation integrates the bed offset to
   `-R''*x/g+S(t)`. Thus the intermediate family (18), with arbitrary
   `R,S`, is genuinely the full hydrodynamic integral under the already
   proved projectability restrictions.

4. **The bed identity removes all remaining arbitrary functions.** Its
   complete polynomial has independent monomials `B_xx,u_x*B_x,u_x,B_x,1`.
   The plain `B_x` coefficient is `-R'`, including at `n=0,K=0`. Thus
   `R'=0` before any diffusion exponent is divided out. The constant term
   fixes `S'=0`. The `B_xx` coefficient gives `T+(2-n)*d=0` and the
   `u_x` coefficient gives `m*K*(m-3)*d=0`; the mixed-jet coefficient then
   vanishes. This integration accounts for every term, not only selected
   necessary equations.

5. **The parameter split has no omitted exceptional value.** With `m>=1`,
   the last equation leaves either `d=0`, or `K=0`, or `m=3`. The first
   equation has coefficient one on `T`, for every real `n`, so `n=0,1,2`
   cannot create a further freedom. The extra field is
   `(n-2)t*d_t+(n-1)x*d_x+2h*d_h+u*d_u+2B*d_B`.
   At `m=3,n=3` it must include time dilation; the spatial-only generator
   belongs to `n=2`. No step divides by `n`, `n-1`, `n-2`, `K`, or `m-3`.

6. **Sufficiency is checked for symbolic exponents.** Its remaining bed
   residual is `m*K*(m-3)*u^(m-1)*u_x`. This is an exact family identity on
   `u>0`, not a finite-exponent sample. Together with the preceding necessity
   integration it proves the claimed local maximal point algebras.

## Root analyzer and integration interface

The root analyzer uses an infinite evolution shell and replaces `B_tx` by
`D_x f3`, introducing a free `B_xxx`. The slope derivation instead keeps
`B_tx` free at order two. These representations are equivalent here because
the coefficient of `B_xxx` in `D_x f3` is `D>0`. It is an invertible triangular
change of the relevant free jet, not an additional constraint. The independent
script compares the **entire unrestricted residual** after this replacement
against every root on-shell row, then reconstructs each row from its split
coefficients. All parameter exponents remain symbolic within the registry's
continuous cells; parameters are not treated as independent jet variables.

The time-leading matrix determinant is one in all cells. Denominators arising
from collecting powers of `u` lie within the positive-`u` chart. No branch
division is justified by a numerical rank test. Root final-family substitution
is checked against every raw determining equation and against the independent
prolongation, in addition to comparing the integration adapter's result to
the appropriate branch solver.

During review, the new adapter passed `n` as the `exponent` argument even for
positive-`K` branches, whose solver contract requires `m`. The cubic
attachment branch therefore raised `ValueError`; generic attachment branches
could receive the wrong exponent silently. This was reported to the author
and corrected to use `m` for positive `K`, `n` only for `slope_only`. The
reviewer did not modify author code. The final receipt covers the corrected
adapter, and the initial failure is retained in its attempt history.

The model/guard fingerprint gate is a useful restriction: the derivations
support these equations and assumptions, not arbitrary inputs sharing a
model name. This review does not certify a universal differential completion
engine, automatic integration of unknown determining PDEs, full equivalence
classification, or optimal-subalgebra completeness.

## Coverage and limits

| Registry cell | Parameter domain | Local point dimension |
|---|---|---:|
| grass_generic | `K>0,G=0,1<=m<=4,m!=3` | 4 |
| grass_cubic | `K>0,G=0,m=3` | 5 |
| zero_transport | `K=G=0`, no `m,n` | 5 |
| slope_attachment_generic | `K>0,G>0,n=m-1,1<=m<=4,m!=3` | 3 |
| slope_attachment_cubic | `K>0,G>0,m=3,n=2` | 4 |
| slope_source_generic | `K>0,G>0,n=m,1<=m<=4,m!=3` | 3 |
| slope_source_cubic | `K>0,G>0,m=3,n=3` | 4 |
| slope_only | `K=0,G>0,0<=n<=4`, no `m` | 4 |

The union is exactly the requested positive-depth, positive-velocity 1D
family. The later addendum below also verifies transfer to `u<0` for the
explicit signed absolute-value flux. The review does not extend to `u=0`, `h=0`, negative transport
or diffusion coefficients, constrained state hypersurfaces, disconnected
finite transformations, generalized/contact/nonlocal/nonclassical symmetries,
2D systems, or global solution/data claims. In particular, local smooth point
classification is an equation-manifold statement, not a smooth-data
well-posedness theorem.

The printed scalar SVE and advectively corrected scalar SVE models were not
used as classification inputs. README.md, the manuscript introduction,
docs/project-map.md, and the current experiment index were inspected for
scope; their older scalar and finite-ansatz evidence cannot establish this
new full-system maximality. No literature novelty claim is adjudicated.

## Reproduction

Run `python -B build/sve-general-symm-20261020/review_classification.py` from
the repository root. The script writes only `classification_review.json`.
The reviewed execution used a 90-second subprocess timeout after a 28-second
attempt exhausted its budget; the latter is a resource event, not a failed
mathematical identity. Detailed per-branch timings, check count, and SHA-256
hashes are in the receipt. The analytical arguments above are indispensable
to the accepted necessity verdicts; passing symbolic tests alone would not
have earned those verdicts.

Repository-wide audit/data-flux/workflow and historical regression suites
belong to the enclosing release gate and are not claimed as rerun by this
independent reviewer. No manuscript or bibliography was edited, so no LaTeX
rebuild is claimed. No 2D work was started.

## Addendum: live review gate, graph reductions, adjoints, and reflection

This addendum reviews the final stage-1 `classification.py`, the adjoint
export in `main.py`, `reductions.py` and its regression tests. The expanded
receipt records their exact hashes, the new independent checks, and all
earlier classification checks. The classification verdicts above remain
accepted on their stated charts.

**Review-gate verdict: accepted for exact-version freshness.** The gate checks
all required source/proof/reviewer-file hashes, exact eight-cell coverage,
per-cell success, all-checks success, and the three accepted mathematical
verdicts. An in-memory filesystem test accepts a current snapshot and rejects
a changed source, missing required hash, missing branch, failed branch, and
rejected verdict. These tests do not mutate author inputs or the live receipt.

There is no receipt self-hash fixed point: `classification_review.json` is
not one of its own hashed inputs. The gate returns that file's hash to its
caller but does not require storing it inside the same receipt. Changing
noncritical receipt metadata therefore changes the returned receipt digest
without invalidating unchanged reviewed inputs. During a review refresh, the
old receipt may correctly leave root reports in `pending_review`; the
independent checks do not infer truth from that status. After the new receipt
is written, the script separately asserts that the live gate accepts it and
does not write the returned receipt hash back into the receipt.

The review script now captures all input hashes **before importing author
modules** and rejects any changed hash at the end. This closes a provenance
gap in the original reviewer script, which had hashed only after execution.
That gap could have attested an input changed concurrently with a computation.
The new receipt explicitly records that the snapshot stayed unchanged.

**Reduction verdict: accepted for the implemented charts.** Translation
characteristics give `z=x-c*t`, and homogeneous diagonal characteristics
give either `z=x*t^(-beta/alpha)` with `t>0,alpha!=0`, or `z=t` with
`x>0,alpha=0,beta!=0`. The graph amplitudes and row factors are the associated
characteristic powers. Their base-chart Jacobians are nonzero under these
guards; no rank-zero generator is silently treated as a reduction. The
symbolic `slope_only` time chart explicitly retains `n!=2`, while `n=2`
uses its spatial chart. Selected generators are independently checked against
the PDE even when a candidate basis contains them.

The new independent checks directly differentiate the reconstructed fields
in the original mass, momentum, and Exner equations. They do not call
`_chain_jets`, `_positive_simplify`, `graph_check`, or a supplied reduced-ODE
formula to construct the original residual. They compare it to the exported
row factor times reduced equation for all eight traveling branches, seven
selected diagonal cases, and `slope_only` diagonal cases at `n=0,1,2,3,4`.
These finite endpoint checks complement the symbolic chart argument; they
do not establish parameter coverage by sampling. Positivity assumptions in
the independent differentiation are imposed only on the chosen orbit
coordinate. The implementation's chain, characteristic, and reconstruction
identities provide additional exact checks.

The reduced systems remain undivided implicit ODEs/DAEs. Their leading
matrices are not inverted, and sonic or stationary singular loci are not
discarded. This proves equation reduction on the guarded invariant graphs,
not existence of profiles, an ODE-order reduction, arbitrary-data compatibility,
or an optimal system of all one-dimensional subalgebras. The initial-graph
helper computes tangency for a supplied symmetry basis and one fixed slice;
its result must retain that supplied-basis and fixed-data scope. The
constant-slope graph is a constructed solution with its positive-velocity
time interval, not an arbitrary-data theorem.

**Adjoint verdict: accepted with the declared sign convention.** The matrix
columns represent `ad_X(Y)=[X,Y]`, and exported matrices use
`exp(epsilon*ad_X)`. An independent coordinate-flow calculation verifies every
exported basis adjoint in all eight cells. For the affine basis fields it
constructs the actual flow `phi_epsilon` and checks

`phi_epsilon^*Y = (D phi_epsilon)^(-1) Y(phi_epsilon(q))`

against the exported matrix combination. This is flow pullback (equivalently
inverse-flow pushforward). Forward-flow pushforward has the opposite exponent
sign. The convention is explicit; the matrices do not constitute an optimal
subalgebra classification.

**Negative-speed transfer verdict: accepted only for the signed closure.**
The reviewed extension is
`K*abs(u)^(m-1)*u-G*abs(u)^n*B_x`. The involution
`(t,x,h,u,B)->(t,-x,h,-u,B)` has Jacobian one and residual multipliers
`(1,-1,1)`. The independent verifier derives its Exner identity using
`D_x abs(u)=sign(u)*u_x` separately on both nonzero-speed charts, with symbolic
real `m,n` and free jets. It also runs the author's map checks and retains
their unresolved full-groupoid status. Conjugation by this invertible map
therefore transports the maximal positive-chart point algebra to the negative
chart of this explicitly signed model. It is not an extension of arbitrary
noninteger `u^m` to negative `u`, and does not cross `u=0`.

The explicit reflection and proved coordinate/scaling maps are sufficient
for the transports and merges they actually establish. Neither this addendum
nor a list of valid maps establishes the full equivalence groupoid, rules out
other cross-parameter maps, or permits discarding a branch using an unproved
equivalence.
