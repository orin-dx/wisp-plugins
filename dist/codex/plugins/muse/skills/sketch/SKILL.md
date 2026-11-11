---
name: sketch
description: Explore several structurally different options for a design or approach, rendered and shown before they are described, with a decision log. Use this, rather than describing options in prose, when the user wants to see options before deciding what to build. Non-binding: no gate, no spec, no tests.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Show options before deciding

Open with "Mode: sketch. Nothing here is binding." This is the light path: there is no gate, no spec and no test requirement, open questions are allowed, and the work stops before implementing. If the request is a shared component, something other code depends on, or behavior and accessibility that must not regress, say the gated path (`component`) fits better and let the user choose. Read `shared/references/architecture/modes.md` for the mode rules.

## Inputs

- Free-text intent, an existing `option-set@1` to continue, or a `requirement@1` for context.
- The project's brand, stack, tokens and real content, when they exist.

## Workflow

1. Write the anchor brief: the problem, the audience, the constraints and the non-goals. Ask at most three short questions, and only when an answer would change the options; otherwise state assumptions and continue.
2. For design work, in the first round propose four distinct, concrete directions, one line each, and let the user pick one. If they say "you choose", pick and say why. Later rounds stay inside the chosen direction.
3. Name three structural bets (five at most) that differ in arrangement, interaction model or information hierarchy, not in color or spacing. Replace any option that differs only in tint.
4. Build each option as a minimal static page (HTML and CSS, no build step) under `.scratch/<id>/<option-id>/`, using real content and tokens. Mark placeholder text as placeholder; invent no numbers, claims or testimonials.
5. Render each option at the viewports and themes in the brief (default 390x844 and 1440x900, light and dark when the project has both) with the project's Playwright script, a browser tool, or the sandboxed browser if the host provides one. Write `.scratch/<id>/board.html` listing each option's title, status, summary and renders side by side. Make each preview frame tall enough to show the whole option (at least 640px) and let the board scroll; a clipped preview hides the design. Present the renders before explaining them. If nothing can render, say so and give the one command that opens the files; never describe a render you did not see. Keep command output and scripts out of the thread as `shared/references/tooling/context.md` says. Look at one render at a time.
6. Record the decision. Set each option's `status` to `chosen`, `rejected` or `parked` with a `reason`, and append a dated entry to `decisions`. Never rewrite an earlier entry or reuse an option id. For another round, re-read the brief and restate it in a line; after about four rounds, restate it and start from it, because options drift.
7. Write the `option-set@1` (conforming to `shared/schemas/option-set@1.json`, with `fidelity` set to `sketch`) to `docs/sketches/<id>.json`, list the assumptions and open questions, and stop. Offer another round, `promote`, or dropping it, and end with one line: "Skipped by design: spec, tests and gates."

## Record shape

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

## Decisions and stopping

Write only under `.scratch/<id>/` and to `docs/sketches/<id>.json`; never edit existing source, configuration or specs. Do not advocate for an option; give a recommendation only when asked. A sketch is never evidence for a gate. After five rounds without a decision, offer to narrow the brief, park it, or abandon it.

## Team use

Before delegating, read `agent-roles/README.md`. To build options in parallel, ask the host to start one subagent per option with the `author` role, at most three at once, and give each the delegation packet: the option id and structural idea, the anchor brief and direction, the sibling options it must differ from, the scratch path it may write under (owned paths), and the output (an `option-set@1` holding only its option). Each subagent builds, renders and returns; it never ranks the options. The primary agent merges the options, shows them and records the decision. If subagents are unavailable or not requested, build the options one after another yourself.
