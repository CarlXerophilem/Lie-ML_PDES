# Three-layer research demos

These command-line programs deliberately keep the three claims separate.

```powershell
python -B -m symm.research_demos.ml_only --output-dir research_artifacts/three-layer-baselines-20260927/ml-only
python -B -m symm.research_demos.lie_only --output-dir research_artifacts/three-layer-baselines-20260927/lie-only
python -B -m symm.research_demos.fusion `
  --certificate research_artifacts/three-layer-baselines-20260927/lie-only/lie_only_report.json `
  --output-dir research_artifacts/three-layer-baselines-20260927/fusion --steps 1000
python -B -m symm.research_demos.sve_family `
  --certificate research_artifacts/three-layer-baselines-20260927/lie-only/sve_certificate_v02.json `
  --output-dir research_artifacts/three-layer-baselines-20260927/sve-family-v02 --steps 1000
```

Use `--quick` on the ML-only, fusion or SVE-family command for a wiring smoke
test. A quick run is not performance evidence.

## Scope

- `ml_only.py` imports no Lie-reduction code. It runs a bounded fixed-IVP
  Duffing comparison and the configured logistic MLP-PINN/PIKAN comparison.
- `lie_only.py` imports no neural-network library. It checks the supplied
  `m=3` chart and multiplier identity exactly and retains `m=4` as a negative
  control. This is not a maximal symmetry classification.
- `fusion.py` refuses to run without the verified JSON emitted by
  `lie_only.py`. It compares exact/Taylor/numerical controls with three neural
  profiles and checks the reconstructed master-PDE residual.
- `sve_family.py` requires the stricter v0.2 certificate. It trains one
  conditional profile on seven initial-curvature values and evaluates every
  seed on four disjoint held-out values. It records regular and singular
  branch statuses rather than treating every solver failure as equivalent.

The v0.2 scope is deliberately local: fixed `m=3`, the supplied
`X_5=t*d_t-2*s*d_s` chart, positive regular branch and the constructed
invariant data surface `s*t^2=1`. It is not a generic-`m` classification or a
certificate for an arbitrary physical boundary-value problem.

The cubic PIKAN is not transferred to the SVE residual because a standard
cubic spline does not provide the global smoothness required for an unchecked
third derivative. PirateNet remains a literature comparator rather than a
reproduction in this CPU/PyTorch implementation.
