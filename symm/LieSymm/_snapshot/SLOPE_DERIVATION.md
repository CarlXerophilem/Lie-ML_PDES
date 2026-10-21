# Unrestricted local point classification of the 1D slope-diffusion SVE family

Status: complete necessary-equation integration and exact sufficient checks;
maximality claim awaits the independent fresh review required by CONTRACT.md.
This document concerns the full evolving-bed system, not either scalar SVE
control. No original manuscript, frozen source, or bibliography is modified.

## 1. Model, chart, and claim to be reviewed

Write

\[
\begin{aligned}
F_1&=h_t+u h_x+h u_x=0,\\
F_2&=u_t+u u_x+g(h_x+B_x)=0,\\
F_3&=B_t+C(u)u_x-D(u)B_{xx}-D'(u)u_xB_x=0,\\
C(u)&=mK u^{m-1},\qquad D(u)=G u^n.
\end{aligned}\tag{1}
\]

Work on a connected open chart with `h>0,u>0,g>0,G>0`; parameters are fixed.
For `K>0`, the requested laws are `n=m-1` and `n=m`, `1<=m<=4`.
For `K=0`, `m` disappears and the deduplicated range is `0<=n<=4`.
The calculations in fact allow any real `n` on the positive-speed chart.
Prime on `C,D` means a derivative in `u`; on one-variable functions of `t`
it means a derivative in `t`.

The result to be reviewed is

\[
\mathfrak g=\operatorname{span}\{\partial_t,\partial_x,\partial_B\}
\quad (K>0,\ m\ne3),\tag{2}
\]

and

\[
\mathfrak g=\operatorname{span}\{\partial_t,\partial_x,\partial_B,\mathcal D_n\},
\qquad
\mathcal D_n=(n-2)t\partial_t+(n-1)x\partial_x+
2h\partial_h+u\partial_u+2B\partial_B,
\tag{3}
\]

when `K=0` or `m=3`. No dependence restriction or polynomial ansatz is imposed
on the starting coefficients. The proof below integrates the necessary
determining equations and substitutes the result back into the full system.
Its maximality argument is that every smooth local point coefficient has been
forced into (2) or (3), not that a finite list of candidates was searched.

In particular, `K>0,m=3,n=2` admits a purely spatial base dilation, whereas
`K>0,m=3,n=3` admits a dilation of **both time and space**. Checking only the
first shape would incorrectly omit the second branch.

## 2. Mixed-order equation manifold and free jets

Let `p=h_x,q=u_x,r=B_x,v=B_xx` and start with the completely arbitrary field

\[
X=\tau(t,x,h,u,B)\partial_t+\xi(t,x,h,u,B)\partial_x+
a(t,x,h,u,B)\partial_h+b(t,x,h,u,B)\partial_u+
c(t,x,h,u,B)\partial_B.\tag{4}
\]

At order two impose `F1=F2=F3=0` **and** `D_t F1=D_x F1=D_t F2=D_x F2=0`.
The latter equations are necessary because the first two rows have order one.
Do not differentiate `F3` within `J2`: that would introduce third-order jets.
This gives the explicit triangular chart

\[
\begin{aligned}
h_t&=f_1=-up-hq,&u_t&=f_2=-uq-g(p+r),\\
B_t&=f_3=Dv+D'qr-Cq,\\
h_{tx}&=D_x f_1,&u_{tx}&=D_x f_2,\\
h_{tt}&=D_t f_1,&u_{tt}&=D_t f_2,
\end{aligned}\tag{5}
\]

where the right sides are reduced with the earlier equations. The free jets
may be taken as

\[
p,q,r,h_{xx},u_{xx},v,B_{tx},B_{tt}.\tag{6}
\]

The diagonal coefficients of the seven solved equations in (5) are all one.
In particular, the momentum time consequence solves `u_tt`; it does not
constrain `B_tx`. At higher order `D_x F3` can solve for `B_xxx` with coefficient
`-D!=0`, so freedom of `B_tx` in this projection is also consistent with the
prolonged evolution system. The symbolic verifier explicitly checks all four
order-two consequences of the first-order rows after applying (5).

Use the standard recursion

\[
\eta_i^\alpha=D_i\eta^\alpha-y_t^\alpha D_i\tau-y_x^\alpha D_i\xi,
\qquad
\eta_{xx}^\alpha=D_x\eta_x^\alpha-y_{tx}^\alpha D_x\tau-y_{xx}^\alpha D_x\xi.
\tag{7}
\]

All coefficients below are those of `pr X(Fj)` on (5). Prolonging the
first-order rows only to their actual order and the third row to order two
is sufficient: invariance of differential consequences then follows by the
prolongation commutator identity. The residuals contain no `h_tx,u_tx,h_tt,u_tt`
after (7), but their freedom was not assumed without the mixed-order chart.

## 3. Necessary projectability, derived from principal jets

The `B_tx` coefficient in the third residual is

\[
2D\,D_x\tau=2D(\tau_x+\tau_h p+\tau_u q+\tau_B r).\tag{8}
\]

