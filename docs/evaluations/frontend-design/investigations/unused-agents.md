# Why were smith:recon/reviewer/mutator/exit-gate, scribe:verifier/arch-auditor and sentinel:* never used? (WP-56)

## Question

In the orin-dx and pages sessions, `muse:drafter/auditor/exit-gate`, `smith:implementer`, `navigator:*` and `scribe:drafter/exit-gate` ran many times. `smith:recon`, `smith:reviewer`, `smith:mutator`, `smith:exit-gate`, `scribe:verifier`, `scribe:arch-auditor` and every `sentinel:*` agent never ran. Why?

Hypothesis tested first: the orchestrating assistant called plugin AGENTS directly and never invoked plugin SKILLS, so the skill pipelines that spawn the other agents never ran.

## Method

- Transcripts: `~/.claude/projects/-Users-gabe-Projects-orin-dx/b8d16e96-....jsonl` (36,217 lines, 29 Sep to 3 Oct) and `~/.claude/projects/-Users-gabe-Projects-pages/24655582-....jsonl` (63,262 lines, 8 to 16 Oct). Line numbers below are 1-based transcript lines. Streamed with `python3 -I` scripts; no file was read whole.
- Listed every `Skill` tool_use, every `<command-name>` slash command, and every `Agent` tool_use by `subagent_type` in both sessions. Counted Skill calls across all 812 transcripts of the orin-dx and pages project dirs (`rows.json`).
- Read the `skill_listing` and `agent_listing_delta` attachments at session start, the user prompts asking for plugins, and the assistant's next actions.
- Compared against `plugins/smith/skills/implement/SKILL.md`, `plugins/sentinel/skills/gate/SKILL.md`, `plugins/scribe/skills/*/SKILL.md`, and the existing digests (`B-orin-dx-sessions.md`, `C-pages-sessions.md`, `D-outcomes.md` in the job tmp dir).
- Limit: the assistant's thinking blocks are empty in the transcripts, so its reasons are inferred from visible text and actions, not read.

## Findings

| # | Finding | Count | Refs |
|---|---|---|---|
| 1 | `Skill` calls, orin-dx session | 0 | whole file |
| 2 | `Skill` calls, pages session | 4: `artifact-design`, `muse:component`, `artifact-capabilities`, `workflow-authoring`. One plugin skill. | pages 3354, 11906, 14968, 21679 |
| 3 | Slash commands | orin: `/effort /fork /exit /model /login`; pages: `/remote-control`. No plugin command. | orin 8, 18920, 20533 |
| 4 | Plugin skill calls across all 812 transcripts in both projects | 7 `Skill` calls in 4 files. Plugin ones: `muse:component` (1), `scribe:gate-spec` (1, inside one subagent file), `vanguard:research` (1, a blog session). `smith:implement`, `navigator:plan`, `sentinel:gate`, `scribe:draft-spec`, `scribe:verify-spec` are never invoked. | rows.json |
| 5 | Skills were available | Yes. Listings of 60 and 61 skills at session start include `muse:component`, `navigator:plan`, `smith:implement`, `sentinel:gate` and all scribe skills. Not truncated. | orin 18, pages 16 |
| 6 | Agents were also listed, each described "Delegate to this subagent when...", including `smith:reviewer`, `smith:mutator`, `sentinel:*` | Direct delegation was always a legal and visible path. | orin 16, pages 14 |
| 7 | Agent calls, orin-dx | `muse:exit-gate` 28, `fork` 26, `muse:drafter` 25, `general-purpose` 18, `smith:implementer` 17, `scribe:exit-gate` 10, `scribe:drafter` 7, `navigator:planner` 3, `navigator:challenger` 3, `muse:auditor` 1 | scan |
| 8 | Agent calls, pages | `muse:exit-gate` 51, untyped fork/teammate 41, `general-purpose` 24, `smith:implementer` 18, `fork` 14, `muse:auditor` 9, `muse:drafter` 8, `scribe:drafter` 3, `scribe:auditor` 3, `navigator:planner` 1, `navigator:challenger` 1 | scan |
| 9 | Trigger prompt, orin 20776 (30 Sep): "Not DocNav then... Do we make these proper react components? Use our plugins for quality work" | Next: Bash `ls`/`cat README.md` in `~/Projects/agent-plugins` (20789-20791), then "build SiteNav using the Muse->Navigator->Smith pipeline" and `Agent muse:drafter` (20797-20798). No `Skill` call. | orin 20776-20798 |
| 10 | The assistant framed plugins as agent personas | "Muse specs..., Navigator plans..., and Smith builds it" (20942). Pages: "After that, Navigator plans, Smith builds with tests, and Sentinel gates" (14940). Sentinel was promised and never ran. | orin 20942, pages 14940 |
| 11 | No explanation for skipping skills | No assistant text in either session mentions skipping a skill, `reviewer`, `mutator` or `sentinel`. | text search of both sessions |
| 12 | When the skill was loaded, the whole pipeline ran | Pages 11905: "I'm loading the component skill so I follow its exact pipeline." Then 8 drafts, 9 audits, 51 gate calls. No unused muse agent in pages. | pages 11905-14898 |
| 13 | Smith steps in some other form | Reviewer/recon/exit-gate equivalents: none (no Agent call is described as review, verify or gate of implementation). Mutation: partly inline, since implementers report "temporary mutations, restored" and discrimination checks. Verification otherwise relied on `just check`, Playwright e2e and the orchestrator's own checks. | orin 28037, 28057, 28074, 28098, 28305; pages 21361 |

### Why exactly these agents

