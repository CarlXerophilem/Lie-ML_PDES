# Historical Evidence Carriers

The [cleanup delivery](CLEANUP.md) records measurements, verification and limits.

These new carriers preserve original paths and file bytes. Older frozen ZIPs
and embedded manifests were not rebuilt. The original expanded historical trees
are not current executable dependencies. References and current sources remain
outside this compaction.
Two original INSPECTION.md documents are also retained byte-identically at
their historical paths because the frozen 16 October publication links to them.

| Carrier | Preserved files |
|---|---:|
| [mathematics-and-symmetries.zip](mathematics-and-symmetries.zip) | 899 |
| [fluid-baseline-20260925.zip](fluid-baseline-20260925.zip) | 67 |
| [free-boundary-scope-inspection-20261014.zip](free-boundary-scope-inspection-20261014.zip) | 65 |
| [live-simulation-20260925.zip](live-simulation-20260925.zip) | 17 |
| [three-layer-baselines-20260927.zip](three-layer-baselines-20260927.zip) | 17 |
| [pilot.zip](pilot.zip) | 6 |
| [dissertation-title-inspection-20261014.zip](dissertation-title-inspection-20261014.zip) | 1 |
| [p0-near-cubic-20261007.zip](p0-near-cubic-20261007.zip) | 1 |
| [root-history.zip](root-history.zip) | 4 |

Adjacent `*.manifest.json` files include SHA-256 for every payload member and the
carrier itself. ZIP payloads use Git LFS; fetch the desired archive before use:

```bash
git lfs pull --include='research_artifacts/archives-20261021/fluid-baseline-20260925.zip' --exclude=''
python -B -X utf8 scripts/evidence_archive.py verify --archive research_artifacts/archives-20261021/fluid-baseline-20260925.zip
python -B -X utf8 scripts/evidence_archive.py restore --archive research_artifacts/archives-20261021/fluid-baseline-20260925.zip --root .
```

Restore preserves extra `ARCHIVED.md` stubs, accepts identical existing bytes,
and refuses conflicting bytes or linked paths. Restored historical files are
ignored so that optional replay does not become a new publication accidentally.
No missing historical archive or archived negative result is relabelled a pass.
