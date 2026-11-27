# `@delivery` User Manual: Symbolic PDE-to-ODE Reduction & Unparsed ML Pipeline

`delivery/` contains the executable symbolic Lie-symmetry reducer, in-memory AST numerical/ML profile solvers, interval-barrier saddle certifier, verification logs, and PDF build scripts for the dissertation ([`../draft/dissertation_wku_compact.tex`](../draft/dissertation_wku_compact.tex)) and defense slides ([`../draft/defense_wku_madrid.tex`](../draft/defense_wku_madrid.tex)).

---

## 1. How It Works

The pipeline maps a system of nonlinear PDEs to reduced ODEs and numerical/learned profiles in five strictly symbolic-to-AST stages, without string parsing, preset ODE ansätze, or hardcoded similarity coordinates:

1. **Complete Jet-Space Specification (`lie_reduce/jets.py`, `lie_reduce/spec.py`)**:
   A PDE system $\Delta(x, u^{(k)}; \mu) = 0$ is compiled directly in SymPy on a complete jet space $J^k(\mathbb{R}^d, \mathbb{R}^m)$ via `JetSpace` and `PDESpec`. `PDESpec.shell_certificate()` verifies a square, explicitly solvable principal derivative block, nonvanishing principal Jacobian on shell, and nonvanishing denominators on the declared positive cone.
2. **Infinitesimal Prolongation & Parameter Strata (`lie_reduce/determining.py`, `lie_reduce/hidden.py`)**:
   Point generators $X = \xi^i(x,u)\partial_{x_i} + \eta^a(x,u)\partial_{u^a}$ are prolonged to order $k$ via total derivatives $D_i$ and constrained by $\operatorname{pr}^{(k)}X(\Delta)\big|_{\Delta=0}=0$. Symbolic affine powers such as $u^m$ and $(u^2+v^2)^{(m-1)/2}$ are normalized into independent positive base symbols before polynomial jet splitting.
   - `--smooth-check` runs automated Spencer second-partial elimination (`smooth_symmetries`) to prove unrestricted smooth point symmetries reduce to affine polynomial form (established on $E_1$, $P$, and $M$ for all real $m \ge 1$).
   - `--strata` extracts exact pivot-minor factors of $\mathsf{A}(\mu)a = 0$ and power resonances, deciding every candidate jump stratum by exact specialization (`{E1: [0,3], P: [0,1,3], M: [0,3]}`).
3. **Canonical Basis & Subalgebra Enumeration (`lie_reduce/algebra.py`)**:
   Discovered generators are RREF-normalized into a deterministic basis (`X1..Xn` or `Y1..Yn`). Closed, projectable rank-$(d-1)$ subalgebras $[\mathfrak{h}, \mathfrak{h}] \subset \mathfrak{h}$ are enumerated from basis singletons and symbolic linear combinations $X_i + \alpha_1 X_j$.
