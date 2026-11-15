---
name: gate-spec
description: >-
  Use this, not a freehand verdict, whenever a spec must be judged ready before planning: "gate this spec", "is this spec ready?", "check this spec before we plan it". Default disposition is fail. Checks the spec on its own terms and returns a verdict@3 with blockers specific enough for scribe/draft-spec to act on.
version: 2.1.0
---

# Scribe — Gate Spec

<overview>
The binding exit gate for a spec entering planning. Delegates to `exit-gate`. On pass, this skill — not the agent — performs the disk-write orchestration below; that step is load-bearing, not decoration. On a retry, pass the gate `retry_count` and the previous round's blockers so it applies the round rules. An `owner_decision` blocker, raised for an `Open decision:` line in `scope`, goes to the user, not to `scribe/draft-spec`: it is a choice only the owner can make. A stated `Assumption:` line is not a blocker.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **exit-gate** | opus / high | A self-checked spec@1 needs a terminal binding pass/fail verdict before planning. It may follow the draft directly; `scribe/verify-spec`, `scribe/audit-spec` and `scribe/audit-architecture` come first only on request, or when the spec is shared or crosses a module boundary. |
</dispatch>

<orchestration>
After `exit-gate` returns a pass verdict, THE SKILL SHALL, before handing off to `navigator`:
1. Write the spec@1 JSON to `<workspace_root>/docs/specs/<id>.json`. Create the directory if it does not exist.
2. Commit the file to version control. An uncommitted spec file is invisible to a fresh checkout, a future session, and `scribe/spec-drift` — it exists only in the current working tree.
3. Set `spec_file_path` to the workspace-relative path (e.g. `docs/specs/SPEC-001.json`) in the spec@1 object.
4. Pass the updated spec@1 — with `spec_file_path` set — to `navigator`.

Without `spec_file_path` set, downstream agents fall back to reading the spec from conversation context, which is lossy under compression and cannot be independently verified.

**2-Round Circuit Breaker**: the gate gets two rounds. An optional drafter ↔ auditor loop (via `scribe/draft-spec` and `scribe/audit-spec`) is capped at 2 iterations before it. On round 2, unresolved debates about internal helper names or line citations are demoted to non-blocking `api_notes` rather than looping further.
</orchestration>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/spec@1.json`, `${CLAUDE_PLUGIN_ROOT}/shared/schemas/verdict@3.json`
</references>

<io>
**Consumes**: `spec@1` (optionally after verify-spec, audit-spec, audit-architecture)
**Produces**: `verdict@3`. On pass, a persisted `spec@1` with `spec_file_path` set, routed to `navigator`. On fail, blockers routed back to `scribe/draft-spec`, and `owner_decision` blockers to the user.
</io>
