# Lie Point Symmetry Reduction of the Scalar Shallow-Water Equation

## An integrated English hand-calculation manuscript leading to Equation (27)

This manuscript integrates the existing worksheet derivation with the fuller supplied exposition. Sections 1–18 retain the original worksheet numbering. Section 0 supplies the physical-coordinate audit; Sections 5.11–5.14 supply the parameter and adjoint calculations; Section 19 supplies the traveling-wave integration. Appendix C is translated into English in full, with its formulas retained. Appendix D lists every coefficient of the unrestricted determining polynomial.

The principal calculation fixes the normalized scalar equation printed as Equation (7) in the source article and the exponent $m=3$. It derives the complete local point-symmetry algebra on the declared chart, selects the $X_5$-invariant graphs, lowers the resulting third-order ODE twice, and reconstructs the scalar field from a first-kind Abel equation.

The last dependent-variable change is essential:

$$
\Sigma=\sigma^{2/3}\mu,\qquad
M=\sigma^{5/3}\frac{d\mu}{d\sigma},\qquad
N=\left(M+\frac23\Sigma\right)^{-1}.
$$

The original invariants give a rational equation for $M(\Sigma)$. The reciprocal shift gives the cubic equation for $N(\Sigma)$ whose coefficients agree with the printed Equation (27).

**Scope.** Section 0 derives the material-coordinate transport term omitted in the supplied physical-model argument. The scalar equation analyzed in the worksheet remains explicit throughout. Its exact reduction is distinct from an equivalence with the conventional Eulerian SVE system. Formal identities, proved local propositions, chart restrictions, numerical checks, and literature repairs are labeled separately.


## 0. Physical provenance, material coordinates, and the equation being reduced

### 0.1 Scope and evidence labels

This section integrates the physical-model discussion supplied with the fuller manuscript. The subsequent Sheets 1–18 retain the scalar equation used in the existing hand-calculation manuscript. A distinction is required: a coordinate transformation of the conventional Eulerian SVE system and a symmetry reduction of the printed scalar Equation (7) are separate mathematical claims.

The following labels specify the status of a statement throughout this manuscript.

| Label | Meaning |
|---|---|
| **Definition** | A declared object or convention. |
| **Proposition** | A mathematical assertion proved under the stated hypotheses. |
| **Exact identity** | An equality of differential expressions obtained algebraically, on the declared domain. |
| **Local chart restriction** | A nonvanishing, sign, rank, or invertibility condition needed for a representation. |
| **Literature repair** | A replacement or additional step justified here; it does not identify an author's unstated intention. |
| **Numerical consistency check** | A finite computational comparison, distinct from an analytic error bound. |

The theoretical conventions follow Olver [1] and Oliveri [2]. In particular, Olver's infinitesimal criterion is used with its rank and local-solvability qualifications; Oliveri's Sections 4.2, 5.4, and 6.3 distinguish prolongation, ODE order reduction, and invariant PDE solutions. The SVE source is [3].

All Lie calculations and profiles below concern classical local solutions. Smooth coefficient functions are used for point generators, and at least three continuous derivatives are required of the scalar field wherever its third-order PDE is evaluated. Additional derivatives or analyticity are stated where used. No weak-solution or shock theorem is asserted.

### 0.2 Eulerian variables and the Grass transport law

**Definition.** Let $h^E(t,x)>0$ be water depth, $u^E(t,x)$ horizontal velocity, and $B^E(t,x)$ bed elevation. The superscript $E$ records that time differentiation holds the Eulerian position $x$ fixed. The conventional one-dimensional SVE equations are

$$
\begin{aligned}
\partial_t h^E+\partial_x(h^Eu^E)&=0,\\
\partial_t(h^Eu^E)+\partial_x\left(h^E(u^E)^2+\tfrac12g(h^E)^2\right)
+gh^E\partial_x B^E&=0,\\
\partial_t B^E+\chi\,\partial_x Q_b^E&=0.
\end{aligned}
\tag{0.1}
$$

Here $g>0$, the bed porosity is $\vartheta\in[0,1)$, and $\chi=(1-\vartheta)^{-1}$. The symbol $\chi$ avoids collision with the material-coordinate component $\xi$ of a symmetry generator; $Q_b$ avoids collision with the invariant-surface characteristic $Q$.

For the positive-velocity branch, prescribe the Grass law

$$
Q_b^E=A_g(u^E)^m,\qquad A_g>0,\quad m\geq1,\quad u^E>0.
$$

Its spatial derivative is

$$
\partial_xQ_b^E=mA_g(u^E)^{m-1}\partial_xu^E.
$$

Define

$$
\kappa=A_g\chi,\qquad \beta=m\kappa=mA_g\chi>0.
$$

The Eulerian Exner equation is therefore

$$
\partial_t B^E+\beta(u^E)^{m-1}\partial_xu^E=0.
\tag{0.2}
$$

The positivity assumption makes the real power smooth. At $m=3$ the power itself permits a wider velocity domain, but the positive branch will be retained for the worked reduction.

### 0.3 Construction of a material label and its inverse map

**Motivation.** A material coordinate should remain fixed on a moving water particle. The continuity equation supplies precisely the compatibility needed to define such a label.

Consider the one-form

$$
ds=h^E\,dx-h^Eu^E\,dt.
\tag{0.3}
$$

The condition for a local potential $s(t,x)$ is

$$
\partial_t h^E=\partial_x(-h^Eu^E),
$$

which is exactly the first equation of (0.1). On a sufficiently small simply connected neighborhood, define $s$ by

$$
s_x=h^E,\qquad s_t=-h^Eu^E.
$$

The Jacobian of $(t,x)\mapsto(t,s)$ is

$$
\det\frac{\partial(t,s)}{\partial(t,x)}=s_x=h^E>0.
$$

**Local chart restriction.** The inverse-function theorem gives a local inverse $x=\phi(t,s)$. This claim is local and does not assert global injectivity through dry states or singularities.

Differentiate $s(t,\phi(t,s))=s$ first with respect to $s$ and then with respect to $t$:

$$
s_x\phi_s=1,\qquad s_t+s_x\phi_t=0.
$$

Using the defining derivatives of $s$ gives

$$
\phi_s=\frac1{h^E(t,\phi(t,s))},\qquad
\phi_t=u^E(t,\phi(t,s)).
\tag{0.4}
$$

For any Eulerian field $f^E$, define its material pullback by

$$
f^L(t,s)=f^E(t,\phi(t,s)).
$$

The chain rule gives, with $v=\phi_t$ and $\rho=\phi_s$,

$$
\begin{aligned}
\partial_t f^L&=(\partial_t f^E)\circ\phi+v(\partial_xf^E)\circ\phi,\\
\partial_sf^L&=\rho(\partial_xf^E)\circ\phi.
\end{aligned}
$$

Consequently the operators at fixed Eulerian and fixed material positions are related by

$$
\boxed{
(\partial_xf^E)\circ\phi=\rho^{-1}D_sf^L,\qquad
(\partial_tf^E)\circ\phi=D_tf^L-\frac v\rho D_sf^L.
}
\tag{0.5}
$$

Here $\circ\phi$ abbreviates evaluation at $(t,\phi(t,s))$. A time derivative of a bed elevation pulled back by a moving coordinate system is thus a material derivative; it is not the original Eulerian partial derivative.

### 0.4 Verification of continuity and transformation of momentum

Set $h^L=\rho^{-1}$ and $u^L=v$. For $\ell=\phi_{ts}$ and $c=\phi_{ss}$, (0.5) gives

$$
\begin{aligned}
(\partial_th^E)\circ\phi
&=D_t(\rho^{-1})-\frac v\rho D_s(\rho^{-1})
=-\frac\ell{\rho^2}+\frac{vc}{\rho^3},\\
(\partial_x(h^Eu^E))\circ\phi
&=\frac1\rho D_s\left(\frac v\rho\right)
=\frac\ell{\rho^2}-\frac{vc}{\rho^3}.
\end{aligned}
$$

Their sum is zero. Thus the material representation satisfies continuity identically.

The momentum terms obey the identity

$$
\begin{aligned}
\partial_t(hu)+\partial_x(hu^2)
&=u h_t+h u_t+u^2h_x+2huu_x\\
&=u\big[h_t+(hu)_x\big]+h(u_t+uu_x).
\end{aligned}
$$

After continuity is used and the equation is divided by $h>0$, momentum becomes

$$
u_t+uu_x+gh_x+gB_x=0.
$$

Equation (0.5) now yields

$$
u_t+uu_x\longmapsto\phi_{tt},\qquad
h_x\longmapsto-\frac{\phi_{ss}}{\phi_s^3},\qquad
B_x\longmapsto\frac{B_s^L}{\phi_s}.
$$

Therefore

$$
\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^3}
+\frac g{\phi_s}B_s^L=0.
\tag{0.6}
$$

### 0.5 The material Exner transport term and the scope of Equation (7)

Transform (0.2) using (0.5):

$$
\boxed{
B_t^L-\frac{\phi_t}{\phi_s}B_s^L
+\beta\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}=0.
}
\tag{0.7}
$$

The fuller supplied text and the printed Equation (6) instead use

$$
B_t^L+\beta\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}=0.
\tag{0.8}
$$

**Literature repair.** Under the standard pullback $B^L(t,s)=B^E(t,\phi(t,s))$, (0.8) omits $-(\phi_t/\phi_s)B_s^L$. The discrepancy follows directly from the chain rule. It cannot be removed merely by calling both derivatives $B_t$. An alternative definition of the bed variable would need an explicit derivation before (0.8) could be identified with the conventional material form.

To display the effect, define

$$
H=\phi_s\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^2},\qquad
J=\beta\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}.
$$

Multiplication of (0.6) by $\phi_s$ gives $B_s^L=-H/g$. The conventional material Exner equation (0.7) then gives

$$
B_t^L=\frac v\rho B_s^L-J=-\frac{vH}{g\rho}-J.
$$

Equality of the mixed derivatives requires

$$
-\frac1gD_tH=-\frac1gD_s\left(\frac{vH}\rho\right)-D_sJ.
$$

Hence its scalar compatibility equation is

$$
\boxed{
\Delta_m^{\mathrm{phys}}
=D_tH-D_s\left(\frac{\phi_tH}{\phi_s}\right)-gD_sJ=0.
}
\tag{0.9}
$$

By contrast, the formal coupled system (0.6), (0.8) has $B_s^L=-H/g$, $B_t^L=-J$, and compatibility

$$
-\frac1gD_tH=-D_sJ
\quad\Longleftrightarrow\quad
\boxed{\Delta_m=D_tH-gD_sJ=0.}
\tag{0.10}
$$

This is the printed scalar Equation (7), which is the equation reduced in Sheets 1–18. Thus

$$
\Delta_m^{\mathrm{phys}}
=\Delta_m-D_s\left(\frac{\phi_tH}{\phi_s}\right).
$$

The Abel calculation below is an exact analysis of (0.10). It does not establish the missing physical equivalence, and its profiles cannot be declared solutions of (0.1) without separately checking (0.9).

### 0.6 Local reconstruction of the formal bed field

For completeness, a solution of (0.10) reconstructs a bed field for the formal pair (0.6), (0.8). The one-form

$$
\omega=-J\,dt-\frac Hg\,ds
$$

is closed because

$$
\partial_t\left(-\frac Hg\right)-\partial_s(-J)
=-\frac1g\Delta_m=0.
$$

On a local simply connected rectangle, fix $(t_0,s_0)$ and a constant $B_0$. Then

$$
B^L(t,s)=B_0-\int_{t_0}^{t}J(r,s_0)\,dr
-\frac1g\int_{s_0}^{s}H(t,q)\,dq.
\tag{0.11}
$$

Differentiate:

$$
\begin{aligned}
B_s^L&=-H(t,s)/g,\\
B_t^L&=-J(t,s_0)-\frac1g\int_{s_0}^{s}D_tH(t,q)\,dq\\
&=-J(t,s_0)-\int_{s_0}^{s}D_sJ(t,q)\,dq=-J(t,s).
\end{aligned}
$$

The reconstruction is unique up to the additive constant $B_0$ on a connected patch. It supplies exactly the formal pair used to derive (0.10).

### 0.7 Normalization and notation

The algebraic terms $b-1$ below use the normalized numerical coefficients of the supplied scalar equation. From Section 1 onward, $t,s,\phi,g,\beta$ denote these normalized variables and parameters, and $b=g\beta$. A physical nondimensionalization must be specified separately before numerical values are assigned physical units. Changing the flux exponent while treating dimensional transport constants as unchanged would also require a scale convention.

The core argument fixes $m=3$. The general-$m$ weight identity and the affine scaling calculation are stated separately; they are not an unrestricted classification at every exponent.

---

## 1. Reduction route and the four operations performed with a generator

A symmetry is a transformation that takes solutions of an equation to solutions of the same equation. An *infinitesimal generator* records the first-order motion produced by a continuous family of such transformations.

The four operations have distinct mathematical objectives and outputs.

| Stage | Objective | Operation | Result |
|---|---|---|---|
| Find the PDE symmetries | Identify transformations preserving the equation. | Start with unknown $\tau,\xi,\eta$; prolong the vector field; solve determining equations. | Five generators $X_1,\ldots,X_5$ when $m=3$. |
| Check the scaling | Determine the exponent restriction for $X_5$. | Compute the scaling weights of derivatives and PDE terms. | $\operatorname{pr}^{(3)}X_5(\Delta_3)=-\Delta_3$. |
| Select similarity solutions | Characterize graphs fixed by the scaling. | Find invariants and impose the invariant-surface condition $Q=0$. | $\phi(t,s)=F(st^2)$ and a third-order ODE. |
| Lower the ODE's order | Describe the quotient of the ODE solution family. | Use differential invariants and retain reconstruction constants. | A second-order equation, then a first-order equation. |

The calculation has the following sequence:

