# Independent review of the two-dimensional local point algebras

The reviewer did not author either two-dimensional necessity derivation. This
report records the mathematical adjudication; `classification_2d_review.json`
records exact source versions and executed checks. Until all five phases and
the final hash check pass, the machine-readable verdict remains pending.
No stage-one source or receipt is edited by this review.

## 1. Scope and primary-model boundary

The system is the four-field evolving-bed SVE model in `(t,x,y,h,u,v,B)` with
isotropic transport `K (u^2+v^2)^((m-1)/2) (u,v)` and slope diffusion
`G (u^2+v^2)^(n/2) grad B`. It is not a prescribed-bed shallow-water system,
the printed scalar SVE equation, or the advectively corrected scalar model.
The source-style slope law `n=m` and attachment law `n=m-1` remain separate.
In particular, the vector cubic law is an isotropic norm times the velocity;
it is not the componentwise vector `(u^3,v^3)`.

The reviewed chart is open and connected, with `h>0`, `u^2+v^2>0`, `g>0`,
and each active `K,G` positive. Neither velocity component must be nonzero.
The real exponent range is `1<=m<=4` on positive transport and `0<=n<=4`
on slope-only cells. Absent exponents disappear. Coriolis is a fixed real
constant; `f=0` and `f!=0` are separate equations, not equivalence parameters.

These are local smooth point symmetries. The normal time-leading matrix is
the identity. The arguments are identities on the regular formal equation
manifold. Smooth coefficient extensions across auxiliary hypersurfaces are
legitimate; symmetries confined to a lower-dimensional constrained state
set would instead concern a different PDE problem.

## 2. First-order necessity: independently adjudicated chain

1. All seven coefficients initially depend on all seven point coordinates.
   The direct restricted prolongation is a quadratic polynomial in eight
   independently free first spatial jets. Neither field projectability nor
   spatial affinity is assumed.
2. For either pure spatial direction, the quadratic expression is
   `A^2 k (tau_w k)-A k (tau_w A k)+k (xi_w A k)-A k (xi_w k)`.
   In an eigenbasis its mixed coefficient is
   `(lambda_i-lambda_j)(lambda_i tau_wj-xi_wj)`. For each `j`, two other
   distinct eigenvalues force both derivatives to vanish. This is a
   pointwise change of linear basis; it does not assume a globally smooth
   diagonalizing coordinate transformation.
3. The full directional symbol has the transverse eigenvalue `u` and a
   three-by-three block. For positive transport, its `q11` is strictly
   positive on the entire speed chart. Positive diagonal symmetrization and
   the irreducible tridiagonal recurrence give three simple real eigenvalues.
   The cubic at `lambda=u` is `-g h u`, so the full four roots are distinct
   on `u!=0`. At zero transport the extra exclusions are the sonic
   hypersurfaces `u^2=g h`. The corresponding y-direction argument uses `v`.
   All exclusions have empty interior, so continuity recovers the axes and
   sonic states. No physical state is deleted from the declared open chart.
4. The passive eigenvectors `(-q12/u,0,1,q12/u)` and its y counterpart are
   used only on their dense valid sets. Their equations and the two matrix
   traces yield `xi_t=2g[tau_x(h+q11)+tau_y q12]` and its y counterpart.
   The free depth coefficient forces `tau_x=tau_y=0`, then
   `xi_t=chi_t=0`. No transport coefficient is divided out.
5. The water matrix entries force `H_u=H_v=H_B=0`, `H=d h`, spatial
   conformality, and `Z_u=Z_v=0`. The two bed/depth entries are
   `-u Z_h=-v Z_h=0`; nonzero speed gives `Z_h=0` even at `K=0`.
   Thus the vertical coefficients are exactly those stated in the proof.
6. Radial tensor homogeneity leaves `(m-3)(p-a)Q=0`. Its positive diagonal
   entry proves the positive-transport condition without dividing by `m-1`.
   The endpoint `m=1` is covered, and `m=3` is the only enhancement in range.
7. Conformality by itself would allow nonlinear spatial functions. The
   constant mass identity is `h[-2 a_t+4 p_x u+4 p_y v]=0`. It forces all
   those derivatives to zero. The remaining constants give
   `g z_x-a f v=0`, `g z_y+a f u=0`, and `z_t=0`, hence `a f=0` and constant
   bed shift. This excludes nonlinear conformal and rotating/moving-frame
   families by determining equations rather than an affine trial ansatz.

The resulting general generator and the two terminal equations in the
author proof are necessary. Their exact direct residual proves sufficiency.
The six first-order dimensions are respectively `6/5`, `7/6`, `7/6` for
nonrotating/rotating generic Grass, cubic Grass, and zero transport.

## 3. Slope necessity and the mixed-order shell

