# LieML — Semi-Analytical & Machine-Learning Methods for Solving PDEs via Lie Symmetry Analysis

Course project "math 4890". Two linked theses live here:

- **CCS-SYM+ (main thesis).** A four-stage pipeline: **REDUCE** a PDE by Lie (or nonclassical/approximate BGI) symmetry to a low-dim ODE → **CLOSE** it with a homotopy-analysis (HAM) series → **CERTIFY** with a theorem-backed three-part convergence+error certificate on the *reduced* equation (headline novelty: operationalizing the Turkyilmazoglu ratio + a computable a-posteriori bound; the deliberately VACUOUS-on-Fisher branch is a feature) → **CORRECT** with a small symmetry-invariant CPU PINN. Validated only against closed-form exact similarity solutions (McGreivy–Hakim-compliant).
- **SAC-NO (companion sub-thesis).** Equivariance **by COORDINATES**: a neural operator on the orbit-quotient (Lie-invariant coords), so the documented loss-penalty "no training signal at symmetric points" pathology is *structurally* absent. See `symm/sacno/SACNO_PLAN.txt`.

## Layout
- `plan.txt` — full phased plan (PART I plan, PART II verified feasibility, PART III infra).
- `intro.tex`/`intro.pdf` — beginner conceptual map. `poster.tex`/`poster.pdf`. `applicability_report.md`.
- `symm/` — verified demos: `feasibility_demo.py`, `fisher_kpp_reduction.py` (PRIMARY: jet/prolongation engine + Fisher HAM in the bounded variable s=e^{z/√6}), `pinn_corrector_demo.py` (321-param PINN), `bgi_probe.py`, `ml_pde_solver_demo.py`. Orchestration: `wf_*.js`.
- `symm/sacno/` — SAC-NO probes (`sacno_equivariance_probe.py`, `sacno_parametric_operator.py`, `sacno_curriculum_warmstart.py`) + `SACNO_PLAN.txt`. All reproduce on this CPU.
- `symm/bench/` — `BUILD_PLAN.md`: a measurement/benchmark harness, fully specified but **not yet built**.
- `ref/` + `pdf2md/output/` — paper corpus (PDFs) + Markdown conversions (run via the `run-pdf-extractor` skill).

## Environment / how to run
- **System Python 3.14.2**: torch 2.12.0+cpu (CPU only), sympy 1.14, numpy 2.3.5, scipy 1.17.1. `pdflatex` via MiKTeX.
- This folder is **NOT a git repo**. Windows; use Bash or PowerShell.
- Run a demo: `python symm/<file>.py`. Build a doc: `pdflatex intro.tex`.

## Conventions (match the existing work)
- **Falsifiable gates + honesty.** Every numeric claim must be reproduced by a runnable script; report negatives (vacuous bounds, non-reproducing claims, ill-conditioned directions) plainly — never inflate. A correctly-labeled negative counts as a pass.
- **Deliver as files.** Verify the math yourself rather than asserting it.
- The author is a **near-beginner** in Lie/PDE theory — explain from first principles with concrete examples.

## Pointers
- Persistent auto-memory: `C:\Users\Administrator\.claude\projects\D--MATHs-math-4890-LieML\memory\MEMORY.md`.
- Cross-project knowledge base and global preferences: see `D:\MATHs\kb` and `~/.claude/CLAUDE.md`.
