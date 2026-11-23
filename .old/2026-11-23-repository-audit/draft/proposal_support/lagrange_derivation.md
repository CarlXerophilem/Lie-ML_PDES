# Lagrangian Proposal: Derivation and Evidence Boundaries

Current basis: Paliathanasis, Leon and Leach (2026), DOI
`10.3390/math14030433`, specifically printed Eq. (7), Proposition 1,
Table 3 and Sections 3.4-3.6/3.9. This replaces the earlier 2022-based
Eulerian near-cubic proposal. It does not replace or invalidate the old
computations on their own stated model.

Update 2026-09-12: `../draft.tex` now gives the formal pre-study write-up;
`../research_record.md` fixes the core claims and eight-week 2027 scope.
The conditional argument below is retained and strengthened there by an
exact-rational L=15 box bound and a first-exit continuation theorem.

## 1. The Beginner-Facing Connection

An Eulerian observer fixes a location x and watches fluid pass through it.
A Lagrangian observer follows a fluid label s. The function phi(t,s) is
the position of that label. Its time derivative is velocity; its label
derivative measures spacing between neighboring fluid parcels. Thus
u=phi_t and h=1/phi_s, with phi_s>0 required to avoid a folded map.

For the source's cubic symmetry, t is multiplied by exp(epsilon) while
s is multiplied by exp(-2 epsilon). Their product sigma=s*t^2 stays
unchanged. Choosing phi=F(sigma) restricts the PDE to an invariant family.
This is variable compression: one profile F replaces an arbitrary function
of two independent variables. It does not describe all PDE solutions.

The semi-analytical stage computes derivatives of F from its reduced ODE
and forms a finite Taylor polynomial. The neural stage approximates the
remaining profile shape. Neither stage discovers symmetries. A good Taylor
or classical solver may make the network unnecessary; the comparison must
be allowed to show that.

## 2. Model Audit Comes Before Physical Claims

Let b(t,s)=B(t,phi(t,s)), J=phi_s>0, u=phi_t. The chain rule gives

\[
\partial_x=J^{-1}\partial_s,\qquad
(\partial_t)_x=(\partial_t)_s-(u/J)\partial_s.
\]

The source's Eulerian Exner Eq. (4), B_t+beta*u^(m-1)*u_x=0,
therefore becomes

\[
b_t-(\phi_t/\phi_s)b_s+
\beta\phi_t^{m-1}\phi_{ts}/\phi_s=0. \tag{L-Exner}
\]

The middle term is absent from its printed Eq. (6), under this ordinary
bed-field pullback. Its printed Eq. (5) does agree with the transformed
momentum equation. With

\[
A=\phi_s\phi_{tt}-g\phi_{ss}/\phi_s^2,
\]

the printed pair specifies b_s=-A/g and
b_t=-beta*phi_t^(m-1)*phi_ts/phi_s. Its compatibility condition is

\[
E_m=A_t-g\beta\partial_s
(\phi_t^{m-1}\phi_{ts}/\phi_s)=0,
\]

which is exactly printed Eq. (7). A smooth solution on a simply connected
regular domain reconstructs a bed for the *printed pair*, up to one
additive constant. A small master residual alone does not supply a
path-independent approximate bed or a bound for that bed.

Including the missing transport term instead produces the compatibility
equation E_m-partial_s(phi_t*A/phi_s)=0. This is a different PDE. No
symmetry classification, similarity formula or numerical result for the
printed equation is automatically a result for the corrected equation.
The user confirmed on 2026-09-12 that the proposal studies the printed
equation with this limitation explicit. The model audit is retained;
correcting the physical model is outside the current scope and requires
a separate decision. Work on the printed equation does not depend on
resolving that correction first.

## 3. Direct Cubic Reduction

Fix m=3 and g,beta>0. The source defines beta=m*A_g*xi; beta is not the
coefficient of a derivative of u^m. All numerical parameters are
dimensionless. On t>0, sigma=s*t^2>0, write phi=F(sigma), r=F', v=F''.
Then

