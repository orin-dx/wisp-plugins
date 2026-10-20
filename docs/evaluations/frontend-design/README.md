# Front-end and design-ideation evaluation of the Wisp plugins

Status: proposal and evidence base, with Wave 0 started (see `IMPLEMENTATION-LOG.md`): the Codex role-card model ids, generated Claude manifests with validation, a reasoning-wording lint, and a hook-validator spike are done; nothing is released. Beyond Wave 0, every change below is a work package (WP) awaiting a decision. No ADR, constitution rule or published schema has changed.

## Why this exists

The plugins were used on two brand sites (techworx and orin-dx). This evaluation reads the sessions and repos from that work, surveys how the industry does agentic design and front-end work, and turns both into a sequenced plan. The trigger was a user observation: the plugin workflows are too rigid for early, experimental, idea-flushing work, where the goal is to see designs and check that tools work without specs, tests or gates.

## Contents

| Path | What it is |
| :-- | :-- |
| `CATALOG.md` | The plan: 144 work packages, a dependency graph, six waves, 10 proposed ADRs, 20 conflicts with resolutions, and post-verification amendments (section 5) |
| `IMPLEMENTATION-LOG.md` | What Wave 0 changed so far, what it found, the change record the repo requires, and the release bookkeeping deliberately not done |
| `ARCHITECTURE-REVIEW.md` | Each architectural assumption tested against what current agent platforms can do, measured repo facts, 28 more work packages (WP-601 to WP-628, 172 in total) added by the review and its verification, and the resulting direction: thinner prompts, thicker harness. Its section 7.1 overrides earlier rows where verification corrected them |
| `traceability/` | Five matrices mapping about 1,000 individual findings to WPs, each with contradictions, claims to verify, and proposed new WPs. `WP-draft.md` is the first draft the matrices were built against |
| `verification/` | `VERIFY-1.md` (transcript and repo claims), `VERIFY-2.md` (web and documentation claims), `VERIFY-3.md` (first-hand measurements: refusal scan, live probe, gate cost, repo structure), `Y1` to `Y6` (full primary-source reads of Claude Code, Anthropic, Codex, AGY and standards, design sources, aviation and evals), and `scripts/` that reproduce the measurements. They correct errors in the evidence notes |
| `evidence/` | The raw research notes. Index and tag legend in `evidence/README.md` |

Paths written `<refs>/...` in the catalog and matrices are *proposed* reference files that do not exist yet. The repo's reference-integrity test validates every literal `shared/references/` path, so proposals are marked this way.

Read in this order: this file, then `CATALOG.md` sections 3 to 5, then `verification/`, then a matrix when you need the source of a specific WP.

## What the sessions show

Scope: about 812 transcript files, but only a handful are real top-level sessions; the rest are subagent transcripts. Plugin agents were used in two sessions: `orin-dx` b8d16e96 (09-29 to 10-03) and `pages` 24655582 (10-05 to 10-16). `vanguard` ran once, on 10-17, for blog-topic research. Everything else, including nearly all design ideation, used no plugin.

1. **Strong on behavior, blind on appearance.** Gates caught real contradictions, accessibility values (a 2.82:1 contrast failure recomputed from the token source), and cross-spec conflicts. Every visible defect was found by a human look, an audit, or the 16 Oct suite. `spec@1` has no way to express visual intent and nothing renders anything.
2. **Gate loops were fix-and-resubmit.** 38 gate calls in the `orin-dx` session (28 muse, 10 scribe) and 51 `muse:exit-gate` calls in the `pages` session (per spec: 7, 5, 6, 9, 4, 6, 8, 6 for SPEC-005 to 012, inside a 57-minute window). Every spec failed its first gate with 9 to 23 blockers. The retry cap of 3 was not enforced: gates said "escalate" from retry 4 and the orchestrator continued with no user message in between (SPEC-005 ended at retry 6, SPEC-008 at 9). All eight specs finished as passes with empty blockers.
3. **Approval in prose failed.** The user repeatedly asked to see rendered examples (the session matrix counts at least seven requests; not independently re-counted) and the agent described first. Drawn prototypes then exposed a touch-target bug the gated spec missed.
4. **Specs lagged the design.** Specs gated on 11 Oct were rewritten the next day after decisions made from drawn pages, and the 12 Oct revisions ran with "no exit gate this round". SPEC-013 supersedes much of SPEC-001 and SPEC-003c.
5. **Exploration worked best outside the plugins.** Option boards (Artifacts in Oct, repo-script Playwright screenshots, local pages) and short answer codes. The user stated the two-phase model explicitly on 2026-10-14 at 20:25 UTC (`pages` line 49946): exploratory build quick, specs and tests when it narrows. The same session built the landing, Tools and Principles pages in about 30 minutes once the audit machinery stopped.
6. **Ceremony still paid off for stable contracts.** The SiteNav migration passed 478 Chromium e2e tests, and the challenger found real plan defects.
7. **Defects shipped past the gates** (documented in commits whose hashes were confirmed to exist): "NaN%" glass opacity on the Orin brand page, card strand fades that cut hard at phone width, tool marks stretched and 2px low, colour-card labels at 2.9 to 4.3:1 contrast, a filter 1px short of the 44px target, duplicate banner landmarks, and misattributed decisions in case-study copy.
8. **Stalls and unused agents.** The `orin-dx` session had 17 failed agent tasks (11 watchdog stalls, 6 API errors); the `pages` session had none. `smith:recon` and every `sentinel:*` agent appear in no transcript, `smith:reviewer`, `smith:mutator` and `smith:exit-gate` ran only in a third project, and the cause is unknown (WP-56).

