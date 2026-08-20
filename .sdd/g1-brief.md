# Task brief — G1: Textbook symmetry-dimension validation table

This is your requirements document. Use the exact values below verbatim.

## Goal

Build a **validation deliverable + regression test** that runs the LieML symmetry
engine on six canonical PDEs whose Lie point symmetry algebra dimensions are known
from the literature, and certifies that the engine agrees with those published
values — or, where it cannot (genuinely infinite-dimensional algebras), that it
correctly *detects* the infinite part via its `stalled` flag rather than reporting
a wrong finite number.

This is ADVISORY.md gate **G1**. Its PASS criterion (from the advisory) is:
*"Engine dim matches the published table, or the discrepancy is explained by the
window and confirmed."* Honesty convention (project-wide): a correctly-labeled
discrepancy is a valid outcome — never silently pass a mismatch.

## Deliverable 1 — `symm/textbook_validation.py`

A script that is BOTH runnable (`python symm/textbook_validation.py` prints a table)
AND importable (`evaluate()` returns structured records for the test). Follow the
shape of the existing `symm/reductor/train_reductor.py` (a `build`/`evaluate` split
+ a `__main__` that prints).

### The six PDEs — construct them EXACTLY like this (verified to run)

```python
import sympy as sp
from symm.sym_engine.jet import PDE
from symm.sym_engine.eliminate import discover
from symm.sym_engine.crosscheck import numeric_nullity   # for the finite cross-check

def build(name):
    if name == "heat":                        # u_t = u_xx
        p = PDE.scalar_1plus1(None, 2, "heat", {})
        p.Delta = p.jet_sym(0, 1) - p.jet_sym(2, 0)
    elif name == "burgers":                   # u_t + u u_x = (1/10) u_xx
        nu = sp.Rational(1, 10)
        p = PDE.scalar_1plus1(None, 2, "burgers", {})
        p.Delta = p.jet_sym(0, 1) + p.u * p.jet_sym(1, 0) - nu * p.jet_sym(2, 0)
    elif name == "fisher":                    # u_t = u_xx + u(1-u)
        p = PDE.scalar_1plus1(None, 2, "fisher", {})
        p.Delta = p.jet_sym(0, 1) - p.jet_sym(2, 0) - p.u * (1 - p.u)
    elif name == "porous2":                   # u_t = (u^2 u_x)_x
        m = sp.Integer(2)
        p = PDE.scalar_1plus1(None, 2, "porous2", {})
        p.Delta = p.jet_sym(0, 1) - (m * p.u**(m - 1) * p.jet_sym(1, 0)**2
                                     + p.u**m * p.jet_sym(2, 0))
    elif name == "kdv":                       # u_t + u u_x + u_xxx = 0   (order 3)
        p = PDE.scalar_1plus1(None, 3, "kdv", {})
        p.Delta = p.jet_sym(0, 1) + p.u * p.jet_sym(1, 0) + p.jet_sym(3, 0)
    elif name == "transport":                 # u_t = u_x   (order 1, linear)
        p = PDE.scalar_1plus1(None, 1, "transport", {})
        p.Delta = p.jet_sym(0, 1) - p.jet_sym(1, 0)
    else:
        raise ValueError(name)
    p._init_onshell()
    return p
```

### The published table (authoritative — assert against these)

| key       | PDE                         | textbook dim | kind     | Dmax to use |
|-----------|-----------------------------|--------------|----------|-------------|
| heat      | u_t = u_xx                  | `"6+inf"`    | infinite | 5           |
| burgers   | u_t + u u_x = ν u_xx        | `5`          | finite   | 4           |
| fisher    | u_t = u_xx + u(1-u)         | `2`          | finite   | 4           |
| porous2   | u_t = (u² u_x)_x            | `4`          | finite   | 4           |
| kdv       | u_t + u u_x + u_xxx = 0     | `4`          | finite   | 3           |
| transport | u_t = u_x                   | `"inf"`      | infinite | 5           |

- Heat: 6-dimensional finite Lie point algebra PLUS an infinite-dimensional
  superposition ideal (β(x,t)∂_u for β solving the heat equation) — written "6 ⊕ ∞".
- Transport (any linear first-order PDE): infinite-dimensional point algebra.

### What `evaluate()` must do, per PDE

1. `res = discover(pde, 1, Dmax, on_step=lambda k, s: seq.append(s["dim"]))`,
   capturing the per-degree dim sequence `seq`.
