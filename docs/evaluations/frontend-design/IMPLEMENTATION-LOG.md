# Wave 0 implementation log

Status as of 2026-10-20 on branch `worktree-frontend-design-evaluation`. Five of the Wave 0 work packages in `CATALOG.md` are started or done. Nothing is released: no plugin version, changelog or tag changed (see "Release bookkeeping").

| WP | Status | What changed | Verified by |
| :-- | :-- | :-- | :-- |
| WP-617 Codex model ids | Done | `harnesses/codex/agent-roles/README.md` names `gpt-6-luna`, `gpt-6.1-sol` and `gpt-6-astra` (the selectable models on the Codex models page, 2026-10-20), notes that effort labels are relative and the tiers are unevaluated; generated `dist/codex` copies regenerated | `just marketplace-check`; no `gpt-5.6` or `terra` left in `dist`, `harnesses` or `.agents` |
| WP-620 Claude manifests | Done | `tools/sync-claude-manifests.py` generates `plugins/<id>/.claude-plugin/plugin.json` (name, version, description, author) from each `plugin.json`, with `--check`; `just claude-manifests` is in `just check` and CI; `just claude-validate` runs `claude plugin validate --strict` on every plugin and the marketplace | `just claude-validate`: 10 plugins and the marketplace pass `--strict`, and validation now reads each manifest (before, the directory form checked nothing) |
| WP-622 AGY and root marketplace | Partly done | Removed the dead `$schema` URL (404) from the root `marketplace.json`; nothing in tests, scripts or CI read it | `just check` |
| WP-624 Hook validator spike | Done, registered | `shared/hooks/validate-handback.py`, a `PreToolUse` hook on `SubagentHandback` that checks exit-gate handbacks against their verdict schema, denies with the errors, caps denials at 3 per agent, enforces the retry cap in the report, and fails open; registered by `hooks/hooks.json` in muse, scribe, smith, sentinel and ranger (ADR 012) | `tests/test_handback_validator.py` (13 tests) and a live run and `verification/scripts/handback-conformance.py` over 45 recorded verdicts |
| WP-01 and WP-02 `muse` fixes | Done | The `muse` docs no longer point to a ranger accessibility taxonomy that does not exist (`plugin.json`, README, `SKILL.md`, root `marketplace.json`); the `muse` exit-gate produces `verdict@3` (agent, skill, README, `plugin.json`, Codex skill and catalog, root README table); `verdict@1` has no producer and is kept unchanged | `just check` (66 tests); `just marketplace-check`; validator tests for `muse` routing and for escalation as a blocker |
| WP-625 Reasoning-wording lint | Done | `tests/test_reasoning_wording.py` fails on text that demands reproduced reasoning (verbatim, step-by-step, chain of thought), with one documented exception for the immutable `requirement@1` schema | Passes; fails when the probe's demand is planted in an agent file |

## What the work found

- **`claude plugin validate plugins/<id>` was a false pass** because the manifests sit at the plugin root. With the generated `.claude-plugin/plugin.json` it validates the manifest, and the repo-only keys (`id`, `consumes`, `produces`) stay in `plugin.json` where Claude Code ignores them.
- **Recorded gate verdicts nearly all conform to their schemas.** 33 of 45 conform; all 12 violations are `verdict_summary` over 300 characters (`VERIFY-3.md` section 5). A hook would have asked for one trim on about 27% of handbacks.
- **`muse` gates mostly emitted `verdict@3`-shaped output** (26 of 36; the other 9 of the 45 files are `scribe` gates) while `muse` documented `verdict@1`, and its prompt told the agent to set `verdict` to `"escalate"`, which no schema allows. WP-02 (done) moved `muse` to `verdict@3` and made escalation an `escalation_required` blocker, as in the other four gates; the validator now checks `muse` against `verdict@3` only.
- **A bug in the validator was found only by real data:** a schema property with a list of types (`["string", "null"]`). It is fixed and has a regression test.
- **The `requirement@1` schema describes `reasoning` as "chain-of-thought during capture".** It is immutable (ADR 004), agents reach it through a file read and not a prompt, so the lint carries a documented exception; a future `requirement@2` should use the "private scratchpad" wording.

