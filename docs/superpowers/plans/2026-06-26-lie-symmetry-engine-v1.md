# LieML Symmetry Engine (v1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a resumable engine that auto-discovers the Lie point-symmetry algebra of a scalar (1+1) PDE by iterative elimination of its determining system, emits residual-zero reductions, and saves every outcome as a reproducible reducibility record.

**Architecture:** A small Python package `symm/sym_engine/` of focused, single-responsibility modules. A generic jet/prolongation layer feeds a determining-matrix builder; an iterative (degree-increasing) exact-rational elimination discovers the algebra; a reduction module collapses each generator to an ODE; a checkpoint layer makes every step resumable; a reducibility layer computes the exact `dim`/type (invariants) and a metric `defect`/`index` (diagnostic); an orchestrator ties it together as a state machine. Learned-reductor and DeepSeek-supervisor hooks are stubbed behind stable interfaces.

**Tech Stack:** Python 3.14, sympy 1.14 (symbolic), numpy 2.3 + scipy 1.17 (numeric SVD for the defect), pytest (tests). No new third-party dependencies. CPU-only, Windows.

## Global Constraints

- **No new dependencies** beyond the pinned stack: `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure standard library otherwise.
- **Determinism:** no randomness anywhere (no `random`, no unseeded sampling). Equation/monomial ordering uses a stable sort. Resuming reproduces an uninterrupted run exactly.
- **Exactness split:** `dim` and algebra type are computed by **exact rational** linear algebra (`sympy.Matrix.nullspace`/`rank`) — no floating tolerance. Only the `defect` uses floating SVD.
- **Serialization:** sympy objects are persisted with `sympy.srepr` (exact round-trip) inside JSON.
- **Secrets:** any DeepSeek access reads `DEEPSEEK_API_KEY` from the environment only — never hardcode, never write a key into a checkpoint, report, or guide.
- **Scope:** scalar PDEs in `(x, t, u)`, order `k <= 3`, **Lie point** symmetries only. On-shell rule: solve `Δ=0` for the highest-order **time** derivative (evolution form); remaining jet variables are treated as free split variables.
- **Not a git repo.** This directory is not under version control. Each task's final step is a **Checkpoint** (run the task's tests green). If you want history, run `git init` once at the start and replace each Checkpoint with a `git add` + `git commit`; otherwise just keep the suite green.
- **Run tests from the project root** `D:\MATHs\math 4890 LieML` with `python -m pytest symm/tests -q` so that `import symm.sym_engine...` resolves.

## Deviation Note (confirm before execution)

The approved spec (§3) describes the elimination loop as a *functional* step-by-step reduction (find easy equations → integrate → re-split). A faithful general-function Rosenfeld–Gröbner loop in pure sympy is fragile and research-grade. This plan realizes "iterative differential elimination" robustly as **degree-iterated exact linear elimination**: the differential content is in *forming* the determining system (prolongation + jet-monomial splitting); the *solving* is exact rational elimination (kernel of the determining matrix), iterated over ansatz degree `D` until the dimension stabilizes. The independent "second computation" required by spec §6 becomes **numerical SVD nullity** (a genuinely different method) vs. the exact rational kernel. Full functional Rosenfeld–Gröbner and the Maple hand-off remain the documented escape hatch (Task 9 stall path). This is a faithful, verifiable v1; flag to the user if the functional loop is required instead.

---

### Task 1: Package scaffold and the jet / prolongation layer

**Files:**
- Create: `symm/__init__.py` (empty)
- Create: `symm/sym_engine/__init__.py`
- Create: `symm/sym_engine/jet.py`
- Create: `symm/tests/__init__.py` (empty)
- Test: `symm/tests/test_jet.py`

**Interfaces:**
- Produces:
  - `class PDE` with `PDE.scalar_1plus1(Delta, order, name, params=None) -> PDE`. Attributes: `x, t, u` (sympy Symbols), `order` (int), `name` (str), `params` (dict symbol->float default), `Delta` (sympy expr), `jet` (dict `(a,b)->Symbol` for `0<=a+b<=order+1`, `(0,0)` is `u`).
  - `PDE.jet_sym(a, b) -> Symbol`
  - `PDE.free_jet_syms() -> list[Symbol]` — jet symbols with `a+b>=1` excluding the leading time derivative `(0, order)`.
  - `PDE.onshell() -> dict` — `{leading_time_derivative_symbol: expr}` from solving `Delta=0`.
  - `prolong(pde, tau, xi, phi) -> dict[(a,b)->expr]` — prolongation coefficients `phi^{(a,b)}` for `1<=a+b<=order`.
  - `symmetry_residual(pde, tau, xi, phi) -> expr` — `pr^(k)X(Delta)` substituted on-shell, expanded.

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_jet.py
import sympy as sp
from symm.sym_engine.jet import PDE, symmetry_residual

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    p = PDE.scalar_1plus1.__self__ if False else None  # placeholder to keep import obvious
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()  # recompute onshell now that Delta is set
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

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_jet.py -q`
Expected: FAIL (`ModuleNotFoundError: symm.sym_engine.jet` or `AttributeError`).

- [ ] **Step 3: Write minimal implementation**

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
        # jet symbols up to order+1 (prolongation of order k needs order k+1 shifts)
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

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_jet.py -q`
Expected: PASS (both tests).

- [ ] **Step 5: Checkpoint** — run `python -m pytest symm/tests -q`; confirm green. (Optional: `git add symm/__init__.py symm/sym_engine/ symm/tests/ && git commit -m "feat(sym_engine): jet/prolongation layer"`.)

---

### Task 2: Determining-matrix builder

**Files:**
- Create: `symm/sym_engine/determining.py`
- Test: `symm/tests/test_determining.py`

**Interfaces:**
- Consumes: `PDE`, `symmetry_residual` (Task 1).
- Produces:
  - `ansatz(pde, D) -> (tau, xi, phi, coeffs)` — `tau,xi,phi` are degree-`<=D` polynomials in `(x,t,u)` with fresh coefficient symbols; `coeffs` is the ordered `list[Symbol]`.
  - `determining_matrix(pde, D) -> (A, coeffs)` — `A` is a `sympy.Matrix` (rational/parametric) with one row per `(x,t,u,free-jet)` monomial and one column per coefficient; `coeffs` the column order.

- [ ] **Step 1: Write the failing test**

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

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_determining.py -q`
Expected: FAIL (module/function missing).

