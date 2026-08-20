# Task 9 brief — Engine orchestrator (state machine, resume, status)

Tasks 1-8 complete (do NOT modify them). Work TEST-FIRST. This module ties the pipeline together:
discover -> checkpoint each degree -> generators -> reductions -> reducibility record -> status, with
a genuine resume (a completed run returns its saved record without recomputation).

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- Determinism: no randomness. A fresh run reproduces the same record; resume returns the saved record.
- Exactness: dim from exact rational rank (Task 3); only the defect uses float SVD.
- Status rule: `CERTIFIED` iff `dim>=1` AND at least one residual-zero reduction AND not stalled;
  `LATENT-ONLY` iff `dim==0`; otherwise `PARTIAL`.
- Secrets: none used here (DeepSeek is Task 10's stub). Not a git repo. Run from project root.

## Interfaces you CONSUME (already implemented)
- `eliminate.discover(pde, Dmin, Dmax, on_step) -> EliminationResult(.dim, .D, .basis, .coeffs, .stalled)`
- `algebra.generators(pde, result)`, `algebra.structure_constants(pde, gens)`, `algebra.algebra_type(sc)`
- `reduce.reduce_by(pde, gen) -> Reduction | None` (Reduction has `.z, .ode, .residual`)
- `reducibility.defect(pde, D)`, `reducibility.reducibility_index(dim, delta, d_star)`,
  `reducibility.ReducibilityRecord`, `reducibility.params_tuple(D, onshell_rule, d_star, param_values)`
- `crosscheck.numeric_nullity(pde, D)`, `crosscheck.agree(a, b)`
- `checkpoint.save_state(workdir, i, state)`, `checkpoint.append_steplog(workdir, line)`

## Interfaces you PRODUCE
- In `symm/sym_engine/engine.py`: `class Engine(pde, workdir, Dmin=1, Dmax=4, d_star=2)` with
  `run(resume=True) -> ReducibilityRecord`.
- Modify `symm/sym_engine/__init__.py` to also export `Engine` and `PDE`.

## Files
- Create: `symm/sym_engine/engine.py`
- Modify: `symm/sym_engine/__init__.py`
- Test: `symm/tests/test_engine.py`

## Step 0 — confirm a barren PDE before writing the LATENT-ONLY test
The barren test needs a scalar (1+1) **polynomial** PDE with NO nontrivial point symmetry (dim 0).
Before finalizing the test, open a quick python check from the project root:
`python -c "import sympy as sp; from symm.sym_engine.jet import PDE; from symm.sym_engine.eliminate import discover; p=PDE.scalar_1plus1(Delta=None,order=2,name='b',params={}); ux=p.jet_sym(1,0); ut=p.jet_sym(0,1); p.Delta=ut-ux**2-p.x*p.t*p.u; p._init_onshell(); print(discover(p,1,3).dim)"`
If it prints `0`, use `Delta = ut - ux**2 - x*t*u`. If it prints nonzero, try these (keep polynomial)
until one prints 0: `ut - ux**2 - x*u`, then `ut - x*ux**2 - t*u`, then `ut - ux**2 - (x+t)*u**2`.
Use whichever is confirmed barren in the test below.

## Step 1 — write the failing test (`symm/tests/test_engine.py`)
(Use the confirmed-barren `Delta` from Step 0 in `_barren()`.)

```python
# symm/tests/test_engine.py
import sympy as sp
from symm.sym_engine import Engine, PDE

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde

def _barren():
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="barren", params={})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1)
    pde.Delta = ut - ux**2 - pde.x * pde.t * pde.u   # <-- replace if Step 0 says nonzero
    pde._init_onshell()
    return pde

def test_burgers_certified(tmp_path):
    rec = Engine(_burgers(), workdir=str(tmp_path)).run(resume=False)
    assert rec.dim == 5
    assert rec.status == "CERTIFIED"
    assert any(r["residual_zero"] for r in rec.reductions)
    assert rec.signature["crosscheck_agrees"]

def test_resume_is_identical(tmp_path):
    eng = Engine(_burgers(), workdir=str(tmp_path))
    full = eng.run(resume=False)
    resumed = Engine(_burgers(), workdir=str(tmp_path)).run(resume=True)
    assert resumed.dim == full.dim
    assert resumed.status == full.status
    assert round(resumed.index, 6) == round(full.index, 6)

def test_barren_is_latent_only(tmp_path):
    rec = Engine(_barren(), workdir=str(tmp_path)).run(resume=False)
    assert rec.dim == 0
    assert rec.status == "LATENT-ONLY"
    assert rec.delta > 0.0
```

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_engine.py -q` → FAIL (Engine missing).

## Step 3 — implementation (`symm/sym_engine/engine.py`)

```python
# symm/sym_engine/engine.py
import os
import json
import sympy as sp
from dataclasses import asdict
from .eliminate import discover
from .algebra import generators, structure_constants, algebra_type
from .reduce import reduce_by
from .reducibility import (defect, reducibility_index, ReducibilityRecord, params_tuple)
from .crosscheck import numeric_nullity, agree
from .checkpoint import save_state, append_steplog


def _record_path(workdir):
    return os.path.join(workdir, "result.json")


def _save_record(workdir, rec):
    os.makedirs(workdir, exist_ok=True)
    with open(_record_path(workdir), "w", encoding="utf-8") as f:
        json.dump(asdict(rec), f, indent=2)


def _load_record(workdir):
    path = _record_path(workdir)
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return ReducibilityRecord(**d)
    except Exception:
        return None


class Engine:
    def __init__(self, pde, workdir, Dmin=1, Dmax=4, d_star=2):
        self.pde = pde
        self.workdir = workdir
        self.Dmin, self.Dmax, self.d_star = Dmin, Dmax, d_star

    def run(self, resume=True):
        if resume:
            cached = _load_record(self.workdir)
            if cached is not None:
                append_steplog(self.workdir, "- RESUMED: returned saved result.json")
                return cached

        pde = self.pde

        def on_step(i, state):
            save_state(self.workdir, i, state)
            append_steplog(self.workdir, f"- degree D={state['D']}: nullity={state['dim']}")

        result = discover(pde, self.Dmin, self.Dmax, on_step=on_step)
        gens = generators(pde, result)

        reductions = []
        for g in gens:
            try:
                red = reduce_by(pde, g)
            except Exception as exc:
                append_steplog(self.workdir, f"- reduction error (skipped): {exc}")
                red = None
            if red is not None:
                reductions.append({
                    "gen": [sp.srepr(c) for c in g],
                    "z": sp.srepr(red.z),
                    "ode": sp.srepr(red.ode),
                    "residual_zero": bool(sp.simplify(red.residual) == 0),
                })

        delta = defect(pde, result.D)
        idx = reducibility_index(result.dim, delta, self.d_star)
        num = numeric_nullity(pde, result.D)
        signature = {"dim": result.dim, "crosscheck_dim": num,
                     "crosscheck_agrees": agree(result.dim, num)}
        if gens:
            try:
                sc = structure_constants(pde, gens)
                signature["algebra_type"] = algebra_type(sc)
            except Exception as exc:
                signature["algebra_type_error"] = str(exc)

        if result.dim == 0:
            status = "LATENT-ONLY"
        elif any(r["residual_zero"] for r in reductions) and not result.stalled:
            status = "CERTIFIED"
        else:
            status = "PARTIAL"

        rec = ReducibilityRecord(
            name=pde.name, dim=result.dim, status=status, delta=delta, index=idx,
            params=params_tuple(result.D, "evolution:highest-t-derivative",
                                self.d_star, pde.params),
            algebra=[[sp.srepr(c) for c in g] for g in gens],
            reductions=reductions, signature=signature,
        )
        _save_record(self.workdir, rec)
        append_steplog(self.workdir, f"- STATUS={status} dim={result.dim} "
                                     f"delta={delta:.3e} index={idx:.3f}")
        return rec
```

## Step 3b — update `symm/sym_engine/__init__.py`
Ensure it exports both names (keep any existing exports):
```python
from .jet import PDE
from .engine import Engine
```

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_engine.py -q` → the three tests PASS.
NOTE: the Burgers run may take ~10-30 s because it attempts a best-effort scaling reduction whose
`sympy.simplify` is slow; that is acceptable — let it finish. CERTIFIED comes from the `d_t` reduction
(residual 0). If a reduction raises, the engine catches it and continues (by design).

## Step 5 — final check
`python -m pytest symm/tests -q` — ALL tests (Tasks 1-9) green.

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-9-report.md` (files, exact pytest commands +
output, which barren Delta you confirmed in Step 0, run timing, deviations, concerns). Return ONLY:
status, files created/modified, one-line test summary, and concerns.