| Unused agent | Where the plugin puts it | What happened |
|---|---|---|
| `smith:recon`, `reviewer`, `mutator`, `exit-gate` | Only inside `smith:implement` (recon, implementer, mutator, reviewer, exit-gate). | Skill never invoked; `implementer` called alone per task (35 times). |
| `sentinel:recon/verifier/exit-gate` | Only inside `sentinel:gate`. | Skill never invoked; no other path leads there. |
| `scribe:verifier` | Separate skill `scribe:verify-spec`, a distinct step between `draft-spec` and `audit-spec`. | Assistant called `scribe:drafter` then `scribe:exit-gate` directly (orin 26597, 26723). |
| `scribe:arch-auditor` | Separate skill `scribe:audit-architecture`. | Same skip. |
| Used: `muse:*` | All three agents in one skill, `muse:component`. | Skill loaded in pages. In orin the agents were called directly, and `muse:auditor` ran only once. |
| Used: `navigator:*`, `scribe:drafter/exit-gate`, `smith:implementer` | Self-contained "do one thing" agents whose descriptions read as direct delegation targets. | Called directly as personas. |

The unused agents are those reachable only through a skill that was never invoked, or through a skipped step of the scribe chain. The used agents are those an orchestrator can pick from the agent list without a skill.

## Verdict on the hypothesis: PARTLY CONFIRMED (mostly confirmed)

Confirmed:
- Orin has 0 `Skill` calls in 36k lines. Pages has 1 plugin skill call in 63k lines. The pipelines were hand-composed from agents.
- The never-used agents are exactly those gated behind the uninvoked skills (`smith:implement`, `sentinel:gate`) or behind skipped steps of the scribe chain.
- The one plugin skill that was loaded (`muse:component`) ran its full pipeline.

Qualified:
- "Skills unavailable" is refuted: they were listed in both sessions.
- Skipping skills is not the whole cause. `muse:*` also ran directly in orin. The shared cause is that the assistant treated plugins as a cast of agents (Muse, Navigator, Smith, Sentinel) and sequenced them itself, a habit the agent descriptions invite.
- Whether cost or stalls drove the omission of reviewer/mutator is not shown. The digests record 17 failed agent tasks and many "stalled" streams, and a repo-wide pre-commit gate that "cost me about a dozen waits" (pages 21361), but no assistant text links these to skipping. Treat as unknown.
- Later, the user directed less ceremony (pages 49946, 14 Oct: "lean less on the specs and tests"). That explains the dropped gates after 14 Oct, not the earlier skipped Smith steps.

## Impact (only where evidence supports it)

- No implementation review, independent exit-gate verdict or baseline recon ever ran on `smith:implementer` output. Verdicts came from the implementers themselves and the orchestrator.
- Defects were found after the fact by human-directed review or late e2e rather than by a plugin gate (D-outcomes.md items 1, 2, 7, 8):
  - Orin 3 Oct review (36196): "the tests assert markup, so all 29 twx tests pass with every defect below present". This is the weakness `smith:mutator` survivor analysis targets. Caveat: the code reviewed was Codex's, not `smith:implementer`'s, so it shows the pattern, not a Smith miss.
  - SiteNav logo-cap regression (AC-112, AC-017) was caught only by a manual `just e2e` run (orin 36113-36143); Playwright is `runInCI: false`.
  - Pages: spec/code drift at the 760px boundary, where 296 nav-fixture tests pinned the wrong constant (D-outcomes item 2); contrast and target-size defects found by the first automated suite four days after base specs passed (item 7); e2e work surfaced 6 product defects and two were "fixed as spec exemptions" by changing the spec (C-pages-sessions, pages ~21276).
- Not supported: that `smith:reviewer`, `mutator` or `exit-gate` would have caught these. The evidence shows a verification gap those agents are designed for (test discrimination, sibling and family search, current-state check), not a demonstrated catch.
- The spec side also skipped `verify-spec` and `audit-architecture`. Drift between SPEC-001/003a/003c and shipped code (D-outcomes item 1) is what `audit-architecture` and `spec-drift` target; again plausible, not shown. The drafting gates that did run produced many real blockers (118 across re-gates, pages 22772), so spec quality was not neglected overall.

## Recommendations

1. Make skills the entry point. State in the harness instructions and each plugin README: "For plugin work, call the plugin's Skill; call its agents directly only when the skill says so." The skills already hold order, retry limits and routing that the orchestrator re-derived by hand.
2. Rewrite agent descriptions that read "Delegate to this subagent when..." to mark skill-internal steps: "Step N of `smith:implement`; do not call alone". Prioritize `smith:implementer`, `navigator:*`, `scribe:drafter/exit-gate`, the agents actually called directly. Hide internal agents from the model-visible agent list if the harness allows.
3. Fold the scribe chain (draft, verify, audit, architecture, gate) into one pipeline skill with optional steps marked, like `muse:component` and `sentinel:gate`. Today `verifier` and `arch-auditor` sit behind separate skills that nothing triggers.
4. Add a router skill mapping intent to pipeline: component spec -> `muse:component`; plan -> `navigator:plan`; implement -> `smith:implement`; "use our plugins" / "quality work" -> the lifecycle in order, ending at `sentinel:gate`. The prompt at orin 20776 matched no skill trigger phrase.
5. In `smith:implement`, forbid calling `smith:implementer` alone. If cost or stalls are the real barrier, define an explicit light mode (recon and exit-gate only) instead of letting steps drop silently.
6. Make skipping visible: the pipeline's final artifact should list which gates ran and which were skipped, so "Sentinel gates" cannot be promised (pages 14940) and then silently dropped.
7. Add a `mason:evaluate` check for the pattern: a smith agent call with no `smith:implement` Skill call, or a spec exit-gate with no preceding verify/audit.
8. Log plugin skill and agent use per session (the `rows.json` scan is enough) so non-use is observable without manual investigation.
