# Frozen affine conditional-distribution analysis

This Stage 3 calculation concerns only the 64 candidates recorded before
evaluation in `nonclassical_candidates.json`, for the full evolving-bed
2D cubic Grass model `G=f=0,m=3,g>0,K>0`. It is a finite proposal search,
not an unrestricted nonclassical classification. The source, tests, and
this note are new files; no Stage 1/2 source is altered.

## Implementation plan and interfaces

`nonclassical.py` exposes `analyze_candidate(candidate, require_gate=True)`,
`conditional_system(c,a,b)`, `invariant_graph(c,a,b)`, and `serialize_result`.
The candidate has exact rational `c`, four `a` coefficients, and four `b`
coefficients. Public evaluation checks the current Stage 2 gate. The root
owns the frozen registry, batch runner, ML certificate, and final release;
classical distribution equivalence and fresh review are independent tasks.

The steps are: derive the original PDE plus Q; verify the rank and bracket;
test the first-jet conditional criterion on regular and singular strata;
integrate Q and split the exact time-dependent PDE pullback; retain the
implicit profile DAE; verify explicit local families and regular Frobenius
compatibility; run bounded tests and retain their receipts. The review
focus is singular jets, parameter-uniform rejection, exact exponential
relations, real/wet/nonzero-speed domains, and the distinction between
invariance of a distribution and a special solution.

## 1. Original equations and projected rank

Let `U=(h,u,v,B)^T`, `p=U_x`, and write the original PDE as
`E=U_t+A(U)U_x+C(U)U_y=0`. The x matrix is

\[
A=\begin{pmatrix}
u&h&0&0\\g&u&0&g\\0&0&u&0\\
0&K(3u^2+v^2)&2Kuv&0
\end{pmatrix}.
\]

For `D=diag(a_h,a_u,a_v,a_B)` and `phi=DU+b`, take
`V1=partial_y` and `V2=partial_t+c partial_x+phi.partial_U`.
They commute. Their base projection has a constant nonzero `(t,y)` minor,
so its rank is two everywhere, independently of any profile or parameters.
The invariant-surface equations are

\[
Q_1=-U_y=0,\qquad Q_2=\phi-U_t-cU_x=0.
\]

Putting `M=A-cI`, the original equations on Q are the implicit first-order
system `J=Mp+phi=0`. Nothing has yet been divided out.

## 2. Conditional invariance is a first-jet tangency test

Define

\[
N=(\phi\cdot\partial_U)A+AD-DA.
\]

Direct first prolongation gives, on Q,

\[
\operatorname{pr}^{(1)}V_2(E)=D(Mp+\phi)+Np.
\]

The `V1` action vanishes. The conditional criterion therefore requires
`Np=0` for **every** first jet satisfying `Mp+phi=0` on the declared chart.
It is not enough to find one such jet, one solution graph, or a smaller
submanifold on which an extra obstruction happens to vanish.

The characteristic determinant is

\[
\det M=-(u-c)\{gK(3u^2+v^2)(u-c)
                    +c[(u-c)^2-gh]\}.
\]

On its nonzero stratum, `p=F=-adj(M)phi/det(M)`. The exact conditional
criterion is the polynomial identity `-N adj(M)phi=0`. Acceptance uses
symbolic zero identities, not sampling. Rejection for all `g,K>0` is
supported by a field-polynomial coefficient whose nonzero parameter
monomials all have the same sign. A rational compatible first-jet witness
illustrates that proof; it is not the proof of parameter coverage.

## 3. Necessary differentiated constraints, without a circular test

Writing `r=U_xx`, the differentiated Q equations give

\[
U_{tx}=Dp-cr,\quad U_{tt}=D\phi-2cDp+c^2r,
\quad U_{xy}=U_{yy}=U_{ty}=0.
\]

On these constraints,

\[
D_xE=Mr+[(p\cdot\partial_U)A]p+Dp,
\qquad(D_t+cD_x)E=D(Mp+\phi)+Np.
\]

Thus solutions of the prolonged joint system necessarily satisfy `Np=0`.
Imposing this extra condition and then testing only that smaller set would
turn mere compatibility into an apparent invariance claim. The program
instead tests all original joint first jets before imposing it.

On the regular stratum, an accepted candidate also satisfies the exact
Frobenius condition `[phi,F]=0`; indeed `M[phi,F]=-NF`. Consequently the
two smooth field flows commute locally. This is a local regular-branch
compatibility result, not a global solution or complete singular-DAE theorem.

## 4. Singular strata are retained

At `c=0`, `det M=-gK u^2(3u^2+v^2)`. Since `g,K>0` and speed is nonzero,
the singular locus is precisely `u=0,v!=0`.

