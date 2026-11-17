# Dissertation citation and claim review map

This resolves the navigation comment in `draft/dissertation_wku.tex`. The authoritative inventory for this edition is [`ref/dissertation-sources.json`](../ref/dissertation-sources.json), with every citation occurrence and source status. It is not a completed claim-validation certificate.

| Claim area | Sources to inspect | Required review distinction |
|---|---|---|
| Physical SVE derivation | `fernandez2017`, `exner1925`, `berthon2012` | Depth averaging, sediment closure, energy assumptions, and model-specific applicability |
| Parameter strata and invariant reduction | `olver`, `anderson2000`, `sve2022`, `ap`, `dengreid2024` | Finite ansatz versus maximal algebra; equivalence versus fibre symmetry; graph transversality |
| Conservation and nonlocal extensions | `druzhkov2024`, `noether1918`, `bluman2005` | Existence of currents, variational hypotheses and added potential variables |
| Analytic crossing and tail control | `teschl2012`, `westreich1982`, `theoremartifact` | Saddle/nonresonance hypotheses, chart domain, analytic branch and explicit remainder estimates |
| Numerical and ML comparison | `lagaris`, `sympinn`, `otto`, `wang2020`, `mishra2023`, `trefethen`, `scalarartifact` | Discrete measurements versus continuous error bounds; comparable costs and baselines |
| Related shallow-water models | `chesnokov`, `gungor2026` | Fixed/variable bed and domain assumptions; do not transfer a result between incompatible models |

The frozen bibliography's bibliographic assertions are retained, not independently reverified by this cleanup. Sources marked bibliography-only and Git LFS pointers remain explicit review limitations. Reviewer findings must name the manuscript locator, source locator, assumptions and gap.
