# Two-Dimensional SVE Source and Derivation Audit

Accessed 2026-09-13 (Asia/Tokyo). Scope: Appendix C of `../draft.tex`.
Two-dimensional means two horizontal spatial coordinates plus time, not
the two independent coordinates of the main paper's one-space-dimensional PDE.

## Confirmed Primary Source

M. J. Castro Diaz, E. D. Fernandez-Nieto, A. M. Ferreiro, C. Pares (2009).
*Two-dimensional sediment transport models in shallow water equations.
A second order finite volume approach on unstructured meshes.*
Computer Methods in Applied Mechanics and Engineering 198(33-36), 2520-2538.
DOI: [10.1016/j.cma.2009.03.001](https://doi.org/10.1016/j.cma.2009.03.001).
Accents are retained in the manuscript bibliography using TeX escapes.

- Crossref's DOI record confirms title, four authors, journal, year and pages.
- OpenAlex identifies the University of Seville repository copy.
- [Repository metadata](https://idus.us.es/handle/11441/32144) independently
  confirms the title, authors, year, DOI and PDF location.
- [Repository PDF](https://idus.us.es/bitstreams/e7c3cba9-d8d8-46b9-b779-b7cbb6827e4f/download)
  returned HTTP 200; 2,371,628 bytes; 38 pages;
  SHA-256 `bbbffd375242b36ddcc1d2d435d05b5767ed33bc6359a26fc2dd46ad5a97e366`.
  This is a repository manuscript, not claimed byte-identical to the
  19-page journal version. Locations below refer to the repository copy.

| Adopted content | Verified location | Translation or limitation |
| --- | --- | --- |
| Two horizontal momentum equations and water mass | p.3, Sec.2.1, Eq.(2) | Source fluid discharges q1,q2 become hu,hv; friction set to zero |
| Sediment balance and constant porosity factor | p.3, Sec.2.2, Eq.(4) | xi=1/(1-rho0); flux excludes porosity correction |
| Cubic vector Grass closure | p.4, Eq.(5) | qb=Ag*(u^2+v^2)*(u,v); not componentwise cubes |
| Coupled four-field system and bed sign | p.5, Sec.2.3, Eqs.(7)-(8) | Our upward B=zb-Htilde=-H_source; fixed substrate has zero Eulerian time derivative |
| Nonconservative-system caveat | p.2, introduction | Smooth-coordinate derivation is not a definition of shock solutions |

The arbitrary-exponent vector closure is explicitly described as an additional
modeling choice, not attributed to the source's cubic Eq.(5). The Lagrangian
equations and equivalence proposition are derived in the appendix from the
chain rule, determinant identity and Piola transform. No claim is made that
the cited authors supplied these Lagrangian formulas, classified their
symmetries, or proved the project's approximation theorem.

## Retrieval Limits

Two bounded alphaXiv discovery queries returned mostly one-dimensional or
adjacent models. The readable arXiv:2506.16287v1 supplied related background
and a reference trail but is not cited as a two-dimensional formulation.
Two title-based PDF queries for Castro and coauthors instead resolved to
arXiv:2303.03810v1 by Macca and Russo. These identity mismatches were rejected
as primary evidence; the latter paper's bibliography provided a lead only.
The ScienceDirect request did not yield usable article text before timeout.
Crossref, OpenAlex and the author-institution repository resolved the exact
two-dimensional source. This was a focused check, not an exhaustive review.

## Local Checks and Scope

`test_sve2d.py` has seven symbolic tests: scalar gradient and fixed-point
time transformations, Piola divergence on a non-affine map, Jacobian/water
mass identities, relative bed-flux conservation, conservative/primitive
momentum equivalence, an exact sloping-bed solution with a negative control,
and the cubic one-dimensional limit. The latter retains the same missing-
transport warning already established in the main manuscript.

These checks do not solve a general 2D IVP, prove hyperbolicity, or address
shocks, dry beds, or loss of invertibility. Existing claims C01-C11 and the
eight-week 2027 printed-master-equation research scope are preserved.
