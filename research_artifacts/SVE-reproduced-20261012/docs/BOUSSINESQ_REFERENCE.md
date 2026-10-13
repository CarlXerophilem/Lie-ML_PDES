# Boussinesq chapter: bounded Section 8 reference note

## Verified citation

M. S. Bruzón and M. L. Gandarias, "Symmetry Analysis and Conservation Laws of a Family of Boussinesq Equations," in *Symmetries and Applications of Differential Equations*, A. C. J. Luo and R. K. Gazizov (eds.), Nonlinear Physical Science, Springer Singapore, 2021, pp. 153-171. DOI: `10.1007/978-981-16-4683-6_5`. This is a **book chapter, not a journal article**. The title page of the local PDF (PDF p. 166, printed p. 153) gives the title, authors, editors, year and DOI. Crossref's DOI record independently gives type `book-chapter`, publisher `Springer Singapore`, and pages `153-171`. The chapter occupies PDF pp. 166-184; the next chapter starts at PDF p. 185 (printed p. 173).

Suggested embedded-bibliography key and entry (adapt to local natbib style):

```latex
\bibitem[Bruz\'{o}n and Gandarias(2021)]{bruzon-gandarias-2021}
M. S. Bruz\'{o}n and M. L. Gandarias,
\emph{Symmetry Analysis and Conservation Laws of a Family of Boussinesq Equations},
in A. C. J. Luo and R. K. Gazizov (eds.),
\emph{Symmetries and Applications of Differential Equations},
Nonlinear Physical Science, Springer Singapore (2021), pp. 153--171.
\newblock \doi{10.1007/978-981-16-4683-6_5}.
\newblock URL \url{https://doi.org/10.1007/978-981-16-4683-6_5}.
```

This follows the existing bibliography's `\doi`/`\url` convention. The proposed entry is metadata, not a claim that this exact LaTeX fragment has compiled.

## Source anchors and what they establish

| Source location (printed pages) | What is actually done | Legitimate scalar-SVE analogy |
|---|---|---|
| p. 153, Eq. (1) | Defines a nonlinear **sixth-order Boussinesq** PDE in time `t` and one spatial variable `x`, with a function `f(u)` and coefficients `b_1,b_2,c_0,d`. | State the SVE **printed scalar** current equation in `t,s`; do not import the Boussinesq PDE, its coefficients, physical conclusions or symmetries. |
| p. 157, Eqs. (8)-(10) | Starts with unrestricted point coefficients `xi(x,t,u), tau(x,t,u), eta(x,t,u)`; applies the **sixth** prolongation criterion on the equation manifold; describes solving an overdetermined linear determining system. | Start Section 8 with unrestricted `tau(t,s,phi), xi(t,s,phi), eta(t,s,phi)` and a **third** prolongation of the SVE master residual; explicitly eliminate the regular leading jet and split remaining free jets. |
| pp. 158-159, Tables 1-3 and Eq. (11) | Tabulates its own nonlinearity-dependent point algebras, uses `eta-tau u_t-xi u_x=0` for invariant graphs, lists similarity forms and reduced ODEs. | Give SVE parameter-stratum generators, bracket/adjoint qualification, invariant graph guards, then direct pullbacks for the nine audited cases. Cite Table 2 only as a model for presentation, not as proof of SVE optimality. |
| pp. 158-160, Eqs. (12)-(17) | Integrates a traveling-wave equation, chooses zero integration constants for a subclass, then tries a Jacobi-elliptic profile ansatz. | SVE ODE integrals and Taylor/IVP work must be independently derived. Do not transfer Jacobi ansatz, zero constants or Boussinesq exact solutions. |
| pp. 166-169, Sec. 4, Eqs. (58)-(71) | Separately constructs low-order multipliers and currents, then uses translation-invariant currents to obtain first integrals of its traveling-wave ODE. It explicitly distinguishes PDE-to-ODE symmetry reduction from further ODE-order reduction. | Mention as a *methodological* example of a second gate: only a verified SVE multiplier/current or directly checked profile first integral justifies lower ODE order. Do not say the chapter's multipliers, currents, first integrals or fourth-order ODE hold for SVE. |

Two precise places to cite: after introducing the Lie-point derivation workflow, `\cite[Sec.~2, pp.~157--159]{bruzon-gandarias-2021}`; after explaining that an inherited or directly verified integral is a separate order-reduction result, `\cite[Sec.~4, pp.~166--169]{bruzon-gandarias-2021}`. One citation to the first span may suffice if Sec. 4 is not substantively discussed.

## Boundaries and source cautions

