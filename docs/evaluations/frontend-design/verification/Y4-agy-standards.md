# Y4: AGY / Agent Plugins / MCP / Skills conformance (2026-10-17)
Tags: [P] primary page read in full or the relevant section; [S] search summary; [I] my inference. WebFetch summarised pages through a small model, so quotes are from the fetch output (Playwright innerText for agent-plugins.org spec and AGY marketplace CLI tab = verbatim).

## 1. Verified facts
| Fact | Quote (<=25 words) | URL | Tag |
|---|---|---|---|
| AGY plugin layout | plugin.json required; optional mcp_config.json, hooks.json, skills/, agents/, rules/ | https://antigravity.google/docs/plugins | P |
| AGY plugin.json fields: only name (required by CLI, `^[a-zA-Z0-9-_]+$`), description, $schema (optional) documented | "$schema": "https://antigravity.google/schemas/v1/plugin.json" | same | P |
| The documented v1 plugin $schema URL returns 404 when fetched | HTTP 404 | https://antigravity.google/schemas/v1/plugin.json | P |
| The $schema this repo's root marketplace.json uses returns 404 | HTTP 404 | https://antigravity.google/schemas/marketplace.json | P |
| AGY marketplace: only the official one; no third-party marketplace.json documented | "<marketplace-name> only supports the official marketplace, antigravity-plugins-official" | https://antigravity.google/docs/marketplace?tab=cli | P |
| AGY install paths: official, GitHub URL ("clone and stage a plugin"), local dir | agy plugin install https://github.com/<owner>/<repo> | same | P |
| AGY manual plugin locations | .agents/plugins/ (workspace), ~/.gemini/config/plugins/ (global) | /docs/plugins | P |
| AGY skills: description required, name optional (defaults to folder) | name: No; description: Yes | https://antigravity.google/docs/skills | P |
| AGY skill dirs: workspace .agents/skills; CLI plugin skills ~/.gemini/antigravity-cli/plugins/<name>/skills/ | Plugin-provided: ~/.gemini/antigravity-cli/plugins/<name>/skills/ | /docs/skills | P |
| AGY rules: .agents/rules/, AGENTS.md, GEMINI.md; modes always_on/model_decision/glob/manual; 24 KB per file, 20k-token aggregate | Per-file: 24 KB maximum | https://antigravity.google/docs/rules | P |
| AGY subagent files: .agents/agents/<name>.md; frontmatter name, description, tools (e.g. view_file), model inherit/flash/pro, commandExecutionPolicy, subagent/mainAgent; nesting depth 10 | model: inherit, flash, or pro | https://antigravity.google/docs/subagents | P |
| AGY workflows stop working 2026-10-19; /migrate-workflows; skill wins on name clash | Legacy workflows will stop working on "October 19, 2026" | https://antigravity.google/docs/migration/workflows-to-skills/ | P |
| A search summary claimed Nov 1, 2026; primary page says Oct 19 | (contradicts primary) | search result | S, superseded |
| AGY browser subagent drives local Chrome in separate profile; screenshots and action videos saved as artifacts | "saving action videos as interactive artifacts" | https://antigravity.google/docs/ide/browser | P (redirect page, thin) |
| AGY models: Gemini 4 Argon, 3.8 Flash, 3.7 Flash/3.1 Pro (enterprise), Claude Sonnet 5.5/Opus 5.5, GPT-OSS-120B; thinking Low/Medium/High | Users can adjust reasoning depth: Low, Medium, High | https://antigravity.google/docs/models | P |
| AGY changelog: per-model effort v2.5.0 (2026-07-31); plugin Customizations tab v2.18.1 (09-28); latest read v2.23.0 (10-12) | "Added per-model reasoning effort levels" | https://antigravity.google/docs/changelog | P (first 100k chars of 382k) |
| Gemini CLI consumer serving stops 2026-06-18; extensions become plugins | stop serving requests on June 18, 2026 | techradar / mcp.directory search results | S |
| Agent Plugins 1.0.0 status "Published" (not working draft) | Spec Version: 1.0.0 Status: Published | https://agent-plugins.org/specification | P |
| Manifest closed: permitted top-level fields | $schema, name, version, description, author, homepage, repository, license, keywords, extensions | same | P |
| $schema and name REQUIRED; $schema must be https://agent-plugins.org/schemas/1.0.0/plugin.schema.json | "The required $schema field ... MUST be the canonical identifier" | same | P |
| Unknown top-level field: report and ignore (non-fatal); other schema violation fatal | Clients MUST report and ignore each unknown field | same | P |
| name: 1-64, a-z 0-9 - . only, no -- or .. | Lowercase alphanumeric characters, hyphens, and periods only | same | P |
| author object: only name/email/url, strings | Any other field or value type makes the manifest invalid | same | P |
| Components v1 = skills (skills/<dir>/SKILL.md, no recursion) + MCP (mcp.json only); plugin.json cannot override locations or hold inline config | plugin.json cannot override these locations or contain inline component configuration | same | P |
| Excluded: commands, hooks, agents, rules, LSP "too client-specific"; also distribution, permissions, trust | remain too client-specific for a stable portable contract | same; https://aaif.io/blog/from-skills-and-tools-to-portable-agent-plugins | P |
| Extensions: reverse-domain keys in `extensions`; client files in top-level dir named for namespace | files for com.example.client belong in com.example.client/ | spec 8.2 | P |
| Path containment: symlinks resolving outside plugin root MUST be rejected | clients MUST reject package paths that resolve outside it | spec 4.1 | P |
| Versioning: spec version = both schemas; plugin version semver SHOULD, not enforced | Clients MUST NOT reject a manifest solely because version is not valid Semantic Versioning | spec 5.4, 10 | P |
| Named clients: Kiro, Cursor, Grok Bot, VS Code, Hermes Agent, OpenClaw, NanoClaw, ChatGPT & Codex, GitHub Copilot, OpenHands. NOT Claude Code, NOT Antigravity | (list) | https://agent-plugins.org/compatible-clients | P |
| TSC: Amazon, Cursor, Microsoft, OpenAI, Vercel | initial Technical Steering Committee includes Core Maintainers from Amazon, Cursor, Microsoft, OpenAI, and Vercel | https://agent-plugins.org | P |
| Claude Code manifest lives at .claude-plugin/plugin.json; optional; without it components load from defaults and name comes from marketplace entry | Save the manifest at .claude-plugin/plugin.json under the plugin root | https://code.claude.com/docs/en/plugins-reference | P |
| Claude: unknown top-level plugin.json key stripped, validate warns | the field is stripped and the plugin loads | same | P |
| Claude plugin.json `$schema` accepted and ignored; `skills`/`agents` accept ./ paths (agents = .md files only, no directories) | agents entries must be .md files | same | P |
| Claude marketplace.json requires name, owner, plugins[]; entry needs name + source; unknown fields warn | The file requires a name, an owner, and a plugins array | https://code.claude.com/docs/en/plugin-marketplaces | P |
| Claude subagent frontmatter: name, description, tools, model (sonnet/opus/haiku/fable/id/inherit), effort low..max, memory, maxTurns, isolation, skills, ...; plugin agents lowest priority | effort: low, medium, high, xhigh, max | https://code.claude.com/docs/en/sub-agents | P |
| Claude skill frontmatter all optional; no `version`/`role` keys listed (metadata is the free-form slot) | metadata: {...} Custom YAML for your tooling | https://code.claude.com/docs/en/skills | P |
| Agent Skills spec: required name (<=64, a-z0-9-, no leading/trailing/double hyphen, must match dir) + description (<=1024); optional license, compatibility, metadata (string map), allowed-tools | Must match the parent directory name | https://agentskills.io/specification | P |
| Skills validation tool | skills-ref validate ./my-skill | same | P |
| Skills body guidance: <5000 tokens, <500 lines, refs one level deep | Keep your main SKILL.md under 500 lines | same | P |
| MCP 2026-07-28: stateless core, no initialize, no Mcp-Session-Id, server/discover | Make MCP stateless: remove the initialize/notifications/initialized handshake | https://modelcontextprotocol.io/specification/2026-07-28/changelog | P |
| MCP: Tasks moved to extension io.modelcontextprotocol/tasks (poll tasks/get, tasks/update; tasks/list removed) | Move experimental tasks out of the core protocol and into an official extension | same | P |
| MCP: MRTR replaces server-initiated roots/sampling/elicitation requests | InputRequiredResult (resultType: "input_required") | same | P |
| MCP deprecated: Roots, Sampling, Logging; HTTP+SSE; DCR; 12-month minimum window | minimum twelve-month deprecation window | same | P |
| MCP Extensions framework: {vendor-prefix}/{name}, negotiated in capabilities.extensions, disabled by default; official: MCP Apps, Tasks, Skills over MCP, auth | Extensions are always disabled by default and require explicit opt-in | https://modelcontextprotocol.io/docs/extensions/overview | P |
| AGENTS.md: no required fields, nested files take precedence, stewarded by AAIF (Linux Foundation), 60k+ projects | No required fields exist | https://agents.md | P |
| llms.txt: agentskills.io, modelcontextprotocol.io and code.claude.com each publish /llms.txt as their doc index (publisher adoption confirmed; no standards-body status verified) | Fetch the complete documentation index at: .../llms.txt | those sites | P (adoption only) |
| Cursor: two formats; Agent Plugins = root plugin.json (skills, MCP); Cursor Plugins = .cursor-plugin/plugin.json (rules, agents, commands, hooks too) | Cursor Plugins: .cursor-plugin/plugin.json | https://cursor.com/docs/plugins | P |
| Copilot skills paths: .github/skills, .claude/skills, .agents/skills; personal ~/.copilot/skills, ~/.agents/skills | Project skills: .github/skills .claude/skills .agents/skills | https://docs.github.com/en/copilot/concepts/agents/about-agent-skills | P |
| Kiro skills: .kiro/skills/, ~/.kiro/skills/; SKILL.md name+description | Skills can exist in two locations | https://kiro.dev/docs/skills/ | P |
| JetBrains Air: shared .agents/skills; per-agent .claude/skills, .codex/skills, .gemini/skills; hosts Codex, Claude Agent, Gemini CLI, Junie; layered AGENTS.md read | Shared skills are stored in .agents/skills | https://www.jetbrains.com/help/air/skills.html | S (search snippet) |

