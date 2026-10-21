# 2026 SVE printed P solution implementation plan

Goal: execute the accepted direct-solving programme, keeping P distinct from E and M.
Domain: g,kappa>0, m>=1, phi_s>0, phi_t>0; demonstration m=1,3/2,2,3,4.
Architecture: additive catalog, solving and validation modules in LieSymm.scalar2026; immutable historical backend and evidence.

## Task A — registry and provenance
Replay material-coordinate audit and the separating witness. Import all nine source subsections and every existing connected-adjoint representative family, including symbolic continuous parameters and resonant charts. Expose solution_catalog(), solve_reduction(reduction_id, *, parameters, data=None), verify_solution(result). Keep no-graph, undefined, identity, regular and singular states distinct.

## Task B — exact solvable families
Retain traveling quadratures, zero speed, zero integral, affine roots and inverse-chart failures. Solve m=1 boost families, including arbitrary-profile acceleration and logarithmic time profiles. Verify Q and original P directly.

## Task C — scaling
Separate L F''=I0 into nonzero I0, affine, and L=0 branches. Derive cubic singular parametric quadrature with rho=z^(2/3)F', w=F/z^(1/3), r=log z; keep equilibrium power solution. Derive 3.5 autonomous Sigma,M dynamics without division by dSigma/dr. Check beta*g=1/4,1, original leading-coefficient zeros, and coordinate boundaries. Regular unsolved branches receive exact degree-six recurrence and numerical continuation; singular germs remain separate.

## Task D — mixed and resonant representatives
Derive all cubic mixed and resonant graphs from the existing classification, splitting a+b=0,a-2b=0,a=0 before normalization. Try first integrals, inherited symmetry and quadrature before series and numerics. Retain unresolved equations; finite sampling never proves continuous-family coverage.

## Data and reconstruction
Map initial jets and constants to phi,velocity,gradient. Check compatible data and printed-bed closedness with one additive bed datum. Use DOP853 and classic RKF45 at rtol=1e-10,atol=1e-12; common interval state discrepancy <=1e-7*(1+max(abs(reference))). Direct finite-difference P checks may not insert the ODE RHS. Preserve convergence diagnostics, integral drift and negative controls. Stop at invalid domains and untreated singularities.

## Delivery and acceptance
Seed-paper-first s,t,phi demo; mask invalid regions. Deliver catalog, derivations, certificates, exact/series/numerical records, PNG/PDF/NPZ, HTML, hashes and fresh review. Report model-stratum, registered-reduction and actual-solution coverage separately. Run historical 410, package/scalar, active 43, engine/chart/script regressions and audit/data-flux/workflow in UTF-8. Preserve the missing 11 October archive failure and all unrelated edits. Update project entrypoints and stale P-import status. No 2D, new nonclassical campaign, core engine rewrite or PINN.
