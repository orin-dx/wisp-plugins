# ADR-017: Agent bodies drop the `<backstory>` section

**Status:** Accepted
**Date:** 2026-11-14
**Amends:** ADR-001 and ADR-006, which listed `<backstory>` as a required section. The rest of both records stands: no `<role>` body section, no `success_criteria` checklist, and a byte-identical `<constitution>`.

## Context

ADR 001 chose an experiential `<backstory>` ("I've seen X...", 2 to 4 sentences) over a role label, on the premise that it shapes judgment where a label would not. The premise was never measured. A backstory is a persona paragraph borrowed from human organizations; it costs tokens in every agent prompt, and it can pull in role behavior. In the 44 agents it mostly restated the failure mode that `<judgment>` already names.

A paired ablation tested the premise: 5 runs per condition on seeded defects, with and without the backstory, on `scribe:exit-gate`, `navigator:challenger` and `courier:changeset-analyzer` (Sonnet 5.5), scored on each agent's own output.

- **Catch rate:** every seeded defect was found in 5 of 5 runs in both conditions. Gate: an untestable criterion, a criterion contradicting the code, a missing out-of-range case, a fail verdict. Challenger: an uncovered criterion, a wrong task order. Analyzer: a link, a direct-push limit, a bold lead-in, a disposition, a semver impact, a scripting field.
- **Size and cost (median per run):** gate 10,346 characters and $0.32 with the backstory, 10,499 and $0.31 without; challenger 6,039 and $0.19, 6,023 and $0.18; analyzer 6,621 and $0.23, 6,359 and $0.23.

The limits: the seeded defects were easy, so every run hit the ceiling and the test could not show a backstory helping; three agents of 44, one model, 5 runs each. It shows no measurable effect, not that there is none. Per-run outputs are not reproduced here.

## Decision

Every agent body defines four sections in order: `<constitution>`, `<goal>`, `<judgment>`, `<output>`, plus the optional `<load_first>` after `<constitution>` as before. All 44 `<backstory>` blocks are removed.

A backstory fact the agent needs that appears nowhere else in its `<goal>`, `<judgment>` or `<output>` becomes a plain sentence in `<judgment>`; persona narrative is not kept. One agent needed this: `weaver:intake` now states that `why` names the pain behind the request, not a restatement of the feature. The other 43 backstories restated their agent's goal or judgment.

`<role>` and `success_criteria` stay out, and the frontmatter `role:` remains routing metadata. EARS stays confined to `<constitution>` and `<output>` (ADR 002 and ADR 006), now with one fewer interior section.

## Options considered

- **Keep the backstories.** Rejected: the only measurement shows no difference in what is caught, and they cost tokens in every prompt and may invite role play. Removing them is the cheaper default when nothing supports keeping them.
- **Remove them from the three tested agents only.** Rejected: it leaves two structures to author and audit, and the other 41 give no reason to expect a different result.
- **Re-run on harder defects first.** Rejected as a precondition: the ceiling effect means a harder run could change the result, but a measured loss is the evidence that should reopen this, and the cost of waiting is the tokens spent in every run meanwhile.

## Consequences

Each agent prompt is shorter by one paragraph, and the authoring rule has one fewer part. The persona that explained why an agent exists is gone, so a reader of the file sees the failure mode in `<judgment>` but not the incident behind it; the commit history keeps the old text. A real effect on harder tasks, or on other models, would be missed by this evidence.

**Restoring one.** If a later measurement shows a loss without the backstory, write a new ADR that supersedes this one, name the agents and the measured difference, and restore the section only for those agents. A restored `<backstory>` sits between `<constitution>` (and `<load_first>`) and `<goal>`; update `PARTS` in `tests/test_agent_structure.py`, the structure rule in `shared/constitution.md`, and the structure statements in `shared/agent-best-practices.md`, `ARCHITECTURE.md`, `README.md`, `CONTRIBUTING.md`, `AGENTS.md` and the mason agents. A useful measurement uses seeded defects hard enough not to saturate, more agents and models, and more than five runs per condition, as in `docs/evaluation-runbook.md`.

**Enforced by:** `tests/test_agent_structure.py` (four parts in order, no `<backstory>` or `<role>` section, byte-identical constitution).
