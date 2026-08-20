# Task 11 brief — CLI and the plan.txt-compatible shim

Tasks 1-10 complete (do NOT modify them). Work TEST-FIRST. A small CLI to run/inspect a PDE, plus a
one-line shim so `from symm.symmetry_engine import Engine` works (matching the project's plan.txt name).

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. stdlib `argparse` is fine.
- Determinism: no randomness.
- Not a git repo. Final step = tests green. Run from project root `D:\MATHs\math 4890 LieML`.

## Interfaces you CONSUME
- `symm/sym_engine/__init__.py`: `Engine`, `PDE`.
- `symm/sym_engine/report.py`: `render`.

## Interfaces you PRODUCE
- `symm/sym_engine_cli.py`: `build_pde(name) -> PDE` (registry: `burgers`, `porous`, `fisher`),
  `main(argv=None) -> int` supporting `run <name> [--workdir DIR] [--no-resume]` which prints the report.
- `symm/symmetry_engine.py`: re-exports `Engine, PDE`.

## Files
- Create: `symm/sym_engine_cli.py`, `symm/symmetry_engine.py`
- Test: `symm/tests/test_cli_shim.py`

## Step 1 — write the failing test (`symm/tests/test_cli_shim.py`)

```python
# symm/tests/test_cli_shim.py
from symm import symmetry_engine
from symm.sym_engine_cli import build_pde, main

def test_shim_exports():
    assert hasattr(symmetry_engine, "Engine")
    assert hasattr(symmetry_engine, "PDE")

def test_build_pde_registry():
    for name in ("burgers", "porous", "fisher"):
        pde = build_pde(name)
        assert pde.name == name and pde.Delta is not None

def test_cli_runs_burgers(tmp_path, capsys):
    rc = main(["run", "burgers", "--workdir", str(tmp_path), "--no-resume"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "CERTIFIED" in out
    assert "dim: 5" in out
```

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_cli_shim.py -q` → FAIL (modules missing).

## Step 3 — minimal implementation

`symm/symmetry_engine.py`:
```python
# symm/symmetry_engine.py
from .sym_engine import Engine, PDE  # noqa: F401
```

`symm/sym_engine_cli.py`:
```python
# symm/sym_engine_cli.py
import argparse
import sympy as sp
from .sym_engine import Engine, PDE
from .sym_engine.report import render


def build_pde(name):
    if name == "burgers":
        nu = sp.Symbol('nu', positive=True)
        pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
        ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
        pde.Delta = ut + pde.u * ux - nu * uxx
        pde._init_onshell()
        return pde
    if name == "porous":
        m = sp.Integer(2)
        pde = PDE.scalar_1plus1(Delta=None, order=2, name="porous", params={})
        ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
        pde.Delta = ut - (m * pde.u**(m - 1) * ux**2 + pde.u**m * uxx)
        pde._init_onshell()
        return pde
    if name == "fisher":
        pde = PDE.scalar_1plus1(Delta=None, order=2, name="fisher", params={})
        ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
        pde.Delta = ut - uxx - pde.u * (1 - pde.u)
        pde._init_onshell()
        return pde
    raise ValueError(f"unknown PDE '{name}'")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="sym_engine")
    sub = parser.add_subparsers(dest="cmd", required=True)
    runp = sub.add_parser("run")
    runp.add_argument("name")
    runp.add_argument("--workdir", default="symm/runs/cli")
    runp.add_argument("--no-resume", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "run":
        pde = build_pde(args.name)
        rec = Engine(pde, workdir=args.workdir).run(resume=not args.no_resume)
        print(render(rec))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_cli_shim.py -q` → PASS. (The Burgers run may take ~5-30s.)

## Step 5 — final check
`python -m pytest symm/tests -q` — ALL tests (Tasks 1-11) green.

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-11-report.md`. Return ONLY: status, files
created, one-line test summary, concerns.
