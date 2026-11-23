# Parameter-Dependent Lie Symmetries and Semi-Analytical Solutions of Nonlinear PDEs

Yihong Xiao · MATH 4890 · Wenzhou-Kean University

This dissertation studies Saint–Venant–Exner systems through exact symmetry reductions, reconstruction of physical fields and local regular or singular profiles. The computational experiments compare classical and learned representations on prescribed invariant families.

| Start here | Contents |
|---|---|
| [Compact dissertation](draft/dissertation_wku_compact.pdf) | Authoritative manuscript. [LaTeX source](draft/dissertation_wku_compact.tex). |
| [Madrid defense](draft/defense_wku_madrid.pdf) | Defense slides. [LaTeX source](draft/defense_wku_madrid.tex). |
| [Manuscript workflow](draft/README.md) | Flowcharts connecting hypotheses, evidence, figures and slides. |
| [Reproduction and verification](delivery/VERIFICATION.md) | Maintained entry points, hypothesis ledger, run logs and source checks. |
| [References](ref/README.md) | Flat inventory of cited literature, publisher links and the literature audit. |
| [Research path](delivery/research_path.md) | Commit chronology, past experiments, negative results and archive map. |

## Dissertation at a glance

**Goal.** Identify when a parameter-dependent symmetry can generate physically admissible reference solutions for water over a mobile bed.

**Method.** Determine point symmetries on declared charts, check orbit rank and data, solve the reduced equation on a regular or singular branch, and reconstruct the original fields. Audit the published scalar equation \(P\) separately. The compatible material equation \(M\) yields a local reconstruction of the original Eulerian model \(E_1\).

**Results.** The positive \(1+1\) charts admit exact local point-algebra classifications for real \(m\ge1\). The manuscript proves material reconstruction, constructs an exact travelling wave and a convergent cubic Laurent branch, and shows that a compatible saddle of the separate annular model has two local analytic crossings. On the controlled profiles, Chebyshev gives smaller sampled field errors than the learning models.

**Scope.** The annular determining calculation is restricted to the stated shared affine class. The rotating exchange demonstration uses a depth-averaged \(2+1\) model on a solid-swirl family. The \(P\)–\(M\) comparison and continuation, general planar classification, and equal-accuracy correction cost remain open.

**Keywords.** Parameter-dependent Lie symmetries, jet bundles, invariant reduction, Saint–Venant–Exner system, material reconstruction, singular branches, Laurent series, structure-constrained neural approximation.

## Active delivery

- [Symbolic Eulerian classification](delivery/symbolic_sv2022.py), [scalar and material certificates](delivery/symbolic_sve2026.py), and [planar fixtures](delivery/symbolic_new_model2026.py).
- [Published scalar reproduction](delivery/reproduce_sve2026.py) with an equation audit and symbolic series.
- [Eulerian](delivery/ml_sv2022.py), [scalar and material](delivery/ml_sve2026.py), and [rotating exchange](delivery/ml_new_model2026.py) numerical comparisons.
- [Annular theorem and replay](delivery/annular-transcritical-theorem-20261101/README.md) and [historical evidence disposition](delivery/artifact_audit.md).

The [audit archive](.old/2026-11-23-repository-audit/) preserves the former documentation, research artifacts and implementation paths. Use the compact dissertation for current claims and the archive for version-specific evidence.
