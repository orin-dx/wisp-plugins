# Z2: Non-Claude harness capabilities (research date 2026-10-17)
Tags: [P] primary page read, [S] search summary only, [U] unverified. Several vendor pages returned 403; secondary blogs are [S].

## 1. Capabilities table
| Harness | Capability | Source + tag | Implication for plugin repo |
|---|---|---|---|
| Codex | Skills = SKILL.md folders (.agents/skills); plugins are the install unit bundling skills, MCP, apps, hooks, browser extensions | learn.chatgpt.com/docs/plugins [P]; codemyspec.com/blog/skill-portability [S] | Skills are the shared authoring unit; Codex counterpart can be near 1:1 |
| Codex | Plugin build: portable root plugin.json (Agent Plugins schema), OpenAI-only data under extensions.com.openai; legacy .codex-plugin/plugin.json overlay; marketplace at $REPO/.agents/plugins/marketplace.json | developers.openai.com/plugins/build/plugins [P] | Matches repo's generated .agents/plugins layout; migrate generator toward portable plugin.json + overlay |
| Codex | Reads Claude-format marketplaces (.claude-plugin/*) reportedly | codex.danielvaughan.com plugin-marketplace posts [S] | Verify before dropping the Codex generator; do not rely on it |
| Codex | Custom agents: TOML in .codex/agents/ or ~/.codex/agents/; required name, description, developer_instructions; optional model/effort/disabled capabilities; built-ins default/worker/explorer; [agents] max_concurrent_threads_per_session, default_subagent_model, default_subagent_reasoning_effort | learn.chatgpt.com/docs/agent-configuration/subagents [P] | Markdown role cards must compile to TOML; model tier maps to model/effort fields |
| Codex | Subagents spawn on explicit request or when AGENTS.md/skill says so; CLI /subagents; IDE background-agent panel | same [P] | Orchestrator skills must say "spawn agent X" explicitly; no automatic dispatch |
| Codex | Hooks stable since v0.124 (Apr 2026), ~12 events incl. PreToolUse/PostToolUse/Stop; hooks.json or inline [hooks] in config.toml/requirements.toml | danielvaughan.com hooks guide, turboai hooks docs [S] | Binding gates can be mechanically enforced via a Stop hook on Codex; Claude hooks need a counterpart |
| Codex | Managed git worktree tools (CLI 0.162.0, 2026-10-08); Command Center task pinning; /daemon; parallel read-only tools (0.163.0, 10-15) | learn.chatgpt.com/docs/changelog [P] | Worktree isolation for parallel agents is native |
| Codex | Browser: sandboxed in-app browser; Chrome extension (2026-05-07) with per-thread tab groups, DevTools, authenticated sessions; Computer Use in desktop app | macrumors.com/2026/05/07/openai-codex-chrome-extension; thenewstack.io [S] | Visual verification native on Codex; skills should name the capability, not the tool |
| Codex | Models: GPT-6.1 Sol default since 2026-09-29; Luna fast/narrow; Astra top tier; effort low/medium/high/ultra (Luna to max); GPT-5.5 retired 10-14; Sol Ultrafast 10-08 | changelog [P]; subagents doc [P] | Tier map: haiku/low -> Luna, sonnet/med -> Sol medium, opus/high -> Sol high/ultra or Astra |
| Codex | Autonomy: OpenAI says GPT-6 handles tasks spanning hours or days; Astra about 40 min/task on OSWorld 2.0 (72.6%); no-CoT 50% horizon about 31 min (UK AISI) | openai.com/index/practical-guide-building-gpt-6 [S, page 403]; dev.to Astra article [P]; lesswrong [S] | Long-run claims are vendor claims; gates must not assume uninterrupted runs; keep durable artifacts on disk |
| Codex | Guardian safety reviews, Code Mode, Instant Interrupt, Multi-agent V2 (also on Bedrock) | changelog [P] | Runtime-level review exists; do not duplicate |
| OpenAI SDK | Agents SDK (py 0.24.0 2026-10-15; TS 0.20.0): handoffs, agents-as-tools, input/output guardrails, tracing spans, sandbox agents with manifest files + resumable sessions; Responses API default | openai.github.io/openai-agents-python; developers.openai.com/api/docs/guides/agents/sandboxes [S] | Role cards + schema-first handoffs map to handoffs + output_type; usable as an eval harness |
| Antigravity (AGY) | Plugins: required plugin.json ($schema antigravity.google/schemas/v1/plugin.json, name), optional mcp_config.json, hooks.json, skills/, agents/, rules/; no Workflows | antigravity.google/docs/plugins [P] | Repo's AGY plugin shape is close; verify hooks/mcp filenames against our layout |
| AGY | `agy plugin install <name>@antigravity-plugins-official`, GitHub URL or local path; marketplace UI + /plugin; third-party marketplace.json schema NOT in public docs | antigravity.google/docs/marketplace [P] | Marketplace schema reference is a verification gap/risk |
| AGY | Antigravity 2.0 (I/O May 2026): desktop app with Manager, CLI (Go), SDK; dynamic subagents on Gemini 3.5 Flash; Artifacts (task lists, plans, screenshots, recordings) | cybernews.com, tosea.ai [S] | Artifacts are native evidence objects; our evidence schema should be attachable as AGY artifacts |
| AGY | Browser subagent: real Chrome, click/type/console/DOM, screenshots + videos saved as commentable artifacts | antigravity.google/docs/ide/browser, /screenshots [S] | Native visual verification; scripting capture is redundant here |
| AGY | Gemini CLI retired 2026-06-18; extensions import as plugins; reads GEMINI.md and AGENTS.md | developers.googleblog.com transition post [S] | Drop a separate Gemini CLI extension target |
| AGY | Workflows stop working 2026-10-19 | search summary of Google docs [S] | Do not author workflows; skills only |
| Cursor | Cursor 3 (2026-04-02): Agents Window, parallel local/cloud/worktree/SSH agents, Design Mode in built-in browser; Bugbot ~80% resolution claim; Cursor co-authored Agent Plugins 1.0 | medium/dev.to reviews [S]; agent-plugins.org [P] | Design Mode is human-in-loop element selection; complements spec gates |
| GitHub Copilot | Coding agent reads AGENTS.md; custom agents as .github/agents/*.agent.md; skills in CLI/VS Code/coding agent; Agent Plugins support | github.blog changelog 2025-08-28 [S]; devleader.ca [S] | Another markdown role-card format; same compile-from-role-card approach |
| Kiro / Amp / Warp / Windsurf / JetBrains Air | Kiro: specs, steering, hooks, skills, powers; Amp: Oracle subagent; Warp: Oz cloud orchestration; Windsurf Cascade; Air details not found | augmentcode.com, builder.aws.com [S]; Air [U] | Reach via AGENTS.md + SKILL.md only; no bespoke targets |

## 2. Standards state
- Agent Skills: open since 2025-12-18, 16+ tools by mid-2026 [S].
- AGENTS.md: 60k+ repos; governed with MCP under AAIF (Linux Foundation, Dec 2025) [S].
- Agent Plugins 1.0.0 (2026-08-06) by Amazon, Cursor, Microsoft, OpenAI, Vercel: plugin.json + skills/ + mcp.json + reverse-domain extension namespaces. Explicitly excludes hooks, commands, agents, marketplaces, permissions, trust. Working draft. Clients: ChatGPT, Codex, Cursor, Copilot, Kiro, VS Code [P: agent-plugins.org, aaif.io/blog/from-skills-and-tools-to-portable-agent-plugins]. Claude Code and AGY not named as adopters.
- MCP 2026-07-28 [P: blog.modelcontextprotocol.io/posts/2026-07-28]: stateless core, Mcp-Method/Mcp-Name headers, Multi Round-Trip Requests (input_required, replaces server-initiated elicitation streams), Tasks extension (poll-based), MCP Apps in Extensions framework, cache hints, CIMD auth; Roots, Sampling, Logging deprecated (12-month window).
- A2A v1.0 (Mar 2026), joined AAIF Aug 2026 [S]. Zed Agent Client Protocol (editor-to-agent) distinct and active [S]. llms.txt not researched [U].

## 3. Evals on front-end / visual verification
- VISTA (arXiv 2605.26144) [P abstract]: 14 deployed agent systems; best web joint score 0.553, Android 0.378; 44.5% of trajectories never examined design screenshots; 73.0% skipped prescribed self-audits; 8.3% reported success despite failed checks; unresponsive controls in 90.1% of audited web deliveries.
- Vision2Web (arXiv 2603.26648) [P]: Claude-Opus-4.5 best (58.9 visual score desktop; 57.6 full-stack); mobile/tablet 10-20% lower; weak at aligning repeated components and color.
- Also 1D-Bench, FronTalk, EvoGenUI-Bench, ProgramDistill [S, unread]. No head-to-head Claude Code vs Codex vs AGY UI eval found; do not claim one.

## 4. Portability analysis
Survives: SKILL.md body, name/description, references/scripts directories, MCP servers, AGENTS.md prose, JSON Schemas (ours, harness-neutral), Agent Plugins core.
Does not survive [S: codemyspec.com, agensi.io]: Claude frontmatter (allowed-tools, model, effort, context: fork, agent:, hooks, dynamic command injection), skill-level hooks (other agents ignore them), install paths (.claude/skills vs .agents/skills vs ~/.gemini/antigravity/skills), subagent definition format (md vs TOML vs .agent.md), workflows, marketplace schema. Agent Plugins deliberately omits hooks/agents/marketplaces, which is exactly what our repo depends on, so those stay per-harness.
Ship-once precedents: shadcn ships 10 skills over Figma + shadcn MCP for Claude/Cursor/Codex/OpenCode [S]; Salesforce SLDS ships an MCP toolset + 3 first-party skills with bundled JSON registries via npm [S]; Adobe Spectrum ships design-data MCP + a skill [S]; Primer evidence thin [U]. Pattern: knowledge lives in MCP/data registries, thin SKILL.md on top, no per-harness agent logic.
Enforcement differs: Codex and Claude hooks can make gates binding; Cursor/Copilot/AGY gate by prose and artifacts only. Binding judgment should therefore live in a schema-validated verdict artifact checked by a script.

## 5. What each harness natively does that our plugins re-implement
- Parallel subagents + worktrees (Codex, Cursor 3, AGY Manager): keep only the handoff contract, not dispatch prose.
- Browser/screenshot/recording capture (Codex Chrome ext + in-app browser, AGY browser subagent, Cursor browser): specify required evidence, let the harness capture.
- Plan/task-list artifacts (AGY Artifacts): plan@1 is analogous; make attachable.
- Review/fix loops (Bugbot, Codex Guardian): do not rebuild.
- Spec-driven workflow (Kiro specs/steering): overlaps scribe/navigator; ours differs via falsifiable criteria and binding gates.
- Tracing/guardrails/handoffs (Agents SDK): our verdict/handoff schemas are the portable analog.
Not found natively anywhere: falsifiable-criterion specs, adversarial refutation, fail-by-default binding gates, enforced self-audit (VISTA shows agents skip it). That is the differentiator.

## 6. Standards to adopt
1. Agent Plugins 1.0 portable plugin.json as manifest core, vendor data under reverse-domain extensions; keep generated Codex overlay until verified redundant.
2. Restrict portable SKILL.md frontmatter to name/description (+ when_to_use); move Claude-only fields to overlay.
3. AGENTS.md canonical; CLAUDE.md/GEMINI.md thin pointers.
4. MCP 2026-07-28 for any server we ship: stateless, Tasks for long checks, MRTR instead of elicitation, MCP Apps optional for verdict UI; avoid Sampling/Roots/Logging.
5. Keep JSON Schema handoffs ours; A2A Agent Card only if cross-vendor calls appear.
6. Add a capability-matrix check: skills declare required capabilities (browser, subagent, hook); generator fails if a target lacks one.
7. Anti-VISTA gate rule: no pass without screenshot/evidence refs and an executed self-audit.

## Gaps
Cursor and Copilot specifics are secondary-source only; JetBrains Air, llms.txt, Primer, Windsurf, Warp not verified; AGY marketplace.json schema undocumented publicly; Codex loading .claude-plugin formats unverified on a primary page; GPT-6 multi-hour autonomy figures are vendor claims I could not read (openai.com 403).
