# Verified facts register

External and measured facts that decisions in this repository rest on, with where each was checked, when, and what should trigger a re-check. Cite a row instead of repeating a number from memory. Tags follow `docs/evidence-quality.md`: `P` primary page read, `P*` primary page read through a summarizing fetch (quotes may be paraphrased), `F` measured first-hand, `S` search summary only.

Sources are files under `docs/evaluations/frontend-design/verification/` unless noted. If a fact here and a note in `evidence/` disagree, this register wins; the note is unedited history.

## Claude Code and Anthropic (checked 2026-10-17 against the live docs; local CLI 2.1.292)

| Fact | Source | Tag | Re-check when |
| :-- | :-- | :-- | :-- |
| In auto mode, since Claude Code 2.1.271, a subagent delivers its report through the `SubagentHandback` tool, so a `SubagentStop` hook's `last_assistant_message` holds only the closing text; the report is `tool_input.message` | Y1 | P | A Claude Code release changes subagent delivery |
| A `PreToolUse` hook with matcher `SubagentHandback` fires for a plugin subagent in `claude -p --permission-mode auto`: `agent_type` is `<plugin>:<agent>`, the report is `tool_input.message`, and a deny reason reaches the subagent, which corrected its report and was accepted on the third attempt (Claude Code 2.1.292, one run) | First-hand live run, 2026-10-20; `IMPLEMENTATION-LOG.md` hook enforcement section | F | A Claude Code release changes subagent delivery or hook matching |
| The same hook fired with `agent_type` `scribe:exit-gate`, `sentinel:exit-gate`, `smith:exit-gate` and `ranger:exit-gate` in `claude -p --model claude-sonnet-5-5 --permission-mode auto` (Claude Code 2.1.311, one run each, from a directory outside the repository, plugin loaded with `--plugin-dir`); scribe, sentinel and smith were accepted on the first report, ranger was denied once and accepted on the second | First-hand live runs, 2026-11-10; `IMPLEMENTATION-LOG.md` gate rounds section | F | A Claude Code release changes subagent delivery or hook matching |
| `Stop` and `SubagentStop` hooks receive `stop_hook_active`; continuations are hard-capped at 8 in a row and the count resets when a tool is called; past the cap the turn ends | Y1 | P | Hooks documentation changes |
| A hook that fails or times out does not block unless `onFailure: "block"` is set, which needs 2.1.295 | Y1 | P | CLI upgraded past 2.1.295 |
| Plugin-shipped agents ignore `hooks`, `mcpServers`, `permissionMode` and `initialPrompt` | Y1 | P | Plugins reference changes |
| Subagent spawn depth defaults to 3 and concurrency to 20; there is no cap on total spawns | Y1 | P | Subagents documentation changes |
| Agent descriptions totaling over 15,000 tokens produce a startup warning, not an error | Y1 | P | Subagents documentation changes |
| Claude Code has 33 hook events | Y1 | P | Hooks documentation changes |
| `claude plugin validate plugins/<id>` with no `.claude-plugin/plugin.json` checks components only and reports a pass; with the manifest it validates the manifest | `VERIFY-3` section 4, `IMPLEMENTATION-LOG.md` | F | CLI upgrade |
| Anthropic's refusals documentation names a `reasoning`, `thinking` or `trace` field and scratchpad sections as `reasoning_extraction` triggers; the API returns HTTP 200 with `stop_reason: "refusal"`; there is no fallback model; pre-output refusals are billed | Y2, VERIFY-2 | P | Refusals documentation or model generation changes |
| The real `muse:drafter` prompt with its scratchpad field completed normally twice on Sonnet 5.5; adding a demand for verbatim chain of thought was refused and billed | `VERIFY-3` section 2 | F | New model generation; also probe Opus 5.5, Fable 5.1, Haiku 5.5 |
| Across 812 transcripts (72k+ Sonnet 5.5 and Opus 5.5 messages) there were no refusals; 157 messages contained a `reasoning` field | `VERIFY-3` section 1 | F | Re-run `scan-refusals.py` after new sessions |
| Subagents share a prompt cache only with the same model, effort, agent type, tools, schema and working directory; subagent caches default to a 5-minute TTL | Y2 | P | Prompt-caching documentation changes |
| "Skills developed for prior models are often too prescriptive" appears on the Fable 5 prompting page only | Y2, VERIFY-2 | P | Model prompting pages change |
| Effort defaults: Fable 5.1 high, Opus 5.5 medium, Sonnet 5.5 high (API), Haiku 5.5 medium | VERIFY-2 | P | New model release |
| Anthropic's multi-agent research post reports about 15 times chat tokens and a 90.2% gain (Opus 4 lead with Sonnet 4 workers against single Opus 4 on an internal research eval); a later guide gives 3 to 10 times; it says multi-agent suits shared-context and tightly coupled work poorly, "most coding tasks" included | Y2 | P* | A newer Anthropic engineering post |
| The simplified long-running harness result is 3h50m and $124.70 on Opus 4.6 for a DAW prompt, against 6h and $200 on Opus 4.5 for a game-maker prompt; the planner and evaluator were kept. It is not a before/after on one task | Y2 | P* | Re-checked on a 5.x model |
| Anthropic's `frontend-design` skill is a two-pass plan (4 to 6 named hex values, type roles, ASCII wireframes, then review against the brief) with five named AI-default clusters | Y5 | P | Skill updated |
| `claude plugin eval` runs each case with and without the plugin (default 3 runs per arm), has six grader types and no code graders, starts in an empty workspace, and its difference never changes the exit code | `investigations/plugin-eval-assessment.md` | P | CLI upgrade |

