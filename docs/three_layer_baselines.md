# Three-layer baselines and fused SVE prototype

Date: 2026-09-27; updated 2026-09-28. The machine-readable record is under
`research_artifacts/three-layer-baselines-20260927/`.

## What is implemented

The experiment has three independently runnable layers. The ML-only layer
does not import Lie code. The Lie-only layer does not import Torch or PyKAN.
The fusion layer reads and validates the Lie-only JSON certificate before it
constructs a neural profile. Tests inspect these import boundaries and reject
an unverified certificate.

The Lie-only demo verifies the supplied local `m=3` reduction for
`X_5=t*d_t-2*s*d_s`, the flow, `sigma=s*t^2`, the invariant-surface equation,
the reduction identity, and the exact profile. Reusing the same supplied
identity at `m=4` returns `unsupported`; this does not prove that `m=4` has no
other symmetries.

## ML-only results

The logistic comparison used 100 uniform collocation points, Adam with
learning rate `0.01`, 10,000 iterations and ten seeds. The MLP has 121
trainable parameters. PyKAN `[1,7,1]`, grid 3 and spline order 3 has 112
trainable parameters after the unused symbolic affine parameters are frozen.

| Method | relative L2 median | mean | min--max | median train time |
| --- | ---: | ---: | ---: | ---: |
| MLP-PINN | 9.740e-1 | 6.895e-1 | 1.294e-3--9.984e-1 | 7.24 s |
| PIKAN | 8.580e-5 | 1.148e-3 | 2.360e-5--7.964e-3 | 63.71 s |

PIKAN therefore reproduces the reported direction, but this is not an exact
numerical reproduction: several MLP seeds converge to a low-residual wrong
branch, and the local best errors differ from the paper's reported values.
All runs are retained rather than selecting the best seed. PIKAN is also about
8.8 times slower per training run in this CPU implementation.

The Duffing comparison is a bounded fixed-IVP experiment with width 64 and
3,000 Adam iterations, not the paper's full parameter/initial-condition
solution-map protocol.

| Horizon | vanilla median relative L2 | higher-order | TM-PINN | TM-PINN range |
| --- | ---: | ---: | ---: | ---: |
| `T=1` | 2.050e-4 | 1.914e-4 | 7.585e-5 | 4.491e-5--1.001e-4 |
| `T=3` | 6.555e-2 | 9.841e-2 | 1.756e0 | 8.678e-2--8.894e0 |

The fixed-IVP trial reproduces the qualitative short-horizon advantage and
long-horizon instability. It does not reproduce the full paper experiment.

## Fused SVE results

The fusion experiment fixes `g=1`, `beta_tr=0.1`, `m=3`,
`sigma in [1,1.5]`, and changes only the initial curvature by
`eta_ic=0.01`. This is distinct from `delta=m-3`, which remains zero.
DOP853 and Radau differ by `3.281e-13`; they use 377 and 2,094 function
evaluations. The DOP853 tolerance ladder uses 92, 197 and 377 evaluations;
the coarse/medium differences from fine are `2.025e-11` and `2.065e-14`.
Fine DOP853 took about 0.0034 s for this one IVP.

Each neural method has 673 trainable parameters, uses 1,000 Adam steps, and
runs seeds 0, 1 and 2. The table reports medians over all three seeds.

| Method | max F error | max raw residual | max normalized residual | max original-PDE residual | train time |
| --- | ---: | ---: | ---: | ---: | ---: |
| hard-IVP PINN | 3.425e-5 | 4.701e-1 | 4.496e-2 | 4.711e-1 | 3.59 s |
| `P2+z^3 N` | 2.670e-6 | 1.804e-1 | 2.535e-2 | 1.831e-1 | 3.81 s |
| `P4+z^5 N` | 3.467e-5 | 5.354e-2 | 5.470e-3 | 5.458e-2 | 4.17 s |

The `P2` correction gives the lowest profile error, while `P4` gives the
lowest residual. This disagreement is retained. Across neural runs the
direct original-PDE residual and the lifted reduced residual differ only at
about `1e-14`; sampled `F'` and the leading coefficient remain regular.
The Taylor controls also show why profile error and residual cannot be merged:
plain `P4` improves profile error over `P2` but has a larger maximum raw
residual on the interval.

