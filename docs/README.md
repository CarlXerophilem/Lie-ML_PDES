> Current dissertation review: [Gemini handoff](gemini-review-handoff.md), [canonical manuscript](../draft/dissertation_wku.tex), [current references](../ref/README.md). The historical project map below is not the current manuscript inventory.

# Documentation index

Start with [project-map.md](project-map.md), the current map of models, evidence and work.

| Purpose | Entry |
|---|---|
| Next writing task: title, outline, evidence map only | [dissertation writing plan](superpowers/plans/2026-10-21-dissertation-writing.md) |
| Portable remote handoff | [Priestess environment, sync and restore](priestess-handoff.md) |
| Current route and precision repair | [three-stage roadmap](research-roadmap-20261021.md), [residual status](residual-resolution-20261021.md), [local demo](../build/sve-P-residual-20261021/campaign-reviewed/index.html) |
| New precision evidence carrier | [401-file follow-up](../research_artifacts/sve-P-residual-20261021/README.md), source baseline 11fe2a8 |
| Current printed-P solutions and publication | [delivery](../build/sve-P-solutions-20261021/DELIVERY.md), [portable results](../research_artifacts/sve-delivery-20261021/README.md) |
| Current 1D research and solver plan | [programme](../research_artifacts/sve-1d-programme-20261021/README.md) |
| Cleanup, archives and restoration | [21 October archive guide](build-archive-20261021.md) |
| Current verification and integration | [refresh report](../research_artifacts/project-refresh-20261021/REPORT.md) |
| Lie reduction concepts | [Lie_reduction.md](Lie_reduction.md), [implementation interface](pde_formalization_and_reduction.md) |
| Detailed older methodology | [map through 19 October](methodology-map-through-20261019.md) |
| Reference reading | [source guide](../ref/README.md), [basic reading notes](basic-reference-reading-notes-20261010.md) |
| Test commands | [validation](validation.md) |
| Older cleanup provenance | [archive.md](archive.md) |
| Equation 27 teaching material | [dated presentation note](2026-10-17-sve-equation27-manim.md) |

Dated proposals, manuscript variants and experiment reports are historical records,
not automatically the current result. The distinct handwritten-manuscript variants
are retained; similarly named files were not deleted as duplicates without byte identity.
The user-edited Lie reduction notes and draft documents remain outside this refresh commit.

The project map links archived historical packages through their ARCHIVED.md
restore stubs. Current reproduction, 2D extension, scalar benchmark, 1D programme
and delivery packages stay expanded. The missing 11 October external archive
remains nonblocking historical provenance, not a current research gate.

Default ripgrep discovery omits bulky references/evidence and snapshot outputs,
not the snapshot's Python implementation. This is search guidance, not a ban on
direct reads or a guarantee about every tool. Use deliberate scoped searches:

```bash
rg --no-ignore --files ref
rg --no-ignore -n --glob '*.md' 'failed|unresolved' research_artifacts/sve-progress-20261010
rg --no-ignore --files research_artifacts/archives-20261021
rg --no-ignore -n 'source_sha256' symm/LieSymm/_snapshot/cases
```
