# Independent symbolic review (2026-10-12)

Scope: `core.py`, `models.py`, `symmetries.py`, `algebra.py`,
`reductions.py`, `source_formulas.py`, the associated tests/docs, and the
local Paliathanasis--Leon--Leach v3 PDF (pp. 2, 4--9). This is a fresh
mathematical/code review of the printed scalar PDE, not a numerical or
full-bed-system review. No author-supplied pass flag was used as a proof.

## Verdict

**Symbolic package: accepted with scope qualifications.** I found no
counterexample to the implemented master equation, positive-chart point
classification, bracket/adjoint algebra, or the nine displayed reductions.
The source-paper claims that disagree with these calculations must remain
labelled as corrected/refuted, not silently reproduced as valid results.
**Entire-source specification: qualified, not certified complete.** The
34-row coverage inventory is useful traceability, but its status count does
not prove that every unnumbered mathematical/physical assertion has been
audited; the selected unnumbered claims are tracked separately. Numerical
claims and release integration were outside this review.

## Claim decisions

| Claim | Decision / severity | Independent check and boundary |
|---|---|---|
| Printed scalar master equation (7), with `beta=m*kappa` | **Accepted** | Direct differentiation gives `E=q*r+a*b-g*x/q**2+2*g*c*b/q**3-g*m*kappa*((m-1)*p**(m-2)*b**2/q+p**(m-1)*x/q-p**(m-1)*b*c/q**2)`. This agrees with `core.master()`. It is the printed scalar model, not automatically the physical Eulerian pullback. |
| Source equation (6) as an Eulerian-bed pullback | **Rejected under stated bed interpretation; high** | For `b(t,s)=B(t,phi(t,s))`, `B_T=b_t-(p/q)b_s`. The source omits `-(p/q)b_s`. At `p=q=g=a=1,c=0`, momentum gives `b_s=-1`, so the missing term equals `+1`, not zero. `models.py` correctly preserves both scalar models. An alternative undefined bed variable is not ruled out. |
| Local unrestricted smooth point-algebra dimension | **Accepted on `p,q,g,kappa>0`, `m>=1`; high** | `q` is the coefficient of free `r`, so normal-form elimination is legal. The successive free-jet coefficients force `xi=xi(s)`, `tau=tau(t)`, `eta=A(t)u+B(t)`, then the two `x`-coefficient equations. Their `m=1`, `m=3`, and remaining strata yield dimensions `5,5,4`; direct off-shell identities verify the resulting bases. No polynomial coefficient ansatz or division by `m-1`/`m-3` is needed. This is not a classification at `p=0`/`q=0`, of generalized symmetries, or of the full bed system. |
| Source Proposition 1's four-or-five statement | **Rejected at `m=1`; high** | `X6=t*d_phi` has `pr3(X6)(E_1)=0` but is independent of the source's four vectors. The printed determining system also gives `3*eta1+xi2_s+2*xi1_t=6` for its own `X4`, so it cannot certify the proposition. |
| Brackets, Table 2 adjoints, and connected-adjoint one-dimensional line classification | **Accepted with declared equivalence; medium** | Coordinate brackets give `[X5,X1]=-X1`, `[X5,X2]=+2X2`, refuting two source Table 1 cells. The negative-ad convention reproduces Table 2. Generic pure translations retain an `RP^2` of lines; `X2+X3` is a missing source representative. At `m=3`, the three stated resonant survivors cannot be removed; at `m=1`, `[X1,X6]=X3` changes the algebra. The normal forms cover connected inner adjoints plus nonzero line scaling, not all discrete/full automorphisms. |
| Nine Table 3 reductions and mixed exceptional chart | **Accepted as local pullbacks; high** | I independently substituted explicit nonlinear profiles into the original third-order PDE. For 3.4, 3.5, 3.6, 3.9, and generic mixed, the direct-to-reduced ratios were respectively `t^-2`, `t^-1`, `1`, `1`, and `t^-9/5` (mixed `alpha=1/4`), including numerical checks away from `t=1`. For the `alpha=-1` mixed chart the ratio was `s^-1/3`. Case 3.8 gave `E=alpha*F'''`; 3.7 gave zero. 3.1 has `p=0` outside the positive chart, 3.2 has `q=0` and is undefined, and 3.3 has `Q=1` and no invariant graph. Normal-form `H=rhs` additionally needs nonzero leading coefficient. |
| Exact first integrals and traveling linearization | **Accepted on stated regular charts; medium** | Directly, for 3.4 `E=dI/dz` with the package's `I`. For traveling graphs `E=-alpha*d[B(P)C]/dz`, with `B=alpha**2*P-g/P**2-g*m*kappa*(alpha3-alpha*P)**(m-1)/P`. Thus `Y(P)=Integral(B(P),dP)` yields `Y''=0` only where `alpha!=0`, `P>0`, velocity `>0`, and `B!=0`; zero first-integral constant is a separate affine branch. This validates the corrected local eight-point/free-particle assertion, not the printed expanded equations globally. |
| Source Eqs. (24)--(31), (33)--(34) as printed | **Rejected on explicit positive-chart witnesses; high** | I inspected PDF equation crops, including Eq. (24)'s nested parentheses, Eq. (28), Eq. (30), Eq. (31)'s complex denominator, Eq. (33), and Eq. (34)'s literal `-alpha**2*kappa` term. The exact specialized source witnesses in `source_formulas.py` are faithful. For example, Eq. (24) gives `H=23/250` at `F=2,P=1/2,C=1/10,z=g=1,kappa=1/30,m=3`, but original pullback is `2367/5000`; Eq. (25) gives `H=-88/25` and original pullback `437/25`. Eq. (34)'s literal implicit profile implies `C=10/69,H=60200/328509` at its test point, yet original pullback is `-118420/328509`. Source Eq. (32)'s quadratic is sufficient but not necessary for its printed, non-invariant graph. These are refutations of universal printed formulas, not a claim that no special solutions exist. |
| Source p. 7 reduced-symmetry vector notation after Eqs. (25)--(26) | **Rejected as printed; low** | The PDF prints `3*sigma*d_sigma+phi*d_sigma` and later `3*sigma*d_sigma-2*mu*d_sigma`. Inducing `X4` on `sigma=s*t**2, phi` gives `3*sigma*d_sigma+phi*d_phi`; differentiating `mu=phi_sigma` gives `3*sigma*d_sigma-2*mu*d_mu`. The printed second directions are wrong, though the intended scaling reduction is recoverable. |
| Cubic power profile and physical interpretation | **Qualified; medium** | The cubic profile solves the original PDE precisely on `(4*beta*g-1)*A**3+27*g=0`, but the 3.4 normal-form leading coefficient also vanishes there. At fixed `s>0`, `phi=A*s**(1/3)*t**(2/3)` grows with `t`, contrary to the paper's decay sentence. A singular boundary at `t=0` does not by itself certify a shock or weak-solution jump condition. |

## Verification and residual risk

- Focused package command: `python -B -m pytest -q tests/test_core.py tests/test_models_sources.py tests/test_symmetries.py tests/test_algebra.py tests/test_reductions.py` -> **25 passed** (4.40 s) at final review time. The tests mostly exercise the same SymPy implementation, so this was supplemented by the explicit direct-PDE substitutions and PDF page-image transcription checks above.
- No numerical solver, full release workflow, historical 43-test package, LaTeX build, or rendered manuscript was reviewed here.
- `coverage.py` classifies all numbered equations and selected unnumbered statements; its `inventory_complete` boolean tests status assignment, not substantive proof. A final release should retain `all_printed_claims_reproduced=False` and explicit unresolved/conditional labels where appropriate.
