# Bounded Source and Novelty Audit

Historical 2022-based Eulerian scope. The current proposal's primary source
and literature audit are in [lagrange_references.md](lagrange_references.md).

Verified 2026-09-12 against the local supplied papers, publisher/Crossref
metadata, and readable primary/alphaXiv full text as specified below.
This is not a systematic or exhaustive review. A search miss is not proof
of novelty. No claim is attributed to Dr. Rana's private views.

| Source | Identity and access | Evidence used and limitation |
| --- | --- | --- |
| A. Paliathanasis, *Lie Symmetry Analysis of the One-Dimensional Saint-Venant-Exner Model*, Symmetry 14(8),1679 (2022) | [DOI](https://doi.org/10.3390/sym14081679); [Crossref](https://api.crossref.org/works/10.3390/sym14081679); supplied PDF `ref/main/Lie Symmetry Analysis of the One-Dimensional SVE.pdf`, full text inspected | Page 2 specifies the power-law sediment flux; page 4 Proposition 1 separates generic m from m=3; Sections 4.10-4.12 give cubic reductions. The model and cubic family are prior work. Printed coefficients require independent checking; see below. |
| R. Di Salvo, M. Gorgone, F. Oliveri, *A consistent approach to approximate Lie symmetries of differential equations*, Nonlinear Dynamics 91(1),371-386 (2018) | [Publisher](https://link.springer.com/article/10.1007/s11071-017-3875-5); [arXiv](https://arxiv.org/abs/2108.02169); raw full text via alphaXiv | Section 3, Eq.(85), imposes approximate prolonged invariance after expansions; Section 4 constructs approximately invariant solutions. Expanding a solution and canceling residuals alone does not verify an approximate Lie generator. Online publication 2017; journal issue 2018; arXiv posting 2021. Cite the journal year 2018. |
| C. K. Nagesh, S. Sankaranarayanan, R. Kaur, T. Sahai, S. Jha, *Taylor-Model Physics-Informed Neural Networks (PINNs) for Ordinary Differential Equations*, PMLR 288,621-642 (2025) | [Publisher](https://proceedings.mlr.press/v288/nagesh25a.html), metadata and methodological abstract inspected | Uses symbolic higher-order Lie derivatives and Taylor series with a neural remainder; the remainder is itself modeled by an ODE. Direct prior art for the trial-function strategy, not evidence of an SVE-specific logarithmic correction theorem. Publisher gives no DOI. |
| T. Akhound-Sadegh, L. Perreault-Levasseur, J. Brandstetter, M. Welling, S. Ravanbakhsh, *Lie Point Symmetry and Physics-Informed Networks*, NeurIPS 36,42468-42481 (2023) | [Publisher](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8493c860bec41705f7743d5764301b94-Abstract-Conference.html); [arXiv](https://arxiv.org/abs/2311.04293); metadata and raw full text inspected | Introduces a symmetry-informed loss. The conclusion notes that not every symmetry provides a useful training signal and more ordinary-PINN samples can produce similar effects. This is different from our hard baseline reduction and derived correction representation. Publisher title hyphenates Physics-Informed; arXiv title does not. |
| M. Raissi, P. Perdikaris, G. E. Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*, JCP 378,686-707 (2019) | [DOI](https://doi.org/10.1016/j.jcp.2018.10.045); Crossref metadata confirmed; journal full text inaccessible; [author exposition](https://maziarraissi.github.io/PINNs/) inspected | Author exposition supports residual collocation with initial/boundary data. Do not claim the journal full text was inspected in this pass. |
| P. J. Olver, *Applications of Lie Groups to Differential Equations*, second edition (1993), Springer | [Publisher](https://link.springer.com/book/10.1007/978-1-4612-4350-2), edition and contents inspected | Classical background for point symmetries and group-invariant solutions. No specific theorem number or page-level proof is claimed checked from this metadata access. |

## Printed SVE Formulas Versus Direct Substitution

The source defines zeta=m*xi*A_g; our kappa=xi*A_g, so zeta=3*kappa
in the cubic case. The PDF's Eq.(25) prints velocity/depth weights that
disagree with the time powers used in its later reduction. The scaling
weights in the proposal are independently obtained from the governing
equations, rather than copied from that display.

For the t^(-1),t^(-2) cubic control, direct substitution gives

\[
u=\frac{2x}{3t},\qquad
h=\frac{3-4g\zeta}{27g}\frac{x^2}{t^2},\qquad
B=\frac{4\zeta}{27}\frac{x^2}{t^2}.
\]

The h and B coefficients printed in Eq.(78), page 10, are interchanged
relative to these checked balances. Literal substitution of those printed
coefficients gives bed residual
2*x^2*(8*g*zeta-3)/(27*g*t^3), generally nonzero. For g=1,kappa=0.1,
the independently checked coefficients are H=1/(15t^2), C=2/(45t^2).

These are bounded consistency findings about specific formulas. They are
not a comprehensive audit or a claim that the entire paper is invalid.
The proposition and code use the explicitly stated original equations.

## What Can Be Called a Contribution

- Known: the power-law SVE setting, enhanced cubic symmetry, and selected
  cubic solution family. A limited scaling lemma reproduces structure;
  it is not a new maximal Lie classification.
- Known: regular perturbation, linear ODE existence, Taylor remainder
  estimates, symmetry-informed PINNs, and Taylor-plus-neural remainders.
- Constructed and checked locally: six finite logarithmic correction ODEs,
  their regularity/residual formulation, and a two-sided numerical pilot.
- Potential contribution requiring comparison: this particular spatial-log
  first-order continuation of the cubic family, together with a measured
  neural correction study. The correctness proof alone is elementary.
- Not claimed: the first occurrence of logarithms in SVE. The 2022 paper
  already contains logarithmic time dependence (Eq.(52), Section 4.11).

A bounded alphaXiv query about SVE, approximate symmetries, and nearby-cubic
spatial-log corrections returned adjacent numerical/perturbation work, not
a direct match. This does not establish absence. The safe proposal wording
is "investigate this model-specific construction and comparison," not
"introduce the first such method."