## Open items from this work

- The README documents AGY installs through the community `agy-plugins-cli`. Fetched source snippets suggest that tool discovers plugins as top-level repository directories, which would not find plugins under `plugins/`. This is unverified; test an install in an isolated environment before changing the README (WP-622, WP-621).
- The installed plugins use `shared -> ../../shared` symlinks and the Claude marketplace installs from the `plugins/<id>` subdirectory (`git-subdir`). Whether the symlink resolves after install is untested (WP-621).
- The hook is a spike: it needs a plugin `hooks/hooks.json` registration, a decision on how it is distributed (the tool lives outside any plugin directory), and a check against a live gate agent in auto mode before WP-602 builds on it.
- Hook behavior on Claude Code 2.1.292: `onFailure: "block"` needs 2.1.295, so a crashing hook does not block (the validator fails open by design).

## Change record (shared/harness-authoring.md)

```text
Classification: Codex workflow (role-card resource), distribution (generated bundle), shared identity (Claude manifest generation, root marketplace)
Counterpart reviewed: plugins/*/plugin.json, .claude-plugin/marketplace.json, harnesses/codex/agent-roles/README.md, shared/harness-authoring.md, docs/codex-marketplace-release-policy.md
Intent preserved: role boundaries and the delegation packet are unchanged; only model ids and a freshness note changed. Plugin identity (id, version, author, consumes, produces) is unchanged and still authoritative in plugins/<id>/plugin.json.
Intentional divergence: Claude Code reads .claude-plugin/plugin.json, so a generated minimal manifest sits beside the repo manifest; Codex tiers were re-chosen by position (luna, sol, astra) and are explicitly unevaluated.
Codex role impact: model ids in all ten materialized agent-roles/README.md files; no skill changes.
Verification: just check; just claude-validate; python3 -m unittest discover -s tests; scripts under docs/evaluations/frontend-design/verification/scripts
```

## Release bookkeeping not done

The repo's contribution checklist asks for a plugin version bump, a plugin changelog entry and a matching marketplace entry when a plugin's behavior changes, and the version check compares all of them. These changes touch every plugin's packaged files (the Codex role README, a new Claude manifest), so a release would bump all ten plugins and the ecosystem version together. That is a release decision, so no version, changelog or tag was changed. Until then `just versions` passes because nothing it compares moved, and the generated Claude manifests copy whatever version `plugin.json` has.

## Second pass (Wave 0 completion)

