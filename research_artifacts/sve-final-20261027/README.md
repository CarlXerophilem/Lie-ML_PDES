# Strict Lie follow-up and concise dissertation

**Mathematical acceptance: INCOMPLETE.** This package reports reproducible partial results and failures. It does not claim a universal PDE reducer, a complete parameter classification, experimental validation or neural superiority.

- [Failure analysis and academic acceptance](FAILURES.md): every declared input is accounted for, with source-formula discrepancies and remaining gates separated from runtime issues.
- [Shared repairs](FIXES.md): minimal counterexamples, active fixes and mathematical effects.
- [Independent review](REVIEW.md): findings, dispositions and bounded acceptance.
- [Native retry analysis](data/remote-summary.json): recorded CAS command time 4564.4 / 7200 seconds; the generic returned algebra is verified on a restricted chart, exceptional layers remain incomplete.
- [Methods comparison](METHODS.md): verified sources, executed variants and unexecuted algorithmic proposals.
- [Parameter/input coverage](data/coverage.csv) and [machine-readable analysis](data/delivery-analysis.json).
- [Figure provenance](figure-manifest.json): exact input and output hashes; Python plots read frozen numerical data.
- [Evidence carrier](evidence.zip) and [archive verification receipt](archive-receipt.json): original negatives, raw CAS inputs/outputs, source snapshots, revalidated chains and test logs.
- [Five-chapter dissertation source](<../../draft/dissertation_2026 (1).tex>) and [PDF](<../../draft/dissertation_2026 (1).pdf>). The earlier draft is retained in `sources/dissertation-before-compression.tex`.

The scientific chain is equation → arbitrary coefficient functions → determining equations → returned families and branch conditions → algebra → selected subalgebra → characteristics → reduction → independent original-equation reconstruction. No polynomial degree is assumed for the generators. Source subgroup selectors enter only after the CAS solve; known profiles are not supplied to the strict reducer.

## Reproduce the recorded checks

From the repository root with Python 3.12+ and the declared requirements:

```bash
python -B -X utf8 -m symm.LieSymm --check-integrity
python -B -X utf8 scripts/validate_strict_final.py --out build/strict-validation-NEW
python -B -X utf8 scripts/revalidate_strict_receipts.py --out build/strict-revalidated-NEW
python -B -X utf8 scripts/strict_traveling_from_cas.py --source build/strict-revalidated-NEW --out build/strict-selected-NEW
python -B -X utf8 scripts/strict_scalar_source_chains.py --stratum general --source build/strict-revalidated-NEW --out build/strict-selected-NEW
python -B -X utf8 scripts/strict_scalar_source_chains.py --stratum 1 --source build/strict-revalidated-NEW --out build/strict-selected-NEW
python -B -X utf8 scripts/strict_scalar_source_chains.py --stratum 3 --source build/strict-revalidated-NEW --out build/strict-selected-NEW
python -B -X utf8 scripts/analyze_strict_delivery.py --reports build/strict-revalidated-NEW --selected build/strict-selected-NEW
python -B -X utf8 scripts/analyze_strict_remote.py
python -B -X utf8 scripts/plot_final_dissertation.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/thesis-NEW "draft/dissertation_2026 (1).tex"
```

The revalidator explicitly rechecks **recorded** CAS output; it does not launch a fresh CAS solve. Restore the evidence carrier before using its default original-receipt path. The validation driver retains nonzero statuses for inherited historical failures. Read their logs rather than treating the command's exit code as a mathematical verdict.

```bash
python -B -X utf8 scripts/evidence_archive.py verify --archive research_artifacts/sve-final-20261027/evidence.zip
python -B -X utf8 scripts/evidence_archive.py restore --archive research_artifacts/sve-final-20261027/evidence.zip --root .
```

The final PDF has **20 total pages** and five main chapters plus appendix. Active
tests pass 346/346; focused native tests pass 49/49. Integrity, data-flux and
workflow checks pass. The project audit retains the missing external historical
archive issue; the frozen legacy suite retains its one relocated-root failure.

## CAS and remote scope

Official REDUCE CSL revision 7335 is used through LIEPDE, CRACK and APPLYSYM. The three package sources match commit `70642a0c2bac8a5bdb95b66a2ec52ed0c72dcaaf` after SVN keyword normalization; this is not a proven commit for the entire binary build. Package hashes, source hashes and the distribution license are retained in `sources/cas/`.

The native Priestess experiment was configured for serial CAS execution and a cumulative 7200-second CAS-command budget. One original cleanup check failed and the launch controller incorrectly continued; no claim of continuously verified non-overlap is made. The repaired controller refuses that transition. The original baseline retains its 1.8 GB address-space cap and 1024 MB heap; optimized formulations use an 8 GB process cap and 4096 MB heap. Runtime bars therefore are not a controlled measurement of hardware speedup across formulations. A timeout supplies no nonexistence theorem.

The original Windows checkout's existing overview edits are retained when the
reviewed active files are synchronized. The remote research checkout is preserved.
Publication uses an isolated checkout and a checksum-verified Git bundle;
credentials and CAS binaries are excluded. Completed remote outcomes are included
here. GitHub ref verification occurs after committing and is reported at handoff.
