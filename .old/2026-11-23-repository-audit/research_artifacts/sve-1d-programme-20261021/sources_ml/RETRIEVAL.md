# ML-source retrieval evidence

Checked 2026-10-21. This is a bounded primary-source pass, citation depth 0, no paid provider, no paywall bypass. The metadata identifiers, versions, read anchors, and scope limits are machine-readable in `../ml_sources.json`.

## Live primary-index and source checks

The arXiv export API was queried by exact identifier; the returned title, version and author metadata were checked against the primary HTML page. The HTML page was retrieved successfully and its section headings were checked. This is a heading/metadata review for these three records, not a full mathematical audit of every section.

| Identifier | Exact arXiv record | Primary text checked | Anchors checked | Access |
|---|---|---|---|---|
| `1509.03580v1` | Brunton, Proctor, Kutz, “Discovering governing equations from data: Sparse identification of nonlinear dynamical systems”; export API `https://export.arxiv.org/api/query?id_list=1509.03580` | `https://arxiv.org/html/1509.03580` | §3 SINDy; §3.2 cross-validation/Pareto selection; §4.2 nonlinear ODE example | HTTP 200; metadata and heading check only |
| `1905.11481v2` | Udrescu, Tegmark, “AI Feynman: a Physics-Inspired Method for Symbolic Regression”; export API `https://export.arxiv.org/api/query?id_list=1905.11481` | `https://arxiv.org/html/1905.11481` | §II methods; §II.5 neural-network tests/transformations; §III results/method comparison | HTTP 200; metadata and heading check only |
| `2311.04293v1` | Akhound-Sadegh et al., “Lie Point Symmetry and Physics Informed Networks”; export API `https://export.arxiv.org/api/query?id_list=2311.04293` | `https://arxiv.org/html/2311.04293` | §3.2 symmetry criterion; §4 heat/Burgers experiments; conclusion/limitations | HTTP 200; metadata and heading check only |

The API date observed in the response was `2026-10-20T16:43Z`; requests were made during this 2026-10-21 task. The HTML endpoint was checked separately and returned HTTP 200. No source bytes were copied into the active evidence package; URLs and access scope are preserved here.

## Prior project-local reads carried forward

The following are read-only inputs from `build/sve-autonomous-20261019/sources/` and the experiment package, not freshly upgraded evidence:

- Paliathanasis et al. SVE source: visually reviewed local primary PDF, pp.2 and 7; complete path, hash, model scope in `ml_sources.json` ML01.
- Olver 1986 first edition: read from local Git LFS object; theorem anchors in ML02.
- SciPy 1.17.1 `solve_ivp`: installed docstring; versioned web URL returned 404, which remains explicit in ML03.
- Krishnapriyan et al. PINN failure analysis: full arXiv HTML and NeurIPS metadata; PDF retrieval timed out. Only HTML section anchors are claimed in ML04.
- PINNacle: full arXiv HTML; PDF retrieval timed out. The read version is arXiv v2, not the later proceedings version; anchors in ML05.
- De Ryck et al. tanh approximation theory and Rackauckas et al. UDE: local primary PDFs and anchors in ML06-ML07.

## Synthesis boundary

SINDy and AI Feynman inform possible structure-proposal baselines; they do not certify a Lie generator, first integral, or order drop. SymPINN informs symmetry-aware neural formulations; it does not establish exact classification or an SVE-ODE cost advantage. PINN failure/benchmark literature informs experimental design only. All accepted mathematical identities in this programme still require exact symbolic verification or a separately stated validated numerical certificate.
