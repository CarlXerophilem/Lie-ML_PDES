# Unrestricted 2+1 first-order SVE point algebra, with and without Coriolis

This new stage-2 calculation treats the full four-field Eulerian system. No
stage-1 file is modified, and no scalar or one-dimensional classification is
transferred to the two-dimensional equations. The argument starts with
arbitrary smooth point coefficients and derives every restriction. The
result is ready for, and remains subject to, independent review.

## 1. Model and the integrated answer

Let \(w=(h,u,v,B)^T\), \(z=(u,v)^T\), and \(r^2=u^2+v^2\). The equations are
\[
\begin{split}
h_t+(hu)_x+(hv)_y&=0,\\
u_t+uu_x+vu_y+g(h+B)_x-fv&=0,\\
v_t+uv_x+vv_y+g(h+B)_y+fu&=0,\\
B_t+K\operatorname{div}(r^{m-1}z)&=0. \tag{1}
\end{split}
\]
Work on an open connected point-coordinate domain with \(h>0,r^2>0\),
fixed \(g>0\), fixed \(K\geq0\), fixed real \(1\leq m\leq4\) when
\(K>0\), and fixed real Coriolis constant \(f\). When \(K=0\), remove
\(m\) completely. Real powers of \(r^2>0\) are smooth on this chart.

Every local smooth point generator is
\[
\begin{split}
X={}&(at+t_0)\partial_t+(px-\omega y+x_0)\partial_x
 +(\omega x+py+y_0)\partial_y\\
 &+2(p-a)h\partial_h+\{(p-a)u-\omega v\}\partial_u
 +\{\omega u+(p-a)v\}\partial_v\\
 &+\{2(p-a)B+b_0\}\partial_B, \tag{2}
\end{split}
\]
where all seven displayed coefficients are constants and
\[
K(m-3)(p-a)=0,\qquad fa=0. \tag{3}
\]
The first condition is absent, rather than parameterized by an artificial
exponent, when \(K=0\).

| Branch | \(f=0\) dimension | \(f\ne0\) dimension |
|---|---:|---:|
| \(K>0,m\ne3\) | 6 | 5 |
| \(K>0,m=3\) | 7 | 6 |
| \(K=0\), exponent removed | 7 | 6 |

These dimensions count equation symmetries, not data stabilizers. Constant
bed shift and planar rotations survive every row of the table. A fixed
nonzero \(f\) excludes time dilation; it does not exclude spatial/field
dilation when the transport branch permits it.

## 2. Arbitrary point coefficients and the first-order matrix form

Start with
\[
X=\tau(t,x,y,w)\partial_t+\xi(t,x,y,w)\partial_x
 +\chi(t,x,y,w)\partial_y+\eta(t,x,y,w)\mathbin{\cdot}\partial_w,
\quad\eta=(H,U,V,Z)^T. \tag{4}
\]
There is no affine ansatz and no projectability assumption. Define
\[
Q=D_z(Kr^{m-1}z)
=Kr^{m-3}\begin{pmatrix}mu^2+v^2&(m-1)uv\\(m-1)uv&u^2+mv^2\end{pmatrix}
=\begin{pmatrix}q_{11}&q_{12}\\q_{12}&q_{22}\end{pmatrix}. \tag{5}
\]
The PDE is \(w_t+Aw_x+Cw_y=F\), with
\[
A=\begin{pmatrix}u&h&0&0\\g&u&0&g\\0&0&u&0\\0&q_{11}&q_{12}&0\end{pmatrix},\quad
C=\begin{pmatrix}v&0&h&0\\0&v&0&0\\g&0&v&g\\0&q_{12}&q_{22}&0\end{pmatrix},\quad
F=\begin{pmatrix}0\\fv\\-fu\\0\end{pmatrix}. \tag{6}
\]
All eight spatial first derivatives are free because the four equations are
in evolution normal form. The first prolongation, restricted by
\(w_t=F-Aw_x-Cw_y\), is polynomial of degree at most two in those derivatives.
Its coefficients are necessary and sufficient determining equations.
`build_determining_system()` constructs them from (4) without projectability.

## 3. Derive projectability from pure-direction quadratic jets

