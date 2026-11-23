# Rotation and cubic scaling in the coupled two-dimensional SVE model

Date: 2026-10-14. Status: independently derived and symbolically checked;
fresh review was pending when this research note was written. The subsequent
release verdict is recorded in `REVIEW.md`. This note owns only the mathematical calculations
below. Primary-source provenance is a separate deliverable. These are new
calculations for the specified coupled Eulerian model, not a transfer of the
existing one-dimensional printed scalar classification.

## 1. Model and notation

Write the horizontal velocity as **U** = (u,v), and denote bed elevation by b.
The model under examination is

\[
\begin{aligned}
E_h&=h_t+\nabla\cdot(h\mathbf U)=0,\\
\mathbf E_U&=\mathbf U_t+(\mathbf U\cdot\nabla)\mathbf U
                  +g\nabla(h+b)=0,\\
E_b&=b_t+K\nabla\cdot\left(|\mathbf U|^{m-1}\mathbf U\right)=0,
\qquad K=\frac{\kappa}{1-p}>0.
\end{aligned}
\]

Here g>0, kappa>0, and 0<=p<1 are fixed constants. We use the smooth
positive-depth chart h>0. For arbitrary real m, impose |**U**|>0 so that
real powers and their derivatives are defined. At m=3 the transport vector
is the polynomial (u^2+v^2)(u,v), which has a smooth extension to zero speed.
That polynomial extension does not remove the separate positive-depth
assumption.

In polar coordinates let

\[
x=r\cos\theta,\quad y=r\sin\theta,\quad
\mathbf e_r=(\cos\theta,\sin\theta),\quad
\mathbf e_\theta=(-\sin\theta,\cos\theta),\qquad r>0.
\]

Use V(t,r) for radial speed and w(t,r) for azimuthal speed (swirl). Thus V is
not the Cartesian component v. The symbol beta below is a scaling weight;
it is not bed elevation.

## 2. Rotation is an exact equation symmetry

The candidate generator is

\[
R=-y\partial_x+x\partial_y-v\partial_u+u\partial_v.
\]

Its finite action rotates spatial position and velocity by the same
orthogonal matrix Q, keeping t, h, and b unchanged. The velocity magnitude
is unchanged. Scalar divergences are invariant, the gradient and the
material acceleration rotate by Q, and therefore the transformed momentum
residual is Q **E**_U. This is an exact covariance argument for the stated
isotropic model, for every real m on the positive-speed chart.

With the order (E_h,E_u,E_v,E_b), the first prolongation identities are

\[
\operatorname{pr}R(E_h)=0,\quad
\operatorname{pr}R(E_u)=-E_v,\quad
\operatorname{pr}R(E_v)=E_u,\quad
\operatorname{pr}R(E_b)=0.
\]

These identities were also checked with independent first-jet symbols.
They verify R; they do not constitute a maximal symmetry classification.

### Invariant graphs retain swirl

The graph equations Q_R=0 give

\[
h_\theta=b_\theta=0,\qquad u_\theta=-v,\qquad v_\theta=u.
\]

Solving the last two equations yields

\[
\boxed{\mathbf U=V(t,r)\mathbf e_r+w(t,r)\mathbf e_\theta},
\qquad
V=\frac{xu+yv}{r},\quad w=\frac{xv-yu}{r}.
\]

A rotation-invariant vector field need not point radially. Its components
rotate with the basis, which is why w is allowed. Setting w=0 is a further
restriction, not a consequence of rotation invariance.

The projected generator has rank one at r>0. A local angle branch makes
(t,r,theta) a smooth chart; its spatial Jacobian is 1/r. The remaining
independent variables are (t,r). At r=0 the projected rank drops and this
chart is unavailable.

## 3. Exact rotation quotient

The polar divergence of an invariant vector F_r **e**_r + F_theta
**e**_theta is (r F_r)_r/r. Differentiating the polar basis in the convective
term gives the radial centrifugal contribution -w^2/r and the azimuthal
contribution Vw/r. Consequently the full quotient is

