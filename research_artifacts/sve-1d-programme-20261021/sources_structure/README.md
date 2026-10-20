# Structure-source evidence

This folder records the source passages and metadata that informed ../STRUCTURE_MEASURES.md. Originals remain read-only in the project corpus or at publisher/metadata endpoints; no duplicate PDFs were created.

## Primary SVE papers

1. Paliathanasis, “Lie Symmetry Analysis of the One-Dimensional Saint-Venant-Exner Model,” Symmetry 14(8), 1679 (2022), DOI 10.3390/sym14081679. Local source: ref/main/Lie Symmetry Analysis of the One-Dimensional SVE.pdf. Read the abstract, system equations (1)-(3), classification in section 2, and reductions in section 4. Crossref resolves title, author, issue, publication date 12 August 2022, and article number. It studies the full 1D shallow-water/Exner field system; do not transfer its classification to the scalar Lagrange PDE.

2. Paliathanasis, Leon, Leach, “Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables,” Mathematics 14(3), 433 (2026), DOI 10.3390/math14030433. Local source: ref/main/Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables-mathematics-14-00433-v3.pdf. The first page gives authors, abstract, date, and DOI. Read model/master equation in equations (4)-(7), Proposition 1 in section 2, and X5 reduction subsection 3.5. The abstract states four symmetries for arbitrary m, one more at m=3, and ODE similarity reductions. Proposition 1 explicitly includes X3=partial_phi, a vertical generator with zero base projection. The project's printed scalar benchmark is tied to this source, but its independently corrected advective model is a separate equation.

## Method sources and bounded access

3. Olver, Applications of Lie Groups to Differential Equations, 2nd ed. (1993), Springer GTM 107, DOI 10.1007/978-1-4612-4350-2. Crossref confirms the 1993 Springer record and author/title. Full text was not opened; cite only as standard background for Lie symmetry reduction, not for an SVE-specific step.

4. Prelle and Singer, “Elementary first integrals of differential equations,” Transactions of the American Mathematical Society 279(1) (1983), DOI 10.1090/S0002-9947-1983-0704611-X. AMS/Crossref identity was resolved. Crossref's current page field is incomplete (215); the commonly catalogued range is 215-229, so the JSON flags the metadata discrepancy. Full text/theorem was not retrieved. It is listed as a conditional first-integral-search method lead, not as proof that the SVE profile is elementary or Darboux-integrable.

5. Muriel and Romero, “New methods of reduction for ordinary differential equations,” IMA Journal of Applied Mathematics 66(2), 111-125 (2001), DOI 10.1093/imamat/66.2.111. Crossref confirms the record. Its title makes it a bounded lead for nonclassical lambda-symmetry reduction; publisher text/theorem was not retrieved, so no theorem statement is used. Any such search is a separate symmetry category from the classical point algebra.

## Retrieval and gaps

The local project sources were read directly; local SVE PDFs are under ref/main/. Primary metadata requests were made to Crossref for the two SVE articles, Olver, Prelle-Singer, and Muriel-Romero. Metadata calls for the 2026 DOI query and one Olver query intermittently failed TLS; local PDF/publisher DOI and alternate title-author Crossref lookup were used where available. No alphaXiv search tool was available in this session, and no discovery beyond the six-source cap was attempted. The Olver and method-paper full texts/theorem anchors remain unread; the note limits its assertions accordingly.

The exact SVE derivative identities are from the local active package research_artifacts/sve-progress-20261010/docs/THEORY.md section 4, not from the method papers. The reviewed point-algebra dimensions are from the read-only 20 October classification package's CLASSIFICATION_REVIEW.md and derivations. These project artifacts are explicit claim anchors, not independent published sources.
