# Deterministic Symbolic Lie Reduction (`delivery/lie_reduce`)

`lie_reduce` is the symbolic core of the [`@delivery` user manual](../README.md). Built on complete SymPy jet spaces (`JetSpace`), it discovers point-symmetry Lie algebras, resolves symbolic parameter strata, enumerates closed rank-$(d-1)$ subalgebra combinations, constructs matrix-exponential orbit quotients, and eliminates variational first integrals while keeping all physical and integration parameters symbolic.

---

## 1. How It Works

1. **Jet-space representation (`jets.py`, `spec.py`)**: Builds $J^k(\mathbb{R}^d, \mathbb{R}^m)$, total derivatives $D_i$, prolonged generator action $\operatorname{pr}^{(k)}X(\Delta)$, and verified principal-derivative shells (`PDESpec.shell_certificate()`).
2. **Symmetry discovery & strata (`determining.py`, `strata.py`, `hidden.py`, `identities.py`)**:
   - Splits on-shell determining equations over free jet variables after normalizing symbolic exponents ($u^m$, $(u^2+v^2)^{(m-1)/2}$) into independent positive base symbols.
   - `smooth_symmetries` performs automated Spencer second-partial elimination to prove smooth-to-affine reduction on $E_1$, $P$, and $M$ ($m \ge 1$).
   - `strata` computes exact pivot-minor roots and power resonances, deciding jump dimensions by exact specialization.
3. **Algebra & subalgebra enumeration (`algebra.py`)**: Normalizes basis generators (`canonical_basis_dict`), verifies Lie brackets and Jacobi identities, and enumerates closed projectable rank-$(d-1)$ subalgebras (`enumerate_subalgebras`).
4. **Orbit-chart quotient & quadrature (`multid.py`, `reduce.py`)**: Integrates affine generator flows via matrix exponentials to form $(z, \mathbf{v}) \mapsto \mathbf{x}$, verifies $\Delta(z,\mathbf{v}) = \mathsf{M}(z,\mathbf{v})\,\mathcal{E}[F](z)$ with $\det\mathsf{M} \neq 0$, checks exactness via the Euler operator (`multi_flux_check`), and eliminates algebraic/cyclic profiles (`integrate_and_eliminate`).
5. **Models & flux extensions (`models.py`, `bed.py`)**: Supplies pure symbolic specifications (`euler_spec`, `scalar_spec`, `planar_e2_spec`, `polar_e2_spec`, `exchange_spec`) and arbitrary autonomous bedload flux reductions $Q(u)$.

---

## 2. How to Run

Run from the repository root using the single general reducer [`delivery/reduce_pde.py`](../reduce_pde.py):

```sh
python delivery/reduce_pde.py --model <path-to-model-file/sympy-compiled-PDEs> --output <path-to-experiment-log>
```

### Concrete Commands

```sh
# 1+1D Eulerian SVE (E1) with parameter strata, smooth-to-affine check, and in-memory ML handoff
python delivery/reduce_pde.py \
  --model delivery/lie_reduce/models.py:euler_spec \
  --strata --smooth-check --ml \
  --output delivery/logs/reduce_E1.json

# 2+1D Cartesian planar SVE (E2) rank-2 rotational bed-drift subalgebra (preserves 9 parameters)
python delivery/reduce_pde.py \
  --model delivery/lie_reduce/models.py:planar_e2_spec \
  --subalgebra "X5 ; X1 + alpha_1*X4" \
  --output delivery/logs/reduce_E2.json

# Arbitrary C^2 bedload flux Q(u) and multi-dimensional random PDE -> ML regression suite
PYTHONPATH=delivery python -B -m lie_reduce.bed --flux 'Q(u)' > delivery/logs/bed_Q_u__.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B delivery/check_multid.py > delivery/logs/check_multid.json
```

Any external `.py` file defining `SPEC = PDESpec(...)` (or `build_spec() -> PDESpec`) can be passed directly to `--model path/to/file.py[:callable_or_attr]`.

---

## 3. Experiment Logs

- [`../logs/reduce_E1.json`](../logs/reduce_E1.json) and [`../logs/reduce_E2.json`](../logs/reduce_E2.json): Complete discovery, subalgebra reduction, first-integral elimination, and ML handoff logs emitted by `delivery/reduce_pde.py`.
- [`../logs/check_multid.json`](../logs/check_multid.json): Symbolic $m$-strata (`E1: {0,3}`, `P: {0,1,3}`, `M: {0,3}`), polar vs. Cartesian $E_2$ scalar ODE equivalence (`0` residual difference), coupled rotational flow check, and `8/8` seeded $(1\text{--}3)+1\text{D}$ random PDEs passed directly in-memory to `_profile_learning.compare`.
- [`../logs/bed_kappa_u__3_.json`](../logs/bed_kappa_u__3_.json) and [`../logs/bed_Q_u__.json`](../logs/bed_Q_u__.json): Bed-shift reductions for cubic and general symbolic flux $Q(u)$.
- [`../logs/experiment_lie_E1.json`](../logs/experiment_lie_E1.json), [`P`](../logs/experiment_lie_P.json), [`M`](../logs/experiment_lie_M.json), [`E2`](../logs/experiment_lie_E2.json): Per-model symbolic verification receipts.

---

## 4. Boundaries and Limits

- **Ansatz class**: Default discovery solves the polynomial point-symmetry system of degree `--degree` (default `1`, affine). All-real-$m$ smooth maximality is proved automatically via `--smooth-check` for $E_1$, $P$, and $M$; planar $E_2$ and general user PDEs are classified strictly within their declared polynomial point-field search class. Contact, nonlocal, and conditional symmetries are excluded.
- **Principal chart**: Requires exact SymPy expressions (no `Float`), a square explicitly solvable principal derivative block, and nonvanishing on-shell principal Jacobian. Overdetermined systems require prior completion to involution.
- **Orbit quotient & elimination**: Automatic matrix-exponential orbit charts require affine point generators on $(x, u)$, a transverse slice of rank $d-1$, and $\det\mathsf{M}(z,\mathbf{v}) \not\equiv 0$. Automatic quadrature covers variational balances with integrating factors $\{1, z, z^{-1}, z^2\}$; non-exact multi-component ODE quotients remain coupled systems.
- **Downstream `--ml` handoff**: Restricted to verified regular scalar ODEs of order $1 \le r \le 3$ away from singular loci ($\Delta_c \neq 0$). Singular transcritical crossings ($\Delta_c = N = 0$) require separate Briot–Bouquet and interval-barrier analysis (`../planar/certify.py`).
