# Reproduction and independent audit of the scalar SVE paper

This report distinguishes paper statements, exact checks, corrected results, and unresolved claims. Numerical IVPs are new constructed dimensionless examples. A successful execution does not certify every source claim.

## Run status

### started utc

2026-10-13T05:15:23.694644+00:00

### stage

all

### selection

all

### case

all

### calculation mode

fresh symbolic derivation and requested numerical stages

### complete audit

True

### source agreement

assessed_per_claim

### numerical scope

constructed dimensionless local IVPs

### elapsed seconds

19.57746099997894

### execution status

finished

### all printed claims reproduced

False

### symbolic passed

True

### symbolic failures

(none)

### numerical passed

True

## Sources and complete equation inventory

### sources

#### id

SVE

#### path

```text
ref/main/Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables-mathematics-14-00433-v3.pdf
```

#### doi

10.3390/math14030433

#### sha256

2b853b7ecf58820105384d8931dcd1f989fd0a1cb2ea7553430f4cd55e8cc5f5

#### pages

11

#### verification

local_primary_pdf_checked

#### accessed

2026-10-13

#### id

RKF-reference

#### path

ref/Two parameters Liegroup analysis and numerical solution of unsteady free convective flow of non-Newtonian fluid.pdf

#### doi

10.1016/j.aej.2016.05.009

#### sha256

aa6d304b132dc9804be653b0dca590136d96ab1a08320c0e0d1333588baa714b

#### pages

10

#### verification

local_primary_pdf_checked

#### accessed

2026-10-13

### source verification complete

True

### environment

#### python

3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]

#### platform

Windows-11-10.0.26300-SP0

#### packages

##### sympy

1.14.0

##### numpy

2.3.5

##### scipy

1.17.1

##### matplotlib

3.10.7

##### pytest

9.0.1

##### pymupdf

1.27.2.3

### method scope

```text
Uddin et al. use RKF fourth-fifth order plus shooting for a different BVP; SVE initial data and algorithm tolerances here are newly specified.
```

### equations

#### equation

1

#### page

2

#### description

Eulerian mass balance

#### evidence module

models

#### status

model_assumption

#### evidence

models: coordinate pullback; the Eulerian balances and power closure are input assumptions, not empirical validation.

#### equation

2

#### page

2

#### description

Eulerian conservative momentum balance

#### evidence module

models

#### status

model_assumption

#### evidence

models: coordinate pullback; the Eulerian balances and power closure are input assumptions, not empirical validation.

#### equation

3

#### page

2

#### description

Exner bed balance

#### evidence module

models

#### status

model_assumption

#### evidence

models: coordinate pullback; the Eulerian balances and power closure are input assumptions, not empirical validation.

#### equation

4

#### page

2

#### description

Power-law sediment closure

#### evidence module

models

#### status

model_assumption

#### evidence

models: coordinate pullback; the Eulerian balances and power closure are input assumptions, not empirical validation.

#### equation

5

#### page

2

#### description

Lagrange momentum equation

#### evidence module

models

#### status

verified

#### evidence

models.checks.momentum_pullback_zero

#### equation

6

#### page

2

#### description

Printed Lagrange bed equation

#### evidence module

models

#### status

corrected_under_declared_bed_pullback

#### evidence

models.discrepancies.D-MODEL-06; missing -(phi_t/phi_s)b_s

#### equation

7

#### page

2

#### description

Printed third-order scalar master equation

#### evidence module

models

#### status

verified_for_printed_pair

#### evidence

models.checks.printed_compatibility_zero; source equation retained

#### equation

8

#### page

3

#### description

General PDE notation

#### evidence module

symmetries

#### status

definition_reproduced

#### evidence

symmetries and core.prolongation

#### equation

9

#### page

3

#### description

Infinitesimal time transformation

#### evidence module

symmetries

#### status

definition_reproduced

#### evidence

symmetries and core.prolongation

#### equation

10

#### page

3

#### description

Infinitesimal label transformation

#### evidence module

symmetries

#### status

definition_reproduced

#### evidence

symmetries and core.prolongation

#### equation

11

#### page

3

#### description

Infinitesimal field transformation

#### evidence module

symmetries

#### status

definition_reproduced

#### evidence

symmetries and core.prolongation

#### equation

12

#### page

3

#### description

General point infinitesimal generator

#### evidence module

symmetries

#### status

definition_reproduced

#### evidence

symmetries and core.prolongation

#### equation

13

#### page

3

#### description

Finite-to-infinitesimal invariance limit

#### evidence module

symmetries

#### status

qualified

#### evidence

Use pr(X)E=0 ON E=0, or pr(X)E=lambda E off shell; the literal unconditional zero condition rejects scaling.

#### equation

14

#### page

3

#### description

Prolonged infinitesimal criterion (on the equation manifold)

#### evidence module

symmetries

#### status

qualified

#### evidence

Use pr(X)E=0 ON E=0, or pr(X)E=lambda E off shell; the literal unconditional zero condition rejects scaling.

#### equation

15

#### page

3

#### description

Lie derivative of a scalar function

#### evidence module

symmetries

#### status

definition_reproduced

#### evidence

symmetries and core.prolongation

#### equation

16

#### page

4

#### description

First prolongation recursion

#### evidence module

symmetries

#### status

verified

#### evidence

core.prolongation recursive formula; unrestricted determining split and direct polynomial substitution tests

#### equation

17

#### page

4

#### description

Ellipsis in the displayed prolongation sequence

#### evidence module

symmetries

#### status

definition_reproduced

#### evidence

symmetries and core.prolongation

#### equation

18

#### page

4

#### description

Higher prolongation recursion

#### evidence module

symmetries

#### status

verified

#### evidence

core.prolongation recursive formula; unrestricted determining split and direct polynomial substitution tests

#### equation

19

#### page

5

#### description

Linear combinations of algebra basis elements

#### evidence module

algebra

#### status

definition_reproduced

#### evidence

algebra.formulas.adjoints and orbits

#### equation

20

#### page

5

#### description

Adjoint equivalence

#### evidence module

algebra

#### status

definition_reproduced

#### evidence

algebra.formulas.adjoints and orbits

#### equation

21

#### page

5

#### description

Nonzero generator rescaling

#### evidence module

algebra

#### status

definition_reproduced

#### evidence

algebra.formulas.adjoints and orbits

#### equation

22

#### page

6

#### description

Invariant characteristic equation

#### evidence module

reductions

#### status

verified_on_recorded_charts

#### evidence

reductions.cases and table3_mixed: Q, invariant coordinates and complete jet pullbacks

#### equation

23

#### page

6

#### description

Functions of invariants

#### evidence module

reductions

#### status

verified_on_recorded_charts

#### evidence

reductions.cases and table3_mixed: Q, invariant coordinates and complete jet pullbacks

#### equation

24

#### page

7

#### description

X4 reduced ODE

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq24

#### detail

##### printed H zero

23/250

##### original residual at zero

2367/5000

##### source

p.7 eq(24)

##### printed

Literal displayed expanded beta terms; positive jet F=2,P=1/2,C=1/10

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### equation

25

#### page

7

#### description

X5 reduced ODE

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq25

#### detail

##### printed H zero

-88/25

##### original residual at zero

437/25

##### source

p.7 eq(25)

##### printed

Displayed X5 third-order equation

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### equation

26

#### page

7

#### description

Derivative reduction of X5 ODE

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq26

#### detail

##### printed mu second zero

-88/25

##### correct mu equation at zero

437/25

##### source

p.7 eq(26)

##### printed

Equation (25) with mu=phi_sigma, hence same failed zero

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### equation

27

#### page

7

#### description

Claimed Abel equation

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq27

#### detail

##### printed Mprime at sample

89/117

##### correct Mprime at sample

-187/65

##### correct rhs

```text
-(36*M**2*Sigma**3*g*kappa - 12*M**2*Sigma**3 - 6*M**2*g + 120*M*Sigma**4*g*kappa - 16*M*Sigma**4 - 5*M*Sigma*g + 72*Sigma**5*g*kappa - 6*Sigma**5)/(Sigma*(3*M + 2*Sigma)*(12*Sigma**3*g*kappa - 4*Sigma**3 + g))
```

##### source

p.7 eq(27)

##### printed

Displayed Abel-type polynomial RHS for M_Sigma

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### status

refuted_as_printed

#### equation

28

#### page

7

#### description

Traveling-wave third-order ODE

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq28

#### detail

##### printed H zero

0

##### original residual at zero

169/1000

##### source

p.7 eq(28)

##### printed

Traveling expanded equation with alpha=-1,m=3

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### equation

29

#### page

8

#### description

Traveling-wave derivative ODE

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq29

#### detail

##### printed H zero

0

##### original residual at zero

169/1000

##### source

p.8 eq(29)

##### printed

Displayed mu second-order equation, alpha=-1,m=3

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### equation

30

#### page

8

#### description

Autonomous order reduction

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq30

#### detail

##### printed Mprime over M at sample

172/35

##### correct Mprime over M at sample

338/71

##### source

p.8 eq(30)

##### printed

Displayed M_Xi/M logarithmic derivative

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### status

refuted_as_printed

#### equation

31

#### page

8

#### description

Claimed explicit reduced solution

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq31

#### detail

##### printed M

```text
3*P**2*g*kappa/(P**3*(3*g*kappa + 1) + g)
```

##### d of correct integral dP at sample

960/8281

##### source

p.8 eq(31)

##### printed

Displayed complex-form M(Xi), real cubic slice M0=1

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### status

refuted_as_printed

#### equation

32

#### page

8

#### description

Claimed quadratic profile in subsection 3.8

#### evidence module

reductions

#### status

qualified

#### evidence

reductions.source_witnesses.eq32

#### detail

##### not necessary witness

phi=t+s+s^3/6 has p=1, q=1+s^2/2>0, E=0, but F_sss=1

##### source

p.8 eq(32)

##### printed

Quadratic F(s) is sufficient but not necessary for printed wrong 3.8 graph

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### printed quadratic is solution

True

##### quadratic residual

0

##### audit verified

True

##### status

qualified

#### equation

33

#### page

8

#### description

Shifted traveling-wave ODE

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq33

#### detail

##### printed H zero

-5/119

##### original residual at zero

40337/119000

##### source

p.8 eq(33)

##### printed

Mixed traveling expanded equation alpha=-1,alpha3=1,m=3

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### equation

34

#### page

9

#### description

Claimed implicit quadrature

#### evidence module

reductions

#### status

refuted_as_printed

#### evidence

reductions.source_witnesses.eq34

#### detail

##### literal implicit first derivative

D(z,P)*C-(P-1)-1=0, D=g/P^2-z+beta*g*(1+P)^2/P

##### literal implied C

10/69

##### literal implied H

60200/328509

##### original residual at implied jet

-118420/328509

##### correct integrand

g/tau^2-alpha^2*tau+beta*g*(alpha3-alpha*tau)^(m-1)/tau

##### note

Even corrected integrand with coefficient 1 fixes first-integral constant I=-1; general I0 must be retained.

##### source

p.9 eq(34)

##### printed

Literal -alpha^2*kappa in integrand; lower limit P0=1

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### status

refuted_as_printed

### tables

#### table

1

#### page

5

#### status

corrected

#### evidence

algebra.formulas.brackets; two source sign errors

#### table

2

#### page

5

#### status

verified

#### evidence

algebra.formulas.adjoints; convention exp(-epsilon ad)

#### table

3

#### page

6

#### status

qualified

#### evidence

recorded invariants verified; alpha=-1 requires a separate chart and the list omits other orbit families

### unnumbered claims

#### source

p.4 Proposition 1

#### status

corrected

#### evidence

symmetries.claims.maximal_classification; the m=1 stratum has X6=t*d_phi

#### source

p.4 printed determining system

#### status

refuted_as_printed

#### evidence

symmetries.discrepancies.printed_determining_X4_witness

#### source

pp.5-6 optimal system

#### status

corrected

#### evidence

algebra.formulas.orbits; missing projective/resonant families

#### source

p.7 reduced generators after (25) and (26)

#### status

corrected

#### printed

3*sigma*d_sigma+phi*d_sigma and 3*sigma*d_sigma-2*mu*d_sigma

#### derived

3*sigma*d_sigma+phi*d_phi and 3*sigma*d_sigma-2*mu*d_mu

#### evidence

X4(s*t^2)=3*s*t^2 and X4(phi)=phi; prolongation to mu=phi_sigma gives mu-3*mu=-2*mu.

#### source

p.8 eight-generator/free-particle statement

#### status

qualified

#### evidence

corrected traveling derivative ODE has invertible Y(P)=Integral(B(P),dP) on B!=0, giving Y_second=0

#### source

pp.7-8 shock/nonsingular descriptions

#### status

unsupported_as_global_claim

#### evidence

local smooth-profile checks do not establish weak shock balances or global absence of singularities

#### source

p.9 variational Lagrangian

#### status

author_reported_negative

#### evidence

authors report not finding a formulation; no nonexistence proof follows

#### source

p.9 initial-value discussion

#### status

source_text_inconsistent

#### evidence

conclusion both says IVP was examined and later says it was not discussed; paper supplies no numerical initial data

### inventory complete

True

### all printed claims reproduced

False

## [master equation]

### model

printed_scalar

### scope

Local smooth material chart q>0; noninteger powers on p>0; g,kappa>0; m>=1.

### master

```text
a*b + 2*b*c*g/q**3 - g*(b**2*kappa*m**2*p**m/(p**2*q) - b**2*kappa*m*p**m/(p**2*q) - b*c*kappa*m*p**m/(p*q**2) + kappa*m*p**m*x/(p*q)) - g*x/q**2 + q*r
```

### master latex

```text
a b + \frac{2 b c g}{q^{3}} - g \left(\frac{b^{2} \kappa m^{2} p^{m}}{p^{2} q} - \frac{b^{2} \kappa m p^{m}}{p^{2} q} - \frac{b c \kappa m p^{m}}{p q^{2}} + \frac{\kappa m p^{m} x}{p q}\right) - \frac{g x}{q^{2}} + q r
```

### beta

m*kappa

### checks

#### mass pullback zero

True

#### momentum pullback zero

True

#### printed compatibility zero

True

#### physical compatibility zero

True

### steps

#### label

Coordinate definitions

#### expression

x=phi(t,s), h=1/phi_s, u=phi_t, b(t,s)=B(t,phi(t,s))

#### label

Eulerian derivative operators

#### expression

D_x=(1/q)D_s; D_T=D_t-(p/q)D_s

#### label

Continuity pullback

#### expression

0

#### label

Momentum pullback

#### expression

```text
a + b_s*g/q - c*g/q**3
```

#### label

Exner pullback

#### expression

```text
b*kappa*m*p**(m - 1)/q - b_s*p/q + b_t
```

#### label

Printed Exner expression

#### expression

```text
b*kappa*m*p**(m - 1)/q + b_t
```

#### label

Missing term under the pullback interpretation

#### expression

-b_s*p/q

#### label

Define A

#### expression

```text
a*q - c*g/q**2
```

#### label

Printed b_s

#### expression

```text
(-a*q + c*g/q**2)/g
```

#### label

Printed b_t

#### expression

```text
-b*kappa*m*p**(m - 1)/q
```

#### label

Compatibility b_st-b_ts

#### expression

```text
-a*b/g + b**2*kappa*m**2*p**m/(p**2*q) - b**2*kappa*m*p**m/(p**2*q) - b*c*kappa*m*p**m/(p*q**2) - 2*b*c/q**3 + kappa*m*p**m*x/(p*q) + x/q**2 - q*r/g
```

#### label

Printed master equation E=0

#### expression

```text
a*b + 2*b*c*g/q**3 - g*(b**2*kappa*m**2*p**m/(p**2*q) - b**2*kappa*m*p**m/(p**2*q) - b*c*kappa*m*p**m/(p*q**2) + kappa*m*p**m*x/(p*q)) - g*x/q**2 + q*r
```

#### label

Advectively corrected compatibility equation

#### expression

```text
-b**2*g*kappa*m**2*p**m/(p**2*q) + b**2*g*kappa*m*p**m/(p**2*q) + b*c*g*kappa*m*p**m/(p*q**2) + 3*b*c*g/q**3 - 3*c**2*g*p/q**4 - g*kappa*m*p**m*x/(p*q) + g*p*y/q**3 - g*x/q**2 - p*w + q*r
```

### physical equals printed

False

### discrepancies

#### id

D-MODEL-06

#### source

p.2 equation (6)

#### printed

```text
b_t + beta*phi_t**(m-1)*phi_ts/phi_s = 0
```

#### derived

```text
b_t - (phi_t/phi_s)*b_s + beta*phi_t**(m-1)*phi_ts/phi_s = 0
```

#### witness

D_T B = b_t - (p/q)b_s; the missing contribution is -p*b_s/q.

#### status

corrected_under_declared_bed_pullback

#### qualification

No inference about an alternative undefined bed variable; source equation (7) is retained as the mathematical reproduction target.

### reconstruction

```text
On a simply connected regular patch, E=0 closes omega=b_t dt+b_s ds and reconstructs the printed bed b up to a constant. This does not repair the Eulerian physical pullback.
```

### lagrangian statement

```text
Lagrange coordinates describe material labels. The source says it could not find a variational Lagrangian; this is not a proof of nonexistence and no Noether argument is used.
```

## [infinitesimal generator]

### general point generator

X=tau(t,s,phi)*d_t+xi(t,s,phi)*d_s+eta(t,s,phi)*d_phi

### invariant graph characteristic

Q=eta-tau*phi_t-xi*phi_s

### prolongation recursion

eta_(J,i)=D_i eta_J-phi_(J,t)D_i tau-phi_(J,s)D_i xi

### criterion

pr^(3)X(E)=0 on E=0; a nonzero multiple of E is permitted off-shell.

## [Symmetries of the SVE Equation]

### scope

#### equation

printed scalar equation (7), not advectively corrected/full bed system

#### branch

p=phi_t>0, q=phi_s>0, g>0, kappa>0, m>=1

#### category

local smooth point generators; direct third-jet prolongation

#### source

Paliathanasis, Leon, Leach, Mathematics 14 (2026) 433, v3 PDF pp. 4-5

### claims

#### listed generators

##### status

proved_direct_identity

##### generic

X1

X2

X3

X4

##### m3 extra

X5

##### m1 extra not in source

X6=t*d_phi

#### maximal classification

##### status

proved_on_declared_branch

##### dimensions

###### m=1

5

###### m=3

5

###### m>=1,m!=1,3

4

##### category

unrestricted smooth local point generators on p,q>0; no singular p=0/q=0 branch

### formulas

#### E m

```text
a*b + 2*b*c*g/q**3 - g*(b**2*kappa*m**2*p**m/(p**2*q) - b**2*kappa*m*p**m/(p**2*q) - b*c*kappa*m*p**m/(p*q**2) + kappa*m*p**m*x/(p*q)) - g*x/q**2 + q*r
```

#### X5 defect

```text
b**2*g*kappa*m**3*p**m/(p**2*q) - 4*b**2*g*kappa*m**2*p**m/(p**2*q) + 3*b**2*g*kappa*m*p**m/(p**2*q) - b*c*g*kappa*m**2*p**m/(p*q**2) + 3*b*c*g*kappa*m*p**m/(p*q**2) + g*kappa*m**2*p**m*x/(p*q) - 3*g*kappa*m*p**m*x/(p*q)
```

#### X5 weight identity

pr3(X5)(E_m)+E_m=(3-m)*E_bedload

#### E bedload

```text
-g*(b**2*kappa*m**2*p**m/(p**2*q) - b**2*kappa*m*p**m/(p**2*q) - b*c*kappa*m*p**m/(p*q**2) + kappa*m*p**m*x/(p*q))
```

### checks

#### X1

##### multiplier

0

##### remainder

0

##### passed

True

##### status

exact_off_shell

#### X2

##### multiplier

0

##### remainder

0

##### passed

True

##### status

exact_off_shell

#### X3

##### multiplier

0

##### remainder

0

##### passed

True

##### status

exact_off_shell

#### X4

##### multiplier

-2

##### remainder

0

##### passed

True

##### status

exact_off_shell

#### X5

##### identity remainder

0

##### passed

True

##### m3 defect

0

##### m4 defect nonzero

True

##### status

exact_off_shell_weight_identity

#### X6 m1

##### remainder

0

##### passed

True

##### m2 nonzero

True

##### status

exact_off_shell

#### unrestricted determining split

##### passed

True

##### free y

###### coefficient

```text
g*(p*Derivative(xi(t, s, u), u) + Derivative(xi(t, s, u), t))*(kappa*m*p**m*q + p)/(p*q**2)
```

###### checked

True

###### consequence

xi_t=xi_u=0; common factor is positive on the branch

##### free w

###### coefficient

```text
2*g*(q*Derivative(tau(t, s, u), u) + Derivative(tau(t, s, u), s))*(kappa*m*p**m*q + p)/(p*q**2)
```

###### checked

True

###### consequence

tau_s=tau_u=0

##### free a b

###### coefficient

```text
-Derivative(eta(t, s, u), s)/q
```

###### checked

True

###### consequence

eta_s=0

##### free a

###### coefficient

```text
q*(4*p*Derivative(eta(t, u), (u, 2)) - 3*Derivative(tau(t), (t, 2)) + 4*Derivative(eta(t, u), t, u))
```

###### checked

True

###### consequence

eta=A(t)*u+B(t), 4*A_prime=3*tau_double_prime

##### free x

###### coefficient

```text
-g*(kappa*m*p**m*q*(p*(m - 3)*(A(t) - Derivative(tau(t), t)) + (m - 1)*(u*Derivative(A(t), t) + Derivative(B(t), t))) + p**2*(-3*A(t) + 2*Derivative(tau(t), t) + Derivative(xi(s), s)))/(p**2*q**2)
```

###### checked

True

###### consequence

2*tau_prime+xi_prime-3*A=0; (m-3)*p*(A-tau_prime)+(m-1)*(A_prime*u+B_prime)=0

##### m1 remaining residual

###### expression

```text
b*Derivative(B(t), (t, 2)) + q*Derivative(B(t), (t, 3))
```

###### checked

True

###### consequence

B_double_prime=0 by free b,q splitting

##### normal form

```text
(-a*b*p**4*q**3 + b**2*g*kappa*m*p**(m + 2)*q**2*(m - 1) - b*c*g*kappa*m*p**(m + 3)*q - 2*b*c*g*p**4 + g*kappa*m*p**(m + 3)*q**2*x + g*p**4*q*x)/(p**4*q**4)
```

### discrepancies

#### printed determining X4 witness

##### source

v3 PDF p. 4, displayed determining system: 3 eta1 + xi2_s + 2 xi1_t = 0

##### substitution

X4: eta1=1, xi2_s=1, xi1_t=1

##### value

6

##### status

refuted_as_printed

##### effect

The printed determining system cannot establish its Proposition 1 or maximality.

#### missing m1 generator

##### source

v3 PDF p. 4 Proposition 1: four for arbitrary m, fifth only m=3

##### counterexample

X6=t*d_phi at m=1; pr3(X6)(E_1)=0

##### status

refutes_source_maximal_count_at_m1

##### corrected dimension

5 on the declared positive branch

## [Commutators of the admitted Lie symmetries for the SVE equation]

Cubic stratum (the generic algebra is the X1--X4 block):

| [row, column] | X1 | X2 | X3 | X4 | X5 |
|---|---|---|---|---|---|
| X1 | 0 | 0 | 0 | 1 X1 | 1 X1 |
| X2 | 0 | 0 | 0 | 1 X2 | -2 X2 |
| X3 | 0 | 0 | 0 | 1 X3 | 0 |
| X4 | -1 X1 | -1 X2 | -1 X3 | 0 | 0 |
| X5 | -1 X1 | 2 X2 | 0 | 0 | 0 |

Endpoint m=1:

| [row, column] | X1 | X2 | X3 | X4 | X6 |
|---|---|---|---|---|---|
| X1 | 0 | 0 | 0 | 1 X1 | 1 X3 |
| X2 | 0 | 0 | 0 | 1 X2 | 0 |
| X3 | 0 | 0 | 0 | 1 X3 | 0 |
| X4 | -1 X1 | -1 X2 | -1 X3 | 0 | 0 |
| X6 | -1 X3 | 0 | 0 | 0 | 0 |

## [listed Lie symmetries]

### source four

X1=d_t; X2=d_s; X3=d_phi; X4=t*d_t+s*d_s+phi*d_phi

### source cubic extra

X5=t*d_t-2*s*d_s (m=3)

### additional verified endpoint

X6=t*d_phi (m=1)

### classification

#### listed generators

##### status

proved_direct_identity

##### generic

X1

X2

X3

X4

##### m3 extra

X5

##### m1 extra not in source

X6=t*d_phi

#### maximal classification

##### status

proved_on_declared_branch

##### dimensions

###### m=1

5

###### m=3

5

###### m>=1,m!=1,3

4

##### category

unrestricted smooth local point generators on p,q>0; no singular p=0/q=0 branch

### scope

#### equation

printed scalar equation (7), not advectively corrected/full bed system

#### branch

p=phi_t>0, q=phi_s>0, g>0, kappa>0, m>=1

#### category

local smooth point generators; direct third-jet prolongation

#### source

Paliathanasis, Leon, Leach, Mathematics 14 (2026) 433, v3 PDF pp. 4-5

## [One-Dimensional Optimal System]

### scope

#### source

v3 PDF pp. 4-6, Tables 1-2 and displayed one-dimensional system

#### convention

[A,B]=A(B)-B(A); Ad(exp(eps A))B=exp(-eps ad_A)B

#### generic basis

X1-X4 for m!=1,3

#### m3 basis

X1-X5

#### m1 basis

X1-X4 plus X6

#### equivalence

connected inner adjoint plus nonzero line rescaling

### claims

#### lie algebra

##### status

verified_for_listed_generators_only

#### source optimal system

##### status

refuted_incomplete

#### complete 1d classification

##### status

derived_connected_inner_adjoint_with_line_scaling_on_each_declared_stratum

### formulas

#### brackets

##### [X1,X1]


##### [X1,X2]


##### [X1,X3]


##### [X1,X4]

###### X1

1

##### [X1,X5]

###### X1

1

##### [X2,X1]


##### [X2,X2]


##### [X2,X3]


##### [X2,X4]

###### X2

1

##### [X2,X5]

###### X2

-2

##### [X3,X1]


##### [X3,X2]


##### [X3,X3]


##### [X3,X4]

###### X3

1

##### [X3,X5]


##### [X4,X1]

###### X1

-1

##### [X4,X2]

###### X2

-1

##### [X4,X3]

###### X3

-1

##### [X4,X4]


##### [X4,X5]


##### [X5,X1]

###### X1

-1

##### [X5,X2]

###### X2

2

##### [X5,X3]


##### [X5,X4]


##### [X5,X5]


#### adjoints

##### Ad(X1)X1

###### X1

1

##### Ad(X1)X2

###### X2

1

##### Ad(X1)X3

###### X3

1

##### Ad(X1)X4

###### X4

1

###### X1

-eps

##### Ad(X1)X5

###### X5

1

###### X1

-eps

##### Ad(X2)X1

###### X1

1

##### Ad(X2)X2

###### X2

1

##### Ad(X2)X3

###### X3

1

##### Ad(X2)X4

###### X4

1

###### X2

-eps

##### Ad(X2)X5

###### X5

1

###### X2

2*eps

##### Ad(X3)X1

###### X1

1

##### Ad(X3)X2

###### X2

1

##### Ad(X3)X3

###### X3

1

##### Ad(X3)X4

###### X4

1

###### X3

-eps

##### Ad(X3)X5

###### X5

1

##### Ad(X4)X1

###### X1

exp(eps)

##### Ad(X4)X2

###### X2

exp(eps)

##### Ad(X4)X3

###### X3

exp(eps)

##### Ad(X4)X4

###### X4

1

##### Ad(X4)X5

###### X5

1

##### Ad(X5)X1

###### X1

exp(eps)

##### Ad(X5)X2

###### X2

exp(-2*eps)

##### Ad(X5)X3

###### X3

1

##### Ad(X5)X4

###### X4

1

##### Ad(X5)X5

###### X5

1

#### m1 brackets

##### [X1,X1]


##### [X1,X2]


##### [X1,X3]


##### [X1,X4]

###### X1

1

##### [X1,X6]

###### X3

1

##### [X2,X1]


##### [X2,X2]


##### [X2,X3]


##### [X2,X4]

###### X2

1

##### [X2,X6]


##### [X3,X1]


##### [X3,X2]


##### [X3,X3]


##### [X3,X4]

###### X3

1

##### [X3,X6]


##### [X4,X1]

###### X1

-1

##### [X4,X2]

###### X2

-1

##### [X4,X3]

###### X3

-1

##### [X4,X4]


##### [X4,X6]


##### [X6,X1]

###### X3

-1

##### [X6,X2]


##### [X6,X3]


##### [X6,X4]


##### [X6,X6]


#### m1 adjoints

##### Ad(X1)X1

###### X1

1

##### Ad(X1)X2

###### X2

1

##### Ad(X1)X3

###### X3

1

##### Ad(X1)X4

###### X4

1

###### X1

-eps

##### Ad(X1)X6

###### X6

1

###### X3

-eps

##### Ad(X2)X1

###### X1

1

##### Ad(X2)X2

###### X2

1

##### Ad(X2)X3

###### X3

1

##### Ad(X2)X4

###### X4

1

###### X2

-eps

##### Ad(X2)X6

###### X6

1

##### Ad(X3)X1

###### X1

1

##### Ad(X3)X2

###### X2

1

##### Ad(X3)X3

###### X3

1

##### Ad(X3)X4

###### X4

1

###### X3

-eps

##### Ad(X3)X6

###### X6

1

##### Ad(X4)X1

###### X1

exp(eps)

##### Ad(X4)X2

###### X2

exp(eps)

##### Ad(X4)X3

###### X3

exp(eps)

##### Ad(X4)X4

###### X4

1

##### Ad(X4)X6

###### X6

1

##### Ad(X6)X1

###### X1

1

###### X3

eps

##### Ad(X6)X2

###### X2

1

##### Ad(X6)X3

###### X3

1

##### Ad(X6)X4

###### X4

1

##### Ad(X6)X6

###### X6

1

#### orbits

##### generic

###### translation projective dimension

2

###### reason

Ad(X4) rescales all X1,X2,X3 equally, hence fixes each translation line.

###### translation representatives

X1+a*X2+b*X3 (a,b real)

X2+a*X3 (a real)

X3

###### missing source family

X2+a*X3 (a nonzero), with projective parameter a

###### nontranslation line