The conventional solver is still faster for this single IVP. No speedup,
uniform error certificate, maximal Lie classification, or superiority over
all nonlinear differential-equation solvers is claimed.

## Stage goal: data-compatible certificate and conditional family

The v0.2 stage goal closes one regular local loop rather than attempting the
unresolved generic-`m` classification. For fixed `m=3`
and the supplied generator, certificate v0.2 must establish all of the
following before ML is admitted:

1. the chart `(sigma,rho)=(s*t^2,t)` has nonzero base rank and orbit speed;
2. the PDE pullback is exact and independent of `rho` on the recorded positive
   branch;
3. the data surface `Sigma_0={s*t^2=1}` and all three jet-data residuals are
   invariant under the prolonged action;
4. the pulled data depend only on the quotient coordinate; and
5. `F'=0` and a zero leading coefficient are retained as distinct singular
   exits rather than hidden by division.

With `K=cuberoot(45)`, the certified family is

```text
F(1)=K,  F'(1)=K/3,  F''(1)=-(2K/9)(1+eta_ic),
eta_ic in [-0.02,0.02].
```

The surface and data were chosen because they are symmetry compatible. They
are not yet a claim about real canal initial/boundary measurements. The exact
certificate is also local: `rho=0`, `F'=0`, and `a=0` are excluded boundaries,
not solved branches.

The conditional model

```text
F_hat(sigma,eta_ic) = P2(sigma,eta_ic)
                      + (sigma-1)^3 N_theta(sigma,eta_ic)
```

therefore preserves all three initial jets exactly. It trains on seven values
`{-0.02,-0.015,-0.01,0,0.01,0.015,0.02}` and is tested on the disjoint set
`{-0.0125,-0.005,0.005,0.0125}`. All three seeds and every failure status are
retained.

The refreshed full run has 11/11 regular DOP853/Radau references and 12/12
completed held-out neural evaluations. The maximum cross-solver difference is
`3.312e-13`; sampled reference margins satisfy `min F'=8.986e-1` and
`min |a|=7.114`. Across the held-out runs, maximum profile error ranges from
`2.636e-5` to `1.670e-4`; the direct master-PDE residual and lifted residual
differ by at most `1.616e-14`, and the hard-data jet error is at most
`1.111e-16`.

| held-out `eta_ic` | conditional median max `F` error | Taylor `P2` | Taylor `P4` |
| ---: | ---: | ---: | ---: |
| -0.0125 | 3.045e-5 | 2.050e-2 | 2.400e-3 |
| -0.0050 | 1.318e-4 | 2.061e-2 | 2.410e-3 |
| 0.0050 | 1.383e-4 | 2.077e-2 | 2.425e-3 |
| 0.0125 | 4.631e-5 | 2.088e-2 | 2.436e-3 |

This is evidence that the conditional correction improves these finite Taylor
controls on the declared held-out set. It is not evidence that it beats the
ODE solvers: median training, DOP853-query and neural-query times are 4.625 s,
0.00326 s and 0.00262 s. Their measured arithmetic break-even is about 7,170
queries, before deployment and uncertainty costs, so `ml_speedup_proved`
remains false.

Artifacts are in `sve-family-v02/`: `sve_family_report.json`,
`sve_family_runs.csv`, and `sve_family_comparison.png`. The report separates
exact symbolic guards from sampled branch margins and records explicit
`rank-drop`, `singular-Fprime`, `singular-leading`,
`reference-disagreement`, and `solver-failure` statuses.

## Bounded novelty check

Exact arXiv queries were run on 2026-09-27 for combinations of
Saint-Venant-Exner, Lie symmetry/reduction, Taylor-model PINN and neural
correction. Broader queries recovered TM-PINN, the 2026 PINN--PIKAN benchmark,
PirateNet, symmetry-enforced PINNs, symmetry-domain decomposition, LieSolver,
and Saint-Venant PINNs. The exact combination implemented here was not found
in those bounded queries. A no-result query is not a proof of novelty.

The defensible contribution at this stage is an auditable composition:
a supplied-chart exact reduction certificate gates a reduced neural solver,
and every learned profile is checked after reconstruction in the original
master PDE. The individual ingredients are prior art or classical analysis.
