---
name: component
description: >-
  Use this, not a freehand spec, whenever a UI component's behavior is specified, audited or checked for readiness: "spec this component", "write a spec for this design", "is this component spec ready?", "gate this component spec". Drafts, audits and gates a spec@1 covering props, variants, per-state behavior and accessibility.
version: 1.0.0
---

# Muse — Component Spec Skill

<overview>
Turns UI or design intent into a component spec a developer could implement — including its accessibility behavior — without asking a single clarifying question. One skill, one draft-then-gate pipeline, reused unchanged regardless of which component is being specified. Muse audits the spec, not the implementation; code-level accessibility scanning of the built component is not yet covered by `ranger`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **drafter** | sonnet / medium | A requirement@1 (or design intent) needs a first spec@1 draft covering props, variants, states, and accessibility criteria. |
| **auditor** | sonnet / medium | Only when the user asks for an audit: adversarial review for missing states, missing accessibility criteria, or unmarked invalid prop combinations. |
| **exit-gate** | opus / high | A drafted, self-checked spec@1 needs a terminal binding pass/fail verdict before it proceeds to `navigator` for planning. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/spec@1.json`, `${CLAUDE_PLUGIN_ROOT}/shared/schemas/verdict@3.json`
</references>

<io>
**Consumes**: `requirement@1`, or free-text design intent describing the component
**Produces**: `spec@1` (persisted to disk only after `exit-gate` passes) and, on failure, a `verdict@3` with blockers routed back to `drafter`. On pass, route the persisted `spec@1` — with `spec_file_path` set — to `navigator`.
</io>

<circuit_breaker>
The drafter self-checks, then the exit gate judges; the auditor does not run in between unless asked, because it reviews the same draft the gate does. The gate gets two rounds. If the second round still fails, or a blocker repeats, stop and give the user a decision: the persistent blockers and the options. On a retry, pass the gate `retry_count` and the previous round's blockers so it applies the round rules.
</circuit_breaker>
