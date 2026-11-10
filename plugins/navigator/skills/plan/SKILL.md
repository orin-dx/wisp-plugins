---
name: plan
description: >-
  Trigger when the user asks to plan, break down, or sequence the implementation of a spec ("write a plan for X", "break this down into tasks", "plan this out"), or when a spec@1 exists and implementation is next. Also covers estimating or challenging an existing plan. Produces a plan@1 of executable tasks linked to acceptance criteria.
version: 1.5.0
---

# Navigator Planning Skill

<overview>
Navigator decomposes a spec@1 into a sequenced, bite-sized plan@1 that a developer or agent can execute without deciding what to build, where, or what proves it. Every task states its outcome, files, signatures, and proving tests, and carries implementation code only where the logic is non-obvious or a wrong shape would be costly. Every task is independently testable.
</overview>

---

<behavior>

navigator is one skill, `plan`. Behavior adapts to what's asked, dispatching to whichever agent below fits the request — there is no separate `navigator/estimate` or `navigator/challenge` skill to invoke; estimating and challenging both happen inside this one skill.

- **Decompose a spec** — `planner` creates ordered, subsystem-batched tasks.
  - Read and propagate persisted spec metadata.
  - In amend mode, change only tasks tied to corrected criteria.

- **Estimate an existing plan** — `estimator` assigns effort estimates (in minutes) to each task in a plan@1, identifies parallelizable tasks, and surfaces blocking dependencies.

- **Challenge a draft plan** — `challenger` checks coverage, order, specificity (outcome, signatures, tests, command; no full bodies for routine code), batch size, error handling, and shared-interface siblings. It loads `shared/references/verification/interface-coverage.md` when a contract or implementation changes. Amended plans receive the same review.

</behavior>

---

<subagent_dispatch_matrix>

| Agent | Role | Model / Effort | Delegate When |
| :--- | :--- | :--- | :--- |
| **planner** | Plan author | sonnet / medium | Decompose a spec into ordered, subsystem-batched implementation tasks. |
| **estimator** | Effort estimator | sonnet / medium | Assign time estimates, identify parallelizable tasks, and surface blocking dependencies. |
| **challenger** | Adversarial reviewer | sonnet / medium | Stress-test a draft plan@1 (max 2 review rounds) before any implementation begins. |

</subagent_dispatch_matrix>

---

<artifact_contracts>

**Consumes**: `spec@1` (or its `spec_file_path`, read from disk when set)
**Produces**: `plan@1` — carries `spec_file_path`, `spec_hash`, and `linked_requirement` propagated from the source spec

</artifact_contracts>

---

<orchestration>
After `challenger` returns an overall `pass` verdict, THE SKILL SHALL, before handing off to `smith`:
1. Write the plan@1 JSON to `<workspace_root>/docs/projects/<linked_spec>.json`. Create the directory if it does not exist.
2. Commit the file to version control. An uncommitted plan file is invisible to a fresh checkout and a future session, the same way an uncommitted spec is invisible to `scribe/spec-drift`.
3. Set `plan_file_path` to the workspace-relative path (e.g. `docs/projects/SPEC-001.json`) in the plan@1 object.
4. Pass the updated plan@1 — with `plan_file_path` set — to `smith`.

An amended plan (planner's amend mode, following a spec correction) overwrites the file at the same `plan_file_path` and commits the change — the path does not change across an amendment, mirroring `scribe/correct-spec`'s rule for corrected specs. The amended plan still passes through `challenger` before this write, per the Spec Correction Loop.

Without `plan_file_path` set, `weaver/audit-backlog` and other downstream agents fall back to treating plan coverage as unverifiable for that requirement, the same graceful-degradation posture as an unset `spec_file_path`.
</orchestration>

---

<implementation_requirement>

Test steps are not required to precede implementation steps within a task. Smith's mutation-testing gate — not step order — is what verifies a test would actually catch a wrong implementation; a controlled comparison found no quality advantage from write-test-first ordering for agent-written code, at several times the token cost, and found it suppressed upfront design work agents otherwise did well ([Böckeler, "TDD inside the agent loop"](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html)).

A task with no test proving a covers_criteria criterion violates this requirement — the criterion has no evidence, regardless of write order. Plan code is optional and, where present, a baseline; see [ADR-009](../../../../docs/adr/009-implementer-shape-latitude.md) for the implementer's latitude and [ADR-014](../../../../docs/adr/014-outcome-level-plans.md) for when a plan carries code.

</implementation_requirement>
