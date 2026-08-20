# Task 6 brief — Checkpoint / resume layer

Tasks 1-5 complete (do NOT modify them). Work TEST-FIRST. This module persists engine state so a
long symbolic run can resume after interruption, and serializes sympy objects exactly via `srepr`.

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- Determinism: no randomness. Serialization must round-trip sympy objects EXACTLY (use `sympy.srepr`).
- Not a git repo. Final step = tests green. Run from project root `D:\MATHs\math 4890 LieML`.

## Interfaces you PRODUCE (later tasks rely on these EXACT names)
In a NEW file `symm/sym_engine/checkpoint.py`:
- `encode(obj)` / `decode(obj)` — recursively convert sympy exprs to `{"__srepr__": "..."}` and back;
  lists/dicts/str/int/float/bool/None pass through.
- `save_state(workdir, step_index, state) -> str` — writes `checkpoint-NNN.json`, returns the path.
- `load_latest(workdir) -> (step_index, state) | (None, None)` — highest-numbered checkpoint; `(None, None)`
  if none/corrupt.
- `append_steplog(workdir, line) -> None` — append a line to `steplog.md`.

## Files
- Create: `symm/sym_engine/checkpoint.py`
- Test: `symm/tests/test_checkpoint.py`

## Step 1 — write the failing test (`symm/tests/test_checkpoint.py`)

```python
# symm/tests/test_checkpoint.py
import sympy as sp
from symm.sym_engine.checkpoint import save_state, load_latest, encode, decode

def test_roundtrip_sympy(tmp_path):
    x = sp.Symbol('x')
    state = {"D": 2, "expr": x**2 + 1, "list": [sp.Integer(3), "ok"]}
    save_state(str(tmp_path), 0, state)
    save_state(str(tmp_path), 1, state)
    idx, loaded = load_latest(str(tmp_path))
    assert idx == 1
    assert loaded["D"] == 2
    assert sp.simplify(loaded["expr"] - (x**2 + 1)) == 0
    assert loaded["list"][1] == "ok"

def test_load_missing_returns_none(tmp_path):
    assert load_latest(str(tmp_path)) == (None, None)

def test_encode_decode_nested(tmp_path):
    x, y = sp.symbols('x y')
    obj = {"a": [x, {"b": y + 1}], "n": 5, "s": "hi"}
    back = decode(encode(obj))
    assert back["a"][0] == x
    assert sp.simplify(back["a"][1]["b"] - (y + 1)) == 0
    assert back["n"] == 5 and back["s"] == "hi"
```

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_checkpoint.py -q` → FAIL (module missing).

## Step 3 — minimal implementation (`symm/sym_engine/checkpoint.py`)

```python
# symm/sym_engine/checkpoint.py
import os
import json
import glob
import sympy as sp


def encode(obj):
    if isinstance(obj, sp.Basic):
        return {"__srepr__": sp.srepr(obj)}
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return {"__repr__": repr(obj)}


def _from_srepr(s):
    return eval(s, {"__builtins__": {}}, dict(sp.__dict__))


def decode(obj):
    if isinstance(obj, dict):
        if "__srepr__" in obj:
            return _from_srepr(obj["__srepr__"])
        return {k: decode(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decode(v) for v in obj]
    return obj


def save_state(workdir, step_index, state):
    os.makedirs(workdir, exist_ok=True)
    path = os.path.join(workdir, f"checkpoint-{step_index:03d}.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"step_index": step_index, "state": encode(state)}, f, indent=2)
    os.replace(tmp, path)
    return path


def load_latest(workdir):
    files = sorted(glob.glob(os.path.join(workdir, "checkpoint-*.json")))
    for path in reversed(files):
        try:
            with open(path, encoding="utf-8") as f:
                blob = json.load(f)
            return blob["step_index"], decode(blob["state"])
        except Exception:
            continue
    return None, None


def append_steplog(workdir, line):
    os.makedirs(workdir, exist_ok=True)
    with open(os.path.join(workdir, "steplog.md"), "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")
```

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_checkpoint.py -q` → PASS (all three tests).

## Step 5 — final check
`python -m pytest symm/tests -q` — ALL tests (Tasks 1-6) green.

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-6-report.md`. Return ONLY: status, files
created, one-line test summary, concerns.