X4 (translation terms removable)

##### exceptional

###### diagonal weights of ad aX4 bX5

###### X1

-(a+b)

###### X2

-(a-2b)

###### X3

-a

###### resonant directions

###### H

X5

###### survivor

X3

###### family

X5+c*X3

###### H

X4-X5

###### survivor

X1

###### family

X4-X5+c*X1

###### H

X4+(1/2)*X5

###### survivor

X2

###### family

X4+(1/2)*X5+c*X2

###### resonant c connected normal forms

0

+1

-1

###### translation line invariant

```text
I=a1**2*a2/a3**3 when a3!=0
```

###### translation invariant scope

Ad(X5) and nonzero line rescaling; support and relative signs require separate strata

###### translation representatives

X1

X2

X3

X1+sigma*X2

X3+sigma*X1

X3+sigma*X2

X3+sigma*X1+K*X2

###### translation parameters

sigma in {+1,-1}; K real nonzero; use only terms with their stated nonzero support

###### nontranslation representatives

H=aX4+bX5, (a:b) in RP1; at the three resonance directions add c*survivor, c=+1 or -1

###### equivalence test

```text
For translation coefficients v,w: w=lambda*(exp(eps)*v1, exp(-2eps)*v2, v3), lambda real nonzero; for H+v, H projective fixed and nonresonant v removed by translations.
```

###### source optimality status

refuted_incomplete

##### m1

###### basis

X1

X2

X3

X4

X6

###### adjoint elementary actions

Ad(exp(eps X1)): v1->v1-eps*h, v3->v3-eps*c

Ad(exp(eps X2)): v2->v2-eps*h

Ad(exp(eps X3)): v3->v3-eps*h

Ad(exp(eps X4)): (v1,v2,v3)->exp(eps)*(v1,v2,v3)

Ad(exp(eps X6)): v3->v3+eps*v1

###### coordinates

Z=v1*X1+v2*X2+v3*X3+h*X4+c*X6

###### representatives

X4+alpha*X6 (alpha real)

X6

X6+sigma*X1+a*X2 (sigma=+1 or -1, a real)

X6+sigma*X2 (sigma=+1 or -1)

X1+a*X2 (a real)

X2+a*X3 (a real)

X3

###### normalization

When c normalized to 1, X4 permits only positive common scaling of (v1,v2), so signs survive.

###### classification status

connected-adjoint orbit representatives on the m=1 five-generator algebra

#### orbit evidence kind

hand-derived classification using computed adjoint actions; not an automatic orbit-classification algorithm

### checks

#### antisymmetry

##### passed

25

##### total

25

#### jacobi

##### passed

125

##### total

125

#### m1 jacobi

##### passed

125

##### total

125

#### table 2

##### status

agrees

##### convention

negative ad

##### comparisons

###### Ad(X1)X1

###### passed

True

###### difference


###### Ad(X1)X2

###### passed

True

###### difference


###### Ad(X1)X3

###### passed

True

###### difference


###### Ad(X1)X4

###### passed

True

###### difference


###### Ad(X1)X5

###### passed

True

###### difference


###### Ad(X2)X1

###### passed

True

###### difference


###### Ad(X2)X2

###### passed

True

###### difference


###### Ad(X2)X3

###### passed

True

###### difference


###### Ad(X2)X4

###### passed

True

###### difference


###### Ad(X2)X5

###### passed

True

###### difference


###### Ad(X3)X1

###### passed

True

###### difference


###### Ad(X3)X2

###### passed

True

###### difference


###### Ad(X3)X3

###### passed

True

###### difference


###### Ad(X3)X4

###### passed

True

###### difference


###### Ad(X3)X5

###### passed

True

###### difference


###### Ad(X4)X1

###### passed

True

###### difference


###### Ad(X4)X2

###### passed

True

###### difference


###### Ad(X4)X3

###### passed

True

###### difference


###### Ad(X4)X4

###### passed

True

###### difference


###### Ad(X4)X5

###### passed

True

###### difference


###### Ad(X5)X1

###### passed

True

###### difference


###### Ad(X5)X2

###### passed

True

###### difference


###### Ad(X5)X3

###### passed

True

###### difference


###### Ad(X5)X4

###### passed

True

###### difference


###### Ad(X5)X5

###### passed

True

###### difference


### discrepancies

#### table 1

##### wrong cells

[X5,X1]

[X5,X2]

##### source values

+X1

-2X2

##### correct values

-X1

+2X2

##### proof

antisymmetry and direct coordinate-vector bracket

#### one dimensional list

##### status

refuted_incomplete

##### generic missing

X2+aX3 for a!=0; X4 acts only by common rescaling on translation lines

##### m3 missing

X5+cX3

X4-X5+cX1

X4+(1/2)X5+cX2

##### qualification

c!=0 witnesses cannot be removed by connected inner adjoint; sign and support strata require explicit tracking

#### m1 missing generator

##### source

v3 PDF p. 4 Proposition 1 and pp. 5-6 Tables 1-2/list, all omitting m=1 stratum

##### generator

X6=t*d_phi

##### new bracket

[X1,X6]=X3

##### effect

At m=1 the listed four-dimensional algebra is a proper subalgebra; its optimal list cannot be complete.

## [Similarity Transformations]

### lagrangian statement

```text
Lagrange coordinates describe material labels. The source says it could not find a variational Lagrangian; this is not a proof of nonexistence and no Noether argument is used.
```

### method

```text
Solve Q=0, verify invariant chart, substitute every jet into original E. Dimension reduction and subsequent ODE order reduction are distinct.
```

### details

See the per-case steps and further-reduction evidence below.

## [One dimensional optimal system and Lie invariants Table]

| Source row | Invariant coordinate | Invariant graph (F is evaluated at that coordinate) | Outcome |
|---|---|---|---|
| 3.1 | `s` | `F` | identity |
| 3.2 | `t` | `F` | undefined |
| 3.3 | `['t', 's']` | `None` | no_invariant_graph |
| 3.4 | `s/t` | `F*t` | regular_ode |
| 3.5 | `s*t**2` | `F` | regular_ode |
| 3.6 | `s + t` | `F` | regular_ode |
| 3.7 | `s` | `F + t` | identity |
| 3.8 | `t` | `F + s` | regular_ode |
| 3.9 | `s + t` | `F + t` | regular_ode |
| table3-mixed | `s/t**(2/5)` | `F*t**(4/5)` | regular_ode |

## [Solution ODE with all 9 reductions]

### cases

#### id

3.1

#### status

identity

#### coordinate

s

#### ansatz

F

#### residual

0

#### leading

0

#### rhs

Not applicable / not supplied.

#### velocity

0

#### gradient

P

#### ode order

0

#### steps

##### label

generator

##### expression

d_t

##### label

Q=0

##### expression

phi_t=0

##### label

jets

##### expression

phi=F(s), phi_t=phi_ts=phi_tt=0; phi_s=P, phi_ss=C, phi_sss=H

##### label

PDE pullback

##### expression

0

#### guards

P>0

velocity=0 is outside the positive-velocity chart

#### source equations

Table 3

3.1

#### id

3.2

#### status

undefined

#### coordinate

t

#### ansatz

F

#### residual

Not applicable / not supplied.

#### leading

Not applicable / not supplied.

#### rhs

Not applicable / not supplied.

#### velocity

P

#### gradient

0

#### ode order

Not applicable / not supplied.

#### steps

##### label

generator

##### expression

d_s

##### label

Q=0

##### expression

phi_s=0

##### label

jets

##### expression

phi=F(t), phi_t=P, phi_tt=C, phi_ttt=H; phi_s=phi_ts=phi_ss=0

##### label

denominator

##### expression

phi_s^2=0

#### guards

phi_s=0 violates the PDE domain

#### source equations

Table 3

3.2

#### id

3.3

#### status

no_invariant_graph

#### coordinate

t

s

#### ansatz

Not applicable / not supplied.

#### residual

Not applicable / not supplied.

#### leading

Not applicable / not supplied.

#### rhs

Not applicable / not supplied.

#### velocity

Not applicable / not supplied.

#### gradient

Not applicable / not supplied.

#### ode order

Not applicable / not supplied.

#### steps

##### label

generator

##### expression

d_phi

##### label

Q=0

##### expression

1=0

#### guards

vertical orbit has no invariant graph

#### source equations

Table 3

3.3

#### id

3.4

#### status

regular_ode

#### coordinate

s/t

#### ansatz

F*t

#### residual

```text
(-3*C**2*F**2*P*g*kappa*z + 3*C**2*P**3*g*kappa*z**3 - C**2*P**3*z**3 - 2*C**2*g*z + 3*C*F**2*P**2*g*kappa - 6*C*F*P**3*g*kappa*z + 3*C*P**4*g*kappa*z**2 - 3*C*P**4*z**2 + C*P*g + 3*F**2*H*P**2*g*kappa*z - 6*F*H*P**3*g*kappa*z**2 + 3*H*P**4*g*kappa*z**3 - H*P**4*z**3 + H*P*g*z)/P**3
```

#### leading

```text
z*(3*F**2*P*g*kappa - 6*F*P**2*g*kappa*z + 3*P**3*g*kappa*z**2 - P**3*z**2 + g)/P**2
```

#### rhs

```text
(3*C**2*F**2*P*g*kappa*z - 3*C**2*P**3*g*kappa*z**3 + C**2*P**3*z**3 + 2*C**2*g*z - 3*C*F**2*P**2*g*kappa + 6*C*F*P**3*g*kappa*z - 3*C*P**4*g*kappa*z**2 + 3*C*P**4*z**2 - C*P*g)/(3*F**2*P**2*g*kappa*z - 6*F*P**3*g*kappa*z**2 + 3*P**4*g*kappa*z**3 - P**4*z**3 + P*g*z)
```

#### velocity

F - P*z

#### gradient

P

#### ode order

3

#### steps

##### label

generator

##### expression

X=t d_t + (1) s d_s + (1) phi d_phi (rescaled)

##### label

invariant graph equation Q

##### expression

0

##### label

invariant coordinate

##### expression

s/t

##### label

invariant graph Q=0

##### expression

F*t

##### label

phi_t at t=1

##### expression

F - P*z

##### label

phi_s at t=1

##### expression

P

##### label

phi_tt at t=1

##### expression

```text
C*z**2
```

##### label

phi_ts at t=1

##### expression

-C*z

##### label

phi_ss at t=1

##### expression

C

##### label

phi_ttt at t=1

##### expression

```text
-C*z**2 - z*(2*C*z + H*z**2)
```

##### label

phi_tts at t=1

##### expression

```text
2*C*z + H*z**2
```

##### label

phi_tss at t=1

##### expression

-C - H*z

##### label

phi_sss at t=1

##### expression

H

##### label

inertial current profile

##### expression

```text
C*P*z**2 - C*g/P**2
```

##### label

sediment flux profile

##### expression

```text
-3*C*kappa*z*(F - P*z)**2/P
```

##### label

PDE pullback multiplier

##### expression

```text
t**(-2)
```

##### label

reduced residual

##### expression

```text
(-3*C**2*F**2*P*g*kappa*z + 3*C**2*P**3*g*kappa*z**3 - C**2*P**3*z**3 - 2*C**2*g*z + 3*C*F**2*P**2*g*kappa - 6*C*F*P**3*g*kappa*z + 3*C*P**4*g*kappa*z**2 - 3*C*P**4*z**2 + C*P*g + 3*F**2*H*P**2*g*kappa*z - 6*F*H*P**3*g*kappa*z**2 + 3*H*P**4*g*kappa*z**3 - H*P**4*z**3 + H*P*g*z)/P**3
```

##### label

first-integral density

##### expression

```text
C*z*(3*F**2*P*g*kappa - 6*F*P**2*g*kappa*z + 3*P**3*g*kappa*z**2 - P**3*z**2 + g)/P**2
```

#### guards

t>0

profile gradient P>0

profile velocity A*F+B*z*P>0

highest-derivative coefficient nonzero

#### source equations

(24)

#### id

3.5

#### status

regular_ode

#### coordinate

```text
s*t**2
```

#### ansatz

F

#### residual

```text
-2*z*(12*C**2*P**3*g*kappa*z**2 - 4*C**2*P**3*z**2 - 2*C**2*g + 60*C*P**4*g*kappa*z - 12*C*P**4*z + 12*H*P**4*g*kappa*z**2 - 4*H*P**4*z**2 + H*P*g + 24*P**5*g*kappa - 2*P**5)/P**3
```

#### leading

```text
-2*z*(12*P**3*g*kappa*z**2 - 4*P**3*z**2 + g)/P**2
```

#### rhs

```text
(-12*C**2*P**3*g*kappa*z**2 + 4*C**2*P**3*z**2 + 2*C**2*g - 60*C*P**4*g*kappa*z + 12*C*P**4*z - 24*P**5*g*kappa + 2*P**5)/(12*P**4*g*kappa*z**2 - 4*P**4*z**2 + P*g)
```

#### velocity

2*P*z

#### gradient

P

#### ode order

3

#### steps

##### label

generator

##### expression

X=t d_t + (-2) s d_s + (0) phi d_phi (rescaled)

##### label

invariant graph equation Q

##### expression

0

##### label

invariant coordinate

##### expression

```text
s*t**2
```

##### label

invariant graph Q=0

##### expression

F

##### label

phi_t at t=1

##### expression

2*P*z

##### label

phi_s at t=1

##### expression

P

##### label

phi_tt at t=1

##### expression

-2*P*z + 2*z*(2*C*z + 2*P)

##### label

phi_ts at t=1

##### expression

2*C*z + 2*P

##### label

phi_ss at t=1

##### expression

C

##### label

phi_ttt at t=1

##### expression

```text
4*P*z - 4*z*(2*C*z + 2*P) + 2*z*(10*C*z + 4*H*z**2 + 2*P)
```

##### label

phi_tts at t=1

##### expression

```text
10*C*z + 4*H*z**2 + 2*P
```

##### label

phi_tss at t=1

##### expression

4*C + 2*H*z

##### label

phi_sss at t=1

##### expression

H

##### label

inertial current profile

##### expression

```text
-C*g/P**2 + P*(-2*P*z + 2*z*(2*C*z + 2*P))
```

##### label

sediment flux profile

##### expression

```text
12*P*kappa*z**2*(2*C*z + 2*P)
```

##### label

PDE pullback multiplier

##### expression

1/t

##### label

reduced residual

##### expression

```text
-2*z*(12*C**2*P**3*g*kappa*z**2 - 4*C**2*P**3*z**2 - 2*C**2*g + 60*C*P**4*g*kappa*z - 12*C*P**4*z + 12*H*P**4*g*kappa*z**2 - 4*H*P**4*z**2 + H*P*g + 24*P**5*g*kappa - 2*P**5)/P**3
```

#### guards

t>0

profile gradient P>0

profile velocity A*F+B*z*P>0

highest-derivative coefficient nonzero

#### source equations

(25)-(27)

#### id

3.6

#### status

regular_ode

#### coordinate

s + t

#### ansatz

F

#### residual

```text
-(3*C**2*P**3*g*kappa - C**2*P**3 - 2*C**2*g + 3*H*P**4*g*kappa - H*P**4 + H*P*g)/P**3
```

#### leading

```text
-(3*P**3*g*kappa - P**3 + g)/P**2
```

#### rhs

```text
(-3*C**2*P**3*g*kappa + C**2*P**3 + 2*C**2*g)/(3*P**4*g*kappa - P**4 + P*g)
```

#### velocity

P

#### gradient

P

#### ode order

3

#### steps

##### label

generator

##### expression

d_t+(-1)d_s+(0)d_phi

##### label

invariant coordinate

##### expression

s + t

##### label

invariant graph Q=0

##### expression

F

##### label

phi

##### expression

F

##### label

phi_t

##### expression

P

##### label

phi_s

##### expression

P

##### label

phi_tt

##### expression

C

##### label

phi_ts

##### expression

C

##### label

phi_ss

##### expression

C

##### label

phi_ttt

##### expression

H

##### label

phi_tts

##### expression

H

##### label

phi_tss

##### expression

H

##### label

phi_sss

##### expression

H

##### label

inertial current

##### expression

```text
C*(P - g/P**2)
```

##### label

sediment flux

##### expression

3*C*P*kappa

##### label

PDE pullback multiplier

##### expression

1

##### label

first-integral density

##### expression

```text
-C*(3*P**3*g*kappa - P**3 + g)/P**2
```

##### label

reduced residual

##### expression

```text
C*(-C*(9*P**2*g*kappa - 3*P**2)/P**2 + 2*C*(3*P**3*g*kappa - P**3 + g)/P**3) - H*(3*P**3*g*kappa - P**3 + g)/P**2
```

#### guards

P>0

alpha3-alpha*P>0

alpha!=0

highest-derivative coefficient nonzero

#### source equations

(28)

(29)-(31)

#### id

3.7

#### status

identity

#### coordinate

s

#### ansatz

F + t

#### residual

0

#### leading

0

#### rhs

Not applicable / not supplied.

#### velocity

1

#### gradient

P

#### ode order

0

#### steps

##### label

generator

##### expression

d_t+(1)d_phi

##### label

Q=0

##### expression

phi_t=alpha

##### label

jets

##### expression

phi_t=alpha, phi_s=P, phi_ss=C; all mixed and higher time jets vanish

##### label

PDE pullback

##### expression

0

#### guards

P>0

alpha>0 for positive-velocity chart

#### source equations

3.7

#### id

3.8

#### status

regular_ode

#### coordinate

t

#### ansatz

F + s

#### residual

H

#### leading

1

#### rhs

0

#### velocity

P

#### gradient

1

#### ode order

3

#### steps

##### label

generator

##### expression

d_s+(1)d_phi

##### label

Q=0

##### expression

phi_s=alpha

##### label

jets

##### expression

phi_t=P, phi_s=alpha, phi_tt=C, phi_ttt=H; all s-derivatives of order >=2 and mixed jets vanish

##### label

PDE pullback

##### expression

H

#### guards

alpha>0

P>0

alpha!=0

#### source equations

(32)

#### id

3.9

#### status

regular_ode

#### coordinate

s + t

#### ansatz

F + t

#### residual

```text
-(3*C**2*P**3*g*kappa - C**2*P**3 - 3*C**2*P*g*kappa - 2*C**2*g + 3*H*P**4*g*kappa - H*P**4 + 6*H*P**3*g*kappa + 3*H*P**2*g*kappa + H*P*g)/P**3
```

#### leading

```text
-(3*P**3*g*kappa - P**3 + 6*P**2*g*kappa + 3*P*g*kappa + g)/P**2
```

#### rhs

```text
(-3*C**2*P**3*g*kappa + C**2*P**3 + 3*C**2*P*g*kappa + 2*C**2*g)/(3*P**4*g*kappa - P**4 + 6*P**3*g*kappa + 3*P**2*g*kappa + P*g)
```

#### velocity

P + 1

#### gradient

P

#### ode order

3

#### steps

##### label

generator

##### expression

d_t+(-1)d_s+(1)d_phi

##### label

invariant coordinate

##### expression

s + t

##### label

invariant graph Q=0

##### expression

F + t

##### label

phi

##### expression

F + t

##### label

phi_t

##### expression

P + 1

##### label

phi_s

##### expression

P

##### label

phi_tt

##### expression

C

##### label

phi_ts

##### expression

C

##### label

phi_ss

##### expression

C

##### label

phi_ttt

##### expression

H

##### label

phi_tts

##### expression

H

##### label

phi_tss

##### expression

H

##### label

phi_sss

##### expression

H

##### label

inertial current

##### expression

```text
C*(P - g/P**2)
```

##### label

sediment flux

##### expression

```text
3*C*kappa*(P + 1)**2/P
```

##### label

PDE pullback multiplier

##### expression

1

##### label

first-integral density

##### expression

```text
-C*(3*P**3*g*kappa - P**3 + 6*P**2*g*kappa + 3*P*g*kappa + g)/P**2
```

##### label

reduced residual

##### expression

```text
C*(-C*(9*P**2*g*kappa - 3*P**2 + 12*P*g*kappa + 3*g*kappa)/P**2 + 2*C*(3*P**3*g*kappa - P**3 + 6*P**2*g*kappa + 3*P*g*kappa + g)/P**3) - H*(3*P**3*g*kappa - P**3 + 6*P**2*g*kappa + 3*P*g*kappa + g)/P**2
```

#### guards

P>0

alpha3-alpha*P>0

alpha!=0

highest-derivative coefficient nonzero

#### source equations

(33)

(34)

### table3 mixed

#### id

table3-mixed

#### status

regular_ode

#### coordinate

```text
s/t**(2/5)
```

#### ansatz

```text
F*t**(4/5)
```

#### residual

```text
2*(-48*C**2*F**2*P*g*kappa*z + 12*C**2*P**3*g*kappa*z**3 - 4*C**2*P**3*z**3 - 50*C**2*g*z + 48*C*F**2*P**2*g*kappa + 48*C*F*P**3*g*kappa*z + 4*C*F*P**3*z - 36*C*P**4*g*kappa*z**2 - 12*C*P**4*z**2 + 50*C*P*g + 48*F**2*H*P**2*g*kappa*z - 48*F*H*P**3*g*kappa*z**2 - 48*F*P**4*g*kappa + 8*F*P**4 + 12*H*P**4*g*kappa*z**3 - 4*H*P**4*z**3 + 25*H*P*g*z + 24*P**5*g*kappa*z + 10*P**5*z)/(125*P**3)
```

#### leading

```text
2*z*(48*F**2*P*g*kappa - 48*F*P**2*g*kappa*z + 12*P**3*g*kappa*z**2 - 4*P**3*z**2 + 25*g)/(125*P**2)
```

#### rhs

```text
(48*C**2*F**2*P*g*kappa*z - 12*C**2*P**3*g*kappa*z**3 + 4*C**2*P**3*z**3 + 50*C**2*g*z - 48*C*F**2*P**2*g*kappa - 48*C*F*P**3*g*kappa*z - 4*C*F*P**3*z + 36*C*P**4*g*kappa*z**2 + 12*C*P**4*z**2 - 50*C*P*g + 48*F*P**4*g*kappa - 8*F*P**4 - 24*P**5*g*kappa*z - 10*P**5*z)/(48*F**2*P**2*g*kappa*z - 48*F*P**3*g*kappa*z**2 + 12*P**4*g*kappa*z**3 - 4*P**4*z**3 + 25*P*g*z)
```

#### velocity

4*F/5 - 2*P*z/5

#### gradient

P

#### ode order

3

#### steps

##### label

generator

##### expression

X=t d_t + (2/5) s d_s + (4/5) phi d_phi (rescaled)

##### label

invariant graph equation Q

##### expression

0

##### label

invariant coordinate

##### expression

```text
s/t**(2/5)
```

##### label

invariant graph Q=0

##### expression

```text
F*t**(4/5)
```

##### label

phi_t at t=1

##### expression

4*F/5 - 2*P*z/5

##### label

phi_s at t=1

##### expression

P

##### label

phi_tt at t=1

##### expression

-4*F/25 + 2*P*z/25 - 2*z*(-2*C*z/5 + 2*P/5)/5

##### label

phi_ts at t=1

##### expression

-2*C*z/5 + 2*P/5

##### label

phi_ss at t=1

##### expression

C

##### label

phi_ttt at t=1

##### expression

```text
24*F/125 - 12*P*z/125 + 12*z*(-2*C*z/5 + 2*P/5)/25 - 2*z*(6*C*z/25 + 4*H*z**2/25 - 6*P/25)/5
```

##### label

phi_tts at t=1

##### expression

```text
6*C*z/25 + 4*H*z**2/25 - 6*P/25
```

##### label

phi_tss at t=1

##### expression

-2*H*z/5

##### label

phi_sss at t=1

##### expression

H

##### label

inertial current profile

##### expression

```text
-C*g/P**2 + P*(-4*F/25 + 2*P*z/25 - 2*z*(-2*C*z/5 + 2*P/5)/5)
```

##### label

sediment flux profile

##### expression

```text
3*kappa*(4*F/5 - 2*P*z/5)**2*(-2*C*z/5 + 2*P/5)/P
```

##### label

PDE pullback multiplier

##### expression

```text
t**(-9/5)
```

##### label

reduced residual

##### expression

```text
2*(-48*C**2*F**2*P*g*kappa*z + 12*C**2*P**3*g*kappa*z**3 - 4*C**2*P**3*z**3 - 50*C**2*g*z + 48*C*F**2*P**2*g*kappa + 48*C*F*P**3*g*kappa*z + 4*C*F*P**3*z - 36*C*P**4*g*kappa*z**2 - 12*C*P**4*z**2 + 50*C*P*g + 48*F**2*H*P**2*g*kappa*z - 48*F*H*P**3*g*kappa*z**2 - 48*F*P**4*g*kappa + 8*F*P**4 + 12*H*P**4*g*kappa*z**3 - 4*H*P**4*z**3 + 25*H*P*g*z + 24*P**5*g*kappa*z + 10*P**5*z)/(125*P**3)
```

#### guards

t>0

profile gradient P>0

profile velocity A*F+B*z*P>0

highest-derivative coefficient nonzero

#### source equations

Table 3

### checks

#### passed

True

#### direct graph checks

##### case

3.1

##### m

3

##### status

identity

##### graph condition

0

##### direct pullback

0

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.2

##### m

3

##### status

undefined_chart

##### gradient

0

##### graph condition

0

##### passed

True

##### case

3.3

##### m

3

##### status

no_invariant_graph

##### graph condition

1

##### passed

True

##### case

3.4

##### m

1

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-(C**2*P**3*z**3 + C**2*P*g*kappa*z + 2*C**2*g*z + 3*C*P**4*z**2 - C*P**2*g*kappa - C*P*g + H*P**4*z**3 - H*P**2*g*kappa*z - H*P*g*z)/(P**3*T**2)
```

##### pullback multiplier

```text
T**(-2)
```

##### difference

0

##### passed

True

##### case

3.4

##### m

3/2

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-(6*C**2*F*P*g*kappa*z + 4*C**2*P**3*z**3*sqrt(F - P*z) - 3*C**2*P**2*g*kappa*z**2 + 8*C**2*g*z*sqrt(F - P*z) - 6*C*F*P**2*g*kappa + 12*C*P**4*z**2*sqrt(F - P*z) + 6*C*P**3*g*kappa*z - 4*C*P*g*sqrt(F - P*z) - 6*F*H*P**2*g*kappa*z + 4*H*P**4*z**3*sqrt(F - P*z) + 6*H*P**3*g*kappa*z**2 - 4*H*P*g*z*sqrt(F - P*z))/(4*P**3*T**2*sqrt(F - P*z))
```

##### pullback multiplier

```text
T**(-2)
```

##### difference

0

##### passed

True

##### case

3.4

##### m

2

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-(2*C**2*F*P*g*kappa*z + C**2*P**3*z**3 + 2*C**2*g*z - 2*C*F*P**2*g*kappa + 3*C*P**4*z**2 + 2*C*P**3*g*kappa*z - C*P*g - 2*F*H*P**2*g*kappa*z + H*P**4*z**3 + 2*H*P**3*g*kappa*z**2 - H*P*g*z)/(P**3*T**2)
```

##### pullback multiplier

```text
T**(-2)
```

##### difference

0

##### passed

True

##### case

3.4

##### m

3

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
(-3*C**2*F**2*P*g*kappa*z + 3*C**2*P**3*g*kappa*z**3 - C**2*P**3*z**3 - 2*C**2*g*z + 3*C*F**2*P**2*g*kappa - 6*C*F*P**3*g*kappa*z + 3*C*P**4*g*kappa*z**2 - 3*C*P**4*z**2 + C*P*g + 3*F**2*H*P**2*g*kappa*z - 6*F*H*P**3*g*kappa*z**2 + 3*H*P**4*g*kappa*z**3 - H*P**4*z**3 + H*P*g*z)/(P**3*T**2)
```

##### pullback multiplier

```text
T**(-2)
```

##### difference

0

##### passed

True

##### case

3.4

##### m

4

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-(4*C**2*F**3*P*g*kappa*z - 12*C**2*F*P**3*g*kappa*z**3 + 8*C**2*P**4*g*kappa*z**4 + C**2*P**3*z**3 + 2*C**2*g*z - 4*C*F**3*P**2*g*kappa + 12*C*F**2*P**3*g*kappa*z - 12*C*F*P**4*g*kappa*z**2 + 4*C*P**5*g*kappa*z**3 + 3*C*P**4*z**2 - C*P*g - 4*F**3*H*P**2*g*kappa*z + 12*F**2*H*P**3*g*kappa*z**2 - 12*F*H*P**4*g*kappa*z**3 + 4*H*P**5*g*kappa*z**4 + H*P**4*z**3 - H*P*g*z)/(P**3*T**2)
```

##### pullback multiplier

```text
T**(-2)
```

##### difference

0

##### passed

True

##### case

3.5

##### m

3

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-2*z*(12*C**2*P**3*g*kappa*z**2 - 4*C**2*P**3*z**2 - 2*C**2*g + 60*C*P**4*g*kappa*z - 12*C*P**4*z + 12*H*P**4*g*kappa*z**2 - 4*H*P**4*z**2 + H*P*g + 24*P**5*g*kappa - 2*P**5)/(P**3*T)
```

##### pullback multiplier

1/T

##### difference

0

##### passed

True

##### case

3.6

##### m

1

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
(C**2*P**3 + C**2*P*g*kappa + 2*C**2*g + H*P**4 - H*P**2*g*kappa - H*P*g)/P**3
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.6

##### m

3/2

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
(4*C**2*P**(9/2) + 8*C**2*P**(3/2)*g + 3*C**2*P**3*g*kappa + 4*H*P**(11/2) - 4*H*P**(5/2)*g - 6*H*P**4*g*kappa)/(4*P**(9/2))
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.6

##### m

2

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
(C**2*P**3 + 2*C**2*g + H*P**4 - 2*H*P**3*g*kappa - H*P*g)/P**3
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.6

##### m

3

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-(3*C**2*P**3*g*kappa - C**2*P**3 - 2*C**2*g + 3*H*P**4*g*kappa - H*P**4 + H*P*g)/P**3
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.6

##### m

4

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-(8*C**2*P**4*g*kappa - C**2*P**3 - 2*C**2*g + 4*H*P**5*g*kappa - H*P**4 + H*P*g)/P**3
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.7

##### m

3

##### status

identity

##### graph condition

0

##### direct pullback

0

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.8

##### m

1

##### status

regular_ode

##### graph condition

0

##### direct pullback

H

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.8

##### m

3/2

##### status

regular_ode

##### graph condition

0

##### direct pullback

H

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.8

##### m

