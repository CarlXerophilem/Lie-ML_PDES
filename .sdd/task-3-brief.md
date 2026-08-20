# Task 3 brief — Iterative (degree-increasing) elimination → algebra discovery

This is your requirements. Use the exact code, signatures, and test cases below verbatim.
Tasks 1 and 2 are complete (do NOT modify `jet.py` or `determining.py`). Work strictly TEST-FIRST.

## Global Constraints (bind every task)

- **No new dependencies** beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- **Determinism:** no randomness anywhere; stable ordering.
- **Exactness:** dimension uses exact `sympy` rational/symbolic linear algebra (`A.rank()`), no float tolerance.
- **Scope:** scalar PDEs in `(x,t,u)`, order `k<=3`, Lie point symmetries.
- **Not a git repo.** No commits. Final step = run the task's tests green.
- **Run tests from project root** `D:\MATHs\math 4890 LieML` with `python -m pytest symm/tests -q`.

## Interfaces you CONSUME (already implemented)
From `symm/sym_engine/determining.py`: `determining_matrix(pde, D) -> (A, coeffs)` (A is a `sympy.Matrix`,
`coeffs` a `list[Symbol]`), and `ansatz(pde, D)`.

## Interfaces you PRODUCE (later tasks rely on these EXACT names/types)
In a NEW file `symm/sym_engine/eliminate.py`:
- `@dataclass EliminationResult` with fields: `dim:int`, `D:int`, `basis:list`, `coeffs:list`,
  `log:list` (default empty), `stalled:bool` (default False). `basis` is a `list[dict]` mapping each
  coefficient Symbol to its (rational) null-space value.
- `discover(pde, Dmin=1, Dmax=4, on_step=None) -> EliminationResult`. Increases ansatz degree D until
  the nullity stabilizes (dim unchanged between consecutive degrees) and reports the stabilizing degree.
  `on_step(step_index:int, state:dict)` is called once per degree with `state` keys `D, dim, coeffs, basis`.

## Files
- Create: `symm/sym_engine/eliminate.py`
- Test: `symm/tests/test_eliminate.py`

## Step 1 — write the failing test (`symm/tests/test_eliminate.py`)

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

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_eliminate.py -q` → FAIL (module missing).

## Step 3 — minimal implementation (`symm/sym_engine/eliminate.py`)

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

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_eliminate.py -q` → PASS.

KNOWN FRAGILITY (handle only if a test actually fails): for Burgers the null-space vectors are
parameter-free rationals, so `sp.nsimplify` is a no-op. If `sp.nsimplify(v[i])` raises or misbehaves
on some entry, replace that single call with `sp.simplify(v[i])` (keep the `{coeff: value}` map shape).
Do NOT change the expected test values. If `A.rank()`/`A.nullspace()` at D=3 is slow, that is
acceptable (it must still finish); do not add tolerances. Report exactly what (if anything) you changed.

## Step 5 — final check
Run `python -m pytest symm/tests -q` and confirm ALL tests green (Tasks 1, 2 must still pass).

## Report contract
Write your full report to `D:\MATHs\math 4890 LieML\.sdd\task-3-report.md` (files created, exact
pytest commands + full output, any deviations, concerns). Then return ONLY: status (DONE /
DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT), files created, one-line test summary, and concerns.
Do not paste full code/output into the returned message.
