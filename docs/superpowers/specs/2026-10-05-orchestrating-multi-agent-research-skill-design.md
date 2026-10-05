# Orchestrating Multi-Agent Research Skill Design

Status: approved for autonomous implementation
Date: 2026-10-05
Approved direction: option 3, a layered research orchestrator. The user selected
this option, authorized Lite Goal and full-automatic progression, allowed
read-only use of strong GitHub repositories, and delegated the remaining design
decisions on 2026-10-05.

## 1. Purpose

Create a personal Codex skill named `orchestrating-multi-agent-research` for
research tasks that benefit from role separation, shared evidence, and an
independent review context. The skill turns multi-agent work into a controlled
research process rather than several agents independently answering the same
question.

The reusable intuition is:

> The controller owns the question and resources; researchers produce evidence;
> a fresh-context reviewer attacks load-bearing claims; the writer releases only
> what survived review; the human retains authority and final responsibility.

The attached Chinese diagram is design input, not an executable instruction or
an identified publication. Its exact blog or paper source was not established
by the bounded search, so the skill must not attribute the design to a named
source without later verification.

## 2. Activation and non-goals

Use the skill when a task has at least two separable research domains, material
evidence or computation requirements, and a meaningful benefit from independent
review. Typical triggers include literature-plus-experiment work, mathematical
research, architecture studies, competitive analyses, and publishable reports.

Do not activate it merely because subagents exist. Prefer one agent when the
task is small, tightly sequential, dominated by one shared mutable state, or
cheaper to complete than to brief and review. The skill does not replace domain
skills, grant external side-effect permission, prove mathematical correctness,
or make all research autonomous.

## 3. Modes

### 3.1 Lite Goal

Lite Goal is selected when the user explicitly requests a goal or when the task
is one bounded research claim with a cheap verification path. It uses a minimal
ledger, one or two researchers, one fresh reviewer, and controller-written
synthesis. A persistent goal tool is created only when the user explicitly
requests goal tracking. No token budget is invented; an explicit user budget is
the only hard token cap.

### 3.2 Full Automatic

Full Automatic proceeds without routine check-ins after scope and permissions
are known:

`freeze -> decompose -> research -> reconcile -> fresh review -> repair or
downgrade -> write -> release check -> report`.

Unattended Full Automatic requires an authorized writable ledger. Without one,
the run downgrades to a bounded non-resumable pass that returns partial evidence
and does not start work whose safe completion depends on recovery.

It stops only for an irreversible or destructive action, a security-sensitive
action, an external mutation that requires consent, an explicit hard budget,
a requested pause, or a defect that makes every continuation path guesswork.
Ambiguities below that threshold receive a recorded controller ruling.

## 4. Roles and slot-aware scheduling

The root agent is always Supervisor/Screener. It freezes the research question,
builds the task DAG, assigns budgets, owns the ledger, reconciles conflicts, and
makes bounded rulings. It does not consume a child slot.

Researchers receive one independent evidence domain each. Their output contract
requires claim-level evidence, exact provenance, negative results, computation
receipts, uncertainties, and a concise handoff. They do not approve their own
claims or write the final release.

The Fresh-context Reviewer receives the frozen question, acceptance criteria,
and the normalized evidence package, but not persuasive summaries or the
researcher's private chain of reasoning. It attacks load-bearing claims,
reproduction, missing branches, unsupported novelty, provenance, and boundary
conditions. A controller cannot substitute its own rereading for this role.

The Writer/Release Checker uses only accepted or explicitly qualified ledger
claims. It checks scope language, citations, reproducibility links, negative
results, artifact construction, and required release commands. In a four-slot
environment the role is usually executed by the controller after the reviewer
slot returns; role separation is semantic and staged, not a demand for four
simultaneous child agents.

The scheduler reserves capacity for review. It must not fill all child slots
with researchers if doing so prevents a fresh review within the deadline.

## 5. Workflow algorithm