$$
\begin{aligned}
\Delta_3[\phi]=0
&\quad\xrightarrow{\ \phi=F(\sigma),\ \sigma=st^2\ }\quad
\text{third-order ODE for }F,\\
&\quad\xrightarrow{\ \mu=F'\ }\quad
\text{second-order ODE for }\mu,\\
&\quad\xrightarrow{\ \Sigma=\sigma^{2/3}\mu,\ M=\sigma^{5/3}\mu'\ }\quad
\text{first-order rational ODE for }M(\Sigma),\\
&\quad\xrightarrow{\ N=(M+\frac23\Sigma)^{-1}\ }\quad
\text{first-order cubic Abel ODE for }N(\Sigma).
\end{aligned}
$$

The first arrow reduces the number of independent variables, from $(t,s)$ to $\sigma$. It does **not** lower the differential order from three. The next two arrows lower the ODE's order.

**Reading guide.** Sections 2–5 construct the symmetry algebra. Sections 6–9 explain the similarity reduction. Sections 10–13 derive Equation (27). Sections 14–16 reconstruct solutions, recover excluded branches, and work through concrete data.

**The two algebraic tasks.**

| Task | Location and result |
|---|---|
| Definition and use of a subalgebra | Sections 5.6–5.10 define the bracket, test closure, select reduction families, and explain which symmetries survive a reduction. |
| Derivation of $X_1,\ldots,X_5$ | Sections 4–5 derive the determining equations, solve for the general generator, count its five free constants, and extract a basis. |

The full symmetry algebra describes the infinitesimal transformations admitted by the PDE. A chosen subalgebra specifies the transformations used in a particular reduction.

**Geometric companion: Appendix C.** Its English exposition follows Sheets 6–13, with definitions of flows, weights, invariant graphs, pushforward, both ODE reductions, and reconstruction. C.12 distinguishes commutativity from projectability; C.9 distinguishes general order reduction from additional invariant-solution constraints.

## 2. Scalar equation, notation, and domain

### 2.1 The scalar model we will transform

The starting point is the scalar equation printed as Equation (7) in the source paper:

$$
\boxed{
\Delta_m[\phi]
=D_t\left(\phi_s\phi_{tt}
-g\frac{\phi_{ss}}{\phi_s^2}\right)
-g\beta D_s\left(
\phi_t^{\,m-1}\frac{\phi_{ts}}{\phi_s}
\right)=0.
}
\tag{P}
$$

Here $t$ is time, $s$ is a material label, and $\phi=\phi(t,s)$ is the unknown scalar field. A subscript means differentiation: for example,

$$
\phi_{ts}=\frac{\partial^2\phi}{\partial t\,\partial s}.
$$

There are two independent variables, so this is a $(1+1)$-dimensional PDE. Its highest derivatives have total order three.

We use the paper's convention $\beta=m\kappa$. The reduction studied here is

$$
m=3,\qquad g>0,\qquad \beta>0,\qquad b:=g\beta.
$$

The letter $b$ is only an abbreviation; it is not a new independent parameter.

We work locally on the positive chart

$$
t>0,\qquad s>0,\qquad \phi_s>0,\qquad \phi_t>0.
\tag{D}
$$

These assumptions justify the divisions and fractional powers used below. At $m=3$ the polynomial velocity powers do not themselves require $\phi_t>0$, but retaining this chart keeps the whole reduction consistent with the manuscript.

The object proved and reduced here is the scalar equation (P). Section 0 derives its formal bed-field compatibility and identifies the additional transport term required for the conventional material pullback of the Eulerian SVE system.

### 2.2 Expand the divergence before doing symmetry calculations

Use the product and quotient rules:

$$
D_t(\phi_s\phi_{tt})
=\phi_{ts}\phi_{tt}+\phi_s\phi_{ttt},
$$

$$
D_t\left(\frac{\phi_{ss}}{\phi_s^2}\right)
=\frac{\phi_{tss}}{\phi_s^2}
-2\frac{\phi_{ss}\phi_{ts}}{\phi_s^3},
$$

and

$$
\begin{aligned}
D_s\left(\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}\right)
={}&(m-1)\phi_t^{m-2}\frac{\phi_{ts}^2}{\phi_s}\\
&+\phi_t^{m-1}\frac{\phi_{tss}}{\phi_s}
-\phi_t^{m-1}\frac{\phi_{ts}\phi_{ss}}{\phi_s^2}.
\end{aligned}
$$

Therefore

$$
\begin{aligned}
\Delta_m={}&\phi_s\phi_{ttt}+\phi_{ts}\phi_{tt}\\
&-g\left(\phi_s^{-2}+\beta\phi_t^{m-1}\phi_s^{-1}\right)\phi_{tss}\\
&+g\left(2\phi_s^{-3}+\beta\phi_t^{m-1}\phi_s^{-2}\right)\phi_{ts}\phi_{ss}\\
&-g\beta(m-1)\phi_t^{m-2}\phi_s^{-1}\phi_{ts}^{\,2}.
\end{aligned}
\tag{2.1}
$$

This expansion is useful for finding symmetries. The original divergence form will be useful again when substituting the similarity ansatz.

### 2.3 Jet coordinates: names for derivative values at one point

A *jet* records a function's value and a finite list of derivative values at a point. During the determining calculation, these derivative values are treated as coordinates.

To shorten the algebra, write

| Derivative order | Names |
|---|---|
| First | $v=\phi_t,\quad \rho=\phi_s$ |
| Second | $a=\phi_{tt},\quad \ell=\phi_{ts},\quad c=\phi_{ss}$ |
| Third | $T=\phi_{ttt},\quad U=\phi_{tts},\quad R=\phi_{tss},\quad V=\phi_{sss}$ |

The symbols $T$ and $R$ here are jet coordinates, not differential operators. At $m=3$, Equation (2.1) becomes

$$
\boxed{
\Delta_3
=\rho T+\ell a
-g(\rho^{-2}+\beta v^2\rho^{-1})R
+g(2\rho^{-3}+\beta v^2\rho^{-2})\ell c
-2g\beta v\rho^{-1}\ell^2.
}
\tag{2.2}
$$

Since $\rho>0$, solve this equation for $T$:

$$
\boxed{
\begin{aligned}
T=T_*:={}&-\frac{\ell a}{\rho}
+g(\rho^{-3}+\beta v^2\rho^{-2})R\\
&-g(2\rho^{-4}+\beta v^2\rho^{-3})\ell c
+2g\beta v\rho^{-2}\ell^2.
\end{aligned}
}
\tag{2.3}
$$

On the equation $\Delta_3=0$, the coordinate $T$ is thus determined by the others. The remaining jet coordinates can vary freely in an open local chart. This fact is what later allows us to set polynomial coefficients to zero.

## 3. Point generators and the infinitesimal symmetry criterion

### 3.0 Bundle, jet manifold, local group, and graph transversality

**Definition.** Let $\Omega\subset\{(t,s):t>0,\ s>0\}$ be open. The scalar bundle is

$$
\pi:E=\Omega\times\mathbb R\longrightarrow\Omega,\qquad
\pi(t,s,\phi)=(t,s).
$$

The point manifold $\mathcal M$ is the total space $E$. A section is a graph $(t,s)\mapsto(t,s,f(t,s))$. The third jet $j^3f$ records its derivatives through order three, and the jet manifold $J^3\pi$ has coordinates

$$
(t,s,\phi,v,\rho,a,\ell,c,T,U,R,V).
$$

Its dimension is $2+1+2+3+4=12$. The equation hypersurface is

$$
\mathcal E_3=\{j\in J^3\pi:\Delta_3(j)=0,\ \rho>0,\ v>0\}.
$$

Since $\partial\Delta_3/\partial T=\rho>0$, this is a regular hypersurface of dimension $11$. Eliminating $T$ leaves the three point coordinates and eight free derivative coordinates. The equation hypersurface consists of admissible jets; it is distinct from the two-dimensional graph of an individual solution.

Let $G$ be an $r_G$-dimensional Lie group with identity $e$, acting smoothly and locally on $\mathcal M$ through $\Phi$. The action satisfies

$$
\Phi(e,q)=q,\qquad \Phi(g,\Phi(h,q))=\Phi(gh,q)
$$

where defined. The Lie algebra $T_eG$ and the tangent space $T_q\mathcal M$ are different spaces. Differentiating the action in a Lie-algebra direction produces a vector field on $\mathcal M$; it does not identify $\mathcal M$ with $G$.

The group dimension $r_G$ is independent of the number of independent variables and the differential order. The five-dimensional algebra found below acts on a three-dimensional point manifold.

For an element $A\in T_eG$, the associated one-parameter subgroup induces a local flow $\Gamma_\epsilon$ with generator $X$. Near $\epsilon=0$ its graph action is defined only where the transformed independent variables remain coordinates on the transformed graph. In formulas this requires

$$
\det
\begin{pmatrix}
D_t\bar t&D_s\bar t\\
D_t\bar s&D_s\bar s
\end{pmatrix}\ne0.
\tag{3.0}
$$

At the identity this determinant is $1$, so it remains nonzero locally for sufficiently small flow parameter. The chart restrictions $t,s,\rho,v>0$ must also be retained on the neighborhood used.

**Infinitesimal criterion and scope.** In this manuscript, a point symmetry preserves the equation hypersurface after the chain-rule prolongation and hence maps admissible local solution graphs to solution graphs. For a maximal-rank equation, tangency gives this preservation. If symmetry is initially defined only by its action on actual solutions, necessity of the full jet criterion also requires local solvability; regularity alone is not that extra hypothesis [1, Theorem 2.31 and Section 2.6].

Here the equation is analytic on $\rho,v>0$ and solved for $\phi_{ttt}$. Analytic Cauchy data $\phi,\phi_t,\phi_{tt}$ on $t=t_0$ can prescribe all the free derivatives in the displayed third jet. The noncharacteristic analytic Cauchy theorem therefore realizes these equation jets locally. This justifies splitting over the free jet chart for the equation under study; it is not an existence theorem for arbitrary smooth Cauchy data or for global PDE solutions.


### 3.1 A generator describes infinitesimal motion of points

Start with a local transformation depending on a small parameter $\epsilon$:

$$
\begin{aligned}
\bar t&=t+\epsilon\tau(t,s,\phi)+O(\epsilon^2),\\
\bar s&=s+\epsilon\xi(t,s,\phi)+O(\epsilon^2),\\
\bar\phi&=\phi+\epsilon\eta(t,s,\phi)+O(\epsilon^2).
\end{aligned}
$$

Its generator is

$$
X=\tau(t,s,\phi)\partial_t
+\xi(t,s,\phi)\partial_s
+\eta(t,s,\phi)\partial_\phi.
\tag{3.1}
$$

For a point function $h(t,s,\phi)$, this means

$$
X(h)=\tau h_{,t}+\xi h_{,s}+\eta h_{,\phi}.
$$

For example, $X(t)=\tau$ and $X(\phi)=\eta$ when $\phi$ is a coordinate in point space.

The group parameter $\epsilon$ is not time $t$. A one-parameter flow is one direction of transformation; it does not mean that the PDE is first order.

### 3.2 Chain-rule action on derivative coordinates

Equation (P) contains derivatives. Moving $(t,s,\phi)$ also changes $\phi_t,\phi_s,\ldots$. Those changes are determined by the chain rule; they are not additional arbitrary choices.

The vector field extended to these derivative coordinates is the *prolongation*, denoted $\operatorname{pr}^{(3)}X$ through third order.

A simple example is a time scaling:

$$
\bar t=e^\epsilon t,\qquad \bar s=s,\qquad \bar\phi=\phi.
$$

Then

$$
\bar\phi_{\bar t}=e^{-\epsilon}\phi_t.
$$

Its infinitesimal change is $-\phi_t$, although the point-coordinate change of $\phi$ is zero. That derivative change is part of the prolonged vector field.

### 3.3 The equation must be preserved on its zero set

The infinitesimal symmetry criterion is

$$
\boxed{
\left.\operatorname{pr}^{(3)}X(\Delta_3)\right|_{\Delta_3=0}=0.
}
\tag{3.2}
$$

Geometrically, this says that the prolonged motion is tangent to the set of jets satisfying the PDE.

It does not require $\operatorname{pr}^{(3)}X(\Delta_3)$ to vanish at every jet. For example, if

$$
\operatorname{pr}^{(3)}X(\Delta_3)=-\Delta_3,
$$

the criterion holds: the right-hand side is zero wherever $\Delta_3=0$.

We implement the restriction in (3.2) by replacing $T$ with $T_*$ from (2.3). We have **not** imposed an invariant-surface condition on a particular solution.

The general foundation is Olver's Section 2.3, Theorem 2.31. Here $\partial\Delta_3/\partial T=\rho>0$ ensures that the PDE defines a regular hypersurface in jet space, as required for the tangency test.

## 4. Explicit construction of the third prolongation

### 4.1 Ordinary partial derivatives and prolonged coefficients are different

We use a comma for an ordinary point partial derivative, such as $\eta_{,t}=\partial\eta/\partial t$.

We use square brackets for a prolonged coefficient, such as $\eta^{[t]}$, the coefficient of $\partial_{\phi_t}$ in $\operatorname{pr}X$.

Thus

$$
\eta_{,t}\quad\text{and}\quad\eta^{[t]}
$$

are different objects. The notation distinguishes the two operations throughout the calculation.

### 4.2 Total derivatives differentiate through all dependencies

For a point function $h(t,s,\phi)$ evaluated along a graph $\phi(t,s)$,

$$
D_t h=h_{,t}+\phi_t h_{,\phi}.
$$

For a jet function $h(t,s,\phi,v,\rho)$, more terms appear:

$$
D_t h=h_{,t}+v h_{,\phi}+a h_{,v}+\ell h_{,\rho}.
$$

Through the derivative levels needed here,

$$
\begin{aligned}
D_t&=\partial_t+v\partial_\phi+a\partial_v+\ell\partial_\rho
+T\partial_a+U\partial_\ell+R\partial_c+\cdots,\\
D_s&=\partial_s+\rho\partial_\phi+\ell\partial_v+c\partial_\rho
+U\partial_a+R\partial_\ell+V\partial_c+\cdots.
\end{aligned}
\tag{4.1}
$$

The dots indicate higher jet coordinates only when the differentiated expression requires them. We do not need fourth-order jets to prolong a point field to third order.

### 4.3 The recurrence

Let $J$ be a string of derivative indices and start with $\eta^{[\varnothing]}=\eta$. Then

$$
\boxed{
\eta^{[Ji]}
=D_i\eta^{[J]}
-\phi_{Jt}D_i\tau
-\phi_{Js}D_i\xi,
\qquad i=t,s.
}
\tag{4.2}
$$

The subtraction terms account for changes in the independent variables.

For example,

$$
\eta^{[t]}=D_t\eta-vD_t\tau-\rho D_t\xi.
$$

Substitute $D_t\eta=\eta_{,t}+v\eta_{,\phi}$ and expand:

$$
\boxed{
\eta^{[t]}
=\eta_{,t}+(\eta_{,\phi}-\tau_{,t})v-\xi_{,t}\rho
-\tau_{,\phi}v^2-\xi_{,\phi}v\rho.
}
\tag{4.3}
$$

Similarly,

$$
\boxed{
\eta^{[s]}
=\eta_{,s}-\tau_{,s}v+(\eta_{,\phi}-\xi_{,s})\rho
-\tau_{,\phi}v\rho-\xi_{,\phi}\rho^2.
}
\tag{4.4}
$$

At second order, for example,

$$
\eta^{[tt]}=D_t\eta^{[t]}-aD_t\tau-\ell D_t\xi.
$$

To see the product rule at work, one piece is

$$
D_t(-\tau_{,\phi}v^2)
=-(\tau_{,t\phi}+v\tau_{,\phi\phi})v^2
-2\tau_{,\phi}va.
$$

Appendix A gives all three second-order coefficients and their complete remainders. It also gives the third-order coefficients needed below. Each follows by repeating (4.2).

The prolonged vector field acts on the PDE as

$$
\begin{aligned}
\operatorname{pr}^{(3)}X(\Delta_3)
={}&\eta^{[t]}\Delta_{3,v}
+\eta^{[s]}\Delta_{3,\rho}
+\eta^{[tt]}\Delta_{3,a}
+\eta^{[ts]}\Delta_{3,\ell}\\
&+\eta^{[ss]}\Delta_{3,c}
+\eta^{[ttt]}\Delta_{3,T}
+\eta^{[tss]}\Delta_{3,R}.
\end{aligned}
\tag{4.5}
$$

There are no explicit $t,s,\phi$ terms in (2.2), and the PDE does not depend on $U$ or $V$. However, the prolonged coefficients in (4.5) can contain $U$ and $V$, which is why those free jet coordinates still matter.

Here $\Delta_{3,v}$ means $\partial\Delta_3/\partial v$, holding the other jet coordinates fixed. A mixed derivative such as $\phi_{ts}=\phi_{st}$ is one coordinate and is counted once.

### 4.4 Full third prolongation and the seven coefficient derivatives

To fix every component of the operator used in the determining calculation, write

$$
\begin{aligned}
\operatorname{pr}^{(3)}X={}&
\tau\partial_t+\xi\partial_s+\eta\partial_\phi\\
&+\eta^{[t]}\partial_v+\eta^{[s]}\partial_\rho\\
&+\eta^{[tt]}\partial_a+\eta^{[ts]}\partial_\ell+\eta^{[ss]}\partial_c\\
&+\eta^{[ttt]}\partial_T+\eta^{[tts]}\partial_U
+\eta^{[tss]}\partial_R+\eta^{[sss]}\partial_V.
\end{aligned}
$$

The point derivative $\eta_{,t}$ is not the prolongation coefficient $\eta^{[t]}$. All second-order coefficients and the complete lower-jet terms of the two third-order coefficients entering the PDE are expanded in Appendix A. The remaining two coefficients are also given there for completeness; they multiply $\Delta_{3,U}=\Delta_{3,V}=0$ in this particular calculation.

The seven nonzero coordinate derivatives of the residual are, without suppressed factors,

$$
\begin{aligned}
\Delta_{3,v}
&=-2g\beta v\rho^{-1}R
+2g\beta v\rho^{-2}\ell c
-2g\beta\rho^{-1}\ell^2,\\
\Delta_{3,\rho}
&=T+g(2\rho^{-3}+\beta v^2\rho^{-2})R\\
&\quad-g(6\rho^{-4}+2\beta v^2\rho^{-3})\ell c
+2g\beta v\rho^{-2}\ell^2,\\
\Delta_{3,a}&=\ell,\\
\Delta_{3,\ell}
&=a+g(2\rho^{-3}+\beta v^2\rho^{-2})c
-4g\beta v\rho^{-1}\ell,\\
\Delta_{3,c}&=g(2\rho^{-3}+\beta v^2\rho^{-2})\ell,\\
\Delta_{3,T}&=\rho,\\
\Delta_{3,R}&=-g(\rho^{-2}+\beta v^2\rho^{-1}).
\end{aligned}
\tag{4.6}
$$

Substituting these seven derivatives and Appendix A into (4.5), replacing $T$ by $T_*$, and multiplying by $\rho^4$ gives the entire determining polynomial in Appendix D. Its full coefficient table makes every coefficient collection in Section 5 explicit.


## 5. Complete local point-symmetry calculation at $m=3$

### 5.1 Turn the tangency condition into coefficient equations

Set

$$
\mathscr P
:=
\rho^4
\left.
\operatorname{pr}^{(3)}X(\Delta_3)
\right|_{T=T_*}.
\tag{5.1}
$$

Multiplication by $\rho^4$ is legitimate because $\rho>0$. It clears the denominators without changing the zero condition.

After expansion, $\mathscr P$ is a polynomial in

$$
(v,\rho,a,\ell,c,U,R,V)
$$

whose coefficients depend on $(t,s,\phi)$ and derivatives of $\tau,\xi,\eta$. The unrestricted expansion has 118 nonzero monomial coefficients.

The unknowns in this calculation are $\tau,\xi,\eta$. We are finding transformations of the equation, rather than solving for $\phi$. Although the original PDE is nonlinear, its determining equations are homogeneous linear equations in these three coefficient functions and their derivatives.

Coefficient separation follows because a polynomial that vanishes for every choice of its variables in an open set is the zero polynomial. We are testing the equation for all admissible jets, rather than testing one selected solution.

### 5.2 Six coefficients separate the variable dependencies

The following coefficients are enough to begin:

| Monomial in $\mathscr P$ | Its coefficient | Consequence |
|---|---|---|
| $v^3\rho^3V$ | $\beta g\,\xi_{,\phi}$ | $\xi_{,\phi}=0$ |
| $v^2\rho^3V$ | $\beta g\,\xi_{,t}$ | $\xi_{,t}=0$ |
| $v^3\rho^3R$ | $-2\beta g\,\tau_{,\phi}$ | $\tau_{,\phi}=0$ |
| $v^3\rho^2R$ | $-2\beta g\,\tau_{,s}$ | $\tau_{,s}=0$ |
| $v^2\rho^2R$ | $2\beta g\,\eta_{,s}$ | $\eta_{,s}=0$ |
| $v\rho^3R$ | $-2\beta g\,\eta_{,t}$ | $\eta_{,t}=0$ |

We can divide by $\beta g$ because it is positive.

The first two rows follow from the following explicit coefficient calculation. The only source of $V$ in (4.5) is

$$
-g(\rho^{-2}+\beta v^2\rho^{-1})\eta^{[tss]}.
$$

The $V$ term of $\eta^{[tss]}$ is $-(\xi_{,t}+\xi_{,\phi}v)V$. Thus

$$
\left.\mathscr P\right|_{\text{terms containing }V}
=g(\rho^2+\beta v^2\rho^3)
(\xi_{,t}+\xi_{,\phi}v)V.
$$

Expand the product and read the coefficients of $v^3\rho^3V$ and $v^2\rho^3V$.

For the remaining four rows, first use $\xi=\xi(s)$. The part proportional to $\beta gR$, with no second-order jets, simplifies to

$$
\beta gR\left(
-2\tau_{,\phi}v^3\rho^3
-2\tau_{,s}v^3\rho^2
+2\eta_{,s}v^2\rho^2
-2\eta_{,t}v\rho^3
\right).
\tag{5.2}
$$

For example, the four contributions to the coefficient of $\beta g\tau_{,\phi}v^3\rho^3R$ add as

$$
2-2-4+2=-2.
$$

They come, respectively, from the $\eta^{[t]}$, $\eta^{[s]}$, $\eta^{[ttt]}$, and $\eta^{[tss]}$ terms in (4.5), after eliminating $T$.

Consequently,

$$
\tau=T_0(t),\qquad \xi=Z_0(s),\qquad \eta=H_0(\phi).
\tag{5.3}
$$

This dependence was **deduced**. We did not assume an affine or scaling form at the start.

### 5.3 The separated prolongation is much simpler

In this subsection, primes on $T_0,Z_0,H_0$ mean differentiation with respect to their own arguments $t,s,\phi$, respectively.

The first- and second-order coefficients become

$$
\begin{aligned}
\eta^{[t]}&=(H_0'-T_0')v,\\
\eta^{[s]}&=(H_0'-Z_0')\rho,\\
\eta^{[tt]}&=(H_0'-2T_0')a+H_0''v^2-T_0''v,\\
\eta^{[ts]}&=(H_0'-T_0'-Z_0')\ell+H_0''v\rho,\\
\eta^{[ss]}&=(H_0'-2Z_0')c+H_0''\rho^2-Z_0''\rho.
\end{aligned}
\tag{5.4}
$$

For the needed third-order coefficients, the complete formulas are

$$
\boxed{
\begin{aligned}
\eta^{[ttt]}={}&(H_0'-3T_0')T
+3H_0''va-3T_0''a
+H_0'''v^3-T_0'''v,\\
\eta^{[tss]}={}&(H_0'-T_0'-2Z_0')R
+2H_0''\rho\ell+H_0''vc
+H_0'''v\rho^2-Z_0''\ell.
\end{aligned}
}
\tag{5.5}
$$

For example, differentiating $(H_0'-2T_0')a$ in $\eta^{[tt]}$ produces $(H_0''v-2T_0'')a$, and differentiating $-T_0''v$ produces another $-T_0''a$. Together these give the term $-3T_0''a$. It must be retained.

Likewise, differentiating $H_0''v\rho$ with $D_s$ gives

$$
D_s(H_0''v\rho)
=H_0'''v\rho^2+H_0''\ell\rho+H_0''vc.
$$

Combining this with the derivative of the coefficient of $\ell$ produces $2H_0''\rho\ell$. It does not produce a term $H_0''\rho a$.

### 5.4 Solve the remaining determining equations

Write

$$
L:=3H_0'-2T_0'-Z_0'.
$$

After (5.3), the complete remaining nonzero coefficient list in $\mathscr P$ is:

| Monomial | Coefficient |
|---|---|
| $\rho^5v^3$ | $-(b-1)H_0'''$ |
| $\rho^4v^2\ell$ | $-(5b-1)H_0''$ |
| $\rho^5va$ | $4H_0''$ |
| $\rho^5v$ | $-T_0'''$ |
| $\rho^4v\ell$ | $-T_0''$ |
| $\rho^4v$ | $-gH_0'''$ |
| $\rho^2vc$ | $gH_0''$ |
| $\rho^5a$ | $-3T_0''$ |
| $\rho^2\ell$ | $-gZ_0''$ |
| $\rho^2R$ | $gL$ |
| $\rho\ell c$ | $-2gL$ |

An equivalent reduced set of determining conditions is therefore

$$
H_0''=0,\qquad T_0''=0,\qquad Z_0''=0,\qquad
3H_0'-2T_0'-Z_0'=0.
\tag{5.6}
$$

All entries in the table vanish when these hold. In particular, no special choice of the positive constant $b$ escapes the conditions $H_0''=T_0''=Z_0''=0$.

To see the number of free parameters before choosing their names, integrate the three second-derivative equations:

$$
T_0(t)=a_0+a_t t,\qquad
Z_0(s)=b_0+a_s s,\qquad
H_0(\phi)=e_0+a_\phi\phi,
$$

where $a_t,a_s,a_\phi$ are real constant slopes, not derivative operators. The last determining equation becomes the single linear constraint

$$
3a_\phi-2a_t-a_s=0.
$$

There are three free translation constants $(a_0,b_0,e_0)$ and two free scaling slopes: three slopes subject to one independent constraint. This is where the count

$$
3+(3-1)=5
$$

comes from.

A convenient parametrization of the two free slopes is

$$
a_\phi=c_0,\qquad a_t=c_0+d_0.
$$

Then

$$
H_0=e_0+c_0\phi.
$$

The slope constraint determines $Z_0'$:

$$
Z_0'=3c_0-2(c_0+d_0)=c_0-2d_0.
$$

Thus

$$
\boxed{
\begin{aligned}
\tau&=a_0+(c_0+d_0)t,\\
\xi&=b_0+(c_0-2d_0)s,\\
\eta&=e_0+c_0\phi.
\end{aligned}
}
\tag{5.7}
$$

Insert (5.7) into $X=\tau\partial_t+\xi\partial_s+\eta\partial_\phi$ and collect the coefficients of the five constants:

$$
\begin{aligned}
X={}&a_0\partial_t+b_0\partial_s+e_0\partial_\phi\\
&+c_0(t\partial_t+s\partial_s+\phi\partial_\phi)\\
&+d_0(t\partial_t-2s\partial_s).
\end{aligned}
\tag{5.7a}
$$

Each basis vector is the coefficient of one free constant:

| Constant set to $1$, all others set to $0$ | Resulting generator |
|---|---|
| $a_0$ | $X_1=\partial_t$ |
| $b_0$ | $X_2=\partial_s$ |
| $e_0$ | $X_3=\partial_\phi$ |
| $c_0$ | $X_4=t\partial_t+s\partial_s+\phi\partial_\phi$ |
| $d_0$ | $X_5=t\partial_t-2s\partial_s$ |

Thus

$$
\boxed{
\begin{aligned}
X_1&=\partial_t,&
X_2&=\partial_s,&
X_3&=\partial_\phi,\\
X_4&=t\partial_t+s\partial_s+\phi\partial_\phi,&
X_5&=t\partial_t-2s\partial_s.
\end{aligned}
}
\tag{5.8}
$$

Their meanings are time translation, material-label translation, field translation, simultaneous scaling, and a second scaling available at $m=3$.

These names and this normalization are convenient choices. Another invertible real linear combination of these five fields is another basis of the same algebra.

### 5.5 Check sufficiency as well as necessity

Substituting (5.7) into the prolonged action gives the identity

$$
\operatorname{pr}^{(3)}X(\Delta_3)
=-(2c_0+d_0)\Delta_3.
\tag{5.9}
$$

It vanishes on the PDE. We have therefore both restricted every smooth local point generator to (5.7) and verified every field in that family. This establishes the five-dimensional local point algebra on the declared chart.

“Five-dimensional” counts independent symmetry directions. It does not count spatial dimensions, PDE order, or arbitrary functions in the PDE solution.

For example, if a constant linear combination of these fields is identically zero, its components satisfy

$$
a_0+(c_0+d_0)t=0,\quad
b_0+(c_0-2d_0)s=0,\quad
e_0+c_0\phi=0
$$

for every point in an open set. Comparing constant and linear coefficients forces all five constants to vanish. The fields are therefore linearly independent over $\mathbb R$.

At one fixed point, their evaluated vectors lie in the three-dimensional tangent space of $(t,s,\phi)$ and cannot all be independent there. The dimension five refers to vector fields on an open set with **constant** linear coefficients. The Lie brackets below describe their algebraic structure.

### 5.6 From five generators to a symmetry algebra

The five fields are a basis. The **symmetry algebra** is the entire space

$$
\boxed{
\mathfrak g
=\operatorname{span}_{\mathbb R}\{X_1,X_2,X_3,X_4,X_5\}
=\{a_0X_1+b_0X_2+e_0X_3+c_0X_4+d_0X_5\}.
}
\tag{5.10}
$$

All five coefficients in this span are real constants. Arbitrary function multiples are not included. For example, $X_1=\partial_t$ is admitted, but $tX_1=t\partial_t$ fails the determining constraint: it has $\tau_{,t}=1$, $\xi_{,s}=\eta_{,\phi}=0$, so $3\eta_{,\phi}-2\tau_{,t}-\xi_{,s}=-2$.

A Lie algebra has both linear combinations and a *Lie bracket*. For vector fields $A,B$, define the bracket by its action on a smooth test function $f$:

$$
[A,B](f):=A(B(f))-B(A(f)).
\tag{5.11}
$$

It measures the leading failure of the two infinitesimal operations to commute. If $[A,B]=0$, their local flows commute.

For coordinate components $x=(t,s,\phi)$,

$$
A=\sum_i A^i\partial_{x^i},\qquad
B=\sum_i B^i\partial_{x^i}
\quad\Longrightarrow\quad
[A,B]=\sum_i\big(A(B^i)-B(A^i)\big)\partial_{x^i}.
$$

**Worked bracket.** With $X_2=\partial_s$ and $X_5=t\partial_t-2s\partial_s$,

$$
\begin{aligned}
{}[X_2,X_5]f
&=\partial_s(tf_t-2sf_s)
-(t\partial_t-2s\partial_s)(f_s)\\
&=tf_{ts}-2f_s-2sf_{ss}-tf_{ts}+2sf_{ss}\\
&=-2f_s.
\end{aligned}
$$

Therefore $[X_2,X_5]=-2X_2$. The full bracket table is:

| $[\,\text{row},\text{column}\,]$ | $X_1$ | $X_2$ | $X_3$ | $X_4$ | $X_5$ |
|---|---|---|---|---|---|
| $X_1$ | $0$ | $0$ | $0$ | $X_1$ | $X_1$ |
| $X_2$ | $0$ | $0$ | $0$ | $X_2$ | $-2X_2$ |
| $X_3$ | $0$ | $0$ | $0$ | $X_3$ | $0$ |
| $X_4$ | $-X_1$ | $-X_2$ | $-X_3$ | $0$ | $0$ |
| $X_5$ | $-X_1$ | $2X_2$ | $0$ | $0$ | $0$ |

Every bracket belongs to the same real span. This is bracket closure. The commutator also supplies bilinearity, antisymmetry, and the Jacobi identity, so this space is a Lie algebra.

The computation of the basis and the computation of its bracket table serve different purposes:

| Calculation | What it establishes |
|---|---|
| Solve the unrestricted determining equations. | Which point generators the PDE admits. |
| Verify their prolonged action on the PDE. | That the candidate generators really are symmetries. |
| Compute their brackets. | How those generators combine and which smaller spans form subalgebras. |

The bracket table organizes the admitted fields. It is not a replacement for the determining calculation.

### 5.7 Lie subalgebras and closure

A **Lie subalgebra** $\mathfrak h$ of $\mathfrak g$ is a real vector subspace closed under the same bracket:

$$
\boxed{
\mathfrak h\subseteq\mathfrak g,\qquad
[A,B]\in\mathfrak h\quad\text{for every }A,B\in\mathfrak h.
}
\tag{5.12}
$$

It is a collection of symmetry directions that closes internally under infinitesimal composition. It corresponds to a connected symmetry subgroup locally; no assertion of a globally closed subgroup is needed for this calculation. Olver's Section 1.4 and Theorem 1.51 explain this correspondence.

For a span $\mathfrak h=\operatorname{span}_{\mathbb R}\{A_1,\ldots,A_k\}$, bilinearity means it is enough to check the brackets of its listed basis fields.

**Example 1: one generator.** Every nonzero field $A\in\mathfrak g$ defines a one-dimensional subalgebra:

$$
\mathfrak h=\operatorname{span}_{\mathbb R}\{A\},\qquad
[aA,bA]=ab[A,A]=0.
$$

In particular,

$$
\mathfrak h_5=\operatorname{span}_{\mathbb R}\{X_5\}
$$

is the subalgebra used for the similarity reduction leading to Equation (27). The field $X_5$ is a generator; its span is the subalgebra. Replacing $X_5$ by $2X_5$ leaves that span and its invariant solutions unchanged.

**Example 2: two commuting generators.** Since $[X_4,X_5]=0$,

$$
\operatorname{span}_{\mathbb R}\{X_4,X_5\}
$$

is a two-dimensional abelian subalgebra. “Abelian” means all brackets inside it vanish.

**Example 3: a subalgebra need not be abelian.** Since $[X_3,X_4]=X_3$,

$$
\operatorname{span}_{\mathbb R}\{X_3,X_4\}
$$

is a two-dimensional nonabelian subalgebra. Its nonzero bracket stays in the span.

**Counterexample: a selected span need not close.** Let

$$
A=X_1+X_2,\qquad B=X_5.
$$

Then

$$
[A,B]=X_1-2X_2
\notin\operatorname{span}_{\mathbb R}\{X_1+X_2,X_5\}.
$$

To check the last statement, suppose $X_1-2X_2=a(X_1+X_2)+bX_5$ with real constants $a,b$. Its $\partial_t$ component would require $1=a+bt$ for all $t$, so $b=0,a=1$. Its $\partial_s$ component would then require $-2=1$, a contradiction.

Adding the missing direction gives the closed algebra $\operatorname{span}_{\mathbb R}\{X_1,X_2,X_5\}$. Merely selecting two symmetry fields does not automatically make their two-dimensional span a subalgebra.

### 5.8 First use: choose a family of invariant solutions

The full algebra describes all admitted infinitesimal point symmetries. For an invariant-solution reduction, we choose a subalgebra $\mathfrak h$ and require the solution graph to be invariant under its local subgroup.

For a basis $A_1,\ldots,A_k$ of $\mathfrak h$, this means

$$
Q_{A_1}=0,\ldots,Q_{A_k}=0,
\qquad
Q_A=\eta_A-\tau_A\phi_t-\xi_A\phi_s.
\tag{5.13}
$$

The conditions for every constant linear combination then follow automatically.

Different choices lead to different ansatzes:

| Chosen subalgebra | Invariants and resulting graph |
|---|---|
| $\operatorname{span}\{X_5\}$ | $\sigma=st^2$, $w=\phi$; hence $\phi=F(st^2)$. This is our Equation (27) route. |
| $\operatorname{span}\{X_4\}$ | $\zeta=s/t$, $w=\phi/t$; hence $\phi=t\Phi(s/t)$. |
| $\operatorname{span}\{X_1+\alpha X_2\}$, $\alpha\ne0$ | $\xi=s-\alpha t$, $w=\phi$; hence the traveling profile $\phi=\Psi(s-\alpha t)$. |
| $\operatorname{span}\{X_3\}$ | $Q_{X_3}=1$, so no graph $\phi=\phi(t,s)$ is invariant under this pure field translation. |

These are candidate invariant forms; substitution into the PDE determines the admissible profiles. Chart conditions must also hold. For example, the traveling profile is in our positive chart only where $\Psi'>0$ and $\alpha<0$, because $\phi_s=\Psi'$ and $\phi_t=-\alpha\Psi'$.

For $\mathfrak h_5$, the generator has nonzero projection $(t,-2s)$ on the independent-variable plane. Its orbits there have rank one, so a regular invariant graph depends on one independent invariant, $\sigma$. This produces an ODE.

In general, the number of independent variables removed is controlled by orbit rank and compatibility with solution graphs, not by the dimension of an arbitrary algebra alone. The $X_3$ example shows why “one generator always gives a PDE-to-ODE reduction” needs these qualifications.

**Worked two-generator example.** Choose the abelian subalgebra $\operatorname{span}\{X_4,X_5\}$. The $X_5$ condition first gives $\phi=F(\sigma)$, $\sigma=st^2$. On such a graph,

$$
\begin{aligned}
Q_{X_4}
&=\phi-t\phi_t-s\phi_s\\
&=F-2\sigma F'-\sigma F'\\
&=F-3\sigma F'.
\end{aligned}
$$

Requiring $Q_{X_4}=0$ gives

$$
F'=F/(3\sigma)
\quad\Longrightarrow\quad
F=K\sigma^{1/3}.
\tag{5.14}
$$

Substitution into (R3), calculated explicitly in Section 15, imposes

$$
K^3=\frac{27g}{1-4b},\qquad 0<b<\frac14
$$

on the positive branch. Thus two independent-variable symmetry directions select a power profile whose amplitude must satisfy an algebraic condition.

The more general exact family $F=F_0+K\sigma^{1/3}$ in Section 15 is not invariant under $X_4$ when $F_0\ne0$: its characteristic above equals $F_0$. Instead, it is invariant under $\operatorname{span}\{X_5,X_4-F_0X_3\}$. This is how a field translation moves the invariant family to a related subalgebra.

### 5.9 Second use: determine which symmetries survive reduction

Once $\mathfrak h_5=\operatorname{span}\{X_5\}$ is chosen, we need to know which other generators act consistently on its orbit coordinates.

A sufficient infinitesimal condition for $A$ to preserve these orbits is

$$
[A,\mathfrak h_5]\subseteq\mathfrak h_5.
$$

The set of all such fields in $\mathfrak g$ is the **normalizer**

$$
\mathfrak n_{\mathfrak g}(\mathfrak h_5)
:=\{A\in\mathfrak g:[A,\mathfrak h_5]\subseteq\mathfrak h_5\}.
\tag{5.15}
$$

The descent property follows directly from the bracket identity. If $I$ is an $\mathfrak h_5$ invariant and $B\in\mathfrak h_5$, then

$$
B(A(I))=[B,A](I)+A(B(I))=0.
$$

Both terms vanish because $[B,A]\in\mathfrak h_5$ and $B(I)=0$. Thus $A(I)$ is again invariant and can be expressed in the quotient coordinates.

For our general field (5.10), use the bracket table:

$$
[A,X_5]=a_0X_1-2b_0X_2.
$$

This belongs to $\operatorname{span}\{X_5\}$ only when $a_0=b_0=0$. Therefore

$$
\boxed{
\mathfrak n_{\mathfrak g}(\mathfrak h_5)
=\operatorname{span}_{\mathbb R}\{X_3,X_4,X_5\}.
}
\tag{5.16}
$$

The $X_5$ direction becomes zero on its own invariants. The two remaining directions act on $\sigma=st^2$ and $w=\phi$ as

$$
\begin{array}{c|cc}
&\sigma&w\\ \hline
X_3&0&1\\
X_4&3\sigma&w
\end{array}
$$

On profile space $(\sigma,F)$, they become

$$
Z=\partial_F,\qquad
Y=3\sigma\partial_\sigma+F\partial_F.
\tag{5.17}
$$

These are exactly the two inherited symmetries used in Section 10.

**Subalgebra versus ideal.** A subalgebra only requires $[\mathfrak h,\mathfrak h]\subseteq\mathfrak h$. An *ideal* of an algebra $\mathfrak a$ satisfies the stronger condition $[\mathfrak a,\mathfrak h]\subseteq\mathfrak h$. A Lie algebra quotient $\mathfrak a/\mathfrak h$ requires that ideal condition.

Here $\mathfrak h_5$ is not an ideal of the full $\mathfrak g$, since $[X_1,X_5]=X_1\notin\mathfrak h_5$. It is an ideal of its normalizer. The inherited algebra just computed is therefore represented by

$$
\boxed{
\mathfrak n_{\mathfrak g}(\mathfrak h_5)/\mathfrak h_5
\simeq\operatorname{span}_{\mathbb R}\{Z,Y\}.
}
\tag{5.18}
$$

This identifies the inherited directions; extra symmetries of the reduced ODE, if present, would require their own determining calculation.

**How this organizes the next order reduction.** The reduced pair satisfies

$$
[Y,Z]=-Z.
$$

Thus $\operatorname{span}\{Z\}$ is an ideal of $\operatorname{span}\{Z,Y\}$. Reducing first by translation $Z$ uses $\mu=F'$ and leaves a scaling that descends as

$$
Y_1=3\sigma\partial_\sigma-2\mu\partial_\mu.
$$

Reducing by $Y_1$ then produces $\Sigma,M$ and the first-order equation of Sections 11–12. The bracket relation explains why this order of reductions retains the second symmetry.

These ODE order reductions use differential invariants and reconstruction. Imposing $Q_Y=0$ instead would select the special power profile (5.14), rather than retain the general regular local profiles described by (R3).

### 5.10 Third use: organize distinct reductions and respect data

There are infinitely many one-dimensional subalgebras:

$$
\operatorname{span}_{\mathbb R}
\{a_0X_1+b_0X_2+e_0X_3+c_0X_4+d_0X_5\},
$$

with the five constants not all zero. Multiplying all five by the same nonzero number gives the same subalgebra. The five basis directions are therefore only five particular choices.

Further equivalences come from symmetry transformations. If a symmetry transformation $S$ takes a subgroup $H$ to $SHS^{-1}$, it takes $H$-invariant solutions to $SHS^{-1}$-invariant solutions. At the algebra level this is the adjoint action $\operatorname{Ad}_S$.

An **optimal system** lists one representative of each subalgebra class under the chosen symmetry group's adjoint action. It organizes reductions without repeatedly treating symmetry-equivalent cases. This is Olver's Section 3.3, especially Proposition 3.6 and Definition 3.11.

For example, a time translation moves scaling about time zero to scaling about a shifted time origin:

$$
X_5-t_*X_1=(t-t_*)\partial_t-2s\partial_s.
$$

Its independent invariant is $s(t-t_*)^2$. Where $t-t_*>0$ and the charts overlap, this is the translated version of the $X_5$ construction, rather than a new scaling mechanism.

Sections 5.12–5.14 give the separate adjoint classification, including the resonant cases absent from the shorter source list. The classification is under the connected local flow action defined there.

Finally, a PDE symmetry need not preserve prescribed data or boundaries. A symmetry of a boundary-value problem must also preserve its data and boundary sets. For example, $X_5$ moves the fixed boundary $s=L>0$ because its $s$ component there is $-2L\ne0$. For an individual similarity candidate, directly check the data compatibility described in Section 14.

The roles of subalgebras can now be summarized concretely:

| Role | What it does in this calculation |
|---|---|
| Select an invariant family. | $\operatorname{span}\{X_5\}$ selects $\phi=F(st^2)$. |
| Impose additional invariance. | $\operatorname{span}\{X_4,X_5\}$ selects a power profile. |
| Control inheritance. | The normalizer of $\operatorname{span}\{X_5\}$ identifies $Z,Y$ after PDE reduction. |
| Organize successive ODE reductions. | The ideal $\operatorname{span}\{Z\}$ allows translation reduction while retaining the scaling. |
| Classify reduction choices. | Adjoint equivalence identifies subalgebras giving symmetry-related ansatzes. |

The algebra $\mathfrak g$ determines all admitted infinitesimal point symmetries. The chosen subalgebra $\mathfrak h\subseteq\mathfrak g$ specifies the directions used in a particular reduction.

### 5.11 The parameter $m$: what the scaling calculation establishes

The unrestricted calculation above proves completeness at $m=3$. A general-exponent statement must be derived separately because the powers used for coefficient separation can coincide or disappear at exceptional exponents.

**Definition.** Consider an affine diagonal scaling with constant slopes

$$
X_{\mathrm{sc}}=a_t t\partial_t+a_s s\partial_s+a_\phi\phi\partial_\phi.
$$

Its flow is $(\bar t,\bar s,\bar\phi)=(e^{a_t\epsilon}t,e^{a_s\epsilon}s,e^{a_\phi\epsilon}\phi)$. A derivative $\phi_{t^is^j}$ has weight $a_\phi-ia_t-ja_s$. The three types of terms in $\Delta_m$ have weights

$$
\begin{aligned}
w_I&=w(\phi_s\phi_{ttt})=w(\phi_{ts}\phi_{tt})
=2a_\phi-a_s-3a_t,\\
w_G&=w\big(D_t(\phi_{ss}/\phi_s^2)\big)=-a_\phi-a_t,\\
w_B&=w\big(D_s(\phi_t^{m-1}\phi_{ts}/\phi_s)\big)
=(m-1)a_\phi-ma_t-a_s.
\end{aligned}
$$

For $g\beta\ne0$, comparison of the independent gravitational and transport jet terms gives

$$
\begin{aligned}
w_I-w_G&=3a_\phi-2a_t-a_s=0,\\
w_I-w_B&=(3-m)(a_\phi-a_t)=0.
\end{aligned}
\tag{5.19}
$$

Equivalently, the two relations are

$$
3a_\phi-2a_t-a_s=0,\qquad
ma_\phi-(m-1)a_t-a_s=0.
\tag{5.20}
$$

Subtracting the first from the second gives $(m-3)(a_\phi-a_t)=0$. Thus the diagonal scaling space is one-dimensional when $m\ne3$, with $a_t=a_s=a_\phi$, and two-dimensional when $m=3$, with $a_s=3a_\phi-2a_t$. This recovers $X_4$ and the exceptional $X_5$.

**Correction to the fuller supplied text.** Its proposed second slope relation,
$(m-1)(a_\phi-a_t)+a_t-a_s=0$, would give $(m-4)(a_\phi-a_t)=0$ after substitution of the first relation. It therefore cannot justify the stated cubic exception. Equations (5.19)–(5.20) are the corrected relations derived directly from the weights.

This calculation classifies diagonal scalings, not all point generators for every $m$. In particular, at $m=1$,

$$
\Delta_1=\rho T+\ell a-g(\rho^{-2}+\beta\rho^{-1})R
+g(2\rho^{-3}+\beta\rho^{-2})\ell c
$$

does not depend on $v=\phi_t$. The transformation

$$
\bar\phi=\phi+\epsilon t,\qquad\bar t=t,\quad\bar s=s
$$

changes only $v$ among its derivative arguments. Hence $t\partial_\phi$ is an additional point symmetry of the stated scalar equation at $m=1$. It is not a constant real combination of $X_1,\ldots,X_4$. This exact example prevents the unqualified inference that the full algebra has dimension four for every $m\ne3$.

### 5.12 Adjoint action: convention, motivation, and complete table

**Motivation.** A symmetry transformation maps an invariant-solution family to the family associated with the conjugate subgroup. Classification up to conjugacy removes duplicated reductions. Classification is a separate task from selecting $\langle X_5\rangle$ for the Abel calculation.

Let $\Gamma_\epsilon^A$ be the local flow of a vector field $A$. Define its action on a vector field $B$ by

$$
\mathcal A_{A,\epsilon}B=(\Gamma_\epsilon^A)_*B.
\tag{5.21}
$$

At a target point $q$, the definition is

$$
\big(\mathcal A_{A,\epsilon}B\big)_q
=d\Gamma_\epsilon^A\big|_{\Gamma_{-\epsilon}^A(q)}
 B_{\Gamma_{-\epsilon}^A(q)}.
$$

With the vector-field bracket $[A,B]=AB-BA$, this convention gives

$$
\left.\frac d{d\epsilon}\right|_0\mathcal A_{A,\epsilon}B=-[A,B],
$$

and therefore

$$
\mathcal A_{A,\epsilon}B
=B-\epsilon[A,B]+\frac{\epsilon^2}{2}[A,[A,B]]
-\frac{\epsilon^3}{6}[A,[A,[A,B]]]+\cdots.
\tag{5.22}
$$

This is the minus-sign convention used in the paper's adjoint table. It is explicitly tied here to pushforward by a flow; a convention using the inverse flow reverses the parameter signs. Both generate the same conjugacy equivalence classes.

For example, $[X_1,X_4]=X_1$ and $[X_1,X_1]=0$, so

$$
\mathcal A_{X_1,\epsilon}X_4=X_4-\epsilon X_1.
$$

The same result follows without a series. Translation sends $(t,s,\phi)$ to $(t+\epsilon,s,\phi)$, so at the target coordinates the coefficient of $\partial_t$ in the pushed-forward $X_4$ is $t-\epsilon$.

For $[X_5,X_2]=2X_2$, all nested brackets are $2^jX_2$, giving

$$
\mathcal A_{X_5,\epsilon}X_2
=\left(1-2\epsilon+\frac{(2\epsilon)^2}{2!}
-\frac{(2\epsilon)^3}{3!}+\cdots\right)X_2
=e^{-2\epsilon}X_2.
$$

Similarly, $\operatorname{ad}_{X_5}^jX_1=(-1)^jX_1$, so the sum is $e^\epsilon X_1$. The translations commute, while $X_4$ scales all three translation fields by $e^\epsilon$. These computations give every entry:

| $\mathcal A_{X_A,\epsilon}X_B$ | $X_1$ | $X_2$ | $X_3$ | $X_4$ | $X_5$ |
|---|---|---|---|---|---|
| $X_1$ | $X_1$ | $X_2$ | $X_3$ | $X_4-\epsilon X_1$ | $X_5-\epsilon X_1$ |
| $X_2$ | $X_1$ | $X_2$ | $X_3$ | $X_4-\epsilon X_2$ | $X_5+2\epsilon X_2$ |
| $X_3$ | $X_1$ | $X_2$ | $X_3$ | $X_4-\epsilon X_3$ | $X_5$ |
| $X_4$ | $e^\epsilon X_1$ | $e^\epsilon X_2$ | $e^\epsilon X_3$ | $X_4$ | $X_5$ |
| $X_5$ | $e^\epsilon X_1$ | $e^{-2\epsilon}X_2$ | $X_3$ | $X_4$ | $X_5$ |

The supplied v3 article's Table 2 already contains $X_3$ in its row $X_2$, column $X_3$. The fuller text's allegation that this particular entry is printed as $X_2$ is not supported by that version. The bracket signs in the final row of Table 1 do require correction, as shown in Section 5.6.

### 5.13 A complete one-dimensional classification under the connected action

**Definition.** Two nonzero generators determine equivalent one-dimensional subalgebras if

$$
\widetilde Z=\lambda\mathcal A_g Z,
\qquad\lambda\in\mathbb R\setminus\{0\},
$$

where $g$ is a composition of the local flows generated by $X_1,\ldots,X_5$. This subsection classifies under that connected action. Additional disconnected symmetries are not included. On the positive coordinate chart, translations are understood locally where the charts overlap.

Write

$$
Z=a_1X_1+a_2X_2+a_3X_3+a_4X_4+a_5X_5\ne0.
$$

Since all brackets lie in the translation ideal $\langle X_1,X_2,X_3\rangle$, the pair $(a_4,a_5)$ is unchanged by every adjoint action. It is multiplied by $\lambda$ when the representative generator is rescaled. For fixed $(a_4,a_5)$, translations act by

$$
\begin{aligned}
a_1&\longmapsto a_1-\epsilon_1(a_4+a_5),\\
a_2&\longmapsto a_2-\epsilon_2(a_4-2a_5),\\
a_3&\longmapsto a_3-\epsilon_3a_4.
\end{aligned}
\tag{5.23}
$$

This formula displays all denominators that must be checked before elimination.

**Case A: $a_4\ne0$.** Divide by $a_4$ and put $\alpha=a_5/a_4$. If $\alpha\ne-1,1/2$, choose

$$
\epsilon_1=\frac{a_1}{1+\alpha},\qquad
\epsilon_2=\frac{a_2}{1-2\alpha},\qquad
\epsilon_3=a_3,
$$

where the $a_i$ now denote the normalized coefficients. The resulting representative is $X_4+\alpha X_5$. This includes $X_4$ at $\alpha=0$.

At $\alpha=-1$, the coefficient of $\epsilon_1$ in (5.23) is zero. Eliminate $a_2,a_3$ using $\epsilon_2=a_2/3$, $\epsilon_3=a_3$, but retain $a_1X_1$. The scaling actions multiply $a_1$ by positive factors, so its residual value can be normalized to $\nu\in\{-1,0,1\}$. The representatives are

$$
X_4-X_5+\nu X_1.
\tag{5.24}
$$

At $\alpha=1/2$, eliminate $a_1,a_3$ with $\epsilon_1=2a_1/3$, $\epsilon_3=a_3$, but retain $a_2X_2$. Again positive scaling leaves three sign cases:

$$
X_4+\tfrac12X_5+\nu X_2,\qquad\nu\in\{-1,0,1\}.
\tag{5.25}
$$

**Case B: $a_4=0$, $a_5\ne0$.** Normalize $a_5=1$. Choose $\epsilon_1=a_1$ and $\epsilon_2=-a_2/2$. The coefficient $a_3$ cannot be removed by translation, because $[X_3,X_5]=0$. The $X_4$ scaling normalizes its magnitude but preserves its sign, giving

$$
X_5+\nu X_3,\qquad\nu\in\{-1,0,1\}.
\tag{5.26}
$$

In particular, deleting $a_3$ without an operation that changes it is not a valid adjoint elimination.

**Case C: $a_4=a_5=0$.** The generator is a nonzero translation. Translations themselves act trivially. The two scalings act by

$$
(a_1,a_2,a_3)\longmapsto
(e^{r+q}a_1,e^{r-2q}a_2,e^ra_3).
\tag{5.27}
$$

The set of nonzero coordinates is preserved. When exactly one coordinate is nonzero, rescaling the generator gives $X_1$, $X_2$, or $X_3$.

When exactly two coordinates are nonzero, normalize one to $1$. The remaining ratios transform by positive factors:

$$
\frac{a_2}{a_1}\mapsto e^{-3q}\frac{a_2}{a_1},\qquad
\frac{a_3}{a_1}\mapsto e^{-q}\frac{a_3}{a_1},\qquad
\frac{a_3}{a_2}\mapsto e^{2q}\frac{a_3}{a_2}.
$$

Their absolute values can be normalized to $1$ but their signs cannot. The representatives are

$$
X_1+\varepsilon X_2,\qquad
X_1+\varepsilon X_3,\qquad
X_2+\varepsilon X_3,\qquad\varepsilon\in\{-1,1\}.
\tag{5.28}
$$

Here $\varepsilon$ is a discrete sign, not the continuous group parameter $\epsilon$.

When all three coordinates are nonzero, first set $a_1=1$. The ratios $r_2=a_2/a_1$ and $r_3=a_3/a_1$ transform as $r_2\mapsto e^{-3q}r_2$ and $r_3\mapsto e^{-q}r_3$. Taking $q=\log|r_3|$ makes the third coefficient $\varepsilon=\operatorname{sgn}(r_3)$. The second becomes

$$
k_o=\frac{r_2}{|r_3|^3}\ne0.
$$

The representatives are

$$
X_1+k_oX_2+\varepsilon X_3,
\qquad k_o\in\mathbb R\setminus\{0\},\quad\varepsilon\in\{-1,1\}.
\tag{5.29}
$$

The invariant $a_1^2a_2/a_3^3=\varepsilon k_o$ and the sign of $a_3/a_1$ distinguish these classes. These invariants also show why both arbitrary coefficients in an unnormalized family cannot simply be regarded as independent orbit moduli.

The complete classification is therefore:

| Nonzero scaling part | Representatives and parameter range |
|---|---|
| Generic $a_4\ne0$ | $\langle X_4+\alpha X_5\rangle$, $\alpha\in\mathbb R\setminus\{-1,1/2\}$ |
| $a_5/a_4=-1$ | $\langle X_4-X_5+\nu X_1\rangle$, $\nu=0,\pm1$ |
| $a_5/a_4=1/2$ | $\langle X_4+\tfrac12X_5+\nu X_2\rangle$, $\nu=0,\pm1$ |
| $a_4=0$, $a_5\ne0$ | $\langle X_5+\nu X_3\rangle$, $\nu=0,\pm1$ |
| No scaling part; one translation component | $\langle X_1\rangle$, $\langle X_2\rangle$, $\langle X_3\rangle$ |
| No scaling part; two translation components | The three sign families in (5.28) |
| No scaling part; three translation components | The family (5.29) |

**Proposition.** The table covers every one-dimensional subalgebra of the five-dimensional algebra under the declared connected adjoint action, without redundant representatives within the listed parameter ranges.

**Proof.** The nonzero pair $(a_4,a_5)$ is unchanged by adjoint action and is determined up to overall scalar multiplication, so Cases A and B are exhaustive and mutually distinct. Formula (5.23) removes exactly the nonresonant translation components. The diagonal scalings multiply any remaining component by an arbitrary positive factor, leaving precisely its sign and zero status. For Case C, (5.27) preserves support; the ratio formulas establish the two-component normalization; (5.29) and its two invariants establish the three-component normalization and uniqueness. Translations have no further action on Case C, and compositions of the displayed flows generate the connected group in question. This proves coverage and the stated inequivalences.

The shorter seven-family list in the source and the fuller supplied text omits the nonzero residual terms in (5.24)–(5.26), as well as mixed $X_2,X_3$ translations. It also contains overlaps. It is not a complete optimal system for the connected action just defined.

### 5.14 Invariants for the representative reduction families

**Definition.** A point invariant $I$ of $Z$ satisfies $Z(I)=0$. Two functionally independent such invariants label regular one-dimensional orbits in the three-dimensional point manifold. They produce an invariant graph only if the graph transversality condition permits a dependent-variable representation.

For $X_4+\alpha X_5$, $\alpha\ne-1$, solve

$$
\dot t=(1+\alpha)t,\qquad
\dot s=(1-2\alpha)s,\qquad
\dot\phi=\phi.
$$

The logarithmic derivatives yield

$$
\frac d{d\epsilon}\left(\log s-\frac{1-2\alpha}{1+\alpha}\log t\right)=0,
\qquad
\frac d{d\epsilon}\left(\phi t^{-1/(1+\alpha)}\right)=0.
$$

Thus the usual invariants are $s t^{(2\alpha-1)/(1+\alpha)}$ and $\phi t^{-1/(1+\alpha)}$. At $\alpha=-1$, division by $1+\alpha$ is invalid; the invariant pair is instead $t$, $\phi s^{-1/3}$ when the residual translation vanishes.

For the exceptional residual branches, integrate the finite orbit equations directly. Their verified invariant pairs, together with the principal families, are:

| Generator | Independent invariant | Dependent invariant | Invariant graph |
|---|---|---|---|
| $X_4$ | $s/t$ | $\phi/t$ | $\phi=t\Phi(s/t)$ |
| $X_5$ | $st^2$ | $\phi$ | $\phi=F(st^2)$ |
| $X_4+\alpha X_5$, $\alpha\ne-1$ | $s t^{(2\alpha-1)/(1+\alpha)}$ | $\phi t^{-1/(1+\alpha)}$ | $\phi=t^{1/(1+\alpha)}\Phi(s t^{(2\alpha-1)/(1+\alpha)})$ |
| $X_4-X_5$ | $t$ | $\phi s^{-1/3}$ | $\phi=s^{1/3}\Phi(t)$ |
| $X_4-X_5+\nu X_1$, $\nu=\pm1$ | $s e^{-3t/\nu}$ | $\phi e^{-t/\nu}$ | $\phi=e^{t/\nu}\Phi(s e^{-3t/\nu})$ |
| $X_4+\tfrac12X_5+\nu X_2$ | $s-\tfrac{2\nu}{3}\log t$ | $\phi t^{-2/3}$ | $\phi=t^{2/3}\Phi(s-\tfrac{2\nu}{3}\log t)$ |
| $X_5+\nu X_3$ | $st^2$ | $\phi-\nu\log t$ | $\phi=\nu\log t+F(st^2)$ |
| $X_1+\alpha X_2+\gamma X_3$ | $s-\alpha t$ | $\phi-\gamma t$ | $\phi=\gamma t+\Phi(s-\alpha t)$ |
| $X_2+\gamma X_3$ | $t$ | $\phi-\gamma s$ | $\phi=\gamma s+\Phi(t)$ |

For example, for $X_4-X_5+\nu X_1=\nu\partial_t+3s\partial_s+\phi\partial_\phi$,

$$
\begin{aligned}
Z(s e^{-3t/\nu})&=3s e^{-3t/\nu}-3s e^{-3t/\nu}=0,\\
Z(\phi e^{-t/\nu})&=\phi e^{-t/\nu}-\phi e^{-t/\nu}=0.
\end{aligned}
$$

For the second exceptional scaling, $Z(t)=3t/2$ and $Z(s)=\nu$, so

$$
Z\left(s-\frac{2\nu}{3}\log t\right)=\nu-\frac{2\nu}{3}\frac32=0,
\qquad
Z(\phi t^{-2/3})=\phi t^{-2/3}-\phi t^{-2/3}=0.
$$

For $X_5+\nu X_3$, $Z(\phi-\nu\log t)=\nu-\nu=0$. These checks also cover $\nu=0$ where no division by $\nu$ occurs in the displayed formula.

For pure $X_1$, invariant graphs have $\phi=F(s)$ and therefore $\phi_t=0$, outside the strictly positive-velocity chart. Pure $X_2$ would require $\phi_s=0$, outside the scalar PDE's denominator chart. Pure $X_3$ has no invariant graph because its characteristic is $1$. These cases remain legitimate algebraic subalgebras; their graph and domain properties must be stated separately.

This table identifies invariant forms. Their substitution and solution are additional steps. The main derivation below performs them completely for $\langle X_5\rangle$; Section 19 supplies the traveling-wave calculation.


## 6. Direct verification of $X_5$ by scaling weights

Appendix C.2–C.4 supplies the flow definition, its explicit integration, and the chain-rule derivation of the weights.

The long prolongation calculation found $X_5$. Once this particular diagonal scaling is known, weights provide a shorter check.

### 6.1 Definition and integration of the one-parameter flow

**Definition.** The local flow of $X=\tau\partial_t+\xi\partial_s+\eta\partial_\phi$ is the solution $\Gamma_\epsilon(t,s,\phi)=(\bar t,\bar s,\bar\phi)$ of

$$
\dot{\bar t}=\tau(\bar t,\bar s,\bar\phi),\quad
\dot{\bar s}=\xi(\bar t,\bar s,\bar\phi),\quad
\dot{\bar\phi}=\eta(\bar t,\bar s,\bar\phi),
$$

with $\Gamma_0=\mathrm{id}$. The dot means $d/d\epsilon$, and the coefficients are evaluated at the moving point. Local uniqueness gives $\Gamma_{\epsilon+\delta}=\Gamma_\epsilon\circ\Gamma_\delta$ where defined. For $X_5$, the system is

$$
\frac{d\bar t}{d\epsilon}=\bar t,\qquad
\frac{d\bar s}{d\epsilon}=-2\bar s,\qquad
\frac{d\bar\phi}{d\epsilon}=0,
$$

with $(\bar t,\bar s,\bar\phi)=(t,s,\phi)$ at $\epsilon=0$:

$$
\bar t=e^\epsilon t,\qquad
\bar s=e^{-2\epsilon}s,\qquad
\bar\phi=\phi.
\tag{6.1}
$$

A quantity has *weight* $w$ if this flow multiplies it by $e^{w\epsilon}$.

Since

$$
D_{\bar t}=e^{-\epsilon}D_t,\qquad
D_{\bar s}=e^{2\epsilon}D_s,
$$

and $\phi$ has weight zero,

$$
w(\phi_{t^i s^j})=2j-i.
\tag{6.2}
$$

| Jet | $v$ | $\rho$ | $a$ | $\ell$ | $c$ | $T$ | $U$ | $R$ | $V$ |
|---|---|---|---|---|---|---|---|---|---|
| Weight | $-1$ | $2$ | $-2$ | $1$ | $4$ | $-3$ | $0$ | $3$ | $6$ |

Weights add in products and subtract in quotients.

### 6.2 Apply weights to the two divergence terms

For this subsection define

$$
\mathcal A_m=D_t\left(\phi_s\phi_{tt}-g\phi_{ss}/\phi_s^2\right),
\qquad
\mathcal B_m=g\beta D_s\left(\phi_t^{m-1}\phi_{ts}/\phi_s\right).
$$

Thus $\Delta_m=\mathcal A_m-\mathcal B_m$.

Inside $\mathcal A_m$, the weights are

$$
w(\phi_s\phi_{tt})=2-2=0,\qquad
w(\phi_{ss}/\phi_s^2)=4-4=0.
$$

The outer $D_t$ contributes $-1$, so $w(\mathcal A_m)=-1$.

Inside $\mathcal B_m$,

$$
w(\phi_t^{m-1}\phi_{ts}/\phi_s)
=-(m-1)+1-2=-m.
$$

The outer $D_s$ contributes $2$, so $w(\mathcal B_m)=2-m$.

Differentiating the scaling factors at $\epsilon=0$ now gives

$$
\begin{aligned}
\operatorname{pr}^{(3)}X_5(\Delta_m)
&=-\mathcal A_m-(2-m)\mathcal B_m\\
&=-\Delta_m+(m-3)\mathcal B_m.
\end{aligned}
\tag{6.3}
$$

For $m=3$,

$$
\boxed{\operatorname{pr}^{(3)}X_5(\Delta_3)=-\Delta_3.}
$$

The equation's zero set is preserved, which is precisely the test in (3.2). For $m\ne3$, the extra term does not vanish on unrestricted solution jets, so this fixed-parameter generator is not a symmetry of the generic equation.

The weight calculation is an efficient form of prolongation for a diagonal scaling. General prolongation remains a valid method.

## 7. Invariant graphs and the PDE similarity ansatz

Appendix C.5–C.7 gives the geometry of orbit labels, graph tangency, and the invariant-surface condition $Q=0$.

### 7.1 Find quantities unchanged along the group orbits

A point invariant $I$ satisfies $X_5(I)=0$. Along a group orbit,

$$
\frac{dt}{t}=\frac{ds}{-2s},\qquad d\phi=0.
$$

The first equality gives

$$
2\,\frac{dt}{t}+\frac{ds}{s}=0
\quad\Longrightarrow\quad
d\log(st^2)=0.
$$

Choose the two point invariants

$$
\sigma=st^2,\qquad w=\phi.
$$

Choose also an orbit coordinate $y=\log t$, because $X_5(y)=1$. Directly,

$$
X_5(\sigma)=t(2st)-2s(t^2)=0,\qquad X_5(w)=0.
$$

The coordinate map is

$$
(t,s,\phi)\longmapsto(y,\sigma,w)
=(\log t,st^2,\phi).
$$

Its Jacobian determinant is $t\ne0$, with inverse

$$
t=e^y,\qquad s=\sigma e^{-2y},\qquad \phi=w.
$$

In these coordinates,

$$
X_5=\partial_y.
$$

This is called straightening the vector field: scaling in the old coordinates becomes translation in $y$.

### 7.2 Graph tangency and the invariant-surface condition

The equation $X_5(w)=0$ says that the point coordinate $w=\phi$ does not move along an ambient group orbit. An arbitrary graph can still have the form

$$
w=\widetilde\phi(y,\sigma)
$$

with genuine $y$ dependence.

To require the graph itself to be invariant, the generator must be tangent to it. For a graph $\phi=f(t,s)$, apply $X$ to its defining function $\phi-f(t,s)$:

$$
X(\phi-f)=\eta-\tau f_t-\xi f_s.
$$

The resulting *characteristic*, evaluated on the graph, is

$$
Q:=\eta-\tau\phi_t-\xi\phi_s.
$$

For $X_5$ this becomes

$$
\boxed{Q=-t\phi_t+2s\phi_s=0.}
\tag{7.1}
$$

At fixed $\sigma$, differentiation with respect to $y$ gives

$$
\widetilde\phi_y=t\phi_t-2s\phi_s.
$$

Therefore $Q=0$ says $\widetilde\phi_y=0$. Only now do we obtain

$$
\boxed{\phi(t,s)=F(\sigma),\qquad \sigma=st^2.}
\tag{7.2}
$$

We have chosen a particular symmetry-invariant family of PDE solutions. This family does not represent arbitrary PDE data.

## 8. Complete derivative table for the similarity ansatz

From this point onward, a prime on $F$ means differentiation with respect to $\sigma$. Write

$$
p=F'(\sigma),\qquad q=F''(\sigma),\qquad r=F'''(\sigma).
$$

These are profile derivatives. The lowercase $q$ is not the invariant-surface characteristic $Q$.

The basic chain-rule quantities are

$$
\sigma_t=2st=\frac{2\sigma}{t},\qquad
\sigma_s=t^2.
$$

In the straightened independent coordinates,

$$
D_t=\frac1tD_y+\frac{2\sigma}{t}D_\sigma,\qquad
D_s=t^2D_\sigma.
\tag{8.1}
$$

Although $F,p,q$ do not depend on $y$, factors such as $t=e^y$ do. They must still be differentiated.

### 8.1 First derivatives

$$
\phi_t=F'\sigma_t=\frac{2\sigma p}{t},
\qquad
\phi_s=F'\sigma_s=t^2p.
\tag{8.2}
$$

Our positive chart therefore gives $p>0$ and $\sigma>0$.

### 8.2 Second derivatives

For $\phi_{tt}$, apply both the product rule and the chain rule:

$$
\begin{aligned}
\phi_{tt}
&=D_t\left(\frac{2\sigma p}{t}\right)\\
&=-\frac{2\sigma p}{t^2}
+\frac1t(2p+2\sigma q)\frac{2\sigma}{t}\\
&=\frac{2\sigma p+4\sigma^2q}{t^2}.
\end{aligned}
$$

For the mixed derivative, $t$ is fixed under $D_s$:

$$
\begin{aligned}
\phi_{ts}
&=\frac1tD_s(2\sigma p)\\
&=\frac1t(2p+2\sigma q)t^2\\
&=2t(p+\sigma q).
\end{aligned}
$$

Similarly,

$$
\phi_{ss}=D_s(t^2p)=t^2q\,\sigma_s=t^4q.
\tag{8.3}
$$

### 8.3 Third derivatives

Let $K=2\sigma p+4\sigma^2q$. Then

$$
K'=2p+10\sigma q+4\sigma^2r.
$$

Hence

$$
\begin{aligned}
\phi_{ttt}
&=D_t(t^{-2}K)
=t^{-3}(-2K+2\sigma K')\\
&=\frac{12\sigma^2q+8\sigma^3r}{t^3},
\end{aligned}
$$

and

$$
\phi_{tts}=D_s(t^{-2}K)=K'
=2p+10\sigma q+4\sigma^2r.
$$

Also,

$$
\begin{aligned}
\phi_{tss}
&=D_t(t^4q)
=4t^3q+t^4r\frac{2\sigma}{t}\\
&=2t^3(2q+\sigma r),
\end{aligned}
$$

and

$$
\phi_{sss}=D_s(t^4q)=t^6r.
\tag{8.4}
$$

For convenient checking, the full list is

$$
\boxed{
\begin{aligned}
\phi_t&=2\sigma p/t,&
\phi_s&=t^2p,\\
\phi_{tt}&=(2\sigma p+4\sigma^2q)/t^2,&
\phi_{ts}&=2t(p+\sigma q),&
\phi_{ss}&=t^4q,\\
\phi_{ttt}&=(12\sigma^2q+8\sigma^3r)/t^3,&
\phi_{tts}&=2p+10\sigma q+4\sigma^2r,\\
\phi_{tss}&=2t^3(2q+\sigma r),&
\phi_{sss}&=t^6r.
\end{aligned}
}
$$

## 9. Exact PDE pullback and the third-order profile equation

### 9.1 Use the divergence form to keep the algebra manageable

For the first bracket in (P),

$$
\begin{aligned}
\phi_s\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^2}
&=(t^2p)\frac{2\sigma p+4\sigma^2q}{t^2}
-g\frac{t^4q}{t^4p^2}\\
&=2\sigma p^2+4\sigma^2pq-g\frac{q}{p^2}.
\end{aligned}
$$

Call this expression $\mathcal A(\sigma)$. At $m=3$, the second bracket is

$$
\begin{aligned}
\phi_t^2\frac{\phi_{ts}}{\phi_s}
&=\frac{4\sigma^2p^2}{t^2}
\frac{2t(p+\sigma q)}{t^2p}\\
&=\frac1{t^3}\,8\sigma^2p(p+\sigma q).
\end{aligned}
$$

Call the last profile expression $\mathcal B(\sigma)=8\sigma^2p(p+\sigma q)$. These $\mathcal A,\mathcal B$ are profile expressions, not the full PDE terms $\mathcal A_m,\mathcal B_m$ of Section 6.

Since $D_t\mathcal A=(2\sigma/t)\mathcal A'$ and $D_s(t^{-3}\mathcal B)=t^{-1}\mathcal B'$,

$$
\left.\Delta_3\right|_{\phi=F(st^2)}
=\frac1t\left(2\sigma\mathcal A'-b\mathcal B'\right).
\tag{9.1}
$$

### 9.2 Differentiate and collect

Use $p'=q$ and $q'=r$:

$$
\begin{aligned}
\mathcal A'
&=2p^2+4\sigma pq
+8\sigma pq+4\sigma^2(q^2+pr)
-g\left(\frac r{p^2}-\frac{2q^2}{p^3}\right)\\
&=2p^2+12\sigma pq+4\sigma^2(q^2+pr)
-g\frac r{p^2}+2g\frac{q^2}{p^3},
\end{aligned}
$$

and

$$
\begin{aligned}
\mathcal B'
&=\frac d{d\sigma}(8\sigma^2p^2+8\sigma^3pq)\\
&=16\sigma p^2+16\sigma^2pq
+24\sigma^2pq+8\sigma^3(q^2+pr)\\
&=16\sigma p^2+40\sigma^2pq+8\sigma^3(q^2+pr).
\end{aligned}
$$

Therefore

$$
\begin{aligned}
2\sigma\mathcal A'-b\mathcal B'
={}&(4-16b)\sigma p^2+(24-40b)\sigma^2pq\\
&+8(1-b)\sigma^3(q^2+pr)
-2g\sigma\frac r{p^2}
+4g\sigma\frac{q^2}{p^3}.
\end{aligned}
$$

Multiply by $-p^3/(2\sigma)$. Define the resulting polynomial residual as $\mathcal R_3$:

$$
\boxed{
\begin{aligned}
\mathcal R_3={}&
p\left[g+4(b-1)\sigma^2p^3\right]r\\
&+\left[4(b-1)\sigma^2p^3-2g\right]q^2\\
&+(20b-12)\sigma p^4q+(8b-2)p^5=0.
\end{aligned}
}
\tag{R3}
$$

The precise residual identity is

$$
\boxed{
\left.\Delta_3\right|_{\phi=F(st^2)}
=-\frac{2\sigma}{tp^3}\,\mathcal R_3.
}
\tag{9.2}
$$

The multiplier is nonzero on our chart. Thus satisfying (R3) is equivalent to satisfying the substituted PDE there.

Keeping this multiplier records exactly why the reduction is valid. Merely displaying a plausible ODE would not establish that equivalence.

## 10. First ODE order reduction by vertical translation

Appendix C.9–C.13 distinguishes invariant graphs from quotienting a solution family and derives the passage from point-space pushforward to jet-space prolongation and descent.

### 10.1 Translation invariants and the slope equation

Equation (R3) contains $F',F'',F'''$, but no undifferentiated $F$. Hence adding any constant to a profile leaves the equation unchanged:

$$
F(\sigma)\longmapsto F(\sigma)+\epsilon.
$$

The generator is $Z=\partial_F$, inherited from $X_3=\partial_\phi$.

The derivative $F'$ is unchanged under this translation. Use it as the new unknown:

$$
\mu(\sigma):=F'(\sigma),\qquad
\mu'=F'',\qquad \mu''=F'''.
$$

Then (R3) becomes the second-order equation

$$
\boxed{
\begin{aligned}
\mathcal R_2={}&
\mu\left[g+4(b-1)\sigma^2\mu^3\right]\mu''\\
&+\left[4(b-1)\sigma^2\mu^3-2g\right](\mu')^2\\
&+(20b-12)\sigma\mu^4\mu'
+(8b-2)\mu^5=0.
\end{aligned}
}
\tag{R2}
$$

We have removed the arbitrary additive level of $F$, rather than imposed another condition on a profile. It returns through

$$
F(\sigma)=F_0+\int_{\sigma_0}^{\sigma}\mu(u)\,du.
\tag{10.1}
$$

### 10.2 Quotient reduction versus invariant-graph selection

For $Z=\partial_F$, its ODE characteristic is

$$
Q_Z=1-0\cdot F'=1.
$$

Thus no graph $F=F(\sigma)$ is invariant under pure vertical translation. Nevertheless, the ODE is translation invariant, and its order can be lowered using $\mu=F'$.

The distinction is:

| Task | What we do |
|---|---|
| Select an invariant solution graph | Impose its characteristic $Q=0$. |
| Reduce an ODE by a symmetry | Describe solution curves through differential invariants and reconstruct afterwards. |

One can separately seek invariant solutions of an ODE when they exist. That is a different task from obtaining its general local order reduction.

### 10.3 Find the scaling that survives the first reduction

Section 5.9 used the normalizer of $\operatorname{span}\{X_5\}$ to identify the inherited directions systematically. We now compute the induced scaling and its derivative action explicitly.

The PDE generator

$$
X_4=t\partial_t+s\partial_s+\phi\partial_\phi
$$

commutes with $X_5$:

$$
[X_4,X_5]=0.
$$

Commuting flows carry $X_5$ orbits to $X_5$ orbits, so $X_4$ acts consistently on the invariant coordinates. Compute

$$
X_4(\sigma)
=t(2st)+s(t^2)=3\sigma,\qquad
X_4(w)=w.
$$

It also has $X_4(y)=1$. After quotienting out the $y$ direction, the action on $(\sigma,F)$ is

$$
Y=3\sigma\partial_\sigma+F\partial_F.
\tag{10.2}
$$

This calculation is a *pushforward*: apply the old vector field to each new coordinate to obtain its new components.

For the derivative $\mu=F'$, the prolongation recurrence gives

$$
\eta_Y^{[\sigma]}
=D_\sigma(F)-F'D_\sigma(3\sigma)
=\mu-3\mu=-2\mu.
$$

Thus the induced generator on $(\sigma,\mu)$ is

$$
\boxed{Y_1=3\sigma\partial_\sigma-2\mu\partial_\mu.}
\tag{10.3}
$$

This also follows from weights: under $\bar\sigma=e^{3\epsilon}\sigma$ and $\bar F=e^\epsilon F$, the derivative transforms as $\bar\mu=e^{-2\epsilon}\mu$.

For completeness, $[Y,Z]=-Z$. This means that the scaling preserves the translation direction used in the first ODE quotient, so it descends to the $\mu$ equation.

As a direct check, the weights of $p,q,r$ under $Y$ are $-2,-5,-8$. Every term of (R3) has weight $-10$, so

$$
\operatorname{pr}^{(3)}Y(\mathcal R_3)=-10\mathcal R_3.
$$

## 11. Second ODE order reduction by differential invariants

Appendix C.14–C.16 expands the derivative transformations and the separate invertibility condition $d\Sigma/d\sigma\ne0$.

### 11.1 Prolong the inherited scaling once

The coefficient of $\partial_{\mu'}$ is

$$
D_\sigma(-2\mu)-\mu'D_\sigma(3\sigma)
=-2\mu'-3\mu'=-5\mu'.
$$

Hence

$$
\operatorname{pr}^{(1)}Y_1
=3\sigma\partial_\sigma-2\mu\partial_\mu-5\mu'\partial_{\mu'}.
\tag{11.1}
$$

We need quantities unchanged by this vector field.

### 11.2 Solve for the differential invariants

Its characteristic equations are

$$
\frac{d\sigma}{3\sigma}
=\frac{d\mu}{-2\mu}
=\frac{d\mu'}{-5\mu'}.
$$

The first pair gives

$$
\frac{d\mu}{\mu}=-\frac23\frac{d\sigma}{\sigma},
\qquad
\log\mu+\frac23\log\sigma=\text{constant}.
$$

Therefore one invariant is

$$
\boxed{\Sigma=\sigma^{2/3}\mu.}
$$

The first and third ratios similarly give the second invariant

$$
\boxed{M=\sigma^{5/3}\mu'.}
\tag{11.2}
$$

The logarithmic calculation for $\mu'$ is only an intermediate way to find the expression on a nonzero-sign patch. The formula for $M$ itself extends to $\mu'=0$. Indeed, direct differentiation verifies

$$
\operatorname{pr}^{(1)}Y_1(\Sigma)=0,\qquad
\operatorname{pr}^{(1)}Y_1(M)=0
$$

without dividing by $\mu'$.

These are *differential invariants*: functions involving derivative coordinates that remain unchanged under the prolonged symmetry.

### 11.3 Coordinate independence and invertibility along a solution

First, coordinate independence is checked at fixed $\sigma$:

$$
\det\frac{\partial(\Sigma,M)}{\partial(\mu,\mu')}
=\sigma^{2/3}\sigma^{5/3}
=\sigma^{7/3}\ne0.
$$

Add the orbit coordinate $z=\frac13\log\sigma$. A complete first-jet coordinate chart is

$$
\sigma=e^{3z},\qquad
\mu=e^{-2z}\Sigma,\qquad
\mu'=e^{-5z}M.
$$

Second, use of $\Sigma$ as an independent variable along a particular solution requires its derivative to be nonzero:

$$
\begin{aligned}
\frac{d\Sigma}{d\sigma}
&=\frac23\sigma^{-1/3}\mu+\sigma^{2/3}\mu'\\
&=\frac1\sigma\left(\frac23\Sigma+M\right).
\end{aligned}
$$

Set

$$
W:=M+\frac23\Sigma.
$$

Then

$$
\boxed{\frac{d\Sigma}{d\sigma}=\frac W\sigma.}
\tag{11.3}
$$

We may write $M=M(\Sigma)$ locally only where $W\ne0$. Independence of the coordinate invariants alone does not imply this additional condition.

### 11.4 Derive the second-derivative substitution carefully

The first two substitutions are just (11.2) solved for the old variables:

$$
\mu=\sigma^{-2/3}\Sigma,\qquad
\mu'=\sigma^{-5/3}M.
$$

To obtain $\mu''$, remember that $M$ now depends on $\Sigma$, which depends on $\sigma$:

$$
\begin{aligned}
\mu''
&=\frac d{d\sigma}\left(\sigma^{-5/3}M(\Sigma(\sigma))\right)\\
&=-\frac53\sigma^{-8/3}M
+\sigma^{-5/3}M_\Sigma\frac{d\Sigma}{d\sigma}\\
&=\sigma^{-8/3}\left(WM_\Sigma-\frac53M\right).
\end{aligned}
$$

Thus

$$
\boxed{
\mu=\sigma^{-2/3}\Sigma,\quad
\mu'=\sigma^{-5/3}M,\quad
\mu''=\sigma^{-8/3}
\left[\left(M+\frac23\Sigma\right)M_\Sigma-\frac53M\right].
}
\tag{11.4}
$$

Here $\mu',\mu''$ are derivatives with respect to $\sigma$, while $M_\Sigma=dM/d\Sigma$. Confusing these derivative variables would change the equation.

## 12. First-order rational equation in the original invariant $M$

### 12.1 Substitute each term and factor out the common scale

Define four coefficient functions:

$$
\begin{aligned}
D(\Sigma)&=g+4(b-1)\Sigma^3,\\
A(\Sigma)&=4(b-1)\Sigma^3-2g,\\
B(\Sigma)&=\frac{\Sigma}{3}\left[8(5b-2)\Sigma^3-5g\right],\\
C(\Sigma)&=2(4b-1)\Sigma^5.
\end{aligned}
\tag{12.1}
$$

The capital $D(\Sigma)$ is a coefficient function; $D_t,D_s$ are total derivative operators.

Since $\sigma^2\mu^3=\Sigma^3$, each term of (R2) has the same factor:

| Term of (R2) | After substituting (11.4) |
|---|---|
| $\mu[g+4(b-1)\sigma^2\mu^3]\mu''$ | $\sigma^{-10/3}\Sigma D(WM_\Sigma-\frac53M)$ |
| $[4(b-1)\sigma^2\mu^3-2g](\mu')^2$ | $\sigma^{-10/3}AM^2$ |
| $(20b-12)\sigma\mu^4\mu'$ | $\sigma^{-10/3}(20b-12)\Sigma^4M$ |
| $(8b-2)\mu^5$ | $\sigma^{-10/3}(8b-2)\Sigma^5$ |

Cancel the nonzero factor $\sigma^{-10/3}$:

$$
0=\Sigma D\left(WM_\Sigma-\frac53M\right)
+AM^2+(20b-12)\Sigma^4M+(8b-2)\Sigma^5.
\tag{12.2}
$$

### 12.2 Collect the coefficient of $M$

The linear terms combine as

$$
\begin{aligned}
-\frac53\Sigma DM+(20b-12)\Sigma^4M
&=\frac{\Sigma M}{3}
\left[-5g+\big(-20(b-1)+60b-36\big)\Sigma^3\right]\\
&=\frac{\Sigma M}{3}
\left[-5g+8(5b-2)\Sigma^3\right]\\
&=BM.
\end{aligned}
$$

Also $(8b-2)\Sigma^5=C$. Hence

$$
\boxed{
\Sigma D\left(M+\frac23\Sigma\right)M_\Sigma
+AM^2+BM+C=0.
}
\tag{I1}
$$

This is the first-order equation produced by exactly the invariants $\Sigma=\sigma^{2/3}\mu$ and $M=\sigma^{5/3}\mu'$.

Where $\Sigma DW\ne0$, solve for the derivative:

$$
\boxed{
M_\Sigma
=-\frac{AM^2+BM+C}
{\Sigma D\left(M+\frac23\Sigma\right)}.
}
\tag{12.3}
$$

The right-hand side is rational in $M$, with a linear factor in its denominator. It is not yet the polynomial cubic displayed in Equation (27).

Keep (I1) as well as (12.3). The implicit form retains compatibility information at points where a denominator vanishes.

## 13. Reciprocal shift and the cubic coefficients of Equation (27)

Appendix C.17 repeats the term-by-term reciprocal substitution; C.18 records reconstruction and excluded branches.

### 13.1 Motivation, definition, and domain of the reciprocal shift

The denominator in (12.3) contains $W=M+\frac23\Sigma$. Replacing that expression by a reciprocal turns the rational equation into a polynomial one.

Define

$$
\boxed{
N(\Sigma)=\frac1{M+\frac23\Sigma},
\qquad
M=\frac1N-\frac23\Sigma.
}
\tag{13.1}
$$

On this chart $W\ne0$, so $N$ is finite and nonzero for finite old variables.

Differentiate the inverse relation:

$$
M_\Sigma=-\frac{N_\Sigma}{N^2}-\frac23.
\tag{13.2}
$$

The term $-\frac23$ comes from differentiating the shift. Omitting it would give the wrong quadratic coefficient.

### 13.2 Substitute, multiply, and collect every power

Insert (13.1)–(13.2) into (I1):

$$
\frac{\Sigma D}{N}
\left(-\frac{N_\Sigma}{N^2}-\frac23\right)
+A\left(\frac1N-\frac23\Sigma\right)^2
+B\left(\frac1N-\frac23\Sigma\right)+C=0.
$$

Expand:

$$
\begin{aligned}
0={}&-\frac{\Sigma D}{N^3}N_\Sigma
-\frac{2\Sigma D}{3N}
+\frac A{N^2}-\frac{4A\Sigma}{3N}
+\frac49A\Sigma^2\\
&+\frac BN-\frac23B\Sigma+C.
\end{aligned}
$$

Multiply by $N^3/(\Sigma D)$, valid where $\Sigma DN\ne0$:

$$
\begin{aligned}
0={}&-N_\Sigma
+\frac A{\Sigma D}N\\
&+\left(-\frac23-\frac{4A}{3D}+\frac B{\Sigma D}\right)N^2\\
&+\left(\frac{4\Sigma A}{9D}-\frac{2B}{3D}
+\frac C{\Sigma D}\right)N^3.
\end{aligned}
\tag{13.3}
$$

Therefore

$$
\boxed{
N_\Sigma=a_3(\Sigma)N^3+a_2(\Sigma)N^2+a_1(\Sigma)N.
}
\tag{A27}
$$

### 13.3 Simplify the three coefficients

The linear coefficient is immediate:

$$
a_1=\frac A{\Sigma D}
=\frac{2[2(b-1)\Sigma^3-g]}{\Sigma D}.
$$

For the quadratic coefficient, use a common denominator:

$$
\begin{aligned}
a_2
&=\frac{-2D-4A+3B/\Sigma}{3D}\\
&=\frac{
-2[g+4(b-1)\Sigma^3]
-4[4(b-1)\Sigma^3-2g]
+[8(5b-2)\Sigma^3-5g]
}{3D}\\
&=\frac{g+8(1+2b)\Sigma^3}{3D}.
\end{aligned}
$$

For the cubic coefficient,

$$
a_3=\frac{4\Sigma^2A-6\Sigma B+9C}{9\Sigma D}.
$$

Its numerator is

$$
\begin{aligned}
4\Sigma^2A-6\Sigma B+9C
={}&[16(b-1)-16(5b-2)+18(4b-1)]\Sigma^5\\
&+(-8+10)g\Sigma^2\\
={}&2(4b-1)\Sigma^5+2g\Sigma^2.
\end{aligned}
$$

Thus

$$
\boxed{
\begin{aligned}
a_3(\Sigma)&=\frac{2\Sigma[g+(4b-1)\Sigma^3]}{9D(\Sigma)},\\
a_2(\Sigma)&=\frac{g+8(1+2b)\Sigma^3}{3D(\Sigma)},\\
a_1(\Sigma)&=\frac{2[2(b-1)\Sigma^3-g]}{\Sigma D(\Sigma)},\\
D(\Sigma)&=g+4(b-1)\Sigma^3.
\end{aligned}
}
\tag{13.4}
$$

Finally restore $b=g\beta$:

$$
\boxed{
\begin{aligned}
\frac{dN}{d\Sigma}
={}&
\frac{2\Sigma[g+(4\beta g-1)\Sigma^3]}
{9[g+4(\beta g-1)\Sigma^3]}N^3\\
&+\frac{g+8(1+2\beta g)\Sigma^3}
{3[g+4(\beta g-1)\Sigma^3]}N^2\\
&+\frac{2[2(\beta g-1)\Sigma^3-g]}
{\Sigma[g+4(\beta g-1)\Sigma^3]}N.
\end{aligned}
}
\tag{27*}
$$

These are the displayed coefficients of the paper's Equation (27). To obtain them from the corrected PDE reduction, its Abel dependent variable must be interpreted as

$$
N=\left(\sigma^{5/3}\mu'
+\frac23\sigma^{2/3}\mu\right)^{-1}.
$$

It cannot simultaneously mean only $M=\sigma^{5/3}\mu'$. A renaming of $N$ to $M$ is harmless only if this definition is also changed.

Equation (A27) is an **Abel equation of the first kind**: a first-order ODE polynomial of degree at most three in the dependent variable. Identifying that form does not by itself supply an elementary general solution. The reduction gives a lower-order problem, local series, special exact families, and a reconstruction procedure.

## 14. Local reconstruction from an Abel solution

A solution $N(\Sigma)$ determines the scalar field after reconstruction of $\sigma$, the profile $F$, and the composition $\phi(t,s)$.

Suppose $N(\Sigma)$ solves (A27) on a local interval where

$$
\Sigma>0,\qquad D(\Sigma)\ne0,\qquad
0<|N(\Sigma)|<\infty.
\tag{14.1}
$$

Choose an anchor $\Sigma_0$ in that interval, a positive number $\sigma_0$, and a real number $F_0$.

### 14.1 Recover the old independent variable

From (11.3) and $W=1/N$,

$$
\frac{d\Sigma}{d\sigma}=\frac1{\sigma N}.
$$

Invert:

$$
\frac{d\sigma}{d\Sigma}=\sigma N,\qquad
\frac{d\log\sigma}{d\Sigma}=N.
$$

Integrating gives

$$
\boxed{
\sigma(\Sigma)=\sigma_0
\exp\left(\int_{\Sigma_0}^{\Sigma}N(u)\,du\right).
}
\tag{14.2}
$$

This is a quadrature: recovering a quantity by a definite integral once the integrand is known.

### 14.2 Recover $\mu$ and $F$

By definition,

$$
\mu(\Sigma)=\Sigma\,\sigma(\Sigma)^{-2/3}.
$$

The profile derivative is $dF/d\sigma=\mu$, so

$$
\begin{aligned}
\frac{dF}{d\Sigma}
&=\frac{dF}{d\sigma}\frac{d\sigma}{d\Sigma}\\
&=\left(\Sigma\sigma^{-2/3}\right)(\sigma N)\\
&=\Sigma\sigma^{1/3}N.
\end{aligned}
$$

Therefore

$$
\boxed{
F(\Sigma)=F_0+
\int_{\Sigma_0}^{\Sigma}
u\,\sigma(u)^{1/3}N(u)\,du.
}
\tag{14.3}
$$

In (14.3), $F(\Sigma)$ abbreviates the parametrized profile $F(\sigma(\Sigma))$.

As a useful check, differentiate $\mu=\Sigma\sigma^{-2/3}$:

$$
\begin{aligned}
\frac{d\mu}{d\Sigma}
&=\sigma^{-2/3}\left(1-\frac23\Sigma N\right),\\
\frac{d\mu}{d\sigma}
&=\frac{\sigma^{-2/3}(1-\frac23\Sigma N)}{\sigma N}\\
&=\sigma^{-5/3}\left(\frac1N-\frac23\Sigma\right)
=\sigma^{-5/3}M.
\end{aligned}
$$

This recovers the defining relation for $M$.

### 14.3 Return to $(t,s)$

Because $d\sigma/d\Sigma=\sigma N\ne0$, invert (14.2) locally to obtain $\Sigma=\Sigma(\sigma)$. Substitute it into (14.3), obtaining $F=F(\sigma)$.

The field is then

$$
\boxed{\phi(t,s)=F(st^2).}
$$

Equations (14.2)–(14.3) also give an exact parametric representation of the profile even when the inversion is not elementary.

### 14.4 Reconstruction constants and compatible data

For a fixed reference value $\Sigma_0$, regular local profiles are described by:

| Constant | Where it enters |
|---|---|
| $N_0=N(\Sigma_0)$ | Initial value for the first-order Abel equation. |
| $\sigma_0>0$ | Integration constant in (14.2). |
| $F_0$ | Integration constant in (14.3). |

These are the three local constants expected for a regular third-order profile ODE. The fixed reference $\Sigma_0$ is an anchoring choice, not an additional fourth profile constant.

This statement concerns the similarity family, not the general solution space of the original PDE.

For example, data at $t=t_0>0$ must satisfy

$$
\phi(t_0,s)=F(st_0^2),\qquad
\phi_t(t_0,s)=2st_0F'(st_0^2).
$$

The field and its time derivative are linked. They cannot be prescribed independently without checking this compatibility.

## 15. Excluded branches and degenerate coordinate charts

A change of coordinates may fail even when a genuine solution remains regular. We therefore return to the undivided equation before discarding a case.

### 15.1 An entire branch with $W=0$

If $W=0$ throughout an interval, (11.3) says that $\Sigma$ is constant. Write

$$
\Sigma=\mu_0>0.
$$

Then

$$
\mu=\mu_0\sigma^{-2/3},\qquad
\mu'=-\frac23\mu_0\sigma^{-5/3},\qquad
\mu''=\frac{10}{9}\mu_0\sigma^{-8/3}.
$$

The corresponding $M$ is $-\frac23\mu_0$, so $W=M+\frac23\Sigma=0$ as required.

Substitute these expressions into (R2), **before** dividing by $W$. The residual simplifies to

$$
\mathcal R_2
=\frac{2\mu_0^2}{9\sigma^{10/3}}
\left[g+(4b-1)\mu_0^3\right].
\tag{15.1}
$$

The four terms of (R2), after removing their common factor $\sigma^{-10/3}$, give

$$
\begin{aligned}
\sigma^{10/3}\mathcal R_2
={}&\frac{10}{9}\mu_0^2[g+4(b-1)\mu_0^3]\\
&+\frac49\mu_0^2[4(b-1)\mu_0^3-2g]\\
&-\frac23(20b-12)\mu_0^5+(8b-2)\mu_0^5\\
={}&\left(\frac{10}{9}-\frac89\right)g\mu_0^2\\
&+\frac{56(b-1)-6(20b-12)+9(8b-2)}9\mu_0^5\\
={}&\frac29g\mu_0^2+\frac{8b-2}9\mu_0^5\\
={}&\frac{2\mu_0^2}9[g+(4b-1)\mu_0^3].
\end{aligned}
$$


It vanishes when

$$
\boxed{
\mu_0^3=\frac{g}{1-4b},\qquad 0<b<\frac14.
}
\tag{15.2}
$$

Integrate $\mu=F'$:

$$
F(\sigma)=F_0+3\mu_0\sigma^{1/3}.
$$

Thus an exact positive family is

$$
\boxed{
\phi(t,s)=F_0+
3\left(\frac{g}{1-4g\beta}\right)^{1/3}(st^2)^{1/3},
\qquad 0<g\beta<\frac14.
}
\tag{15.3}
$$

This family is outside the reciprocal chart because $N=1/W$ is undefined there. The original PDE reduction still verifies it.

An isolated zero of $W$ is a different situation. It makes $\Sigma$ unsuitable as a local independent variable at that point; it does not, by itself, make the original profile invalid.

### 15.2 An affine exact family when $b=\frac14$

Consider the affine profile

$$
F(\sigma)=F_0+C_1\sigma,\qquad C_1>0.
$$

Then $p=C_1$, $q=r=0$, and

$$
\mathcal R_3=(8b-2)C_1^5.
$$

Consequently every such affine profile solves the equation when $b=\frac14$:

$$
\boxed{
\phi(t,s)=F_0+C_1st^2,\qquad
g\beta=\frac14,\quad C_1>0.
}
\tag{15.4}
$$

Here $\mu=C_1$, $M=0$, and

$$
\Sigma=C_1\sigma^{2/3},\qquad
N=\frac{3}{2\Sigma}.
$$

This $N$ solves (A27) wherever its coefficient denominator $D$ is nonzero. The direct affine profile remains meaningful at a point where the Abel normal form becomes undefined.

### 15.3 Other chart boundaries

| Condition | Meaning | What to check |
|---|---|---|
| $\phi_s=0$ | A denominator in the original PDE vanishes. | Outside the present classical PDE chart. |
| $\Sigma=0$ | Incompatible with $\sigma>0,\mu>0$. | Requires another sign or boundary chart. |
| $W=0$ at an isolated point | $d\Sigma/d\sigma=0$. | Continue in $\sigma$ if the profile equation permits; do not force $M(\Sigma)$. |
| $W=0$ on an interval | Constant-$\Sigma$ branch. | Use (15.1)–(15.3). |
| $D=0$ | The highest-derivative coefficient of (R2) vanishes. | Use the undivided equation and its compatibility conditions. |
| $N=0$ | A formal solution of the cubic Abel equation. | No finite $M=1/N-\frac23\Sigma$ exists in this reciprocal chart. |

For $0<b<1$, the positive zero of $D$ is

$$
\Sigma_D=\left(\frac{g}{4(1-b)}\right)^{1/3}.
$$

At that value, a finite jet must at least satisfy

$$
AM^2+BM+C=0.
\tag{15.5}
$$

Using $D=0$ to eliminate $b$, this condition is

$$
-3gM^2+(8\Sigma^4-5g\Sigma)M
+6\Sigma^5-2g\Sigma^2=0.
$$

It is a necessary algebraic compatibility condition. It does not alone prove that a smooth solution continues through the degenerate point.

A singular expression or an unbounded derivative also does not establish a weak shock solution. Such a claim requires an appropriate weak formulation and jump calculation.

## 16. Worked regular initial-value example and local series

### 16.1 Choose regular initial data

Take normalized constants and profile data

$$
g=1,\qquad \beta=\frac18,\qquad b=\frac18,
$$

$$
\sigma_0=1,\qquad F(1)=2,\qquad
F'(1)=1,\qquad F''(1)=0.
\tag{16.1}
$$

Thus $p_0=1$ and $q_0=0$. The coefficient of $r=F'''$ in (R3) is

$$
p_0\left[g+4(b-1)\sigma_0^2p_0^3\right]
=1+4\left(-\frac78\right)
=-\frac52\ne0.
$$

The ODE can therefore be solved for $F'''$ near these data. Its right-hand side is analytic there, so there is a unique local analytic profile.

### 16.2 Compute $F'''(1)$ directly

At the initial point, the terms involving $q$ vanish. Equation (R3) gives

$$
-\frac52r+(8b-2)=0
\quad\Longrightarrow\quad
-\frac52r-1=0.
$$

Hence

$$
\boxed{F'''(1)=-\frac25.}
$$

### 16.3 Differentiate the equation to compute $F^{(4)}(1)$

View $\mathcal R_3=\mathcal R_3(\sigma,p,q,r)$ and use

$$
p'=q,\qquad q'=r,\qquad r'=F^{(4)}.
$$

Along the solution,

$$
0=\frac{d\mathcal R_3}{d\sigma}
=\mathcal R_{3,\sigma}
+q\mathcal R_{3,p}
+r\mathcal R_{3,q}
+F^{(4)}\mathcal R_{3,r}.
\tag{16.2}
$$

The residual partial derivatives entering (16.2) are explicitly

$$
\begin{aligned}
\mathcal R_{3,\sigma}
&=8(b-1)\sigma p^4r+8(b-1)\sigma p^3q^2+(20b-12)p^4q,\\
\mathcal R_{3,p}
&=[g+16(b-1)\sigma^2p^3]r+12(b-1)\sigma^2p^2q^2\\
&\quad+4(20b-12)\sigma p^3q+5(8b-2)p^4,\\
\mathcal R_{3,q}
&=2[4(b-1)\sigma^2p^3-2g]q+(20b-12)\sigma p^4,\\
\mathcal R_{3,r}
&=p[g+4(b-1)\sigma^2p^3].
\end{aligned}
$$


At the initial jet, the required partial derivatives are

$$
\mathcal R_{3,\sigma}=\frac{14}{5},\qquad
\mathcal R_{3,q}=-\frac{19}{2},\qquad
\mathcal R_{3,r}=-\frac52,
$$

and $q=0$. Therefore

$$
0=\frac{14}{5}
+\left(-\frac25\right)\left(-\frac{19}{2}\right)
-\frac52F^{(4)}(1)
=\frac{33}{5}-\frac52F^{(4)}(1).
$$

Thus

$$
\boxed{F^{(4)}(1)=\frac{66}{25}.}
$$

### 16.4 Write the Taylor solution

For $x=\sigma-1$,

$$
\begin{aligned}
F(1+x)
&=F(1)+F'(1)x+\frac{F''(1)}{2!}x^2
+\frac{F'''(1)}{3!}x^3+\frac{F^{(4)}(1)}{4!}x^4+O(x^5)\\
&=\boxed{2+x-\frac{x^3}{15}+\frac{11x^4}{100}+O(x^5).}
\end{aligned}
\tag{16.3}
$$

The corresponding field has the local representation

$$
\phi(t,s)
=2+(st^2-1)-\frac{(st^2-1)^3}{15}
+\frac{11(st^2-1)^4}{100}
+O\big((st^2-1)^5\big).
$$

This is an expansion near $\sigma=st^2=1$, with $t,s>0$. The finite polynomial is a truncation of the local solution, rather than an exact global solution.

Higher coefficients can be obtained successively by differentiating (16.2) again, or by substituting a power series into (R3) and equating powers of $x$.

### 16.5 Convert the same initial jet to Abel data

Definitions (11.2) give

$$
\Sigma_0=1,\qquad M_0=0,\qquad
W_0=\frac23,\qquad N_0=\frac32.
$$

At $\Sigma=1$, the coefficients (13.4) are

$$
a_3=-\frac{2}{45},\qquad
a_2=-\frac{22}{15},\qquad
a_1=\frac{11}{5}.
$$

Hence

$$
\begin{aligned}
N_\Sigma(1)
&=-\frac{2}{45}\left(\frac32\right)^3
-\frac{22}{15}\left(\frac32\right)^2
+\frac{11}{5}\left(\frac32\right)\\
&=-\frac3{20}-\frac{33}{10}+\frac{33}{10}
=\boxed{-\frac3{20}}.
\end{aligned}
$$

This is also a concrete check that $M$ and $N$ cannot be conflated. From (11.4), the same initial data give

$$
M_\Sigma(1)=\frac{\mu''(1)}{W_0}
=\frac{-2/5}{2/3}=-\frac35.
$$

The relation

$$
N_\Sigma=-N^2\left(M_\Sigma+\frac23\right)
$$

turns $-\frac35$ into $-\frac3{20}$, exactly as required.

For one more Abel series coefficient, write the right-hand side of (A27) as $f(\Sigma,N)$. Then

$$
N_{\Sigma\Sigma}=f_{,\Sigma}+f_{,N}f.
$$

To calculate the derivative without suppressing the rational differentiation, put

$$
\begin{aligned}
U_3&=2\Sigma[g+(4b-1)\Sigma^3],&
U_3'&=2g+8(4b-1)\Sigma^3,\\
U_2&=g+8(1+2b)\Sigma^3,&
U_2'&=24(1+2b)\Sigma^2,\\
U_1&=4(b-1)\Sigma^3-2g,&
U_1'&=12(b-1)\Sigma^2,\\
D&=g+4(b-1)\Sigma^3,&D'&=12(b-1)\Sigma^2.
\end{aligned}
$$

Primes in these displayed coefficient formulas mean $d/d\Sigma$. The quotient rule gives

$$
\begin{aligned}
a_3'&=\frac{U_3'D-U_3D'}{9D^2},\\
a_2'&=\frac{U_2'D-U_2D'}{3D^2},\\
a_1'&=\frac{U_1'\Sigma D-U_1(D+\Sigma D')}{(\Sigma D)^2}.
\end{aligned}
$$

At $\Sigma=1$, $g=1$, $b=1/8$, the intermediate values are

$$
\begin{gathered}
D=-5/2,\quad D'=-21/2,\quad
U_3=1,\quad U_3'=-2,\\
U_2=11,\quad U_2'=30,\quad
U_1=-11/2,\quad U_1'=-21/2.
\end{gathered}
$$

Therefore

$$
\begin{aligned}
a_3'(1)&=\frac{(-2)(-5/2)-(1)(-21/2)}{9(25/4)}
=\frac{62}{225},\\
a_2'(1)&=\frac{30(-5/2)-11(-21/2)}{3(25/4)}
=\frac{54}{25},\\
a_1'(1)&=\frac{(-21/2)(-5/2)-(-11/2)(-5/2-21/2)}{25/4}
=-\frac{181}{25}.
\end{aligned}
$$

For $f(\Sigma,N)=a_3N^3+a_2N^2+a_1N$,

$$
\begin{aligned}
f_{,\Sigma}
&=a_3'N^3+a_2'N^2+a_1'N\\
&=\frac{62}{225}\frac{27}{8}
+\frac{54}{25}\frac94-\frac{181}{25}\frac32\\
&=\frac{93}{100}+\frac{486}{100}-\frac{1086}{100}
=-\frac{507}{100},\\
f_{,N}
&=3a_3N^2+2a_2N+a_1\\
&=3\left(-\frac2{45}\right)\frac94
+2\left(-\frac{22}{15}\right)\frac32+\frac{11}5\\
&=-\frac3{10}-\frac{22}5+\frac{11}5=-\frac52.
\end{aligned}
$$


At the initial point,

$$
f_{,\Sigma}=-\frac{507}{100},\qquad
f_{,N}=-\frac52,\qquad
f=-\frac3{20},
$$

so

$$
N_{\Sigma\Sigma}(1)
=-\frac{507}{100}+\frac38
=-\frac{939}{200}.
$$

With $h=\Sigma-1$, the Abel solution begins

$$
\boxed{
N(1+h)=\frac32-\frac3{20}h-\frac{939}{400}h^2+O(h^3).
}
\tag{16.4}
$$

### 16.6 Check the PDE jet and the reconstruction independently

At $(t,s)=(1,1)$, the derivative table gives

$$
\phi=2,\quad \phi_s=1,\quad \phi_t=2,\quad
\phi_{tt}=2,\quad\phi_{ts}=2,\quad\phi_{ss}=0.
$$

It also gives

$$
T=\phi_{ttt}=-\frac{16}{5},\qquad
R=\phi_{tss}=-\frac45.
$$

Insert these values into (2.2):

$$
\begin{aligned}
\Delta_3
&=-\frac{16}{5}+4
-\left(1+\frac18\cdot4\right)\left(-\frac45\right)
-2\cdot\frac18\cdot2\cdot 2^2\\
&=-\frac{16}{5}+4+\frac65-2=0.
\end{aligned}
$$

This checks the starting PDE, not just the final Abel equation.

A second check integrates two different systems:

1. The original profile equation, as $F'=p$, $p'=q$, $q'=r(\sigma,p,q)$ obtained from (R3).
2. The Abel equation together with $\sigma_\Sigma=\sigma N$ and $F_\Sigma=\Sigma\sigma^{1/3}N$.

Using DOP853 with relative tolerance $10^{-11}$ and absolute tolerance $10^{-13}$, the maximum differences at 101 comparison points on $1\le\Sigma\le1.05$ were:

| Reconstructed quantity | Maximum absolute difference between the two integrations |
|---|---|
| $F$ | $1.87\times10^{-14}$ |
| $\mu$ | $3.86\times10^{-14}$ |
| $\mu'$ | $1.21\times10^{-13}$ |

The corresponding endpoint in this run is $\sigma\approx1.0775882790$. At the sampled points, $|D|\ge2.5$ and $|N|>1.487$. These numerical agreements support the implementation of the identities; they are not rigorous bounds on the true solution error or a proof of global existence.

## 17. Comparison with the printed literature formulas

The derivation above starts from the paper's scalar Equation (7). It does not assume that the intermediate printed Equations (25)–(26) already follow from it.

### 17.1 A direct test of printed Equation (26)

In the typeset article, $\mu_{,\sigma}\sigma$ means $\sigma\mu'$. The second $\sigma$ is on the baseline and is a multiplier; it is not another derivative index. With that product read explicitly, the printed residual is

$$
\begin{aligned}
\mathcal P_{26}={}&
4\sigma\mu^3\mu'(\sigma\mu'+3\mu)
+2g(\mu')^2\\
&+\beta\sigma\left[
(\sigma\mu'+5\mu)\sigma\mu'
+(2\mu+\sigma^2\mu'')\mu
\right].
\end{aligned}
\tag{17.1}
$$

Use the exact family from Section 15 with

$$
g=\frac12,\qquad \beta=\frac14,\qquad b=\frac18,\qquad \mu_0=1.
$$

At $\sigma=1$,

$$
\mu=1,\qquad \mu'=-\frac23,\qquad \mu''=\frac{10}{9}.
$$

The corrected residual (R2) vanishes, since

$$
g+(4b-1)\mu_0^3=\frac12-\frac12=0.
$$

But the three terms in (17.1) give

$$
\mathcal P_{26}
=-\frac{56}{9}+\frac49+\frac1{18}
=\boxed{-\frac{103}{18}\ne0}.
$$

This exact counterexample shows that the printed Equation (26) is not the equation obtained from the stated PDE by this reduction.

The alternate value $-1303/162$ in the fuller supplied text results from replacing the baseline products $\sigma\mu'$ by $\mu''$. The value above follows the typeset v3 formula, checked visually. These are different residuals, so their exact values must not be conflated.

Replacing $(\mu,\mu',\mu'')$ by $(F',F'',F''')$ gives the same test of printed Equation (25), using $F=F_0+3\sigma^{1/3}$.

### 17.2 The repairs needed along this route

| Location in the printed route | Formula justified by the calculation |
|---|---|
| Similarity profile equation (25) | Use (R3), derived with residual identity (9.2). |
| Scaling after (25) | $3\sigma\partial_\sigma+F\partial_F$; the dependent-variable direction is $\partial_F$. |
| Derivative equation (26) | Use (R2), with $\mu=F'$. |
| Scaling after (26) | $3\sigma\partial_\sigma-2\mu\partial_\mu$; the dependent-variable direction is $\partial_\mu$. |
| Equation (27) | Its cubic coefficients are recovered using $N=(M+\frac23\Sigma)^{-1}$. |

The five PDE symmetry generators agree with the reported basis. Recovering the Abel coefficients specifies a sufficient mathematical repair; it does not establish what unstated calculation the authors intended.

The detailed calculation accompanying the manuscript is used here with the complete prolongation formulas (5.5). In particular, the $-3T_0''a$ term and the full $2H_0''\rho\ell+H_0''vc+H_0'''v\rho^2$ contribution are retained.

### 17.3 Integration record and status of the repaired statements

The fuller supplied text contains substantive additions but also repeats several statements that do not follow from its own formulas. The merged English manuscript retains the additions with the following explicit corrections.

| Item | Established statement | Status and scope |
|---|---|---|
| Eulerian-to-material bed equation | The standard pullback gives (0.7), including the transport term | Exact chain-rule identity; the printed scalar model is retained separately |
| Formal bed elimination | The formal pair (0.6), (0.8) has scalar compatibility $\Delta_m=0$ and reconstruction (0.11) | Local equivalence for this formal pair, up to an additive bed constant |
| General-exponent slope relations | Equations (5.19)–(5.20) give the cubic scaling exception | Exact affine-scaling calculation; the fuller text's second relation has incorrect factors |
| Full point-symmetry classification | The unrestricted determining system gives exactly five parameters at $m=3$ | Proven locally for the stated scalar equation; not a theorem covering every $m$ |
| Endpoint $m=1$ | The additional generator $t\partial_\phi$ is admitted | Exact counterexample to an unqualified four-dimensional classification for all $m\ne3$ |
| Bracket table | $[X_5,X_1]=-X_1$ and $[X_5,X_2]=2X_2$ | Direct computation; corrects Table 1's final row |
| Adjoint Table 2 | Its v3 row $X_2$, column $X_3$ already reads $X_3$ | No repair is supported for that particular entry |
| Optimal-system elimination | Resonances $\alpha=-1,1/2$ and the residual $X_3$ term with $X_5$ must be retained | Complete classification under the connected action specified in Section 5.13 |
| Equations (25)–(26) | The pullback gives (R3), then (R2) | Exact residual identity; the printed formula fails the rational counterexample |
| Counterexample value | The typeset baseline products give $-103/18$ | Exact rational computation; $-1303/162$ refers to a different transcription |
| Equation (27) | The printed cubic coefficient functions follow after $N=(M+\frac23\Sigma)^{-1}$ | A sufficient mathematical repair; the originally defined $M$ satisfies a rational equation |
| Power-law profile | Equation (15.3) is an exact classical solution on its open positive chart | Its boundary singular behavior alone does not prove a weak shock |
| Traveling-wave integrability | Equations (19.3)–(19.10) supply a first integral and local point linearization | Requires $\alpha\ne0$ and, for inversion, $K\ne0$; all three integration constants retained |
| Algebraic closed form | The cubic relation (19.12) holds at $m=3,\gamma=0$ | The general $\gamma\ne0$ quadrature contains a logarithm |

The Lie algebra labels used in classification catalogues are not needed for these arguments. The basis, brackets, adjoint action, and orbit equivalences have been specified directly, avoiding an unverified identification with a catalogue entry.


## 18. Domain correspondence and verification status

### 18.1 Keep the domain conditions attached to each step

| Step | New object | Conditions or information to retain |
|---|---|---|
| Starting scalar PDE | $\Delta_3[\phi]=0$ | Positive chart (D); local classical solutions. |
| Equation-manifold restriction | $T=T_*$ | $\rho=\phi_s\ne0$. |
| Similarity ansatz | $\phi=F(st^2)$ | Select invariant graphs with $Q=0$; $t,s>0$. |
| First order reduction | $\mu=F'$ | Restore the additive constant of $F$. |
| Differential invariants | $\Sigma=\sigma^{2/3}\mu$, $M=\sigma^{5/3}\mu'$ | $\sigma>0$; no requirement that $\mu'\ne0$. |
| New independent variable | $M=M(\Sigma)$ | $W=M+\frac23\Sigma\ne0$. |
| Rational normal form | Equation (12.3) | $\Sigma DW\ne0$. |
| Cubic Abel normal form | $N=1/W$ | $\Sigma D\ne0$ and finite nonzero $N$. |
| Reconstruction | Equations (14.2)–(14.3) | Restore $\sigma_0,F_0$ and invert locally. |
| Excluded branches | Undivided equations | Check $W=0$ and $D=0$ before making conclusions. |

### 18.2 Reproducible calculation protocol

1. **Write the equation first.** Fix whether $\beta$ or $\kappa$ is being used.
2. **Specify the operation.** Distinguish symmetry determination, symmetry verification, invariant-graph selection, and ODE order reduction.
3. **State the differentiation variable.** A prime on $\mu$ is a $\sigma$ derivative; a subscript $\Sigma$ is a $\Sigma$ derivative.
4. **Use the chain rule before simplifying.** In particular, retain explicit powers of $t$ and the factor $d\Sigma/d\sigma$.
5. **Record every division.** Its zero set may contain valid solutions.
6. **Keep the residual multiplier.** Equation (9.2) checks the link back to the original PDE.
7. **Reconstruct.** An ODE for $N$ alone is not yet a field $\phi(t,s)$.
8. **Check a concrete jet or exact family.** The examples in Sections 15–17 expose both notation errors and incorrect intermediate equations.

For this version, exact symbolic algebra checked all 118 unrestricted determining coefficients, the 11 separated coefficients, the affine symmetry identity, both forms of the PDE pullback, the reciprocal substitution, the power branch, the traveling-wave antiderivative, and the rational counterexample. The local series coefficients were also computed from the displayed equations. The numerical comparison in Section 16 is a separate finite consistency check.

These results establish a local symmetry algebra and a local reduction/reconstruction route for the stated scalar model. They do not classify every PDE solution, prove global regularity, or supply a general elementary solution of the Abel equation.

---

## 19. Traveling-wave reductions, first integrals, and local linearization

This section integrates the final topic of the fuller supplied text. It is an additional reduction of the same printed scalar model; it is not a step required to obtain Equation (27).

### 19.1 Motivation, group flow, invariants, and domain

The translation combination

$$
Z_{\alpha,\gamma}=X_1+\alpha X_2+\gamma X_3
=\partial_t+\alpha\partial_s+\gamma\partial_\phi
$$

is admitted by $\Delta_m$ for every exponent on its positive-velocity branch. Its flow is obtained from

$$
\frac{d\bar t}{d\epsilon}=1,\quad
\frac{d\bar s}{d\epsilon}=\alpha,\quad
\frac{d\bar\phi}{d\epsilon}=\gamma,
$$

giving $(\bar t,\bar s,\bar\phi)=(t+\epsilon,s+\alpha\epsilon,\phi+\gamma\epsilon)$. Hence

$$
k=s-\alpha t,\qquad w=\phi-\gamma t
$$

are point invariants: $Z_{\alpha,\gamma}(k)=-\alpha+\alpha=0$ and $Z_{\alpha,\gamma}(w)=\gamma-\gamma=0$. The full coordinate change $(t,s,\phi)\mapsto(y,k,w)=(t,s-\alpha t,\phi-\gamma t)$ has determinant $1$ and inverse

$$
t=y,\qquad s=k+\alpha y,\qquad\phi=w+\gamma y.
$$

The invariant-surface condition is

$$
Q_Z=\gamma-\phi_t-\alpha\phi_s=0.
$$

In the new coordinates this is $w_y=0$. Thus an invariant graph has the form

$$
\phi(t,s)=\gamma t+\Phi(k),\qquad k=s-\alpha t.
\tag{19.1}
$$

Here $\Phi$ is an unknown profile. Define its slope and the material velocity along the ansatz by

$$
\mu(k)=\frac{d\Phi}{dk},\qquad
v_{\mathrm{tw}}(k)=\gamma-\alpha\mu(k).
$$

The local domain requires

$$
\mu>0,\qquad v_{\mathrm{tw}}>0,
$$

and $t,s>0$ when the common positive coordinate chart is retained. This permits real powers $v_{\mathrm{tw}}^{m-1}$ without complex branch choices. For $\gamma=0$, the positive branch requires $\alpha<0$.

### 19.2 Every derivative needed for the pullback

Since $k_t=-\alpha$ and $k_s=1$, the chain rule gives

$$
\begin{aligned}
\phi_t&=\gamma-\alpha\mu,&\phi_s&=\mu,\\
\phi_{tt}&=-\alpha\mu' k_t=\alpha^2\mu',&
\phi_{ts}&=-\alpha\mu',&\phi_{ss}&=\mu',\\
\phi_{ttt}&=\alpha^2\mu'' k_t=-\alpha^3\mu'',&
\phi_{tts}&=\alpha^2\mu'',\\
\phi_{tss}&=-\alpha\mu'',&\phi_{sss}&=\mu''.
\end{aligned}
\tag{19.2}
$$

Primes in this section mean $d/dk$, so $\mu'=\Phi''$ and $\mu''=\Phi'''$. For a function of $k$ alone,

$$
D_t=-\alpha\frac d{dk},\qquad D_s=\frac d{dk}.
$$

These operator formulas apply to the profile expressions; explicit $t$-dependent factors would still require differentiation.

### 19.3 Exact divergence reduction and its first integral

Substitute (19.2) into the two brackets of the scalar equation:

$$
\begin{aligned}
H&=\phi_s\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^2}
=\left(\alpha^2\mu-\frac g{\mu^2}\right)\mu',\\
\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}
&=-\alpha\frac{(\gamma-\alpha\mu)^{m-1}}\mu\mu'.
\end{aligned}
$$

Consequently,

$$
\begin{aligned}
\left.\Delta_m\right|_{\phi=\gamma t+\Phi(k)}
&=-\alpha\frac d{dk}\left[
\left(\alpha^2\mu-\frac g{\mu^2}\right)\mu'\right]
+\alpha g\beta\frac d{dk}\left[
\frac{(\gamma-\alpha\mu)^{m-1}}\mu\mu'\right]\\
&=-\alpha\frac d{dk}\left[K(\mu)\mu'\right],
\end{aligned}
\tag{19.3}
$$

where the coefficient function is defined explicitly as

$$
\boxed{
K(\mu)=\alpha^2\mu-\frac g{\mu^2}
-\frac{g\beta}{\mu}(\gamma-\alpha\mu)^{m-1}.
}
\tag{19.4}
$$

**Local chart restriction.** Assume $\alpha\ne0$ before dividing by the prefactor. Then the second-order slope equation is

$$
\frac d{dk}\left[K(\mu)\mu'\right]=0.
\tag{19.5}
$$

The differentiated coefficient is

$$
\begin{aligned}
K_\mu
&=\alpha^2+\frac{2g}{\mu^3}
-g\beta\frac d{d\mu}\left[\mu^{-1}(\gamma-\alpha\mu)^{m-1}\right]\\
&=\alpha^2+\frac{2g}{\mu^3}
-g\beta\left[-\frac{(\gamma-\alpha\mu)^{m-1}}{\mu^2}
-\frac{\alpha(m-1)}\mu(\gamma-\alpha\mu)^{m-2}\right]\\
&=\alpha^2+\frac{2g}{\mu^3}
+\frac{g\beta}{\mu^2}(\gamma-\alpha\mu)^{m-1}
+\frac{g\beta\alpha(m-1)}\mu(\gamma-\alpha\mu)^{m-2}.
\end{aligned}
$$

Thus (19.5) expands to

$$
K(\mu)\mu''+K_\mu(\mu)(\mu')^2=0.
$$

Its first integral is

$$
\boxed{K(\mu)\mu'=C_1.}
\tag{19.6}
$$

This integral follows from the displayed total derivative. It does not follow solely from the existence of a symmetry generator, and its constant has not been set to $1$.

### 19.4 Point linearization and the meaning of maximal symmetry

**Motivation.** Equation (19.5) is already the second derivative of a single function of $\mu$. This suggests using that function as the new dependent variable.

Fix a reference value $\mu_*>0$ on a patch satisfying $\gamma-\alpha\mu>0$. Define

$$
z=\Psi(\mu),\qquad
\Psi(\mu)=\int_{\mu_*}^{\mu}K(r)\,dr.
\tag{19.7}
$$

This is a point transformation of the slope equation on $(k,\mu)$ space. Its Jacobian is

$$
\det\frac{\partial(k,z)}{\partial(k,\mu)}=\Psi'(\mu)=K(\mu).
$$

It is locally invertible only when $K(\mu)\ne0$. The chain rule then gives

$$
\frac{dz}{dk}=K(\mu)\mu',\qquad
\frac{d^2z}{dk^2}=K(\mu)\mu''+K_\mu(\mu)(\mu')^2=0.
\tag{19.8}
$$

Therefore the regular slope equation is locally point equivalent to the free-particle equation $z''=0$.

The eight independent projective generators of $z''=0$ can be written

$$
\begin{gathered}
\partial_k,\quad\partial_z,\quad
k\partial_k,\quad z\partial_k,\quad
k\partial_z,\quad z\partial_z,\\
k^2\partial_k+kz\partial_z,\qquad
kz\partial_k+z^2\partial_z.
\end{gathered}
$$

They are the infinitesimal projective transformations taking local straight-line graphs to straight-line graphs. The corresponding Lie algebra is $\mathfrak{sl}(3,\mathbb R)$, with the usual local point-symmetry interpretation of a regular scalar second-order ODE [2, Section 5.6]. The inverse transformation pulls these fields back to symmetries of (19.5), with $\partial_z=K^{-1}\partial_\mu$.

Thus maximal symmetry is justified by an explicit invertible linearizing transformation. The presence of two translations by itself would not establish eight-dimensional symmetry. The algebra $\mathfrak{sl}(3,\mathbb R)$ must also be distinguished from the group $\mathrm{SL}(3,\mathbb R)$.

### 19.5 Complete local reconstruction with all constants retained

Integrate $z''=0$:

$$
z(k)=C_1(k-k_0)+C_2.
$$

The reference $k_0$ is fixed; it is not an additional free constant. The slope is determined locally by

$$
\boxed{\Psi(\mu(k))=C_1(k-k_0)+C_2.}
\tag{19.9}
$$

Recover the profile and scalar field by

$$
\Phi(k)=C_3+\int_{k_0}^{k}\mu(r)\,dr,\qquad
\phi(t,s)=\gamma t+\Phi(s-\alpha t).
\tag{19.10}
$$

The constants $C_1,C_2,C_3$ are the three local constants of the regular third-order profile equation. The pair $\alpha,\gamma$ specifies the chosen generator and is fixed during this integration.

When $C_1=0$ and $K\ne0$, (19.9) yields a constant $\mu=\mu_0$. This gives the affine family

$$
\Phi(k)=C_3+\mu_0(k-k_0),\qquad
\phi_s=\mu_0>0,\qquad\phi_t=\gamma-\alpha\mu_0>0.
$$

Setting $C_1=1$ in advance would discard this branch and restrict the nonzero-constant data. A normalization by a coordinate rescaling would require a separate equivalence and data argument.

At $\alpha=0$, (19.1) becomes $\phi=\gamma t+\Phi(s)$. Here $\phi_{tt}=\phi_{ts}=0$, the remaining divergence bracket is independent of $t$, and $\Delta_m=0$ identically. Thus arbitrary $C^3$ profiles with $\Phi'>0$ and $\gamma>0$ solve the scalar equation on the positive chart. Formula (19.5) must not be imposed after division by a zero $\alpha$.

At $K=0$, the linearizing map loses rank. Equation (19.6), or the original undivided pullback (19.3), must be used. No general continuation or uniqueness assertion through that set follows from the regular linearization.

### 19.6 Explicit cubic-exponent quadrature and the limit of an algebraic formula

For $m=3$ and $b=g\beta$, expand the square:

$$
(\gamma-\alpha\mu)^2=\gamma^2-2\alpha\gamma\mu+\alpha^2\mu^2.
$$

Therefore

$$
\begin{aligned}
K(\mu)
&=\alpha^2\mu-\frac g{\mu^2}
-b\left(\frac{\gamma^2}\mu-2\alpha\gamma+\alpha^2\mu\right)\\
&=\alpha^2(1-b)\mu+2b\alpha\gamma
-\frac{b\gamma^2}\mu-\frac g{\mu^2}.
\end{aligned}
$$

An unanchored antiderivative, differing from (19.7) by a constant, is

$$
\Psi_0(\mu)=\frac{\alpha^2(1-b)}2\mu^2
+2b\alpha\gamma\mu-b\gamma^2\log\mu+\frac g\mu.
\tag{19.11}
$$

Each term differentiates to the corresponding term of $K$. For $\gamma\ne0$, a logarithm is present, so this quadrature is not in general an algebraic equation for $\mu$.

For $\gamma=0$, the logarithm and linear term vanish. Absorbing the anchoring constant into $C_2$ gives

$$
\frac{\alpha^2(1-b)}2\mu^2+\frac g\mu
=C_1(k-k_0)+C_2.
$$

Multiplication by $\mu>0$ yields the cubic algebraic relation

$$
\boxed{
\frac{\alpha^2(1-b)}2\mu^3
-\big[C_1(k-k_0)+C_2\big]\mu+g=0.
}
\tag{19.12}
$$

The admissible real root must satisfy $\mu>0$, $-\alpha\mu>0$, and the regularity guard $K\ne0$ where the inverse construction is used. At $b=1$, the cubic term vanishes and the relation reduces to $\mu=g/[C_1(k-k_0)+C_2]$ on a nonzero-denominator patch.

### 19.7 An exact implicit traveling-profile example

Choose

$$
m=3,\quad g=1,\quad\beta=\frac18,\quad
\alpha=-1,\quad\gamma=0,\quad k=s+t.
$$

Take $k_0=2$, $C_1=1/16$, and choose the unanchored constant so that

$$
\frac7{16}\mu^2+\frac1\mu=\frac{k+21}{16}.
$$

Then (19.12) is

$$
7\mu^3-(k+21)\mu+16=0.
\tag{19.13}
$$

At $k=2$, $\mu=1$ is a root. The derivative of its left side with respect to $\mu$ is $21\mu^2-(k+21)=-2\ne0$. The implicit-function theorem therefore gives a unique local analytic branch $\mu(k)$ through $(2,1)$.

Differentiate (19.13):

$$
\big[21\mu^2-(k+21)\big]\mu'-\mu=0,
\qquad \mu'(2)=-\frac12.
$$

The coefficient (19.4) at the initial slope is

$$
K(1)=\frac78-1=-\frac18,
\qquad K(1)\mu'(2)=\frac1{16}=C_1.
$$

Define $\Phi(k)=\int_2^k\mu(r)\,dr$. Then $\phi(t,s)=\Phi(s+t)$ satisfies the scalar PDE exactly on a sufficiently small patch around $(t,s)=(1,1)$, by (19.3). Both $\phi_s=\mu$ and $\phi_t=\mu$ are positive there. This is an exact implicit solution and reconstruction, independent of a numerical solver.

---


## Appendix A. Complete prolongation algebra

This appendix makes the unrestricted calculation in Sections 4–5 reproducible. It can be read after the main reduction.

Throughout, commas indicate ordinary partial derivatives. For example, $\tau_{,t\phi}$ means $\partial^2\tau/(\partial t\,\partial\phi)$, whereas $\eta^{[tt]}$ is a prolonged coefficient. The variables $v,\rho,a,\ell,c$ retain their jet meanings from Section 2.

### A.1 Second-order coefficients and complete remainders

Separate terms containing second-order jets from terms containing only point coordinates and first-order jets:

$$
\begin{aligned}
\eta^{[tt]}
={}&(\eta_{,\phi}-2\tau_{,t}-3\tau_{,\phi}v-\xi_{,\phi}\rho)a\\
&-2(\xi_{,t}+\xi_{,\phi}v)\ell+\mathcal E_{tt},
\end{aligned}
\tag{A.1}
$$

where

$$
\boxed{
\begin{aligned}
\mathcal E_{tt}={}&
\eta_{,tt}+(2\eta_{,t\phi}-\tau_{,tt})v-\xi_{,tt}\rho\\
&+(\eta_{,\phi\phi}-2\tau_{,t\phi})v^2
-2\xi_{,t\phi}v\rho\\
&-\tau_{,\phi\phi}v^3-\xi_{,\phi\phi}v^2\rho.
\end{aligned}
}
\tag{A.2}
$$

For the mixed coefficient,

$$
\begin{aligned}
\eta^{[ts]}={}&
-(\tau_{,s}+\tau_{,\phi}\rho)a\\
&+(\eta_{,\phi}-\tau_{,t}-\xi_{,s}
-2\tau_{,\phi}v-2\xi_{,\phi}\rho)\ell\\
&-(\xi_{,t}+\xi_{,\phi}v)c+\mathcal E_{ts},
\end{aligned}
\tag{A.3}
$$

where

$$
\boxed{
\begin{aligned}
\mathcal E_{ts}={}&
\eta_{,ts}+(\eta_{,s\phi}-\tau_{,ts})v
+(\eta_{,t\phi}-\xi_{,ts})\rho\\
&-\tau_{,s\phi}v^2
+(\eta_{,\phi\phi}-\tau_{,t\phi}-\xi_{,s\phi})v\rho
-\xi_{,t\phi}\rho^2\\
&-\tau_{,\phi\phi}v^2\rho-\xi_{,\phi\phi}v\rho^2.
\end{aligned}
}
\tag{A.4}
$$

Finally,

$$
\begin{aligned}
\eta^{[ss]}={}&
-2(\tau_{,s}+\tau_{,\phi}\rho)\ell\\
&+(\eta_{,\phi}-2\xi_{,s}-\tau_{,\phi}v-3\xi_{,\phi}\rho)c
+\mathcal E_{ss},
\end{aligned}
\tag{A.5}
$$

where

$$
\boxed{
\begin{aligned}
\mathcal E_{ss}={}&
\eta_{,ss}-\tau_{,ss}v+(2\eta_{,s\phi}-\xi_{,ss})\rho\\
&-2\tau_{,s\phi}v\rho
+(\eta_{,\phi\phi}-2\xi_{,s\phi})\rho^2\\
&-\tau_{,\phi\phi}v\rho^2-\xi_{,\phi\phi}\rho^3.
\end{aligned}
}
\tag{A.6}
$$

These $\mathcal E$ expressions are explicit polynomials; they are not errors or assumed zero terms.

### A.2 Third-order coefficients, including the lower-jet terms

For compactness, name the already displayed second-order coefficients:

$$
\begin{aligned}
K_{tt}&=\eta_{,\phi}-2\tau_{,t}-3\tau_{,\phi}v-\xi_{,\phi}\rho,\\
L_{tt}&=-2(\xi_{,t}+\xi_{,\phi}v),\\
K_{ts}&=-(\tau_{,s}+\tau_{,\phi}\rho),\\
L_{ts}&=\eta_{,\phi}-\tau_{,t}-\xi_{,s}
-2\tau_{,\phi}v-2\xi_{,\phi}\rho,\\
H_{ts}&=-(\xi_{,t}+\xi_{,\phi}v).
\end{aligned}
$$

Thus $\eta^{[tt]}=K_{tt}a+L_{tt}\ell+\mathcal E_{tt}$ and $\eta^{[ts]}=K_{ts}a+L_{ts}\ell+H_{ts}c+\mathcal E_{ts}$.

Define two shorter operators acting on functions of $(t,s,\phi,v,\rho)$:

$$
\mathcal L_t=\partial_t+v\partial_\phi,\qquad
\mathcal L_s=\partial_s+\rho\partial_\phi,
$$

where $v,\rho$ are held fixed in these partial operations. Then

$$
D_t h=\mathcal L_t h+a h_{,v}+\ell h_{,\rho},
\qquad
D_s h=\mathcal L_s h+\ell h_{,v}+c h_{,\rho}.
\tag{A.7}
$$

Apply the recurrence once more:

$$
\begin{aligned}
\eta^{[ttt]}
&=D_t\eta^{[tt]}-T D_t\tau-U D_t\xi\\
&=(\eta_{,\phi}-3\tau_{,t}-4\tau_{,\phi}v-\xi_{,\phi}\rho)T\\
&\quad-3(\xi_{,t}+\xi_{,\phi}v)U+\mathcal E_{ttt},
\end{aligned}
\tag{A.8}
$$

with the complete lower-jet expression

$$
\boxed{
\begin{aligned}
\mathcal E_{ttt}={}&
(\mathcal L_tK_{tt})a+(\mathcal L_tL_{tt})\ell
+\mathcal L_t\mathcal E_{tt}\\
&+a^2K_{tt,v}
+a\ell(K_{tt,\rho}+L_{tt,v})
+\ell^2L_{tt,\rho}\\
&+a\mathcal E_{tt,v}+\ell\mathcal E_{tt,\rho}.
\end{aligned}
}
\tag{A.9}
$$

Here, for example, $K_{tt,v}$ means the partial derivative of the explicitly defined polynomial $K_{tt}$ with respect to $v$.

Likewise,

$$
\begin{aligned}
\eta^{[tss]}
&=D_s\eta^{[ts]}-U D_s\tau-R D_s\xi\\
&=-2(\tau_{,s}+\tau_{,\phi}\rho)U\\
&\quad+(\eta_{,\phi}-\tau_{,t}-2\xi_{,s}
-2\tau_{,\phi}v-3\xi_{,\phi}\rho)R\\
&\quad-(\xi_{,t}+\xi_{,\phi}v)V+\mathcal E_{tss},
\end{aligned}
\tag{A.10}
$$

where

$$
\boxed{
\begin{aligned}
\mathcal E_{tss}={}&
(\mathcal L_sK_{ts})a+(\mathcal L_sL_{ts})\ell
+(\mathcal L_sH_{ts})c+\mathcal L_s\mathcal E_{ts}\\
&+a\ell K_{ts,v}+acK_{ts,\rho}
+\ell^2L_{ts,v}
+\ell c(L_{ts,\rho}+H_{ts,v})+c^2H_{ts,\rho}\\
&+\ell\mathcal E_{ts,v}+c\mathcal E_{ts,\rho}.
\end{aligned}
}
\tag{A.11}
$$

Equations (A.2), (A.4), and the definitions of $K,L,H$ make (A.9) and (A.11) finite explicit differentiation formulas. No unspecified third-order remainder has been discarded.

#### A.2.1 Fully expanded lower-jet remainders

Expanding every derivative in (A.9) and (A.11) gives the following polynomials. No differentiation of a named remainder is left unevaluated. A parenthesized negative coefficient retains its usual algebraic sign.

$$
\begin{aligned}
\mathcal E_{ttt}={}&\left(- 3 \tau_{,\phi}\right)a^{2}\\
&+\left(- 3 \xi_{,\phi}\right)a \ell\\
&+\left(- 6 \tau_{,\phi\phi}\right)a v^{2}\\
&+\left(- 3 \xi_{,\phi\phi}\right)a \rho v\\
&+\left(3 \left(\eta_{,\phi\phi} - 3 \tau_{,t\phi}\right)\right)a v\\
&+\left(- 3 \xi_{,t\phi}\right)a \rho\\
&+\left(3 \left(- \tau_{,tt} + \eta_{,t\phi}\right)\right)a\\
&+\left(- 3 \xi_{,\phi\phi}\right)\ell v^{2}\\
&+\left(- 6 \xi_{,t\phi}\right)\ell v\\
&+\left(- 3 \xi_{,tt}\right)\ell\\
&+\left(- \tau_{,\phi\phi\phi}\right)v^{4}\\
&+\left(- \xi_{,\phi\phi\phi}\right)\rho v^{3}\\
&+\left(\eta_{,\phi\phi\phi} - 3 \tau_{,t\phi\phi}\right)v^{3}\\
&+\left(- 3 \xi_{,t\phi\phi}\right)\rho v^{2}\\
&+\left(3 \left(\eta_{,t\phi\phi} - \tau_{,tt\phi}\right)\right)v^{2}\\
&+\left(- 3 \xi_{,tt\phi}\right)\rho v\\
&+\left(- \tau_{,ttt} + 3 \eta_{,tt\phi}\right)v\\
&+\left(- \xi_{,ttt}\right)\rho\\
&+\left(\eta_{,ttt}\right)
\end{aligned}
$$

$$
\begin{aligned}
\mathcal E_{tss}={}&\left(- \tau_{,\phi}\right)a c\\
&+\left(- \tau_{,\phi\phi}\right)a \rho^{2}\\
&+\left(- 2 \tau_{,s\phi}\right)a \rho\\
&+\left(- \tau_{,ss}\right)a\\
&+\left(- 2 \tau_{,\phi}\right)\ell^{2}\\
&+\left(- 3 \xi_{,\phi}\right)c \ell\\
&+\left(- 4 \tau_{,\phi\phi}\right)\ell \rho v\\
&+\left(- 4 \tau_{,s\phi}\right)\ell v\\
&+\left(- 3 \xi_{,\phi\phi}\right)\ell \rho^{2}\\
&+\left(2 \left(\eta_{,\phi\phi} - \tau_{,t\phi} - 2 \xi_{,s\phi}\right)\right)\ell \rho\\
&+\left(- \xi_{,ss} + 2 \eta_{,s\phi} - 2 \tau_{,st}\right)\ell\\
&+\left(- \tau_{,\phi\phi}\right)c v^{2}\\
&+\left(- 3 \xi_{,\phi\phi}\right)c \rho v\\
&+\left(\eta_{,\phi\phi} - \tau_{,t\phi} - 2 \xi_{,s\phi}\right)c v\\
&+\left(- 3 \xi_{,t\phi}\right)c \rho\\
&+\left(\eta_{,t\phi} - 2 \xi_{,st}\right)c\\
&+\left(- \tau_{,\phi\phi\phi}\right)\rho^{2} v^{2}\\
&+\left(- 2 \tau_{,s\phi\phi}\right)\rho v^{2}\\
&+\left(- \tau_{,ss\phi}\right)v^{2}\\
&+\left(- \xi_{,\phi\phi\phi}\right)\rho^{3} v\\
&+\left(\eta_{,\phi\phi\phi} - \tau_{,t\phi\phi} - 2 \xi_{,s\phi\phi}\right)\rho^{2} v\\
&+\left(2 \eta_{,s\phi\phi} - \xi_{,ss\phi} - 2 \tau_{,st\phi}\right)\rho v\\
&+\left(\eta_{,ss\phi} - \tau_{,sst}\right)v\\
&+\left(- \xi_{,t\phi\phi}\right)\rho^{3}\\
&+\left(\eta_{,t\phi\phi} - 2 \xi_{,st\phi}\right)\rho^{2}\\
&+\left(- \xi_{,sst} + 2 \eta_{,st\phi}\right)\rho\\
&+\left(\eta_{,sst}\right)
\end{aligned}
$$

### A.3 Explicit assembly of the determining polynomial

For a convenient check of (4.5), define

$$
f(v,\rho)=\rho^{-2}+\beta v^2\rho^{-1},
\qquad
h(v,\rho)=2\rho^{-3}+\beta v^2\rho^{-2}.
$$

Then (2.2) is

$$
\Delta_3=\rho T+\ell a-gfR+gh\ell c-2g\beta(v/\rho)\ell^2.
$$

Apply the prolonged field using the product rule:

$$
\begin{aligned}
\operatorname{pr}^{(3)}X(\Delta_3)
={}&\eta^{[s]}T+\rho\eta^{[ttt]}
+\eta^{[ts]}a+\ell\eta^{[tt]}\\
&-g\left[
f\eta^{[tss]}+(f_{,v}\eta^{[t]}+f_{,\rho}\eta^{[s]})R
\right]\\
&+g\left[
h(\eta^{[ts]}c+\ell\eta^{[ss]})
+(h_{,v}\eta^{[t]}+h_{,\rho}\eta^{[s]})\ell c
\right]\\
&-2g\beta\left[
\left(\frac{\eta^{[t]}}{\rho}
-\frac{v\eta^{[s]}}{\rho^2}\right)\ell^2
+\frac{2v}{\rho}\ell\eta^{[ts]}
\right].
\end{aligned}
\tag{A.12}
$$

All coefficient derivatives are elementary:

$$
\begin{aligned}
f_{,v}&=2\beta v\rho^{-1},
&f_{,\rho}&=-2\rho^{-3}-\beta v^2\rho^{-2},\\
h_{,v}&=2\beta v\rho^{-2},
&h_{,\rho}&=-6\rho^{-4}-2\beta v^2\rho^{-3}.
\end{aligned}
$$

To reproduce Section 5: insert the prolongation coefficients into (A.12), replace $T$ by (2.3), multiply by $\rho^4$, and collect free jet monomials. The six selected coefficients force (5.3); the complete separated table then forces (5.6); the direct identity (5.9) closes the sufficiency check.

### A.4 The two remaining third-order components

These components do not enter (4.5), because the scalar residual is independent of $U$ and $V$. They are included to specify the complete third prolongation without unnamed remainders. The recurrence gives

$$
\eta^{[tts]}=D_s\eta^{[tt]}-T D_s\tau-U D_s\xi,\qquad
\eta^{[sss]}=D_s\eta^{[ss]}-R D_s\tau-V D_s\xi.
$$

Expanding each product and collecting the free jets gives

$$
\begin{aligned}
\eta^{[tts]}={}&\left(- \tau_{,\phi}\right)T \rho\\
&+\left(- \tau_{,s}\right)T\\
&+\left(- 3 \tau_{,\phi}\right)U v\\
&+\left(- 2 \xi_{,\phi}\right)U \rho\\
&+\left(\eta_{,\phi} - 2 \tau_{,t} - \xi_{,s}\right)U\\
&+\left(- 2 \xi_{,\phi}\right)R v\\
&+\left(- 2 \xi_{,t}\right)R\\
&+\left(- 3 \tau_{,\phi}\right)a \ell\\
&+\left(- \xi_{,\phi}\right)a c\\
&+\left(- 3 \tau_{,\phi\phi}\right)a \rho v\\
&+\left(- 3 \tau_{,s\phi}\right)a v\\
&+\left(- \xi_{,\phi\phi}\right)a \rho^{2}\\
&+\left(\eta_{,\phi\phi} - 2 \tau_{,t\phi} - \xi_{,s\phi}\right)a \rho\\
&+\left(\eta_{,s\phi} - 2 \tau_{,st}\right)a\\
&+\left(- 2 \xi_{,\phi}\right)\ell^{2}\\
&+\left(- 3 \tau_{,\phi\phi}\right)\ell v^{2}\\
&+\left(- 4 \xi_{,\phi\phi}\right)\ell \rho v\\
&+\left(2 \left(\eta_{,\phi\phi} - 2 \tau_{,t\phi} - \xi_{,s\phi}\right)\right)\ell v\\
&+\left(- 4 \xi_{,t\phi}\right)\ell \rho\\
&+\left(- \tau_{,tt} + 2 \eta_{,t\phi} - 2 \xi_{,st}\right)\ell\\
&+\left(- \xi_{,\phi\phi}\right)c v^{2}\\
&+\left(- 2 \xi_{,t\phi}\right)c v\\
&+\left(- \xi_{,tt}\right)c\\
&+\left(- \tau_{,\phi\phi\phi}\right)\rho v^{3}\\
&+\left(- \tau_{,s\phi\phi}\right)v^{3}\\
&+\left(- \xi_{,\phi\phi\phi}\right)\rho^{2} v^{2}\\
&+\left(\eta_{,\phi\phi\phi} - 2 \tau_{,t\phi\phi} - \xi_{,s\phi\phi}\right)\rho v^{2}\\
&+\left(\eta_{,s\phi\phi} - 2 \tau_{,st\phi}\right)v^{2}\\
&+\left(- 2 \xi_{,t\phi\phi}\right)\rho^{2} v\\
&+\left(2 \eta_{,t\phi\phi} - \tau_{,tt\phi} - 2 \xi_{,st\phi}\right)\rho v\\
&+\left(- \tau_{,stt} + 2 \eta_{,st\phi}\right)v\\
&+\left(- \xi_{,tt\phi}\right)\rho^{2}\\
&+\left(\eta_{,tt\phi} - \xi_{,stt}\right)\rho\\
&+\left(\eta_{,stt}\right)
\end{aligned}
$$

$$
\begin{aligned}
\eta^{[sss]}={}&\left(- 3 \tau_{,\phi}\right)R \rho\\
&+\left(- 3 \tau_{,s}\right)R\\
&+\left(- \tau_{,\phi}\right)V v\\
&+\left(- 4 \xi_{,\phi}\right)V \rho\\
&+\left(\eta_{,\phi} - 3 \xi_{,s}\right)V\\
&+\left(- 3 \tau_{,\phi}\right)c \ell\\
&+\left(- 3 \tau_{,\phi\phi}\right)\ell \rho^{2}\\
&+\left(- 6 \tau_{,s\phi}\right)\ell \rho\\
&+\left(- 3 \tau_{,ss}\right)\ell\\
&+\left(- 3 \xi_{,\phi}\right)c^{2}\\
&+\left(- 3 \tau_{,\phi\phi}\right)c \rho v\\
&+\left(- 3 \tau_{,s\phi}\right)c v\\
&+\left(- 6 \xi_{,\phi\phi}\right)c \rho^{2}\\
&+\left(3 \left(\eta_{,\phi\phi} - 3 \xi_{,s\phi}\right)\right)c \rho\\
&+\left(3 \left(- \xi_{,ss} + \eta_{,s\phi}\right)\right)c\\
&+\left(- \tau_{,\phi\phi\phi}\right)\rho^{3} v\\
&+\left(- 3 \tau_{,s\phi\phi}\right)\rho^{2} v\\
&+\left(- 3 \tau_{,ss\phi}\right)\rho v\\
&+\left(- \tau_{,sss}\right)v\\
&+\left(- \xi_{,\phi\phi\phi}\right)\rho^{4}\\
&+\left(\eta_{,\phi\phi\phi} - 3 \xi_{,s\phi\phi}\right)\rho^{3}\\
&+\left(3 \left(\eta_{,s\phi\phi} - \xi_{,ss\phi}\right)\right)\rho^{2}\\
&+\left(- \xi_{,sss} + 3 \eta_{,ss\phi}\right)\rho\\
&+\left(\eta_{,sss}\right)
\end{aligned}
$$

## Appendix B. Definitions and notation glossary

| Term | Meaning in this calculation |
|---|---|
| Lie point symmetry | A smooth local transformation of $(t,s,\phi)$ that maps solution graphs to solution graphs. |
| Generator | The vector field giving the transformation's derivative at group parameter $\epsilon=0$. |
| Symmetry algebra $\mathfrak g$ | The real vector space of admitted infinitesimal point symmetries, equipped with the Lie bracket. |
| Basis of the algebra | Independent generator fields whose constant real linear combinations give every admitted field. |
| Lie bracket $[A,B]$ | The commutator $AB-BA$ acting on smooth functions; it describes how infinitesimal transformations interact. |
| Subalgebra $\mathfrak h$ | A real vector subspace of $\mathfrak g$ closed under brackets of its own elements. |
| Ideal of $\mathfrak a$ | A subalgebra $\mathfrak h$ satisfying $[\mathfrak a,\mathfrak h]\subseteq\mathfrak h$; it permits a Lie algebra quotient $\mathfrak a/\mathfrak h$. |
| Normalizer $\mathfrak n_{\mathfrak g}(\mathfrak h)$ | The fields $A\in\mathfrak g$ with $[A,\mathfrak h]\subseteq\mathfrak h$; they preserve the chosen symmetry directions infinitesimally. |
| Inherited symmetry | A symmetry whose action descends consistently to the variables of a reduction. |
| Adjoint equivalence | Equivalence of subalgebras under a symmetry transformation's conjugation action. |
| Optimal system | A list of subalgebra representatives covering distinct classes under the chosen adjoint action. |
| Flow | The local family of maps $\Gamma_\epsilon$ generated by a vector field. |
| Orbit | The path $\Gamma_\epsilon(p)$ traced from a fixed starting point $p$. |
| Jet | A function value and its derivative values at a point, regarded as coordinates. |
| Prolongation | The chain-rule extension of a point transformation to derivative coordinates. |
| Determining equations | Equations for $\tau,\xi,\eta$ obtained from the symmetry criterion at all admissible solution jets. |
| Weight | The exponent $w$ in a scaling factor $e^{w\epsilon}$. |
| Invariant | A quantity unchanged by the transformation; infinitesimally, $X(I)=0$. |
| Invariant graph | A particular solution graph preserved by the group; its tangency condition is $Q=0$. |
| Characteristic $Q$ | The vertical graph displacement $\eta-\tau\phi_t-\xi\phi_s$. |
| Canonical coordinates | Coordinates in which the chosen generator becomes a simple translation. |
| Pushforward | Sending tangent vectors through a map’s derivative; a field descends through a quotient only when its image components agree along each fiber. |
| Differential invariant | An invariant allowed to depend on derivatives, such as $M=\sigma^{5/3}\mu'$. |
| Quotient / order reduction | Describing ODE solution curves through symmetry-invariant information, with reconstruction afterwards. |
| Normal form | A form solved for its highest derivative; any divisions used require stated nonzero conditions. |
| Abel equation of the first kind | A first-order ODE cubic in the dependent variable, with coefficients depending on the independent variable. |
| Quadrature | Recovery by integration once the integrand is known. |
| Local chart | A region where the chosen variables and coordinate changes are well-defined and invertible. |

## Appendix C. Geometric companion: from a known generator to Equation (27)

This appendix corresponds to Sheets 6–13 of the existing manuscript. It supplies the logical connections among group flows, weights, invariant graphs, pushforward, and differential invariants. The algebraic calculations, excluded branches, and examples remain in Sections 6–16; their central identities are repeated here with the geometric definitions.

### C.1 Unknown generators and generators used as reduction operators

In the determining stage, corresponding to Sheets 2–5, write

$$
X=\tau(t,s,\phi)\frac{\partial}{\partial t}
+\xi(t,s,\phi)\frac{\partial}{\partial s}
+\eta(t,s,\phi)\frac{\partial}{\partial\phi},
$$

All three coefficient functions are unknown. Section 5 determines them by third prolongation and coefficient separation, then extracts $X_1,\ldots,X_5$ from the resulting free constants.

In the later stages, corresponding to Sheets 6–13, the generators are known. The remaining tasks are to integrate their motion, identify invariant quantities, and express the equation in those quantities.

| Stage | Known object | Object to determine | Operation |
|---|---|---|---|
| Determination | Original PDE | All admitted local point generators at $m=3$ | Solve the determining equations |
| Verification | Candidate $X_5$ | Preservation of the PDE | Integrate the flow and compute weights |
| Invariant PDE solutions | Verified $X_5$ | Graphs preserved by its flow | Find point invariants and impose $Q=0$ |
| ODE order reduction | Reduced ODE and inherited symmetries | Invariant information describing solution curves | Use differential invariants and reconstruct by integration |

The local assumptions are $m=3$, $g>0$, $\beta>0$, $t>0$, $s>0$, $\phi_s>0$, and $\phi_t>0$, with $b=g\beta$. General-$m$ power expressions are also evaluated on the branch $\phi_t>0$.

Three qualifications are retained throughout: commutativity is sufficient for quotient descent but is not necessary; $Q=0$ may select special ODE solutions but is not the general order-reduction construction; and the order and integration-constant counts apply only on the stated regular patches.

### C.2 One-parameter flows as finite transformations (Sheet 6)

On the three-dimensional point manifold $\mathcal M=\{(t,s,\phi)\}$, a vector field $X$ assigns the tangent vector with components $(\tau,\xi,\eta)$ to each point.

The associated velocity is measured with respect to the group parameter $\epsilon$, which is distinct from physical time $t$. From a fixed initial point, the integral curve is

$$
\Gamma_\epsilon(t,s,\phi)
=\bigl(\bar t(\epsilon),\bar s(\epsilon),\bar\phi(\epsilon)\bigr).
$$

By definition, its derivative equals the vector field evaluated at the current point:

$$
\begin{aligned}
\frac{d\bar t}{d\epsilon}
&=\tau(\bar t,\bar s,\bar\phi),\\
\frac{d\bar s}{d\epsilon}
&=\xi(\bar t,\bar s,\bar\phi),\\
\frac{d\bar\phi}{d\epsilon}
&=\eta(\bar t,\bar s,\bar\phi),
\end{aligned}
\qquad
\begin{aligned}
\bar t(0)&=t,\\
\bar s(0)&=s,\\
\bar\phi(0)&=\phi.
\end{aligned}
\tag{C.1}
$$

The right-hand side is evaluated at the moving point. Local existence and uniqueness for the flow ODE give

$$
\Gamma_0=\mathrm{id},\qquad
\Gamma_{\epsilon+\delta}
=\Gamma_\epsilon\circ\Gamma_\delta,\qquad
\Gamma_\epsilon^{-1}=\Gamma_{-\epsilon},
$$

These identities hold wherever both sides are defined. They define a local one-parameter transformation group. A general vector field need not have a flow for every real parameter value; the scaling considered here can be integrated explicitly.

For the additional scaling generator

$$
X_5=t\frac{\partial}{\partial t}
-2s\frac{\partial}{\partial s},
$$

the coefficients are $\tau=t$, $\xi=-2s$, and $\eta=0$. Therefore

$$
\frac{d\bar t}{d\epsilon}=\bar t,\qquad
\frac{d\bar s}{d\epsilon}=-2\bar s,\qquad
\frac{d\bar\phi}{d\epsilon}=0.
$$

Integrating each equation and applying its initial condition gives

$$
\begin{aligned}
\bar t=C_1e^\epsilon,\quad \bar t(0)=t
&\ \Longrightarrow\ C_1=t,\\
\bar s=C_2e^{-2\epsilon},\quad \bar s(0)=s
&\ \Longrightarrow\ C_2=s,\\
\bar\phi=C_3,\quad \bar\phi(0)=\phi
&\ \Longrightarrow\ C_3=\phi.
\end{aligned}
$$

The resulting finite transformation is

$$
\boxed{\bar t=e^\epsilon t,\qquad
\bar s=e^{-2\epsilon}s,\qquad \bar\phi=\phi.}
\tag{C.2}
$$

For $\epsilon>0$, the time coordinate increases, the material-label coordinate decreases, and the dependent point coordinate is fixed. The identity $\bar\phi=\phi$ does not imply that an arbitrary function graph is fixed; graph invariance is treated in C.5.

### C.3 Weights as the chain-rule form of prolongation (Sheet 6)

Let $\phi=u(t,s)$ denote a scalar graph in this appendix; this temporary graph function is distinct from the Eulerian velocity in Section 0. Its transformed graph is

$$
\bar u(\bar t,\bar s)
=u(e^{-\epsilon}\bar t,e^{2\epsilon}\bar s).
$$

At corresponding points, the chain rule gives

$$
\frac{\partial}{\partial\bar t}
=e^{-\epsilon}\frac{\partial}{\partial t},\qquad
\frac{\partial}{\partial\bar s}
=e^{2\epsilon}\frac{\partial}{\partial s}.
$$

Each differentiation in the new time contributes $e^{-\epsilon}$; each differentiation in the new material label contributes $e^{2\epsilon}$. Thus, for nonnegative integers $a,j$,

$$
\frac{\partial^{a+j}\bar u}{\partial\bar t^{\,a}\partial\bar s^{\,j}}
=e^{(2j-a)\epsilon}
\frac{\partial^{a+j}u}{\partial t^a\partial s^j}.
\tag{C.3}
$$

**Definition.** If a quantity $H$ transforms as $\bar H=e^{w\epsilon}H$, then $w$ is its weight under this scaling. The weight depends on the chosen generator.

| Derivative coordinate | $a$ | $j$ | Weight $2j-a$ |
|---|---|---|---|
| $\phi_t$ | 1 | 0 | $-1$ |
| $\phi_s$ | 0 | 1 | $2$ |
| $\phi_{tt}$ | 2 | 0 | $-2$ |
| $\phi_{ts}$ | 1 | 1 | $1$ |
| $\phi_{ss}$ | 0 | 2 | $4$ |
| $\phi_{ttt}$ | 3 | 0 | $-3$ |
| $\phi_{tts}$ | 2 | 1 | $0$ |
| $\phi_{tss}$ | 1 | 2 | $3$ |
| $\phi_{sss}$ | 0 | 3 | $6$ |

Prolongation extends a point transformation to derivative coordinates by the chain rule. If $z^{(3)}$ denotes a point together with its derivative coordinates through order three, the definition is

$$
\bigl(\operatorname{pr}^{(3)}X_5\bigr)(H)
=\left.\frac{d}{d\epsilon}
H\!\left(\operatorname{pr}^{(3)}\Gamma_\epsilon(z^{(3)})\right)
\right|_{\epsilon=0}.
$$

For a homogeneous quantity of fixed weight, differentiation gives

$$
\bigl(\operatorname{pr}^{(3)}X_5\bigr)(H)
=\left.\frac{d}{d\epsilon}(e^{w\epsilon}H)\right|_{0}
=wH.
\tag{C.4}
$$

The weight method therefore computes a prolongation. Diagonal scaling makes its chain-rule calculation particularly direct. A sum of terms with different weights must be treated term by term.

### C.4 The cubic exponent from the PDE weights (Sheet 6)

Separate the scalar equation into two differential expressions:

$$
\begin{aligned}
\Delta_m&=\mathcal A_m-\mathcal B_m,\\
\mathcal A_m
&=D_t\left(\phi_s\phi_{tt}
-g\frac{\phi_{ss}}{\phi_s^2}\right),\\
\mathcal B_m
&=g\beta D_s\left(\phi_t^{m-1}
\frac{\phi_{ts}}{\phi_s}\right).
\end{aligned}
$$

The parameters $g,\beta$ are fixed and have weight zero. Weights add under multiplication and subtract under division. In this scaling, $D_t$ lowers a homogeneous expression's weight by $1$, while $D_s$ raises it by $2$.

For the first expression,

$$
\begin{aligned}
w(\phi_s\phi_{tt})&=2-2=0,\\
w\!\left(g\frac{\phi_{ss}}{\phi_s^2}\right)&=4-2\cdot2=0,\\
w(\mathcal A_m)&=0-1=-1.
\end{aligned}
$$

For the second expression,

$$
\begin{aligned}
w\!\left(\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}\right)
&=-(m-1)+1-2=-m,\\
w(\mathcal B_m)&=-m+2=2-m.
\end{aligned}
$$

Consequently,

$$
\operatorname{pr}^{(3)}X_5(\Delta_m)
=-\mathcal A_m-(2-m)\mathcal B_m
=-\Delta_m+(m-3)\mathcal B_m.
$$

When $m=3$, the two expressions have equal weight and the following exact identity holds:

$$
\boxed{\operatorname{pr}^{(3)}X_5(\Delta_3)=-\Delta_3.}
\tag{C.5}
$$

Equivalently, the finite transformation gives $\bar\Delta_3=e^{-\epsilon}\Delta_3$. This nonzero factor preserves the zero set. For $m\ne3$, the remaining term $(m-3)\mathcal B_m$ does not vanish identically on the equation hypersurface. Its accidental vanishing on a particular solution does not establish a symmetry of the full equation.

### C.5 Invariant solution graphs and orbit labels (Sheet 7)

A symmetry group may send one solution graph to another. An invariant solution is a graph mapped to itself by the entire local subgroup.

For $X_5$ and a graph $\phi=u(t,s)$, this means

$$
u(e^\epsilon t,e^{-2\epsilon}s)=u(t,s).
\tag{C.6}
$$

Such a surface is locally a union of group orbits. Only the transverse label of each orbit is needed to describe its function value. On the regular graph chart this reduces the two independent variables to one invariant coordinate.

**Definition.** A point invariant $I(t,s,\phi)$ satisfies

$$
I(\Gamma_\epsilon(t,s,\phi))=I(t,s,\phi),
$$

and hence, along each orbit,

$$
\frac{dI}{d\epsilon}=X_5(I)
=t\frac{\partial I}{\partial t}
-2s\frac{\partial I}{\partial s}=0.
$$

The orbit equations are

$$
\frac{dt}{d\epsilon}=t,\qquad
\frac{ds}{d\epsilon}=-2s,\qquad
\frac{d\phi}{d\epsilon}=0.
$$

On $t,s>0$, the first two equations imply

$$
\frac{dt}{t}=\frac{ds}{-2s}
\quad\Longrightarrow\quad
2\frac{dt}{t}+\frac{ds}{s}=0
\quad\Longrightarrow\quad
\log(st^2)=\text{constant}.
$$

The third equation states directly that $\phi$ is constant on an orbit; no division by a zero component is used. Choose

$$
\boxed{\sigma=st^2,\qquad w=\phi.}
\tag{C.7}
$$

The symbol $w$ denotes a new point coordinate; $F$ will denote the unknown profile function. A single invariant level set is generally a surface. The common level set of the two independent invariants $(\sigma,w)$ is locally the one-dimensional orbit.

In the $(t,s)$ plane, an orbit satisfies $s=\sigma/t^2$. It is an inverse-square curve.

### C.6 The characteristic from the tangent plane of a graph (Sheet 7)

Write the graph as the level set

$$
\Psi(t,s,\phi)=\phi-u(t,s)=0.
$$

A normal vector is

$$
\nabla\Psi=(-u_t,-u_s,1).
$$

The vector field is tangent to the graph precisely when

$$
X(\Psi)=\nabla\Psi\cdot(\tau,\xi,\eta)
=\eta-\tau u_t-\xi u_s=0
\quad\text{on }\Psi=0.
$$

This gives the characteristic and the invariant-surface condition:

$$
\boxed{Q=\eta-\tau\phi_t-\xi\phi_s,\qquad Q=0.}
\tag{C.8}
$$

For $X_5$,

$$
Q_{X_5}=-t\phi_t+2s\phi_s=0.
$$

The same condition follows by differentiating (C.6) at $\epsilon=0$. Solving it makes the function value constant along the orbits, so on the current local graph chart

$$
\boxed{\phi(t,s)=F(\sigma),\qquad \sigma=st^2.}
\tag{C.9}
$$

The profile $F$ remains unknown. The condition $Q=0$ determines the similarity form; substitution into the PDE determines the admissible profiles.

### C.7 Canonical coordinates and the straightened group direction (Sheet 7)

Define the complete coordinate system

$$
y=\log t,\qquad \sigma=st^2,\qquad w=\phi.
$$

Since $X_5(y)=1$ and $X_5(\sigma)=X_5(w)=0$, the new group direction is the $y$ direction. The coordinate chain rule gives

$$
\begin{aligned}
\frac{\partial}{\partial t}
&=\frac1t\frac{\partial}{\partial y}
+\frac{2\sigma}{t}\frac{\partial}{\partial\sigma},\\
\frac{\partial}{\partial s}
&=t^2\frac{\partial}{\partial\sigma}.
\end{aligned}
$$

Substitution into the vector field yields

$$
\begin{aligned}
X_5
&=t\left(\frac1t\frac{\partial}{\partial y}
+\frac{2\sigma}{t}\frac{\partial}{\partial\sigma}\right)
-2st^2\frac{\partial}{\partial\sigma}\\
&=\frac{\partial}{\partial y}
+(2\sigma-2\sigma)\frac{\partial}{\partial\sigma}
=\frac{\partial}{\partial y}.
\end{aligned}
\tag{C.10}
$$

The Jacobian determinant is $t\ne0$. The inverse coordinate map is

$$
t=e^y,\qquad s=\sigma e^{-2y},\qquad \phi=w.
$$

These are local canonical coordinates. A general graph is $w=\widetilde u(y,\sigma)$; an invariant graph satisfies

$$
Q_{X_5}=-\frac{\partial\widetilde u}{\partial y}=0,
\qquad\widetilde u(y,\sigma)=F(\sigma).
$$

The fact that $w$ is a point invariant does not make a general graph independent of $y$. Independence follows only after the graph tangency condition has been imposed.

### C.8 Chain-rule substitution of the similarity graph (Sheets 8–9)

All derivatives of $F$ below are taken with respect to $\sigma$. From

$$
\frac{\partial\sigma}{\partial t}=\frac{2\sigma}{t},\qquad
\frac{\partial\sigma}{\partial s}=t^2
$$

one obtains

$$
\phi_t=\frac{2\sigma}{t}\frac{dF}{d\sigma},\qquad
\phi_s=t^2\frac{dF}{d\sigma}.
$$

For a pure profile expression $H(\sigma)$, the derivative rules are

$$
D_t H=\frac{2\sigma}{t}\frac{dH}{d\sigma},\qquad
D_s H=t^2\frac{dH}{d\sigma}.
$$

If the expression already contains an explicit factor of $t$, that factor must also be differentiated. For example,

$$
\begin{aligned}
\phi_{tt}
&=D_t\left(\frac{2\sigma}{t}\frac{dF}{d\sigma}\right)\\
&=-\frac{2\sigma}{t^2}\frac{dF}{d\sigma}
+\frac2t\left(\frac{dF}{d\sigma}
+\sigma\frac{d^2F}{d\sigma^2}\right)\frac{2\sigma}{t}\\
&=\frac1{t^2}\left(2\sigma\frac{dF}{d\sigma}
+4\sigma^2\frac{d^2F}{d\sigma^2}\right).
\end{aligned}
$$

The other required derivatives are

$$
\begin{aligned}
\phi_{ts}&=2t\left(\frac{dF}{d\sigma}
+\sigma\frac{d^2F}{d\sigma^2}\right),\\
\phi_{ss}&=t^4\frac{d^2F}{d\sigma^2},\\
\phi_{ttt}&=\frac1{t^3}\left(12\sigma^2\frac{d^2F}{d\sigma^2}
+8\sigma^3\frac{d^3F}{d\sigma^3}\right),\\
\phi_{tss}&=2t^3\left(2\frac{d^2F}{d\sigma^2}
+\sigma\frac{d^3F}{d\sigma^3}\right).
\end{aligned}
\tag{C.11}
$$

Substitution into the two divergence brackets can be performed before expanding the full third-order PDE. Define

$$
\begin{aligned}
\mathcal A(\sigma)
&=2\sigma\left(\frac{dF}{d\sigma}\right)^2
+4\sigma^2\frac{dF}{d\sigma}\frac{d^2F}{d\sigma^2}
-g\frac{d^2F/d\sigma^2}{(dF/d\sigma)^2},\\
\mathcal B(\sigma)
&=8\sigma^2\left(\frac{dF}{d\sigma}\right)^2
+8\sigma^3\frac{dF}{d\sigma}\frac{d^2F}{d\sigma^2}.
\end{aligned}
$$

Then

$$
\phi_s\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^2}=\mathcal A,
\qquad
\phi_t^2\frac{\phi_{ts}}{\phi_s}=t^{-3}\mathcal B,
$$

and therefore

$$
\left.\Delta_3\right|_{\phi=F(st^2)}
=\frac1t\left(2\sigma\frac{d\mathcal A}{d\sigma}
-b\frac{d\mathcal B}{d\sigma}\right).
$$

The product and quotient rules give

$$
\begin{aligned}
\frac{d\mathcal A}{d\sigma}
={}&2\left(\frac{dF}{d\sigma}\right)^2
+12\sigma\frac{dF}{d\sigma}\frac{d^2F}{d\sigma^2}\\
&+4\sigma^2\left[\left(\frac{d^2F}{d\sigma^2}\right)^2
+\frac{dF}{d\sigma}\frac{d^3F}{d\sigma^3}\right]\\
&-g\frac{d^3F/d\sigma^3}{(dF/d\sigma)^2}
+2g\frac{(d^2F/d\sigma^2)^2}{(dF/d\sigma)^3},\\[2pt]
\frac{d\mathcal B}{d\sigma}
={}&16\sigma\left(\frac{dF}{d\sigma}\right)^2
+40\sigma^2\frac{dF}{d\sigma}\frac{d^2F}{d\sigma^2}\\
&+8\sigma^3\left[\left(\frac{d^2F}{d\sigma^2}\right)^2
+\frac{dF}{d\sigma}\frac{d^3F}{d\sigma^3}\right].
\end{aligned}
$$

Multiply $2\sigma\mathcal A'-b\mathcal B'$ by $-(dF/d\sigma)^3/(2\sigma)$ and collect terms. The third-order profile residual is

$$
\begin{aligned}
\mathcal R_3={}&
\frac{dF}{d\sigma}
\left[g+4(b-1)\sigma^2\left(\frac{dF}{d\sigma}\right)^3\right]
\frac{d^3F}{d\sigma^3}\\
&+\left[4(b-1)\sigma^2\left(\frac{dF}{d\sigma}\right)^3-2g\right]
\left(\frac{d^2F}{d\sigma^2}\right)^2\\
&+(20b-12)\sigma\left(\frac{dF}{d\sigma}\right)^4
\frac{d^2F}{d\sigma^2}
+(8b-2)\left(\frac{dF}{d\sigma}\right)^5.
\end{aligned}
\tag{C.12}
$$

The exact pullback identity is

$$
\boxed{
\left.\Delta_3\right|_{\phi=F(st^2)}
=-\frac{2\sigma}{t(dF/d\sigma)^3}\,\mathcal R_3.
}
\tag{C.13}
$$

On $t>0$, $\sigma>0$, and $dF/d\sigma>0$, its prefactor is nonzero. The substituted PDE is therefore equivalent to $\mathcal R_3=0$ on that chart. The number of independent variables has decreased from two to one; the differential order remains three.

### C.9 ODE order reduction and additional invariant solutions (Sheet 10)

Near a regular point where the highest derivative can be solved for, a third-order ODE has three local initial constants. A symmetry relates different solution curves, so a quotient description can omit the information identifying a point on a symmetry orbit. Reconstruction restores the corresponding constant.

Consider vertical translation:

$$
Z=\frac{\partial}{\partial F},\qquad
(\bar\sigma,\bar F)=(\sigma,F+\epsilon)
$$

Adding a constant changes the graph's height while leaving its slope fixed. Identifying these translated graphs produces the quotient used in this example.

Requiring one graph itself to be fixed by every vertical translation would instead impose

$$
Q_Z=1-0\cdot\frac{dF}{d\sigma}=1=0,
$$

which has no solution. The translation still relates distinct solution curves and supplies an order reduction.

An absolute prohibition on using $Q=0$ for ODEs would be incorrect. For other generators it selects special invariant solutions. For example, for

$$
Y=3\sigma\frac{\partial}{\partial\sigma}
+F\frac{\partial}{\partial F},
$$

the invariant-graph condition is

$$
F-3\sigma\frac{dF}{d\sigma}=0
\quad\Longrightarrow\quad F=K\sigma^{1/3}.
$$

Substitution into $\mathcal R_3=0$ is still required to determine $K$. This selects a special family and does not replace the general regular order reduction.

An order reduction by one requires a regular group action and usable differential-invariant coordinates along the solutions under consideration. Singular orbits and degenerate coordinate changes require separate analysis.

### C.10 The first ODE quotient: slope as a differential invariant (Sheet 10)

**Definition.** A differential invariant is a function of independent variables, dependent variables, and finitely many derivative coordinates that is invariant under the prolonged action. Point invariants are its order-zero case.

Under vertical translation,

$$
\bar\sigma=\sigma,\qquad
\frac{d\bar F}{d\bar\sigma}
=\frac{d(F+\epsilon)}{d\sigma}
=\frac{dF}{d\sigma}.
$$

Thus $\sigma$ is an order-zero invariant and $dF/d\sigma$ is an order-one invariant. Define

$$
\boxed{\mu(\sigma)=\frac{dF}{d\sigma},\qquad
\frac{d\mu}{d\sigma}=\frac{d^2F}{d\sigma^2},\qquad
\frac{d^2\mu}{d\sigma^2}=\frac{d^3F}{d\sigma^3}.}
\tag{C.14}
$$

Equation (C.12) contains no undifferentiated $F$. Substitution gives the second-order equation

$$
\begin{aligned}
\mathcal R_2={}&
\mu\left[g+4(b-1)\sigma^2\mu^3\right]
\frac{d^2\mu}{d\sigma^2}\\
&+\left[4(b-1)\sigma^2\mu^3-2g\right]
\left(\frac{d\mu}{d\sigma}\right)^2\\
&+(20b-12)\sigma\mu^4\frac{d\mu}{d\sigma}
+(8b-2)\mu^5=0.
\end{aligned}
\tag{C.15}
$$

Fix a reference point $\sigma_*>0$. A solution $\mu$ reconstructs a profile family through

$$
F(\sigma)=F_*+\int_{\sigma_*}^{\sigma}\mu(r)\,dr
$$

Here $r$ is a dummy integration variable. The constant $F_*$ restores the vertical level omitted by the quotient.

### C.11 Pushforward of $X_4$ to the profile space (Sheet 10)

For a smooth map $\pi:\mathcal M\to\mathcal Q$, its differential maps each source tangent vector to a target tangent vector. In target coordinates $q^i$,

$$
d\pi_p(X_p)
=\sum_i X(q^i\circ\pi)(p)\,
\left.\frac{\partial}{\partial q^i}\right|_{\pi(p)}.
$$

This is the chain rule for tangent vectors. If different source points map to the same target point, their image vectors must agree before they define a vector field on the target. This condition is projectability.

In the present reduction,

$$
\pi(t,s,\phi)=(\sigma,w)=(st^2,\phi).
$$

A fiber is locally one $X_5$ orbit, and the invariant coordinates label these orbits. For

$$
X_4=t\frac{\partial}{\partial t}
+s\frac{\partial}{\partial s}
+\phi\frac{\partial}{\partial\phi},
$$

the pushforward can be calculated in two equivalent ways.

**Method A: differentiate the new coordinates along the old field.**

$$
\begin{aligned}
X_4(\sigma)
&=t\frac{\partial(st^2)}{\partial t}
+s\frac{\partial(st^2)}{\partial s}
+\phi\frac{\partial(st^2)}{\partial\phi}\\
&=t(2st)+s(t^2)+0=3st^2=3\sigma,\\
X_4(w)&=X_4(\phi)=\phi=w.
\end{aligned}
$$

The resulting components depend only on the target coordinates and hence define a target field. Using the profile-space coordinate notation $w=F$, write

$$
\boxed{Y=3\sigma\frac{\partial}{\partial\sigma}
+F\frac{\partial}{\partial F}.}
\tag{C.16}
$$

In the full coordinates $(y,\sigma,w)$, $X_4=\partial_y+3\sigma\partial_\sigma+w\partial_w$. The $y$ component is removed only on passage to the $X_5$ orbit quotient.

**Method B: transform the new coordinates by the finite flow.**

$$
(\bar t,\bar s,\bar\phi)
=(e^\epsilon t,e^\epsilon s,e^\epsilon\phi)
$$

The finite flow induces

$$
\bar\sigma=\bar s\bar t^2=e^{3\epsilon}\sigma,
\qquad\bar w=e^\epsilon w.
$$

Differentiation at $\epsilon=0$ gives the components $3\sigma,w$, reproducing (C.16).

### C.12 Projectability, commutativity, and the normalizer (Sheet 10)

If $X_5(I)=0$, the bracket identity gives

$$
X_5\bigl(X_4(I)\bigr)
=[X_5,X_4](I)+X_4\bigl(X_5(I)\bigr).
$$

Since $[X_5,X_4]=0$, the expression is zero. Thus $X_4$ maps an invariant to an invariant, and its target components are independent of the orbit coordinate.

Vanishing of the bracket is sufficient, but is not required. For this regular one-dimensional orbit foliation, a more general projectability condition is

$$
[X_5,A]=a(t,s,\phi)X_5
$$

for a smooth coefficient $a$. Then $[X_5,A](I)=aX_5(I)=0$ still holds. The Lie-algebra normalizer condition used in Section 5.9,

$$
[A,\mathfrak h]\subseteq\mathfrak h,
\qquad\mathfrak h=\operatorname{span}_{\mathbb R}\{X_5\},
$$

ensures this property. Its linear combinations have constant real coefficients; preservation of the orbit distribution may allow a variable coefficient $a$.

For a counterexample, $X_1=\partial_t$ gives

$$
X_1(\sigma)=2st=\frac{2\sigma}{t},
\qquad
X_5\!\left(\frac{2\sigma}{t}\right)=-\frac{2\sigma}{t}\ne0.
$$

The component still depends on the eliminated coordinate $t$. It therefore fails to define a field depending only on $(\sigma,w)$ in this fixed quotient. A time translation generally carries an $X_5$-invariant graph to a graph invariant under a conjugate generator.

### C.13 Prolongation before descent from functions to slopes (Sheet 10)

The quantity $\mu=dF/d\sigma$ is a derivative coordinate. Consequently $(\sigma,F)\mapsto(\sigma,\mu)$ is not an ordinary point-coordinate transformation. The field must first be prolonged to the first jet space and then descended through vertical translation.

The finite scaling is

$$
\bar\sigma=e^{3\epsilon}\sigma,\qquad
\bar F=e^\epsilon F,
$$

so at corresponding points

$$
\bar\mu
=\frac{d\bar F}{d\bar\sigma}
=\frac{e^\epsilon\,dF}{e^{3\epsilon}\,d\sigma}
=e^{-2\epsilon}\mu.
$$

Differentiate in the group parameter:

$$
\operatorname{pr}^{(1)}Y
=3\sigma\frac{\partial}{\partial\sigma}
+F\frac{\partial}{\partial F}
-2\mu\frac{\partial}{\partial\mu}.
$$

Its components on the two translation invariants $(\sigma,\mu)$ are $3\sigma,-2\mu$. Hence

$$
\boxed{Y_1=3\sigma\frac{\partial}{\partial\sigma}
-2\mu\frac{\partial}{\partial\mu}.}
\tag{C.17}
$$

This also exhibits descent without commutativity: $[Y,Z]=-Z\ne0$, but $Y$ preserves the subalgebra $\operatorname{span}\{Z\}$ and therefore descends to the slope equation.

### C.14 The second ODE quotient: two differential invariants (Sheet 11)

Temporarily denote the slope jet $d\mu/d\sigma$ by $\upsilon$. It is a jet coordinate, not an additional independent function assumption. From

$$
\bar\sigma=e^{3\epsilon}\sigma,\qquad
\bar\mu=e^{-2\epsilon}\mu
$$

one obtains

$$
\bar \upsilon=\frac{d\bar\mu}{d\bar\sigma}
=e^{-5\epsilon}\upsilon,
\qquad
\operatorname{pr}^{(1)}Y_1
=3\sigma\partial_\sigma-2\mu\partial_\mu-5\upsilon\partial_\upsilon.
$$

Combining quantities of opposite weights gives

$$
\begin{aligned}
\bar\sigma^{2/3}\bar\mu
&=e^{2\epsilon}\sigma^{2/3}e^{-2\epsilon}\mu
=\sigma^{2/3}\mu,\\
\bar\sigma^{5/3}\bar \upsilon
&=e^{5\epsilon}\sigma^{5/3}e^{-5\epsilon}\upsilon
=\sigma^{5/3}\upsilon.
\end{aligned}
$$

Choose

$$
\boxed{\Sigma=\sigma^{2/3}\mu,\qquad
M=\sigma^{5/3}\frac{d\mu}{d\sigma}.}
\tag{C.18}
$$

The same expressions follow from $d\sigma/(3\sigma)=d\mu/(-2\mu)=d\upsilon/(-5\upsilon)$. The weight verification does not divide by $\upsilon$, so $M$ is defined at $\upsilon=0$ as well.

At fixed $\sigma>0$, the invariants are independent because

$$
\det\frac{\partial(\Sigma,M)}{\partial(\mu,\upsilon)}
=\sigma^{7/3}\ne0
$$

is nonzero. Adding $z=(\log\sigma)/3$ gives a full first-jet coordinate system.

Independence as invariant coordinates and the ability to use $\Sigma$ as the independent variable along a particular solution are distinct conditions. The second must be checked separately.

### C.15 Derivative conversion and local invertibility (Sheets 11–12)

Differentiate $\Sigma=\sigma^{2/3}\mu(\sigma)$:

$$
\begin{aligned}
\frac{d\Sigma}{d\sigma}
&=\frac23\sigma^{-1/3}\mu
+\sigma^{2/3}\frac{d\mu}{d\sigma}\\
&=\frac23\sigma^{-1/3}\sigma^{-2/3}\Sigma
+\sigma^{2/3}\sigma^{-5/3}M\\
&=\frac1\sigma\left(M+\frac23\Sigma\right).
\end{aligned}
\tag{C.19}
$$

Define $W=M+\frac23\Sigma$. Only where $W\ne0$ is $d\Sigma/d\sigma\ne0$, allowing the local representation $M=M(\Sigma)$.

Solve the invariant definitions for the original slope coordinates:

$$
\mu=\sigma^{-2/3}\Sigma,\qquad
\frac{d\mu}{d\sigma}=\sigma^{-5/3}M(\Sigma).
$$

Differentiate both the power factor and the composite function:

$$
\begin{aligned}
\frac{d^2\mu}{d\sigma^2}
&=\frac{d}{d\sigma}\left[\sigma^{-5/3}M(\Sigma(\sigma))\right]\\
&=-\frac53\sigma^{-8/3}M
+\sigma^{-5/3}\frac{dM}{d\Sigma}\frac{d\Sigma}{d\sigma}\\
&=-\frac53\sigma^{-8/3}M
+\sigma^{-5/3}\frac{dM}{d\Sigma}\frac{W}{\sigma}\\
&=\sigma^{-8/3}
\left[\left(M+\frac23\Sigma\right)\frac{dM}{d\Sigma}
-\frac53M\right].
\end{aligned}
\tag{C.20}
$$

The quantities $d\mu/d\sigma$ and $dM/d\Sigma$ differentiate different functions with respect to different independent variables. The full notation is retained in the subsequent substitution.

### C.16 Term-by-term reduction of the second-order equation (Sheet 12)

Since $\sigma^2\mu^3=\Sigma^3$, define the coefficient functions

$$
\begin{aligned}
D(\Sigma)&=g+4(b-1)\Sigma^3,\\
A(\Sigma)&=4(b-1)\Sigma^3-2g,\\
B(\Sigma)&=\frac{\Sigma}{3}\left[8(5b-2)\Sigma^3-5g\right],\\
C(\Sigma)&=2(4b-1)\Sigma^5.
\end{aligned}
\tag{C.21}
$$

The polynomial $D(\Sigma)$ is distinct from the total derivative operators $D_t,D_s$. Substitution of (C.20) and the two preceding relations into (C.15) gives

$$
\begin{aligned}
\mu[g+4(b-1)\sigma^2\mu^3]\frac{d^2\mu}{d\sigma^2}
&=\sigma^{-10/3}\Sigma D
\left(W\frac{dM}{d\Sigma}-\frac53M\right),\\
{}[4(b-1)\sigma^2\mu^3-2g]\left(\frac{d\mu}{d\sigma}\right)^2
&=\sigma^{-10/3}AM^2,\\
(20b-12)\sigma\mu^4\frac{d\mu}{d\sigma}
&=\sigma^{-10/3}(20b-12)\Sigma^4M,\\
(8b-2)\mu^5&=\sigma^{-10/3}(8b-2)\Sigma^5.
\end{aligned}
$$

The four powers are respectively $-2/3-8/3=-10/3$, $2(-5/3)=-10/3$, $1-8/3-5/3=-10/3$, and $5(-2/3)=-10/3$.

This establishes the common factor directly. An arbitrary residual representation need not have a single weight merely because its equation has a symmetry; the homogeneous representation used here has been checked term by term.

Divide by the nonzero factor $\sigma^{-10/3}$:

$$
\Sigma D\left(W\frac{dM}{d\Sigma}-\frac53M\right)
+AM^2+(20b-12)\Sigma^4M+(8b-2)\Sigma^5=0.
$$

The coefficient of the terms linear in $M$ is

$$
\begin{aligned}
-\frac53\Sigma D+(20b-12)\Sigma^4
&=\frac\Sigma3\left[-5g+(-20b+20+60b-36)\Sigma^3\right]\\
&=\frac\Sigma3\left[-5g+8(5b-2)\Sigma^3\right]=B.
\end{aligned}
$$

The derivative-free constant term is $C$. Therefore

$$
\boxed{\Sigma D\left(M+\frac23\Sigma\right)\frac{dM}{d\Sigma}
+AM^2+BM+C=0.}
\tag{C.22}
$$

Where $\Sigma D W\ne0$,

$$
\frac{dM}{d\Sigma}
=-\frac{AM^2+BM+C}{\Sigma D(M+\frac23\Sigma)}.
\tag{C.23}
$$

The equation is first order, but its right-hand side is rational in $M$. A further dependent-variable substitution is required for the cubic Abel form.

### C.17 The reciprocal shift and the cubic Abel form (Sheet 13)

The factor multiplying the derivative is $W=M+\frac23\Sigma$. Define a shift followed by a reciprocal:

$$
\boxed{N=\frac1{M+\frac23\Sigma},\qquad
M=\frac1N-\frac23\Sigma.}
\tag{C.24}
$$

This is an algebraic dependent-variable change. It does not use a new Lie symmetry and does not lower the order further.

Differentiation with respect to $\Sigma$ gives

$$
\frac{dM}{d\Sigma}
=-\frac1{N^2}\frac{dN}{d\Sigma}-\frac23.
$$

Substitute into the implicit equation (C.22):

$$
\frac{\Sigma D}{N}
\left(-\frac1{N^2}\frac{dN}{d\Sigma}-\frac23\right)
+A\left(\frac1N-\frac23\Sigma\right)^2
+B\left(\frac1N-\frac23\Sigma\right)+C=0.
$$

Expanding every term gives

$$
\begin{aligned}
0={}&-\frac{\Sigma D}{N^3}\frac{dN}{d\Sigma}
-\frac{2\Sigma D}{3N}
+\frac A{N^2}-\frac{4A\Sigma}{3N}
+\frac49A\Sigma^2\\
&+\frac BN-\frac23B\Sigma+C.
\end{aligned}
$$

Multiply by $N^3/(\Sigma D)$ on its nonzero-denominator patch and rearrange:

$$
\begin{aligned}
\frac{dN}{d\Sigma}
={}&\frac A{\Sigma D}N\\
&+\left(-\frac23-\frac{4A}{3D}+\frac B{\Sigma D}\right)N^2\\
&+\left(\frac{4\Sigma A}{9D}-\frac{2B}{3D}
+\frac C{\Sigma D}\right)N^3.
\end{aligned}
\tag{C.25}
$$

The quadratic contribution $-2/3$ arises from differentiating the shift $-2\Sigma/3$.

To derive the coefficient functions, put each expression over a common denominator. The linear coefficient is

$$
a_1=\frac A{\Sigma D}
=\frac{2[2(b-1)\Sigma^3-g]}{\Sigma D}.
$$

The numerator of the quadratic coefficient is

$$
\begin{aligned}
-2D-4A+3B/\Sigma
={}&-2[g+4(b-1)\Sigma^3]
-4[4(b-1)\Sigma^3-2g]\\
&+[8(5b-2)\Sigma^3-5g]\\
={}&g+8(1+2b)\Sigma^3.
\end{aligned}
$$

The cubic coefficient has denominator $9\Sigma D$ and numerator

$$
\begin{aligned}
4\Sigma^2A-6\Sigma B+9C
={}&[16(b-1)-16(5b-2)+18(4b-1)]\Sigma^5\\
&+(-8+10)g\Sigma^2\\
={}&2(4b-1)\Sigma^5+2g\Sigma^2.
\end{aligned}
$$

Consequently,

$$
\boxed{
\begin{aligned}
\frac{dN}{d\Sigma}
={}&\frac{2\Sigma[g+(4b-1)\Sigma^3]}{9[g+4(b-1)\Sigma^3]}N^3\\
&+\frac{g+8(1+2b)\Sigma^3}{3[g+4(b-1)\Sigma^3]}N^2\\
&+\frac{2[2(b-1)\Sigma^3-g]}{\Sigma[g+4(b-1)\Sigma^3]}N,
\qquad b=g\beta.
\end{aligned}}
\tag{C.26}
$$

This is the first-kind Abel equation (A27). Restoring $b=g\beta$ gives (27*). These cubic coefficients belong to $N$, not to the originally defined $M=\sigma^{5/3}d\mu/d\sigma$. The explicit change (C.24) completes the derivation.

### C.18 Reconstruction constants and excluded branches (Sheets 14–16)

On a local interval with $\Sigma>0$, $D(\Sigma)\ne0$, and $0<|N|<\infty$, equations (C.19), (C.24) give

$$
\frac{d\Sigma}{d\sigma}=\frac1{N\sigma}
\quad\Longrightarrow\quad
\frac{d\sigma}{d\Sigma}=N\sigma.
$$

Fix $\Sigma_*$ and integrate:

$$
\sigma(\Sigma)
=\sigma_*\exp\left(\int_{\Sigma_*}^{\Sigma}N(v)\,dv\right),
\qquad\sigma_*>0.
$$

Then

$$
\mu(\Sigma)=\Sigma\sigma(\Sigma)^{-2/3},\qquad
\frac{dF}{d\Sigma}
=\frac{dF}{d\sigma}\frac{d\sigma}{d\Sigma}
=\Sigma\sigma(\Sigma)^{1/3}N(\Sigma),
$$

and therefore

$$
F(\Sigma)=F_*+
\int_{\Sigma_*}^{\Sigma}v\sigma(v)^{1/3}N(v)\,dv.
$$

Since $d\sigma/d\Sigma=N\sigma\ne0$, invert locally to obtain $\Sigma=\Sigma(\sigma)$ and then $\phi(t,s)=F(st^2)$. The initial value for the Abel equation and the reconstruction constants $\sigma_*,F_*$ restore the three local constants of the regular third-order profile equation.

**Excluded constant-invariant branch.** If $W=0$ throughout an interval, then $d\Sigma/d\sigma=0$, so $\Sigma=k$ is constant and

$$
\mu=k\sigma^{-2/3},\qquad
\frac{d\mu}{d\sigma}=-\frac23k\sigma^{-5/3},\qquad
\frac{d^2\mu}{d\sigma^2}=\frac{10}{9}k\sigma^{-8/3}.
$$

Substitute directly into the second-order equation, without the invalid representation $M=M(\Sigma)$:

$$
\left.\mathcal R_2\right|_{W=0}
=\frac29 k^2\sigma^{-10/3}
\left[g+(4b-1)k^3\right].
$$

On the positive branch $k>0$, this implies

$$
k^3=\frac{g}{1-4b},\qquad 0<b<\frac14,
\qquad
F(\sigma)=F_*+3k\sigma^{1/3}.
$$

This is an exact family outside the reciprocal chart. An isolated zero of $W$ only indicates degeneration of the chosen independent variable; it does not force the entire profile into this family.

Similarly, $D=0$ marks degeneration of the highest-derivative coefficient and requires the undivided equation. The formal Abel solution $N=0$ has no finite inverse $M$ in this chart. Section 15 records these branch conditions, and Section 16 supplies a regular local series example.

### C.19 Operation and domain correspondence

| Location | Definition or reason | Result | Condition retained |
|---|---|---|---|
| Sheet 6 | Integral curves of the generator | Exponential flow of $X_5$ | Group parameter differs from physical time |
| Sheet 6 | Chain-rule transformation of derivatives | Weights $2j-a$ and $\operatorname{pr}^{(3)}X_5(\Delta_3)=-\Delta_3$ | Parameters fixed; homogeneous terms checked separately |
| Sheet 7 | Graph tangency | $Q_{X_5}=0$ and $\phi=F(st^2)$ | A selected invariant-solution family |
| Sheets 8–9 | Substitution with a nonzero residual multiplier | Third-order equation $\mathcal R_3=0$ | Explicit $t$ factors are differentiated |
| Sheet 10 | Translation invariance of the slope | $\mu=dF/d\sigma$ and $\mathcal R_2=0$ | Restore the additive constant $F_*$ |
| Sheet 10 | Projectability and prolongation | $X_4\mapsto Y\mapsto Y_1$ | Normalizer condition suffices; commutativity is not required |
| Sheets 11–12 | Order-zero and order-one differential invariants | $\Sigma,M$ and a first-order rational equation | $W\ne0$ to use $\Sigma$ as independent variable |
| Sheet 13 | Reciprocal of a shifted invariant | $N=1/W$ and the cubic Abel equation | $D\ne0$, $N\ne0$; excluded branches checked separately |

At each stage the function's independent variable, the distinction between invariant-graph selection and quotient reduction, and the invertibility domain remain explicit. These data determine the precise mathematical meaning of every transformation in the reduction.


## Appendix D. Complete unrestricted determining polynomial at $m=3$

This is an exact coefficient expansion of $\mathscr P$ in (5.1). Every entry must vanish. Point derivatives use commas, and the row monomials contain only the free jet coordinates. The expansion has 118 nonzero coefficients before restrictions are imposed. The table records the complete identity, rather than only the six coefficients used to begin its triangular solution.

| No. | Free jet monomial | Coefficient |
|---|---|---|
| 1 | $\rho^{5} v^{4}$ | $\left(\beta g - 1\right) \tau_{,\phi\phi\phi}$ |
| 2 | $\rho^{4} v^{4}$ | $2 \beta g \tau_{,s\phi\phi}$ |
| 3 | $\rho^{3} v^{4}$ | $\beta g \tau_{,ss\phi}$ |
| 4 | $c \rho^{2} v^{4}$ | $- \beta g \tau_{,s\phi}$ |
| 5 | $\rho^{6} v^{3}$ | $\left(\beta g - 1\right) \xi_{,\phi\phi\phi}$ |
| 6 | $\rho^{5} v^{3}$ | $- \beta g \eta_{,\phi\phi\phi} + \beta g \tau_{,t\phi\phi} + 2 \beta g \xi_{,s\phi\phi} + \eta_{,\phi\phi\phi} - 3 \tau_{,t\phi\phi}$ |
| 7 | $\ell \rho^{4} v^{3}$ | $\left(7 \beta g - 1\right) \tau_{,\phi\phi}$ |
| 8 | $c \rho^{4} v^{3}$ | $2 \beta g \xi_{,\phi\phi}$ |
| 9 | $\rho^{4} v^{3}$ | $- \beta g \left(2 \eta_{,s\phi\phi} - \xi_{,ss\phi} - 2 \tau_{,st\phi}\right)$ |
| 10 | $\ell \rho^{3} v^{3}$ | $6 \beta g \tau_{,s\phi}$ |
| 11 | $c \rho^{3} v^{3}$ | $\beta g \xi_{,s\phi}$ |
| 12 | $R \rho^{3} v^{3}$ | $- 2 \beta g \tau_{,\phi}$ |
| 13 | $V \rho^{3} v^{3}$ | $\beta g \xi_{,\phi}$ |
| 14 | $\rho^{3} v^{3}$ | $- \beta g \left(\eta_{,ss\phi} - \tau_{,sst}\right)$ |
| 15 | $c \ell \rho^{2} v^{3}$ | $2 \beta g \tau_{,\phi}$ |
| 16 | $\ell \rho^{2} v^{3}$ | $- \beta g \tau_{,ss}$ |
| 17 | $c^{2} \rho^{2} v^{3}$ | $- \beta g \xi_{,\phi}$ |
| 18 | $c \rho^{2} v^{3}$ | $\beta g \left(\eta_{,s\phi} - \tau_{,st}\right)$ |
| 19 | $R \rho^{2} v^{3}$ | $- 2 \beta g \tau_{,s}$ |
| 20 | $c \ell \rho v^{3}$ | $3 \beta g \tau_{,s}$ |
| 21 | $\rho^{6} v^{2}$ | $\left(\beta g - 3\right) \xi_{,t\phi\phi}$ |
| 22 | $a \rho^{5} v^{2}$ | $\left(\beta g - 7\right) \tau_{,\phi\phi}$ |
| 23 | $\ell \rho^{5} v^{2}$ | $2 \left(3 \beta g - 2\right) \xi_{,\phi\phi}$ |
| 24 | $\rho^{5} v^{2}$ | $- \beta g \eta_{,t\phi\phi} + 2 \beta g \xi_{,st\phi} + 3 \eta_{,t\phi\phi} - 3 \tau_{,tt\phi}$ |
| 25 | $a \rho^{4} v^{2}$ | $\left(2 \beta g - 1\right) \tau_{,s\phi}$ |
| 26 | $\ell \rho^{4} v^{2}$ | $- 5 \beta g \eta_{,\phi\phi} + 6 \beta g \tau_{,t\phi} + 6 \beta g \xi_{,s\phi} + \eta_{,\phi\phi} - 2 \tau_{,t\phi}$ |
| 27 | $c \rho^{4} v^{2}$ | $2 \beta g \xi_{,t\phi}$ |
| 28 | $U \rho^{4} v^{2}$ | $2 \beta g \tau_{,\phi}$ |
| 29 | $R \rho^{4} v^{2}$ | $2 \beta g \xi_{,\phi}$ |
| 30 | $\rho^{4} v^{2}$ | $- g \left(- \beta \xi_{,sst} + 2 \beta \eta_{,st\phi} - \tau_{,\phi\phi\phi}\right)$ |
| 31 | $a \rho^{3} v^{2}$ | $\beta g \tau_{,ss}$ |
| 32 | $\ell^{2} \rho^{3} v^{2}$ | $- 2 \beta g \tau_{,\phi}$ |
| 33 | $c \ell \rho^{3} v^{2}$ | $4 \beta g \xi_{,\phi}$ |
| 34 | $\ell \rho^{3} v^{2}$ | $- 2 \beta g \left(2 \eta_{,s\phi} - 3 \tau_{,st}\right)$ |
| 35 | $c \rho^{3} v^{2}$ | $\beta g \xi_{,st}$ |
| 36 | $U \rho^{3} v^{2}$ | $2 \beta g \tau_{,s}$ |
| 37 | $V \rho^{3} v^{2}$ | $\beta g \xi_{,t}$ |
| 38 | $\rho^{3} v^{2}$ | $- g \left(\beta \eta_{,sst} - 2 \tau_{,s\phi\phi}\right)$ |
| 39 | $a c \rho^{2} v^{2}$ | $- \beta g \tau_{,s}$ |
| 40 | $\ell^{2} \rho^{2} v^{2}$ | $- 6 \beta g \tau_{,s}$ |
| 41 | $\ell \rho^{2} v^{2}$ | $\beta g \eta_{,ss}$ |
| 42 | $c^{2} \rho^{2} v^{2}$ | $- \beta g \xi_{,t}$ |
| 43 | $c \rho^{2} v^{2}$ | $g \left(\beta \eta_{,st} - \tau_{,\phi\phi}\right)$ |
| 44 | $R \rho^{2} v^{2}$ | $2 \beta g \eta_{,s}$ |
| 45 | $\rho^{2} v^{2}$ | $g \tau_{,ss\phi}$ |
| 46 | $c \ell \rho v^{2}$ | $- 3 \beta g \eta_{,s}$ |
| 47 | $c \rho v^{2}$ | $- 2 g \tau_{,s\phi}$ |
| 48 | $a \rho^{6} v$ | $- 4 \xi_{,\phi\phi}$ |
| 49 | $\rho^{6} v$ | $- 3 \xi_{,tt\phi}$ |
| 50 | $a \rho^{5} v$ | $4 \eta_{,\phi\phi} - 10 \tau_{,t\phi} - \xi_{,s\phi}$ |
| 51 | $\ell \rho^{5} v$ | $4 \left(\beta g - 2\right) \xi_{,t\phi}$ |
| 52 | $U \rho^{5} v$ | $- 3 \xi_{,\phi}$ |
| 53 | $\rho^{5} v$ | $g \xi_{,\phi\phi\phi} - \tau_{,ttt} + 3 \eta_{,tt\phi}$ |
| 54 | $a \ell \rho^{4} v$ | $4 \beta g \tau_{,\phi}$ |
| 55 | $a c \rho^{4} v$ | $- \xi_{,\phi}$ |
| 56 | $a \rho^{4} v$ | $\eta_{,s\phi} - \tau_{,st}$ |
| 57 | $\ell^{2} \rho^{4} v$ | $2 \left(2 \beta g - 1\right) \xi_{,\phi}$ |
| 58 | $\ell \rho^{4} v$ | $- 4 \beta g \eta_{,t\phi} + 4 \beta g \xi_{,st} - \tau_{,tt} + 2 \eta_{,t\phi}$ |
| 59 | $R \rho^{4} v$ | $2 \beta g \xi_{,t}$ |
| 60 | $\rho^{4} v$ | $- g \left(\eta_{,\phi\phi\phi} - \tau_{,t\phi\phi} - 2 \xi_{,s\phi\phi}\right)$ |
| 61 | $a \ell \rho^{3} v$ | $\left(4 \beta g + 1\right) \tau_{,s}$ |
| 62 | $c \ell \rho^{3} v$ | $2 \beta g \xi_{,t}$ |
| 63 | $\ell \rho^{3} v$ | $- 2 g \left(2 \beta \eta_{,st} - \tau_{,\phi\phi}\right)$ |
| 64 | $c \rho^{3} v$ | $g \xi_{,\phi\phi}$ |
| 65 | $R \rho^{3} v$ | $- 2 \beta g \eta_{,t}$ |
| 66 | $\rho^{3} v$ | $- g \left(2 \eta_{,s\phi\phi} - \xi_{,ss\phi} - 2 \tau_{,st\phi}\right)$ |
| 67 | $\ell^{2} \rho^{2} v$ | $4 \beta g \eta_{,s}$ |
| 68 | $c \ell \rho^{2} v$ | $2 \beta g \eta_{,t}$ |
| 69 | $c \rho^{2} v$ | $g \left(\eta_{,\phi\phi} - \tau_{,t\phi}\right)$ |
| 70 | $R \rho^{2} v$ | $- 5 g \tau_{,\phi}$ |
| 71 | $V \rho^{2} v$ | $g \xi_{,\phi}$ |
| 72 | $\rho^{2} v$ | $- g \left(\eta_{,ss\phi} - \tau_{,sst}\right)$ |
| 73 | $c \ell \rho v$ | $10 g \tau_{,\phi}$ |
| 74 | $\ell \rho v$ | $- 2 g \tau_{,ss}$ |
| 75 | $c^{2} \rho v$ | $- 2 g \xi_{,\phi}$ |
| 76 | $c \rho v$ | $2 g \left(\eta_{,s\phi} - \tau_{,st}\right)$ |
| 77 | $R \rho v$ | $- 3 g \tau_{,s}$ |
| 78 | $c \ell v$ | $8 g \tau_{,s}$ |
| 79 | $a \rho^{6}$ | $- 4 \xi_{,t\phi}$ |
| 80 | $\rho^{6}$ | $- \xi_{,ttt}$ |
| 81 | $a^{2} \rho^{5}$ | $- 4 \tau_{,\phi}$ |
| 82 | $a \ell \rho^{5}$ | $- 4 \xi_{,\phi}$ |
| 83 | $a \rho^{5}$ | $- 3 \tau_{,tt} + 4 \eta_{,t\phi} - \xi_{,st}$ |
| 84 | $\ell \rho^{5}$ | $- 4 \xi_{,tt}$ |
| 85 | $U \rho^{5}$ | $- 3 \xi_{,t}$ |
| 86 | $\rho^{5}$ | $g \xi_{,t\phi\phi} + \eta_{,ttt}$ |
| 87 | $a^{2} \rho^{4}$ | $- \tau_{,s}$ |
| 88 | $a c \rho^{4}$ | $- \xi_{,t}$ |
| 89 | $a \rho^{4}$ | $g \tau_{,\phi\phi} + \eta_{,st}$ |
| 90 | $\ell^{2} \rho^{4}$ | $2 \left(\beta g - 1\right) \xi_{,t}$ |
| 91 | $\ell \rho^{4}$ | $g \xi_{,\phi\phi} + \eta_{,tt}$ |
| 92 | $\rho^{4}$ | $- g \left(\eta_{,t\phi\phi} - 2 \xi_{,st\phi}\right)$ |
| 93 | $a \ell \rho^{3}$ | $- \eta_{,s}$ |
| 94 | $a \rho^{3}$ | $2 g \tau_{,s\phi}$ |
| 95 | $\ell^{2} \rho^{3}$ | $- 2 \beta g \eta_{,t}$ |
| 96 | $\ell \rho^{3}$ | $2 g \tau_{,t\phi}$ |
| 97 | $c \rho^{3}$ | $g \xi_{,t\phi}$ |
| 98 | $U \rho^{3}$ | $2 g \tau_{,\phi}$ |
| 99 | $R \rho^{3}$ | $- g \xi_{,\phi}$ |
| 100 | $\rho^{3}$ | $- g \left(- \xi_{,sst} + 2 \eta_{,st\phi}\right)$ |
| 101 | $a c \rho^{2}$ | $- g \tau_{,\phi}$ |
| 102 | $a \rho^{2}$ | $g \tau_{,ss}$ |
| 103 | $\ell^{2} \rho^{2}$ | $- 2 g \tau_{,\phi}$ |
| 104 | $c \ell \rho^{2}$ | $3 g \xi_{,\phi}$ |
| 105 | $\ell \rho^{2}$ | $g \left(- \xi_{,ss} + 2 \eta_{,s\phi} + 2 \tau_{,st}\right)$ |
| 106 | $c \rho^{2}$ | $g \eta_{,t\phi}$ |
| 107 | $U \rho^{2}$ | $2 g \tau_{,s}$ |
| 108 | $R \rho^{2}$ | $g \left(3 \eta_{,\phi} - 2 \tau_{,t} - \xi_{,s}\right)$ |
| 109 | $V \rho^{2}$ | $g \xi_{,t}$ |
| 110 | $\rho^{2}$ | $- g \eta_{,sst}$ |
| 111 | $a c \rho$ | $- 2 g \tau_{,s}$ |
| 112 | $\ell^{2} \rho$ | $- 4 g \tau_{,s}$ |
| 113 | $c \ell \rho$ | $- 2 g \left(3 \eta_{,\phi} - 2 \tau_{,t} - \xi_{,s}\right)$ |
| 114 | $\ell \rho$ | $2 g \eta_{,ss}$ |
| 115 | $c^{2} \rho$ | $- 2 g \xi_{,t}$ |
| 116 | $c \rho$ | $2 g \eta_{,st}$ |
| 117 | $R \rho$ | $3 g \eta_{,s}$ |
| 118 | $c \ell$ | $- 8 g \eta_{,s}$ |

## Bibliography

References are written manually in the sequential numerical form of GB/T 7714. The book edition is the edition actually supplied: Olver's 1986 first edition.

[1] OLVER P J. Applications of Lie groups to differential equations[M]. New York: Springer-Verlag, 1986. DOI: [10.1007/978-1-4684-0274-2](https://doi.org/10.1007/978-1-4684-0274-2).

[2] OLIVERI F. Lie symmetries of differential equations: theory, applications, and symbolic computation[M]. Cham: Birkhäuser, 2026. DOI: [10.1007/978-3-032-12791-4](https://doi.org/10.1007/978-3-032-12791-4).

[3] PALIATHANASIS A, LEON G, LEACH P G L. Lie symmetries and similarity solutions for a shallow-water model with bed elevation in Lagrange variables[J]. Mathematics, 2026, 14(3): 433. DOI: [10.3390/math14030433](https://doi.org/10.3390/math14030433).

### Source integration and reference locations

The two supplied working texts are the existing hand-calculation manuscript and the fuller Chinese derivation. They are unpublished working sources, not additional published research references. The present version integrates their material, translates every Chinese explanatory passage, preserves the worksheet calculations, and records substantive corrections in Section 17.3.

Olver [1], Section 1.4, supplies the subgroup–subalgebra framework; Section 2.3, Theorem 2.31, and Section 2.6 supply the infinitesimal criterion and its regularity and local-solvability qualifications; Section 3.3 supplies the adjoint-classification framework. Oliveri [2], Sections 4.2–4.3, supplies prolongation and the infinitesimal criterion; Sections 5.4 and 5.6 treat order reduction and second-order linearization; Sections 6.3 and 6.8 treat invariant PDE solutions and classification.

The v3 article [3] was inspected at its printed page 2 for Equations (1)–(7), pages 4–6 for the reported generators and Tables 1–3, page 7 for the typeset Equations (25)–(27), and pages 7–8 for the traveling-wave discussion. In particular, the $\sigma\mu'$ baseline products in Equation (26) were checked visually rather than inferred from extracted text.

The reduction methods are classical. The propositions here establish the stated algebraic and local geometric claims for the normalized scalar equation. They do not assert novelty, a global solution classification, a physical SVE equivalence absent the transport term, or a general elementary solution of the Abel equation.
