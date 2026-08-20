# Task 11 Report — CLI and Shim

## Status: DONE

### Files Created
1. `symm/symmetry_engine.py` — Re-export shim providing plan.txt-compatible interface
2. `symm/sym_engine_cli.py` — CLI module with `build_pde()` registry and `main()` entry point
3. `symm/tests/test_cli_shim.py` — Test suite (3 tests, all green)

### Test Summary
All 32 tests pass (Tasks 1–11): 3 new tests in test_cli_shim.py + 29 existing tests. Full suite runs in 6.04s.
- `test_shim_exports`: Verifies `Engine` and `PDE` are exported from `symmetry_engine`
- `test_build_pde_registry`: Verifies `build_pde()` correctly builds burgers, porous, fisher PDEs
- `test_cli_runs_burgers`: Full end-to-end CLI run of Burgers equation with Lie reduction, HAM closure, and CERTIFIED output

### Implementation Notes
- **No new dependencies**: Only uses sympy, numpy, scipy, pytest (existing).
- **Deterministic**: No randomness; full Burgers run completes in ~1.6s.
- **PDE Registry**: `build_pde()` supports `"burgers"` (ν=0.1), `"porous"` (m=2), `"fisher"` (unit coeffs).
- **CLI Interface**: `main(["run", <name>, "--workdir", <dir>, "--no-resume"])` orchestrates Engine→render pipeline.
- **TDD Workflow**: Test-first; all tests fail before implementation, all pass after.

### Verification
```
$ cd D:\MATHs\math 4890 LieML
$ python -m pytest symm/tests -q
32 passed in 6.04s
```

No concerns. Task complete.
