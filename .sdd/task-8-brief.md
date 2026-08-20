# Task 8 brief — Reducibility: defect, index, record, parameter tuple

Tasks 1-7 complete (do NOT modify them). Work TEST-FIRST. This module turns the determining matrix
into the headline diagnostic: an exact-backed dimension plus a metric `defect` and `reducibility_index`.

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- Determinism: no randomness.
- The defect is `sigma_min(A_hat) / sigma_max(A_hat)` with `W_V = W_E = I` (column-normalized matrix).
- Not a git repo. Final step = tests green. Run from project root `D:\MATHs\math 4890 LieML`.

## Interfaces you CONSUME
- `symm/sym_engine/crosscheck.py`: `numeric_matrix(pde, D)`, `_column_normalize(M)`.

## Interfaces you PRODUCE (later tasks rely on these EXACT names)
In a NEW file `symm/sym_engine/reducibility.py`:
- `defect(pde, D) -> float`
- `reducibility_index(dim, delta, d_star=2) -> float`
- `@dataclass ReducibilityRecord` with fields `name, dim, status, delta, index, params, algebra, reductions, signature`.
- `params_tuple(D, onshell_rule, d_star, param_values) -> dict`.

## Files
- Create: `symm/sym_engine/reducibility.py`
- Test: `symm/tests/test_reducibility.py`

## Step 1 — write the failing test (`symm/tests/test_reducibility.py`)

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

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_reducibility.py -q` → FAIL (module missing).

## Step 3 — minimal implementation (`symm/sym_engine/reducibility.py`)

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

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_reducibility.py -q` → PASS.

## Step 5 — final check
`python -m pytest symm/tests -q` — ALL tests (Tasks 1-8) green.

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-8-report.md`. Return ONLY: status, files
created, one-line test summary, concerns.
