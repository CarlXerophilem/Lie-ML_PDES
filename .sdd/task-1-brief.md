# Task 1 brief — Package scaffold and the jet / prolongation layer

This is your requirements. Use the exact values, signatures, and test cases below verbatim.
You are building the foundation module of a Lie-symmetry engine for PDEs. Work test-first (TDD):
write the failing test, run it to see it fail, implement minimally, run it to see it pass.

## Global Constraints (bind every task)

- **No new dependencies** beyond: `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- **Determinism:** no randomness anywhere. Stable sort for any ordering.
- **Exactness split:** `dim` and algebra type use exact rational linear algebra (no float tolerance). Only the `defect` (a later task) uses floating SVD.
- **Serialization:** sympy objects persist via `sympy.srepr` (later task).
- **Secrets:** any future DeepSeek access reads `DEEPSEEK_API_KEY` from env only — never hardcode (not relevant to Task 1).
- **Scope:** scalar PDEs in `(x, t, u)`, order `k <= 3`, Lie point symmetries. On-shell rule: solve `Δ=0` for the highest-order **time** derivative `(0, order)`; remaining jet variables are free split variables.
- **Not a git repo.** No commits required. Final step = run the task's tests green.
- **Run tests from project root** `D:\MATHs\math 4890 LieML` with `python -m pytest symm/tests -q`.

## Files

- Create: `symm/__init__.py` (empty)
- Create: `symm/sym_engine/__init__.py`
- Create: `symm/sym_engine/jet.py`
- Create: `symm/tests/__init__.py` (empty)
- Test: `symm/tests/test_jet.py`

## Interfaces this task PRODUCES (later tasks rely on these exact names/types)

- `class PDE` with `PDE.scalar_1plus1(Delta, order, name, params=None) -> PDE`. Attributes:
  `x, t, u` (sympy Symbols), `order` (int), `name` (str), `params` (dict symbol->float),
  `Delta` (sympy expr), `jet` (dict `(a,b)->Symbol` for `0<=a+b<=order+1`, `(0,0)` is `u`).
- `PDE.jet_sym(a, b) -> Symbol`
- `PDE.free_jet_syms() -> list[Symbol]` — jet symbols with `a+b>=1` excluding the leading time
  derivative `(0, order)`.
- `PDE.onshell() -> dict` — `{leading_time_derivative_symbol: expr}` from solving `Delta=0`.
- `PDE._init_onshell()` — (re)compute onshell; callable after setting `pde.Delta`.
- `prolong(pde, tau, xi, phi) -> dict[(a,b)->expr]` — prolongation coefficients for `1<=a+b<=order`.
- `symmetry_residual(pde, tau, xi, phi) -> expr` — `pr^(k)X(Delta)` substituted on-shell, expanded.

## Step 1 — write the failing test (`symm/tests/test_jet.py`)

Note: write CLEAN test code. The `_burgers()` helper below constructs a PDE with `Delta=None`,
sets `pde.Delta`, then calls `pde._init_onshell()`. Do not include any junk placeholder lines.

```python
# symm/tests/test_jet.py
import sympy as sp
from symm.sym_engine.jet import PDE, symmetry_residual

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde, nu

def test_known_burgers_generators_have_zero_residual():
    pde, nu = _burgers()
    t, x, u = pde.t, pde.x, pde.u
    gens = [
        (sp.Integer(1), sp.Integer(0), sp.Integer(0)),          # d_t
        (sp.Integer(0), sp.Integer(1), sp.Integer(0)),          # d_x
        (sp.Integer(0), t, sp.Integer(1)),                      # Galilean
        (2*t, x, -u),                                           # scaling
        (t**2, t*x, x - t*u),                                   # projective
    ]
    for tau, xi, phi in gens:
        r = sp.simplify(symmetry_residual(pde, tau, xi, phi))
        assert r == 0

def test_non_symmetry_has_nonzero_residual():
    pde, nu = _burgers()
    r = sp.simplify(symmetry_residual(pde, pde.u, sp.Integer(0), sp.Integer(0)))  # tau=u: not a symmetry
    assert r != 0
```

## Step 2 — run to verify it fails

`python -m pytest symm/tests/test_jet.py -q` → FAIL (module/attribute missing).

## Step 3 — minimal implementation (`symm/sym_engine/jet.py`)

```python
# symm/sym_engine/jet.py
import sympy as sp


