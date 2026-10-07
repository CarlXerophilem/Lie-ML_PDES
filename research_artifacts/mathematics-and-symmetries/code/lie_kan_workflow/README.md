# Seven-step Lie analyzer and a series-first KAN experiment

Start with `lie_analyzer.py`. It is a single **ML-free** script: its only external dependency is SymPy. The second script, `series_kan.py`, reviews the existing neural baseline by separating the effect of a coupled series, edge-KAN architecture, and iterative correction chain.

Here the requested spatial dimension range is interpreted as **integer d=1 or d=2**, plus time `t>0`. Noninteger spatial dimensions are rejected. The main input contract is one conservation/constraint equation and two main equations. Full 2D Grass SVE necessarily has four balances and is an explicitly declared extension; no bed equation is silently dropped.

## Installation and first run

Python 3.11/3.12 is suitable. For the analyzer alone:

```bash
python -m pip install sympy
python lie_analyzer.py --builtin swe2d --out results/my_swe2d.json
python lie_analyzer.py --self-test --out results/my_tests.json
```

For learning, install `requirements.txt`; CPU PyTorch can be installed from its CPU index. Set one thread when reproducing timing comparisons:

```bash
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python series_kan.py --verify-only
python series_kan.py --family flat --steps 600 --seeds 0 1 2 \
  --out results/my_flat_kan
python series_kan.py --family sve --steps 600 --seeds 0 1 2 \
  --out results/my_sve_kan
```

No pykan installation is required. The independently implemented Gaussian edge network is informed by inspected author code and uses analytic smooth functions. It is a conditional-field adaptation, not a reproduction of DeepOKAN's neural-operator experiments.

## The seven steps

| Step | What the script actually computes | What it does not assume |
|---|---|---|
| 1. Model and admissibility | Jet coordinates, exact parameters, declared leading-jet chart, nonzero determinant condition, domains | Every chart or parameter value is regular |
| 2. Prolong and determine | Recursive point prolongation through jet order 1–3; candidate tangency after on-shell restriction | A supplied candidate is already a symmetry |
| 3. Split and solve | Exact polynomial coefficient split and nullspace in a declared degree-0/1/2 ansatz | A finite ansatz is a maximal classification |
| 4. Verify and organize | Independent substitution of every discovered basis vector; nonzero commutators | Every subgroup preserves the initial/boundary problem |
| 5. Flows, invariants, charts | Exact augmented-matrix exponential representation for affine flows; explicit invariants/rank for supported reductions | One orbit direction reduces a 2+1 PDE to an ODE |
| 6. Reduce | A verified expansion chart, or a conditional x-translation reduction | Arbitrary data belong to an invariant solution family |
| 7. Reconstruct and check | Exact supplied ODE profile reconstructed into the original SWE; zero residual check | Every reduced PDE has a solved profile |

Time is recorded separately for these computations. A custom unsupported reduction is returned as unsupported/pending, not replaced with a fabricated solution. The expansion route completes all seven steps for a declared exact family. The translation route returns the reduced system and states the missing data/solution certificate.

The point generator coefficients depend on coordinates and fields within the polynomial ansatz; parameters are fixed under the action. Unknown parameter values use a generic symbolic kernel. **Recompute every exceptional stratum** instead of dividing by a factor and discarding it. Nonpolynomial splitting is explicitly unsupported; exact verification of supplied generators remains available. Mixed-order systems include differential consequences of lower-order equations through the common jet order, but general constrained systems can require further compatibility/involutive completion. The result states that limitation.

## Three-equation PDE input

The default two-spatial-coordinate SWE is

\[
\begin{aligned}
h_t+u h_x+v h_y+h(u_x+v_y)&=0,\\
u_t+u u_x+v u_y+g h_x-fv+\gamma u&=0,\\
v_t+u v_x+v v_y+g h_y+fu+\gamma v&=0.
\end{aligned}
\]

The 1D built-in retains transverse velocity `v`; it is a three-field 1D SWE, not the two-field h/u model. The optional `navier2d` example has divergence constraint plus two momentum equations and is only a related constrained-system control. The attached 3D Navier–Stokes manuscript is not treated as a shallow-water constitutive model.

Write an editable input and analyze it:

```bash
python lie_analyzer.py --builtin swe2d --write-example examples/my_pde.json
python lie_analyzer.py --input examples/my_pde.json --out results/custom.json
python lie_analyzer.py --input examples/time_dependent_swe.json \
  --verify-only --reduction none --out results/nonautonomous.json
python lie_analyzer.py --builtin sve2d --parameter m=3.1 \
  --verify-only --reduction none --out results/near_cubic.json
```

