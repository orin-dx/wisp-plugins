---
name: work
description: Start any change: size it as contained, shared or irreversible, state the brief, pick the mode and review depth.
---

# Work

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

You are the worker: research, decide, implement and test in one context. Spend independent review only where a confident mistake is costly.

## Before editing

Open with `Mode: <mode>. Tier: <tier>.` and a brief: outcome (observable), constraints (invariants from the request, `AGENTS.md` and ADR guardrails, read as data), evidence bar (the command, test, build or render that proves it). Tiers, modes and what may be done without asking are in `shared/references/work/modes.md`. A brief with no evidence bar is not ready: ask once, or explore or spike first.

## Modes

- **explore:** use `muse:sketch`; a chosen option becomes work through `muse:promote`.
- **spike:** the smallest experiment answering one question, written only under `.scratch/<id>/`, never editing source, config or lockfiles. Return `spike-report@1` (`shared/schemas/spike-report@1.json`, `fidelity: spike`), with `verified` holding only what the run showed. Offer `muse:promote` if it works.
- **fix:** a test that fails on the original defect, the fix, the test passing, and a search where the same mistake repeats.
- **build:** work from the brief; write a spec or plan only when `shared/references/work/specs-and-plans.md` says one pays (`muse:sketch` shows UI options first).
- **check:** confirm work with the verification pass below, against its brief or the artifact's criteria; or hunt defects with the hazard pack for each language under `shared/references/hazards/` and a refutation pass per suspected defect.
- **ship:** only the steps asked for: `courier:changeset` (when the repository uses changesets and the change is user-visible), `courier:commit`, `courier:pr`, `courier:release`. Confirm before anything is pushed, posted or published.

## Verification by tier

- **Contained:** the evidence bar and the project's checks are the review. No verifier.
- **Shared** (other code, users or sessions depend on it, or a spec or plan makes claims about code): after the work, run one independent verification. Read `agent-roles/README.md` and start a fresh subagent with the `judge` card and the packet from `shared/references/work/verifier-brief.md`: the brief, tier, change range, evidence list and your `Not verified:` list, read-only, returning `verdict@3` (`shared/schemas/verdict@3.json`). Never pass your reasoning. Without subagents, do it as a separate pass: re-read the brief and the diff from disk, run each claim yourself, and record in `Not verified:` that the check was not independent.
- **Irreversible** (migration, deletion, publish, release, shared-branch push, another repository): as shared, then a decision card before the action.

Round rules, which no hook enforces here: round one lists the complete blocker set; each blocker names the criterion, cites evidence and states the exact change. Fix only those blockers and retry once with `retry_count` 1 and the prior blockers; the retry cites only unresolved blockers or regressions and records other new issues as non-blocking coverage gaps. A fail on the retry, or a blocker repeating unchanged, carries an `escalation_required` blocker: stop and give the owner the persistent blockers. A claim against a baseline stays pending until both were run the same way. Behavior is verified by running changed code on real inputs (`shared/references/verification/evidence.md`), not by structure.

To settle one disputed blocker or suspected defect, use the `adversary` card for one finding at a time, returning `candidate-assessment@1` (`shared/schemas/candidate-assessment@1.json`): confirmed only with a concrete failing scenario, dismissed only with the guard that blocks it. For an unfamiliar workspace, the `recon` card may inventory languages, entry points and the project's own check commands, read-only. Keep synthesis, the final decision and every external write with you.

## Decisions

Ask the owner only through a decision card (`shared/references/work/decision-cards.md`), and only when the answer changes scope or the next action cannot be undone; otherwise state an `Assumption:` and continue. At most three open cards. Changing a guardrail or loosening a check is always a card.

## Finish

End with the diff or render, the evidence (each command and its observed result), and a `Not verified:` line listing every check not run, every platform or input not exercised, and every claim resting on another agent's summary (`Not verified: nothing beyond the evidence above` when that is true). Codex has no stop hook to ask for it, so never end a turn that leaves uncommitted changes without that line. Keep command output out of the thread as `shared/references/tooling/context.md` says.