def _jet_name(a, b):
    return "u_" + "x" * a + "t" * b if (a + b) > 0 else "u"


class PDE:
    def __init__(self, Delta, order, name, params=None):
        self.x, self.t, self.u = sp.symbols('x t u')
        self.order = int(order)
        self.name = name
        self.params = dict(params or {})
        self.jet = {(0, 0): self.u}
        for o in range(1, self.order + 2):
            for a in range(o + 1):
                b = o - a
                self.jet[(a, b)] = sp.Symbol(_jet_name(a, b))
        self.Delta = None if Delta is None else sp.sympify(Delta)
        self._onshell = {}
        if self.Delta is not None:
            self._init_onshell()

    @classmethod
    def scalar_1plus1(cls, Delta, order, name, params=None):
        return cls(Delta, order, name, params)

    def jet_sym(self, a, b):
        return self.jet[(a, b)]

    def leading_time_derivative(self):
        return self.jet[(0, self.order)]

    def free_jet_syms(self):
        lead = (0, self.order)
        return [self.jet[k] for k in sorted(self.jet) if (k[0] + k[1]) >= 1 and k != lead]

    def _init_onshell(self):
        lead = self.leading_time_derivative()
        sol = sp.solve(sp.Eq(self.Delta, 0), lead, dict=True)
        if not sol:
            raise ValueError("Delta is not solvable for the leading time derivative")
        self._onshell = sol[0]

    def onshell(self):
        return dict(self._onshell)

    def _Dx(self, f):
        f = sp.sympify(f)
        res = sp.diff(f, self.x)
        for (a, b), s in self.jet.items():
            nxt = (a + 1, b)
            if nxt in self.jet:
                res += sp.diff(f, s) * self.jet[nxt]
        return res

    def _Dt(self, f):
        f = sp.sympify(f)
        res = sp.diff(f, self.t)
        for (a, b), s in self.jet.items():
            nxt = (a, b + 1)
            if nxt in self.jet:
                res += sp.diff(f, s) * self.jet[nxt]
        return res


def prolong(pde, tau, xi, phi):
    """Prolongation coefficients phi^{(a,b)} for 1 <= a+b <= pde.order."""
    tau, xi, phi = map(sp.sympify, (tau, xi, phi))
    P = {(0, 0): phi}
    for o in range(1, pde.order + 1):
        for a in range(o + 1):
            b = o - a
            if a >= 1:
                prev = P[(a - 1, b)]
                P[(a, b)] = (pde._Dx(prev)
                             - pde.jet[(a, b)] * pde._Dx(xi)
                             - pde.jet[(a - 1, b + 1)] * pde._Dx(tau))
            else:
                prev = P[(0, b - 1)]
                P[(0, b)] = (pde._Dt(prev)
                             - pde.jet[(1, b - 1)] * pde._Dt(xi)
                             - pde.jet[(0, b)] * pde._Dt(tau))
    return {k: v for k, v in P.items() if (k[0] + k[1]) >= 1}


def symmetry_residual(pde, tau, xi, phi):
    tau, xi, phi = map(sp.sympify, (tau, xi, phi))
    P = prolong(pde, tau, xi, phi)
    expr = (tau * sp.diff(pde.Delta, pde.t)
            + xi * sp.diff(pde.Delta, pde.x)
            + phi * sp.diff(pde.Delta, pde.u))
    for (a, b), coeff in P.items():
        expr += coeff * sp.diff(pde.Delta, pde.jet[(a, b)])
    return sp.expand(expr.subs(pde.onshell()))
```

## Step 4 — run to verify it passes

`python -m pytest symm/tests/test_jet.py -q` → PASS (both tests).

## Step 5 — final check

Run `python -m pytest symm/tests -q` and confirm green. No commit needed (not a git repo).

## Report contract

Write your full report to `D:\MATHs\math 4890 LieML\.sdd\task-1-report.md` containing: files
created, the exact pytest command(s) run and their output (pass/fail counts), any deviations from
the brief, and any concerns. Return only: a one-line status (DONE / DONE_WITH_CONCERNS / BLOCKED /
NEEDS_CONTEXT), the list of files, a one-line test summary, and any concerns.