2

##### status

regular_ode

##### graph condition

0

##### direct pullback

H

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.8

##### m

3

##### status

regular_ode

##### graph condition

0

##### direct pullback

H

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.8

##### m

4

##### status

regular_ode

##### graph condition

0

##### direct pullback

H

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.9

##### m

1

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
(C**2*P**3 + C**2*P*g*kappa + 2*C**2*g + H*P**4 - H*P**2*g*kappa - H*P*g)/P**3
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.9

##### m

3/2

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
(4*C**2*P**3*sqrt(P + 1) + 3*C**2*P**2*g*kappa + 6*C**2*P*g*kappa + 8*C**2*g*sqrt(P + 1) + 4*H*P**4*sqrt(P + 1) - 6*H*P**3*g*kappa - 6*H*P**2*g*kappa - 4*H*P*g*sqrt(P + 1))/(4*P**3*sqrt(P + 1))
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.9

##### m

2

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
(C**2*P**3 + 2*C**2*P*g*kappa + 2*C**2*g + H*P**4 - 2*H*P**3*g*kappa - 2*H*P**2*g*kappa - H*P*g)/P**3
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.9

##### m

3

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-(3*C**2*P**3*g*kappa - C**2*P**3 - 3*C**2*P*g*kappa - 2*C**2*g + 3*H*P**4*g*kappa - H*P**4 + 6*H*P**3*g*kappa + 3*H*P**2*g*kappa + H*P*g)/P**3
```

##### pullback multiplier

1

##### difference

0

##### passed

True

##### case

3.9

##### m

4

##### status

regular_ode

##### graph condition

0

##### direct pullback

```text
-(8*C**2*P**4*g*kappa + 12*C**2*P**3*g*kappa - C**2*P**3 - 4*C**2*P*g*kappa - 2*C**2*g + 4*H*P**5*g*kappa + 12*H*P**4*g*kappa - H*P**4 + 12*H*P**3*g*kappa + 4*H*P**2*g*kappa + H*P*g)/P**3
```

##### pullback multiplier

1

##### difference

0

##### passed

True

#### first integral checks

##### 3.4

###### difference

0

###### passed

True

###### scope

symbolic m; traveling alpha=-1 and declared alpha3

##### 3.6

###### difference

0

###### passed

True

###### scope

symbolic m; traveling alpha=-1 and declared alpha3

##### 3.9

###### difference

0

###### passed

True

###### scope

symbolic m; traveling alpha=-1 and declared alpha3

### exact certificates

#### common scaling

##### I

```text
-C*z*(P**3*z**2 - P*g*kappa*m*(F - P*z)**(m - 1) - g)/P**2
```

##### dI

```text
-(-C**2*F*P**3*z**3 - C**2*F*P*g*kappa*m*z*(F - P*z)**(m - 1) - 2*C**2*F*g*z + C**2*P**4*z**4 - C**2*P**2*g*kappa*m**2*z**2*(F - P*z)**(m - 1) + 2*C**2*P**2*g*kappa*m*z**2*(F - P*z)**(m - 1) + 2*C**2*P*g*z**2 - 3*C*F*P**4*z**2 + C*F*P**2*g*kappa*m*(F - P*z)**(m - 1) + C*F*P*g + 3*C*P**5*z**3 - C*P**3*g*kappa*m*z*(F - P*z)**(m - 1) - C*P**2*g*z - F*H*P**4*z**3 + F*H*P**2*g*kappa*m*z*(F - P*z)**(m - 1) + F*H*P*g*z + H*P**5*z**4 - H*P**3*g*kappa*m*z**2*(F - P*z)**(m - 1) - H*P**2*g*z**2)/(P**3*(-F + P*z))
```

##### domain

z>0, P>0, F-z*P>0; all real m; I is constant on reduced solutions

#### traveling 3 6

##### B

```text
-(3*P**3*g*kappa - P**3 + g)/P**2
```

##### I

```text
-C*(3*P**3*g*kappa - P**3 + g)/P**2
```

##### dI

```text
-(3*C**2*P**3*g*kappa - C**2*P**3 - 2*C**2*g + 3*H*P**4*g*kappa - H*P**4 + H*P*g)/P**3
```

##### linearization

Y(P)=Integral(B(P),dP); Y(z) is affine if B(P)!=0

##### quadrature

z-z0=(Integral(B(P),dP)-Y0)/I0 for I0!=0; I0=0 implies P constant on B!=0 chart

##### domain

P>0, alpha3-alpha*P>0, alpha!=0, B(P)!=0

#### traveling 3 9

##### B

```text
-(3*P**3*g*kappa - P**3 + 6*P**2*g*kappa + 3*P*g*kappa + g)/P**2
```

##### I

```text
-C*(3*P**3*g*kappa - P**3 + 6*P**2*g*kappa + 3*P*g*kappa + g)/P**2
```

##### dI

```text
-(3*C**2*P**3*g*kappa - C**2*P**3 - 3*C**2*P*g*kappa - 2*C**2*g + 3*H*P**4*g*kappa - H*P**4 + 6*H*P**3*g*kappa + 3*H*P**2*g*kappa + H*P*g)/P**3
```

##### linearization

Y(P)=Integral(B(P),dP); Y(z) is affine if B(P)!=0

##### quadrature

z-z0=(Integral(B(P),dP)-Y0)/I0 for I0!=0; I0=0 implies P constant on B!=0 chart

##### domain

P>0, alpha3-alpha*P>0, alpha!=0, B(P)!=0

#### cubic power law

##### profile

```text
A*z**(1/3)
```

##### condition printed

```text
12*A**3*g*kappa - A**3 + 27*g
```

##### x4 residual

```text
-4*(12*A**3*g*kappa - A**3 + 27*g)/(81*A*z**(1/3))
```

##### x5 residual

```text
-4*(12*A**3*g*kappa - A**3 + 27*g)/(81*A*z**(1/3))
```

##### x4 leading

```text
z**(7/3)*(12*A**3*g*kappa - A**3 + 27*g)/(3*A**2)
```

##### x5 leading

```text
-2*z**(7/3)*(12*A**3*g*kappa - 4*A**3 + 27*g)/(3*A**2)
```

##### domain

z>0, A>0, g>0, kappa>0; x4 normal-form coefficient vanishes on the printed condition

### source witnesses

#### eq24

##### printed H zero

23/250

##### original residual at zero

2367/5000

##### source

p.7 eq(24)

##### printed

Literal displayed expanded beta terms; positive jet F=2,P=1/2,C=1/10

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### eq25

##### printed H zero

-88/25

##### original residual at zero

437/25

##### source

p.7 eq(25)

##### printed

Displayed X5 third-order equation

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### eq26

##### printed mu second zero

-88/25

##### correct mu equation at zero

437/25

##### source

p.7 eq(26)

##### printed

Equation (25) with mu=phi_sigma, hence same failed zero

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### eq27

##### printed Mprime at sample

89/117

##### correct Mprime at sample

-187/65

##### correct rhs

```text
-(36*M**2*Sigma**3*g*kappa - 12*M**2*Sigma**3 - 6*M**2*g + 120*M*Sigma**4*g*kappa - 16*M*Sigma**4 - 5*M*Sigma*g + 72*Sigma**5*g*kappa - 6*Sigma**5)/(Sigma*(3*M + 2*Sigma)*(12*Sigma**3*g*kappa - 4*Sigma**3 + g))
```

##### source

p.7 eq(27)

##### printed

Displayed Abel-type polynomial RHS for M_Sigma

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### status

refuted_as_printed

#### eq28

##### printed H zero

0

##### original residual at zero

169/1000

##### source

p.7 eq(28)

##### printed

Traveling expanded equation with alpha=-1,m=3

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### eq29

##### printed H zero

0

##### original residual at zero

169/1000

##### source

p.8 eq(29)

##### printed

Displayed mu second-order equation, alpha=-1,m=3

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### eq30

##### printed Mprime over M at sample

172/35

##### correct Mprime over M at sample

338/71

##### source

p.8 eq(30)

##### printed

Displayed M_Xi/M logarithmic derivative

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### status

refuted_as_printed

#### eq31

##### printed M

```text
3*P**2*g*kappa/(P**3*(3*g*kappa + 1) + g)
```

##### d of correct integral dP at sample

960/8281

##### source

p.8 eq(31)

##### printed

Displayed complex-form M(Xi), real cubic slice M0=1

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### status

refuted_as_printed

#### eq33

##### printed H zero

-5/119

##### original residual at zero

40337/119000

##### source

p.8 eq(33)

##### printed

Mixed traveling expanded equation alpha=-1,alpha3=1,m=3

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### printed residual at witness

0

##### status

refuted_as_printed

#### eq32

##### not necessary witness

phi=t+s+s^3/6 has p=1, q=1+s^2/2>0, E=0, but F_sss=1

##### source

p.8 eq(32)

##### printed

Quadratic F(s) is sufficient but not necessary for printed wrong 3.8 graph

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### printed quadratic is solution

True

##### quadratic residual

0

##### audit verified

True

##### status

qualified

#### eq34

##### literal implicit first derivative

D(z,P)*C-(P-1)-1=0, D=g/P^2-z+beta*g*(1+P)^2/P

##### literal implied C

10/69

##### literal implied H

60200/328509

##### original residual at implied jet

-118420/328509

##### correct integrand

g/tau^2-alpha^2*tau+beta*g*(alpha3-alpha*tau)^(m-1)/tau

##### note

Even corrected integrand with coefficient 1 fixes first-integral constant I=-1; general I0 must be retained.

##### source

p.9 eq(34)

##### printed

Literal -alpha^2*kappa in integrand; lower limit P0=1

##### domain

g=1,kappa_physical=1/30,m=3; positive P and velocity; see sample

##### audit verified

True

##### status

refuted_as_printed

#### sample

##### m

3

##### alpha

-1

##### alpha3

1

##### g

1

##### kappa

1/30

##### z

1

##### P

1/2

##### C

1/10

##### Sigma

1

##### M

1

### translation witnesses

#### 3.1 source graph Q at Fprime 2

-2

#### 3.2 source graph Q at Fprime 2

-2

#### 3.7 source graph Q at alpha 1 Fprime 2

-1

#### 3.8 source graph Q at alpha 1 Fprime 2

-1

#### 3.8 wrong graph counterexample

##### phi

```text
s**3/6 + s + t
```

##### phi s

```text
s**2/2 + 1
```

##### phi t

1

##### F sss

1

##### original PDE

0

##### note

For any real s this is q>0 and p>0; it violates the printed F_sss=0 requirement while solving the printed scalar PDE.

### further reduction

#### common scaling

I=C*(-z^3*P+g*z/P^2+g*m*kappa*z*(F-z*P)^(m-1)/P); dI/dz equals the third-order residual for symbolic m

#### traveling 3.6 3.9

I=C*(alpha^2*P-g/P^2-g*m*kappa*(alpha3-alpha*P)^(m-1)/P); I is constant; for I!=0, dz/dP=B(P)/I

#### 3.8

H=0, so F(t)=c0+c1*t+c2*t^2/2

#### 3.5

translation in F permits mu=P, a second-order equation; additional scaling gives a rational first-order equation on 2*Sigma/3+M!=0

### printed comparison

#### 3.1 3.2

Source subsection prose reverses Table 3: X1 gives F(s), X2 gives F(t); X2 is outside q>0 domain.

#### 3.7 3.8

Source subsection ansatzes are reversed. Correct 3.7: alpha*t+F(s), identity; correct 3.8: alpha*s+F(t), alpha*F_ttt=0.

#### 3.4

```text
Printed cubic power profile and amplitude condition agree exactly, but the normal-form leading coefficient vanishes there; phi grows like t^(2/3) at fixed s>0.
```

#### 3.5

Printed (25)--(27) fail exact rational witnesses; source power profile is exact and (27) should have an additional 2*Sigma/3+M denominator.

#### 3.6 3.9

```text
Printed (29), (31), (33) fail exact rational witnesses. Correct traveling residual is -alpha*dI/dz. Free-particle linearization is valid locally where B(P)!=0; (34) selects I=-1, not the general family.
```

## [Numeric solutions to the ODEs]

### settings

#### rtol

1e-09

#### atol

1e-11

#### rkf tableau

classic six-stage Fehlberg 4(5)

#### reference

SciPy DOP853, independent comparator

#### pde gate

1e-06

#### solver and integral gate

1e-07

### runs

#### case

3.4

#### m

1

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.03333333333333333

#### equation sha256

f39c9f542268bf09540558660ee1f97ed766403127635e4b5b6bba65561651d9

#### interval

1.0

1.4

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

1.1944423228271717e-10

##### ladder steps

8

13

##### ladder times

1.0

1.0589182305093434

1.1153259359975538

1.1718512231063374

1.224037645874237

1.2726227612032983

1.3181194575164308

1.3608263407648415

1.4

1.0

1.0388059723094785

1.0787414056735738

1.1157941352385692

1.1506340433950384

1.1837410098273662

1.215384996992675

1.2457282358179957

1.2748758025862905

1.3029033866719475

1.329869360749791

1.3558213958746679

1.3808003274377918

1.4

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

1.9984014443252818e-15

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

7.327471962526033e-15

##### initial

0.3566666666666667

#### second order

##### status

passed

##### scaled disagreement

1.9984014443252818e-15

##### integral constant

0.3566666666666667

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.190306410479459e-07

##### error floor

2.190306410479459e-07

##### refinements

###### h

0.003

###### max abs residual

2.190306410479459e-07

###### min velocity

1.4759059540451784

###### min gradient

0.5177707949289797

###### h

0.002

###### max abs residual

5.987460465302005e-07

###### min velocity

1.475905954045317

###### min gradient

0.5177707949289886

###### h

0.001

###### max abs residual

5.311500633444453e-06

###### min velocity

1.4759059540445267

###### min gradient

0.5177707949289134

##### min velocity

1.4759059540445267

##### min gradient

0.5177707949289134

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-2.190306410479459e-07

##### perturbed

0.0024090967140082287

##### absolute change

0.0024093157446492767

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.1518441130005672e-07

##### error floor

2.1518441130005672e-07

##### refinements

###### h

0.003

###### max abs residual

2.1518441130005672e-07

###### min velocity

1.4759059540451038

###### min gradient

0.5177707949295314

###### h

0.002

###### max abs residual

1.0409509800168512e-06

###### min velocity

1.4759059540455364

###### min gradient

0.5177707949286159

###### h

0.001

###### max abs residual

5.328905731044609e-06

###### min velocity

1.4759059540447461

###### min gradient

0.5177707949294081

##### min velocity

1.4759059540447461

##### min gradient

0.5177707949286159

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.4520638899196583

##### min gradient

0.5

##### min abs leading

3.4078465898264607

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m1.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m1.png

#### csv sha256

703d8c738fcf7b47dd76f6cf26cd5e7508f717f9b792083a39d979dcf4c76865

#### status

passed

#### case

3.4

#### m

1.5

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.05

#### equation sha256

efbd683a43fa3f035098e4667cc4616b1fd363c9ee03d5094cc526348b20e77d

#### interval

1.0

1.4

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

1.0865885968769362e-10

##### ladder steps

8

13

##### ladder times

1.0

1.0597383670889664

1.1168047483175851

1.173998059939472

1.226725894917207

1.2757780778533094

1.3216993212546575

1.3648000374786522

1.4

1.0

1.0393993243915856

1.0799758639767985

1.1175033833062877

1.152727835617915

1.1861714924312377

1.2181212052453039

1.2487495325585098

1.2781664148702558

1.306450396252151

1.3336616471517972

1.3598490247607309

1.3850541802550307

1.4

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

2.3314683517128287e-15

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

6.827871601444713e-15

##### initial

0.3622474487139159

#### second order

##### status

passed

##### scaled disagreement

2.4424906541753444e-15

##### integral constant

0.3622474487139159

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.0923331913298417e-07

##### error floor

1.0923331913298417e-07

##### refinements

###### h

0.003

###### max abs residual

1.0923331913298417e-07

###### min velocity

1.4759305512812628

###### min gradient

0.5177569753355514

###### h

0.002

###### max abs residual

5.713600652722944e-07

###### min velocity

1.4759305512811587

###### min gradient

0.5177569753354335

###### h

0.001

###### max abs residual

3.755647306416185e-06

###### min velocity

1.4759305512803451

###### min gradient

0.5177569753352075

##### min velocity

1.4759305512803451

##### min gradient

0.5177569753352075

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-1.0923331913298417e-07

##### perturbed

0.0024212368333889882

##### absolute change

0.0024213460667081212

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

3.575139224318291e-07

##### error floor

3.575139224318291e-07

##### refinements

###### h

0.003

###### max abs residual

3.575139224318291e-07

###### min velocity

1.4759305512811864

###### min gradient

0.517756975335636

###### h

0.002

###### max abs residual

6.032760043166857e-07

###### min velocity

1.4759305512813783

###### min gradient

0.5177569753351701

###### h

0.001

###### max abs residual

1.010513736298714e-05

###### min velocity

1.47593055128123

###### min gradient

0.5177569753360303

##### min velocity

1.4759305512811864

##### min gradient

0.5177569753351701

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.4521747375136285

##### min gradient

0.5

##### min abs leading

3.479454374403078

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m1p5.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m1p5.png

#### csv sha256

06816cc738e62842464e159be167fd482f2a8f6e264ae61e82d38a10082623d4

#### status

passed

#### case

3.4

#### m

2

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.06666666666666667

#### equation sha256

484571c75be4f2a7fd280346d35edceb5c095b8aa87240953d0e23b554afde5c

#### interval

1.0

1.4

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

1.0108547332521312e-10

##### ladder steps

8

13

##### ladder times

1.0

1.060765535863336

1.1186464015631448

1.17666702154273

1.230060286147485

1.279685043932193

1.3261268591022615

1.3697109702634498

1.4

1.0

1.040149646467181

1.0815397047612203

1.1196581883192938

1.1553557329268653

1.1892117554654316

1.221535306691029

1.252512165865603

1.282258394773712

1.3108560982945112

1.338367661712105

1.3648433823400514

1.3903258957073492

1.4

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

2.220446049250313e-15

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

6.439293542825908e-15

##### initial

0.37000000000000005

#### second order

##### status

passed

##### scaled disagreement

2.3314683517128287e-15

##### integral constant

0.37000000000000005

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.8021413514951456e-07

##### error floor

1.8021413514951456e-07

##### refinements

###### h

0.003

###### max abs residual

1.8021413514951456e-07

###### min velocity

1.4759602086855454

###### min gradient

0.5177402987659685

###### h

0.002

###### max abs residual

5.267846019691574e-07

###### min velocity

1.4759602086854424

###### min gradient

0.5177402987660019

###### h

0.001

###### max abs residual

3.335268389042037e-06

###### min velocity

1.4759602086850838

###### min gradient

0.5177402987657042

##### min velocity

1.4759602086850838

##### min gradient

0.5177402987657042

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

1.288807565218153e-07

##### perturbed

0.0024443315444127693

##### absolute change

0.0024442026636562475

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

3.206168738782017e-07

##### error floor

3.206168738782017e-07

##### refinements

###### h

0.003

###### max abs residual

3.206168738782017e-07

###### min velocity

1.4759602086856203

###### min gradient

0.517740298766143

###### h

0.002

###### max abs residual

1.3882679111062307e-06

###### min velocity

1.475960208685001

###### min gradient

0.5177402987660148

###### h

0.001

###### max abs residual

8.679047619393823e-06

###### min velocity

1.4759602086853103

###### min gradient

0.5177402987657713

##### min velocity

1.475960208685001

##### min gradient

0.5177402987657713

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.4523077409005598

##### min gradient

0.5

##### min abs leading

3.5764745096015393

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m2.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m2.png

#### csv sha256

8c903fd0a03cdbb2303817c4695bf777a9c08a9ae954a9a9d13a233a5b8497a7

#### status

passed

#### case

3.4

#### m

3

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.1

#### equation sha256

9315908df0855665d782c9ca5b51cd19cea3820094960221979483e1807bfc5d

#### interval

1.0

1.4

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

9.269962575331192e-11

##### ladder steps

8

12

##### ladder times

1.0

1.063590270707536

1.1236358125610975

1.1838629552373245

1.2390021485344915

1.2901219394189756

1.3379246205188624

1.382776056863304

1.4

1.0

1.0422501696696547

1.0859259575205094

1.125637635573638

1.1625776163272548

1.1975065197215748

1.230800099370951

1.2626812028127792

1.2932828904569162

1.3226968676823558

1.3509913110051213

1.3782201938150445

1.4

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

7.771561172376096e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

3.7192471324942744e-15

##### initial

0.395

#### second order

##### status

passed

##### scaled disagreement

5.551115123125783e-16

##### integral constant

0.395

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.9173936712663098e-07

##### error floor

1.9173936712663098e-07

##### refinements

###### h

0.003

###### max abs residual

1.9173936712663098e-07

###### min velocity

1.4760336475057445

###### min gradient

0.5176989572892626

###### h

0.002

###### max abs residual

4.910832498428164e-07

###### min velocity

1.476033647505882

###### min gradient

0.5176989572891637

###### h

0.001

###### max abs residual

4.701230153017488e-06

###### min velocity

1.4760336475054352

###### min gradient

0.5176989572888945

##### min velocity

1.4760336475054352

##### min gradient

0.5176989572888945

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-4.841001313704574e-08

##### perturbed

0.0025354523170170347

##### absolute change

0.0025355007270301717

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

4.6667830887539563e-07

##### error floor

4.6667830887539563e-07

##### refinements

###### h

0.003

###### max abs residual

4.6667830887539563e-07

###### min velocity

1.4760336475058924

###### min gradient

0.517698957289125

###### h

0.002

###### max abs residual

1.6448962107257215e-06

###### min velocity

1.476033647506103

###### min gradient

0.5176989572893381

###### h

0.001

###### max abs residual

1.3111767576255706e-05

###### min velocity

1.4760336475058793

###### min gradient

0.5176989572887799

##### min velocity

1.4760336475058793

##### min gradient

0.5176989572887799

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.4526348416326536

##### min gradient

0.5

##### min abs leading

3.8782086429384566

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m3.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m3.png

#### csv sha256

cee52fd1a63949beec1f7f7b87ca4a5b666578b3485a323917d10bdf645c0f17

#### status

passed

#### case

3.4

#### m

4

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.13333333333333333

#### equation sha256

3856bd91ea6460795bd724b908c5369f84af12359fe2d397eec03283cfac83d2

#### interval

1.0

1.4

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

8.012139562918463e-11

##### ladder steps

7

12

##### ladder times

1.0

1.0677006434245762

1.1306614305810265

1.193881672363338

1.2513186286730045

1.3043924638693447

1.3539813478083855

1.4

1.0

1.0453818128765222

1.087298593638605

1.1293167036043503

1.168209163055178

1.2047750572311748

1.2395297762938333

1.2727570789719054

1.3046296205790224

1.3352571687358075

1.3647182441102044

1.3930730249411634

1.4

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

1.7763568394002505e-15

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

5.384581669432009e-15

##### initial

0.4399999999999995

#### second order

##### status

passed

##### scaled disagreement

1.6653345369377348e-15

##### integral constant

0.4399999999999995

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.48970396893211e-07

##### error floor

1.48970396893211e-07

##### refinements

###### h

0.003

###### max abs residual

1.48970396893211e-07

###### min velocity

1.4761180651509098

###### min gradient

0.5176514081614616

###### h

0.002

###### max abs residual

9.452355116887357e-07

###### min velocity

1.4761180651509385

###### min gradient

0.5176514081613943

###### h

0.001

###### max abs residual

2.2403253312833216e-06

###### min velocity

1.4761180651504702

###### min gradient

0.5176514081611403

##### min velocity

1.4761180651504702

##### min gradient

0.5176514081611403

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

1.3107343164314722e-07

##### perturbed

0.0027026043551340653

##### absolute change

0.002702473281702422

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

3.2398957711815557e-07

##### error floor

3.2398957711815557e-07

##### refinements

###### h

0.003

###### max abs residual

3.2398957711815557e-07

###### min velocity

1.476118065150908

###### min gradient

0.5176514081615681

###### h

0.002

###### max abs residual

1.1019982615947943e-06

###### min velocity

1.476118065150827

###### min gradient

0.5176514081609425

###### h

0.001

###### max abs residual

1.7328717200636168e-05

###### min velocity

1.4761180651513548

###### min gradient

0.5176514081613623

##### min velocity

1.476118065150827

##### min gradient

0.5176514081609425

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.4530089644599662

##### min gradient

0.5

##### min abs leading

4.398670021320328

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m4.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-4-m4.png

#### csv sha256

428ce21f7f7179a3cd96fe6b67176d3b2f775fdb31a076f4cf73e32fea94b61b

#### status

passed

#### case

3.5

#### m

3

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.1

#### equation sha256

729701d3ab64dd04791d02e22daa7fa4ced0dea9e343c94e101ade67a00c4002

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

2.5305213480208977e-10

##### ladder steps

7

11

##### ladder times

1.0

1.016820889438969

1.0339865141783524

1.0502332174498807

1.0655231498264282

1.0798736115487333

1.0933017396814075

1.1

1.0

1.0107774410202828

1.021642562935689

1.0321465680887707

1.042281810979731

1.052053147306904

1.061465426481685

1.0705230136824728

1.0792296353363475

1.0875882507688148

1.095600907722067

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

1.086630785351872e-13

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

no_certified_integral

##### scaled drift

Not applicable / not supplied.

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

7.984503500590989e-07

##### error floor

4.5925002201130383e-07

##### refinements

###### h

0.003

###### max abs residual

7.984503500590989e-07

###### min velocity

1.0554840028576147

###### min gradient

0.505016269310095

###### h

0.002

###### max abs residual

4.5925002201130383e-07

###### min velocity

1.0554840028582908

###### min gradient

0.5050162693101835

###### h

0.001

###### max abs residual

4.875998125042358e-06

###### min velocity

1.0554840028580346

###### min gradient

0.5050162693099365

##### min velocity

1.0554840028576147

##### min gradient

0.5050162693099365

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

5.615970211092502e-07

##### perturbed

0.00671962173406615

##### absolute change

0.006719060137045041

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

6.507333518701586e-07

##### error floor

6.507333518701586e-07

##### refinements

###### h

0.003

###### max abs residual

6.507333518701586e-07

###### min velocity

1.0554840028573944

###### min gradient

0.5050162693099572

###### h

0.002

###### max abs residual

1.3145536603698105e-06

###### min velocity

1.055484002858404

###### min gradient

0.505016269310197

###### h

0.001

###### max abs residual

6.448723085972219e-06

###### min velocity

1.0554840028575982

###### min gradient

0.5050162693101841

##### min velocity

1.0554840028573944

##### min gradient

0.5050162693099572

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.0

##### min gradient

0.5

##### min abs leading

3.441062684269527

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-5-m3.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-5-m3.png

#### csv sha256

ca779ba324abf121b3b8e8dc51509dc123712838c542cd174c3c8315a8931b81

#### status

passed

#### case

3.6

#### m

1

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.03333333333333333

#### equation sha256

b0ee67bbae1f102fe8dab22ca12ac1fc11b0555e4b08d3d5435c3b7a08cca690

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

7.491335985355648e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

6.582793312495718e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

1.1102230246251565e-15

##### initial

-0.3566666666666667

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.842113392248445e-07

##### error floor

1.842113392248445e-07

##### refinements

###### h

0.003

###### max abs residual

1.842113392248445e-07

###### min velocity

0.5045492882535647

###### min gradient

0.504549288253571

###### h

0.002

###### max abs residual

5.406936004254039e-07

###### min velocity

0.5045492882533958

###### min gradient

0.5045492882534116

###### h

0.001

###### max abs residual

4.846749949585696e-06

###### min velocity

0.5045492882531538

###### min gradient

0.5045492882532809

##### min velocity

0.5045492882531538

##### min gradient

0.5045492882532809

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-1.5506526134510291e-07

##### perturbed

0.003645033307769306

##### absolute change

0.0036451883730306512

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

7.310522064270242e-07

##### error floor

7.310522064270242e-07

##### refinements

###### h

0.003

###### max abs residual

7.310522064270242e-07

###### min velocity

0.504549288253711

###### min gradient

0.5045492882536914

###### h

0.002

###### max abs residual

1.0812500070849114e-06

###### min velocity

0.5045492882536188

###### min gradient

0.5045492882536093

###### h

0.001

###### max abs residual

9.095138463609265e-06

###### min velocity

0.5045492882540403

###### min gradient

0.5045492882538544

##### min velocity

0.5045492882536188

##### min gradient

0.5045492882536093

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

0.5

##### min gradient

0.5

##### min abs leading

3.396027087177261

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m1.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m1.png

#### csv sha256

7ef2d91991e37dc7f882abde91d96c74d8d473d409dd8755cd11663406e6efb4

#### status

passed

#### case

3.6

#### m

1.5

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.05

#### equation sha256

1ef5a41328b8ac2a2a5cf431a0961961d7f5787fc5f5f134a5849b0545ff381d

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

7.276926686870626e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

4.440892098500626e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

7.216449660063518e-16

##### initial

-0.3570710678118655

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

7.316276852929737e-08

##### error floor

7.316276852929737e-08

##### refinements

###### h

0.003

###### max abs residual

7.316276852929737e-08

###### min velocity

0.5045490471741932

###### min gradient

0.5045490471742575

###### h

0.002

###### max abs residual

5.553048063088387e-07

###### min velocity

0.5045490471742686

###### min gradient

0.5045490471742322

###### h

0.001

###### max abs residual

7.928942113898541e-06

###### min velocity

0.5045490471734022

###### min gradient

0.50454904717369

##### min velocity

0.5045490471734022

##### min gradient

0.50454904717369

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

7.316276852929737e-08

##### perturbed

0.0036412176113270623

##### absolute change

0.003641144448558533

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

5.903538622007917e-07

##### error floor

5.903538622007917e-07

##### refinements

###### h

0.003

###### max abs residual

5.903538622007917e-07

###### min velocity

0.5045490471742673

###### min gradient

0.5045490471740725

###### h

0.002

###### max abs residual

1.2441133065738304e-06

###### min velocity

0.5045490471741585

###### min gradient

0.5045490471741914

###### h

0.001

###### max abs residual

1.2918048047554868e-05

###### min velocity

0.5045490471745107

###### min gradient

0.5045490471746156

##### min velocity

0.5045490471741585

##### min gradient

0.5045490471740725

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

0.5

##### min gradient

0.5

##### min abs leading

3.400716398760724

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m1p5.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m1p5.png

#### csv sha256

2d7b6d48e127ba017cc3fee02c5261bf4db4025dcc367ebb18cd91bed6c9e890

#### status

passed

#### case

3.6

#### m

2

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.06666666666666667

#### equation sha256

7e9a303bb3ee92e40f471d00f6d94fb937e510cfe504fa7ce743de47d6778591

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

7.116661128762635e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

4.440892098500626e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

8.881784197001252e-16

##### initial

-0.3566666666666667

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.098783455099131e-07

##### error floor

1.098783455099131e-07

##### refinements

###### h

0.003

###### max abs residual

1.098783455099131e-07

###### min velocity

0.5045488953311383

###### min gradient

0.5045488953311065

###### h

0.002

###### max abs residual

5.699436329575404e-07

###### min velocity

0.5045488953309426

###### min gradient

0.5045488953310017

###### h

0.001

###### max abs residual

2.4524559156463913e-06

###### min velocity

0.5045488953310172

###### min gradient

0.5045488953310381

##### min velocity

0.5045488953309426

##### min gradient

0.5045488953310017

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

8.186379160972021e-08

##### perturbed

0.00363339729587381

##### absolute change

0.0036333154320822

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

4.896615345851424e-07

##### error floor

4.896615345851424e-07

##### refinements

###### h

0.003

###### max abs residual

4.896615345851424e-07

###### min velocity

0.5045488953306937

###### min gradient

0.5045488953308191

###### h

0.002

###### max abs residual

1.343663987963574e-06

###### min velocity

0.5045488953310536

###### min gradient

0.5045488953310094

###### h

0.001

###### max abs residual

1.035321273181464e-05

###### min velocity

0.5045488953305731

###### min gradient

0.5045488953305767

##### min velocity

0.5045488953305731

##### min gradient

0.5045488953305767

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

0.5

##### min gradient

0.5

##### min abs leading

3.3973986140568737

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m2.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m2.png

#### csv sha256

b3c5eb3a96dddb2a3a8210569e2e0714a4fd208e79224b38a9992d825718cabe

#### status

passed

#### case

3.6

#### m

3

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.1

#### equation sha256

d781aee509f1ddc72940d424049d1bee7ca41db4d9c694b83d6f7b1e60c4e06c

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

6.962892772724089e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

1.5226451375354063e-15

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

4.996003610813204e-16

##### initial

-0.355

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.001464332493201e-07

##### error floor

2.001464332493201e-07

##### refinements

###### h

0.003

###### max abs residual

2.001464332493201e-07

###### min velocity

0.5045488320917975

###### min gradient

0.5045488320918207

###### h

0.002

###### max abs residual

3.0725414482124513e-07

###### min velocity

0.5045488320916686

###### min gradient

0.5045488320916399

###### h

0.001

###### max abs residual

3.295745058719962e-06

###### min velocity

0.5045488320912391

###### min gradient

0.5045488320912059

##### min velocity

0.5045488320912391

##### min gradient

0.5045488320912059

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-2.001464332493201e-07

##### perturbed

0.0036150427250003793

##### absolute change

0.0036152428714336287

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

4.886602440372714e-07

##### error floor

4.886602440372714e-07

##### refinements

###### h

0.003

###### max abs residual

4.886602440372714e-07

###### min velocity

0.5045488320916512

###### min gradient

0.5045488320914401

###### h

0.002

###### max abs residual

1.4628822722073664e-06

###### min velocity

0.5045488320915601

###### min gradient

0.5045488320915208

###### h

0.001

###### max abs residual

7.6287739080708496e-06

###### min velocity

0.5045488320914638

###### min gradient

0.5045488320913669

##### min velocity

0.5045488320914638

##### min gradient

0.5045488320913669

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

0.5

##### min gradient

0.5

##### min abs leading

3.3817619537069894

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m3.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m3.png

#### csv sha256

15718ea5f251e4c818d3b3750fe974daaa973179d63c787e03b6e0f278be458a

#### status

passed

#### case

3.6

#### m

4

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.13333333333333333

#### equation sha256

1f21c87e112899ca628c8b49754c634a08df7cb047e4b675aabc52d70b345bcf

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

6.984550216653361e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

6.499277345189808e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

4.440892098500626e-16

##### initial

-0.35333333333333333

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.7906112531260177e-07

##### error floor

1.7906112531260177e-07

##### refinements

###### h

0.003

###### max abs residual

1.7906112531260177e-07

###### min velocity

0.5045489665263614

###### min gradient

0.5045489665262944

###### h

0.002

###### max abs residual

3.208830644269717e-07

###### min velocity

0.5045489665262987

###### min gradient

0.5045489665263602

###### h

0.001

###### max abs residual

1.0492034215807237e-06

###### min velocity

0.5045489665260549

###### min gradient

0.5045489665262678

##### min velocity

0.5045489665260549

##### min gradient

0.5045489665262678

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-1.7906112531260177e-07

##### perturbed

0.0036018739426952264

##### absolute change

0.003602053003820539

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

4.449854977650429e-07

##### error floor

4.449854977650429e-07

##### refinements

###### h

0.003

###### max abs residual

4.449854977650429e-07

###### min velocity

0.5045489665260653

###### min gradient

0.5045489665262355

###### h

0.002

###### max abs residual

9.884115631181647e-07

###### min velocity

0.5045489665264105

###### min gradient

0.5045489665264113

###### h

0.001

###### max abs residual

3.474783589827845e-06

###### min velocity

0.5045489665260557

###### min gradient

0.5045489665262529

##### min velocity

0.5045489665260557

##### min gradient

0.5045489665262355

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

0.5

##### min gradient

0.5

##### min abs leading

3.365439963734349

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m4.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-6-m4.png

#### csv sha256

8c7618d96c16bc15068de1e3e9b0c38975deebc36b8ea0eeac4db4b19349fcd9

#### status

passed

#### case

3.8

#### m

1

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.03333333333333333

#### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

#### interval

0.0

0.4

#### initial jet

0.0

1.0

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

5.551115123125783e-17

##### ladder steps

2

4

##### ladder times

0.0

0.2

0.4

0.0

0.1

0.2

0.30000000000000004

0.4

##### ladder distinct history

True

##### ladder interpretation

roundoff_level_control

##### scaled disagreement

5.3427479529603235e-15

#### exact quadratic

##### status

passed

##### max abs error

4.440892098500626e-15

##### formula

F=F0+P0*(t-t0)+C0*(t-t0)^2/2

#### integral

##### status

no_certified_integral

##### scaled drift

Not applicable / not supplied.

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.1411940196124478e-08

##### error floor

2.1411940196124478e-08

##### refinements

###### h

0.003

###### max abs residual

2.1411940196124478e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998578

###### h

0.002

###### max abs residual

8.184871343964148e-08

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

9.61258731088077e-07

###### min velocity

1.01799999999984

###### min gradient

0.999999999999641

##### min velocity

1.01799999999984

##### min gradient

0.999999999999641

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

2.1411940196124478e-08

##### perturbed

0.0060000035540030364

##### absolute change

0.005999982142062841

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

3.382106223308606e-08

##### error floor

3.382106223308606e-08

##### refinements

###### h

0.003

###### max abs residual

3.382106223308606e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998774

###### h

0.002

###### max abs residual

1.1370803010013993e-07

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

7.440702872869725e-07

###### min velocity

1.0179999999996179

###### min gradient

0.9999999999996897

##### min velocity

1.0179999999996179

##### min gradient

0.9999999999996897

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.0

##### min gradient

1.0

##### min abs leading

1.0

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m1.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m1.png

#### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

#### status

passed

#### case

3.8

#### m

1.5

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.05

#### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

#### interval

0.0

0.4

#### initial jet

0.0

1.0

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

5.551115123125783e-17

##### ladder steps

2

4

##### ladder times

0.0

0.2

0.4

0.0

0.1

0.2

0.30000000000000004

0.4

##### ladder distinct history

True

##### ladder interpretation

roundoff_level_control

##### scaled disagreement

5.3427479529603235e-15

#### exact quadratic

##### status

passed

##### max abs error

4.440892098500626e-15

##### formula

F=F0+P0*(t-t0)+C0*(t-t0)^2/2

#### integral

##### status

no_certified_integral

##### scaled drift

Not applicable / not supplied.

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.1643794816557366e-08

##### error floor

2.1643794816557366e-08

##### refinements

###### h

0.003

###### max abs residual

2.1643794816557366e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998578

###### h

0.002

###### max abs residual

8.25330810118024e-08

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

9.724998540564042e-07

###### min velocity

1.01799999999984

###### min gradient

0.999999999999641

##### min velocity

1.01799999999984

##### min gradient

0.999999999999641

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

2.1643794816557366e-08

##### perturbed

0.006000003798596527

##### absolute change

0.005999982154801711

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

3.412248913258548e-08

##### error floor

3.412248913258548e-08

##### refinements

###### h

0.003

###### max abs residual

3.412248913258548e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998774

###### h

0.002

###### max abs residual

1.139983572562547e-07

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

7.443278582074284e-07

###### min velocity

1.0179999999996179

###### min gradient

0.9999999999996897

##### min velocity

1.0179999999996179

##### min gradient

0.9999999999996897

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.0

##### min gradient

1.0

##### min abs leading

1.0

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m1p5.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m1p5.png

#### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

#### status

passed

#### case

3.8

#### m

2

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.06666666666666667

#### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

#### interval

0.0

0.4

#### initial jet

0.0

1.0

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

5.551115123125783e-17

##### ladder steps

2

4

##### ladder times

0.0

0.2

0.4

0.0

0.1

0.2

0.30000000000000004

0.4

##### ladder distinct history

True

##### ladder interpretation

roundoff_level_control

##### scaled disagreement

5.3427479529603235e-15

#### exact quadratic

##### status

passed

##### max abs error

4.440892098500626e-15

##### formula

F=F0+P0*(t-t0)+C0*(t-t0)^2/2

#### integral

##### status

no_certified_integral

##### scaled drift

Not applicable / not supplied.

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.188021899084344e-08

##### error floor

2.188021899084344e-08

##### refinements

###### h

0.003

###### max abs residual

2.188021899084344e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998578

###### h

0.002

###### max abs residual

8.32322641465843e-08

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

9.839625249786945e-07

###### min velocity

1.01799999999984

###### min gradient

0.999999999999641

##### min velocity

1.01799999999984

##### min gradient

0.999999999999641

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

2.188021899084344e-08

##### perturbed

0.0060000040480391445

##### absolute change

0.005999982167820154

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

3.4429856765323204e-08

##### error floor

3.4429856765323204e-08

##### refinements

###### h

0.003

###### max abs residual

3.4429856765323204e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998774

###### h

0.002

###### max abs residual

1.1429496957305933e-07

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

7.44590505516656e-07

###### min velocity

1.0179999999996179

###### min gradient

0.9999999999996897

##### min velocity

1.0179999999996179

##### min gradient

0.9999999999996897

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.0

##### min gradient

1.0

##### min abs leading

1.0

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m2.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m2.png

#### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

#### status

passed

#### case

3.8

#### m

3

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.1

#### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

#### interval

0.0

0.4

#### initial jet

0.0

1.0

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

5.551115123125783e-17

##### ladder steps

2

4

##### ladder times

0.0

0.2

0.4

0.0

0.1

0.2

0.30000000000000004

0.4

##### ladder distinct history

True

##### ladder interpretation

roundoff_level_control

##### scaled disagreement

5.3427479529603235e-15

#### exact quadratic

##### status

passed

##### max abs error

4.440892098500626e-15

##### formula

F=F0+P0*(t-t0)+C0*(t-t0)^2/2

#### integral

##### status

no_certified_integral

##### scaled drift

Not applicable / not supplied.

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.2367048830122388e-08

##### error floor

2.2367048830122388e-08

##### refinements

###### h

0.003

###### max abs residual

2.2367048830122388e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998578

###### h

0.002

###### max abs residual

8.467604966840432e-08

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

1.00756573839651e-06

###### min velocity

1.01799999999984

###### min gradient

0.999999999999641

##### min velocity

1.01799999999984

##### min gradient

0.999999999999641

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

2.2367048830122388e-08

##### perturbed

0.00600000456176301

##### absolute change

0.00599998219471418

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

3.506276892710659e-08

##### error floor

3.506276892710659e-08

##### refinements

###### h

0.003

###### max abs residual

3.506276892710659e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998774

###### h

0.002

###### max abs residual

1.1490746227674777e-07

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

7.451313323915893e-07

###### min velocity

1.0179999999996179

###### min gradient

0.9999999999996897

##### min velocity

1.0179999999996179

##### min gradient

0.9999999999996897

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.0

##### min gradient

1.0

##### min abs leading

1.0

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m3.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m3.png

#### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

#### status

passed

#### case

3.8

#### m

4

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.13333333333333333

#### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

#### interval

0.0

0.4

#### initial jet

0.0

1.0

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

5.551115123125783e-17

##### ladder steps

2

4

##### ladder times

0.0

0.2

0.4

0.0

0.1

0.2

0.30000000000000004

0.4

##### ladder distinct history

True

##### ladder interpretation

roundoff_level_control

##### scaled disagreement

5.3427479529603235e-15

#### exact quadratic

##### status

passed

##### max abs error

4.440892098500626e-15

##### formula

F=F0+P0*(t-t0)+C0*(t-t0)^2/2

#### integral

##### status

no_certified_integral

##### scaled drift

Not applicable / not supplied.

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.2872984444225824e-08

##### error floor

2.2872984444225824e-08

##### refinements

###### h

0.003

###### max abs residual

2.2872984444225824e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998578

###### h

0.002

###### max abs residual

8.618205069841397e-08

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

1.032095266605055e-06

###### min velocity

1.01799999999984

###### min gradient

0.999999999999641

##### min velocity

1.01799999999984

##### min gradient

0.999999999999641

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

2.2872984444225824e-08

##### perturbed

0.006000005095766874

##### absolute change

0.00599998222278243

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

3.572051990580516e-08

##### error floor

3.572051990580516e-08

##### refinements

###### h

0.003

###### max abs residual

3.572051990580516e-08

###### min velocity

1.017999999999922

###### min gradient

0.9999999999998774

###### h

0.002

###### max abs residual

1.155463484746542e-07

###### min velocity

1.0179999999999023

###### min gradient

0.9999999999998594

###### h

0.001

###### max abs residual

7.456933841702903e-07

###### min velocity

1.0179999999996179

###### min gradient

0.9999999999996897

##### min velocity

1.0179999999996179

##### min gradient

0.9999999999996897

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.0

##### min gradient

1.0

##### min abs leading

1.0

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m4.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-8-m4.png

#### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

#### status

passed

#### case

3.9

#### m

1

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.03333333333333333

#### equation sha256

b0ee67bbae1f102fe8dab22ca12ac1fc11b0555e4b08d3d5435c3b7a08cca690

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

7.491335985355648e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

6.582793312495718e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

1.1102230246251565e-15

##### initial

-0.3566666666666667

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.4577930336235586e-07

##### error floor

2.4577930336235586e-07

##### refinements

###### h

0.003

###### max abs residual

2.4577930336235586e-07

###### min velocity

1.5045492882534859

###### min gradient

0.5045492882535075

###### h

0.002

###### max abs residual

1.724419977751834e-06

###### min velocity

1.5045492882528735

###### min gradient

0.5045492882533442

###### h

0.001

###### max abs residual

3.133935333792621e-06

###### min velocity

1.5045492882528544

###### min gradient

0.5045492882528676

##### min velocity

1.5045492882528544

##### min gradient

0.5045492882528676

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-2.4577930336235586e-07

##### perturbed

0.0036449515454755423

##### absolute change

0.0036451973247789045

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

5.461882635702381e-07

##### error floor

5.461882635702381e-07

##### refinements

###### h

0.003

###### max abs residual

5.461882635702381e-07

###### min velocity

1.504549288253484

###### min gradient

0.5045492882535725

###### h

0.002

###### max abs residual

1.5864903579918769e-06

###### min velocity

1.5045492882534295

###### min gradient

0.5045492882535418

###### h

0.001

###### max abs residual

6.422977558625696e-06

###### min velocity

1.5045492882532985

###### min gradient

0.5045492882537195

##### min velocity

1.5045492882532985

##### min gradient

0.5045492882535418

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.5

##### min gradient

0.5

##### min abs leading

3.396027087177261

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m1.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m1.png

#### csv sha256

7ef2d91991e37dc7f882abde91d96c74d8d473d409dd8755cd11663406e6efb4

#### status

passed

#### case

3.9

#### m

1.5

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.05

#### equation sha256

fc9ca7d0e6f7ebc0a805b348a6c573deabdc42b38464c0ccd9a96b5519d2ab06

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

7.019202389806035e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

6.537823479988413e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

3.3306690738754696e-16

##### initial

-0.3622474487139159

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.2464625998048354e-07

##### error floor

2.2464625998048354e-07

##### refinements

###### h

0.003

###### max abs residual

2.2464625998048354e-07

###### min velocity

1.5045487178128623

###### min gradient

0.5045487178128969

###### h

0.002

###### max abs residual

4.91944746975996e-07

###### min velocity

1.5045487178126404

###### min gradient

0.5045487178128092

###### h

0.001

###### max abs residual

7.513345113773287e-06

###### min velocity

1.5045487178122083

###### min gradient

0.5045487178123593

##### min velocity

1.5045487178122083

##### min gradient

0.5045487178123593

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-7.17909199527203e-08

##### perturbed

0.0036416319623189695

##### absolute change

0.0036417037532389222

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

5.423148075750506e-07

##### error floor

5.423148075750506e-07

##### refinements

###### h

0.003

###### max abs residual

5.423148075750506e-07

###### min velocity

1.5045487178127148

###### min gradient

0.5045487178128183

###### h

0.002

###### max abs residual

1.8841789203817225e-06

###### min velocity

1.5045487178125319

###### min gradient

0.504548717812756

###### h

0.001

###### max abs residual

5.1833205241104754e-06

###### min velocity

1.5045487178122083

###### min gradient

0.5045487178127895

##### min velocity

1.5045487178122083

##### min gradient

0.504548717812756

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.5

##### min gradient

0.5

##### min abs leading

3.451171107551896

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m1p5.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m1p5.png

#### csv sha256

a79d852931cd7c8786097e7f0a35de1f8f5d2e535147bd83ce2396ca72276429

#### status

passed

#### case

3.9

#### m

2

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.06666666666666667

#### equation sha256

541bd41e0e32a4fb8c19aee70935beb50a4d9cdb6abaf4c0df0a085c083a8fe0

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

6.321830679415099e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

1.5226452058255827e-15

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

5.551115123125783e-16

##### initial

-0.37000000000000005

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

2.5226434934456227e-07

##### error floor

2.5226434934456227e-07

##### refinements

###### h

0.003

###### max abs residual

2.5226434934456227e-07

###### min velocity

1.5045478526671243

###### min gradient

0.5045478526671646

###### h

0.002

###### max abs residual

1.4813565817582697e-06

###### min velocity

1.5045478526670706

###### min gradient

0.5045478526670698

###### h

0.001

###### max abs residual

6.394347023035152e-06

###### min velocity

1.5045478526658598

###### min gradient

0.5045478526666772

##### min velocity

1.5045478526658598

##### min gradient

0.5045478526666772

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-9.809160849121729e-08

##### perturbed

0.003633542751492887

##### absolute change

0.0036336408431013783

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

5.229835341579586e-07

##### error floor

5.229835341579586e-07

##### refinements

###### h

0.003

###### max abs residual

5.229835341579586e-07

###### min velocity

1.5045478526671219

###### min gradient

0.5045478526673076

###### h

0.002

###### max abs residual

1.660763711263183e-06

###### min velocity

1.5045478526675138

###### min gradient

0.5045478526673857

###### h

0.001

###### max abs residual

4.310747688338751e-06

###### min velocity

1.504547852666302

###### min gradient

0.504547852666752

##### min velocity

1.504547852666302

##### min gradient

0.504547852666752

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.5

##### min gradient

0.5

##### min abs leading

3.5281421504819996

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m2.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m2.png

#### csv sha256

664f20a71e4818a1fd4517866a9af7fa1b1e65ee974984e3abb73b64a13edd21

#### status

passed

#### case

3.9

#### m

3

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.1

#### equation sha256

32b928ee12fee2a62946e8a63e8e094c1714b836bcc4e22c6ad2cc9a1fa92865

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

4.2210520833911306e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

6.607477084810661e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

8.326672684688674e-16

##### initial

-0.395

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.214725868399491e-07

##### error floor

1.214725868399491e-07

##### refinements

###### h

0.003

###### max abs residual

1.214725868399491e-07

###### min velocity

1.5045448501566103

###### min gradient

0.504544850156826

###### h

0.002

###### max abs residual

1.0062594627824328e-06

###### min velocity

1.5045448501564165

###### min gradient

0.5045448501566365

###### h

0.001

###### max abs residual

2.0894316442553185e-06

###### min velocity

1.5045448501558465

###### min gradient

0.5045448501562594

##### min velocity

1.5045448501558465

##### min gradient

0.5045448501562594

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

8.571672034315969e-08

##### perturbed

0.0035866315473274575

##### absolute change

0.0035865458306071143

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

5.164278437594372e-07

##### error floor

5.164278437594372e-07

##### refinements

###### h

0.003

###### max abs residual

5.164278437594372e-07

###### min velocity

1.5045448501563148

###### min gradient

0.5045448501564623

###### h

0.002

###### max abs residual

1.39742703546622e-06

###### min velocity

1.5045448501566419

###### min gradient

0.5045448501566431

###### h

0.001

###### max abs residual

7.06454666707379e-06

###### min velocity

1.5045448501558518

###### min gradient

0.5045448501561272

##### min velocity

1.5045448501558518

##### min gradient

0.5045448501561272

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.5

##### min gradient

0.5

##### min abs leading

3.7780806558462383

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m3.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m3.png

#### csv sha256

846874f12121c78769dead4a3b61f38fdcfef9a03442cc4325ed20091843a88c

#### status

passed

#### case

3.9

#### m

4

#### model

printed scalar

#### g

1.0

#### kappa

0.03333333333333333

#### beta

0.13333333333333333

#### equation sha256

f1d4adbe163db30e4bb2f60bb9658679e7c1b4e12bef962c28aa261df595b301

#### interval

1.0

1.1

#### initial jet

2.0

0.5

0.1

#### solver

##### status

completed

##### steps

80

##### rejected

0

##### nfev

480

##### tight ladder disagreement

1.6091549936350132e-13

##### ladder steps

2

4

##### ladder times

1.0

1.05

1.1

1.0

1.025

1.0499999999999998

1.0749999999999997

1.1

##### ladder distinct history

True

##### ladder interpretation

finite_step_comparison

##### scaled disagreement

4.4022370946043354e-16

#### exact quadratic

##### status

not_applicable

##### max abs error

Not applicable / not supplied.

#### integral

##### status

passed

##### scaled drift

5.551115123125783e-16

##### initial

-0.43999999999999995

#### second order

##### status

not_applicable

##### scaled disagreement

Not applicable / not supplied.

#### pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

1.4631268808323883e-07

##### error floor

1.4631268808323883e-07

##### refinements

###### h

0.003

###### max abs residual

1.4631268808323883e-07

###### min velocity

1.5045394628922806

###### min gradient

0.5045394628923898

###### h

0.002

###### max abs residual

1.2473233633042424e-06

###### min velocity

1.5045394628921072

###### min gradient

0.504539462892126

###### h

0.001

###### max abs residual

2.2146029277914092e-06

###### min velocity

1.504539462891212

###### min gradient

0.5045394628916788

##### min velocity

1.504539462891212

##### min gradient

0.5045394628916788

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

DOP853 reference reconstruction

#### negative control

##### baseline

-1.1856428128176333e-07

##### perturbed

0.0034640038686463426

##### absolute change

0.0034641224329276243

##### passed

True

##### perturbation

phi + 0.001*t^3

#### rkf pde

##### status

passed

##### acceptance h

0.003

##### acceptance max abs residual

9.361751006145558e-07

##### error floor

9.361751006145558e-07

##### refinements

###### h

0.003

###### max abs residual

9.361751006145558e-07

###### min velocity

1.504539462891911

###### min gradient

0.5045394628919775

###### h

0.002

###### max abs residual

2.3131478720378462e-06

###### min velocity

1.504539462892331

###### min gradient

0.5045394628926481

###### h

0.001

###### max abs residual

8.286120069048164e-06

###### min velocity

1.5045394628912174

###### min gradient

0.5045394628918275

##### min velocity

1.5045394628912174

##### min gradient

0.5045394628918275

##### stencil

nine-point tensor finite differences of reconstructed phi

##### trajectory

tight RKF45 local degree-11 interpolation

#### branch

##### min velocity

1.5

##### min gradient

0.5

##### min abs leading

4.231632293292684

##### sample count

81

#### csv

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m4.csv

#### plot

D:\MATHs\math 4890 LieML\research_artifacts\SVE-reproduced-20261012\results\numerical\3-9-m4.png

#### csv sha256

c9052ada042b51800165bc1edffc91878e253f1fcb226b73e179341a0d964d6e

#### status

passed

### non numerical

#### case

3.5

#### m

1

#### status

incompatible_exponent

#### reason

X5 is a symmetry only at m=3

#### case

3.5

#### m

1.5

#### status

incompatible_exponent

#### reason

X5 is a symmetry only at m=3

#### case

3.5

#### m

2

#### status

incompatible_exponent

#### reason

X5 is a symmetry only at m=3

#### case

3.5

#### m

4

#### status

incompatible_exponent

#### reason

X5 is a symmetry only at m=3

#### case

3.1

#### status

identity

#### reason

no regular positive-branch IVP in this campaign

#### case

3.2

#### status

undefined

#### reason

no regular positive-branch IVP in this campaign

#### case

3.3

#### status

no_invariant_graph

#### reason

no regular positive-branch IVP in this campaign

#### case

3.7

#### status

identity

#### reason

no regular positive-branch IVP in this campaign

#### case

table3-mixed

#### status

symbolic_only_companion

#### reason

no regular positive-branch IVP in this campaign

### all passed

True

## Local analytic existence and ODE series

### order

6

### model

printed scalar SVE, corrected reductions

### regular runs

#### case

3.4

#### m

1

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
119237278253*h**6/49154850375000 - 11839081*h**5/15313037500 + 39187*h**4/5724500 - 32*h**3/8025 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

-32/8025

39187/5724500

-11839081/15313037500

119237278253/49154850375000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

107/30

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

-64/2675

##### coefficient

-32/8025

##### degree

4

##### rhs coefficient

235122/1431125

##### coefficient

39187/5724500

##### degree

5

##### rhs coefficient

-35517243/765651875

##### coefficient

-11839081/15313037500

##### degree

6

##### rhs coefficient

119237278253/409623753125

##### coefficient

119237278253/49154850375000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.19999999999999996

###### z

1.2

###### polynomial

2.1019789603142987

0.5197390233025638

0.09849352177047582

###### rkf45

2.1019789602242422

0.5197390366741125

0.09849459384273986

###### dop853

2.101978960224242

0.5197390366741123

0.09849459384274009

###### abs error vs dop853

9.00568508654942e-11

1.337154842406818e-08

1.072072264268753e-06

###### abs error vs rkf45

9.005640677628435e-11

1.3371548646112785e-08

1.0720722640328306e-06

###### rkf dop disagreement

4.440892098500626e-16

2.220446049250313e-16

2.3592239273284576e-16

###### diagnostic resolution threshold

1.4935458809079036e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.10000000000000009

###### z

1.1

###### polynomial

2.0504966917043026

0.5099075147627421

0.09842074977538895

###### rkf45

2.0504966916909897

0.5099075139547746

0.09842071124100413

###### dop853

2.0504966916909892

0.5099075139547746

0.09842071124100427

###### abs error vs dop853

1.3313350422095027e-11

8.079674707062168e-10

3.853438468315318e-08

###### abs error vs rkf45

1.3312906332885177e-11

8.079674707062168e-10

3.8534384821931056e-08

###### rkf dop disagreement

4.440892098500626e-16

0.0

1.3877787807814457e-16

###### diagnostic resolution threshold

1.4569655289811502e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251245441382335

0.5049734965900241

0.09900762496283252

###### rkf45

2.025124544138081

0.5049734965696708

0.09900762267451506

###### dop853

2.025124544138081

0.5049734965696707

0.09900762267451514

###### abs error vs dop853

1.5232259897857148e-13

2.0353385643545607e-11

2.288317382803662e-09

###### abs error vs rkf45

1.5232259897857148e-13

2.0353274621243145e-11

2.2883174660703887e-09

###### rkf dop disagreement

0.0

1.1102230246251565e-16

8.326672684688674e-17

###### diagnostic resolution threshold

1.438937533846798e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531190361765

0.5024929498396289

0.09945299714536263

###### rkf45

2.0125311903617633

0.5024929498392506

0.09945299705700102

###### dop853

2.0125311903617633

0.5024929498392506

0.09945299705700104

###### abs error vs dop853

1.7763568394002505e-15

3.7825298448979083e-13

8.836158194025501e-11

###### abs error vs rkf45

1.7763568394002505e-15

3.7825298448979083e-13

8.836160969583062e-11

###### rkf dop disagreement

0.0

0.0

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4299894178021783e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

703d8c738fcf7b47dd76f6cf26cd5e7508f717f9b792083a39d979dcf4c76865

###### equation sha256

f39c9f542268bf09540558660ee1f97ed766403127635e4b5b6bba65561651d9

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.4

#### m

3/2

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
-159958856830575889*sqrt(6)*h**6/3484994863510753200000 + 679997977008999479*h**6/272265223711777593750 - 53049398855359*h**5/79121710564200000 - 1074616912837*sqrt(6)*h**5/15824342112840000 - 15019093*sqrt(6)*h**4/258673348800 + 747328723*h**4/107780562000 - 1859*h**3/489400 - 113*sqrt(6)*h**3/880920 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

-(565*sqrt(6) + 16731)/4404600

-(-8967944676 + 75095465*sqrt(6))/1293366744000

-(5373084564185*sqrt(6) + 53049398855359)/79121710564200000

-(-43519870528575966656 + 799794284152879445*sqrt(6))/17424974317553766000000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

sqrt(6)/20 + 7/2

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

-5577/244700 - 113*sqrt(6)/146820

##### coefficient

-(565*sqrt(6) + 16731)/4404600

##### degree

4

##### rhs coefficient

747328723/4490856750 - 15019093*sqrt(6)/10778056200

##### coefficient

-(-8967944676 + 75095465*sqrt(6))/1293366744000

##### degree

5

##### rhs coefficient

-53049398855359/1318695176070000 - 1074616912837*sqrt(6)/263739035214000

##### coefficient

-(5373084564185*sqrt(6) + 53049398855359)/79121710564200000

##### degree

6

##### rhs coefficient

2719991908035997916/9075507457059253125 - 159958856830575889*sqrt(6)/29041623862589610000

##### coefficient

-(-43519870528575966656 + 799794284152879445*sqrt(6))/17424974317553766000000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.19999999999999996

###### z

1.2

###### polynomial

2.101977849491138

0.519721686873404

0.09830526694607168

###### rkf45

2.1019778487401566

0.5197216764629036

0.09830559802358306

###### dop853

2.1019778487401557

0.5197216764629031

0.09830559802358328

###### abs error vs dop853

7.509823873874666e-10

1.0410500905777553e-08

3.3107751160055265e-07

###### abs error vs rkf45

7.509814992090469e-10

1.0410500461688343e-08

3.3107751137850805e-07

###### rkf dop disagreement

8.881784197001252e-16

4.440892098500626e-16

2.220446049250313e-16

###### diagnostic resolution threshold

1.4935450911509603e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.10000000000000009

###### z

1.1

###### polynomial

2.050496560437489

0.5099035088907178

0.09833776589041604

###### rkf45

2.050496560419466

0.5099035077489842

0.09833770699799083

###### dop853

2.050496560419465

0.509903507748984

0.09833770699799095

###### abs error vs dop853

1.802424876018449e-11

1.1417338185992776e-09

5.889242508938519e-08

###### abs error vs rkf45

1.802336058176479e-11

1.1417335965546727e-09

5.889242521428528e-08

###### rkf dop disagreement

8.881784197001252e-16

2.220446049250313e-16

1.249000902703301e-16

###### diagnostic resolution threshold

1.4569654357071222e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251245281309798

0.5049725285816391

0.09896828133043761

###### rkf45

2.025124528130792

0.5049725285563148

0.09896827844101429

###### dop853

2.0251245281307924

0.5049725285563148

0.09896827844101436

###### abs error vs dop853

1.8740564655672642e-13

2.5324298214002283e-11

2.8894232562137745e-09

###### abs error vs rkf45

1.8784973576657649e-13

2.5324298214002283e-11

2.8894233256027135e-09

###### rkf dop disagreement

4.440892098500626e-16

0.0

6.938893903907228e-17

###### diagnostic resolution threshold

1.4389375224729352e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531188383853

0.5024927115968559

0.09943379270670559

###### rkf45

2.0125311883838513

0.5024927115964017

0.09943379260005335

###### dop853

2.0125311883838513

0.5024927115964019

0.09943379260005339

###### abs error vs dop853

1.7763568394002505e-15

4.54081217071689e-13

1.0665220095962269e-10

###### abs error vs rkf45

1.7763568394002505e-15

4.5419223937415154e-13

1.0665224259298611e-10

###### rkf dop disagreement

0.0

1.1102230246251565e-16

4.163336342344337e-17

###### diagnostic resolution threshold

1.4299894163967872e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

06816cc738e62842464e159be167fd482f2a8f6e264ae61e82d38a10082623d4

###### equation sha256

efbd683a43fa3f035098e4667cc4616b1fd363c9ee03d5094cc526348b20e77d

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.4

#### m

2

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
266275417213*h**6/113855280750000 - 10402939*h**5/11396925000 + 3454*h**4/513375 - 71*h**3/16650 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

-71/16650

3454/513375

-10402939/11396925000

266275417213/113855280750000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

37/10

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

-71/2775

##### coefficient

-71/16650

##### degree

4

##### rhs coefficient

27632/171125

##### coefficient

3454/513375

##### degree

5

##### rhs coefficient

-10402939/189948750

##### coefficient

-10402939/11396925000

##### degree

6

##### rhs coefficient

266275417213/948794006250

##### coefficient

266275417213/113855280750000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.19999999999999996

###### z

1.2

###### polynomial

2.1019765083132564

0.5197007731597919

0.09807854795605186

###### rkf45

2.1019765067986147

0.5197007352943754

0.09807802458668435

###### dop853

2.1019765067986165

0.5197007352943751

0.09807802458668455

###### abs error vs dop853

1.5146399690024737e-09

3.786541680206312e-08

5.233693673167839e-07

###### abs error vs rkf45

1.514641745359313e-09

3.7865416468996216e-08

5.233693675110729e-07

###### rkf dop disagreement

1.7763568394002505e-15

3.3306690738754696e-16

1.942890293094024e-16

###### diagnostic resolution threshold

1.7763568394002505e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.10000000000000009

###### z

1.1

###### polynomial

2.050496401749139

0.5098986681040943

0.0982375649403459

###### rkf45

2.050496401725655

0.5098986665757087

0.09823748247719556

###### dop853

2.050496401725657

0.5098986665757087

0.0982374824771957

###### abs error vs dop853

2.348210514924176e-11

1.5283856402703577e-09

8.246315019722061e-08

###### abs error vs rkf45

2.348432559529101e-11

1.5283856402703577e-09

8.246315033599849e-08

###### rkf dop disagreement

2.220446049250313e-15

0.0

1.3877787807814457e-16

###### diagnostic resolution threshold

2.220446049250313e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251245087684224

0.5049713578912535

0.09892071802826063

###### rkf45

2.0251245087681937

0.5049713578601608

0.09892071444150878

###### dop853

2.025124508768194

0.5049713578601608

0.09892071444150885

###### abs error vs dop853

2.282618538629322e-13

3.109268398304721e-11

3.5867517844678787e-09

###### abs error vs rkf45

2.2870594307278225e-13

3.109268398304721e-11

3.5867518538568177e-09

###### rkf dop disagreement

4.440892098500626e-16

0.0

6.938893903907228e-17

###### diagnostic resolution threshold

1.4389375087149817e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531185990663

0.5024924233603387

0.09941056271190878

###### rkf45

2.0125311859906607

0.5024924233597964

0.0994105625840174

###### dop853

2.012531185990661

0.5024924233597964

0.09941056258401744

###### abs error vs dop853

1.7763568394002505e-15

5.42343947529389e-13

1.2789133641000205e-10

###### abs error vs rkf45

2.220446049250313e-15

5.42343947529389e-13

1.2789137804336548e-10

###### rkf dop disagreement

4.440892098500626e-16

0.0

4.163336342344337e-17

###### diagnostic resolution threshold

1.4299894146963234e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

8c903fd0a03cdbb2303817c4695bf777a9c08a9ae954a9a9d13a233a5b8497a7

###### equation sha256

484571c75be4f2a7fd280346d35edceb5c095b8aa87240953d0e23b554afde5c

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.4

#### m

3

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
97895097811*h**6/43818841125000 - 13543709*h**5/12325975000 + 41037*h**4/6241000 - 11*h**3/2370 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

-11/2370

41037/6241000

-13543709/12325975000

97895097811/43818841125000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

79/20

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

-11/395

##### coefficient

-11/2370

##### degree

4

##### rhs coefficient

123111/780125

##### coefficient

41037/6241000

##### degree

5

##### rhs coefficient

-40631127/616298750

##### coefficient

-13543709/12325975000

##### degree

6

##### rhs coefficient

97895097811/365157009375

##### coefficient

97895097811/43818841125000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.19999999999999996

###### z

1.2

###### polynomial

2.101973181187445

0.5196489495023321

0.09751799536427673

###### rkf45

2.1019731779032513

0.5196488481223264

0.09751549961164248

###### dop853

2.1019731779032513

0.5196488481223265

0.09751549961164271

###### abs error vs dop853

3.284193805797031e-09

1.0138000561266125e-07

2.495752634015802e-06

###### abs error vs rkf45

3.284193805797031e-09

1.0138000572368355e-07

2.4957526342517244e-06

###### rkf dop disagreement

0.0

1.1102230246251565e-16

2.3592239273284576e-16

###### diagnostic resolution threshold

1.493541772321728e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.10000000000000009

###### z

1.1

###### polynomial

2.0504960074347904

0.5098866456960555

0.09798896287854608

###### rkf45

2.0504960073985847

0.5098866432672743

0.09798882558432849

###### dop853

2.050496007398585

0.5098866432672743

0.09798882558432861

###### abs error vs dop853

3.6205261011446055e-11

2.428781176178063e-09

1.372942174671099e-07

###### abs error vs rkf45

3.6205705100655905e-11

2.428781176178063e-09

1.3729421759201e-07

###### rkf dop disagreement

4.440892098500626e-16

0.0

1.249000902703301e-16

###### diagnostic resolution threshold

1.4569650427621533e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251244606189367

0.5049684474192938

0.09880252849945384

###### rkf45

2.0251244606186116

0.5049684473747253

0.098802523284478

###### dop853

2.0251244606186125

0.5049684473747255

0.09880252328447807

###### abs error vs dop853

3.241851231905457e-13

4.4568349011342434e-11

5.2149757706621e-09

###### abs error vs rkf45

3.2507330161024584e-13

4.4568460033644897e-11

5.214975840051039e-09

###### rkf dop disagreement

8.881784197001252e-16

1.1102230246251565e-16

6.938893903907228e-17

###### diagnostic resolution threshold

1.4389374745026462e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531180037229

0.5024917064149607

0.09935279569009021

###### rkf45

2.0125311800372265

0.5024917064142119

0.09935279551251416

###### dop853

2.0125311800372265

0.5024917064142119

0.09935279551251419

###### abs error vs dop853

2.6645352591003757e-15

7.487344078072056e-13

1.7757602333023925e-10

###### abs error vs rkf45

2.6645352591003757e-15

7.487344078072056e-13

1.7757605108581487e-10

###### rkf dop disagreement

0.0

0.0

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4299894104661537e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

cee52fd1a63949beec1f7f7b87ca4a5b666578b3485a323917d10bdf645c0f17

###### equation sha256

9315908df0855665d782c9ca5b51cd19cea3820094960221979483e1807bfc5d

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.4

#### m

4

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
35907084667*h**6/16866432000000 - 16795637*h**5/12777600000 + 74369*h**4/11616000 - 67*h**3/13200 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

-67/13200

74369/11616000

-16795637/12777600000

35907084667/16866432000000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

22/5

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

-67/2200

##### coefficient

-67/13200

##### degree

4

##### rhs coefficient

74369/484000

##### coefficient

74369/11616000

##### degree

5

##### rhs coefficient

-16795637/212960000

##### coefficient

-16795637/12777600000

##### degree

6

##### rhs coefficient

35907084667/140553600000

##### coefficient

35907084667/16866432000000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.19999999999999996

###### z

1.2

###### polynomial

2.1019693532264054

0.5195893541972505

0.09687406416304384

###### rkf45

2.101969348043435

0.5195891848519751

0.09686946552355416

###### dop853

2.101969348043435

0.5195891848519747

0.09686946552355438

###### abs error vs dop853

5.182970497230599e-09

1.6934527580225733e-07

4.598639489455936e-06

###### abs error vs rkf45

5.182970497230599e-09

1.6934527535816812e-07

4.59863948967798e-06

###### rkf dop disagreement

0.0

4.440892098500626e-16

2.220446049250313e-16

###### diagnostic resolution threshold

1.4935390510426565e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.10000000000000009

###### z

1.1

###### polynomial

2.0504955534557325

0.509872806937274

0.0977029177835123

###### rkf45

2.0504955534057436

0.5098728035342439

0.09770272126752483

###### dop853

2.0504955534057423

0.5098728035342438

0.09770272126752495

###### abs error vs dop853

4.999023417440185e-11

3.403030190973766e-09

1.9651598734404807e-07

###### abs error vs rkf45

4.99889019067723e-11

3.4030300799514634e-09

1.9651598746894816e-07

###### rkf dop disagreement

1.3322676295501878e-15

1.1102230246251565e-16

1.249000902703301e-16

###### diagnostic resolution threshold

1.4569647201808367e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.025124405167111

0.5049650958779994

0.09866645444728767

###### rkf45

2.025124405166683

0.5049650958187701

0.09866644746247911

###### dop853

2.0251244051666824

0.5049650958187701

0.09866644746247917

###### abs error vs dop853

4.285460875053104e-13

5.922928814072748e-11

6.9848084954804435e-09

###### abs error vs rkf45

4.2810199829546036e-13

5.922928814072748e-11

6.984808550991595e-09

###### rkf dop disagreement

4.440892098500626e-16

0.0

5.551115123125783e-17

###### diagnostic resolution threshold

1.43893743510168e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.0125311731798656

0.5024908806551042

0.09928626771778915

###### rkf45

2.0125311731798625

0.5024908806541303

0.09928626748603489

###### dop853

2.012531173179862

0.5024908806541303

0.09928626748603492

###### abs error vs dop853

3.552713678800501e-15

9.738876372011873e-13

2.317542269203443e-10

###### abs error vs rkf45

3.1086244689504383e-15

9.738876372011873e-13

2.3175425467591992e-10

###### rkf dop disagreement

4.440892098500626e-16

0.0

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4299894055937032e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

428ce21f7f7179a3cd96fe6b67176d3b2f775fdb31a076f4cf73e32fea94b61b

###### equation sha256

3856bd91ea6460795bd724b908c5369f84af12359fe2d397eec03283cfac83d2

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.5

#### m

3

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
2893976089*h**6/3294225000 + 73808*h**5/226875 + 8309*h**4/60500 + 83*h**3/1100 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

83/1100

8309/60500

73808/226875

2893976089/3294225000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-22/5

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

249/550

##### coefficient

83/1100

##### degree

4

##### rhs coefficient

49854/15125

##### coefficient

8309/60500

##### degree

5

##### rhs coefficient

295232/15125

##### coefficient

73808/226875

##### degree

6

##### rhs coefficient

2893976089/27451875

##### coefficient

2893976089/3294225000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.025135405576422

0.5056463920907549

0.12773455893774335

###### rkf45

2.025135407985645

0.5056467385605181

0.12777767811832044

###### dop853

2.0251354079856467

0.5056467385605179

0.12777767811832044

###### abs error vs dop853

2.409224819643896e-09

3.4646976299068655e-07

4.311918057708919e-05

###### abs error vs rkf45

2.4092230432870565e-09

3.4646976321273115e-07

4.311918057708919e-05

###### rkf dop disagreement

1.7763568394002505e-15

2.220446049250313e-16

0.0

###### diagnostic resolution threshold

1.7763568394002505e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012532486016733

0.5026507478244614

0.1124601819721764

###### rkf45

2.012532486033926

0.5026507526978359

0.11246137095840224

###### dop853

2.0125324860339266

0.502650752697836

0.11246137095840296

###### abs error vs dop853

1.7193801937764874e-11

4.8733745927620475e-09

1.188986226557942e-06

###### abs error vs rkf45

1.7193357848555024e-11

4.873374481739745e-09

1.188986225836297e-06

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

7.216449660063518e-16

###### diagnostic resolution threshold

1.429990338432622e-14

7.105427357601002e-15

7.216449660063518e-15

###### resolved vs reference

True

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062579633277906

0.5012864835989393

0.1059299526611398

###### rkf45

2.00625796332792

0.5012864836714865

0.10592998775763712

###### dop853

2.0062579633279194

0.5012864836714864

0.10592998775763719

###### abs error vs dop853

1.2878587085651816e-13

7.2547079454921e-11

3.5096497388864556e-08

###### abs error vs rkf45

1.2922996006636822e-13

7.254719047722347e-11

3.509649731947562e-08

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

6.938893903907228e-17

###### diagnostic resolution threshold

1.4255320219035066e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269717592375

0.5006339789818066

0.10289555175034332

###### rkf45

2.0031269717592384

0.5006339789829141

0.10289555281756263

###### dop853

2.0031269717592384

0.5006339789829141

0.10289555281756269

###### abs error vs dop853

8.881784197001252e-16

1.1074474670635936e-12

1.0672193684335696e-09

###### abs error vs rkf45

8.881784197001252e-16

1.1074474670635936e-12

1.0672193129224183e-09

###### rkf dop disagreement

0.0

0.0

5.551115123125783e-17

###### diagnostic resolution threshold

1.4233073185886542e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

ca779ba324abf121b3b8e8dc51509dc123712838c542cd174c3c8315a8931b81

###### equation sha256

729701d3ab64dd04791d02e22daa7fa4ced0dea9e343c94e101ade67a00c4002

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.6

#### m

1

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

0

#### polynomial

```text
90762076561*h**6/589858204500000 + 88636643*h**5/183756450000 + 120679*h**4/68694000 + 257*h**3/32100 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

