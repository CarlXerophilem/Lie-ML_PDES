# Portable current build evidence — 21 October 2026

[current-build.zip](current-build.zip) preserves the 19/20 October working evidence
and the dissertation's `week-4` inputs at their original repository-relative paths.
No frozen stage gate or historical failed receipt was rewritten.

- Archive SHA256: `270dc54d2a33589500251e8a6031db65eda40b099aefe900591578e2d32a031e`.
- 10849 ordinary files; 107,622,521 uncompressed bytes;
  52,892,588 compressed bytes.
- All 4,924 files bound by the general-symm RELEASE_MANIFEST match exactly.
- Optional pytest current aliases and Python bytecode caches are omitted. The
  full ordinary numbered-test targets remain included. See [snapshot.json](snapshot.json).

From the repository root after cloning:

```powershell
python -X utf8 scripts/build_archive.py verify --archive research_artifacts/sve-current-20261021/current-build.zip
python -X utf8 scripts/build_archive.py restore --archive research_artifacts/sve-current-20261021/current-build.zip
```

Restore refuses to overwrite different local bytes. Existing identical files
are retained. The ZIP includes `build/sve-general-symm-20261020`,
`build/sve-systematic-20261020`, `build/sve-autonomous-20261019`, and `build/week-4`.
It does not contain the obsolete pre19 build archive or the absent 11 October
hydrated historical snapshot. Old absolute paths inside frozen execution receipts
remain provenance; new execution must use the current root and fresh outputs.

After restoration read the [20 October delivery](../../build/sve-general-symm-20261020/DELIVERY.md).
The [new 1D programme](../sve-1d-programme-20261021/README.md) is tracked as readable
source and records further work separately from the frozen package.

Frozen gate receipts retain Windows separators and execution paths. Restoration
and gate revalidation were tested on Windows; a non-Windows gate replay has not
been validated and may require a path adapter without modifying frozen bytes.
