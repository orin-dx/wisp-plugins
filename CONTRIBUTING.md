# Contributing

By participating in this project, you agree to abide by the [Code of Conduct](./CODE_OF_CONDUCT.md). Found a security issue? See [SECURITY.md](./SECURITY.md) instead of opening a public issue.

---

## Start Here

Run `just install` once, then `just check` before every pull request. Pick the row that matches your change.

| You are changing | Read | Also run |
| :--- | :--- | :--- |
| A new plugin | [Authoring a New Plugin](#authoring-a-new-plugin) | `mason:scaffold-plugin`, `mason:audit-plugin` |
| An agent, skill or reference | [Agent Authoring Checklist](#agent-authoring-checklist), [Capability Change Checklist](#capability-change-checklist) | `just platform-limits`, `just reference-size` |
| A schema | [Adding a Shared Schema](#adding-a-shared-schema) | `just wiring`, `just test` |
| A hook (handback, Stop, pack injection) | [Hooks](#hooks) | the hook's test in `tests/` |
| A house pack | [Adding a Pack](#adding-a-pack) | `just test`, `just marketplace-sync` |
| An architectural rule | [Decision Records](#decision-records) | `just adr-style` |
| A version or release | [Releasing](#releasing) | `just claude-manifests-sync && just marketplace-sync` |
| Codex behavior | [`shared/harness-authoring.md`](./shared/harness-authoring.md) | `just marketplace-sync`, `just marketplace-check` |
| A diagram | `shared/references/authoring/diagrams.md` | `just mermaid` |

The v5 set is `wisp` (the `work` skill, `verifier`, `adversary`, `recon`), `wisp-packs`, `courier`, `muse` and `mason`. [`ARCHITECTURE.md`](./ARCHITECTURE.md) explains how they fit; [`AGENTS.md`](./AGENTS.md) is the short rule list for coding agents.

---

## Authoring a New Plugin

The fastest way to scaffold a new plugin is with the `mason` plugin:

```
"Create a plugin called <id> that does <goal>"
```

`mason:scaffold-plugin` generates the directory structure, `plugin.json`, `SKILL.md`, and any stub agent files. Run `mason:audit-plugin` afterward to verify conformance.

To scaffold manually:

```bash
mkdir -p plugins/<id>/skills/<id> plugins/<id>/agents
ln -s ../../shared plugins/<id>/shared
```

Then create `plugin.json`, `skills/<id>/SKILL.md`, and `agents/*.md` following the conventions below.

---

## Plugin Structure

```
plugins/<id>/
├── plugin.json
├── README.md
├── CHANGELOG.md
├── skills/<id>/SKILL.md
└── agents/              (few: `wisp` has verifier, adversary and recon; `muse` has one)
    └── <agent>.md
```

Add an agent only where a separate context or a different risk tier pays for itself: an independent check, one disputed finding, a read-only inventory, or an isolated build (ADR 018). Do not add a role agent, a per-stage gate or a handoff document between stages; the worker that holds the context does the work. Agent files are never prefixed with the plugin id (`verifier.md`, not `my-plugin-verifier.md`) — Claude Code already namespaces agents as `<plugin_id>:<agent_name>`, so a prefix produces redundant `my-plugin:my-plugin-verifier` stuttering. See `shared/agent-best-practices.md`'s Namespacing Rule.

A plugin defaults to this single-skill layout. IF its scope covers several genuinely independent, heterogeneous intents on the same artifact — not a linear pipeline invoked as one flow — `skills/<id>/` may split into `skills/<skill-name>/SKILL.md` per skill instead (see `courier`, `mason`, `muse`); `wisp` keeps one `work` skill with one-line mode aliases. A new skill name defaults to a single lifecycle-stage word; go to a specific compound name (`audit-plugin`, not `plugin-audit`) only when the bare word is ambiguous or collides with another plugin's existing skill name — never resolve a collision by prefixing the plugin id, since `plugin:skill` invocation already disambiguates that. See `shared/constitution.md`'s Plugin Structure and Skill Names sections.

### `plugin.json`

```json
{
  "id": "my-plugin",
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "One sentence.",
  "author": {
    "name": "Gabriel Castro",
    "email": "gabe@techworx.dev"
  },
  "skills": "./skills/",
  "agents": ["./agents/verifier.md"]
}
```

`skills` is always the path string `"./skills/"` — the loader discovers every `SKILL.md` under it, whether that's one directory or several. `agents` is the explicit list of agent file paths; every file listed must exist, and every file present must be listed (`just wiring` checks that listed files exist; `mason:audit-plugin` checks both directions).

### `SKILL.md`

The skill prompt is what the user invokes. It should:

- Have a concise frontmatter `description` covering when to activate the skill, its input, its output, and key constraints
- Name which agents it delegates to, when, and what each returns; a plugin with no agent lists none (`"agents": []`)
- Reference shared schemas by exact relative path
- Use the shortest direct wording that preserves each action, condition, evidence requirement, and consequence

---

## Agent Authoring Checklist

Read `shared/agent-best-practices.md` before authoring. The hard requirements:

### 4-part structure (frontmatter + body)

- [ ] **Constitution** — copied byte-for-byte from an existing agent, never authored fresh. See `shared/constitution.md`'s Static Prompt Prefix Invariant.
- [ ] **Goal** — what the agent must produce and why. Intent, not steps.
- [ ] **Judgment** — how to tell if the goal was genuinely achieved vs. output that merely looks like it was. Name the key failure mode.
- [ ] **Output** — structured shape; reference a schema from `shared/schemas/` when output flows to another agent.

No `<role>` or `<backstory>` section in the body (ADR 017). The frontmatter `role:` field is platform metadata (short display label for routing) and should be kept. No `success_criteria:` checklist. No filler: "your job is to", "make sure to", "please ensure".

### Instruction economy

- [ ] Each paragraph or list item contains one independently actionable rule
- [ ] Sub-bullets express real branches, evidence, or attributes rather than split a long sentence cosmetically
- [ ] Numbered steps are reserved for operations whose order affects correctness
- [ ] Repeated rationale, process narration, filler, and synonymous restatement are removed
- [ ] Non-obvious context appears once, at the decision it changes
- [ ] Bodies over 300 words and list items over 40 words are reviewed, not automatically rejected
- [ ] Material concerns state evidence, consequence, and confidence directly; blockers are not softened and praise is not manufactured

### Progressive context loading

- [ ] Declares one `<load_first>` block naming only the focused `shared/references/` files needed for this agent's phase
- [ ] Does not load reference files outside its cognitive mode (scanner loads hazards, not smells)
- [ ] Places references under the cognitive concern; uses language filenames only for language-specific evidence
- [ ] Keeps human indexes out of runtime load chains
- [ ] For Codex, every exact `shared/` path loaded directly or transitively appears in `harnesses/codex/catalog.json`; historical mentions omit the path when runtime access is unnecessary

### EARS placement

- [ ] EARS notation (`WHEN`, `IF`, `WHILE`, `WHERE`) used only in output contracts and never-do rules
- [ ] No EARS in implementation steps, search strategies, or reasoning guidance

### Model and effort

- [ ] `haiku` / `low` — deterministic enumeration and mechanical work (inventory, commit messages)
- [ ] `sonnet` / `medium` — analysis and drafting (changesets, pull requests, plugin audits, exploration)
- [ ] `opus` / `high` — judgment (the verifier's `verdict@3`, refutation that decides a finding, evaluation adjudication)
- [ ] An agent whose output a verifier or a human judges again stays `sonnet` / `medium`

### Routing and hooks

- [ ] An agent's `description` names the skill that starts it, so the model reaches it through the skill and its checks run; there is no routing guard hook, and the plugin's single entry point is where routing lives
- [ ] A new agent that issues a binding `verdict@3` gets a `ROUTES` entry in `shared/hooks/validate-handback.py` and the plugin registers `validate-handback.py` in `hooks/hooks.json` (ADR 012); only `wisp:verifier` has one, and a new one needs a new ADR (ADR 018)
- [ ] These hooks run only in Claude Code; the skill text must still state the rule for Codex and Antigravity

### Tool language

- [ ] Uses abstract tool language: "use your file reading tool", "use your search tool"
- [ ] No tool-specific calls (`view_file`, `read_file`, `grep_search`, etc.)
- [ ] No absolute paths

### Schema conformance

- [ ] If the output is a named schema (e.g. `verdict@3`), every field in the output shape is declared in `shared/schemas/` — no undeclared fields, no missing required fields

### Verification evidence

- [ ] Behavioral claims name evidence that can falsify them; tool invocation alone is not evidence
- [ ] Generative checks name the generator and oracle
- [ ] Semantic sibling searches derive candidates from domain responsibility, state transitions, and architecture, then record each outcome
- [ ] External or asynchronous checks use fresh state and terminal results
- [ ] Unsupported or disproportionate checks are recorded as coverage gaps

### Runtime reference quality

- [ ] States the outcome and condition that make the reference useful
- [ ] Treats heuristics as candidate signals and names evidence that confirms or refutes them
- [ ] Prescribes implementation or order only when correctness, safety, or protocol sequence requires it
- [ ] Derives abstractions from live architecture instead of importing project-specific names
- [ ] Covers every language or platform it claims, or states the missing target as a coverage gap
- [ ] Uses word and line thresholds as review signals rather than proof of poor quality

---

## Adding a Shared Schema

Shared schemas in `shared/schemas/` are the inter-plugin API. To add one:

1. Create `shared/schemas/<name>@<version>.json` using JSON Schema draft-2020-12
2. Set `additionalProperties: false`
3. Include a `reasoning: string` field (`candidate@1` and `implementation-context@1` predate this rule)
4. Document which plugin produces it and which consume it
5. **Never modify an existing versioned schema** — create `<name>@<version+1>.json` instead

---

## Registering in `marketplace.json`

Add an entry to the `"plugins"` array:

```json
{
  "id": "my-plugin",
  "name": "my-plugin",
  "version": "1.0.0",
  "path": "./plugins/my-plugin",
  "description": "One sentence description. Skills: skill-one, skill-two."
}
```

---

## Capability Change Checklist

For a change spanning Claude/AGY and Codex, read [`shared/harness-authoring.md`](./shared/harness-authoring.md) first. It defines which concerns are shared, which are native, and the counterpart-review record required before release.

When you add or change what an existing agent can do — a new dimension, a new output status, a new default posture — the code change alone leaves the ecosystem inconsistent. Work through this list in the same change:

- [ ] Frontmatter `description` reflects the new capability
- [ ] If the agent's output gained a new status/enum value, the plugin's `SKILL.md` names what the caller does with it — or states it's terminal
- [ ] New references live under the reader's concern, have a real caller, and update `shared/references/README.md` when they introduce a concern
- [ ] If runtime reference behavior changed, every consuming Claude/AGY and Codex route was reviewed and affected plugin versions were updated
- [ ] Every prose description still matches the agent's current behavior:
  - Plugin README subagent and output-schema sections
  - SKILL.md overview, dispatch, and I/O sections
  - Narrowed or corrected capabilities, not only additions
- [ ] Plugin `CHANGELOG.md` gets a new dated entry
- [ ] Version bumped in `plugin.json` only (see `shared/references/delivery/changesets.md`), then `just claude-manifests-sync && just marketplace-sync` write the README, marketplace, Claude and Codex copies; a bump needs no other hand edit
- [ ] `mason:scaffold-plugin` and `mason:audit-plugin` reflect any new structural convention; capability-only changes need no Mason update

This isn't automated. `mason:audit-plugin` checks structural conformance; it does not (yet) check that every downstream doc/version file was updated to match a capability change. Until it does, this checklist is the thing standing between "the agent works" and "the ecosystem knows the agent works."

---

## Hooks

Rules that must hold are hooks, not prompts, and hooks run only in Claude Code. A skill must still state the rule for Codex and Antigravity.

- **Registration:** `plugins/<id>/hooks/hooks.json`, with scripts in `shared/hooks/` (standard library only, fail open).
- **Existing hooks:** `validate-handback.py` (`wisp:verifier`'s `verdict@3` and round cap; trace with `WISP_HANDBACK_TRACE=<file>`), `stop-check.py` (asks once for a `Not verified:` line; off with `WISP_STOP_CHECK=off`), `pack-inject.py` (injects declared packs at session start).
- **Every hook change:** update its test (`tests/test_handback_validator.py`, `tests/test_wisp_core.py`, `tests/test_wisp_packs.py`), its row in [`ARCHITECTURE.md` section 5](./ARCHITECTURE.md#5-hooks-and-where-they-run) and [`docs/repository-hooks.md`](./docs/repository-hooks.md).

## Adding a Pack

A pack is plain markdown in `plugins/wisp-packs/packs/<name>.md` on how the owner builds in one area.

- **Shape:** the first line says when it applies. Per rule: the outcome, the evidence that shows it holds, and the check that enforces it when there is one. End with an exemplar to imitate.
- **Admission:** a rule enters a shared pack only when it holds in at least two repositories. Prefer a check (a lint, a type, an architecture test) over prose; say so when a rule has none.
- **Never:** add a command the repository does not declare, or loosen a check unasked.
- **After adding:** run `just test` and `just marketplace-sync`, mention the pack in `plugins/wisp-packs/README.md` and bump its version.

## Decision Records

Write an ADR in `docs/adr/` only when the choice is architectural and expensive to reverse or not obvious from the code; `shared/references/architecture/decision-records.md` has the two gates and the shape. Do not rewrite an accepted record: change its status and links, or supersede it with a new one. Add the index row in `docs/adr/README.md`; `just adr-style` warns when a record reads as a session log.

---

## Engineering Invariants

- **No absolute paths:** prompt and skill paths are relative.
- **Self-contained subagents:** each prompt is readable in isolation and has no dependency on another agent's private prompt.
- **Pull, don't inject:** subagents load `shared/references/` on demand; the host does not preload them. The one exception is a pack a repository opts into with a `Packs:` line (`pack-inject.py`).
- **Authoring-only guidance:** never load `shared/agent-best-practices.md` at runtime.
- **Abstract tool language:** keep prompts portable across harnesses.
- **Conventional commits:** use the applicable type and plugin scope.
- **Clean writing:** omit AI filler, marketing language, and non-warning ALL CAPS.
- **Diagrams:** follow `shared/references/authoring/diagrams.md` when Mermaid materially clarifies a relationship.

---

## Releasing

You run `just release`, not an agent: it publishes. A release has three levels, and this marketplace installs from `main`:

- **Shipped:** merged to `main` with the version bumped and the changelog entry written. Claude Code updates a plugin when its version changes, so this is what users get.
- **Pinned:** annotated git tags: `vX.Y.Z` for the ecosystem and `<plugin>--vA.B.C` for each plugin version, all on the merged commit. They give a rollback point and an exact version to install.
- **Announced:** a GitHub release for the ecosystem tag. Write its notes in `docs/releases/vX.Y.Z.md` (short highlights, then a pointer to the changelog); without that file the release uses the top changelog entry.

After the version-bump PR merges, check out `origin/main` and run `just release --dry-run`, then `just release`. It checks the tree is clean and on `origin/main`, runs `just check`, creates and pushes the missing tags (your git configuration signs them) and creates the GitHub release. You run it, not an agent: it publishes.

## Development Setup

```bash
git clone https://github.com/orin-dx/wisp-plugins.git
cd wisp-plugins

# Install pinned documentation-check dependencies (just and pnpm must be on PATH)
just install

# Run every check
just check
```

`just test` runs every `tests/test_*.py` (the list, with what each prevents, is in [`ARCHITECTURE.md` section 11](./ARCHITECTURE.md#11-validation-and-release-model)); add or update the test for the behavior you change. `just --list` shows each check as its own recipe (`just versions`, `just mermaid`, and so on) for running a subset while editing; a Mermaid syntax error is invisible to every other check — it's still valid markdown, `jq` never touches it, and it reads fine as source, so `just mermaid` is worth running on its own after touching a diagram. `just fmt` formats the repo in place with `oxfmt`; `just fmt-check` only verifies. Neither is part of `just check` yet — the repo doesn't have a baseline format pass, so `fmt-check` would fail on unrelated files today.

Before a `git commit`, the repository-local Claude and Codex hook checks immutable schema versions and Codex generated-output freshness. See [`docs/repository-hooks.md`](./docs/repository-hooks.md).

`just check` runs automatically in CI (`.github/workflows/validate.yml`) on every PR and every push to `main`.
