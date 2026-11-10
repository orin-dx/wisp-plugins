# Modes: exploring, building and pinning down

Gating every step suits a contract many things depend on and fails an idea nobody has seen. Pick the mode that matches how settled the work is, say so, and keep the gates that belong to it. Invoke the skill; its agents are internal.

## Modes

| Mode | Use when | Writes | Gate | Entry skill | Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| sketch | You want to see options before deciding | `docs/sketches/<id>.json`, a scratch directory | None | `muse/sketch` | `option-set@1` |
| spike | You need to know whether a tool or approach works | A scratch directory | None; a smoke check is reported | `smith/spike` | `spike-report@1` |
| promote | A chosen option or working spike should become real work | A requirement draft | Gated later, by the consuming stage | `muse/promote` | `requirement@1` |
| specify | Behavior must be pinned down | `docs/specs/` | Binding exit gate | `muse/component`, `scribe/draft-spec` | `spec@1`, `verdict@3` |
| plan, implement | A gated spec exists and the change must be correct | The repository | Challenger, then recon, mutation, review, exit gate | `navigator/plan`, `smith/implement` | `plan@1`, `verdict@3` |

Use the full pipeline, not an exploration mode, for shared components, anything other code depends on, behavior and accessibility that must not regress, and anything in production.

## Exploration rules

1. **State the mode first**, for example "Mode: sketch. Nothing here is binding." If a gated mode fits better, say so and let the user choose.
2. **No gate, spec or test requirement.** Open questions and unverified assumptions are allowed and listed in the artifact.
3. **Write only to scratch** (`.scratch/<id>/`; suggest ignoring it) and to the artifact. Never edit existing source, configuration or specs.
4. **Mark the artifact** `fidelity: sketch` or `spike`, so no one mistakes it for a spec.
5. **Stop before implementing.** End with options and open questions, or a conclusion. Building from it is a separate request, made through `promote`.
6. **Show, then describe.** Render visual work and present it before explaining it. With no render tool, give the file paths and the command that opens them, and say nothing was seen.
7. **Keep a decision log**, appended and never rewritten. Re-read the anchor brief each round; after about four revisions restate it and start from it, because output drifts.
8. **Say what was not checked.** A spike lists what it verified and what it did not; a sketch lists the assumptions its options make.

## Moving between modes

- Exploration reaches a gated stage only through `promote`, which names the choice, carries its verified and unverified lists, and yields a requirement for the next stage to gate.
- An exploration artifact is never evidence for a gate; a gate cites the requirement or spec.
- When a gated stage keeps failing on something that cannot be specified yet, stop the retry loop, explore that part, and promote the result.
- A reply that took a lighter path ends with one line naming the gates it did not run.

## Defaults

Three options per round, structurally different (not color or spacing), five at most. At the first direction commit for design work, offer four directions and let the user pick one.

## In a repository

Add one line to `AGENTS.md`: "For exploratory work use the sketch and spike skills; they are non-binding. Use the specify, plan and implement skills for shared or production work."
