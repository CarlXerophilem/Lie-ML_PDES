# Independent scalar-SVE reductions and source audit

Reference: Paliathanasis, Leon and Leach, *Mathematics* **14** (2026), 433,
v3 PDF, pp. 6-9, Table 3, equations (24)-(34). This note concerns its
**printed scalar** equation (7), not the advectively corrected physical model
or the full bed-field system. The paper's reduced formulas are comparison
targets, not inputs to `derive_reduction`.

## Equation, jets, and chart

Write `p=phi_t`, `q=phi_s`, `a=phi_tt`, `b=phi_ts`, `c=phi_ss`, and use
`r,w,x,y` for `phi_ttt,phi_tts,phi_tss,phi_sss`. The source equation is

```
E_m = D_t(q*a - g*c/q^2)
      - g*D_s(m*kappa*p^(m-1)*b/q) = 0, beta=m*kappa.
```

We use `g>0`, `kappa>0`, and the local real chart `q>0,p>0`. A reduction
that crosses `q=0` is undefined, not a solution of the divided equation.
For noninteger `m`, `p>0` also chooses the real power branch. In a regular
third-order row, the normal form `H=rhs` additionally requires the displayed
coefficient of `H` to be nonzero. `z,F,P,C,H` mean
`z,F(z),F'(z),F''(z),F'''(z)`. Each API row lists all ten pulled-back jets,
the PDE pullback, the highest coefficient, and the original `p,q` at `t=1`.

## Translation generators and graph invariance

For `X=tau*d_t+xi*d_s+eta*d_phi`, a graph must satisfy
`Q=eta-tau*phi_t-xi*phi_s=0`. This is separate from equation symmetry.

| Row | Generator and Q | Invariant graph | Outcome |
|---|---|---|---|
| 3.1 | `X1=d_t`, `Q=-phi_t` | `phi=F(s)` | `E=0`; `p=0` is outside positive-velocity chart. |
| 3.2 | `X2=d_s`, `Q=-phi_s` | `phi=F(t)` | `q=0`, so source PDE is undefined. |
| 3.3 | `X3=d_phi`, `Q=1` | None | No invariant graph, despite invariant base coordinates `t,s`. |
| 3.6 | `X1+alpha*X2` | `phi=F(s-alpha*t)` | Regular ODE if `alpha!=0` and its leading coefficient is nonzero. |
| 3.7 | `X1+alpha*X3`, `Q=alpha-phi_t` | `phi=alpha*t+F(s)` | Identity `E=0`; positive chart only if `alpha>0,P>0`. |
| 3.8 | `X2+alpha*X3`, `Q=alpha-phi_s` | `phi=alpha*s+F(t)` | `E=alpha*F'''(t)`; if `alpha>0`, `F=c0+c1*t+c2*t^2/2`. |
| 3.9 | `X1+alpha*X2+alpha3*X3` | `phi=alpha3*t+F(s-alpha*t)` | Regular ODE if `alpha!=0` and leading coefficient nonzero. |

The source's prose for 3.1-3.2 swaps `t` and `s` relative to its own Table 3.
Its displayed ansatzes for 3.7-3.8 are likewise reversed. At `alpha=1`,
`phi=t+s+s^3/6` has `p=1`, `q=1+s^2/2>0`, and `E=0`, although its
`F'''(s)=1`: the source 3.8 claim that the *wrong* graph requires `F'''=0`
is false. The printed quadratic (32) is a valid special solution of the PDE,
but neither the general solution on that graph nor an invariant under the
claimed generator. The correct 3.8 quadratic is a function of `t`.

At `alpha=0`, 3.6 becomes 3.1 and 3.9 becomes 3.7; neither involves the
division by `alpha` used below. They are separately typed as identities.

## Traveling rows 3.6 and 3.9

Set `z=s-alpha*t`, `v=alpha3-alpha*P`, and `phi=alpha3*t+F(z)`;
3.6 is `alpha3=0`. The complete jets are

```
phi=alpha3*t+F, p=v, q=P,
a=alpha^2*C, b=-alpha*C, c=C,
r=-alpha^3*H, w=alpha^2*H, x=-alpha*H, y=H.
```

The inertial current is `A=(alpha^2*P-g/P^2)*C`; the sediment flux is
`J=-alpha*m*kappa*v^(m-1)*C/P`. Thus the *original* equation pulls back,
without multiplying by a possibly zero expression, to

```
E = -alpha*dI/dz,
I = B(P)*C,
B(P)=alpha^2*P-g/P^2-g*m*kappa*v^(m-1)/P.
```

