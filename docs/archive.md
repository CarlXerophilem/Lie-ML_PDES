# Preserved history and evidence integrity

The cleanup starts from Git commit `3bc20b0`. A SHA-256-verified snapshot of all
1,502 then-tracked entries is stored outside this repository at
`../Lie-ML_PDES-archive/2026-10-11`. Its `ARCHIVE_MANIFEST.json` records hydrated
file bytes and symlink targets. The backup branch
`backup/astra-before-cleanup-20261011` also retains the original tracked history.
The external snapshot is local to this machine; Git history is the portable
recovery route. Neither is a complete export of inaccessible account history.

Historical manuscripts, chat excerpts, source inventories, deployment files,
and superseded experiment bundles were removed from the active reading tree
after verification. Existing `symm` package paths were kept for compatibility.
Ignored local `ref/kb/` files were preserved and remain outside the canonical
portable reference corpus.

## Current experiment carrier

The 2026-10-10 frozen ZIP and its manifest remain byte-for-byte unchanged. All
78 manifest entries match the ZIP. The expanded checkout omits 52 NPZ files
(40 candidates and 12 references), all recoverable from that carrier. Three
expanded outputs differ from the frozen versions: `experiment_results.csv`,
`pytest.txt`, and `symbolic_certificates.json`. They must not be presented as
the original frozen bytes. Read the current source/certificates and replay into
a fresh output directory; preserve the frozen carrier for provenance.

The older imported export already lacked 216 manifest-listed entries before
this cleanup. The external archive preserves what was actually available;
it does not reconstruct those missing original files. Archived project chats
are partial excerpts and labeled summaries, not native ChatGPT memories.

`python scripts/project.py audit` verifies the local external archive,
canonical PDF hashes, active links and frozen ZIP entries. Its JSON reports
which expanded files are missing or revised. The small cleanup baseline is
recorded in `cleanup.json`; the full archive manifest stays outside the active
reading tree.
