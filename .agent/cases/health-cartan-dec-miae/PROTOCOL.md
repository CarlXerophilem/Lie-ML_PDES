# Protocol for Cartan-DEC-MiAE

This runbook is the health application at
<https://scientist-two.github.io/#applications/Health%20(Cartan-DEC-MiAE)>,
written so an agent can execute `.agent/WORKFLOW.md` without mixing three
different experiments. The frozen numbers, commands, and gates live in
`contract.json`. Policy decisions live in `.agent/policy.py`.

## Objects

A residue carries a frame `T_i = (E_i, t_i)` in `SE(3)`. The origin `t_i` is
the Cα coordinate. The columns of `E_i` in `SO(3)` are built from backbone
`N`, `Cα`, and `C` as in contract equation `eq-frame`.

The contact graph connects residues whose Cα atoms lie inside a cutoff. The
gallery default cutoff is 8 Å. An edge carries the connection 1-form

```text
omega_ij = log(E_i^T E_j) in so(3)
```

A contact triangle `(i, j, k)` carries the curvature 2-form

```text
Omega_f = omega_ij + omega_jk + omega_ki + (1/2)[omega_ij, omega_jk]
```

with the cross product as the bracket on rotation vectors. The decoder
predicts forms for masked residues and integrates them from a visible anchor:

```text
E_hat_m = E_a exp(sum of omega_hat along the path)
t_hat_m = t_a + sum of E_hat_u theta_hat_e along the path
```

The gallery loss on masked residues is

```text
L = L_theta + L_pos + L_rot + L_omega + L_Omega
```

The independent implementation at commit `720cea1217423968a70ac9046558f60a11ed1af6`
also exposes an integration weight. Stage S6 names the list that was trained.

## Holonomy convention

Appendix A of the gallery PDF states that, on frame-exact coordinates, the
true group holonomy of a closed loop is the identity, because the product of
the relative rotations telescopes. The non-abelian bracket inside `Omega_f`
is the curvature term that remains. Locked reading `N5` therefore requires
the defect score used for masking and features to be the curvature energy
built from `Omega`. A method section records that convention. Open reading
`O2` keeps the body's `||H(gamma) - I||` formula visible as the quantity
Appendix A sets to zero on exact frames.

## Three endpoints

The smoke tier measures whether predicted connection forms integrate back to
the anchor geometry. Its primary metric is
`reconstruction.integrated_position_rmse`. Probe accuracy is stored and is
rejected by `promote` if someone tries to use it as the primary metric,
because the four synthetic families saturate a linear probe.

The paper tier measures 965-way CATH topology classification. Its primary
metric id is `macro_f1`, reported on the TEDBench test split and on external
CATH 4.4, with top-1 accuracy beside it. The encoder, data, step count, and frozen
mean-plus-max MLP probe stay matched to the vanilla MAE baseline. Table 1
of the gallery PDF is the quotation source for that comparison. The
from-scratch curvature-biased row prints 60.18 top-1 and 39.30 macro F1 on
TEDBench, and 64.12 / 37.93 on CATH. The public MiAE-B probe row in the same
table prints 74.20 / 57.79 and 86.09 / 66.73. Those two rows answer different
questions, and both stay in the ledger.

Gallery locked reading `N2` records that MST path integration reaches 2.61 Å
RMSD with 41.95 CATH top-1, while K-shortest integration reaches 3.82 Å with
46.40 CATH top-1. A smoke improvement in RMSE is an observation about the
transport loss. It does not update the transfer comparison.

## Locked results an idea may not overwrite

These are quotation findings. A later smoke run can add a new observation.
It leaves the finding in force on the paper endpoint.

- `N1`. Table 6: span masking at ratio 0.50 prints CATH top-1 50.56 and
  macro F1 13.44. Hard holonomy masking prints 38.47 and 6.14. Soft
  holonomy at temperature 2.0 prints 44.67 and 9.26, still below uniform
  masking at 46.67 and 11.34. Idea `I3` may compare geometry masking on
  smoke RMSE only.
- `N3`. Curvature-only attention prints −0.33 TEDBench and −2.15 CATH top-1
  against the no-bias encoder. Combined heat and curvature attention prints
  +5.75 and +6.33.
- `N4`. The paper claim is the matched delta against vanilla MAE, whose
  Table 1 row is 56.91 / 32.23 on TEDBench and 51.10 / 23.90 on CATH.
  Printed deltas for the DEC objective are +2.39 / +5.50 and +10.69 / +11.03.