1. Freeze a one-sentence objective, deliverables, authorization boundary,
   success tests, and explicit non-claims.
2. Estimate coordination cost. Use one agent if delegation plus review is not
   expected to improve coverage, latency, or independence.
3. Build a DAG whose nodes declare dependencies, evidence target, tools,
   context-pack path, token policy, CPU class, timeout, outputs, and stop rule.
4. Partition only independent nodes. Serialize shared-state edits and competing
   CPU-heavy jobs.
5. Dispatch minimal, path-based briefs with isolated context. Keep a stable
   common prefix and a short role-specific suffix when the runtime can benefit
   from prefix caching.
6. Normalize returns into the shared ledger. Missing evidence is a status, not
   prose to be smoothed over.
7. Reconcile contradictions without voting. Prefer primary evidence, replayable
   computation, and narrower claims.
8. Dispatch a fresh reviewer on the normalized package. Route material findings
   to a bounded repair loop. A materially changed claim or evidence package gets
   a new revision and must be reviewed again; if time expires, retain an already
   reviewed narrower claim or reject it.
9. Construct the deliverable from accepted and qualified claims only.
10. Run release checks and report evidence, costs, negative results, rulings,
    residual risks, and uncompleted work.

## 6. Shared research ledger

The ledger is the durable recovery boundary. Todos may mirror it but may not
replace it. Each run records:

- run ID, mode, objective, deliverables, permissions, deadline, and hard caps;
- task nodes with state `queued`, `running`, `evidence-ready`, `blocked`,
  `failed`, `review`, `accepted`, `qualified`, or `rejected`, plus typed
  dependencies that distinguish evidence readiness from claim approval;
- claims with stable IDs, exact statement, evidence IDs, confidence label,
  branch/domain assumptions, author, reviewer verdict, and downstream uses;
- sources with URL or local path, title, author/publisher, accessed date,
  version or commit, license when code is involved, and verification status;
- computations with command, working directory, inputs/hashes, environment,
  timeout, exit code, relevant output, and artifact paths;
- negative results and failed searches without converting absence of evidence
  into evidence of absence;
- review findings, repairs, controller rulings, and the cost if a ruling is
  wrong;
- resource observations and estimates, clearly distinguished.

Detailed field templates belong in `references/research-ledger.md`; role prompt
contracts belong in `references/role-briefs.md`.

## 7. Resource policy

### 7.1 Tokens and context

Use isolated child contexts and minimal context packs. Prefer references to
stable files over pasted transcripts. Require bounded structured returns and
deduplicate evidence before review. Record actual token counts only when the
runtime exposes them; otherwise label estimates as estimates.

### 7.2 KV cache

The skill distinguishes two different concepts:

- provider prompt/prefix caching, whose hits and billing may be hidden;
- inference-time key/value memory, which generally grows with active context.

Stable prefixes and shorter contexts are reasonable optimizations, not proof of
cache hits or savings. The skill must not claim control of provider cache
eviction, exact cache reuse, or saved cost without runtime telemetry.

### 7.3 CPU and memory

Text research can be parallel while CPU-heavy local computations are governed
by named resource leases. On CPU-only machines, default to one heavy job at a
time unless measurements justify more. Every computation receives a timeout,
thread/process cap where supported, memory-aware input bound, and an explicit
termination rule. A timeout or unavailable backend is a valid negative result.

### 7.4 Cost-aware adaptation

At each fan-out boundary the Supervisor compares expected coverage/latency gain
with briefing, context, and review cost. It may merge tasks, serialize them,
switch to Lite Goal, or stop low-value branches. Review independence is not the
first item sacrificed; reduce researcher count before deleting the reviewer.

## 8. External repositories and literature

Repository activity and stars are discovery signals, never correctness proof.
Record an exact commit and license, read authoritative documentation and tests,
and seek a paper or independent implementation for load-bearing algorithms.
Default access is read-only. Forking, issues, PRs, pushes, and publication are
external mutations and retain their normal authorization gates.

