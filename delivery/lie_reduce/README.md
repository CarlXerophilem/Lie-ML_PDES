<!-- Math rendering: GitHub MathJax / KaTeX compatible LaTeX. Use $...$ or standalone $$ blocks; no custom macros or injected scripts. -->

# Deterministic Symbolic Lie Reduction (`delivery/lie_reduce`)

`lie_reduce` is the symbolic core of the [`@delivery` user manual](../README.md). Built on complete SymPy jet spaces (`JetSpace`), it discovers point-symmetry Lie algebras, resolves symbolic parameter strata, enumerates closed rank $d-1$ subalgebra combinations, constructs matrix-exponential orbit quotients, and eliminates variational first integrals while keeping all physical and integration parameters symbolic.

---

## 1. How It Works

1. **Jet-space representation (`jets.py`, `spec.py`)**: Builds $J^k(\mathbb{R}^d, \mathbb{R}^m)$, total derivatives $D_i$, prolonged generator action $\mathrm{pr}^{(k)}X(\Delta)$, and verified principal-derivative shells (`PDESpec.shell_certificate()`).
2. **Symmetry discovery & strata (`determining.py`, `strata.py`, `hidden.py`, `identities.py`)**:
   - Splits on-shell determining equations over free jet variables after normalizing symbolic exponents ($u^m$, $(u^2+v^2)^{(m-1)/2}$) into independent positive base symbols.
   - `smooth_symmetries` performs automated Spencer second-partial elimination to prove smooth-to-affine reduction on $E_1$, $P$, and $M$ ($m \ge 1$).
   - `strata` computes exact pivot-minor roots and power resonances, deciding jump dimensions by exact specialization.
3. **Algebra & subalgebra enumeration (`algebra.py`)**: Normalizes basis generators (`canonical_basis_dict`), verifies Lie brackets and Jacobi identities, and enumerates closed projectable rank $d-1$ subalgebras (`enumerate_subalgebras`).
4. **Orbit-chart quotient & quadrature (`multid.py`, `reduce.py`)**: Integrates affine generator flows via matrix exponentials to form $(z, \mathbf{v}) \mapsto \mathbf{x}$, verifies $\Delta(z,\mathbf{v}) = \mathsf{M}(z,\mathbf{v})\,\mathcal{E}[F](z)$ on charts where $\det\mathsf{M} \neq 0$, checks exactness via the Euler operator (`multi_flux_check`), and eliminates algebraic/cyclic profiles (`integrate_and_eliminate`).
5. **Models & flux extensions (`models.py`, `bed.py`)**: Supplies pure symbolic specifications (`euler_spec`, `scalar_spec`, `planar_e2_spec`, `polar_e2_spec`, `exchange_spec`) and arbitrary autonomous bedload flux reductions $Q(u)$.

---

## 2. Install and use

```bash
python -m pip install -e .
lie-reduce --model E1 --subalgebra X1 --output build/E1.json
```

The equivalent module command is `python -m lie_reduce`. The console command
accepts the built-in model names `E1`, `P`, `M`, `E2_planar`, `E2_polar`
and `E_exch`. It emits JSON with the model parameters, basis, reduction
statuses, checks, first integrals, preserved parameters and lift formulas.
Exit status 0 indicates at least one verified quotient; 2 indicates none.
Read individual statuses when some attempted subalgebras fail.

```bash
# Parameter strata and smooth-to-affine verification
lie-reduce --model M --strata --smooth-check --output build/M.json

# Rotation and bed drift in the planar model
lie-reduce --model E2_planar --subalgebra "X5 ; X1 + alpha_1*X4" --output build/E2.json

# General autonomous bed flux on a trusted local command line
python -m lie_reduce.bed --flux 'Q(u)' > build/bed.json
```

