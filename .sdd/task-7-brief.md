# Task 7 brief — Independent numerical cross-check (SVD nullity)

Tasks 1-6 complete (do NOT modify them). Work TEST-FIRST. This module independently confirms the
exact algebra dimension via floating-point SVD of the determining matrix — a different method from the
exact rational rank, so agreement is a real completeness check.

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- Determinism: no randomness (numpy SVD is deterministic).
- Scope: scalar PDEs `(x,t,u)`, order `k<=3`.
- Not a git repo. Final step = tests green. Run from project root `D:\MATHs\math 4890 LieML`.

## Interfaces you CONSUME
- `symm/sym_engine/determining.py`: `determining_matrix(pde, D) -> (A, coeffs)` (A is a `sympy.Matrix`).
- `pde.params` is a dict mapping parameter Symbols to float values (e.g. `{nu: 0.1}`).

## Interfaces you PRODUCE (later tasks rely on these EXACT names)
In a NEW file `symm/sym_engine/crosscheck.py`:
- `numeric_matrix(pde, D) -> (M, coeffs)` — `A` with `pde.params` substituted to floats, as a numpy array.
- `_column_normalize(M)` — divide each nonzero column by its 2-norm (also imported by Task 8).
- `numeric_nullity(pde, D, tol=1e-9) -> int` — number of (near-)zero singular values of the
  column-normalized matrix, i.e. the numeric nullity.
- `agree(exact_dim, num_dim) -> bool`.

## Files
- Create: `symm/sym_engine/crosscheck.py`
- Test: `symm/tests/test_crosscheck.py`

## Step 1 — write the failing test (`symm/tests/test_crosscheck.py`)

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

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_crosscheck.py -q` → FAIL (module missing).

## Step 3 — minimal implementation (`symm/sym_engine/crosscheck.py`)

```python
# symm/sym_engine/crosscheck.py
import numpy as np
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

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_crosscheck.py -q` → PASS (numeric nullity == exact dim == 5).

## Step 5 — final check
`python -m pytest symm/tests -q` — ALL tests (Tasks 1-7) green.

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-7-report.md`. Return ONLY: status, files
created, one-line test summary, concerns.
