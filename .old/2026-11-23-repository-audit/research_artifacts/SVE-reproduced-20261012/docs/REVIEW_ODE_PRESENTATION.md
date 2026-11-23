# Independent review: ODE presentation and figures

Date: 2026-10-13. Scope: the printed scalar SVE equation only, the revised
`draft/main.tex` presentation, and the new cubic-IVP figures in
`results/presentation/`. This review does not extend to the advectively
corrected scalar equation, the full bed-field system, or arbitrary IBVP data.

## Claim-level verdict

| Requested purpose | Verdict and boundary |
|---|---|
| Account for source (28)--(31), (33) | **Accepted as a corrected, explicitly mapped account.** The manuscript identifies (28) as the 3.6 third-order profile equation, (29) as its `P=F'` second-order form, (30) as the nonconstant-`P` first-order equation for `M(P)=P'`, (31) as its integrated `M=I0/B` form, and (33) as the 3.9 traveling family with `alpha3` retained. Its separate exact witnesses continue to refute those *printed* formulas as universal equations; it does not claim source agreement. |
| Explain PDE-to-ODE compression | **Accepted.** The flow of `X=d_t+alpha*d_s+alpha3*d_phi` fixes `z=s-alpha*t` and `w=phi-alpha3*t`; graph invariance gives `phi=alpha3*t+F(z)`. The displayed chain rule and `D_t=-alpha*D_z`, `D_s=D_z` show why one invariant coordinate replaces `(t,s)`. This selects invariant solutions, not all PDE solutions. |
| Lower ODE order and independently check the numerical solutions | **Accepted locally and numerically.** Direct substitution gives `E=-alpha*d_z[B(P)C]`, with `B=alpha^2 P-g/P^2-g m kappa (alpha3-alpha P)^(m-1)/P`. For `alpha!=0`, `I=B C=I0`; where `B!=0`, the two-state system is `F'=P`, `P'=I0/B(P)`. The separate DOP853 two-state solve and evaluation of `I` on the RKF45 three-state grid are finite consistency diagnostics, not rigorous error bounds. The manuscript also retains the distinct 3.4 first integral and does not assert one for 3.5. |
| Combine numerical and series evidence with plots | **Accepted with finite-precision qualifications.** The new figures pair degree-six Taylor profiles with saved RKF45/DOP853 nodes and show componentwise differences at four matching saved nodes. A second figure shows signed integral drift and two-state/three-state disagreement. Captions identify constructed cubic IVPs, distinct solved intervals, resolution-screen markers, and the absence of a certified remainder, convergence radius, or continuous error bound. Both PNGs were visually inspected; labels, legends and axes are legible with no overlap. |

## Independent checks

- Re-derived the traveling pullback from `p=alpha3-alpha*P`, `q=P`,
  `a=alpha^2*C`, `b=-alpha*C`, `c=C`; it equals the manuscript's undivided
  `-alpha*d_z[B(P)C]`. Expanding the derivative gives
  `B(F')F'''+B'(F')(F'')^2=0`, then `B(P)P''+B'(P)(P')^2=0`.
- For `alpha=-1`, `alpha3=0`, `m=3`, `g=1`, `kappa=1/30`, independently
  obtained `B=(9P^3-10)/(10P^2)`, `I0=-71/200` at `(P,C)=(1/2,1/10)`,
  and `-B'/B=338/71` at `P=1/2`. The printed nonzero branch of (31) gives
  `d_P(B*M_source)=960/8281` there, not zero. This is an exact rational
  source-formula counterexample, not a rounding discrepancy.
- Independently evaluated the 3.4, 3.6 and 3.9 cubic first-integral
  formulas on saved DOP853 CSVs and checked their SHA-256 values against
  `numerics.json`. Their initial constants are `79/200`, `-71/200`,
  `-79/200`; maximum absolute grid drifts were respectively
  `4.44e-16`, `1.67e-16`, `2.22e-16`. This check used direct array formulas,
  not the package's density helper.
- Inspected `plots.json`: each of three cases passes model, parameters,
  interval, initial jet, equation fingerprint and CSV-byte provenance
  checks; each has four saved series comparison nodes. The present
  `main.py` source hash and all four figure hashes match the receipt.
- Read the new integration test. It regenerates both figures from copied
  bound data, independently evaluates the three integrals, and rejects a
  stale CSV before producing figures or a success receipt.

## Conditions and execution record

The regular traveling chart requires `P>0`, `v=alpha3-alpha*P>0`,
`alpha!=0`, and `B(P)!=0`. The further `M(P)` coordinate additionally
requires nonconstant `P` (`I0!=0` on this chart); `I0=0` gives the separate
constant-`P`, affine-`F` branch. The local free-particle/eight-point claim
uses only the invertible `Y(P)=Integral(B(P),dP)` chart, not a global
classification through zeros of `B`. For the cubic 3.6 slice, the positive
zero of `B` is `(10/9)^(1/3)`, away from the checked initial `P=1/2`.

I inspected the saved active-package and focused-integration test logs:
**76 passed in 16.60 s** and **1 passed in 3.47 s**, respectively. The
director ran the final canonical plot generation and native manuscript
build. The build log reports 36 pages with no overfull box or undefined
citation/reference; it does retain underfull-box layout diagnostics. The
director rendered and inspected changed pages 25--31 and 34--36; I
independently inspected the two standalone PNG figures, not every PDF page.
The required data-flux checker returned `verified` and the workflow runner
`passed`, as reported in `PRESENTATION_VALIDATION.md`. The repository audit
still reports **218 existing issues** and exits 1; the broader regression
has **168 passes and one pre-existing Windows CRLF fixture failure**.
An initial quiet full-package attempt was stopped after a stall; the final
diagnostic retry passed. I did not rerun those broader commands or the
full LaTeX build; their outcome is attributed to the director's records.
