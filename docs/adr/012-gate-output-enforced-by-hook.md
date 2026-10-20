# ADR-012: Gate output conformance and the retry cap are enforced by a hook, not a prompt

**Status:** Accepted
**Date:** 2026-10-20

## Context

Every exit gate returns a `verdict@3` and is told to stop retrying after three attempts and hand the decision to a human. Both rules lived only in prompts. In the two audited projects, 12 of 45 recorded verdicts broke the schema (all 12 by a `verdict_summary` over 300 characters), and eight specs passed their gate with `retry_count` between 4 and 9. The `muse` gate was also told to emit a verdict value that no schema allows. A rule that matters in every run, and can be checked by a program, should not depend on a model remembering it.

Claude Code 2.1.271 and later deliver a subagent's report in auto mode through the `SubagentHandback` tool. A `PreToolUse` hook on that tool sees the report in `tool_input.message` and can deny it with a reason the subagent reads, so the subagent can correct and hand back again. The platform checks were recorded in `docs/verified-facts.md`.

## Decision

Ship one stdlib-only hook, `shared/hooks/validate-handback.py`, and register it in the five plugins that own an exit gate (`muse`, `scribe`, `smith`, `sentinel`, `ranger`) through `hooks/hooks.json`.

- It acts only for the exit-gate agent types in its routing table and lets every other subagent through.
- It validates the report against `verdict@3`, including the conditional blocker rules.
- It denies a non-conforming report with the first errors, up to three times per subagent; the fourth report passes to the orchestrator, which owns human escalation.
- It enforces the retry cap in the report: a `retry_count` above 3 is accepted only as a `fail` with a blocker whose criterion is `escalation_required`.
- It fails open: an internal error never blocks a subagent.
- `WISP_HANDBACK_TRACE` appends one line per inspected report, for evaluation.

The prompts keep stating the rules, so harnesses without the hook still get the instruction. The hook is the enforcement where the host supports it.

## Options considered

- **Keep the rules in prompts.** Rejected: the recorded violations show it does not hold.
- **Validate in the orchestrator skill.** Rejected: the orchestrator is the model that skipped the rule, and it cannot make the subagent correct its own output in place.
- **A workflow script that owns the retry loop.** Deferred to WP-603; it can replace the cap check later, but the schema check is useful either way.
- **Third-party JSON Schema library.** Rejected: hooks run on user machines with no install step. The validator implements only the keywords the verdict schemas use, and a test covers each.

## Consequences

Gate conformance is checked on every run in Claude Code auto mode, and the retry cap can no longer be passed silently. Limits: the hook covers only the Claude Code host, only auto mode and only local, non-fork subagents; a hook failure or timeout does not block (`onFailure: "block"` needs Claude Code 2.1.295, and the local CLI is 2.1.292); plugin hooks fire for every subagent, so the routing table is the scope. Codex and Antigravity have no equivalent yet. A new gate agent needs a routing entry and a test. The validator supports a subset of JSON Schema, so a schema that adds keywords needs the validator extended in the same change. A live run on 2026-10-20 showed the hook denying twice and accepting the corrected third report from `muse:exit-gate`.