257/32100

120679/68694000

88636643/183756450000

90762076561/589858204500000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-107/30

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

257/5350

##### coefficient

257/32100

##### degree

4

##### rhs coefficient

120679/2862250

##### coefficient

120679/68694000

##### degree

5

##### rhs coefficient

88636643/3062607500

##### coefficient

88636643/183756450000

##### degree

6

##### rhs coefficient

90762076561/4915485037500

##### coefficient

90762076561/589858204500000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251260119117194

0.5050609404721458

0.10245580676422876

###### rkf45

2.0251260119117633

0.5050609404782072

0.10245580749422234

###### dop853

2.0251260119117624

0.5050609404782067

0.1024558074942224

###### abs error vs dop853

4.3076653355456074e-14

6.0609295360336546e-12

7.299936349847158e-10

###### abs error vs rkf45

4.39648317751562e-14

6.061373625243505e-12

7.299935794735646e-10

###### rkf dop disagreement

8.881784197001252e-16

4.440892098500626e-16

5.551115123125783e-17

###### diagnostic resolution threshold

1.438938576762725e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531375788335

0.502515122430984

0.10121426283395023

###### rkf45

2.012531375788336

0.5025151224310778

0.1012142628564717

###### dop853

2.0125313757883356

0.5025151224310777

0.10121426285647173

