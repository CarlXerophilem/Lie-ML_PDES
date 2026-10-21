# Historical Live Simulation

Preserved in [the hash-verified carrier](../archives-20261021/live-simulation-20260925.zip).
Run from the repository root:

```bash
git lfs pull --include='research_artifacts/archives-20261021/live-simulation-20260925.zip' --exclude=''
python -B -X utf8 scripts/evidence_archive.py restore --archive research_artifacts/archives-20261021/live-simulation-20260925.zip --root .
```

Restoration does not start services or reinterpret historical logs. See
[archive policy](../archives-20261021/README.md).