## Codex and Antigravity

| Fact | Source | Checked | Tag | Re-check when |
| :-- | :-- | :-- | :-- | :-- |
| The selectable Codex models are `gpt-6.1-sol`, `gpt-6-luna` and `gpt-6-astra`; `gpt-5.5` retires from ChatGPT sign-in Codex on 2026-10-14; `gpt-5.4` and `gpt-5.3-codex-spark` are retired | Codex models page, via `IMPLEMENTATION-LOG.md` | 2026-10-20 | P* | New Codex model release |
| Codex's AGENTS.md combined size cap is 32 KiB by default and configurable | VERIFY-2 | 2026-10-17 | P | Codex configuration reference changes |
| Codex has 12 hook events; a Stop `decision: "block"` injects a continuation prompt; `stop_hook_active` is the loop guard and `continue: false` wins; a PreToolUse failure fails open; hooks need user trust review; plugin hooks are not supported under cloud orchestration | Y3 | 2026-10-17 | P | Hooks documentation changes |
| Codex custom agents are natively TOML files in `.codex/agents/`; subagents inherit the parent's sandbox and approvals and cannot override them | Y3, VERIFY-2 | 2026-10-17 | P | Codex agents documentation changes |
| Codex spawns subagents only when asked; most intelligence levels need direct requests and proactive delegation happens at Ultra | Y3 | 2026-10-17 | P | Codex release |
| Antigravity workflows stop working on 2026-10-19; Antigravity's plugin `$schema` URLs return 404 and no third-party marketplace schema is documented | Y4 | 2026-10-17 | P | Antigravity documentation changes |

## Standards and platforms

| Fact | Source | Tag | Re-check when |
| :-- | :-- | :-- | :-- |
| Agent Plugins 1.0.0 is published (2026-08-06); its manifest requires `$schema` and `name`, clients reject paths leaving the plugin root, and it excludes hooks, commands, agents, marketplaces and permissions | Y4 | P | A new Agent Plugins version |
| The Agent Skills specification requires the skill name to equal its directory name and caps the description at 1,024 characters; it defines no top-level `version` | Y4 | P | Specification update |
| MCP 2026-07-28 makes the core stateless, moves Tasks and MCP Apps into opt-in Extensions, and deprecates Roots, Sampling and Logging with a 12-month floor | Y4, VERIFY-2 | P | A new MCP revision |
| WCAG 2.5.8 (AA) is 24 by 24 CSS pixels; the 44 by 44 figure is 2.5.5 (AAA) | VERIFY-2 | P | WCAG revision |
| DTCG design-token format reached its first stable version in 2025.10 | VERIFY-2 | P | A new DTCG version |
| Deque's 57% is the share of accessibility issues found by automated testing, by issue volume, in a 2021 vendor-run study of over 13,000 pages | Y6 | P | A newer study |

## Design and front-end industry practice

