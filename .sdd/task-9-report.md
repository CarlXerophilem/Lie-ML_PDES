# Task 9 Report — Engine orchestrator

## Files Created / Modified

- **Created**: `symm/sym_engine/engine.py` — full Engine class implementation
- **Created**: `symm/tests/test_engine.py` — three tests (TDD)
- **Modified**: `symm/sym_engine/__init__.py` — added `from .jet import PDE` and `from .engine import Engine`

## Step 0: Confirmed Barren Delta

The brief's four listed candidates all returned dim >= 1:
- `ut - ux**2 - x*t*u` → dim=1
- `ut - ux**2 - x*u` → dim=2
- `ut - x*ux**2 - t*u` → dim=1
- `ut - ux**2 - (x+t)*u**2` → dim=1

A wider search found several barren candidates. The confirmed-barren Delta used in the test:

```
Delta = ut - ux**2 + x**3 * u + t**2 * ux
```

Verified with `discover(p, 1, 4)`: dim=0, D=1, stalled=False, delta=0.512 > 0. All barren-test assertions satisfied.

## Step 1: Test written (TDD)

`symm/tests/test_engine.py` — used confirmed-barren Delta as noted above (deviation from brief's placeholder: the brief says "replace if Step 0 says nonzero", and Step 0 did confirm the placeholder nonzero — so replacement is correct per brief).

## Step 2: Confirmed FAIL

```
ImportError: cannot import name 'Engine' from 'symm.sym_engine'
1 error in 0.51s
```

## Step 3: Implementation

`symm/sym_engine/engine.py` implemented exactly per brief. One deviation/fix needed beyond the brief's verbatim code: the `algebra_type()` function (Task 7) returns a dict whose `"dim"` key is a `sympy.Integer` (from `C.shape[0]` on a sympy Array). This causes `json.dump(asdict(rec))` to raise `TypeError: Object of type Integer is not JSON serializable`. Fix: added a `_jsonify()` helper that recursively converts sympy scalars to Python native types, called in `_save_record()` before serializing. No other changes to Tasks 1-8.

## Step 4: Engine test run

```
python -m pytest symm/tests/test_engine.py -q -v
3 passed in 2.49s
```

Total elapsed wall time for the three tests: ~2.5 s (Burgers ran fast because Dmax=4 stabilized quickly and simplify on the translation reduction was immediate; the scaling reduction raised and was caught/skipped as expected).

## Step 5: Full suite

```
python -m pytest symm/tests -q
26 passed in 5.14s
```

All Tasks 1-9 green.

## Deviations from Brief

1. **Barren Delta replaced**: the brief placeholder `ut - ux**2 - x*t*u` gives dim=1, not 0. All four brief-listed fallbacks also failed. Used `ut - ux**2 + x**3*u + t**2*ux` (confirmed dim=0 in Step 0). This is explicitly authorized by the brief ("replace if Step 0 says nonzero").

2. **Added `_jsonify()` helper**: the brief's verbatim `_save_record` calls `json.dump(asdict(rec))` without a custom encoder. sympy `Integer` values in the `algebra_type` sub-dict cause a `TypeError` in Python's json module. Added a 12-line recursive converter; all logic is still in `engine.py` only and touches no existing module.

## Concerns

None. All assertions pass; resume works; barren test correctly labels LATENT-ONLY with delta > 0.

## Fix 1 (review: resume test coverage)

Enhanced `test_resume_is_identical` to close a coverage gap: the original test checked only 3 of 9 Record fields (`dim`, `status`, `index`). Added two assertions immediately after the original three:

```python
    assert resumed.reductions == full.reductions
    assert resumed.params == full.params
```

These assertions verify that the result.json round-trip preserves the `reductions` list and `params` dict exactly, catching any serialization bug in those critical fields.

Pytest output:

```
python -m pytest symm/tests/test_engine.py -q
3 passed in 2.77s

python -m pytest symm/tests -q
26 passed in 5.09s
```

All tests pass with the new assertions. Resume round-trip fidelity is now verified for reductions and params.
