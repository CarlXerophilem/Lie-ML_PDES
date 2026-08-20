# Task 4 brief — Generators, dimension, structure constants, algebra type

This is your requirements. Use the exact code, signatures, and test cases below verbatim.
Tasks 1-3 are complete (do NOT modify `jet.py`, `determining.py`, `eliminate.py`). Work TEST-FIRST.

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- Determinism: no randomness; stable ordering.
- Exactness: all algebra over exact sympy rationals; no float tolerance.
- Scope: scalar PDEs `(x,t,u)`, order `k<=3`, point symmetries.
- Not a git repo. Final step = tests green. Run from project root `D:\MATHs\math 4890 LieML`.

## Interfaces you CONSUME (already implemented)
- `symm/sym_engine/eliminate.py`: `discover(pde, Dmin, Dmax) -> EliminationResult` with `.D`, `.dim`,
  `.basis` (list of dict coeff-Symbol -> rational value), `.coeffs`.
- `symm/sym_engine/determining.py`: `ansatz(pde, D) -> (tau, xi, phi, coeffs)`.
- `symm/sym_engine/jet.py`: `PDE` with `.x, .t, .u`.

## Interfaces you PRODUCE (later tasks rely on these EXACT names)
In a NEW file `symm/sym_engine/algebra.py`:
- `generators(pde, result) -> list[tuple(tau, xi, phi)]`
- `bracket(pde, g1, g2) -> tuple(tau, xi, phi)`  (Lie bracket of two generators as vector fields)
- `structure_constants(pde, gens) -> sympy.Array`  (`C[k,i,j]`: `[e_i,e_j] = sum_k C[k,i,j] e_k`)
- `algebra_type(struct) -> dict` with keys `dim, abelian, nilpotent, solvable, derived_dims`.

## Files
- Create: `symm/sym_engine/algebra.py`
- Test: `symm/tests/test_algebra.py`

## Step 1 — write the failing test (`symm/tests/test_algebra.py`)

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
    # the Burgers point algebra contains an sl(2,R) subalgebra, hence is NON-solvable
    assert info["solvable"] is False
```

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_algebra.py -q` → FAIL (module missing).

## Step 3 — minimal implementation (`symm/sym_engine/algebra.py`)

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
    var = (pde.t, pde.x, pde.u)   # ordering matches generator tuple (tau, xi, phi)

    def apply(comps, f):
        return sum(comps[i] * sp.diff(f, var[i]) for i in range(3))

    return tuple(sp.expand(apply(g1, g2[i]) - apply(g2, g1[i])) for i in range(3))


def _coordinate_vector(pde, g, basis):
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


def _bracket_coords(C, n, a, b):
    out = []
    for k in range(n):
        s = sp.Integer(0)
        for i in range(n):
            for j in range(n):
                s += a[i] * b[j] * C[k, i, j]
        out.append(sp.expand(s))
    return out


def _span_basis(vectors, n):
    if not vectors:
        return []
    M = sp.Matrix.hstack(*[sp.Matrix(n, 1, list(v)) for v in vectors])
    return [list(col) for col in M.columnspace()]


def _series_dims(C, n, lower_central):
    full = [[sp.Integer(1) if i == j else sp.Integer(0) for i in range(n)] for j in range(n)]
    current = full
    dims = [n]
    while True:
        left = full if lower_central else current
        brackets = [_bracket_coords(C, n, a, b) for a in left for b in current]
        nb = _span_basis(brackets, n)
        d = len(nb)
        if d == 0:
            dims.append(0)
            break
        if d == dims[-1]:
            dims.append(d)
            break
        dims.append(d)
        current = nb
    return dims


def algebra_type(struct):
    C = struct
    n = C.shape[0]
    abelian = all(C[k, i, j] == 0 for k in range(n) for i in range(n) for j in range(n))
    derived = _series_dims(C, n, lower_central=False)
    lower = _series_dims(C, n, lower_central=True)
    return {"dim": n, "abelian": abelian, "nilpotent": lower[-1] == 0,
            "solvable": derived[-1] == 0, "derived_dims": derived}
```

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_algebra.py -q` → PASS. The `solvable is False` assertion is the real
correctness gate for the derived-series computation. Do NOT change expected test values. If
`structure_constants` raises "algebra not closed in basis", the generators are inconsistent — STOP and
report BLOCKED (it means an upstream issue), do not work around it.

## Step 5 — final check
`python -m pytest symm/tests -q` — ALL tests (Tasks 1-4) green.

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-4-report.md`. Return ONLY: status, files
created, one-line test summary, concerns.
