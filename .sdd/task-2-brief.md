# Task 2 brief — Determining-matrix builder

This is your requirements. Use the exact values, signatures, and test cases below verbatim.
You are building on a completed Task 1 (a jet/prolongation layer). Work strictly TEST-FIRST (TDD).

## Global Constraints (bind every task)

- **No new dependencies** beyond: `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- **Determinism:** no randomness anywhere. Stable sort for any ordering.
- **Exactness:** the determining matrix `A` has exact rational/symbolic entries (`sympy.Matrix`); rank/nullity use exact `sympy` linear algebra (no float tolerance).
- **Scope:** scalar PDEs in `(x, t, u)`, order `k <= 3`, Lie point symmetries.
- **Not a git repo.** No commits. Final step = run the task's tests green.
- **Run tests from project root** `D:\MATHs\math 4890 LieML` with `python -m pytest symm/tests -q`.

## Interfaces you CONSUME from Task 1 (already implemented — do not modify `jet.py`)

From `symm/sym_engine/jet.py`:
- `class PDE`, `PDE.scalar_1plus1(Delta, order, name, params=None)`, attribute `.x, .t, .u`, `.jet_sym(a,b)`.
- `PDE.free_jet_syms() -> list[Symbol]` — returns the jet symbols with `a+b>=1` EXCLUDING the on-shell
  leading time derivative (detected from `Delta`). For Burgers this excludes `u_t` and includes
  `u_x, u_xx, u_xt, ...`.
- `symmetry_residual(pde, tau, xi, phi) -> expr` — `pr^(k)X(Delta)` substituted on-shell, expanded,
  linear in the infinitesimals.

## Interfaces you PRODUCE (later tasks rely on these exact names/types)

In a NEW file `symm/sym_engine/determining.py`:
- `ansatz(pde, D) -> (tau, xi, phi, coeffs)` — `tau,xi,phi` are degree-`<=D` polynomials in `(x,t,u)`
  with fresh coefficient symbols; `coeffs` is the ordered `list[Symbol]`.
- `determining_matrix(pde, D) -> (A, coeffs)` — `A` is a `sympy.Matrix` with one row per
  `(x,t,u,free-jet)` monomial and one column per coefficient; `coeffs` is the column order.

## Files

- Create: `symm/sym_engine/determining.py`
- Test: `symm/tests/test_determining.py`

## Step 1 — write the failing test (`symm/tests/test_determining.py`)

```python
# symm/tests/test_determining.py
import sympy as sp
from symm.sym_engine.jet import PDE
from symm.sym_engine.determining import ansatz, determining_matrix

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde

def test_ansatz_coeff_count():
    pde = _burgers()
    tau, xi, phi, coeffs = ansatz(pde, D=2)
    # 3 infinitesimals * C(2+3,3)=10 monomials = 30 coefficients
    assert len(coeffs) == 30

def test_determining_matrix_shape_and_rank_drop():
    pde = _burgers()
    A, coeffs = determining_matrix(pde, D=2)
    assert A.cols == 30
    assert A.rows > 0
    # exact nullity must equal the Burgers algebra dimension, 5
    assert A.cols - A.rank() == 5
```

## Step 2 — run to verify it fails

`python -m pytest symm/tests/test_determining.py -q` → FAIL (module/function missing).

## Step 3 — minimal implementation (`symm/sym_engine/determining.py`)

```python
# symm/sym_engine/determining.py
import sympy as sp
from itertools import count
from .jet import symmetry_residual


def _monomials(vars_, D):
    x, t, u = vars_
    monos = []
    for du in range(D + 1):
        for dt in range(D + 1 - du):
            for dx in range(D + 1 - du - dt):
                monos.append(x**dx * t**dt * u**du)
    return monos


def ansatz(pde, D):
    x, t, u = pde.x, pde.t, pde.u
    monos = _monomials((x, t, u), D)
    ctr = count()
    coeffs = []
    parts = []
    for _label in ("tau", "xi", "phi"):
        cs = [sp.Symbol(f"c_{next(ctr)}") for _ in monos]
        coeffs.extend(cs)
        parts.append(sum(c * m for c, m in zip(cs, monos)))
    tau, xi, phi = parts
    return tau, xi, phi, coeffs


def determining_matrix(pde, D):
    tau, xi, phi, coeffs = ansatz(pde, D)
    residual = sp.expand(symmetry_residual(pde, tau, xi, phi))
    split_vars = pde.free_jet_syms() + [pde.x, pde.t, pde.u]
    poly = sp.Poly(residual, *split_vars)
    rows = []
    for _monom, c_expr in poly.terms():
        c_expr = sp.expand(c_expr)
        rows.append([c_expr.coeff(ci) for ci in coeffs])
    A = sp.Matrix(rows) if rows else sp.zeros(0, len(coeffs))
    return A, coeffs
```

## Step 4 — run to verify it passes

`python -m pytest symm/tests/test_determining.py -q` → PASS.

If `test_determining_matrix_shape_and_rank_drop` does NOT give nullity 5, do NOT change the test's
expected value. First check that `split_vars` excludes `u_t` (it must, via `free_jet_syms`). If
`A.rank()` is slow or returns a symbolic-rank issue because of the parameter `nu`, you MAY substitute
`pde.params` into `A` before calling `.rank()` (i.e. `A.subs(pde.params).rank()`) — but keep the
RETURNED `A` symbolic (substitute only for the rank computation inside the test path if needed).
Report exactly what you did.

## Step 5 — final check

Run `python -m pytest symm/tests -q` and confirm ALL tests green (Task 1's tests must still pass).

## Report contract

Write your full report to `D:\MATHs\math 4890 LieML\.sdd\task-2-report.md` (files created, exact
pytest command(s) + full output, any deviations, concerns). Then return ONLY: a one-line status
(DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT), the files list, a one-line test summary, and
any concerns. Do not paste full code/output into the returned message.
