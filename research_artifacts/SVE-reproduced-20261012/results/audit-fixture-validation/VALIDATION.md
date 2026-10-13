# Project-audit fixture repair, 2026-10-14

The failing test was `test_missing_expanded_evidence_is_not_a_false_carrier_failure`.
It is a test-fixture portability defect, not an SVE equation or solver failure.

## Cause and change

The fixture used `write_text("unique history\n")`. On Windows this wrote
`b"unique history\r\n"`, but its manifest recorded the hash of
`b"unique history\n"`. The byte-preservation audit correctly rejected the mismatch.
The fixture now uses `write_bytes(history)` and hashes the same `history` value.
Production audit code and its byte-integrity requirements are unchanged.

The original failure was reproduced before editing; `before.log` and
`diagnosis.json` retain the assertion, actual bytes, both hashes and audit issue.
Historical validation records are preserved as records of their dated runs.

## Fresh verification

- All 8 audit tests passed, including archive/ZIP corruption detection.
- The same combined regression set now passes: **174 passed, 0 failed** in 50.56 seconds.
- The project data-flux checker and workflow runner passed.
- Source-only `git diff --check` passed.
- Frozen manifest and ZIP hashes are unchanged; `integrity.json` records them.
- The separate project audit still reports **218 issues**; identical issue set to the preceding validation: **True**.

The audit categories are: 1 available_history_preserved, 30 canonical_reference_integrity, 41 active_markdown_links, 146 temporary_outputs_untracked.

Exact commands, timings and results are in `commands.json` and `validation.json`; full command output is retained in the adjacent logs.
