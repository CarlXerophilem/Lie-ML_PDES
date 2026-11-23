# Repository Cleanup And Priestess Handoff

**Goal:** Retire at least 1,000 historical tracked paths, limit default core
search to 500 files, preserve research evidence, and publish a reproducible
GitHub/Priestess handoff without rewriting history.

**Architecture:** Explicit-file ZIP archives preserve original paths and SHA-256
hashes. Restore is non-overwriting. Runtime sources, frozen releases, canonical
references, current experiments and manuscript inputs retain their paths.

**Tech Stack:** Python standard library, Git/LFS, pytest, native Windows LaTeX.

## Execution

- [x] Capture baseline, user-file hashes and existing audit failures.
- [x] Implement and test explicit-file archive pack/verify/restore.
- [x] Archive eight approved historical trees and four root artifacts.
- [x] Package only the 401 durable precision evidence files.
- [x] Remove verified test scratch; retain linked staging under the ruling below.
- [x] Simplify navigation/search; deliver dissertation outline and handoff.
- [x] Run integrity, regression, workflow, archive and LaTeX checks; review.
- [ ] Commit explicit paths, publish astra and verify Priestess synchronization.

## Constraints

Do not stage, move or edit the 15 pre-existing dirty/untracked items. Never
rewrite Git history, replace frozen ZIPs, prune LieSymm/_snapshot, alter the
reference corpus or remove build/week-4 manuscript inputs. Historical missing
archives and unrelated test failures are recorded, not silently repaired.

## Rulings

- Work in the existing astra checkout: this cleanup explicitly includes its
  ignored generated files and must preserve its dirty user work. A fresh
  worktree would omit these inputs and create another duplicate tree.
- Precision evidence is selected from the existing 398-file manifest plus
  three manifest files, not from the complete directory containing test copies.
- Compilation remains on Windows. Priestess receives research code, evidence,
  environment receipts and an outline-only writing task; no remote TeX install.
- The staging preservation preflight found junction aliases and a nested
  repository's pre-existing deletions. Retain that staging tree in place and
  exclude it from publication instead of moving or pruning uncertain state.
- Two original INSPECTION.md files remain byte-identical at their old paths:
  the frozen 16 October publication links directly to them. This retains
  compatibility without editing a frozen report or hiding a link regression.

## Evidence

Execution receipts are written to build/repo-cleanup-20261021 and published in
a separate carrier after review. No computational failure is erased by retiring
its expanded directory. Source baseline: 11fe2a8042a468405fa1b60056114ae826e34c59.
