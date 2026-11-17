# Current dissertation references

The bibliography is embedded in `draft/dissertation_wku.tex`, not in the `main.tex` wrapper. It contains **23 entries**. [dissertation-sources.json](dissertation-sources.json) maps every key to citation line numbers, source URLs and available repository resources. The canonical manuscript is unchanged.

| Key | Availability | Repository resource |
|---|---|---|
| `exner1925` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `fernandez2017` | bundled-pdf | [resource](<../ref/dissertation/fernandez-nieto-2017.pdf>) |
| `olver` | git-lfs-pointer | [resource](<../ref/large-pdfs/applications-of-lie-groups-to-differential-equations.pdf>) |
| `anderson2000` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `sve2022` | bundled-pdf | [resource](<../ref/main/Lie Symmetry Analysis of the One-Dimensional SVE.pdf>) |
| `ap` | bundled-pdf | [resource](<../ref/main/Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables-mathematics-14-00433-v3.pdf>) |
| `druzhkov2024` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `chesnokov` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `berthon2012` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `teschl2012` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `lagaris` | bundled-pdf | [resource](<../ref/large-pdfs/lagaris.pdf>) |
| `sympinn` | bundled-pdf | [resource](<../ref/large-pdfs/Lie Point Symmetry and Physics Informed Networks.pdf>) |
| `otto` | bundled-pdf | [resource](<../ref/large-pdfs/otto.pdf>) |
| `wang2020` | bundled-pdf | [resource](<../ref/small-pdfs/wanggradient.pdf>) |
| `mishra2023` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `trefethen` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `gungor2026` | bibliography-only | See source URLs in JSON; PDF not bundled |
| `scalarartifact` | repository-artifact | [resource](<../research_artifacts/sve-progress-20261010>) |
| `theoremartifact` | repository-artifact | [resource](<../research_artifacts/annular-transcritical-theorem-20261101>) |
| `dengreid2024` | bundled-pdf | [resource](<../ref/large-pdfs/approxalg.pdf>) |
| `noether1918` | bundled-pdf | [resource](<../ref/large-pdfs/noether.pdf>) |
| `bluman2005` | bundled-pdf | [resource](<../ref/dissertation/bluman-cheviakov-2005.pdf>) |
| `westreich1982` | bibliography-only | See source URLs in JSON; PDF not bundled |

The two PDFs under `dissertation/` are exact copies of project-supplied resources; title/DOI were checked on their first pages. The annular theorem subtree is recovered unchanged from the commit cited in the manuscript. Its `theorem-evidence.zip` and the Olver book require Git LFS hydration; no claim is made that their large objects are portable in a plain checkout.

`inventory.json` and `pdf-citations.json` are **legacy inventories** associated with earlier manuscripts and citation keys (for example `approxalg`, `noether`, `sveold`, and `wanggradient`). Their corpus is retained for historical evidence and broader research, not counted as the current bibliography. Do not delete an uncited resource merely because it is absent from this edition. The earlier reference guide is preserved in `.old/2026-11-17-review-cleanup/ref/README.md`.

Run `python tools/audit_dissertation_sources.py` from the repository root. Existence and key matching do not establish that a source proves the cited assertion. In particular, assess the precise version and theorem/page locator before accepting analytical arguments.
