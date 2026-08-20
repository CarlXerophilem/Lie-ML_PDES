# Task 8 Report — Reducibility: defect, index, record, parameter tuple

## Implementation Status: DONE

### Summary
Task 8 has been successfully completed following TEST-FIRST methodology. The reducibility diagnostic module is now fully implemented with exact-backed dimension computation, defect metric, and reducibility index calculation.

### Files Created
1. **`symm/sym_engine/reducibility.py`** — Core implementation
   - `defect(pde, D) -> float`: Computes σ_min/σ_max ratio of column-normalized determining matrix
   - `reducibility_index(dim, delta, d_star=2) -> float`: Boundary-aware index formula (dim ≥ 1 → 0.5 + 0.5*min(dim/d_star, 1.0); dim = 0 → 0.5*(1-delta))
   - `ReducibilityRecord`: Dataclass with fields name, dim, status, delta, index, params, algebra, reductions, signature
   - `params_tuple(D, onshell_rule, d_star, param_values) -> dict`: Parameter tuple builder

2. **`symm/tests/test_reducibility.py`** — Test suite
   - `test_defect_zero_when_symmetry_exists()`: Verifies defect < 1e-6 for Burgers equation with known 5-dimensional symmetry algebra
   - `test_index_formula_boundaries()`: Validates index formula at four boundary points (dim=5, dim=1, dim=0 with delta=0 and delta=1)

### Test Results
- Task 8 tests (new): **2 passed** ✓
- Full suite (Tasks 1-8): **23 passed** ✓
- No failures; all existing tasks remain passing

### Implementation Details

#### `defect(pde, D)`
- Calls `numeric_matrix(pde, D)` to get the determining matrix M
- Column-normalizes M using `_column_normalize(M)` (per brief: W_V = W_E = I)
- Computes SVD to get singular values s
- Returns σ_min/σ_max; handles edge cases (empty matrix, zero singular values)

#### `reducibility_index(dim, delta, d_star=2)`
- When dim ≥ 1: returns 0.5 + 0.5 * min(dim/d_star, 1.0) (saturates at index=1.0 for dim ≥ d_star)
- When dim = 0: returns 0.5 * (1.0 - delta) (barren case, ranges from 0.5 at perfect near-symmetry to 0.0 at structureless)

#### `ReducibilityRecord`
- Dataclass with 9 fields: name, dim, status, delta, index, params, algebra (list), reductions (list), signature (dict)
- Provides structured record for later task consumption

#### `params_tuple(...)`
- Builds dictionary with D, onshell_rule, W_V="identity", W_E="identity", d_star, param_values
- Param values coerced to floats with string keys (for JSON/serialization compat)

### Validation
- Burgers equation (ν=0.1, D=2) has documented 5-dimensional symmetry algebra; test confirms defect < 1e-6
- Index formula tested at all four boundary cases specified in brief; all assertions pass
- Full regression suite confirms no regressions in Tasks 1-7

### Dependencies
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`
- Interfaces consumed from `crosscheck.py`: `numeric_matrix(pde, D)`, `_column_normalize(M)`
- Pure stdlib otherwise

## Concerns
None. Implementation is deterministic, minimal, and matches brief specification exactly.
