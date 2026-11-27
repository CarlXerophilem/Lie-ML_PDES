<!-- Math rendering: GitHub MathJax / KaTeX compatible LaTeX. Use $...$ or standalone $$ blocks; no custom macros or injected scripts. -->

# `@delivery` User Manual: Symbolic PDE-to-ODE Reduction & Unparsed ML Pipeline

`delivery/` contains the executable symbolic Lie-symmetry reducer, in-memory AST numerical/ML profile solvers, planar transcritical Briot–Bouquet ODE benchmark suite, verification logs, and PDF build scripts for the dissertation ([`../draft/dissertation_wku_compact.tex`](../draft/dissertation_wku_compact.tex)) and defense slides ([`../draft/defense_wku_madrid.tex`](../draft/defense_wku_madrid.tex)).

---

## 1. How It Works

On a verified transverse invariant chart the pipeline maps a system of nonlinear PDEs to reduced ODEs and numerical/learned profiles in five strictly symbolic-to-AST stages, without parsing PDE formula strings, preset ODE profiles, or hardcoded similarity coordinates in the symbolic core:

1. **Complete Jet-Space Specification (`lie_reduce/jets.py`, `lie_reduce/spec.py`)**:
   A PDE system $\Delta(x, u^{(k)}; \mu) = 0$ is compiled directly in SymPy on a complete jet space $J^k(\mathbb{R}^d, \mathbb{R}^m)$ via `JetSpace` and `PDESpec`. `PDESpec.shell_certificate()` verifies a square, explicitly solvable principal derivative block, nonvanishing principal Jacobian on shell, and nonvanishing denominators on the declared positive cone.
2. **Infinitesimal Prolongation & Parameter Strata (`lie_reduce/determining.py`, `lie_reduce/hidden.py`)**:
   Point generators $X = \xi^i(x,u)\partial_{x_i} + \eta^a(x,u)\partial_{u^a}$ are prolonged to order $k$ via total derivatives $D_i$ and constrained by $\mathrm{pr}^{(k)}X(\Delta)\big|_{\Delta=0}=0$. Symbolic affine powers such as $u^m$ and $(u^2+v^2)^{(m-1)/2}$ are normalized into independent positive base symbols before polynomial jet splitting.
   - `--smooth-check` runs automated Spencer second-partial elimination (`smooth_symmetries`) to prove unrestricted smooth point symmetries reduce to affine polynomial form (established on $E_1$, $P$, and $M$ for all real $m \ge 1$).
   - `--strata` extracts exact pivot-minor factors of $\mathsf{A}(\mu)a = 0$ and power resonances, deciding every candidate jump stratum by exact specialization (`{E1: [0,3], P: [0,1,3], M: [0,3]}`).
3. **Canonical Basis & Subalgebra Enumeration (`lie_reduce/algebra.py`)**:
   Discovered generators are RREF-normalized into a deterministic basis (`X1..Xn` or `Y1..Yn`). Closed, projectable rank $d-1$ subalgebras $[\mathfrak{h}, \mathfrak{h}] \subset \mathfrak{h}$ are enumerated from basis singletons and symbolic linear combinations $X_i + \alpha_1 X_j$.