## What the plugins lack, by design

- No browser, screenshot, Storybook or visual capability anywhere; the `workspace-manifest@1` capability list is closed and cannot record one.
- No schema for a direction, brief, wireframe, prototype, copy deck or critique, and no divergent cognitive mode.
- Muse's docs point three times to "ranger's accessibility hazard taxonomy"; ranger has none, so implemented accessibility is never checked (WP-01, WP-44).
- Every build path runs recon, mutation, review and a binding exit-gate; there is no spike or sketch mode. Constitution rules (default-fail gates, no TBDs) make an unfinished idea an invalid artifact.
- 29 of 31 schemas carry a mandatory `reasoning` scratchpad field (constitution line 242). Anthropic's refusals documentation names a `reasoning`, `thinking` or `trace` field as a `reasoning_extraction` trigger. First-hand evidence (`verification/VERIFY-3.md`): zero refusals in 72k+ Sonnet 5.5 and Opus 5.5 messages from the sessions, and a live probe in which the real `muse:drafter` prompt with its scratchpad field completed normally twice while one added line demanding verbatim chain of thought was refused and billed. The trigger is wording that asks for reproduced reasoning, not the field's existence. WP-625 adds a wording lint and a per-model-generation probe.

## What the industry shows

Corrected after verification; see `verification/VERIFY-2.md` for evidence.

