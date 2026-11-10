---
name: sketch
description: >-
  Use this, rather than describing options in prose, whenever the user wants to see options before deciding: "show me some options", "try a few directions", "sketch this", "what could this look like", "I want to see it before we spec it". Builds and renders three structurally different options as an option-set@1 with a decision log. Non-binding: no gate, spec or tests. Stops before implementing; use promote to build.
version: 1.0.0
---

# Muse — Sketch Skill

<overview>
Lets the user see options before anything is decided. The output is a sketch: a small set of structurally different options, each built as a quick static page, rendered, shown, and recorded with a status and a reason. Nothing here is binding: no gate, spec or tests, and the skill stops before implementing. Open the reply with "Mode: sketch. Nothing here is binding."
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **explorer** | sonnet / medium | An option needs building and rendering in its own context. Up to three explorers may run in parallel, one per option. For a single small option, build it directly instead. |

The explorer is internal to this skill. Do not call it on its own, and never ask it to rank the options.
</dispatch>

<references>
`shared/references/architecture/modes.md`, `shared/schemas/option-set@1.json`

When running render or build commands, keep command output and scripts out of the thread as `shared/references/tooling/context.md` says. Look at one render at a time.
</references>

<io>
**Consumes**: free-text intent, an existing `option-set@1` to continue, or a `requirement@1` for context
**Produces**: `option-set@1` written to `docs/sketches/<id>.json` (`fidelity: sketch`), with working files under `.scratch/<id>/`
</io>

<record_shape>
```json
{
  "id": "SKETCH-001",
  "title": "Hero section",
  "brief": { "problem": "string", "audience": "string", "constraints": ["string"], "non_goals": ["string"] },
  "direction": "string",
  "status": "exploring",
  "round": 1,
  "options": [
    {
      "id": "OPT-split",
      "title": "string",
      "summary": "string",
      "structure": "what makes it structurally different from the others",
      "status": "open",
      "assumptions": ["string"],
      "open_questions": ["string"],
      "renders": [{ "kind": "file", "location": ".scratch/SKETCH-001/OPT-split/index.html", "viewport": "1440x900", "theme": "light" }]
    }
  ],
  "decisions": [{ "option_id": "OPT-split", "decision": "chosen", "reason": "string", "date": "2026-10-20" }],
  "fidelity": "sketch",
  "reasoning": "string"
}
```

Follow it exactly, because the file is checked against `option-set@1` and a record in another shape is rejected. Required: `id` (`SKETCH-` and three or more digits), `title`, `brief` (with `problem` and `audience`), `status` (`exploring`, `decided` or `abandoned`), `round` (an integer from 1), `options` (one to five), `fidelity` (always `sketch`) and `reasoning`. Each option needs `id` (`OPT-` and a lowercase slug), `title`, `summary`, `structure` and `status` (`open`, `parked`, `chosen` or `rejected`); every status except `open` needs a `reason`. A `decided` sketch needs at least one `decisions` entry, and each entry needs `option_id`, `decision`, `reason` and a `YYYY-MM-DD` date. `kind` in a render is `file`, `url` or `screenshot`. No other fields are allowed.
</record_shape>

<workflow>
1. **State the mode, and check it fits.** Begin your first message with exactly: "Mode: sketch. Nothing here is binding." If the work is a shared component, something other code depends on, or behavior and accessibility that must not regress, say the gated path (`muse/component`) fits better and let the user choose.
2. **Write the anchor brief**: the problem, the audience, the constraints (brand, stack, tokens, real content) and the non-goals. Ask at most three short questions, and only when an answer would change the options; otherwise state your assumptions and go on.
3. **Commit a direction** (design work, first round only). Propose four distinct, concrete directions, one line each, and let the user pick one; if they say "you choose", pick and say why. Skip this for non-visual exploration. Later rounds stay inside the chosen direction.
4. **Plan the round.** Name three structural bets (five at most) that differ in arrangement, interaction model or information hierarchy, not in color or spacing. If two options differ only in tint, replace one.
5. **Build each option** as a minimal static page (HTML and CSS, no build step) under `.scratch/<id>/<option-id>/`, using the brief's real content and tokens. Mark placeholder text as placeholder; never invent numbers, claims or testimonials. Use the `explorer` for parallel builds.
6. **Render, then show.** Capture each option at the viewports and themes the brief names (default 390x844 and 1440x900, and light and dark when the project has both) with the project's own Playwright script, a browser tool, or the host's browser. Write `.scratch/<id>/board.html` that lists each option's title, status, summary and renders side by side. Make each preview frame tall enough to show the whole option (at least 640px) and let the board scroll; a clipped preview hides the design. Present the renders before explaining them. If nothing can render, say so plainly and give the one command that opens the files; do not describe a render you did not see.
7. **Record the decision.** The user chooses, rejects or parks. Set each option's `status` with a `reason`, and append an entry with the date to `decisions`; never rewrite an earlier entry or reuse an option id. For another round, re-read the anchor brief, restate it in a line, and generate new options inside the direction. After about four rounds restate the brief and start from it, because options drift.
8. **Close and stop.** Set `status` to `decided` or `abandoned`, write `docs/sketches/<id>.json`, and list the assumptions and open questions. Do not start building. Offer the next step: another round, `muse/promote` to carry the chosen option into real work, or drop it. End with one line naming what was skipped: "Skipped by design: spec, tests and gates."
</workflow>

<rules>
- Write only under `.scratch/<id>/` and to `docs/sketches/<id>.json`. Never edit existing source, configuration or specs. Suggest adding `.scratch/` to the ignore file.
- Keep option ids stable and never reuse one for a different option.
- Do not advocate. Present the options and their trade-offs; the user decides. Give a recommendation only when asked.
- A sketch is never evidence for a gate. Anything that continues goes through `muse/promote`.
- Allowed here and not in a spec: open questions, unverified assumptions, placeholder content, a rough build.
</rules>

<circuit_breaker>
There is no gate to loop on. After five rounds without a decision, say so and offer to narrow the brief, park the exploration, or abandon it.
</circuit_breaker>