Set the \(y\) derivatives to zero when examining the quadratic terms, and
write \(k=w_x\), \(r_\tau=\partial_w\tau\),
\(r_\xi=\partial_w\xi\). Their vector coefficient is
\[
A^2k(r_\tau k)-Ak(r_\tau Ak)+k(r_\xi Ak)-Ak(r_\xi k). \tag{7}
\]
The Coriolis source is of order zero and does not contribute to (7). At a
state with distinct eigenvalues \(\lambda_i\) of \(A\), the coefficient of
\(k_i k_j\) in component \(i\), for \(i\ne j\), is
\[
(\lambda_i-\lambda_j)(\lambda_i(r_\tau)_j-(r_\xi)_j). \tag{8}
\]
For each \(j\), choose two other, distinct eigenvalues. The two equations
force \((r_\tau)_j=(r_\xi)_j=0\). The identical \(y\)-direction argument
gives \(\partial_w\chi=0\).

Here are the required spectrum checks, including all exceptional state
surfaces. Reorder the \(x\)-direction fields as \((h,u,B,v)\). The diagonal
blocks are
\[
A_3=\begin{pmatrix}u&h&0\\g&u&g\\0&q_{11}&0\end{pmatrix},\qquad (u).
\]
For \(K>0\), \(q_{11}>0\): the factors are \(K>0,r^{m-3}>0\), and
\(mu^2+v^2>0\), using \(m\geq1,r^2>0\).
\(\operatorname{diag}(g/h,1,g/q_{11})A_3\) is symmetric and its symmetric
similarity form has nonzero adjacent entries. The elementary tridiagonal
eigenvector recurrence gives three simple eigenvalues. Moreover,
\[
\det(\lambda I-A_3)|_{\lambda=u}=-ghu, \tag{9}
\]
so the fourth eigenvalue \(u\) is distinct whenever \(u\ne0\).
For \(K=0\),
\[
\det(\lambda I-A)=(\lambda-u)\lambda\{(\lambda-u)^2-gh\}, \tag{10}
\]
which has distinct roots when \(u\ne0\) and \(u^2\ne gh\).
The analogous statements hold for \(C\) with \(u\) replaced by \(v\).

Each excluded state set is a hypersurface with empty interior in the
declared open domain. The conclusions extend to it by continuity of the
smooth coefficient derivatives. A symmetry defined only on such a
constraint surface is a different PDE problem. Consequently,
\[
\tau=\tau(t,x,y),\quad\xi=\xi(t,x,y),\quad\chi=\chi(t,x,y). \tag{11}
\]
This is full projectability, obtained without a spatial-affinity assumption.

## 4. Projectable determining matrices

Let \(J=\partial_w\eta\). After (11), the residual is
\(C_0+M_xw_x+M_yw_y\), where
\[
\begin{split}
M_x={}&AJ-JA+\eta\cdot\partial_wA
 +(\tau_t-\xi_x)A-\xi_yC+\tau_xA^2+\tau_yCA-\xi_tI,\\
M_y={}&CJ-JC+\eta\cdot\partial_wC
 -\chi_xA+(\tau_t-\chi_y)C+\tau_xAC+\tau_yC^2-\chi_tI,\\
C_0={}&\eta_t+A\eta_x+C\eta_y+(J-\tau_tI)F-F_w\eta
 -\tau_xAF-\tau_yCF. \tag{12}
\end{split}
\]
These equations are necessary and sufficient after the already proved
projectability. The code independently compares (12) with direct first
prolongation, retaining a general projectable base field and arbitrary
vertical coefficient functions.

## 5. A passive eigenpair and two traces force \(\tau=\tau(t)\) and static spatial coefficients

On \(u\ne0\), a right/left pair for the eigenvalue \(u\) of \(A\) is
\[
r_x=(-q_{12}/u,0,1,q_{12}/u)^T,\qquad \ell_x=(0,0,1,0).
\]
It satisfies \(\ell_xr_x=1\), \(\ell_xCr_x=v\), and
\(\ell_x(\eta\cdot\partial_wA)r_x=U\). Hence
\(\ell_xM_xr_x=0\) gives
\[
U=\xi_t+(\xi_x-\tau_t)u+\xi_yv-u(\tau_xu+\tau_yv). \tag{13}
\]
The \(y\)-direction pair
\(r_y=(-q_{12}/v,1,0,q_{12}/v)^T\), \(\ell_y=(0,1,0,0)\)
similarly gives
\[
V=\chi_t+\chi_xu+(\chi_y-\tau_t)v-v(\tau_xu+\tau_yv). \tag{14}
\]
These identities extend by smoothness across \(u=0\) and \(v=0\).

