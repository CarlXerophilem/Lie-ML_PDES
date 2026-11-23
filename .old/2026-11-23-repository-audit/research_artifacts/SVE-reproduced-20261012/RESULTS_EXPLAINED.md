# Reading the reproduction and animated solutions

## Is the paper all correct?

No. Several conclusions survive independent checks, but some printed
formulas and classification claims do not. This conclusion concerns the
supplied v3 paper, with each comparison tied to its displayed equation.

The four generic generators are valid; the additional cubic generator is
valid at `m=3`. The positive-chart calculation also admits `t*d_phi` at
`m=1`, which the paper omits. Table 1 has two reversed-commutator sign errors;
the printed optimal system misses connected-adjoint families. The original
Eulerian bed pullback has an advective term missing from the printed scalar
derivation. We keep that printed scalar equation as the reproduction target.

Equations (24)--(31) and (33)--(34), read literally, fail exact
original-equation substitution tests. Equation (32) needs qualification and
correction of the invariant variables. These counterexamples refute the
universal formulas; they do not refute every special solution. In particular,
the cubic power solution remains exact, with a singular normal-form caveat.

For a concrete check of (24), take `m=3`, `g=1`, `kappa=1/30`, reduced
coordinate `z=1`, and `(F,F',F'')=(2,1/2,1/10)`. Its printed equation gives
`F'''=23/250`. Substituting that jet into the original master equation
instead gives `2367/5000`, not zero. This is an exact rational discrepancy,
not a solver-tolerance effect. See `results/REPORT.md` for the complete audit.

## What is the reconstructed two-dimensional field?

An ODE supplies a curve `F(z)`. A similarity transformation turns it into a
field on two independent variables, time `t` and material coordinate `s`.
The field `x=phi(t,s)` is the particle-position map, **not the water depth**.
With the normalized mass coordinate, velocity is `u=phi_t` and depth is
`h=1/phi_s`. This is one spatial dimension plus time, not two spatial
dimensions. An Eulerian spatial plot could instead use `x=phi(t,s)` as its
horizontal coordinate when `phi_s>0`; material-coordinate calculations use `s`.

| Source equations | Corrected reconstruction | Velocity | Depth |
|---|---|---|---|
| (24) | `z=s/t`, `phi=t F(z)` | `F-z F'` | `1/F'` |
| (25)--(27), `m=3` | `z=s t^2`, `phi=F(z)` | `2 s t F'` | `1/(t^2 F')` |
| (28)--(31), `alpha=-1` | `z=s+t`, `phi=F(z)` | `F'` | `1/F'` |
| (32), corrected graph | `phi=s+F(t)` | `F'(t)` | `1` |
| (33), `alpha=-1, alpha3=1` | `z=s+t`, `phi=t+F(z)` | `1+F'` | `1/F'` |

For example, the common-scaling initial jet at `z=1` has `F=2`, `F'=0.5`.
At `t=s=1` it reconstructs `phi=2`, `u=1.5`, `h=2`. The program then uses
the numerical profile over its solved interval to reconstruct the local patch.

The retained `reconstruct_profile_fields()` function evaluates a local patch
from a supplied profile interpolant and masks coordinates outside its solved
interval or positive chart. Their boundaries are data limits, not wavefronts.
The HTML animation was retired in the computation-only revision. Kinematic
depth/velocity do not establish that the field solves the advectively corrected
full bed system; interpolation supplies no continuous error bound.

Equations (24)--(33) are not ten independent numerical IVPs. Equations
(26)/(29) describe `mu=F'`; (27) uses `(Sigma,M)=(z^(2/3)F',z^(5/3)F'')`;
(30)/(31) use `(P,C)=(F',F'')`. These further reductions share the
same underlying profile. The transformed curves are parametric; treating
them as single-valued functions requires a nonzero transformed-coordinate
derivative. Each source number is explicitly labeled as a corrected reduction.

## What would a variational Lagrangian add?

Material (Lagrange) coordinates and a variational Lagrangian are different
ideas. A genuine variational formulation specifies an action, for example
`S[phi]=integral L(t,s,phi,derivatives of phi) dt ds`, whose Euler--Lagrange
equation is proved equivalent to the intended model on a stated domain.

It could add:

1. **Noether currents.** A symmetry preserving the action up to a boundary
   divergence gives a conservation law `D_t J^t + D_s J^s = 0` on solutions.
   Time or space translations can yield energy or momentum currents when
   the particular action has those variational symmetries. A Lie symmetry
   of the equation need not preserve the action.
2. **Further order reduction.** A current compatible with a similarity
   ansatz may yield an ODE first integral. It must be derived and checked for
   independence; it need not improve on the first integrals already found here.
3. **Additional numerical structure.** Discretizing the action can guide
   variational integrators and useful conservation diagnostics. Conservation,
   stability, and accuracy still require checks; RKF45 does not become a
   variational integrator merely because a Lagrangian exists.

An auxiliary-field construction such as `L=v E[phi]` produces the original
equation by varying `v`, but also produces an adjoint equation by varying
`phi`. That enlarged system is not automatically the sought original-field
Lagrangian. Nor would any variational formulation repair an incorrect
reduction or turn a printed scalar solution into a full physical SVE solution.
The source reports not finding a Lagrangian; this reproduction does not prove
that none exists.

## What does the convergence check show?

The new experiment separates fixed-step refinement from adaptive tolerance
refinement. All 21 regular IVPs complete both sweeps. The fifth-order accepted
Fehlberg state approaches empirical order five on the scaling examples:
last resolved orders are 4.97--4.98 for (24), and 4.93 for (25).

The short traveling examples have only one resolved adjacent pair each,
around 4.95--4.97; subsequent errors are too close to the reference/roundoff
floor to estimate an order. The quadratic (32) is an exact control with no
measurable nontrivial order. Tightening tolerance reduces error for the
scaling examples, but the short traveling problems retain the same two steps
through this sweep and therefore do not show tolerance convergence.

The exact non-polynomial control `y'=y` independently approaches order five.
No `t_eval` grid forces the adaptive steps. The floor decision is an explicit
resolution screen, not an error theorem. Read `docs/CONVERGENCE.md` and
`results/convergence/convergence.json` for every error, count and qualification.

## Run and edit

The implementation is ordinary source inside `main.py`; there is no local
runtime implementation package. The default calculates new results; the
report-only option merely formats existing evidence and checks its code hash.
See `docs/COMPUTATION.md` for the live-computation map.

```powershell
python main.py
python main.py --stage convergence
python main.py --stage series
python main.py --stage plots
```

`main.py` can also run alone when copied to another directory with the listed
third-party dependencies installed. If the reference PDFs are absent, their
verification status is explicitly unavailable; `--repo-root PATH` can point
to the original checkout. The prior modular release is retained in
`archive/release-before-animation.zip`.