## 2. CORRECTIONS vs Z2-other-harnesses.md
1. Z2 AGY row: "$schema antigravity.google/schemas/v1/plugin.json, name required". Fix: only `name` is required (by the CLI); `$schema` and `description` optional; the v1 schema URL itself 404s, so it cannot validate anything. Unlisted fields are undefined in AGY docs.
2. Z2 gap "marketplace.json schema undocumented" is understated. Primary docs say the CLI marketplace-name suffix supports ONLY antigravity-plugins-official. No third-party marketplace mechanism is documented. A search snippet says "marketplace defined by marketplace.json with relative paths, GitHub repos" [S, unconfirmed on a Google page]. The repo's `$schema` URL 404s.
3. Z2 "Agent Plugins 1.0.0 ... Working draft": spec says Status: Published.
4. Z2 "Cursor, Copilot specifics secondary-only": now [P]. Cursor has two plugin formats; Copilot reads .claude/skills and .agents/skills.
5. Z2 "Antigravity 2.0: dynamic subagents on Gemini 3.5 Flash": AGY models page lists Gemini 4 Argon / 3.8 Flash; no 3.5 Flash. Model names in Z2 are stale or from secondary sources.
6. Z2 workflows date [S] -> now [P] 2026-10-19 (migration page). A conflicting Nov 1 date in a search summary is wrong or stale.
7. Z2 "Agent Plugins ... named clients: ChatGPT, Codex, Cursor, Copilot, Kiro, VS Code": full list also includes Grok Bot, Hermes Agent, OpenClaw, NanoClaw, OpenHands.
8. Z2 "Agent Plugins excludes hooks, commands, agents, marketplaces, permissions, trust": spec lists commands, hooks, agents, rules, LSP as out-of-v1 component types; AAIF blog lists distribution (registries, marketplaces), runtime (permissions, sandbox, UI), trust, client-specific. Both true; `rules` was missing.
9. Z2 "Restrict portable SKILL.md frontmatter to name/description (+ when_to_use)": `when_to_use` is not in the Agent Skills spec. Spec optional fields are license, compatibility, metadata, allowed-tools. Use `metadata` for version.
10. Z2 JetBrains Air [U]: Air reads shared .agents/skills and per-agent skill dirs including .claude/skills and .gemini/skills, and AGENTS.md [S].
11. Z2 MCP row correct; additions: server/discover, Tasks is an extension (not core), `extensions` negotiated per request, 12-month deprecation floor.

