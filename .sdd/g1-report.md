# G1 report — Textbook symmetry-dimension validation table

Status: **DONE**. All six PDEs PASS (4 MATCH + 2 INF-DETECTED), zero unexplained
discrepancies. Full test suite green at 45 passed (40 pre-existing + 5 new),
no regressions. TDD followed: test written first (confirmed red), then the
implementation (confirmed green).

## Files created

- `symm/textbook_validation.py` — the deliverable script/module (`build()`,
  `TABLE`, `evaluate()`, `__main__` printer).
- `symm/tests/test_textbook_validation.py` — the regression test pinning the
  gate (5 test functions).

No existing file was modified.

## TDD sequence

1. Wrote `symm/tests/test_textbook_validation.py` against the not-yet-existing
   `symm.textbook_validation` module.
2. Confirmed RED: `python -m pytest symm/tests/test_textbook_validation.py -q`
   failed collection with `ModuleNotFoundError: No module named
   'symm.textbook_validation'`.
3. Before writing the implementation, independently re-ran the brief's exact
   PDE-construction + `discover()` calls in a scratch `python -c` script to
   confirm the "verified controller recon" numbers reproduce on this machine
   *before* committing to hard-coded test assertions. They reproduced exactly
   (see table below).
4. Wrote `symm/textbook_validation.py`.
5. Confirmed GREEN: all 5 new tests pass, and the full suite (45 tests) is
   green with no regressions to the pre-existing 40.

## Exact `python symm/textbook_validation.py` output

Run from the project root, reproduced identically under both Bash (git-bash)
and Windows PowerShell:

```
heat       textbook 6+inf   engine dim=12  stalled=True   seq=[6, 8, 10, 11, 12]     -> INF-DETECTED
burgers    textbook 5       engine dim=5   stalled=False  seq=[4, 5, 5]              -> MATCH
fisher     textbook 2       engine dim=2   stalled=False  seq=[2, 2]                 -> MATCH
porous2    textbook 4       engine dim=4   stalled=False  seq=[4, 4]                 -> MATCH
kdv        textbook 4       engine dim=4   stalled=False  seq=[4, 4]                 -> MATCH
transport  textbook inf     engine dim=98  stalled=True   seq=[10, 22, 40, 65, 98]   -> INF-DETECTED

6/6 PASS  (4 MATCH + 2 INF-DETECTED)
DISCREPANCY rows: (none - expected, good outcome)

NOTE (honesty guardrail on heat - do not overclaim):
  D=1 window reports dim=6, numerically = textbook finite-part dim. NOT a verified recovery of the 6 finite generators (window also mixes in low-degree superposition solutions); only stalled=True (infinite part detected) is verified.
  Verified claim for heat/transport is ONLY: the engine detects the
  infinite-dimensional part (stalled=True); the finite/infinite split
  is not separately extracted - a known window limitation.
```

This matches the brief's "Expected result (from a verified controller recon)"
table exactly, value for value: engine_dim, stalled, and the full per-degree
`seq` for every one of the six PDEs (heat dim=12 seq=[6,8,10,11,12]; burgers
dim=5 seq=[4,5,5]; fisher dim=2 seq=[2,2]; porous2 dim=4 seq=[4,4]; kdv dim=4
seq=[4,4]; transport dim=98 seq=[10,22,40,65,98]).

## Exact pytest command and output

Baseline, before any new files (recorded for the record — confirms the "40"
in the brief):

```
$ python -m pytest symm/tests -q
40 passed in 23.89s
```

Command run for this deliverable, from the project root, after both new files
were added:

```
$ python -m pytest symm/tests -q
45 passed in 45.92s
```

45 = 40 pre-existing + 5 new (`test_textbook_validation.py`). No regressions.
Isolated run of just the new file:

```
$ python -m pytest symm/tests/test_textbook_validation.py -v
test_all_six_pdes_present_with_required_schema PASSED
test_evaluate_returns_six_passing_records_with_no_discrepancy PASSED
test_finite_cases_match_textbook_dimension_exactly PASSED
test_infinite_cases_are_detected_via_stall_and_monotone_growth PASSED
test_heat_and_transport_do_not_overclaim_finite_extraction PASSED
5 passed in 23.65s
```

## What `evaluate()` does (per the brief's spec)

For each of the six PDEs, in the brief's order (heat, burgers, fisher,
porous2, kdv, transport):

1. Builds the PDE via `build(name)` — the brief's construction code, copied
   verbatim (byte-identical `Delta` formulas, `Dmax` per PDE from the
   authoritative table).
2. Calls `discover(pde, 1, Dmax, on_step=...)`, capturing the per-degree
   nullity sequence `seq`.
3. **Finite kind** (burgers, fisher, porous2, kdv): computes
   `numeric_nullity(pde, res.D)` and requires it to equal `res.dim`
   (`numeric_ok`); verdict is `"MATCH"` iff `not stalled AND dim == textbook
   AND numeric_ok`, else `"DISCREPANCY"`.