###### abs error vs dop853

4.440892098500626e-16

9.370282327836321e-14

2.2521498554972652e-11

###### abs error vs rkf45

8.881784197001252e-16

9.381384558082573e-14

2.2521470799397036e-11

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4299895495556823e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578281802064

0.5012537667044263

0.10060378017308953

###### rkf45

2.0062578281802064

0.5012537667044279

0.10060378017378885

###### dop853

2.0062578281802064

0.5012537667044278

0.10060378017378888

###### abs error vs dop853

0.0

1.4432899320127035e-15

6.993433609991939e-13

###### abs error vs rkf45

0.0

1.5543122344752192e-15

6.993156054235783e-13

###### rkf dop disagreement

0.0

1.1102230246251565e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.425531925875281e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269550823314

0.5006259399494168

0.10030105948930103

###### rkf45

2.0031269550823314

0.500625939949417

0.10030105948932282

###### dop853

2.0031269550823314

0.5006259399494168

0.10030105948932282

###### abs error vs dop853

0.0

0.0

2.1788126858268697e-14

###### abs error vs rkf45

0.0

1.1102230246251565e-16

2.1788126858268697e-14

###### rkf dop disagreement

0.0

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.423307306738999e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

7ef2d91991e37dc7f882abde91d96c74d8d473d409dd8755cd11663406e6efb4

###### equation sha256

b0ee67bbae1f102fe8dab22ca12ac1fc11b0555e4b08d3d5435c3b7a08cca690

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.6

#### m

3/2

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

0

#### polynomial

```text
-6423107069173*sqrt(2)*h**6/575539484083216000 + 47464357695701*h**6/287769742041608000 - 3598390749*sqrt(2)*h**5/146881248490000 + 59516359899*h**5/117504998792000 - 502953*sqrt(2)*h**4/9596161600 + 173535*h**4/95961616 - 9*sqrt(2)*h**3/97960 + 11899*h**3/1469400 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

-(-11899 + 135*sqrt(2))/1469400

-3*(-5784500 + 167651*sqrt(2))/9596161600

-3*(-99193933165 + 4797854332*sqrt(2))/587524993960000

-(-94928715391402 + 6423107069173*sqrt(2))/575539484083216000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-7/2 - sqrt(2)/20

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

11899/244900 - 27*sqrt(2)/48980

##### coefficient

-(-11899 + 135*sqrt(2))/1469400

##### degree

4

##### rhs coefficient

520605/11995202 - 1508859*sqrt(2)/1199520200

##### coefficient

-3*(-5784500 + 167651*sqrt(2))/9596161600

##### degree

5

##### rhs coefficient

178549079697/5875249939600 - 10795172247*sqrt(2)/7344062424500

##### coefficient

-3*(-99193933165 + 4797854332*sqrt(2))/587524993960000

##### degree

6

##### rhs coefficient

142393073087103/7194243551040200 - 19269321207519*sqrt(2)/14388487102080400

##### coefficient

-(-94928715391402 + 6423107069173*sqrt(2))/575539484083216000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251260069805563

0.5050606416535987

0.1024436153188185

###### rkf45

2.0251260069805976

0.5050606416594203

0.10244361601999151

###### dop853

2.0251260069805976

0.5050606416594206

0.1024436160199915

###### abs error vs dop853

4.1300296516055823e-14

5.821898518831858e-12

7.011729946659884e-10

###### abs error vs rkf45

4.1300296516055823e-14

5.821676474226933e-12

7.011730085437762e-10

###### rkf dop disagreement

0.0

2.220446049250313e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4389385732589216e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.0125313751810463

0.5025150491963453

0.10120834612783891

###### rkf45

2.012531375181047

0.5025150491964351

0.1012083461494737

###### dop853

2.0125313751810467

0.5025150491964352

0.1012083461494737

###### abs error vs dop853

4.440892098500626e-16

8.992806499463768e-14

2.1634791180780155e-11

###### abs error vs rkf45

8.881784197001252e-16

8.981704269217516e-14

2.1634791180780155e-11

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.4299895491241775e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578281048546

0.5012537485754881

0.10060086527060405

###### rkf45

2.0062578281048546

0.5012537485754893

0.10060086527127589

###### dop853

2.0062578281048546

0.5012537485754894

0.10060086527127589

###### abs error vs dop853

0.0

1.3322676295501878e-15

6.718375855641057e-13

###### abs error vs rkf45

0.0

1.2212453270876722e-15

6.718375855641057e-13

###### rkf dop disagreement

0.0

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.4255319258217402e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.003126955072947

0.5006259354394014

0.10029961274228627

###### rkf45

2.003126955072947

0.5006259354394013

0.1002996127423072

###### dop853

2.003126955072947

0.5006259354394014

0.1002996127423072

###### abs error vs dop853

0.0

0.0

2.09277040141842e-14

###### abs error vs rkf45

0.0

1.1102230246251565e-16

2.09277040141842e-14

###### rkf dop disagreement

0.0

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.423307306732331e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

2d7b6d48e127ba017cc3fee02c5261bf4db4025dcc367ebb18cd91bed6c9e890

###### equation sha256

1ef5a41328b8ac2a2a5cf431a0961961d7f5787fc5f5f134a5849b0545ff381d

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.6

#### m

2

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

0

#### polynomial

```text
381330073*h**6/2621592020000 + 5682783*h**5/12250430000 + 7869*h**4/4579600 + 17*h**3/2140 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

17/2140

7869/4579600

5682783/12250430000

381330073/2621592020000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-107/30

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

51/1070

##### coefficient

17/2140

##### degree

4

##### rhs coefficient

23607/572450

##### coefficient

7869/4579600

##### degree

5

##### rhs coefficient

17048349/612521500

##### coefficient

5682783/12250430000

##### degree

6

##### rhs coefficient

1143990219/65539800500

##### coefficient

381330073/2621592020000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.025126003877093

0.5050604533445407

0.10243591272443439

###### rkf45

2.025126003877133

0.5050604533501722

0.10243591340263433

###### dop853

2.025126003877133

0.5050604533501719

0.10243591340263436

###### abs error vs dop853

3.9968028886505635e-14

5.6311622032012565e-12

6.781999684069007e-10

###### abs error vs rkf45

3.9968028886505635e-14

5.631495270108644e-12

6.78199940651325e-10

###### rkf dop disagreement

0.0

3.3306690738754696e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4389385710537774e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.0125313747995976

0.5025150031663813

0.10120462249602814

###### rkf45

2.012531374799598

0.5025150031664684

0.10120462251695626

###### dop853

2.0125313747995976

0.5025150031664684

0.10120462251695628

###### abs error vs dop853

0.0

8.704148513061227e-14

2.0928134225606243e-11

###### abs error vs rkf45

4.440892098500626e-16

8.704148513061227e-14

2.0928120347818435e-11

###### rkf dop disagreement

4.440892098500626e-16

0.0

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4299895488531417e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.006257828057571

0.5012537371958488

0.10059903438017687

###### rkf45

2.0062578280575716

0.5012537371958501

0.1005990343808268

###### dop853

2.006257828057571

0.5012537371958501

0.10059903438082683

###### abs error vs dop853

0.0

1.3322676295501878e-15

6.499661919789901e-13

###### abs error vs rkf45

4.440892098500626e-16

1.3322676295501878e-15

6.499384364033745e-13

###### rkf dop disagreement

4.440892098500626e-16

0.0

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4255319257881433e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269550670614

0.5006259326102861

0.10029870490813912

###### rkf45

2.0031269550670614

0.5006259326102861

0.10029870490815936

###### dop853

2.0031269550670614

0.5006259326102862

0.10029870490815938

###### abs error vs dop853

0.0

1.1102230246251565e-16

2.0261570199409107e-14

###### abs error vs rkf45

0.0

0.0

2.0233814623793478e-14

###### rkf dop disagreement

0.0

1.1102230246251565e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.423307306728149e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

b3c5eb3a96dddb2a3a8210569e2e0714a4fd208e79224b38a9992d825718cabe

###### equation sha256

7e9a303bb3ee92e40f471d00f6d94fb937e510cfe504fa7ce743de47d6778591

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.6

#### m

3

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

0

#### polynomial

```text
1077541127*h**6/7623504300000 + 1632377*h**5/3579110000 + 17201*h**4/10082000 + 169*h**3/21300 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

169/21300

17201/10082000

1632377/3579110000

1077541127/7623504300000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-71/20

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

169/3550

##### coefficient

169/21300

##### degree

4

##### rhs coefficient

51603/1260250

##### coefficient

17201/10082000

##### degree

5

##### rhs coefficient

4897131/178955500

##### coefficient

1632377/3579110000

##### degree

6

##### rhs coefficient

1077541127/63529202500

##### coefficient

1077541127/7623504300000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251260025919593

0.5050603746148682

0.1024326317007503

###### rkf45

2.025126002591997

0.5050603746202718

0.10243263235149926

###### dop853

2.025126002591998

0.5050603746202719

0.10243263235149923

###### abs error vs dop853

3.863576125695545e-14

5.403677505455562e-12

6.507489269669264e-10

###### abs error vs rkf45

3.774758283725532e-14

5.403566483153099e-12

6.50748954722502e-10

###### rkf dop disagreement

8.881784197001252e-16

1.1102230246251565e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.438938570140634e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531374643942

0.5025149842915042

0.10120308085213524

###### rkf45

2.012531374643942

0.5025149842915876

0.10120308087221945

###### dop853

2.0125313746439426

0.5025149842915878

0.10120308087221945

###### abs error vs dop853

4.440892098500626e-16

8.359979375427429e-14

2.0084212071225238e-11

###### abs error vs rkf45

0.0

8.337774914934926e-14

2.0084212071225238e-11

###### rkf dop disagreement

4.440892098500626e-16

2.220446049250313e-16

0.0

###### diagnostic resolution threshold

1.429989548742542e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578280384185

0.5012537325750577

0.1005982872979246

###### rkf45

2.006257828038418

0.5012537325750588

0.10059828729854836

###### dop853

2.0062578280384185

0.5012537325750589

0.10059828729854838

###### abs error vs dop853

0.0

1.2212453270876722e-15

6.237788063856442e-13

###### abs error vs rkf45

4.440892098500626e-16

1.1102230246251565e-15

6.237649285978364e-13

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4255319257745345e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.003126955064686

0.500625931467146

0.10029833718372858

###### rkf45

2.003126955064685

0.5006259314671458

0.10029833718374802

###### dop853

2.003126955064686

0.500625931467146

0.10029833718374802

###### abs error vs dop853

0.0

0.0

1.9442780718748054e-14

###### abs error vs rkf45

8.881784197001252e-16

1.1102230246251565e-16

1.9442780718748054e-14

###### rkf dop disagreement

8.881784197001252e-16

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.4233073067264612e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

15718ea5f251e4c818d3b3750fe974daaa973179d63c787e03b6e0f278be458a

###### equation sha256

d781aee509f1ddc72940d424049d1bee7ca41db4d9c694b83d6f7b1e60c4e06c

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.6

#### m

4

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

0

#### polynomial

```text
16011886241*h**6/113622926400000 + 653183*h**5/1429219200 + 23099*h**4/13483200 + 253*h**3/31800 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

253/31800

23099/13483200

653183/1429219200

16011886241/113622926400000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-53/15

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

253/5300

##### coefficient

253/31800

##### degree

4

##### rhs coefficient

23099/561800

##### coefficient

23099/13483200

##### degree

5

##### rhs coefficient

653183/23820320

##### coefficient

653183/1429219200

##### degree

6

##### rhs coefficient

16011886241/946857720000

##### coefficient

16011886241/113622926400000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251260053491826

0.5050605409419406

0.10243935649715777

###### rkf45

2.025126005349221

0.5050605409472906

0.1024393571414239

###### dop853

2.025126005349221

0.5050605409472905

0.10243935714142388

###### abs error vs dop853

3.8191672047105385e-14

5.349831688761242e-12

6.442661126815352e-10

###### abs error vs rkf45

3.8191672047105385e-14

5.349942711063704e-12

6.44266126559323e-10

###### rkf dop disagreement

0.0

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4389385720997586e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531374985811

0.5025150254267675

0.10120638946421245

###### rkf45

2.0125313749858122

0.5025150254268502

0.10120638948409855

###### dop853

2.012531374985812

0.5025150254268502

0.10120638948409855

###### abs error vs dop853

8.881784197001252e-16

8.271161533457416e-14

1.988609277248088e-11

###### abs error vs rkf45

1.3322676295501878e-15

8.271161533457416e-14

1.988609277248088e-11

###### rkf dop disagreement

4.440892098500626e-16

0.0

0.0

###### diagnostic resolution threshold

1.4299895489854548e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578280809786

0.501253742803387

0.10059992826063775

###### rkf45

2.006257828080979

0.5012537428033881

0.10059992826125543

###### dop853

2.006257828080979

0.5012537428033882

0.10059992826125543

###### abs error vs dop853

4.440892098500626e-16

1.2212453270876722e-15

6.176725797502058e-13

###### abs error vs rkf45

4.440892098500626e-16

1.1102230246251565e-15

6.176725797502058e-13

