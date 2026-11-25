# Dissertation and reference audit — 25 November 2026

The 24 November compact dissertation has a substantially traceable mathematical argument, but its references and delivery need corrections before a reader can reproduce all the claims from the advertised paths. The highest-priority findings are an incorrect author list, a bundled book edition that differs from the cited edition, seven broken reference links that also break the scalar replay, and two gaps in the provenance of numerical evidence. The annular interval bounds were recovered and reproduced; the three-run timing medians remain untraced.

This is an audit deliverable. It does not change the manuscript, move reference PDFs, replace historical controls, or resolve the deferred printed-P/material-M comparison. Findings distinguish confirmed errors, missing delivery evidence, and improvements to attribution.

## Snapshot and scope

- Manuscript of record: [dissertation_wku_compact.tex](../../draft/dissertation_wku_compact.tex), 1,206 lines, dated 24 November 2026; [PDF](../../draft/dissertation_wku_compact.pdf), 26 pages.
- Git snapshot: `65985e3fc6098ec54514e83dc2ea16049ce62e98`.
- Source SHA-256: `73a827f199f0bfbe3377439bd89db4a15e3178b249f1399b2dc25c1143ac0d98`.
- Delivered dissertation PDF SHA-256: `c3c91241df88f8ac1addcaab3a52154c8d5d9c1e8c60183b10ef908cbae04a4a`.
- Starting context: [project README](../../README.md), [verification dossier](../VERIFICATION.md), [reference index](../../ref/README.md), [literature audit](../../ref/Literature%20Verification%20and%20Source%20Boundaries.md), and [research history](../research_path.md).
- Read the complete compact manuscript, matched all 21 bibliography entries, checked the principal source passages supporting its claims, inventoried the 23 tracked reference PDFs (20 unique contents), and ran the targeted checks below. Peripheral uncited PDFs were screened for identity and relevance; this is not a page-by-page review of every textbook in the library.
- There are 19 used bibliography keys, two unused entries (`chesnokov`, `oliveri`), and no undefined citation keys. `arora2023` is absent from the reference index and existing literature audit.
- An independent concurrent edit appeared in `delivery/VERIFICATION.md` during the audit. It was inspected and preserved. No commit, merge, or push was made.

The matching inventory is [source_matching.json](source_matching.json); PDF identities, page counts and hashes are in [pdf_inventory.json](pdf_inventory.json). Findings and line numbers below refer to the source snapshot above. Confidence is high for the concrete metadata/path findings and executed checks, and moderate for claims that no additional evidence exists outside the searched project files.

## Findings requiring correction or evidence

### F1. The Arora entry contains an author who is not on the paper

**Priority: high. Confirmed bibliographic error.** Source lines 1117–1120; introductory citation at line 190.

