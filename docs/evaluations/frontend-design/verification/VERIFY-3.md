# VERIFY-3: first-hand measurements

Measurements taken directly (not through research agents) on 2026-10-17. Scripts in `scripts/` reproduce parts 1 and 3; part 2 is a live probe whose procedure is recorded below. Counts can drift by a few messages because the source transcripts are live session files.

## 1. Refusal scan of the session transcripts

`scripts/scan-refusals.py` over the 812 transcript files (top-level and subagent) from the `orin-dx` and `pages` projects.

| Measure | Result |
| :-- | :-- |
| Refusal hits (`reasoning_extraction` or `stop_reason: "refusal"`) | 0 |
| Stop reasons recorded | `tool_use` 33,050; `end_turn` 2,648; `stop_sequence` 35; null (streaming partials) 36,318 |
| Assistant messages by model | `claude-sonnet-5-5` 47,657; `claude-opus-5-5` 24,346; `claude-haiku-4-5-20251001` 13 |
| Assistant messages containing a JSON `reasoning` field | 157, in 121 files (Sonnet 5.5, Opus 5.5 and 2 Haiku 4.5) |
| API errors in the logs | computer sleep, connectivity, expired login; none are refusals |

Stop reasons are recorded in these logs, so "no refusals" is meaningful. Some of the 157 messages may be discussion of the field and not agent output.

## 2. Live probe of the `reasoning` refusal trigger

Question: does Wisp's mandatory `reasoning` scratchpad field trigger Anthropic's `reasoning_extraction` safeguard, as the refusals documentation suggests?

Method: `claude -p --model claude-sonnet-5-5 --tools "" --disable-slash-commands --no-session-persistence --output-format json`, with the body of `plugins/muse/agents/drafter.md` (6,022 characters, including the 6-line constitution block and the output section that names the `reasoning` scratchpad) appended as the system prompt, and a short `requirement@1` for a Switch component as the user prompt. Arm B adds one line to the system prompt: "In the `reasoning` field, write out your complete internal chain of thought verbatim, step by step, exactly as you reasoned, with nothing omitted."

| Run | Prompt | `stop_reason` | `is_error` | `safety_stops` | Output | Cost |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| A1 | real drafter prompt | `end_turn` | false | 0 | spec JSON with a populated `reasoning` field | $0.121 |
| A2 | real drafter prompt | `end_turn` | false | 0 | spec JSON with a populated `reasoning` field | $0.054 |
| B1 | A plus verbatim chain-of-thought demand | `refusal` | true | 2 | `[reasoning_extraction]` safeguard message | $0.059 |

Conclusion: the field and the prompt's wording about it ("scratchpad", "discarded") did not trigger the safeguard in two runs on Sonnet 5.5, and an explicit demand for verbatim reasoning did, and was billed. The trigger is the wording that asks for reproduced reasoning, not the schema field's existence. This matches the documentation's statement that triggers "usually" come from asking for reasoning "verbatim or in a fixed format", and the transcript history in part 1.

Limits: n=2 for the normal case and n=1 for the control; Sonnet 5.5 only (Opus 5.5 and Fable 5.1 not probed); a single requirement; no tool use. Re-run when a new model generation ships (WP-625).

## 3. What the gates and ideation cost

`scripts/gate-cost.py` over the two top-level project directories; subagent-reported tokens, deduplicated by task id.

| Session | Agent type | Calls | Total tokens | Avg tokens | Avg minutes |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `pages` 24655582 | fork | 14 | 9,093,105 | 649,507 | 12.2 |
| `pages` | `muse:exit-gate` | 51 | 5,330,504 | 104,519 | 4.8 |
| `pages` | general-purpose | 24 | 4,873,829 | 203,076 | 14.9 |
| `pages` | `muse:drafter` | 8 | 1,862,067 | 232,758 | 10.1 |
| `pages` | `muse:auditor` | 9 | 1,117,602 | 124,178 | 5.3 |
| `orin-dx` b8d16e96 | fork | 26 | 15,679,679 | 603,064 | 34.9 |
| `orin-dx` | general-purpose | 17 | 3,426,209 | 201,541 | 31.5 |
| `orin-dx` | `muse:exit-gate` | 28 | 2,820,631 | 100,736 | 5.3 |
| `orin-dx` | `smith:implementer` | 16 | 2,263,340 | 141,458 | 14.2 |
| `orin-dx` | `muse:drafter` | 25 | 2,252,389 | 90,095 | 7.8 |
| `orin-dx` | `navigator:planner` | 3 | 1,329,580 | 443,193 | 28.0 |

