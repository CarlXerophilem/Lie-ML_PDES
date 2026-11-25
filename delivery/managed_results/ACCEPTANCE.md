# Managed solver acceptance

Current branch: `codex/final`; observed remote head and manuscript baseline: `b9842d6`. The compact manuscript and its tables are unchanged.

- 30 tests passed (11 independent-manager tests and 19 existing Lie-pipeline tests).
- 131 emitted reductions passed independent paper-PDE pullback checks; 29 exclusions remain exclusions.
- Independent characteristic prolongation passed for E1 at m=2, P at m=1 and M at m=3. These are sufficiency checks, not unrestricted classification proofs.
- All 20 task/method combinations completed. Each neural run used only 20 Adam steps; all 36 independent endpoint/midpoint derivative probes passed.
- N1 and N2 implicit analytic solutions passed the independent symbolic verifier without ML.
- Candidate construction took 25.49 wall seconds in aggregate; separate verification took 32.14 seconds. Peak process RSS was 386.7 MiB, cumulative across methods.

[Sampled results](ode/1795628927577810852/STATISTICS.md), [machine-readable receipt](ACCEPTANCE.json), [test and symbolic replay log](final_checks.log).

The five methods are Taylor, nonlinear Chebyshev collocation, PINN, the one-input LNN architecture and a series-prefix neural remainder. The table is an interface pilot, not a matched-accuracy benchmark. Neural residuals and derivative probes are sampled evidence; no continuous neural error bound is asserted. The N3 table reports both remainder q and physical H differences to expose small-domain scaling.

Mathematica/Maple feature parity is not established. General smooth determining-system completion, multivariate parameter CAD, a planar optimal system and arbitrary symbolic ODE integration are outside this acceptance. Reviewed equation transcriptions are required; the verifier does not infer mathematical meaning from arbitrary paper prose.
