# Native plugin eval and skill-doctor assessment (WP-517, WP-601)

Date: 2026-10-20. Local CLI: Claude Code 2.1.292 (docs require 2.1.269+). Sources, all raw pages saved in `/Users/gabe/.claude/jobs/2d213021/tmp/docs/`: `plugin-evals.md` (read in full), `plugins_cli-reference.md` (plugin eval sections), `skills.md` (skill-doctor, eval sections), `errors.md`, `memory.md` (grep); repo: `plugins/mason/skills/evaluate/SKILL.md`, `plugins/mason/agents/evaluation-{runner,adjudicator}.md`, `shared/references/evaluation/behavioral.md`, `docs/codex-behavioral-evaluation.md`, `tests/fixtures/{behavioral,cross-harness}/`, `verification/Y1-claude-code-docs.md`.

Evidence tags: [P] stated in the docs or repo; [E] my estimate or inference; [U] unverified.

Local check: `claude plugin --help` lists `eval [options] [target]` ("Run eval cases (<eval dir>/**/case.yaml or prompt.md + graders/*.md ...") and `details` ("component inventory and projected token cost"). I could not run `claude plugin eval --help`: the sandbox guard refuses any command containing the word `eval`. Option names below come from the docs, not from the local help text [U for local option parity]. No eval was run.

## 1. How `claude plugin eval` works

