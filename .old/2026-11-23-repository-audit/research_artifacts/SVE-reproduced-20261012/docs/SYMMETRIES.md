# Printed scalar SVE: unrestricted point symmetries and algebra audit

Source: Paliathanasis, Leon, and Leach, *Mathematics* **14** (2026) 433,
local v3 PDF `ref/main/*00433-v3.pdf`, equation (7), Proposition 1 and its
displayed determining equations (p. 4), Tables 1-2 and the one-dimensional
list (pp. 5-6). This is an audit of **that printed scalar equation**, not of
the advectively corrected scalar model or the full bed-field system.

## Equation and branch

Set $u=\phi$, $p=u_t>0$, $q=u_s>0$, $a=u_{tt}$, $b=u_{ts}$,
$c=u_{ss}$, $r=u_{ttt}$, $w=u_{tts}$, $x=u_{tss}$, $y=u_{sss}$.
Let $g,\kappa>0$, $m\geq1$, and $\beta=m\kappa$. The source's equation is

\[
 E_m=D_t(qa-gc/q^2)-gm\kappa D_s(p^{m-1}b/q)=0. \tag{S1}
\]

All point coefficients below are unrestricted sufficiently smooth functions
of $(t,s,u)$ on a local open chart. Real powers are smooth because $p>0$.
The coefficient of $r$ is $q>0$, so solve uniquely for $r=R$ and split
the remaining free jets. This is a regular local equation-manifold argument;
it says nothing about $p=0$, $q=0$, global flows or boundary-data
preservation. The exact normal form is in `build_symmetry_report()`.

## Unrestricted determining split

For the unrestricted generator
\[
X=\tau(t,s,u)\partial_t+\xi(t,s,u)\partial_s+
\eta(t,s,u)\partial_u,
\]
let
\(\Omega=\operatorname{pr}^{(3)}X(E_m)|_{r=R}\).
The prolongation is generated recursively from

\[
 \eta_i=D_i\eta-u_jD_i\xi^j,\qquad
 \eta_{Ii}=D_i\eta_I-u_{Ij}D_i\xi^j.
\]

The following coefficient identities were independently expanded by SymPy
from the original (S1), not copied from the printed determining system.
Subscripts on $\tau,\xi,\eta$ here mean ordinary partial derivatives.
Each row is used only **after** the preceding row's consequence.

1. The coefficient of free $y$ is
   \[
   [y]\Omega={g(\kappa mp^mq+p)\over pq^2}(\xi_t+p\xi_u).
   \]
   Its prefactor is strictly positive on the branch. Since $p$ varies
   freely, $\xi_t=\xi_u=0$, so $\xi=\xi(s)$.
2. With that restriction, the coefficient of free $w$ is
   \[
   [w]\Omega={2g(\kappa mp^mq+p)\over pq^2}(\tau_s+q\tau_u).
   \]
   Free $q>0$ gives $\tau_s=\tau_u=0$, hence $\tau=\tau(t)$.
3. The coefficient of $ab$ is $-\eta_s/q$. Thus $\eta_s=0$.
4. The coefficient of $a$ after these restrictions is
   \[
   [a]\Omega=q(4p\eta_{uu}-3\tau_{tt}+4\eta_{tu}).
   \]
   Free $p>0$ gives $\eta_{uu}=0$ and $4\eta_{tu}=3\tau_{tt}$.
   Therefore $\eta=A(t)u+B(t)$ and $4A'=3\tau''$.
