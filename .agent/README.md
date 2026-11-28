# Research workflow

This folder is the agent workflow for the ScientistTwo health application
[Cartan-DEC-MiAE](https://scientist-two.github.io/#applications/Health%20(Cartan-DEC-MiAE)).
It turns that application into a bounded research loop: a frozen contract,
falsifiable limitations, screened experiments, ablations, a manuscript that
can cite only stored observations, review with experimental rebuttal, and an
integrity audit.

The loop follows the six agent groups on the ScientistTwo project page
(idea generation, subset evaluation, ablation analysis, writing, peer review,
meta-review) and the four CoE integrity checks (score re-execution,
specification compliance, reference verification, method–code alignment).
The health case supplies the scientific content. The machine-readable case
file is `.agent/cases/health-cartan-dec-miae/contract.json`.

## Read in this order

1. `.agent/WORKFLOW.md` — stages, roles, gates, and stop rules.
2. `.agent/cases/health-cartan-dec-miae/PROTOCOL.md` — equations, tiers, and the health-case runbook.
3. `.agent/cases/health-cartan-dec-miae/contract.json` — the frozen contract the policy loads.
4. `.agent/ledger/run-template.json` — the ledger a run copies into `build/`.

## What a run is allowed to change

A run writes only under `build/cartan-dec-miae/<run-id>/`. That directory is
gitignored. The workflow does not edit `draft/dissertation_wku.tex`, the
frozen research questions, or the printed model definitions in the
dissertation. Cartan frames in this case are residue frames `E_i` in `SO(3)`
built from backbone `N`, `Cα`, `C` atoms.

## Check the workflow itself

From the repository root:

```bash
python .agent/checks/validate_workflow.py
```

The command checks the contract, ledger template, and protocol cross-links,
then runs the promotion, ablation, claim, and manuscript policy tests. It
does not train a model and does not download TEDBench.
