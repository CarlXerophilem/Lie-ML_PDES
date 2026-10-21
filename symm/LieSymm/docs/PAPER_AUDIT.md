# Paper 2026 v3: nine reductions and solution claims

Reference checked directly: Paliathanasis, Leon & Leach, *Mathematics* 14 (2026), 433, v3, DOI `10.3390/math14030433`. The local PDF SHA-256 is `2b853b7ecf58820105384d8931d1cd1f989fd0a1cb2ea7553430f4cd55e8cc5f5`; the PDF text extraction used for navigation is in `sources/paper2026/paper-v3-extract.txt`. Equations were visually checked against PDF pp. 6-9, including Table 3 and (24)-(34); extraction is not treated as authoritative for ambiguous formula layout.

## Model boundary

`P` denotes the paper's printed scalar master equation (7), equivalently the compatibility equation obtained from its printed bed equations. `M` denotes the advectively corrected scalar material-coordinate equation obtained when the bed variable is interpreted as `b(t,s)=B(t,phi(t,s))`; the missing bed-advection term means `P` and `M` are not equivalent. `E` denotes the full Eulerian shallow-water/bed system, which is not solved merely by solving `P`.

The source equation audited here is

```text
P = D_t(q*a - g*c/q^2) - g*D_s(m*kappa*p^(m-1)*b/q) = 0,
p=phi_t, q=phi_s, a=phi_tt, b=phi_ts, c=phi_ss.
```

The local real chart used for noninteger powers and physical reconstruction is `p>0`, `q>0`, with `g,kappa>0`. Any divided third-order normal form additionally needs its leading coefficient nonzero. A formal `P` solution gives `h=1/q`, `u=p`, and position map `x=phi(t,s)` on a regular material patch; it does **not** by itself establish `M` or `E`. Smooth profiles and a singularity of a derivative do not establish a shock; the paper supplies no jump/entropy construction here.

## Case inventory

The invariant-surface condition is `Q=eta-tau*p-xi*q=0`. It is required in addition to invariance of the PDE; invariant base coordinates alone do not define a graph reduction.

