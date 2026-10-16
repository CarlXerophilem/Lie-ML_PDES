# Bounded source inspection: free-boundary extensions of LieML

Checked 2026-10-14. Scope: four retained/read papers, citation depth zero; no
citation-chain expansion, novelty search, manuscript edit, or proof audit.
The named local `ref/` corpus was checked first; no directly matching copy of
these four papers was located in its inventory. alphaXiv tools were unavailable
in the tool inventory. Public arXiv API/PDF and Crossref DOI endpoints supplied
the fallback. All four identities are **confirmed**, and all four PDFs are
**readable**. Claims below refer to the specified arXiv versions, not an assumed
identical journal text. PDF licenses were not independently established
(`license=unknown`).

## Verified identities and access

| Key | Verified bibliographic identity | Exact readable version | Status |
|---|---|---|---|
| E | Daniel Coutand and Steve Shkoller, *Well-posedness in smooth function spaces for moving-boundary 1-D compressible Euler equations in physical vacuum*, Communications on Pure and Applied Mathematics **64**(3), 328–366 (2011); online 2010. [DOI:10.1002/cpa.20344](https://doi.org/10.1002/cpa.20344) | [arXiv:0910.3136v1](https://arxiv.org/abs/0910.3136v1), 2009; `source_euler.pdf`, 27 pages | confirmed; text extracted |
| S | Roman Cherniha and Sergii Kovalenko, *Lie symmetry of a class of nonlinear boundary value problems with free boundaries*, Banach Center Publications **93**, 95–104 (2011). [DOI:10.4064/bc93-0-8](https://doi.org/10.4064/bc93-0-8) | [arXiv:1211.6282v1](https://arxiv.org/abs/1211.6282v1), 2012; `source_stefan.pdf`, 10 pages | confirmed; text extracted |
| W | V. A. Dorodnitsyn and E. I. Kaptsov, *Shallow water equations in Lagrangian coordinates: Symmetries, conservation laws and its preservation in difference models*, Communications in Nonlinear Science and Numerical Simulation **89**, 105343 (2020). [DOI:10.1016/j.cnsns.2020.105343](https://doi.org/10.1016/j.cnsns.2020.105343) | [arXiv:1912.13314v1](https://arxiv.org/abs/1912.13314v1), 2019; `source_shallow.pdf`, 28 pages | confirmed; text extracted |
| A | Thomas C. Sideris, *Global Existence and Asymptotic Behavior of Affine Motion of 3D Ideal Fluids Surrounded by Vacuum*, Archive for Rational Mechanics and Analysis **225**(1), 141–176 (2017). [DOI:10.1007/s00205-017-1106-3](https://doi.org/10.1007/s00205-017-1106-3) | [arXiv:1512.03288v5](https://arxiv.org/abs/1512.03288v5); `source_affine.pdf`, 38 pages | confirmed; text extracted |

The S journal date predates its arXiv upload; both records identify the same
title, authors and DOI. This is a date distinction, not an inferred new edition.

## Source statements and exact anchors

Page numbers below are PDF pages (also the printed preprint page numbers).

**E — actual free-boundary Euler data, and material coordinates.** Page 2,
equations (1.1a–f), states momentum and mass balance on the unknown interval
`I(t)`, `p=0` on its boundary, and `V(Gamma(t))=u`. Equation (1.2) uses
`p=C_gamma rho^gamma`, `gamma>1`; the interior density is positive and vanishes
at the boundary. Page 3, Section 1.2 and equations (1.8)–(1.9), fixes the
reference interval using the particle map `eta_t=u composed with eta` and
`rho composed with eta=rho_0/eta_x`. These are **initial particle labels**, with
the initial density retained, rather than the mass coordinate `x_s=1/rho`.
Page 4, Theorem 1.1, and page 26, Theorem 8.1, state short-time results under
specified weighted regularity and physical-vacuum hypotheses; no such theorem
is being transferred to the project or to arbitrary data.

**W — the closest shallow-water representation bridge.** Page 3, equations
(5)–(10), sets the total-depth variable `rho=h+eta`, defines
`ds=rho dx-rho u dt`, and gives `D_s=(1/rho)D_x`. Page 4, equations (14)–(16),
uses `x_t=u`, `x_s=1/rho` to obtain the scalar potential equation. Remark 1 and
equation (17) explicitly connect this one-dimensional shallow-water system to
polytropic gas dynamics with `gamma=2` and normalized pressure `p=rho^2/2`.
The text says: “equation (16) corresponds to one-dimensional gas dynamics of
polytrophic gas with gamma = 2.” This supports a close model-family bridge,
not a theorem about a two-dimensional shoreline or the mobile-bed SVE system.

**S — equation invariance is only one part of BVP invariance.** Pages 3–4,
equations (9)–(14) and Definition 2, distinguish prescribed surfaces `s_a`
from unknown free surfaces `S_b`, stating that the latter “must be found”.
The free-boundary conditions include derivatives of `S_b`; the definition
requires invariance of these boundary relations as well as the PDEs. Page 5,
equations (18)–(22), supplies nonlinear heat equations with interface flux and
velocity conditions. These are **parabolic Stefan-type problems**, outside
the proposed hyperbolic core. Page 6 specifically sets aside pure spatial
translation because its invariant ansatz cannot supply the desired moving
interfaces. This illustrates task-dependent usefulness; it must not be
rewritten as a universal invalidity of translation symmetry. The paper also
omits an initial temperature distribution in its posed class (page 2), so its
BVP statements are not arbitrary-initial-data statements.

**A — named prior art for affine free-boundary checks.** Page 8, equations
(3.9)–(3.15), states three-dimensional ideal-gas Euler, material motion of the
free boundary, zero boundary pressure, and a physical-vacuum condition. Page
10, equation (3.23), gives the affine matrix ODE
`A''=(det A)^(1-gamma) A^(-T)`. Pages 11–12, Theorem 1 and equations
(3.30)–(3.32), reconstruct the velocity, density and internal energy on
`Omega_t=A(t)B`. Page 13's isentropic remark gives
`rho_0(s)=[(gamma-1)(1-s^2)/(2 gamma)]^(1/(gamma-1))` when `p=rho^gamma`.
The theorem is restricted to **3D affine motions with its prescribed radial
profiles**. The controller's planar expanding-disk residual check is a
separate derived example, not a reproduction or extension of this theorem.

## Synthesis for the scope decision

The coherent primary family is smooth shallow-water/polytropic-Euler flow
with explicit vacuum or shoreline kinematics and pressure/depth conditions.
The gamma-two relationship is a useful bridge; higher-dimensional equations
and any bed evolution must still be derived and checked in their own form.
Use S as a methodological comparison for boundary compatibility, not as
evidence that hyperbolic and parabolic free boundaries share one theorem.

A mass chart divides by density and therefore does not remain a regular chart
at a dry/vacuum boundary. In contrast, an initial-label material map retains
`rho_0` and may have a nonzero deformation Jacobian where `rho_0=0`; the
governing equation still degenerates there. This is a **synthesis** from E/W's
displayed transformations, not a boundary regularity theorem. It motivates
separate checks for the interior chart, its limiting boundary description,
the unknown interface law, and fixed initial/boundary data.

No source here establishes maximal symmetry classification for the proposed
family, a general free-boundary existence result for SVE, novel affine
solutions, or an ML advantage.

## Receipts and limits

`source_crossref_*.json` stores the four exact DOI records and retrieval
times. `source_arxiv_*.xml` plus `*_receipt.json` preserves arXiv metadata.
`source_pdf_*_receipt.json` records the final HTTPS URL, retrieval time, PDF
signature check, size and SHA-256. `source_*_inspection.json` records page
count, no encryption, and successful `pdftotext -layout` extraction;
`source_*.txt` retains the extract for anchor inspection. All outputs stay in
this build directory; the reference corpus and manuscript were not modified.

A preliminary Crossref title query for planar shallow-water classification
returned HTTP 429. That optional branch was stopped and replaced by the
affine-Euler seed; it is **unreachable**, not evidence of absent prior art.
Neighboring metadata hits were not read or used, and no citation edges were
followed. Public journal full texts were not separately audited; proof
correctness and version-to-version equivalence remain unverified.