\[
\boxed{\begin{aligned}
h_t+\frac1r(rhV)_r&=0,\\
V_t+VV_r-\frac{w^2}{r}+g(h+b)_r&=0,\\
w_t+Vw_r+\frac{Vw}{r}&=0,\\
b_t+\frac Kr\left[rV(V^2+w^2)^{(m-1)/2}\right]_r&=0.
\end{aligned}}
\tag{RQ}
\]

In particular, the radial sediment flux contains the full speed, including
swirl. The azimuthal sediment flux has zero divergence in this quotient,
but the azimuthal speed still changes the radial flux magnitude.

The swirl equation has the equivalent form

\[
(rw)_t+V(rw)_r=0.
\]

Thus specific angular momentum rw is transported along radial particle
paths. No division by V or w was used, and the quotient includes V=0 or
w=0 where the original constitutive law remains defined.

To check (RQ) independently, use

\[
\partial_x=\cos\theta\,\partial_r-\frac{\sin\theta}{r}\partial_\theta,
\qquad
\partial_y=\sin\theta\,\partial_r+\frac{\cos\theta}{r}\partial_\theta,
\]

substitute u=V cos(theta)-w sin(theta), v=V sin(theta)+w cos(theta), and
project the Cartesian momentum residual onto the two polar basis vectors.
All four equalities were checked symbolically before imposing any reduced
equation. This is a reduction from three independent variables to two;
it is not an ODE order reduction.

## 4. Diagonal scaling and the cubic parameter stratum

Consider only the declared diagonal ansatz

\[
X=a t\partial_t+\beta(x\partial_x+y\partial_y)
 +c(u\partial_u+v\partial_v)+d h\partial_h+e b\partial_b.
\]

Under the associated positive one-parameter scaling, the relevant weights
are:

| Equation | Time derivative | Advection or sediment divergence | Pressure terms |
| --- | --- | --- | --- |
| Continuity | d-a | d+c-beta | -- |
| Momentum | c-a | 2c-beta | d-beta and e-beta |
| Exner | e-a | mc-beta | -- |

For fixed nonzero g and K and arbitrary local solution jets, matching these
weights gives

\[
\boxed{c=\beta-a,\qquad d=e=2c,\qquad (m-3)c=0.}
\tag{SC}
\]

This follows from the entire equation system, rather than from a selected
special solution. With g,K nonzero there is no omitted parameter division.
The last equality must be split into parameter strata, not divided by m-3.

* If m is not 3, c=d=e=0 and beta=a: the diagonal family is generated by
  S=t partial_t+x partial_x+y partial_y.
* If m=3, a and c are free, beta=a+c and d=e=2c. The two-dimensional
  diagonal space is spanned by S and

\[
D=x\partial_x+y\partial_y+u\partial_u+v\partial_v
                      +2h\partial_h+2b\partial_b.
\]

For D the exact off-shell identities are

\[
\operatorname{pr}D(E_h)=2E_h,\qquad
\operatorname{pr}D(\mathbf E_U)=\mathbf E_U,
\]

\[
\boxed{\operatorname{pr}D(E_b)=2E_b+(m-3)K
\nabla\cdot\left(|\mathbf U|^{m-1}\mathbf U\right).}
\tag{DEF}
\]

Hence D is admitted at m=3. The last term is the explicit noncubic defect
for this candidate. Conditions (SC) classify only the stated diagonal
ansatz; they say nothing about maximality of the unrestricted point algebra.

## 5. Simultaneous R,D invariance at m=3

The bracket [R,D] is zero. Their projected spatial columns are (-y,x) and
(x,y), whose determinant is -r^2. Thus the subgroup is closed, its projected
rank is two on r>0, and its full rank is also two there. A local orbit chart
is (t,rho,theta), rho=log(r), with spatial Jacobian 1/r^2. The quotient has
only t as an independent variable.

The D graph equations in the rotation quotient are

\[
rh_r=2h,\quad rb_r=2b,\quad rV_r=V,\quad rw_r=w.
\]

Their invariant family is

