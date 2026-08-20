# Task 5 Report — Reduction: invariants and the residual-zero reduced ODE

## Status
DONE

## Files Created
- `symm/tests/test_reduce.py` — test file (verbatim from brief Step 1)
- `symm/sym_engine/reduce.py` — implementation (verbatim from brief Step 3, with one deviation in scaling branch noted below)

## Pytest Commands and Output

### Step 2 — confirm FAIL before implementation
```
python -m pytest symm/tests/test_reduce.py -q
# Result: ERROR (ImportError: No module named 'symm.sym_engine.reduce') — EXPECTED FAIL
```

### Step 4 — confirm three tests PASS
```
python -m pytest symm/tests/test_reduce.py -v
# Result:
# PASSED symm/tests/test_reduce.py::test_travelling_wave_reduction_residual_zero
# PASSED symm/tests/test_reduce.py::test_steady_reduction_from_dt
# PASSED symm/tests/test_reduce.py::test_dx_alone_returns_none
# 3 passed in 0.53s
```

### Step 5 — full suite (Tasks 1–5)
```
python -m pytest symm/tests -q
# 16 passed in 3.01s
```

## Deviations
- **Scaling branch (touched, minor simplification):** The brief's `tpow`/`cand` logic using `sp.gcd(Ez, t)` was replaced with the simpler `cand = Ez` per the NOTES fallback ("you may replace the `tpow`/`cand` lines with `cand = Ez`"). This reports the residual honestly if `t` remains; it does not affect the three tested cases (all translation-branch). No test exercises the scaling branch.
- No test assertions were changed.

## Concerns
None. All 16 tests (Tasks 1–5) pass cleanly. Translation branch is fully correct. Scaling branch is best-effort as specified.

## Fix 1 — Constant-check guards on scaling-family coefficients

### Changes
1. **`symm/sym_engine/reduce.py` (lines 40–45):** Added `_is_const` guards to reject non-constant coefficients in the scaling family.
   - `a = tau/t` must now be constant in `(x, t, u)` before accepting the scaling branch
   - `b = xi/x` and `e = phi/u` must now be constant in `(x, t, u)` before accepting the scaling branch
   - Non-constant generators (e.g., projective `tau=t**2` giving `a=t`) now correctly fall through to `return None`

2. **`symm/tests/test_reduce.py` (appended):** Added regression test `test_projective_generator_returns_none()` to verify projective generators are rejected.

### Pytest Commands and Output

```
python -m pytest symm/tests/test_reduce.py -q
# 4 passed in 0.53s
```

```
python -m pytest symm/tests -q
# 17 passed in 3.00s
```

### Status
**DONE** — All 17 tests pass (including the new regression test). The scaling-family branch now correctly enforces constant coefficients.
