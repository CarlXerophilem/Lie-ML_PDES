# Managed PDE and ODE workflow

The mandatory boundary is `verifier(solver_output, paper_txt_respective)`, exposed
by **lie_pde_reducer.py** and implemented independently in
**independent_verifier.py**. The checker imports no reduction engine, ODE solver,
NumPy, SciPy or PyTorch. A neutral restricted expression parser transports
expressions without `eval`. Training receives neither the checker nor reference
solutions. AST isolation tests enforce these import boundaries.

The paper-text argument is a reviewed JSON equation transcription with an actual
manuscript excerpt and anchor. Arbitrary PDF prose/LaTeX is **not** silently
interpreted or marked verified. `paper_contracts/` stores independent PDE
transcriptions; the checker differentiates their graph substitutions afresh.
The polar E2 contract explicitly checks the polar PDE, not an independent proof
of Cartesian-to-polar coordinate equivalence. Source hashes identify the snapshot.

## Three stages

Create the isolated environment once, from the repository root:

```sh
python -m venv build/nonlinear-env
build/nonlinear-env/bin/python -m pip install -r delivery/requirements-managed.txt
```

```sh
# 1. Pure SymPy PDE analysis, independent pullback checks and task export.
build/nonlinear-env/bin/python -B delivery/lie_pde_reducer.py --all-models
build/nonlinear-env/bin/python -B delivery/lie_pde_reducer.py --discover --model M --exponent 3 --degree 2 --out delivery/managed_results/discovery_M3.json
build/nonlinear-env/bin/python -B delivery/lie_pde_reducer.py --export-tasks --out delivery/managed_results/tasks.json

# 2. All five candidate methods: short integration test, NOT the thesis benchmark.
build/nonlinear-env/bin/python -B delivery/spinn_ode_solver.py --all-tasks --method all --degree 8 --steps 20 --cpu-seconds 3

# Optional analytic route: no neural training, mandatory symbolic verification.
build/nonlinear-env/bin/python -B delivery/spinn_ode_solver.py --task N1 --method analytic
build/nonlinear-env/bin/python -B delivery/spinn_ode_solver.py --task N2 --method analytic

# 3. Post-solve references, 1025-point diagnostics and tables.
build/nonlinear-env/bin/python -B delivery/managed_statistics.py --run <printed-run-directory>
```

The maintained `symbolic_sv2022.py`, `symbolic_sve2026.py` and
`symbolic_new_model2026.py` remain frozen/replay evidence. New model selection is
managed by `lie_pde_reducer.py`; model PDE definitions live under `lie_reduce/`.
All new ODE methods are selected through `spinn_ode_solver.py`. Records preserve
method settings, coefficients or weights, termination, resource cost and
independent verification. Output directories are unique per run.
Each numerical run freezes its task export as `TASKS.json`; statistics use this
snapshot by default. Numerical method records include CPU, RAM, library versions
and process costs. Symbolic commands write a matching `.resources.json` sidecar.
Peak RSS is cumulative for the process, not an isolated method allocation.

## Actual implemented methods

| Selection | Recipe | Termination / evidence |
|---|---|---|
| `taylor` | Exact rational/algebraic recurrence for regular scalar and supported BB polynomial numerators | Requested truncation degree; every recurrence coefficient checked |
| `chebyshev` | Lobatto differentiation matrix, analytic residual Jacobian, damped Newton, hard trace row | Residual tolerance, failed line search/Jacobian or iteration budget |
| `pinn` | 1D tanh MLP, four hidden layers of width 64, differential residual plus soft trace | Adam, fixed step/CPU budget; 12,673 parameters |
| `lnn` | Same trunk plus four liquid residual blocks, free width-64 alpha initialized at 0.5 | Adam, fixed budget; 29,569 parameters |
| `prefix` | Third-degree exact prefix plus s^4 times the same MLP; Picard/BB integral-defect loss | 16-node training quadrature; independent 16/32/64 sensitivity diagnostics |
| `analytic` | Autonomous first-order quadrature; SymPy `dsolve` fallback for nonautonomous scalar IVPs | Implicit equation, exact differentiated check and nonzero trace Jacobian |