\[
\boxed{h=r^2H(t),\quad V=rA(t),\quad w=rW(t),\quad b=r^2B(t).}
\tag{AN}
\]

### Constant bed offsets require the translated generator

Constant bed translation Z=partial_b is an exact symmetry, because only
derivatives of b appear. Consequently b=b0+r^2B(t) is also allowed as a
solution family for constant b0. However, if b0 is nonzero, it is **not**
invariant under the literal generator D: its bed graph characteristic is
Q_D[b]=2b0. It is invariant under the conjugate generator

\[
D_{b_0}=D-2b_0\partial_b
=x\partial_x+y\partial_y+u\partial_u+v\partial_v
                   +2h\partial_h+2(b-b_0)\partial_b.
\]

The two generators R,D_b0 still commute and have the same projected rank.
A time-dependent offset is not admitted by this ansatz: Exner would give
a separate r-independent term b0'(t), forcing b0'=0 on an open radial
interval.

### Reduced ODEs

Substitution of (AN) into (RQ), at m=3, gives

\[
\boxed{\begin{aligned}
H'&=-4AH,\\
A'&=W^2-A^2-2g(H+B),\\
W'&=-2AW,\\
B'&=-4KA(A^2+W^2).
\end{aligned}}
\tag{ODE}
\]

The coefficient 4 comes from the radial geometry. For example,
(rhV)_r/r=(AHr^4)_r/r=4AHr^2. The cubic radial transport is
V(V^2+w^2)=r^3 A(A^2+W^2), so its divergence is
4r^2 A(A^2+W^2). Swirl changes the closure factor from A^3 to
A(A^2+W^2).

An independent Cartesian derivation avoids every polar division. Set

\[
\begin{aligned}
h&=H(x^2+y^2),& b&=b_0+B(x^2+y^2),\\
u&=Ax-Wy,&v&=Ay+Wx.
\end{aligned}
\tag{CAR}
\]

Define

\[
\begin{aligned}
C_H&=H'+4AH,\\
C_A&=A'+A^2-W^2+2g(H+B),\\
C_W&=W'+2AW,\\
C_B&=B'+4KA(A^2+W^2).
\end{aligned}
\]

Direct differentiation gives the off-shell residual factorization

\[
\boxed{E_h=(x^2+y^2)C_H,\quad
E_u=xC_A-yC_W,\quad E_v=yC_A+xC_W,\quad
E_b=(x^2+y^2)C_B.}
\tag{RES}
\]

On any open annulus, (RES) is equivalent to all four ODEs. It also proves
that every sufficiently smooth ODE solution reconstructs a solution of
the original Cartesian equations on its declared chart.

The ODE time-derivative coefficient is the identity matrix; there is no
singular leading coefficient to divide out. Its polynomial right-hand side
gives a unique local analytic ODE solution from finite real initial values.
If H(t0)>0 then, while that solution exists,

\[
H(t)=H(t_0)\exp\left[-4\int_{t_0}^t A(s)\,ds\right]>0.
\]

This elementary ODE statement concerns the constructed invariant family.
It is not a theorem about arbitrary-data PDE well-posedness, hyperbolicity,
global continuation, or shocks.

One independently checked ODE first integral is

\[
I=\frac{W^2}{H},\qquad I'=0\quad(H>0).
\]

It is nonconstant as a function of the state and does not require division
by W. For a selected sign and nonzero W one could use it to eliminate one
dependent variable. That optional ODE simplification is distinct from the
rank-two reduction of independent-variable dimension already performed.

## 6. An exact evolving solution with nonzero swirl

There is a particularly simple reference family. Put t>0, choose a real
constant omega, and define

\[
\begin{aligned}
A&=\frac1{2t},& W&=\frac{\omega}{t},\\
B&=\frac{K(\omega^2+1/4)}{t^2},&
H&=\frac{(\omega^2+1/4)(1/(2g)-K)}{t^2}.
\end{aligned}
\tag{EX}
\]

All four ODE residuals vanish identically. For this particular family,
positive depth requires 2gK<1; that restriction does **not** apply to the
general local ODE construction. Taking omega nonzero gives swirl.

