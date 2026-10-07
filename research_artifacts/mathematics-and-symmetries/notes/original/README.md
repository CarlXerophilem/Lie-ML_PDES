# SVE-informed Lie/PINN experiment

Four runnable scripts implement the **scalar master equation in `main.tex` at
m=3**. This is a verified, smooth benchmark implementation, not a production
solver for arbitrary SVE initial data or a completed research result.

## Run

Keep all four `.py` files in the same directory. Python 3.11 or later is
recommended. In a virtual environment:

```bash
python -m pip install -r requirements.txt
python test.py --self-test
python base_LieReduct.py --out results
python test.py --out results
python base_PINN.py --out results
python pde_scene.py results
```

Open `results/scene.html` in a browser. Every solver already calls the
visualizer unless `--no-scene` is supplied; rerunning it combines all available
methods. The page works offline, with Play/Pause, a time slider, field selection,
and Eulerian/Lagrangian coordinate selection. `spacetime.png` gives static
two-dimensional spacetime heatmaps. This is a 1+1 dimensional calculation,
not a two-spatial-dimensional flow simulation.

To explicitly select CPU PyTorch before installing the remaining dependencies:

```bash
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```

A shorter smoke run uses `--steps 200 --lbfgs 80 --points 128`. Defaults are
1000 SOAP iterations, up to 100 L-BFGS iterations, 256 collocation points,
and a three-hidden-layer, width-24 tanh network. These are exposed demonstration
budgets, **not optimized hyperparameters**. Use `--help` for parameters, seed,
device, domain, network sizes, and sampling controls. Do not mix different
problems in one output directory. Use separate directories for parameter sweeps
and seeds; repeated runs intentionally overwrite that method's outputs.

## What each file does

| Script | Calculation |
|---|---|
| `test.py` | X5 reduction; second-order Taylor lift; one-input neural remainder; full PDE validation |
| `base_PINN.py` | Direct two-input `(t,s)` network; no invariant-coordinate input or symmetry loss; original PDE residual |
| `base_LieReduct.py` | SymPy verification of generator, invariant, reduction, and exact solution; DOP853 reduced IVP; coordinate identities |
| `pde_scene.py` | Shared offline interactive display and static heatmaps of position, velocity, depth, and PDE residual |

The first two use the same SOAP optimizer and L-BFGS polishing, float64,
Sobol collocation, soft-data gradient balancing, and Cauchy/boundary functions.
The direct network enforces three time-Cauchy functions exactly. The reduced
network enforces three Taylor coefficients exactly and the remaining Cauchy
and boundary samples softly. Thus the construction encodes different prior
structure, which must be considered when interpreting comparisons.

## Equation and data

The implemented unforced equation is

```text
E[phi] = Dt(phi_s phi_tt - g phi_ss/phi_s^2)
         - g beta Ds(phi_t^2 phi_ts/phi_s) = 0.
```

All variables here are dimensionless; beta is the m=3 transport coefficient.
The default fixture uses g=1, beta=1/8, and 1<=t,s<=1.2. These choices select
a smooth positive branch with a known solution:

```text
phi_exact(t,s) = C (s t^2)^(1/3),
C^3 = 27 g / (1 - 4 g beta),    0 < g beta < 1/4.
```

This expression satisfies the homogeneous PDE: no manufactured forcing is
added. It supplies phi, phi_t, phi_tt at t=t0 and phi at s=s0,s1. Interior
exact values are used only for validation. The experiment is deliberately a
verification fixture; its simple separability is not evidence of generality.
Changing to arbitrary physical data requires a new admissibility and
well-posedness analysis, not just changing these numerical defaults.

The verified point symmetry and finite action are

```text
X5 = t partial_t - 2s partial_s,
S5(epsilon): (t,s,phi) -> (exp(epsilon)t, exp(-2epsilon)s, phi).
sigma = s t^2,    phi = F(sigma),    E[F(s t^2)] = R[F]/t.
A = 2 sigma F'^2 + 4 sigma^2 F' F'' - g F''/F'^2
B = 8 sigma^2 F' (F' + sigma F'')
R = 2 sigma A' - g beta B'.
```

