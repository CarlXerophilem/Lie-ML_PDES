# Closed research loop

Every case under `.agent/cases/` is a contract plus a protocol. The supervisor
owns the contract and the ledger. Specialists append evidence. A reviewer
sees the frozen contract and the observation ledger, and does not see the
specialists' private reasoning. The writer may use a claim only after the
ledger records an observation id for every number in that claim.

```text
S0 contract
  -> S1 limitations
  -> S2 ideation
  -> S3 subset screening
  -> S4 full grid and one evolution round
  -> S5 component ablations
  -> S6 manuscript from observations
  -> S7 review and experimental rebuttal
  -> S8 meta-review
  -> S9 integrity audit
```

A completed stage is reloaded from its ledger artifact. The supervisor does
not rerun it to "improve" a number. A failed gate stops the run with the
ledger status `blocked` and a reason code from `.agent/policy.py`.

## Roles

| Role | Reads | Writes | Cannot do |
| --- | --- | --- | --- |
| Supervisor | contract, ledger | stage state, rulings | approve its own measurement |
| Idea generator | contract, limitations | idea records | edit evaluation, masking, probe, or data code |
| Evaluator | ideas, budget | `metrics.json` observations | promote from prose |
| Analyzer | selected idea, ablation list | one-factor runs | change two factors in one run |
| Writer | accepted claims | manuscript draft | introduce a number without an observation id |
| Reviewer | contract, observations, draft | review scores, experiment requests | clear a results objection by text alone |
| Rebuttal | review requests, budget | supplementary runs | answer a results objection without a new run |
| Meta-reviewer | reviews, integrity preconditions | accept, revise, or reject | lower the contract threshold |
| Auditor | sealed artifacts and commands | four audit checks | treat model text as a measured score |

The supervisor reserves a reviewer pass before any accept decision. Filling
every worker slot with idea or experiment roles, and skipping review, is a
broken run.

## Stage gates

S0. Hash `contract.json`. Choose one tier from the contract (`quote`, `smoke`,
or `paper`). Record `compute_authorization`. The default authorization is
`smoke-only`. The `paper` tier stays a quotation protocol until the ledger
records an explicit full-corpus authorization.

S1. Every limitation names the mechanism it concerns and a test that points
at one declared endpoint. A limitation without a test is dropped.

S2. Every idea names the limitation ids it targets, the single change it
makes, the risk that would falsify it, and a command template. An idea that
predicts a paper-tier number as its smoke outcome is rejected at this gate.

S3. Run only the subset budget. Read the primary metric from `metrics.json`.
Call `promote` in `.agent/policy.py`. One seed moving the wrong way rejects
the idea. The smoke primary metric is integrated reconstruction error.
Probe accuracy on the synthetic families is recorded and is not a promotion
metric.

S4. Promote at most the contract's `top_ideas`. Run the full smoke budget on
the survivors. Allow one evolved idea whose change is the composition of two
surviving mechanisms. Select by the primary metric.

S5. Remove one declared component at a time. Keep the selected command
otherwise fixed. `ablation_status` returns `clean` only when at least
three quarters of the ablations degrade the primary metric by the contract's
minimum relative drop. Anything short of that is `partial`, and the
manuscript says so.

S6. Draft from accepted and qualified claims. `unbacked_numbers` must return
an empty list. Quotation claims carry quote-tier observation ids. Measurement
claims carry observations from the same tier as the run.

S7. The reviewer scores the draft against the contract. A results objection
produces a supplementary experiment id. The rebuttal role runs that
experiment inside the remaining review budget. A wording edit leaves the
objection open.

S8. Accept when the review score meets `review_threshold` and S5 status is
recorded. Otherwise revise once, or reject. A second failure rejects the run.
The threshold is not edited inside the run.

S9. Run the four integrity checks. `pass` requires a re-executed score check,
no protected-path edits, every cited reference resolved, and a method section
that names the same losses, masks, and integration path as the command.
Skipping re-execution records `partial` and blocks accept.

## Ledger

Copy `.agent/ledger/run-template.json` to
`build/cartan-dec-miae/<run-id>/ledger.json` at S0. Status values are
`queued`, `running`, `evidence-ready`, `blocked`, `failed`, `review`,
`accepted`, `qualified`, and `rejected`. A claim records its statement,
kind (`measurement`, `quotation`, or `mechanism`), tier, and observation ids.
The policy functions are the only promotion and admission rules.

## Stop rules

Stop, record the reason, and leave the ledger blocked when any of these hold:

- the next action would edit the dissertation sources named in the contract firewall;
- the next action would edit a protected evaluation file;
- a `paper`-tier training command is reached under `smoke-only` authorization;
- the primary metric file is missing, non-numeric, or produced by a command
  different from the idea command;
- a mechanism claim depends on an open reading that the run has not resolved
  with a new observation;
- two heavy training commands would run at the same time on one CPU machine.

A timeout, a missing dataset, and a metric that fails to clear the gain are
completed negative results. They stay in the ledger.