The optional regular numerical layer is installed with
`python -m pip install -e ".[regular]"`; pass `--ml` only for a supplementary
sampled comparison. Time limits use POSIX main-thread alarms for each quotient
attempt; on platforms without them, use WSL or explicitly set
`--stage-seconds 0` to disable these limits. Discovery itself is not bounded by
the quotient timer.

### Python API

```python
from lie_reduce import discover_and_enumerate, reduce_spec
from lie_reduce.models import euler_spec

spec, basis, subalgebras = discover_and_enumerate(euler_spec())
sub = next(s for s in subalgebras if s["id"] == "X1")
result = reduce_spec(spec, sub["generators"])
if result.status == "verified":
    print(result.reduced_equations)
    print(result.first_integrals)
else:
    print(result.status, result.reason)
```

Use `JetSpace` and `PDESpec` to supply a custom trusted Python file. The
[custom PDE example](../README.md#defining-a-custom-sympy-compiled-pde-file-my_modelpy)
sets all equations, derivative coordinates, symbolic parameters and chart conditions.
The CLI executes the Python module, not arbitrary untrusted text.

### Reproduce

Run `bash delivery/reproduce_all.sh` from a repository clone. This checks the
paper's current symbolic identities and source reproduction without re-training
or replacing the archived reports. Earlier experiments remain under
[bin](../../bin/README.md).

---

## 3. Experiment Logs

- [`../logs/reduce_E1.json`](../logs/reduce_E1.json) and [`../logs/reduce_E2.json`](../logs/reduce_E2.json): Complete discovery, subalgebra reduction, first-integral elimination, and ML handoff logs emitted by `delivery/reduce_pde.py`.
- [`../logs/check_multid.json`](../logs/check_multid.json): Symbolic $m$-strata (`E1: {0,3}`, `P: {0,1,3}`, `M: {0,3}`), polar vs. Cartesian $E_2$ scalar ODE equivalence (`0` residual difference), coupled rotational flow check, and `8/8` seeded $(1\text{--}3)+1\text{D}$ random PDEs passed directly in-memory to `_profile_learning.compare`.
- [`../logs/bed_kappa_u__3_.json`](../logs/bed_kappa_u__3_.json) and [`../logs/bed_Q_u__.json`](../logs/bed_Q_u__.json): Bed-shift reductions for cubic and general symbolic flux $Q(u)$.
- [`../logs/experiment_lie_E1.json`](../logs/experiment_lie_E1.json), [`P`](../logs/experiment_lie_P.json), [`M`](../logs/experiment_lie_M.json), [`E2`](../logs/experiment_lie_E2.json): Per-model symbolic verification receipts.

---

## 4. Boundaries and Limits

- **Ansatz class**: Default discovery solves the polynomial point-symmetry system of degree `--degree` (default `1`, affine). All-real $m$ smooth maximality is proved automatically via `--smooth-check` for $E_1$, $P$, and $M$; planar $E_2$ and general user PDEs are classified strictly within their declared polynomial point-field search class. Contact, nonlocal, and conditional symmetries are excluded.
- **Principal chart**: Requires exact SymPy expressions (no `Float`), a square explicitly solvable principal derivative block, and nonvanishing on-shell principal Jacobian. Overdetermined systems require prior completion to involution.
- **Orbit quotient & elimination**: Automatic matrix-exponential orbit charts require affine point generators on $(x, u)$, a transverse slice of rank $d-1$, and $\det\mathsf{M}(z,\mathbf{v}) \not\equiv 0$. Automatic quadrature covers variational balances with integrating factors $\{1, z, z^{-1}, z^2\}$; non-exact multi-component ODE quotients remain coupled systems.
- **Downstream `--ml` handoff**: Restricted to verified regular scalar ODEs of order $1 \le r \le 3$ away from singular loci ($\Delta_c \neq 0$). Singular transcritical crossings ($\Delta_c = N = 0$) require separate Briot–Bouquet analysis (`../planar/classical.py`); the earlier interval-barrier experiment is historical.
