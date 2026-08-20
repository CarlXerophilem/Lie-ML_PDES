# Task 4 Report — Generators, dimension, structure constants, algebra type

## Status
DONE

## Files created
- `symm/tests/test_algebra.py` — test file (verbatim from brief)
- `symm/sym_engine/algebra.py` — implementation (verbatim from brief)

## TDD sequence

### Step 1 — write failing test
Wrote `symm/tests/test_algebra.py` exactly as specified in the brief.

### Step 2 — confirm FAIL
```
python -m pytest symm/tests/test_algebra.py -q
```
Result:
```
ERROR collecting symm/tests/test_algebra.py
ModuleNotFoundError: No module named 'symm.sym_engine.algebra'
1 error in 0.60s
```
Confirmed: ImportError as expected (module does not yet exist).

### Step 3 — write implementation
Wrote `symm/sym_engine/algebra.py` exactly as specified in the brief. No deviations.

### Step 4 — confirm PASS
```
python -m pytest symm/tests/test_algebra.py -q
```
Result:
```
...                                                                     [100%]
3 passed in 1.85s
```
All 3 tests pass including the critical `info["solvable"] is False` gate, confirming the
derived-series computation correctly identifies the Burgers point algebra as non-solvable
(it contains an sl(2,R) subalgebra).

### Step 5 — full suite
```
python -m pytest symm/tests -q
```
Result:
```
.............                                                           [100%]
13 passed in 2.95s
```
All 13 tests across Tasks 1-4 pass.

## Deviations
None. Both files are verbatim copies of the code in the brief.

## Concerns
None. The `structure_constants` call did NOT raise "algebra not closed in basis", confirming
the generators from `eliminate.discover` are consistent and the algebra closes. Runtime was
~2 seconds total for the full suite (sympy operations are fast at degree 2 for Burgers).
