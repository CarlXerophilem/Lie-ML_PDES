# Orchestrating Multi-Agent Research Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and behaviorally validate a resource-aware personal Codex skill for evidence-led multi-agent research with independent review.

**Architecture:** A concise `SKILL.md` performs routing and enforces workflow invariants. Three focused references provide the durable ledger schema, role briefs, and pinned prior-art evidence without loading all details on every invocation. Behavioral validation compares five fresh-context runs against the already-recorded no-skill baseline.

**Tech Stack:** Markdown Agent Skill, YAML UI metadata, bundled Python skill initializer and validator, Codex multi-agent tools.

**Spec:** `docs/superpowers/specs/2026-10-05-orchestrating-multi-agent-research-skill-design.md`

## Global Constraints

- Install at `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research`.
- Keep automatic invocation enabled.
- Use only `SKILL.md`, `agents/openai.yaml`, and three focused reference files.
- Do not add scripts, dependencies, examples, or unrelated configuration.
- Preserve authorization boundaries and require explicit approval for external mutations.
- Never claim token, KV-cache, CPU, or cost savings without corresponding telemetry.
- Do not edit the LieML engine or `intro.tex` while building this skill.
- The project and skill directories are not treated as a Git repository; do not invent commit steps.

## Review Focus

- Four total slots: the workflow reserves a fresh reviewer rather than occupying every child slot with researchers.
- Hidden KV telemetry: the workflow labels provider cache behavior unknown instead of inferring hits from short prompts.
- CPU-only experiments: multiple research agents do not launch competing unbounded numerical jobs.
- Conflicting sources: reconciliation uses evidence and qualifiers rather than majority vote.
- Unattended mode: the workflow proceeds within scope but stops at real authorization or hard-budget boundaries.

---

### Task 1: Record the RED baseline

**Files:**
- Modify: `docs/superpowers/specs/2026-10-05-orchestrating-multi-agent-research-skill-design.md`

**Interfaces:**
- Consumes: five isolated no-skill responses to the frozen LieML pressure scenario.
- Produces: baseline failure counts and representative wording in specification section 10.

- [x] **Step 1: Run five fresh-context samples without the new skill**

Use `fork_turns: "none"`, a low-cost model, no file access, no edits, and the identical 30-minute LieML scenario.

- [x] **Step 2: Score observable behavior**

Score reviewer reservation, ledger state, DAG representation, token/KV distinction, CPU scheduling, permissions, autonomy, provenance, self-approval prevention, and release gating.

- [x] **Step 3: Verify the expected failure is present**

Expected RED signal: all five samples use the available child slots for research and none schedules a genuinely fresh reviewer or complete resource-aware ledger.

### Task 2: Initialize and write the minimal skill package

**Files:**
- Create: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\SKILL.md`
- Create: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\agents\openai.yaml`
- Create: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\references\research-ledger.md`
- Create: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\references\role-briefs.md`
- Create: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\references\prior-art.md`

**Interfaces:**
- Consumes: specification sections 1-9 and baseline failures in section 10.
- Produces: `$orchestrating-multi-agent-research`, its UI metadata, and selectively loaded operational references.

- [x] **Step 1: Initialize the package**

Run:

```powershell
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\init_skill.py orchestrating-multi-agent-research --path C:\Users\Administrator\.codex\skills --resources references --interface 'display_name=Orchestrating Multi-Agent Research' --interface 'short_description=Evidence-led research with independent agent review' --interface 'default_prompt=Use $orchestrating-multi-agent-research to coordinate this research task with bounded resources and fresh-context review.'
```

Expected: the skill directory, starter `SKILL.md`, `agents/openai.yaml`, and empty `references` directory exist.

- [x] **Step 2: Replace the scaffold with the routing contract**

Write a concise `SKILL.md` whose description starts with “Use when”, whose core principle is role separation plus shared evidence, and whose algorithm explicitly reserves a reviewer, distinguishes Lite Goal from Full Automatic, and links each reference only at its point of use.

- [x] **Step 3: Add exact reference contracts**

Write the ledger fields and state transitions in `research-ledger.md`; copy-ready Supervisor, Researcher, Reviewer, and Writer output contracts in `role-briefs.md`; and the five pinned repositories with their scope limits in `prior-art.md`.

- [x] **Step 4: Check package scope**

Run:

```powershell
Get-ChildItem -Recurse C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research | Select-Object FullName
```

Expected: exactly the five specified files plus their containing directories; no scripts or placeholder examples.

### Task 3: Run structural validation

**Files:**
- Test: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\SKILL.md`
- Test: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\agents\openai.yaml`
- Test: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\references\*.md`

