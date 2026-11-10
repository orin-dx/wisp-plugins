# muse — Component Specification

**Stage:** Design · **Output:** `spec@1` · **Version:** 1.0.1

Turns UI or design intent into a component spec a developer can implement — including its accessibility behavior — without a single clarifying question. Muse audits the spec, not the implementation. It also has a light, non-binding path for early work: see options first, decide, then carry the choice forward.

- **Drafts** a component spec from a requirement or free-text design intent: props, variants, every interactive state, and accessibility criteria as testable propositions
- **Audits** the draft for missing states, missing accessibility criteria, and unmarked invalid prop combinations
- **Gates** the spec with a binding, default-fail exit gate before it proceeds to planning
- **Sketches** structurally different options, rendered and shown before they are described, with a decision log — no gate, no spec, no tests
- **Promotes** a chosen option into a `requirement@1`, the only route from a sketch into the gated stages

The `component` skill is one draft-audit-gate pipeline, reused unchanged regardless of which component is being specified. `sketch` and `promote` are the exploration path and never gate anything (see `shared/references/architecture/modes.md`).

---

## When to Use

- You have a `requirement@1` (or a design description/mockup) and need a formal component spec
- You want to check a drafted component spec for missing interactive states or ARIA criteria before it's implemented
- You need a binding pass/fail gate on a component spec before it enters planning
- You are about to write a component spec by hand: invoke `muse/component` first
- You want to see a few directions for a screen or component before deciding what to build (`sketch`), or a chosen option is ready to become real work (`promote`)

**Invoke with:** `"Spec this component"`, `"Draft a component spec for this design"`, `"Audit this component spec"`, `"Is this component spec ready?"`, `"Gate this component spec"`, `"Show me some options for this screen"`, `"Promote option B"`

Muse specs the component, not the code that implements it. Code-level accessibility scanning of the built component is not yet covered: **[ranger](../ranger/)** has no accessibility hazard pack.

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/wisp-plugins
/plugin install muse
```

**AGY** — installs the full repo; see the [root README](../../README.md#install) for instructions.

**Codex** — see the [root Codex setup](../../README.md#codex), then run `codex plugin add muse@wisp-plugins`.

---

## Skills

| Skill | What it does | Subagent |
| :--- | :--- | :--- |
| `muse/component` | Drafts, audits, and gates a component `spec@1` — props, variants, per-state behavior, and accessibility criteria as testable propositions | `drafter`, `auditor`, `exit-gate` |
| `muse/sketch` | Builds and renders three structurally different options per round, shows them before describing them, and keeps a decision log in an `option-set@1`. Non-binding: no gate, no spec, no tests | `explorer` |
| `muse/promote` | Turns a chosen option (or a spike that worked) into a `requirement@1` that carries the decision, the approved render, and what was and was not verified | none |

`component` is one skill, not three — the request itself determines which stage runs; there is no separate `muse/draft` or `muse/audit` to invoke.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `drafter` | Component Specification Drafter | sonnet / medium | Produces a `spec@1` from a `requirement@1` or design intent: props, variants, per-state observable behavior, and accessibility criteria. No TBDs permitted. Also runs in correction mode. |
| `auditor` | Component Specification Auditor | sonnet / medium | Adversarially reviews the draft for missing interactive states, missing accessibility criteria, and invalid prop combinations not marked as error cases. |
| `exit-gate` | Component Specification Exit Gate | opus / high | Binding pass/fail verdict before the spec enters planning. Default disposition: fail. Maximum 3 retries before escalation to a human. |
| `explorer` | Divergent Option Explorer | sonnet / medium | Builds and renders one structurally different option for a sketch and returns an `option-set@1` holding only that option. Writes only to a scratch directory, never ranks options. Internal to `sketch`. |

---

## Pipeline

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10px,ry:10px,font-weight:600;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10px,ry:10px,font-weight:600;

    Req["<b>Design intent</b><br/><code>requirement@1</code> or free text"] --> Draft["<b>Drafter</b><br/>component spec"]
    Draft --> Audit["<b>Auditor</b><br/>design review"]
    Audit --> Gate{{"<b>Exit gate</b><br/>binding verdict"}}
    Gate -->|"pass"| Spec(["spec@1"])
    Gate -.->|"targeted blockers"| Draft

    class Req source
    class Draft,Audit engine
    class Gate router
    class Spec output
```

Drafter/auditor review loops are capped at 2 iterations before reaching the exit gate. On fail, specific blockers are returned to `drafter` for a targeted retry. Maximum 3 retries before escalation to a human.

---

## Output Schemas

**`spec@1`** — see `shared/schemas/spec@1.json` (same schema `scribe` produces; muse introduces no new shape)

| Field | Required | Description |
| :--- | :--- | :--- |
| `id` | yes | Unique spec identifier |
| `purpose` | yes | One-sentence statement of what this component accomplishes |
| `scope` | yes | What is in scope for this spec |
| `non_goals` | yes | Explicit list of what this spec does NOT cover — including any state deliberately left unspecified |
| `api_surface` | no | The component's props — one entry per prop, `signature` carrying its type/domain |
| `acceptance_criteria` | yes | Array of testable propositions covering every prop, variant, state, and accessibility criterion; each has `is_error_case` flag |
| `spec_file_path` | no | Workspace-relative path where this spec is written on disk. Set after `exit-gate` passes. |
| `revision_note` | no | Set only on a correction — what changed and why, citing the affected criterion_id |
| `reasoning` | yes | Scratchpad — never forwarded downstream |

**`verdict@3`** — produced by `exit-gate` only; see `shared/schemas/verdict@3.json`

**`option-set@1`** — produced by `sketch`; see `shared/schemas/option-set@1.json`. A non-binding sketch (`fidelity: sketch`): an anchor `brief`, a `status` (`exploring`, `decided`, `abandoned`), a `round`, and one to five structurally different `options`, each with its own `status` (`open`, `parked`, `chosen`, `rejected`), a `reason` for every status except `open`, assumptions, open questions and `renders`; plus an append-only `decisions` log. Open questions are allowed here and not in a spec. Nothing in it enters planning until `promote` turns the chosen option into a requirement.

**`requirement@1`** — produced by `promote` from a decided sketch; see `shared/schemas/requirement@1.json` (the shape `weaver` produces).

---

## Next Stage

Feed the gated `spec@1` to **[navigator](../navigator/)** for implementation planning.