Use explicit independent-jet names: `h_t`, `h_x`, `u_xy`, `v_txx`, etc. `order` must cover all referenced jets. JSON specifies fields, parameters (exact strings or symbolic assumptions), equations, one leader per original equation, roles, and domains. Optional `generators` maps a name to a vector of coefficients ordered as `(independent variables, fields)`. Expressions use a restricted arithmetic DSL with `sin/cos/exp/log/sqrt/tanh`; attributes, imports, and arbitrary calls are rejected.

## Completed compatible reduction

For flat SWE, take `rho=1+a*t`, `a>=0`, and the commuting generators
`Xx=Tx+a*Gx`, `Xy=Ty+a*Gy`. Their spatial projected rank is two in 2D. The invariants are

\[
t,\quad h,\quad u-\frac{ax}{1+at},\quad v-\frac{ay}{1+at}.
\]

Substitute `h=H(t)`, `u=ax/rho+U(t)`, `v=ay/rho+V(t)`. The reduced equations are

\[
H'+\frac{2aH}{\rho}=0,\qquad U'+\frac{aU}{\rho}=0,\qquad V'+\frac{aV}{\rho}=0.
\]

Reconstruction gives `h=H0/rho^2`, `u=(ax+U0)/rho`, `v=(ay+V0)/rho`. The script verifies the original residuals exactly. The initial data and chart are explicit; this is a nonperiodic full-plane/local family, not a symmetry reduction of the benchmark's nonuniform periodic data. The 1D counterpart has `H=H0/rho` and constant transverse `V`.

For this analytic ODE family, the rational solution already exists: neural learning is unnecessary. Its Taylor expansion is valid locally for `|a*t|<1` when `a!=0`. This is a useful control for deciding when to stop at exact/series solving.

The reduced linear ODE also supplies a concrete function-iteration certificate. On `C([0,T];R^3)` in the sup norm, its Volterra map has contraction bound `kappa=d*log(1+a*T)`. For `a=.5,T=.25`, the script checks seven Picard iterates against the exact depth and a geometric error bound. This is a sufficient local bound for the supplied ODE; it does not prove convergence for the full PDE or for learned corrections.

## The half-way process before function-space operators

For the coupled evolution system `U_t=F(U;p)`, construct

\[
P_2=U_0+t a_1+t^2 a_2,\qquad
a_1=F(U_0;p),\qquad a_2=\tfrac12 DF(U_0;p)[a_1].
\]

`series_kan.py` derives all four coefficients symbolically and checks them against independent autograd. The bed's first time coefficient is zero for the constant initial velocity, but its second coefficient is generally nonzero because evolving velocity drives sediment transport. Water and sediment coefficients are therefore coupled from the start.

The correction is

\[
U_K=P_2+\frac{t^3}{T^2}S(p)\sum_{k=1}^{K}\alpha_k C_k(t,x,y;p).
\]

The factor preserves the initial value and the first two time derivatives exactly. Smooth Fourier features preserve periodicity. Each `C_k` composes edge-function layers

\[
z_j^{\ell+1}=\sum_i\left[a_{ji}z_i^\ell+
\sum_r c_{jir}\exp\!\left(-\frac{(z_i^\ell-\mu_r)^2}{\sigma^2}\right)\right]+b_j.
\]

The hidden normalization is smooth tanh. Gaussian/linear edges are C-infinity; finite third derivatives and first/second derivative consistency are tested. A cubic spline KAN is only C2 at simple knots and should not be silently substituted into the manuscript's classical third-order residual without a smoothness/weak-formulation decision.

For a correction chain, earlier blocks freeze while a new block trains against the **full nonlinear PDE residual**. Backtracking tries weights `1,.5,.25,.125,0` on separate physics points of the training family. Including zero preserves the previous accepted iterate. Reference solutions of test cases never select weights. This is a projected damped defect-correction experiment; it is not an exact Newton step or a proved contractive Picard iteration.

The default `--acceptance total` protects the total sampled validation loss. The optional `--acceptance per_equation` rejects a weight if any equation's validation MSE increases. The extra evolving-bed trial records both before/after vectors and retains rejected stages as zero corrections. Neither gate guarantees improvement in prediction error.

The optional `--sensitivity-weight 1 --sensitivity-step .01` adds a physics term for the parameter-sensitivity equation: central differences of the **full residual** at `p+epsilon` and `p-epsilon`, including both changed coefficients and changed predicted fields. It uses `m` for SVE and `f` for flat SWE. This is a finite-difference proxy for `d_p R=0`, not a reference-data loss or an exact parameter-gradient certificate. Its extra forward/derivative evaluations are included in measured training cost.

Picard's formal map is `T[V]=U0+integral(F(V;p))`. Its first local coefficients motivate the series. A Banach fixed-point argument would require a mapping and norm with a verified contraction. Spatial derivatives prevent assuming that F is Lipschitz from C0 to C0. This package does not transfer a contraction theorem, a convergence radius for the general PDE, or the attached NS manuscript's specialized residual-gain estimates.

