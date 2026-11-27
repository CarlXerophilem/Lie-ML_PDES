<!-- Math rendering: GitHub MathJax / KaTeX compatible LaTeX. Use $...$ or standalone $$ blocks; no custom macros or injected scripts. -->

# Parameter-Dependent Lie Symmetries and Semi-Analytical Solutions of Nonlinear PDEs

Yihong Xiao · MATH 4890 · Wenzhou-Kean University

This dissertation studies Saint–Venant–Exner systems through exact symmetry reductions, reconstruction of physical fields and local regular or singular profiles. The computational experiments compare classical and learned representations on prescribed invariant families; ML is supplementary and does not improve the overall result.

| Start here | Contents |
|---|---|
| [Compact dissertation](draft/dissertation_wku_compact.pdf) | Authoritative manuscript. [LaTeX source](draft/dissertation_wku_compact.tex). |
| [Madrid defense](draft/defense_wku_madrid.pdf) | Defense slides. [LaTeX source](draft/defense_wku_madrid.tex). |
| [Delivery user manual](delivery/README.md) | End-to-end PDE-to-ODE reducer CLI (`delivery/reduce_pde.py`), log directory map, and mathematical/computational limits. |
| [Manuscript workflow](draft/README.md) | Flowcharts connecting hypotheses, evidence, figures and slides. |
| [Reproduction and verification](delivery/VERIFICATION.md) | Maintained entry points, hypothesis ledger, run logs and source checks. |
| [References](ref/README.md) | Inventory of cited literature, publisher links and the literature audit. |
| [Research path](delivery/research_path.md) | Commit chronology, past experiments, negative results and archive map. |

## Dissertation at a glance

**Goal.** Identify when a parameter-dependent symmetry can generate physically admissible reference solutions for water over a mobile bed.

**Method.** Determine point symmetries on declared charts, check orbit rank and data, reduce the PDE directly to scalar ODEs via symbolic first integrals, resolve local regular or singular branches analytically, and reconstruct the original fields. Audit the published scalar equation $P$ separately. The compatible material equation $M$ ($\mathcal E_L$) yields an exact local reconstruction of the original Eulerian model $E_1$.

**Results.** The positive $1+1$ charts admit exact local point-algebra classifications for real $m\ge1$. The manuscript proves material reconstruction of water and mobile sediment bed, constructs an exact bed-drift family for arbitrary $C^2$ flux $Q(u)$ and a convergent cubic Laurent branch, and shows that any hydraulically critical point of the separate $(2+1)$D sloping-bed annular sediment-transport model $\mathcal E_2$ admits two local analytic Briot–Bouquet crossings whenever $\det\mathbf J_*<0$. Across held-out tuples in a USACE `HEC-RAS`-motivated sediment-transport box ($m\in[1.5,3.5]$, $k=K/G\in[2,10]$, $\delta\in[1,3]$) on the smooth annulus $r\in[0.85,2.0]$, classical 1D Chebyshev collocation reconstructs water depth to $3.37\times 10^{-11}$ median error and mobile bed elevation to $2.96\times 10^{-13}$ median error in $40.7\text{ ms}$ with zero training, whereas a supplementary remainder-learning `LNN-PINN` study shows no overall advantage over Chebyshev.

**Scope.** The annular determining calculation is restricted to the stated shared affine class and open radial water/sediment throughflow. General initial–boundary value problems, site-calibrated `HEC-RAS` frictional channels, supercritical fold regimes $\delta\le 0$, and CPU-only symbolic-ML search for general closures remain open.

**Keywords.** Parameter-dependent Lie symmetries, jet bundles, invariant reduction, Saint–Venant–Exner system, material reconstruction, transcritical Briot–Bouquet branches, Laurent series, Chebyshev collocation, structure-constrained neural approximation.

## Quick start

Requires Python 3.10 or later. From a fresh clone:

```bash
python -m pip install -e .
lie-reduce --model E1 --subalgebra X1 --output build/E1.json
bash delivery/reproduce_all.sh
```

The core requires SymPy only. Installation also supports `python -m lie_reduce`
and the former `python delivery/reduce_pde.py` entry point. Use a trusted local
Python module exporting `PDESpec` to analyze your own equations. See the
[API and CLI manual](delivery/lie_reduce/README.md) for a complete example.

| Task | Entry point |
|---|---|
| Symbolic classification, quotient and first integrals | `lie-reduce --model M --strata --smooth-check --output build/M.json` |
| Reproduce the current paper's symbolic claims | `bash delivery/reproduce_all.sh` |
| Build dissertation and slides | `bash delivery/build_pdfs.sh` |
| Re-run the supplementary planar ML comparison | `bash delivery/reproduce_ml.sh` (opt-in, install `delivery/requirements-ml.txt` first) |
| Historical comparisons | [`bin/`](bin/README.md) (not part of the default replay) |
| Cited papers and DOI access | [`ref/`](ref/README.md), [DOI inventory](ref/doi_inventory.json) |

The reducer accepts exact SymPy PDE specifications on a declared chart and
returns a report of admitted generators, attempted reductions, verified
quotients, first integrals and unsolved cases. It does not guarantee that every
PDE admits an ODE quotient or closed form. Parameter search is class-bounded;
local analytic existence and physical admissibility require separate tests.
The main proof and experimental evidence are explained in
[the delivery manual](delivery/README.md) and [verification dossier](delivery/VERIFICATION.md).

## Research history

[CoT.json](.old/CoT.json) preserves selected, dated public research milestones,
commit links and an inventory of the former archive. It is not a complete
conversation transcript. Original historical files are retrievable from the
pinned pre-cleanup commit; the cleanup does not rewrite Git history.
See the [research path](delivery/research_path.md) and
[artifact audit](delivery/artifact_audit.md) for evidence and negative controls.
