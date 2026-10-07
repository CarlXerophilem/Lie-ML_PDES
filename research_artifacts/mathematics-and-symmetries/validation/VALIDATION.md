# Export-time validation

Executed 2026-10-06. These checks verify the recovered deliverable; they do not
reproduce every historical experiment in the current manuscript.

| Check | Result | Evidence |
|---|---|---|
| Revised LaTeX/BibTeX build | Passed; 17-page PDF, resolved citations, no overfull boxes or BibTeX warnings | `latex-main.log`, `bibtex-main.blg`, `../main.pdf` |
| Visual inspection | Export-status page and final bibliography page inspected; text/citations readable | Compiled PDF pages 14 and 17 |
| BibTeX parsing | 42 named research records and 117 archive/link records; no invalid blocks | `../references.bib`, `../references/archived_sources.bib` |
| Python syntax | All 81 recovered/generated Python sources parsed successfully | `code/export_tools/validate_package.py` reruns AST parsing |
| Scalar SVE Lie-only run | Passed exact reduction/anchor checks; relative position error about `1.87e-12`, reconstructed residual RMS about `2.98e-15` | `fresh/scalar_sve/LieReduct_metrics.json` |
| Independent scalar master control | Passed cubic identity, near-cubic unchanged-generator rejection, coefficient-defect and pullback checks; DOP853/Radau differ about `5.1e-12` | `fresh/scalar_master_control.json` |
| Standalone ML-free analyzer self-test | Passed all listed tests; 1D/2D affine candidate nullities 7/8, reconstructed profile checks and negative controls passed | `fresh/analyzer_self_test.json` |
| Original attachments | Archived supplied TeX and Navier--Stokes PDF match their input SHA-256 hashes | Original-source provenance and package manifest |
| Public source PDFs | 18 downloads succeeded; PDF signatures and title pages checked against reference identities | `../references/public-download-status.json` |
| Source/index coverage | 81 archived source PDFs and 108 discovered HTTP links mapped to BibTeX keys | PDF/link JSON indexes; package validator |
| File/ZIP integrity | SHA-256 manifest and ZIP CRC checks run after final assembly | `../FILE_MANIFEST.json` and package validator |

The final LaTeX log has four underfull-line warnings in bibliography formatting;
they do not leave unresolved references or text outside the margins.

## Archived evidence preserved without retraining

- The Eulerian benchmark package reports 108 main neural runs; its original delivery-check JSON and all checkpoint/metric files are retained. It also contains additional controls, so checkpoint-file count need not equal main-run count.
- The Lie/KAN package contains 42 checkpoint files, original replay/solver/analyzer checks, metrics and reports.
- The scalar/animation archives retain their original solution arrays, metrics and verification outputs.
- The public repository regression suite and neural training were not rerun for this export. Source syntax, archive identity and the explicit cheap mathematical checks above were run.

## Unverified or missing

No new verification is claimed for the current draft's missing Duffing/logistic/
fusion/v0.2-family source artifacts, mature differential-completion backends,
the remote services, a maximal symmetry classification, a near-cubic deformed
generator, interval error bounds or physical scalar/full-SVE equivalence.
See `../EXPORT_STATUS.md` and `../NEXT.md` for the recovery queue.

Host/library versions for the fresh checks are recorded in `environment.json`.
Timings belong to this execution environment and are not replacements for
historical performance tables.