Since `D=G u^n>0` and `p,q,r` are free, it follows that
`tau_x=tau_h=tau_u=tau_B=0`, hence `tau=tau(t)`.
With this restriction, the coefficients of `h_xx,u_xx` in the same residual
are

\[
-D(c_h-r\xi_h),\qquad -D(c_u-r\xi_u).\tag{9}
\]

Splitting in `r` gives `c_h=c_u=xi_h=xi_u=0`. Thus at this intermediate step
`c=c(t,x,B)` and `xi=xi(t,x,B)`. The `v` coefficient is now

\[
D(2\xi_x-\tau'+2r\xi_B)-D'b.\tag{10}
\]

The coefficient `b` is a point coefficient and therefore has no `r` dependence.
Splitting (10) in `r` gives `xi_B=0`, hence `xi=xi(t,x)`. We retain the rest of
(10), rather than divide by `D'` or `n`. This is essential to include `n=0`.

In the first two residuals, the `v` coefficients are respectively

\[
D a_B,\qquad D b_B.\tag{11}
\]

Therefore `a_B=b_B=0`. The `r` coefficient of the first residual then gives
`-g a_u=0`. Consequently all admissible fields satisfy

\[
\tau=\tau(t),\quad \xi=\xi(t,x),\quad
a=a(t,x,h),\quad b=b(t,x,h,u),\quad c=c(t,x,B).\tag{12}
\]

No projectability hypothesis was used to obtain (12).

## 4. Integrate the hydrodynamic determining equations

After (12), the first two residuals vanish if and only if the following seven
equations hold. They are displayed in coefficient order, so each can be
independently matched to the prolonged equations:

\[
\begin{array}{rll}
\text{coefficient of }p\text{ in }F_1:&h b_h+b-\xi_t+u(\tau'-\xi_x)=0,&(13a)\\
\text{coefficient of }q\text{ in }F_1:&a-ha_h+hb_u+h(\tau'-\xi_x)=0,&(13b)\\
\text{constant in }F_1:&a_t+u a_x+h b_x=0,&(13c)\\
\text{coefficient of }p/g\text{ in }F_2:&-b_u+a_h+\tau'-\xi_x=0,&(13d)\\
\text{coefficient of }q\text{ in }F_2:&-h b_h+b-\xi_t+u(\tau'-\xi_x)=0,&(13e)\\
\text{coefficient of }r/g\text{ in }F_2:&-b_u+c_B+\tau'-\xi_x=0,&(13f)\\
\text{constant in }F_2:&b_t+u b_x+g(a_x+c_x)=0.&(13g)
\end{array}
\]

Subtracting (13e) from (13a) gives `2h b_h=0`, so `b_h=0`. Their sum gives

\[
b=\xi_t+(\xi_x-\tau')u.\tag{14}
\]

Equations (13d,f) then imply

\[
a_h=c_B=2(\xi_x-\tau')=:A(t,x).
\tag{15}
\]

Integrating only in the indicated variables gives
`a=A h+H(t,x)`, `c=A B+J(t,x)`. Equation (13b) gives `H=0`.
Equation (13c), divided by nonzero `h` and split in `u`, is

\[
3\xi_{tx}-2\tau''=0,\qquad 3\xi_{xx}=0.\tag{16}
\]

Therefore `xi=L(t)x+R(t)` and `3L'-2tau''=0`. Equation (13g) becomes

\[
L''x+R''+(2L'-\tau'')u+gJ_x=0.\tag{17}
\]

Here `J` has no `u` dependence, so `2L'-tau''=0`. Combining with (16) gives
`L'=tau''=0`. Denote the constants by `L` and `T=tau'`, and set `d=L-T`.
The remaining part of (17) integrates to `J=-R''x/g+S(t)`. Every possible
point symmetry therefore has the form

\[
\boxed{
\begin{aligned}
\tau&=Tt+t_0,& \xi&=Lx+R(t),\\
a&=2dh,& b&=du+R'(t),\\
c&=2dB-R''(t)x/g+S(t),&d&=L-T.
\end{aligned}}
\tag{18}
\]

The two hydrodynamic residuals vanish identically for (18), as checked
symbolically. This intermediate family includes an arbitrary time-dependent
change of moving frame, coupled to a compensating bed slope; the third
equation decides whether it actually survives.

## 5. Integrate the entire remaining bed identity

Substitution of (18) into the third residual gives exactly

\[
\begin{aligned}
0={}&D\left[T+(2-n)d-\frac{nR'}u\right]v\\
&+D'\left[T+(2-n)d-\frac{(n-1)R'}u\right]qr\\
&+\left\{C\left[(m-3)d+\frac{(m-1)R'}u\right]
                +\frac{D'R''}{g}\right\}q\\
&-R'r-\frac{R'''}g x+S'.
\end{aligned}\tag{19}
\]

The independent monomials are `v,qr,q,r,1`. The plain `r` coefficient gives
`R'=0` even at `n=0` and `K=0`. It follows that `R''=R'''=0`. The constant
coefficient gives `S'=0`. The `v` coefficient, divided only by `D>0`, then
gives

\[
T+(2-n)d=0.\tag{20}
\]

The `qr` coefficient now vanishes by (20), including when `D'=0`.
The `q` coefficient gives

\[
mK(m-3)d=0.\tag{21}
\]

There are no further equations. In the required range `m>=1`, (21) says
`K=0` or `m=3` or `d=0`. If `d=0`, (20) gives `T=0`, then `L=0`, yielding
exactly the three translations (2). If `K=0` or `m=3`, then
`T=(n-2)d`, `L=(n-1)d`; `d` remains arbitrary and yields (3).

Every branch division used in the necessity proof is by one of
`D=G u^n`, `g`, `h`, or a nonzero numerical constant. The displayed rewriting
of powers in (19) uses `u>0`. There is **no division by** `n,n-1,n-2,m-3,K`.
Thus the special values `n=0,1,2` cannot be lost by the elimination.

## 6. Sufficiency, brackets, and exact branches

For arbitrary fixed real `m,n` on `u>0`, direct prolongation yields

\[
\left.\operatorname{pr}\mathcal D_n(F_1,F_2,F_3)\right|_{\mathcal E}
=\left(0,0,mK(m-3)u^{m-1}u_x\right).\tag{22}
\]

The three translations have identically zero residuals. Equation (22)
proves sufficiency on exactly the stated branches. Combined with the
unrestricted necessity proof, it proves the proposed classification,
subject to the separate required fresh-review gate.

| Fixed-parameter family | Dimension | Additional basis element |
| --- | ---: | --- |
| `K>0,G>0,n=m-1,m!=3` | 3 | none |
| `K>0,G>0,n=m,m!=3` | 3 | none |
| `K>0,G>0,m=3,n=2` | 4 | `x d_x+2h d_h+u d_u+2B d_B` |
| `K>0,G>0,m=3,n=3` | 4 | `t d_t+2x d_x+2h d_h+u d_u+2B d_B` |
| `K=0,G>0,0<=n<=4` | 4 | `D_n` in (3); no `m` parameter remains |

The nonzero brackets, with the displayed ordering convention, are

\[
[\mathcal D_n,\partial_t]=-(n-2)\partial_t,\quad
[\mathcal D_n,\partial_x]=-(n-1)\partial_x,\quad
[\mathcal D_n,\partial_B]=-2\partial_B.\tag{23}
\]

The finite flow of the extra generator is

\[
(t,x,h,u,B)\longmapsto
(e^{(n-2)\varepsilon}t,e^{(n-1)\varepsilon}x,
 e^{2\varepsilon}h,e^\varepsilon u,e^{2\varepsilon}B).\tag{24}
\]

It preserves the positive chart. This is the connected local point algebra;
no classification of disconnected finite transformations, optimal
subalgebras, boundary-data symmetries, reductions, or arbitrary-IBVP solvability
is asserted here. Equivalence between different parameter values is a
separate task and is not inferred from (23).

## 7. Independent symbolic verification and broken hypotheses

Run from the project root:

```powershell
python -B build/sve-general-symm-20261020/research_slope.py
```

The script implements total derivatives and point prolongation independently
of the main engine. It checks (5), each principal-jet identity (8)--(11), the
seven-coefficient reconstruction (13), the integrated hydro identities,
the **complete** remaining residual (19), and symbolic-parameter sufficiency
(22), and the constant-system solutions on all five slope branches. Its JSON
receipt records 40 passed exact identities in approximately 1.12 seconds.
The script is a verifier of the displayed
unrestricted derivation, rather than an automated PDE-integration oracle.

The callable `general_solution(branch, coordinates=None, exponent=None)` uses
`sympy.linsolve` on (20),(21) **after** the branch's parameter substitution.
It substitutes that solution into (18) with constant `R,S`, returns a
`coefficients` matrix and its `free_constants`, and derives each basis column
by differentiation with respect to those solved free constants. The generic
positive-`K` branches explicitly record `1<=m<=4,m!=3`, justifying the nonzero
coefficient `mK(m-3)` used in that linear solve. `coordinates` is the tuple
`(t,x,h,u,B)`, and `exponent` denotes `m` on positive-`K` branches or `n` on
`slope_only`. No preset basis list is used to construct a branch solution.

Broken-hypothesis controls give nonzero residuals:

* At `m=n=3`, the spatial-only field from the `n=2` branch has bed residual
  `-G u^3 B_xx-3G u^2 u_x B_x`; the mixed time-space generator in (3) succeeds.
* At `n=0,K=0`, the Galilean field `t d_x+d_u` has bed residual `-B_x`.
  Constant diffusion does not restore that boost.
* The time-dependent bed shift `t d_B` has bed residual `1`.
* At `m=2,K=1`, the proposed extra dilation has bed residual `-2u u_x`.

The model and allowed branches are taken from this task's `CONTRACT.md`.
The active README, manuscript introduction, project map and experiment index
were inspected to keep this full-system result separate from the earlier
scalar and bounded-ansatz evidence. No external literature novelty claim is
made by this calculation.
