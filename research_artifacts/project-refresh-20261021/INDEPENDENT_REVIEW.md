# Independent review: archive lifecycle and 1D SVE programme

Review date: 21 October 2026. This was a bounded fresh read-only review of
`scripts/build_archive.py`, `scripts/tests/test_build_archive.py`, the refresh
contract, `STRUCTURE_MEASURES.md`, `ML_DECISION.md`, and the local evidence they
cite. I did not run the heavy symbolic workload or modify source/research files.

## Verdict

**Archive/prune: conditionally acceptable, but prune is not yet cleared by this
review.** The path guards, source re-inventory, byte hashes, non-overwriting
restore, and refusal of linked entries are materially sound. Prune may proceed
only after an isolated restore smoke test succeeds and the tracked links into
archived build output have an explicit restore notice. The checkout must remain
quiescent until deletion finishes. The final external ZIP and pack receipt now
exist: the receipt says `verified=true`, 6,927 files in 25 directories, and my
independent archive hash calculation matched its SHA-256
`8c14e984863d510af42bd67e60d9cfd3c218914c126922efe3fe463854e98530`.

**Research programme: accepted after one resolved scope correction.** The P/M
scalar identities, local first-integral/order claim, and bounded ML decision
agree with the cited project evidence. `STRUCTURE_MEASURES.md:23` now states the
reviewed full-system parameter ranges at the claim site and distinguishes the
mixed-order slope family.

## Findings

### [P1] State the proved exponent range on the maximal-algebra claim

**Resolved during review.**

`STRUCTURE_MEASURES.md:23` previously said the full first-order system has
maximal point dimension 4 for `m != 3` and 5 for `m = 3`, without stating the
range there.
The accepted review in
`build/sve-general-symm-20261020/CLASSIFICATION_REVIEW.md:11-19` proves this only
for fixed `1 <= m <= 4`; its slope cells are `n=m-1` or `n=m` in that range,
with the separate `K=0`, `0 <= n <= 4` family. As written, the sentence can be
read as an all-real-`m` maximality theorem. The revised line now gives these
ranges directly and identifies the slope system's mixed order. This does not
affect the later scalar common-dilation statement, which is a different model
and certificate.

### [P1, operational] Preserve the reparse-point exception receipt

The first `pack-old` attempt correctly failed because ten selected directories
contained 182 pytest `*current` directory symlinks; `inventory()` refuses them
at `scripts/build_archive.py:39-40`. The remediation is acceptable: all 182 were
symlinks (zero junctions), each resolved to a numbered target inside the same
selected build child, and the numbered target bytes remain ordinary archived
inputs. The external sidecar
`D:/MATHs/Lie-ML_PDES-archive/2026-10-21/pytest-cache-aliases.json` had SHA-256
`bb645c9ba967e22cbd79048bcfa279b04b6ed5abbb2988f676f0577209711cec`; the local
receipt records the same value, and a post-removal scan found no selected
reparse points. Keep both receipts with the final archive receipt. Alias
recreation is optional and must never be required for evidence recovery.

### [P1, operational] Prune has a final-check-to-delete race

`prune()` verifies hashes and re-inventories at lines 91-94, then recursively
deletes at line 99. A concurrent writer can create a file or replace a subtree
after the last inventory and before/during `rmtree`; that new material will not
be represented in the ZIP. Multiple directories are also deleted sequentially,
so interruption can leave a partial prune. The archive makes the latter
recoverable, but not an unarchived concurrent write. The root reports all old
writers inactive; retain that as an explicit operational precondition and do
not run tests/builds against the selected directories during prune.

### [P2] Archived build links need a visible restore route

The current selection includes `build/sve-equation27-manim-20261017`, while
tracked `docs/2026-10-17-sve-equation27-manim.md` links repeatedly into that
directory. Other tracked validation records also name archived build paths.
The contract permits an explicit restore path instead of retaining those trees,
but deleting them without a durable archive location, archive hash, and exact
`restore --directory ...` command leaves knowingly broken local links. Record
that route in the refresh artifact or archive documentation before integration.

### [P2] Archive tests cover the main happy/refusal paths, not the full contract

The focused test file passed 9 tests. It covers round-trip bytes, refusal of
modified/new post-pack files, overwrite refusal, and basic member traversal.
It does not cover the actual multi-directory `pack-old` selection, corrupt ZIP
or malformed manifest metadata, duplicate directory arguments, empty-directory
loss, interruption/partial restore, or the pytest-alias sidecar procedure.
This is not a reason to weaken the guards. The final acceptance should therefore
include a real archive verification plus a restore smoke test into an isolated
temporary root, not rely on the unit result alone.

## Research checks

