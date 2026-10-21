# Verified 2D subalgebra representatives

This Stage 2 extension uses the bases obtained by integration in
`research_first_order_2d.py` and `research_slope_2d.py`. It verifies selected
one-dimensional subalgebras and concrete rank-two subalgebras. Its status is
`verified_representatives`; **optimal-system completeness is not proved**.
The source classification's independent-review status is preserved separately.

## Implementation and evidence plan

The assigned interface is `representative_subalgebras(name, basis=None)`.
The implementation has three parts: formal constant-span extraction and actual
brackets; selected generators and invariant charts; regression checks against
all 17 refined cells, including rejected nonconstant spans and slope resonances.
Only the new Stage 2 module, notes, and tests are edited. The frozen Stage 1
classification and its optimal-system statements are separate artifacts.

## Algebra and adjoint convention

Write point coordinates as `(t,x,y,h,u,v,B)`, and let

\[
T=\partial_t,\quad X=\partial_x,\quad Y=\partial_y,\quad Z=\partial_B,
\qquad R=-y\partial_x+x\partial_y-v\partial_u+u\partial_v.
\]

For a solved diagonal scaling define

\[
S_{a,b}=at\partial_t+b(x\partial_x+y\partial_y)
 +2(b-a)h\partial_h+(b-a)(u\partial_u+v\partial_v)
 +2(b-a)B\partial_B.
\]

The nonzero brackets are

\[
[R,X]=-Y,\quad[R,Y]=X,\quad
[S_{a,b},T]=-aT,\quad[S_{a,b},X]=-bX,\quad
[S_{a,b},Y]=-bY,\quad[S_{a,b},Z]=-2(b-a)Z.
\]

The scalings commute with each other and with `R`; the four translations
commute. The code computes these from the vector fields rather than assuming
a table or a basis ordering. Every bracket and every selected representative
is reconstructed with **constant** coefficients. Formal affine coefficient
extraction is used, not evaluation at one point. An optional mixed/reordered
basis must have the same constant span as the solved algebra. Any introduced
parameter denominator is returned as an explicit additional basis guard.
Definite complex or nonfinite constant coefficients are rejected; undecidable
reality/finiteness is recorded in `basis_reality_guards`. A requested finite
adjoint action requires explicitly finite real coefficient and time parameters.

The convention is
`ad_A(C)=[A,C]`, `Ad(exp(epsilon A))=exp(epsilon ad_A)`. In particular,

\[
\operatorname{Ad}(e^{\epsilon R})X=\cos\epsilon\,X-\sin\epsilon\,Y,
\qquad
\operatorname{Ad}(e^{\epsilon S_{a,b}})T=e^{-a\epsilon}T.
\]

Only actual connected inner adjoints are available here. A reflection may
change the sign of the fixed Coriolis parameter, so it is not silently used
to identify line families at fixed nonzero `f`.

## Selected lines and their meaning

The catalogue contains the four translations, joint rotation, `T+cX`,
`T+bZ`, `X+bZ`, and `R+aT+bZ`, plus each admitted scaling from the solved
constant system. Continuous parameters remain explicit. Equivalent entries
may occur, and these families are not advertised as an optimal system.

The pure bed line `span(Z)` is a valid algebraic subalgebra but admits no
invariant graph over `(t,x,y)`: its bed characteristic is `Q_B=1`. This is
recorded as `graph_admissible=False`. A spatial rotation without the velocity
rotation is not substituted for `R`.

Put `r=sqrt(x^2+y^2)`, `U_r=(xu+yv)/r`, `U_theta=(xv-yu)/r`. For rotation,
the six invariants are `(t,r,h,U_r,U_theta,B)`. For the screw line,
they are `(t-a theta,r,h,U_r,U_theta,B-b theta)`, with
`theta=atan(y/x)` on the local chart `x>0`. This local spatial chart does not
exclude either velocity axis and does not restrict the classification.

## Rank-two reductions

| Subalgebra | Remaining base invariant | Profile geometry |
| --- | --- | --- |
| `span(T+cX,Y)` | `x-ct` | Plane wave, all four fields retained |
| `span(T+cX+aZ,Y)` | `x-ct` | Bed invariant `B-at` |
| `span(X,Y)` | `t` | Spatially homogeneous profiles |
| `span(T,R)` | `r` | Stationary radial and azimuthal profiles |
| `span(S_{a,b},R)` when admitted | `t^b r^(-a)` | Joint rotation/scaling profiles |

Each pair closes, has rank two on its displayed base chart, and has five
independent full-space invariants. Thus it reduces three independent variables
to one at the level of invariant graphs. PDE substitution is still required
to derive and solve the resulting ODE/DAE; no first integral, decrease in ODE
order, or existence theorem follows from this rank statement. The concrete
plane-wave and radial substitutions are independently implemented in
`reductions_2d.py`. Transverse velocity is retained, especially at nonzero `f`.

For every scaling, use `t>0,r>0` and the invariant fields

\[
H=ht^2/r^2,\qquad U=t(xu+yv)/r^2,\qquad
V=t(xv-yu)/r^2,\qquad W=Bt^2/r^2.
\]

Together with `z=t^b r^{-a}`, these are annihilated by both generators.
For the scaling line alone, add the invariant angle. The tests check the
directional derivatives and actual Jacobian minors. No division by `a` or
`b` is used. Since `(a,b)!=(0,0)`, at least one base derivative of `z` is
nonzero on the chart. The implementation uses `x>0` to select one local
angular chart and exhibits two minors so zero time or spatial weights remain
covered.

For the positive-diffusion scaling, `(a,b)=(n-2,n-1)`. It is admitted only
when `(K=0 or m=3)` and `f(n-2)=0`, inherited from the solved generator.
At `n=1`, the spatial dilation weight is zero and `z=r`; at `n=2`, the time
weight is zero and `z=t`. At `n=3,4`, equal adjoint weights may affect an
optimal-system proof, but do not invalidate the displayed representatives.
The code retains all four values and divides by neither `n-1` nor `n-2`.
The rotating slope-only family uses the explicit `n=2` and `n!=2` cells.

## Verification and nonclaims

Run the new checks under the shared symbolic CPU lease:

```powershell
python -B -c "import subprocess,sys; subprocess.run([sys.executable,'-B','-m','pytest','build/sve-general-symm-20261020/tests/test_algebra_2d.py','-q'],timeout=60,check=True)"
```

The test was first observed to fail at collection because the requested
module did not yet exist. The completed suite then passed **31 tests in
6.24 seconds**, with process time **7.179 seconds** under the enforced
60-second limit. The preserved receipts are `runs/algebra2d-first.log`
and `runs/algebra2d-first-receipt.json`. A valid invariant chart is not a solution of the PDE,
boundary-data compatibility, maximal-classification proof, or optimal-system
coverage certificate. Conditional/nonclassical and learned stages remain
outside this work.
