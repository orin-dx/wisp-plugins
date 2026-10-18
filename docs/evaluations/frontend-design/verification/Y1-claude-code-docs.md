# Y1: Claude Code docs, primary-source verification (2026-10-17)

Method: full raw markdown of each page fetched with curl from `https://code.claude.com/docs/en/<page>.md` (no summarizer, no truncation) and read by section, saved under `/Users/gabe/.claude/jobs/2d213021/tmp/docs/`. Sizes: hooks 273,668 chars; sub-agents 111,181; skills 109,922; plugin-evals 64,289; plugins/cli-reference 61,681; plugins/components 54,973; memory 51,526; plugins/marketplace-reference 44,335; plugins/manifest-reference 41,987 (also served at /plugins-reference); workflows 41,609; agent-teams 40,432; headless 34,282. Local CLI: Claude Code 2.1.292. All rows tagged [P]. Quotes are verbatim, trimmed to 25 words.

Base URL for all rows: https://code.claude.com/docs/en/

## 1. Verified facts

### Hooks (hooks)
| Fact | Quote | URL | Tag |
|---|---|---|---|
| Stop loop flag | "`stop_hook_active` field is `true` when Claude Code is already continuing as a result of a stop hook." | hooks#stop-input | [P] |
| Stop loop cap (answers WP-616) | "after stop hooks have continued the turn eight times in a row, Claude Code overrides the next block and ends the turn" | hooks#stop-input | [P] |
| Cap resets and is tunable | "count ... resets each time Claude calls a tool. To raise the cap, set CLAUDE_CODE_STOP_HOOK_BLOCK_CAP." | hooks#stop-input | [P] |
| Cap is documented under Stop; SubagentStop "uses the same decision control format" and `additionalContext` keeps "the same loop protections ... `stop_hook_active` input and the 8-consecutive-continuation cap". Whether SubagentStop has its own separate count is not stated | (see left) | hooks#stop-decision-control | [P] |
| SubagentStop input | "receive `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, and `last_assistant_message`" | hooks#subagentstop | [P] |
| SubagentStop block | "Returning `decision: "block"` with a `reason` keeps the subagent running and delivers `reason` to the subagent as its next instruction." | hooks#subagentstop | [P] |
| SubagentHandback changes where the report is | "`last_assistant_message` field then holds the subagent's closing text ... which is not the delivered report." Read it via PreToolUse/PostToolUse on `SubagentHandback`, `tool_input.message` | hooks#subagentstop | [P] |
| SubagentHandback availability | "Provided only in auto mode, to subagents that the Agent tool runs locally other than forks" (v2.1.271+) | tools-reference | [P] |
| SubagentStart cannot block | "SubagentStart hooks can't block subagent creation, but they can inject context into the subagent." | hooks#subagentstart | [P] |
| Plugin agent matcher name | "the agent type is the plugin-scoped identifier such as `my-plugin:reviewer` ... anchor the matcher with `^` and `$`" | hooks#subagentstart | [P] |
| Exit 2 blocks Stop/SubagentStop/TaskCompleted/TeammateIdle/PreToolUse | Table: Stop "Prevents Claude from stopping"; SubagentStop "Prevents the subagent from stopping"; TaskCompleted "Prevents the task from being marked as completed" | hooks#exit-code-2-behavior-per-event | [P] |
| Exit 2 file-missing exemption | "exits 2 with nothing on stdout and its stderr says a file is missing ... treats the run as a non-blocking error" | hooks#exit-code-output | [P] |
| Failed/timed-out hooks do not block by default | "A timed-out command, http, or mcp_tool hook doesn't block the tool call ... don't count on a stalled hook to act as a gate." | hooks#exit-code-output | [P] |
| `onFailure: "block"` | "set "onFailure": "block" on a command or http hook. Requires Claude Code v2.1.295 or later." (local CLI is 2.1.292) | hooks#block-the-action-when-a-hook-fails | [P] |
| Handler types | "five types": command, http, mcp_tool, prompt, agent ("experimental"); agent hooks "After up to 50 turns" | hooks#hook-handler-fields | [P] |
| Which events accept prompt/agent hooks | Stop, SubagentStop, TaskCompleted, TaskCreated, TeammateIdle, PreToolUse, PostToolUse, PostToolBatch, UserPromptSubmit etc.; SubagentStart is command/http/mcp_tool only | hooks#prompt-based-hooks | [P] |
| Prompt-hook escape hatch | "`impossible` ... On Stop and SubagentStop, Claude Code then lets the turn end instead of feeding the reason back." | hooks#response-schema | [P] |
| Timeouts | "Defaults: 600 for command, http, and mcp_tool; 30 for prompt; 60 for agent." | hooks#hook-handler-fields | [P] |
| Event count | 33 events in the lifecycle table (not "~36") | hooks#hook-lifecycle | [P] |
| Plugin hooks scope | "Hooks from settings files, managed policy settings, and plugins also run inside subagents." | hooks#hook-locations | [P] |
| Plugin hooks fire for the whole session | "A plugin's hooks don't wait for one of the plugin's skills or commands to be used ... narrow its `matcher`." | plugins/components#hooks | [P] |
| Plugin hook file shape | "A hooks file wraps the event map in a top-level "hooks" key ... A file that contains only the event map ... fails to load." | plugins/manifest-reference#hooks | [P] |
| Hook env | "export them as the environment variables CLAUDE_PROJECT_DIR, CLAUDE_PLUGIN_ROOT, and CLAUDE_PLUGIN_DATA" | hooks#exec-form-and-shell-form | [P] |
| PreToolUse can rewrite input | "`updatedInput` directly under `hookSpecificOutput` replaces a tool's arguments before it runs" | hooks#json-output | [P] |
| Agent tool result | "Subagents run in the background by default, an Agent call that omits `run_in_background` also produces `async_launched`" | hooks#agent | [P] |
| Workspace trust | "Frontmatter hooks in a project subagent run only after you accept the workspace trust dialog ... A -p session doesn't count" | hooks#hooks-in-skills-and-agents | [P] |