2. Assign a **verdict**:
   - **finite** kind → PASS iff `(not res.stalled) and res.dim == textbook_dim`.
     Otherwise `"DISCREPANCY"`.
   - **infinite** kind → PASS iff `res.stalled` (engine detected the infinite part).
     Otherwise `"DISCREPANCY"`. (A growing `seq` is the corroborating evidence.)
   - Name the two passing verdicts distinctly, e.g. `"MATCH"` (finite) and
     `"INF-DETECTED"` (infinite), so the table reads honestly.
3. **Finite cross-check (rigor, do this):** for the finite cases, also compute
   `numeric_nullity(pde, res.D)` and confirm it equals `res.dim`. This is the same
   exact-rational-vs-numeric-SVD agreement the fuzz test uses; include it in the
   record as `numeric_ok`. If it ever disagrees, that is a `"DISCREPANCY"` too.
4. Return a list of records (dicts) with at least:
   `name, pde_str, textbook, kind, engine_dim, stalled, seq, final_D, numeric_ok, verdict`.
   Also return/print a summary: number of rows PASS, and an explicit list of any
   DISCREPANCY rows (empty is the expected, good outcome).

### Expected result (from a verified controller recon — your output must reproduce this)

```
heat       textbook 6+inf   engine dim=12 stalled=True   seq=[6,8,10,11,12]  -> INF-DETECTED
burgers    textbook 5       engine dim=5  stalled=False  seq=[4,5,5]         -> MATCH
fisher     textbook 2       engine dim=2  stalled=False  seq=[2,2]           -> MATCH
porous2    textbook 4       engine dim=4  stalled=False  seq=[4,4]           -> MATCH
kdv        textbook 4       engine dim=4  stalled=False  seq=[4,4]           -> MATCH
transport  textbook inf     engine dim=98 stalled=True   seq=[10,22,40,65,98]-> INF-DETECTED
```

All six PASS: 4 finite MATCH + 2 INF-DETECTED, zero unexplained discrepancies.

### Honesty guardrail on the heat row (IMPORTANT — do not overclaim)

The heat D=1 window happens to report 6, which equals the textbook *finite-part*
dimension. You MAY print this as an **observation** (e.g. a comment or a note column
"D=1 window = 6, = finite-part dim"), but you must NOT assert or claim that the
engine "recovers the 6 finite generators" — that exact identification is unverified
and the windowed count also includes low-degree superposition solutions. The only
verified claim for heat/transport is: *the engine detects the infinite-dimensional
part (stalled=True); the finite/infinite split is not separately extracted — a known
window limitation.* State it that way in any docstring or printed note.

## Deliverable 2 — `symm/tests/test_textbook_validation.py`

Pin the outcome so it can never silently regress. Assert:

- `evaluate()` returns exactly 6 records; every record's `verdict` is a PASS verdict
  (MATCH or INF-DETECTED); the DISCREPANCY list is empty.
- **Finite cases** (burgers, fisher, porous2, kdv): assert exact `engine_dim`
  (5, 2, 4, 4 respectively), `stalled is False`, and `numeric_ok is True`.
- **Infinite cases** (heat, transport): assert `stalled is True` and that `seq` is
  strictly increasing (monotone growth — the infinite-part signature). Do NOT pin
  the exact growing dim values beyond, at most, `seq[0]` if you want one regression
  anchor (heat seq[0]==6, transport seq[0]==10) — keep it robust, assert growth not
  full sequences.

## Constraints & conventions (match the existing codebase)

- **Environment:** system Python 3.14, sympy 1.14, numpy 2.3.5. **No sklearn.**
  torch is CPU-only (not needed here). This folder is **NOT a git repo** — do not
  run any git command.
- **Run tests** from the project root: `python -m pytest symm/tests -q`. The full
  suite is currently **40 passed**; after your two files it should be 40 + your new
  test's cases, all green, with no regression to the existing 40.
- Imports use the `symm.` package prefix (e.g. `from symm.sym_engine.jet import PDE`),
  exactly as `symm/tests/test_generator_fuzz.py` does.
- Match the house style of `symm/reductor/train_reductor.py`: module docstring stating
  what is measured and the honesty caveats; deterministic (no RNG — `discover` is
  deterministic); a `__main__` that prints a readable table.
- Keep it self-contained: import only from `symm.sym_engine.*`. Do not modify any
  existing engine module.

## TDD

Write the test first (it will fail because the script doesn't exist yet), then the
script, then green. Report the exact `pytest` command you ran and its output.
