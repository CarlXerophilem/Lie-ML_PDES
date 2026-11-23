# Verified fluid baseline accomplishments — 2026-09-25

The project source and reductor have been deployed and executed on SSH alias
`priestess`, in conda environment `pinn`. All **139 pytest tests**, **22 legacy
standalone checks**, and **21 baseline gates across 17 evolution cases** passed.
These results establish a reproducible computational baseline. They do not
establish algorithmic novelty or a fluid-PINN performance improvement.

## Deployment and evidence

- Remote release: `/home/carl/lieml/releases/20260925-fluid-baseline-v1`.
- Results: `results/fluid-baseline/` beneath that release.
- Local copy: `research_artifacts/fluid-baseline-20260925/fluid-baseline/`.
- Live dashboard: <http://127.0.0.1:8878/>, through an SSH tunnel to the
  server's loopback interface. It remains available while the server and
  tunnel processes run. It is not publicly exposed.
- Runtime: Python 3.12.14; NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0,
  Plotly 7.1.0, Matplotlib 3.11.2, pytest 9.1.1. CPU PyTorch 2.14.0 was
  installed for existing regression scripts. See `pip-freeze.txt` for the
  complete environment.
- Source snapshot: **148 files**, including source, configs, documentation,
  draft text and main/proposal PDFs. Git history, reference-library PDFs,
  `pdf2md`, old runs, caches and other binaries are excluded. This is a
  working-tree snapshot; unrelated local changes were preserved.
- Source archive SHA256:
  `5ad0f9a76934d6f9aee34c8b66ad968c948f3bc81425f4976d03e9441826ed44`.
- Downloaded results archive SHA256:
  `31dee238a353d03bf5cbd4888628f8b424eb11cbc81d6987de182858a1f8fb84`.

The source archive and every listed deployed source file were hash-checked.
The downloaded result archive was independently hash-checked before extraction.
After the completed run, the shell wrapper gained an early existing-manifest
guard so reruns cannot overwrite earlier test logs before being rejected.
This operational patch and the final reports have a separate
`postrun_changes.json` hash record; the numerical and symbolic source is unchanged.
The dashboard also received a post-run fix: diagnostic subplots are rebuilt
when cases change, avoiding stale Plotly axis references when switching from
two NS diagnostics to three SVE diagnostics. Both transition directions were
then checked with actual saved datasets. Scientific simulations were not rerun
for these presentation/launch changes.
`provenance.json` records the numerical/symbolic source hashes and actual host.
`symbolic_records.json` holds inputs, supplied charts, reduction records and
`PDEsReductor` rankings. `verification.json` holds gates and thresholds;
`pytest.xml`, `pytest.txt`, `standalone-tests.txt` and `run.log` retain execution
evidence. Each case has full-precision NPZ arrays and dashboard JSON; field
samples in the dashboard copy are rounded to seven decimal places. The
reported errors use full-precision arrays, not the displayed values.

## Models, reductions, and actual numerical targets

All displayed parameters and coordinates are nondimensional. Write `B` for
bed elevation, `h>0` for water depth and `u` for velocity. The original
one-space-dimensional Eulerian SVE balances used here are

\[
 h_t+(hu)_x=0,\qquad
 (hu)_t+(hu^2+\tfrac12 gh^2)_x+ghB_x=0,\qquad
 B_t+\kappa(u^m)_x=0.
\]

Here `kappa=A_g*xi_sed` includes the fixed sediment/porosity multiplier.
The positive-velocity branch is used throughout. This is a `(p,q,r)=(2,3,3)`
system, with one spatial dimension plus time; it is not a 2D spatial SVE model.
It is separate from the 2026 paper's printed scalar Lagrangian master PDE.

At `m=3`, the supplied generator and invariant reconstruction are

\[
 X=x\partial_x+2h\partial_h+u\partial_u+2B\partial_B,
 \quad (h,u,B)=(x^2H(t),xV(t),x^2C(t)).
\]

The chart verifier checks `pr(X)Delta=diag(2,3,2)Delta` and all chain-rule
pullbacks. On `x>0,H>0`, the three reduced balances give

\[
 H'=-3HV,\qquad V'=-V^2-2g(H+C),\qquad C'=-3\kappa V^3.
\]

Independent direct differentiation verifies the control

