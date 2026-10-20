# One-dimensional SVE exact-first literature map

## Decision boundary

The next solver must treat three different equations as three different research
objects:

- **E:** the Eulerian three-field Saint-Venant--Exner system for
  \((h,u,B)\), after fixing the sediment-flux closure and its sign/threshold
  branch.
- **P:** the third-order scalar material-coordinate equation printed as Eq. (7)
  in Paliathanasis--Leon--Leach (2026).
- **M:** the project's independently derived scalar equation with the missing
  material advection of the pulled-back Eulerian bed restored.

Only E and P have primary-paper reduction claims in this first pass. No retained
source classifies or solves M. A solution of P is not evidence for M, and a
fixed-bottom shallow-water result is not an SVE result.

Search boundary: local corpus first, then exact DOI metadata and openly readable
publisher, arXiv, and institutional copies. Citation depth was one, six records
were retained from a limit of twelve, and no paid source was used. This is a
bounded nearest-work map, not an exhaustive literature review or novelty proof.
The final local filename/hash snapshot covered 95 PDF paths (78 unique hashes);
one unrelated PDF appeared concurrently during validation. The
active portable inventory has 47 records and 30 canonical PDFs. Three unique
local PDFs were read for this pass; 75/78 local unique PDFs were not content-read
beyond filename/metadata screening. Those 75 are unvisited, not declared
irrelevant.

## Retained evidence

| ID | Paper and exact object | Actual reduction/solution content | Exactness and limits |
|---|---|---|---|
| S01 | Paliathanasis (2022), DOI `10.3390/sym14081679`. E with \(Q=A_g u^m\), \(m\ge1\), porosity factor \(\xi\). | Self-similar \(x/t\) gives one rational first-order ODE plus quadratures; translation-plus-bed-shift gives elementary families; a reparametrized traveling family gives exponentials; cubic \(m=3\) gives coupled first-order systems and a claimed Abel reduction. | Closed-form and implicit families, no series and no source numerical solve. Noninteger powers need a real sign chart. Printed cubic generator weights conflict with the paper's own ansatz; use the corrected generator before reproducing reductions. |
| S02 | Paliathanasis--Leon--Leach (2026), DOI `10.3390/math14030433`. Printed scalar P derived from \(\phi_t=u,\phi_s=1/h\). | Common scaling and cubic scaling give third-order profile equations; derivative/symmetry reductions claim second- and first-order equations, including an Abel-type equation; traveling reductions claim maximal linearization and a quadrature. | The singular power profile and generators survive separate checks, but the project's exact audit refutes displayed Eqs. (24)--(31), (33), and literal (34) as universal formulas. P also omits the material bed-advection term required for M. |
| S03 | Berthon--Cordier--Delestre--Le (2012), DOI `10.1016/j.crma.2012.01.007`. E with Grass or threshold stress law. | Under smooth constant discharge \(q=hu\), stationary \(h,u\), and active transport, \(q_b=\alpha x+\beta\), \(z_b=-\alpha t+z_{b0}(x)\), and \(z_{b0}\) is algebraic in \(u,q\). | A genuine exact restricted benchmark, followed by a relaxation-scheme comparison. It is not Lie classification, arbitrary-data solvability, or an inactive/interface solution. |
| S04 | Fernandez-Nieto et al. (2014), DOI `10.1016/j.compfluid.2013.11.031`. Extended E with moving and static sediment layers. | The flux \(\widetilde q_b=z_m v_b\) explicitly depends on moving-layer thickness and reduces to a classical flux only in quasi-uniform regime. Appendix B gives a restricted algebraic/implicit family under constant discharge, Darcy--Weisbach stress, zero threshold, and constant affine-flux coefficients. | Exact restricted family plus finite-volume experiments. This four-field closure cannot be substituted silently for \(Q=A_g u^m\). |
| S05 | Dorodnitsyn--Kaptsov (2020), DOI `10.1016/j.cnsns.2020.105343`, arXiv `1912.13314`. One-dimensional SWE with prescribed bottom, no Exner equation. | Potential equation \(x_{tt}-x_{ss}/x_s^3-h_x=0\); after the paper's flat-bottom pressure rescaling, traveling reduction \(\psi''(\alpha^2\psi'^3-2)=0\) and dilation reduction \(\psi^2\psi''+12=0\), with \(x=(54st^2)^{1/3}\). | Useful material-coordinate and invariant-scheme comparator only. Its variational action and Noether laws do not transfer to an evolving-bed SVE equation. |
| S06 | Sjoberg (2007), DOI `10.1016/j.amc.2006.06.059`. General double-reduction theorem. | If a verified symmetry is associated with a verified conservation law, the invariant \(q\)-order PDE reduces through \(T^r=k\) to an ODE of order \(q-1\). | Methodological support for exact-first order reduction. It supplies no SVE current or association proof; that check must be done separately for E, P, and M. |