###### rkf dop disagreement

0.0

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.4255319258047756e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.003126955069995

0.5006259340173134

0.10029915434256152

###### rkf45

2.0031269550699955

0.5006259340173133

0.10029915434258078

###### dop853

2.003126955069995

0.5006259340173134

0.10029915434258078

###### abs error vs dop853

0.0

0.0

1.9262369477246466e-14

###### abs error vs rkf45

4.440892098500626e-16

1.1102230246251565e-16

1.9262369477246466e-14

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.4233073067302336e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

8c7618d96c16bc15068de1e3e9b0c38975deebc36b8ea0eeac4db4b19349fcd9

###### equation sha256

1f21c87e112899ca628c8b49754c634a08df7cb047e4b675aabc52d70b345bcf

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.8

#### m

1

#### order

6

#### z0

0

#### initial jet

0

1

1/10

#### g

1

#### kappa

1/30

#### alpha

1

#### alpha3

1

#### polynomial

```text
h**2/20 + h
```

#### coefficients

0

1

1/20

0

0

0

0

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

1

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1

#### gradient at initial

1

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

0

##### coefficient

0

##### degree

4

##### rhs coefficient

0

##### coefficient

0

##### degree

5

##### rhs coefficient

0

##### coefficient

0

##### degree

6

##### rhs coefficient

0

##### coefficient

0

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.2

###### z

0.2

###### polynomial

0.202

1.02

0.1

###### rkf45

0.20199999999999985

1.0199999999999978

0.1

###### dop853

0.20199999999999987

1.0199999999999994

0.1

###### abs error vs dop853

1.3877787807814457e-16

6.661338147750939e-16

0.0

###### abs error vs rkf45

1.6653345369377348e-16

2.220446049250313e-15

0.0

###### rkf dop disagreement

2.7755575615628914e-17

1.5543122344752192e-15

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

1.554312234475219e-14

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.1

###### z

0.1

###### polynomial

0.1005

1.01

0.1

###### rkf45

0.10049999999999996

1.009999999999999

0.1

###### dop853

0.10049999999999995

1.009999999999999

0.1

###### abs error vs dop853

5.551115123125783e-17

1.1102230246251565e-15

0.0

###### abs error vs rkf45

4.163336342344337e-17

1.1102230246251565e-15

0.0

###### rkf dop disagreement

1.3877787807814457e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.176481631177004e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.05

###### z

0.05

###### polynomial

0.050125

1.005

0.1

###### rkf45

0.05012499999999999

1.0049999999999994

0.1

###### dop853

0.05012499999999998

1.0049999999999994

0.1

###### abs error vs dop853

2.0816681711721685e-17

4.440892098500626e-16

0.0

###### abs error vs rkf45

1.3877787807814457e-17

4.440892098500626e-16

0.0

###### rkf dop disagreement

6.938893903907228e-18

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.140954494389003e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.025

###### z

0.025

###### polynomial

0.02503125

1.0025

0.1

###### rkf45

0.025031249999999998

1.0024999999999997

0.1

###### dop853

0.02503124999999997

1.0024999999999997

0.1

###### abs error vs dop853

3.122502256758253e-17

2.220446049250313e-16

0.0

###### abs error vs rkf45

3.469446951953614e-18

2.220446049250313e-16

0.0

###### rkf dop disagreement

2.7755575615628914e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.123190925995002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

###### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.8

#### m

3/2

#### order

6

#### z0

0

#### initial jet

0

1

1/10

#### g

1

#### kappa

1/30

#### alpha

1

#### alpha3

1

#### polynomial

```text
h**2/20 + h
```

#### coefficients

0

1

1/20

0

0

0

0

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

1

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1

#### gradient at initial

1

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

0

##### coefficient

0

##### degree

4

##### rhs coefficient

0

##### coefficient

0

##### degree

5

##### rhs coefficient

0

##### coefficient

0

##### degree

6

##### rhs coefficient

0

##### coefficient

0

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.2

###### z

0.2

###### polynomial

0.202

1.02

0.1

###### rkf45

0.20199999999999985

1.0199999999999978

0.1

###### dop853

0.20199999999999987

1.0199999999999994

0.1

###### abs error vs dop853

1.3877787807814457e-16

6.661338147750939e-16

0.0

###### abs error vs rkf45

1.6653345369377348e-16

2.220446049250313e-15

0.0

###### rkf dop disagreement

2.7755575615628914e-17

1.5543122344752192e-15

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

1.554312234475219e-14

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.1

###### z

0.1

###### polynomial

0.1005

1.01

0.1

###### rkf45

0.10049999999999996

1.009999999999999

0.1

###### dop853

0.10049999999999995

1.009999999999999

0.1

###### abs error vs dop853

5.551115123125783e-17

1.1102230246251565e-15

0.0

###### abs error vs rkf45

4.163336342344337e-17

1.1102230246251565e-15

0.0

###### rkf dop disagreement

1.3877787807814457e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.176481631177004e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.05

###### z

0.05

###### polynomial

0.050125

1.005

0.1

###### rkf45

0.05012499999999999

1.0049999999999994

0.1

###### dop853

0.05012499999999998

1.0049999999999994

0.1

###### abs error vs dop853

2.0816681711721685e-17

4.440892098500626e-16

0.0

###### abs error vs rkf45

1.3877787807814457e-17

4.440892098500626e-16

0.0

###### rkf dop disagreement

6.938893903907228e-18

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.140954494389003e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.025

###### z

0.025

###### polynomial

0.02503125

1.0025

0.1

###### rkf45

0.025031249999999998

1.0024999999999997

0.1

###### dop853

0.02503124999999997

1.0024999999999997

0.1

###### abs error vs dop853

3.122502256758253e-17

2.220446049250313e-16

0.0

###### abs error vs rkf45

3.469446951953614e-18

2.220446049250313e-16

0.0

###### rkf dop disagreement

2.7755575615628914e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.123190925995002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

###### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.8

#### m

2

#### order

6

#### z0

0

#### initial jet

0

1

1/10

#### g

1

#### kappa

1/30

#### alpha

1

#### alpha3

1

#### polynomial

```text
h**2/20 + h
```

#### coefficients

0

1

1/20

0

0

0

0

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

1

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1

#### gradient at initial

1

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

0

##### coefficient

0

##### degree

4

##### rhs coefficient

0

##### coefficient

0

##### degree

5

##### rhs coefficient

0

##### coefficient

0

##### degree

6

##### rhs coefficient

0

##### coefficient

0

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.2

###### z

0.2

###### polynomial

0.202

1.02

0.1

###### rkf45

0.20199999999999985

1.0199999999999978

0.1

###### dop853

0.20199999999999987

1.0199999999999994

0.1

###### abs error vs dop853

1.3877787807814457e-16

6.661338147750939e-16

0.0

###### abs error vs rkf45

1.6653345369377348e-16

2.220446049250313e-15

0.0

###### rkf dop disagreement

2.7755575615628914e-17

1.5543122344752192e-15

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

1.554312234475219e-14

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.1

###### z

0.1

###### polynomial

0.1005

1.01

0.1

###### rkf45

0.10049999999999996

1.009999999999999

0.1

###### dop853

0.10049999999999995

1.009999999999999

0.1

###### abs error vs dop853

5.551115123125783e-17

1.1102230246251565e-15

0.0

###### abs error vs rkf45

4.163336342344337e-17

1.1102230246251565e-15

0.0

###### rkf dop disagreement

1.3877787807814457e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.176481631177004e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.05

###### z

0.05

###### polynomial

0.050125

1.005

0.1

###### rkf45

0.05012499999999999

1.0049999999999994

0.1

###### dop853

0.05012499999999998

1.0049999999999994

0.1

###### abs error vs dop853

2.0816681711721685e-17

4.440892098500626e-16

0.0

###### abs error vs rkf45

1.3877787807814457e-17

4.440892098500626e-16

0.0

###### rkf dop disagreement

6.938893903907228e-18

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.140954494389003e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.025

###### z

0.025

###### polynomial

0.02503125

1.0025

0.1

###### rkf45

0.025031249999999998

1.0024999999999997

0.1

###### dop853

0.02503124999999997

1.0024999999999997

0.1

###### abs error vs dop853

3.122502256758253e-17

2.220446049250313e-16

0.0

###### abs error vs rkf45

3.469446951953614e-18

2.220446049250313e-16

0.0

###### rkf dop disagreement

2.7755575615628914e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.123190925995002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

###### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.8

#### m

3

#### order

6

#### z0

0

#### initial jet

0

1

1/10

#### g

1

#### kappa

1/30

#### alpha

1

#### alpha3

1

#### polynomial

```text
h**2/20 + h
```

#### coefficients

0

1

1/20

0

0

0

0

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

1

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1

#### gradient at initial

1

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

0

##### coefficient

0

##### degree

4

##### rhs coefficient

0

##### coefficient

0

##### degree

5

##### rhs coefficient

0

##### coefficient

0

##### degree

6

##### rhs coefficient

0

##### coefficient

0

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.2

###### z

0.2

###### polynomial

0.202

1.02

0.1

###### rkf45

0.20199999999999985

1.0199999999999978

0.1

###### dop853

0.20199999999999987

1.0199999999999994

0.1

###### abs error vs dop853

1.3877787807814457e-16

6.661338147750939e-16

0.0

###### abs error vs rkf45

1.6653345369377348e-16

2.220446049250313e-15

0.0

###### rkf dop disagreement

2.7755575615628914e-17

1.5543122344752192e-15

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

1.554312234475219e-14

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.1

###### z

0.1

###### polynomial

0.1005

1.01

0.1

###### rkf45

0.10049999999999996

1.009999999999999

0.1

###### dop853

0.10049999999999995

1.009999999999999

0.1

###### abs error vs dop853

5.551115123125783e-17

1.1102230246251565e-15

0.0

###### abs error vs rkf45

4.163336342344337e-17

1.1102230246251565e-15

0.0

###### rkf dop disagreement

1.3877787807814457e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.176481631177004e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.05

###### z

0.05

###### polynomial

0.050125

1.005

0.1

###### rkf45

0.05012499999999999

1.0049999999999994

0.1

###### dop853

0.05012499999999998

1.0049999999999994

0.1

###### abs error vs dop853

2.0816681711721685e-17

4.440892098500626e-16

0.0

###### abs error vs rkf45

1.3877787807814457e-17

4.440892098500626e-16

0.0

###### rkf dop disagreement

6.938893903907228e-18

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.140954494389003e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.025

###### z

0.025

###### polynomial

0.02503125

1.0025

0.1

###### rkf45

0.025031249999999998

1.0024999999999997

0.1

###### dop853

0.02503124999999997

1.0024999999999997

0.1

###### abs error vs dop853

3.122502256758253e-17

2.220446049250313e-16

0.0

###### abs error vs rkf45

3.469446951953614e-18

2.220446049250313e-16

0.0

###### rkf dop disagreement

2.7755575615628914e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.123190925995002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

###### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.8

#### m

4

#### order

6

#### z0

0

#### initial jet

0

1

1/10

#### g

1

#### kappa

1/30

#### alpha

1

#### alpha3

1

#### polynomial

```text
h**2/20 + h
```

#### coefficients

0

1

1/20

0

0

0

0

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

1

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

1

#### gradient at initial

1

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

0

##### coefficient

0

##### degree

4

##### rhs coefficient

0

##### coefficient

0

##### degree

5

##### rhs coefficient

0

##### coefficient

0

##### degree

6

##### rhs coefficient

0

##### coefficient

0

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.2

###### z

0.2

###### polynomial

0.202

1.02

0.1

###### rkf45

0.20199999999999985

1.0199999999999978

0.1

###### dop853

0.20199999999999987

1.0199999999999994

0.1

###### abs error vs dop853

1.3877787807814457e-16

6.661338147750939e-16

0.0

###### abs error vs rkf45

1.6653345369377348e-16

2.220446049250313e-15

0.0

###### rkf dop disagreement

2.7755575615628914e-17

1.5543122344752192e-15

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

1.554312234475219e-14

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.1

###### z

0.1

###### polynomial

0.1005

1.01

0.1

###### rkf45

0.10049999999999996

1.009999999999999

0.1

###### dop853

0.10049999999999995

1.009999999999999

0.1

###### abs error vs dop853

5.551115123125783e-17

1.1102230246251565e-15

0.0

###### abs error vs rkf45

4.163336342344337e-17

1.1102230246251565e-15

0.0

###### rkf dop disagreement

1.3877787807814457e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.176481631177004e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.05

###### z

0.05

###### polynomial

0.050125

1.005

0.1

###### rkf45

0.05012499999999999

1.0049999999999994

0.1

###### dop853

0.05012499999999998

1.0049999999999994

0.1

###### abs error vs dop853

2.0816681711721685e-17

4.440892098500626e-16

0.0

###### abs error vs rkf45

1.3877787807814457e-17

4.440892098500626e-16

0.0

###### rkf dop disagreement

6.938893903907228e-18

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.140954494389003e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.025

###### z

0.025

###### polynomial

0.02503125

1.0025

0.1

###### rkf45

0.025031249999999998

1.0024999999999997

0.1

###### dop853

0.02503124999999997

1.0024999999999997

0.1

###### abs error vs dop853

3.122502256758253e-17

2.220446049250313e-16

0.0

###### abs error vs rkf45

3.469446951953614e-18

2.220446049250313e-16

0.0

###### rkf dop disagreement

2.7755575615628914e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.123190925995002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

###### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.9

#### m

1

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
90762076561*h**6/589858204500000 + 88636643*h**5/183756450000 + 120679*h**4/68694000 + 257*h**3/32100 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

257/32100

120679/68694000

88636643/183756450000

90762076561/589858204500000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-107/30

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

257/5350

##### coefficient

257/32100

##### degree

4

##### rhs coefficient

120679/2862250

##### coefficient

120679/68694000

##### degree

5

##### rhs coefficient

88636643/3062607500

##### coefficient

88636643/183756450000

##### degree

6

##### rhs coefficient

90762076561/4915485037500

##### coefficient

90762076561/589858204500000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251260119117194

0.5050609404721458

0.10245580676422876

###### rkf45

2.0251260119117633

0.5050609404782072

0.10245580749422234

###### dop853

2.0251260119117624

0.5050609404782067

0.1024558074942224

###### abs error vs dop853

4.3076653355456074e-14

6.0609295360336546e-12

7.299936349847158e-10

###### abs error vs rkf45

4.39648317751562e-14

6.061373625243505e-12

7.299935794735646e-10

###### rkf dop disagreement

8.881784197001252e-16

4.440892098500626e-16

5.551115123125783e-17

###### diagnostic resolution threshold

1.438938576762725e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531375788335

0.502515122430984

0.10121426283395023

###### rkf45

2.012531375788336

0.5025151224310778

0.1012142628564717

###### dop853

2.0125313757883356

0.5025151224310777

0.10121426285647173

###### abs error vs dop853

4.440892098500626e-16

9.370282327836321e-14

2.2521498554972652e-11

###### abs error vs rkf45

8.881784197001252e-16

9.381384558082573e-14

2.2521470799397036e-11

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4299895495556823e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578281802064

0.5012537667044263

0.10060378017308953

###### rkf45

2.0062578281802064

0.5012537667044279

0.10060378017378885

###### dop853

2.0062578281802064

0.5012537667044278

0.10060378017378888

###### abs error vs dop853

0.0

1.4432899320127035e-15

6.993433609991939e-13

###### abs error vs rkf45

0.0

1.5543122344752192e-15

6.993156054235783e-13

###### rkf dop disagreement

0.0

1.1102230246251565e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.425531925875281e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269550823314

0.5006259399494168

0.10030105948930103

###### rkf45

2.0031269550823314

0.500625939949417

0.10030105948932282

###### dop853

2.0031269550823314

0.5006259399494168

0.10030105948932282

###### abs error vs dop853

0.0

0.0

2.1788126858268697e-14

###### abs error vs rkf45

0.0

1.1102230246251565e-16

2.1788126858268697e-14

###### rkf dop disagreement

0.0

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.423307306738999e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

7ef2d91991e37dc7f882abde91d96c74d8d473d409dd8755cd11663406e6efb4

###### equation sha256

b0ee67bbae1f102fe8dab22ca12ac1fc11b0555e4b08d3d5435c3b7a08cca690

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.9

#### m

3/2

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
-31847909816123743*sqrt(6)*h**6/3484994863510753200000 + 1446091659409006021*h**6/8712487158776883000000 - 4959446329*sqrt(6)*h**5/247255345513125 + 40219760267647*h**5/79121710564200000 - 2225513*sqrt(6)*h**4/51734669760 + 195230437*h**4/107780562000 - 67*sqrt(6)*h**3/880920 + 793*h**3/97880 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

-(-7137 + 67*sqrt(6))/880920

-(-2342765244 + 55637825*sqrt(6))/1293366744000

-(-40219760267647 + 1587022825280*sqrt(6))/79121710564200000

-(-2892183318818012042 + 159239549080618715*sqrt(6))/17424974317553766000000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-7/2 - sqrt(6)/20

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

2379/48940 - 67*sqrt(6)/146820

##### coefficient

-(-7137 + 67*sqrt(6))/880920

##### degree

4

##### rhs coefficient

195230437/4490856750 - 2225513*sqrt(6)/2155611240

##### coefficient

-(-2342765244 + 55637825*sqrt(6))/1293366744000

##### degree

5

##### rhs coefficient

40219760267647/1318695176070000 - 19837785316*sqrt(6)/16483689700875

##### coefficient

-(-40219760267647 + 1587022825280*sqrt(6))/79121710564200000

##### degree

6

##### rhs coefficient

1446091659409006021/72604059656474025000 - 31847909816123743*sqrt(6)/29041623862589610000

##### coefficient

-(-2892183318818012042 + 159239549080618715*sqrt(6))/17424974317553766000000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.025126000240327

0.505060233543921

0.10242699188516659

###### rkf45

2.025126000240366

0.5050602335494648

0.10242699255282617

###### dop853

2.025126000240366

0.5050602335494649

0.10242699255282617

###### abs error vs dop853

3.907985046680551e-14

5.543898673465719e-12

6.676595804000485e-10

###### abs error vs rkf45

3.907985046680551e-14

5.543787651163257e-12

6.676595804000485e-10

###### rkf dop disagreement

0.0

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.438938568469699e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531374349937

0.5025149490116139

0.10120025868288891

###### rkf45

2.0125313743499373

0.5025149490116995

0.10120025870349249

###### dop853

2.012531374349937

0.5025149490116997

0.10120025870349249

###### abs error vs dop853

0.0

8.58202398035246e-14

2.0603574402144886e-11

###### abs error vs rkf45

4.440892098500626e-16

8.559819519859957e-14

2.0603574402144886e-11

###### rkf dop disagreement

4.440892098500626e-16

2.220446049250313e-16

0.0

###### diagnostic resolution threshold

1.4299895485336385e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578280016674

0.5012537237547917

0.10059687604714333

###### rkf45

2.006257828001668

0.5012537237547929

0.1005968760477832

###### dop853

2.0062578280016674

0.501253723754793

0.10059687604778318

###### abs error vs dop853

0.0

1.3322676295501878e-15

6.398492846670933e-13

###### abs error vs rkf45

4.440892098500626e-16

1.2212453270876722e-15

6.398631624549012e-13

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4255319257484213e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269550600923

0.5006259292621167

0.10029763156453643

###### rkf45

2.003126955060092

0.5006259292621167

0.10029763156455634

###### dop853

2.0031269550600923

0.5006259292621167

0.10029763156455636

###### abs error vs dop853

0.0

0.0

1.992850329202156e-14

###### abs error vs rkf45

4.440892098500626e-16

0.0

1.9914625504213745e-14

###### rkf dop disagreement

4.440892098500626e-16

0.0

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4233073067231972e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

a79d852931cd7c8786097e7f0a35de1f8f5d2e535147bd83ce2396ca72276429

###### equation sha256

fc9ca7d0e6f7ebc0a805b348a6c573deabdc42b38464c0ccd9a96b5519d2ab06

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.9

#### m

2

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
21376667*h**6/166333500000 + 7069*h**5/16650000 + 217*h**4/133200 + 7*h**3/900 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

7/900

217/133200

7069/16650000

21376667/166333500000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-37/10

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

7/150

##### coefficient

7/900

##### degree

4

##### rhs coefficient

217/5550

##### coefficient

217/133200

##### degree

5

##### rhs coefficient

7069/277500

##### coefficient

7069/16650000

##### degree

6

##### rhs coefficient

21376667/1386112500

##### coefficient

21376667/166333500000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251259825389636

0.5050591614065097

0.10238329271553874

###### rkf45

2.0251259825389987

0.5050591614113114

0.1023832932937796

###### dop853

2.025125982538998

0.5050591614113117

0.10238329329377963

###### abs error vs dop853

3.419486915845482e-14

4.801936626108727e-12

5.782408857291088e-10

###### abs error vs rkf45

3.5083047578154947e-14

4.8016035592013395e-12

5.782408579735332e-10

###### rkf dop disagreement

8.881784197001252e-16

3.3306690738754696e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4389385558921204e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531372168334

0.5025146859906618

0.10117901931761906

###### rkf45

2.012531372168334

0.5025146859907359

0.10117901933547037

###### dop853

2.012531372168334

0.5025146859907361

0.10117901933547038

###### abs error vs dop853

0.0

7.427392034742297e-14

1.7851317646311315e-11

###### abs error vs rkf45

0.0

7.405187574249794e-14

1.7851303768523508e-11

###### rkf dop disagreement

0.0

2.220446049250313e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4299895469835164e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.006257827730876

0.5012536586129667

0.10058640462913235

###### rkf45

2.006257827730876

0.5012536586129677

0.10058640462968686

###### dop853

2.006257827730876

0.5012536586129679

0.10058640462968685

###### abs error vs dop853

0.0

1.2212453270876722e-15

5.545008896490344e-13

###### abs error vs rkf45

0.0

9.992007221626409e-16

5.545147674368422e-13

###### rkf dop disagreement

0.0

2.220446049250313e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4255319255560124e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269550263615

0.5006259130525262

0.10029243239989814

###### rkf45

2.0031269550263615

0.5006259130525262

0.10029243239991543

###### dop853

2.0031269550263615

0.5006259130525264

0.10029243239991543

###### abs error vs dop853

0.0

1.1102230246251565e-16

1.7291723608536813e-14

###### abs error vs rkf45

0.0

0.0

1.7291723608536813e-14

###### rkf dop disagreement

0.0

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.42330730669923e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

664f20a71e4818a1fd4517866a9af7fa1b1e65ee974984e3abb73b64a13edd21

###### equation sha256

541bd41e0e32a4fb8c19aee70935beb50a4d9cdb6abaf4c0df0a085c083a8fe0

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.9

#### m

3

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
14467743241*h**6/175275364500000 + 23103299*h**5/73955850000 + 10247*h**4/7489200 + 173*h**3/23700 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

173/23700

10247/7489200

23103299/73955850000

14467743241/175275364500000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-79/20

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

173/3950

##### coefficient

173/23700

##### degree

4

##### rhs coefficient

10247/312050

##### coefficient

10247/7489200

##### degree

5

##### rhs coefficient

23103299/1232597500

##### coefficient

23103299/73955850000

##### degree

6

##### rhs coefficient

14467743241/1460628037500

##### coefficient

14467743241/175275364500000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251259210976507

0.5050554408709601

0.1022317169851667

###### rkf45

2.0251259210976693

0.5050554408736493

0.10223171730888114

###### dop853

2.02512592109767

0.5050554408736495

0.10223171730888117

###### abs error vs dop853

1.9539925233402755e-14

2.6894042548519792e-12

3.237144718948315e-10

###### abs error vs rkf45

1.865174681370263e-14

2.689182210247054e-12

3.237144441392559e-10

###### rkf dop disagreement

8.881784197001252e-16

2.220446049250313e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4389385122354314e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.0125313645934457

0.5025137728386481

0.10110529707597078

###### rkf45

2.0125313645934453

0.5025137728386896

0.10110529708597979

###### dop853

2.0125313645934457

0.5025137728386897

0.1011052970859798

###### abs error vs dop853

0.0

4.163336342344337e-14

1.000902138947879e-11

###### abs error vs rkf45

4.440892098500626e-16

4.1522341120980855e-14

1.0009007511690982e-11

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4299895416012346e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578267904883

0.5012534324048512

0.10055004606198273

###### rkf45

2.0062578267904883

0.5012534324048518

0.10055004606229385

###### dop853

2.0062578267904883

0.501253432404852

0.10055004606229388

###### abs error vs dop853

0.0

7.771561172376096e-16

3.1115388043900793e-13

###### abs error vs rkf45

0.0

5.551115123125783e-16

3.111261248633923e-13

###### rkf dop disagreement

0.0

2.220446049250313e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4255319248878267e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269549092143

0.5006258567578608

0.1002743770674107

###### rkf45

2.0031269549092148

0.5006258567578608

0.10027437706742037

###### dop853

2.0031269549092143

0.5006258567578609

0.10027437706742039

###### abs error vs dop853

0.0

1.1102230246251565e-16

9.686695889854491e-15

###### abs error vs rkf45

4.440892098500626e-16

0.0

9.672818102046676e-15

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.423307306615992e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

846874f12121c78769dead4a3b61f38fdcfef9a03442cc4325ed20091843a88c

###### equation sha256

32b928ee12fee2a62946e8a63e8e094c1714b836bcc4e22c6ad2cc9a1fa92865

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### case

3.9

#### m

4

#### order

6

#### z0

1

#### initial jet

2

1/2

1/10

#### g

1

#### kappa

1/30

#### alpha

-1

#### alpha3

1

#### polynomial

```text
436121809*h**6/16866432000000 + 1901011*h**5/12777600000 + 3617*h**4/3872000 + 17*h**3/2640 + h**2/20 + h/2 + 2
```

#### coefficients

2

1/2

1/20

17/2640

3617/3872000

1901011/12777600000

436121809/16866432000000

#### verification

##### passed

True

##### through degree

3

##### residual coefficients

0

0

0

0

##### residual remainder order

4

#### leading at initial

-22/5

#### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

#### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

#### velocity at initial

3/2

#### gradient at initial

1/2

#### status

regular_analytic_germ

#### recurrence

##### degree

3

##### rhs coefficient

17/440

##### coefficient

17/2640

##### degree

4

##### rhs coefficient

10851/484000

##### coefficient

3617/3872000

##### degree

5

##### rhs coefficient

1901011/212960000

##### coefficient

1901011/12777600000

##### degree

6

##### rhs coefficient

436121809/140553600000

##### coefficient

436121809/16866432000000

#### formal remainders

##### F

7

##### F prime

6

##### F double prime

5

#### comparison

##### status

existing_grid_nodes_only

##### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251258108095302

0.5050487672235854

0.10196021924904682

###### rkf45

2.025125810809534

0.505048767224124

0.10196021931380626

###### dop853

2.0251258108095342

0.5050487672241241

0.10196021931380625

###### abs error vs dop853

3.9968028886505635e-15

5.38680211548126e-13

6.475943392647565e-11

###### abs error vs rkf45

3.552713678800501e-15

5.385691892456634e-13

6.475944780426346e-11

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4389384338709975e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531350981889

0.5025121325396413

0.10097296195590388

###### rkf45

2.012531350981889

0.5025121325396495

0.10097296195791397

###### dop853

2.012531350981889

0.5025121325396498

0.10097296195791396

###### abs error vs dop853

0.0

8.43769498715119e-15

2.0100726638716537e-12

###### abs error vs rkf45

0.0

8.215650382226158e-15

2.0100865416594615e-12

###### rkf dop disagreement

0.0

2.220446049250313e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4299895319296418e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.006257825099793

0.5012530257821064

0.10048471189329224

###### rkf45

2.006257825099793

0.5012530257821065

0.10048471189335488

###### dop853

2.0062578250997927

0.5012530257821066

0.10048471189335484

###### abs error vs dop853

4.440892098500626e-16

2.220446049250313e-16

6.260270080105101e-14

###### abs error vs rkf45

0.0

1.1102230246251565e-16

6.264433416447446e-14

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

4.163336342344337e-17

###### diagnostic resolution threshold

1.4255319236865153e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269546985446

0.5006257555298624

0.10024191587968628

###### rkf45

2.003126954698545

0.5006257555298624

0.10024191587968828

###### dop853

2.0031269546985446

0.5006257555298624

0.10024191587968825

###### abs error vs dop853

0.0

0.0

1.970645868709653e-15

###### abs error vs rkf45

4.440892098500626e-16

0.0

1.9984014443252818e-15

###### rkf dop disagreement

4.440892098500626e-16

0.0

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4233073064663022e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

##### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

c9052ada042b51800165bc1edffc91878e253f1fcb226b73e179341a0d964d6e

###### equation sha256

f1d4adbe163db30e4bb2f60bb9658679e7c1b4e12bef962c28aa261df595b301

##### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

### nine rows

#### 3.1

##### case

3.1

##### m

3

##### order

6

##### z0

1

##### initial jet

2

1/2

1/10

##### g

1

##### kappa

1/30

##### alpha

-1

##### alpha3

1

##### polynomial

Not applicable / not supplied.

##### coefficients

(none)

##### verification

Not applicable / not supplied.

##### leading at initial

Not applicable / not supplied.

##### assumptions

printed scalar equation

real local chart

##### local existence

Not applicable / not supplied.

##### status

outside_positive_chart

##### reason

stationary phi=F(s) has phi_t=0; arbitrary stationary profiles form an identity family outside p>0

#### 3.2

##### case

3.2

##### m

3

##### order

6

##### z0

1

##### initial jet

2

1/2

1/10

##### g

1

##### kappa

1/30

##### alpha

-1

##### alpha3

1

##### polynomial

Not applicable / not supplied.

##### coefficients

(none)

##### verification

Not applicable / not supplied.

##### leading at initial

Not applicable / not supplied.

##### assumptions

printed scalar equation

real local chart

##### local existence

Not applicable / not supplied.

##### status

undefined_chart

##### reason

phi_s=0 makes the printed scalar PDE undefined

#### 3.3

##### case

3.3

##### m

3

##### order

6

##### z0

1

##### initial jet

2

1/2

1/10

##### g

1

##### kappa

1/30

##### alpha

-1

##### alpha3

1

##### polynomial

Not applicable / not supplied.

##### coefficients

(none)

##### verification

Not applicable / not supplied.

##### leading at initial

Not applicable / not supplied.

##### assumptions

printed scalar equation

real local chart

##### local existence

Not applicable / not supplied.

##### status

no_invariant_graph

##### reason

vertical translation requires the impossible graph equation 1=0

#### 3.4

##### case

