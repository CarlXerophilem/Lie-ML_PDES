# Task 2 Implementation Report — Determining-Matrix Builder

## Summary
Task 2 (determining-matrix builder) completed successfully. All tests green; no deviations or fallbacks required.

## Files Created
1. `D:\MATHs\math 4890 LieML\symm\sym_engine\determining.py` — implementation (exact code from brief)
2. `D:\MATHs\math 4890 LieML\symm\tests\test_determining.py` — tests (exact code from brief)

## Test Execution

### Step 2: Verify Initial Failure
```
cd /d/MATHs/math\ 4890\ LieML
python -m pytest symm/tests/test_determining.py -q
```
Result: FAILED (as expected — module `determining` did not exist)
```
ERROR collecting symm/tests/test_determining.py
ModuleNotFoundError: No module named 'symm.sym_engine.determining'
```

### Step 4: Verify Implementation Passes
```
python -m pytest symm/tests/test_determining.py -q
```
Result: PASSED
```
.. 
2 passed in 0.78s
```

### Step 5: Full Test Suite
```
python -m pytest symm/tests -q
```
Result: ALL PASSED
```
......
6 passed in 0.89s
```

## Implementation Details

### `ansatz(pde, D) -> (tau, xi, phi, coeffs)`
- Generates polynomial infinitesimals `tau, xi, phi` of degree `<= D` in `(x, t, u)`
- Returns coefficients as a list of fresh symbols `c_0, c_1, ...`
- For Burgers `D=2`: 3 infinitesimals × 10 monomials = 30 coefficients ✓

### `determining_matrix(pde, D) -> (A, coeffs)`
- Calls `ansatz` to get the infinitesimals and coefficient symbols
- Computes the symmetry residual via `symmetry_residual(pde, tau, xi, phi)` (from Task 1)
- Expands the residual over the full variable set: `free_jet_syms() + [x, t, u]`
- Extracts polynomial coefficients w.r.t. each variable monomial
- Returns each row as the linear dependence of that monomial on `coeffs`
- For Burgers `D=2`: 30 columns, `rank = 25`, nullity = 5 ✓

### Nullity Check
- Test expects `A.cols - A.rank() == 5` (Burgers Lie algebra dimension)
- No parameter substitution was needed; symbolic rank computation completed correctly
- No fallback required

## Deviations / Fallbacks
None. Implementation and tests used exactly as specified in the brief.

## Concerns
None. All constraints satisfied:
- No new dependencies (uses sympy 1.14, numpy, scipy, pytest only)
- Determinism: no randomness; polynomial monomial order is stable
- Exactness: all matrix entries are symbolic rational/polynomial (no floats)
- Scope: scalar PDEs in `(x, t, u)`, order `k <= 3`, Lie point symmetries ✓
- Task 1 tests remain unmodified and pass ✓

## Completion Date
2026-06-27
