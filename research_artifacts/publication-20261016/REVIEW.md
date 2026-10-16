# Post-Push Code Review

Date: 2026-10-16. Reviewer: fresh-context read-only code-review subagent.
Workflow: `superpowers:requesting-code-review`.

Original reviewed range:

- Base: `f5ed597b18f96fba0eae0f9ebb4fc99e5ca844df`.
- First publication: `7dac22925fa9319b61541d47f92c3b0801086001`.
- Resolution: the byte-preserving path correction committed with this report.

## Findings

### Important: Published Inspection Paths Added Audit Failures (Resolved)

The original publication README described tracked `build/` exceptions, but
`scripts/project.py:110` unconditionally flags these paths. The first commit
tracked 66 inspection files under `build/`; its base tracked none. This added
66 audit failures. Documentation alone did not establish an audit exception.

All 66 files were promoted byte-for-byte into `research_artifacts/`, preserving
their original local `build/` snapshots and all frozen manifests. Publication
links, byte-preserving attributes and the publication manifest were updated.
The reviewer verified these exact-byte renames and the relocated scope replay.
No tracked `build/` paths remain. Fresh before/after audit comparison returned
to the same 227 baseline issues, with zero added or removed issues.

No Critical finding or remaining actionable Important/Minor finding was found.

## Verified Evidence

- Reviewer replay: 68 SVE zero remainders, five nonzero negative controls and
  all numerical acceptance gates. The numerical CSV hash was reproduced.
- Reviewer scope replay: 14 zero identities and three negative controls.
- Reviewer tests: 94 selected project/active-package tests and 10 extension
  tests passed, 104 in total.
- Reviewer publication checks: all 161 included sizes/hashes matched original
  committed blobs, and all 22 excluded source copies were absent from Git.
- Correction checks: all 161 updated manifest entries matched staged blobs;
  the promoted scope replay still passed 14 identities and three controls.
- A separate validation agent exported the exact first publication commit,
  reproduced all 104 tests, both calculations and numerical gates, and checked
  all publication hashes again after running. No excluded source copy, pytest
  temporary tree or Python cache was present in that exported publication.
- Source checksums, negative receipts and scientific report contents were
  unchanged by the correction.

The publication manifest subsequently adds this report and updates the
publication README hash; those are documentation additions, not scientific
calculator changes. The manifest itself is explicitly self-excluded.

## Boundaries And Residual Risks

- The repository audit still fails with 227 baseline issues. This review does
  not claim a clean repository audit or approve unrelated dirty changes.
- Complete source-copy fidelity was not re-audited for the deliberately
  excluded third-party papers; restore the recorded versions first.
- Historical runner portability is explicitly unsupported. Use the safe
  replay commands in the publication README, not the archived runner paths.
- Fresh LaTeX compilation/page rendering was not repeated. Neither the
  manuscript nor the scientific report content changed in this correction.
- Full-range whitespace checking reports existing whitespace in one frozen
  generated SVG and two historical failure logs. Scientific Python files and
  newly written publication files pass the scoped whitespace check; frozen
  receipt bytes were preserved instead of reformatted.
- Maximal classification, general free-boundary software support, learned
  first integrals, neural superiority and global theorems are outside scope.

## Assessment

Ready to merge with the verified correction included. The original
publication-path defect is resolved; no remaining actionable defect was
found within the declared publication scope.
