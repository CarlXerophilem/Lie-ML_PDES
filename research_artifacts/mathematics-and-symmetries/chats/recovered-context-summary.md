# Retrieved project-context summary

**This is a retrieved summary, not a verbatim chat export.** Message dates and
historical assistant claims are useful for navigation but require their original
artifacts for verification. Relative-age annotations are retained from retrieval.
Only project-related material is included.

[convo search]
- [USER_FACT] [c0] U@2026-09-21T13:42:45Z, +15d: project-specific session “Visualize ShallowWater Simulation” (2026-09-21); requested Manim/Python visualization of SVE shallow-water equations.
- [PRIOR_ASSISTANT_OUTPUT] [c0] A@2026-09-21T13:57:03Z, +15d: created `sve-python-manim.zip`, `sve-manim.mp4`, `sve-space-time.png`; flat-bed \(\beta=0\), Lie reduction, exact/numerical solution, Lagrange mapping; verified residuals, mass conservation, mesh convergence, 0.84% error.
- [PRIOR_ASSISTANT_OUTPUT] [c0] A@2026-09-24T05:34:45Z, +12d: updated `canal-flow.html` with Exner erosion/deposition, Grass transport, adjustable porosity/coefficient, implicit geometry `y=0 && f(x,y)=0`; 53 mm erosion/72 mm deposition reported, balances near floating-point precision.

- [USER_CONSTRAINT] [c1] U@2026-10-06T03:42:28Z, -8h: benchmark SVE PDE families with PINNs, methods, Lie-parameter subgroups, unexpected Lie-PINN results; require symbolic/training/classical timing, visualization, limits, and beyond Lie-point analysis.
- [PRIOR_ASSISTANT_OUTPUT] [c1] A@2026-10-06T04:14:29Z, -8h: `sve_liepinn_benchmark.zip`, `RESEARCH_REPORT.md`, `baseline_section.tex`; 108 neural runs, symbolic audits 0.033–0.245s, classical solves 0.015–0.018s, no matched-accuracy PINN speedup; verified Lie loss equals residual weighting with 39% less optimizer compute; smooth periodic Grass SVE only, excluding shocks/dry beds.
- [PRIOR_ASSISTANT_OUTPUT] [c1] A@2026-10-06T04:14:29Z, -8h: benchmark scripts include subgroup verification, numerical references, vanilla/Lie-PINN and architecture controls, conservation exploration, checkpoints, metrics, plots/GIF; scalar manuscript equation has separate verification.

- [USER_FACT] [c2] U@2026-09-08T02:32:05Z, -28d: project repo: https://github.com/CarlXerophilem/Lie-ML_PDES; related repos include SolveIterativeFunctions, math_structur, prime_loop_verification.
- [USER_CONSTRAINT] [c2] U@2026-09-09T02:23:44Z, -27d: proposal direction accepted around Paliathanasis–Leon–Leach SVE; wants Lie symmetry first, with verified reduction/error bounds and ML secondary.
- [PRIOR_ASSISTANT_OUTPUT] [c2] A@2026-09-12T04:24:05Z, -24d: proposal.tex target: computable finite-time error bound guaranteeing positive depth, with velocity/bed-elevation error bounds; neural remainder later; DeepSeek link inaccessible and no additional sessions recovered.

- [USER_CONSTRAINT] [c3] U@2026-09-10T09:25:55Z, -26d: `proposal.tex` must be 4–6 pages, Times New Roman 12pt, double-spaced; cover problem, objectives, methodology, outcomes, references.
- [USER_PREFERENCE] [c3] U@2026-09-08T01:33:59Z, -28d: analysis-first 2D nonlinear shallow-water/Saint–Venant–Exner PDE; manually reduce via Lie symmetry to 1D before ML; explore self-similarity/fractional symmetry and connected PDE/Lie-algebra graphs.
- [PRIOR_ASSISTANT_OUTPUT] [c3] A@2026-09-10T09:31:47Z, -26d: recovered artifacts: `proposal.tex`, `proposal.pdf`; six-page skeleton, analysis-first scope, objectives/methodology/neural evaluation/expected outcomes/timeline, with unresolved comments.

- [USER_CONSTRAINT] [c4] U@2026-09-14T15:51:55Z, -22d: Export project “mathematics and symmetries”; preserve exact project chats/files, not unrelated chats.
- [USER_FACT] [c4] U@2026-09-14T15:51:55Z, -22d: Project centers on SVE near \(m=3\), Lie reduction to ODEs, analytical/neural correction, \(S_i(\varepsilon)\), approximate symmetry, certified residuals; repo https://github.com/CarlXerophilem/Lie-ML_PDES.
- [PRIOR_ASSISTANT_OUTPUT] [c4] A@2026-09-20T17:44:26Z, -16d: Recovered outputs: `proposal.tex`/PDF, `draft.tex`/PDF, `main.tex`; `intro.tex`/PDF earlier. Main draft includes \(m=3\) reduction, TikZ diagrams, neural construction/loss/comparisons; proposal revised to six pages. Source links: sandbox `/workspace/scratch/b5f8c61d654b/output/`.

- [USER_FACT] [c5] U@2026-09-10T12:01:46Z, -26d: project brainstorming covers Hopf–Lie/PDE reduction, Saint–Venant neighbors, proposal revisions, symbolic hierarchy, neural correction, and verification.
- [PRIOR_ASSISTANT_OUTPUT] [c5] A@2026-09-11T14:35:03Z, -25d: updated `proposal.tex` and `sve_worked_example.md`; proposal uses SVE benchmark family, time-varying drag, Taylor-plus-neural remainder, reference PDFs/citations, sensitivity and verification outcomes. Created `lie_pde_brainstorming_summary.md`.
- [PRIOR_ASSISTANT_OUTPUT] [c5] A@2026-09-11T16:46:36Z, -25d: proposed core result is conditional reconstructed-SVE error bound from continuous residual, uniform Lipschitz control, common existence interval, and positive-depth bounds; originality not yet established.

- [PRIOR_ASSISTANT_OUTPUT] [c7] A@2026-09-06T16:15:24Z, -30d: Project decision: use steady 2D Prandtl/Blasius as secondary realistic benchmark; preserve Fisher–KPP primary exact benchmark and Burgers regression; later Falkner–Skan, then Navier–Stokes.
- [PRIOR_ASSISTANT_OUTPUT] [c7] A@2026-09-06T16:28:46Z, -30d: Unfinished work: implement generic (p=2,q=2,r=2) primitive-system validation, scalar stream-function prototype, HAM/PINN correction comparisons, branch-aware Falkner–Skan tests, independent certificates; no repository files modified.
- [PRIOR_ASSISTANT_OUTPUT] [c7] A@2026-09-07T02:06:06Z, -29d: Recoverable technical content: Blasius reduction \(f'''+\tfrac12ff''=0\), BCs \(f(0)=f'(0)=0,f'(\infty)=1\), target \(f''(0)\approx0.3320573362\); proposed PINN learns correction to finite HAM series from residual/BC loss, not labeled solution values.

Additional recovered topics: basic 2+1D SWE discussion (2026-10-05) and ML-free analyzer / KAN review (2026-10-06). These may be continuations of the benchmark session; their native session identities and full turns were not exposed. The latter outputs are present under `code/lie_kan_workflow/`.