4. **Matrix-Exponential Orbit Quotient & First-Integral Elimination (`lie_reduce/multid.py`, `lie_reduce/reduce.py`)**:
   A transverse coordinate slice and matrix-exponential flows construct the orbit chart and invariant surface. Check the reduction identity:

   $$
   \Delta(z,\mathbf{v})=\mathsf{M}(z,\mathbf{v})\,\mathcal{E}[F](z).
   $$

   The matrix must be independent of the profile, with determinant nonzero on the local chart. Search the integrating factors from $\{1,z,z^{-1},z^2\}$ using the Euler operator:

   $$
   \mathsf{E}_a(\mu_{\ell}\mathcal{E})=0
   \quad\Longrightarrow\quad
   \mathcal{I}_{\ell}(z,F,F')=C_{\ell}.
   $$

   First integrals eliminate algebraic and cyclic profiles when possible while retaining the symbolic physical and integration parameters.
5. **Unparsed In-Memory AST-to-Solver Handoff (`_profile_learning.py`, `planar/model.py`, `planar/classical.py`, `planar/bench.py`)**:
   - **Regular branches ($\Delta_c \neq 0$)**: `Case.from_reduction` compiles the live SymPy `ReducedODE` AST directly in-memory (`sp.lambdify` + AST power-series traversal) to run linked two-chart Taylor recurrence, linear/nonlinear Chebyshev collocation, and a trace-exact gated residual cell (`LNN-PINN`), selecting admissible solvers solely via trace error ($\le 10^{-8}$) and governing-balance residual ($\le 10^{-6}$).
   - **Transcritical saddle branches ($\Delta_c = N = 0$ in $E_2$)**: `planar/model.py`, `planar/classical.py`, and `planar/bench.py` ingest the live SymPy `ReducedODE` AST from `discover_planar_e2()`, verify the three solvability gates automatically, compute exact Briot–Bouquet slopes $\ell_\pm$ and $K=16$ Taylor germs, continue inward/outward with `DOP853` (equipped with sonic/dry-bed terminal events), and compare classical 1D Chebyshev collocation against a crossing-exact joint-parameter `LNN-PINN` remainder network on $r\in[0.85,2.0]$. (Earlier outward-rounded interval-barrier and 5-route continuation scripts are preserved under [`../.old/2026-11-27-interval-and-multiroute-archive/`](https://github.com/CarlXerophilem/Lie-ML_PDES/tree/dc9a44517a85312fe09945d94b9a7a5e0aba4ef7/.old/2026-11-27-interval-and-multiroute-archive).)

---

## 2. How to Run

Install dependencies from the repository root (`Python 3.10+`, `SymPy 1.14`):

```sh
python -m pip install -e .
# Optional regular profile comparison: python -m pip install -e ".[regular]"
```

### General Single-Entry Symbolic PDE-to-ODE Reducer (`delivery/reduce_pde.py`)

Template:

```sh
lie-reduce --model my_model.py --output build/my_model.json
```

(`--pde` is accepted as an alias for `--model`, `--log` as an alias for `--output`, and positional `<model> [<output>]` is also supported.)

#### Examples with repository PDE specifications

```sh
# 1+1D Eulerian SVE (E1): discover symmetries, prove smooth->affine, find m-strata, reduce all subalgebras, and run ML handoff
lie-reduce --model E1 --subalgebra X1 --output build/E1.json
# Optional full symbolic stratum check
lie-reduce --model E1 --strata --smooth-check --output build/E1_strata.json

# 2+1D Cartesian planar SVE (E2): 4 balances -> 3 first integrals -> 1 scalar ODE with all 9 parameters preserved
lie-reduce --model E2_planar \
  --subalgebra "X5 ; X1 + alpha_1*X4" \
  --output build/E2.json

# Built-in shorthand names (E1, P, M, E2_planar, E2_polar, E_exch)
lie-reduce --model M --strata --smooth-check --output build/M.json
```

#### Defining a custom SymPy-compiled PDE file (`my_model.py`)

Create a trusted local Python module exposing `SPEC = PDESpec(...)` (or `build_spec() -> PDESpec`) on a `JetSpace`:

```python
import sympy as sp
from lie_reduce import JetSpace, PDESpec

t, x = sp.symbols('t x', real=True)
u = sp.Symbol('u', positive=True)
nu, mu = sp.symbols('nu mu', positive=True)

jets = JetSpace((t, x), (u,), 2)
eq = jets.D(u, 0) - nu * jets.D(jets.D(u, 1), 1) + u * jets.D(u, 1) + mu * u

SPEC = PDESpec(
    name='damped_burgers_1p1D',
    jets=jets,
    equations=(sp.expand(eq),),
    principal=(jets.jet(0, 1, 0),),
    parameters=(nu, mu),
    conditions=('u>0', 'nu,mu>0'),
    positive=(u, nu, mu),
)
```

Then run:

```sh
lie-reduce --model my_model.py --output build/my_model.json
```

### Full Verification, Planar ML Certification & Manuscript Builds

```sh
# Current exact symbolic and source-paper verification (no training)
bash delivery/reproduce_all.sh

# Optional retired experiments (fresh logs under build/legacy-reproduction/)
# bash bin/reproduce_legacy.sh

# Run the planar river-bend Briot-Bouquet ODE, 1D Chebyshev & supplementary LNN-PINN benchmark suite (requires requirements-ml.txt)
bash delivery/reproduce_ml.sh

# Build vector workflow figures, compact dissertation PDF, and Madrid defense slides PDF
bash delivery/build_pdfs.sh
```

---

## 3. Published experiment logs (`delivery/logs/`)

These are recorded research receipts. Earlier per-model ML and multi-dimensional results are historical; their replay scripts are in [bin](../bin/README.md). Example commands for reading existing receipts must not overwrite them during routine verification.

| Experiment log path | Generating script / command | Contents and verification scope |
|---|---|---|
| [`logs/reduce_E1.json`](logs/reduce_E1.json) | `python delivery/reduce_pde.py --model delivery/lie_reduce/models.py:euler_spec --strata --smooth-check --ml --output delivery/logs/reduce_E1.json` | Full CLI run on $E_1$: smooth-to-affine proof, $m\in\{0,3\}$ jump strata, 9 subalgebra evaluations, 3 scalar ODEs, and in-memory ML comparison |
| [`logs/reduce_E2.json`](logs/reduce_E2.json) | `python delivery/reduce_pde.py --model delivery/lie_reduce/models.py:planar_e2_spec --subalgebra "X5 ; X1 + alpha_1*X4" --output delivery/logs/reduce_E2.json` | Cartesian $E_2$ rank-2 reduction preserving all 9 symbolic parameters $(C_1,C_2,C_3,G,K,c,f,g,m)$ |
| [`logs/check_multid.json`](logs/check_multid.json) | `python bin/legacy/check_multid.py` | Symbolic $m$-strata on $(E_1,P,M)$, polar vs. Cartesian $E_2$ quotient equality (`0` difference), non-diagonal rotational quotient, and `8/8` seeded $(1\text{--}3)+1\text{D}$ random PDEs passed in-memory to ML |
| [`logs/experiment_lie_E1.json`](logs/experiment_lie_E1.json), [`P`](logs/experiment_lie_P.json), [`M`](logs/experiment_lie_M.json), [`E2`](logs/experiment_lie_E2.json) | `python -B bin/legacy/experiment_lie_<MODEL>.py` | Written symbolic verifiers for each manuscript PDE family on `JetSpace` |
| [`logs/experiment_ml_E1.json`](logs/experiment_ml_E1.json), [`P`](logs/experiment_ml_P.json), [`M`](logs/experiment_ml_M.json), [`Eexch`](logs/experiment_ml_Eexch.json) | `python -B bin/legacy/experiment_ml_<MODEL>.py` | Held-out field errors, parent-balance residuals, trace errors, and solver selection across `Taylor`, `Chebyshev`, and `LNN-PINN` |
| [`logs/bed_kappa_u__3_.json`](logs/bed_kappa_u__3_.json), [`logs/bed_Q_u__.json`](logs/bed_Q_u__.json) | `python -m lie_reduce.bed --flux '<law>'` | Bed-drift reduction of $E_1[Q]$ for power-law and arbitrary symbolic $C^2$ bedload flux $Q(u)$ |
| [`logs/verify_planar.json`](logs/verify_planar.json) | `python delivery/verify_planar.py` | 42 exact SymPy identities for potential lift, general-$f$ saddle determinant, critical drift $c_*$, convex bowl, and drift lower bound |
| [`logs/planar_ml/planar_ode_results.json`](logs/planar_ml/planar_ode_results.json), [`planar_ode_grids.json`](logs/planar_ml/planar_ode_grids.json), [`weights_lnn_pinn.npz`](logs/planar_ml/weights_lnn_pinn.npz) | `bash delivery/reproduce_ml.sh` | Live SymPy-AST `ReducedODE` solvability gates, Briot–Bouquet $K=16$ Taylor germs, `DOP853` references with sonic/dry-bed event probes, classical 1D Chebyshev collocation, supplementary joint-parameter `LNN-PINN` remainder fits on $r\in[0.85,2.0]$, Cauchy majorant check, and non-power $C^2$ flux / convex-bowl controls |

---

## 4. Mathematical & Computational Boundaries and Limits

1. **Symmetry search class**:
   - By default, `discover_and_enumerate` searches projectable polynomial point symmetries of declared `--degree` (default `1`, affine in $(x, u)$).
   - `--smooth-check` proves unrestricted smooth point symmetries reduce to affine form on $E_1$, $P$, and $M$ ($m \ge 1$). For $2+1\text{D}$ planar $E_2$ and arbitrary user-supplied higher-dimensional PDEs, completeness holds **only within the declared polynomial point-symmetry ansatz**; contact, higher-order generalized, nonlocal, and conditional symmetries (such as the vertical swirl offset $b(t)$ in $E_{\mathrm{exch}}$) are not discovered by point-subalgebra enumeration.
2. **Exact PDE presentation & principal shell**:
   - `PDESpec` requires exact SymPy rational/symbolic expressions (`sp.Float` coefficients are rejected) and a square principal derivative block of full rank on shell ($\det \partial\Delta/\partial u_{\mathrm{prin}} \neq 0$). Overdetermined or differential-algebraic systems without an explicit square principal block must be completed to involution before calling `reduce_pde.py`.
3. **Subalgebra combinations & orbit-chart quotients**:
   - `enumerate_subalgebras` deterministically tests basis singletons and combinations up to `--max-combo-terms` (default `2`, i.e., $X_i + \alpha_1 X_j$). Exhaustive classification of connected-adjoint optimal systems in dimension $\ge 2$ is not claimed.
   - `orbit_graph` constructs matrix-exponential coordinate charts for affine generators on $(x, u)$ with equal base and point orbit rank $d-1$ on a transverse slice, requiring $\Delta(z,\mathbf{v}) = \mathsf{M}(z,\mathbf{v})\,\mathcal{E}[F](z)$ with profile-free $\mathsf{M}$ and $\det\mathsf{M} \not\equiv 0$. Non-affine generators (e.g., degree at least 2 base fields) are discovered in `discovery.basis` but rejected at the matrix-exponential chart stage unless a section is supplied.
   - Stage execution is bounded by `--stage-seconds` (default `20s` per subalgebra) using `SIGALRM` (`POSIX`/`Linux` main thread).
4. **Variational quadrature & multi-profile elimination**:
   - `integrate_and_eliminate` integrates exact total-derivative balances detected via the Euler operator $\mathsf{E}_a(\mu_\ell \mathcal{E}) = 0$ for multipliers $\mu_\ell \in \{1, z, z^{-1}, z^2\}$ and eliminates algebraically solvable or cyclic profiles. Coupled reduced ODE systems without enough elementary variational integrals remain verified multi-component ODEs (`len(reduced_equations) > 1`) rather than scalar ODEs.
5. **Numerical/ML solver & certification scope**:
   - `_profile_learning.Case.from_reduction` (`--ml`) accepts verified **regular** scalar ODEs of order $1 \le r \le 3$ on bounded intervals where the leading derivative coefficient $\Delta_c$ does not vanish. Its residual gate ($\le 10^{-6}$ on held-out grids) is a **sampled diagnostic**, not a continuous error proof.
   - Transcritical singularities ($\Delta_c(r_*, H_*) = N(r_*, H_*) = 0$) cannot be integrated by generic IVP/PINN routines directly through $r_*$; they require nondegenerate saddle hypotheses ($\det DF(r_*, H_*) < 0$), desingularized Briot–Bouquet germs (`planar/classical.py`), adaptive `DOP853` continuation up to maximal Picard–Lindelöf / second-sonic chart boundaries, and classical Chebyshev collocation (`planar/bench.py`).
   - Direct $P$–$M$ continuation, turbulent bed friction closures, supercritical/fold regimes $c \ge c_*$, and symbolic-ML search for general closures remain open problems.
