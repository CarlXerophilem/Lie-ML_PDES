# Mathematics and symmetries — project export

Export snapshot: 2026-10-06.

Start with [main.pdf](main.pdf), [NEXT.md](NEXT.md), and [AGENT.md](AGENT.md).
Read [EXPORT_STATUS.md](EXPORT_STATUS.md) for coverage limits.

| Path | Contents |
|---|---|
| `main(1).tex` | Revised canonical manuscript: external BibTeX citations and export/reproducibility notes |
| `main.tex` | Stable wrapper for building the canonical manuscript |
| `references.bib` | Named research bibliography, retaining original citation keys |
| `references/` | Supplied PDFs/images, additional public PDFs, bibliography/link inventory and provenance |
| `chats/` | Seven visible project sessions plus this export request in Markdown; explicitly partial excerpts |
| `code/scalar_sve/` | Original four-script cubic scalar SVE package, requirements and demo evidence |
| `code/sve_animation/` | Python/Manim visualization package with solution/verification data |
| `code/sve_liepinn_benchmark/` | Smooth periodic 2+1 SWE/SVE PINN benchmark, 108 archived runs and checkpoints |
| `code/lie_kan_workflow/` | Single-file ML-free analyzer, series-first KAN comparisons and 42 archived checkpoints |
| `code/library_scripts/` | Unchanged loose source scripts from the project folder/recent outputs |
| `code/visualizations/` | Offline canal and PDE HTML visualizations |
| `code/repository/` | Public repository snapshot with its own source corpus, docs and historical guidance |
| `notes/` | Original project reading/review/checklist documents and recent experiment reports |
| `manuscript_history/` | Unchanged earlier LaTeX sources, including supplied main(1).tex before revision |
| `media/` | Recovered SVE animation video |
| `archive/original_packages/` | Unchanged original ZIP releases in addition to expanded code |
| `validation/` | Fresh export-time checks and build evidence, separate from historical experiment results |
| `FILE_MANIFEST.json` | File sizes and SHA-256 hashes for checking the package |

## Build and verify

Install a LaTeX distribution with TikZ, listings and natbib. From this folder:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
python code/export_tools/validate_package.py
```

BibTeX reads both `references.bib` and `references/archived_sources.bib`.
The latter records additional PDFs/HTTP links without invented metadata;
only sources actually cited by the manuscript are printed in its bibliography.
`references/LINKS.md` and the JSON indexes map source records to files/URLs.

Each experiment has its own requirements and README. Preserve those folder
boundaries because files such as `pde_scene.py`, `models.py` and `numerics.py`
have different meanings in different packages. Existing results remain archived;
write new experiments to a new results directory.

The requested complete native chat history could not be recovered through the
available interfaces. Markdown files clearly mark truncated/summary coverage;
they must not be described as complete transcripts. Some newer code/evidence
referenced by the manuscript is also absent from the public repository snapshot.
Those recovery tasks are the first checklist in `NEXT.md`.