4. **Matrix-Exponential Orbit Quotient & First-Integral Elimination (`lie_reduce/multid.py`, `lie_reduce/reduce.py`)**:
   From a transverse coordinate slice, matrix-exponential flows build the orbit chart $(z, \mathbf{v}) \mapsto \mathbf{x}$ and invariant surface $Q_{\mathfrak{h}}[U] = 0$. A quotient is accepted only when $\Delta(z, \mathbf{v}) = \mathsf{M}(z, \mathbf{v})\,\mathcal{E}[F](z)$ with profile-free $\mathsf{M}$ and $\det\mathsf{M} \not\equiv 0$. Exact balances satisfying the Euler operator test $\mathsf{E}_a(\mu_\ell \mathcal{E}) = 0$ ($\mu_\ell \in \{1, z, z^{-1}, z^2\}$) are integrated to $\mathcal{I}_\ell(z, F, F') = C_\ell$, eliminating algebraic and cyclic profiles while preserving all symbolic parameters $\mu$ and constants $C_\ell$.
5. **Unparsed In-Memory AST-to-ML Handoff (`_profile_learning.py`, `planar/bench.py`, `planar/certify.py`)**:
   - **Regular branches ($\Delta_c \neq 0$)**: `Case.from_reduction` compiles the live SymPy `ReducedODE` AST directly in-memory (`sp.lambdify` + AST power-series traversal) to run linked two-chart Taylor recurrence, linear/nonlinear Chebyshev collocation, and a trace-exact gated residual cell (`LNN-PINN`), selecting admissible solvers solely via trace error ($\le 10^{-8}$) and governing-balance residual ($\le 10^{-6}$).
   - **Transcritical saddle branches ($\Delta_c = N = 0$ in $E_2$)**: `planar/bench.py` and `planar/certify.py` evaluate desingularized Briot–Bouquet slopes $s_\pm$ and enclose candidate profiles (`Chebyshev`, `PINN`, `RF`, `gated`) via outward-rounded `float64` interval barriers.

---

## 2. How to Run

Install dependencies from the repository root (`Python 3.10+`, `SymPy 1.14`):

```sh
python -m pip install -r delivery/requirements.txt
```

### General Single-Entry Symbolic PDE-to-ODE Reducer (`delivery/reduce_pde.py`)

Template:

```sh
python delivery/reduce_pde.py --model <path-to-model-file/sympy-compiled-PDEs> --output <path-to-experiment-log>
```

(`--pde` is accepted as an alias for `--model`, `--log` as an alias for `--output`, and positional `<model> [<output>]` is also supported.)

#### Examples with repository PDE specifications

```sh
# 1+1D Eulerian SVE (E1): discover symmetries, prove smooth->affine, find m-strata, reduce all subalgebras, and run ML handoff
python delivery/reduce_pde.py \
  --model delivery/lie_reduce/models.py:euler_spec \
  --strata --smooth-check --ml \
  --output delivery/logs/reduce_E1.json

# 2+1D Cartesian planar SVE (E2): 4 balances -> 3 first integrals -> 1 scalar ODE with all 9 parameters preserved
python delivery/reduce_pde.py \
  --model delivery/lie_reduce/models.py:planar_e2_spec \
  --subalgebra "X5 ; X1 + alpha_1*X4" \
  --output delivery/logs/reduce_E2.json

# Built-in shorthand names (E1, P, M, E2_planar, E2_polar, E_exch)
python delivery/reduce_pde.py --model M --strata --smooth-check --output delivery/logs/reduce_M.json
```

#### Defining a custom SymPy-compiled PDE file (`my_model.py`)

Create any Python module exposing `SPEC = PDESpec(...)` (or `build_spec() -> PDESpec`) on a `JetSpace`:

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
python delivery/reduce_pde.py --model my_model.py --ml --output delivery/logs/my_model.json
```

### Full Verification, Planar ML Certification & Manuscript Builds

```sh
# Run all 4 Lie verifiers, 4 ML profile benchmarks, arbitrary bed-flux Q(u) checks,
# (1..3)+1D random PDE -> ML suite (check_multid.py), and 42 planar identities (verify_planar.py)
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 bash delivery/reproduce_all.sh

# Run the planar river-bend saddle continuation & interval-barrier certification suite (requires requirements-ml.txt)
bash delivery/reproduce_ml.sh

# Build vector workflow figures, compact dissertation PDF, and Madrid defense slides PDF
bash delivery/build_pdfs.sh
```

---

## 3. Experiment Logs (`delivery/logs/`)

| Experiment log path | Generating script / command | Contents and verification scope |
|---|---|---|
| [`logs/reduce_E1.json`](logs/reduce_E1.json) | `python delivery/reduce_pde.py --model delivery/lie_reduce/models.py:euler_spec --strata --smooth-check --ml --output delivery/logs/reduce_E1.json` | Full CLI run on $E_1$: smooth-to-affine proof, $m\in\{0,3\}$ jump strata, 9 subalgebra evaluations, 3 scalar ODEs, and in-memory ML comparison |
| [`logs/reduce_E2.json`](logs/reduce_E2.json) | `python delivery/reduce_pde.py --model delivery/lie_reduce/models.py:planar_e2_spec --subalgebra "X5 ; X1 + alpha_1*X4" --output delivery/logs/reduce_E2.json` | Cartesian $E_2$ rank-2 reduction preserving all 9 symbolic parameters $(C_1,C_2,C_3,G,K,c,f,g,m)$ |
| [`logs/check_multid.json`](logs/check_multid.json) | `python delivery/check_multid.py` | Symbolic $m$-strata on $(E_1,P,M)$, polar vs. Cartesian $E_2$ quotient equality (`0` difference), non-diagonal rotational quotient, and `8/8` seeded $(1\text{--}3)+1\text{D}$ random PDEs passed in-memory to ML |
| [`logs/experiment_lie_E1.json`](logs/experiment_lie_E1.json), [`P`](logs/experiment_lie_P.json), [`M`](logs/experiment_lie_M.json), [`E2`](logs/experiment_lie_E2.json) | `python -B delivery/experiment_lie_<MODEL>.py` | Written symbolic verifiers for each manuscript PDE family on `JetSpace` |
| [`logs/experiment_ml_E1.json`](logs/experiment_ml_E1.json), [`P`](logs/experiment_ml_P.json), [`M`](logs/experiment_ml_M.json), [`Eexch`](logs/experiment_ml_Eexch.json) | `python -B delivery/experiment_ml_<MODEL>.py` | Held-out field errors, parent-balance residuals, trace errors, and solver selection across `Taylor`, `Chebyshev`, and `LNN-PINN` |
| [`logs/bed_kappa_u__3_.json`](logs/bed_kappa_u__3_.json), [`logs/bed_Q_u__.json`](logs/bed_Q_u__.json) | `python -m lie_reduce.bed --flux '<law>'` | Bed-drift reduction of $E_1[Q]$ for power-law and arbitrary symbolic $C^2$ bedload flux $Q(u)$ |
| [`logs/verify_planar.json`](logs/verify_planar.json) | `python delivery/verify_planar.py` | 42 exact SymPy identities for potential lift, general-$f$ saddle determinant, critical drift $c_*$, convex bowl, and drift lower bound |
| [`logs/planar_ml/experiments.json`](logs/planar_ml/experiments.json), [`bounds.json`](logs/planar_ml/bounds.json), [`neighborhoods.json`](logs/planar_ml/neighborhoods.json), [`continuation.json`](logs/planar_ml/continuation.json) | `bash delivery/reproduce_ml.sh` | River-bend $f=0$ saddle `DOP853` references, `Chebyshev`/`PINN`/`RF`/`gated` fits, `float64` interval-barrier certificates, `mpmath` cross-checks, and warm- vs. cold-start continuation costs |

---

## 4. Mathematical & Computational Boundaries and Limits

1. **Symmetry search class**:
   - By default, `discover_and_enumerate` searches projectable polynomial point symmetries of declared `--degree` (default `1`, affine in $(x, u)$).
   - `--smooth-check` proves unrestricted smooth point symmetries reduce to affine form on $E_1$, $P$, and $M$ ($m \ge 1$). For $2+1\text{D}$ planar $E_2$ and arbitrary user-supplied higher-dimensional PDEs, completeness holds **only within the declared polynomial point-symmetry ansatz**; contact, higher-order generalized, nonlocal, and conditional symmetries (such as the vertical swirl offset $b(t)$ in $E_{\mathrm{exch}}$) are not discovered by point-subalgebra enumeration.
2. **Exact PDE presentation & principal shell**:
   - `PDESpec` requires exact SymPy rational/symbolic expressions (`sp.Float` coefficients are rejected) and a square principal derivative block of full rank on shell ($\det \partial\Delta/\partial u_{\mathrm{prin}} \neq 0$). Overdetermined or differential-algebraic systems without an explicit square principal block must be completed to involution before calling `reduce_pde.py`.
3. **Subalgebra combinations & orbit-chart quotients**:
   - `enumerate_subalgebras` deterministically tests basis singletons and combinations up to `--max-combo-terms` (default `2`, i.e., $X_i + \alpha_1 X_j$). Exhaustive classification of connected-adjoint optimal systems in dimension $\ge 2$ is not claimed.
   - `orbit_graph` constructs matrix-exponential coordinate charts for affine generators on $(x, u)$ with equal base and point orbit rank $d-1$ on a transverse slice, requiring $\Delta(z,\mathbf{v}) = \mathsf{M}(z,\mathbf{v})\,\mathcal{E}[F](z)$ with profile-free $\mathsf{M}$ and $\det\mathsf{M} \not\equiv 0$. Non-affine generators (e.g., $\degree \ge 2$ base fields) are discovered in `discovery.basis` but rejected at the matrix-exponential chart stage unless a section is supplied.
   - Stage execution is bounded by `--stage-seconds` (default `20s` per subalgebra) using `SIGALRM` (`POSIX`/`Linux` main thread).
4. **Variational quadrature & multi-profile elimination**:
   - `integrate_and_eliminate` integrates exact total-derivative balances detected via the Euler operator $\mathsf{E}_a(\mu_\ell \mathcal{E}) = 0$ for multipliers $\mu_\ell \in \{1, z, z^{-1}, z^2\}$ and eliminates algebraically solvable or cyclic profiles. Coupled reduced ODE systems without enough elementary variational integrals remain verified multi-component ODEs (`len(reduced_equations) > 1`) rather than scalar ODEs.
5. **Numerical/ML solver & certification scope**:
   - `_profile_learning.Case.from_reduction` (`--ml`) accepts verified **regular** scalar ODEs of order $1 \le r \le 3$ on bounded intervals where the leading derivative coefficient $\Delta_c$ does not vanish. Its residual gate ($\le 10^{-6}$ on held-out grids) is a **sampled diagnostic**, not a continuous error proof.
   - Transcritical singularities ($\Delta_c(r_*, H_*) = N(r_*, H_*) = 0$) cannot be integrated by generic IVP/PINN routines directly through $r_*$; they require nondegenerate saddle hypotheses ($\det DF(r_*, H_*) < 0$), desingularized Briot–Bouquet germs, and outward-rounded interval-barrier verification (`planar/certify.py`), certified only on the declared slices and parameter boxes.
   - Direct $P$–$M$ continuation, turbulent bed friction closures, and supercritical/fold regimes $c \ge c_*$ remain open problems.
