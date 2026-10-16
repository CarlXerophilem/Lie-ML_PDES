# Research publication checkpoint, 2026-10-16

This checkpoint publishes the 2D SVE extension and the dissertation-title and
related free-boundary scope inspections. It does not implement new PDE input
support, change the dissertation title, or modify the manuscript. Other local
manuscript, reproduction, slide and reference-corpus changes are excluded.

## Reading Order

1. [2D SVE calculation](../SVE-2D-extension-20261014/README.md).
2. [Title inspection](../../build/dissertation-title-inspection-20261014/INSPECTION.md).
3. [Free-boundary scope inspection](../../build/free-boundary-scope-inspection-20261014/INSPECTION.md).

The last two directories are intentionally tracked exceptions to the existing
`build/` ignore rule. No pytest temporary tree or unrelated build output is
published. The inspections are dated recommendations, not approved manuscript
changes or claims of implemented free-boundary support. Some historical links
and receipts name the original Windows checkout; use the repository-relative
links above in another checkout. Chat-only calculations mentioned by the title
inspection are not part of this release's verified evidence.

## Source Copies And Integrity

`PUBLICATION_MANIFEST.json` distinguishes included files from intentional
source-copy exclusions and gives their original SHA-256 hashes. The original
`MANIFEST.json` and `RELEASE_MANIFEST.json` remain unchanged: they describe the
complete local research snapshots, not a promise that every third-party
source copy is redistributed in Git. Missing entries listed as exclusions in
the publication manifest are therefore expected in a fresh clone.

Paper PDFs, full-text extractions, page images and publisher-page captures
without verified redistribution permission remain local. Retrieval receipts,
version-specific URLs, hashes and the source audits are published. Restore
excluded sources from their recorded URLs, checking the recorded hashes,
before attempting a complete source-copy audit. Text/image derivatives must
also match their recorded extraction/rendering hashes; a new extraction is
not silently equivalent to the frozen one.

The retained Chavarrias article and its extracted/rendered derivatives are
attributed to Victor Chavarrias, Ralph Schielen, Willem Ottevanger and Astrid
Blom, *Ill posedness
in modelling two-dimensional morphodynamic problems: effects of bed slope
and secondary flow*, Journal of Fluid Mechanics (2019),
[DOI:10.1017/jfm.2019.166](https://doi.org/10.1017/jfm.2019.166), under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The PDF is unmodified; the text extracts and page images are format conversions.
Consult the source manifest for authoritative author metadata and provenance.

## Replay Without Rewriting Frozen Receipts

From the repository root:

```powershell
$env:PYTHONUTF8='1'
python -B research_artifacts/SVE-2D-extension-20261014/main.py --out build/publication-replay/sve-2d
python -B -c "import runpy,json; m=runpy.run_path('build/free-boundary-scope-inspection-20261014/verify_scope.py'); print(json.dumps(m['run'](),indent=2))"
python -B -m pytest -q -p no:cacheprovider scripts/tests symm/tests/test_chart_reduction.py symm/tests/test_engine.py research_artifacts/sve-progress-20261010/tests research_artifacts/SVE-2D-extension-20261014/tests --basetemp=build/publication-replay/pytest
```

The original `verify_scope.py` entry point and `run_validation.py` write into
their inspection directory. Use the read-only `runpy` call above for a replay.
The historical `results/reviewer/independent_checks.py` is an original-run
receipt, not a portable CLI: it expects restored source PDFs and its original
`build/sve-2d-extension-20261014/reviewer-replay/` location with matching replay
outputs. The supported scientific replay commands above need no source PDFs.

## Current Validation

Fresh checks on 2026-10-16 in the existing working tree: 104 selected tests
passed; the SVE replay returned 68 zero remainders and five detected negative
controls; the scope replay returned 14 zero identities and three negative
controls. The data-flux checker and workflow runner passed. Both original local
manifests were hash-checked successfully (106 and 72 entries).

The repository audit failed with 227 issues in the current working tree,
including missing archive/reference paths and historical links. This is not
the older 218-issue snapshot reported in the frozen inspections. No clean
repository audit or new LaTeX build is claimed. Current replay outputs are in
the ignored `build/publication-check-20261016/`, outside this checkpoint.
