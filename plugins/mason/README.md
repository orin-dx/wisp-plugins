# mason — Plugin Authoring

**Stage:** Meta · **Output:** plugin artifacts and evaluations · **Version:** 3.2.3

Mason scaffolds plugins, audits conformance, designs inter-agent schemas, and evaluates workflow behavior with fixed hidden-oracle fixtures.

---

## When to Use

- You want to build a new plugin and need the correct directory structure
- You've written a plugin and want to verify it conforms to ecosystem rules
- You need to design a new JSON schema for a new inter-agent artifact type
- You want to generate a single conformant subagent `.md` file for an existing plugin
- You want a repeatable release or regression evaluation with exact plugin provenance

**Invoke with:** `"Create a plugin called X that does Y"`, `"Audit the X plugin for conformance"`, `"Design a schema for an artifact that carries Z"`, `"Write a subagent for task T"`, or `"Evaluate this workflow against fixture F"`.

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/wisp-plugins
/plugin install mason
```

**AGY** — installs the full repo; see the [root README](../../README.md#install) for instructions.

**Codex** — see the [root Codex setup](../../README.md#codex), then run `codex plugin add mason@wisp-plugins`.

---

## Skills

| Skill | What it does | Subagent |
| :--- | :--- | :--- |
| `mason/scaffold-plugin` | Generates a complete, ready-to-install plugin directory given a plugin ID and description | `scaffolder` |
| `mason/audit-plugin` | Audits an existing plugin directory against all ecosystem conformance rules; returns structured pass/fail/warn per check | `auditor` |
| `mason/design-schema` | Designs a new JSON Schema (draft 2020-12) for an inter-agent artifact; checks for conflicts with existing schemas | `schema-designer` |
| `mason/scaffold-subagent` | Generates a single conformant subagent `.md` file for an existing plugin — skips plugin.json/SKILL.md/symlink | `scaffolder` (single-subagent mode) |
| `mason/evaluate` | Runs an isolated behavioral fixture and records a provenance-complete `harness-evaluation@2` | `evaluation-runner`, `evaluation-adjudicator` |

`audit-plugin` is not bare `audit` — that word is already `ranger`'s plugin-level skill name (code/bug auditing). See `shared/constitution.md`'s Skill Names rule.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `scaffolder` | Scaffolder | sonnet / medium | Generates a complete plugin directory: `plugin.json`, `SKILL.md`, stub subagents, `shared` symlink. |
| `auditor` | Conformance Auditor | sonnet / medium | Audits a plugin directory for ecosystem conformance across all required fields, structure rules, and authoring principles. |
| `schema-designer` | Schema Designer | sonnet / medium | Designs a new JSON Schema for a proposed inter-agent artifact; checks for conflicts with existing schemas. |
| `evaluation-runner` | Evaluation Runner | haiku / low | Runs public fixture input in isolation without seeing the oracle. |
| `evaluation-adjudicator` | Evaluation Adjudicator | opus / high | Validates artifacts and seeded detections after the oracle is revealed. |

---

## Dispatch

Mason exposes independent authoring, audit, schema, and evaluation routes. The routes with multi-stage or agent-backed flow are:

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10px,ry:10px,font-weight:600;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10px,ry:10px,font-weight:600;

    SP["scaffold-plugin"] --> SC["<b>Scaffolder</b><br/>complete plugin"]
    SS["scaffold-subagent"] --> SC
    AP["audit-plugin"] --> AU["<b>Auditor</b><br/>conformance"]
    DS["design-schema"] --> SD["<b>Schema designer</b><br/>versioned contract"]
    EV["evaluate"] --> ER["<b>Evaluation runner</b><br/>oracle hidden"] --> EA{{"<b>Evaluation adjudicator</b><br/>oracle revealed"}} --> Report(["harness-evaluation@2"])

    class SP,SS,AP,DS,EV source
    class SC,AU,SD,ER engine
    class EA router
    class Report output
```

The paths are independent. `scaffold-plugin` and `scaffold-subagent` share the scaffolder in different modes.

---

## Output Schemas

- `evaluation-run@1` — immutable runner evidence captured before the hidden oracle is revealed; see `shared/schemas/evaluation-run@1.json`
- `harness-evaluation@2` — adjudicated detections, false passes, corrections, provenance, and comparison data; see `shared/schemas/harness-evaluation@2.json`

Scaffold and audit routes produce or inspect repository files rather than an inter-agent JSON artifact. `design-schema` produces the requested new versioned schema.

---

## Conformance Checks (auditor)

The checks and their rules live in `shared/constitution.md` and `agents/auditor.md`. A plugin that fails any check is not ecosystem-conformant.

---

## Directory Layout

Plugins produced by `scaffolder` follow this exact layout — one skill directory named after the plugin id, the default for a new plugin:

```
plugins/<id>/
├── plugin.json                  # id, name, version, description, author, skills, agents
├── shared -> ../../shared       # symlink — never copy
├── subagents -> agents          # symlink
├── skills/
│   └── <id>/
│       └── SKILL.md             # YAML frontmatter + body
└── agents/
    └── <agent-name>.md          # one file per agent in plugin.json
```

If a plugin's scope later grows to cover several genuinely independent, heterogeneous intents on the same artifact — not a linear pipeline invoked as one flow — `skills/<id>/` may split into multiple directories, one per skill (`skills/<skill-name>/SKILL.md`), each still following the frontmatter and 5-part-body rules. `courier`, `scribe`, `weaver`, and `mason` itself are all examples.

`mason/audit-plugin` checks every `SKILL.md` found under `skills/`, not just one — it doesn't assume the single-directory default.

---

## Key Authoring Principles

See `shared/constitution.md` and `shared/agent-best-practices.md`.

---

## References

- `shared/agent-best-practices.md` — full authoring checklist (mason authors use this; subagent bodies do not reference it at runtime)
- `shared/harness-authoring.md` — cross-harness identity, contract, workflow, and packaging boundaries
- `shared/references/evaluation/behavioral.md` — hidden-oracle evaluation and provenance rules
- `shared/schemas/` — existing schemas to check against when designing a new one
