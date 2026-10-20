# ADR-011: Exploration modes are non-binding and enter the pipeline only through promote

**Status:** Accepted
**Date:** 2026-10-20

## Context

Every path through the plugins is gated: recon, a spec that may not contain a TBD, a binding exit gate, a plan, a challenger, then implementation with mutation, review and a second exit gate. That fits a contract many things depend on. It does not fit an idea nobody has seen yet.

Two real projects (the Orin DX and Techworx sites, September and October 2026) showed the cost. Eight component specs took 51 gate calls in under an hour, every one failed its first gate, and the retry cap of 3 was not enforced. The specs described behavior well and appearance not at all, so the owner asked for drawings and rewrote the gated specs the next day. On 14 October the owner asked for two phases, exploring quickly first and adding specs and tests once ideas narrow, and the audit machinery was stopped by hand; the landing, Tools and Principles pages then took about 30 minutes. Design ideation ran almost entirely outside the plugins: forks and general-purpose agents spent about 24.8 million subagent tokens, more than all the gates together, and decisions were lost between sessions. The plugin skills were also almost never invoked (7 Skill calls in 812 transcripts), so agents reachable only through skills never ran.

The evidence and the measurements are in `docs/evaluations/frontend-design/` (the transcript metrics, the unused-agents investigation and the verification notes). Industry practice points the same way: Vercel's product-design skill routes between a read-only shaping mode and a hardening mode, and Anthropic's own guidance says exploratory work may skip planning.

## Decision

Add exploration modes beside the gated pipeline, not inside it.

- **`muse/sketch`** produces an `option-set@1`: three structurally different options per round (cap five), each with a status and a reason, rendered locally, with an append-only decision log.
- **`smith/spike`** produces a `spike-report@1`: a throwaway experiment that checks whether a tool or approach works, with what was verified and what was not.
- **`muse/promote`** turns a chosen option or a working spike into a `requirement@1`. It is the only route from an exploration artifact into a gated stage.
- Exploration modes are **non-binding**: no gate, no spec, no test requirement, open questions allowed. They write only to a scratch directory and to the artifact, mark the artifact `fidelity: sketch` or `spike`, and stop before implementing. An exploration artifact is never evidence for a gate.
- Divergent generation, producing structurally different options without judging them, is a new cognitive mode with its own agent (`muse/explorer`), as ADR 003 requires for any new cognitive phase. Judging the options stays with the user.
- The modes and their rules live in one reference (`shared/references/architecture/modes.md`), loaded by the three skills. The skill is the entry point; its agents are internal.

## Options considered

- **Loosen the existing gates.** Rejected because the gates earn their cost on stable contracts: the SiteNav work passed 478 end-to-end tests, and loosening a gate for everyone weakens the cases that need it.
- **A light flag on each existing skill.** Rejected because one skill would carry two contracts, and the sessions show the orchestrator skipping skills it finds heavy; a separate, named, light skill is easier to choose and easier to evaluate.
- **A new plugin for exploration.** Deferred. `muse` is the only plugin that owns UI and design, and `AGENTS.md` lets one plugin hold several skills for heterogeneous intents. The artifact schema is UI-neutral so sketching can move into its own plugin if it is used outside UI work.
- **Leave exploration ad hoc.** Rejected: it produced the largest token cost, the lost decisions and the unreviewed visual defects.

## Consequences

There is now a named, light path for early work, and a stated way back into the gated pipeline. The risks are that an exploration artifact is mistaken for a spec, and that the light path is used where the gated path is needed. The `fidelity` marker, the promote-only rule, the list of cases that must use the full pipeline in `modes.md`, and the required note of which gates were skipped address them. Each new skill and agent needs its Codex counterpart; no plugin version or changelog changes until a release is cut. The new schemas follow ADR 004 and are immutable once published. Whether the light path is chosen when it should be, and whether it speeds exploration without raising the defects found later, is an open evaluation (see `docs/evaluation-methodology.md`).