- **E/P/M scope:** accepted. `ML_DECISION.md:5-16` keeps Eulerian `E`, printed
  scalar `P`, and advectively corrected scalar `M` distinct. Neither reviewed
  note transfers the scalar integral to the full system.
- **PDE dimension versus ODE order:** accepted. `STRUCTURE_MEASURES.md:9-19`
  separates point-algebra dimension, projected base-orbit rank, and usable
  first integrals. The example correctly distinguishes the rank-one
  PDE-to-ODE quotient from the later third-to-second-order drop.
- **First integral:** accepted within its declared chart. The formulas at
  `STRUCTURE_MEASURES.md:33-59` match
  `research_artifacts/sve-progress-20261010/docs/THEORY.md:198-232`: both P and
  M residuals are exact derivatives, and `F''=I0/L` is asserted only where
  `t>0`, `P>0`, `V>0`, and the model-specific `L != 0`. The note explicitly
  leaves `L=0`, data compatibility, bed reconstruction, and global continuation
  outside that symbolic identity.
- **ML decision:** accepted as a bounded negative. The 0/23 combined-gate
  count, 21 full L-BFGS budgets, error ranges, Chebyshev passes, and 284.0249 s
  campaign time match the 19 October report and saved JSON. The note says these
  results reject the tested pure-PINN workload, not all neural or hybrid
  methods; it requires matched-accuracy classical baselines and total-cost
  accounting for any reopened pilot.
- **No universal claim:** accepted. Neither note claims arbitrary-IBVP
  solvability, maximal scalar classification, neural speedup, a continuous
  learned-error certificate, or universal PINN failure.

## Checks run

```text
python -B -m pytest -q -p no:cacheprovider scripts/tests/test_build_archive.py
9 passed in 0.21s
```

Pytest then emitted the known Windows atexit warning while removing its global
`pytest-current` link; the nine test results themselves were complete. I also
enumerated the real `pack-old` selection, inspected tracked references to those
directories, verified the alias-sidecar hash, and re-scanned selected trees for
reparse points and independently matched the final ZIP's SHA-256 to the pack
receipt. I did not execute pack, prune, restore, the project-wide audit, LaTeX,
or the CPU-symbolic check; those remain root-owned acceptance steps.

## Narrow follow-up review: top-level aliases and duplicate selections

Review date: 21 October 2026. This follow-up inspected only the revised
`inventory()` path checks and the two added regression tests. No test command,
archive operation, or mathematical workload was run in this follow-up.

### [P2] Duplicate selection is checked by spelling, not by target identity

`scripts/build_archive.py:32` rejects `['old', 'old']`, but distinct spellings
can still designate the same direct child. For example, `['old', 'old/.']`
passes the `set(directories)` comparison, while both entries normalize to the
same `build/old` path. Packing then writes a manifest with two directory entries;
`prune()` constructs the same target twice, deletes it once, and fails on the
second `shutil.rmtree`. On Windows, case variants should also be treated by
resolved `WindowsPath` identity rather than raw strings. The new duplicate test
at `scripts/tests/test_build_archive.py:53-56` covers only byte-identical input.

Resolve each already-unlinked direct child, maintain a `seen_paths` set, and
reject a path already present before traversing it. Add at least the
`['old', 'old/.']` regression; a Windows case-variant case is also appropriate.

### Verdict

**Top-level alias fix accepted; duplicate-selection fix requires the narrow
canonical-target correction above.** The order at
`scripts/build_archive.py:35-40` now checks the unresolved direct child for a
non-direct spelling, symlink, or junction before `resolve()`, so an internal
top-level alias can no longer select another build directory. Descendant links
remain refused during traversal. The historical pack/prune receipt is not
invalidated: its selected names were unique, link-free direct children and the
archive bytes were independently verified. The previously recorded
final-check-to-delete race remains an operational limitation and is not changed
by this patch.

## Final code closure

The normalized-duplicate finding above is **resolved; the narrow archive patch
is accepted with no remaining code blocker**. `inventory()` now preserves the
pre-resolution rejection of non-direct spellings, symlinks, and junctions,
then compares each resolved direct-child `Path` against `seen_paths` before
traversal. This rejects `old` versus `old/.`; on Windows, `WindowsPath`
identity also rejects `old` versus `OLD`.

The parametrized regression covers `old`, `old/.`, and `OLD`, in addition to
the top-level alias test. I did not rerun tests in this final text-only review.
The saved `validation/archive-final-receipt.json` records the focused command,
exit code 0, and log SHA-256
`cc64e90fd2d9c2671032a8f52ada87dfa2751e4c1db264fadcb2d7f0c6b0a5af`;
the bound log reports `13 passed in 0.14s`. The earlier operational
final-check-to-delete race remains documented, but it is not a regression in
this patch or a blocker to the already completed, quiescent archive operation.
