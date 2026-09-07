# LieML Research Training Runbook

## Purpose

This runbook executes the bounded, auditable pilot for the generic `(p,q,r)`
Lie-PDE kernel. The exact checker creates labels; the CPU tree ranks candidate
reductions. The ML result is never a certificate and never removes a branch.

## Local smoke run

From the project root:

```text
python -m symm.generic.research_cli --output research_artifacts/pilot
python -m pytest symm/tests -q --disable-warnings
```

The pilot writes:

- `corpus_manifest.jsonl`: shape, provenance, domain tag, and system fingerprint;
- `oracle_records.jsonl`: candidate features, exact status, checks, timing, and RSS;
- `model.json`: JSON-safe depth-limited CPU tree and model fingerprint;
- `evaluation.json`: grouped held-out ranking and abstention metrics;
- `run_metadata.json`: resource policy, status counts, and system fingerprints;
- `REPORT.md`: a short human-readable run summary.

The checked-in registry is structural validation data. Its boundary/initial
conditions and external publication provenance are intentionally marked as
missing until supplied from authoritative sources.

## Cloud policy

The target VM configuration is `configs/sa9.8xlarge64.json`:

- 32 vCPU and 64 GiB RAM;
- four exact-worker slots for Maple/REDUCE when licensed and installed;
- twelve vCPU for feature extraction and CPU ML;
- eight vCPU reserved for I/O, retries, and the operating system;
- at least 200 GiB fast disk;
- no GPU requirement;
- approximately 1.8 GB RSS hard limit per worker.

The ten-hour schedule is: preflight (30 minutes), corpus/provenance (90
minutes), exact oracle labels (3 hours), ML/features (2 hours), active hard
cases (2 hours), and held-out evaluation/package (1 hour).

Maple and REDUCE binaries, licenses, credentials, and customer data must not
be copied into the repository or artifacts. If a backend is absent, the run
must retain `backend-unavailable`; an executable discovery result alone is not
an exact adapter or a proof certificate.

## Acceptance gates

- Existing scalar and generic tests remain green.
- No model score upgrades a certificate status.
- Every `verified` label passes the exact local checks available to that path.
- Held-out split is by PDE case/family, not by duplicate candidate rows.
- Recall@5, abstention, confident precision, status counts, RSS, and runtime are
  reported even when a target gate fails.
- Full differential completion remains explicitly unverified until a
  version-pinned Maple or REDUCE adapter produces replayable output and the
  Python-side checks pass.