5. The coefficient of free $x$ then is
   \[
   [x]\Omega=-{g\over p^2q^2}\left\{
       \kappa mp^mq\big[(m-3)p(A-\tau')+(m-1)(A'u+B')\big]
       +p^2(2\tau'+\xi'-3A)\right\}. \tag{S2}
   \]
   Splitting its distinct $q$-powers gives
   \(2\tau'+\xi'-3A=0\) and
   \((m-3)p(A-\tau')+(m-1)(A'u+B')=0\) for all $p,u$.

No polynomial, affine, or diagonal ansatz was imposed on the initial
coefficient functions. The affine form of $\eta$ is a *deduction* from the
free-jet coefficients. Every division uses $p,q,g,\kappa,m>0$, or the
strictly positive factor $\kappa mp^mq+p$. There is no division by
$m-1$ or $m-3$ before those parameter strata are separated.

For $m\ne1,3$, (S2) yields $A=\tau'$, $A'=B'=0$, and $\xi'=A$.
For $m=3$, it yields $A'=B'=0$, then $\tau''=0$, and
$\xi'=3A-2\tau'$. For $m=1$, it yields $A=\tau'$; combining
$4A'=3\tau''$ with $A'=\tau''$ forces $\tau''=A'=0$, while
$\xi'=A$. Only $B(t)$ remains. After substituting these coefficients,
the **off-shell** expression is
\[
 \operatorname{pr}^{(3)}X(E_1)+2A E_1=bB''(t)+qB'''(t).
\]
Its restriction to $E_1=0$ yields the same condition. Since $b,q$ are free,
$B''=0$. These are all solutions of the necessary
system, and direct off-shell prolongation verifies every resulting basis
generator, so the list is sufficient as well.

Consequently the complete local smooth point algebra on this branch is

| Parameter | Basis | Dimension |
|---|---|---:|
| $m\geq1,\ m\ne1,3$ | $X_1=\partial_t,\ X_2=\partial_s,\ X_3=\partial_u,\ X_4=t\partial_t+s\partial_s+u\partial_u$ | 4 |
| $m=3$ | $X_1,X_2,X_3,X_4,\ X_5=t\partial_t-2s\partial_s$ | 5 |
| $m=1$ | $X_1,X_2,X_3,X_4,\ X_6=t\partial_u$ | 5 |

The extra $m=1$ generator reflects the absence of $p=u_t$ in the
bedload flux $p^{m-1}b/q$ at $m=1$. Directly,
$\operatorname{pr}^{(3)}X_6(E_1)=0$, whereas its general-$m$ residual
is nonzero when $m>1$.

## Direct identities and source discrepancy

Off shell, $\operatorname{pr}^{(3)}X_i(E_m)=0$ for $i=1,2,3$, and
$\operatorname{pr}^{(3)}X_4(E_m)=-2E_m$. If
$E_{\rm bed}=-gm\kappa D_s(p^{m-1}b/q)$, exact weight accounting and
direct prolongation give
\[
 \operatorname{pr}^{(3)}X_5(E_m)+E_m=(3-m)E_{\rm bed}. \tag{S3}
\]
Thus $X_5$ is admitted at $m=3$, not at generic $m$. The PDF p. 4
prints the determining equation
$3\eta_1+\xi^2_s+2\xi^1_t=0$. Its own listed $X_4$ has
$\eta_1=\xi^2_s=\xi^1_t=1$, giving $6=0$. The printed system is
internally inconsistent; it cannot prove Proposition 1. More decisively,
the source's four-or-five count omits the verified $m=1$ fifth
generator. The corrected classification here applies only to (S1) and the
stated positive branch.

## Brackets and adjoints

Use $[A,B]=A(B)-B(A)$ and the paper's convention
\(\operatorname{Ad}(e^{\epsilon A})B=e^{-\epsilon\operatorname{ad}_A}B\).
For $m\ne1,3$, the only nonzero independent brackets are
\([X_i,X_4]=X_i\) for $i=1,2,3$. At $m=3$, additionally
\([X_1,X_5]=X_1\), \([X_2,X_5]=-2X_2\), and
\([X_3,X_5]=[X_4,X_5]=0\). At $m=1$, instead
\([X_1,X_6]=X_3\), \([X_4,X_6]=0\), and
\([X_2,X_6]=[X_3,X_6]=0\). Reversed bracket orders have opposite signs.
The implementation computes every ordered bracket from the coordinate
fields, checks all 125 ordered Jacobi triples in each five-dimensional
stratum, and constructs every elementary adjoint exponential. Source Table 2
agrees with this convention for its listed $m=3$ basis. Source Table 1
gets two reverse-order cells wrong:

| Cell | Printed | Correct |
|---|---:|---:|
| \([X_5,X_1]\) | $+X_1$ | $-X_1$ |
| \([X_5,X_2]\) | $-2X_2$ | $+2X_2$ |

## Connected-adjoint line orbits

Here equivalence means connected inner adjoint transformations, followed by
nonzero real rescaling of a one-dimensional subalgebra generator. This
specified equivalence is narrower than an unspecified full automorphism
group. The following orbit reductions are for **all** lines in the
respective classified finite-dimensional local point algebras.

For the generic four-dimensional algebra, all nontranslation lines reduce
to $X_4$. Adjoint $X_4$ scales all three translations equally, so it
fixes every line in their translation ideal. That ideal's orbit space is
\(\mathbb{RP}^2\), represented in three charts by
\(X_1+aX_2+bX_3\), \(X_2+aX_3\), and \(X_3\). The paper's list omits
the second chart's $a\ne0$ family; for example $X_2+X_3$ cannot be
conjugated to a listed pure translation or one with nonzero $X_1$.

At $m=3$, write $Z=v_1X_1+v_2X_2+v_3X_3+aX_4+bX_5$.
The commuting dilation pair acts diagonally on translations:
\[
 \operatorname{ad}_{aX_4+bX_5}|_V
   =\operatorname{diag}(-(a+b),-(a-2b),-a).
\]
For nonzero $H=aX_4+bX_5$, nonresonant translation components can be
removed. Its projective direction \((a:b)\in\mathbb{RP}^1\) cannot be
changed by inner adjoints. Exactly three directions have one zero weight:
\(X_5+cX_3\), \(X_4-X_5+cX_1\), and
\(X_4+\tfrac12X_5+cX_2\). The survivor $c\ne0$ cannot be translated
away. A complementary dilation normalizes $c$ to $+1$ or $-1$, but
connected adjoints do not flip its sign after the $H$ normalization.
The $c=0$ case is the pure $H$ already included.

For pure translations $v=(v_1,v_2,v_3)$, the exact equivalence test is
\[
 v' =\lambda(e^\epsilon v_1,e^{-2\epsilon}v_2,v_3),
 \qquad \lambda\in\mathbb R\setminus\{0\},\ \epsilon\in\mathbb R.
\]
Support and normalized relative signs are invariant. When $v_3\ne0$,
\(I=v_1^2v_2/v_3^3\) is invariant as well. Disjoint representatives are
\(X_1,X_2,X_3\); \(X_1\pm X_2\); \(X_3\pm X_1\);
\(X_3\pm X_2\); and \(X_3+\sigma X_1+KX_2\), with
\(\sigma\in\{+1,-1\}\), $K\ne0$. In the last family $K=I$.
The explicit equivalence equation, not just this normalized display,
resolves any parameter-boundary question.

At $m=1$, put
\(Z=v_1X_1+v_2X_2+v_3X_3+hX_4+cX_6\).
The elementary connected adjoints act by
\[
\begin{array}{c|l}
X_1&v_1\mapsto v_1-\epsilon h,\quad v_3\mapsto v_3-\epsilon c\\
X_2&v_2\mapsto v_2-\epsilon h\\
X_3&v_3\mapsto v_3-\epsilon h\\
X_4&(v_1,v_2,v_3)\mapsto e^\epsilon(v_1,v_2,v_3)\\
X_6&v_3\mapsto v_3+\epsilon v_1.
\end{array}
\]
Thus $h\ne0$ reduces to $X_4+\alpha X_6$, $\alpha\in\mathbb R$.
When $h=0,c\ne0$, normalize $c=1$, remove $v_3$, and obtain
$X_6$, $X_6+\sigma X_1+aX_2$ ($a\in\mathbb R$), or
$X_6+\sigma X_2$, with $\sigma=\pm1$. Only positive common scaling
of the remaining $(v_1,v_2)$ is available, so these signs persist.
When $h=c=0$, use $X_6$ to remove $v_3$ if $v_1\ne0$, giving
$X_1+aX_2$; if $v_1=0$, retain $X_2+aX_3$ and $X_3$.
These cases are disjoint by the invariant vanishing pattern of $(h,c)$
and the indicated support; the explicit adjoint actions prove coverage.

These orbit statements classify *algebra lines* under the declared
equivalence. They do not imply all associated invariant graphs exist on
the positive chart, satisfy particular data or boundary fluxes, or yield
regular ODE reductions. Those are separate gates.