For g=1, K=1/30, omega=1, the fields are

\[
\boxed{\begin{aligned}
h&=\frac{7(x^2+y^2)}{12t^2},\\
u&=\frac{x/2-y}{t},\qquad v=\frac{y/2+x}{t},\\
b&=b_0+\frac{x^2+y^2}{24t^2}.
\end{aligned}}
\tag{EX1}
\]

These four expressions were substituted directly into the original
Cartesian m=3 system: all four residuals simplify to zero. At t=1 the
profile initial values are (H,A,W,B)=(7/12,1/2,1,1/24). This is a constructed
analytic reference, not a measured-flow experiment or a reproduced source
initial-value problem. On a compact interval 0<t0<=t<=t1 and an annulus
0<R_-<=r<=R_+, its depth and speed have explicit positive lower bounds.

There is also a simple stationary check for any real m: take A=0,
H=H0>0, W=W0 nonzero, and B=W0^2/(2g)-H0. The swirl balances the free-surface
slope, and the sediment flux is purely azimuthal with zero divergence.

## 7. Initial data, annular boundaries, and Cartesian regularity

Rotation alone admits arbitrary smooth radial profiles at an initial
time, subject to h>0 and any constitutive-law chart guard. The combined
family restricts initial data to

\[
h_0=r^2H_0,\quad V_0=rA_0,\quad w_0=rW_0,\quad
b_0(r)=\bar b+r^2B_0,
\]

with the same four constants across the entire annulus. Here bar b is the
constant bed datum, not the initial bed function. Both R and D leave an
initial-time slice t=t0 invariant because neither changes t.

For the annulus R_-<r<R_+, exact boundary traces at either radius R are

\[
h(t,R)=R^2H(t),\quad V(t,R)=RA(t),\quad w(t,R)=RW(t),\quad
b(t,R)=\bar b+R^2B(t).
\]

Thus boundary values at the two radii cannot be chosen independently.
Prescribing these traces constructs data compatible with the explicit
solution; it is not a claim that prescribing every component is a correct
well-posed boundary formulation for arbitrary nearby PDE data.

A fixed finite annulus is invariant under rotation, but is not invariant
under spatial scaling D. Accordingly one first derives the local
invariant solution and then restricts it to the annulus. It is incorrect
to call the fixed-annulus initial-boundary problem itself D-invariant.

For an impermeable circular wall, U dot n=0 at a positive radius implies
A=0 throughout the imposed time interval. The evolving reference (EX1)
therefore requires open boundaries with its induced fluxes, rather than
an impermeable wall. At r=R the outward normal is +e_r on the outer circle
and -e_r on the inner one. The water flux density and cubic physical
sediment flux density are respectively

\[
h\mathbf U\cdot\mathbf n=\pm R^3HA,\qquad
\mathbf q\cdot\mathbf n=\pm\kappa R^3A(A^2+W^2).
\]

The Exner balance uses the scaled flux q/(1-p), hence K replaces kappa.
For Delta4=R_+^4-R_-^4, exact integrated balances are

\[
\frac{d}{dt}\left(\frac\pi2H\,\mathrm{Delta4}\right)
+2\pi AH\,\mathrm{Delta4}=0,
\]

\[
\frac{d}{dt}\left[\frac\pi2B\,\mathrm{Delta4}
+\pi\bar b(R_+^2-R_-^2)\right]
+2\pi KA(A^2+W^2)\,\mathrm{Delta4}=0.
\]

Both were checked symbolically using (ODE).

The Cartesian reconstruction (CAR) is polynomial in x,y. It therefore
extends smoothly to the origin whenever its time coefficients are smooth.
At m=3 the polynomial equations continue to vanish there. But h(t,0)=0:
the origin is outside the assumed positive-depth chart, and the polar
orbit rank also changes there. A smooth algebraic extension must not be
presented as a positive-depth classical solution through the origin.