The relevant trace identities are
\[
\operatorname{tr}A=3u,\quad\operatorname{tr}C=3v,\quad
\operatorname{tr}A^2=3u^2+2g(h+q_{11}),\quad
\operatorname{tr}(CA)=3uv+2gq_{12}. \tag{15}
\]
Substituting (13)--(14) in \(\operatorname{tr}M_x=\operatorname{tr}M_y=0\)
gives
\[
\begin{split}
\xi_t&=2g\{\tau_x(h+q_{11})+\tau_yq_{12}\},\\
\chi_t&=2g\{\tau_xq_{12}+\tau_y(h+q_{22})\}. \tag{16}
\end{split}
\]
The left sides and \(\tau_x,\tau_y\) depend only on base coordinates;
\(Q\) has no depth dependence. Split the free variable \(h\):
\[
\tau_x=\tau_y=0,\qquad \xi_t=\chi_t=0. \tag{17}
\]
Thus \(\tau=\tau(t)\), and \(\xi,\chi\) are arbitrary functions of
\((x,y)\) at this stage. Put \(a=\tau_t\). Equations (13)--(14) reduce to
\[
\binom UV=(D_{(x,y)}(\xi,\chi)^T-aI)\binom uv. \tag{18}
\]
No transport coefficient was divided out in this step; it includes \(K=0\).

## 6. Water rows force a conformal spatial field and determine all vertical coefficients

For compactness write
\(p=\xi_x,q=\xi_y,r=\chi_x,s=\chi_y\) temporarily. Equation (18) gives
\(U=(p-a)u+qv\), \(V=ru+(s-a)v\). Use actual entries of (12), rather
than relying on trace equations alone:

1. \((M_x)_{hh}=-gH_u\) and \((M_y)_{hh}=-gH_v\) give \(H_u=H_v=0\).
   Their \((h,B)\) entries then give \(uH_B=vH_B=0\); since \(r^2>0\),
   \(H_B=0\). The \((h,u)\) entry is \(H-hH_h=0\). Therefore
   \(H=d(t,x,y)h\).

2. The cross momentum/depth entry gives \(-g(q+r)=0\), while the difference
   of the two diagonal momentum/depth entries gives \(2g(s-p)=0\).
   Consequently
   \[
   \xi_x=\chi_y=p,\qquad\chi_x=-\xi_y=\omega. \tag{19}
   \]
   These are the planar conformal (Cauchy--Riemann) equations, not yet an
   assumption that the spatial map is affine.

3. The other momentum entries give
   \[
   Z_u=Z_v=0,\quad Z_h=2(p-a)-d,\quad Z_B=2(p-a). \tag{20}
   \]
   The bed-row/depth entries, after \(Z_u=Z_v=0\), are
   \(-uZ_h=-vZ_h=0\). Again \(r^2>0\) forces \(Z_h=0\), even when
   \(K=0\). Thus \(d=2(p-a)\).

Putting \(\lambda=p-a\), the unrestricted vertical coefficients are now
\[
H=2\lambda h,\quad U=\lambda u-\omega v,\quad
V=\omega u+\lambda v,\quad Z=2\lambda B+z(t,x,y). \tag{21}
\]
At this point \(p,\omega\) can still depend on \((x,y)\), and \(a\)
can still depend on \(t\). Their later constancy will follow from the
constant-jet equations.

## 7. Bed-row homogeneity gives the complete transport stratum

Let \(R=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)\).
The radial tensor in (5) satisfies the exact identities
\[
(u\partial_u+v\partial_v)Q=(m-1)Q,\qquad
(-v\partial_u+u\partial_v)Q=RQ-QR. \tag{22}
\]
Substitute (19)--(21) in the remaining bed-row entries of (12). The rotation
terms cancel by the second identity, and the resulting two velocity rows
are exactly the two rows of
\[
\lambda(m-3)Q=0. \tag{23}
\]
For \(K>0\), \(q_{11}>0\), so (23) is equivalent to
\((m-3)\lambda=0\). For \(K=0\), \(Q=0\), so it imposes no condition.
The proof does not divide by \(m-1\); the endpoint \(m=1\) is covered
without an unexamined special case. Within \(1\leq m\leq4\), the only
positive-transport exponent enhancement is \(m=3\).

## 8. Constant jets eliminate nonlinear conformal fields and determine the Coriolis stratum