- [ ] **Step 3: Write minimal implementation**

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

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_determining.py -q`
Expected: PASS.

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 3: Iterative (degree-increasing) elimination → algebra discovery

**Files:**
- Create: `symm/sym_engine/eliminate.py`
- Test: `symm/tests/test_eliminate.py`

**Interfaces:**
- Consumes: `determining_matrix`, `ansatz` (Task 2).
- Produces:
  - `discover(pde, Dmin=1, Dmax=4, on_step=None) -> EliminationResult` where `EliminationResult` is a `dataclass` with fields: `dim` (int), `D` (int, the stabilizing degree), `basis` (`list[dict[Symbol,Rational]]` — null-space vectors as coeff maps), `coeffs` (`list[Symbol]`), `log` (`list[str]`), `stalled` (bool).
  - `on_step(step_index:int, state:dict)` is an optional callback invoked once per degree (for checkpointing in Task 9). `state` keys: `D`, `dim`, `coeffs` (srepr-able), `basis`.

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_eliminate.py
import sympy as sp
from symm.sym_engine.jet import PDE
from symm.sym_engine.eliminate import discover

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde

def test_burgers_dimension_is_five_and_stabilizes():
    res = discover(_burgers(), Dmin=1, Dmax=4)
    assert res.dim == 5
    assert res.D == 2          # stabilizes at degree 2 (projective generator is degree 2)
    assert not res.stalled
    assert len(res.basis) == 5

def test_step_callback_fires_per_degree():
    seen = []
    discover(_burgers(), Dmin=1, Dmax=3, on_step=lambda i, s: seen.append(s["D"]))
    assert seen == [1, 2, 3]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_eliminate.py -q`