For the rotation-only family, sufficient smooth-axis conditions are
h=hat h(t,r^2), b=hat b(t,r^2), V=r hat V(t,r^2), and
w=r hat w(t,r^2), with the hatted functions smooth. Arbitrary radial
profiles need not have a smooth Cartesian extension. The present quadratic
family satisfies these sufficient regularity conditions but still has
zero depth at r=0.

## 8. Negative controls and exceptional branches

### Geometric terms cannot be dropped

For the stationary check g=1,H=B=1,W=2,A=0, the correct radial momentum
residual is -4r+4r=0. Removing -w^2/r leaves the nonzero residual 4r.
Removing the 1/r divergence geometry similarly changes the cubic depth
coefficient from 4AH to 3AH.

If the correct cubic ODE solution is evaluated in an incorrectly truncated
Exner equation with flux V^3, its residual is -4KAW^2 r^2. At A=W=K=1
this is -4r^2, not zero. This control detects losing swirl from the
transport magnitude.

### The same spatial powers do not generically close away from m=3

For the ansatz V=rA,w=rW,b=bar b+r^2B, the general-exponent Exner residual is

\[
\boxed{E_b=r^2B'+K(m+1)A(A^2+W^2)^{(m-1)/2}r^{m-1}.}
\tag{GEN}
\]

On an open radial interval, at nonzero speed, matching the two spatial
powers generically selects m=3. For example, at a cubic ODE jet with
A=W=K=1 and B'=-8, using m=2 produces

\[
E_b=-8r^2+3\sqrt2\,r,
\]

which is already nonzero at r=1.

There are important exceptions to the statement about generic closure:

* For m=-1, the coefficient m+1 vanishes. The radial sediment flux is
  proportional to 1/r and has zero divergence. The ansatz can satisfy the
  equations with B'=0 and the first three ODEs, on its nonzero-speed chart,
  even though D is not a symmetry of the full m=-1 equation system.
* For m different from 3 and -1, (GEN) requires A=0 and B'=0 throughout
  a time interval for this family. The other equations then require
  constant H,W and W^2=2g(H+B), giving the stationary swirling family above.

Thus failure of D as a full-system symmetry does not prove absence of all
special solutions with the same spatial powers. If the intended physical
exponent range excludes m=-1, retain it as a mathematical branch
qualification, not a physical calibration claim.

## 9. Verification receipt and scope

Two fresh in-memory Python/SymPy 1.14.0 calculations ran with a 60-second
subprocess timeout. They took approximately 3.9 seconds and 1.5 seconds.
The first checked 29 exact identities: polar pullback, velocity norm,
angular momentum, Cartesian residual factorization, R and D graph
equations including the bed offset, the ODE substitution, W^2/H, the
explicit solution, and the diagonal-weight defect. The second checked
11 exact identities: four prolonged R residuals, four prolonged D
residuals including the general-m defect, the general radial flux power,
and two annular integral balances. All 40 final checks returned zero.
The displayed negative witnesses returned the stated nonzero expressions.

An intermediate general-m D check failed at the level of symbolic
simplification: SymPy retained different powers of u^2+v^2. Its direct
specializations m=-1,0,1,2,3,4 all returned zero. Replacing u^2+v^2 by a
positive auxiliary norm, dividing out its nonzero common power, and then
substituting the norm identity reduced the symbolic general-m expression
to zero. This is justified only on the declared positive-speed chart and
is recorded as a CAS normalization failure, not a rejected generator or
an obstruction. The cubic polynomial checks did not need that division.

The parent computation task is responsible for permanent executable
tests, package-wide validation, source verification, and fresh review.
This note does not claim those steps are complete. No manuscript or
frozen evidence files were changed by this derivation task.

The mathematical conclusions are exact for the stated model and charts:
an admitted rotation, the diagonal scaling condition, the rotation
quotient retaining swirl, a rank-two cubic reduction, and constructed
Cartesian solutions with compatible data and fluxes. There is no claim
of maximal symmetry classification, new publication priority, generic
PDE well-posedness, arbitrary-data compatibility, global continuation,
shock behavior, or ML benefit.
