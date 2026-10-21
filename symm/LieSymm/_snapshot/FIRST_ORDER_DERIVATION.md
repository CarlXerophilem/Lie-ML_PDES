# Unrestricted local point algebra of the one-dimensional first-order SVE system

This is a new calculation for the **full three-field first-order system**.
No printed or corrected scalar classification is imported. The algebra below
is maximal among smooth local point fields under the stated open-domain
assumptions, by integrating necessary and sufficient determining equations.
It remains subject to independent review in the enclosing project gate.

## 1. Model, domain, and answer

Write \(w=(h,u,B)^T\), \(q(u)=mKu^{m-1}\), and

\[
w_t+A(w)w_x=0,\qquad
A=\begin{pmatrix}u&h&0\\g&u&g\\0&q&0\end{pmatrix}. \tag{1}
\]

The domain is an open connected subset of \((t,x,h,u,B)\)-space with
\(h>0,u>0\), fixed \(g>0,K\geq0\), and fixed real \(1\leq m\leq4\).
The positive-velocity chart makes real powers smooth. The equations are solved
for all three time derivatives, so the three spatial first jets are free in
the infinitesimal criterion. This is a local equation-manifold classification;
it asserts neither well-posedness nor compatibility with any chosen data.

Every admitted smooth point field has the following form, with constants
\(\alpha,\beta,t_0,x_0,d_0\):

\[
\begin{split}
X={}&(\alpha t+t_0)\partial_t+(\beta x+x_0)\partial_x
 -2(\alpha-\beta)h\partial_h-(\alpha-\beta)u\partial_u\\
 &+\{d_0-2(\alpha-\beta)B\}\partial_B, \tag{2}
\end{split}
\]

subject only to

\[
K(m-3)(\alpha-\beta)=0. \tag{3}
\]

Thus:

| Parameter branch | Maximal point algebra dimension | Basis |
|---|---:|---|
| \(K>0,m\ne3\) | 4 | \(T,P,Z,D\) |
| \(K>0,m=3\) | 5 | \(T,P,Z,D,S\) |
| \(K=0\), remove \(m\) | 5 | \(T,P,Z,D,S\) |

Here
\[
T=\partial_t,\quad P=\partial_x,\quad Z=\partial_B,\quad
D=t\partial_t+x\partial_x,\quad
S=t\partial_t-2h\partial_h-u\partial_u-2B\partial_B. \tag{4}
\]
The \(K=0\) equation is exactly \(B_t=0\). It is not the two-field
shallow-water system with a fixed flat bed: \(B\) remains an arbitrary field
coupled through \(B_x\). In particular, its maximal point algebra here is
finite; arbitrary bed relabelings and Galilean boosts fail the original PDE.

## 2. Begin with arbitrary coefficient functions

Do **not** assume projectability, linearity, or affine coefficients. Begin with

\[
X=\tau(t,x,w)\partial_t+\xi(t,x,w)\partial_x+
  \eta^i(t,x,w)\partial_{w^i},\qquad \eta=(H,U,Z)^T. \tag{5}
\]

Let \(p=w_x\), \(J=\partial_w\eta\), and let the row vectors
\(r=\partial_w\tau\), \(s=\partial_w\xi\). Substitution of \(w_t=-Ap\)
in the ordinary first prolongation gives the polynomial identity

\[
0=C+Mp+Q(p), \tag{6}
\]

where
\[
\begin{split}
C&=\eta_t+A\eta_x,\\
M&=AJ-JA+\eta\mathbin{\cdot}\partial_wA
 +(\tau_t-\xi_x)A+\tau_xA^2-\xi_tI,\\
Q(p)&=A^2p(rp)-Ap(rAp)+p(sAp)-Ap(sp). \tag{7}
\end{split}
\]
All displayed partial derivatives hold the other coordinates fixed. Because
\(p\) is free, the constant, linear, and quadratic parts must each vanish.
Conversely, those identities imply the full infinitesimal criterion, so this
split loses no equations. The verifier compares (6) with an independent direct
first-prolongation implementation before any coefficient restriction.

## 3. Projectability is a consequence of the quadratic equations

At a state where \(A\) has three distinct eigenvalues \(\lambda_i\), choose
an eigenbasis just for this pointwise algebraic argument. The coefficient of
\(p_ip_j\), \(j\ne i\), in component \(Q_i\) is

\[
(\lambda_i-\lambda_j)(\lambda_i r_j-s_j)=0. \tag{8}
\]

For each fixed \(j\), the two other, distinct eigenvalues imply
\(r_j=s_j=0\). Hence \(\tau_w=\xi_w=0\).

