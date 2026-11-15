# ADR-012: Gate output conformance and the retry cap are enforced by a hook, not a prompt

**Status:** Accepted; the retry cap is amended to one retry by ADR-015
**Date:** 2026-10-20

## Decision

Ship one stdlib-only hook, `shared/hooks/validate-handback.py`, registered through `hooks/hooks.json` in the five plugins that own an exit gate (`muse`, `scribe`, `smith`, `sentinel`, `ranger`).

- It acts only for the exit-gate agent types in its routing table, and validates the report against `verdict@3`, including the conditional blocker rules.
- It denies a non-conforming report with the first errors, up to three times per subagent; the fourth passes to the orchestrator, which owns human escalation.
- It enforces the retry cap: a `retry_count` above 3 is accepted only as a `fail` with an `escalation_required` blocker.
- It fails open: an internal error never blocks a subagent. `WISP_HANDBACK_TRACE` logs each inspected report.

Prompts keep stating the rules for harnesses without the hook.

## Why

A rule that matters in every run and can be checked by a program should not depend on a model remembering it. The schema and the retry cap lived only in prompts, and audited runs broke both. In Claude Code auto mode a subagent's report arrives through `SubagentHandback`; a `PreToolUse` hook sees it in `tool_input.message` and can deny it with a reason the subagent reads, so it corrects its output in place (`docs/verified-facts.md`).

## Rejected

- **Keep the rules in prompts:** the recorded violations show it does not hold.
- **Validate in the orchestrator skill:** the orchestrator is the model that skipped the rule, and it cannot make the subagent correct itself in place.
- **A workflow script that owns the retry loop:** deferred to WP-603; the schema check is useful either way.
- **A third-party JSON Schema library:** hooks run on user machines with no install step, so the validator implements only the keywords the verdict schemas use, each covered by a test.

## Consequences

The cap cannot pass silently. Limits: Claude Code only, auto mode only, local non-fork subagents only; a hook failure does not block, because `onFailure: "block"` needs Claude Code 2.1.295; Codex and Antigravity have no equivalent. A new gate agent needs a routing entry, and a schema that adds keywords needs the validator extended in the same change.

Revisit when `onFailure: "block"` is available on every supported host (fail closed), or Codex or Antigravity gain an equivalent hook.

**Enforced by:** `tests/test_handback_validator.py` (validator, and every exit-gate agent routed with its plugin registering the hook).

**Evidence:** `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "ADR evidence", ADR 012.
