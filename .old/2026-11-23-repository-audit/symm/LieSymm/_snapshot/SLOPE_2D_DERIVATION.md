# Unrestricted two-dimensional slope-family point symmetries

This is a new two-dimensional calculation. It does not infer completeness
from the one-dimensional classification. The starting point coefficients
are arbitrary smooth functions of all seven point coordinates. The result
below has a complete necessary-equation integration and an independent exact
verifier; the maximality release gate remains **pending fresh review**.

## 1. Model and regular chart

Let `r=(x,y)^T`, `w=(u,v)^T`, `q=u^2+v^2`, and

\[
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
F(w)=Kq^{(m-1)/2}w,\qquad D(w)=Gq^{n/2}.
\tag{1}
\]

The full evolving-bed system is

\[
\begin{aligned}
E_h&=h_t+w\cdot\nabla h+h\,\nabla\cdot w=0,\\
E_w&=w_t+(w\cdot\nabla)w+g\nabla(h+B)+fJw=0,\\
E_B&=B_t+\nabla\cdot F(w)-\nabla\cdot(D(w)\nabla B)=0.
\end{aligned}\tag{2}
\]

The signs in (2) are `-fv` in the x-momentum equation and `+fu` in the
y-momentum equation. `f` is a fixed constant, with separate `f=0` and
`f!=0` branches. Work on a connected open chart with

\[
h>0,\quad q=u^2+v^2>0,\quad g>0,\quad G>0.\tag{3}
\]

Neither `u` nor `v` is individually assumed nonzero. Thus the proof covers
regular points on either velocity axis, and joint rotations are admissible.
For `K>0`, `1<=m<=4` and the requested laws are `n=m-1` or `n=m`. For `K=0`,
`m` is absent and `0<=n<=4`. All powers are real smooth powers of positive `q`.

The generator is initially unrestricted:

\[
X=\tau\partial_t+\xi^1\partial_x+\xi^2\partial_y+
a\partial_h+b^1\partial_u+b^2\partial_v+c\partial_B,
\tag{4}
\]

where every one of the seven coefficients depends on `(t,x,y,h,u,v,B)`.

## 2. The mixed-order `J2` equation manifold

The mass and two momentum rows have order one. Their first differential
consequences in **all three** independent directions must therefore be
included at order two. Write their solved right sides as `R_h,R_u,R_v` and
the bed right side as

\[
R_B=-\nabla\cdot F+\nabla\cdot(D\nabla B).
\tag{5}
\]

Use the triangular chart

\[
\begin{aligned}
z_t&=R_z, &&z=h,u,v,B,\\
z_{tx_i}&=D_{x_i}R_z, &&z=h,u,v,\ i=1,2,\\
z_{tt}&=D_tR_z, &&z=h,u,v,
\end{aligned}\tag{6}
\]

reducing the right sides with earlier rules. The thirteen solved jet
coordinates have unit leading coefficients. All spatial first and second
jets remain free, as do `B_tx,B_ty,B_tt`. In particular, the momentum time
consequences solve `u_tt,v_tt`; they do not impose extra constraints on
`B_tx,B_ty`.

Differentiating the second-order bed row is not an additional `J2` equation.
On the infinite prolongation its first spatial derivatives give, at highest
order,

\[
B_{tx}=D(B_{xxx}+B_{xyy})+\cdots,\qquad
B_{ty}=D(B_{xxy}+B_{yyy})+\cdots.
\tag{7}
\]

Because `D>0`, the free third spatial derivatives can realize independent
values of `B_tx,B_ty`. Thus the `J2` freedom used below agrees with the
projection of the prolonged evolution system. The independent script checks
all nine order-two consequences of the first-order rows on (6).

## 3. Projectability is forced by the bed principal jets

Use the usual point-prolongation recursion, without a projectability ansatz:

\[
\eta_i^\alpha=D_i\eta^\alpha-z_j^\alpha D_i\xi^j,
\qquad
\eta_{ii}^\alpha=D_i\eta_i^\alpha-z_{ij}^\alpha D_i\xi^j,
\tag{8}
\]

where the base components are `(tau,xi^1,xi^2)` and repeated base indices
include time. The coefficients of the two free mixed jets `B_tx_i` in
`pr X(E_B)` on (6) are

\[
2D\,D_{x_i}\tau,\qquad i=1,2.\tag{9}
\]

Splitting their total derivatives in all free spatial first jets gives
`tau=tau(t)`. No spatial or field dependence of `tau` survives.

For any fluid field `z=h,u,v`, the coefficient of `z_xx` is then

\[
-D\left(c_z-B_x\xi^1_z-B_y\xi^2_z\right).\tag{10}
\]

The independent `B_x,B_y` give `c_z=xi^1_z=xi^2_z=0`. Hence the spatial
coefficients and `c` may depend only on `(t,x,y,B)` at this stage.

