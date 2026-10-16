# Independent scope review

Reviewed 2026-10-14. Verdict: **accepted as a bounded scope recommendation**,
not as an implemented free-boundary solver or a new classification/existence
result. C5 revision 2 and revisions 1 of C1–C4 and C6–C8 are accepted. There
are no unresolved blocking findings.

I inspected the project instructions, run contract, relevant manuscript
theorems, project map/index, code anchors, four local source extracts and
metadata, and validation receipts. I reran `verify_scope.py` by importing it
and calling `run()` in one light Python process, without invoking its output
writer. All 14 zero identities and three negative controls exactly match the
retained result. Independent pressure/enthalpy and boundary-gradient checks
also passed. The receipt is `review_computation_receipt.json`; source PDF
hashes and all five `LOCAL_EVIDENCE.json` hashes matched.

| Claim | Decision | Mathematical/evidence basis and binding limits |
|---|---|---|
| C1 | Accepted | The theorem at `draft/main.tex:218` is an analytic finite-matrix rank result, with fixed ansatz rank, order, branch and exact splitting. The local reconstruction theorem at line 652 also assumes a regular projectable action, equal base/total orbit ranks and regular quotient charts. These support general methodology, not unrestricted symmetry discovery or free-boundary software. |
| C2 | Accepted | With flat fixed bed and no additional forces, the shallow-water momentum flux is `h u tensor u + (g h^2/2) I`, giving precisely `rho=h`, `gamma=2`, `K=g/2`. This identity is dimension-independent; W explicitly supplies its normalized **1D** version. The hierarchy is a reasonable scope choice, not a theorem that SVE and Stefan problems belong to one interchangeable class. |
| C3 | Accepted | Unknown interface geometry, its evolution, and boundary-supported laws must be specified. The local 2D SVE report uses `h>0` and a constructed fixed annulus, and does not solve a wet/dry interface. A physical free-surface height or moving bed represented over a fixed horizontal domain must not be confused with an unknown horizontal wet region. |
| C4 | Accepted | The identity follows from **mass continuity plus** `X_t=u composed with X`: `d_t[(rho composed with X)J]=0`. `rho0` is reference mass density unless the initial map is the identity. `J>0` ensures local invertibility, not arbitrary global injectivity or continuation. Mass normalization sets the reference mass density to one and gives `X_s=1/rho`; general material labels retain `rho0`. The affine example is a concrete counterexample to “vacuum makes every material map singular.” The bed chain rule must retain `u dot grad b`. |
| C5 rev. 2 | Accepted | `problem.py:72–73` rejects a declared dependent-field symbol in the surface. The reviewer also confirmed that an opaque `Phi(t,x,y)` passes that symbol check, so it is not a semantic rejection of every unknown-function expression. This does not provide interface equations or an interface solver. `chart_reduction.py:115,133` enforces projectability and affine fibre reconstruction; line 250 provides the bounded `data-compatible` status. |
| C6 | Accepted | For `k=gamma-1>0`, enthalpy is `H=K(1+k)a^(-2k)(C-D r^2/a^2)/k`. Material acceleration is `(a''/a)(x,y)`, yielding exactly `a''=2K(1+k)D a^(-2k-1)/k`. The level set has nonzero spatial gradient and satisfies `D_t Phi=2a' Phi/a`; `p` tends to zero and `R'=u dot n`. At `k=1,K=g/2`, the scale ODE becomes `a''=2gD/a^3`. These are interior identities and boundary traces for the stated affine family. |
| C7 | Accepted | Determining-matrix rank, pointwise projected orbit rank, and stabilizers of fixed data answer different questions. Exact boundary rows may be stacked only in the same declared candidate space after valid boundary-jet splitting. For example, rotation loses projected rank at the origin without changing its algebra dimension; translation preserves the fluid equation family but fails tangency to a fixed centered circle. The eligibility filter need not consist of subalgebras or ideals. |
| C8 | Accepted as a recorded validation claim | The retained UTF-8 log says **94 passed**; data-flux is `verified`, workflow is `passed`, and parameter controls report PASS. The first audit and one regression record GBK decoding failures. The UTF-8 audit still fails with **218 issues**, while frozen-manifest/carrier checks pass. I inspected these receipts rather than independently rerunning the regression suite. No manuscript/LaTeX work is represented by this review. |

The boundary regularity limit in C6 matters: near the disk edge,
`rho` is proportional to inward distance raised to `1/(gamma-1)`. For
`gamma>2`, its normal derivative is unbounded. Thus the verified traces do
not establish a density field smooth through vacuum. Separately, the
one-sided sound-speed-squared slope is
`-2 K gamma sqrt(C D) a^(-(2 gamma-1)) < 0`; this elementary check is not a
well-posedness theorem. A positive `a` and positive-density interior remain
the explicit chart assumptions.

The four cited identities and substantive anchors match the retained texts:
E, pp. 2–3, equations (1.1), (1.2), (1.8)–(1.9), gives material vacuum
kinematics and initial-label coordinates; W, pp. 3–4, equations (5)–(17),
gives mass coordinates and the normalized gamma-two bridge; S, pp. 3–4,
Definition 2, includes unknown surfaces and their jets, and p. 6 restricts
translation for its desired moving-interface ansatz; A, pp. 8, 10–13,
equations (3.9)–(3.15), (3.23), (3.30)–(3.32), gives **3D** affine prior art
and its isentropic specialization. Their DOI metadata agree with the
identities in `SOURCES.md`. The planar formula is justified by its separate
substitution, not by transferring Sideris's 3D theorem. The Stefan result is
not transferred to hyperbolic fluid equations.

Unjudged: novelty or exhaustive literature coverage; proofs of the cited
well-posedness theorems; journal/preprint equivalence; maximal parameter-wise
Lie classification; any exceptional gamma stratum; general planar shoreline
or full SVE-interface well-posedness; global material-map continuation;
weak/shock solutions; a generic unknown-interface backend; ML benefit;
independent reproduction of all 94 tests; repairs to the 218 audit issues.
These are outside this review's authorized scope.