3.4

##### m

3

##### order

6

##### z0

1

##### initial jet

2

1/2

1/10

##### g

1

##### kappa

1/30

##### alpha

-1

##### alpha3

1

##### polynomial

```text
97895097811*h**6/43818841125000 - 13543709*h**5/12325975000 + 41037*h**4/6241000 - 11*h**3/2370 + h**2/20 + h/2 + 2
```

##### coefficients

2

1/2

1/20

-11/2370

41037/6241000

-13543709/12325975000

97895097811/43818841125000

##### verification

###### passed

True

###### through degree

3

###### residual coefficients

0

0

0

0

###### residual remainder order

4

##### leading at initial

79/20

##### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

##### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

##### velocity at initial

3/2

##### gradient at initial

1/2

##### status

regular_analytic_germ

##### recurrence

###### degree

3

###### rhs coefficient

-11/395

###### coefficient

-11/2370

###### degree

4

###### rhs coefficient

123111/780125

###### coefficient

41037/6241000

###### degree

5

###### rhs coefficient

-40631127/616298750

###### coefficient

-13543709/12325975000

###### degree

6

###### rhs coefficient

97895097811/365157009375

###### coefficient

97895097811/43818841125000

##### formal remainders

###### F

7

###### F prime

6

###### F double prime

5

##### comparison

###### status

existing_grid_nodes_only

###### samples

###### offset

0.19999999999999996

###### z

1.2

###### polynomial

2.101973181187445

0.5196489495023321

0.09751799536427673

###### rkf45

2.1019731779032513

0.5196488481223264

0.09751549961164248

###### dop853

2.1019731779032513

0.5196488481223265

0.09751549961164271

###### abs error vs dop853

3.284193805797031e-09

1.0138000561266125e-07

2.495752634015802e-06

###### abs error vs rkf45

3.284193805797031e-09

1.0138000572368355e-07

2.4957526342517244e-06

###### rkf dop disagreement

0.0

1.1102230246251565e-16

2.3592239273284576e-16

###### diagnostic resolution threshold

1.493541772321728e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.10000000000000009

###### z

1.1

###### polynomial

2.0504960074347904

0.5098866456960555

0.09798896287854608

###### rkf45

2.0504960073985847

0.5098866432672743

0.09798882558432849

###### dop853

2.050496007398585

0.5098866432672743

0.09798882558432861

###### abs error vs dop853

3.6205261011446055e-11

2.428781176178063e-09

1.372942174671099e-07

###### abs error vs rkf45

3.6205705100655905e-11

2.428781176178063e-09

1.3729421759201e-07

###### rkf dop disagreement

4.440892098500626e-16

0.0

1.249000902703301e-16

###### diagnostic resolution threshold

1.4569650427621533e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251244606189367

0.5049684474192938

0.09880252849945384

###### rkf45

2.0251244606186116

0.5049684473747253

0.098802523284478

###### dop853

2.0251244606186125

0.5049684473747255

0.09880252328447807

###### abs error vs dop853

3.241851231905457e-13

4.4568349011342434e-11

5.2149757706621e-09

###### abs error vs rkf45

3.2507330161024584e-13

4.4568460033644897e-11

5.214975840051039e-09

###### rkf dop disagreement

8.881784197001252e-16

1.1102230246251565e-16

6.938893903907228e-17

###### diagnostic resolution threshold

1.4389374745026462e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531180037229

0.5024917064149607

0.09935279569009021

###### rkf45

2.0125311800372265

0.5024917064142119

0.09935279551251416

###### dop853

2.0125311800372265

0.5024917064142119

0.09935279551251419

###### abs error vs dop853

2.6645352591003757e-15

7.487344078072056e-13

1.7757602333023925e-10

###### abs error vs rkf45

2.6645352591003757e-15

7.487344078072056e-13

1.7757605108581487e-10

###### rkf dop disagreement

0.0

0.0

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4299894104661537e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

cee52fd1a63949beec1f7f7b87ca4a5b666578b3485a323917d10bdf645c0f17

###### equation sha256

9315908df0855665d782c9ca5b51cd19cea3820094960221979483e1807bfc5d

###### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### 3.5

##### case

3.5

##### m

3

##### order

6

##### z0

1

##### initial jet

2

1/2

1/10

##### g

1

##### kappa

1/30

##### alpha

-1

##### alpha3

1

##### polynomial

```text
2893976089*h**6/3294225000 + 73808*h**5/226875 + 8309*h**4/60500 + 83*h**3/1100 + h**2/20 + h/2 + 2
```

##### coefficients

2

1/2

1/20

83/1100

8309/60500

73808/226875

2893976089/3294225000

##### verification

###### passed

True

###### through degree

3

###### residual coefficients

0

0

0

0

###### residual remainder order

4

##### leading at initial

-22/5

##### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

##### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

##### velocity at initial

1

##### gradient at initial

1/2

##### status

regular_analytic_germ

##### recurrence

###### degree

3

###### rhs coefficient

249/550

###### coefficient

83/1100

###### degree

4

###### rhs coefficient

49854/15125

###### coefficient

8309/60500

###### degree

5

###### rhs coefficient

295232/15125

###### coefficient

73808/226875

###### degree

6

###### rhs coefficient

2893976089/27451875

###### coefficient

2893976089/3294225000

##### formal remainders

###### F

7

###### F prime

6

###### F double prime

5

##### comparison

###### status

existing_grid_nodes_only

###### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.025135405576422

0.5056463920907549

0.12773455893774335

###### rkf45

2.025135407985645

0.5056467385605181

0.12777767811832044

###### dop853

2.0251354079856467

0.5056467385605179

0.12777767811832044

###### abs error vs dop853

2.409224819643896e-09

3.4646976299068655e-07

4.311918057708919e-05

###### abs error vs rkf45

2.4092230432870565e-09

3.4646976321273115e-07

4.311918057708919e-05

###### rkf dop disagreement

1.7763568394002505e-15

2.220446049250313e-16

0.0

###### diagnostic resolution threshold

1.7763568394002505e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012532486016733

0.5026507478244614

0.1124601819721764

###### rkf45

2.012532486033926

0.5026507526978359

0.11246137095840224

###### dop853

2.0125324860339266

0.502650752697836

0.11246137095840296

###### abs error vs dop853

1.7193801937764874e-11

4.8733745927620475e-09

1.188986226557942e-06

###### abs error vs rkf45

1.7193357848555024e-11

4.873374481739745e-09

1.188986225836297e-06

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

7.216449660063518e-16

###### diagnostic resolution threshold

1.429990338432622e-14

7.105427357601002e-15

7.216449660063518e-15

###### resolved vs reference

True

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062579633277906

0.5012864835989393

0.1059299526611398

###### rkf45

2.00625796332792

0.5012864836714865

0.10592998775763712

###### dop853

2.0062579633279194

0.5012864836714864

0.10592998775763719

###### abs error vs dop853

1.2878587085651816e-13

7.2547079454921e-11

3.5096497388864556e-08

###### abs error vs rkf45

1.2922996006636822e-13

7.254719047722347e-11

3.509649731947562e-08

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

6.938893903907228e-17

###### diagnostic resolution threshold

1.4255320219035066e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269717592375

0.5006339789818066

0.10289555175034332

###### rkf45

2.0031269717592384

0.5006339789829141

0.10289555281756263

###### dop853

2.0031269717592384

0.5006339789829141

0.10289555281756269

###### abs error vs dop853

8.881784197001252e-16

1.1074474670635936e-12

1.0672193684335696e-09

###### abs error vs rkf45

8.881784197001252e-16

1.1074474670635936e-12

1.0672193129224183e-09

###### rkf dop disagreement

0.0

0.0

5.551115123125783e-17

###### diagnostic resolution threshold

1.4233073185886542e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

ca779ba324abf121b3b8e8dc51509dc123712838c542cd174c3c8315a8931b81

###### equation sha256

729701d3ab64dd04791d02e22daa7fa4ced0dea9e343c94e101ade67a00c4002

###### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### 3.6

##### case

3.6

##### m

3

##### order

6

##### z0

1

##### initial jet

2

1/2

1/10

##### g

1

##### kappa

1/30

##### alpha

-1

##### alpha3

0

##### polynomial

```text
1077541127*h**6/7623504300000 + 1632377*h**5/3579110000 + 17201*h**4/10082000 + 169*h**3/21300 + h**2/20 + h/2 + 2
```

##### coefficients

2

1/2

1/20

169/21300

17201/10082000

1632377/3579110000

1077541127/7623504300000

##### verification

###### passed

True

###### through degree

3

###### residual coefficients

0

0

0

0

###### residual remainder order

4

##### leading at initial

-71/20

##### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

##### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

##### velocity at initial

1/2

##### gradient at initial

1/2

##### status

regular_analytic_germ

##### recurrence

###### degree

3

###### rhs coefficient

169/3550

###### coefficient

169/21300

###### degree

4

###### rhs coefficient

51603/1260250

###### coefficient

17201/10082000

###### degree

5

###### rhs coefficient

4897131/178955500

###### coefficient

1632377/3579110000

###### degree

6

###### rhs coefficient

1077541127/63529202500

###### coefficient

1077541127/7623504300000

##### formal remainders

###### F

7

###### F prime

6

###### F double prime

5

##### comparison

###### status

existing_grid_nodes_only

###### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251260025919593

0.5050603746148682

0.1024326317007503

###### rkf45

2.025126002591997

0.5050603746202718

0.10243263235149926

###### dop853

2.025126002591998

0.5050603746202719

0.10243263235149923

###### abs error vs dop853

3.863576125695545e-14

5.403677505455562e-12

6.507489269669264e-10

###### abs error vs rkf45

3.774758283725532e-14

5.403566483153099e-12

6.50748954722502e-10

###### rkf dop disagreement

8.881784197001252e-16

1.1102230246251565e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.438938570140634e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.012531374643942

0.5025149842915042

0.10120308085213524

###### rkf45

2.012531374643942

0.5025149842915876

0.10120308087221945

###### dop853

2.0125313746439426

0.5025149842915878

0.10120308087221945

###### abs error vs dop853

4.440892098500626e-16

8.359979375427429e-14

2.0084212071225238e-11

###### abs error vs rkf45

0.0

8.337774914934926e-14

2.0084212071225238e-11

###### rkf dop disagreement

4.440892098500626e-16

2.220446049250313e-16

0.0

###### diagnostic resolution threshold

1.429989548742542e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578280384185

0.5012537325750577

0.1005982872979246

###### rkf45

2.006257828038418

0.5012537325750588

0.10059828729854836

###### dop853

2.0062578280384185

0.5012537325750589

0.10059828729854838

###### abs error vs dop853

0.0

1.2212453270876722e-15

6.237788063856442e-13

###### abs error vs rkf45

4.440892098500626e-16

1.1102230246251565e-15

6.237649285978364e-13

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4255319257745345e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.003126955064686

0.500625931467146

0.10029833718372858

###### rkf45

2.003126955064685

0.5006259314671458

0.10029833718374802

###### dop853

2.003126955064686

0.500625931467146

0.10029833718374802

###### abs error vs dop853

0.0

0.0

1.9442780718748054e-14

###### abs error vs rkf45

8.881784197001252e-16

1.1102230246251565e-16

1.9442780718748054e-14

###### rkf dop disagreement

8.881784197001252e-16

1.1102230246251565e-16

0.0

###### diagnostic resolution threshold

1.4233073067264612e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

15718ea5f251e4c818d3b3750fe974daaa973179d63c787e03b6e0f278be458a

###### equation sha256

d781aee509f1ddc72940d424049d1bee7ca41db4d9c694b83d6f7b1e60c4e06c

###### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### 3.7

##### case

3.7

##### m

3

##### order

6

##### z0

1

##### initial jet

2

1/2

1/10

##### g

1

##### kappa

1/30

##### alpha

1

##### alpha3

1

##### polynomial

Not applicable / not supplied.

##### coefficients

(none)

##### verification

Not applicable / not supplied.

##### leading at initial

Not applicable / not supplied.

##### assumptions

printed scalar equation

real local chart

##### local existence

Not applicable / not supplied.

##### status

identity_family

##### reason

phi=alpha*t+F(s) is an identity; any local analytic F with F_prime>0 is allowed, not a unique recurrence

#### 3.8

##### case

3.8

##### m

3

##### order

6

##### z0

0

##### initial jet

0

1

1/10

##### g

1

##### kappa

1/30

##### alpha

1

##### alpha3

1

##### polynomial

```text
h**2/20 + h
```

##### coefficients

0

1

1/20

0

0

0

0

##### verification

###### passed

True

###### through degree

3

###### residual coefficients

0

0

0

0

###### residual remainder order

4

##### leading at initial

1

##### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

##### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

##### velocity at initial

1

##### gradient at initial

1

##### status

regular_analytic_germ

##### recurrence

###### degree

3

###### rhs coefficient

0

###### coefficient

0

###### degree

4

###### rhs coefficient

0

###### coefficient

0

###### degree

5

###### rhs coefficient

0

###### coefficient

0

###### degree

6

###### rhs coefficient

0

###### coefficient

0

##### formal remainders

###### F

7

###### F prime

6

###### F double prime

5

##### comparison

###### status

existing_grid_nodes_only

###### samples

###### offset

0.2

###### z

0.2

###### polynomial

0.202

1.02

0.1

###### rkf45

0.20199999999999985

1.0199999999999978

0.1

###### dop853

0.20199999999999987

1.0199999999999994

0.1

###### abs error vs dop853

1.3877787807814457e-16

6.661338147750939e-16

0.0

###### abs error vs rkf45

1.6653345369377348e-16

2.220446049250313e-15

0.0

###### rkf dop disagreement

2.7755575615628914e-17

1.5543122344752192e-15

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

1.554312234475219e-14

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.1

###### z

0.1

###### polynomial

0.1005

1.01

0.1

###### rkf45

0.10049999999999996

1.009999999999999

0.1

###### dop853

0.10049999999999995

1.009999999999999

0.1

###### abs error vs dop853

5.551115123125783e-17

1.1102230246251565e-15

0.0

###### abs error vs rkf45

4.163336342344337e-17

1.1102230246251565e-15

0.0

###### rkf dop disagreement

1.3877787807814457e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.176481631177004e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.05

###### z

0.05

###### polynomial

0.050125

1.005

0.1

###### rkf45

0.05012499999999999

1.0049999999999994

0.1

###### dop853

0.05012499999999998

1.0049999999999994

0.1

###### abs error vs dop853

2.0816681711721685e-17

4.440892098500626e-16

0.0

###### abs error vs rkf45

1.3877787807814457e-17

4.440892098500626e-16

0.0

###### rkf dop disagreement

6.938893903907228e-18

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.140954494389003e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### offset

0.025

###### z

0.025

###### polynomial

0.02503125

1.0025

0.1

###### rkf45

0.025031249999999998

1.0024999999999997

0.1

###### dop853

0.02503124999999997

1.0024999999999997

0.1

###### abs error vs dop853

3.122502256758253e-17

2.220446049250313e-16

0.0

###### abs error vs rkf45

3.469446951953614e-18

2.220446049250313e-16

0.0

###### rkf dop disagreement

2.7755575615628914e-17

0.0

0.0

###### diagnostic resolution threshold

7.105427357601002e-15

7.123190925995002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

False

###### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

de61cc352ee9d2c829f36268298f0ed914392f0b293d3aed650b22980caf8adc

###### equation sha256

bbdb6f892387e88393e858d8ef514d6114713b50b8e7fc7aa883ebfdfb88f88b

###### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

#### 3.9

##### case

3.9

##### m

3

##### order

6

##### z0

1

##### initial jet

2

1/2

1/10

##### g

1

##### kappa

1/30

##### alpha

-1

##### alpha3

1

##### polynomial

```text
14467743241*h**6/175275364500000 + 23103299*h**5/73955850000 + 10247*h**4/7489200 + 173*h**3/23700 + h**2/20 + h/2 + 2
```

##### coefficients

2

1/2

1/20

173/23700

10247/7489200

23103299/73955850000

14467743241/175275364500000

##### verification

###### passed

True

###### through degree

3

###### residual coefficients

0

0

0

0

###### residual remainder order

4

##### leading at initial

-79/20

##### assumptions

g>0

kappa>0

m>=1

positive real velocity and gradient

nonzero third-derivative coefficient at initial jet

scaling rows additionally require t>0

##### local existence

```text
The corrected normal form F_triple_prime=R(z,F,F_prime,F_double_prime) is real analytic near this regular jet. Analytic ODE local existence and uniqueness give a unique local analytic profile germ. The degree-N polynomial is a formal truncation, not an exact solution or a radius bound.
```

##### velocity at initial

3/2

##### gradient at initial

1/2

##### status

regular_analytic_germ

##### recurrence

###### degree

3

###### rhs coefficient

173/3950

###### coefficient

173/23700

###### degree

4

###### rhs coefficient

10247/312050

###### coefficient

10247/7489200

###### degree

5

###### rhs coefficient

23103299/1232597500

###### coefficient

23103299/73955850000

###### degree

6

###### rhs coefficient

14467743241/1460628037500

###### coefficient

14467743241/175275364500000

##### formal remainders

###### F

7

###### F prime

6

###### F double prime

5

##### comparison

###### status

existing_grid_nodes_only

###### samples

###### offset

0.050000000000000044

###### z

1.05

###### polynomial

2.0251259210976507

0.5050554408709601

0.1022317169851667

###### rkf45

2.0251259210976693

0.5050554408736493

0.10223171730888114

###### dop853

2.02512592109767

0.5050554408736495

0.10223171730888117

###### abs error vs dop853

1.9539925233402755e-14

2.6894042548519792e-12

3.237144718948315e-10

###### abs error vs rkf45

1.865174681370263e-14

2.689182210247054e-12

3.237144441392559e-10

###### rkf dop disagreement

8.881784197001252e-16

2.220446049250313e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4389385122354314e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

True

True

True

###### offset

0.02499999999999991

###### z

1.025

###### polynomial

2.0125313645934457

0.5025137728386481

0.10110529707597078

###### rkf45

2.0125313645934453

0.5025137728386896

0.10110529708597979

###### dop853

2.0125313645934457

0.5025137728386897

0.1011052970859798

###### abs error vs dop853

0.0

4.163336342344337e-14

1.000902138947879e-11

###### abs error vs rkf45

4.440892098500626e-16

4.1522341120980855e-14

1.0009007511690982e-11

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.4299895416012346e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

True

True

###### offset

0.012499999999999956

###### z

1.0125

###### polynomial

2.0062578267904883

0.5012534324048512

0.10055004606198273

###### rkf45

2.0062578267904883

0.5012534324048518

0.10055004606229385

###### dop853

2.0062578267904883

0.501253432404852

0.10055004606229388

###### abs error vs dop853

0.0

7.771561172376096e-16

3.1115388043900793e-13

###### abs error vs rkf45

0.0

5.551115123125783e-16

3.111261248633923e-13

###### rkf dop disagreement

0.0

2.220446049250313e-16

2.7755575615628914e-17

###### diagnostic resolution threshold

1.4255319248878267e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### offset

0.006250000000000089

###### z

1.00625

###### polynomial

2.0031269549092143

0.5006258567578608

0.1002743770674107

###### rkf45

2.0031269549092148

0.5006258567578608

0.10027437706742037

###### dop853

2.0031269549092143

0.5006258567578609

0.10027437706742039

###### abs error vs dop853

0.0

1.1102230246251565e-16

9.686695889854491e-15

###### abs error vs rkf45

4.440892098500626e-16

0.0

9.672818102046676e-15

###### rkf dop disagreement

4.440892098500626e-16

1.1102230246251565e-16

1.3877787807814457e-17

###### diagnostic resolution threshold

1.423307306615992e-14

7.105427357601002e-15

7.105427357601002e-15

###### resolved vs reference

False

False

True

###### provenance

###### metadata

numerics.json

###### checks

###### passed reference

True

###### model

True

###### g

True

###### kappa

True

###### interval

True

###### center

True

###### initial jet

True

###### equation

True

###### csv bytes

True

###### csv sha256

846874f12121c78769dead4a3b61f38fdcfef9a03442cc4325ed20091843a88c

###### equation sha256

32b928ee12fee2a62946e8a63e8e094c1714b836bcc4e22c6ad2cc9a1fa92865

###### interpretation

finite endpoint diagnostics; no interpolation, radius, or certified remainder

### regular count

21

### all verified

True

### elapsed seconds

5.8916127999837045

### scope

local analytic germs on regular positive chart; no radius or global PDE claim

## Detailed derivations and discrepancy explanations

### COMPUTATION.md

# What the reproduction computes

The default `python main.py` performs new calculations. It does not read
`evidence.json` or stored trajectories as substitutes for those calculations.
It writes symbolic traces, exact certificates, numerical CSVs, convergence
experiments and static figures. The HTML template, viewer data packaging,
viewer CLI and generated `solutions.html` have been removed; the previous
viewer is retained only in the pre-edit archive.

| Object | Live calculation | Authored inputs / scope |
|---|---|---|
| Master equation | `total()` differentiates the two currents; `build_model_report()` computes coordinate pullbacks and compatibility differences. | The balances, constitutive law and choice of printed scalar model are mathematical inputs. |
| Infinitesimal symmetries | Recursive third prolongation, arbitrary-function determining coefficients and generator defects are computed with SymPy. | The split sequence and integration of the determining conditions are guided by the documented mathematical derivation. This is not a general autonomous PDE-classification engine. |
| Lie algebra and Table 2 | Coordinate brackets, Jacobi identities and adjoint actions are computed; all 25 Table 2 cells are compared with source transcriptions. | The listed source fields and Table 2 formulas are inputs. Optimal-system representatives and chart arguments are hand-derived from the computed actions, not discovered by an orbit-classification algorithm. |
| Nine reductions | `derive_reduction()` constructs profile jets/residuals. `verify_reduction_pullbacks()` independently differentiates the invariant graphs and substitutes every jet into `master()`. | Nine chosen graphs and the campaign exponents are inputs; the two-variable multiplier identities are checked symbolically, retaining time for scaling/traveling graphs. |
| First integrals | The total derivative of each supplied candidate is compared with the corrected ODE residual for symbolic m. | The candidate integral is supplied analytically; verification is computed. This is not learned integral discovery. |
| Source discrepancies | Source equations are solved/substituted at exact witness jets. A verdict requires an actual nonzero residual or mismatch; zero tests of the printed formulas are also recorded. | Source formulas and witness choices are transcribed inputs. The PDF text is extracted and hashed, not automatically converted into all mathematical formulas. |
| Numerical profiles | The six-stage Fehlberg 4(5) integrator evaluates the generated RHS; DOP853, original-PDE finite differences and first-integral solves give separate checks. | Constants, tolerances and constructed IVP data are explicitly chosen. They are not the source paper's numerical experiments. |
| Series and convergence | Taylor coefficients and undivided residual coefficients are calculated exactly; fresh fixed-step and adaptive sweeps produce endpoint comparisons. | A completed sweep is not automatically a resolved convergence order. A finite polynomial or small measured difference is not a radius/error certificate. |

The direct graph audit contains 25 entries: the 21 regular campaign IVPs
and four distinct nonregular/identity rows. The 3.4 and 3.5 checks retain the
symbolic multipliers T^-2 and T^-1, respectively, on T>0. Traveling checks
use the declared alpha=-1 examples; they do not test every possible group
parameter. Three additional first-integral identities use symbolic m.

Failure of the named model/symmetry checks, Table 2 comparisons, independent
pullbacks, integral identities or source-witness tests makes the symbolic
CLI gate fail. Source disagreement is expected and remains distinct from a
failed calculation. The numerical and series gates are evaluated separately.

`--stage report` only formats saved results: it says so explicitly and
refuses results with a different/missing recorded code hash. It is not a
fresh calculation. `--stage plots` reads hash-matched numerical data and
computes Taylor comparisons and separate second-order solves; use the default
full run when fresh numerical trajectories are required. Missing source PDFs
set `complete_audit=false` even if the computations themselves succeed.

The computation revision was also run from a copied `main.py` with an empty
output directory. Negative controls alter the master equation and an adjoint
sign and require the calculated checks to fail; another control supplies a
new initial jet and checks its newly integrated/derived solution. Receipts
and limitations are in `COMPUTATION_VALIDATION.md`.

### CONVERGENCE.md

# Endpoint convergence of the constructed regular IVPs

This experiment tests the **printed scalar** SVE profile ODEs, not physical
data, arbitrary PDE initial/boundary data, or a continuous error bound. Run
from this package directory:

```powershell
python -B main.py --stage convergence
```

The script calls `run_convergence(out_dir)` and writes
`results/convergence/convergence.json`, `.csv`, and `.png`. The JSON retains
the endpoint vector, step/RHS counts, failures, comparator settings, and
resolved/unresolved decisions for every run. It does not replace the original
81-point numerical campaign. The original 21 initial jets and intervals are
unchanged: 3.4 on `[1,1.4]`, 3.5/3.6/3.9 on `[1,1.1]`, and 3.8 on `[0,.4]`.

## Protocol

The fixed-step ladder takes exactly `N=1,2,4,8,16,32,64` steps with the
classic six-stage Fehlberg **fifth-order accepted state**. There is no error
controller. Each endpoint is compared componentwise with a tight SciPy
`DOP853` solution at the same endpoint, scaled by `max(1,|reference|)`.
Two DOP853 policies, `(rtol,atol,max_step)=(1e-12,1e-14,L/8)` and
`(1e-13,1e-15,L/16)`, supply a reference-disagreement diagnostic; the
tighter policy supplies the comparison value. Neither reference has an
output grid. For 3.8, the exact quadratic replaces DOP853.

The adaptive sweep uses the same Fehlberg implementation with `rtol` from
`1e-3` through `1e-10`, `atol=rtol/100`, `first_step=L/2`, and the same
nonrestrictive `max_step=L` at every tolerance. There is **no `t_eval`**.
Its step counts, rejections and function evaluations are saved. Holding the
step policy fixed isolates tolerance changes from a changing maximum step;
it does not force the method to choose different steps on a short/easy IVP.

To avoid calling floating-point noise an order, a fixed-step endpoint error
is *resolved* only if it exceeds `10*max(32*epsilon_machine,
10*DOP853_pair_disagreement)`. The maximum comparator disagreement in this
run was `1.89e-15`; thus the resolved-error thresholds range from
`7.11e-14` to `1.89e-13`. Pairwise order `log2(E_N/E_2N)` is reported only
when **both** errors exceed that threshold. This is an operational resolution
screen, not a rigorous upper bound on either solver's error.

## Measured results (2026-10-12, Python 3.14.2)

All 21 established IVPs completed both sweeps. Of 147 fixed-step endpoint
errors, 55 exceeded the resolution threshold and 92 did not. There are 39
resolved adjacent-step order estimates. For the five 3.4 exponent rows,
the resolved late-ladder orders approach five: the last resolved order is
between `4.97` and `4.98`. The cubic 3.5 row's last resolved order is
`4.93`. These are empirical global endpoint orders on these smooth local
IVPs, not an error certificate for the original PDE.

The short 3.6 and 3.9 traveling-wave intervals each give only one resolved
adjacent pair, around `4.95`--`4.97`; further halving reaches the floor.
That supports consistency with fifth order but does **not** establish an
asymptotic range for those rows. The five 3.8 rows have the exact quadratic
`F(t)=F0+P0*t+C0*t^2/2`; their fixed-step differences are roundoff-level
and no nontrivial convergence order can be inferred.

The separate exact non-polynomial control `y'=y`, `y(0)=1` on `[0,2]`
has fixed-step orders `4.44, 4.72, 4.86, 4.93, 4.96` for successive
halvings. This tests the code's fifth-order behavior without relying on a
numerical reference. It does not by itself establish the SVE model's order.

On 3.4 and 3.5, adaptive endpoint error decreases from about `1e-7` to
`1e-11` as tolerance tightens and accepted steps rise from 2 to 12 and
11, respectively. The first four tolerance settings use identical two-step
histories, so their error is identical: a genuine coarse-tolerance plateau.
The 3.6 and 3.9 rows remain two-step histories throughout this chosen sweep;
their errors do not change with tolerance. The 3.8 adaptive endpoints equal
the exact quadratic to floating precision (zero in the reported scaled
metric). A tolerance sweep cannot demonstrate convergence where the step
history does not change.

Every positive-branch guard is checked at solver stages and fixed-step
endpoints. Only local, sampled regularity is established. The figure omits
zero adaptive errors from its log axis; the CSV and JSON retain them. Source
equation errors, branch singularities, and behavior outside these intervals
are not resolved by this experiment.

### DISSERTATION_NOTES.md

# Dissertation integration notes: 2026-10-12 SVE reproduction

The standalone `research_artifacts/SVE-reproduced-20261012/manuscript_section.tex`
is integrated inline immediately before `\section{Related work and research position}`
in `draft/main.tex`. It uses the existing `amsmath`, `booktabs`, `tabularx`,
`natbib`, and `hyperref` setup and prefixes new labels `sve-repro-`. It cites
the existing `ap` item and the added `uddin2016rkf` item (DOI `10.1016/j.aej.2016.05.009`; local reference PDF
has 2016 in-press metadata, so do not invent volume or page numbers).

The section is additive to the earlier example and keeps the printed scalar
model distinct from the advectively corrected physical pullback. Its numeric
claim uses the accepted post-repair 21-run snapshot in
`research_artifacts/SVE-reproduced-20261012/build/numerics-smoke/numerics.json`
and the qualifications in `docs/REVIEW_NUMERICS.md`. The symbolic scope
follows `docs/REVIEW_SYMBOLIC.md`: complete local smooth point algebra only
on the declared positive regular chart, not a full-bed-system or singular
branch classification. Source equations (24)--(34) are individually
qualified/refuted via explicit witnesses; the cubic power solution remains
valid on its singular normal-form stratum.

The director completed native `latexmk`, final citation/reference diagnostics,
rendered-page inspection, and the project and package validation commands.
See `../VALIDATION.md` for the results and retained failures. The standalone
section and the inline manuscript block match exactly. The source PDF, frozen 2026-10-10 package,
manifest, and existing unrelated deletion must remain untouched.

### MANUSCRIPT_REFOCUS.md

# Manuscript refocus handoff (2026-10-13)

## Scope and preservation

- Edited `draft/main.tex` and `draft/dissertation.tex` outside the existing
  `% BEGIN/END SVE REPRODUCTION 20261012` span. The director owns insertion of
  the verified series result there and synchronization with
  `manuscript_section.tex`.
- The dissertation has `% BEGIN/END VERIFIED SVE SERIES INSERTION 20261013`
  comments after its existing scalar SVE analysis. Only the verified
  recurrence, coefficient checks, numerical comparison, and exclusion
  statuses should be inserted there. No series metric is asserted here.
