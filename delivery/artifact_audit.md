# Disposition of the research artifacts

This inventory covers the 23 top-level packages in the pre-audit `research_artifacts/` tree at commit `126a598`. Their original trees are preserved in the [audit archive](../.old/2026-11-23-repository-audit/research_artifacts/) and in Git history. The current dissertation uses the maintained paths below.

| Former package | Evidence and disposition |
|---|---|
| `annular-transcritical-theorem-20261101` | Proof and replay carried forward into [delivery](annular-transcritical-theorem-20261101/README.md). Contains the shared affine search, invariant coordinates, undivided radial equation, independent Cartesian checker, proof and versioned receipts. The archived ZIP reference retains its original Git LFS status. |
| `SVE-reproduced-20261012` | Replaced for current use by [the deterministic published-scalar reproduction](reproduce_sve2026.py). The older Fehlberg/DOP853 results, extended source transcriptions and figure work stay in the archive. |
| `sve-progress-20261010` | Frozen scalar benchmark of 12 classical references and 40 approximation runs. Its archived run-level records retain 16 budget stops, including all 12 Taylor–tanh runs. The maintained delivery has separate controlled cases. |
| `SVE-2D-extension-20261014` | Early reviewed 2D extension, accepted and rejected claims, and validation. Kept as provenance for the later annular theorem and rotating-exchange example. |
| `dissertation-title-inspection-20261014`, `free-boundary-scope-inspection-20261014` | Title and scope inspections. Moving shorelines and free-boundary results remain outside the proved model classes. |
| `fluid-baseline-20260925`, `live-simulation-20260925`, `pilot`, `three-layer-baselines-20260927` | Exploratory reductions, deployment and classical/learning baselines. Historical evidence, distinct from the current dissertation's controlled cases. |
| `p0-near-cubic-20261007` | Near-cubic obstruction within the declared diagonal-scaling ansatz. Retained as a scoped negative result. |
| `mathematics-and-symmetries`, `archives-20261021` | Reading and study material, historical evidence carriers and restoration instructions. Preserved under the archive. |
| `publication-20261016`, `project-refresh-20261021` | Publication checkpoints, independent review and integrity/provenance records. |
| `sve-1d-programme-20261021` | Exact-first reduction catalogue, source ledger, solver criteria and proof boundaries. The maintained executable proof and orbit ledger are in [delivery](VERIFICATION.md). |
| `sve-P-residual-20261021`, `sve-current-20261021`, `sve-delivery-20261021` | Portable publications, precision repair and validation. The high-precision cross-check passed 11/11; the original float64 campaign retained its 10/11 outcome and its failing trace. See the archived [precision report](../.old/2026-11-23-repository-audit/docs/residual-resolution-20261021.md). |
| `sve-acceptance-review-20261027`, `sve-final-20261027`, `sve-lie-retry-20261027` | Strict CAS and native retry records, including failed acceptance, incomplete elimination, and operational failures. The later exact hand-derived certificates have a narrower explicit contract. |
| `sve-regular-correction-20261117` | Imported regular prototype and source-level review, with no new training run certified by the import. The \(P\)–\(M\) continuation code and comparison log are separately archived as deferred work. |

The active delivery contains the released mathematical dependencies. The archive keeps former relative layout and original bytes where possible. For checkout-dependent historical runners, use the recorded baseline commit, because the archive has different directory ancestry.