Differentiate (19). Its integrability identities are
\[
\omega_y=p_x,\qquad\omega_x=-p_y. \tag{24}
\]
Substitute (21) in the continuity component of \(C_0=0\). Since
\(\lambda_t=-a_t\), \(\lambda_x=p_x\), and \(\lambda_y=p_y\), that
single equation is
\[
h\{-2a_t+(3p_x+\omega_y)u+(3p_y-\omega_x)v\}
=h\{-2a_t+4p_xu+4p_yv\}=0. \tag{25}
\]
Free variation of \(u,v\) on the open nonzero-speed chart gives
\(a_t=p_x=p_y=0\). Equation (24) gives
\(\omega_x=\omega_y=0\). Therefore \(a,p,\omega\) are constants and
\[
\tau=at+t_0,\quad\xi=px-\omega y+x_0,\quad
\chi=\omega x+py+y_0. \tag{26}
\]
This is where affine dependence is **derived**, rather than imposed.

The remaining constant-jet equations reduce to
\[
gz_x-afv=0,\qquad gz_y+afu=0,\qquad z_t=0. \tag{27}
\]
Because \(z\) is independent of \(u,v\), their free variation implies
\(af=0\), \(z_x=z_y=z_t=0\). Thus \(z=b_0\), proving all necessity
claims in (2)--(3). In particular, a fixed nonzero Coriolis constant removes
time scaling. The sign of \(f\ne0\) introduces no further local
point-algebra stratum.

## 9. Sufficiency and useful failure controls

For the general constant-coefficient integral (2), direct prolongation of
all four original rows has the on-shell residual
\[
\begin{pmatrix}
0\\-afv\\afu\\(p-a)(m-3)K\operatorname{div}(r^{m-1}z)
\end{pmatrix}. \tag{28}
\]
In the last entry, \(K\operatorname{div}(r^{m-1}z)\) denotes its
first-jet expression, not a substituted zero on the PDE. It vanishes
identically exactly under the terminal constraints (3). This proves
sufficiency. Combined with Sections 2--8, it proves maximality among the
declared unrestricted local smooth point fields, pending independent review.

A Galilean boost \(t\partial_x+\partial_u\) already fails at \(K=f=0\):
its bed-row residual is \(-B_x\). The full \(B_t=0\) system retains an
arbitrary spatial bed field, so flat-bed boosts cannot be appended.
Similarly, the nonlinear conformal candidate
\[
(x^2-y^2)\partial_x+2xy\partial_y+4xh\partial_h
 +(2xu-2yv)\partial_u+(2yu+2xv)\partial_v+4xB\partial_B
\]
has mass-row residual \(8hu\), even at \(K=f=0\). Thus local conformal
freedom from the derivative equations does not survive the full determining
system as an infinite-dimensional family.

## 10. Implementation, evidence, and nonclaims

`general_solution(branch, coordinates=None, exponent=None, f_value=None)`
accepts names such as `grass_generic_f0`, `grass_cubic_f_nonzero`, and
`zero_transport_f0`, optionally prefixed by `2d__`. It solves the two
terminal constant equations with `linsolve`, returns the integrated
coefficients and surviving constants, and obtains a basis by differentiating
those coefficients. Coordinate order is `(t,x,y,h,u,v,B)`. Custom exponent
and Coriolis inputs must be fixed finite real constants, independent of the
supplied point coordinates; the API rejects detected violations and carries
undecided real/finite conditions as guards.

`integration_certificate()` supplies the passive-eigenpair equations,
their solved velocity coefficients, and the trace elimination data.
`build_determining_system()` is independently available for the full
arbitrary-coefficient determining polynomial. `run_verification()` checks
the critical identities, the general solution on all six parameter cells,
and explicit rejected candidates. The readable integration proof is needed
for necessity; finite symbolic candidate checks are not a replacement.

Run the verifier within the symbolic CPU lease and a bounded subprocess:

```powershell
python -c "import subprocess; subprocess.run(['python','-B','build/sve-general-symm-20261020/research_first_order_2d.py'], timeout=60, check=True)"
```

The final receipt records **55/55 exact checks passed in 4.88 seconds**.
The initial run passed 48/49; the Euler homogeneity identity was left as an
uncombined zero involving neighboring real powers of \(u^2+v^2\). That
failed receipt is retained at `runs/first_order_2d_initial_failure.json`.
The repair uses a positive temporary radius-squared symbol, groups only
integer shifts of its powers, and restores its defining polynomial in each
coefficient. It does not assume that either velocity component is positive.

The verifier writes only `first_order_2d_results.json`. No claim is made about the
zero-speed maximal algebra, generalized/contact/nonlocal symmetries,
disconnected equivalence transformations, an optimal subalgebra system,
initial/boundary-data compatibility, arbitrary-data well-posedness,
conditional symmetries, or machine learning.