Call: `claude plugin eval [target] [options]` (plugins/cli-reference#plugin-eval). Target is a plugin dir, one `prompt.md`/`case.yaml`, `name[@marketplace]`, or `name@skills-dir`. Default: current directory.

**Case files and location [P].** Suite dir is `evals/` under the plugin root, or the manifest key `experimental.evals`, or `--eval-dir` (relative, no `..`). A case is a subdirectory holding `prompt.md` and/or `case.yaml`; "a case without one fails to load" if it has no grader (plugin-evals, Write and refine cases). Layout:

```text
plugins/<id>/evals/<case>/prompt.md        # frontmatter = run fields; body = prompt, sent verbatim
plugins/<id>/evals/<case>/graders/<n>.md   # frontmatter = type + options; body = rubric (llm)
plugins/<id>/evals/<case>/case.yaml        # optional: schema_version "1.1", name, context.*
plugins/<id>/evals/mocks/<server>/<tool>.md  # optional MCP mocks
plugins/<id>/evals/results/<ts>/           # aggregate-result.json, report.html (gitignore)
```

`prompt.md` fields: `name, description, tags, plugins, runs (1-50, default 3), expected_outcome, model, max_turns (default 10, cap 200), timeout_seconds (default 300, cap 3600), allowed_tools, append_system_prompt, env (EVAL_* only)`. "An unknown key is an error." `plugins:` is a list, so one case can load several plugin dirs [P].

**Graders [P].** Six types: `regex` (target: last_message default, trace, files, file contents, mock_calls; `match: not_contains` or `count:N`; JS regex, `flags: i`), `tool_used` (tool, `input_match` regex over JSON input, min, max), `tool_order`, `file_exists` (only files created in the run), `llm` (3 judge votes, 2 must PASS), `baseline` (judge vs a reference `.jsonl`). Quote: "There are no custom-code graders." `weight` and `arm` (`with-only`, `both`) are per grader. The llm judge sees the first 12 and last 12 trace messages, or the final message, or one file.

**Arms and scoring [P].** Each run: fresh isolated `claude -p` child with a temp home, cwd and config. Default 3 runs per arm. Score = weighted fraction of graders passed; case score = mean of runs; case passes at `--threshold` (default 1.0). Default is two arms, with plugin and with none ("W/OUT"); Δ = with minus without. Quote: "If a case scores 1.0 both with and without the plugin, the plugin isn't what made it pass." In two-arm runs these graders are unscored indicators: every `tool_used` with `tool: Skill`, `mock_calls` graders on the plugin's own mocks, and `arm: with-only`. Single arm by default for `history_file` cases and for a case whose plugin was not resolved (set `plugins: ["../.."]`). A `tool_used` on `Agent` is NOT auto-excluded, so without `arm: with-only` it fails in the baseline and inflates Δ [E, from the exclusion list].

**Workspace [P].** "Each run starts in an empty working directory." Fixtures need `case.yaml` `context.scaffold_script` (Bash, runs as you, only with `--scaffold`, 120 s limit, files and git state only), `context.add_dirs` (read-only), or `history_file`. Nothing from user settings, CLAUDE.md, AGENTS.md, other plugins, memory, `.claude/` or `.mcp.json` loads, and the eval dir is hidden from the agent: "The case definitions are hidden from the agent." The Artifact tool is off.

**Tools [P].** Never prompts. Read-only set grantable per case via `allowed_tools`: Read, Glob, Grep, NotebookRead, Skill, AskUserQuestion, Agent, TodoWrite, task tools. Bash, Write, Edit, WebFetch, WebSearch only via run-wide `--allow-tools`; Bash runs under the OS sandbox (macOS ok, needs bubblewrap/socat on Linux, WSL2 on Windows). Plugin hooks do load and run outside the sandbox. Plugin agents are dispatchable by namespaced name (`scribe:exit-gate`) when `Agent` is allowed; in the baseline the same call fails with "Agent type ... not found", which the docs call expected.

**Limits and parallelism [P].** `-j` 1-8 (default 1), shared rate limit. `--model` pins the agent under test; `--judge-model` pins the judge (default: the background-task model).

**Cost model [P].** "roughly cases × runs agent runs with the plugin and the same number again" without it, plus "three short judge calls per `llm` or `baseline` grader per run". Reported cost is a list-price estimate, not billing. `--max-cost-usd` is checked before each run starts; started runs finish, so overshoot is possible; unstarted runs mean exit 2 with `partial: true`. `--ablation none` runs one arm. The only dollar figure in the docs is the illustration `1 case, 6 runs, $0.41` for a trivial skill, about $0.07 per run [P].

**Exit codes [P].** 0 pass; 1 case below threshold, load error, no cases, run could not start, API-error run, untrusted dir without `--trust-plugin`, bad option or unwritable JSON; 2 partial (cost ceiling or rejected credential); 130 interrupted; 143 terminated. Quote: Δ "is reported but never changes the exit code."

**Output [P].** `aggregate-result.json` (`schemaVersion: 1`: `aggregates.overallScore`, `casesPassed`, `meanDelta`, `cases[].arms.with[].error`, `costUsd`, `claudeVersion`), `report.html`, optional private artifact publish (`--no-publish` to keep local).

**What it cannot do [P unless noted].**
- No custom-code graders: no JSON Schema validation, no source-citation checking. Only regex over text, tool-call counts, file existence, and an LLM judge.
- Empty workspace; any fixture repo needs `--scaffold`, which trusts the script.
- Claude Code only. No Codex or AGY. No team mode.
- One `claude -p` session per run: no interactive turns, no `AskUserQuestion` answers, no mid-run human.
- Skills that write or run code need run-wide Bash/Write/Edit grants, applying to every case in the run.
- Subagent-heavy pipelines are bounded by `max_turns` 200 and `timeout_seconds` 3600 per run.
- Hooks you did not write make scores "advisory" unless run in a container or CI runner.
- Can be switched off server-side ("plugin eval is currently unavailable") and has an "early access" state.
- Does not record plugin source revision or dirty state; it records `claudeVersion` only [E, from the field list].
- Whether `@path`-style or skill-relative `../../shared` reads work in the temp copy is not documented [U].

## 2. Comparison with `mason:evaluate`

| Dimension | `claude plugin eval` | `mason:evaluate` (runner + adjudicator) |
| :-- | :-- | :-- |
| Purpose | Fast, repeatable measure of "did the plugin cause this behavior" with a no-plugin control | Release gate and cross-harness comparison on a fixed fixture with provenance (SKILL.md Outcome) |
| Unit | Prompt + mechanical graders, k runs per arm | One fixture run per record, one `harness-evaluation@2` |
| Baseline | Built in (no-plugin arm, Δ) | None. Compares runs only on identical fixture/route/provenance |
| Isolation | Mechanical: temp home, no user/project config, case dir unreadable by the agent | Convention: "Copy only public input into a disposable workspace"; oracle kept out by instruction. The oracle JSON sits in the same repo as the plugin |
| Oracle | Graders are the oracle; hidden because the eval dir is unreadable. Static patterns only | Real hidden oracle (`oracle.seeded_defects`, `false_pass_if`) judged by an independent Opus adjudicator after the run |
| Judgment | 3-vote small-model judge over a final message or 24 trace messages | Adjudicator follows cited evidence to source, validates schemas, tests consumer usability, counts false passes and corrections |
| Provenance | `claudeVersion`, model flags, cost | host, model, mode, roles, plugin versions, source revisions, dirty state |
| Harness | Claude Code only | Claude and Codex (single-agent and team), per `docs/codex-behavioral-evaluation.md` |
| Cost | List-price estimate per run, `--max-cost-usd` | Not metered by the tool; one runner plus an Opus adjudicator per run |
| CI | Native: exit codes, JSON, threshold | Manual or session-driven; no exit code |

Overlaps: both run a workflow on a fixed input in a clean workspace and refuse credit for tool invocation alone. Gaps in `mason:evaluate`: no baseline arm, no repetition (k=1), no mechanical isolation, no CI gate. Observed in the worktree: `tests/fixtures/behavioral/implementation-verification.json` names four `workspace_fixture` values, but `tests/fixtures/` holds only two JSON files and no workspace directories, so the suite cannot run as committed [P, from directory listing]. Gaps in native eval: no schema or source-evidence validation, no cross-harness, no provenance of plugin revision, empty workspace, judge is weaker than the adjudicator.

**How to combine [E].**
1. Static layer stays `just check` (schemas, manifests, `claude plugin validate` on explicit paths).
2. Native eval is the cheap, repeatable, CI-able layer for: trigger routing, contract-shape adherence, default-fail behavior, negative controls, and "what does the plugin add" Δ. It is where WP-601 and WP-605 collapsed-variant tests belong.
3. `mason:evaluate` stays the release-gate layer for seeded-defect fixtures, cross-harness lifecycle (`lifecycle.json`), and any judgment needing evidence-to-source checks. Fixes needed: commit the workspace fixtures; pass `aggregate-result.json` `claudeVersion` and `costUsd` into the run record; keep the oracle outside the plugin dir used by the runner.
4. Hybrid for hidden-oracle-lite: put expected detections in native graders (`regex` on `src/tag.ts:37` in the final message, `tool_used` min/max) with a `scaffold_script` building the workspace. Keep full-credit adjudication in `mason:evaluate`.
5. Do not average the two. Report native Δ and adjudicated pass/fail separately, per `behavioral.md` ("Do not average independent failures into a passing score").

## 3. `skill-doctor`

Found in `skills.md` (#find-unused-skills), `errors.md`, `plugins_cli-reference.md` (`/plugin stats`). It is a built-in slash command, not a skill and not part of plugin eval:
- Quote: "Run `/skill-doctor` to see what each of your skills costs and how often it gets used."
- Interactive: report opens in the `/plugin` manager's Stats tab. Non-interactive: `claude -p "/skill-doctor"` prints text.
- Scope: skills in the session other than bundled and enterprise skills; flags skills in the listing never invoked and says where to turn them off; lists plugins not used recently.
- Needs 2.1.252+; unavailable when feature-flag fetching is skipped; over Remote Control it replies "Skill usage reports are not available on this connection."

Applies to this repo: partly. It measures context cost of the skill listing (30 skills, 44 agents across 10 plugins counted by directory) and real usage by one user, so it is a telemetry check for a maintainer who has installed the plugins (the owner's dogfooding), not a quality test and not CI-able. It answers "which skills are never fired" and "what does the listing cost", which supports the WP-615 description-budget item and WP-605 agent-count audit as input. It cannot compare against a baseline, and it counts only skills, not subagent descriptions. Related and cheaper static tools: `claude plugin details <plugin>` ("projected token cost"), `/doctor` (listing cost estimate), and `/doctor prompt-audit` (memory.md; audits CLAUDE.md, AGENTS.md and `.claude/` skills and subagents by default, so a plugin path must be passed explicitly [U whether it accepts plugin dirs]). Recommended use: run `claude -p "/skill-doctor"` once from a normal working session where all 10 plugins are enabled and record the output as WP-517 baseline evidence; not run here.

## 4. First eval suite for this repo

**Layout decision [E].** One target plugin per directory, so keep each case under the plugin that owns the skill (`plugins/scribe/evals/...`), using `plugins: ["../.."]` when needed. Cross-plugin cases list several dirs in `plugins:`. Verify first that the Codex build (`tools/build-codex-marketplace.py`) and the marketplace `git-subdir` install ignore or exclude `evals/`, and add `evals/results/` to `.gitignore`.

**Design rules.** Inputs go in the prompt (empty workspace). No Write/Bash in v1: results come back in the final message, so no `--scaffold` or `--allow-tools`. Each case has one result grader and one process grader, per the docs' advice. Mark `Agent` graders `arm: with-only`. Pin `--model claude-sonnet-5` (the docs' CI example) and `--judge-model` to a stronger model than the default for llm graders.

| # | Case (plugin) | Prompt (summary) | Graders | Why plugin vs none discriminates |
| :-- | :-- | :-- | :-- | :-- |
| 1 | `gate-spec-rejects-vague-spec` (scribe) | Inline `spec@1` with "fast", a TBD, no error case: "Is this spec ready for planning?" | regex `"verdict"\s*:\s*"fail"`; regex blockers mention error case and TBD; Skill gate-spec (indicator); Agent `scribe:exit-gate` (with-only) | Plugin gives default-fail `verdict@3`; baseline Claude catches defects but not in the contract shape. The semantic blocker grader may show Δ near 0: that is a real finding |
| 2 | `capture-need-omits-unknowns` (weaver) | Free-text need with no stakeholder named | regex requires `statement`, `done_when`; regex `not_contains` fabricated stakeholder value; regex `out_of_scope` is empty; Agent `weaver:intake` (with-only) | Plugin contract says omit, never fabricate, no clarifying question; baseline tends to invent a stakeholder or ask |
| 3 | `draft-spec-no-tbd-error-cases` (scribe) | Inline `requirement@1`: "spec this out" | regex `not_contains` `TBD`; regex `count`-style `is_error_case"\s*:\s*true` at least once; regex `non_goals`; llm: each criterion falsifiable from outside | Plugin enforces no TBD, `is_error_case`, non-empty `non_goals`; baseline writes prose |
| 4 | `component-spec-states-and-a11y` (muse) | "Spec a combobox component" | regex per state (hover, focus, disabled, loading, error, empty) via `count`; regex role/keyboard; Agent `muse:drafter` (with-only); llm on testability | Plugin demands every state and ARIA criteria; this is the frontend-facing case for the branch |
| 5 | `plan-covers-every-criterion` (navigator) | Inline 3-criterion `spec@1`: "write a plan" | regex each `AC-00N` appears in a `covers_criteria`; regex `commit_message` per task; regex `not_contains` "as appropriate" | Plugin forces exact files, commit messages and total criterion coverage; baseline outlines steps |
| 6 | `clarify-asks-one-question` (weaver) | Inline thin `requirement@1` | regex `count:1` on question marks in the question field; llm: asks the single highest-priority gap | Plugin rule "one question per invocation, never a list" |
| 7 | `commit-message-control` (courier) | Inline diff: rename `getUser` to `fetchUser`, "commit this" | llm: conventional type, explains why not what | Control: Claude already does this; expect Δ near 0 and the case proves the harness measures no false lift |
| 8 | `unrelated-request-no-hijack` (scribe, sentinel, weaver via `plugins:`) | "What does this regex do? `^a+$`" | `tool_used` Skill min 0 max 0 with `arm: both`; `tool_used` Agent min 0 max 0 with `arm: both` | Over-triggering of 30 skill descriptions; both arms must be clean |
| 9 | deferred: `ts-semantic-sibling-audit` (ranger, smith) | Public input of `typescript-semantic-sibling` | needs hidden oracle: sibling site must be found, not just the reported one | Needs scaffold + Bash + committed workspace; keep in `mason:evaluate` |
| 10 | deferred: `go-fresh-state-gate` (sentinel) | Public input of `go-fresh-state` | needs hidden oracle: reads post-mutation state, no pending goroutines | Needs real execution and evidence-following; keep in `mason:evaluate` |

Cases 1-8 are the v1 suite (8 cases). Cases 9-10 need hidden oracles (seeded defects, evidence-to-source checks) and stay on `mason:evaluate` until their workspaces are committed.

**Cost estimate [E, not from docs].** The docs give only the $0.07 per-run trivial figure. Pipelines here dispatch Sonnet or Opus-high subagents, so with-plugin runs cost more than the example:

| Case | With-plugin per run | Without per run |
| :-- | :-- | :-- |
| 1 gate-spec | $0.30 - 0.90 | $0.02 - 0.08 |
| 2 capture-need | $0.05 - 0.15 | $0.02 - 0.05 |
| 3 draft-spec | $0.30 - 0.80 | $0.03 - 0.08 |
| 4 muse component | $0.30 - 0.80 | $0.03 - 0.08 |
| 5 plan | $0.40 - 1.00 | $0.03 - 0.10 |
| 6 clarify | $0.05 - 0.15 | $0.02 - 0.05 |
| 7 commit | $0.05 - 0.15 | $0.02 - 0.05 |
| 8 no-hijack | $0.02 - 0.10 | $0.02 - 0.05 |
| Sum (one run each) | $1.47 - 4.05 | $0.19 - 0.54 |

Full run at 3 runs per arm: with-arm $4.4 - 12.2, without-arm $0.6 - 1.6, judge calls (cases 1, 3, 4, 6, 7 have llm graders, 3 votes each, both arms, 30 grader runs, 90 votes) about $0.5 - 2. Total about $6 - 16 per full run. `--ablation none` saves only the without-arm, about $1 - 2, because the baseline is cheap here; iterate with `--case X --runs 1 --ablation none` at $0.1 - 1 per case. Treat the numbers as assumptions to calibrate on a single pilot case; the reported `costUsd` is authoritative. Recommended first command: `claude plugin eval plugins/scribe --case gate-spec-rejects-vague-spec --runs 1 --ablation none --max-cost-usd 3` (no tool grants needed). Then CI: `--trust-plugin --json results.json --threshold 0.8 --model claude-sonnet-5 --judge-model <stronger> --no-publish --max-cost-usd 20`.

### Example case A: `plugins/scribe/evals/gate-spec-rejects-vague-spec/`

`prompt.md`:

```markdown
---
name: gate-spec-rejects-vague-spec
tags: [smoke, gate]
plugins: ["../.."]
runs: 3
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Agent]
---

Is this spec ready to go to planning? Here it is:

{"id":"SPEC-901","purpose":"Make the export button fast.","scope":"Export button on the reports page.","non_goals":["Redesign the reports page"],"acceptance_criteria":[{"id":"AC-001","criterion":"Export completes quickly for typical reports."},{"id":"AC-002","criterion":"Error handling is TBD."}]}
```

`graders/verdict-fail.md`:

```markdown
---
type: regex
pattern: '"verdict"\s*:\s*"fail"'
flags: i
---
```

`graders/names-defects.md`:

```markdown
---
type: llm
weight: 2
---

PASS if the final message rejects the spec and its blockers name all three defects: the unmeasurable word "fast"/"quickly", the TBD in AC-002, and the absence of an explicit error case.
FAIL if it passes the spec, or names fewer than three of these defects, or only gives generic advice.
```

`graders/exit-gate-dispatched.md`:

```markdown
---
type: tool_used
tool: Agent
input_match: '"subagent_type"\s*:\s*"scribe:exit-gate"'
arm: with-only
---
```

`graders/skill-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?gate-spec"'
---
```

(The last grader is an unscored indicator in a two-arm run, by the docs' rule.) The `subagent_type` field name is my assumption of the Agent tool input key [U]; confirm from a `--keep-temp` trace before relying on it.

### Example case B: `plugins/weaver/evals/capture-need-omits-unknowns/`

`prompt.md`:

```markdown
---
name: capture-need-omits-unknowns
tags: [smoke, intake]
plugins: ["../.."]
max_turns: 15
allowed_tools: [Read, Skill, Agent]
---

We need to cut checkout abandonment, people are leaving at the payment step.
```

`graders/required-fields.md`:

```markdown
---
type: regex
pattern: '"statement"\s*:[\s\S]*"done_when"\s*:\s*\['
---
```

`graders/no-fabricated-stakeholder.md`:

```markdown
---
type: llm
weight: 2
---

PASS if the output is a requirement object that either omits the stakeholder field or leaves it unfilled, asks no clarifying question, and leaves out_of_scope empty or absent.
FAIL if it invents a named stakeholder or role not stated in the request, asks the user a question, or fills out_of_scope.
```

`graders/intake-dispatched.md`:

```markdown
---
type: tool_used
tool: Agent
input_match: '"subagent_type"\s*:\s*"weaver:intake"'
arm: with-only
---
```

Optional `case.yaml` is not needed for either case (no fixtures, no scaffold). Both are expected to show a high WITH and a lower W/OUT on the shape graders; the llm grader decides whether the plugin adds judgment or only format.

## 5. Risks and checks before running

1. **Cost.** All numbers above are my estimates. Run one case at `--runs 1 --ablation none --max-cost-usd 3`; read `costUsd`; extrapolate. The ceiling is a pre-run check, so a started Opus-high run can overshoot [P].
2. **Server-side disable or early access.** "plugin eval is currently unavailable" cannot be fixed locally [P]. Verify the command runs at all before building anything; keep `mason:evaluate` as the fallback.
3. **Option parity.** Local `--help` for `eval` was not read (sandbox guard); run it yourself and compare against the docs' option table. The local CLI (2.1.292) is below the version some docs fixes name (e.g. API-error scoring 0 since v2.1.299 [P]; before that, runs were graded on partial output).
4. **Empty workspace and symlinks.** Each plugin has `shared -> ../../shared` and `subagents -> agents` symlinks, and agents/skills read `shared/...`. Whether an eval copy dereferences them is undocumented [U]. Use `--keep-temp` on the pilot and check that `shared/` resolves in the temp copy; a broken link would make every with-arm run misleading.
5. **Manifest.** The runtime needs `plugin.json` or `.claude-plugin/plugin.json`; the worktree now has the generated `.claude-plugin/plugin.json` (e.g. scribe), so path targets should resolve. If a case shows "ablation requested but no plugin resolved", add `plugins: ["../.."]`.
6. **Trust and security.** Path targets prompt `Trust this plugin directory?` (whole repo is trusted); use `--trust-plugin` only in CI. Plugin hooks (e.g. a handback validator) load and run outside the sandbox, so scores are advisory unless run in a clean runner [P].
7. **Agent dispatch in `-p`.** Subagents default to background in non-interactive mode; `-p` waits for them [P, Y1 table]. `SubagentHandback` exists only in auto mode, so the final message the grader sees may differ by mode [U]. Check one trace for where the verdict text lands.
8. **Δ pitfalls.** `Agent` graders need `arm: with-only`; shape-only regex graders reward contract adherence, not judgment; a negative Δ with a passing Skill grader means suspect the judge [P]. Pin `--model` and `--judge-model`; judge variance is the main noise source. Three runs per arm is low statistical power for `llm` graders; do not treat one run set as proof.
9. **What a green run says.** It does not validate source-cited evidence, schema validity, or seeded-defect detection, and does not cover Codex or AGY. It must not replace `mason:evaluate` for release gates, and a passing bundled suite "says nothing about whether the plugin is safe" [P].
10. **Repo hygiene.** Add `evals/results/` to `.gitignore`; confirm `just check`, `versions`, and the Codex generator tolerate `plugins/<id>/evals/`; the `Agent` tool and `Skill` allowances widen no other grants (case `allowed_tools` cannot widen run-wide grants [P]).

## Recommendation

Adopt native eval as the Layer-2 regression and Δ measurement (WP-601) with the 8-case v1 suite, start with one pilot case to calibrate cost and confirm symlink resolution, and keep `mason:evaluate` for hidden-oracle and cross-harness gates after committing its workspace fixtures. Treat `/skill-doctor` as a one-time maintainer telemetry run, not a test. WP-517 closes as: eval and skill-doctor are complements to, not replacements for, the repo's evaluation machinery.
