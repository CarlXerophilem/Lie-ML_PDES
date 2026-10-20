# Reading and Defending the Near-Cubic SVE Proposal

**Historical scope:** this document supports the earlier 2022-based Eulerian
near-cubic proposal. The active 2026 Lagrangian basis is in
[lagrange_derivation.md](lagrange_derivation.md). Do not transfer these
results to the printed Lagrangian master equation.

This is a teaching and verification companion, not part of the six-page limit.
The proposition is a local correctness result built from classical facts. Its
SVE-specific construction is not claimed novel without a stronger literature
comparison. No neural network has been trained for the submission pilot.

## 1. The Question Before the Techniques

The question is not "Can a neural network solve fluid equations?" It is:

> Starting from a known special solution family selected by a Lie symmetry,
> can we derive a small correction system when a model exponent changes, and
> then test a neural approximation of those specific correction functions?

There are three different objects: the original PDE, its selected exact cubic
solution family, and a first-order approximation for nearby exponents. We do
not identify any of them with the set of all physical fluid solutions.

All coordinates and fields below are dimensionless, using fixed reference
scales before the exponent is varied. This makes logarithms meaningful and
keeps the meaning of the fixed coefficient kappa consistent. This convention
is not a proposed contribution in dimensional analysis.

## 2. What the Three Equations Say

Let h(t,x) be water depth, u(t,x) velocity, and B(t,x) bed elevation. Use

\[
h_t+(hu)_x=0,\quad u_t+u u_x+g(h+B)_x=0,\quad
B_t+\kappa(u^{3+\delta})_x=0. \tag{1}
\]

Depth and velocity are positive on the region under discussion, g,kappa>0
are fixed, and delta changes only the transport exponent. The first equation
balances water mass, the second is the smooth velocity form of momentum
balance, and the third describes bed change driven by sediment transport.
There is no drag perturbation, viscosity, thermal equation, or experimental
parameter identification in this submission.

An initial value selects a solution; it is not an optional piece of the
mathematical problem. We use local smooth profiles and then restrict them to
a compact observation window. We do not solve an independently prescribed
boundary-value problem on that window.

## 3. From a Lie Generator to the Ansatz

At delta=0, consider the one-parameter transformations

\[
(t,x,h,u,B)\longmapsto(t,e^\rho x,e^{2\rho}h,e^\rho u,e^{2\rho}B).
\]

Differentiate with respect to rho at rho=0. This gives the generator

\[
X=x\partial_x+2h\partial_h+u\partial_u+2B\partial_B.
\]

This is the promised "variable compression": t, h/x^2, u/x, and B/x^2
are unchanged by this transformation. A solution that is itself unchanged
along these group orbits must therefore have the form

\[
h=x^2H(t),\qquad u=xv(t),\qquad B=x^2C(t). \tag{2}
\]

Equivalently, the invariant-surface conditions are 2h-x h_x=0,
u-x u_x=0, and 2B-x B_x=0. Integrating them in x gives (2).
The group maps solutions to solutions; the invariant-surface conditions
select solutions that the group fixes. These are different statements.