\[
 H=\frac{1-4g\kappa}{9gt^2},\quad
 V=\frac{2}{3t},\quad C=\frac{4\kappa}{9t^2},
 \qquad t>0,\quad 0\le4g\kappa<1.
\]

The ODE is integrated numerically and reconstructed on `x in [0.5,2]`.
Boundary values are traces of this invariant solution; this plotted window
is not treated as a periodic closed system. Reusing this scaling at `m=2`
or `m=4` fails the supplied symmetry identity. Other symmetries are not ruled
out. The periodic full-SVE simulations use separate initial data and do not
pretend to lie in the scaling-invariant family.

The 2D incompressible Navier–Stokes target is

\[
 u_t+uu_x+vu_y+p_x=\nu\Delta u,\quad
 v_t+uv_x+vv_y+p_y=\nu\Delta v,\quad u_x+v_y=0.
\]

It has `(p,q,r)=(3,3,3)` with coordinates `(t,x,y)`. Reduction by `X=∂x`
is verified and gives

\[
 U_t+VU_y-\nu U_{yy}=0,\quad
 V_t+VV_y+P_y-\nu V_{yy}=0,\quad V_y=0.
\]

The specialization `V=0,P=constant` gives the heat equation. Its exact shear
solution checks the full 2D numerical solver. Taylor–Green and interacting
vortex cases are full 2D evolutions, not `x`-invariant reductions.
The Oseen control replaces advecting `(u,v)` by fixed `(a,b)=(0.3,-0.2)`.
Pressure is eliminated in the periodic vorticity evolution; a conserved mean
velocity plus streamfunction recovers the divergence-free velocity. Pressure
is not a displayed numerical field.

| Case family | Parameter sweep and data | Numerical method |
|---|---|---|
| Original periodic SVE, 6 cases | `m=2,3,4`; `kappa=0.05,0.1`; `g=1`; `h0=1+0.03cos(x)`, `u0=0.4+0.02sin(x)`, `B0=0.015cos(2x)`; `t=0..0.4`. | 128-cell Rusanov FV + centered bed source + SSPRK3; 256/512-cell refinements. Initial primitive fields use cell averages, with second-order-accurate `q=h*u` initialization. |
| Cubic invariant SVE, 3 cases | `kappa=0.05,0.1,0.2`, `g=1`; exact control initialized at `t=1`, evolved to `1.5`. | Three-profile DOP853, `rtol=1e-11`, `atol=1e-13`. |
| 2D NS shear, 2 cases | `nu=0.01,0.1`; `u0=cos(y),v0=0`; periodic `[0,2pi)^2`, `t=0..1`. | 64² Fourier vorticity + strict 2/3 truncation + RK4; exact reduced heat-equation reference. |
| 2D NS Taylor–Green, 2 cases | Same viscosities; `u0=sin(x)cos(y)`, `v0=-cos(x)sin(y)`. | Same solver; exact velocity amplitude `exp(-2 nu t)` and independently differentiated pressure control. |
| 2D NS interacting vortices, 2 cases | Same viscosities; `psi0=sin(x)sin(y)+0.2cos(2x)cos(y)+0.15sin(x)cos(2y)`; `u=psi_y,v=-psi_x`. | 64²/128² joint grid/timestep refinement, `dt<=0.01/0.005` with CFL/diffusion restrictions. |
| 2D Oseen, 2 cases | Same viscosities and interacting vorticity, fixed mean/advection `(0.3,-0.2)`. | Fourier RK4 checked against the independent exact Fourier semigroup. |

Each case has 41 saved time frames. The SVE numerical method is intended for
these short, smooth positive runs. It is not well-balanced for arbitrary
lake-at-rest data, and no shock-capturing or global-existence claim is made.

## Measured results

