# Wisp Plugins AI Agent & Skill Specification (`AGENTS.md`)

This guide defines the top-level repository guidelines for AI coding agents (Claude Code, AGY, Cursor, Copilot, Codex) working on or utilizing the Wisp Plugins repository (`orin-dx/wisp-plugins`).

---

## 1. Authoritative Sources

All hard rules for plugin and agent authoring live in one place:

- [**`shared/constitution.md`**](./shared/constitution.md): EARS-format authoritative constraints. The fence all plugin development must stay inside. Read this first and last.
- [**`shared/agent-best-practices.md`**](./shared/agent-best-practices.md): Principles behind the constitution, explained with examples. Authoring-time only — never loaded by agents at runtime.
- [**`shared/debugging-laws.md`**](./shared/debugging-laws.md): Core proof laws, read-only investigation rules, verification that tells the wrong behavior from the correction, with no fixed test order.
- [**`shared/harness-authoring.md`**](./shared/harness-authoring.md): Cross-harness change classification, native workflow boundaries, and required counterpart review.
- [**`docs/adr/README.md`**](./docs/adr/README.md): Index of accepted architectural decisions, each with a guardrail. Read the record before changing what its guardrail names; [`shared/references/architecture/decision-records.md`](./shared/references/architecture/decision-records.md) says when and how to write one.
- [**`shared/references/tooling/cli.md`**](./shared/references/tooling/cli.md): Capability-aware preferences for modern CLI tools, with repository-native commands and safe fallbacks taking priority.

---

## 2. Directory Layout Standard

```text
plugins/<plugin-id>/
├── plugin.json                   <-- Plugin Manifest (id, version, skills, agents)
├── README.md                     <-- Purpose, trigger phrases, agent table, install
├── CHANGELOG.md                  <-- Semver history
├── skills/
│   └── <plugin-id>/
│       └── SKILL.md              <-- Skill definition (dispatch matrix, pipeline)
├── hooks/hooks.json              <-- Only when the plugin ships a Claude Code hook
└── agents/                       <-- Few. `wisp`: verifier (opus/high), adversary (opus/high), recon (haiku/low)
```

The v5 set is `wisp` (core), `wisp-packs`, `courier`, `muse` and `mason` (ADR 018).

A plugin defaults to one skill directory named after the plugin id, as above. IF the plugin's scope covers several genuinely independent, heterogeneous intents on the same artifact — not a linear pipeline invoked as one flow — `skills/<plugin-id>/` may split into `skills/<skill-name>/SKILL.md` per skill instead. `courier`, `mason`, and `muse` are examples; `wisp` keeps one `work` skill with mode skills as one-line aliases. The skill-routing key is the directory name, not the frontmatter `name:` field. A new skill name defaults to a single lifecycle-stage word; only go to a specific compound name when the bare word is ambiguous or collides with another plugin's existing skill name. See `shared/constitution.md`'s Plugin Structure and Skill Names sections.

Agents are split by **context and risk**, not by role, cognitive mode or pipeline position: one worker holds the context, and a separate agent exists only for an independent check, one disputed finding, or a cheap read-only inventory (ADR 018). See `shared/constitution.md` for the model/effort tier rules.

---

## 3. Quick Checklist for Adding New Plugins

1. **Use `mason`** — run `mason:scaffold-plugin` to generate the directory structure and stubs, and `mason:audit-plugin` to check conformance.
2. **Few agents, 4-part structure** — add an agent only for context isolation or a risk tier (ADR 018); no role agents, per-stage gates or mandatory spec or plan stages. Every agent body: `<constitution>` (copied byte-for-byte from an existing agent), `<goal>`, `<judgment>`, `<output>`. No `<role>` or `<backstory>` body sections (ADR 017). No `success_criteria` checklists.
3. **EARS in output only** — WHEN/IF/WHILE/WHERE notation belongs only in `<output>` contracts and never-do rules.
4. **Progressive context loading** — one `<load_first>` block per agent, naming only the focused references needed for its cognitive phase.
5. **Schema-first handoffs** — define `shared/schemas/<name>@<version>.json` before writing the agent that produces it.
6. **Abstract tool language** — "use your file reading tool", never `view_file`, `read_file`, or `Bash tool`.
7. **Instruction economy** — keep one actionable rule per item, remove repeated rationale, and number only order-dependent work.
8. **Radical candor** — state material concerns, evidence, consequence, and confidence directly; do not soften blockers, manufacture praise, or overstate certainty.
9. **Reference routing and quality** — organize by cognitive concern, use language filenames only for language-specific evidence, and state outcome, applicability, evidence, refutation, and disposition.
10. **Verification evidence** — match checks to risk; require generators and oracles, independently derived semantic candidates, fresh state, terminal results, and explicit gaps when relevant. A behavior that must hold gets a hook or a test in `tests/`, not only a prompt.
11. **Cross-harness review** — preserve identity, skill routes, artifact contracts, evidence, and acceptance intent in Claude/AGY and Codex sources; native wording and delegation may differ.
12. **Manifest registration** — add an entry to root `marketplace.json` and validate: `jq . marketplace.json`.
13. **Legal attribution** — set `author` in `plugin.json` to the `{name, email}` object shown in `CONTRIBUTING.md`.

---

## 4. Validation

```bash
just check
```

`just --list` shows each check as its own recipe (`just manifests`, `just test` for `tests/test_*.py`, `just versions`, `just skills-doc`, `just reference-size`, `just adr-style`, `just platform-limits`, `just claude-manifests`, `just marketplace-check`, `just mermaid`, `just wiring`) for running a subset while editing; run the full set before release. `just fmt`/`just fmt-check` format with `oxfmt`; not yet part of `just check` until the repo has a baseline format pass. To bump a version, edit `plugins/<id>/plugin.json` (the ecosystem's is `marketplace.json`'s top-level `version`), add the matching top `CHANGELOG.md` entry, and run `just claude-manifests-sync && just marketplace-sync`; never hand-edit the README `**Version:**` line, badge, marketplace entry, or Claude or Codex manifest versions. Generated Codex files in `.agents/plugins/` and `dist/codex/` must match their authored sources; never edit them directly — run `just marketplace-sync` after a Codex source change.
