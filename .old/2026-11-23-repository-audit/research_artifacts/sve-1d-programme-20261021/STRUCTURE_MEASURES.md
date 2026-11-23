# 1D SVE structure measures and order-reduction programme

Research boundary: this is a source-backed design note, not a new SVE classification or a claim that every profile ODE is solved. It separates the reviewed full first-order system from the printed and advectively corrected scalar Lagrange equations. Retrieval was bounded to six retained sources (depth 1; no citation-graph expansion); the local project corpus and dated evidence were checked first, then Crossref/publisher records. No paid source or heavy CAS was used.

## What each quantity measures

There is no defensible one-number “nonlinearity-symmetry score.” Record a vector of quantities with a stated equation, parameter stratum, category, chart, and purpose:

| Quantity | Definition and use | Does it lower ODE order? |
|---|---|---|
| d_pt = dim(g_pt) | Dimension of the admitted local point algebra of one fixed equation, in a named category and on an open regular chart. An exact dimension requires integrated necessary equations plus sufficiency; a finite ansatz nullity is only its restricted nullity. | No. It counts available generators, including vertical ones. |
| ell_H = rank(xi_a^i) | Rank of the selected subgroup's projection to independent-variable coordinates. On a constant-rank regular chart it removes ell_H independent variables: p becomes p - ell_H. For a two-variable scalar PDE, ell_H = 1 yields a one-variable profile ODE. | It changes independent-variable dimension, not profile order. |
| r_I | Number of functionally independent first integrals certified on the reduced ODE jet space, with independence and pivot conditions recorded. One integral D_z I = 0, with partial I / partial F^(n-1) nonzero, locally solves for F^(n-1) and lowers an n-th order ODE by one. | Yes, one per independent usable integral, locally. |
| s_Lie | Longest verified chain of compatible solvable point-symmetry subalgebras for the particular reduced ODE; record each generator, reduction variable, regularity condition, and reduced equation. This is not the full algebra dimension. | Potentially, one order per successful regular reduction step; a chain is not implied by d_pt >= s. |
| rho_det(lambda) | Rank/nullity stratification of the determining operator for parameter vector lambda, after fixing model, symmetry category, jet order, and any ansatz. Its nullity equals algebra dimension only after unrestricted necessity/integration has been established. | No direct effect. It diagnoses parameter strata where candidates appear or disappear. |
| nu_N, d_Newt | Homogeneity weights, polynomial degree, and Newton-polytope support/degree of a specified cleared-denominator reduced vector field in specified coordinates. Useful to prioritize symbolic first-integral searches. These change under coordinates and denominator clearing; they are not intrinsic nonlinearities. | No. They affect search cost/representation, not ODE order. |
| N, kappa_obs | Perturbation/continuation bookkeeping: N is the highest verified formal correction order; kappa_obs is the first proved regular obstruction order in a declared category. Keep separate from m, the physical sediment-flux exponent, and solver iteration counts. | No, unless the calculation produces a separately verified first integral of the reduced ODE. |

Definitions require local independence. For a set I_1,...,I_r, check the Jacobian rank of their restrictions in the ODE's jet coordinates; merely finding D_z I_j = 0 does not show independence. Similarly, a generator with zero base component has projected rank zero even when it increases d_pt.

## Exponent is a branch parameter, not an order count

For the reviewed first-order transport family (G=0) on h>0, u>0, g>0, K>0 and 1<=m<=4, the unrestricted maximal point-algebra dimension is 4 for m != 3 and 5 for m=3; at K=0, m drops out and the dimension is 5. The slope family includes the declared ranges 1<=m<=4 with n=m-1 or n=m, plus slope_only 0<=n<=4. Because the bed equation contains D_x(u^n B_x), the G>0 slope equations are mixed second order in space, not first-order systems. Their extra generator also requires m=3 for K>0, with the generator depending on whether n=m-1 or n=m. These are facts about the specified equations and fixed-parameter positive charts; they are not a classification of either scalar equation. Read-only anchors: build/sve-general-symm-20261020/CLASSIFICATION_REVIEW.md, FIRST_ORDER_DERIVATION.md, SLOPE_DERIVATION.md.

For the scalar Lagrange equations in the active progress package, the common dilation Xc = t*d_t + s*d_s + phi*d_phi is admitted for every real m on the stated positive chart. It has base orbit rank one, so y=log(t), z=s/t, v=phi/t are local quotient coordinates for t>0, with v=F(z). The different generator X5 = t*d_t - 2s*d_s is the cubic-exponent enhancement in the cited scalar Lagrange paper. Thus m=3 can increase the menu of invariant reductions; it is not needed for the common-scaling PDE-to-ODE reduction below.

A concrete warning from Proposition 1 of that scalar paper is X3 = partial_phi. It contributes to the point-algebra dimension, but its projection to the (t,s) base is zero, so by itself it cannot remove either independent variable. This is an immediate counterexample to using total algebra dimension as an ODE-order or PDE-dimension reduction score.

