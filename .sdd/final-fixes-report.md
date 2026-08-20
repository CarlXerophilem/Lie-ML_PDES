# Final Code-Review Fixes Report

Date: 2026-06-27

## FIX I1 — Strip common (x,t) monomial in reduce.py scaling branch

**File:** `symm/sym_engine/reduce.py`

**Change:** In the scaling-family branch, replaced the naive `cand = Ez` fallback with a proper monomial-factor extraction. After `powsimp`/`expand`/`simplify`, the code now:
1. Extracts the first term's (x,t)-only factor via `_xt_factor` (iterating `Mul.make_args`, keeping factors that have neither `z` nor `U`).
2. Divides the whole `Ez` by that common factor to produce `cand`.
3. Checks whether `cand` still contains `x` or `t` to set `residual`.

**New test added:** `symm/tests/test_reduce.py::test_porous_scaling_reduction_residual_zero`
- Builds the porous-medium PDE with m=2: `u_t = 2 u u_x^2 + u^2 u_xx`.
- Applies the Barenblatt scaling generator `(2t, x, 0)`.
- Asserts `red is not None` and `sp.simplify(red.residual) == 0`.
- This test FAILS on the old `cand = Ez` code and PASSES with the fix (the t-power monomial
  that survived simplify is now divided out, leaving a pure-z ODE).

---

## FIX I2 — Correct W_V label in params_tuple

**File:** `symm/sym_engine/reducibility.py`

**Change:** In `params_tuple`, changed `"W_V": "identity"` to `"W_V": "column-normalized"`.

**Rationale:** The `defect()` function calls `_column_normalize(M)` before the SVD, so `W_V`
(the column weighting scheme) is factually "column-normalized", not "identity". The label is
metadata only and does not affect any computation; W_E stays "identity" (no row weighting).

---

## FIX I3 — Resume cache guard + corrupt-record warning + recompute test

**File:** `symm/sym_engine/engine.py`

**(a) Corrupt-record warning in `_load_record`:**
Added `append_steplog(workdir, "- WARN: unreadable result.json, recomputing")` in the
`except Exception` branch so corrupt or truncated JSON files produce a visible steplog entry
rather than silently returning None.

**(b) Stale-cache guard in `Engine.run`:**
Changed the resume check from an unconditional "return if any cached record exists" to:
- Return the cache only if `cached.params.get("d_star") == self.d_star`.
- If a record exists but d_star differs, log "cache d_star mismatch; recomputing" and fall
  through to recompute.

This prevents a cached result computed with one `d_star` threshold from being silently returned
when the engine is re-instantiated with a different `d_star`.

**New assertions in:** `symm/tests/test_engine.py::test_resume_is_identical`
- After the existing resume assertions, deletes `result.json` from `tmp_path`.
- Calls `Engine(...).run(resume=True)` — with no cache file, the engine must recompute.
- Asserts `recomputed.dim == full.dim`, `recomputed.status == full.status`, and
  `recomputed.reductions == full.reductions`.
- This verifies deterministic recompute parity on Burgers' equation.

---

## Test Run

```
python -m pytest symm/tests -q
```

```
.....................................                                     [100%]
37 passed in 10.63s
```

**Previous count:** 36 tests. **New count:** 37 tests (added `test_porous_scaling_reduction_residual_zero`).
The `test_resume_is_identical` test now contains additional assertions (not a separate test node).
All 37 pass; no regressions.

---

## Concerns

None. The porous-medium residual gate is the key correctness gate and it passes. The W_V
label change has no effect on any numeric result (metadata only). The d_star cache guard is
conservative and correctly leaves the "same d_star" path unchanged.
