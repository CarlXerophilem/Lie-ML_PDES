# Project refresh and 1D research programme — 21 October 2026

The repository cleanup and the reviewed one-dimensional research package are complete.
The integration target is `astra`; Git commit and remote-ref receipts are recorded
separately at release time, so this report does not invent a self-referential commit hash.

## Cleanup and preservation

- Archived and pruned 25 pre19 build directories: 6,927 files, 1,313,541,529 bytes.
  The verified archive is 1,172,045,698 bytes, outside this repository. See the
  [restore guide](../../docs/build-archive-20261021.md) and [receipt](old-build-archive-summary.json).
- Recorded 182 internal pytest symlink aliases separately; all numbered target
  files were archived. No junction or outside-target link was followed.
- Retained `build/week-4` because the dissertation directly inputs its table and figure.
- Removed 146 `tmp/` files from Git tracking only; local bytes and prior Git history
  remain intact. The [hash manifest](tmp-untracking-manifest.json) records them.
- Restored 30 canonical reference records to their original SHA256 identities,
  including a locally available Olver LFS object and an exact historical PDF recovery.
- Recovered three previously tracked prose files from `39d0f80^`; the restored
  week4 plan's reference path was then updated. Repaired genuine links and formula
  parsing, added UTF8 handling, and preserved the old detailed map under a dated name.
- All six preexisting tracked user-diff sections still matched the initial snapshot
  byte-for-byte before integration. User-edited drafts and Lie notes were not staged.

The [portable current carrier](../sve-current-20261021/README.md) contains 10,849
ordinary files / 107,622,521 bytes in a 52,892,588-byte ZIP. Both its source and an
isolated restored copy matched all 4,924 frozen release hashes and all three stage
gates. Optional cache aliases/bytecode are excluded; source/evidence bytes are preserved.
Old absolute execution paths remain provenance. Non-Windows gate replay is unvalidated.

## Current audit and validation

| Check | Current result |
|---|---|
| Project audit | **Failed, 1 issue**, down from 234: old 11 October external archive unavailable |
| Canonical references | 30 original hashes match |
| Active Markdown links | No missing targets |
| Frozen scalar carrier | All 78 entries and carrier hash preserved |
| data-flux / workflow | Verified / passed |
| Engine, chart and audit suite | 62 passed |
| Active scalar package | 43 passed |
| Frozen general-symm package | 410 passed |
| Final guarded-archive controls | 13 passed, including raw/normalized duplicate targets and top-level link rejection |
| New mathematical identities/control outcomes | 19 passed; fresh independent review accepted |

Commands, exit codes, timings and log hashes are in [receipts.json](receipts.json).
The final archive repair has a separate [receipt](archive-final-receipt.json).
The [audit report](audit/audit.md) retains the single failure; Git source history
is available but does not certify the missing hydrated external archive.
Historical 234-issue receipts were not rewritten. No TeX/bibliography source was
changed, so this cycle does not claim a fresh manuscript build or visual PDF QA.
`git diff --check` on the entire dirty workspace detects the user's preexisting
blank line in Lie_reduction.md; that unrelated file was preserved. Release files
are checked separately before commit.

## Research result and next gate

The [1D programme](../sve-1d-programme-20261021/README.md) imports 17 accepted E
traveling/scaling certificates from 8 branches, using the hash-bound seed0 run.
The later directory named final contains an execution timeout and is not the
acceptance authority. Classification coverage, registered reductions and solved
profiles are reported separately.

The demonstration verifies P/M common-scaling first integrals for symbolic m,
E traveling reduction to a separable first-order ODE on its regular slope chart,
and an independent evolving-bed E exact solution with a momentum-coupling negative
control. Exact local quadrature is distinguished from an elementary closed form.
Singular strata and general data remain explicit follow-up work.

Pure PINN training is stopped for the present workload. Hybrid ML remains a
conditional future option only for a named unmet task and measurable matched-cost
value; no new training ran. The bounded literature pass is not exhaustive:
75 local unique PDFs were not fully read, and the historical P nine-reduction
import remains pending. The next gate is to complete that source/reduction
inventory before claiming complete one-dimensional solution coverage.

[Independent mathematical review](../sve-1d-programme-20261021/FINAL_REVIEW.md)
and [cleanup/code review](INDEPENDENT_REVIEW.md) record the accepted scope and
repairs. E, printed P and corrected M evidence remain separate.
