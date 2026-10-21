# Published computational evidence — 21 October 2026

These carriers supplement the immutable [19/20 October snapshot](../sve-current-20261021/README.md).
Together they preserve every currently available ordinary file in the active
build directories at publication, including failed attempts, numerical samples,
series, exact certificates, review receipts, figures, logs and test fixtures.
Python caches and optional pytest alias links are omitted; their ordinary
numbered target files remain present. No original evidence was deleted.

| Carrier | Files | Compressed bytes | SHA256 |
|---|---:|---:|---|
| [library-evidence.zip](library-evidence.zip) | 6,445 | 23,681,696 | `9a138519e9362ba84da42e45a3ef509aa889dfa4b85d25b9e518dbbd175c8481` |
| [printed-P-evidence.zip](printed-P-evidence.zip) | 6,531 | 41,568,904 | `01f2581e45fcc1e38220bbc4b6da80de1342d597e74882041d690bd7214a94a9` |
| [other-current-evidence.zip](other-current-evidence.zip) | 4,650 | 6,495,279 | `4b1f21d8f829a0e6ea36c1c65f1e5632d8b2bb692ac97a73a88d63e3e4c7a22d` |

All carriers passed a hash comparison against the live source files. The
[snapshot metadata](snapshots.json) records file counts, byte counts, optional
aliases and excluded cache directories. Each ZIP contains a complete per-file
`ARCHIVE_MANIFEST.json`; restoration verifies it and refuses changed local files.
The older carrier has no changed overlapping files.

See the [root README](../../README.md) for Ubuntu installation, astra synchronization,
restoration and reproduction commands. After restoration open:

- [Current P solution delivery](../../build/sve-P-solutions-20261021/DELIVERY.md)
- [P surface demo](../../build/sve-P-solutions-20261021/campaign-reviewed/index.html)
- [Library packaging and prior-art review](../../build/lie-symm-library-20261021/PACKAGING.md)

## Status and publication scope

The [printed-P receipt](printed-P-validation.json) records 18 registered families,
12/12 exact demonstrations, 21/21 seed IVPs and 10/11 extended IVPs. The remaining
finite-difference PDE diagnostic and missing 11 October archive remain failures.
General closed forms and untreated singular continuations are unresolved.

This publication includes the LieSymm source, frozen source snapshot, related
project status/plan/audit fixes, and all available active computation evidence.
Concurrent draft-document and Lie-note edits, new unrelated reference downloads,
and the local conversation dump remain in the working directory outside this
publication. Their bytes are not reset or overwritten.

The pre19 video/intermediate archive stays machine-local as documented in the
[archive guide](../../docs/build-archive-20261021.md). The absent 11 October archive
cannot be published. Those are separate historical gaps, not silently filled
by these current carriers. Frozen Windows execution paths remain provenance.
The release restore and tests are run locally on Windows; no full Ubuntu
numerical campaign is claimed.

## Publication checks

[Restoration validation](restore-validation.json) confirms 28,475 restored files
across all four carriers. An isolated checkout of the staged library preserved
all 445 source/evidence files exactly and passed its integrity gates. The current
[library/scalar suite](publication-library-tests.txt) passed 66 tests; the
[retained suite](publication-retained-tests.txt) passed 110 tests, including the
43 active-package tests. The first combined run was interrupted after prolonged
symbolic computation; its status is retained in publication-test-interruption.json.
No mathematical source changes or relaxed tolerances were used for the reruns.

[Publication validation](publication-validation.json) and
[the project audit](publication-audit.json) retain the known failures. The
[README command check](readme-command-check.json) checks Bash syntax, not a full
Ubuntu execution. Unrelated local edits remain byte-identical to the scope receipt.