| Paper case | Invariant graph / pullback into P | Audit status |
|---|---|---|
| 3.1, `X1=∂t` | `phi=F(s)`, hence `p=0`; P vanishes identically wherever defined. | Identity only, outside the declared `p>0` chart. Paper prose instead says `phi=phi(t)`, which belongs to the `X2` graph. No admissible positive-velocity reduction. |
| 3.2, `X2=∂s` | `phi=F(t)`, hence `q=0`; P has denominators in `q`. | Undefined singular chart, not a solution of the source equation as written. Paper prose instead says `phi=phi(s)`, swapping 3.1/3.2. |
| 3.3, `X3=∂phi` | `Q=1`; no invariant graph. | No reduction. Table 3's invariants `t,s` are base invariants, not a dependent-variable graph. |
| 3.4, `X4=t∂t+s∂s+phi∂phi` | `z=s/t`, `phi=t F(z)`, `p=F-zF'`, `q=F'`. Restricting the **printed source residual** `P` to this ansatz gives `P|ansatz=t^-2 R_4`; `R_4=0` is the reduced equation for `t>0`. | Valid fixed-`m` similarity reduction for `t>0`, subject to `P>0` and nonzero leading coefficient for a normal form. The displayed expanded Eq. (24) is refuted by exact substitution (witness below). Its separate cubic power profile remains an exact singular-branch solution. |
| 3.5, `X5=t∂t-2s∂s` at `m=3` | `z=s t^2`, `phi=F(z)`, `p=2z/t F'`, `q=t^2F'`; restricting the **printed source residual** gives `P|ansatz=t^-1 R_5`, hence `R_5=0` for `t>0`. `F` drops out, so `mu=F'` gives a second-order equation. | Valid reduction only at `m=3`, `t>0`, `z>0`, `mu>0` in the chosen chart. Printed (25)/(26)/(27) fail exact comparison; the corrected scaling invariants are `Sigma=z^(2/3)mu`, `M=z^(5/3)mu'`, with chain-rule denominator `(2/3)Sigma+M`, which must be nonzero. |
| 3.6, `X1+alpha X2` | `z=s-alpha*t`, `phi=F(z)`; `p=-alpha F'`, `q=F'`. Source pullback is `-alpha*d_z[B(P)P']=0`, where `B(P)=alpha^2 P-g/P^2-g*m*kappa*(-alpha P)^(m-1)/P`. | For `alpha!=0`, an exact first integral `B(P)P'=I0` is valid on real branch `P>0`, `-alpha P>0` (paper's generic real-power expression is not defined for arbitrary real `m,alpha`). At `alpha=0` it collapses to 3.1 and is chart-invalid. The paper's expanded (28)/(29)/(30)/(31) are refuted. On `B!=0`, `Y'=B(P)P'` linearizes to `Y''=0`; this supports a local corrected-equation free-particle claim, not the printed expansions globally. |
| 3.7, `X1+alpha X3` | Correct invariant graph is `phi=alpha*t+F(s)`, so `p=alpha`, `q=F'`; P is identically zero. | Paper's displayed graph `alpha*s+F(t)` is for 3.8, not 3.7. With `alpha>0`, `F'>0` gives a regular `P` chart, and arbitrary smooth `F` solves this scalar equation. This does not establish a solution of `M` or `E`. |
| 3.8, `X2+alpha X3` | Correct graph is `phi=alpha*s+F(t)`, so `q=alpha`, `p=F'`; P reduces to `alpha F'''(t)=0`. | For `alpha>0`, the solution is quadratic in `t`: `F=c0+c1*t+c2*t^2/2`, with `F'>0` if retaining the positive velocity chart. Paper swaps 3.7/3.8 ansatzes and prints a quadratic in `s` in (32). That quadratic is a special `P` solution under the other graph, not the claimed general graph solution. |
| 3.9, `X1+alpha X2+alpha3 X3` | `z=s-alpha*t`, `phi=alpha3*t+F(z)`, `p=alpha3-alpha F'`, `q=F'`; same first-integral structure as 3.6 with `v=alpha3-alpha P`, `B(P)=alpha^2P-g/P^2-g*m*kappa*v^(m-1)/P`. | For `alpha!=0`, valid first integral `B(P)P'=I0` on `P>0,v>0`; at `alpha=0` it is the 3.7 identity. Printed (33)/(34) fail exact checks. No global completeness or physical shock conclusion. |

Table 3 also contains the mixed scaling `X4+lambda X5` (not one of numbered 3.1-3.9). It has one common time power at `m=3` (and at `lambda=0`, which is X4, for any `m`). In the chart `lambda!=-1`, its graph is `phi=t^A F(s*t^B)`, `A=1/(1+lambda)`, `B=(2lambda-1)/(1+lambda)`. At `lambda=-1`, the time-normalized formula is singular; on `s>0`, use `phi=s^(1/3)F(t)` instead. Do not count this family as evidence that every Table 3 row is a valid reduction for every `m`.

## Formula and solution-claim verdicts

| Source item | Verdict | Independent check / qualification |
|---|---|---|
| (24) | Refuted literally | At `m=3,g=1,kappa=1/30,z=1,(F,P,C)=(2,1/2,1/10)`, printed expression vanishes at `H=23/250`, while direct P pullback is `2367/5000`. Page-image transcription of the beta term is delicate; this verdict applies to the literal displayed expression. |
| Cubic power profile in 3.4 | Exact but singular normal-form branch | `F=A z^(1/3)` satisfies direct P pullback iff `(12*g*kappa-1)A^3+27g=0` (same as `(4*beta*g-1)A^3+27g=0` for `m=3`). On that profile the coefficient of `H` in the 3.4 residual vanishes, so it cannot be obtained by regular division. The reconstructed position is `phi=A*s^(1/3)*t^(2/3)`, increasing in `t` for fixed `s>0`; “decays with time” is false. A shock claim is unsupported. |
| (25), (26) | Refuted literally | For the same positive test jet, printed equation sets `H=-88/25`, but original P residual is `437/25`. The `mu=F'` substitution itself is legitimate when differentiability/chart assumptions hold; the printed equation is not its correct result. |
| Reduced vector fields after (25),(26) | Refuted as typeset | Correct fields are `3z∂z+F∂F` and, after `mu=F'`, `3z∂z-2mu∂mu`. PDF prints `∂z` in the dependent-coordinate component in both places. |
| (27) | Refuted | At `Sigma=M=g=z=1,kappa=1/30`, source gives `M_Sigma=89/117`; correct transformed equation gives `-187/65`. The coordinate derivative denominator `(2/3)Sigma+M` is required and is nonzero at this witness. |
| Claimed cubic `mu` solution after (26) | Exact special solution, qualified | Same cubic amplitude condition as above. It is a singular profile at `z=0` and a singular branch of the 3.4 normal form; singularity is not a shock without weak-solution/jump analysis. |
| (28), (29) | Refuted literally | At `alpha=-1,m=3,g=1,kappa=1/30,z=1,(F,P,C)=(2,1/2,1/10)`, printed formula solved at `H=0` leaves original P residual `169/1000`; corresponding `mu''=0` witness also leaves `169/1000`. |
| Eight symmetries/free-particle assertion for (29) | Conditional and locally supported for corrected reduction | The corrected equation has first integral `B(P)P'=I0`; where `P>0`, `v>0`, `B(P)!=0`, `Y(P)=integral B(P)dP` is a locally invertible point coordinate and `Y''=0`. This verifies the local claim for the independently corrected ODE, not the printed (29), and does not cover zeros/singular branches or imply global completeness. |
| (30) | Refuted | At the paper's comparison witness, printed `M_Xi/M=172/35`; corrected first-integral equation gives `-B'/B=338/71`. Division requires `M!=0` and `B!=0`; `I0=0` is a separate constant-`P` branch. |
| (31) | Refuted for nonzero integration constant | For `alpha=-1,m=3,I0=1`, differentiating the required conserved product `B(P)M(P)` at `P=1/2` gives `960/8281`, not zero. The `I0=0` branch is separately trivial and does not rescue the asserted general formula. |
| (32) and “nonsingular” | Qualified / graph mismatch | The quadratic in `s` is a valid special solution on the 3.7 graph `phi=alpha*t+F(s)` (with appropriate positive chart); it is not forced there. For 3.8 the correct quadratic is in `t`. “Nonsingular” is only meaningful on a stated chart and does not imply physical regularity outside it. |
| (33) | Refuted literally | At `alpha=-1,alpha3=1,m=3,g=1,kappa=1/30,z=1,(F,P,C)=(2,1/2,1/10)`, printed equation sets `H=-5/119`, but original P residual is `40337/119000`. |
| (34) | Refuted literally; corrected quadrature conditional | The page image reads `integral^mu [g/tau^2 - alpha^2*kappa + (beta*g/tau)*(alpha3-alpha*tau)^(m-1)] d tau - (kappa-kappa0)=0`. Here `kappa` outside the integral is the traveling coordinate, but the same `kappa` appears in its integrand; it is not the integration variable. For `alpha=-1, alpha3=1, m=3`, the printed integrand becomes `g/tau^2-kappa+beta*g*(1+tau)^2/tau`, matching the literal-witness denominator `D=g/P^2-z+beta*g*(1+P)^2/P`. With lower limit `P0=1`, differentiating the printed formula at `P=1/2,z=1` forces `C=10/69,H=60200/328509`, leaving P residual `-118420/328509`. Replacing the coordinate `kappa` inside the integrand by dummy `tau` gives a valid first-integral quadrature for one normalization `I0=-1`, not the general family. |

The witnesses refute displayed reduced formulas, not every source generator or every exact profile. The corrected power law and local free-particle structure survive independently. Neither yields all solutions of the nonlinear ODE, arbitrary initial/boundary-data existence, entropy/shock theory, global chart continuation, or a theorem for `M`/`E`.

## Reconstruction claims

The kinematic identities `x=phi`, `u=phi_t`, `h=1/phi_s` are valid locally where the material map is invertible (`q=phi_s>0`); positive-velocity claims additionally require `p>0`. Thus a plot of `phi` is a particle-position map, not depth. Example ansatzes reconstruct as follows:

| Case | `phi(t,s)` | `u` | `h` | additional chart conditions |
|---|---|---|---|---|
| 3.4 | `t F(s/t)` | `F-zF'` | `1/F'` | `t>0`, `F'>0`, `F-zF'>0` |
| 3.5 (`m=3`) | `F(st^2)` | `2st F'` | `1/(t^2F')` | `t>0`, `s>0`, `F'>0`, `2stF'>0` |
| 3.6 | `F(s-alpha*t)` | `-alpha F'` | `1/F'` | `F'>0`, `-alpha F'>0` |
| 3.7 | `alpha*t+F(s)` | `alpha` | `1/F'` | `alpha>0`, `F'>0` |
| 3.8 | `alpha*s+F(t)` | `F'` | `1/alpha` | `alpha>0`, `F'>0` |
| 3.9 | `alpha3*t+F(s-alpha*t)` | `alpha3-alpha F'` | `1/F'` | `F'>0`, `alpha3-alpha F'>0` |

These reconstruct a local smooth shallow-water kinematic field from a `P` profile. The source derivation omits the bed-advection term required under the stated material pullback (`b_t-(p/q)b_s+...=0`); consequently they are **not** certified solutions of corrected `M` or full Eulerian `E`. A one-dimensional profile also does not establish arbitrary data, global continuation, or a shock. The paper itself says no Lagrangian was found; that statement is not a nonexistence proof and does not validate its reductions.

## Evidence boundary

Formula statuses and exact rational witnesses above agree with the independent derivations in `research_artifacts/SVE-reproduced-20261012/docs/REDUCTIONS.md` and narrative checks in `research_artifacts/SVE-reproduced-20261012/RESULTS_EXPLAINED.md`. The PDF text extraction was checked against page images 7-10 retained under `sources/paper2026/`; formula layout and the literal (34) integrand were visually confirmed. The scalar recovery source is `build/sve-autonomous-20261019/recovery/package/main.py`, SHA-256 `71224cf2e4a3ed456dc0cf9b5bb467fdf484b3ce7b4a7b7d713f649aa9747aa9`; the current `research_artifacts/SVE-reproduced-20261012/main.py` is a separate Eulerian analysis and was not used as the scalar target. No broad numerical campaign was run for this audit.
