# Task 12 brief — M1 acceptance suite + zero-to-one guide

Tasks 1-11 complete (do NOT modify them). This is the FINISH LINE: consolidate the M1 acceptance gate
and write the beginner guide with a REAL worked trace. Work TEST-FIRST for the M1 tests.

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- Determinism: no randomness.
- Not a git repo. Final step = full suite green + guide written. Run from project root.

## Interfaces you CONSUME
- `symm/sym_engine.Engine`, `symm.sym_engine_cli.build_pde`,
- `symm/sym_engine/crosscheck.py`: `numeric_nullity`, `agree`,
- `symm/sym_engine/eliminate.py`: `discover`,
- `symm/sym_engine/jet.py`: `symmetry_residual`.

## Files
- Create: `symm/tests/test_m1_gate.py`
- Create: `symm/sym_engine/GUIDE_zero_to_one.md`

## Step 1 — write the M1 acceptance tests (`symm/tests/test_m1_gate.py`)

```python
# symm/tests/test_m1_gate.py
import sympy as sp
from symm.sym_engine import Engine
from symm.sym_engine_cli import build_pde
from symm.sym_engine.crosscheck import numeric_nullity, agree
from symm.sym_engine.eliminate import discover

def test_m1_burgers_full_gate(tmp_path):
    pde = build_pde("burgers")
    rec = Engine(pde, workdir=str(tmp_path)).run(resume=False)
    assert rec.dim == 5 and rec.status == "CERTIFIED"
    assert any(r["residual_zero"] for r in rec.reductions)
    assert rec.signature["crosscheck_agrees"]

def test_m1_porous_scaling_family():
    pde = build_pde("porous")
    res = discover(pde, 1, 4)
    assert res.dim >= 2                      # at least translations + scaling
    assert agree(res.dim, numeric_nullity(pde, res.D))

def test_m1_negative_control_rejected():
    pde = build_pde("burgers")
    from symm.sym_engine.jet import symmetry_residual
    r = sp.simplify(symmetry_residual(pde, pde.u, sp.Integer(0), sp.Integer(0)))
    assert r != 0

def test_m1_resume_bit_identical(tmp_path):
    pde = build_pde("burgers")
    a = Engine(pde, workdir=str(tmp_path)).run(resume=False)
    b = Engine(build_pde("burgers"), workdir=str(tmp_path)).run(resume=True)
    assert (a.dim, a.status, round(a.index, 6)) == (b.dim, b.status, round(b.index, 6))
```

## Step 2 — run the M1 gate
`python -m pytest symm/tests/test_m1_gate.py -q` → all four PASS.
If `test_m1_porous_scaling_family` is slow at high degree, it should still stabilize early and finish;
let it run. If it genuinely FAILS (dim < 2 or crosscheck disagrees), STOP and report BLOCKED with the
observed dim — do NOT weaken the assertions.

## Step 3 — generate the real Burgers trace
Run: `python -m symm.sym_engine_cli run burgers --workdir symm/runs/burgers --no-resume`
This writes `symm/runs/burgers/steplog.md`. Read it and copy its lines into the guide's section 6.

## Step 4 — write the guide (`symm/sym_engine/GUIDE_zero_to_one.md`)
Use exactly this skeleton, and paste the REAL steplog lines from Step 3 into section 6 (replace the
`<paste...>` placeholder). Keep the rest as written:

```markdown
# From Zero to One: the LieML Symmetry Engine

## 1. The math in five lines
A symmetry is a generator X = tau d_t + xi d_x + phi d_u. Prolong it to derivatives, demand
pr^(k)X(Delta)=0 on solutions, and split on the free jet monomials -> the determining system. Its
solution space is the symmetry algebra. Pick a generator, find its invariants, substitute -> the PDE
collapses to an ODE. See ../../intro.tex sections 2-4 for the why.

## 2. Architecture (one line each)
- jet.py         generic prolongation + the PDE type
- determining.py the determining matrix A from a degree-D polynomial ansatz
- eliminate.py   degree-iterated exact-rational elimination -> the algebra (with checkpoints)
- algebra.py     generators, dimension, structure constants, algebra type
- reduce.py      characteristic invariants -> residual-zero reduced ODE
- reducibility.py exact dim (invariant) + metric defect/index (diagnostic)
- checkpoint.py  srepr<->JSON save/load + step log
- crosscheck.py  independent numerical SVD nullity
- engine.py      the state machine: run(resume=True)
- report.py / interfaces.py  human report + reductor/supervisor hooks

## 3. Run it
    python -m pytest symm/tests -q
    python -m symm.sym_engine_cli run burgers --workdir symm/runs/burgers --no-resume

## 4. What you get back (the reducibility record)
dim (exact, invariant) | algebra type | reductions (residual 0) | defect delta |
index rho in [0,1] | params pi | status. LATENT-ONLY = "no symmetry, saved anyway".
delta and rho are defined precisely in
docs/superpowers/specs/2026-06-26-lie-symmetry-engine-v1-design.tex (section 6).

## 5. Resume
The engine checkpoints each degree to symm/runs/<name>/checkpoint-NNN.json and saves the final
record to result.json. Re-running the same command with resume returns the saved record; a fresh run
is deterministic, so an interrupted run reproduces the same result.

## 6. Worked trace (Burgers)
<paste the symm/runs/burgers/steplog.md lines here>

## 7. How it will grow
propose_reductions() (interfaces.py) will become a learned ranker; review() will call
DeepSeek-V4-Pro with the key read from the DEEPSEEK_API_KEY environment variable (never hardcoded).
Both interfaces already exist as deterministic stubs.
```

## Step 5 — final full suite
`python -m pytest symm/tests -q` — ALL tests green (the complete engine).

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-12-report.md` (M1 results, the porous dim
observed, the pasted trace confirmation, final suite count). Return ONLY: status, files created,
one-line test summary, concerns.
