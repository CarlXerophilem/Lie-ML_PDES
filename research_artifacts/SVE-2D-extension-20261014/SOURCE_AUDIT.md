# Source audit for the two-horizontal-dimensional SVE extension

Checked on 2026-10-14 (Asia/Tokyo; retrievals began 2026-10-13 UTC).
Status: **model provenance confirmed, with the qualifications below**.
This is a bounded equation-and-scope check of two papers, not a novelty search,
proof audit, or well-posedness classification. The manifest is
`sources/source_manifest.json`; downloaded originals, metadata, extracted text,
and page images are retained in `sources/`.

## Verified sources and anchors

| Paper | Identity and readable version | Evidence used |
|---|---|---|
| E. D. Fernández-Nieto, T. Morales de Luna, G. Narbona-Reina and J. D. Zabsonré, *Formal deduction of the Saint-Venant–Exner model including arbitrarily sloping sediment beds and associated energy* | **ESAIM: M2AN 51(1) (2017), 115–145**, DOI [10.1051/m2an/2016018](https://doi.org/10.1051/m2an/2016018). Journal PDF from [Numdam](https://www.numdam.org/item/10.1051/m2an/2016018.pdf), 31 pages. | Journal p.116 / PDF p.2: equation (1.1), immediately following variable definitions, unnumbered Grass paragraph, equation (1.2) and porosity definition. Journal p.117 / PDF p.3: limitations of classic transport laws and slope-corrected example (1.7). |
| V. Chavarrías, R. Schielen, W. Ottevanger and A. Blom, *Ill posedness in modelling two-dimensional morphodynamic problems: effects of bed slope and secondary flow* | **Journal of Fluid Mechanics 868 (2019), 461–500**, DOI [10.1017/jfm.2019.166](https://doi.org/10.1017/jfm.2019.166). Publisher PDF, 40 pages; matches the uploaded Cambridge link. | pp.463–464 / PDF pp.3–4: (2.1)–(2.5), shallow-water equations and Chézy friction. pp.466–468 / PDF pp.6–8: (2.11), (2.16)–(2.25), pore-inclusive flux convention, active layer, transport direction and reference state. p.491 / PDF p.31: Appendix D, its low-Froude quasi-steady assumption and (D1)–(D7). |

Crossref, Numdam and the actual Fernández-Nieto title page agree on the journal
identity. Crossref records online publication on 2016-11-28; the issue and
printed title page are dated **2017**. These dates are distinct, not a conflict.
The separately retained arXiv:1506.05642v1 is a **2015, 44-page preprint**.
Its equation labels differ from the 31-page journal version. All model anchors
below refer to the journal PDF, not silently to the preprint.

## Source statements: classical two-dimensional model and Grass flux

Fernández-Nieto et al., equation (1.1), print the following vector system:

\[
\begin{aligned}
 \partial_t h_1+\operatorname{div}_x q_1&=0,\\
 \partial_t q_1+\operatorname{div}_x(q_1\otimes q_1/h_1)
 +\nabla_x(gh_1^2/2)+gh_1\nabla_x(h_2+b_0)+\tau/\rho_1&=0,\\
 \partial_t h_2+\operatorname{div}_x q_b^{\mathrm{src}}&=0.
\end{aligned}
\]

Here `b_0` denotes the source's fixed bedrock `b`, renamed only to avoid
confusing it with the evolving bed elevation in the project. The source
explicitly defines two horizontal coordinates, `x=(x_1,x_2)`, water discharge
`q_1=h_1 u_1`, a two-component horizontal velocity `u_1`, sediment thickness
`h_2`, and bed surface `eta=b_0+h_2`. Thus its vector momentum equation is two
scalar equations; the system contains four scalar PDEs.

The unnumbered paragraph on that same page gives the isotropic Grass closure

\[
 q_b^{\mathrm{src}}=A_g|u_1|^{m_g-1}u_1,
 \qquad 1\le m_g\le4.
\]

This is the speed of the whole horizontal velocity vector, not separate powers
of the two velocity components. The source describes this closure as sediment
moving in the fluid direction without an incipient-motion threshold. Its
equation (1.2) includes a factor `1/(1-varphi)` and explicitly identifies
`varphi` as averaged porosity. Chavarrías et al., equation (2.16) and the
paragraph continuing on p.467, independently make the convention explicit:
their Exner fluxes include pores and porosity is assumed constant.

## Derived mapping to the frozen project model

This subsection is an elementary change of notation and modeling
specialization, rather than a theorem claimed by either source. Set

\[
 h=h_1,\qquad U=(u,v)=u_1,\qquad B=b_0+h_2,\qquad \tau=0.
\]

Let `q_s` denote solid-volume transport excluding pore volume. With constant
porosity `0<=p<1`, define

\[
 q_b^{\mathrm{src}}=\frac{q_s}{1-p},\qquad
 q_s=\kappa |U|^{m-1}U,\qquad
 m=m_g,\qquad A_g=\frac{\kappa}{1-p}.
\]

Because `b_0` is time independent, `B_t=(h_2)_t`. The source's Exner equation
therefore becomes `(1-p) B_t+div(q_s)=0`. The resulting model is precisely

\[
\begin{aligned}
 h_t+(hu)_x+(hv)_y&=0,\\
 (hu)_t+(hu^2+gh^2/2)_x+(huv)_y&=-ghB_x,\\
 (hv)_t+(huv)_x+(hv^2+gh^2/2)_y&=-ghB_y,\\
 (1-p)B_t+\kappa\nabla\!\cdot\bigl(|U|^{m-1}U\bigr)&=0.
\end{aligned}
\]

Do not set `A_g=kappa` while also retaining the `(1-p)` in this Exner equation:
that counts the convention differently. Equivalently, if Exner is written as
`B_t+K div(|U|^(m-1)U)=0`, then `K=kappa/(1-p)`.

The source-grounded label has the following limits:

- The Grass paragraph states `1<=m<=4`; arbitrary real `m` on the open chart
  `|U|>0` is a **project mathematical extension**, not a range asserted by this
  source. The cubic case lies inside the stated source range. Its smooth
  polynomial extension to `U=0` is an elementary separate observation.
- `h>0`, constant `g>0`, `kappa>0`, and constant `0<=p<1` are the project's
  declared model/regularity assumptions. The coefficient `1/(1-p)` requires
  `p!=1`; rewriting conservative momentum as velocity equations requires
  `h!=0`.
- Setting the momentum stress to zero while retaining phenomenological Grass
  transport is the chosen **frictionless mathematical idealization**. This
  audit does not identify it with the paper's later asymptotically deduced,
  energy-consistent two-layer models.
- The water momentum bed force `-gh grad(B)` remains present. Omitting a
  sediment-transport slope correction is a different choice. The source's
  p.117 discusses nearly horizontal-bed limitations of classical closures and
  modifications for arbitrary slopes. The title's arbitrary-slope/energy
  properties must not be attributed to the simple Grass specialization.
- A fixed or locally chosen bedrock datum can recover `h_2=B-b_0`. Physical
  positivity of the sediment thickness or finite sediment supply is an
  additional condition; an unconstrained elevation field alone does not
  establish it.

## JFM identity, scope and non-transfer of its conclusion

The uploaded paper is correctly identified. Its full model includes Chézy
friction with coefficient `C_f`, optional turbulent diffusion, a secondary-flow
intensity `I`, mixed-size sediment and an active layer, and transport-direction
corrections. On p.467 it names Engelund–Hansen and Ashida–Michiue magnitude
relations; equations (2.20)–(2.23) describe sediment deflection by slope and
secondary flow. Its linearization in section 2.4 uses steady uniform straight
flow on an inclined bed with slope balancing friction.

**The paper is not only about mixed-size sediment.** Section 4.2 and Appendix D
also address a unisize four-unknown shallow-water–Exner model without secondary
flow, momentum diffusion or a bed-slope correction to the transport direction.
It would therefore be inaccurate to dismiss its relevance solely because the
project has no active-layer variables.

However, Appendix D explicitly invokes a low-Froude separation of time scales
(`Fr` approximately at most `0.7`) and replaces the water response by a
quasi-steady one. Equation (D7) assumes transport nonlinearity
`n=(Q/q_b) (partial q_b/partial Q)>1`. The displayed growth-rate formula (D2)
retains the friction coefficient:

\[
 \omega_i=
 \frac{q_b C_f k_{wx}^{2}}{k_{wx}^{2}w_2^2+w_1^2}
 \left(w_3+(n-1)k_{wy}^{4}\right).
\]

These assumptions and this frictional reference calculation have not been
matched to, or proved for, the project's full unsteady `C_f=0` Grass system.
Consequently the audited use of this paper is a **model-dependent warning**;
it supplies neither a transferred ill-posedness theorem nor a well-posedness
guarantee for the frozen project equations. The audit verifies what the source
states and its explicit assumptions; it does not independently certify every
step of its stability proof.

## Retrieval, integrity and visual verification

- Search boundary: two supplied seed papers; maximum permitted five; no
  citation expansion was needed (actual depth 0, allowed depth at most 1).
  Grass (1981), listed by Fernández-Nieto as reference [29], was not retrieved
  or represented as independently checked. Unrelated Crossref search hits
  were not retained as evidence.
- No alphaXiv callable provider appeared in the available tool inventory.
  Public Crossref, OpenAlex, arXiv, Numdam and Cambridge were the fallbacks.
  OpenAlex was used only to locate an open copy, not as equation evidence.
- Each HTTP request used a 45-second timeout. No transient retry was needed.
  The initially attempted ESAIM HTML path returned HTTP 403; it remains a
  recorded access failure, not evidence of absence. Numdam supplied the
  journal version without authentication or an access-control workaround.
- PDFs were downloaded with the alphaXiv skill's `download_open_pdf.py`, which
  checks the PDF signature and emits final URL, UTC retrieval time, byte count
  and SHA-256. `inspect_pdf.py` confirmed all three files, page counts and
  extraction readiness. All are unencrypted.
- `pdftotext -layout` extracted the texts. The arXiv preprint extraction emitted
  an xref-reconstruction warning; the journal extraction and inspected journal
  pages supply the operative model evidence. One diagnostic terminal print
  failed under Windows' GBK console encoding; the already saved HTML was
  unaffected, and subsequent Python reads used UTF-8.
- `pdftoppm` rendered primary pages. The researcher visually compared
  Fernández-Nieto journal PDF pages **2, 3**, and Chavarrías PDF pages
  **4, 6, 7, 8, 31** against the extracted equations and assumptions. The saved
  page-32 image was generated for context but is not counted as a visual check.
  In particular, the Grass exponent, vector magnitude, bedrock/elevation
  distinction, porosity convention, friction factor and quasi-steady qualifier
  were checked on the page images.
- Journal PDF SHA-256: Fernández-Nieto
  `d33ba2ce6faff6979703e334f29bb7a0da7c5ae41ec4c00da7ba501be14c63fc`;
  Chavarrías
  `d90b30921b98b5fecd356ce565ced7e532b53ef734af74346db831fd17bdd1f7`.
- Reuse licenses are version-specific: Chavarrías is **CC BY 4.0**, printed
  on p.461 and corroborated by Crossref. The Fernández-Nieto journal copy
  prints copyright EDP Sciences/SMAI 2016, with **no open reuse license
  verified**. Its arXiv v1 landing page links the arXiv nonexclusive-distribution
  license; this is not a blanket Creative Commons reuse license. Public access
  alone is not treated as permission for unrestricted reuse.

Only this audit and its `sources/` directory were written by the source task.
No manuscript, bibliography, `ref/` corpus, frozen package or Git history was
changed. Project-wide computational and manuscript validation belongs to the
controller's integration step; it was not rerun for this read-only source check.