For `alpha!=0`, `I=I0` is an exact first integral. Since `C=P'`, the
second-order profile equation is `d/dz[B(P)*P']=0`. On an interval where
`B(P)!=0`, `Y(P)=Integral(B(P),dP)` is a locally invertible **point**
transformation and `Y''(z)=0`. This independently verifies the local
free-particle/eight-point-symmetry assertion for the *corrected* equation;
it does not rescue the printed expanded equations. The eight-symmetry claim
is local to this regular `B!=0` chart, not a global classification through
zeros or singular branches. For `I0!=0`, the exact quadrature is
`z-z0=(Y(P)-Y(P0))/I0`. For `I0=0` and `B!=0`, `P` is constant and `F`
is affine; this branch would be lost by division by `I0`. The branch guards
are `P>0`, `v>0`, and `B(P)!=0` for the linearizing chart.

For `alpha=-1,alpha3=0,m=3`, `B=(1-beta*g)*P-g/P^2`, so a real closed
form for the autonomous first-order reduction is
`M(P)=P'=I0*P^2/[(1-beta*g)*P^3-g]`. This avoids complex powers of `-1`.

## Scaling rows 3.4, 3.5, and Table 3 mixed row

Use the common template `phi=t^A F(z)`, `z=s*t^B`, `t>0` and generator
`X=t*d_t-B*s*d_s+A*phi*d_phi`. Its graph equation vanishes exactly. Define
`D=d/dz+P*d/dF+C*d/dP+H*d/dC` and `V=A*F+B*z*P`. At `t=1`, all jets are

```
phi=F, p=V, q=P,
a=(A-1)*V+B*z*D(V), b=D(V), c=C,
r=(A-2)*a+B*z*D(a), w=D(a), x=D(b), y=H.
```

Their powers away from `t=1` are respectively `t^A`, `t^(A-1)`,
`t^(A+B)`, `t^(A-2)`, `t^(A+B-1)`, `t^(A+2B)`, `t^(A-3)`,
`t^(A+B-2)`, `t^(A+2B-1)`, and `t^(A+3B)`. Substitution in equation (7)
gives `t^(-A-1)*R`, where

```
J_A = P*a-g*C/P^2,
J_s = m*kappa*V^(m-1)*b/P,
R = -A*J_A+B*z*D(J_A)-g*D(J_s).
```

This single-power factorization holds for X4 for any real `m`, and for X5
and nonzero mixed X4+lambda X5 at `m=3`. Otherwise two distinct time
powers remain: those generators are not reductions of the fixed-`m` PDE.
The cases are:

| Row | A | B | z | phi |
|---|---:|---:|---|---|
| 3.4, X4 | 1 | -1 | `s/t` | `t*F(z)` |
| 3.5, X5, m=3 | 0 | 2 | `s*t^2` | `F(z)` |
| mixed X4+lambda X5, m=3 | `1/(1+lambda)` | `(2*lambda-1)/(1+lambda)` | `s*t^B` | `t^A*F(z)` |

For `lambda=0`, mixed equals X4 and is valid for general `m`. The
resonance `lambda=-1` cannot use this time-normalized chart because the
generator has zero time component. Instead `X4-X5=3s*d_s+phi*d_phi`;
on `s>0` its invariants are `t,phi*s^(-1/3)`, and the graph is
`phi=s^(1/3)*F(t)`. Its source pullback is `s^(-1/3)*R(t,F,P,C,H)` at
`m=3`, evaluated in the implementation at `s=1` with every jet listed.

For X4 there is an additional exact certificate at **symbolic** exponent:

```
I_X4 = C*(-z^3*P+g*z/P^2
          +g*m*kappa*z*(F-z*P)^(m-1)/P),
D(I_X4)=R_X4.
```

This reduces ODE order by one; it does not further reduce the number of
independent variables, which was already one. Its real branch requires
`z>0,P>0,F-z*P>0`. The initial jet `(2,1/2,1/10)` at `z=1` meets
these guards for `g=1,kappa=1/30`.

## Printed power law and further X5 reduction

At `m=3`, the paper's `F=A*z^(1/3)` has
`P=A*z^(-2/3)/3`, `C=-2A*z^(-5/3)/9`, `H=10A*z^(-8/3)/27`.
Direct substitution into both 3.4 and 3.5 original-PDE pullbacks gives
zero exactly if `(12*g*kappa-1)*A^3+27*g=0`, the printed condition
`(4*beta*g-1)*A^3+27*g=0`. For the dimensionless campaign parameters,
`A^3=45>0`. However, the 3.4 coefficient of `H` on this profile is
`z^(7/3)*[(12*g*kappa-1)*A^3+27*g]/(3*A^2)=0`. Therefore it belongs
to a singular normal-form branch and cannot be reached by dividing by
that coefficient at its jet. The profile value is
`phi=A*s^(1/3)*t^(2/3)`, which **increases** with `t` for fixed `s>0`;
it tends to zero as `t` tends to zero, although derivatives can blow up.
Nothing here establishes a shock: a shock requires discontinuity/jump
information absent from this smooth local profile.

