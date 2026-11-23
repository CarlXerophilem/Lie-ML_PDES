# Source Audit for the 2026 Lagrangian Proposal

Checked 2026-09-12. This is a bounded source review, not an exhaustive
novelty search. No statements here represent Dr. Rana's private views.

## Primary Source and Equation Map

**Confirmed:** A. Paliathanasis, G. Leon, P. G. L. Leach,
*Lie Symmetries and Similarity Solutions for a Shallow-Water Model with
Bed Elevation in Lagrange Variables*, Mathematics 14(3),433 (2026).
[DOI](https://doi.org/10.3390/math14030433).
[Crossref](https://api.crossref.org/works/10.3390/math14030433)
independently confirms title, authors, issue and 26 January 2026 publication.
The supplied filename ending `mathematics-14-00433-v3.pdf` is the primary
full-text copy; its suffix is not treated as an arXiv version number.

| Location in supplied PDF | Proposal use | Verification boundary |
| --- | --- | --- |
| p.2, Eqs.(1)-(4) | Eulerian context and beta=m*A_g*xi convention | Chain-rule conversion checked independently |
| p.2, Eqs.(5)-(7) | Printed pair, third-order master equation | Missing bed transport under the usual pullback; exact counterexample in accompanying code |
| p.4, Proposition 1 | Extra cubic generator X5=t*d_t-2s*d_s | Selected generator and invariant are used; no independent maximal-algebra certification claimed |
| p.6, Table 3; p.7, Section 3.5 | sigma=s*t^2, phi=F(sigma) | Arbitrary-profile substitution into Eq.(7) checked symbolically; working ODE rederived rather than copied from Eq.(25) |
| p.7, Section 3.4 | Power-law exact control and cubic root relation | Direct master-equation substitution confirms the selected positive branch |
| pp.7-9, Sections 3.6/3.9 | Traveling-wave reduction and linearization prior art | Compact reduction independently derived; invertibility requires nonzero linearizing derivative |
| p.8, Section 3.8/Eq.(32) | Bounded source discrepancy | phi=c*t+Phi(s) solves printed Eq.(7) for arbitrary smooth positive-slope Phi, not only quadratic profiles |

The precise coordinate-conversion assumption matters: the audit sets
b(t,s)=B(t,phi(t,s)). If the source intended a different transformed bed
variable, that definition and its reconstruction must be supplied before
asserting equivalence. The local PDF does not specify such a repair.

## Methodological References

| Citation | Current access and identity | Role and limitation |
| --- | --- | --- |
| Olver, *Applications of Lie Groups to Differential Equations*, 2nd ed., 1993; DOI `10.1007/978-1-4612-4350-2` | Crossref identity/year rechecked; publisher edition checked in earlier audit | Classical invariant-solution background, not a newly claimed theorem; no new page-level book verification |
| Nagesh, Sankaranarayanan, Kaur, Sahai, Jha, *Taylor-Model Physics-Informed Neural Networks (PINNs) for Ordinary Differential Equations*, PMLR 288,621-642 (2025) | [Publisher](https://proceedings.mlr.press/v288/nagesh25a.html) citation metadata rechecked | Direct Taylor/neural-remainder prior art; our scalar trial is not asserted to reproduce their full method |
| Raissi, Perdikaris, Karniadakis, JCP 378,686-707 (2019); DOI `10.1016/j.jcp.2018.10.045` | Crossref title/authors/year rechecked; prior audit inspected author exposition, not journal full text | Residual collocation and PINN background, not evidence of speed or accuracy for this ODE |
| Akhound-Sadegh et al., *Lie Point Symmetry and Physics-Informed Networks*, NeurIPS 36,42468-42481 (2023) | [Publisher](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8493c860bec41705f7743d5764301b94-Abstract-Conference.html) title/authors/pages rechecked; primary full text inspected in earlier audit | Symmetry-informed training is prior art; does not establish this proposal's success |
| Shah, Butt, Ahmad, Saeed, *Enhancing PINN Performance Through Lie Symmetry Group*, arXiv:2509.26113 (2025) | [arXiv](https://arxiv.org/abs/2509.26113) metadata rechecked; raw full text accessed through alphaXiv | Section 2.2 transforms collocation points and changes Burgers-PINN loss rather than directly reducing that PDE; a preprint, not labeled peer reviewed |

## Search Boundary and Novelty

One bounded alphaXiv discovery query combined Lie symmetries, PINN,
shallow-water and Lagrange variables. Returned candidates included
arXiv:2509.26113, 2604.08002, 2412.14578, 2605.11001 and 2606.18149.
Only 2509.26113 was read and independently metadata-checked for inclusion;
the others remain unreviewed candidates, not evidence of coverage or
novelty. No negative search result is used to infer absence of prior art.

Known foundations: the master equation, cubic invariant/power-law family,
traveling-wave linearization, Lie reduction, Taylor expansions, Gronwall
estimates and PINN/symmetry-informed learning. Checked local work: direct
reduction, model-equivalence counterexample, regular-branch formulation,
and numerical control/perturbed-profile pilot. Prospective contribution:
a source-audited benchmark and a controlled, quantitative comparison of
Taylor information in hard-invariant profile approximations. Neither a
new general method nor a new symmetry classification is established.

The prior 2022 Eulerian source and spatial-log perturbation construction
are documented in `references.md` and `derivation.md` as historical scope.
They are no longer the primary basis of `draft/proposal.tex`.