The parameter delta=m-3 and perturbation iteration index are different data. A first-order obstruction to continuing one generator family near delta=0, or a verified correction through order N, concerns persistence of that symmetry in the specified class. It does not by itself change the order of F's ODE. Record it as symmetry-continuation evidence, not an ODE integral.

## Exact scalar example: two separate reductions

Keep the printed and corrected equations labelled. The active scalar evidence sets P=F', V=F-zP, beta=m*kappa, A=F''*(z^2*P-g/P^2), and J=z*V^(m-1)*F''/P. On t>0, P>0, V>0, direct pullback by phi=t*F(s/t) gives E_m=t^(-2)*R_m, where

    R_print = -A - z*A' + g*beta*J'
    R_corrected = R_print - (V*A/P)'

Each is an exact total derivative:

    R_m = I_m'
    I_print = L_print*F''
    L_print = -z^3*P + g*z/P^2 + g*beta*z*V^(m-1)/P
    I_corrected = L_corrected*F''
    L_corrected = F*(g/P^3-z^2) + g*beta*z*V^(m-1)/P

The original scalar equation is third order in F. The identity I_m'=0 first gives a constant I_m=I0; on a subinterval where the relevant L is nonzero, solve F''=I0/L(z,F,F';m). This is one certified order reduction from the divergence structure, valid for general m under chart and pivot assumptions. It is not caused by having more point generators. If L=0, this pivot argument does not apply; record a separate singular branch instead of dividing.

Concrete contrast:

- PDE-to-ODE: p=2 and ell_<Xc>=1 leave 2-1=1 independent variable z. The profile equation is still third order before using its first integral.
- ODE order: the certified independent integral I_m gives r_I=1, and the nonzero L pivot lowers order 3 to 2. A five-dimensional PDE symmetry algebra alone would not establish this step.
- Parameter control: the same first-integral formula is parameterized by m, but its coefficients depend on m. Compare printed versus corrected L, and test m=1,2,3,4 plus a symbolic generic-m identity. Do not infer that the full physical bed system inherits this scalar integral.

The exact symbolic check root can run without a large classification solve is: define z,F(z),g,beta,m, set P=F', V=F-zP, form A,J,L_print,L_corrected above, and simplify both residuals

    R_print - D_z(L_print*F'')
    R_corrected - D_z(L_corrected*F'')

Both must be identically zero before any numerical solve. This verifies only the derivative identities; it does not verify PDE symmetry, data compatibility, bed reconstruction, or solutions across L=0.

## Candidate search order for exact-first profile solving

| Priority | Test | Exact acceptance condition | Stop/fallback |
|---:|---|---|---|
| 0 | Freeze model and chart | Explicit printed/corrected/full-system label; parameters fixed; t>0, P>0, V>0 (or another stated regular chart); highest-derivative coefficient nonzero. | Separate equations/branches; no shared coefficient cache across models. |
| 1 | Extract conservation/divergence structure before group search | Find D_z I = mu*R with mu nonzero on a chart and verify symbolically against the exact residual. Current scalar cases use mu=1. | Retain original order if the identity or multiplier fails. |
| 2 | Unrestricted point-symmetry reduction of the reduced ODE | Solve determining equations in the stated point category; verify the prolonged identity; establish projected action and valid invariant coordinate. | Do not use PDE algebra dimension as a substitute. |
| 3 | Continue only along an admissible solvable chain | Check closure/solvability and regular action at every step; pull back the equation and all data. | Stop when subgroup is nonsolvable, isotropy/pivot fails, or data are incompatible. |
| 4 | Rational/polynomial first-integral searches | Normalize as a first-order system, state the field/ring and denominator exclusions, then try Darboux-polynomial or Prelle-Singer-style integrating-factor/integral candidates. | No solution from a bounded-degree search is “not found in the ansatz,” not nonintegrability. For noninteger m, V^(m-1) is not polynomial in naive variables. |
| 5 | Generalized/nonclassical candidates | If the classical point route stalls, declare a separate contact, lambda, nonlocal, or nonclassical category and verify its defining differential constraint. | Such a result does not upgrade the classical point classification. No such SVE candidate is certified here. |
| 6 | Numerical and learned fallback | Integrate the exact reduced IVP with independent solver checks; any learned symmetry/integral candidate must pass exact residual and independence checks. | A fitted profile or low residual is not an order-reduction certificate. |

The retained sources support classical reduction theory and identify methods worth checking; only priorities 0-1 have current scalar SVE certificates. Priority 4 is conditional on polynomial/rational normal form and a useful ansatz. Priority 5 is a distinct research extension, not a recommendation to mix categories in one score.

## Source/evidence boundary

Bibliographic identity, local/publisher retrieval outcomes, and exact anchors are in structure_sources.json. Short source notes are in sources_structure/README.md. The SVE formulas above come from the active evidence package research_artifacts/sve-progress-20261010/docs/THEORY.md §4 (read-only); they are not quotations from the cited paper. The maximal full-system dimensions and slope branches come from the independent review and derivations in the 20 October package. Neither package establishes a complete solution theory for arbitrary nonlinear SVE data, equivalence of the printed scalar PDE to the full physical system, or a global/nonlocal symmetry classification.