**Interfaces:**
- Consumes: the complete skill package from Task 2.
- Produces: validator, YAML, link, placeholder, and file-count evidence.

- [x] **Step 1: Run the bundled validator**

```powershell
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research
```

Expected: `Skill is valid!` and exit code 0.

- [x] **Step 2: Parse UI metadata and inspect invocation policy**

```powershell
python -c "from pathlib import Path; import yaml; p=Path(r'C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\agents\openai.yaml'); d=yaml.safe_load(p.read_text()); assert d['interface']['default_prompt'].startswith('Use $orchestrating-multi-agent-research'); assert d.get('policy', {}).get('allow_implicit_invocation', True) is True; print('OPENAI_YAML_OK')"
```

Expected: `OPENAI_YAML_OK`.

- [x] **Step 3: Scan placeholders and relative links**

```powershell
rg -n 'TODO|TBD|\[TODO:' C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research
```

Expected: no matches. Independently resolve every Markdown target under `references/` and require every target to exist.

- [x] **Step 4: Check entrypoint size**

```powershell
(Get-Content -Raw C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\SKILL.md | Measure-Object -Word).Words
```

Expected: the entrypoint is concise enough for frequent loading; conditional schemas remain in references.

### Task 4: Run GREEN behavior tests

**Files:**
- Test: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\SKILL.md`
- Test: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\references\*.md`

**Interfaces:**
- Consumes: the exact baseline LieML scenario and the installed skill.
- Produces: five isolated responses scored against all ten acceptance criteria.

- [x] **Step 1: Run five fresh-context samples with the skill**

Each prompt says only: `Use $orchestrating-multi-agent-research at <absolute path> to answer this scenario`, followed by the unchanged baseline scenario. The prompt does not reveal expected findings or prior failures.

- [x] **Step 2: Read and score every response manually**

Require all ten criteria from specification section 12. Do not use keyword counts as substitutes for reading the decision sequence.

- [x] **Step 3: Compare with the no-guidance control**

Expected GREEN signal: `5/5` reserve a fresh review stage, use a recoverable ledger, distinguish KV concepts and telemetry limits, bound CPU work, and retain automatic progress and permission discipline.

### Task 5: Refactor, revalidate, and obtain independent review

**Files:**
- Modify if required: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\SKILL.md`
- Modify if required: `C:\Users\Administrator\.codex\skills\orchestrating-multi-agent-research\references\*.md`

**Interfaces:**
- Consumes: structural results and all GREEN responses.
- Produces: the final package and an independent finding report.

- [x] **Step 1: Correct only observed failures**

If any GREEN sample misses a criterion, amend the smallest relevant instruction or schema. Do not add rules for hypothetical failures.

- [x] **Step 2: Re-run the affected five-sample variant**

Use a fresh context for every repetition and require convergence on the intended workflow shape.

- [x] **Step 3: Re-run every structural check from Task 3**

Expected: validator, YAML parse, placeholder scan, link resolution, and file inventory all pass after the last edit.

- [x] **Step 4: Dispatch one independent final reviewer**

Give the reviewer the specification and final package, but not the intended verdict. Require findings ordered by severity for trigger scope, permission drift, resource claims, role independence, progressive disclosure, and unsupported source claims.

- [x] **Step 5: Report deployment state without committing**

Report exact files, test counts, failures or residual risks, repository provenance, and the explicit negative result that the attached image's exact publication source remains unidentified.