For a pure nonzero depth shift, `phi=b_h e_h`, its bed equation forces
`p_u=0` there and the mass equation forces `b_h=0`, a contradiction.
More explicitly, `K v^2` times the mass row minus `h` times the bed row is
the nonzero quantity `K v^2 b_h`. There are no compatible singular first
jets. The regular conditional certificate therefore covers every compatible
jet on the declared wet/nonzero-speed domain.

For a pure velocity shift `phi=b_u e_u`, the same singular locus instead
admits `p_u=0`, `g(p_h+p_B)=-b_u`, with `p_h,p_v` free. Its prolonged mass
residual is `b_u p_h`, which need not vanish. The operator is certified only
on `u!=0`; it fails the full-chart first-jet criterion. A particular smooth
solution may cross `u=0` without repairing that failed distribution criterion.

For zero or pure bed-shift profiles `N=0` identically, including all singular
jets. On `u=c`, the joint equations reduce to
`p_u=0`, `p_B=-p_h`, and `c(p_h+2K v p_v)+b_B=0`.
The second characteristic factor is retained as another implicit DAE when
`u-c!=0`: `p_v=0`, `(u-c)p_h+h p_u=0`,
`g(p_h+p_B)+(u-c)p_u=0`, and `b_B=0`. Its higher compatibility conditions
are not silently dropped or replaced by a complete-profile claim.
Rejected ambient candidates retain their singular DAE with an explicit
unresolved status; their regular failure does not exclude special solutions.

## 5. Invariant graph and exact reduced equations

The remaining independent variable is `z=x-ct`. Each field has the exact
reconstruction

\[
U_i(t,x,y)=
\begin{cases}
e^{a_i t}F_i(z)+\dfrac{b_i}{a_i}(e^{a_i t}-1),&a_i\ne0,\\
F_i(z)+b_i t,&a_i=0.
\end{cases}
\]

The base Jacobian is one and the field Jacobian is
`exp((a_h+a_u+a_v+a_B)t)>0` for finite real t. There is no profile or
characteristic division. The code computes the original conservation-law
pullback and an independent matrix-chain-rule pullback, and verifies they
agree. Each row is a finite sum `t^k exp(r t)` with rational r. Collecting
equal rates and powers yields exact implicit coefficient equations in
`F,F_z`; distinct exponential-polynomial terms are linearly independent
on any open time interval. These equations reconstruct the original PDE
exactly even when the proposed conditional symmetry has failed.

## 6. Actual local solution branches and data

The two nonzero depth shifts at c=0 admit

\[
h=H_0+b_h t-b_hx/U_0,\quad u=U_0\ne0,\quad v=V_0,
\quad B=B_0+b_hx/U_0,
\]

on the interval/domain where h is positive. The velocity shifts admit

\[
h=H_0>0,\quad u=U_0+b_ut,\quad v=V_0,
\quad B=B_0-b_ux/g.
\]

Their conditional certification additionally requires `U_0+b_ut!=0`.
Both families are verified by direct differentiation in all four original
PDEs and both invariant-surface equations. Their t=0 profiles are retained.
Their existence alone does not establish novelty or distribution inequivalence.

For zero/bed-shift profiles, the regular traveling profiles have first
integrals `h(u-c)=J`, `(u-c)^2/2+g(h+B)=E0`, and
`K(u^3+V0^2 u)-cB+b_B z=S0`, with `v=V0`. The scalar implicit velocity
relation has nonzero derivative exactly on its regular chart, so the
implicit function theorem constructs a local profile through any admitted
initial root. Singular `u=c!=0` profiles are also explicitly retained:
`v=W(z)`, `h=H0-K W(z)^2-(b_B/c)z`, `B=b_B t+B0-h`, with arbitrary smooth
W and positive h. At `c=b_B=0`, the singular stationary transverse-shear
family is `u=0,v=W(x)!=0,h=H(x)>0,B=B0-H(x)`.

## 7. Status and evidence boundaries

`conditional_status` distinguishes full declared-chart certification,
regular-subchart certification, parameter-uniform failure, and unresolved
strata. `global_chart_admitted` is false for velocity shifts. Graph pullback,
compatible families, and independent review each have separate statuses.
Classical equivalence is deliberately left to the independent distribution
analysis. No training, novelty, unrestricted nonclassical classification,
or complete singular-profile theorem is claimed.

An initial exploratory algebra calculation took 22.47 seconds and was not
wrapped in an enforced subprocess timeout. It is a recorded workflow
limitation, not the official verification receipt. All subsequent official
checks use bounded subprocesses and preserve their logs and exit status.
