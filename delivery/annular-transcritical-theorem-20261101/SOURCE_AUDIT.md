# Source–claim audit for this proof note

Publication note: this is the recorded local theorem-package audit. Its original source PDFs, extracted text and raw alphaXiv page bodies remain local; consult SOURCE_AUDIT.json for versions, hashes and public URLs. Detailed validation paths are available after restoring theorem-evidence.zip.

This audit covers the three works cited in `document/local-continuation.tex`. It does not represent a new audit of every dissertation reference. The source PDFs, existing extracted text, exact versions and copied alphaXiv responses are preserved under `references/`; `SOURCE_AUDIT.json` records SHA-256 bindings. Hashes identify consulted artifacts, not the truth of a mathematical claim.

| Source and exact version | Original locator checked | Supported use | Limits and alphaXiv status |
|---|---|---|---|
| Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, author preliminary version distributed with AMS permission; printed work 2012 | Theorems 9.4–9.5, printed p. 259 / PDF p. 270; Theorem 9.6, printed p. 260 / PDF p. 271 | Stable/unstable manifolds tangent to eigenspaces; local characterization by approaching orbits; smooth parameter dependence | General classical theory, not an SVE theorem. The downloaded author version is not asserted byte-identical to the printed edition. alphaXiv exact-title lookup returned no exact match; original PDF text was reviewed directly |
| Alexander Chesnokov, *Symmetries and exact solutions of the rotating shallow water equations*, arXiv:0808.1490v1 (11 August 2008) | p. 1 Eq. (1.1); pp. 13–14 Eqs. (5.1)–(5.2) and critical-boundary discussion; p. 16 Eqs. (5.6)–(5.7) | Fixed-flat-bottom rotating water model; stationary annular constants; radial hydraulic criticality and the discussed nonsmooth endpoints; existing affine/quadratic vortex class | Does not include an evolving Exner bed or this slope flux. The inspected critical-ring result does not prove every possible flat-bed critical point is nonsmooth. alphaXiv returned original pages explicitly identified as v1, checked against the local exact-v1 PDF |
| Christophe Berthon, Stéphane Cordier, Olivier Delestre, Minh Hoang Le, *An analytical solution of the shallow water system coupled to the Exner equation*, C. R. Math. 350 (2012), 183–186, DOI 10.1016/j.crma.2012.01.007 | p. 183 Eqs. (1)–(3); p. 184 Proposition 2.1 and Eq. (7); p. 185 Eqs. (10)–(12) | Distinct one-dimensional analytical SVE family with steady water and a linearly drifting bed; prevents attributing that broad mechanism to this note | No rotation or the present two-dimensional slope law. alphaXiv exact-title lookup returned no match; original Numdam/Elsevier PDF was reviewed directly |

The local existence proof applies Teschl's classical mechanism to the displayed reduced vector field. Its model-specific content consists of the compatible coupled-bed saddle criterion, exact continuous example, derived quotient and full Cartesian reconstruction. The inspected sources support a distinction from their results. They do **not** establish worldwide priority, exhaustiveness of the literature, or absence of an earlier theorem for this exact closure.

The note distinguishes **radial** Froude criticality from total-speed Froude criticality. In the constructed example they are respectively 1 and 5/4 when squared; Chesnokov discusses both the radial sonic condition and total-speed classification. The note does not transfer a first-order water-only characteristic determinant to the full slope-dependent, mixed-order PDE.

Source URLs:

- Teschl: https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf
- Chesnokov exact version: https://arxiv.org/pdf/0808.1490v1
- Berthon et al.: https://www.numdam.org/articles/10.1016/j.crma.2012.01.007/

No source-access failure or negative search is used as an obstruction or novelty proof. No new external communications or library mutations were performed for this note.