For \(K>0\), \(q>0\). The positive diagonal matrix
\[
W=\operatorname{diag}(g/h,1,g/q)
\]
makes \(WA\) symmetric. Equivalently, \(W^{1/2}AW^{-1/2}\) is a real
symmetric tridiagonal matrix with nonzero adjacent entries
\(\sqrt{gh}\) and \(\sqrt{gq}\). Such a matrix has simple eigenvalues:
an eigenvector is determined by its first component by the tridiagonal
recurrence, and a zero first component forces every component to vanish;
symmetry then makes each eigenspace one-dimensional and all multiplicities
one. Thus the argument applies at every positive-transport state.

For \(K=0\),
\[
\det(\lambda I-A)=\lambda\{(\lambda-u)^2-gh\},\qquad
\operatorname{disc}=4gh(u^2-gh)^2. \tag{9}
\]
The eigenvalues are distinct away from \(u^2=gh\). That complement is dense
in any open state domain; continuity of the coefficient derivatives extends
\(\tau_w=\xi_w=0\) to the hypersurface. No division by \(u^2-gh\) is
used to discard a branch. A symmetry defined only on that hypersurface would
be a different constrained system, not an open-domain point symmetry here.

Therefore, in **both** branches,
\[
\tau=\tau(t,x),\qquad \xi=\xi(t,x). \tag{10}
\]

## 4. The nine linear-jet equations

Set
\[
a=\tau_t-\xi_x,\quad b=\tau_x,\quad c=\xi_t,\quad q'=dq/du. \tag{11}
\]
The nine entries of \(M=0\) are

\[
\begin{array}{ll}
M_{11}:&-gH_u+U+hU_h+au+bgh+bu^2-c=0,\\
M_{12}:&H-qH_B-hH_h+hU_u+ah+2bhu=0,\\
M_{13}:&uH_B-gH_u+hU_B+bgh=0,\\
M_{21}:&g(H_h-U_u+Z_h+a+2bu)=0,\\
M_{22}:&gH_u+U-qU_B-hU_h+gZ_u+au+bgh+bgq+bu^2-c=0,\\
M_{23}:&gH_B+uU_B-gU_u+gZ_B+ag+bgu=0,\\
M_{31}:&qU_h-uZ_h-gZ_u+bgq=0,\\
M_{32}:&q'U+qU_u-qZ_B-hZ_h-uZ_u+aq+bqu=0,\\
M_{33}:&qU_B-gZ_u+bgq-c=0. \tag{12}
\end{array}
\]

These equations plus \(C=0\) are necessary and sufficient after (10).
We solve them using three traces which remove the commutator \(AJ-JA\).

## 5. Spectral invariants determine \(U,H\) and the exceptional parameters

