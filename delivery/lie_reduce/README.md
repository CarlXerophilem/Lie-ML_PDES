# Checked Lie reduction, without ML

This is a new pipeline, separate from the three maintained symbolic entries. The
manuscript and legacy learning results are unchanged. It accepts vector PDEs and
computes point prolongations without importing the old P/M prolongation engine.

Run from the repository root (Python 3.10+, SymPy 1.14):

```sh
PYTHONPATH=delivery python -B -m lie_reduce.frozen_PM
PYTHONPATH=delivery python -B -m lie_reduce.test_pipeline
PYTHONPATH=delivery python -B -m lie_reduce.run --catalogue --stage-seconds 15
```

`results/pipeline.json` contains equations, generators, basis coordinates, graph
conditions, first-integral identities, leading coefficients, stage timings,
CPU/RSS accounting, environment and source hashes. `results/ODE_INVENTORY.md`
lists every computed ODE. `results/SUMMARY.md` records status counts. RSS is the
process high-water mark, **not** an individual stage's incremental memory.
The schema is a **symbolic provenance extension** of Definition 6.1, not a
numerical error certificate or trained-model record.

## What is secured

- `frozen/` preserves the P/M proof sources and their complete JSON, byte-hashed.
  `frozen_PM` runs the frozen source in its own process and compares the JSON.
  It preserves the pre-existing output-only `V = F - P*z` binding addition.
- `JetSpace` supports any number of independent and dependent variables and a
  declared finite jet order. Independent tests compare every third-order
  coefficient with the frozen prolongation for nonlinear point fields.
- `PDESpec` specifies PDEs, principal derivatives, parameters and positive
  quantities. No principal coefficient is assumed positive. A unique explicit
  principal chart is required and denominator exclusions are returned.
- `symmetries` solves the full coefficient system within the declared polynomial
  point-field class, degree 2 by default. P/M and E1 are replayed at m=1,2,3,4;
  P/M bases are compared by span with the immutable JSON, not by list order.
  An unrelated heat equation regression exercises the same engine.
- Appendix B representatives are explicit inputs. Their membership, brackets,
  local graphs, scalar weights and reduced equations are computed. The
  representative catalogue itself is **not** discovered or proved optimal by
  this program. Connected-chart equivalence is not inferred from algebraic
  conjugacy. Each graph carries its pulled-back positivity conditions.
- Table 3.2 graph pullbacks are checked against a separately differentiated
  frozen PDE implementation. Source X5 is manuscript Y5. Printed Eq. (25)
  remains refuted; the correct PDE pullback and exact source witnesses are
  both exported. P and M remain distinct equations.
- E2 uses an explicit polar rank-two section, not a planar optimal system.
  All four balances are pulled back, three first-integral identities are
  verified and elimination gives undivided `D H' = N`. The two critical slopes
  are computed from D and N. No division by D occurs at the critical point.

## Explicit boundaries

1. Polynomial splitting currently requires polynomial jet dependence after
   clearing denominators. **Symbolic noninteger m is unsupported in the new
   discovery engine.** Tests at four exponents do not prove an all-real-m
   classification. That claim remains supported by the frozen smooth-class
   proof. The generic catalogue row is instantiated at m=2 and m=4.
2. Multivariate rank drops are the common zero set of the maximal-minor ideal,
   including denominator exclusions. Separate univariate gcds are unsound:
   `[a,b]` loses rank at `(0,0)` despite having gcd 1. Enumeration is capped;
   exceeding the cap is explicitly `not_computed`. Further stratification is
   not silently claimed.
3. Automatic graph construction covers diagonal affine base flows and affine
   vertical flows (including the printed m=1 boost). Other flows require an
   explicit graph. Rewriting in orbit coordinates avoids expensive comparisons
   of equivalent `Subs(Derivative(...))` expressions.
4. Positive quantities that vanish identically give `chart-incompatible`;
   undecided profile inequalities remain conditions, not a positivity proof.
   Nonzero projection, equal orbit/base ranks and transversality are necessary;
   **subalgebra dimension alone is not orbit rank**.
5. A verified Euler-operator zero is a local exactness test. The implemented
   flux constructor must additionally pass its differentiated identity. A
   leading-coefficient zero is only a singularity candidate. `dsolve` is not
   used as an unrestricted or higher-order Lie solver.
6. `to_task` exports a local regular scalar normal form only after checking
   the initial denominator. It does not certify an entire interval. N1 and
   N2 interface records are exported; N2 uses a short smoke-test interval,
   not the later fold-distance experiment. N3 is an implicit critical task
   with `picard_rhs: null` until the BB normal form and its bounds are verified.
   The chapter-six benchmark/ML implementation is therefore still gated.
7. Every symbolic stage has a time limit. Failed, unsupported, chart-incompatible
   and timed-out outcomes are retained. No experiment invokes ML.

## Changes to the proposed implementation

The existing `_positive_unit` is left frozen: its caller already divides by
its return value. A positive dummy check can be sufficient on a larger domain;
changing it mechanically to `m=1+mu` is not itself a proof improvement.
Similarly, a two-dimensional subalgebra in two independent variables need not
have base rank two. Optimal-system enumeration does not waive the rank check.
The annular, printed, compatible and exchange models retain their distinct
balance counts and claims.