For example, (hu)_x=(x^3Hv)_x=3x^2Hv, so the first PDE becomes
x^2(H'+3Hv)=0. On x>0 this gives H'=-3Hv. All three equations yield

\[
Y_0'=f(Y_0),\quad Y_0=(H,v,C)^T,\quad
f(Y_0)=(-3Hv,-v^2-2g(H+C),-3\kappa v^3)^T. \tag{3}
\]

The interval [1,2] is not preserved by arbitrary scaling. It is an observation
window cut from the family defined on x>0, not evidence of symmetry-compatible
arbitrary boundary data. Boundary traces, if used, must be taken from the
constructed family and may depend on delta.

### Why the Exponent Three Is Special

For the restricted diagonal transformation with weights (a,b,c,d,e) on
(t,x,u,h,B), invariance at fixed g,kappa implies

\[
c=b-a,\qquad d=e=2c,\qquad (m-3)c=0. \tag{4}
\]

One can obtain these equations by prolonging the diagonal generator, or by
tracking its action on each derivative term. When m=3, nonzero amplitude
scaling is possible. When m is not three, this restricted class has c=0 and
b=a: simultaneous t,x dilation still survives. No claim is made here about
the completeness of all possible point-symmetry generators.

The cubic structure is known in Paliathanasis (2022). The printed generator
weights and exact coefficients are not imported unchecked; see `references.md`
for the particular discrepancies and direct-substitution checks.

## 4. Why a Logarithm Appears

For a positive dimensionless number a,

\[
a^{3+\delta}=a^3\exp(\delta\log a)
=a^3[1+\delta\log a+O(\delta^2)].
\]

For the cubic velocity a=xv(t), log a=log x+log v(t). That is the source of
the spatial logarithm. We do not add it just because it looks convenient.
Use p=Y_1, q=Y_log, ell=log x, and D(x)=diag(x^2,x,x^2):

\[
W_\delta=D(x)[Y_0(t)+\delta(p(t)+\ell q(t))]. \tag{5}
\]

Here p and q each have three components ordered (depth, velocity, bed).
The correction has six unknown functions of time, not six additional fields
depending freely on both x and t. Formula (5) is a first-order perturbative
ansatz, not an exact invariant ansatz for the noncubic PDE.

The linearized transport flux is

\[
u^{3+\delta}=x^3\{v^3+\delta[3v^2(p_v+\ell q_v)
+v^3(\ell+\log v)]\}+O(\delta^2).
\]

Differentiating the logarithm as well as x^3 matters. In particular,
(x^3 log x)_x=x^2(3 log x+1); the extra 1 must not be dropped.

## 5. The Six Equations, Without Hidden Elimination

Separate the coefficients of delta*log x and delta in each original balance:

\[
\begin{aligned}
q_H'&=-3v q_H-3Hq_v,\\
q_v'&=-2v q_v-2g(q_H+q_C),\\
q_C'&=-9\kappa v^2q_v-3\kappa v^3,\\
p_H'&=-3v p_H-3Hp_v-vq_H-Hq_v,\\
p_v'&=-2v p_v-2g(p_H+p_C)-vq_v-g(q_H+q_C),\\
p_C'&=-9\kappa v^2p_v-3\kappa v^2q_v-\kappa v^3(1+3\log v).
\end{aligned} \tag{6}
\]

These have the triangular form

\[
q'=Jq+b,\qquad p'=Jp+Kq+c, \tag{7}
\]

where

\[
J=\begin{pmatrix}-3v&-3H&0\\-2g&-2v&-2g\\0&-9\kappa v^2&0\end{pmatrix},\quad
K=\begin{pmatrix}-v&-H&0\\-g&-v&-g\\0&-3\kappa v^2&0\end{pmatrix},
\]
\[
b=(0,0,-3\kappa v^3)^T,\qquad
c=(0,0,-\kappa v^3[1+3\log v])^T.
\]

First solve the baseline, then q, then p; alternatively solve all six
corrections together. The coefficient of (q',p') is I_6. There is no need to
invert J. A zero determinant of J is not a singular derivative constraint.
This is different from a characteristic x/t reduction in which a matrix
such as A(Y)-zI might have to be inverted.

For the pilot p(1)=q(1)=0. Thus W_delta(1,x)=W_0(1,x) exactly for every
delta: the exponent changes but the initial fields do not. Arbitrary fixed
finite correction initial values are also permitted by the proposition;
they describe a different, first-order parameter dependence of initial data.

## 6. Main Proposition and Proof

**Proposition (regular first-order corrections and uniform residual order).**
Let I=[t0,T] be compact. Suppose Y0 solves (3), is smooth on I, and
H(t)>=H_min>0, v(t)>=v_min>0 there. Let Kx=[a,b] with 0<a<b<infinity,
and fix finite initial values p(t0),q(t0), independent of delta.
Then (7) has a unique C^1 solution on I. There are delta0>0 and C_*<infinity
such that, for |delta|<=delta0, the fields (5) have positive depth and velocity,
3+delta>0, and

\[
\sup_{(t,x)\in I\times K_x}\|F_\delta[W_\delta](t,x)\|_\infty
\le C_*\delta^2. \tag{8}
\]

Here F_delta is precisely the three-component original residual (1), and
the norm takes the maximum over its components.

**Proof.** Smooth bounded baseline profiles and v>=v_min make J,K,b,c
continuous on I. The six equations form a finite-dimensional linear
inhomogeneous IVP. The linear ODE existence/uniqueness theorem gives its
unique solution on the whole compact interval. Both corrections and their
first derivatives are bounded there.

Let E_H=sup|p_H+log(x)q_H| and E_v=sup|p_v+log(x)q_v| on I x Kx.
They are finite because a>0 and b<infinity. Choose delta0<1 small enough
that delta0*E_H<=H_min/2 and delta0*E_v<=v_min/2. If one E is zero,
the corresponding restriction is unnecessary. The reconstructed scaled
depth and velocity stay uniformly positive, and 3+delta>0.

Define `R(delta,t,x)=F_delta[W_delta](t,x)`. On the resulting compact set,
R has a continuous bounded second derivative in delta: all real powers and
logarithms have uniformly positive arguments, and the needed time/space
derivatives of (5) are continuous. Direct coefficient identities (3),(6)
give R(0,t,x)=0 and partial_delta R(0,t,x)=0. Taylor's integral remainder
therefore gives (8), with C_*=one half of the supremum of the componentwise
second derivative on [-delta0,delta0] x I x Kx. The same proof covers
positive and negative delta. QED.

This is a proof of existence of a finite constant, not a floating-point
evaluation of a rigorous numerical C_*. The proof uses classical facts;
its packaging is not itself a novelty claim.

### What Is Not Proved

- No exact solution of the noncubic PDE has been constructed by (5).
- No O(delta^2) distance to an exact PDE solution follows from (8) alone.
- No existence theorem for arbitrary fixed boundary data, no shock result,
  and no global-in-time stability result is claimed.
- No approximate symmetry generator or maximal Lie classification is proved.
- A large sampled error or failed bound is not a proof of blow-up.

For orientation only, the positive-state quasilinear PDE has coefficient
matrix A=[[u,h,0],[g,u,g],[0,kappa*m*u^(m-1),0]]. The diagonal matrix
S=diag(g/h,1,g/(kappa*m*u^(m-1))) is positive for h,u,g,kappa,m>0 and
SA is symmetric. This is an algebraic entry point to local hyperbolic
well-posedness theory, not a completed initial-boundary-value analysis.

## 7. Reproducible Initial Evidence

The control is g=1, kappa=0.1 and

\[
Y_0(t)=\left(\frac{1}{15t^2},\frac{2}{3t},\frac{2}{45t^2}\right)^T.
\]

It solves all three baseline equations. I=[1,1.5], Kx=[1,2], p(1)=q(1)=0.
The reference is DOP853, first with rtol=1e-11/atol=1e-13 and then with
rtol=1e-12/atol=1e-14. Evaluate 101 time points and 61 spatial points;
test delta=+/-{0.08,0.04,0.02,0.01,0.005}.

The numerical residual uses fourth-order five-point time differences of
the returned dense solution, including one-sided endpoint formulas.
Spatial derivatives are direct derivatives of (5). The time-difference
steps are 1e-4,5e-5,2.5e-5. The derivative is not replaced by (6): doing
that would hide a wrong approximation. A deliberately perturbed curve tests
that this protocol actually detects a correction-equation defect.

The uncorrected cubic family is the negative control. Its first-order bed
defect is kappa*x^2*v^3*[1+3 log(xv)], generically nonzero. It is expected
to show order one, not order two. Vanishing at an isolated point is not a
counterexample to this generic statement.

Run from the repository root:

```powershell
python -B draft/proposal_support/verify_corrections.py --output-dir draft/proposal_support/evidence
python -B -m unittest discover -s draft/proposal_support -p test_verify_corrections.py -v
```

`evidence/report.json` records versions, the script hash, settings, every
gate, both signs, all residual components, and refinement differences.
The proposal table and numbers are generated from that record. The plot
`evidence/residual_scaling.pdf` visualizes the measured order; it does not
show error relative to an exact noncubic PDE solution.

### An Independent Reference Specific to This Control

This exact baseline is simple enough to admit a matrix-exponential oracle.
Set s=log t, Q=diag(t^2,t,t^2)q, P=diag(t^2,t,t^2)p. Then
Q_s=M Q+b0 and P_s=M P+N Q+c0+s*c1, with

\[
M=\begin{pmatrix}0&-1/5&0\\-2&-1/3&-2\\0&-2/5&2\end{pmatrix},\quad
N=\begin{pmatrix}-2/3&-1/15&0\\-1&-2/3&-1\\0&-2/15&0\end{pmatrix},
\]

b0=(0,0,-4/45), c0=(0,0,-4[1+3log(2/3)]/135), c1=(0,0,4/45).
Augment (Q,P,s,1) to an eight-dimensional constant linear system, and use
scipy.linalg.expm. This independently checks the adaptive integrator.
It also makes clear that this pilot is a cheap classical control, not
evidence that neural computation is necessary.

## 8. What the Network Will Learn, and What It Cannot Inherit

The planned network learns w=(q,p), six functions of time. It does not
discover the supplied generator, and it does not learn arbitrary PDE
solutions. Let G(t,w) denote the right side of (7). If learned corrections
have coefficient defects

\[
r_q=\widehat q'-J\widehat q-b,\qquad
r_p=\widehat p'-J\widehat p-K\widehat q-c,
\]

then direct expansion gives

\[
F_\delta[\widehat W_\delta]
=\delta D(x)[r_p+\log x\,r_q]+O(\delta^2). \tag{9}
\]

Thus a bounded coefficient defect epsilon produces a residual contribution
O(|delta|*epsilon), in addition to the perturbation truncation. A fixed
nonzero neural defect will eventually obscure quadratic scaling as delta
tends to zero. Training on the six coefficient equations avoids the small
delta factor hiding this problem. It does not eliminate the problem by fiat.

The future comparison is fixed as follows, but is NOT performed in this pilot:

- Compare second-order time Taylor truncation, adaptive ODE integration,
  an initial-value-constrained PINN, and a Taylor-plus-PINN.
- Use z=(t-1)/0.5 and w0=0. Define D_w=diag(1/15,2/3,2/45) repeated twice.
  The plain trial is (t-1)D_w N_theta(z); the hybrid is
  P2(t)+z^3 D_w N_theta(z), where P2=w0+(t-1)G0+
  (t-1)^2*(G_t+G_w G)_0/2. These are time-series coefficients, distinct
  from the first-order expansion in the transport exponent.
- Both networks have two hidden layers of width 16, tanh activation and
  six outputs, with seeds 0,1,2. Use 128 midpoint collocation points,
  Adam at 1e-3 for 2000 steps, then L-BFGS with max_iter=200 and a
  strong-Wolfe line search; record actual closure evaluations and time.
- Minimize mean squared D_w^(-1)[w_theta'-G(t,w_theta)]. No reference
  solution values enter training. Evaluate on a distinct 1001-point time
  grid and the corresponding reconstructed spatial grid.
- Report componentwise absolute and scaled RMS profile errors against the
  classical correction reference, coefficient defects, original PDE
  residuals, positivity checks, and setup/training/evaluation costs.
- Reconstructed-field differences from the classical truncated ansatz are
  not errors against an exact noncubic PDE solution. Neural superiority
  is not required; a correctly measured negative comparison is informative.

## 9. A Short Oral-Defense Route

1. Explain what h,u,B represent and which equation the exponent changes.
2. Show how the scaling flow gives h/x^2,u/x,B/x^2 and hence three ODEs.
3. Explain why m=3 is special without claiming all other symmetry disappears.
4. Derive the log term by differentiating a power with respect to its exponent.
5. Explain why identity times the correction derivative means no hidden DAE.
6. State exactly what the proposition bounds, and what it does not bound.
7. Point to the independent numerical derivative and negative-control tests.
8. State that ML approximates correction profiles and must be compared fairly.

Do not conflate the group parameter rho, exponent perturbation delta,
time coordinate z, Taylor order N, and network parameters theta.

The archived source/PDF in `archive/` preserve the pre-revision annotated
draft byte-for-byte. `references.md` records the bounded source audit.