\[
\phi_s=t^2r,\quad \phi_t=2\sigma r/t,\quad
\phi_{tt}=(2\sigma r+4\sigma^2v)/t^2.
\]

Consequently

\[
A=2\sigma r^2+4\sigma^2rv-gv/r^2,
\qquad C=8\sigma^2r(r+\sigma v),
\]

and direct substitution gives the arbitrary-profile identity

\[
tE_3[F(st^2)]=2\sigma A'-g\beta C'=aF'''+b=:R[F],
\]

where

\[
a=8(1-g\beta)\sigma^3r-2g\sigma/r^2,
\]
\[
b=4\sigma(1-4g\beta)r^2+8\sigma^2(3-5g\beta)rv+
\{8\sigma^3(1-g\beta)+4g\sigma/r^3\}v^2.
\]

`verify_lagrange.py` differentiates the original master expression for an
arbitrary symbolic F and checks this identity, rather than checking only
one exact solution or copying printed Eq. (25).

Where r>0 and a!=0, the reduced state Y=(F,r,v) satisfies
Y'=G=(r,v,-b/a). Its leading-coefficient zero set is
4*(1-g*beta)*sigma^2*r^3=g. Division there is not allowed. Local IVP
existence follows from smoothness off this set; numerical samples alone
do not certify continuation over an entire interval.

## 4. Conditional Error Estimate and Proof

Fix I=[sigma_0,sigma_1], length ell, and the vector infinity norm.
Suppose the exact state Y and trial state Yhat=(Fhat,Fhat',Fhat'')
remain in a common regular region in which G is uniformly L-Lipschitz
in its state. For example, a convex compact state tube with a proven
bound on the state Jacobian of G suffices. Require Fhat in C^3 and a
uniform normalized defect bound

\[
|Fhat'''+b(\sigma,Fhat',Fhat'')/a(\sigma,Fhat')|\le\varepsilon.
\]

If all three initial data match, variation of constants in integral form
and the Lipschitz inequality imply

\[
\|Yhat(\sigma)-Y(\sigma)\|_\infty
\le\int_{\sigma_0}^{\sigma}
\{L\|Yhat(\rho)-Y(\rho)\|_\infty+\varepsilon\}\,d\rho.
\]

Gronwall gives epsilon*(exp(L*ell)-1)/L, or epsilon*ell if L=0.
With an initial mismatch e0, add exp(L*ell)*e0. This is a classical
conditional ODE bound, not a new theorem or an already evaluated
interval certificate. A large/vacuous bound must be reported as such.

For Omega={(t,s): t_min<=t<=t_max, sigma_0<=s*t^2<=sigma_1},
the exact identity yields ||E_3[Fhat]||<=||R[Fhat]||/t_min.
If r and rhat share a positive lower bound r_min, their reconstructed
depths at the *same fluid labels* obey
|hhat-h|<=|rhat-r|/(t_min^2*r_min^2); velocity differences are at most
2*sigma_1*|rhat-r|/t_min. These are not fixed-Eulerian-location errors,
bed errors or a full-PDE solution-error theorem.

## 5. Exact Controls and a Negative Test

For g*beta<1/4, the positive real branch

\[
F_0=K\sigma^{1/3},\qquad K^3=27g/(1-4g\beta)
\]

has zero master residual, consistent with the root stated in source
Section 3.4. The executable control uses g=1,beta=0.1,K=cuberoot(45),
I=[1,1.5]. This stays away from sigma=0; it is not a shock calculation.

For a separate traveling-wave reduction, let phi=c*t+Phi(z), z=s-a*t,
r=Phi'>0, c-a*r>0 and a!=0. Direct substitution gives

