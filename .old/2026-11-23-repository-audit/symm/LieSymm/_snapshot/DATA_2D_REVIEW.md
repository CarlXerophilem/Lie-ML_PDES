# Independent review of the 2D data controls

Review status: **accepted**. The three bounded phases contain 1005 independently checked identities and conditions. The exact source hashes and individual phase receipts are bound in `data_2d_review.json`.

The reviewer did not author `data_experiments_2d.py`. The review reconstructs all four PDE rows with ordinary partial derivatives for the two returned flow graphs in all 17 refined branches. Initial-data dimensions are recomputed as nullities of independently assembled polynomial tangency matrices; returned stabilizer directions are checked to span the entire kernel for the three specified profiles. A separate order-two jet derivative checks the primitive/conservative chain rule, invertible field and equation-row maps, and signed-f reflection.

The field map is `(h,u,v,B) -> (h,hu,hv,B)` and both its Jacobian determinant and the equation-row multiplier determinant equal `h^2`. Hence the equivalence is restricted to `h>0`. The reflection `(y,v,f) -> (-y,-v,-f)` preserves the parameterized equations; at fixed nonzero f, omitting the parameter flip leaves the checked nonzero momentum residuals `(2fv,2fu)`. No complete equivalence groupoid is inferred.

The review identified a real-domain gap for complex/nonfinite initial profiles. The author was asked to reject those profiles; the independent initial-data phase includes both regressions. Unknown profile rank pivots retain explicit guards and unresolved zero-pivot branches. Nonpolynomial profile splitting is explicitly unresolved.

Acceptance covers two constructed smooth flows, three fixed-time data profiles per branch, and the two explicit maps. Positivity and nonzero-speed conditions restrict the charts; the planar-bed flow is not claimed global. A fixed initial graph is not a future evolution or boundary-compatibility theorem. Classification maximality and any conditional-symmetry or learned stage are outside this review.