- Both the cited Boussinesq example and the scalar SVE example have **two independent variables total**, time plus one space/material coordinate. Here `s` is a one-dimensional material (Lagrangian-coordinate) label and `phi(t,s)` is particle position. It is not a second spatial dimension; this is not a `2+1` SVE system.
- A **Lagrangian coordinate** is a label following material/particles. A **variational Lagrangian** is an action density whose Euler-Lagrange equation yields a PDE. The first does not imply the second, or authorize Noether's theorem. Multiplier conservation laws do not require a variational Lagrangian.
- The chapter's classification is for its Boussinesq family. It cannot certify SVE's `m=1`, generic and `m=3` point algebras, connected-inner-adjoint optimal systems, the nine source reductions, or their regularity. Cite the chapter for exposition/method only and cite the SVE source or independent certificates for SVE-specific facts.
- Source formulas themselves must not be imported unchecked: visually, Eq. (1) has `-(...-b_2 u_{xx}+...)_{xx}`, whose expansion contributes **positive** `b_2 u_{xxxx}`, whereas displayed Eq. (10) has a negative `b_2 u_{xxxx}`. Table 3's generic traveling ODE has a sixth derivative with coefficient `-d lambda^2`, but the twice-integrated Eq. (12) prints `b_1 mu^2 h''''` as its leading fourth-derivative term. These apparent internal discrepancies reinforce independent pullback checking; they are not SVE discrepancy claims.
- The SVE printed scalar equation and advectively corrected scalar model remain separate. The chapter supplies neither a full-bed SVE equivalence nor a variational action, numerical error theorem, global well-posedness result or learned reduction.

## Recommended Section 8 narrative and pseudocode

Pedagogical ordering: model/positive chart -> expanded master equation/normal jet -> point field and graph characteristic -> recursive prolongation -> coefficient splitting with `m` strata -> direct off-shell generator check -> brackets and qualified adjoint orbits -> invariant graph/coordinate and all nine direct original-PDE pullbacks -> separate first-integral identities -> Taylor/Fehlberg initial-value examples and independent numerical checks. Keep each step's status (exact, constructed numerical example, nonregular, unresolved) next to the claim. For a beginner, explain that the Lie algebra compresses families of coordinate changes, whereas an invariant graph is a particular solution compatible with one change.

Suggested prose near the start (edit notation/labels to match surrounding text):

> Bruzón and Gandarias illustrate the classical order of work for a different, sixth-order Boussinesq equation: write a general point field, prolong it to the PDE's order, solve the resulting determining equations, and only then pass from the graph-invariance condition to similarity variables and reduced ODEs [Sec. 2 citation]. We follow that *method*, not their equation or classification. Our scalar Saint--Venant--Exner benchmark has independent variables time `t` and one material coordinate `s`; its printed current equation is third order and is analyzed locally where `phi_t>0` and `phi_s>0`.

Suggested prose before integrals:

> Obtaining an ODE by quotienting the two-variable PDE and lowering that ODE's order are different operations. The Boussinesq chapter makes this separation visible by deriving conservation laws before using their traveling-wave first integrals [Sec. 4 citation]. Here we claim an SVE first integral only where differentiating our stated candidate reproduces the corresponding corrected reduced residual under its declared chart guards. This is not a transfer of the chapter's currents or a Noether assertion.

Suggested *mathematical* pseudocode, not program paths/commands:

```text
Input: printed scalar currents, g>0, kappa>0, m>=1, regular chart p=phi_t>0, q=phi_s>0
E := D_t(A) - D_s(J); expand E and solve for its regular leading jet r=phi_ttt
X := tau(t,s,phi) d_t + xi(t,s,phi) d_s + eta(t,s,phi) d_phi
Q := eta - tau*p - xi*q
Construct pr^(3)X recursively; Omega := pr^(3)X(E) after r=R
Split Omega in all remaining free jets; integrate the full determining system
Branch on m=1, m=3, and m outside {1,3}; verify each basis field off-shell
Compute brackets and connected-inner adjoint actions; state orbit equivalence used
For each audited case: solve Q=0, record graph and chart guards, substitute into original E
For each candidate profile first integral I: verify D_z(I)=multiplier*reduced_E exactly
For constructed IVPs: derive RHS, integrate, cross-check original-PDE residual and series
Output: equations, generators, regularity/status, discrepancies and independent checks
```

This describes the existing `main.py` stages as mathematics. It should not imply automatic discovery of hand-derived optimal-system representatives or supplied first integrals: the current computation map says the split/integration, optimal-system chart arguments and candidate integrals include authored mathematical inputs, while prolongation, pullbacks, brackets, identities and numerical cross-checks are computed.

## Verification record

- Opened local PDF with PyMuPDF/Poppler; inspected title and pp. 157-159 as rendered images, and extracted full relevant text of Sec. 4, pp. 166-169. PDF page index is printed page +13 for this chapter.
- Queried Crossref DOI `10.1007/978-981-16-4683-6_5` on 2026-10-13; returned book-chapter, exact title/authors and pages 153-171.
- Read current README, project map, experiment index, and Section 8; checked the current reproduction computation map. No SVE calculation or classifier run was performed for this note.
