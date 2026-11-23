# Three independent parents and the material-coordinate control

The full Eulerian parent is the 2022 three-field model (R02, DOI
10.3390/sym14081679). The current historical `main.py` implements that
model; the recovered manifest-matching 2026 source implements printed scalar
P (R01, DOI 10.3390/math14030433). They are different PDE problems.

`audit_parents.py` parses the historical style template without executing it
and records its line-186 indentation error. It reproduces the Eulerian
parent's mixed generic/specialized shell defect: the alleged cubic check
has residual `3*zeta*u_x*(u**(m-1)-u**2)` and gives -6 at the recorded
witness. The new kernel uses one specialized PDE for both prolongation and
its equation shell. It accepts the corrected cubic coefficient field and
rejects the printed inconsistent one. No historical file is repaired in place.

The new engine preserves real-power multiplication and exponent collisions,
splits free jets rather than fixed physical parameters, and retains any
unintegrated determining equations. Explicit analytical integration and
independent review supply maximality for declared models. A fixed iteration
count or a list of passing generators does not supply it.

For scalar controls let q=phi_s>0, v=phi_t>0 and

    A = q*phi_tt - g*phi_ss/q**2,
    C = m*K*v**(m-1)*phi_ts/q,
    P = D_t(A) - g*D_s(C),
    M = P - D_s(v*A/q).

Momentum reconstructs bed_s=-A/g. Printed P uses bed_t=-C; corrected M
uses bed_t=-v*A/(g*q)-C. The latter retains the bed's transport relative to
water particles. Each scalar equation is checked as its own closedness
identity in `parent_models.py`; their common scaling is verified separately
with the new parent jet kernel. This is a generator control, not a maximal
classification for either scalar model.

An exact separating example is phi=s**2/2+c*t on s,c,g>0:
P=0 but M=-3*g*c/s**4. Thus a printed-scalar solution cannot automatically
be reconstructed into a solution of the physical material system.

In one dimension the mass form ds=h*dx-h*u*dt is closed precisely when
water mass is conserved. On h>0, (t,x)->(t,s) has Jacobian h and a local
inverse x=phi(t,s) with phi_s=1/h and phi_t=u. This depends on a solution;
it is not an ordinary point map of the original Eulerian point space.
The bed balance is

    bed_t - v*bed_s/q + C = 0,
    D_t(q*bed) + D_s(K*v**m-bed*v) = 0.

Their difference is identically zero using q_t=v_s. Bed reconstruction
requires closedness, a simply connected neighborhood (or zero periods),
one additive datum, and matching bed data. No arbitrary-data compatibility
is inferred.

The exact constant-slope control has

    phi = s/H + U*t - g*k*t**2/2,
    bed = k*phi+B0,
    s = H*(x-U*t+g*k*t**2/2).

Its chart Jacobian is H>0 and its positive-speed interval obeys U-g*k*t>0.
Both corrected bed derivatives agree. The printed bed_t rule has defect
k*(U-g*k*t). These are constructed controls, not source experiments.

`parent_models_receipt.json` binds these computations to freshly checked
local bytes for primary sources R01/R02/R03/R04/R07/R08. The source ledger
retains DOI, version and equation/page anchors. No new literature novelty
claim is made.
