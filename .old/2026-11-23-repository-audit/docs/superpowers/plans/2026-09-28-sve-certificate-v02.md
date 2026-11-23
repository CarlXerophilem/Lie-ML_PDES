# SVE Reduction Certificate v0.2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the fixed `m=3` SVE baseline to a strict-data-compatible regular-branch certificate and a one-parameter, held-out-evaluation reduced-profile model without claiming complete symmetry classification or ML speedup.

**Architecture:** Keep the existing generic chart reducer and v1 demos compatible. Add a deliberately strict sufficient test for data invariance to the chart outcome, build an SVE-specific v0.2 certificate on the invariant surface `sigma=st^2=1`, and place the parameter-family numerics/ML in a new research-demo module that consumes that certificate. Exact symbolic evidence and sampled numerical branch evidence remain separate in every report.

**Tech Stack:** Python 3.14, SymPy, NumPy, SciPy `solve_ivp`, PyTorch CPU, pytest, Matplotlib, LaTeX.

**Spec:** Active thread Goal created 2026-09-28; the user-approved mathematical target is the fixed `m=3`, `X5=t*d_t-2*s*d_s` regular chart with invariant data surface and initial-curvature parameter family.

## Global Constraints

- Preserve the existing `lieml.three-layer.*.v1` reports and all legacy APIs.
- Work in the current dirty checkout because the v1 baseline is uncommitted authoritative state; do not revert, commit, or overwrite unrelated changes.
- Use only the fixed `m=3` branch; `eta_ic` is a data parameter and must remain distinct from `delta=m-3`.
- Label exact symbolic checks separately from sampled numerical regularity checks.
- Retain every parameter/seed result and every failure status.
- Do not claim generic-`m` completeness, maximality, an equivalence-group result, `m=3+delta` continuation, global topology, interval certification, or ML speedup.

## Review Focus

- A data condition can be compatible only when both its base surface and jet residuals are invariant under the prolonged action.
- The generic reducer must not reject a valid PDE reduction merely because supplied data are incompatible.
- `F'=0` and `a=0` must be reported as distinct singular statuses rather than solver noise.
- Training and held-out `eta` values must be disjoint, with hard preservation of `F(1)`, `F'(1)`, and `F''(1;eta)`.
- Direct master-PDE and lifted reduced residuals must be compared independently on reconstructed fields.

## Task 1: Strict data compatibility and SVE v0.2 certificate

- [ ] Add failing tests for exact SVE data invariance, orbit-independent pullback data, and preservation of `pulled-back-only` for incompatible data.
- [ ] Extend `ChartReductionOutcome` with serialized data-invariance checks/residuals without changing reduction status.
- [ ] Add `sve_data_family_case()` with `Sigma0={st^2=1}` and the three invariant data residuals.
- [ ] Make Lie-only emit `sve_certificate_v02.json` containing the structural classification, exact rank guards, data proof, reduced equation and singular guards.
- [ ] Run focused chart/demo tests.

## Task 2: Reference family and branch statuses

- [ ] Add failing tests for the complete status vocabulary and DOP853/Radau regular references.
- [ ] Create `symm/research_demos/sve_family.py` with declared train/held-out `eta` sets.
- [ ] Generate DOP853/Radau references, branch margins and explicit failure records for every `eta`.
- [ ] Keep exact rank evidence separate from sampled `F'`/`a` evidence.
- [ ] Run focused numerical tests.

## Task 3: Parameter-conditioned reduced profile

- [ ] Add failing tests that the conditional `P2+z^3 N(sigma,eta)` preserves all three initial jets for multiple unseen `eta` values.
- [ ] Train seeds 0, 1 and 2 using only the reduced residual on declared training parameters.
- [ ] Evaluate every seed on held-out parameters against DOP853 and Taylor `P2/P4`.
- [ ] Record profile derivatives, raw/normalized residuals, original-PDE residual, lifting difference, branch margins and costs.
- [ ] Report a finite amortization break-even only when the measured denominator is positive.

## Task 4: Artifacts, manuscript and verification

- [ ] Emit JSON, CSV and PNG artifacts plus source hashes and rerun commands.
- [ ] Update the README, baseline document, checklist, research record and `draft/main.tex` with bounded claims.
- [ ] Run focused tests, full repository regression, standalone historical ML checks and three independent CLI smoke runs.
- [ ] Compile and visually inspect the manuscript and update the verification record.
- [ ] Perform a requirement-by-requirement completion audit before updating the active Goal.

