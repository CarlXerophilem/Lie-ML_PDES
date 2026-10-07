# Basic-to-advanced 2D SWE/SVE PINN benchmark

Here **2D means two spatial coordinates and time**: `(t, x, y)`, four fields `(h, u, v, b)`. Start with the flat-bed shallow-water baseline, then activate fixed topography, Coriolis/linear drag, and evolving Grass sediment transport. Everything is dimensionless.

This is an executable **SVE adaptation** of *Lie Point Symmetry and Physics Informed Networks*, not a reproduction of its heat/Burgers tables. It evaluates actual neural PDE solvers. The symbolic work verifies declared candidates and a finite scaling ansatz; it does not claim a maximal Lie classification.

## Start at the basic level

Use Python 3.11 or 3.12. Install the CPU version of PyTorch separately if desired:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python benchmark.py --task verify
python benchmark.py --task suite --cases flat --architectures mlp \
  --methods vanilla lie reweighted --seeds 0 1 2 --steps 600 \
  --out results/my_flat_baseline
```

The first command checks equations, one-parameter subgroup actions, initial/boundary conditions, exact classical controls, and loss/gradient identities. The second trains the simplest baseline: one smooth fixed-bed problem with a plain MLP. All methods use the same hard initial condition, periodic architecture, optimizer, initial weights, and collocation points for each paired seed.

Next, change `--cases flat` to `--cases all`. Then run the conditional family:

```bash
python benchmark.py --task family --architectures mlp modified deeponet \
  --methods vanilla lie reweighted cosine conservation --seeds 0 1 2 \
  --steps 600 --collocation 128 --out results/my_family