The correct `J2` shell contains four original equations and all nine first
differential consequences of the three first-order hydrodynamic equations.
The thirteen solved jets are four first time derivatives, six fluid
space-time derivatives, and three fluid second time derivatives. The free
jets are eight first spatial, twelve second spatial, and `B_tx,B_ty,B_tt`:
twenty-three in total. Differentiating Exner adds third-order information,
not an additional second-order constraint.

The leading lift of `(B_tx,B_ty)` is `D(B_xxx+B_xyy, B_xxy+B_yyy)`. Since
`D>0`, these can be prescribed independently by third spatial jets. The
leading fourth-order part of `B_tt` is `D^2 Delta^2 B`, so its independent
value can likewise be lifted after the lower-order choices. This explains
the regular projection from the prolonged evolution system; a free mixed
bed jet must not be set to zero or silently removed by the splitter.

The independently adjudicated elimination is:

1. The `B_tx_i` coefficients are `2 D D_i tau`. Splitting free spatial
   first jets forces `tau=tau(t)`.
2. The fluid Hessian coefficients force `c_z=xi^1_z=xi^2_z=0` for each
   fluid field. The diagonal and off-diagonal bed Hessian coefficients
   then remove spatial-coefficient dependence on `B` and force planar
   conformality. The mixed coefficient has the required factor two.
3. Hydrodynamic Laplacian coefficients remove bed dependence of the
   remaining fluid coefficients. Mass bed-gradient coefficients remove
   velocity dependence of the depth coefficient. These steps divide only
   by `D>0` or `g>0`; they work at `n=0` and on either velocity axis.
4. The full hydro determining polynomial retains the gradient matrix `P`.
   Its cross diagonal entries force `b_h=0`; the other entries give
   `b=xi_t+(A-tau' I)w`. Gradient identities give
   `a=2(sigma-tau')h` and `c=2(sigma-tau')B+psi`. The possible additive
   depth shift is eliminated by the mass velocity-gradient coefficient.
5. The constant mass identity forces spatially uniform `sigma` and
   `tau''=2 sigma'`, after which conformality yields
   `xi=(sigma I+omega J)r+p(t)`. The momentum identities retain arbitrary
   time functions, with `2 omega'+f tau'=0` and the explicit quadratic
   pressure/bed correction `psi` in the proof. The signs of the `f J`
   terms and the integrated `f^2 tau'` term have been checked independently.
6. The full bed divergence transformation is valid for arbitrary smooth
   `D(u,v)` and vector `F(u,v)`. Radial covariance subsequently reduces it
   to the stated form. Its Hessian identity `L=0` is an identity in point
   variables, so every total derivative of `L` also vanishes. After removing
   `div(L grad B)`, the only remaining bed-gradient term is
   `-xi_t dot grad B`; thus `xi_t=0`, including constant diffusivity `n=0`.
   This is the decisive exclusion of arbitrary moving/rotating frames.
7. The remaining equations are exactly
   `T+(2-n)d=0`, `m K (m-3)d=0`, and `f T=0`. The transport contraction
   `w^T F_w w=m K (u^2+v^2)^((m+1)/2)>0` supplies the required nonvanishing
   condition without a division by an individual velocity component.

The eleven slope cells therefore have dimension five, plus one precisely
when `(K=0 or m=3)` and `f(n-2)=0`. In particular, the rotating slope-only
family must split `n=2` from `n!=2`. The nonrotating family has constant
dimension six through `n=0,1,2,3,4`; the base rank of a particular dilation
may change without changing the dimension of the point algebra.

## 4. Independent implementation and exact-version controls

The reviewer script contains its own finite jet coordinates, total
derivatives, point-prolongation recursion, PDE construction, and triangular
mixed-order shell. It compares the full unrestricted on-shell identities
with the root frontend and both independent authors. The slope comparison
uses arbitrary diffusivity and vector flux, not a finite exponent sample.
All seventeen model cells are compared with a separately assembled model;
all seventeen general integrals are substituted into that independent PDE.

The symbolic normalizer does not force power identities. If ordinary exact
simplification is insufficient, it uses the positive rational velocity
chart `u=rho(1-z^2)/(1+z^2), v=2rho z/(1+z^2)`, `rho>0`. This keeps actual
related radial powers related. A smooth identity on this dense chart
extends to its omitted ray. The normalization is an exact identity check,
not numerical parameter sampling or exponent-independence inference.

The frontend is accepted only for its declared regular model family. Its
integrator is a model-specific certificate adapter, not a universal solver
of arbitrary determining PDEs. Exact model, parameter and guard fingerprints
prevent applying the certificate to a changed equation. The receipt hashes
the imported one-dimensional branch registry as well as all new code,
derivations, tests, contract and reviewer files before importing them, and
checks the same hashes after each phase. The receipt does not hash itself.
Virtual rejection controls never write a live accepted review fixture.