- The pre-series manuscript and bibliography are preserved in
  `archive/release-before-series-20261013.zip` (presence checked). No reference
  PDF or reference corpus was deleted by this refocus.

## Narrative changes

- Both title/abstract/introduction paths lead with the printed scalar SVE
  source audit, corrected local ODE solutions, existing exact first integrals,
  and finite numerical evidence. Refuted source formulas and unresolved
  branches remain part of the result.
- The next step begins with unrestricted `tau(t,s,phi)`, `xi(t,s,phi)`, and
  `eta(t,s,phi)`, their prolongation, and the original-PDE master determining
  equation. The active package's `build_symmetry_report` is SVE-specific;
  `derive_reduction` verifies selected generators downstream. A reusable
  unrestricted arbitrary-PDE determining solver is proposed, not claimed as
  implemented.
- The proposed ML target is a nonconstant, independent first integral
  `I(z,F,P,C)` satisfying `I_z + P I_F + C I_P + R I_C = 0` on an open regular
  chart, with `I_C != 0` when solving locally for `C` to reduce order; an
  admitted reduced-ODE generator is an alternative. Exact verification,
  compatible data, and matched-cost classical controls are required. The
  older learned-profile campaign remains secondary and does not demonstrate
  learned ODE order reduction.
- Three named interests are the Lagrange-coordinate option (not a variational
  action), exact exceptional parameter and orbit-rank strata (not a
  probability distribution without a sampling law), and task-dependent
  trivial-symmetry filtration (not automatically a chain of subalgebras or an
  ideal quotient). Valid translations and valid but task-unhelpful symmetries
  are not mislabelled invalid. Hybrid architectures and conservation analogies
  are deferred.
- The main related-work survey and unrelated quantum/decoherence appendix
  were removed from the active narrative. Their prior text remains in the
  archived release. The dissertation's prior profile-fitting chapters retain
  their negative outcomes but are explicitly labeled historical.

## Bibliography inventory

`draft/main.tex`: **52 -> 19** embedded entries. Retained keys, all currently
cited: `olver`, `oliveri2026`, `anderson2000`, `ap`, `otto`, `kovalev`,
`approxalg`, `tarayrah2023`, `teschl2012`, `lagaris`, `cohen2015`,
`mishra2023`, `koval2023`, `levi2015`, `sympinn`, `sveold`, `noether`,
`fernandez2017`, `uddin2016rkf`.

`draft/dissertation.tex`: **12 -> 12** selected entries; all currently cited.
Keys: `olver`, `olver1986`, `oliveri2026`, `anderson2000`, `ap`,
`tarayrah2023`, `teschl2012`, `lagaris`, `cohen2015`, `mishra2023`,
`sympinn`, `hijazi`. `teschl2012` is retained for the local analytic-ODE
existence statement and the director's series subsection. No new online
bibliographic claim was introduced by this edit.

The source-level citation-key inventory found no missing or uncited keys in
either manuscript. This regex inventory is navigation only, **not** native
LaTeX citation validation. Both manuscripts are **unbuilt at this handoff**:
the director will insert the checked series material, run `latexmk`, inspect
the final citation/reference warnings, and render changed pages. Broader
project audits and regression tests are also outside this writing handoff.

### NUMERICS.md

# Numerical SVE reproduction

## Scope and interface

Run from this package directory:

```powershell
python -B -c "from sve_reproduce.numerics import run_campaign; print(run_campaign('build/numerics')['all_passed'])"
python -B -m pytest -q -p no:cacheprovider tests/test_rkf45.py tests/test_numerics.py
```

`run_campaign(out_dir, rtol=1e-9, atol=1e-11, selected_reduction='all',
selected_case='all')` writes `numerics.json`, one CSV and one PNG per regular
run. `selected_reduction` names a section (`3.1` to `3.9`, or `table3-mixed`);
`selected_case` is the exponent `m` in `1, 1.5, 2, 3, 4`. The default contains
21 regular IVPs: five exponents each for 3.4, 3.6, 3.8 and 3.9, plus cubic
3.5. It also records nonnumerical rows and incompatible parameter
combinations separately. A requested unsupported name is an input error.

These are new dimensionless initial-value demonstrations for the **printed
scalar** equation, not measured flow data and not arbitrary boundary-value
solutions. Set `g=1`, `kappa=1/30`, `beta=m*kappa`. The nonlinear initial jet
is `(F,F',F'')=(2,0.5,0.1)` at `z=1`; 3.4 uses `[1,1.4]`, the others
`[1,1.1]`. Traveling rows use `alpha=-1`; 3.9 also uses `alpha3=1`. The
linear 3.8 rows use `alpha=1`, `(0,1,0.1)` at `t=0`, and `[0,0.4]`.

## Integrator and checks

`rkf45.py` declares the rational six-stage classic Fehlberg tableau. Its
fifth-order state is accepted, while the fourth/fifth difference gives a
weighted RMS local error with scale `atol + rtol*max(|y_n|,|y_{n+1}|)`.
The controller uses safety `0.9`, exponent `-1/5`, and factor clamp
`[0.2,5]`. Defaults are `rtol=1e-9`, `atol=1e-11`. It bounds accepted steps,
rejections and minimum steps; checks finite stage/state values and branch
guards at every stage and accepted endpoint. The solver returns typed stop
statuses. `scipy.integrate.RK45` is not used or identified as Fehlberg;
SciPy `DOP853` is a separate tight-reference comparator.

Every run records endpoint completion, regular leading coefficient and
positive velocity/gradient at all 81 sampled RKF states. A separate
coarse-versus-tight RKF endpoint integration uses distinct half-interval and
quarter-interval maximum steps and retains both accepted time histories.
Roundoff-level differences are labeled controls, not observed convergence
orders. The exponential IVP test separately checks fifth-order global error.
The 3.8 rows also compare against the exact quadratic
`F(t)=F0+P0*t+C0*t^2/2`. Certified first integrals are checked only
for 3.4, 3.6 and 3.9; the other rows report
`no_certified_integral`. For 3.4, the certified X4 integral is additionally
used to solve an independent two-state system and compare it with the
three-state profile. These tests establish consistency of the declared
local IVP, not global existence or a continuous error certificate.

The PDE check reconstructs `phi(t,s)` from the symbolic ansatz and samples
the original two-dimensional coordinates. A nine-point tensor finite
difference stencil estimates the derivatives of `phi` directly, including
third derivatives, and evaluates the printed divergence-form scalar PDE.
It never substitutes the reduced residual or RHS for the PDE residual.
One check reconstructs from the DOP853 dense profile; a second uses local
degree-11 barycentric interpolation of a tight RKF profile. Each trajectory
is labeled in JSON; the barycentric weight-order seed is fixed at `0` for
repeatable third-derivative diagnostics. The predeclared acceptance stencil
is `h=0.003` at three interior points, with `h=0.002` and `h=0.001` retained
as resolution diagnostics, not monotone convergence evidence.
The pass threshold is `1e-6` at **the fixed acceptance stencil**, not the
minimum of the three. Smaller stencils can worsen through cancellation of
third derivatives: the reported `error_floor` is an observed finite-grid
minimum, not proof of asymptotic convergence. An added `0.001*t^3` field
perturbation must change the PDE residual by more than `1e-4`; this is a
negative control that detects a vacuous residual checker.

The remaining pass thresholds are `1e-7` for scaled RKF/DOP853 state
disagreement, RKF joint tolerance/maximum-step disagreement, certified-integral drift,
and the 3.4 two-state/three-state comparison. Failure or unavailable
branches remain explicit rows; they are not omitted to make `all_passed`
true. This finite sampling does not certify positivity between samples.

## Bounded run evidence

The 2026-10-12 smoke run at `build/numerics-smoke/numerics.json` finished
21/21 regular rows under the listed gates. The largest scaled RKF/DOP853
state disagreement was `1.09e-13`. The largest fixed-stencil original-PDE
residual was `7.98e-7` on the DOP853 reconstruction and `9.36e-7` on
the tight-RKF reconstruction. The largest certified-integral drift was
`7.33e-15`; the largest X4 two-state/three-state disagreement was
`2.44e-15`. The independent coarse/tight RKF endpoint ladder differed by
at most `2.53e-10`; all histories differed, while five exact-quadratic 3.8
rows were roundoff-level controls. The maximum exact-quadratic error was
`4.44e-15`. Minimum sampled velocity and gradient were both `0.5`, and
the minimum absolute leading coefficient was `1`. The smallest
negative-control residual change was `0.00241`. These figures are measured
on the finite grid, not rigorous error bounds. The run JSON retains every
stencil value; for many rows the finest `h=0.001` value is worse than the
acceptance value due to numerical differentiation roundoff.

The cited reference PDF, *Two parameters Liegroup analysis and numerical
solution of unsteady free convective flow of non-Newtonian fluid* in `ref/`,
reports Runge-Kutta-Fehlberg fourth/fifth order **with shooting** for a
different boundary-value fluid problem. Its abstract does not specify
tolerances for these SVE IVPs and supplies no SVE boundary data. The method
name motivates an integrator choice only; this package does not reproduce
that paper's BVP or infer its numerical accuracy.

### REDUCTIONS.md

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

### SERIES.md

# Local series for the corrected similarity equations

## What exists

For each regular row 3.4, 3.5, 3.6, 3.8 and 3.9, the corrected printed-scalar
PDE pullback has the form

```text
E(z,F,P,C,H) = A(z,F,P,C) H + B(z,F,P,C) = 0,
P=F', C=F'', H=F'''.
```

At a jet with `g,kappa>0`, `m>=1`, original velocity `p>0`, original gradient
`q>0`, and `A!=0`, it is a normal-form ODE `F'''=-B/A`. On a sufficiently
small neighborhood of that jet the denominators stay nonzero and positive
real-power arguments stay positive. Hence the first-order vector field
`(F,P,C)'=(P,C,-B/A)` is real analytic. Locally choosing the corresponding
complex branches, the analytic IVP theorem gives a **unique convergent
analytic profile germ** for each such initial triple. This proves local
similarity-solution existence: inserting that germ into its invariant graph
solves the corrected pullback and therefore the printed scalar PDE wherever
the local reconstruction and positive chart remain valid. It supplies no
global continuation, physical-data match, or computable convergence radius.

The analytic-IVP step follows Gerald Teschl, *Ordinary Differential Equations
and Dynamical Systems* (AMS, 2012), Chapter 4, section 4.1, Theorems 4.1 and
4.2, printed pp. 113 ff. The author-hosted, AMS-permitted PDF is at
`https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf`; the checked local
copy is `build/series-sources/teschl-ode.pdf` (SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`).
The theorem asserts existence on *some* neighborhood. This package has not
computed its polydisc constants or a radius lower bound.

## Exact recurrence and audit

Set `h=z-z0` and `F_N(h)=sum(a_j*h^j, j=0..N)`, with
`a0=F0`, `a1=P0`, `a2=C0/2`. Given coefficients through `a_(n+2)`, let
`R=-B/A`. The triangular recurrence is

```text
a_(n+3) = [h^n] R(z0+h,F_(n+2),F'_(n+2),F''_(n+2))
          / ((n+3)(n+2)(n+1)),        n=0,...,N-3.
```

`compute_ode_series()` performs bounded exact SymPy power-series arithmetic
with rational inputs (and exact algebraic radicals for fractional `m`). It
then substitutes the finished polynomial into the **undivided corrected
residual**, not only the normal form, and checks coefficients `h^0` through
`h^(N-3)` are exactly zero. Thus the residual is formally `O(h^(N-2))`.
For the actual local analytic germ, Taylor's theorem gives local remainders
`F-F_N=O(h^(N+1))`, `F'-F_N'=O(h^N)`, and `F''-F_N''=O(h^(N-1))` as `h->0`.
A combined `(F,P,C)` norm is generally limited by the last exponent, not
the profile's `N+1`. None of these big-O statements supplies a *numerical*
constant or a verified radius. The finite polynomial is not itself an exact
solution unless the residual vanishes identically (as in 3.8).

Use from the package directory:

```powershell
python -B main.py --stage series --series-order 6 --trace summary
python -B -c "from main import compute_ode_series; r=compute_ode_series('3.4', exponent=3); print(r['polynomial'], r['verification'])"
```

The API returns inspectable SymPy `polynomial`, exact `coefficients`,
`recurrence`, chart values and assumptions, a typed `status`, and exact
`verification`. Degree is restricted to 3--8 for a bounded calculation.
Input decimal floats are converted to a simple fraction only when the
fraction round-trips to the identical float; otherwise their exact decimal
representation is retained. A finite `sympy.Float` is also accepted. This
avoids silently turning a tiny positive chart value into zero.

`run_series_campaign(out_dir, order=6, compare_dir=...)` writes
`series.json`, `series_trace.txt` and `series_comparison.csv`. With an
existing `numerical/` directory, comparison samples come **only** from its
saved 81-point RKF45/DOP853 CSV grid at offsets `L/2`, `L/4`, `L/8`, `L/16`;
there is no interpolation or output-grid claim about the new series solver.
The CSV keeps separate absolute errors for `F`, `F'`, `F''` and records
RKF/DOP853 disagreement plus an operational floating-resolution threshold.
These comparisons are diagnostics, not certified remainders or radius tests.
Comparison also requires a passed numerical receipt matching the model,
exponent, constants, initial jet, center and interval, with the exact
corrected-equation fingerprint and a matching CSV SHA-256. Missing, stale or
modified references receive an explicit unavailable/mismatch status and no
error values. Rerun the numerical or full campaign after editing the IVP or
equation; merely finding an old CSV with the same filename is insufficient.

## Measured finite evidence

The 2026-10-13 degree-six run completed and exactly verified all 21 regular
campaign IVPs. All 21 also found their four existing numerical grid nodes.
The nine subsection statuses are: 3.1 `outside_positive_chart` (stationary
identity family with `p=0`); 3.2 `undefined_chart` (`q=0`); 3.3
`no_invariant_graph`; 3.4, 3.5, 3.6, 3.8 and 3.9
`regular_analytic_germ`; and 3.7 `identity_family` (arbitrary analytic
`F(s)` with `alpha>0`, `F'>0`, not a unique ODE recurrence). The `alpha=0`
traveling exceptions are typed separately. X5 at `m!=3` is incompatible.

For the cubic 3.4 IVP `(z0,F0,P0,C0)=(1,2,1/2,1/10)`, the degree-six
coefficients are

```text
[2, 1/2, 1/20, -11/2370, 41037/6241000,
 -13543709/12325975000, 97895097811/43818841125000].
```

Its original corrected residual coefficients `h^0..h^3` are exactly zero.
The cubic 3.5 coefficients begin `a3=83/1100`, `a4=8309/60500` and pass
the same check. The 3.8 recurrence terminates at the exact quadratic
`F(h)=h+h^2/20` for its declared jet. Fractional `m=3/2` rows have exact
algebraic, not necessarily rational, coefficients and also pass.

At offsets `0.2,0.1,0.05,0.025`, the 3.4 cubic profile's absolute
series-vs-DOP853 errors are approximately `3.28e-9, 3.62e-11, 3.24e-13,
2.66e-15`. The last is at floating precision and is **not** an observed
order. Its `F''` errors are `2.50e-6, 1.37e-7, 5.21e-9, 1.78e-10`, as
expected to decrease more slowly. The short 3.6 and 3.9 profiles reach
roundoff in `F` quickly; they do not supply a useful profile-error slope.
The 3.8 quadratic differs from the stored numerical profiles only by
floating arithmetic. All rows and unresolved comparison flags remain in
the JSON and CSV.

## Singular and exceptional charts

`normal_form_singular` means only that dividing by `A` is invalid at the
given jet. It does **not** mean that no similarity solution exists. An exact
counterexample is the cubic X4 profile `F(z)=A*z^(1/3)` on `z>0`, with
`A^3=27*g/(1-12*g*kappa)` when `g*kappa<1/12`. For the campaign constants
`g=1`, `kappa=1/30`, `A^3=45`; the corrected residual vanishes but its
highest-derivative coefficient also vanishes along this branch. The API
does not claim existence/uniqueness from its regular normal form there.
Similarly, an identity reduction allows many profiles rather than a
three-jet-determined analytic germ, and 3.2 is undefined in the scalar PDE.

All conclusions concern the printed scalar reduction. The advectively
corrected scalar equation, full bed system, arbitrary IBVP, shocks, and
learned error are not established here.

### SINGLE_SCRIPT.md

# Standalone script layout

`main.py` contains ordinary Python source in one editable file, including
convergence checks, reconstructed fields and static scientific plots.
It does not import any local implementation package. Run `python main.py
--help` from any working directory. The script resolves its default output
directory relative to its own location.

Edit `DEFAULT_RTOL`, `DEFAULT_ATOL`, and `DEFAULT_TRACE` near the imports, or
override them with `--rtol`, `--atol`, and `--trace`. The numerical model
constants `G`, `KAPPA`, `CASES`, `EXPONENTS` and per-case initial jets and
intervals in `NUMERICAL_CASE_SETTINGS` are beside those top-level defaults.
The symbolic jet variables and `master` are in Core. The independent source
checks, corrected reductions, Fehlberg solver, numerical checks, evidence
coverage, and report writer each have labeled sections.

The source locator searches the script directory and its ancestors for the
two `ref/` PDFs. `--repo-root PATH` explicitly selects a repository when the
script has been copied elsewhere. Missing PDFs or PyMuPDF are recorded in
`source_manifest.json` as unavailable; no source extraction is fabricated.
The symbolic and numerical computations can still run, but their source
verification status must be read separately from their execution status.
`run.complete_audit` is false if either primary PDF could not be checked.
`code_manifest.json` hashes the executed script, not unused historical files.

`_reductions_step` constructs human-readable symbolic trace rows;
`_rkf45_step` is the integrator's internal numerical step. Those two former
`_step` helpers have different purposes and were renamed to avoid a global
namespace collision. All former `j.<symbol>` core aliases now refer directly
to the named top-level core symbols/functions. Other original public
functions retain their names so tests can exercise them directly.

The historical modules and original entrypoint are archived in
`archive/release-before-animation.zip`. The retired runtime directory was
removed after exact symbolic/numerical parity checks. Tests now import the
actual `main.py` definitions. A copied-script run without the local package
or PDFs also completed all 21 numerical and convergence cases.

The subsequent computation-only revision removes the HTML template, viewer
data packaging and HTML command-line options. It adds live source-Table-2,
original-master pullback and source-witness gates. See `COMPUTATION.md` for
the exact distinction between authored inputs and computed results.

### SYMMETRIES.md

# Printed scalar SVE: unrestricted point symmetries and algebra audit

Source: Paliathanasis, Leon, and Leach, *Mathematics* **14** (2026) 433,
local v3 PDF `ref/main/*00433-v3.pdf`, equation (7), Proposition 1 and its
displayed determining equations (p. 4), Tables 1-2 and the one-dimensional
list (pp. 5-6). This is an audit of **that printed scalar equation**, not of
the advectively corrected scalar model or the full bed-field system.

## Equation and branch

Set $u=\phi$, $p=u_t>0$, $q=u_s>0$, $a=u_{tt}$, $b=u_{ts}$,
$c=u_{ss}$, $r=u_{ttt}$, $w=u_{tts}$, $x=u_{tss}$, $y=u_{sss}$.
Let $g,\kappa>0$, $m\geq1$, and $\beta=m\kappa$. The source's equation is

\[
 E_m=D_t(qa-gc/q^2)-gm\kappa D_s(p^{m-1}b/q)=0. \tag{S1}
\]

All point coefficients below are unrestricted sufficiently smooth functions
of $(t,s,u)$ on a local open chart. Real powers are smooth because $p>0$.
The coefficient of $r$ is $q>0$, so solve uniquely for $r=R$ and split
the remaining free jets. This is a regular local equation-manifold argument;
it says nothing about $p=0$, $q=0$, global flows or boundary-data
preservation. The exact normal form is in `build_symmetry_report()`.

## Unrestricted determining split

For the unrestricted generator
\[
X=\tau(t,s,u)\partial_t+\xi(t,s,u)\partial_s+
\eta(t,s,u)\partial_u,
\]
let
\(\Omega=\operatorname{pr}^{(3)}X(E_m)|_{r=R}\).
The prolongation is generated recursively from

\[
 \eta_i=D_i\eta-u_jD_i\xi^j,\qquad
 \eta_{Ii}=D_i\eta_I-u_{Ij}D_i\xi^j.
\]

The following coefficient identities were independently expanded by SymPy
from the original (S1), not copied from the printed determining system.
Subscripts on $\tau,\xi,\eta$ here mean ordinary partial derivatives.
Each row is used only **after** the preceding row's consequence.

1. The coefficient of free $y$ is
   \[
   [y]\Omega={g(\kappa mp^mq+p)\over pq^2}(\xi_t+p\xi_u).
   \]
   Its prefactor is strictly positive on the branch. Since $p$ varies
   freely, $\xi_t=\xi_u=0$, so $\xi=\xi(s)$.
2. With that restriction, the coefficient of free $w$ is
   \[
   [w]\Omega={2g(\kappa mp^mq+p)\over pq^2}(\tau_s+q\tau_u).
   \]
   Free $q>0$ gives $\tau_s=\tau_u=0$, hence $\tau=\tau(t)$.
3. The coefficient of $ab$ is $-\eta_s/q$. Thus $\eta_s=0$.
4. The coefficient of $a$ after these restrictions is
   \[
   [a]\Omega=q(4p\eta_{uu}-3\tau_{tt}+4\eta_{tu}).
   \]
   Free $p>0$ gives $\eta_{uu}=0$ and $4\eta_{tu}=3\tau_{tt}$.
   Therefore $\eta=A(t)u+B(t)$ and $4A'=3\tau''$.
5. The coefficient of free $x$ then is
   \[
   [x]\Omega=-{g\over p^2q^2}\left\{
       \kappa mp^mq\big[(m-3)p(A-\tau')+(m-1)(A'u+B')\big]
       +p^2(2\tau'+\xi'-3A)\right\}. \tag{S2}
   \]
   Splitting its distinct $q$-powers gives
   \(2\tau'+\xi'-3A=0\) and
   \((m-3)p(A-\tau')+(m-1)(A'u+B')=0\) for all $p,u$.

No polynomial, affine, or diagonal ansatz was imposed on the initial
coefficient functions. The affine form of $\eta$ is a *deduction* from the
free-jet coefficients. Every division uses $p,q,g,\kappa,m>0$, or the
strictly positive factor $\kappa mp^mq+p$. There is no division by
$m-1$ or $m-3$ before those parameter strata are separated.

For $m\ne1,3$, (S2) yields $A=\tau'$, $A'=B'=0$, and $\xi'=A$.
For $m=3$, it yields $A'=B'=0$, then $\tau''=0$, and
$\xi'=3A-2\tau'$. For $m=1$, it yields $A=\tau'$; combining
$4A'=3\tau''$ with $A'=\tau''$ forces $\tau''=A'=0$, while
$\xi'=A$. Only $B(t)$ remains. After substituting these coefficients,
the **off-shell** expression is
\[
 \operatorname{pr}^{(3)}X(E_1)+2A E_1=bB''(t)+qB'''(t).
\]
Its restriction to $E_1=0$ yields the same condition. Since $b,q$ are free,
$B''=0$. These are all solutions of the necessary
system, and direct off-shell prolongation verifies every resulting basis
generator, so the list is sufficient as well.

Consequently the complete local smooth point algebra on this branch is

| Parameter | Basis | Dimension |
|---|---|---:|
| $m\geq1,\ m\ne1,3$ | $X_1=\partial_t,\ X_2=\partial_s,\ X_3=\partial_u,\ X_4=t\partial_t+s\partial_s+u\partial_u$ | 4 |
| $m=3$ | $X_1,X_2,X_3,X_4,\ X_5=t\partial_t-2s\partial_s$ | 5 |
| $m=1$ | $X_1,X_2,X_3,X_4,\ X_6=t\partial_u$ | 5 |

The extra $m=1$ generator reflects the absence of $p=u_t$ in the
bedload flux $p^{m-1}b/q$ at $m=1$. Directly,
$\operatorname{pr}^{(3)}X_6(E_1)=0$, whereas its general-$m$ residual
is nonzero when $m>1$.

## Direct identities and source discrepancy

Off shell, $\operatorname{pr}^{(3)}X_i(E_m)=0$ for $i=1,2,3$, and
$\operatorname{pr}^{(3)}X_4(E_m)=-2E_m$. If
$E_{\rm bed}=-gm\kappa D_s(p^{m-1}b/q)$, exact weight accounting and
direct prolongation give
\[
 \operatorname{pr}^{(3)}X_5(E_m)+E_m=(3-m)E_{\rm bed}. \tag{S3}
\]
Thus $X_5$ is admitted at $m=3$, not at generic $m$. The PDF p. 4
prints the determining equation
$3\eta_1+\xi^2_s+2\xi^1_t=0$. Its own listed $X_4$ has
$\eta_1=\xi^2_s=\xi^1_t=1$, giving $6=0$. The printed system is
internally inconsistent; it cannot prove Proposition 1. More decisively,
the source's four-or-five count omits the verified $m=1$ fifth
generator. The corrected classification here applies only to (S1) and the
stated positive branch.

## Brackets and adjoints

Use $[A,B]=A(B)-B(A)$ and the paper's convention
\(\operatorname{Ad}(e^{\epsilon A})B=e^{-\epsilon\operatorname{ad}_A}B\).
For $m\ne1,3$, the only nonzero independent brackets are
\([X_i,X_4]=X_i\) for $i=1,2,3$. At $m=3$, additionally
\([X_1,X_5]=X_1\), \([X_2,X_5]=-2X_2\), and
\([X_3,X_5]=[X_4,X_5]=0\). At $m=1$, instead
\([X_1,X_6]=X_3\), \([X_4,X_6]=0\), and
\([X_2,X_6]=[X_3,X_6]=0\). Reversed bracket orders have opposite signs.
The implementation computes every ordered bracket from the coordinate
fields, checks all 125 ordered Jacobi triples in each five-dimensional
stratum, and constructs every elementary adjoint exponential. Source Table 2
agrees with this convention for its listed $m=3$ basis. Source Table 1
gets two reverse-order cells wrong:

| Cell | Printed | Correct |
|---|---:|---:|
| \([X_5,X_1]\) | $+X_1$ | $-X_1$ |
| \([X_5,X_2]\) | $-2X_2$ | $+2X_2$ |

## Connected-adjoint line orbits

Here equivalence means connected inner adjoint transformations, followed by
nonzero real rescaling of a one-dimensional subalgebra generator. This
specified equivalence is narrower than an unspecified full automorphism
group. The following orbit reductions are for **all** lines in the
respective classified finite-dimensional local point algebras.

For the generic four-dimensional algebra, all nontranslation lines reduce
to $X_4$. Adjoint $X_4$ scales all three translations equally, so it
fixes every line in their translation ideal. That ideal's orbit space is
\(\mathbb{RP}^2\), represented in three charts by
\(X_1+aX_2+bX_3\), \(X_2+aX_3\), and \(X_3\). The paper's list omits
the second chart's $a\ne0$ family; for example $X_2+X_3$ cannot be
conjugated to a listed pure translation or one with nonzero $X_1$.

At $m=3$, write $Z=v_1X_1+v_2X_2+v_3X_3+aX_4+bX_5$.
The commuting dilation pair acts diagonally on translations:
\[
 \operatorname{ad}_{aX_4+bX_5}|_V
   =\operatorname{diag}(-(a+b),-(a-2b),-a).
\]
For nonzero $H=aX_4+bX_5$, nonresonant translation components can be
removed. Its projective direction \((a:b)\in\mathbb{RP}^1\) cannot be
changed by inner adjoints. Exactly three directions have one zero weight:
\(X_5+cX_3\), \(X_4-X_5+cX_1\), and
\(X_4+\tfrac12X_5+cX_2\). The survivor $c\ne0$ cannot be translated
away. A complementary dilation normalizes $c$ to $+1$ or $-1$, but
connected adjoints do not flip its sign after the $H$ normalization.
The $c=0$ case is the pure $H$ already included.

For pure translations $v=(v_1,v_2,v_3)$, the exact equivalence test is
\[
 v' =\lambda(e^\epsilon v_1,e^{-2\epsilon}v_2,v_3),
 \qquad \lambda\in\mathbb R\setminus\{0\},\ \epsilon\in\mathbb R.
\]
Support and normalized relative signs are invariant. When $v_3\ne0$,
\(I=v_1^2v_2/v_3^3\) is invariant as well. Disjoint representatives are
\(X_1,X_2,X_3\); \(X_1\pm X_2\); \(X_3\pm X_1\);
\(X_3\pm X_2\); and \(X_3+\sigma X_1+KX_2\), with
\(\sigma\in\{+1,-1\}\), $K\ne0$. In the last family $K=I$.
The explicit equivalence equation, not just this normalized display,
resolves any parameter-boundary question.

At $m=1$, put
\(Z=v_1X_1+v_2X_2+v_3X_3+hX_4+cX_6\).
The elementary connected adjoints act by
\[
\begin{array}{c|l}
X_1&v_1\mapsto v_1-\epsilon h,\quad v_3\mapsto v_3-\epsilon c\\
X_2&v_2\mapsto v_2-\epsilon h\\
X_3&v_3\mapsto v_3-\epsilon h\\
X_4&(v_1,v_2,v_3)\mapsto e^\epsilon(v_1,v_2,v_3)\\
X_6&v_3\mapsto v_3+\epsilon v_1.
\end{array}
\]
Thus $h\ne0$ reduces to $X_4+\alpha X_6$, $\alpha\in\mathbb R$.
When $h=0,c\ne0$, normalize $c=1$, remove $v_3$, and obtain
$X_6$, $X_6+\sigma X_1+aX_2$ ($a\in\mathbb R$), or
$X_6+\sigma X_2$, with $\sigma=\pm1$. Only positive common scaling
of the remaining $(v_1,v_2)$ is available, so these signs persist.
When $h=c=0$, use $X_6$ to remove $v_3$ if $v_1\ne0$, giving
$X_1+aX_2$; if $v_1=0$, retain $X_2+aX_3$ and $X_3$.
These cases are disjoint by the invariant vanishing pattern of $(h,c)$
and the indicated support; the explicit adjoint actions prove coverage.

These orbit statements classify *algebra lines* under the declared
equivalence. They do not imply all associated invariant graphs exist on
the positive chart, satisfy particular data or boundary fluxes, or yield
regular ODE reductions. Those are separate gates.
