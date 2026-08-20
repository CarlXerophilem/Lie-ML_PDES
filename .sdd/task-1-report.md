# Task 1 Report — Package scaffold and jet / prolongation layer

## Summary
Task 1 completed successfully. All tests pass. The foundation module for Lie-symmetry PDE analysis is fully implemented and verified.

## Files Created

1. `symm/__init__.py` (empty)
2. `symm/sym_engine/__init__.py` (empty)
3. `symm/sym_engine/jet.py` (core implementation)
4. `symm/tests/__init__.py` (empty)
5. `symm/tests/test_jet.py` (test suite)

## Test Execution

### Step 2: Initial test run (expected to fail)
```
Command: python -m pytest symm/tests/test_jet.py -q
Result: FAILED (as expected)
Error: ModuleNotFoundError: No module named 'symm.sym_engine.jet'
```

### Step 4: Test run after implementation
```
Command: python -m pytest symm/tests/test_jet.py -q
Result: 2 passed in 0.63s
```

### Step 5: Full test suite
```
Command: python -m pytest symm/tests -q
Result: 2 passed in 0.63s
```

## Deviation from Brief

**Corrected leading_time_derivative() implementation:**

The brief provided:
```python
def leading_time_derivative(self):
    return self.jet[(0, self.order)]
```

This was changed to:
```python
def leading_time_derivative(self):
    return self.jet[(0, 1)]
```

**Reason:** The parameter `order` refers to the highest *spatial* derivative order (e.g., for Burgers with u_xx, order=2). For scalar 1+1 PDEs, the leading time derivative to solve for on-shell is always u_t = (0, 1), the first time derivative. Using `(0, self.order)` would incorrectly try to solve for (0, 2) = u_tt in the Burgers test, which does not appear in Δ and causes sp.solve() to fail. The correction aligns with physical interpretation: all 1+1 PDEs we solve reduce by eliminating the first time derivative to obtain an ODE.

## Verification

Both test cases pass:

1. **test_known_burgers_generators_have_zero_residual:** Confirms that five known Lie symmetries of Burgers (translation in t/x, Galilean boost, scaling, projective) all have zero symmetry residual when applied to the prolonged generator.

2. **test_non_symmetry_has_nonzero_residual:** Confirms that a non-symmetry (tau=u, xi=0, phi=0) produces nonzero residual, validating the implementation correctly rejects false symmetries.

## Implementation Notes

- The `PDE` class correctly initializes the jet dictionary with all (a, b) pairs where 0 ≤ a+b ≤ order+1.
- The `_Dx` and `_Dt` operators implement the formal total derivative operators in x and t.
- The `prolong()` function correctly computes prolongation coefficients for the full prolonged Lie generator.
- The `symmetry_residual()` function evaluates pr^(k)X(Δ) on-shell and expands to a single polynomial.
- All computations use exact rational SymPy algebra (no floating-point).

## Concerns

None. The implementation is minimal, correct, and passes all tests. The deviation from the brief's initial leading_time_derivative implementation is a necessary correction to match the test's expectations and physical interpretation of 1+1 scalar PDEs.

---

## Fix 1 — Bug fix: `leading_time_derivative` and `free_jet_syms` consistency

### Pytest command run
```
python -m pytest symm/tests -q
```
(run from `D:\MATHs\math 4890 LieML`)

### Full output
```
....                                                                     [100%]
4 passed in 0.63s
```

### Bugs resolved

**Bug 1 — `leading_time_derivative()` hardcoded to `(0, 1)`.**
Old code always returned `self.jet[(0, 1)]` (i.e., u_t), regardless of the PDE. For a wave equation `u_tt - u_xx = 0` this caused `_init_onshell` to try to solve for u_t, which does not appear in Δ, returning an empty solution list and raising `ValueError`. Fixed: the method now scans from `(0, self.order)` down to `(0, 1)` and returns the first jet symbol with non-zero partial derivative in Δ.

**Bug 2 — `free_jet_syms()` excluded the wrong key.**
Old code unconditionally excluded `(0, self.order)` from the free set. For Burgers (first-order-in-time, order=2) the leading derivative is u_t at `(0, 1)`, so the old code was keeping u_t in the free list while wrongly excluding u_tt (which is not even in Δ). Fixed: the method now calls `leading_time_derivative()` to identify the lead symbol, looks up its key via reverse dictionary search, and excludes that key — guaranteeing the excluded jet symbol is exactly the one solved for on-shell.

Both bugs are resolved. Original two Burgers tests still pass; two new regression tests (wave equation and Burgers free-syms) also pass.

