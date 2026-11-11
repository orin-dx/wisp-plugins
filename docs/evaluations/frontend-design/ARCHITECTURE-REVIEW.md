# Architecture review against current agent capabilities

Status: proposal, revised after primary-source verification (section 7.1 and `verification/Y1` to `Y6`, `VERIFY-3`). Nothing here changes a plugin, schema, constitution or ADR. It tests each architectural assumption in `ARCHITECTURE.md` against what the current agent platforms can do, and adds the work packages that follow (WP-601 to WP-616 first, WP-617 to WP-628 after verification; 172 in total with the catalog's 144). Where section 7.1 and an earlier row differ, 7.1 wins.

Inputs: `ARCHITECTURE.md`; `evidence/Z1-claude-platform.md` (Claude Code and Anthropic engineering guidance); `evidence/Z2-other-harnesses.md` (Codex, Antigravity, Cursor, Copilot, standards); repo measurements taken for this review (section 1). Claims tagged [P] were read on a primary page, [S] come from a search summary, [I] are inference. Z1 read only the first 100k characters of the hooks and subagents pages, and the fetch tool summarizes pages, so quotes are the fetcher's wording.

## 0. Corrections to earlier statements

1. **The constitution is not 290 lines per agent.** Every one of the 44 agents embeds the same 6-line `<constitution>` block (one distinct block, checked by hash). The 290-line `shared/constitution.md` is the authoring-time rulebook; among agents only the `mason` auditor reads it at runtime. The research notes and `traceability/MAP-5-M-X.md` assumed a 290-line copy per agent, and so did my earlier summaries. The per-agent cost is about 6 lines. This lowers the priority of the "shrink the constitution" ablation (WP-62, ADR N10). See section 2, row 3.
2. **Cross-harness shape (from the user).** Codex has its own native plugin format, set up in this repo under `harnesses/codex/`; AGY's format is similar to Claude Code's and shares the authored tree. The cost is therefore one authored tree for Claude and AGY plus one native Codex tree, not three. The AGY risks are specific (section 6), not a third tree.
3. **Agent descriptions are inside the platform's budget.** Descriptions across the 44 agents total 26,908 characters, about 6.7k tokens by a 4-characters-per-token estimate, against a 15,000-token cap on all agent descriptions [P per Z1]. That is about 45% of the cap. There is headroom, but every agent added (the structure decision proposes 3) draws on the same budget, so keep descriptions short.

## 1. Where the repo stands (measured)

| Fact | Value |
| :-- | :-- |
| Plugins / skills / agents | 10 / 30 / 44 |
| Agent frontmatter keys in use | `name`, `role`, `model`, `effort`, `description` only. No `tools`, `maxTurns`, `isolation`, `skills`, `memory` or other native controls |
| Tier distribution | sonnet/medium 27, opus/high 8, haiku/low 7, `claude-fable-5-1`/high 2 |
| Skill frontmatter keys | `name`, `description`, `version` |
| Plugin-shipped hooks, `bin/` validators, workflows, LSP servers | none (the repo has a commit-time integrity hook for its own development only) |
| Distinct `<constitution>` blocks across agents | 1 (6 lines) |
| Average agent body | about 4.4k characters |
| Orchestration | skill prompts that spawn subagents; retry counter lives in `verdict@3` and is incremented by the exit-gate agent |

## 2. Assumption ledger

Verdicts: **Keep**, **Change**, **Test first** (evidence is mixed; measure before deciding), **Lower priority**.

| # | Assumption (where it lives) | What current platforms and evidence say | Verdict | Work |
| :-- | :-- | :-- | :-- | :-- |
| 1 | Context is scarce; load references on demand (`ARCHITECTURE.md` section 1) | Skills are progressive disclosure natively; Anthropic's context-engineering guidance asks for the minimal information that fully outlines behavior [P per Z1]. Subagent frontmatter can preload skills | **Keep** | WP-606 (use native preload where it helps) |
| 2 | One agent per cognitive mode (ADR 003) | Anthropic's guide calls splitting by role (planner, implementer, tester, reviewer) an anti-pattern and recommends splitting by *context* [P per Z1]. Verifier and adversary splits are justified by independent context. Multi-agent runs cost about 15x chat tokens in one post and 3 to 10x single-agent in a later guide; it underperforms on tightly coupled work, "most coding tasks" included. A multi-agent research setup beat single-agent Opus 4 by 90.2% on an internal eval. No vendor test of 40-plus role agents in a linear pipeline exists | **Test first** | WP-605, WP-601 |
| 3 | A byte-identical constitution is the shared cache prefix (ADR 006) | The block is only 6 lines, so its cost is small whatever it saves. Cache prefixes are shared only between requests with the same model, effort, agent type, tools, schema and working directory, and subagent caches default to a 5-minute TTL [P per Z1], so the cache benefit across 44 differently configured agents is probably small [I]. The drift guard (byte-identity check) already exists | **Lower priority** | WP-62 retargets to backstory and skeleton; WP-604 only measures |
| 4 | Capability tiers by model and effort (`ARCHITECTURE.md` section 5) | Effort is a native per-agent control; defaults differ by model (Fable 5.1 high, Opus 5.5 medium, Sonnet 5.5 high on the API, Haiku 5.5 medium); Opus 5.5 at medium roughly matches Opus 5 at high per Anthropic. Pricing per million tokens: Fable 5.1 $10/$50, Opus 5.5 $4/$20, Sonnet 5.5 $2/$10 [P per Z1]. Two agents already run on Fable 5.1 | **Keep as hints; re-measure** | WP-63 |
| 5 | JSON schemas are the inter-agent contract, with a mandatory `reasoning` scratchpad (ADR 004) | Schemas remain the portable contract across harnesses. Workflow scripts can pass a JSON schema to `agent()` with validation retries, and a `SubagentStop` hook can run a validator [P per Z1]. Anthropic names a `reasoning` field as a refusal trigger; first-hand (`VERIFY-3`): the real drafter prompt with its scratchpad field completed normally twice, only a demand for verbatim reasoning was refused, and 72k+ transcript messages show no refusals | **Keep schemas; change enforcement; test the field first** | WP-602, WP-61 |
| 6 | Default-fail gates with a retry cap of 3, then a human (`ARCHITECTURE.md` section 6) | The gate concept is a differentiator no harness provides natively (section 5). But a prompt-based gate is only a request: in the `pages` session the cap was not enforced. Anthropic's harness post says evaluators drift lenient and the multi-agent guide names the "early victory problem"; VISTA found 8.3% of agents claiming success despite failed checks [P abstract per Z2]. `Stop`, `SubagentStop` and `TaskCompleted` hooks can block with a reason, and the hook can hold a counter a model cannot reliably keep | **Keep the gate; make it deterministic** | WP-602 |
| 7 | Orchestration is a skill prompt that spawns subagents | Every result lands in the orchestrator's context. Plugins can ship workflow scripts (`agent()`, `pipeline()`, `parallel()`) that keep state outside the model, are resumable, and allow 16 concurrent agents and 1,000 agents per run [P per Z1]; they run in the CLI, headless mode and the SDK. Not portable: Antigravity workflows stop on 2026-10-19 [S per Z2], and Codex has no equivalent plugin construct | **Change on Claude; keep the skill as the cross-harness path** | WP-603 |
| 8 | Work is a sequential pipeline of ten plugins | Testimonials (not controlled benchmarks) report 18-plus-hour unattended runs on Opus 5.5 and a 38-hour run on Fable 5.1 [P per Z1]; Anthropic's harness post reports a simplified harness (sprint construct removed; planner and evaluator kept) at 3h50m and $124.70 on Opus 4.6, against an earlier 6h/$200 run on Opus 4.5 with a different prompt; it is not a before/after on one task and was not re-checked on 5.x. Stage granularity tuned for short horizons will not stay right | **Change: make stages elidable, gates at boundaries** | WP-608, WP-18 |
| 9 | Plans carry exact implementation code (navigator, ADR 009) | Anthropic says prescriptive skills "can degrade output quality" on Fable 5 [P]; plans of 60 to 130 KB stalled agents in the sessions (VERIFY-1: 17 failed tasks in the `orin-dx` session) | **Change: outcome-level plans** | WP-608, WP-36 |
| 10 | Verification evidence is text, code and tests; "render" is only a label | Browser capture is native in Claude Code, Codex, Antigravity and Cursor [S for most]; VISTA found 44.5% of trajectories never looked at the design screenshots and 73% skipped prescribed self-audits | **Change** | WP-607 |
| 11 | Agents are stateless across sessions | Subagents can have persistent `memory`; plugins have a persistent data directory; routines and scheduled runs exist [P per Z1] | **Change** | WP-612 |
| 12 | One lifecycle contract, two source trees | Agent Plugins 1.0.0 (2026-08-06) standardizes the portable core (root `plugin.json`, `skills/`, `mcp.json`) and excludes hooks, commands, agents, marketplaces and permissions [P per Z2]. Claude Code and AGY are not named in it; AGY's plugin format is similar to Claude's | **Keep two trees; narrow the duplication** | WP-610 |
| 13 | Humans approve through written artifacts | Rendered review surfaces exist (Artifacts, MCP Apps, Claude Design handoff); the user asked for pictures repeatedly | **Change** | WP-614, WP-34 |
| 14 | Agents use platform controls only through `model` and `effort` | Native controls available: `tools` allowlists, `maxTurns`, `isolation: worktree`, `skills` preload, `memory`, `omitClaudeMd`. Plugin-shipped agents ignore `hooks`, `mcpServers` and `permissionMode` [P per Z1] | **Change** | WP-606, WP-615 |

## 3. What the harnesses do natively and what we re-implement

| Capability | Native | In this repo today | Call |
| :-- | :-- | :-- | :-- |
| Parallel agents and worktrees | Claude `isolation: worktree`; Codex managed worktrees (CLI 0.162.0); Antigravity parallel agents | File ownership is prose in plans; no worktree isolation | Adopt natively (WP-606, WP-55) |
| Browser capture and screenshots | Claude built-in browser and Chrome extension; Codex in-app browser; Antigravity browser subagent with Artifacts; Cursor browser | None | Capability-detected adapters (WP-607) |
| Plugin evals with a no-plugin baseline | `claude plugin eval` runs each case 3 times with and 3 without the plugin [P per Z1] | `mason:evaluate` with hidden-oracle fixtures | Complementary: native gives the baseline, ours gives cross-harness fixtures (WP-601) |
| Deterministic gates | Hooks (33 events on Claude [P]; 12 events on Codex [P]; `hooks.json` in AGY plugins) | One repo-level commit hook; none shipped in plugins | Adopt (WP-602) |
| Orchestration scripts | Claude workflow scripts; Codex Agents SDK | Skill prompts | Adopt on Claude (WP-603) |
| Review bots and plan artifacts | Cursor Bugbot, Copilot review, Antigravity plan Artifacts | `ranger`, `sentinel`, `navigator` | Keep; ours add refutation and falsifiable gates |
| Code intelligence | LSP servers can be bundled in Claude plugins [P per Z1]; Netflix and JetBrains report 20 to 30% efficiency gains for Java | Language-service guidance in smith (commit `f10e6b8`) | Extend to UI facts (WP-611) |

## 4. Platform features this repo does not use yet

Plugin-level hooks as gates; `claude plugin eval` with a no-plugin baseline; plugin-shipped workflows; `bin/` validators; `SendMessage` resume for repair loops; `isolation: worktree`; per-agent `maxTurns` as a stall guard; `tools` allowlists; `skills` preload; subagent `memory` and a persistent plugin data directory for counters; plugin `dependencies`; routines for drift checks; bundled LSP servers.

## 5. Differentiators to protect

The harnesses natively do parallel agents, worktrees, browser capture, plan artifacts and review bots. None of them provides falsifiable specs, adversarial refutation, fail-by-default binding gates, or enforced self-audit [S per Z2]. These are why the plugins exist. The direction below moves the *enforcement* of those properties out of prose and into deterministic harness features, and leaves the properties themselves unchanged.

## 6. Direction: thinner prompts, thicker harness

1. **Move enforcement out of prose.** Retry caps, schema validity, "no pass without evidence refs" and self-audit become hook- or workflow-enforced where the harness allows, with the prompt-only path as the cross-harness fallback.
2. **Split agents by context, not by role.** Keep splits that buy independent or high-volume context (verifier, adversary, recon). Audit the rest against that criterion with a measured baseline.
3. **Design for longer autonomy.** Plans state outcomes, ownership and verification; progress is a resumable artifact; gates sit at boundaries, not inside every step.
4. **Make capabilities pluggable and detected.** Browser, worktree, memory and design-source access are adapters selected by capability, with identical artifacts out (`render-evidence`, `design-source`).
5. **Keep schemas as the cross-harness contract,** and share skill bodies where orchestration semantics are identical.
6. **Record the assumptions.** A register of what each component assumes the model cannot do, reviewed on each model generation (WP-609), so stale scaffolding is retired on evidence.

Cross-harness specifics:
- **Codex:** native plugin format under `harnesses/codex/`; custom agents are natively TOML [P], and this repo's policy keeps role cards as markdown resources (ADR N8 decides whether an optional generator may emit TOML). Subagents spawn only when asked or when a skill or AGENTS.md instructs it, so Codex orchestrator skills must say so. Re-check the generated tree against the new `extensions.com.openai` convention [P per Z2].
- **AGY:** plugin fields `plugin.json` (with `$schema`), optional `mcp_config.json`, `hooks.json`, `skills/`, `agents/`, `rules/`; workflows are not supported in plugins and stop working on 2026-10-19 [S], so author skills only. The public docs do not document the third-party marketplace schema, so the `$schema` reference in the root `marketplace.json` needs re-verifying [P per Z2]. Gemini CLI was retired in June [S].
- **Standards:** AGENTS.md, the Agent Skills `SKILL.md` standard, MCP 2026-07-28 (stateless core; Roots, Sampling and Logging deprecated), and Agent Plugins 1.0.0 as the portable manifest core.

## 7. New work packages

WP-601 to WP-616 are appended to the catalog's 144 (160); section 7.1 adds WP-617 to WP-628 (172). Waves follow `CATALOG.md` section 3.

| ID | Title | Scope | Extends | Type | Size | Wave |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| WP-601 | Plugin eval suite with a no-plugin baseline | `claude plugin eval` cases run with and without each plugin, including variants that collapse agents; run in CI; cost budget | WP-60 | eval | M | 0 |
| WP-602 | Deterministic gate enforcement | Plugin hooks: a `SubagentStop` schema validator, `Stop`/`TaskCompleted` blocks, retry counters in persistent plugin data with a loop guard; parity for Codex hooks and AGY `hooks.json`; prompt path stays as fallback | WP-51, WP-512 | tooling | L | 2 |
| WP-603 | Plugin-shipped workflow scripts | Orchestration for the main pipelines as resumable workflow scripts with schema-checked `agent()` calls (Claude); skills remain the cross-harness path; no AGY workflows | WP-55 | tooling | L | 2 |
| WP-604 | Constitution block cost and cache check | Measure whether the 6-line block shares a cache prefix in practice and whether the drift guard is worth keeping; no change unless net benefit is shown | WP-62 | eval | S | 4 |
| WP-605 | Agent-count audit by context isolation | Classify each of the 44 agents as an independent-context split or a role-flavor split; test collapsed variants with WP-601 | ADR 003 | eval | M | 2 |
| WP-606 | Adopt native agent controls | `maxTurns` stall guard, `tools` allowlists, worktree isolation for parallel writers, `skills` preload, per-agent `effort`; per-harness capability matrix in the generator | WP-54, WP-55 | docs/tooling | M | 2 |
| WP-607 | Capability-detected render adapters | Claude built-in browser or Chrome or Playwright MCP, Codex browser, AGY browser subagent with Artifacts, repo-script Playwright; one `render-evidence` artifact out; rule: no pass without evidence refs and an executed self-audit | WP-40, WP-41, WP-307 | schema/tooling | L | 3 |
| WP-608 | Long-horizon harness design | Outcome-level `plan@2`, progress artifacts, resumable runs, gates at boundaries; re-evaluate stage granularity each model generation | WP-36, WP-58 | docs/schema | L | 4 |
| WP-609 | Harness-assumption register | A durable table of each component's assumption, the evidence that retires it, and a review date per model generation (section 2 is the first version) | WP-501 | docs | S | 0 |
| WP-610 | Cross-harness manifest convergence | Adopt the Agent Plugins core where it applies, minimal portable `SKILL.md` frontmatter, shared skill bodies where orchestration is identical, update the Codex manifest convention, re-verify the AGY plugin format and marketplace schema | WP-70, WP-71 | tooling | L | 4 |
| WP-611 | UI code-intelligence layer | A bundled LSP or `bin/` query layer for computed styles, accessibility tree and token and component usage | WP-47, WP-74, WP-312 | tooling | L | 3 |
| WP-612 | Native memory and persistence | Persistent plugin data, subagent memory, repo decision log, routines for drift checks, session search | WP-13, WP-73, WP-201 | tooling | M | 4 |
| WP-613 | Resumed repair loops | Correct a spec by resuming the drafter with `SendMessage` instead of re-spawning; verify handback and context semantics | WP-205 | tooling | S | 2 |
| WP-614 | Rendered review surfaces | MCP Apps or Artifacts as the approval surface; Claude Design handoff import; MCP servers shipped on the 2026-07-28 spec | WP-34, WP-35 | tooling | M | 3 |
| WP-615 | Platform-limit checks in `just check` | Plugin agents ignore `hooks`, `mcpServers`, `permissionMode`; total description budget (15,000 tokens; now about 6.7k); spawn depth 3; concurrency | WP-508 | tooling | S | 0 |
| WP-616 | Verify platform claims | `stop_hook_active` and loop behavior, cache sharing across subagents, Codex reading `.claude-plugin` formats, the 18 to 38 hour testimonials, the AGY dates | WP-90 | research | S | 0 |

### 7.1 Changes after primary-source verification

Sources: `verification/Y1-claude-code-docs.md` (full pages from raw markdown), `Y2-anthropic-primary.md`, `Y3-codex.md`, `Y4-agy-standards.md`, `Y5-design-sources.md`, `Y6-aviation-evals.md`, and `VERIFY-3.md` (first-hand measurements). This section supersedes the rows above where they differ.

**Changes to existing work packages**

| WP | Change |
| :-- | :-- |
| WP-602 (rewrite) | The validator hooks `PreToolUse` or `PostToolUse` with matcher `SubagentHandback` and reads `tool_input.message`: in auto mode (since Claude Code 2.1.271) subagents deliver reports through that tool and a `SubagentStop` hook's `last_assistant_message` holds only the closing text. Scope matchers (for example `^scribe:exit-gate$`) because plugin hooks fire for every subagent. A hook that fails or times out does not block unless `onFailure: "block"` (needs 2.1.295; local CLI is 2.1.292), so also use exit code 2. Stop-hook continuations are hard-capped at 8 in a row (reset by a tool call) and past the cap the turn ends, which looks like a pass, so the retry counter of 3 lives in the hook and the gate is also checked on artifacts. Codex: a Stop `decision: "block"` injects a continuation prompt, `stop_hook_active` is the loop guard, `continue: false` wins, a PreToolUse failure fails open, hooks need user trust review, and plugin hooks are not supported under cloud orchestration. AGY: `hooks.json`. |
| WP-603 | Plugins ship `workflows/*.js`, run as `/plugin:name`. In headless `-p` mode a workflow needs a `Workflow` allow rule, `AskUserQuestion` is stripped, subagents run in the background by default, and resume is same-session only, with no `import` or clock calls in scripts. Human escalation must happen in the main session. |
| WP-606 | Drop the assumption that an `Agent(x,y)` allowlist restricts subagents: it applies only to a main-thread `claude --agent`. Keep `maxTurns`, `tools`, `isolation`, `skills` preload, per-agent `effort`. Plugin agents ignore `hooks`, `mcpServers`, `permissionMode` and `initialPrompt`. Spawn depth is 3 and concurrency 20, with no cap on total spawns. |
| WP-610 | Narrowed to Codex/AGY/standards convergence and split across WP-620 to WP-623. |
| WP-615 | Validate with an explicit manifest path (`claude plugin validate plugins/<id>/plugin.json`); the directory form false-passes. Flag unknown keys; make `--strict` pass after WP-620. The 15,000-token description limit is a startup warning, not an error. |
| WP-616 | Shrinks: the Stop-loop question is answered. Remaining: Opus 5.5 and Fable 5.1 probes, Codex loading Claude agents and hooks from `.claude-plugin`, install behavior with the `shared` symlink in each harness, and whether `skills-ref` rejects a top-level `version`. |
| WP-61 / WP-518 | Outcome: keep the `reasoning` field; the trigger is wording that asks for reproduced reasoning. Replace the rename plan with WP-625. |
| WP-60 / WP-402 | Design WP-402 as a matched, blind, holdout benchmark; use a three-arm design (none, terse control, treatment) and the JetBrains ladder (transcript replay, wiring check, k=1 smoke, k=3, full run at each effort). No source gives a general none/skill/MCP/CLI/DESIGN.md result. |
| WP-11 / WP-15 | Adopt the prototype rules of Matt Pocock's `prototype` skill (read in `Y5`): 3 variants by default, cap 5, structurally different, served with a `?variant=` parameter on the real route. This settles the 3-versus-4 options conflict (K1). |
| WP-16 | Drop "taste dials" (the current flagship has none): use a direction draw plus a named-cluster ban list, and Anthropic's two-pass plan (4 to 6 named hex values, type roles, ASCII wireframes, review against the brief). |
| WP-31 / WP-404 / WP-412 | Keep DESIGN.md compatibility, positioned for greenfield work, noting only `broken-ref` is an error in its lint; specify WP-404 from the Adobe and Salesforce scoring formulas; adopt Vercel's promotion ladder (rule, reference, exemplar, lint, eval, coverage gap, no change) with human approval. |
| WP-51 / WP-53 | Use UK CAP 413 vocabulary: CONFIRM (not VERIFY, which is FAA usage), and "OK" is simply not a defined word. Drop the unsourced claims (a duty to report after an emergency deviation; IFR pick-up in flight). Qualify AFIS (UK FISOs may relay clearances and instruct on the movement area) and IFR separation by airspace class. Treat the aviation framing as analogy. |
| WP-65 / WP-68 | Run the brevity instruction as an A/B against a "be concise" control; do not cite the 65% claim or the brevity preprint for agent narration. Lower WP-68: independent tests found no savings. |
| WP-401 | Add flags for vendor-run results, preprints, version drift, volatile counters and stale READMEs. |

**New work packages**

| ID | Title | Scope | Type | Size | Wave |
| :-- | :-- | :-- | :-- | :-- | :-- |
| WP-617 | Fix stale Codex model ids | Replace `gpt-5.6-luna`, `-terra`, `-sol` in `harnesses/codex/agent-roles/README.md` with current ids (`gpt-6-luna`, `gpt-6.1-sol`, `gpt-6-astra`); no mechanical tier translation (harness-authoring policy); check `terra` against current pages | docs | S | 0 |
| WP-618 | Codex delegation wording | Replace "when agent teams are available" and "teammate" in the 18 Codex skills with explicit "spawn subagent <role> with this packet", keep the sequential fallback, say subagents spawn only when told; verify with a behavioral run | skill text | M | 2 |
| WP-619 | Codex read-only enforcement | Role cards cannot enforce read-only (subagents inherit the parent sandbox and approvals); document the sandbox and approval settings the skills require, and check gate output against artifacts | docs/tooling | M | 2 |
| WP-620 | Claude manifest relocation and validation | Add `.claude-plugin/plugin.json` per plugin; move or drop `id`, `consumes`, `produces` (repo-private manifest or an extension namespace); run explicit-path `claude plugin validate` in `just check`; make `--strict` pass | tooling | M | 0 |
| WP-621 | `shared` symlink strategy | Test install behavior per harness; decide build-time copy versus symlink (Agent Plugins forbids paths leaving the plugin root; `validate` does not follow symlinks) | tooling | M | 1 |
| WP-622 | AGY and root marketplace cleanup | Remove the dead `$schema` URLs (both return 404), document the root `marketplace.json` as repo-private, record AGY install forms (local path; a GitHub URL install needs a plugin at the repo root), author skills only because AGY workflows end 2026-10-19 | docs | S | 0 |
| WP-623 | Frontmatter portability | Move skill `version` under `metadata`; decide the doc-only `role` key (no runtime effect); generate AGY agent frontmatter; run `skills-ref` | tooling | S | 1 |
| WP-624 | Hook validator spike | Prototype a `SubagentHandback` validator on one agent with a scoped matcher; measure; precondition for WP-602 | tooling | S | 0 |
| WP-625 | Reasoning-wording lint and periodic probe | Lint agents, skills and schemas for prompts that demand verbatim or step-by-step reasoning; keep the field; re-run the `VERIFY-3` probe on each model generation and on Opus 5.5, Fable 5.1 and Haiku 5.5 | eval/tooling | S | 0 |
| WP-626 | Verified-facts register | A table of external facts with source URL, date, evidence tag and re-verify trigger, cited by the constitution and ADRs; seeded from `verification/` | docs | S | 0 |
| WP-627 | Adopt verified design-file templates | Prototype rules, DESIGN.md front matter with an `omitted` section, Vercel modes, decision-record template and P0 to P3 definitions, Adobe and Salesforce scoring and gate formulas, the Component.MD skeleton and ARIA table, avoid-ai-design rule ids, from `Y5` | docs | S | 1 |
| WP-628 | Aviation vocabulary correction | Apply the `Y6` corrections to WP-53 and WP-51 text (CAP 413 terms, dropped unsourced claims, qualified AFIS and IFR statements) | docs | S | 2 |

## 8. ADR implications

- **New ADR N11, deterministic enforcement layer.** Gates and retry caps are enforced by hooks or workflows where the harness provides them; prose is the fallback. Touches the constitution's retry rules; sits beside N4 and N5.
- **N8 widens** to cover the manifest convergence (WP-610) and Codex hook parity.
- **N10 narrows** to backstory and skeleton ablations; the constitution-block question (WP-604) no longer needs an ADR unless the measurement says so.
- **ADR 003 may need a note** if WP-605 finds role-flavor splits worth merging; no change before that evidence.
- ADR 005 (artifact-agnostic gate) is unaffected: hooks and render evidence arrive as generic evidence kinds.

## 9. Risks and what is unverified

- Multi-agent token cost is 3 to 15 times a single agent in Anthropic's own figures. WP-601 must price every new agent and workflow.
- The long-autonomy figures are testimonials, not benchmarks; the harness-simplification result is Opus 4.6-era and was not re-checked on 5.x.
- Hook loop behavior is confirmed (7.1): Claude caps stop-hook continuations at 8, after which the turn ends and can look like a pass, so the retry counter and artifact checks are required.
- The Codex hook count (12) and Stop semantics, the AGY workflow shutdown (2026-10-19) and AGY's plugin fields are now primary-sourced; Antigravity 2.0 product details and several Cursor and Copilot specifics remain secondary.
- The cache-sharing conclusion in row 3 is inference from the documented sharing conditions.
- No head-to-head comparison of Claude Code, Codex and Antigravity on UI tasks exists. VISTA and Vision2Web evaluate agents, not these harnesses against each other.

## 10. Order of attack

1. WP-609, WP-615, WP-616 (cheap, remove uncertainty), and WP-601 (the baseline everything else is measured against).
2. Wave 1 exploration modes, unchanged.
3. WP-602, WP-603, WP-605, WP-606, WP-613 in Wave 2 with the gate-hygiene work, so enforcement and the retry rules land together.
4. WP-607, WP-611, WP-614 with the Wave 3 visual-evidence bundle.
5. WP-608, WP-610, WP-612, WP-604 in Wave 4.