For 3.5, `F` is absent from its residual; setting `mu=P` converts it to a
second-order ODE. The inherited scaling is
`3z*d_z-2mu*d_mu`. Its invariants are
`Sigma=z^(2/3)*mu`, `M=z^(5/3)*mu'`. The correct derivative is

```
dM/dSigma = [(5/3)*M+z^(8/3)*mu''] / [(2/3)*Sigma+M].
```

The source page 7 also prints the wrong coordinate derivative in each second
component: `3sigma*d_sigma+phi*d_sigma` after (25), and
`3sigma*d_sigma-2mu*d_sigma` after (26). The correct fields are
`3sigma*d_sigma+phi*d_phi` and `3sigma*d_sigma-2mu*d_mu`.
Indeed, `X4(s*t^2)=3*s*t^2`, `X4(phi)=phi`, and the first prolongation
coefficient for `mu=phi_sigma` is `mu-3mu=-2mu`.

Insert `mu''` from the correct 3.5 residual. This yields a rational
first-order equation only where `(2/3)*Sigma+M!=0` and the original
third-order leading coefficient is nonzero. It is not the printed (27);
at `Sigma=M=g=z=1,kappa=1/30`, (27) gives `89/117`, whereas the
correct derivative gives `-187/65`. Calling either expression "Abel-type"
does not prove solvability or specify a classical Abel normal form.

## Equation-by-equation source verdict

`source_formulas.printed_equation_witnesses()` returns the exact, JSON-safe
status records. Except where shown otherwise, witnesses use `m=3`,
`g=1`, `kappa=1/30`, `z=1`, `P=1/2`, `C=1/10`, and positive original
velocity and gradient. A witness sets a printed formula to zero and then
evaluates the independently derived original-PDE residual at the same jet.

| Eq. | Status and decisive check |
|---|---|
| (24) | Refuted as literally typeset: its expanded expression sets `H=23/250` with `F=2`, but original residual is `2367/5000`. The separate power-law amplitude is nevertheless exact. Its beta-term typography is delicate; the source file preserves the literal page-image transcription. |
| (25) | Refuted: printed zero at `H=-88/25`; original residual `437/25`. |
| (26) | Refuted as the `mu=F'` rewrite of (25): same failed zero. |
| (27) | Refuted: printed `M_Sigma=89/117`; correct `-187/65`. Its chain-rule denominator is absent. |
| (28) | Refuted for `alpha=-1`: printed zero at `H=0`; original residual `169/1000`. |
| (29) | Refuted for the same slice: printed zero at `mu''=0`; original residual `169/1000`. |
| (30) | Refuted: printed `M_Xi/M=172/35`; exact `-B'/B=338/71`. |
| (31) | Refuted for nonzero `M0=1`, `alpha=-1,m=3`: the derivative of the required conserved `B(P)M(P)` at `P=1/2` is `960/8281`, not zero. `M0=0` is a trivial separate branch. |
| (32) | Qualified: quadratic in `s` is a valid special PDE solution, but is not forced and is attached to the wrong 3.8 generator. |
| (33) | Refuted for `alpha=-1,alpha3=1`: printed zero at `H=-5/119`; original residual `40337/119000`. |
| (34) | Refuted literally: the PDF has `-alpha^2*kappa` **inside** the integral, where `kappa` is the traveling coordinate, not `-alpha^2*tau`. With lower limit `P0=1`, differentiating it and setting `z=1,P=1/2` forces `C=10/69,H=60200/328509`, but the original residual is `-118420/328509`. Replacing `kappa` by dummy `tau` recovers one normalization `I0=-1`; it does not give the general `I0` family. |

These are failures of the displayed *reduced formulas*, not a claim that
the entire article, its verified generator list, or every analytic special
solution is false. The exact power law and the local free-particle structure
survive independent derivation. No result here extends to arbitrary initial
or boundary data, an entropy/shock theory, a global physical chart, or the
advectively corrected/full Saint-Venant--Exner system.

## Reproduction

From the repository root, run
`python -B -m pytest -q research_artifacts/SVE-reproduced-20261012/tests/test_reductions.py`.
The API also exposes `build_reduction_report()`, which serializes all nine
rows, the Table 3 mixed row, certified integrals, and source witnesses.
The main runner defaults to this package's `results/`; `--out` selects a
separate output directory. The frozen historical package is not rewritten.