\[
E_m=a(K_w(r)r')',\qquad
K_w(r)=g/r^2-a^2r+g\beta(c-ar)^{m-1}/r.
\]

Thus W(r)=integral K_w(r)dr satisfies W''=0. Local inversion requires
K_w!=0; constant profiles must not be lost by dividing by r'. The
linearization theme is prior work in source Sections 3.6 and 3.9.

For m=3,g=beta=1,a=-1,c=0, an explicit check is

\[
\phi=-\log(2-s-t),\qquad
b=s-\frac{1}{2(2-s-t)^2}.
\]

On 0<=s+t<=1, phi_s=phi_t=1/(2-s-t)>0 and K_w=1/r^2>0.
The printed momentum, bed and master residuals are identically zero.
Eulerian reconstruction gives

\[
h=e^{-x},\quad u=e^x,\quad
B=2-t-e^{-x}-\tfrac12 e^{2x}.
\]

Its mass and momentum balances vanish, but its Exner residual is
exp(3*x)-1, not identically zero. This exact symbolic counterexample
rules out unrestricted equivalence under the stated pullback convention.
It is a consistency finding about specific equations, not a blanket
judgment about the paper or its authors.

Another bounded source check: Section 3.8/Eq. (32) states a quadratic
restriction for phi=c*t+Phi(s), but printed Eq. (7) vanishes for any
smooth such Phi with Phi'>0. The code retains this check. We make no
claim to have audited the entire optimal system or maximal algebra.

## 6. Reproducible Pilot and Planned Neural Comparison

The pilot compares DOP853 with the analytic cubic state on 501 points.
A second IVP multiplies F0''(1) by 1.01, holding the other two initial
data fixed; m remains 3. DOP853 refinement changes both tolerances and
maximum step size. Radau supplies an independent integration algorithm.
Five-point finite differences of the computed state curve, with steps
0.001 and 0.0005 on [1.01,1.49], check derivative consistency without
substituting the ODE right-hand side as an observed derivative.

That diagnostic is a *state-ODE* defect, not direct third differentiation
of the interpolated position map. The arbitrary-profile PDE pullback is
verified symbolically. Tolerances, agreement and sampling are not
rigorous interval enclosures. Results, versions and script hash are in
`lagrange_evidence/report.json`; do not copy old Eulerian pilot numbers.

Let f=-b/a. Taylor data are F,r,v,f and
f_sigma+f_r*v+f_v*f at sigma_0. Compare P2 and P4 alone, classical
integration, and Fhat=P_N+z^(N+1)*N_theta(z), N=2 or 4. Both networks
match the same three initial data. N=4 adds two derivatives implied by
the ODE, but also changes the remainder factor and its conditioning.
This compares combined parameterizations, not the isolated effect of
Taylor order. A P2-plus-remainder hard-IVP ansatz alone is not a separate
novel Taylor method: it is also a standard way to enforce third-order
initial conditions.

Planned protocol: float64 CPU; two tanh hidden layers of width 16;
seeds 0,1,2; 128 uniform training points; 1001 separate uniform
evaluation points; Adam learning rate 0.001 for 5000 steps; then at most
200 L-BFGS iterations with function evaluations reported. Use the same
scaling, points and optimizer schedule for N=2 and N=4; this is not an
equal wall-clock budget. No solution labels in the
residual loss. Reject sampled F'<=0 or |a|<1e-6 as failed runs rather
than suppressing denominators. Independent dense evaluation still is
not an interval guarantee. At the initial protocol stage no networks had
been trained. Two subsequent 400-step one-seed CPU trials are now recorded
in `feasibility_20260912/`; they are not the formal multi-seed 2027 study.

Record F,F',F'' errors, normalized and unnormalized residuals, original
master residual, initial jets, derivative ranges, parameter count,
training/evaluation time and seeds. Use the same regular domain for all
arms. Do not compare only training loss or call a network faster while
excluding its training cost. Quantitative uniform Lipschitz/defect bounds
are a proposed next stage, not completed evidence.