### Sub-agents (sub-agents)
| Fact | Quote | URL | Tag |
|---|---|---|---|
| Frontmatter keys | name, description (required); tools, disallowedTools, model, permissionMode, maxTurns, autoCompactWindow, skills, mcpServers, hooks, memory, background, omitClaudeMd, effort, isolation, color, initialPrompt, experimental.cacheTtl | sub-agents#supported-frontmatter-fields | [P] |
| Unknown keys silently ignored | "Claude Code ignores a field it doesn't recognize without reporting an error." (v2.1.296+ debug log names them) | sub-agents#supported-frontmatter-fields | [P] |
| Plugin-agent supported set | "`name`, `description`, `model`, `effort`, `maxTurns`, `autoCompactWindow`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `omitClaudeMd`, `isolation`, `color`, ... `cacheTtl`" | plugins/components#agents | [P] |
| Plugin-agent ignored set | "**Ignored fields**: `permissionMode`, `hooks`, `mcpServers`, and `initialPrompt`." | plugins/components#agents | [P] |
| Description budget is a warning, not an error | "Claude Code loads every agent whether or not the total is over the limit, so the warning doesn't change what loads." | errors#agent-descriptions... | [P] |
| What counts | "Each agent counts its name plus its `description` frontmatter"; built-in agents excluded; 15,000 tokens "as Claude Code estimates them" | errors | [P] |
| `Agent(x,y)` allowlist scope | "applies only to an agent running as the main thread with `claude --agent`. In a subagent definition ... any type list inside the parentheses is ignored." | sub-agents#restrict-which-subagents-can-be-spawned | [P] |
| Tools removed from every subagent | "AskUserQuestion, EndConversation, EnterPlanMode, ExitPlanMode (unless plan), ScheduleWakeup, WaitForMcpServers, Workflow" and `Agent` at the depth limit | sub-agents#available-tools | [P] |
| Background tool set | background subagents keep only Read, Grep, Glob, LSP, Bash, Edit, Write, WebFetch, WebSearch, Skill, ToolSearch, SendMessage, Artifact etc. plus SubagentHandback | sub-agents#available-tools | [P] |
| Foreground vs background default | "Where fork mode is off, Claude runs the subagent in the background by default and in the foreground when it needs the result". Fork mode "off in non-interactive mode with `-p`" | sub-agents#run-subagents-in-foreground-or-background | [P] |
| Depth | "up to three layers below the main conversation" (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`); v2.1.172-216 five, 217-218 one | sub-agents#let-subagents-spawn-their-own-subagents | [P] |
| Concurrency | "when 20 subagents are running ... spawning another fails with `Concurrent subagent limit reached`, and the error tells Claude not to retry" | sub-agents#concurrent-subagent-limit | [P] |
| No total spawn cap | "There's no limit on the total number of subagents Claude can spawn over a session." | sub-agents#concurrent-subagent-limit | [P] |
| Skills preload | "full content of each listed skill is injected ... up to the first 32 distinct names"; skills with `disable-model-invocation: true` cannot be preloaded | sub-agents#preload-skills-into-subagents | [P] |
| Memory | `memory: user|project|local`; first "200 lines or 25KB of MEMORY.md"; Read/Write/Edit auto-enabled; off if auto memory disabled | sub-agents#enable-persistent-memory | [P] |
| Resume | "Claude uses the `SendMessage` tool with the agent's ID or name as the `to` field"; resumed run "keeps the tool set from where the subagent first ran" | sub-agents#resume-subagents | [P] |
| maxTurns | "Claude Code returns its output marked as partial, and Claude can resume it" (v2.1.246+) | frontmatter table | [P] |
| Per-invocation effort | parameter "overrides the `effort` field and stays in effect when the subagent is resumed" (v2.1.292+) | sub-agents#choose-an-effort-level | [P] |
| Model resolution | per-invocation param, then frontmatter, then CLAUDE_CODE_SUBAGENT_MODEL, then main model | sub-agents#choose-a-model | [P] |
| Subagent context | CLAUDE.md files (incl. AGENTS.md), git status, preloaded skills load into every non-fork subagent unless `omitClaudeMd`; "Subagents receive only this system prompt plus basic environment details" | sub-agents#what-loads-at-startup | [P] |
| Output scanning | report is scanned; may get backslashes inserted and a `[harness: subagent output matched instruction-shaped pattern(s):` marker line (v2.1.210+) | sub-agents#subagent-output-scanning | [P] |
| Plugin agent namespacing | subfolder in `agents/` becomes part of the name: `agents/review/security.md` -> `my-plugin:review:security` | sub-agents#choose-the-subagent-scope | [P] |
| Priority | Plugin `agents/` is lowest of five scopes | sub-agents#choose-the-subagent-scope | [P] |

### Skills (skills)
| Fact | Quote | URL | Tag |
|---|---|---|---|
| Recognized frontmatter | name, description, when_to_use, argument-hint, arguments, disable-model-invocation, user-invocable, allowed-tools, disallowed-tools, model, effort, context, agent, background, hooks, paths, shell, metadata, license, compatibility | skills#frontmatter-reference | [P] |
| `version` is NOT a skill field | not in the table; "Claude Code ignores a field it doesn't recognize without reporting an error." (use `metadata:` for custom data) | skills#frontmatter-reference | [P] |
| Description cap | "combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing" | skills#frontmatter-reference | [P] |
| `allowed-tools` is a grant, not a restriction, and is per turn | "Tools Claude can use without asking permission during the turn ... The grant clears when you send your next message." | skills#frontmatter-reference | [P] |
| context: fork | "Claude Code starts a new subagent of the type set in the `agent` field and gives it the skill content as its prompt. The subagent doesn't see your conversation history" | skills#run-skills-in-a-subagent | [P] |
| Fork skill background | runs in background by default; waits "In non-interactive mode, with the -p flag or the Agent SDK"; background fork gets the narrower tool set | skills#run-skills-in-a-subagent | [P] |
| Compaction | "keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens" | skills#skill-content-lifecycle | [P] |
| Plugin skill naming | `/plugin:dir`; frontmatter `name` replaces last segment | skills#how-a-skill-gets-its-command-name | [P] |
| Claude.ai/API upload limits | extra fields cause hard error: "Allowed properties are: allowed-tools, compatibility, description, license, metadata, name" | skills#using-skill-frontmatter-outside-claude-code | [P] |
| Variables | `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_EFFORT}` substituted in skill body and `allowed-tools` | skills#available-string-substitutions | [P] |

### Plugins (plugins/manifest-reference, plugins/components, plugins/loading, plugins/dependencies, marketplace-reference)
| Fact | Quote | URL | Tag |
|---|---|---|---|
| Manifest location | "Save the manifest at `.claude-plugin/plugin.json` under the plugin root. Put every other plugin file at the plugin root" | plugins/manifest-reference#manifest-file | [P] |
| Manifest optional | "Without it, Claude Code loads the components it finds in the standard layout." | same | [P] |
| Unknown top-level field | "the field is stripped and the plugin loads. `claude plugin validate` reports each unrecognized top-level field as a warning" | same#unrecognized-fields | [P] |
| Strict objects | userConfig options, channels, lspServers configs, monitors entries: "An unknown key inside one is an error, and the plugin doesn't load" | same | [P] |
| Bundleable | skills, commands, agents, hooks, mcpServers, lspServers, outputStyles, workflows, experimental.themes/monitors/evals, settings (only `agent`, `subagentStatusLine`), userConfig, channels, dependencies, `bin/` | same#fields | [P] |
| Replace vs add | `agents`, `commands`, `workflows` replace default dir; `skills` adds; `hooks`/`mcpServers`/`lspServers` merge | same#how-each-key-combines... | [P] |
| `bin/` | "Files here are on the Bash tool's PATH while the plugin is enabled"; not shadowing system commands; claude.ai/Cowork do not install plugins with `bin/` | plugins/components#executables | [P] |
| Env vars | `${CLAUDE_PLUGIN_ROOT}` changes on update ("don't write state there"); `${CLAUDE_PLUGIN_DATA}` = `~/.claude/plugins/data/<id>/` kept across updates; not in Bash tool env | same#environment-variables | [P] |
| Root CLAUDE.md | "A CLAUDE.md at the plugin root isn't loaded as context, and `claude plugin validate` warns" | same#standard-layout | [P] |
| Version pin | "Setting it pins the plugin to that version until you change it"; plugin.json `version` beats marketplace entry | same#version; marketplace-reference | [P] |
| Copy to cache; files outside plugin dir not copied | "Files outside the plugin directory aren't copied, so when a script inside a copied plugin reads a path above the plugin root, such as `../shared`, it doesn't find them" | plugins/loading#in-place-and-copied-plugins | [P] |
| Symlinks | symlink resolving "Elsewhere within the same marketplace: the symlink is dereferenced. The target's content is copied into the cache"; "Outside the marketplace: skipped"; local-path installs keep only symlinks inside the plugin | plugins/host-marketplace#share-files-within-a-marketplace-with-symlinks | [P] |
| Dependencies | `dependencies`: "Plugins that must be enabled for this one to work"; semver ranges resolve against git tags; cross-marketplace needs `allowCrossMarketplaceDependenciesOn`. Plugin-level only (no file sharing) | plugins/dependencies | [P] |
| marketplace.json | required `name`, `owner`, `plugins`; entry requires `name` and `source`; "Claude Code ignores an unknown top-level key or plugin-entry key"; location `.claude-plugin/marketplace.json` | marketplace-reference#top-level-fields | [P] |
| `author` shape | "`author` | Object | `name`, which is required, plus optional `email` and `url`" | manifest-reference#fields | [P] |
| Agent teams reuse | teammate applies `tools`, `model`, `disallowedTools`, `effort`, `autoCompactWindow`, body; "doesn't apply the definition's `skills`" | agent-teams | [P] |

### `claude plugin eval` / validate (plugins/cli-reference, plugin-evals)
| Fact | Quote | URL | Tag |
|---|---|---|---|
| Runs | "Claude Code runs it several times in an isolated session with only the target plugin loaded, and by default also without the plugin"; 3 runs default, `runs` 1-50 | plugin-evals | [P] |
| Baseline | "WITH and W/OUT. Their difference, Δ"; the Δ "is reported but never changes the exit code" | plugin-evals#the-no-plugin-baseline; #run-evals-in-ci | [P] |
| Graders | six types: regex, tool_used, tool_order, file_exists (free), llm, baseline (judge); "There are no custom-code graders." | plugin-evals#grade-the-result | [P] |
| Skill-fired graders excluded from score | "Every `tool_used` grader whose `tool` is `Skill`" is reported `scored: false` in two-arm runs | plugin-evals#compare-against-a-no-plugin-baseline | [P] |
| Tools in runs | "Runs never stop to ask for permission"; Bash/Write/Edit need `--allow-tools`; Bash runs in OS sandbox; `Agent` is in the read-only grantable set | plugin-evals#grant-tools | [P] |
| Workspace | "Each run starts in an empty workspace" (use `context.scaffold_script` + `--scaffold`, 120 s limit) | plugin-evals | [P] |
| Limits | `max_turns` default 10 (cap 200), `timeout_seconds` default 300 (cap 3600), `-j` 1-8 | plugin-evals#prompt-md-fields; cli-reference | [P] |
| Cost control | `--max-cost-usd`, exit 2 on partial; `--ablation none` halves cost; model calls "roughly cases x runs agent runs with the plugin and the same number again" without | plugin-evals; cli-reference | [P] |
| CI | `--trust-plugin --json results.json --threshold 0.8 --model ... --judge-model ... --no-publish --max-cost-usd 20`; exits 0/1/2/130/143 | plugin-evals#run-evals-in-ci | [P] |
| Availability | v2.1.269+, git 2.31+; "Anthropic has switched the command off server-side" is a possible state ("currently in early access"/"currently unavailable") | plugin-evals#troubleshooting | [P] |
| validate | `claude plugin validate <path> [--strict] [--json]`; exit 0 pass / 1 fail / 2 validator error; picks marketplace.json, else plugin.json, else component dirs by directory name | plugins/cli-reference#plugin-validate | [P] |
| validate does not follow symlinks | "Claude Code doesn't follow symlinks inside the directory you name"; linked skills/agents dirs "warns that nothing in it was read" | same | [P] |
| Marketplace run does not open plugin files | "from a marketplace directory, Claude Code doesn't open the skill, agent, command, or hook files of plugins the marketplace lists in other directories" | same | [P] |
| `plugin details` | "Show a plugin's component inventory and projected token cost" (local help) | `claude plugin details --help` | [P] |

### Workflows (workflows, tools, agent-sdk/typescript, workflow-authoring skill)
| Fact | Quote | URL | Tag |
|---|---|---|---|
| What it is | "A dynamic workflow is a JavaScript script that orchestrates many subagents at once"; intermediate results "stay in script variables" | workflows | [P] |
| Script API | `agent(prompt,{label,phase,schema,model,effort,isolation:'worktree',agentType})`, `pipeline`, `parallel`, `phase`, `log`, `args`, `budget`, `workflow()` (one nesting level) | workflow-authoring skill | [P] |
| Custom agent types | "`agentType` uses a custom subagent type ... resolved from the same registry as the Agent tool; composes with schema" | workflow-authoring skill | [P] |
| Schema retries | "If the subagent's output still fails validation after five attempts, the call fails" (`MAX_STRUCTURED_OUTPUT_RETRIES`) | workflows#what-the-saved-script-looks-like | [P] |
| Plugin shipping | "Place the script in a `workflows/` directory at the plugin root"; runs as `/acme-tools:release-audit` | workflows#distribute-a-workflow-in-a-plugin | [P] |
| Limits | 16 concurrent (fewer with fewer CPUs; env 1-256), 4,096 items per call, 1,000 agents per run, no `import()`, no mid-run user input | workflows#behavior-and-limits | [P] |
| Determinism | "makes `Date.now()`, `Math.random()`, and a no-argument `new Date()` throw inside the script" | workflows#edit-a-saved-script | [P] |
| Resume | same session; "Failed: runs again, and so does every agent that started after it"; `resumeFromRunId` "Same session only"; surviving `claude --resume` possible | workflows#resume-after-a-pause; typescript Workflow | [P] |
| Opt-in | `ultracode` keyword works only in human-typed prompts, "It doesn't start a workflow when it reaches the session ... a prompt passed with `-p`" | workflows#where-the-keyword-works | [P] |
| Running in -p/SDK | "available in ... non-interactive mode with `claude -p`, and the Agent SDK"; no prompt, so need allow rule `Workflow` / `Workflow(<name>)`, auto or bypass mode, or a PreToolUse hook returning allow | workflows#approve-the-plan-before-it-runs | [P] |
| Subagents cannot launch workflows | `Workflow` is in the removed-from-subagents list | sub-agents#available-tools | [P] |
| Disable | `disableWorkflows` / `CLAUDE_CODE_DISABLE_WORKFLOWS=1` | workflows#turn-workflows-off | [P] |
| Plan availability | "all paid plans, with Anthropic API access, and on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry" | workflows | [P] |
| Cost warning | `Large workflow` when ">25 agents, or projected token total passes 1.5 million"; default size guideline `medium` (`small` on Pro) | workflows#cost | [P] |
| Cache sharing | same "model, effort level, agent type, tools, output schema, and working directory"; 5 min TTL default; stagger hold 5000 ms | workflows#prompt-caching-in-a-fan-out | [P] |

### Memory, headless, teams
| Fact | Quote | URL | Tag |
|---|---|---|---|
| AGENTS.md is read by Claude Code | a built-in plugin `cc-plugin-agents-md@builtin` reads AGENTS.md; subagents get it unless `omitClaudeMd` | memory#agents-md | [P] |
| Subagent memory vs main | "The main conversation's auto memory isn't loaded into subagents" | memory#how-it-works | [P] |
| Headless | `claude -p`; `--bare` skips "hooks, skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md"; `--plugin-dir`, `--agents <file-or-json>` (file form v2.1.281+) | headless | [P] |
| -p waits for background | "the run stays open until that work completes" (subagents and workflows) | headless | [P] |
| Agent teams | experimental, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, "Spawning teammates also requires an interactive session"; "No nested teams"; "No session resumption with in-process teammates"; enabling makes named subagents become teammates | agent-teams | [P] |

## 2. CORRECTIONS to Z1-claude-platform.md

| # | Z1 claim | Verified | Severity |
|---|---|---|---|
| 1 | Header caveat: hooks/subagents read only first 100k; `stop_hook_active` and loop caps [U] | Resolved. `stop_hook_active` exists on Stop and SubagentStop; hard 8-consecutive-continuation cap (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`), resets on any tool call. A blocking Stop hook cannot loop forever; it silently ends the turn after 8 blocks. | High (WP-616 answer) |
| 2 | "Retry caps must be implemented in the hook (counter file keyed on agent_id)" | Partly stale: the platform already caps at 8; a counter is only needed for a cap other than 8 (the repo's cap is 3, so a counter IS still needed to stop at 3). Note: past the cap Claude Code ends the turn, it does not fail the gate, so a cap-exhausted gate looks like a pass unless the hook records it. | High |
| 3 | SubagentStop validator can check the output | Wrong in auto mode: on v2.1.271+ a subagent using `SubagentHandback` delivers the report via that tool; `last_assistant_message` is only closing text. A schema validator must hook `PreToolUse`/`PostToolUse` matcher `SubagentHandback` and read `tool_input.message` (and handle the non-handback case). Handback is "Provided only in auto mode" and excludes forks. | High |
| 4 | "Hooks ~36 events" | 33 events in the lifecycle table. | Low |
| 5 | "Spawn depth ... `Agent(x,y)` allowlist in tools: use `tools: Agent(...)` to restrict who can spawn whom" | Wrong for subagents. The allowlist "applies only to an agent running as the main thread with `claude --agent`"; in a subagent definition the type list is ignored. Restrict spawning by omitting `Agent` from `tools` or `disallowedTools: Agent` (all-or-nothing), or `permissions.deny: Agent(name)` (session-wide). | High |
| 6 | "Error above 15,000 tokens of agent descriptions" | A startup warning only; every agent still loads. Counts name + description of non-built-in agents, estimated tokens. | Medium |
| 7 | "Skill -> orchestrator subagent -> worker is 2-3 deep: near the limit" | Depth 3 below main, so skill(main) -> orchestrator subagent(1) -> worker(2) -> sub-worker(3) is allowed. Not "near" for 2 layers. But `Workflow` and `AskUserQuestion` are removed from all subagents. | Low |
| 8 | "background subagents get a reduced tool set and cannot ask the user" | Correct, but incomplete: AskUserQuestion is removed from ALL subagents (foreground too), background is the DEFAULT when fork mode is off (which includes `-p`/SDK), and `SendMessage`-resumed agents resume in the background. | Medium |
| 9 | Plugin bundle: "`claude plugin validate [--strict]`" and implied that validation protects the repo | The repo's plugin.json files live at `plugins/<id>/plugin.json`, not `.claude-plugin/plugin.json`; validate on the plugin directory reports a vacuous "Validation passed" with `manifest: null, contents: []` (see section 3). | High |
| 10 | "Ten plugins sharing `shared/` need dependency declarations or duplication" | Neither works for file sharing. `dependencies` only guarantees another plugin is enabled. Files outside a plugin dir are not copied to the cache; the only supported sharing is a symlink to elsewhere in the same marketplace, which is dereferenced (copied) at install, and `validate` does not follow symlinks. The repo's `plugins/<id>/shared -> ../../shared` is of that kind. | Medium |
| 11 | Plugin eval graders "regex, tool_used, file, llm rubric (judge)" | Six types: regex, tool_used, tool_order, file_exists, llm, baseline. No custom-code graders. | Low |
| 12 | Eval "CI threshold; costs real tokens" | Add: Δ never changes the exit code (only absolute score vs `--threshold`); `tool_used: Skill` graders are excluded from scoring in two-arm runs; runs start in an EMPTY workspace; Bash/Write need `--allow-tools`; Bash needs an OS sandbox; command can be disabled server-side. | Medium |
| 13 | Workflow row | Add: `agentType` option lets `agent()` use a custom (plugin) subagent; `effort`, `model`, `isolation:'worktree'` per call; `workflow()` one level; `Date.now/Math.random` throw; `Workflow` unavailable inside subagents; `ultracode` keyword does not trigger in `-p`, so headless needs an allow rule; resume is same-session; failed agent re-runs all later agents; meta must be a pure literal. | Medium |
| 14 | "`maxTurns` makes results resumable" | Correct; partial marking v2.1.246+. | none |
| 15 | "Skills ... after compaction only the most recent ~5K tokens per skill is kept" | Correct (5,000 per skill, 25,000 combined, most recent first). | none |
| 16 | "Plugin-agent restrictions: ignore hooks, mcpServers, permissionMode" | Also `initialPrompt` ignored. Correct otherwise. | Low |
| 17 | "Agent teams ... skills and plugin hooks NOT applied" | `skills` not applied: verified. Plugin hooks still run in the session (hooks fire for teammates). Teams reuse `tools`, `model`, `disallowedTools`, `effort`, `autoCompactWindow`, body. | Low |
| 18 | Subagent frontmatter list | Missing `color`; `name` max 256 chars and no `:`; correct otherwise. `experimental.cacheTtl` correct. | Low |
| 19 | "Fork / background / resume: `/subtask` fork" | Fork mode is on by default only in interactive sessions; off in `-p`/SDK unless enabled. | Low |
| 20 | "Plugin hooks as deterministic gates (PreToolUse path fences; TaskCompleted blocking)" | Correct, but all matching hooks run in parallel, a failing/timed-out hook does NOT block unless `onFailure:"block"` (v2.1.295+; local CLI 2.1.292 lacks it), and a plugin hook fires for every subagent/session event, so it must be matcher-scoped (`^scribe:exit-gate$`). | High |
| 21 | Skill row implies `allowed-tools` restricts | It is a per-turn pre-approval; use `disallowed-tools` to remove tools; per-agent `tools` restricts. | Medium |

Unchanged and confirmed: `omitClaudeMd` (v2.1.271+), `skills` preload 32, memory 200 lines/25KB, `isolation: worktree`, 20 concurrent, CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH, `${CLAUDE_PLUGIN_DATA}`, `bin/`, workflow 16/1,000 limits, root CLAUDE.md not loaded, agent teams off by default and interactive-only.

## 3. Conformance run (Claude Code 2.1.292, read-only, repo worktree)

Environment: `claude --version` -> `2.1.292 (Claude Code)`. `claude plugin --help` lists: configure, details, disable, enable, eval, help, init|new, install|i, and the rest (install, list, marketplace, prune, tag, test, uninstall, update, validate). `claude plugin eval` was NOT run.

Repo layout observed: `.claude-plugin/marketplace.json` (the root `marketplace.json` is also present); each `plugins/<id>/` has `plugin.json` at the plugin ROOT (no `.claude-plugin/` directory), `agents/`, `skills/`, symlinks `shared -> ../../shared` and `subagents -> agents`.

Commands and verbatim results:

```
$ claude plugin validate .
Validating marketplace manifest: .../frontend-design-evaluation/.claude-plugin/marketplace.json

✔ Validation passed
$ claude plugin validate . --strict
Validating marketplace manifest: .../.claude-plugin/marketplace.json

✔ Validation passed
```

```
$ claude plugin validate plugins/scribe          (same shape for any plugin dir)
Validating components in: .../plugins/scribe

✔ Validation passed
$ claude plugin validate plugins/scribe --strict --json
{ "success": true, "strict": true, "target": ".../plugins/scribe", "manifest": null, "contents": [] }
```
-> Vacuous: `manifest: null`, `contents: []`. The validator found no `.claude-plugin/plugin.json` and no `.claude/` component dirs, so it checked nothing. `claude plugin validate <plugin dir>` gives a false pass for all 10 plugins.

Validating the root `plugin.json` explicitly, for each of courier, mason, muse, navigator, ranger, sentinel, smith, vanguard, weaver and scribe (identical output for all ten):
```
$ claude plugin validate plugins/<id>/plugin.json
Validating plugin manifest: .../plugins/<id>/plugin.json

⚠ Found 3 warnings:

  ❯ id: Field 'id' belongs in the marketplace entry (marketplace.json), not plugin.json. It's harmless here but unused — Claude Code ignores it at load time.
  ❯ consumes: Unknown field 'consumes'. Claude Code ignores it at load time.
  ❯ produces: Unknown field 'produces'. Claude Code ignores it at load time.

✔ Validation passed with warnings
$ claude plugin validate plugins/scribe/plugin.json --strict
... (same 3 warnings)
✘ Validation failed (--strict treats warnings as errors)
```

Component directories, explicit (all 10 plugins, `agents` and `skills`):
```
$ claude plugin validate plugins/<id>/agents    -> Validating components in: .../plugins/<id>/agents ✔ Validation passed
$ claude plugin validate plugins/<id>/skills    -> Validating components in: .../plugins/<id>/skills ✔ Validation passed
```
(20 runs, no warnings or errors. Note this passes agent files carrying unrecognized keys such as `role`, and skill files carrying `version`, because unknown frontmatter is ignored silently by design; the validator does not flag them.)

Findings from the run:
1. `--strict` fails every plugin manifest on `id`, `consumes`, `produces` (warnings, ignored at load).
2. Manifest location `plugins/<id>/plugin.json` is not the documented `.claude-plugin/plugin.json`. The manifest reference documents only the latter; the eval page tolerates "`plugin.json` or `.claude-plugin/plugin.json`". Whether the runtime loads a root `plugin.json` for a `git-subdir` marketplace install was NOT proven here [U]. If it does not, the marketplace entry is the manifest (name/description from marketplace.json) and `skills: "./skills/"` / `agents:[...]` from plugin.json are dropped; defaults `skills/` and `agents/` still load. A load test (`claude --plugin-dir plugins/scribe` then `claude plugin details`/`/plugin` Errors tab) would settle it; I did not run an interactive session.
3. Root `marketplace.json` and `.claude-plugin/marketplace.json` both exist (the repo's `diff` was not run because the shell blocked git-adjacent forms); the validator reads only `.claude-plugin/`.
4. `author` in these manifests is an object (OK). AGENTS.md rule 13 ("author": "Gabriel Castro (Orin DX)") is a string in AGENTS.md text but objects in files; docs require the object form.
5. Not checked by the validator: per-plugin skill/agent files via the marketplace run ("Claude Code doesn't open the skill, agent, command, or hook files of plugins the marketplace lists in other directories").

## 4. PLAN IMPACT

Read: ARCHITECTURE-REVIEW.md (sections 0-10).

| Item | Review assumption | What changes |
|---|---|---|
| Section 9 + WP-616 | "`stop_hook_active` and loop behavior not confirmed; a blocking Stop hook without a counter can loop." | RESOLVED, close the open question: `stop_hook_active` exists; platform hard cap of 8 consecutive continuations (tunable); resets on tool call. The risk is the opposite: at the cap the turn simply ends, so a gate that blocks 8 times is silently bypassed. WP-616 shrinks to: test whether SubagentStop shares/has its own 8-count (docs ambiguous), and the cache-sharing, Codex, AGY, testimonial items. |
| WP-602 (SubagentStop schema validator, `Stop`/`TaskCompleted` blocks, counters) | Hook on SubagentStop reading the output; counter in plugin data | Must change: (a) in auto mode the report is in `SubagentHandback` `tool_input.message`, not `last_assistant_message`; validator needs both paths; (b) matchers must be scoped `^<plugin>:<agent>$` since plugin hooks fire for all subagents; (c) a hook failure/timeout does not block unless `onFailure:"block"` (v2.1.295; local CLI 2.1.292 cannot); (d) block count of 3 needs a counter (platform cap is 8), keyed by `agent_id` in `${CLAUDE_PLUGIN_DATA}`; (e) agent/prompt hooks are experimental/LLM-based, prefer command hooks; (f) hooks run in parallel and `-p` runs under workspace-trust rules for project (not plugin) hooks; (g) the gate cannot rely on the verdict@3 retry counter incremented by the exit-gate agent itself. |
| WP-603 (plugin workflows) | skills remain cross-harness path | Feasible: `workflows/*.js` in plugin, `/plugin:name`. Add constraints: `agent({agentType:'plugin:agent', schema})` composes with schema; `Workflow` tool is stripped from subagents (a skill running as `context: fork` subagent cannot launch one); `-p` needs `Workflow`/`Workflow(name)` allow rule; `ultracode` keyword does not work in `-p`; resume is same-session only and re-runs everything after a failed agent; no `import`, no clock/random; schema retries 5 (not 3). Whether a workflow `agent()` with `agentType` honors the agent's `tools`/`model`/`effort` frontmatter is likely but not documented [U]. |
| WP-601 (eval suite with baseline) | Native plugin eval with/without arms; "hand-off schema validity is gradable via file graders" | Constraints: runs start in an empty workspace (needs `scaffold_script` + `--scaffold`); Bash/Write require `--allow-tools` and an OS sandbox (WSL2 on Windows); only the six graders, no code graders (so schema validation needs a `bin/` validator run through `Bash` + `tool_used`/`file_exists`, or a regex); `Skill`-fired graders are unscored in two-arm; `max_turns` cap 200, `timeout_seconds` cap 3600 (a long pipeline may not fit); Δ never gates CI; command may be disabled server-side; requires 2.1.269+ (met). Cross-harness fixtures (hidden-oracle `mason:evaluate`) remain complementary. Claude `plugin eval` cannot run skills that spawn many subagents cheaply; budget with `--max-cost-usd`. |
| WP-605 (agent-count audit), ADR 003 | collapsed variants tested via WP-601 | Fine; note collapsed variant needs `plugins/<id>/agents` dirs swapped via `--plugin-dir` copies. |
| WP-606 (native agent controls) | `maxTurns`, `tools` allowlists, worktree isolation, `skills` preload, `effort` | Mostly supported in plugin agents. Corrections: `tools` allowlist only restricts the agent itself; `Agent(x,y)` spawn-allowlist does NOT apply to subagents; spawn restriction = omit `Agent`. `skills:` preload is blocked for skills with `disable-model-invocation:true` and cannot preload a skill from another plugin unless discoverable. Background subagents drop non-listed built-ins (e.g. `AskUserQuestion`, `Workflow`, `EnterPlanMode`), so `tools` lists naming them fail silently. `memory:` needs auto memory enabled. `isolation: worktree` valid in plugin agents. |
| WP-615 (platform-limit checks in `just check`) | description budget "15,000 tokens; now about 6.7k" is a hard limit | It is a warning and counts name+description of non-built-ins as the CLI estimates; ~6.7k is a 4 chars/token estimate. Add checks: unknown frontmatter keys (the repo's `role`, skill `version` are silently ignored, so they are dead weight); `name` max 256 and no `:`; plugin.json location and `.claude-plugin/`; unknown manifest keys (`id`, `consumes`, `produces`) under `--strict`; strip `hooks`/`mcpServers`/`permissionMode`/`initialPrompt`. Make `claude plugin validate` a real gate by validating `plugins/<id>/plugin.json`, `agents/`, `skills/` explicitly, not the plugin dir. |
| Section 1 table: "Skill frontmatter keys: name, description, version" and "Agent keys: name, role, model, effort, description" | treated as in use | `version` (skills) and `role` (agents) are not recognized fields and are silently ignored. Descriptions of agents ARE read (routing); `role` has no runtime effect. |
| Section 0 item 3 / assumption 14 | description budget fine at 45% | Still true as estimate; reword as warning. Plugin-scoped name (`scribe:exit-gate`) adds characters to name count. |
| Assumption 7 (orchestration) | skills spawn subagents turn by turn | Add: skill with `context: fork` already exists natively for 1:1 spawn (runs in background by default; waits in `-p`/SDK). |
| Assumption 12 / WP-610 (two trees, shared) | `shared/` linked per plugin | The `shared -> ../../shared` symlink works only because it resolves within the same marketplace (dereferenced at install); `claude plugin validate` and local-path installs ("preserves only symlinks that resolve within the plugin's own directory") do not follow it. Install via `git-subdir` (as marketplace.json does) copies the content once per plugin: 10x duplication in cache, no deduplication. Plugin `dependencies` cannot share files. |
| Assumption 11 (memory / persistence) / WP-612 | plugin data dir + subagent memory | Verified. `${CLAUDE_PLUGIN_DATA}` kept across updates; deleted on last uninstall by default. Subagent `memory` needs auto memory on. |
| Assumption 3 / WP-604 (cache prefix) | cache shared only with same model/effort/type/tools/schema/cwd, 5 min TTL | Verified for workflows; the same condition list for subagents is linked (prompt-caching#subagents-and-the-cache) but I did not read that page; resumed subagents reuse their own cache. `experimental.cacheTtl: 1h` per agent file; `subagentPromptCacheTtl` setting. |
| Section 6 Codex/AGY bullets | n/a | Not covered by Claude Code docs; unchanged. |
| WP-613 (resume repair loops) | `SendMessage` resume | Verified; resumed subagent keeps original tool set, per-invocation `model`/`effort` persist. Resume is by agent ID or `name` given at spawn; resuming runs in the background; `-p` ends only when background work finishes. A name collision is refused. In agent-teams-enabled sessions, a named subagent launches as a teammate instead (so keep teams disabled). |
| WP-607 render adapters | n/a | Not covered here. |
| Assumption 6 (retry cap 3 then human) | gate escalates to human | Subagents cannot call `AskUserQuestion`; the escalation must happen in the orchestrating main session, and in workflow/`-p` there is no mid-run user input. |
| New risk | not in review | Subagent final reports are scanned and may be altered (backslash insertion, `[harness: ...]` marker line) when they contain `<system-reminder>` or permission-setting words; JSON verdicts quoting such text could break schema parsing. Reports are also classifier-reviewed in auto mode. |