## 3. Conformance table (this repo)
| File | Field / convention | Issue | Spec ref | Severity |
|---|---|---|---|---|
| marketplace.json (root, AGY) | `$schema` https://antigravity.google/schemas/marketplace.json | URL 404; no such schema documented | AGY /docs/marketplace | High (false authority) |
| marketplace.json (root) | whole file | AGY documents no third-party marketplace.json; CLI marketplace suffix = official only. File is read by nothing documented | AGY marketplace CLI tab | High: it is a repo-private manifest, not an AGY artifact |
| marketplace.json plugins[] | `id`, `path`, `version`, `supersedes` | Not in any documented spec; `supersedes` meaningful only to our tooling | n/a | Medium |
| .claude-plugin/marketplace.json | `$schema` anthropic.com/claude-code/marketplace.schema.json | Not verified (not fetched); Claude docs do not list a marketplace $schema; likely ignored | Claude marketplace docs | Low [I] |
| .claude-plugin/marketplace.json | name/description/owner/plugins, entries name+source(git-subdir url,path,ref) | Conforms to required fields; no `version` in entries (version comes from plugin manifest) | Claude marketplace docs | OK |
| plugins/*/plugin.json | location = plugin root | Claude Code reads only .claude-plugin/plugin.json; root plugin.json is invisible to Claude (name falls back to marketplace entry; version/description/author lost) | Claude plugins-reference | High |
| plugins/*/plugin.json | location = plugin root | Same location IS what Agent Plugins, AGY, Cursor-AgentPlugins read | Agent Plugins 5.1; AGY plugins | OK for AGY/AP |
| plugins/*/plugin.json | missing `$schema` | Agent Plugins: required, else plugin REJECTED (fatal). AGY: optional | AP 5.3 | High for AP clients |
| plugins/*/plugin.json | `id` | Unknown top-level field: AP reports+ignores; Claude strips+warns; AGY undocumented | AP 5.2 | Low |
| plugins/*/plugin.json | `skills: "./skills/"` | AP: unknown field (fixed location skills/ anyway). Claude: accepted, adds to default scan (duplicate scan of same dir) | AP 6.1; Claude fields | Low |
| plugins/*/plugin.json | `agents: ["./agents/x.md",...]` | AP: unknown, agents excluded. Claude: valid but REPLACES default agents/ scan (fine, list is complete). AGY: undocumented key; AGY discovers agents/ by directory | AP 7; Claude path rules | Low |
| plugins/*/plugin.json | `consumes`, `produces` | Unknown to AP/Claude/AGY; stripped/ignored; used only by our tooling | AP 5.2 | Low |
| plugins/*/plugin.json | `author` {name,email} | Valid in AP and Claude | AP 5.4 | OK |
| plugins/*/plugin.json | `name` | kebab lowercase: valid in all three | AP 5.5, Claude, AGY | OK |
| plugins/*/shared (symlink -> ../../shared) | symlink escapes plugin root | AP: clients MUST reject paths resolving outside root; Claude: component paths must resolve inside; git-subdir/marketplace copy of plugins/<id> gives a dangling link outside the monorepo [I]; `agy plugin install <github-url>` of repo root has no root plugin.json | AP 4.1; Claude path rules | High [I for dangling-copy behavior; unverified by install test] |
| plugins/*/subagents -> agents (symlink) | harmless alias in-root | Duplicate discovery risk if a client scans both; none of the three scan `subagents/` | n/a | Low |
| plugins/*/skills/*/SKILL.md | `name`,`description` | Valid; all 30 names equal dir names; no description over 1024 chars | agentskills spec | OK |
| SKILL.md | top-level `version` (30/30) | Not in Agent Skills spec (should live under `metadata`); Claude ignores; skills-ref may flag unknown key [I, validator not run]; AGY not documented | agentskills spec | Medium |
| plugins/*/agents/*.md | `role`, `effort`, `model: haiku/sonnet/opus` | Claude: role ignored/unknown, effort and model valid. AGY: `model` accepts inherit/flash/pro only (haiku/sonnet/opus invalid or ignored), no `effort`, `tools` uses AGY tool names. Agent Plugins: agents out of scope | AGY subagents; Claude sub-agents | High for AGY: model tiers silently not applied [I on failure mode] |
| plugins/*/agents/*.md | no `tools`, `maxTurns`, `isolation`, `skills` | Claude: all optional; inherits all tools. AGY: tools optional? undocumented | Claude sub-agents | Medium (design, not defect) |
| .agents/plugins/marketplace.json + dist/codex | Codex format | Generated; Agent Plugins portable core not yet adopted (WP-610) | developers.openai.com per Z2 | Info |
| plugin dirs | no hooks.json / mcp_config.json / rules/ | Nothing shipped; fine | AGY plugins | OK |
| (all) | `.claude-plugin/plugin.json` absent in every plugin | Claude installs fine without it (manifest optional) | Claude plugins-reference | Info |

## 4. Minimal convergence manifest
Root `plugins/<id>/plugin.json` (valid under Agent Plugins 1.0.0, AGY, Cursor-AgentPlugins; Claude ignores unknown keys):
```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "courier",
  "version": "3.0.3",
  "description": "Shipping plugin ...",
  "author": { "name": "Gabriel Castro (Orin DX)", "email": "gabe@techworx.dev" },
  "license": "MIT",
  "repository": "https://github.com/orin-dx/wisp-plugins",
  "keywords": ["shipping"],
  "extensions": { "dev.orindx.wisp": { "consumes": [], "produces": ["changeset@2","release-artifact@2"], "agents": ["./agents/changeset-analyzer.md"] } }
}
```
- Drop top-level id/skills/agents/consumes/produces (move to `extensions.<reverse-domain>`; our tooling reads from there).
- Claude: add `.claude-plugin/plugin.json` (can be a copy minus `$schema`, or the same file via generator) so version/description/author register; optional since Claude auto-discovers skills/ and agents/.
- AGY: same root plugin.json works; agents/ files need AGY frontmatter (model inherit/flash/pro, tools) to take effect, via generated overlay or by relying on defaults (AGY agents with unknown fields: undocumented).
- Replace the `shared` symlink with a generated in-root copy at build time (or hoist references into each plugin).
- Move SKILL.md `version` under `metadata:`; run `skills-ref validate`.
- Marketplace: keep .claude-plugin/marketplace.json (Claude, valid). Delete or relabel root marketplace.json: it is not an AGY artifact; remove the 404 `$schema`.

## 5. PLAN IMPACT vs ARCHITECTURE-REVIEW.md
- Row 12 "AGY's plugin format is similar to Claude's": TRUE for components (plugin.json at root of a dir with skills/, agents/, mcp, hooks, rules); DIFFERENT in: manifest location (root vs .claude-plugin/), manifest fields (AGY documents 3), mcp file (mcp_config.json vs .mcp.json), hooks (hooks.json at root vs hooks/hooks.json), agent frontmatter (flash/pro vs haiku/sonnet/opus), marketplace (official-only vs user marketplaces), install unit (single-plugin repo URL or local dir vs marketplace add). Claude and AGY are not "two trees" today: the repo already ships ONE authored tree that AGY can install per plugin via local path; the real trees are authored, generated Codex (dist/codex, harnesses/codex), and per-harness overlays. Reframe as "one authored tree + generated overlays: Claude manifest, AGY agent/hooks, Codex".
- WP-610 corrections: (a) the portable core is a manifest everyone can read, not a Claude/AGY convergence: Agent Plugins does not name either; AGY follows its own near-superset; (b) required work item: add `$schema` + move custom keys under `extensions` (otherwise AP clients REJECT the plugin, i.e. Cursor/Copilot/Kiro/VS Code/Codex portable installs fail); (c) fix symlink; (d) fix SKILL.md `version`; (e) "re-verify AGY marketplace schema" result: it does not exist publicly; remove it and the 404 `$schema`, and say AGY distribution = `agy plugin install <github-url|local path>` (one repo or subpath per plugin) or the Google-curated official marketplace via the interest form.
- AGY install of the monorepo by GitHub URL cannot work as-is (no plugin.json at repo root); document `agy plugin install plugins/<id>` locally or publish per-plugin repos [I: GitHub-subdir install is not documented].
- WP-616: AGY workflow date confirmed [P] 2026-10-19; this repo ships no workflows, so no action. Claude has its own `workflows` plugin component (JS) unrelated to AGY workflows: do not conflate.
- WP-607 evidence: AGY browser subagent saves screenshots and videos as artifacts [P, thin page]; Gemini model names in Z2 are stale.
- MCP (WP-614): spec is 2026-07-28; Tasks and MCP Apps are Extensions (opt-in, negotiated); Skills over MCP extension exists and could ship skills with a server; the Agent Plugins mcp.json uses its own closed schema (`type` required, `mcpServers`, `${PLUGIN_ROOT}`) distinct from Claude `.mcp.json` and AGY `mcp_config.json`: three MCP config file names.
- Skill portability: AGY, Copilot, Kiro, Air, Cursor, Codex all load Agent Skills folders; paths differ (.agents/skills is the common one: AGY, Copilot, Air). Authoring skills into `.agents/skills`-compatible form is the widest reach. Rules/hooks/agents remain per-harness.
- Unverified: whether Claude, AGY actually reject/warn on `role`, `version`; install behavior of dangling symlink; skills-ref strictness; Cursor/Copilot/Kiro install of our layout (Cursor and AP clients would reject for missing `$schema`; Copilot/Kiro plugin load unverified).
