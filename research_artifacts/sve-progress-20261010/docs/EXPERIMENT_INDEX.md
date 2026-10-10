# Experiment artifact index

This directory is the external evidence package for the SVE work reported on
2026-10-10. draft/main.tex contains only a short evidence pointer; experiment
protocols, outputs, and historical records live here.

## Current reproducible evidence

- [README](../README.md): environment, run commands, file map, and evidence
  boundary.
- [THEORY](THEORY.md): the two declared scalar models, the general smooth
  point-correction obstruction, the common-scaling reduction, the extra first
  integral, and the local physical-model reconstruction.
- [FINDINGS](FINDINGS.md): measured classical and approximation results,
  including failed or budget-exhausted runs.
- [Symbolic certificates](../results/symbolic_certificates.json): exact
  machine-readable witness data.
- [Reference tube certificates](../results/reference_tube_certificates.json):
  exact rational bootstrap certificate for the reference family.
- [Experiment results](../results/experiment_results.json): run-level budgets,
  seeds, statuses, errors, residuals, and timings.
- [Manifest](../MANIFEST.json) and
  [frozen ZIP](../lie-ml-sve-progress-20261010.zip): frozen package inventory
  and complete evidence carrier.

The current package records 38 passing tests, 12 classical reference cases,
and 40 bounded approximation runs. Sixteen learned runs reached the evaluation
budget. The Chebyshev control was most accurate on this small smooth benchmark,
so the artifact makes no ML speedup or neural-superiority claim.

## Archived manuscript material

[LEGACY_MANUSCRIPT_EXPERIMENTS.tex](LEGACY_MANUSCRIPT_EXPERIMENTS.tex) is a
verbatim extraction of the former manuscript block containing the prospective
ML protocol, unreproduced historical numerical reports, the fixed-\(m=3\)
family study, and the old implementation listing. It is retained for
provenance, is not included by draft/main.tex, and must not be cited as current
evidence.

## Supersession rules

1. THEORY.md, FINDINGS.md, and the JSON certificates govern current claims.
2. The exact witness
   \(\operatorname{coeff}_{p^2q^2}(q^3\partial_{\phi_{tss}}\Omega)
   =3g\kappa\ne0\) supersedes the
   archived diagonal-scaling-only status.
3. Generalized, contact, nonlocal, nonclassical, singular-parameter, and FS
   symmetry questions remain open. The result is not a maximal point-algebra
   classification and does not cover the full bed-field SVE system.
4. Numerical consistency and held-out residuals are not rigorous continuous
   error bounds. Budget exhaustion is reported as such, not as convergence.