[arXiv:2310.17053v2](https://arxiv.org/abs/2310.17053v2), *Invariant Physics-Informed Neural Networks for Ordinary Differential Equations*, has three authors: **Shivam Arora, Alex Bihlo, and Francis Valiquette**. Patrick Francisquez is not an author. Both the `\bibitem` author label and its rendered author list add this name.

The cited v2 is dated **11 March 2024**; the first submission was 25 October 2023. The current label uses 2023 and the printed entry omits a year. Specify whether the intended reference is the 2023 first submission or the 2024 revision, and make the label and entry consistent. The internal key `arora2023` need not change merely to fix its displayed metadata.

The source learns in differential-invariant coordinates and reconstructs using equivariant moving frames. That is related to, but distinct from, restricting the dissertation's trial solutions to an invariant graph satisfying `Q_X = 0`. “Follows the motivation” is defensible; add a sentence identifying the methodological difference rather than attributing the exact dissertation construction to this paper. Add the source and this boundary to the reference index/audit.

### F2. The bundled Olver book is a different edition from the one cited

**Priority: high. Confirmed source-to-edition mismatch.** Source line 1093.

The bibliography declares the **1993 second edition**, consulted as the **corrected third printing (1998)**, DOI [10.1007/978-1-4612-4350-2](https://doi.org/10.1007/978-1-4612-4350-2). The copyright page of the [bundled PDF](../../ref/main/applications-of-lie-groups-to-differential-equations.pdf), PDF page 5, identifies the **1986 first edition**, DOI [10.1007/978-1-4684-0274-2](https://doi.org/10.1007/978-1-4684-0274-2). This was checked visually as well as in extracted text.

This does not establish which edition the author consulted elsewhere. Either supply/index the declared consulted edition or revise the bibliographic edition and any locators to match the copy actually used. The general prolongation and invariant-reduction attribution remains appropriate.

### F3. Seven reference links are broken, and the advertised scalar replay fails

**Priority: high. Confirmed reproducibility failure.** Reference index lines 7, 9, 11, 12, 21, 22, 25; replay lines 1291–1293.

The [index](../../ref/README.md) calls `ref/` flat, but most PDFs are now under `ref/main/`. Some filenames changed as well. These seven indexed PDF targets do not exist:

| Index key | Actual available file under `ref/main/` |
|---|---|
| `fernandez2017` | `Formal Deduction of the Saint-Venant-Exner Model Including Arbitrarily Sloping Sediment Beds and Associated Energy.pdf` |
| `oliveri` | `Lie Symmetries of Differential Equations - Theory, Applications, and Symbolic Computation.pdf` |
| `sve2022` | `Lie Symmetry Analysis of the One-Dimensional Saint-Venant-Exner Model.pdf` |
| `ap` | `Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables.pdf` |
| `dengreid2024` | `Contributions to the Algorithmic Foundations of Approximate Lie Symmetry Algebras of Differential Equations.pdf` |
| `noether1918` | `noether(Invariant Variation Problems).pdf` |
| `parvin2026` | `A Hyperbolic Moment Based Shallow Water Model for Coupled Bedload–Suspended Load Morphodynamics with Variable Density.pdf` |

The live command `python delivery/reproduce_sve2026.py --order 6 --output ...` fails when hashing its expected flat-path primary PDF, after completing the mathematical calculations. See the [failure receipt](reproduce_sve2026.txt).

A fresh isolated replay copied the unchanged `reproduce_sve2026.py` and `symbolic_sve2026.py` into a temporary layout and put the existing source PDF at the expected `ref/` path. It **passed**, reporting nine sections, eleven displayed-equation audits, 23 Taylor jets and the listed critical branches. See [successful receipt](reproduce_sve2026_isolated.txt) and [full result](reproduce_sve2026_isolated.json). The source PDF hash is `2b853b7ecf58820105384d8931dcd1f989fd0a1cb2ea7553430f4cd55e8cc5f5`.

Restore a canonical flat reference layout in accordance with `AGENTS.md`, reconcile exact names with the index and code, and rerun the live entry. Preserve duplicate/history provenance when reorganizing. This audit leaves the live failure visible rather than silently changing the reference set.

### F4. The regular annular enclosure is cited to a package that does not carry it

**Priority: high for portable verification. Confirmed provenance gap; reproduced bounds.** Source lines 770–772 and bibliography lines 1131–1135.

The 500-cell regular enclosure is cited to `theoremartifact`, whose [delivered package](../annular-transcritical-theorem-20261101/README.md) concerns the local transcritical theorem. Its files do not contain the regular-box interval calculation quoted here. The matching implementation and certificate were instead located in ignored historical build files:

- [regular_box.py](../../build/defence-final-20261101/experiments/src/regular_box.py)
- [validate_annulus.py](../../build/defence-final-20261101/experiments/src/validate_annulus.py)
- [annulus-certificate.json](../../build/defence-final-20261101/experiments/annulus-certificate.json)
- [historical experiment note](../../build/defence-final-20261101/experiments/README.md)

A fresh replay in a separate directory reproduced these lower bounds:

| Quantity | Replayed lower bound | Manuscript claim |
|---|---:|---:|
| H | 1.158142915646593 | H > 1.1581 |
| S | 0.8436801644744709 | S > 0.8436 |
| Delta_c | 0.47723306243382096 | Delta_c > 0.4772 |

The inputs match the printed independent parameter box, `r in [1,21/20]`, `H(1) in [1.199,1.201]`, and `Z(1)=0`. The implementation uses exact `Fraction` arithmetic with outward rounding on a rational grid of spacing `10^-14`, and 500 cells of length `10^-4`. See [replay receipt](annular_replay.txt) and [summary with historical file hashes](annular_historical_summary.json).

Deliver this regular-box source, inputs, proof note and output under `delivery/` and cite it separately. Keep the historical unsplit-tube failure and shortened-interval pass. The current summary preserves the successful bounds but is not a replacement for distributing the executable historical package and its controls.

The regular enclosure has `Delta_c > 0`; it does not certify a radius through the saddle. Its fixed affine diagnostic is also not a high-accuracy learned solver: the original bed residual bound is approximately **6.5433**. Keep that distinction when moving or describing the evidence.

### F5. The exact bed-drift family needs its antecedent cited where it is derived

**Priority: medium. Attribution improvement with a verified formula match.** Source lines 598–616 and benchmark lines 907–909.

[Berthon et al. (2012), Proposition 2.1](https://www.numdam.org/item/10.1016/j.crma.2012.01.007.pdf), printed p.184 / PDF p.2, gives an exact SVE solution with constant water discharge and a bed drifting linearly in time. In the zero-threshold power-law case, take the paper's transport exponent to be `m/2`. Then `u^m` is affine in x, `h=q/u`, and

`B = C - u^2/(2g) - q/u - alpha_paper*t`.

This is the dissertation's zero-physical-speed branch `gamma=0`, with `q=-c` and `alpha_paper=-alpha_thesis`, on the positive-flux chart. The paper is currently cited only in the introductory model motivation.

Add an explicit citation at the identification of the Eulerian bed-drift family and clarify that the dissertation recovers this known family in material coordinates. Distinguish that antecedent from the tilted material reduction and reconstruction arguments. The manuscript already says the first and third benchmark tasks use the same family; retain that statement. This finding does not claim that the manuscript expressly labels the old physical family as new.

### F6. The timing table's three-run medians are not traceable to the delivered logs

**Priority: medium. Missing evidence, not a demonstrated numerical falsehood.** Source lines 944–955, Table 6.3.

The caption reports medians of three single-thread BLAS replays on an AMD EPYC 9V74. The delivered logs contain one result per task:

| Task | Reported median fit seconds | Fit seconds in delivered log |
|---|---:|---:|
| Eulerian drift | 1.916 | 2.433097975 |
| Printed scalar | 1.886 | 2.322281082 |
| Material wave | 1.860 | 1.835130936 |
| Rotating exchange | 1.786 | 2.076131086 |

Sources: [Eulerian log](../logs/ml_sv2022.txt), [scalar/material log](../logs/ml_sve2026.txt), [exchange log](../logs/ml_new_model2026.txt). The field errors in Table 6.2 match these logs at the printed precision. Different elapsed times across runs are expected, but one run cannot establish the claimed median. No matching three-run receipts or aggregation script were found in the current delivery and searched project evidence.

Supply the three original receipts, the relevant environment/machine record, and the aggregation method, or relabel the table to the evidence actually retained. New measurements should be identified as new measurements. Do not infer a matched-accuracy cost advantage from these fixed-configuration timings; the manuscript already leaves that comparison open.

### F7. The Chebyshev bound needs a locator that supports that particular theorem

**Priority: low. Citation precision; the displayed bound is correct.** Source lines 935–942 and bibliography line 1126.

For an analytic profile bounded by `M_rho` on a Bernstein ellipse, the degree-d Chebyshev truncation bound `2 M_rho rho^(-d)/(rho-1)` is standard. The bibliography documents only Chapter 6 of *Spectral Methods in MATLAB*, a passage about differentiation matrices. That is not a precise locator for the truncation theorem.

A direct matching statement is Trefethen's *Approximation Theory and Approximation Practice*, **Theorem 8.2**, visible in the [author's sample](https://people.maths.ox.ac.uk/trefethen/trefethen_sample.pdf). Use bibliographic metadata for the edition actually consulted; the available sample is a draft. Alternatively, give the short coefficient-tail derivation. Retain the distinction already made between a truncation bound and empirical collocation error.

The logarithmic singularity at `t=0`, mapped to `x=-3` from `[1,2]`, gives the stated limiting ellipse parameter `3+2 sqrt(2)`.

### F8. A missing TeX backslash is visible in the saddle proof

**Priority: low. Confirmed rendering defect.** Source line 745; printed p.12 / PDF p.16.

The source contains `a=...<-1,qquad`; it should contain `a=...<-1,\qquad`. Literal italic “qquad” appears in both the delivered PDF and the isolated rebuilt PDF. A clean LaTeX log does not detect this typo. Correct it and render the page after rebuilding.

## Complete bibliography-to-claim matching

“Matched” below describes source identity and the cited passage's scope. It does not mean the external source proves a new theorem of this dissertation. Source line numbers allow each use to be checked in the [manuscript](../../draft/dissertation_wku_compact.tex).

| Key; bibliography line | Uses; source/passage checked | Match and boundary |
|---|---|---|
| `fernandez2017`; 1089 | Lines 190, 338; local primary article, derivation and energy context; DOI 10.1051/m2an/2016018 | Supports physical model motivation. Its slope/energy derivation does not automatically certify every closure in the thesis. Broken indexed PDF path: F3. |
| `olver`; 1092 | Lines 451, 837, 1043; local book, prolongation and reduction foundations | Appropriate foundational source; bundled edition mismatch: F2. |
| `anderson2000`; 1095 | Line 477; *Group Invariant Solutions without Transversality*, abstract/introduction and kinematic reduction setting | Supports the warning that ordinary transverse graph reduction is not the whole theory. The manuscript must retain its own orbit-rank and graph assumptions. |
| `sve2022`; 1098 | Lines 188, 362, 1040; local publisher PDF, model and Eq. (25); DOI 10.3390/sym14081679 | Correct target for the Eulerian audit. The printed depth/velocity cubic scaling weights require the correction described in the thesis. Independent symbolic check passed. F3 applies to access. |
| `ap`; 1101 | Lines 188, 379, 1040; local publisher v3, Eq. (7), Proposition 1 and section 3; DOI 10.3390/math14030433 | Defines printed P. Does not establish compatible M. The m=1 boost and missing adjoint representative are independently checked. Isolated full replay passed; live path fails (F3). |
| `druzhkov2024`; 1104 | Line 659; [Part I, arXiv:2412.02965v1](https://arxiv.org/abs/2412.02965v1), invariant conservation-law reduction | Appropriate context for first integrals under additional hypotheses. The local Part IV PDF is a different work, not the cited source. |
| `chesnokov`; 1107 | No in-text use; [arXiv:0808.1490v1](https://arxiv.org/abs/0808.1490v1), rotating shallow-water model | Bibliographic identity matched. Its flat-bottom three-field system does not include the evolving sediment balance. Add a scoped related-work citation if retained, or remove an unused entry. |
| `berthon2012`; 1111 | Line 190; original four-page article, Proposition 2.1 | Metadata and model motivation match. Exact-family attribution should also appear at lines 598–616 (F5). |
| `teschl2012`; 1114 | Line 869; [author's preliminary book](https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf), ODE stability/contraction; manifold Theorems 9.4–9.6 | Bibliography's manifold locators suit the historical annular note. For the present residual-stability use, add the relevant Chapter 2 existence/dependence/Gronwall passage. Theorem 2.1 is the contraction principle, not a standalone residual-error theorem. |
| `arora2023`; 1117 | Line 190; arXiv v2 metadata and method | Related invariant-coordinate ODE learning; author/version correction and method boundary required (F1). |
| `mishra2023`; 1122 | Line 869; [arXiv:2006.16144v3](https://arxiv.org/abs/2006.16144v3), Theorem 2.6 and assumptions; journal DOI 10.1093/imanum/drab093 | Supports stability-dependent generalization estimates. Requires stability, quadrature/sampling and regularity assumptions; does not turn arbitrary small residuals into unconditional field-error bounds. Thesis qualification is appropriate. |
| `trefethen`; 1125 | Lines 919, 938; official Chapter 6 sample and Chebyshev truncation statement | Suitable spectral-method background. Improve the theorem locator as in F7. |
| `gungor2026`; 1128 | Line 1043; [arXiv:2610.34129v1](https://arxiv.org/abs/2610.34129v1), model Eq. (1.1) | Correct related prescribed-bottom problem. It does not classify the thesis's evolving-bed model. |
| `theoremartifact`; 1131 | Lines 716, 772; project annular proof/replay | Appropriate for the restricted affine search and local theorem history. Does not deliver the regular interval certificate cited at line 772 (F4). |
| `dengreid2024`; 1137 | Line 558; local PDF, abstract/introduction; [arXiv:2410.20608v1](https://arxiv.org/abs/2410.20608v1) | Supports stating algorithmic/search assumptions. Does not establish this project's exact maximality claims. Broken link and duplicate copies noted. |
| `noether1918`; 1143 | Line 659; local Tavel translation, Section 1 | Translation/year metadata distinguishes the 1918 original and 1971 translation. Variational hypotheses are necessary; point symmetry alone is insufficient for a conservation-law claim. Thesis retains this boundary. F3 applies. |
| `westreich1982`; 1149 | Line 757; original *Canadian Mathematical Bulletin* 25(2), pp.230–233; DOI 10.4153/CMB-1982-032-0 | Classical Briot–Bouquet context, with resonant cases prominent in that paper. The thesis supplies its own nonresonant saddle contraction rather than transferring an unmatched theorem. |
| `oliveri`; 1156 | No in-text use; local book front matter, DOI 10.1007/978-3-032-12791-4 | Title/author/year matched. Cite a specific useful passage if retained, or remove an unused entry. Broken indexed path: F3. |
| `tao2026`; 1159 | Line 919; [arXiv:2508.08935v4](https://arxiv.org/abs/2508.08935v4), architecture; journal DOI 10.1016/j.cpc.2026.110237 | Three-author attribution and residual-gating motivation match. The thesis's six-feature cell is a small adaptation. Publisher full-text access was restricted; method checked in the preprint. |
| `parvin2026`; 1162 | Line 781; local [arXiv:2505.22278v2](https://arxiv.org/abs/2505.22278v2), model/abstract | Related coupled bedload/suspended-load model with variable density. It is not the source of the thesis's exact simpler rotating two-reservoir closure. F3 applies. |
| `klausen2026`; 1167 | Line 190; [arXiv:2510.25731v2](https://arxiv.org/abs/2510.25731v2), metadata, abstract and method | Seven authors and revised title match. Linear homogeneous PDEs, solution bricks and superposition limit transfer. The introduction appropriately identifies linear IBVP scope. |

## Other local references and duplicate handling

The following are additional unique tracked PDFs, not exact sources for entries in the compact bibliography. Their presence alone is not a reason to cite them. The full paths and hashes are in [pdf_inventory.json](pdf_inventory.json).

| Local work | Relevance and recommended treatment |
|---|---|
| Druzhkov and Shevyakov, *Invariant Reduction … IV: Symmetries that Rescale Geometric Structures* (2026) | Distinct from cited Part I (2024). May inform later geometric-reduction discussion; index it under its own identity. |
| Nagesh et al., *Taylor-Model PINNs for Ordinary Differential Equations* (PMLR 288, 2025) | Closely related to Taylor prefixes plus learned remainders and parameterized ODE families. A bounded comparison would improve the trace/Taylor/learning discussion; do not imply identical certification. Already indexed under `nagesh`, but absent from the compact bibliography. |
| Li, Bespalov and Li, *Nemytskii Neural Operator* (arXiv:2511.07684v2) | Defense context for nonlinear reduced representations and online residual refinement. Does not supply an executed equal-accuracy comparison for these SVE equations. |
| Wang et al., *Understanding and Mitigating Gradient Pathologies in PINNs* | Defense/training context. Does not prove the error or conditioning behavior of this compact benchmark. |
| Otto et al., *A Unified Framework to Enforce, Discover, and Promote Symmetry in Machine Learning* (JMLR, 2025) | Broader symmetry-learning context; distinguishes learning/enforcement from exact determining equations. Optional related work. |
| Bluman and Cheviakov, *Framework for Potential Systems and Nonlocal Symmetries* (2005) | Relevant if developing potential-variable/nonlocal extensions. The present stated point-symmetry search should remain separate. |
| Bürger et al., *Well-balanced Physics-based Finite Volume Schemes for Saint-Venant–Exner-type Models* (2025) | Useful candidate numerical background for future full-PDE correction and matched-accuracy studies, not evidence for present learned-solver performance. |
| Dzimah et al., *A Unified Benchmark of PINNs and Kolmogorov–Arnold Networks for ODEs and PDEs* (2026) | Comparative benchmark context. Different tasks and protocols do not establish the current four-task result. |
| Zhong et al., *Learning First Integrals via Backward-Generated Data and Guided Reinforcement Learning* (2026) | Discovery methodology; not a proof of the dissertation's exact first-integral identity. |
| Exner, *Über die Wechselwirkung zwischen Wasser und Geschiebe in Flüssen* | Historical model background. Modern equation/closure claims still need the actual modern primary source. |
| Luo and Gazizov, eds., *Symmetries and Applications of Differential Equations* (2021) | Edited volume. Cite a specific chapter/author if used; it is not interchangeable with Olver or Oliveri. |

Three pairs are byte-identical: the long/abbreviated Deng filenames, the ASCII/en-dash Fernández-Nieto filenames, and the root/main Wang copies. Retain one canonical active file per content if reorganizing, record the mapping, and preserve historical material under `.old/` as required. This audit did not delete or rename any source.

## Mathematical scope retained in this audit

| Model or claim | Assumptions and evidence boundary |
|---|---|
| Eulerian E1 | Local smooth point generators on the positive chart `h,u,g,kappa>0`, real `m>=1`; separate m=1 argument and exceptional m=3 stratum. The determining proof and exact identities support this range; finite sampled exponents alone would not. |
| Printed P | The published scalar equation is audited as printed, on `phi_s,phi_t>0`. Its m=1 boost and scalar solutions do not establish physical reconstruction into E1. |
| Compatible M | Reconstruction uses the closed bed one-form, local integrability and `phi_s>0`; approximation in label coordinates needs the stated inverse-map/derivative controls before comparison at common Eulerian positions. |
| Annular E2 symmetries | Six generators are the kernel of a shared, parameter-independent affine search (56 coefficients, rank 50). For maximum clarity, spell out that coefficients are affine in `(t,x,y,h,u,v,B)` across the open positive parameter family. This is not unrestricted planar classification. |
| Annular quotient | `r>0` makes the rotation and time/bed-drift base directions independent, so orbit and base ranks are two. Rotation alone retains `(t,r)`. Reconstruction uses `H>0`, `C1!=0`, `G>0`, `S>0`; the equation must remain undivided at `Delta_c=0`. |
| Annular saddle | A compatible zero of `(Delta_c,N)`, negative Jacobian determinant, nonvertical eigendirections and local nonvanishing desingularized denominator are essential. The manuscript supplies a contraction argument for local analytic germs. Formal coefficient checks alone are not that theorem. |
| Regular annular enclosure | The independent parameter box is a regular region with `Delta_c>0`; it is different from the frozen critical-point relation tying C3 to c. F4 concerns evidence placement. |
| Rotating exchange | The exact swirl fixture uses `V=0`, `W=omega*r`, `D_a=0` and prescribed data. This is a selected family of the time-radius quotient, not a general solution of the rotating PDE. |
| Learned profile comparisons | Five training traces and 24 interior points per trace; evaluation uses four held-out traces and 401 points per trace. Reported field errors are sampled results. Continuous tank defect bounds use their separate contraction and interval assumptions. |
| Open problems | Direct P–M comparison/continuation, exhaustive singular classification, unrestricted planar classification and matched-accuracy correction cost remain deferred. |

The concurrent verification edit usefully makes the annular quotient and chosen learned profile explicit. It does not close the missing regular-box delivery or timing receipts identified above.

## Executed checks and receipts

Python was 3.12.14 and SymPy 1.14.0. Assertions were enabled. These are fresh checks unless described as inspection of a retained log.

| Check | Result | Receipt |
|---|---|---|
| `python delivery/symbolic_sv2022.py` | Passed; 39 exact proof identities and controls | [Eulerian](symbolic_sv2022.txt) |
| `python delivery/symbolic_sve2026.py` | Passed; positive-chart P/M determining results and model-specific identities | [Scalar](symbolic_sve2026.txt) |
| `python delivery/symbolic_new_model2026.py` | Passed; separate annular quotients and exact exchange fixture | [Planar/exchange](symbolic_new_model2026.txt) |
| `python -B delivery/test_sve2026_ansatz_layers.py` | 7 tests passed, including independent prolongation and negative controls | [Ansatz tests](ansatz_tests.txt) |
| `python -B delivery/test_semianalytic_defect.py` | 3 tests passed | [Certificate tests](semianalytic_tests.txt) |
| `python -B delivery/audit-20261125/check_formulas.py` | 13 checks passed: 12 exact zero identities and one rational-majorant check | [Source](check_formulas.py), [results](formula_checks.json) |
| Live full scalar replay at order 6 | Failed only at the missing expected PDF path | [Failure](reproduce_sve2026.txt) |
| Full scalar replay in copied canonical layout | Passed; 23 jets, 9 sections, 11 displayed-equation audits | [Success](reproduce_sve2026_isolated.txt), [JSON](reproduce_sve2026_isolated.json) |
| `python -B delivery/semianalytic_defect.py` | Certified trace and positivity; fit bounds match Table 6.1 | [Fit](defect_fit.json) |
| `python -B delivery/semianalytic_defect.py --method taylor` | Independent Taylor-control bounds match Table 6.1 | [Taylor](defect_taylor.json) |
| Historical regular annular source replayed in a fresh directory | Passed; same 500-cell enclosure | [Receipt](annular_replay.txt), [summary](annular_historical_summary.json) |
| Table 6.2 vs delivered ML logs | Printed field errors match; neural optimization was not rerun in this audit | Linked original logs in F6 |

The extra formula checks directly substitute the tilted and common-scaling material graphs at m=2, check the characteristic determinant identity, verify all three balances of the explicit cubic Eulerian wave, differentiate the annular critical field/Jacobian, and bound the regular-series complex polydisk with rational majorants, obtaining radius `1/64`. The m=2 spot checks are not a new all-m classification or a formal proof assistant verification.

Table 6.1's key values reproduced as follows:

| Quantity | Fitted trial | Independent Taylor trial |
|---|---:|---:|
| Weighted continuous error bound | 3.5842275993109506e-8 | 0.0027771582665381492 |
| Continuous residual bound | 1.8963549744049723e-7 | 0.00760858154296875 |
| Sampled error | 2.2486970791495757e-10 | 0.0005308236733918371 |

These computations corroborate the listed identities and particular certificates. They do not by themselves prove completeness of a symmetry classification, all claims in the dissertation, or uniform accuracy of the historical neural comparisons.

## PDF and visual checks

The prescribed [build_pdfs.sh](../build_pdfs.sh) was run on a copied source layout under `build/dissertation-audit-20261125/build-root/`, using the available local TinyTeX toolchain. Both vector workflows built. The compact dissertation completed all three passes and produced a 26-page PDF; its final log had no undefined-reference/citation or overfull/underfull-box diagnostics. See [build receipt](pdf_build.txt) and [dissertation diagnostics](dissertation_wku_compact_build_diagnostics.txt).

The combined script then failed while building the defense because `appendixnumberbeamer.sty` was unavailable. See [defense diagnostics](defense_wku_madrid_build_diagnostics.txt). This is an environment/dependency limitation; a successful rebuild of both active PDFs is not claimed. The live PDFs were preserved.

Rendered and visually inspected the delivered saddle-proof page, delivered bibliography page, bundled Olver copyright page, and rebuilt saddle-proof page. The missing-backslash defect in F8 survives a warning-free build.

## Targeted evaluation and next edits

Using the scholar-evaluation rubric for the two requested axes: **citation accuracy/support: 3/5**, and **reproducibility/traceability: 3/5**. These are targeted editorial ratings, not an overall mathematical grade. Primary-source coverage and explicit model boundaries are strengths; metadata mistakes and evidence-location gaps prevent a publication-ready rating.

1. Correct the Arora author/version metadata; reconcile the Olver edition and consulted copy.
2. Restore the flat canonical reference paths and rerun the scalar entry against the same hashed publisher PDF.
3. Deliver and separately cite the regular annular certificate, preserving its historical failed controls and coarse affine diagnostic.
4. Add the Berthon antecedent at the zero-speed family; distinguish invariant-PINN methods; improve the Chebyshev and Teschl locators. Consider the directly relevant Taylor-model comparison.
5. Recover the timing receipts or replace the caption/table with accurately labeled retained evidence. Keep sampled and continuous-error claims separate.
6. Fix the visible TeX typo, rebuild through the prescribed script with the missing Beamer dependency available, and render the affected pages.