python symbolic_benchmark.py --repeats 5
```

Included pilot outputs are in `results/family_pilot` and `results/suite_pilot`. Read their `SUMMARY.md`, `metrics.csv`, and `results.json`. Exact installed versions and CPU settings are recorded in each result file. Commands in `run_protocol.py` describe larger runs:

```bash
python run_protocol.py --protocol samples
python run_protocol.py --protocol weights
python run_protocol.py --protocol zero
python run_protocol.py --protocol extended
```

These print commands without executing them. Add `--execute` to run them sequentially. The extended protocol is substantially more expensive than the included pilot. A sample-count sweep is necessary before making a sample-efficiency claim; the included fixed-count pilot alone does not establish one.

The manuscript's printed scalar master equation is a separate **1+1** literature control. Run `python scalar_master_control.py` to verify its cubic `X5=t*d_t-2*s*d_s` subgroup, invariant `sigma=s*t^2`, pullback identity, regular reduced IVP, near-cubic rejection, and time-coefficient symmetry defect. Its data and symmetries are not identified with the two-spatial-coordinate Grass system. No new physical derivation or generic-exponent scalar reduction is claimed.

## PDE and reference problem

On a periodic square `[0, 2*pi)^2`, the primitive residual is

\[
\begin{aligned}
\Delta_h&=h_t+u h_x+v h_y+h(u_x+v_y),\\
\Delta_u&=u_t+u u_x+v u_y+g(h_x+b_x)-f v+\gamma u,\\
\Delta_v&=v_t+u v_x+v v_y+g(h_y+b_y)+f u+\gamma v,\\
\Delta_b&=b_t+\nabla\cdot\bigl[\kappa (u^2+v^2)^{(m-1)/2}(u,v)\bigr].
\end{aligned}
\]

`kappa` includes a constant porosity factor; `gamma` is **linear** drag. The initial fields are
`h=1+A*cos(x)*cos(y)`, `u=0.25`, `v=0.15`, `b=B*sin(x)*sin(y)`.
Phase translations are also supported. Defaults are `A=.03`, `B=.02`, `g=1`, `T=.25`.

| Family | Sediment | Bed | Source terms |
|---|---|---|---|
| `flat` | off | fixed zero | none |
| `topography` | off | fixed nonuniform | none |
| `rotation_drag` | off | fixed nonuniform | `f=.2`, `gamma=.05` |
| `sve_m2.9`, `sve_m3`, `sve_m3.1`, `sve_m4` | `kappa=.01` | evolves | none |

`numerics.py` solves the **coupled conservative system** `(h, hu, hv, b)` with Fourier collocation, a two-thirds frequency filter on flux/source derivatives, and adaptive DOP853. It refines spatial grids and temporal tolerances independently, records mass/bed-mean drift, and probes real characteristic speeds. Filtering does not prove stability or exact dealiasing of arbitrary nonpolynomial fluxes. The high-mode diagnostic of the filtered state is supplementary; grid refinement is the principal accuracy check.

This classical reference is appropriate to the smooth periodic pilot. It is not a shock-capturing or wetting/drying solver. Positive depth, a nonzero-speed branch for active noninteger flux, short horizon, numerical convergence, and sampled hyperbolicity are explicit restrictions. They are not a proof of global regularity or hyperbolicity for the Grass closure. For shocks, add a separately verified well-balanced finite-volume baseline and weak/conservative neural formulation before comparing results.

## What each neural baseline tests

| Loss | Implementation | Scientific question |
|---|---|---|
| `vanilla` | scaled PDE residual MSE | Basic PINN baseline |
| `lie` | PDE MSE plus squared jet-gradient/prolongation dot products | SVE adaptation of the paper's Eq. 11 |
| `reweighted` | replaces those dot products with verified `M_X * Delta` | Does a Lie gain simply reflect residual weighting? |
| `cosine` | PDE MSE plus squared normalized jet-space cosines | Does angle normalization change the optimization? |
| `conservation` | PDE MSE plus periodic water-mass and bed-mean constraints | Does integral physics help beyond local Lie analysis? |

The printed Eq. 11 is signed. This benchmark explicitly uses a **nonnegative squared-dot adaptation**, and uses squared cosine for the normalized variant. It retains the PDE loss: a rotation generator alone constrains only momentum residual combinations. Equation scales and a symmetry weight are fixed before training. Different normalization choices define different methods and must be reported.

The cosine uses the Euclidean metric in the declared dimensionless jet coordinates. Its value depends on that metric and coordinate scaling; it is not an intrinsic coordinate-independent angle.

Architectures are a tanh MLP, Wang et al.'s tanh-gated modified MLP, and a small branch/trunk dot-product network. Widths are selected to match trainable parameter counts within about 2%; parameter matching does not equate compute or representation capacity. All use the same hard-IC ansatz, periodic Fourier coordinate features, positive-depth ansatz, and exact frozen bed when sediment is off. With default width 32 the parameter counts are 2628, 2596, and 2641.

The conditional task trains on six `(m,A)` pairs: `m in {2.9,3,3.1}`, `A in {.02,.04}`. It tests previously unseen exponents `2.95,3.05` with amplitude `.03`. A translated first test case checks exact translation canonicalization. This is interpolation within a small prescribed initial-data family, not arbitrary-function operator generalization. The same phase-aware representation is used for every architecture/loss. The translated case is not an independent parameter sample and is excluded from aggregate errors.

No future reference snapshots supervise training. Reference errors are logged as diagnostics at nine fixed stages; they do not select the checkpoint, loss weight, architecture, or seed. The final fixed checkpoint is reported. Test-informed model selection would require a new independent test set. The `weights` protocol is an ablation; selecting a weight from it requires separate validation/test families.

## One-parameter subgroups and the key control

Let `D=t*d_t+x*d_x+y*d_y`, `V=x*d_x+y*d_y+2h*d_h+u*d_u+v*d_v+2b*d_b`, and `J=-y*d_x+x*d_y-v*d_u+u*d_v`. The implemented exact flows and local invariants are:

| Generator | Flow with parameter `epsilon` | Local invariants / ansatz |
|---|---|---|
| `D` | `(t,x,y)` multiplied by `exp(epsilon)`; fields fixed | `x/t,y/t`; fields `F(x/t,y/t)` for `t>0` |
| `V` | `(x,y)` multiplied by `exp(epsilon)`; `(h,b)` by `exp(2epsilon)`; `(u,v)` by `exp(epsilon)` | `t,y/x,h/x^2,b/x^2,u/x,v/x` for `x!=0` |
| `J` | rotate coordinates and velocity by `epsilon` | `t,r,h,b,u_r,u_theta`; axisymmetric fields in polar coordinates |
| `Tx`, `Ty`, `Tt` | shift the corresponding coordinate | Omit that coordinate only if the full initial/boundary problem permits it |

`finite_action()` transforms first jets by the chain rule. Verification checks finite residual covariance in addition to infinitesimal identities. Rotations/scalings are bulk PDE symmetries; continuous rotations and dilations are **not global actions on the fixed square torus**. They are used only as verified local residual identities. The nonuniform initial condition is not invariant under spatial translation; a hard reduction to spatially constant solutions would be invalid. Translation acts on the whole initial-data family by shifting its phase, which is implemented consistently.

For each accepted generator, symbolic verification obtains
\[
\operatorname{pr}^{(1)}X\,\Delta=M_X\Delta.
\]
Here `M_D=-I`, `M_V=diag(2,1,1,2)`, and `M_J` rotates the two momentum residuals. Spatial/time translation yields zero because the autonomous residual has no explicit coordinates. Consequently the squared-dot Lie objective is a residual weighting for these candidates. This is an off-solution identity, not merely an on-solution statement. The code compares both losses and **parameter gradients** and uses paired training to test that conclusion.

The extra scaling `V` is valid for active cubic Grass transport (`m=3`), but rejected at `m=2.9,3.1,4`. `D` is rejected when fixed Coriolis/drag coefficients are active. `J` remains valid with those isotropic sources. Within the five-coefficient isotropic scaling ansatz, source-free cubic SVE has nullity two and nearby noncubic SVE nullity one. This finite ansatz is not a completeness argument.

The audit's four-field frozen-bed system allows arbitrary bed profiles. A Galilean boost fails for that enlarged system, but succeeds on the truly flat-bed restriction `b_t=b_x=b_y=0`. This distinction is recorded explicitly; rejected candidates do not establish absence of all other symmetries.

## Unexpected results and exploration

Appendix C of the supplied Lie-PINN paper reports that a modified MLP performed worse than a plain MLP for their heat experiment. It also discusses generators that yield zero or redundant PDE-like loss. Treat those as hypotheses to investigate, not universal outcomes to reproduce. This package tests:

1. Matched-size plain, modified, and branch/trunk networks across three paired seeds.
2. Lie loss versus its cheaper algebraic weighting, including loss/gradient identity checks.
3. Squared-dot versus squared-cosine normalization.
4. Water-mass/bed-mean constraints, with drift and local residual reported separately.
5. Cubic versus nearby noncubic transport, initial-amplitude interpolation, and exact translation-family equivariance.
6. Separate sample-count, symmetry-weight, and zero-generator protocols for future larger experiments.

Classic Grass SVE does not generally justify a dissipative energy equation without additional closure assumptions. This implementation therefore constrains periodic water mass and bed mean; it does not impose an invented energy conservation law. A future energy-compatible, slope-aware closure is a substantive physics extension, alongside hyperbolicity-aware parameter selection, inverse-parameter identification, conservative weak PINNs, adaptive sampling, and equivariant operator architectures.

## Complexity and honest time comparison

The first-order jet contains `3 + 4 + 4*3 = 19` coordinates, the residual Jacobian has shape `4 x 19`, and seven supplied candidates are checked. If an equation evaluation has expression cost `S`, assembling/differentiating the residual Jacobian and contracting `K` known generators grows with expression size and `K`. **Exact simplification can have much worse and expression-dependent cost**; there is no claimed polynomial complexity for maximal Lie classification. The declared scaling ansatz is only a matrix with five unknown coefficients and three to five rows. Its dense arithmetic nullspace has cubic worst-case scaling in matrix dimensions, with additional exact-arithmetic coefficient costs.

`symbolic_benchmark.py` retains every repeated build/audit/scaling timing, median/range, candidate timings, and operation counts. SymPy cache effects are identified; these are measured implementation costs, not a complexity proof. Negative candidates can be more expensive than successful ones, particularly with noninteger powers.

For `S_opt` optimization steps, `N_r` points, `P` network parameters, and `K` generators, first-order PINN work is roughly `O(S_opt*N_r*P)` times architecture/AD constants plus the jet-gradient/prolongation contractions. This notation omits exact graph-memory and higher-order reverse-mode constants; measured timings are decisive. Directly using `M_X*Delta` avoids unnecessary jet-gradient work when the identity is exact. The Fourier reference uses approximately `O(nfev*N_x*N_y*log(N_x*N_y))` work and `O(N_x*N_y)` state storage, with flux and FFT constants.

Recorded costs distinguish symbolic build/audit, converged reference construction, optimizer compute, monitoring, initialization, training wall time, full benchmark wall time, and warm-grid inference. A cached classical trajectory also answers repeated spatial/temporal queries without re-solving. Thus cheap neural evaluation alone is not evidence of an advantage for one fixed PDE.

Accuracy is evaluated both relative to the whole field and relative to its **change from the initial state**. The latter prevents nearly unchanged background depth/bed from hiding poor dynamics. Bed error is reported separately. Cost matching requires every active field's relative evolution L2 error to be at most `--accuracy` (default 5%), with a separate reference-refinement guard. No break-even estimate is emitted when accuracy is unmatched. For a conditional model only, the logged candidate break-even is
`ceil(training_wall_seconds / (new_classical_solve_seconds - inference_seconds))`, if the denominator is positive and the test query passes accuracy. It is an estimate for new parameter solves at the measured resolution, not a production guarantee. Reference construction/analysis costs remain separately visible and must be added if they are needed in a deployment workflow.

## Outputs and reproducibility

Each run retains a checkpoint (`model.pt`), complete fixed-stage learning history, prediction/reference arrays, and optimization snapshots. Each benchmark saves `verification.json`, `symbolic.json`, numerical grid/tolerance diagnostics, full per-seed metrics, environment/configuration, and aggregate summaries. Plots show every seed. The GIF depicts learning at fixed final physical time; it is not a time-evolution movie. The displayed exemplar is selected by median error within a method for visualization only.

`gradient_diagnostics` reports final PDE/extra parameter-gradient norms and their cosine on a fixed training batch. This is a sampled local diagnostic, not a causal explanation for the training outcome. `requirements-tested.txt` records exact package builds; `requirements.txt` is the broader installation specification.

Checkpoints and JSON paths can be moved with the package. For regenerating figures after relocation, `visualize.py` resolves stored run directories relative to the result root. Only load checkpoints from trusted sources.

## Sources

- Akhound-Sadegh et al. (2023), [Lie Point Symmetry and Physics Informed Networks](https://arxiv.org/abs/2311.04293), especially sections 3.1/3.2/4 and appendices B/C; the user's attached PDF was inspected.
- Wang, Teng, Perdikaris (2021), [Understanding and mitigating gradient flow pathologies in physics-informed neural networks](https://arxiv.org/abs/2001.04536), modified MLP equations 43--47.
- Fernández-Nieto et al. (2017), [Formal deduction of the Saint-Venant–Exner model including arbitrarily sloping sediment beds and associated energy](https://www.numdam.org/item/M2AN_2017__51_1_115_0/), closure/energy caveats.

These sources support design decisions. New SVE identities and measured results are derived and tested in this package.
