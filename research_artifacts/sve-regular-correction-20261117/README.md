# Regular correction prototype — review source import

These three existing workspace scripts are imported unchanged on 17 November 2026 to resolve the implementation filenames in Chapter 5 of `draft/dissertation_wku.tex`. This import does not reproduce a training run or establish the provenance of historical numerical results.

- `sve_basis.py`: physical reference, symbolic audit, reference data and discrete correction.
- `sve_baseline.py`: shared baseline training/evaluation engine; imports `sve_basis`.
- `sve_architecture.py`: reference-plus-remainder architecture; imports `sve_baseline`.

Python >=3.10; dependencies: NumPy, SciPy, SymPy, threadpoolctl; PyTorch >=2.2 for the baseline/architecture. Run commands from this directory so sibling imports resolve. Only Python syntax was checked for this import; dependencies were not freshly installed and training/evaluation was not run.

The scripts implement a restricted smooth positive Eulerian family with g=1 and m=1, parameters (c,p0,kappa,beta,epsilon). This is one prototype within the multi-parameter research programme, not the definition of the full dissertation model family. A discrete Newton–Krylov correction is not a continuous PDE error certificate. Refer to each module's docstring for assumptions and CLI examples. Do not start training as part of review.
