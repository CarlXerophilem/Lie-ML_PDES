<!-- Math rendering: GitHub MathJax / KaTeX compatible LaTeX. Use $...$ or standalone $$ blocks; no custom macros or injected scripts. -->

# Local smooth transcritical continuation — 1 November 2026

The [eight-page proof](pdf/local-continuation.pdf) establishes exactly two smooth local crossing germs in a derived invariant class of the full two-dimensional rotating Saint–Venant–Exner system with sediment flux `K |w|^2 w - G |w|^2 grad B`. At a positive compatible hydraulic critical point, the hypothesis is `D=N=0` and `det d(D,N)<0`. Both branches reconstruct all original Cartesian equations, including at the critical radius.

The solution profile is not prescribed upfront. The chain is **original PDE → shared affine determining equations → returned generators → derived invariants → reduced currents/ODE → continuation proof → independent Cartesian reconstruction**. The determining result is complete only in its declared parameter-independent affine class. The smooth-manifold argument is classical and credited to Teschl.

| Read or replay | Artifact |
|---|---|
| Theorem and proof | [PDF](pdf/local-continuation.pdf), [English LaTeX and TikZ](document/local-continuation.tex) |
| Hypotheses and excluded strata | [Assumptions](ASSUMPTIONS.md), [claim ledger](CLAIMS.json) |
| Source checks and proof review | [Source audit](SOURCE_AUDIT.md), [versions/URLs/hashes](SOURCE_AUDIT.json), [reasoning review](REVIEW.md) |
| Computation | [Determining solver](src/determine_shared_affine.py), [invariants](src/derive_invariants.py), [reduction](src/replay_reduction.py), [independent checker](src/check_cartesian.py) |
| Validation | [Recorded results and limitations](VALIDATION.md), [publication integrity](PUBLICATION_VALIDATION.json) |
| Complete authored evidence | [215-file carrier](theorem-evidence.zip), [hash receipt](ARCHIVE_RECEIPT.json), [selection](SELECTION.json) |
| Next milestone | [Regular-IVP ML approximation, continuous certificate and 2D reconstruction](NEXT_STEPS.md) |

The dimensionless family `g=K=G=f=C1=C2=1`, `C3=c/2-15/16`, `c<-77/12` gives an exact compatible saddle at `(r,H)=(1,1)`. This establishes continuous parameter coverage for the stated example, not a sampling-based inference.

Fresh symbolic replay and Cartesian verification passed; the recorded focused regression suite had 66 passes. The native TeX build has no final warnings and all eight pages were visually inspected. One pre-existing project-audit failure remains recorded. These checks do not replace the mathematical proof.

## Reproduce

The four current scripts and serial native runner are directly available. On Linux with Python 3.12+ and SymPy 1.14.0, run from the repository root into fresh outputs:

```bash
python -B delivery/annular-transcritical-theorem-20261101/replay.py \
  --out build/transcritical-replay-NEW \
  --campaign build/transcritical-campaign-NEW \
  --prefix audit
```

Use a fresh campaign only for a newly scheduled audit; reuse the existing campaign when continuing work within its budget. The driver executes serially and enforces the recorded limits. It copies only source programs, then generates each dependency afresh. It requires neither downloaded literature nor prior answers.

For the original ZIP and its restore commands, use the [versioned publication](https://github.com/CarlXerophilem/Lie-ML_PDES/tree/c48d9994e4bfaf69a91913c73a59e7ef8f1e1bf7/research_artifacts/annular-transcritical-theorem-20261101). The publication's manifest and receipts describe that snapshot. The 23 November 2026 replay is recorded in the [repository audit log](../logs/repository_audit.txt). For the general symbolic Cartesian/polar reducer CLI (`python delivery/reduce_pde.py --model delivery/lie_reduce/models.py:planar_e2_spec --subalgebra "X5 ; X1 + alpha_1*X4" --output delivery/logs/reduce_E2.json`), logs, and pipeline boundaries, see the [`@delivery` user manual](../README.md).

The restored note is under `build/transcritical-snapshot-NEW/build/annular-transcritical-theorem-20261101/`. Its `replay-reviewed/` directory is the authoritative executed chain. Earlier runs, failed serialization, negative cases and source versions remain preserved. The archive's `ARCHIVE_MANIFEST.json` governs the public selection; the nested original manifest documents the larger local package.

Nine scholarly-source bodies (PDFs, extracted text and raw alphaXiv page responses) remain local, following the earlier review publication policy. Their versions, locators, hashes and source URLs are included. Teschl and Berthon exact-title alphaXiv queries returned no match; their original texts were checked directly. This source audit covers the three citations of this note, not every dissertation reference.

The theorem concerns the derived invariant class, not arbitrary 2D initial/boundary data. The local interval is qualitative. Unrestricted classification, other singular strata, global connections, numerical error bounds, empirical calibration and literature priority remain open. ML is required in the next solver milestone and was not run here. The existing dissertation remains unchanged by this publication.
