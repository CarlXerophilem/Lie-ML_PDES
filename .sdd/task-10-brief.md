# Task 10 brief — Report + extension interfaces (reductor ranker, supervisor stub)

Tasks 1-9 complete (do NOT modify them). Work TEST-FIRST. Two small modules: a markdown report
renderer, and the stable interfaces the deferred learned-reductor / DeepSeek-supervisor will implement.

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- Determinism: no randomness; stable sort.
- **Secrets:** `review` may read `DEEPSEEK_API_KEY` from the environment to set a boolean flag, but must
  make NO network call and must NEVER include the key value in its output.
- Not a git repo. Final step = tests green. Run from project root `D:\MATHs\math 4890 LieML`.

## Interfaces you CONSUME
- `symm/sym_engine/reducibility.py`: `ReducibilityRecord` (fields `name, dim, status, delta, index,
  params, algebra, reductions, signature`).

## Interfaces you PRODUCE (later tasks rely on these EXACT names)
- `symm/sym_engine/report.py`: `render(record) -> str` (markdown).
- `symm/sym_engine/interfaces.py`:
  - `propose_reductions(record) -> list[dict]` — deterministic ranker: orders `record.reductions` by
    ascending total `srepr` length of the generator (simplest first).
  - `review(record, steplog_text) -> dict` — deterministic supervisor stub with keys
    `crosscheck_ok, all_reductions_verified, stalled, note, deepseek_enabled`.

## Files
- Create: `symm/sym_engine/report.py`, `symm/sym_engine/interfaces.py`
- Test: `symm/tests/test_report_interfaces.py`

## Step 1 — write the failing test (`symm/tests/test_report_interfaces.py`)

```python
# symm/tests/test_report_interfaces.py
from symm.sym_engine.reducibility import ReducibilityRecord
from symm.sym_engine.report import render
from symm.sym_engine.interfaces import propose_reductions, review

def _rec():
    return ReducibilityRecord(
        name="burgers", dim=5, status="CERTIFIED", delta=0.0, index=1.0,
        params={"D": 2, "d_star": 2},
        algebra=[["Integer(1)", "Integer(0)", "Integer(0)"]],
        reductions=[{"gen": ["Integer(1)", "Symbol('c')", "Integer(0)"], "z": "Symbol('z')",
                     "ode": "x", "residual_zero": True}],
        signature={"dim": 5, "crosscheck_dim": 5, "crosscheck_agrees": True})

def test_render_contains_key_fields():
    txt = render(_rec())
    assert "burgers" in txt and "CERTIFIED" in txt and "index" in txt.lower()

def test_ranker_orders_by_simplicity():
    rec = _rec()
    rec.reductions.append({"gen": ["Add(Symbol('x'), Mul(Symbol('t'), Symbol('u')))",
                                   "Mul(Symbol('t'), Symbol('x'))", "Symbol('x')"],
                           "z": "z", "ode": "x", "residual_zero": True})
    ranked = propose_reductions(rec)
    def total(red):
        return sum(len(s) for s in red["gen"])
    assert total(ranked[0]) <= total(ranked[-1])     # simplest generator first
    assert total(ranked[0]) < total(ranked[1])       # the two differ, ordering is real

def test_review_no_secret_leak(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "SECRET123")
    out = review(_rec(), "steplog")
    assert out["deepseek_enabled"] is True
    assert "SECRET123" not in str(out)
    assert out["crosscheck_ok"] is True
    assert out["all_reductions_verified"] is True
```

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_report_interfaces.py -q` → FAIL (modules missing).

## Step 3 — minimal implementation

`symm/sym_engine/report.py`:
```python
# symm/sym_engine/report.py
def render(record):
    r = record
    lines = [f"# Reducibility report: {r.name}", "",
             f"- status: **{r.status}**",
             f"- dim: {r.dim}",
             f"- defect (delta): {r.delta:.6e}",
             f"- reducibility index: {r.index:.3f}",
             f"- params (pi): {r.params}",
             f"- crosscheck: {r.signature.get('crosscheck_dim')} "
             f"(agrees={r.signature.get('crosscheck_agrees')})",
             "", "## Generators"]
    for i, g in enumerate(r.algebra):
        lines.append(f"{i+1}. (tau, xi, phi) = {g}")
    lines += ["", "## Reductions"]
    if not r.reductions:
        lines.append("(none emitted)")
    for red in r.reductions:
        lines.append(f"- gen={red['gen']}  residual_zero={red['residual_zero']}")
    return "\n".join(lines)
```

`symm/sym_engine/interfaces.py`:
```python
# symm/sym_engine/interfaces.py
import os


def propose_reductions(record):
    def simplicity(red):
        return sum(len(s) for s in red["gen"])
    return sorted(record.reductions, key=simplicity)


def review(record, steplog_text):
    sig = record.signature
    all_verified = bool(record.reductions) and all(r["residual_zero"] for r in record.reductions)
    note_parts = []
    if not sig.get("crosscheck_agrees", True):
        note_parts.append("exact/numeric dimension disagree -> possible incompleteness")
    if record.status == "PARTIAL":
        note_parts.append("stalled or no reduction emitted; consider Maple hand-off")
    if record.status == "LATENT-ONLY":
        note_parts.append(f"no exact symmetry; nearest-symmetry defect={record.delta:.3e}")
    return {
        "crosscheck_ok": bool(sig.get("crosscheck_agrees", True)),
        "all_reductions_verified": all_verified,
        "stalled": record.status == "PARTIAL",
        "note": "; ".join(note_parts) or "ok",
        "deepseek_enabled": bool(os.environ.get("DEEPSEEK_API_KEY")),
    }
```

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_report_interfaces.py -q` → PASS (all four tests).

## Step 5 — final check
`python -m pytest symm/tests -q` — ALL tests (Tasks 1-10) green.

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-10-report.md`. Return ONLY: status, files
created, one-line test summary, concerns.