The coefficients of `B_xx,B_yy,B_xy` are, respectively,

\[
\begin{aligned}
&D(2\xi^1_x-\tau'+2B_x\xi^1_B)-D_w\cdot b,\\
&D(2\xi^2_y-\tau'+2B_y\xi^2_B)-D_w\cdot b,\\
&2D(\xi^1_y+\xi^2_x+B_y\xi^1_B+B_x\xi^2_B).
\end{aligned}\tag{11}
\]

Because `b` is a point coefficient, it has no jet dependence. Splitting (11)
gives `xi^1_B=xi^2_B=0` and the plane conformality equations

\[
\xi^1_x=\xi^2_y=:\sigma,\qquad \xi^1_y+\xi^2_x=0.
\tag{12}
\]

The remaining scalar Hessian coefficient is retained as

\[
(2\sigma-\tau')D-D_w\cdot b=0.\tag{13}
\]

In particular, (13) is **not** divided by `n` or by `D_w`.

The Laplacian coefficients in the three hydrodynamic rows are
`D a_B,D b^1_B,D b^2_B`. They give `a_B=b^1_B=b^2_B=0`. The two bed-gradient
coefficients in the mass row now give `-g a_u=-g a_v=0`. Thus every possible
point symmetry already satisfies

\[
\tau=\tau(t),\quad \xi=\xi(t,x,y),\quad
a=a(t,x,y,h),\quad b=b(t,x,y,h,u,v),\quad c=c(t,x,y,B).
\tag{14}
\]

This conclusion holds at `n=0`, at `u=0`, and at `v=0` on (3).

## 4. The full remaining hydro determining polynomial

To make the integration checkable, define matrices

\[
A_{ij}=\partial_{x_j}\xi^i,\quad
P_{ij}=\partial_{x_j}w_i,\quad
(B_w)_{ij}=\partial_{w_j}b^i,
\qquad V=b-\xi_t+\tau'w-Aw.
\tag{15}
\]

Partial derivatives in the following constant terms hold the dependent
variables fixed. The mass residual after (14) is exactly

\[
\begin{aligned}
\mathcal R_h={}&a_t+w\cdot\nabla_x a+h\,\nabla_x\cdot b
 +(V+h b_h)\cdot\nabla h\\
&+\sum_{i,j}\left[h((B_w)_{ij}-A_{ij})
 +(a-ha_h+h\tau')\delta_{ij}\right]P_{ji}.
\end{aligned}\tag{16}
\]

The two momentum residuals form the vector

\[
\begin{aligned}
\mathcal R_w={}&b_t+(w\cdot\nabla_x)b+g\nabla_x(a+c)
 +f\{Jb-B_wJw+\tau'Jw\}\\
&+g\{(a_h+\tau')I-B_w-A^T\}\nabla h\\
&+g\{(c_B+\tau')I-B_w-A^T\}\nabla B
 +PV-hb_h\operatorname{tr}P.
\end{aligned}\tag{17}
\]

The script reconstructs all three complete residuals from (16),(17). These
are determining identities in free first jets, not identities tested on a
finite collection of sample fields.

In the first momentum component, the coefficient of `v_y` gives
`-h b^1_h=0`; in the second, the coefficient of `u_x` gives `-h b^2_h=0`.
Thus `b_h=0`. All remaining independent `P` coefficients in (17) then give
`V=0`, hence

\[
b=\xi_t+(A-\tau'I)w.\tag{18}
\]

Subtract the two gradient-matrix identities in (17). They give
`a_h=c_B=:chi(t,x,y)`. Substituting (18) into either matrix identity and
using (12) gives

\[
\chi=2(\sigma-\tau'),\qquad
a=\chi h+H(t,x,y),\qquad c=\chi B+\psi(t,x,y).
\tag{19}
\]

The diagonal `P` coefficient of (16) is now `H`, so `H=0`. Its constant part,
divided only by `h>0`, becomes

\[
4\sigma_t-2\tau''+4w\cdot\nabla\sigma=0.\tag{20}
\]

An identity linear in `(u,v)` on an open nonzero-speed chart has all its
coefficients zero. Therefore `sigma=sigma(t)` and `tau''=2sigma'`.
Integrating the two conformality equations (12), with spatially uniform
`sigma`, yields

\[
\xi=(\sigma(t)I+\omega(t)J)r+p(t),\qquad A=\sigma I+\omega J.
\tag{21}
\]

Thus affine dependence on the spatial coordinates has been **derived**.
It was not imposed at the beginning of the calculation.

## 5. Integrate all hydro time dependence before using the bed equation

Put `alpha=sigma-tau'`, so `chi=2alpha`. The constant part of (17) reduces to

\[
\xi_{tt}+fJ\xi_t+g\nabla\psi
 +\{(2\sigma'-\tau'')I+(2\omega'+f\tau')J\}w=0.
\tag{22}
\]

Consequently

\[
\tau''=2\sigma',\qquad 2\omega'+f\tau'=0,
\qquad \nabla\psi=-\frac{\xi_{tt}+fJ\xi_t}{g}.
\tag{23}
\]

The curl condition on the last expression is
`omega''+f sigma'=0`, already the derivative consequence of the first two
equations. Write the fully integrated hydro family as

\[
\begin{aligned}
\sigma&=\tfrac12\tau'+k,&\omega&=\omega_0-\tfrac12f\tau,\\
\xi&=(\sigma I+\omega J)r+p(t),&
b&=\xi_t+(A-\tau'I)w,\\
a&=2(\sigma-\tau')h,&c&=2(\sigma-\tau')B+\psi,
\end{aligned}\tag{24}
\]

where `tau(t)`, the two components of `p(t)`, and `S(t)` are still arbitrary,
`k,omega_0` are constants, and

\[
\psi=-\frac{\tau'''+f^2\tau'}{4g}(x^2+y^2)
      -\frac{(p''+fJp')\cdot r}{g}+S(t).
\tag{25}
\]

Substitution of (24),(25) makes **all three** hydrodynamic residuals exactly
zero. These arbitrary time functions have not been discarded on an ansatz
or physical plausibility argument; the evolving-bed equation removes them.

## 6. Integrate the bed determining identity without losing exponent strata

For a scalar radial diffusivity and the radial vector flux in (1),

\[
F_w(\alpha I+\omega J)w=(m\alpha I+\omega J)F,
\qquad D_w\cdot(\alpha I+\omega J)w=n\alpha D.
\tag{26}
\]

These identities follow from homogeneity and rotational covariance, and are
checked symbolically with arbitrary real `m,n`. Define

\[
L=(2\sigma-\tau')D-D_w\cdot b.
\tag{27}
\]

For (21),(24), direct prolongation and the original bed equation yield the
**complete** remaining residual

\[
\begin{aligned}
\mathcal R_B={}&\chi'B+\psi_t-\xi_t\cdot\nabla B
 +\nabla\cdot(F_w\xi_t)
 +(m-3)\alpha\,\nabla\cdot F\\
&+\nabla\cdot(L\nabla B)-\nabla\cdot(D\nabla\psi).
\end{aligned}\tag{28}
\]

For independent checking of the entire divergence transformation, before
using radial homogeneity the same residual is

\[
\begin{aligned}
&(\chi-\tau')B_t+\chi'B+\psi_t-\xi_t\cdot\nabla B
 +\nabla\cdot(F_wb-AF)\\
&\quad-\nabla\cdot\left(
 \{(D_w\cdot b+\chi D)I-D(A+A^T)\}\nabla B+D\nabla\psi\right),
\end{aligned}\tag{29}
\]

with `B_t` replaced using (5). The verifier checks (29) against direct
prolongation with arbitrary smooth functions `D(u,v),F1(u,v),F2(u,v)`.
It separately checks (26), so no special exponent sample stands in for (28).

The Hessian coefficient (13) is exactly `L=0`. Since this is an identity in
all point variables, all its total derivatives vanish, and the entire term
`div(L grad B)` can now be removed from (28). Every other term except
`-xi_t dot grad B` is independent of the bed gradient. Splitting the two free
bed-gradient components therefore gives

\[
\xi_t=0.\tag{30}
\]

This step also works when `n=0`; it never divides by the velocity derivative
of `D`. It rules out moving-frame and time-dependent-rotation remnants.
Equations (21),(23),(30) give

\[
\sigma'=\omega'=p'=\tau''=0,\qquad f\tau'=0,
\qquad \nabla\psi=0.\tag{31}
\]

Hence `chi'=0` as well, and `psi=S(t)`. Equation (28) is reduced to

\[
S'+(m-3)\alpha\,\nabla\cdot F=0.\tag{32}
\]

Its constant term gives `S'=0`. The coefficient matrix of the free velocity
gradient in the second term is `(m-3)alpha F_w`. This matrix cannot vanish
identically when `K>0,1<=m<=4`: contracting it along `w` uses the exact identity

\[
w^TF_ww=mKq^{(m+1)/2}.\tag{33}
\]

On (3), (32) is therefore equivalent to `mK(m-3)alpha=0`. No coordinate
velocity was divided out in this contraction. At `K=0` the complete source
term is already zero and `m` must be removed.

## 7. Final constant system and complete candidate classification

Let `T=tau'`, `L_0=sigma`, and `d=L_0-T`. The fully integrated generator is

\[
\boxed{
\begin{aligned}
\tau&=Tt+t_0,\\
\xi^1&=(T+d)x-\omega_0y+x_0,\\
\xi^2&=\omega_0x+(T+d)y+y_0,\\
a&=2dh,\qquad b^1=du-\omega_0v,\qquad b^2=\omega_0u+dv,\\
c&=2dB+b_0,
\end{aligned}}
\tag{34}
\]

subject to exactly three constant equations:

\[
\boxed{T+(2-n)d=0,\qquad mK(m-3)d=0,\qquad fT=0.}\tag{35}
\]

The first is (27) after (30); the other two were derived in (31),(33).
The function `general_solution` uses `sympy.linsolve` on this actual system
after the declared branch specialization, then differentiates the solved
coefficients with respect to their remaining constants to obtain the basis.

Every branch contains

\[
T_0=\partial_t,\quad X_0=\partial_x,\quad Y_0=\partial_y,\quad
Z_0=\partial_B,\quad
\mathcal R=-y\partial_x+x\partial_y-v\partial_u+u\partial_v.
\tag{36}
\]

The spatial and velocity parts of `R` are inseparable: a spatial rotation
alone is generally not a symmetry. An additional independent basis element
exists precisely when

\[
(K=0\ \text{or}\ m=3)\quad\text{and}\quad f(n-2)=0,
\tag{37}
\]

and is

\[
\mathcal D_n=(n-2)t\partial_t+(n-1)(x\partial_x+y\partial_y)
 +2h\partial_h+u\partial_u+v\partial_v+2B\partial_B.
\tag{38}
\]

| Model branch | `f=0` dimension | `f!=0` dimension |
| --- | ---: | ---: |
| `K>0,m!=3`, either slope law | 5 | 5 |
| `K>0,m=3,n=m-1=2` | 6 | 6 |
| `K>0,m=3,n=m=3` | 6 | 5 |
| `K=0,n=2` | 6 | 6 |
| `K=0,0<=n<=4,n!=2` | 6 | 5 |

The rotating slope-only family must therefore be split into the explicit
registry cells `slope_only_generic_f_nonzero` and
`slope_only_n2_f_nonzero`. The nonrotating slope-only family needs no
additional dimension strata. There is no loss of a branch at `n=0` or at
`m=1`: both remain in the unrestricted derivation above.

## 8. Exact sufficiency, verification receipts, and limits

Direct point prolongation of (38) on the original system gives

\[
\left.\operatorname{pr}\mathcal D_n(E_h,E_u,E_v,E_B)\right|_{\mathcal E}
=\left(0,-f(n-2)v,f(n-2)u,(m-3)\nabla\cdot F\right).
\tag{39}
\]

The five fields in (36) have zero residuals for arbitrary real `m,n` on (3).
Thus (39) proves sufficiency on exactly (37). The necessity argument
(9)--(35), rather than a finite affine trial space, supplies the proposed
maximality. The separate review gate must accept both parts before release.

The independent verifier has its own total derivatives and recursive point
prolongation; it does not import the parent engine. It checks unrestricted
principal-jet coefficients, all nine first-row consequences, the complete
hydro determining polynomial, the arbitrary-time hydro family, the full
bed divergence transformation, arbitrary-exponent radial identities, and
the final generator obstruction. Individual coordinate axes are never
excluded by a division.

Run with an enforced process timeout from the project root:

```powershell
python -B -c "import subprocess,sys; subprocess.run([sys.executable,'-B','build/sve-general-symm-20261020/research_slope_2d.py','--phase','all','--timeout-seconds','60'],timeout=60,check=True)"
```

The `--timeout-seconds` flag records metadata; the outer `subprocess` enforces
the actual limit. The result is written only to `slope_2d_results.json`.
The repaired complete run passed all **90 exact checks** in **5.993 seconds**
under the enforced 60-second process limit. Its classification status remains
`unrestricted_classification_pending_fresh_review`.
The four selectable phases (`principal`, `hydro`, `bed`, `final`) allow a
slow check to be decomposed without declaring a mathematical obstruction.

For general real exponents, raw SymPy simplification may leave
`u^2 q^a+v^2 q^a-q^(a+1)` structurally nonzero. The verifier groups only
integer shifts of the **same actual radial power**, then imposes
`q=u^2+v^2>0` on rational coefficients. It never treats related radial powers
as independent symbols. The first run exposed precisely this normalization
issue in (33); it was resolved by that guarded algebraic normalization.

Broken-hypothesis controls include spatial rotation without velocity
rotation, the rejected `m=n=3` dilation at `f!=0`, and a time-dependent bed
gauge. No conditional/nonclassical symmetry, optimal-system completeness,
boundary-data compatibility, arbitrary-IBVP theorem or learned result is
inferred here. The frozen stage-one files are unchanged.