## Controlled learning comparisons

| Method | Initial forward field | Architecture | Stages |
|---|---|---|---|
| `direct_mlp` | exact U0 | tanh MLP | 1 |
| `direct_kan` | exact U0 | smooth edge-KAN | 1 |
| `series_mlp` | exact P2 | tanh MLP remainder | 1 |
| `series_kan` | exact P2 | smooth edge-KAN remainder | 1 |
| `chain_mlp` | exact P2 | frozen MLP correction chain | 2 |
| `chain_kan` | exact P2 | frozen KAN correction chain | 2 |

Pure `P0`, `P1`, and `P2` controls are retained. One MLP has 2628 parameters and one KAN 2588. Two-block chains have twice that total capacity but the **same total optimization-step budget**, split between stages. The MLP chain controls for the effect of chaining; gains cannot automatically be attributed to KAN architecture. Methods share paired collocation points and seeds. Every last-layer output starts at zero, so direct and series initial forward fields are respectively U0 and P2 across architectures.

The basic family interpolates unseen `(Coriolis f, initial amplitude A)` pairs in three-field flat SWE. The evolving-bed family interpolates unseen `(Grass exponent m, amplitude A)` pairs with all four balances. Both train six pairs and test two disjoint pairs. These are finite-dimensional parameter-conditioned field approximations. They are not arbitrary-function solution operators, and KAN edge functions are not physical differential operators merely because they compose.

Exact algebra and data compatibility come before any group-conditioned learning. The exceptional m=3 algebra does not authorize applying its hard reduction to nearby exponents or to incompatible initial data. Use the full coordinates when reduction is unavailable. Do not cluster samples into Lie groups from a series fit; model/data symmetries determine the permitted actions.

## Review of the existing solver

The earlier spectral reference and residual modules were retained as `baseline_core` and rechecked through the new series tests. The Lie loss's residual-weighting identity remains an important control. The main weaknesses are the short-time/smooth domain, limited collocation/seed budgets, per-field sediment error, and the absence of function-space or shock guarantees.

A small whole-field relative error can conceal poor dynamics. This experiment records evolution errors, maximum active-field errors, mass/bed means, CPU costs, stage residuals, and pure-series controls. Acceptance of a stage guarantees only the sampled physics-validation objective does not increase; it does not guarantee test error decreases. Within-stage learning curves show proposals before backtracking; the accepted-stage scatter and final metrics identify the actual retained iterates.

Run the independent checks and post-hoc replay/sensitivity analysis with:

```bash
python solver_checks.py
python sensitivity_review.py results/sve_kan_pilot
python series_kan.py --family sve --methods chain_kan --acceptance per_equation \
  --steps 600 --seeds 0 1 2 --out results/my_component_gate
python series_kan.py --family sve --methods series_kan --sensitivity-weight 1 \
  --steps 600 --seeds 0 1 2 --out results/my_sensitivity_run
```

`solver_checks.py` tests exact uniform rotation/drag, a lake at rest, spectral interpolation, an independent finite-difference Grass-flux divergence, refinement, and conservation. `sensitivity_review.py` replays saved checkpoints and compares central parameter differences with refined numerical differences. It reports reference derivative scales because tiny derivatives can make relative sensitivity errors ill-conditioned. The series generator currently covers the documented sinusoidal wave family; it does not automatically expand arbitrary input functions.

The scalar master equation remains a separate printed model with third-order derivatives and a special cubic subgroup. This experiment does not assert that its physical elimination or invariant chart transfers unchanged to the four-field 2D system.

## Sources and deliverables

`SOURCE_AUDIT.json` records inspected GitHub commits, source hashes, provenance, and license status. Author code was inspected without redistributing unlicensed source files. Relevant primary sources:

- [DeepOKAN paper](https://arxiv.org/abs/2405.19143) and [author code](https://github.com/DiabAbu/DeepOKAN).
- [pykan author repository](https://github.com/KindXiaoming/pykan), for edge activations and scientific examples.
- [LPSDA author repository](https://github.com/brandstetter-johannes/LPSDA), a related symmetry augmentation method, not the Lie-PINN implementation.
- [SymPy Lie-group documentation](https://docs.sympy.org/latest/modules/solvers/ode.html), which documents ODE heuristics rather than a universal PDE classifier.
- The user's uploaded `main.tex` workflow and `navier-stokes-c,d.pdf`, section 9, for the distinction between compatible reduction and iterative residual correction.

`REVIEW_AND_RESULTS.md` gives measured outcomes, including failures of undamped KAN correction. `results/` contains analyzer traces, derivative verification, per-seed learning histories, stage decisions, numerical refinement diagnostics, predictions, and checkpoints. Exact installation versions used in the pilot are supplied separately.