4. **Infinite kind** (heat, transport): verdict is `"INF-DETECTED"` iff
   `res.stalled`, else `"DISCREPANCY"`. The monotone-growth `seq` is kept in
   the record as corroborating evidence (and is asserted strictly increasing
   in the test).
5. Returns a list of 6 dicts, each with `name, pde_str, textbook, kind,
   engine_dim, stalled, seq, final_D, numeric_ok, verdict` (all fields the
   brief required) plus one additional field, `note` (`None` for five rows,
   the honesty-guardrail text for `heat`) — an optional "note column" the
   brief explicitly permitted ("You MAY print this as an observation...").
6. `__main__`/verbose mode prints the table, a `"k/6 PASS (... MATCH + ...
   INF-DETECTED)"` summary, the `DISCREPANCY` list (empty here), and the
   heat honesty note, unconditionally.

## Honesty guardrail — how it's enforced, not just stated

Per the brief's binding instruction, the heat row's D=1 window value of 6 is
**never** asserted or printed as "the engine recovers the 6 finite
generators." Concretely:

- `textbook` for heat is kept as the string `"6+inf"` (not the bare int `6`),
  so the verdict machinery structurally cannot call it a numeric `"MATCH"` —
  only `"INF-DETECTED"` is reachable for `kind == "infinite"`.
- The module docstring's "HONESTY GUARDRAIL" section and the printed
  `HEAT_NOTE` string state, verbatim, that only `stalled=True` is verified,
  and that the finite/infinite split is not separately extracted.
- `symm/tests/test_textbook_validation.py::test_heat_and_transport_do_not_overclaim_finite_extraction`
  pins `by_name["heat"]["textbook"] == "6+inf"` and
  `by_name["transport"]["textbook"] == "inf"` as a regression guard against
  someone later "simplifying" the textbook column to a bare finite number.

## Deviations from the brief (both disclosed, neither changes the math)

1. **sys.path shim, added to make the literal run command actually work.**
   The brief mandates package-style imports (`from symm.sym_engine.jet import
   PDE`, matching `test_generator_fuzz.py`) AND that `python
   symm/textbook_validation.py` be directly runnable. Those two requirements
   conflict without help: when Python runs a script by path, it puts the
   *script's own directory* (`.../symm/`) on `sys.path[0]`, not the project
   root — so `import symm...` from inside a directly-run `symm/*.py` file
   raises `ModuleNotFoundError: No module named 'symm'`. (Pytest doesn't hit
   this because its rootdir-insertion mechanism separately puts the project
   root on `sys.path`.) I confirmed this failure directly before fixing it.
   Fix: a 4-line, standard, idempotent shim at the top of
   `textbook_validation.py` that inserts the project root into `sys.path` if
   it isn't already there:
   ```python
   _ROOT = Path(__file__).resolve().parent.parent
   if str(_ROOT) not in sys.path:
       sys.path.insert(0, str(_ROOT))
   ```
   This touches only the new file, has no effect when the module is imported
   normally (pytest's path is already correct, so the `if` is a no-op), and
   was verified to work identically under both Bash and PowerShell. Flagging
   this because it's the one piece of plumbing the brief didn't anticipate.
2. **Two extra test functions beyond the minimum pinned set:** a schema check
   (`test_all_six_pdes_present_with_required_schema`, confirming all 6 names
   appear and every record has at least the brief's required keys) and the
   honesty-guardrail label check described above. Both are additive
   regression safety nets, not changes to required behavior.
3. **One extra record field**, `note` (see above) — additive, does not
   remove or rename any of the brief's required fields.

No other deviations. `Dmax` per PDE, the `build()` bodies, the verdict names
(`MATCH`/`INF-DETECTED`/`DISCREPANCY`), and the returned-record schema all
match the brief exactly.

## Concerns

None blocking. Two things worth flagging for whoever reads this next:

- The heat/transport `numeric_ok` field is `None` (not computed) per the
  brief's scope ("for the finite cases, also compute..." — infinite cases
  were not asked for a numeric cross-check, and `numeric_nullity` at `D=5`
  on a 5th-order-window ansatz would be materially more expensive for no
  specified benefit). If a future gate wants a numeric cross-check on the
  infinite cases too, that's a new requirement, not something silently
  skipped here.
- This satisfies gate **G1** only. Per `ADVISORY.md`, G1 is a prerequisite
  for G7 (results write-up) but the course-thesis bar is G1 **+ G5**; G5
  (end-to-end Fisher run) is untouched by this task.

## Environment notes

- System Python 3.14.2, sympy 1.14.0, numpy 2.3.5 — no sklearn used, no
  torch used (not needed for this deliverable).
- No git command was run at any point (confirmed the folder is not a git
  repo; this task required no git interaction regardless).
- No existing module under `symm/sym_engine/` (or anywhere else) was
  modified.
