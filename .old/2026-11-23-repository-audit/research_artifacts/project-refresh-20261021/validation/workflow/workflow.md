# Manuscript symmetry workflow

Replay: **passed**. Workflow: **scoped-replay-complete**.

A passing replay applies to the declared scalar benchmark and constructed reference family. It does not establish maximal SVE classification, full physical IBVP equivalence, or neural speedup.

| Stage | Status | Evidence and scope |
|---|---|---|
| 1. Freeze the model | verified | Two declared scalar models; nondimensional fixed g,kappa and positive branch. [Exact checks](workflow.json#checks), [Scalar theory](..\..\..\..\research_artifacts\sve-progress-20261010\docs\THEORY.md) |
| 2. Verify symmetry candidates | verified | Parameter examples and exact Xc/X5 identities; first-order X5 obstruction. No independent maximal classification. [Exact checks](workflow.json#checks), [Scalar theory](..\..\..\..\research_artifacts\sve-progress-20261010\docs\THEORY.md) |
| 3. Select subgroup and rank | verified | Singleton Xc is bracket closed; local projected and total rank are one. [Exact checks](workflow.json#checks), [Scalar theory](..\..\..\..\research_artifacts\sve-progress-20261010\docs\THEORY.md) |
| 4. Construct the quotient chart | verified | y=log(t), z=s/t, v=phi/t; exact inverse and Jacobian checks. [Exact checks](workflow.json#checks), [Scalar theory](..\..\..\..\research_artifacts\sve-progress-20261010\docs\THEORY.md) |
| 5. Pull back jets and data | verified | Exact jet pullbacks and compatible normalized three-jet data on s=t; the declared scalar density/source/flux and incompatible controls pass. Arbitrary physical IBVPs remain separate. [Exact checks](workflow.json#checks), [Scalar theory](..\..\..\..\research_artifacts\sve-progress-20261010\docs\THEORY.md), [Data and flux checks](..\data-flux\data_flux.json) |
| 6. Certify reduced equations | verified | Independent direct pullbacks at m=1,2,3,4; arbitrary-m scaling and first-integral identities. [Exact checks](workflow.json#checks), [Scalar theory](..\..\..\..\research_artifacts\sve-progress-20261010\docs\THEORY.md) |
| 7. Approximate the profile | numerically-replayed | Twelve classical controls regenerated; 40 stored comparisons are historical, including 16 exhausted budgets. No training. [Classical controls](classical\classical_results.json), [Historical comparisons](..\..\..\..\research_artifacts\sve-progress-20261010\results\experiment_results.json) |
| 8. Reconstruct and validate | numerically-replayed | Local bed compatibility, exact reference-family rational tube, and independent second-/third-order controls. Candidate guards remain sampled. [Exact checks](workflow.json#checks), [Scalar theory](..\..\..\..\research_artifacts\sve-progress-20261010\docs\THEORY.md), [Classical controls](classical\classical_results.json) |
| 9. Report scope and total cost | verified | Source hashes, exact/numerical distinctions, failures and historical budgets retained; no measured neural speedup. [Detailed report](workflow.json), [Readable report](workflow.md) |

## Replay checks

- verify_power_diffusion: **verified**
- verify_quadratic_reaction: **verified**
- verify_nonzero_resonance_counterexample: **verified**
- common_scaling_chart: **verified**
- scalar_model_printed: **verified**
- scalar_model_physical_corrected: **verified**
- local_bed_reconstruction: **verified**
- classical_controls: **verified**

Historical comparisons: 40; budget exhausted: 16. These are stored measurements; no learning was rerun.

Specific data/flux compatibility: verified-constructed-data-flux.

Exact and numerical results, source hashes, per-case controls and historical failures are in workflow.json.
