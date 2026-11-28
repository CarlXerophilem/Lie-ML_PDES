# Case: Health (Cartan-DEC-MiAE)

Source page:
<https://scientist-two.github.io/#applications/Health%20(Cartan-DEC-MiAE)>

The gallery manuscript recasts masked autoencoding of protein backbones as
prediction and integration of Cartan connection and curvature forms. This case
file freezes three tiers so those results keep their own endpoints.

| Tier | What it can support | Primary endpoint |
| --- | --- | --- |
| `quote` | Printed numbers from the 11-page gallery PDF | none; the run writes a reading memo |
| `smoke` | Synthetic 60–90 residue chains, CPU budget in the contract | integrated position RMSE, lower is better |
| `paper` | A future matched run on TEDBench and CATH 4.4 | macro F1 on both splits |

The default authorization is `smoke-only`. Paper-tier training waits for
`paper-authorized` in the ledger.

Read `PROTOCOL.md` for the equations, the locked negative results, and the
stage runbook. The JSON contract is what `.agent/policy.py` loads.