LNN architecture provenance: the Drift–Decay implementation in
https://github.com/Uderwood-TZ/LNN-PINN-A-Unified-Physics-Only-Training-Framework-with-Liquid-Residual-Blocks
at commit `c7fbea453cd320b567160f188e93ee5c92cc1b8f`. Input dimension is changed from
two to one; there are four width-64 alpha vectors, not bounded scalar gates.
This is not the historical 66-parameter adapted gated cell, which stays untouched.

Default training limits are 8,000 Adam steps and 150 CPU seconds per run, seed 27,
128 residual coordinates and float64 CPU execution. The pilot command explicitly
overrides those limits. The managed-training ledger caps aggregate CPU at 7,200
seconds and reserves 120 seconds for earlier work; this conservative reservation
is not a reconstructed timing audit of every historical run. All termination
records remain `fixed_budget_approximation`, never “converged”. No default
multi-seed campaign or new manuscript result is implied by a smoke test.

## Verification meaning

- PDE records: independent invariant-surface and original-PDE pullback identities,
  conditional on chart, rank and nonzero weights. This does not re-prove the full
  determining-system classification or global reduction completeness.
- `--discover` computes the finite polynomial class for E1, P or M. A second,
  independent characteristic-prolongation implementation checks every emitted
  generator against the original paper equation and its principal Jacobian.
  This check proves sufficiency on the stated regular chart, not independence
  or completeness of the supplied list. Empty lists and model mismatches fail.
  E2 discovery reports `unsupported_scope`; its selected two-generator reduction
  is supported separately, under the existing shared affine classification.
- Exact analytic candidates: equation and trace identities plus regular implicit
  trace condition. Analytic output never requires an ML detour.
- Taylor/Chebyshev: independent symbolic derivative and rational/algebraic residual
  composition. A finite approximation usually has nonzero residual; that is
  reported as `approximation`, not an exact solution or failed solver.
- Neural candidates: independent symbolic layer derivative rules and high-precision
  probes at both endpoints and the midpoint, cross-checked against recorded torch derivatives. This is not a symbolic
  identity claiming that the neural residual vanishes, and gives no continuous
  neural error bound.
- Classical solve/verification stages are bounded; timeouts and unsupported cases
  produce explicit records. The checker itself has a 30-second time limit.
- N2 currently retains the small local interface interval [0,1/64]. N3 uses the
  selected certified saddle and scaled q variable. These pilots do not complete
  the earlier proposed near-fold scans, matched-accuracy costs or multi-seed study.

## Mathematica / Maple target

Commercial-system parity is **not established**. This delivery implements a
specific, testable subset: vector jets, finite point-class discovery, declared
catalogue reductions, checked regularization/fixed loci, first integrals,
autonomous quadrature, local series, and the five approximation recipes above.
It does not provide arbitrary nonlinear PDE classification, a general Janet/CAD
engine, every special-function DSolve case, a computed planar optimal system or
a formal interval proof for neural networks. Claiming their full functionality
without a shared conformance corpus and measured runs would be unsupported.

Regression command:

```sh
build/nonlinear-env/bin/python -B delivery/test_managed_pipeline.py
```

To independently recheck every emitted catalogue ODE (not just the six short
examples), use:

```sh
build/nonlinear-env/bin/python -B delivery/lie_pde_reducer.py --verify-catalogue delivery/lie_reduce/results/pipeline.json --out delivery/managed_results/catalogue_verification.json
```

The observed run checks 131 emitted local reductions; the 29 excluded/no-graph
records are explicitly not treated as verified ODEs. The six-example run also
checks the four-balance E2 polar quotient. The manager refuses stale paper
transcriptions when the compact manuscript hash or excerpt changes. The external
Mathematica/Maple executables were not available in this environment; commercial
feature-parity acceptance remains open.
