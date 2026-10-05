# PDE formalization and a checked reduction algorithm

The first executable methodology uses the existing `symm.generic` kernel.
It reduces a supplied projectable one-generator action in a supplied local
chart. It verifies candidates rather than claiming to discover every symmetry.
The mathematical exposition is in `draft/main.tex`; the working checklist is
`checklist.md`. The prior generic architecture and scalar APIs are retained.

## Mathematical input

`PDEProblem` consists of:

| Part | Mathematical role | Python representation |
| --- | --- | --- |
| Base and fields | `p` independent variables and `q` field coordinates | `JetSpace` |
| Jets | `u[a,J]`, `|J| <= n`, including data derivatives | `jet_symbol(a,J)` |
| Equations | `r` residual expressions equal to zero, possibly `r != q` | `DifferentialSystem.equations` |
| Inequations | Expressions required to be nonzero | `DifferentialSystem.inequations` |
| Parameters | Fixed symbols, distinct from coordinates | `PDEProblem.parameters` |
| Domain | Real-branch and sign predicates, including jet conditions | `PDEProblem.domain` |
| Data | Residual equations on `surface = 0` | `DataCondition(name,surface,residuals)` |

Use residual expressions, not `Eq` objects, for equations. Use Boolean
predicates for the domain. Unknown symbols, unevaluated derivatives and
out-of-budget jets are rejected. Source expressions must already represent
smooth functions on the specified real branch. The code cannot reconstruct a
denominator that SymPy canceled *before* the problem was supplied; declare
such exclusions explicitly as inequations.

Jet names preserve the legacy generic convention: suffix `x` means a
derivative with respect to the **first** coordinate, `y` the second, etc.
Thus with coordinates `(t,s)`, `phi_x` means `phi_t`, and with `(sigma,)`,
`F_x` means `F_sigma`. Always construct jets by multi-index, not by parsing
these display names. This release preserves that convention rather than
changing old serialized records.

`jet_structure` reports polynomial, rational or nonpolynomial dependence on
the field jets. Coefficients may depend on base coordinates and parameters.
This classification is neither a polynomial assumption on solutions nor a
completeness result for a polynomial generator search. Denominator guards
are reported even if the dependence is polynomial in jets.

## Reduction contract

Supply `ReductionChart` with:

1. A fresh reduced `JetSpace` of dimension `p-1`, with `q` profile coordinates.
2. The invariant functions `I(x)` and an orbit coordinate `R(x)`.
3. The inverse base map `x=H(z,rho)`.
4. An affine reconstruction `u=C(x)U+b(x)`, using fresh profile symbols.
5. One nonzero source-coordinate factor `a_A(x)` per equation.

Supply a `PointGenerator` and, when needed, an `r` by `r` matrix `M(x)`.
Its default is zero. All these expressions may depend on declared fixed
parameters. Derivative-dependent and nonprojectable generators are not
supported by this first chart reducer.

The algorithm checks, in order:

1. Dimensions, fresh namespaces and allowed expression dependencies.
2. `X(I)=0`, nonzero orbit speed, local base rank, and both inverse identities.
3. Affine fiber reconstruction and nonzero fiber determinant.
4. The exact sufficient symmetry identity `pr(X) Delta = M Delta`.
5. Jet pullbacks, generated recursively by the chain rule.
6. The invariant-surface equations after reconstruction.
7. `pullback(Delta_A)=a_A R_A`, with no orbit variable in `R_A`.
8. Preservation of domain, inequations, denominator guards and data traces.

The result contains the reduced system, checks, residual identities,
fingerprints, pulled constraints and regularity conditions. Conditions still
depending on `rho` remain in the outcome even when they cannot be inserted
into the reduced system alone. **Retain the entire outcome**, not just its
reduced equations. All guard statements are conditions on the local chart;
the routine does not prove that their intersection contains a solution.

The exact identities are sufficient to justify local invariant PDE reduction
under the recorded smoothness and regularity assumptions. They do not require
a complete symmetry classification. Conversely, failure of the supplied
multiplier/chart test is not a proof that no other symmetry or reduction exists.
General invariants, nonlinear fiber charts, differential-operator multipliers,
and nonclassical symmetries require further implementation.

Data have a separate `pulled-back-only` status. For example, a traveling chart
`z=x-c*t`, `rho=t`, `u=U(z)` maps data `u(0,x)=x^2` to the constraint
`U-(z+c*rho)^2=0` on `rho=0`. This is an exact trace expression, not a proof
of existence, compatibility, or invariance of the original IBVP.

## Run the SVE example

From the repository root:

```powershell
python -B -m symm.generic.sve_reduction
python -B -m symm.generic.sve_reduction --m 4
```

The first command verifies the supplied cubic scaling and emits its reduced
ODE and guards as JSON to stdout. The second intentionally exits with code 2:
the supplied cubic symmetry identity fails for `m=4`. It does not claim absence
of all noncubic symmetries. No files are written by either command.

```python
from symm.generic import reduce_in_chart
from symm.generic.sve_reduction import sve_scaling_case

problem, X, chart, M = sve_scaling_case(m=3)
result = reduce_in_chart(problem, X, chart, symmetry_multipliers=M)
assert result.certificate.status == "verified"
print(result.reduced_system.equations)
print(result.pulled_domain)
print(result.regularity_conditions)
```

Here `beta=m*kappa`, with `kappa=A_g*xi_sed` fixed. The chart is
`sigma=s*t**2`, `rho=t`, `t=rho`, `s=sigma/rho**2`, and `phi=F(sigma)`.
The factor identity is `E_3[phi]=R_0[F]/t`, for arbitrary smooth admissible
profiles; a reduced solution is required to make that residual vanish.
For numerical IVP use, additionally exclude zeros of the coefficient of
`F'''` before solving explicitly for that derivative. The symbolic reducer
does not divide by that coefficient.

## Verification and source boundary

Tests include a hand-derived third-order SVE ODE and direct differentiation
of a nonpolynomial reconstructed field, mixed derivatives with field scaling,
a two-field three-equation system reduced from three to two variables, data
traces, retained domain denominators, and rejection of invalid charts or guards.

```powershell
python -B -m pytest symm/tests/test_chart_reduction.py -q -p no:cacheprovider
python -B -m pytest -q -p no:cacheprovider --ignore=symm/test_ml_pde_solver.py
python -B symm/test_ml_pde_solver.py
```

The last file is an existing standalone check script that exits at module
level, so importing it during bare pytest collection aborts collection.
Run it separately as shown. On 2026-09-25, the pytest suite passed 130 tests
(including 19 new tests), and the standalone script passed 22 internal checks.
The Windows pytest cleanup warning and PDF build details are in `checklist.md`.

The classical local invariant-reduction framework is described by Olver,
*Applications of Lie Groups to Differential Equations*, 2nd edition (1993).
The worked equation and cubic scaling come from Paliathanasis, Leon and Leach,
*Mathematics* 14, 433 (2026), DOI `10.3390/math14030433`, Eq. (7),
Proposition 1 and Table 3. The implemented reduced residual is obtained by
independent substitution; the paper's printed reduced formulas and tables
are not copied as correctness certificates. Interpretation as the full
physical SVE system retains the coordinate-conversion qualification in the
manuscript. No ML accuracy or speedup is claimed by this algorithm.