The stage-two release wrapper additionally requires a nonempty exact source
inventory, one successful receipt per cell, the canonical child log, and the
recorded digest of that child's `derivation.json`. Validation must contain
the six named completed commands and their canonical logs. Accepted data and
algebra review receipts are mandatory and must bind their implementations.
The reviewer exercises missing, duplicate, failed, timed-out, tampered and
unbound variants entirely in memory; no virtual fixture creates a live gate.
Every nested input hashed by either additional review is also included in
the stage gate's evidence. This includes reviewed Markdown outside the
Python source inventory. A virtual post-release Markdown edit is checked
with the actual gate reader and must invalidate the previously accepted gate.

Two initial analyzer failures are preserved. `grass_generic_f0` constructed
151 determining equations in 22.55 seconds and passed the general integral
through them, but its common base scaling failed the unnormalized recursive
check on the identity `s^a=s*s^(a-1)`, `s=u^2+v^2>0`. The exact isolated
failure is in `runs/reviewer-first-profile-failure.json`. The generic slope
profile reached the enclosing 120-second process limit before returning a
report; `runs/reviewer-slope-profile-timeout.json` records that negative.
Neither event is a mathematical obstruction. Root subsequently introduced
an explicit positive-speed normalizer and instrumented the pipeline; only
the final reviewed source hashes and executed phase results determine
whether those repairs are accepted.
The first complete independent review passed 227 checks and is preserved as
`runs/classification_2d_review-before-nested-evidence-refresh.json`. A final
release audit then found the missing nested Markdown dependency described
above. The repaired helper and new regression control require a fresh full
review receipt; the preserved snapshot is not substituted for that refresh.

## 5. Reductions: ranks, signs, inverses and repairs

Two commuting translations yield the plane-wave coordinate `z=x-c t` and
four profiles. The transverse profile is retained: at `f!=0`, setting it
identically to zero leaves `f U` in the transverse momentum equation.
No division by `c` or `U-c` is used, so the result remains an implicit
ODE/DAE on characteristic or stationary strata. Real finite speeds are
required; unknown symbolic realness/finite properties become explicit guards.

Joint spatial/velocity rotation has base rank one and leaves a PDE in
`(t,r)`. On the local polar chart `r>0`, the Jacobian is `r` and the velocity
rotation determinant is one. The radial momentum has `-V^2/r-f V`; the
azimuthal equation has `U V/r+f U`. The tangential transport flux has zero
angular divergence under this invariant graph; it is not an omitted force.
The independent Cartesian cross-section check is transported around every
regular orbit by the separately verified joint rotation.

Joint rotation and pure spatial/field scaling commute and have base minor
`-(x^2+y^2)`. Their invariant graph is
`h=(x^2+y^2)H(t)`, `(u,v)=(A x-W y,W x+A y)`, `B=(x^2+y^2)Z(t)`.
For cubic attachment transport the exact four time equations are

```
H' + 4 A H = 0
A' + A^2 - W^2 - f W + 2 g(H+Z) = 0
W' + 2 A W + f A = 0
Z' + 4(A^2+W^2)(K A - 2 G Z) = 0.
```

These are independent-variable reductions, not claims of a first integral
or ODE-order reduction. The original Cartesian rows are reconstructed by
an invertible row map on the stated chart. Unsupported pure scaling is
rejected by the original PDE residual. The previously inaccessible valid
`slope_only_f0,n=2` slice now has an explicit exponent specialization.

The root's initial reduction receipt was inspected: its log states
`29 passed in 38.27s`, exit code zero, and its live SHA256 agrees with
`059f3cc3089bc5d891ca238c284a16a31b79c3b8f6316f2cedca79ec82936002`.
That supporting test run does not replace the independent pullbacks above.

## 6. Verdict boundary and reproducibility

Run the five reviewer phases `raw`, `necessity`, `branches`, `reductions`,
and `adapter` sequentially in bounded subprocesses, then `finalize`. Each
phase records its checks and source hashes. A failed, partial, changed-source
or missing-cell result keeps `all_checks_passed=false`; exceptions are
retained in `prior_attempts`. The accompanying final receipt determines the
executed status and exact check count, rather than a number copied here.

Acceptance, if the final receipt passes, is for all seventeen declared local
smooth point algebras and the specified regular reduction charts. It is not
an optimal-system classification in two dimensions, a full disconnected
point-equivalence groupoid, a zero-speed or zero-depth classification,
arbitrary boundary/data compatibility, well-posedness, a shock theorem,
conditional/nonclassical completeness, or an ML result. Source provenance
for the model does not import another paper's prescribed-bed maximality
claim. The final stage gate remains a separate root-owned release operation.