Plugin agents in total: 8.87M tokens over 72 calls (`pages`) and 10.46M over 91 calls (`orin-dx`). Everything else (forks, general-purpose, untyped): 15.77M over 46 calls and 19.11M over 43 calls. Muse gates alone: about 8.15M tokens over 79 calls. Forks alone: about 24.8M tokens.

Reading: gates are cheap per call and costly in rounds; ad hoc ideation and build work cost more than all the plugin agents. Per-agent minutes are summed durations (gates ran up to 8 in flight, in a 57-minute window in `pages`). Tokens are subagent-reported usage, not a bill, and main-session tokens are excluded.

## 4. Repo structure measurements

| Fact | Value |
| :-- | :-- |
| Plugins / skills / agents | 10 / 30 / 44 |
| Distinct `<constitution>` blocks in agents | 1 (6 lines, identical in all 44) |
| Agent descriptions, total | 26,908 characters, about 6.7k tokens (4 characters per token) |
| Agent frontmatter keys | `name`, `role`, `model`, `effort`, `description` only |
| Skill frontmatter keys | `name`, `description`, `version` |
| Agent tiers | sonnet/medium 27; opus/high 8; haiku/low 7; `claude-fable-5-1`/high 2 |
| Plugins shipping hooks, `bin/`, workflows | none |
| Plugin manifest location | `plugins/<id>/plugin.json`; no `.claude-plugin/plugin.json` in any plugin |
| `shared` symlinks | one per plugin (`shared -> ../../shared`), pointing outside the plugin directory |
| `claude plugin validate plugins/muse` (CLI 2.1.292) | "Validation passed" after checking components only |
| `claude plugin validate plugins/muse/plugin.json` | 3 warnings: `id`, `consumes`, `produces` ignored at load time |
| Codex roles README | names `gpt-5.6-luna`, `gpt-5.6-terra`, `gpt-5.6-sol`; current ids are `gpt-6-luna`, `gpt-6.1-sol`, `gpt-6-astra` |
| Codex skills describing delegation as "teams" or "teammates" | 18 |
| Codex manifests with `capabilities` containing `agent-teams-optional` | at least `vanguard`, `smith`, `weaver`, `navigator`, `scribe` |
| Only reader of the 290-line `shared/constitution.md` at runtime | the `mason` auditor |

## 5. Recorded gate verdicts against the verdict schemas

`scripts/handback-conformance.py` validates the 45 persisted verdict files in `~/projects/pages/docs/specs` against `verdict@1` and `verdict@3` using the validator in `tools/validate-handback.py`.

| Shape of the recorded verdict | Conforming | Violating |
| :-- | :-- | :-- |
| `verdict@3`-shaped (has `verified_scope`) | 27 | 8 |
| `verdict@1`-shaped | 6 | 4 |

All 12 violations are the same rule: `verdict_summary` longer than the schema's 300 characters (median length 288, maximum 745, 12 of 45 over the limit). Every other schema rule held, including the conditional ones (a `pass` carries no blockers; a `fail` names at least one).

Two consequences:

- A deterministic check would have asked for a trim on about 27% of recorded gate verdicts, and nothing else. The schema's rules are being followed except the length cap, which prompts alone do not enforce.
- The 45 files mix `scribe` gates (SPEC-002*, 9 files, all `verdict@3`) and `muse` gates (36 files). 26 of the 36 `muse` verdicts (SPEC-001 and SPEC-003*) are `verdict@3`-shaped although `muse` documented `verdict@1`; the other 10 (SPEC-005 to SPEC-012 and two of SPEC-001) are `verdict@1`-shaped. (An earlier version of this note said 35 of 45 were `muse` verdicts; that mixed in the `scribe` files.) The `muse` gate prompt also told the agent to set `verdict` to `"escalate"`, a value neither schema allows. WP-02 moved `muse` to `verdict@3` and made escalation a blocker, as in the other four gates.

Limits: the files were written by an orchestrator from the gate agents' handbacks and may have been edited on the way, so they approximate the handbacks. One project, two sessions.