| Check | Remote result | Interpretation |
|---|---|---|
| Original cubic SVE and NS/Oseen supplied charts | All exact symbolic checks pass | Conditional local invariant pullback; no maximal classification or IBVP existence claim. |
| Original-balance analytic controls | All three residuals vanish for SVE, Taylor–Green and shear | Independent differentiation in original coordinates. |
| Cubic SVE numerical profiles | Maximum error `1.25e-12` across tested parameters | Agreement with a known exact family. |
| Periodic SVE mass / bed mean | Relative mass drift ≤ `2.23e-16`; absolute bed-mean drift ≤ `1.81e-18` | Periodic conserved-integral diagnostics. |
| Periodic SVE branch | Minimum depth > `0.9700`; velocity > `0.3650`; sampled characteristic eigenvalues real | No observed loss of the declared smooth branch at saved states. |
| SVE three-grid self-convergence | Discrepancy ratios `1.9440..1.9443` | Consistent with first-order convergence, not a rigorous error bound. |
| NS analytic velocity controls | Maximum error < `2.8e-15` | Low-mode analytic controls; not evidence of this accuracy for arbitrary flows. |
| NS interacting-vortex refinement | Vorticity RMS discrepancy `8.82e-7` at `nu=.01`; `1.28e-11` at `nu=.1` | 64² versus 128² plus timestep refinement, not error against an exact solution. |
| NS/Oseen divergence | Maximum < `1.63e-14` | Spectral incompressibility check. |
| NS energy and enstrophy | Decrease throughout saved times | Expected viscous dissipation in these unforced periodic runs. |
| Oseen exact evolution | Maximum vorticity error < `1.62e-11` | Independent Fourier-semigroup control. |

The earlier 48²/96² low-viscosity vortex pilot gave discrepancy `4.85e-5`,
failing the preselected `1e-5` gate. Resolution was increased without loosening
that threshold. This diagnostic is retained in `diagnostic-resolution.txt`.
The initial remote pytest collection failed because `pinn` lacked PyTorch;
that log is preserved as `pytest-initial-missing-torch.txt`. Installing CPU
PyTorch resolved the dependency; the subsequent complete selected suite passed.
The existing standalone script calls `sys.exit()` at import time, so it is
excluded from pytest collection and run separately; its 22 checks passed.
Those legacy Fisher/PINN checks are not fluid ML experiments.

## Visualization and reproducibility

The dashboard provides a case/parameter selector, field selector, time slider,
play/pause, whole-domain field, a 24% local crop, a movable point probe and its
time history, plus global diagnostics with a shared time cursor. Whole-domain
and local spatial field scales remain fixed across time. “Global” means the
whole simulated finite domain, not global-in-time mathematical validity.

Browser checks confirmed loading, switching from 1D to 2D, field/time selection,
fixed scales, local crop, probe history and displayed values against the saved
JSON, and advancing/stopping playback. At `t=0.75`, the low-viscosity NS probe
at `x=y=pi/2` displayed vorticity `1.2366939`, exactly matching the dashboard
dataset. The overview PNG/PDF and rendered dashboard were visually inspected.

To rerun on the deployed host, use a fresh output folder:

```bash
ssh priestess
cd /home/carl/lieml/releases/20260925-fluid-baseline-v1
source /home/carl/miniforge3/etc/profile.d/conda.sh
conda activate pinn
bash symm/fluid_baselines/remote_run.sh results/fluid-baseline-rerun
python -B symm/test_ml_pde_solver.py
```

The runner refuses to overwrite a directory that already contains a manifest.
To run only the symbolic/numerical cases after dependencies are installed:

```bash
python -B -m symm.fluid_baselines.run --output results/fluid-baseline-new
```

To reopen the existing remote dashboard after the tunnel closes, run locally:

```powershell
ssh -N -L 127.0.0.1:8878:127.0.0.1:8878 priestess
```

The remote HTTP server is bound to `127.0.0.1:8878`; release-level `server.json`
records its PID. If it has stopped, launch it from the active `pinn` environment:

```bash
python -m http.server 8878 --bind 127.0.0.1 --directory results/fluid-baseline
```

The downloaded local copy can also be served with `python -m http.server`
from its results directory on an unused localhost port. No external JavaScript
CDN is required. This is a session-launched service, not a boot-persistent daemon.

## Research status

Read [the focused novelty audit](fluid_baseline_novelty.md) for named sources,
exact anchors and access limits. The established reductions and integrators are
baseline prior art. Our accomplishment is a transparent, replayable implementation
with explicit negative outcomes and an end-to-end symbolic/numerical evidence
trail. Maple/REDUCE were not found on the remote PATH; their completion/oracle
capabilities were not run. ML improvements and new mathematical results remain
future claims requiring separate experiments and proofs.