| Fact | Source | Tag | Re-check when |
| :-- | :-- | :-- | :-- |
| Atlassian measured 7.21M tokens for a DESIGN.md, 3.75M for MCP, 4.43M for a skill and 4.20M with no context on one login-screen task; model and run count not stated; Atlassian says it is not a research paper | VERIFY-2, Y5 | P | Atlassian publishes a larger test |
| Vercel's design.md result is 39 against 91 known deterministic-check failures on 6 pages, first attempts, Codex only; Vercel itself calls the sample far too small | Y5 | P | Vercel publishes more |
| Kaelig Deloumeau-Prigent's survey covers 21 design systems, 200 affordances and 165 techniques; 15 of 21 ship `llms.txt` (some served as 404 or an HTML shell) | VERIFY-2 | P | Survey updated |
| Google's DESIGN.md is alpha (Apache-2.0); its lint has 11 rules of which only `broken-ref` is an error and contrast is a warning | Y5, VERIFY-2 | P | Specification release |
| uSpec is MIT-licensed and owned by a personal GitHub account, with an Uber-bylined blog post dated 2026-03-11 | Y5 | P | Ownership or license changes |
| Figma's Code Connect figures are +1 quality point, -29.5% tokens and -19.6% duration over 27 tasks on 2 design systems; the Figma Starter limit is 20 calls per month | VERIFY-2 | P | Figma publishes new figures |
| v0 Design Systems 2.0 launched 2026-06-25 | VERIFY-2 | P | n/a |
| The Storybook MCP test tool is `test-run`; there are 9 tools and the feature is in preview | Y5 | P | Storybook release |

## Evaluations

| Fact | Source | Tag | Re-check when |
| :-- | :-- | :-- | :-- |
| JetBrains measured Caveman at -8.5% output tokens over 82 paired tasks (Sonnet 5, low effort, activation forced), with no detectable quality change (64 tied, 10 better, 8 worse, p = 0.82); the repository's own eval now reports 3% for the basic mode over an "Answer concisely" control | `evidence/X-conversation-findings.md`, Y6 | P | New runs |
| JetBrains measured rtk at +7.6% cost at low effort (p = 0.004) and no difference at high effort, with unchanged quality over 151 paired tasks; its own `rtk gain` scoreboard reported 96.2M tokens saved while the bill rose | `evidence/X-conversation-findings.md` | P | New runs |
| VISTA (arXiv 2605.26144): 44.5% of agent trajectories never looked at the design screenshots, 73% skipped prescribed self-audits and 8.3% claimed success despite failed checks | Y6 | P | Updated paper |
| In this repository's two sessions, plugin agents used 19.3M of 54.3M subagent-reported tokens; muse gates used about 8.2M over 79 calls | `VERIFY-3` section 3 | F | Re-run `tools/transcript-metrics.py agents` |
| Recorded gate verdicts: 33 of 45 conform to a verdict schema and all 12 violations are `verdict_summary` over 300 characters | `VERIFY-3` section 5 | F | Re-run the conformance script |

## Aviation terms (an analogy used for gate vocabulary; checked against UK CAP 413 and SKYbrary, not ICAO documents directly)

| Fact | Source | Tag | Re-check when |
| :-- | :-- | :-- | :-- |
| The standard words include affirm, negative, roger (meaning "received"), wilco, unable, standby, say again, correction, disregard, approved and request; UK material uses CONFIRM where the FAA uses VERIFY; "OK" is simply not a defined word | Y6 | P | Before any normative use, read ICAO Annex 10 and 11 and Docs 4444 and 9432 |
| Readback and hearback: the controller must listen to the readback and correct errors (Annex 11 3.7.3); missed approach and lost-communications procedures are predefined | Y6 | P* | As above |
| UK AFIS officers may give advice, relay air traffic control clearances and instruct on the movement area; pilots remain wholly responsible for collision avoidance | Y6 | P | As above |

## Not verified

The Figma 25,000-token response cap, Shopify and Airbnb figures, GPT-6 effort `none` support on every model, Atlassian's earlier 34% and 16% figures, whether Codex loads Claude agents or hooks from `.claude-plugin` formats, install behavior of the `shared` symlink in each harness, whether `skills-ref` rejects a top-level `version`, and the pages repository's commit counts.

## Plugin installation (checked 2026-10-20, Claude Code 2.1.292)

| Fact | Source | Tag | Re-check when |
| :-- | :-- | :-- | :-- |
| Claude Code dereferences a plugin symlink whose target is elsewhere in the same marketplace when it copies the plugin into its cache; a target outside the marketplace is skipped | Claude Code documentation (host marketplace), `evaluations/frontend-design/verification/VERIFY-3.md` section 7 | P, F | CLI upgrade |
| A `git-subdir` source is fetched with a sparse checkout of one subdirectory, so a `../../shared` symlink target is absent and the installed `shared` dangles; a relative-path source installs the whole marketplace's files | Claude Code documentation, first-hand install into an isolated config | P, F | CLI upgrade |