| WP | Status | What exists | Not yet done |
| :-- | :-- | :-- | :-- |
| WP-03, WP-91, WP-515, WP-516 transcript metrics | Done | `tools/transcript-metrics.py` (`agents`, `skills`, `gates`, `outputs`) with `tests/test_transcript_metrics.py`; results in `verification/VERIFY-3.md` sections 3 to 6 | Per-spec time to first visual and post-gate defect counts need a labelled corpus, not a script |
| WP-04, WP-508, WP-615 platform and cross-reference checks | Done for these checks | `scripts/check-platform-limits.py` in `just check` and CI: cross-references, skill metadata, agent description budget (now about 6.8k of 15k tokens), Codex description budget; `tests/test_platform_limits.py` | Authoring-conformance checks beyond these (for example frontmatter key policy for `role` and `version`, which Claude Code ignores) |
| WP-05 repo claims | Done | The README and `ARCHITECTURE.md` counts (ten plugins, 44 agents, 30 skills, 31 schemas) were checked and are accurate | none |
| WP-56 unused agents | Done | `investigations/unused-agents.md`: the skills were never invoked, so agents reachable only through them never ran | Acting on it is Wave 1 (skills as the entry point, a router) |
| WP-60, WP-514, WP-422 evaluation method | Done as tooling and method | `tools/paired-analysis.py` (paired medians, exact tests, Cohen's kappa) with `tests/test_paired_analysis.py`; `docs/evaluation-methodology.md` | Wiring into `mason:evaluate` and its runner (a plugin change) |
| WP-517, WP-601 native plugin eval | Assessed | `investigations/plugin-eval-assessment.md` with a first eight-case suite design | The suite is not committed or run: cost is unverified ($6 to $16 per full run is an estimate), and the eval copy may not resolve the `shared` symlink |
| WP-609 assumptions register | Done | `docs/architecture-assumptions.md` | Reviews on each model generation |
| WP-626, WP-401 facts and evidence quality | Done as documents | `docs/verified-facts.md`, `docs/evidence-quality.md` | Runtime wiring into `vanguard` (a plugin change) |
| WP-510 Codex TOML policy | Done | `shared/harness-authoring.md` now states that Codex custom agents are TOML, that role cards cannot enforce read-only, and that Codex delegates only when told; the optional generator stays an open decision (proposed record N8) | The decision itself |
| WP-61, WP-518, WP-616 | Done | Probe and scan (`VERIFY-3`); hook questions answered by the Claude Code and Codex reads | Probe on Opus 5.5, Fable 5.1 and Haiku 5.5 |
| WP-90 | Mostly done | Six primary-source verification reads and the register's "not verified" list | The listed unverified items |

Still open in Wave 0: WP-109 (defect-corpus fixtures for `mason:evaluate`), WP-440 (instruction-file linter), the `mason:evaluate` integration of the new analysis tool, the committed plugin-eval suite, and the isolated install test for WP-621 and WP-622.

## Wave 1: exploration modes

Decision record: `docs/adr/011-exploration-modes.md` (written as Accepted by the author on this branch; it needs the reviewer's confirmation in the pull request). Pilots: `investigations/exploration-pilots.md`.

| WP | Status | What exists | Not yet done |
| :-- | :-- | :-- | :-- |
| WP-10 exploratory-mode decision | Done | ADR 011 and its index row | Review |
| WP-18 mode router | Done as a reference | `shared/references/architecture/modes.md` (modes, rules, moving between them, one line for a repository's `AGENTS.md`), loaded by the three skills | A router skill; consumer-repo adoption |
| WP-11 `sketch` | Done | `muse/sketch` skill, `muse/explorer` agent (sonnet, medium), `option-set@1`, Codex counterpart; piloted | Evaluation against ad hoc exploration |
| WP-14a promote (lightweight) | Done | `muse/promote` skill producing a `requirement@1`, Codex counterpart; piloted | The full `spec@2` version (Wave 3) |
| WP-15 `spike` | Done | `smith/spike` skill, `spike-report@1`, Codex counterpart; piloted | Evaluation |
| WP-211 show-first | Done inside `sketch` | Render, then show, then describe; honest "not rendered" fallback; mode and skipped-gates lines | A deterministic render check |
| WP-12 rendering medium | Partly | Static pages plus a `board.html`, browser capability used when present, fallback when not | Capability detection per harness; a tested board generator |
| WP-13 decision log | Partly | Append-only `decisions` inside the sketch, with reasons | Cross-session retrieval and rule promotion; a place in consumer repos beyond `docs/sketches/` |
| WP-16 direction commit | Partly | Four directions offered at the first round | Anti-slop controls (ban lists, named clusters, a scanner) |
| WP-305, WP-306 divergence and re-anchoring | Partly | Re-anchor after about four revisions; the explorer's judgment section rejects variation-only options | An automated divergence check |
| WP-512 write guard | Not done as a guard | Scratch-only writes are an instruction | A deterministic hook (needs the hook work in WP-602) |
| WP-19, WP-20, WP-21, WP-309 | Not started | | |

Also added: `tests/test_exploration_schemas.py` (the two new schemas, with the failure cases each rule exists for), `tests/test_agent_structure.py` (the five-part agent structure, the byte-identical constitution and tiers, for all 45 agents), `pattern` support in the validator tool, and README updates for `muse`, `smith` and the root schema table.

Counts after Wave 1: 10 plugins, 33 skills, 45 agents, 33 schemas; `just check` runs 103 tests.

## Install check (WP-621, Claude Code)

| Finding | Action | Evidence |
| :-- | :-- | :-- |
| Installed from the marketplace's sparse-checkout sources, every plugin got a dangling `shared` symlink and no schemas or shared references | All ten `.claude-plugin/marketplace.json` entries now use relative-path sources (`./plugins/<id>`); `tests/test_claude_marketplace_sources.py` guards it; `tests/test_brand_identity.py` now accepts relative sources while still requiring the publisher repository and the `orin-dx/wisp-plugins` install line | `verification/VERIFY-3.md` section 7: before and after installs of all ten plugins in isolated configs, and the red-to-green test run |

This explains why a pilot run could not read `option-set@1.json`, and it means the schema-file reads that every skill relies on could not have worked for a marketplace install. Sessions in the two projects may have run plugins from a local checkout, where the symlink resolves. Still open: Antigravity and Codex install behavior, and a GitHub-sourced install after merge.

## Hook enforcement (WP-602, WP-624)

| Finding | Action | Evidence |
| :-- | :-- | :-- |
| The validator spike lived in `tools/`, outside every plugin directory, so an installed plugin could not run it | Moved to `shared/hooks/validate-handback.py`, which reaches each plugin through the `shared` symlink and finds the schemas beside it | `tests/test_handback_validator.py`, `tests/test_exploration_schemas.py` |
| The retry cap of 3 was a prompt instruction; eight specs passed with `retry_count` 4 to 9 | A report with `retry_count` above 3 is denied unless it is a `fail` with an `escalation_required` blocker | `test_a_retry_past_the_cap_must_escalate_instead_of_passing` |
| The hook had not run against a real gate agent | Registered in five plugins; ran `muse:exit-gate` through `claude -p --permission-mode auto`: `agent_type` arrives as `muse:exit-gate`, the report is `tool_input.message`, and the trace shows denied, denied, accepted as the agent corrected its output | `WISP_HANDBACK_TRACE` output of that run (one run, one gate, one model) |

ADR 012 records the decision. Not done: Codex and Antigravity enforcement, and live runs of scribe, smith, sentinel and ranger (same routing, not run). A test now requires every exit-gate agent to have a route and its plugin to register the hook.

## Context composition (new)

| Finding | Action | Evidence |
| :-- | :-- | :-- |
| No view of what fills the context window; the earlier measure covered tool results only | Added `context` to `tools/transcript-metrics.py` (characters by origin, tool-result and tool-call shares, largest results) with a test | `verification/VERIFY-4.md`: Bash is about 60% of all characters (output and command text together); the largest single results are whole-page `Artifact` reads of 50k characters; delegation is 3% |

| Skills had no rule for command output, inline scripts or whole-page reads | Added `shared/references/tooling/context.md` and routed it from `smith/implement`, `smith/spike`, `smith/implementer` and the Codex counterparts | `just check`; effect on context is unmeasured |

Not done: the same rule for `ranger`, `sentinel`, `muse` and `scribe` skills (smith first, to measure before spreading); porting the description cuts from the review-slop branch; moving the exploration record shapes out of the skill bodies (needs a re-pilot).

## Courier changeset guidance (Callisto request)

| Finding | Action | Evidence |
| :--- | :--- | :--- |
| `changeset@2` capped the summary at 200 characters and the agent, skill and schema repeated one-clause and one-sentence limits, so a limit users will hit went into the unforwarded `reasoning` | New `changeset@3` (no cap, Markdown, `disposition` of new, update-existing or none) and `release-artifact@3`; `changeset@2` and `release-artifact@2` are untouched per ADR 004 | `tests/test_changeset_schema.py` |
| The agent worked per diff topic, with no way to update an entry or say none is needed | Outcome-level granularity and `disposition` in the agent, skills and Codex counterparts | Live run below |
| The Semver table had no rows for a CLI's flags, output, exit codes or serialized files | Rows added to `shared/references/delivery/changesets.md`, with an entry-shape section and a bad-versus-good pair (117 lines of the 120 cap) | `just check` |
| Claude sessions wrote changesets, commits and PR text freehand | The `changeset`, `commit` and `pr` skill descriptions now say to use the skill instead, and the courier README says when to use each; no hook | Tests on the descriptions |
| Courier moved to 3.1.0 with changelog | `plugin.json`, README, CHANGELOG, marketplace and Codex manifest agree | `just versions` |

Live run: `courier:changeset-analyzer` on `gh pr diff 483 --repo orin-dx/callisto` (24.9 kB), one run on Sonnet 5.5. It returned one `new` entry for one outcome: a lead line on the link, then what you see and where, the limit that a changeset pushed straight to the branch gets no link, the optional `pr` field for scripts, and that upgrading needs no action. It classified the change as a minor new capability. It did not write the "why it helps" as a separate bullet but put it in the lead line.

**Finding: `shared/...` reference paths depend on the working directory.** In that run the agent reported it could not find `shared/references/delivery/changesets.md` and fell back to the schema-implied rules. The agent was started from a directory outside the plugin, and its `load_first` paths are relative to the plugin root, not to where the agent runs. This is separate from, and in addition to, the dangling-symlink install defect fixed in the marketplace sources (VERIFY-3 section 7): even a correct install leaves a relative `shared/...` path unresolvable from a user's project. It likely explains the pilots where schema files were not readable at run time. Not fixed here. Options: pass the plugin root into the skill and agent instructions if the host substitutes it, name the references in the skill body so they load with it, or inline the few rules an agent cannot work without. Needs a host check first.

`pr-narrator` and `commit-analyzer` were then changed to match: they follow the repository's own conventions (a pull request template, recent commit scopes and subject style), keep limits in the body instead of the scratchpad, mark breaking changes to command output, exit codes and file formats, and the narrator names or recommends a changeset. One live run of both on the same PR 483 diff: the PR body followed the template sections, put four limits under a "Limits a reader will hit" list, said the tests were not run and gave commands, and added a Changeset section. Two weaknesses: the narrator stated an inferred behavior (shallow clones give no link and no error) as fact while its scratchpad called it an inference, which a new rule now forbids; and the haiku commit body described the mechanism and omitted the direct-push limit, which is not fixed (a commit body is short and the limit belongs in the changeset and PR). Both agents again could not find their `shared/` reference, the working-directory finding above.

Not done: changes in the Callisto repo (its AGENTS.md or PR template), which are recommendations only: say in its AGENTS.md to invoke `courier/changeset` for changesets and `courier/pr` for PR text, and add a changeset prompt to its PR template.

## Paired evaluation runbook (track C)

| Finding | Action | Evidence |
| :-- | :-- | :-- |
| Plugin changes were judged from single-run pilots; turns and rework had no measure | Added a `turns` subcommand to `tools/transcript-metrics.py` (human prompts, assistant turns, tool calls, subagent spawns, narrowly defined retries, reported subagent tokens; `--trial` emits a paired-analysis line) | `tests/test_transcript_metrics.py` (`TurnsTests`) |
| No procedure for running the paired design on real work | `docs/evaluation-runbook.md`: three task kinds with control and treatment arms, fixed settings, capture commands, a blinded scoring sheet, minimum pairs and null-result limits, a results table | `DryRunTests` runs the pipeline on synthetic sessions: turns, trials file, `compare`, `agreement` |

Not done: no real paired run yet, so no claim about the plugin changes follows from this. The control arm for spec gating (`50bdcf1b^`) and the pair counts are proposals for the owner to confirm.


## Track D: routing wording and context hygiene (ranger, sentinel, muse, scribe)

| Finding | Action | Evidence |
| :--- | :--- | :--- |
| Skills were invoked 7 times in 812 transcripts; assistants wrote specs, reviews and verdicts freehand | The skill descriptions now lead with the situation and request phrases; "Use this, not a freehand ..." appears only where a freehand alternative exists (`ranger/audit`, `sentinel/gate`, `muse/component`, `scribe/draft-spec`, `audit-spec`, `gate-spec`); read-only diagnostics (`spec-drift`, `audit-architecture`, `verify-spec`, `architect`, `promote`) make no such claim. `muse/sketch` says to use it instead of describing options in prose. Muse `sketch` and `promote` descriptions cut to 450 characters or fewer. Four READMEs gained one "about to do it by hand" line | `tests/test_skill_routing.py` |
| Bash output and scripts were about 60% of context | `shared/references/tooling/context.md` is routed from the ranger, sentinel, muse sketch and scribe audit-architecture and spec-drift skills; from the `<load_first>` of ranger recon, scanner, boundary-tracer and adversary, sentinel recon and verifier, scribe arch-auditor, drift-checker and verifier, and muse explorer; from the Codex counterparts; and in the Codex catalog `runtime_files` | `tests/test_skill_routing.py`, `just check` |

Not done: the descriptions' effect on invocation rate cannot be measured here; it needs a transcript comparison after release. The sketch, promote and spike record shapes stay inline pending the path-resolution investigation. The new `load_first` paths are relative to the plugin root, so they carry the working-directory risk recorded in the courier finding above. Exit-gate agents were left to track B.


## Outcome-level plans (track E, assumption 10, review-slop C4)

| Finding | Action | Evidence |
| :--- | :--- | :--- |
| `planner` wrote exact code for every task that `implementer` may discard and `challenger` policed; `plan@1` does not require code (only `id`, `title`, `files`, `steps`, `commit_message`) | No schema change. `planner` now states outcome, files, signatures, proving tests with assertions, verification command, commit message and `covers_criteria`, with code only for non-obvious or costly-to-reshape logic; `challenger` flags full bodies for routine logic and no longer treats absent code as a defect; Claude and Codex skills and the README updated. ADR 014 supersedes ADR 009's every-task code requirement only | `tests/test_navigator_plan.py`; `just check` |

Measured once each (Sonnet 5.5, a two-task, six-criterion Python fixture with the schema path given in the prompt): the old planner wrote 9,777 characters (8 steps, 18 function definitions); the new one wrote 5,578 (18 steps, 1 definition). Both validated against `plan@1` and covered all six criteria. One run each is weak evidence on one small fixture. Not tested: whether implementers do better or worse from the smaller plans, and the challenger on either shape.

**Finding: without the schema in reach, the planner invents fields.** A first pair of runs started from a directory with no `shared/schemas` and both wrote task keys the schema forbids (`outcome`, `approach`, `tests`, `verify_command`), the same working-directory problem as the courier finding above. The planner now says to add no keys outside the schema and to carry the content in `steps`; the final runs also named the schema path in the prompt.

Not done: the `plan@1` field descriptions still say "exact code" (a published schema is not edited, ADR 004); a `plan@2` with explicit outcome, signature and test fields is deferred.

## Gate rounds (track B, ADR 013)

| Finding | Action | Evidence |
| :-- | :-- | :-- |
| Every spec failed its first gate and blocker counts were non-monotonic (SPEC-001: 18, 5, 6, 0, 0, 2, 0, 6, 2, 3, 2, 8, 3) | Each of the five exit gates now states two output rules, worded the same: round one lists the complete blocker set; a retry cites only unresolved prior blockers or regressions the fix introduced, and any other new issue is a non-blocking `coverage_gaps` entry; every blocker names the criterion, cites quoted text or a location and states the exact change; wording or style issues are notes | `just check` exit 0; `verdict@3` unchanged |
| Drafters sent unchecked drafts to the gate | New `shared/references/verification/gate-readiness.md` (blocker shape, rounds, spec checklist) loaded by `muse:drafter` and `scribe:drafter`, with a short inline fallback if the path does not resolve; Codex `author` and `judge` role cards updated | `just check` |
| Blocker shape could not be enforced deterministically without false denials | The hook denies only a blocker or coverage gap whose text is whitespace; evidence citing is not checked | `tests/test_handback_validator.py` |

Live runs, one run each on Sonnet 5.5 (Claude Code 2.1.311, `claude -p --permission-mode auto --plugin-dir`, working directory outside the repository, `WISP_HANDBACK_TRACE` set). The prompt read a task file asking for one delegation to `<plugin>:exit-gate` with a small spec or finding that had known defects. The trace showed `agent_type` `<plugin>:exit-gate` in all four. Scribe, sentinel and smith were accepted on the first report. Ranger was denied once and accepted on the second; the trace does not record the denial reason, so what the first report broke is unknown. All four returned fail with blockers that gave a criterion or finding id, a location and an exact change; the smith report also listed `missing_mutation_gate` and `unresolved_review` as blockers, and the scribe report flagged the TBD and the vague "gracefully" criterion. These runs were round one only: they confirm the hook fires and the gates produce evidence-citing blockers, not that rounds fall. Nothing here measures the retry rule.

Not done: a measured comparison of round counts before and after (needs a paired run of gate, fix and regate, WP-60); passing the prior round's blockers into the gate on retry (the skills do not, so the retry rule depends on the orchestrator); a self-check for `smith:implementer`, `sentinel:verifier` and `ranger` producers; a check that the `shared/...` path resolves from a user's project (see the Courier finding above).

## Integration, path resolution and versions

| Finding | Action | Evidence |
| :--- | :--- | :--- |
| Relative `shared/...` paths in agents and skills do not resolve reliably: with `shared` a symlink, a probe skill first tried its own directory and a probe agent first tried the working directory, each costing a failed read; an explicit `${CLAUDE_PLUGIN_ROOT}/shared/...` path read on the first try in both | Rewrote 163 references in 66 agent and skill files to the plugin-root form. Codex sources are unchanged because Codex does not substitute the token | Four probe runs (one each, Claude Code 2.1.311, Sonnet 5.5); then `courier:changeset-analyzer` on the Callisto PR 483 diff reported its reference loaded from the full plugin path on the first read |
| The gate retry rule needs `retry_count` and the prior blockers as input; no skill passed them | One sentence in the gate-calling skills (muse `component`, scribe `gate-spec`, sentinel `gate`, smith `implement`, ranger `audit`) and the Codex counterparts | `just check` |
| Tracks B to E (gate hygiene, measurement, skill routing, planner) ran in parallel worktrees and were merged here | Merged with log-only conflicts resolved by keeping both sides | `just check` exit 0 after each merge |
| Nine plugins had changed against `main` with no version or changelog | muse 1.1.0, smith 2.5.0, navigator 2.4.0, scribe 3.5.0, courier 3.1.0; sentinel, ranger, mason, vanguard and weaver patch bumps; ecosystem 4.5.0 | `just versions`, `just check`, `just claude-validate` |

Limits: the path finding rests on single probe runs; Antigravity's handling of `${CLAUDE_PLUGIN_ROOT}` in skill and agent text was not tested, and its format shares the authored tree, so confirm it before releasing. The hook-only plugins (sentinel, ranger) are patch bumps although a gate can now deny a report that used to pass; scribe is a minor because its drafter and skills also changed behavior.