From \(\operatorname{tr}M=0\),
\[
U=\frac32c-au-b\{u^2+g(h+q)\}. \tag{13}
\]
From \(\operatorname{tr}(AM)=0\), using \(q'=(m-1)q/u\),
\[
\begin{split}
H={}&-2ah+a(m-3)q+\frac{bg(m-1)q(h+q)}u
 -4bhu+b(m-2)qu\\
&-\frac{3c(m-1)q}{2u}-\frac{cu}{g}. \tag{14}
\end{split}
\]
The only denominators in this step are \(u,g\), both strictly positive.
The determinant equation is obtained from \(\operatorname{tr}(\operatorname{adj}(A)M)=0\).
It does not require \(A\) invertible and therefore also applies at \(K=0\).
Since \(\det A=-gqu\), it is
\[
-g(q+uq')U-3agqu-2bgqu^2-c\{u^2-g(h+q)\}=0. \tag{15}
\]
Substitute (13) and split:
\[
\begin{split}
0={}&agqu(m-3)+bgqu^2(m-2)+bg^2mq^2\\
&+cgq(1-3m/2)-cu^2+gh(bgmq+c). \tag{16}
\end{split}
\]

### 5a. \(K>0\), \(m>1\)

The coefficient of the free state variable \(h\) in (16) implies
\(c=-bgmq(u)\). The left coefficients \(b,c\) depend only on \(t,x\).
Differentiate this identity in \(u\):
\[
0=bgm q'(u),\qquad q'=mK(m-1)u^{m-2}>0. \tag{17}
\]
Consequently \(b=c=0\). Equation (16) then becomes
\[
agqu(m-3)=0. \tag{18}
\]
All of \(g,q,u\) are nonzero, leaving exactly \((m-3)a=0\).
There are no other real exceptional exponents in \(1<m\leq4\).

### 5b. \(K>0\), \(m=1\)

Now \(q=K>0\) is constant, so (17) cannot be used. The coefficient of \(h\)
still gives \(c=-bgq\). The remaining equation (16) is
\[
\frac{gq}{2}(-4au+3bgq)=0. \tag{19}
\]
Splitting the free variable \(u\) gives \(a=0\), then \(b=0\), then
\(c=0\). This endpoint is covered explicitly rather than discarded by
division by \(m-1\).

In all positive-transport cases, (13)--(14) thus reduce to
\[
U=-au,\qquad H=-2ah,\qquad b=c=0,\qquad (m-3)a=0. \tag{20}
\]

### 5c. \(K=0\): retain the full \(B_t=0\) equation

Here \(q=0\), and the parameter \(m\) disappears. Equation (15) gives
\(-c(u^2-gh)=0\) identically in free \(h,u\), hence \(c=0\).
Equations (13)--(14) become
\[
U=-au-b(u^2+gh),\qquad H=-2ah-4bhu. \tag{21}
\]
The invariant equations alone do not determine \(b\), so we now use an
actual matrix equation: substitution in \(M_{11}=0\) gives
\[
3ghb=0. \tag{22}
\]
Since \(g,h>0\), \(b=0\). Therefore (20) holds without its last
parameter restriction. This step prevents a spurious nonconstant-time
coefficient from surviving a trace-only calculation.

## 6. Integrate the remaining coefficient equations without an ansatz

For both surviving cases, use \(H=-2ah,U=-au,b=c=0\) in (12).
The entries \(M_{21},M_{31},M_{23}\), in this order, give
\[
gZ_h=0,\qquad -uZ_h-gZ_u=0,\qquad g(Z_B+2a)=0.
\]
Hence
\[
Z=-2a(t,x)B+d(t,x). \tag{23}
\]
All remaining entries vanish once the recorded parameter condition is used.
The constant-jet equations \(C=0\) are now
\[
\begin{split}
-2h a_t-3hu a_x&=0,\\
-u a_t-(2gh+u^2+2gB)a_x+gd_x&=0,\\
-2B a_t-qu a_x+d_t&=0. \tag{24}
\end{split}
\]
Divide the first equation by \(-h\) and split its free \(u\):
\(a_t=a_x=0\). The second and third equations then imply
\(d_x=d_t=0\). Thus \(a,d\) are constants.

Because \(b=c=0\), we already know \(\tau=\tau(t),\xi=\xi(x)\).
The definition \(a=\tau_t-\xi_x\) and its constant value give
\(\tau=\alpha t+t_0\), \(\xi=\beta x+x_0\), with
\(a=\alpha-\beta\). This proves the **necessity** of (2)--(3).

## 7. Sufficiency, completeness, and negative controls

Substitute (2) into the unrestricted first prolongation, without suppressing
any original equation. Its on-shell residual is exactly
\[
\begin{pmatrix}0\\0\\(3-m)(\alpha-\beta)q\,u_x\end{pmatrix}. \tag{25}
\]
It vanishes on precisely the recorded parameter branches. This proves
**sufficiency**. Together with Sections 2--6 it proves unrestricted local
point-algebra completeness on the declared domain, rather than completeness
within a polynomial search space.

Three useful rejected candidates are:

* \(S\) at generic \(K>0,m\ne3\): defect \((3-m)q u_x\) in the bed equation.
* A Galilean boost \(t\partial_x+\partial_u\): defect
  \(q'u_x-B_x\) in the bed equation, including \(-B_x\) at \(K=0\).
* The nonlinear bed relabeling \(B^2\partial_B\) at \(K=0\): defect
  \(2gB B_x\) in the momentum equation.

Thus neither familiar flat-bed shallow-water boosts nor arbitrary functions
of the static bed may be silently appended to this algebra. The verifier
also rejects the nonprojectable trial \(h\partial_t\).

The nonzero basis brackets, with \([X,Y]=XY-YX\), are
\[
[D,T]=-T,\quad[D,P]=-P,\quad[S,T]=-T,\quad[S,Z]=2Z. \tag{26}
\]
Brackets involving \(S\) are present only on the five-dimensional branches.
These give the algebra structure; they do not claim an optimal subalgebra
system, an equivalence-group classification, or data compatibility.

## 8. Reproduction and scope of the receipt

Run from the repository root:

```powershell
python -B build/sve-general-symm-20261020/research_first_order.py
```

The script writes only `first_order_results.json` beside itself. It checks
the unrestricted prolongation decomposition, the eigenbasis quadratic
coefficients, determinant/trace identities, the exceptional endpoint
\(m=1\), the \(K=0\) discriminant and final matrix constraint, the zero-jet
integration identities, all basis generators, and rejected-candidate defects.
The readable integration proof is essential: the finite exact checks support
its identities and do not replace it. No high-cost symbolic solve is used.

This note does not establish full equivalence-group maximality, optimal
subalgebra classification, generalized/contact/nonlocal symmetries,
conditional symmetries, 2D results, arbitrary initial/boundary-data
compatibility, or any machine-learning result. It has no dependence on the
historical scalar package beyond respecting the model-separation boundary.