Primary identities, open-access routes, hashes, page counts, and extracted text
are recorded in `sources1d/receipts.json`. The machine-readable source map is
`literature_1d.json`.

## What the two SVE papers actually leave to solve

### E reductions from the 2022 paper

The useful registered cases are not all of the same type.

1. **Algebraic/trivial:** time or space translation produces stationary or
   uniform constants; pure bed translation does not reduce the two independent
   variables.
2. **One scalar first-order ODE:** \(X_3=t\partial_t+x\partial_x\) produces
   Eq. (40), with \(h=(u-\chi)^2/(2g)\) and bed elevation obtained by
   quadrature. This is the cleanest generic-\(m\) exact-first target.
3. **Coupled rational first-order systems:** \(X_3+\alpha X_4\) and the cubic
   mixed generators produce three-state ODE systems with explicit singular
   denominators. They are numerical only after those denominators and physical
   branches are registered.
4. **Reparametrized elementary solution:** the
   \(X_1+\alpha X_2+\beta X_4\) system becomes linear in \(\Sigma\), but the
   physical similarity coordinate still requires integrating
   \(d\sigma=\bar K\,d\Sigma\).
5. **Cubic Abel claim:** the \(m=3\) reduction is potentially important, but the
   printed generator is inconsistent with its ansatz. Re-derive the undivided
   system before accepting Eq. (69) or its reconstructed power branch.

The paper supplies no series solution or ODE numerical campaign. Its discussion
of data gives invariance conditions, not a solved initial-boundary value problem.

### P reductions from the 2026 paper

The source's conceptual chain is sound as a programme: PDE symmetry -> invariant
profile -> derivative reduction -> first-order equation -> reconstruction. The
displayed formulas are not reliable enough to be solver specifications. The
existing exact audit found:

- nonzero counterexamples for displayed Eqs. (24)--(31), (33), and literal
  (34);
- an omitted \(m=1\) generator \(t\partial_\phi\), missing optimal-system
  orbit families, and two bracket-table sign errors;
- corrected reduced vector fields
  \(3\sigma\partial_\sigma+\phi\partial_\phi\) and
  \(3\sigma\partial_\sigma-2\mu\partial_\mu\);
- an exact cubic power profile that is singular in divided normal form and grows
  like \(t^{2/3}\) at fixed \(s>0\), contrary to the printed decay description.

The source also states both that the initial-value problem was examined and that
it was not discussed. No source initial data or numerical ODE solution is given.
Project-created series and numerical trajectories are therefore extensions, not
source reproduction.

### M is a separate unsolved literature target

For an Eulerian bed field pulled back along particle paths, the bed balance is

\[
B_t-\frac{\phi_t}{\phi_s}B_s
+\beta\frac{\phi_t^{m-1}\phi_{ts}}{\phi_s}=0,
\]

not the printed P balance without the advective term. The project has already
derived for the common scaling \(\phi=tF(s/t)\) an exact first integral and a
second-order normal form for both P and M, but this is derived project evidence,
not a literature claim. The literature gap is therefore precise: classify which
P generators/currents survive for M, including exceptional parameter and
singular-denominator strata.

## Exact-first implications

1. Register the undivided profile residual for every E, P, or M reduction before
   solving for a highest derivative. Store every leading coefficient and its
   zero set.
2. Search for a current or first integral next. S06 lowers order only when the
   symmetry-current association identity is proved; a symmetry name is not
   enough.
3. Classify the resulting ODE by actual form: algebraic, separable, linearizable,
   Abel/Riccati, implicit quadrature, or coupled rational system. Do not label a
   printed equation "Abel" after its chain rule has failed.
4. Keep exact singular branches. The cubic power profile lies on a vanishing
   highest-derivative coefficient and must not be discarded by division.
5. Use S03 as an independent E regression target and S04 as a separate
   extended-closure target. Passing either does not validate P or M.
6. Only after exact identities, branch guards, and data compatibility pass should
   local Taylor series or numerical integration be added. No retained source
   proves global continuation, shock admissibility, or arbitrary-IBVP coverage.

## Unvisited and unresolved leads

Screened but not retained in the six-record budget were Chesnokov's rotating
SWE exact solutions (`10.1017/S0956792509990064`), Paliathanasis's rotating SWE
reductions (`10.1515/zna-2019-0063`), Pandey's prescribed-bottom SWE
(`10.1515/ijnsns-2015-0093`), Siviglia--Nobile--Colombini's quasi-conservative
SVE formulation, and Hudson--Sweby's numerical SVE formulation. They are valid
follow-up leads, but none is evidence for the missing M classification.

The highest-value open questions are: corrected registration of every E
reduction; explicit association tests for E/P/M currents; classification of
singular ODE branches; signed and threshold closure strata; moving-layer state
extensions; and invariant initial/boundary data. No exhaustive absence-of-prior-
art claim is made.
