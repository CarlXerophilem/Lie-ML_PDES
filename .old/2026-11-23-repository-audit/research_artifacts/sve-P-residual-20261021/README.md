# Printed-P Precision Evidence

[precision-evidence.zip](precision-evidence.zip) contains the 398 files verified
by the existing delivery manifest and its three manifest files: **401 files**.
The 9,795 pytest scratch files were not research outputs and are excluded.
Original campaigns, negative controls, logs and the independent review remain.
The [carrier manifest](precision-evidence.manifest.json) records exact hashes.

```bash
git lfs pull --include='research_artifacts/sve-P-residual-20261021/precision-evidence.zip' --exclude=''
python -B -X utf8 scripts/evidence_archive.py verify --archive research_artifacts/sve-P-residual-20261021/precision-evidence.zip
python -B -X utf8 scripts/evidence_archive.py restore --archive research_artifacts/sve-P-residual-20261021/precision-evidence.zip --root .
```

After restoration open `build/sve-P-residual-20261021/campaign-reviewed/index.html`.
The reference-checked campaign has 12/12 exact, 21/21 seed and 11/11 extended
cases. The old raw float64 failure and frozen 10/11 campaign are retained. These
are sampled numerical/reference checks, not a continuous PDE certificate for
double-precision interpolants. See [the precision account](../../docs/residual-resolution-20261021.md).