SymPy solves R=0 for F''' for the non-neural baseline. The Lie-PINN uses
`F = P2 + (sigma-sigma0)^3 N_theta(sigma)`, where P2 contains only the
three prescribed anchor coefficients. This is a provisional, explicit
semi-analytical construction for experimentation; it does not finalize the
paper's method. Both neural methods are scored on the **original PDE** by
automatic differentiation at an independent evaluation grid.

The material map requires phi_s>0. The IVP and final neural evaluation reject
a nonpositive Jacobian. Loss terms discourage violation during training;
nonfinite residuals stop training rather than being silently clamped. No
shock handling, dry-bed regularization, or extrapolation guarantee is provided.

## Full SVE versus the scalar benchmark

The full Eulerian system is also written symbolically in `equations.txt`:

```text
h_t + (h v)_x = 0
v_t + v v_x + g(h+b)_x = 0
b_t + beta v^(m-1) v_x = 0.
```

With x=phi(t,s), h=1/phi_s, v=phi_t, the bed equation becomes

```text
b_t - (v/phi_s) b_s + (beta/phi_s) v^(m-1) v_s = 0.
```

The time derivative in the latter equation is at fixed s. In particular, its
convective bed term cannot be silently dropped. The current paper has not
established equivalence of its scalar master equation to this full system.
**These scripts do not reconstruct b or claim to solve all three equations.**
Eulerian visualization means plotting reconstructed fields at x=phi(t,s),
on moving material intervals; it does not turn coordinate conversion into
a new symmetry reduction. `base_LieReduct.py` is specialized to the verified
SVE benchmark, not a black-box classifier for an arbitrary PDE system.

## Baseline choice and sources (checked 21 September 2026)

There is no universally best PINN algorithm or Lie reduction. SOAP is a
documented modern default with a maintained PyTorch implementation. The
2026 optimizer literature also compares natural-gradient and self-scaled
quasi-Newton alternatives; it does not establish a universal SVE winner.
An Adam option is explicit (`--optimizer adam`), never a silent fallback.
This tanh-MLP implementation is not claimed to reproduce PirateNets or the
complete configuration of any cited benchmark paper.

- Paliathanasis, Leon and Leach (2026), scalar benchmark and symmetry:
  https://doi.org/10.3390/math14030433
- Wang et al., Gradient Alignment in Physics-informed Neural Networks:
  https://arxiv.org/abs/2502.00604
- Jnini et al. (2026), Curvature-Aware Optimization for High-Accuracy PINNs:
  https://arxiv.org/abs/2604.05230
- Wang et al., PirateNets (architecture alternative, not implemented here):
  https://arxiv.org/abs/2402.00326
- Kavousanakis et al. (2026), symmetry reduction integrated with PINNs:
  https://doi.org/10.1038/s41467-026-75936-3

## Verification and outputs

`python test.py --self-test` checks the symbolic reduction, infinitesimal
criterion, invariant, mass-coordinate identity, exact solution, an off-solution
autodiff reduction identity, hard Taylor coefficients, and network invariance.
The solver scripts produce `.npz` field arrays, JSON metrics, symbolic equation
exports, and neural checkpoints. Small field error alone is insufficient:
inspect original-PDE residual, derivative errors, and Cauchy mismatch too.
The conventional ODE residual uses the ODE's own derivative and therefore is
not an independent error estimator; the separate exact-solution errors are.

The included `demo/` results use the default network budgets and seed 7.
They are a single smooth verification run, not a statistical performance
study. Neural training was run concurrently on CPU; recorded wall times
must not be interpreted as a controlled speed comparison. Checkpoints and
metrics preserve configuration, architecture size, seed, and Torch version.

Tested environment: NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0,
PyTorch 2.14.0+cpu, pytorch-optimizer 3.10.1, Matplotlib 3.10.8.

### Observed verification run

| Method | Relative position error | Original PDE RMS residual |
|---|---:|---:|
| LiePINN | 2.612e-08 | 1.922e-03 |
| PINN | 1.973e-08 | 1.207e-04 |
| LieReduct | 1.866e-12 | 2.980e-15 |

The reduced neural method did not win every metric. The direct PINN had
a smaller PDE residual; the Lie-PINN had smaller velocity/depth errors.
This experiment validates the code and does not establish methodological superiority.
