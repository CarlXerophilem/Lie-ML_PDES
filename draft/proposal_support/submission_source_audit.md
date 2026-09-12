# Submission Source and Feasibility Audit

Verified 2026-09-12. Scope: the central claims actually used in `draft.tex`
and `proposal.tex`, not mathematical certification of every statement in
every cited work. Metadata confirmation and proof validation are different.
No exhaustive novelty claim is made. The authors' personal intentions or
Dr. Rana's private views are not inferred.

## Primary File Integrity

The [publisher PDF](https://mdpi-res.com/d_attachment/mathematics/mathematics-14-00433/article_deploy/mathematics-14-00433-v3.pdf)
returned HTTP 200 and 290300 bytes. Its 11-page contents are byte-identical
to the user-supplied `ref/main/...mathematics-14-00433-v3.pdf`:
SHA-256 `2b853b7ecf58820105384d8931dcd1f989fd0a1cb2ea7553430f4cd55e8cc5f5`.
Crossref confirms Paliathanasis, Leon, Leach; Mathematics 14(3),433;
publication 26 January 2026; DOI `10.3390/math14030433`.

| Source statement used | Printed location | Independent disposition |
| --- | --- | --- |
| Power-law coefficient beta=m*A_g*xi and master Eq.(7) | p.2,Eqs.(1)-(7) | Transcribed with matching coefficient convention; printed-model scope explicit |
| Cubic generator X5 | p.4,Proposition1 | Scaling-weight calculation verifies selected invariance, not algebra completeness |
| sigma=s*t^2, phi=F(sigma) | p.6,Table3;p.7,Sec.3.5 | Characteristics and arbitrary-profile substitution verified |
| Cubic root (4 beta g-1)K^3+27g=0 | p.7,Sec.3.4 | Exact residual check; positivity and a=2K*sigma^(7/3) proved |
| Traveling-wave linearization | pp.7-9,Secs.3.6,3.9 | Compact direct reduction verified independently; invertibility explicitly restricted |
| Printed bed equation as usual Eulerian pullback | p.2,Eq.(6) | Conflict: chain rule requires a transport term; exact negative test retained |
| Quadratic-only restriction on phi=c*t+Phi(s) | p.8,Sec.3.8,Eq.(32) | Conflict: arbitrary smooth positive-slope Phi has zero printed master residual |
| Maximal classification / complete optimal system | Prop.1 and Sec.2.2 | Not independently certified and not adopted as a new or necessary result |

The source's final p.9 paragraph says the IVP was not discussed; a nearby
sentence contradicts this. We do not use either sentence as evidence of
physical validation. Expanded Eqs.(25)-(34) are not blindly transcribed;
the working reduced equations are derived from Eq.(7).

## Methodological Claims

| Reference and authoritative link | Content supporting the manuscript | Limits |
| --- | --- | --- |
| Olver (1993), [DOI](https://doi.org/10.1007/978-1-4612-4350-2) | Classical Lie reduction background; identity/year confirmed by Crossref | No fresh page-level book access; all specific project propositions have local proofs rather than invented book theorem numbers |
| Nagesh et al. (2025), [PMLR](https://proceedings.mlr.press/v288/nagesh25a.html), [PDF](https://raw.githubusercontent.com/mlresearch/v288/main/assets/nagesh25a/nagesh25a.pdf) | PDF pp.5-7,Sec.3.1,Eq.(2),Theorems4-6: Taylor plus scaled neural remainder, remainder dynamics, conditional analysis | Direct prior art; their state-system approach avoids higher neural derivatives, whereas our scalar profile differentiates three times. Table1/pp.9-10 shows longer-horizon deterioration and slower epochs. Their bounds do not certify our network automatically |
| Raissi et al. (2019), [DOI](https://doi.org/10.1016/j.jcp.2018.10.045) | PINN residual-collocation background; exact identity/authors/pages rechecked | Journal full text not newly inspected; no speed/accuracy promise attributed to this source |
| Akhound-Sadegh et al. (2023), [publisher](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8493c860bec41705f7743d5764301b94-Abstract-Conference.html), [arXiv](https://arxiv.org/abs/2311.04293) | PDF pp.6-7,Sec.3.2,Eq.(11): symmetry loss; pp.8-10: generator-specific redundancy and benefits, low-data setting and limitations | Not evidence that all symmetry-informed learning has zero gradient or fails; manuscript removes that unsupported universal attribution while archiving the old text |
| Shah et al. (2025), [arXiv](https://arxiv.org/abs/2509.26113) | PDF p.6,Sec.2.2,Eqs.(30)-(33): transformed collocation points, explicitly without directly reducing Burgers | Preprint, not confirmed peer-reviewed; best-of-ten selection is not adopted as our reporting protocol |
| McGreivy and Hakim (2024), [DOI](https://doi.org/10.1038/s42256-024-00897-5), [arXiv](https://arxiv.org/abs/2407.07218) | arXiv v1 p.8,Sec.5: efficient baselines/equal-accuracy comparisons; p.11,Sec.6.1.4: hardware and amortized cost | Does not require exclusively closed-form oracles or prohibit refined numerical reference solutions; supports reporting all runs and separating reference accuracy from practical baseline cost |

Publisher/arXiv metadata and readable alphaXiv primary full text were used
as indicated. The previous bounded discovery query and its unreviewed
candidates are retained in `lagrange_references.md`; they are not claimed
as comprehensive coverage.

## Capability Assessment

Feasible: one known invariant reduction, an analytic control, one perturbed
regular IVP, a classical Taylor construction, CPU neural approximations,
exact algebra checks and a conditional Gronwall/first-exit bound.

Verified locally: the symbolic identities and classical pilot; an exact
rational uniform L=15 box bound; two one-seed 400-step CPU smoke runs.
The last runs reduce profile error but disagree on residual/error ranking.
Web literature alone does not establish this project's capability; the
local artifacts supply the bounded operational evidence.

Not established: novel method, complete classification, physical Eulerian
equivalence, a uniformly certified trained network, a multi-seed outcome,
or superiority to a tuned classical integrator. An eight-week 2027 study
should treat successful uniform neural certification as a stretch target.