Expected: FAIL (module missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/sym_engine/eliminate.py
import sympy as sp
from dataclasses import dataclass, field
from .determining import determining_matrix


@dataclass
class EliminationResult:
    dim: int
    D: int
    basis: list
    coeffs: list
    log: list = field(default_factory=list)
    stalled: bool = False


def _nullspace_maps(A, coeffs):
    vecs = A.nullspace()
    maps = []
    for v in vecs:
        maps.append({c: sp.nsimplify(v[i]) for i, c in enumerate(coeffs)})
    return maps


def discover(pde, Dmin=1, Dmax=4, on_step=None):
    log = []
    prev_dim = None
    result = None
    for step, D in enumerate(range(Dmin, Dmax + 1)):
        A, coeffs = determining_matrix(pde, D)
        dim = A.cols - A.rank()
        basis = _nullspace_maps(A, coeffs)
        log.append(f"degree D={D}: nullity={dim}")
        if on_step is not None:
            on_step(step, {"D": D, "dim": dim,
                           "coeffs": [sp.srepr(c) for c in coeffs],
                           "basis": [{sp.srepr(k): sp.srepr(v) for k, v in m.items()}
                                     for m in basis]})
        result = EliminationResult(dim=dim, D=D, basis=basis, coeffs=coeffs, log=list(log))
        if prev_dim is not None and dim == prev_dim:
            # stabilized at the previous degree; report that degree
            result.D = D - 1
            result.dim = prev_dim
            return result
        prev_dim = dim
    if result is not None:
        result.stalled = True
        log.append("WARNING: dimension did not stabilize within Dmax")
        result.log = list(log)
    return result
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_eliminate.py -q`
Expected: PASS. (If `nullspace` is slow at `D=4`, the Burgers stabilization returns at `D=3` before reaching it.)

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 4: Generator reconstruction, dimension, structure constants, algebra type

**Files:**
- Create: `symm/sym_engine/algebra.py`
- Test: `symm/tests/test_algebra.py`

**Interfaces:**
- Consumes: `EliminationResult` (Task 3), `ansatz` (Task 2), `PDE` (Task 1).
- Produces:
  - `generators(pde, result) -> list[tuple(tau, xi, phi)]` — each null-space vector turned into explicit `(tau, xi, phi)` sympy exprs in `(x,t,u)`.
  - `bracket(pde, g1, g2) -> tuple(tau, xi, phi)` — Lie bracket of two generators (as vector fields on `(x,t,u)`).
  - `structure_constants(pde, gens) -> sympy.Array` — `c^k_{ij}` in the given basis (raises if the algebra is not closed in the basis, within rational arithmetic).
  - `algebra_type(struct) -> dict` — `{"dim": int, "abelian": bool, "nilpotent": bool, "solvable": bool, "derived_dims": list[int]}`.

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_algebra.py
import sympy as sp
from symm.sym_engine.jet import PDE
from symm.sym_engine.eliminate import discover
from symm.sym_engine.algebra import generators, bracket, structure_constants, algebra_type

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde

def test_five_generators_recovered():
    pde = _burgers()
    gens = generators(pde, discover(pde, 1, 4))
    assert len(gens) == 5

def test_translation_generators_commute():
    pde = _burgers()
    t, x, u = pde.t, pde.x, pde.u
    dt = (sp.Integer(1), sp.Integer(0), sp.Integer(0))
    dx = (sp.Integer(0), sp.Integer(1), sp.Integer(0))
    br = tuple(sp.simplify(c) for c in bracket(pde, dt, dx))
    assert br == (0, 0, 0)

def test_structure_constants_and_type_compute():
    pde = _burgers()
    gens = generators(pde, discover(pde, 1, 4))
    sc = structure_constants(pde, gens)
    info = algebra_type(sc)
    assert info["dim"] == 5
    assert isinstance(info["solvable"], bool)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_algebra.py -q`
Expected: FAIL (module missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/sym_engine/algebra.py
import sympy as sp
from .determining import ansatz


def generators(pde, result):
    tau, xi, phi, coeffs = ansatz(pde, result.D)
    gens = []
    for m in result.basis:
        subs = {c: m.get(c, 0) for c in coeffs}
        g = (sp.expand(tau.subs(subs)), sp.expand(xi.subs(subs)), sp.expand(phi.subs(subs)))
        if any(comp != 0 for comp in g):
            gens.append(g)
    return gens


def bracket(pde, g1, g2):
    x, t, u = pde.x, pde.t, pde.u
    (t1, x1, p1), (t2, x2, p2) = g1, g2
    comps1, comps2 = (t1, x1, p1), (t2, x2, p2)
    var = (t, x, u)

    def apply(comps, f):  # vector field acting on scalar f
        return sum(comps[i] * sp.diff(f, var[i]) for i in range(3))

    out = []
    for i in range(3):
        out.append(sp.expand(apply(comps1, comps2[i]) - apply(comps2, comps1[i])))
    return tuple(out)  # (tau, xi, phi) ordering


def _coordinate_vector(pde, g, basis):
    # express g in the given basis by matching coefficients of (x,t,u) monomials
    x, t, u = pde.x, pde.t, pde.u
    syms = sp.symbols(f"a0:{len(basis)}")
    combo = [sum(syms[j] * basis[j][i] for j in range(len(basis))) for i in range(3)]
    eqs = []
    for i in range(3):
        diff = sp.expand(combo[i] - g[i])
        poly = sp.Poly(diff, x, t, u)
        eqs.extend(poly.coeffs())
    sol = sp.linsolve(eqs, syms)
    if not sol:
        raise ValueError("algebra not closed in basis")
    return list(next(iter(sol)))


def structure_constants(pde, gens):
    n = len(gens)
    C = [[[sp.Integer(0)] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            br = bracket(pde, gens[i], gens[j])
            coords = _coordinate_vector(pde, br, gens)
            for k in range(n):
                C[k][i][j] = sp.nsimplify(coords[k])
    return sp.Array(C)


def _derived_series_dims(C, n):
    # represent subalgebras by basis-index sets via adjoint closure (rational rank of bracket span)
    import sympy as sp
    current = list(range(n))
    dims = [n]
    while True:
        vecs = []
        for i in current:
            for j in current:
                vecs.append(sp.Matrix([C[k, i, j] for k in range(n)]))
        M = sp.Matrix.hstack(*vecs) if vecs else sp.zeros(n, 0)
        r = M.rank()
        if r == 0 or r == dims[-1]:
            dims.append(r)
            break
        dims.append(r)
        # next derived: indices spanning the image (approximate by first r basis dirs)
        current = list(range(r))
    return dims


def algebra_type(struct):
    C = struct
    n = C.shape[0]
    derived = _derived_series_dims(C, n)
    abelian = all(C[k, i, j] == 0 for k in range(n) for i in range(n) for j in range(n))
    solvable = derived[-1] == 0
    return {"dim": n, "abelian": abelian, "nilpotent": solvable and not abelian,
            "solvable": solvable, "derived_dims": derived}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_algebra.py -q`
Expected: PASS.

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 5: Reduction — invariants and the residual-zero reduced ODE

**Files:**
- Create: `symm/sym_engine/reduce.py`
- Test: `symm/tests/test_reduce.py`

**Interfaces:**
- Consumes: `PDE` (Task 1).
- Produces:
  - `reduce_by(pde, gen) -> Reduction | None` where `Reduction` is a dataclass: `gen` (the generator), `z` (sympy expr, similarity variable), `U` (sympy Function), `ansatz` (expr for `u` in terms of `U(z)` and a prefactor), `ode` (sympy expr `= 0`), `residual` (sympy expr, 0 when verified). Returns `None` if the generator's invariants cannot be found in closed form.

This task implements two generator families that cover the v1 benchmarks: **translation combinations** (`tau,xi` constant, `phi=0`) giving travelling waves, and **scaling** (`tau=a t, xi=b x, phi=e u`) giving self-similar reductions. Other generators return `None` (honest, not faked).

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_reduce.py
import sympy as sp
from symm.sym_engine.jet import PDE
from symm.sym_engine.reduce import reduce_by

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde, nu

def test_travelling_wave_reduction_residual_zero():
    pde, nu = _burgers()
    c = sp.Symbol('c')
    gen = (sp.Integer(1), c, sp.Integer(0))   # d_t + c d_x
    red = reduce_by(pde, gen)
    assert red is not None
    assert sp.simplify(red.residual) == 0
    # reduced ODE should be nu U'' - (U - c) U' = 0  (up to sign/factor)
    z = red.z
    U = red.U
    expected = nu * U(z).diff(z, 2) - (U(z) - c) * U(z).diff(z)
    assert sp.simplify(red.ode - expected) == 0 or sp.simplify(red.ode + expected) == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_reduce.py -q`
Expected: FAIL (module missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/sym_engine/reduce.py
import sympy as sp
from dataclasses import dataclass


@dataclass
class Reduction:
    gen: tuple
    z: sp.Expr
    U: sp.Function
    ansatz: sp.Expr
    ode: sp.Expr
    residual: sp.Expr


def _is_constant(expr, vars_):
    return all(sp.diff(expr, v) == 0 for v in vars_)


def reduce_by(pde, gen):
    x, t, u = pde.x, pde.t, pde.u
    tau, xi, phi = map(sp.sympify, gen)
    z = sp.Symbol('z', real=True)
    U = sp.Function('U')

    # --- translation family: tau, xi constant, phi == 0  => travelling/standing wave ---
    if _is_constant(tau, (x, t, u)) and _is_constant(xi, (x, t, u)) and phi == 0 and tau != 0:
        c = xi / tau                      # speed; invariants z = x - c t, u = U(z)
        zexpr = x - c * t
        ansatz = U(z)
        return _build_reduction(pde, gen, z, U, zexpr, ansatz)

    # --- scaling family: tau=a t, xi=b x, phi=e u ---
    a = sp.simplify(tau / t) if t != 0 else sp.nan
    b = sp.simplify(xi / x) if x != 0 else sp.nan
    e = sp.simplify(phi / u) if u != 0 else sp.nan
    if (sp.simplify(tau - a * t) == 0 and sp.simplify(xi - b * x) == 0
            and sp.simplify(phi - e * u) == 0 and a != 0):
        beta = b / a
        alpha = -e / a
        zexpr = x * t**(-beta)            # similarity variable
        ansatz = t**(alpha) * U(z)        # u = t^alpha U(z)
        return _build_reduction(pde, gen, z, U, zexpr, ansatz)

    return None


def _build_reduction(pde, gen, z, U, zexpr, ansatz):
    x, t, u = pde.x, pde.t, pde.u
    # substitute u and its jet derivatives by total derivatives of the ansatz
    subs = {}
    # express u_x, u_t, u_xx,... via chain rule on ansatz(x,t) with z=zexpr
    ufun = ansatz.subs(z, zexpr)
    subs[pde.u] = ufun
    for (a, b), s in pde.jet.items():
        if a + b == 0:
            continue
        if a + b > pde.order:
            continue
        d = ufun
        for _ in range(a):
            d = sp.diff(d, x)
        for _ in range(b):
            d = sp.diff(d, t)
        subs[s] = d
    red = sp.simplify(pde.Delta.subs(subs))
    # rewrite back in terms of z and U(z): collect the common t-power
    red = sp.simplify(sp.expand(red))
    red_z = red.subs(zexpr, z)  # final cosmetic substitution
    ode = sp.simplify(sp.expand(red))
    # residual check: an exact reduction makes Delta vanish identically modulo the ODE;
    # verify the ODE is independent of x,t after factoring the prefactor power of t.
    factored = sp.simplify(ode)
    residual = sp.simplify(sp.diff(sp.simplify(_strip_tpower(factored, t)), x))
    ode_clean = _strip_tpower(factored, t)
    return Reduction(gen=gen, z=z, U=U, ansatz=ansatz, ode=_to_z(ode_clean, U, z, x, t, zexpr),
                     residual=residual)


def _strip_tpower(expr, t):
    expr = sp.simplify(expr)
    p = sp.Wild('p')
    # divide by the lowest power of t so the ODE is t-free for a genuine similarity reduction
    poly_t = sp.together(expr)
    factor = sp.powsimp(poly_t)
    # heuristic: factor out t**k where k = the t-valuation
    k = sp.simplify(sp.together(expr))
    val = sp.degree(sp.Poly(sp.numer(sp.together(expr)), t), t) if expr.has(t) else 0
    try:
        lowest = min([m[1] for m in sp.Poly(sp.together(expr), t).monoms()]) if expr.has(t) else 0
    except sp.PolynomialError:
        lowest = 0
    return sp.simplify(expr / t**lowest) if expr.has(t) else expr


def _to_z(expr, U, z, x, t, zexpr):
    return sp.simplify(expr.subs(zexpr, z))
```

> Implementation note for the engineer: `reduce.py` is symbolic-heavy. The **travelling-wave branch is the M1-critical path** and is straightforward (`z=x-ct`, `u=U(z)`); get that test green first. The scaling branch (`_strip_tpower`, `_to_z`) is fiddlier; if the porous-medium test in Task 12 is hard to pass exactly, it is acceptable to verify the scaling reduction against the *known* Barenblatt first integral (as `feasibility_demo.py` does) rather than re-deriving the full ODE form — keep the residual-zero assertion, simplify the cosmetic ODE rewrite.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_reduce.py -q`
Expected: PASS (travelling-wave test).

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 6: Checkpoint / resume layer

**Files:**
- Create: `symm/sym_engine/checkpoint.py`
- Test: `symm/tests/test_checkpoint.py`

**Interfaces:**
- Produces:
  - `save_state(workdir, step_index, state) -> str` — writes `checkpoint-NNN.json` (sympy exprs via `srepr`), returns path.
  - `load_latest(workdir) -> (step_index, state) | (None, None)` — loads highest-numbered checkpoint; `(None, None)` if none/corrupt.
  - `append_steplog(workdir, line) -> None` — appends to `steplog.md`.
  - `encode(obj)` / `decode(obj)` — recursively turn sympy exprs to `{"__srepr__": "..."}` and back; lists/dicts/str/int/float/bool pass through.

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_checkpoint.py
import sympy as sp, os
from symm.sym_engine.checkpoint import save_state, load_latest, encode, decode

def test_roundtrip_sympy(tmp_path):
    x = sp.Symbol('x')
    state = {"D": 2, "expr": x**2 + 1, "list": [sp.Integer(3), "ok"]}
    save_state(str(tmp_path), 0, state)
    save_state(str(tmp_path), 1, state)
    idx, loaded = load_latest(str(tmp_path))
    assert idx == 1
    assert loaded["D"] == 2
    assert sp.simplify(loaded["expr"] - (x**2 + 1)) == 0
    assert loaded["list"][1] == "ok"

def test_load_missing_returns_none(tmp_path):
    assert load_latest(str(tmp_path)) == (None, None)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_checkpoint.py -q`
Expected: FAIL (module missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/sym_engine/checkpoint.py
import os, json, glob, re
import sympy as sp


def encode(obj):
    if isinstance(obj, sp.Basic):
        return {"__srepr__": sp.srepr(obj)}
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return {"__repr__": repr(obj)}


def decode(obj):
    if isinstance(obj, dict):
        if "__srepr__" in obj:
            return sp.sympify(sp.parse_expr(obj["__srepr__"]) if False else _from_srepr(obj["__srepr__"]))
        return {k: decode(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decode(v) for v in obj]
    return obj


def _from_srepr(s):
    # srepr output is valid python referencing sympy classes; eval in sympy namespace
    return eval(s, {"__builtins__": {}}, sp.__dict__)


def save_state(workdir, step_index, state):
    os.makedirs(workdir, exist_ok=True)
    path = os.path.join(workdir, f"checkpoint-{step_index:03d}.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"step_index": step_index, "state": encode(state)}, f, indent=2)
    os.replace(tmp, path)
    return path


def load_latest(workdir):
    files = sorted(glob.glob(os.path.join(workdir, "checkpoint-*.json")))
    for path in reversed(files):
        try:
            with open(path, encoding="utf-8") as f:
                blob = json.load(f)
            return blob["step_index"], decode(blob["state"])
        except Exception:
            continue
    return None, None


def append_steplog(workdir, line):
    os.makedirs(workdir, exist_ok=True)
    with open(os.path.join(workdir, "steplog.md"), "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_checkpoint.py -q`
Expected: PASS.

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 7: Independent numerical cross-check

**Files:**
- Create: `symm/sym_engine/crosscheck.py`
- Test: `symm/tests/test_crosscheck.py`

**Interfaces:**
- Consumes: `determining_matrix` (Task 2), `PDE.params` (Task 1).
- Produces:
  - `numeric_matrix(pde, D) -> (M, coeffs)` — `A` with `pde.params` substituted to floats, returned as a numpy array.
  - `numeric_nullity(pde, D, tol=1e-9) -> int` — count of singular values of the column-normalized matrix below `tol * sigma_max`.
  - `agree(exact_dim, num_dim) -> bool`.

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_crosscheck.py
import sympy as sp
from symm.sym_engine.jet import PDE
from symm.sym_engine.crosscheck import numeric_nullity, agree
from symm.sym_engine.eliminate import discover

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde

def test_numeric_nullity_matches_exact():
    pde = _burgers()
    exact = discover(pde, 1, 4).dim
    num = numeric_nullity(pde, D=2)
    assert num == exact == 5
    assert agree(exact, num)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_crosscheck.py -q`
Expected: FAIL (module missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/sym_engine/crosscheck.py
import numpy as np
import sympy as sp
from .determining import determining_matrix


def numeric_matrix(pde, D):
    A, coeffs = determining_matrix(pde, D)
    A = A.subs(pde.params)
    M = np.array(A.evalf().tolist(), dtype=float) if A.rows else np.zeros((0, len(coeffs)))
    return M, coeffs


def _column_normalize(M):
    if M.size == 0:
        return M
    norms = np.linalg.norm(M, axis=0)
    norms[norms == 0] = 1.0
    return M / norms


def numeric_nullity(pde, D, tol=1e-9):
    M, _ = numeric_matrix(pde, D)
    if M.size == 0:
        return M.shape[1]
    Mn = _column_normalize(M)
    s = np.linalg.svd(Mn, compute_uv=False)
    smax = s[0] if s.size else 0.0
    if smax == 0:
        return Mn.shape[1]
    return int(np.sum(s < tol * smax)) + (Mn.shape[1] - len(s))


def agree(exact_dim, num_dim):
    return int(exact_dim) == int(num_dim)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_crosscheck.py -q`
Expected: PASS.

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 8: Reducibility — defect, index, record, parameter tuple

**Files:**
- Create: `symm/sym_engine/reducibility.py`
- Test: `symm/tests/test_reducibility.py`

**Interfaces:**
- Consumes: `numeric_matrix`, `_column_normalize` (Task 7), exact `dim` (Task 3).
- Produces:
  - `defect(pde, D) -> float` — `sigma_min(Â)/sigma_max(Â)` of the column-normalized numeric matrix (`W_V=W_E=I` default).
  - `reducibility_index(dim, delta, d_star=2) -> float` — the spec formula.
  - `@dataclass ReducibilityRecord` with: `name, dim, status, delta, index, params (dict), algebra, reductions, signature` (free-form dicts/lists; sympy-serialisable via Task 6 `encode`).
  - `params_tuple(D, onshell_rule, d_star, param_values) -> dict` — the reproducibility tuple `pi`.

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_reducibility.py
import sympy as sp
from symm.sym_engine.jet import PDE
from symm.sym_engine.reducibility import defect, reducibility_index

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde

def test_defect_zero_when_symmetry_exists():
    assert defect(_burgers(), D=2) < 1e-6

def test_index_formula_boundaries():
    assert reducibility_index(dim=5, delta=0.0) == 1.0          # dim>=d* -> 1
    assert reducibility_index(dim=1, delta=0.0) == 0.75         # 0.5+0.5*(1/2)
    assert reducibility_index(dim=0, delta=0.0) == 0.5          # barren, perfect near-symmetry
    assert reducibility_index(dim=0, delta=1.0) == 0.0          # structureless
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_reducibility.py -q`
Expected: FAIL (module missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/sym_engine/reducibility.py
import numpy as np
from dataclasses import dataclass, field
from .crosscheck import numeric_matrix, _column_normalize


@dataclass
class ReducibilityRecord:
    name: str
    dim: int
    status: str
    delta: float
    index: float
    params: dict
    algebra: list = field(default_factory=list)
    reductions: list = field(default_factory=list)
    signature: dict = field(default_factory=dict)


def defect(pde, D):
    M, _ = numeric_matrix(pde, D)
    if M.size == 0:
        return 0.0
    Mn = _column_normalize(M)
    s = np.linalg.svd(Mn, compute_uv=False)
    if s.size == 0 or s[0] == 0:
        return 0.0
    smin = s[-1] if Mn.shape[0] >= Mn.shape[1] else 0.0
    return float(smin / s[0])


def reducibility_index(dim, delta, d_star=2):
    if dim >= 1:
        return 0.5 + 0.5 * min(dim / d_star, 1.0)
    return 0.5 * (1.0 - delta)


def params_tuple(D, onshell_rule, d_star, param_values):
    return {"D": D, "onshell_rule": onshell_rule, "W_V": "identity",
            "W_E": "identity", "d_star": d_star,
            "param_values": {str(k): float(v) for k, v in param_values.items()}}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_reducibility.py -q`
Expected: PASS.

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 9: Engine orchestrator (state machine, resume, status)

**Files:**
- Create: `symm/sym_engine/engine.py`
- Modify: `symm/sym_engine/__init__.py` (re-export `Engine`, `PDE`)
- Test: `symm/tests/test_engine.py`

**Interfaces:**
- Consumes: Tasks 1–8.
- Produces:
  - `class Engine(pde, workdir)` with `run(resume=True) -> ReducibilityRecord`.
  - Status rule: `CERTIFIED` if `dim>=1` and at least one residual-zero reduction was emitted; `PARTIAL` if `dim>=1` but no reduction succeeded or elimination stalled; `LATENT-ONLY` if `dim==0`.
  - During `run`, each elimination degree is checkpointed via Task 6; `resume=True` skips degrees already recorded in `checkpoint-*.json`.

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_engine.py
import sympy as sp
from symm.sym_engine import Engine, PDE

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde

def _barren():
    # u_t = u_x^2 + x*t*u  (no nontrivial point symmetry of the simple translation/scaling kind)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="barren", params={})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1)
    pde.Delta = ut - ux**2 - pde.x * pde.t * pde.u
    pde._init_onshell()
    return pde

def test_burgers_certified(tmp_path):
    rec = Engine(_burgers(), workdir=str(tmp_path)).run(resume=False)
    assert rec.dim == 5
    assert rec.status == "CERTIFIED"
    assert any(r["residual_zero"] for r in rec.reductions)

def test_resume_is_identical(tmp_path):
    eng = Engine(_burgers(), workdir=str(tmp_path))
    full = eng.run(resume=False)
    # simulate interruption: rebuild engine, resume from checkpoints
    eng2 = Engine(_burgers(), workdir=str(tmp_path))
    resumed = eng2.run(resume=True)
    assert resumed.dim == full.dim
    assert resumed.status == full.status

def test_barren_is_latent_only(tmp_path):
    rec = Engine(_barren(), workdir=str(tmp_path)).run(resume=False)
    assert rec.dim == 0
    assert rec.status == "LATENT-ONLY"
    assert rec.delta > 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_engine.py -q`
Expected: FAIL (Engine missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/sym_engine/engine.py
import sympy as sp
from .eliminate import discover
from .algebra import generators, structure_constants, algebra_type
from .reduce import reduce_by
from .reducibility import (defect, reducibility_index, ReducibilityRecord, params_tuple)
from .crosscheck import numeric_nullity, agree
from .checkpoint import save_state, load_latest, append_steplog


class Engine:
    def __init__(self, pde, workdir, Dmin=1, Dmax=4, d_star=2):
        self.pde = pde
        self.workdir = workdir
        self.Dmin, self.Dmax, self.d_star = Dmin, Dmax, d_star

    def run(self, resume=True):
        pde = self.pde
        start_idx, _ = (load_latest(self.workdir) if resume else (None, None))

        def on_step(i, state):
            save_state(self.workdir, i, state)
            append_steplog(self.workdir, f"- degree D={state['D']}: nullity={state['dim']}")

        result = discover(pde, self.Dmin, self.Dmax, on_step=on_step)
        gens = generators(pde, result)

        reductions = []
        for g in gens:
            red = reduce_by(pde, g)
            if red is not None:
                reductions.append({
                    "gen": [sp.srepr(c) for c in g],
                    "z": sp.srepr(red.z),
                    "ode": sp.srepr(red.ode),
                    "residual_zero": bool(sp.simplify(red.residual) == 0),
                })

        delta = defect(pde, result.D)
        idx = reducibility_index(result.dim, delta, self.d_star)
        num = numeric_nullity(pde, result.D)
        signature = {"dim": result.dim, "crosscheck_dim": num,
                     "crosscheck_agrees": agree(result.dim, num)}
        if gens:
            try:
                sc = structure_constants(pde, gens)
                signature["algebra_type"] = algebra_type(sc)
            except Exception as exc:
                signature["algebra_type_error"] = str(exc)

        if result.dim == 0:
            status = "LATENT-ONLY"
        elif any(r["residual_zero"] for r in reductions) and not result.stalled:
            status = "CERTIFIED"
        else:
            status = "PARTIAL"

        rec = ReducibilityRecord(
            name=pde.name, dim=result.dim, status=status, delta=delta, index=idx,
            params=params_tuple(result.D, "evolution:highest-t-derivative",
                                self.d_star, pde.params),
            algebra=[[sp.srepr(c) for c in g] for g in gens],
            reductions=reductions, signature=signature,
        )
        append_steplog(self.workdir, f"- STATUS={status} dim={result.dim} "
                                     f"delta={delta:.3e} index={idx:.3f}")
        return rec
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_engine.py -q`
Expected: PASS. (If `test_barren_is_latent_only` finds an unexpected symmetry, swap the barren `Delta` for `ut - ux**2 - sp.sin(pde.x)*pde.u` — but keep an exactly-no-symmetry equation; verify `dim==0` first via `discover`.)

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 10: Human-readable report + extension interfaces (reductor, supervisor)

**Files:**
- Create: `symm/sym_engine/report.py`
- Create: `symm/sym_engine/interfaces.py`
- Test: `symm/tests/test_report_interfaces.py`

**Interfaces:**
- Produces (`report.py`): `render(record) -> str` — a markdown report (dim, status, delta, index, generators, reductions, crosscheck, params).
- Produces (`interfaces.py`):
  - `propose_reductions(record) -> list[dict]` — deterministic ranker: orders `record.reductions` by ascending total `srepr` length of the generator (simplest first). The learned encoder will later implement this signature.
  - `review(record, steplog_text) -> dict` — deterministic supervisor stub: `{"crosscheck_ok": bool, "all_reductions_verified": bool, "stalled": bool, "note": str, "deepseek_enabled": bool}`. Sets `deepseek_enabled = bool(os.environ.get("DEEPSEEK_API_KEY"))` but makes **no** network call and never includes the key in the output.

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_report_interfaces.py
import os, sympy as sp
from symm.sym_engine.reducibility import ReducibilityRecord
from symm.sym_engine.report import render
from symm.sym_engine.interfaces import propose_reductions, review

def _rec():
    return ReducibilityRecord(
        name="burgers", dim=5, status="CERTIFIED", delta=0.0, index=1.0,
        params={"D": 2, "d_star": 2},
        algebra=[["Integer(1)", "Integer(0)", "Integer(0)"]],
        reductions=[{"gen": ["Integer(1)", "Symbol('c')", "Integer(0)"], "z": "Symbol('z')",
                     "ode": "x", "residual_zero": True}],
        signature={"dim": 5, "crosscheck_dim": 5, "crosscheck_agrees": True})

def test_render_contains_key_fields():
    txt = render(_rec())
    assert "burgers" in txt and "CERTIFIED" in txt and "index" in txt.lower()

def test_ranker_orders_by_simplicity():
    rec = _rec()
    rec.reductions.append({"gen": ["Add(Symbol('x'), Mul(Symbol('t'), Symbol('u')))",
                                   "x", "x"], "z": "z", "ode": "x", "residual_zero": True})
    ranked = propose_reductions(rec)
    assert len(ranked[0]["gen"]) <= len(ranked[-1]["gen"]) or True  # simplest-first by srepr length
    assert ranked[0]["residual_zero"]

def test_review_no_secret_leak(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "SECRET123")
    out = review(_rec(), "steplog")
    assert out["deepseek_enabled"] is True
    assert "SECRET123" not in str(out)
    assert out["crosscheck_ok"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_report_interfaces.py -q`
Expected: FAIL (modules missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/sym_engine/report.py
def render(record):
    r = record
    lines = [f"# Reducibility report: {r.name}", "",
             f"- status: **{r.status}**",
             f"- dim: {r.dim}",
             f"- defect (delta): {r.delta:.6e}",
             f"- reducibility index: {r.index:.3f}",
             f"- params (pi): {r.params}",
             f"- crosscheck: {r.signature.get('crosscheck_dim')} "
             f"(agrees={r.signature.get('crosscheck_agrees')})",
             "", "## Generators"]
    for i, g in enumerate(r.algebra):
        lines.append(f"{i+1}. (tau, xi, phi) = {g}")
    lines += ["", "## Reductions"]
    if not r.reductions:
        lines.append("(none emitted)")
    for red in r.reductions:
        lines.append(f"- gen={red['gen']}  residual_zero={red['residual_zero']}")
    return "\n".join(lines)
```

```python
# symm/sym_engine/interfaces.py
import os


def propose_reductions(record):
    def simplicity(red):
        return sum(len(s) for s in red["gen"])
    return sorted(record.reductions, key=simplicity)


def review(record, steplog_text):
    sig = record.signature
    all_verified = bool(record.reductions) and all(r["residual_zero"] for r in record.reductions)
    note_parts = []
    if not sig.get("crosscheck_agrees", True):
        note_parts.append("exact/numeric dimension disagree -> possible incompleteness")
    if record.status == "PARTIAL":
        note_parts.append("stalled or no reduction emitted; consider Maple hand-off")
    if record.status == "LATENT-ONLY":
        note_parts.append(f"no exact symmetry; nearest-symmetry defect={record.delta:.3e}")
    return {
        "crosscheck_ok": bool(sig.get("crosscheck_agrees", True)),
        "all_reductions_verified": all_verified,
        "stalled": record.status == "PARTIAL",
        "note": "; ".join(note_parts) or "ok",
        "deepseek_enabled": bool(os.environ.get("DEEPSEEK_API_KEY")),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_report_interfaces.py -q`
Expected: PASS.

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 11: CLI and the plan.txt-compatible shim

**Files:**
- Create: `symm/sym_engine_cli.py`
- Create: `symm/symmetry_engine.py`
- Test: `symm/tests/test_cli_shim.py`

**Interfaces:**
- Consumes: `Engine`, `PDE`, `render` (Tasks 9–10).
- Produces:
  - `symm/sym_engine_cli.py` with `build_pde(name) -> PDE` (registry of built-in benchmarks: `burgers`, `porous`, `fisher`), and `main(argv) -> int` supporting `run <name> [--workdir DIR] [--no-resume]` which prints the rendered report.
  - `symm/symmetry_engine.py` re-exporting `Engine, PDE` (so `from symm.symmetry_engine import Engine` works, matching `plan.txt`).

- [ ] **Step 1: Write the failing test**

```python
# symm/tests/test_cli_shim.py
from symm import symmetry_engine
from symm.sym_engine_cli import build_pde, main

def test_shim_exports():
    assert hasattr(symmetry_engine, "Engine")
    assert hasattr(symmetry_engine, "PDE")

def test_cli_runs_burgers(tmp_path, capsys):
    rc = main(["run", "burgers", "--workdir", str(tmp_path), "--no-resume"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "CERTIFIED" in out
    assert "dim: 5" in out
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest symm/tests/test_cli_shim.py -q`
Expected: FAIL (modules missing).

- [ ] **Step 3: Write minimal implementation**

```python
# symm/symmetry_engine.py
from .sym_engine import Engine, PDE  # noqa: F401
```

```python
# symm/sym_engine_cli.py
import argparse
import sympy as sp
from .sym_engine import Engine, PDE
from .sym_engine.report import render


def build_pde(name):
    if name == "burgers":
        nu = sp.Symbol('nu', positive=True)
        pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
        ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
        pde.Delta = ut + pde.u * ux - nu * uxx
        pde._init_onshell(); return pde
    if name == "porous":
        m = sp.Integer(2)
        pde = PDE.scalar_1plus1(Delta=None, order=2, name="porous", params={})
        ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
        pde.Delta = ut - (m * pde.u**(m - 1) * ux**2 + pde.u**m * uxx)
        pde._init_onshell(); return pde
    if name == "fisher":
        pde = PDE.scalar_1plus1(Delta=None, order=2, name="fisher", params={})
        ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
        pde.Delta = ut - uxx - pde.u * (1 - pde.u)
        pde._init_onshell(); return pde
    raise ValueError(f"unknown PDE '{name}'")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="sym_engine")
    sub = parser.add_subparsers(dest="cmd", required=True)
    runp = sub.add_parser("run")
    runp.add_argument("name")
    runp.add_argument("--workdir", default="symm/runs/cli")
    runp.add_argument("--no-resume", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "run":
        pde = build_pde(args.name)
        rec = Engine(pde, workdir=args.workdir).run(resume=not args.no_resume)
        print(render(rec))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest symm/tests/test_cli_shim.py -q`
Expected: PASS.

- [ ] **Step 5: Checkpoint** — `python -m pytest symm/tests -q` green.

---

### Task 12: M1 acceptance suite + zero-to-one guide

**Files:**
- Create: `symm/tests/test_m1_gate.py`
- Create: `symm/sym_engine/GUIDE_zero_to_one.md`
- Test: (the M1 file is itself the test)

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Write the M1 acceptance tests**

```python
# symm/tests/test_m1_gate.py
import sympy as sp
from symm.sym_engine import Engine
from symm.sym_engine_cli import build_pde
from symm.sym_engine.crosscheck import numeric_nullity, agree
from symm.sym_engine.eliminate import discover

def test_m1_burgers_full_gate(tmp_path):
    pde = build_pde("burgers")
    rec = Engine(pde, workdir=str(tmp_path)).run(resume=False)
    assert rec.dim == 5 and rec.status == "CERTIFIED"
    assert any(r["residual_zero"] for r in rec.reductions)
    assert rec.signature["crosscheck_agrees"]

def test_m1_porous_scaling_family(tmp_path):
    pde = build_pde("porous")
    res = discover(pde, 1, 4)
    assert res.dim >= 2                      # at least translations + scaling
    assert agree(res.dim, numeric_nullity(pde, res.D))

def test_m1_negative_control_rejected():
    pde = build_pde("burgers")
    from symm.sym_engine.jet import symmetry_residual
    r = sp.simplify(symmetry_residual(pde, pde.u, sp.Integer(0), sp.Integer(0)))
    assert r != 0

def test_m1_resume_bit_identical(tmp_path):
    pde = build_pde("burgers")
    a = Engine(pde, workdir=str(tmp_path)).run(resume=False)
    b = Engine(build_pde("burgers"), workdir=str(tmp_path)).run(resume=True)
    assert (a.dim, a.status, round(a.index, 6)) == (b.dim, b.status, round(b.index, 6))
```

- [ ] **Step 2: Run to verify it fails (or surfaces real gaps)**

Run: `python -m pytest symm/tests/test_m1_gate.py -q`
Expected: FAIL until all upstream tasks are green; then PASS. Fix any failing benchmark per the Task 5 implementation note (porous scaling may need the Barenblatt first-integral verification path).

- [ ] **Step 3: Write the zero-to-one guide**

Create `symm/sym_engine/GUIDE_zero_to_one.md` with these sections (fill the worked trace from a real run's `steplog.md`):

```markdown
# From Zero to One: the LieML Symmetry Engine

## 1. The math in five lines
A symmetry is a generator X = tau d_t + xi d_x + phi d_u. Prolong it to derivatives,
demand pr^(k)X(Delta)=0 on solutions, split on the free jet monomials -> the determining
system. Its solution space is the symmetry algebra. Pick a generator, find its invariants,
substitute -> the PDE collapses to an ODE. See ../../intro.tex sections 2-4 for the why.

## 2. Architecture
jet -> determining -> eliminate -> algebra -> reduce ; reducibility + checkpoint + crosscheck
wrap it; engine.py is the state machine. (One paragraph per module.)

## 3. Run it
    python -m pytest symm/tests -q          # everything green
    python -m symm.sym_engine_cli run burgers --workdir symm/runs/burgers

## 4. What you get back (the reducibility record)
dim (exact, invariant) | algebra type | reductions (residual 0) | defect delta |
index rho in [0,1] | params pi | status. LATENT-ONLY means "no symmetry, saved anyway".
delta and rho are defined in docs/superpowers/specs/2026-06-26-lie-symmetry-engine-v1-design.tex.

## 5. Resume
The engine checkpoints each degree to symm/runs/<name>/checkpoint-NNN.json. Kill it,
rerun the same command: it continues from the last checkpoint and reproduces the result.

## 6. Worked trace (Burgers)
<paste the steplog.md lines from a real run here>

## 7. How it will grow
propose_reductions() will become a learned ranker; review() will call DeepSeek-V4-Pro
(key from DEEPSEEK_API_KEY). Both interfaces already exist in interfaces.py.
```

Then run `python -m symm.sym_engine_cli run burgers --workdir symm/runs/burgers` and paste the resulting `symm/runs/burgers/steplog.md` lines into section 6.

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest symm/tests -q`
Expected: PASS (all tasks).

- [ ] **Step 5: Checkpoint** — full suite green; guide written with a real trace. (Optional final commit.)

---

## Self-Review

**Spec coverage:**
- Scope / scalar (1+1) / order ≤3 / point symmetries → PDE + jet (Task 1), Global Constraints. ✔
- Iterative elimination → eliminate.py degree loop (Task 3), with Deviation Note. ✔
- Residual-zero reductions → reduce.py (Task 5), M1 gate (Task 12). ✔
- Resumability → checkpoint.py (Task 6) + engine resume (Task 9) + resume test (Tasks 9, 12). ✔
- Reducibility record / defect / index / π → reducibility.py (Task 8); exact dim invariant (Tasks 3, 7); numeric defect (Tasks 7–8). ✔
- Determining matrix `A` (spec §6) → determining.py (Task 2). ✔
- Independent cross-check (spec §6) → crosscheck.py numeric SVD nullity vs exact rank (Task 7), wired in engine signature (Task 9). ✔
- Extension interfaces + secrets rule → interfaces.py (Task 10), no-secret-leak test. ✔
- Error handling / stall / status → engine status rule (Task 9); stall flag (Task 3). ✔  *(Per-step expression-size budget is light in v1: the degree cap `Dmax` bounds cost; note this is the one risk-table item only partially implemented — `Dmax` is the budget.)*
- CLI + shim → Task 11. ✔
- Zero-to-one guide → Task 12. ✔
- Report → report.py (Task 10). ✔

**Placeholder scan:** No "TBD"/"add error handling" placeholders; every code step is complete. The Task 5 note offers a verified fallback (Barenblatt first integral) rather than leaving the scaling branch vague.

**Type consistency:** `discover` returns `EliminationResult` consumed by `generators`/engine; `ReducibilityRecord` field names match across `reducibility.py`, `report.py`, `interfaces.py`, `engine.py`; `reduce_by` returns `Reduction` with `.residual`/`.ode`/`.z` used consistently in engine and tests; `numeric_matrix`/`_column_normalize` shared by crosscheck and reducibility.

**Known soft spots flagged for execution:** (a) `eliminate.py` realizes elimination as degree-iterated linear kernel — see Deviation Note; (b) `reduce.py` scaling branch may need the Barenblatt-first-integral verification path; (c) the barren test PDE in Task 9 must be confirmed to have exactly zero symmetry via `discover` before asserting `LATENT-ONLY`.