- **Intent and behavior are separate artifacts** (DESIGN.md, uSpec, Storybook, Atlassian). `spec@1` mixes them and can express only behavior.
- **Extract deterministically, then let the model add judgment** (uSpec; Netflix and JetBrains code intelligence; Spectrum's generated skills). It maps to the stale-number problem in the specs.
- **Render, then compare** is the standard verification loop, and Anthropic's own guidance recommends giving the agent a way to verify its work. A clean axe run covers about 57% of accessibility issues by volume (Deque, 2021).
- **Lint is the preferred gate** (Salesforce, Primer, Spectrum, Vercel). Gates that only judge text miss rendered defects.
- **Mode routing separates exploring from hardening** (Vercel's product-design skill: shape, implement, review, copy, harden; exploration modes make no edits).
- **A monolithic DESIGN.md is costly:** Atlassian measured 7.21M tokens against 3.75M for MCP, 4.43M for a skill and 4.20M for no context on one task. Vercel's design.md showed 39 vs 91 failures but on six pages, so it is weak evidence either way. Use a small routed intent file and lookups, and run our own paired test (WP-402).
- **Nobody has a real decision log.** Claude Design has no version history and Figma Make users ask for branching.
- **Token-saving prompts and tools do little in agentic work.** Caveman: about 8.5% output tokens on 82 paired tasks with no detectable quality change (JetBrains, Sonnet 5 at low effort, a ceiling because activation was forced). rtk: no token saving and a +7.6% cost at low effort (p=0.004), none at high effort; its own `rtk gain` scoreboard reported 96.2M tokens saved while the bill rose. The method is the reusable part: paired runs, medians, bill-based, failures excluded from both arms, and never trusting k=1.
- **Corrections from verification:** 15 of 21 design systems ship `llms.txt` (not "almost none"); Coinbase's Code Connect figures are +1 quality point, -29.5% tokens and -19.6% duration over 27 tasks on two design systems; v0 Design Systems 2.0 launched 2026-06-25; the Figma Starter limit is 20 calls per month; `test-run` is the Storybook MCP tool name; WCAG 2.5.8 is AA at 24x24 and the 44x44 figure is 2.5.5 at AAA; Codex custom agents are natively TOML (repo policy still keeps role cards markdown).
- **Not found:** first-party Airbnb or Netflix design-system AI material (Netflix's JetBrains case study concerns Java code intelligence), and verified Shopify design-rules material. These are dispositions in the matrices, not silent omissions.

## The plan

144 work packages from the evidence mapping, none dropped, plus 28 from the architecture review and its verification (172 in total). Eight overlap another WP and are merged into it with a reason; about 20 more overlap and are kept with the reason stated. Full table in `CATALOG.md`.

| Wave | Theme | WPs | Needs first |
| :-- | :-- | :-- | :-- |
| 0 | Defects, baselines, measurement | 21 | nothing |
| 1 | Exploration modes (the stated priority) | 19 | ADR N1 |
| 2 | Gate hygiene and orchestration | 27 | ADR N4, N5 |
| 3 | Visual intent and evidence | 43 | ADR N2, N3 (one schema bundle) |
| 4 | Prompt, model, Codex, AGENTS.md, distribution | 27 | ADR N8, N9, N10 (conditional) |
| 5 | Consumer-repo and research follow-ups | 7 | nothing |

Highlights:
- **Wave 0:** fix the muse dangling reference and move muse to `verdict@3`; baseline the gate metrics from transcripts; build the paired-eval harness; test the `reasoning` refusal risk first (WP-61); find why agents went unused (WP-56).
- **Wave 1:** a mode router (shape, sketch, spike, implement, review, copy, harden, promote); a `sketch` skill with durable option files (stable ids, status, one-line reason) that double as the decision log, rendered locally as a brand x theme x viewport matrix, TBDs allowed, no gate; a smith `spike` skill to check that a tool or library works; a show-first rule; direction-commit and anti-slop controls; a lightweight promote (WP-14a) that carries a chosen option forward as a requirement plus a brief.
- **Wave 2:** evidence-citing blockers, "no findings" as a valid pass, enforced retry caps with logged overrides, readback in correction loops, a small fixed vocabulary, stall procedures, orchestrator-owned spawning, and file ownership for parallel work.
- **Wave 3:** `spec@2` with token and visual references, a render-evidence artifact and manifest capability, deterministic UI checks (tokens, contrast, target size, landmarks, copy provenance), the full promote path, a visual critic, and ground-truth extraction before drafting.
- **Wave 4:** ablations of the constitution and prompt structure measured net of cache hits, tier re-checks per model, Codex role cards, an AGENTS.md strategy, and skill versioning and maintenance.

Design choices made in the catalog's conflict table (section 4): 3 options per round and 4 directions only at the first direction-commit; 3 parallel writers by default and up to 5 for disjoint work; scanners report everything and a separate stage filters while gates stay scoped to stated requirements (test first in WP-60); no tier changes on vendor claims until measured (WP-63).

## Architecture review (summary)

Full text in `ARCHITECTURE-REVIEW.md`. Measured facts: 10 plugins, 30 skills, 44 agents; agents use only five frontmatter keys and none of the platform's native controls (`tools`, `maxTurns`, `isolation`, `skills`, `memory`); no plugin ships hooks, validators, workflows or code-intelligence servers.

- **Keep:** the schemas as the cross-harness contract, progressive disclosure, and the differentiators no harness provides natively: falsifiable specs, adversarial refutation, fail-by-default binding gates, enforced self-audit.
- **Change:** enforcement. Retry caps, schema validity and "no pass without evidence" move from prompts into hooks or workflow scripts where the harness supports it, with the prompt path as the cross-harness fallback (the retry cap failed in the `pages` session because it lived only in a prompt). Plans become outcome-level and resumable for longer autonomous runs. Visual evidence comes from capability-detected native browsers.
- **Test before deciding:** whether role-based agent splits pay for their cost (Anthropic recommends splitting by context, not role; multi-agent runs cost 3 to 15 times a single agent). WP-601 sets up `claude plugin eval` with a no-plugin baseline.
- **Lower priority than first thought:** the constitution is a 6-line block in each agent, not 290 lines. The 290-line file is the authoring-time rulebook (catalog amendment P8).
- **Shape:** Codex has its own native plugin format in `harnesses/codex/`; AGY's format is similar to Claude Code's and shares the authored tree. AGY workflows stop working on 2026-10-19, so author skills only.

## Conformance findings from primary-source verification

Details in `verification/Y1` to `Y6` and `ARCHITECTURE-REVIEW.md` section 7.1.

- **Claude Code.** `claude plugin validate plugins/<id>` reports a pass after checking components only, because the manifests sit at the plugin root and not at `.claude-plugin/plugin.json`. Validated explicitly, each manifest gets 3 warnings (`id`, `consumes`, `produces` are ignored at load time) and `--strict` would fail all 10. Agent `role` and skill `version` frontmatter have no runtime effect. Each plugin's `shared` symlink points outside the plugin directory. Subagents deliver reports through a `SubagentHandback` tool in auto mode (since 2.1.271), so a `SubagentStop` validator would read the wrong field. Stop-hook continuations are hard-capped at 8, and a failing or timed-out hook does not block unless `onFailure: "block"` (needs 2.1.295; local CLI is 2.1.292). The 15,000-token agent-description limit is a startup warning, not an error.
- **Codex.** The roles README names retired or unknown model ids (`gpt-5.6-luna`, `-terra`, `-sol`; current: `gpt-6-luna`, `gpt-6.1-sol`, `gpt-6-astra`). 18 skills phrase delegation as "teams" or "teammates"; Codex delegates only when told to, so only the sequential fallback runs today. Role cards cannot enforce read-only (subagents inherit the parent sandbox). Only the legacy `.codex-plugin/plugin.json` exists, and `capabilities` carries an undocumented value (`agent-teams-optional`).
- **Antigravity and standards.** The `$schema` URLs in the root `marketplace.json` and AGY's documented plugin schema both return 404, and no third-party AGY marketplace schema is documented, so that file is repo-private. Agent Plugins 1.0.0 requires `$schema` and `name` in its manifest and rejects paths leaving the plugin root. AGY workflows stop on 2026-10-19 (primary page).
- **Claims corrected.** The harness-simplification result (6h/$200 vs 3h50m/$124.70) compares different models and prompts and kept the planner and evaluator; the "31-minute UK AISI horizon" is not in the cited paper; "Astra about 40 minutes per task" is a vendor latency simulation, not an autonomy duration; Caveman's "65%" is stale (its repo now reports 3% over a concise-control for the basic mode); `taste-skill` v2 has no dials; "verify" is FAA usage, ICAO and UK material uses "confirm"; AFIS and IFR claims needed qualification.

## How the user's guidance is covered

| Guidance | Where |
| :-- | :-- |
| Flexible, "vibe-coded" exploration without worrying about specs and tests | Wave 1: WP-10, 11, 12, 13, 15, 16, 18, 19; mode router gives each mode its own gate set (conflict K12) |
| See designs | WP-12 (rendered option matrix, local first), WP-211 (show-first rule), WP-34 |
| Validate that tools work | WP-15 smith `spike`: smoke-check evidence, verified-vs-unverified report, promote or discard |
| Specs and tests once ideas narrow, without regressions | WP-14a/b promote, WP-19 harden, WP-106 to 108 spec hygiene, WP-204 test taxonomy |
| Do not cut things | 144 WPs, 8 merged with reasons, dispositions for items with no action; nothing was dropped |
| Learn from industry, model vendors, AGENTS.md, uSpec, ICAO, TanStack Intent | Waves 3 and 4; WP-32 and 33 (uSpec), WP-71 (AGENTS.md), WP-53, 54 and 212 (ICAO ideas), WP-72 (Intent) |

## Open items and limits

- **Unverified here:** pages commit counts (repo history access was blocked for that repo), the `a859e2f` origin claim, the 271 KB JS budget, whether SPEC-013 supersedes 26 of SPEC-001's and 35 of SPEC-003c's criteria, Shopify and Airbnb figures, the Figma 25k response cap, whether Codex loads Claude agents or hooks from `.claude-plugin` formats, install behavior of the `shared` symlink in each harness, whether `skills-ref` rejects a top-level `version`, and the refusal probe on Opus 5.5 and Fable 5.1 (only Sonnet 5.5 was probed). The aviation items were checked against UK CAP 413 and SKYbrary, not ICAO documents directly; see `verification/Y6-aviation-evals.md`.
- **Weak evidence by nature:** vendor self-benchmarks and small samples (Vercel's six pages, Atlassian's single task). WP-401 proposes tagging them.
- **One project:** all transcript evidence is from two sessions in one body of work. Gate cost was measured from those sessions (`verification/VERIFY-3.md`) and covers subagent-reported tokens only, not a bill or main-session tokens.
- **Not read:** several newer Anthropic posts (infrastructure noise, eval awareness, auto mode), the Codex computer-use and MCP pages and release notes before 0.162, and ICAO Annex 10/11, Doc 4444 and Doc 9432 directly.
- **User configuration untouched:** `~/.claude/RTK.md` installs rtk with the same hook JetBrains tested. Whether it helps this workflow is an open paired test (WP-68), not a recommendation to change it.

## Next decisions

1. Accept or amend the wave order, in particular Wave 1 before Wave 2.
2. Write ADR N1 (exploratory mode, amending ADR 003) and N6 (the `reasoning` field policy: keep the field, lint the wording), and start with the Wave 0 conformance fixes (WP-617, WP-620, WP-622, WP-624, WP-625).
3. Decide whether sketch and promote live as skills in `muse` (which already owns UI) or in a new plugin; `AGENTS.md` allows several skills in one plugin when intents are heterogeneous, and the catalog assumes `muse`.
