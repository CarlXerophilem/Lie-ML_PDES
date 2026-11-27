# Parameter-Dependent Lie Symmetries and Semi-Analytical Solutions of Nonlinear PDEs

Yihong Xiao · MATH 4890 · Wenzhou-Kean University

This dissertation studies Saint–Venant–Exner systems through exact symmetry reductions, reconstruction of physical fields and local regular or singular profiles. The computational experiments compare classical and learned representations on prescribed invariant families.

| Start here | Contents |
|---|---|
| [Compact dissertation](draft/dissertation_wku_compact.pdf) | Authoritative manuscript. [LaTeX source](draft/dissertation_wku_compact.tex). |
| [Madrid defense](draft/defense_wku_madrid.pdf) | Defense slides. [LaTeX source](draft/defense_wku_madrid.tex). |
| [Delivery user manual](delivery/README.md) | End-to-end PDE-to-ODE reducer CLI (`delivery/reduce_pde.py`), log directory map, and mathematical/computational limits. |
| [Manuscript workflow](draft/README.md) | Flowcharts connecting hypotheses, evidence, figures and slides. |
| [Reproduction and verification](delivery/VERIFICATION.md) | Maintained entry points, hypothesis ledger, run logs and source checks. |
| [References](ref/README.md) | Flat inventory of cited literature, publisher links and the literature audit. |
| [Research path](delivery/research_path.md) | Commit chronology, past experiments, negative results and archive map. |

## Dissertation at a glance

**Goal.** Identify when a parameter-dependent symmetry can generate physically admissible reference solutions for water over a mobile bed.

**Method.** Determine point symmetries on declared charts, check orbit rank and data, reduce the PDE directly to scalar ODEs via symbolic first integrals, resolve local regular or singular branches analytically, and reconstruct the original fields. Audit the published scalar equation \(P\) separately. The compatible material equation \(M\) (\(\mathcal E_L\)) yields an exact local reconstruction of the original Eulerian model \(E_1\).

**Results.** The positive \(1+1\) charts admit exact local point-algebra classifications for real \(m\ge1\). The manuscript proves material reconstruction of water and mobile sediment bed, constructs an exact bed-drift family for arbitrary \(C^2\) flux \(Q(u)\) and a convergent cubic Laurent branch, and shows that any hydraulically critical point of the separate \((2+1)\)D sloping-bed annular sediment-transport model \(\mathcal E_2\) admits two local analytic Briot–Bouquet crossings whenever \(\det\mathbf J_*<0\). Across held-out tuples in a USACE `HEC-RAS`-motivated sediment-transport box (\(m\in[1.5,3.5]\), \(k=K/G\in[2,10]\), \(\delta\in[1,3]\)) on the smooth annulus \(r\in[0.85,2.0]\), classical 1D Chebyshev collocation reconstructs water depth to \(3.37\times 10^{-11}\) median error and mobile bed elevation to \(2.96\times 10^{-13}\) median error in \(40.7\text{ ms}\) with zero training, whereas a supplementary remainder-learning `LNN-PINN` study shows no overall advantage over Chebyshev.

**Scope.** The annular determining calculation is restricted to the stated shared affine class and open radial water/sediment throughflow. General initial–boundary value problems, site-calibrated `HEC-RAS` frictional channels, supercritical fold regimes \(\delta\le 0\), and CPU-only symbolic-ML search for general closures remain open.

**Keywords.** Parameter-dependent Lie symmetries, jet bundles, invariant reduction, Saint–Venant–Exner system, material reconstruction, transcritical Briot–Bouquet branches, Laurent series, Chebyshev collocation, structure-constrained neural approximation.

## Active delivery

See the [`@delivery` user manual](delivery/README.md) for full architecture, custom SymPy `PDESpec` authoring, experiment logs, and explicit mathematical/computational limits.

```sh
python delivery/reduce_pde.py --model <path-to-model-file/sympy-compiled-PDEs> --output <path-to-experiment-log>
# Example:
python delivery/reduce_pde.py --model delivery/lie_reduce/models.py:planar_e2_spec --subalgebra "X5 ; X1 + alpha_1*X4" --output delivery/logs/reduce_E2.json
```

- [General symbolic PDE-to-ODE reducer CLI](delivery/reduce_pde.py) and [`lie_reduce` package manual](delivery/lie_reduce/README.md): complete jet-space prolongation, automated Spencer smoothness proof, parameter-stratum classification, basis combination enumeration, orbit-chart quotient, and constructive variational first-integral elimination with all symbolic parameters preserved.
- [Symbolic Eulerian classification](delivery/symbolic_sv2022.py), [scalar and material certificates](delivery/symbolic_sve2026.py), [planar and rotating-exchange reductions](delivery/symbolic_new_model2026.py), and [multi-dimensional & random-PDE end-to-end suite](delivery/check_multid.py).
- [Published scalar reproduction](delivery/reproduce_sve2026.py) with an equation audit and symbolic series.
- [Eulerian](delivery/ml_sv2022.py), [scalar and material](delivery/ml_sve2026.py), and [rotating exchange](delivery/ml_new_model2026.py) numerical comparisons compiled directly in-memory from live SymPy `ReducedODE` ASTs via [`_profile_learning.py`](delivery/_profile_learning.py), with JSON receipts written to [`delivery/logs/`](delivery/logs/).
- [Annular theorem and replay](delivery/annular-transcritical-theorem-20261101/README.md), [planar transcritical ODE & Chebyshev vs. `LNN-PINN` suite](delivery/reproduce_ml.sh) ([`delivery/logs/planar_ml/`](delivery/logs/planar_ml/)), and [historical evidence disposition](delivery/artifact_audit.md).
- **Boundaries and limits**: Point-symmetry discovery defaults to affine generators (`--degree 1`), with unrestricted smooth-to-affine reduction proved automatically on $E_1, P, M$ ($m\ge 1$) and scoped to the declared affine class on planar $E_2$ and custom higher-dimensional PDEs. `PDESpec` requires exact SymPy expressions and an explicit square principal shell; orbit quotients require affine flows with $\det\mathsf{M}\not\equiv 0$; `--ml` targets regular scalar ODEs of order $1\le r\le 3$ ($\Delta_c\neq 0$) under sampled residual gates, whereas transcritical saddles ($\Delta_c=N=0$) are resolved by Briot–Bouquet Taylor germs, adaptive `DOP853` continuation with sonic/dry-bed event detection, and classical 1D Chebyshev collocation (`delivery/planar_ode_experiments.py`).

The [audit archive](.old/2026-11-23-repository-audit/) and [retired interval/multi-route archive](.old/2026-11-27-interval-and-multiroute-archive/) preserve the former documentation, research artifacts and implementation paths. Use the compact dissertation for current claims and `.old/` for version-specific evidence.