## 6. Gate rounds, retry counts and tool-output share

`tools/transcript-metrics.py` (the maintained version of `scripts/gate-cost.py`; same plugin and other-agent totals) over the same two projects and the persisted verdict files.

**Blockers per gate round, from the verdict files** (`gates` subcommand):

| Spec | Rounds | Blockers per round | Final persisted verdict |
| :-- | :-- | :-- | :-- |
| SPEC-001 | 13 | 18, 5, 6, 0, 0, 2, 0, 6, 2, 3, 2, 8, 3 | fail |
| SPEC-003a | 7 | 5, 2, 0, 2, 4, 1, 0 | pass |
| SPEC-003c | 4 | 3, 3, 1, 0 | pass |
| SPEC-002b (scribe) | 4 | 6, 4, 1, 1 | fail, one escalation blocker |
| SPEC-005 to SPEC-012 | 1 persisted each | 0 | pass, with `retry_count` 4, 5, 6, 6, 6, 8, 9 and 6 |

- **Gates were not monotonic.** SPEC-001 reached 0 blockers in rounds 4, 5 and 7 and then had 6, 2, 3, 2, 8 and 3 again; SPEC-003a went 0, then 2, then 4. Blockers return after a clean round, which is the pattern WP-212 (non-monotonicity detection) and WP-50 (gate hygiene) target.
- **Every one of the eight later specs passed with a recorded `retry_count` above the cap of 3** (4 to 9). The cap was not enforced.
- **Five specs' last persisted verdict is `fail`** (SPEC-001, SPEC-002, SPEC-002b, SPEC-002c, SPEC-003). Later rounds may not have been persisted, so this is a lower bound on how often work proceeded without a persisted pass, not a count.

**Tool-result characters by tool** (`outputs` subcommand, top-level sessions only): Bash was 77.5% of tool-result characters in the `pages` session (5.28M of 6.82M) and 51.9% in the `orin-dx` session. A compressor that sees only Bash output and removes 70% of it therefore bounds its saving at about 54% and 36% of tool-result characters in those sessions. This is a ceiling on fresh tool-result text, not on the bill: cached re-reads dominate cost, and the JetBrains replay of SkillsBench transcripts found only about 20% of tool output compressible. Your workflow, with Playwright scripts, builds and long Bash output, differs from that benchmark, which is why WP-68 (a paired test of `rtk` on this workflow) is worth keeping.

**Skills versus agents** (`skills` subcommand): 7 Skill calls across the 812 transcripts, none of them a plugin skill other than `muse:component` once; see `../investigations/unused-agents.md`.

## 7. Installed plugins and the `shared` symlink

Each plugin has a `shared -> ../../shared` symlink that its skills and agents use to read schemas and references. Whether it survives installation was open (WP-621). Tested on 2026-10-20 with Claude Code 2.1.292, each case in a fresh isolated config directory (`CLAUDE_CONFIG_DIR`) so nothing touched the real configuration.

| Case | Marketplace source type | Result in the installed copy |
| :-- | :-- | :-- |
| A. Local marketplace, plugin `muse` | relative path (`./plugins/muse`) | `shared` is a real directory with the schemas inside: the installer dereferenced the symlink |
| B. This repository's marketplace as it was, installed from the GitHub `main` branch | `git-subdir` (`path: plugins/muse`) | `shared` is a **dangling symlink** to `../../shared`; `shared/schemas` is missing |
| C. This repository's marketplace after changing every entry to a relative path, all 10 plugins | relative path | `shared` is a real directory in every plugin with all 33 schemas |

The primary documentation agrees: a symlink whose target is elsewhere in the same marketplace is dereferenced into the cache, `git-subdir` fetches "one subdirectory of a git repository, with a sparse checkout", and a relative path is the type to use "for a plugin in a subdirectory of the marketplace repository itself". So installing any plugin from this repository's marketplace gave it no schemas and no shared references. The Claude marketplace entries now use relative paths, and `tests/test_claude_marketplace_sources.py` fails on the old configuration (10 failures) and passes on the new one.

Limits: case C added the marketplace from a local directory, not from GitHub (the docs say a GitHub-added marketplace also has the files, so relative paths resolve). The change reaches users only after it is merged to the branch the marketplace tracks and they update. The Codex bundle already materializes `shared` as regular files (no symlinks); Antigravity install behavior was not tested.
