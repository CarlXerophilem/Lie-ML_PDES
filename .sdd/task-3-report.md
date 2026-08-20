# Task 3 Report — Iterative elimination / algebra-discovery loop

## Files Created

- `symm/tests/test_eliminate.py` — test file (Step 1, verbatim from brief)
- `symm/sym_engine/eliminate.py` — implementation (Step 3, verbatim from brief)

## Pytest Commands and Full Output

### Step 2 — Confirm failing (before implementation)

```
cd "D:/MATHs/math 4890 LieML"
python -m pytest symm/tests/test_eliminate.py -q
```

Output (truncated to key lines):
```
E   ModuleNotFoundError: No module named 'symm.sym_engine.eliminate'
1 error in 0.75s
```
FAIL confirmed as expected.

### Step 4 — Verify new tests pass

```
python -m pytest symm/tests/test_eliminate.py -q -v
```

Output:
```
platform win32 -- Python 3.14.2, pytest-9.0.1, pluggy-1.6.0
rootdir: D:\MATHs\math 4890 LieML
plugins: anyio-4.13.0
collected 2 items

symm\tests\test_eliminate.py .. [100%]

2 passed in 1.99s
```

### Step 5 — Full suite

```
python -m pytest symm/tests -q -v
```

Output:
```
platform win32 -- Python 3.14.2, pytest-9.0.1, pluggy-1.6.0
rootdir: D:\MATHs\math 4890 LieML
plugins: anyio-4.13.0
collected 8 items

symm\tests\test_determining.py .. [ 25%]
symm\tests\test_eliminate.py .. [ 50%]
symm\tests\test_jet.py .... [100%]

8 passed in 2.15s
```

ALL 8 tests green. Tasks 1, 2, and 3 all pass.

## Deviations / Fallbacks

None. The implementation was used verbatim from the brief with no changes.
- `sp.nsimplify` worked without issue on Burgers null-space entries (they are plain rationals).
- No `simplify` fallback was needed.
- `A.rank()` / `A.nullspace()` at degree D=3 ran quickly (~2 s total for both test functions), well within limits.

## Observed behaviour

- Burgers at D=1: nullity = 3 (spatial translation, time translation, scaling — the linear generators).
- Burgers at D=2: nullity = 5 (adds the Galilean boost and projective generator, which is quadratic in t).
- D=1 → D=2 dimension change: 3 → 5. D=2 → D=3 dimension stays 5 → stabilized; `result.D` is set back to 2, matching `assert res.D == 2`.
- The callback test (`seen == [1, 2, 3]`) confirms `on_step` fires at every degree iterated, not just on stabilization.

## Concerns

None. All gates pass; no vacuous bounds; no numeric tolerance introduced; implementation is exact sympy rational.

## Fix 1 — Critical bug: basis/coeffs inconsistency on stabilization

### Bug description

In the original `discover`, when dimension stabilized the code set `result.D = D-1` and `result.dim = prev_dim` but left `result.basis` and `result.coeffs` from degree `D`. Because `ansatz` in `determining.py` assigns coefficient symbols `c_i` to different monomials at each degree, the returned triple `(D, basis, coeffs)` was inconsistent: the basis vectors used degree-D numbering while the reported degree was D-1. Downstream generator reconstruction produced wrong (or zero) generators.

### Fix applied

`symm/sym_engine/eliminate.py` — `discover` now tracks `prev_basis` and `prev_coeffs` alongside `prev_dim`. On stabilization it restores all three to the earlier degree's values before returning:

```python
result.D = D - 1
result.dim = prev_dim
result.basis = prev_basis
result.coeffs = prev_coeffs
```

Two regression tests added to `symm/tests/test_eliminate.py`:
- `test_discovered_generators_are_real_symmetries` — rebuilds the ansatz at `res.D`, substitutes each basis vector, and asserts `symmetry_residual == 0` for all 5 generators. This is the real gate: it FAILS against the old buggy code and PASSES after Fix 1.
- `test_single_degree_is_marked_stalled` — confirms a single-degree run is correctly flagged `stalled=True`.

### Pytest command and output

```
cd "D:\MATHs\math 4890 LieML"
python -m pytest symm/tests -q
```

```
..........                                                               [100%]
10 passed in 2.08s
```

All 10 tests green: 4 from test_jet.py (Tasks 1-2), 2 from test_determining.py (Task 2), 4 from test_eliminate.py (original Task 3 pair + both new Fix 1 regression tests).

### Concerns

None. The fix is minimal and surgical — only `discover` is changed; `EliminationResult` and `_nullspace_maps` are untouched. All assertions are exact sympy rational arithmetic; no floating-point tolerance introduced.
