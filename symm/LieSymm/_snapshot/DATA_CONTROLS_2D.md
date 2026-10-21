# Specified 2D data controls and explicit point maps

This module checks specified examples after obtaining the unrestricted
coefficient families. It does not derive a PDE solution from an initial
profile, infer future boundary compatibility, or classify the full
equivalence groupoid.

## 1. Two exact flow families

Write \(R=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)\),
\(W=(u,v)^T\), and \(\Delta=t-t_0\). Spatially uniform flow with constant
\(h=H>0,B=B_0\) satisfies
\[
W_t=-fRW,\qquad W=e^{-fR\Delta}W_0.
\]
The component formula is
\(u=U_0\cos(f\Delta)+V_0\sin(f\Delta)\),
\(v=V_0\cos(f\Delta)-U_0\sin(f\Delta)\). Speed squared is the constant
\(U_0^2+V_0^2>0\).

For the planar bed \(B=kx+\ell y+B_0\), retain constant depth and solve
\[
W_t=-g(k,\ell)^T-fRW.
\]
At \(f=0\), \(W=W_0-g(k,\ell)^T\Delta\). At \(f\ne0\),
\[
W_*=(-g\ell/f,gk/f)^T,\qquad
W=W_*+e^{-fR\Delta}(W_0-W_*).
\]
The sediment flux is spatially uniform for both Grass and slope terms, so
its divergence vanishes even though its value can vary with time. These
flows solve every registered branch on the stated interval where
\(H>0\) and \(u^2+v^2>0\). There is no all-time nonzero-speed assertion
for the accelerated family.

## 2. Fixed-time initial graph stabilizers

The implementation imports the actual solved general coefficients, renames
their free constants to avoid collisions with data parameters, and solves
\[
\tau|_{t=t_0}=0,\qquad
\eta_i-\xi\partial_x U_{0,i}-\chi\partial_y U_{0,i}=0.
\]
Polynomial identities are split exactly in \(x,y\); no samples are used.
Unknown nonzero pivots retain explicit guards and unresolved zero-pivot
branches. Nonpolynomial identities remain unresolved. The frozen initial
profile's original-PDE diagnostic is reported separately and is not called
an evolving solution.

Flow and initial profiles must be real and finite on their declared domain.
Definite complex or nonfinite values are rejected; undecidable symbolic
reality or finiteness remains an explicit `data_domain_guards` condition.

For the concrete constant \((h,u,v)=(2,3,4)\), fixed velocity removes the
rotation and velocity-dilation coefficients. The flat initial bed admits
three stabilizer dimensions for the \(G=0,f=0\) branches, and two for
the other branches. A nonzero linear bed admits two combined spatial/bed
translations. The full quadratic bed \(1+x^2+y^2\) admits none. These
dimensions describe these particular initial graphs only.

## 3. Primitive/conservative field point map

The field map and inverse are
\[
(h,u,v,B)\mapsto(h,P,Q,B)=(h,hu,hv,B),\qquad
u=P/h,\quad v=Q/h.
\]
Its field Jacobian is \(h^2\), so it is locally invertible on \(h>0\).
The nonzero-speed guard becomes \(P^2+Q^2>0\). The conservative equations
are
\[
\begin{split}
h_t+P_x+Q_y&=0,\\
P_t+(P^2/h+gh^2/2)_x+(PQ/h)_y+ghB_x-fQ&=0,\\
Q_t+(PQ/h)_x+(Q^2/h+gh^2/2)_y+ghB_y+fP&=0,
\end{split}
\]
with the same bed equation after substituting \(u=P/h,v=Q/h\) in its
actual flux. If \(E_h,E_u,E_v,E_B\) denote the pulled-back primitive rows,
the conservative rows are exactly
\[
(E_h,\ uE_h+hE_u,\ vE_h+hE_v,\ E_B)^T.
\]
The row multiplier also has determinant \(h^2\). This is an explicit
field point equivalence, unlike a mass-coordinate or scalar-elimination
construction. The generator pushforward includes both product-rule terms:
\(\eta_P=u\eta_h+h\eta_u\),
\(\eta_Q=v\eta_h+h\eta_v\).

## 4. One verified signed-Coriolis equivalence

The reflection
\[
(t,x,y,h,u,v,B,f)\mapsto(t,x,-y,h,u,-v,B,-f)
\]
preserves the chart and radial transport/diffusion laws. Its four PDE rows
have parity \((+,+,-,+)\), checked with all required derivative signs.
For \(f\ne0\), this maps between opposite parameter values; it is not a
symmetry at one fixed nonzero \(f\). At \(f=0\), it is a discrete symmetry
of the fixed model. No assertion is made that this map generates all
disconnected equivalences.

## 5. Reproduction and status

`run_data_controls(name)` returns `verified_specified_data_controls` only
when both constructed flows, all three initial graphs, the conservative
point map, and the signed-Coriolis reflection pass their exact checks.
Every result carries guards and per-test residuals/statuses. The test module
also independently checks the velocity ODE signs, initial values, one
parameter rank drop, domain rejection, and the generator product rule.

```powershell
python -B -m pytest -q build/sve-general-symm-20261020/tests/test_data_experiments_2d.py
python -B build/sve-general-symm-20261020/data_experiments_2d.py --branch grass_cubic_f_nonzero
```

The first bounded module run passed all 34 tests in 9.13 seconds (10.223
seconds including process startup), within its 60-second limit. The full
output and command/timing receipt are retained in `runs/data2d-first.log`
and `runs/data2d-first-receipt.json`. The real/finite profile-domain repair
was made before this first run. Independent review is a separate gate,
recorded in `DATA_2D_REVIEW.md` and `data_2d_review.json`; this test result
does not by itself assert Stage 2 completion.