- `O1`. Mean entropy in Table 3 is 3.61 for no bias and 3.04 for the
  combined bias, while the prose describes deep-layer collapse of the
  no-bias encoder. A mechanism claim that cites collapse needs a per-layer
  entropy observation that resolves `O1`.
- `O3`. Keep printed cells and printed deltas as separate observations where
  they differ by 0.01. The contract lists each pair.
- `O4`. Ablation tables use the 50K/20K, 10-epoch protocol. Table 1 uses
  369,740 structures and 5 epochs.

## Smoke commands

Commands are templates in the contract. They assume a checkout of the
independent implementation, placed under the run directory, with the
protected files left byte-for-byte as pinned. This repository does not vendor
that code. A run that has `compute_authorization = smoke-only` may execute
the smoke templates. `authorize_training` rejects a paper-tier command under
that authorization.

The baseline turns curvature bias, heat bias, connection loss, curvature
loss, and integration loss off. `I1` restores the full Cartan-DEC objective.
`I2` sets the integration and connection weights to 4. `I3` switches the
mask strategy to `geometry`. `I4` is the single evolved idea: `I2` plus
curvature weight 2. Ablations `A1`–`A4` each remove one of those ingredients.
Supplementary `R1` lengthens chains to 80–140 residues. `R2` switches to
random masking.

Screening uses 96 training chains, 8 epochs, and seeds 0 and 1. The full
smoke grid uses 160 chains and 15 epochs. The test split is generated with
seed offset 10000. The reconstruction mask seed is 1234. Subset and full
budgets are otherwise the architecture in `smoke_budget`.

## Stage actions

S0. Hash `contract.json` into the ledger. Set `tier` to `smoke` unless the
human authorization says `quote` or `paper`. Copy `run-template.json` to
`build/cartan-dec-miae/<run-id>/ledger.json`.

S1. Copy limitations `L1`–`L4` into the ledger. Add a limitation only with a
test that names one metric in the active tier.

S2. Copy ideas `I1`–`I3` and evolved idea `I4`. Reject an idea whose command
edits a protected path or whose expected claim uses a Table 1 number as a
smoke measurement.

S3. Run the subset budget. Build one observation per seed from `metrics.json`.
Call `promote` with `primary_metric` equal to
`reconstruction.integrated_position_rmse`, direction `min`,
`min_relative_gain` 0.05, and `probe.accuracy` forbidden.

S4. Rerun promoted ideas at the full smoke budget. Train `I4` only if `I2`
was promoted. Select the best primary metric. Record a decision of
`none_promoted` when the gate fails. That decision is a finished result.

S5. Run `A1`–`A4` from the selected command by changing one factor. Call
`ablation_status` with `min_gain` 0.03 and `clean_fraction` 0.75. Three of
the four ablations must worsen the primary metric by at least 3 percent
relative before the manuscript may say the attribution is clean.

S6. Write the draft from admitted claims. `admit_claim` rejects a
measurement that cites a quote-tier observation, and rejects a mechanism
claim that requires `O1` without a resolving observation.
`unbacked_numbers` must be empty.

S7. The reviewer works from the contract and the ledger. The first health-case
pattern in the smoke implementation expects the opening draft to miss the
threshold, then runs `R1` and `R2`. A rebuttal that only rewrites sentences
leaves the objection open.

S8. Accept at review score 9.0 or higher with an ablation status recorded.
That threshold is the smoke-case gate recorded by the Scientist3 health case.
The project page's ScholarPeer mean of 7.5 is a separate, already-published
aggregate and is not a substitute for this gate. One revision is available.
The second miss rejects the run. A run that promotes no idea still closes,
with `none_promoted` as the result.

S9. Re-execute the selected command and compare every manuscript number with
the new `metrics.json`. Confirm the protected paths still match the pinned
checkout. Confirm each citation resolves. Confirm the method section states
the loss list, the mask, the anchor path, and the `N5` holonomy convention.
A skipped re-execution is status `partial` and cannot accept.

## Dissertation boundary

This case studies residue frames for protein backbones. The dissertation in
`draft/dissertation_wku.tex` keeps its frozen questions, its multi-parameter
Saint-Venant–Exner systems, and its printed scalar models. A ledger note may
record that both documents use the name Cartan, and that note carries no
observation id for either document's theorems.
