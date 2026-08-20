# Task 7 Report — Independent Numerical Cross-Check (SVD Nullity)

## Status
**DONE** — All tests green, implementation complete.

## Implementation Summary

**Task 7** implements an independent floating-point SVD cross-check of the determining matrix rank, providing a numerically-distinct verification of the exact rational algebra dimension.

### Files Created
1. **`symm/tests/test_crosscheck.py`** — Test suite (1 test: `test_numeric_nullity_matches_exact()`)
2. **`symm/sym_engine/crosscheck.py`** — Core module with four exported functions

### Core Module (`crosscheck.py`)

**Public interface (4 functions):**

- `numeric_matrix(pde, D) -> (M, coeffs)` — Substitutes parameter symbols from `pde.params` into the exact symbolic determining matrix (from `determining_matrix()`), converts to float numpy array.
  
- `_column_normalize(M)` — Divides each nonzero column by its 2-norm; zero columns become 1.0 (identity operation). Guards against empty arrays.
  
- `numeric_nullity(pde, D, tol=1e-9) -> int` — Computes the numeric dimension of the null space via singular-value filtering:
  - Normalizes columns of the numeric matrix
  - Computes full SVD (singular values only)
  - Counts singular values < tolerance × max singular value
  - Handles edge cases: empty matrices, zero max singular value
  
- `agree(exact_dim, num_dim) -> bool` — Binary agreement check (`int(exact_dim) == int(num_dim)`).

### Key Design Decisions

1. **Column normalization before SVD** — Prevents conditioning issues from disparate coefficient scales; standard practice in rank computation.

2. **Relative tolerance** — Uses `tol=1e-9` as a threshold fraction of max singular value, making the test robust to numerical precision.

3. **Deterministic SVD** — numpy's SVD is deterministic (no randomness), consistent with task requirements.

4. **Parameter substitution chain** — Parameters are substituted at `numeric_matrix()` level, preserving parameter semantics from the PDE object.

### Test Results

```
symm/tests/test_crosscheck.py::test_numeric_nullity_matches_exact PASSED
  ✓ numeric_nullity(burgers_pde, D=2) == 5
  ✓ discover(burgers_pde, 1, 4).dim == 5  (exact rational rank)
  ✓ agree(5, 5) == True
```

**Full suite:** 21 tests pass (Tasks 1–7 all green, no regressions).

### Verification Details

The test uses the **Burgers equation** as the canonical test case:
- PDE: `u_t + u·u_x - ν·u_xx = 0` (with ν=0.1)
- Jet space: (x, t, u, u_x, u_t, u_xx)
- Expected algebra dim (exact rational): **5**
- Computed numeric nullity (SVD): **5** ✓

The agreement of the floating-point SVD rank with the exact rational rank confirms:
1. The determining system is correctly assembled.
2. Numerical conditioning is acceptable (no spurious singular values).
3. The exact symbolic dimension is operationally sound.

### No Concerns
- All dependencies (sympy, numpy, scipy, pytest) present.
- No external files or configuration needed.
- Code is production-ready for Task 8+ (which import `_column_normalize`).
