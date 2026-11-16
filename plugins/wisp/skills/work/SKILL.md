---
name: work
description: >-
  Use when starting any change in a repository, or when unsure which path fits: a bug, a feature, a refactor, a check, an experiment or a release. Sizes the change as contained, shared or irreversible, states outcome, constraints and evidence bar first, picks the mode (explore, spike, fix, build, check, ship) and review depth, and asks the owner only for decisions that change scope or cannot be undone.
version: 1.0.0
---

# Wisp — Work

<capability>
One entry for all work. The primary agent is the worker: it researches, decides, implements and tests in one context, and may fork read-only searches. Independent review is spent only where a confident mistake is costly: the verifier switches on at the shared tier and above. Must-hold rules are hooks and project checks, not this text.
</capability>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/references/work/modes.md` (tiers, modes, autonomy, output), `${CLAUDE_PLUGIN_ROOT}/shared/references/work/decision-cards.md`, `${CLAUDE_PLUGIN_ROOT}/shared/references/work/verifier-brief.md`, `${CLAUDE_PLUGIN_ROOT}/shared/references/work/specs-and-plans.md`, `${CLAUDE_PLUGIN_ROOT}/shared/references/verification/evidence.md`, `${CLAUDE_PLUGIN_ROOT}/shared/references/tooling/context.md`, `${CLAUDE_PLUGIN_ROOT}/shared/references/workspace/conventions.md`, `${CLAUDE_PLUGIN_ROOT}/shared/schemas/spike-report@1.json`, `${CLAUDE_PLUGIN_ROOT}/shared/schemas/verdict@3.json`
</references>

<start>
Open the reply with `Mode: <mode>. Tier: <tier>.` and the brief: outcome, constraints, evidence bar (`modes.md`, Brief and Tiers). Read the project's invariants as `conventions.md` describes before choosing the tier. If an alias started this skill, its mode stands unless the request plainly fits another; say so if you switch.
</start>

<modes>
- **explore:** start `muse:sketch` with the request and any brief or brand constraints. A chosen option becomes work through `muse:promote`.
- **spike:** answer one question with the smallest experiment, written only under `.scratch/<id>/`, never editing source, config or lockfiles. Return a `spike-report@1` with `fidelity: spike`, and `verified` holding only what the run showed. Offer `muse:promote` if it works.
- **fix:** write a test that fails on the original defect, fix it, see the test pass, and search where the same mistake repeats. Each review finding is one claim to fix.
- **build:** work from the brief. Write a spec or plan only when `specs-and-plans.md` says one pays; for UI work where the look is undecided, `muse:sketch` shows options first.
- **check:** to confirm existing work, start the verifier with the work's brief or the artifact's criteria. To hunt defects, load the hazard pack for each language under `${CLAUDE_PLUGIN_ROOT}/shared/references/hazards/`, then send each suspected defect to the adversary; confirmed ones go to fix mode.
- **ship:** only the steps asked for, in this order: `courier:changeset` when the repository uses changesets and the change is user-visible, `courier:commit`, `courier:pr`, `courier:release`. Confirm with the owner before anything is pushed, posted or published.
</modes>

<agents>
| Agent | Tier | Start when |
| :--- | :--- | :--- |
| `recon` | haiku / low | The workspace is unfamiliar or polyglot and the check commands or entry points are not obvious. Skip it when `AGENTS.md` or the `justfile` already names them. |
| `verifier` | opus / high | Shared or irreversible work is done, or a spec or plan makes claims about code. Pass exactly the fields in `verifier-brief.md`, never your reasoning. |
| `adversary` | opus / high | One finding or claim needs settling before acting on it: a verifier blocker you dispute, a suspected bug from a hunt, or a fix whose correctness is costly to get wrong. One per finding. |
</agents>

<review>
- Contained: the evidence bar and the project's checks are the review.
- Shared: start the verifier. On fail, fix only its blockers and resubmit once with `retry_count` 1 and the prior blockers. On `escalation_required`, stop and give the owner the persistent blockers.
- Irreversible: as shared, then a decision card before the irreversible action itself.
</review>

<decisions>
Ask the owner only through a decision card (`decision-cards.md`), and only when the answer changes scope or the next action cannot be undone. Otherwise state an `Assumption:` and continue. At most three open cards. Encode every answer where the next session will find it.

When the work keeps hitting the same friction (the same area fixed again, the same finding derived twice, a guardrail that no longer fits), raise one card with two or three structurally different options instead of patching around it. Changing a guardrail or loosening a check is always a card.
</decisions>

<finish>
End with what the owner reads: the diff or render, the evidence (each command and its observed result), a `Not verified:` list, and the next step (`ship`, or the open card). Never report a claim done that you did not see pass. With uncommitted changes, the Stop hook asks once for a missing `Not verified:` line.
</finish>