Read-only architecture references inspected on 2026-10-05:

- `langchain-ai/open_deep_research`, commit
  `1b7d2e80db9faa586165c60e09096dbbfd483a64`, MIT: separate research,
  compression, and final-report models; publishes token/cost benchmark data.
- `assafelovic/gpt-researcher`, commit
  `0957c301ed06c2a5857b834358c7227c739041d4`, Apache-2.0: planner,
  execution agents, source tracking, and publisher aggregation.
- `SamuelSchmidgall/AgentLaboratory`, commit
  `d9017d90e329112d2a80b7712f37ee9094d2cd27`, MIT: staged literature,
  experimentation, and report-writing workflow with compute-resource input.
- `SakanaAI/AI-Scientist-v2`, commit
  `96bd51617cfdbb494a9fc283af00fe090edfae48`, license metadata not asserted:
  bounded worker/step/debug parameters and distinct writeup/review models.
- `microsoft/autogen`, commit
  `027ecf0a379bcc1d09956d46d12d44a3ad9cee14`: orchestration reference only;
  the repository declares maintenance mode and points new users elsewhere.

These projects inform completeness checks; none is copied into the skill, and
none establishes the mathematical validity of the proposed workflow.

## 9. Failure and status semantics

Use explicit outcomes: `verified`, `qualified`, `conflicted`, `unsupported`,
`backend-unavailable`, `timeout`, `budget-exhausted`, `permission-required`,
and `not-checked`. A writer may include qualified claims with their qualifier.
It may not promote the other states to verified.

An agent failure is not automatically retried. Retry once only when the failure
is plausibly transient and the remaining budget supports both the retry and
review. Repeated failure is ledgered and the branch is narrowed or stopped.

## 10. Baseline test and required behavioral change

Five fresh-context baseline samples received the same time-pressured LieML
scenario without this skill. All five respected the project design gate and
proposed bounded evidence gathering. The common failure was architectural:

- `5/5` assigned all three child slots to research tasks;
- `0/5` reserved a genuinely fresh reviewer;
- `0/5` defined a recoverable claim/task/resource ledger state machine;
- `0/5` cleanly separated provider prefix-cache telemetry from inference-time
  KV memory and from ordinary token accounting;
- `0/5` staged an independent Writer/Release Checker.

Representative baseline wording included “allocate the three non-controller
slots to the saved independent tasks” and “reconcile agent reports” in the
controller. The skill must change these observable decisions without weakening
the already-correct evidence and permission discipline.

## 11. Skill package

Create only:

```text
C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\
|-- SKILL.md
|-- agents\openai.yaml
`-- references\
    |-- research-ledger.md
    |-- role-briefs.md
    `-- prior-art.md
```

No executable script is justified. `SKILL.md` holds routing, invariants, the
algorithm, resource rules, and links. References hold schemas, role contracts,
and pinned external evidence. Automatic invocation remains enabled.

## 12. Acceptance tests

The same LieML scenario is run in at least five fresh contexts with the skill.
Every passing sample must:

1. reserve or schedule an independent reviewer instead of spending all slots on
   researchers;
2. define a durable evidence/claim ledger and explicit states;
3. use a DAG or equivalent dependency-aware algorithm representation;
4. distinguish measured token data, estimates, provider prefix caching, and
   inference-time KV memory;
5. serialize or lease CPU-heavy jobs under CPU-only constraints;
6. preserve negative results and authorization boundaries;
7. continue automatically within scope without routine check-ins;
8. treat GitHub as implementation evidence with commit/license provenance, not
   mathematical proof;
9. prevent researchers from approving their own claims;
10. finish with a writer/release gate using only accepted or qualified claims.

Run the bundled `quick_validate.py`, parse `openai.yaml`, scan for placeholders,
verify every relative link, and obtain one independent final review. Because the
project and personal skill directory are not a shared Git repository, record
the artifacts without a commit or push.
