# MAP-5: traceability of M1, M2, X findings to work packages

Repo cross-check basis (grep/read, 2026-10-17): constitution tier table is haiku/low, sonnet/medium, opus/high, claude-fable-5-1/high (bounded architecture only, never gates); all 44 agents carry `<backstory>`; constitution L242 mandates `reasoning: string` in every schema; ranger scanner already says "emit every match, let adversary evaluate" (aligned); Sentinel Retry Caller Constraint exists (blockers-delta only); retry cap of 3 lives in muse exit-gate description, not as an enforced constitution rule; harness-authoring.md says Codex uses portable markdown role cards in `harnesses/codex/.../agent-roles/` and "No TOML agent file is shipped as a plugin behavior contract"; no repo text mentions Playwright/Storybook/axe; no phraseology/readback vocabulary outside two muse/scribe exit-gate mentions; ADRs 001-010 exist (003 forbids merging enumeration+judgment; 006 byte-identical constitution; 004 immutable schemas).

Legend: P = fetched primary; S = search summary; U = unverified; K = author knowledge; I = inference. Repo status: ALIGNED / CONTRADICTS / SILENT / PARTIAL.

| ID | finding | tag | mapped WP | note |
|---|---|---|---|---|
| M1-01 | Master prompting page lists Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 5, Opus 4.8/4.7/4.6, Sonnet 5.5, Sonnet 5, Sonnet 4.6, Haiku 5.5, Haiku 4.5 | P | WP-63 | Repo tier table names only haiku/sonnet/opus/fable-5-1 without versions. Need concrete model-id pinning policy: see WP-501. |
| M1-02 | Haiku 5.5 is first Haiku with effort levels (default medium); Wisp haiku recon tier should be re-evaluated | P | WP-63 | Repo: silent on Haiku version; recon fixed at haiku/low. Partial: WP-63 names Haiku 5.5 but not the "low skips searches/checks" risk (M1-48). |
| M1-03 | Each model has own prompting page; "treat as measured on that model, re-check against your own evals" | P | WP-60, WP-63 | Repo: constitution has no per-model-generation re-check trigger. WP-501 adds the trigger. |
| M1-04 | Effort levels low/medium/high/xhigh/max; defaults high except Opus 5.5 and Haiku 5.5 = medium; names not comparable across models | P | WP-63 | Repo pins effort per agent but has no sweep/re-pin rule on model change (conflicts with "high" gate default for Opus 5.5, see M1-24). |
| M1-05 | Effort doc: low suits "simpler tasks... such as subagents" | P | WP-63 | ALIGNED with repo (recon low). |
| M1-06 | Thinking always-on/adaptive-only on Fable 5.1, Fable 5, Opus 5.5; Sonnet 5.5 lowest setting `between_tools`; budget_tokens returns 400 on 4.7+; prefill unsupported since 4.6 | P | UNMAPPED -> WP-502 | Repo silent on API-level params; relevant for any direct API/SDK use and Codex `none` analogue. Low priority; record in model-notes reference. |
| M1-07 | Fable 5: older skills "often too prescriptive... can degrade output quality"; consider removing older instructions if default is better | P | WP-64, WP-62 | Repo CONTRADICTS in spirit: 44 agents with constitution+backstory+5-part skeleton. Needs ablation (WP-62) before removal; ADR 001/006 guardrails require new ADR. |
| M1-08 | Fable 5: re-evaluate which instructions, tools, guardrails are still needed | P | WP-62, WP-64 | Same as M1-07. |
| M1-09 | Fable 5: brief instruction can steer most behaviors; no need to enumerate each | P | WP-64 | Repo: constitution is ~290 lines of EARS enumeration. Candidate shrink; ablation first. |
| M1-10 | Master: prefer general instructions over prescriptive steps; "think thoroughly" beats hand-written plan | P | WP-64 | Repo: planner emits "exact implementation code" (ADR 009 allows latitude); tension with navigator:planner prescriptiveness. WP-58 only partly covers; WP-64 should audit planner. |
| M1-11 | Harness blog: every harness component encodes an assumption about what the model cannot do; stress-test them | P | WP-64, WP-62 | SILENT in repo. WP-62 covers by ablation; add an "assumption ledger" per agent -> WP-503. |
| M1-12 | Opus 4.6 required significantly less scaffolding than 4.5 (fetch-tool paraphrase) | S | WP-64 | Paraphrase only; verify (WP-90). |
| M1-13 | Master: dial back "CRITICAL: You MUST" language; models may overtrigger | P | WP-64 | Repo: constitution uses SHALL/NEVER/MUST throughout; skill descriptions use long "Trigger when" lists (overtrigger risk low, but audit). |
| M1-14 | Claude Code: if you emphasize many lines none stands out; bloated CLAUDE.md gets ignored | P | WP-64, WP-71 | AGENTS.md is 5.7K (fine); constitution copied in every agent is the bloat risk. |
| M1-15 | Emphasis is rationed, not banned (Sonnet 5 frontend snippet still uses "NEVER") | P | WP-64 | Informs WP-64 rule: ration, do not zero. |
| M1-16 | Sonnet 5 interprets prompts literally; does not generalize an instruction from one item to another; state scope explicitly | P | UNMAPPED -> WP-504 | Repo silent. Per-item rules in agents ("for X, do Y") may not generalize; audit scope statements. |
| M1-17 | Review prompts "only report high-severity / be conservative" are followed literally and lower recall; report everything, filter in a separate pass | P | WP-50, WP-64 | ALIGNED for ranger scanner (L67); WP-50 covers all scanners. Other plugins' auditors (scribe/muse auditor) untested - audit. |
| M1-18 | Sonnet 5 review sample: report every issue incl. uncertain, with confidence and estimated severity; separate verification step filters | P | WP-50 | Repo candidate@1 schema fields unchecked for confidence+severity; verify. |
| M1-19 | Opus 5.5: effort is main thinking control; start at medium, set explicitly, test several levels | P | WP-63 | Repo CONTRADICTS: gates on opus/high. |
| M1-20 | Opus 5.5 medium matches/exceeds Opus 5 high on coding and knowledge work; on several coding evals low comes close | P | WP-63 | Vendor claim, no numbers verified (M1-F3); verify with own evals. |
| M1-21 | To think less lower effort; prompt instructions to think less are less reliable (Opus 5.5, Sonnet 5.5, Haiku 5.5) | P | WP-64, WP-63 | Repo SILENT. Rule for constitution: use effort frontmatter, not prose. |
| M1-22 | Remove "think carefully" lines (Opus 5.5 chat prompts) | P | WP-64 | Repo ALIGNED: grep finds zero "think carefully/step by step/double-check" in plugin agents. |
| M1-23 | Sonnet 5.5 JSON-only output: keep thinking on, effort >= high, or add "Think the problem through before you answer" (lifts to near xhigh) | P | UNMAPPED -> WP-505 | Relevant: every Wisp agent emits JSON handoffs on sonnet/medium. Test with eval. |
| M1-24 | Lower effort -> fewer tool calls, direct action without preamble | P | WP-63, WP-65 | Informs recon tier and narration. |
| M1-25 | Per-message effort change (beta header mid-conversation-output-config-2026-07-01) preserves cache | P | UNMAPPED -> WP-502 | Beta; optional; record only. |
| M1-26 | Sonnet 5.5 at low can skip verifying a change; low/medium more likely to stop and check in with user | P | WP-63, WP-506 | Implementer on sonnet/medium: repo has independent verification, but producers may report done without real check; see WP-506. |
| M1-27 | Haiku 5.5 at low more likely to skip a search/stop early/skip a check; low->medium roughly halved early stopping | P | WP-63 | Direct risk to haiku/low recon. Add recon-completeness check (compare to ripgrep ground truth). |
| M1-28 | Opus 5 verifies its own work unprompted; explicit verification instructions cause over-verification; same for legacy separate verification steps | P | WP-64 | Repo: smith:implementer/mutator/reviewer instruct verification. Run on sonnet, so partially N/A; audit Opus producers (scribe:architect is fable). Tension with M1-29. |
| M1-29 | Sonnet 5.5/Haiku 5.5 at low/medium report done without real check; supplied paragraph: run a real check, syntax-only does not count, name unrun check | P | UNMAPPED -> WP-506 | Repo constitution has risk-based verification but not this exact "real check" wording; CONTRADICTION with M1-28 across models (see C-1). |
| M1-30 | "Do not use subagents to verify or double-check your own work" sample prompt | P | WP-55 | ALIGNED with draft WP-55 (orchestrator owns spawning). Repo: smith dispatches implementer per batch (constitution L174); check agents do not spawn verifiers. |
| M1-31 | Fable 5: separate fresh-context verifier subagents outperform self-critique | P | WP-50, WP-55 | ALIGNED with repo gates; contradicts M1-30 only superficially (C-2). |
| M1-32 | Fable 5: audit each claim against a tool result from this session before reporting progress; nearly eliminated fabricated status reports | P | UNMAPPED -> WP-506 | Repo: criteria_evidence exists in smith; no constitution rule on claim-to-tool-result audit. |
| M1-33 | Harness blog: separating worker from judge is a strong lever; self-graders praise own work | P | WP-50 | ALIGNED with ADR 003. |
| M1-34 | Claude Code: reviewer prompted to find gaps will report some even when sound; chasing findings over-engineers; flag only gaps affecting correctness or stated requirements | P | WP-50, WP-51 | Explains gate churn seen in X (wording blockers). WP-50 covers "no findings valid pass"; add "correctness/requirement impact required per blocker" explicitly. |
| M1-35 | Claude Code: give Claude a check it can run; deterministic gates via Stop hook or /goal | P | WP-42, WP-512 | Repo partially: `just check`. Hook-based gating not used in plugins -> WP-512. |
| M1-36 | Opus 4.6/5 delegate to subagents more readily; costs multiply on small tasks; sample "delegate only large independent tasks" | P | WP-55 | Repo SILENT on delegation threshold; constitution L174 only batch rule. |
| M1-37 | Fable 5/5.1 dependable parallel subagents; lead continues while subagents run | P | WP-55 | Orchestration option; WP-55 ceiling 3-5. |
| M1-38 | Sonnet 5.5 at xhigh/max can launch reviewer subagents; stopping that cut session cost about a third with no quality change | P | WP-55, WP-91 | Vendor figure; verify on own transcripts (WP-91). |
| M1-39 | Claude Code subagent frontmatter: model (sonnet/opus/haiku/fable), effort, tools, skills, memory, maxTurns; "Use Haiku for Exploration" | P | WP-63, WP-509 | Repo frontmatter uses name/role/model/effort/description only; no `tools`, `maxTurns`, `skills`, `memory`. Partial; WP-509. Verify plugin-agent support (M1-F2). |
| M1-40 | Subagent description should be short; logic in body | P | WP-64 | Repo CONTRADICTS: agent descriptions are very long (see agent list). Check against plugin spec; instruction-economy concern. |
| M1-41 | Depth cap default 3, concurrency 20; env CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH / _MAX_CONCURRENT_SUBAGENTS | P | WP-55, WP-509 | Repo SILENT. |
| M1-42 | XML tags, one-sentence role, 3-5 examples remain recommended and not deprecated | P | WP-62 | ALIGNED partly; repo uses XML (ADR 001). Repo has no `<example>` sections -> potential gap (WP-507). |
| M1-43 | No guidance requires fixed N-part tag skeleton; XML separates content types | P | WP-62 | Inference. ADR 001 fixed skeleton neither required nor forbidden; ablation (WP-62). |
| M1-44 | Fable 5.1: one complete example fixed unmarked quoting. Sonnet 5: positive examples beat negative examples/"don't" instructions | P | WP-64, WP-507 | Repo uses "never-do rules" in `<output>`; positive examples absent. WP-507. |
| M1-45 | Tell Claude what to do, give reason; Claude generalizes from explanation; Fable 5 performs better knowing intent | P | WP-64 | Repo CONTRADICTS: EARS "SHALL NEVER" with little rationale in agent bodies; ADR 002 constrains EARS to `<output>`. Reconcile in WP-64 (explain "never X"). |
| M1-46 | Fable/Opus/Sonnet 5.5 prompts asking model to write out its reasoning may be declined with `reasoning_extraction`; ask for short explanation/summary of actions; server fallback does not retry | P | WP-61 | Repo CONTRADICTS (verified): 29/31 schemas have `reasoning`; constitution L242 mandates it; 44 agents mention it. Highest-priority defect. WP-61 should be promoted to G0. |
| M1-47 | Wisp should rename to `rationale`/`evidence_summary`/`actions_taken`; cap length; never say "show your reasoning" | I | WP-61 | Needs ADR 004 handling: schema @n+1 for 29 schemas (huge); alternative is prompt-only reframing. WP-61 should cost both. |
| M1-48 | Opus 5 longer by default; effort does not shorten visible output; prompt for length; do not pad written deliverables | P | WP-65 | Repo constitution has instruction-economy rules; ALIGNED. |
| M1-49 | Fable 5.1 formats less; remove anti-formatting language | P | WP-64 | Repo SILENT. Low. |
| M1-50 | Sonnet 5.5/Opus 5.5/Fable 5.1 progress text arrives as thinking blocks with empty text unless display "updates"; remove "hold all findings for final response" | P | UNMAPPED -> WP-502 | Affects orchestrators streaming status; record. |
| M1-51 | Fable 5: keep output short by being selective, not compressing into fragments, abbreviations, arrow chains | P | WP-65 | CONTRADICTS caveman style (X-CV) for user-facing prose; WP-65 must exclude telegraphic style (C-5). |
| M1-52 | Sonnet 5.5/Haiku 5.5 autonomy sample: keep working until done; stop to ask only when blocked or risky; do not add unasked features/tests/docs | P | WP-64, WP-505 | Repo ALIGNED w/ smith scope rules; verify in implementer text. |
| M1-53 | Fable 5.1: request sets scope; the scope is the deliverable; do not quietly narrow/widen/swap | P | WP-504 | Matches X-U5 user frustration ("did you lose that decision"). New WP-504. |
| M1-54 | Unattended runs: "Want me to...?" blocks work (Fable 5.1) | P | WP-504 | Repo SILENT; relevant for headless Codex runs. |
| M1-55 | Opus 5.5 unattended: treat text-only end_turn as report; checklist; stop after 2-3 automatic continuations | P | WP-51 | ALIGNED with cap 3, but enforcement missing (WP-51). |
| M1-56 | Confirm destructive/irreversible/externally visible actions remains | P | WP-18 | Repo: courier posts only after confirmation; ALIGNED. |
| M1-57 | Multi-window: first window sets framework (tests.json, init.sh), later iterate; JSON for state, text for progress, git | P | WP-66 | ALIGNED with plan/spec persistence (constitution L120+); add progress-notes file. |
| M1-58 | Prefer fresh context over compaction; models discover state from filesystem | P | WP-66 | Repo ALIGNED (file-path persistence). |
| M1-59 | Fable 5 memory: one lesson per file, one-line summary on top, delete wrong notes | P | WP-13 | Format for decision log/rules; partial; WP-13 should adopt. |
| M1-60 | Claude Code: context is fundamental constraint; subagents for investigation; /clear after 2 corrections | P | WP-66 | Informational. |
| M1-61 | Fable 5.1/Opus 5.5: append-only history; changing system/tools mid-session invalidates thinking blocks/cache | P | WP-66 | Repo ALIGNED (static constitution prefix, constitution L~52). |
| M1-62 | Skills: default assume Claude is smart; add only missing context | P | WP-64 | Informs. |
| M1-63 | Degrees of freedom: low freedom only for fragile/consistency-critical ops | P | WP-64, WP-72 | Informs script-vs-prose choice in WP-42/72. |
| M1-64 | Skill description third person, what+when, <=1024 chars; SKILL.md <500 lines; references one level deep | P | UNMAPPED -> WP-508 | Repo: `just reference-size` exists (check threshold); description length unverified (skill descriptions in listing look long). Add checks. |
| M1-65 | Validation feedback loops; plan-validate-execute with machine-verifiable intermediate files for high-stakes ops | P | WP-30, WP-42 | ALIGNED with schema-first. |
| M1-66 | Eval-driven skill authoring: >=3 evals before extensive docs; test with Haiku, Sonnet, Opus; Claude A/B iteration | P | WP-60, WP-67 | Repo has mason:evaluate; no rule "evals before docs". Add to constitution authoring (WP-508). |
| M1-67 | Gerund skill names suggested; Wisp uses single lifecycle words, acceptable | P | none needed | ALIGNED (AGENTS.md §2). Explicit disposition: no action. |
| M1-68 | Template strictness: "ALWAYS use this exact template" for strict formats | P | WP-64 | Informs emphasis rationing. |
| M1-69 | Frontend: model converges to generic "AI slop"; vary fonts/themes; still converges on Space Grotesk | P | WP-16 | Repo muse SILENT. |
| M1-70 | Opus 5.5: "avoid generic AI look" swaps one default for another; name specific patterns to avoid; iterate by extending list | P | WP-16 | Sample bans: cream bg, italic accent words, numbered 01/02/03 labels, monospace labels, pill buttons; add to WP-16 ban-list seed. |
| M1-71 | Sonnet 5: generic instructions shift to a different fixed palette; specify concrete alternative or propose options first | P | WP-16, WP-11 | Both approaches covered. |
| M1-72 | Sonnet 5: "propose 4 distinct visual directions... user picks, implement only that" | P | WP-16, WP-11 | WP-16 says ~4; WP-11 says ~3 options default. Minor inconsistency (C-8). |
| M1-73 | Frontend blog: four vectors typography, themes, motion, backgrounds; avoid exact hex codes AND vague high-altitude guidance | P | WP-16, WP-31 | Tension with WP-31 token-heavy DESIGN.md (C-9). |
| M1-74 | Harness blog evaluator design criteria: design quality, originality, craft, functionality | P | WP-17 | Add as critic rubric. |
| M1-75 | Claude Design (support article 14604416) is canvas for interactive design iteration; page not fetched | S | WP-12, WP-90 | Unverified. Potential handoff target; WP-511. |
| M1-76 | Haiku 5.5: default medium, thinking on by default, 128k max_tokens; can disable thinking at <=high | P | WP-63 | Record. |
| M1-77 | Sonnet 5.5: default high; agentic coding start medium (well specified) then high; tends to add tests/docs unprompted | P | WP-63 | Repo scanner/implementer sonnet/medium ALIGNED. |
| M1-78 | Opus 5.5: default medium; thinks more per turn than Opus 5 at same level; better code review (more bugs, fewer false alarms) | P | WP-63 | "Fewer false alarms" is vendor claim; verify. |
| M1-79 | Fable 5.1: default high; low often competitive with Opus/Sonnet on cost per task with higher score; strongest long-horizon; longer turns | P | WP-63 | Repo already uses fable-5-1/high for architecture but forbids it on gates; contradicts "test Fable on hardest gate". |
| M1-80 | Keep: scanner/recon recall vs adversary/gate filter split | P | none needed | ALIGNED (ADR 003). |
| M1-81 | Keep: gate in fresh context, no self-grading | P | none needed | ALIGNED. |
| M1-82 | Keep: schema-first JSON handoffs; use structured outputs where available | P | WP-61, WP-70 | Structured outputs adoption not in any WP -> WP-505. |
| M1-83 | Keep: retry caps (Opus "2-3 continuations", Stop-hook cap) | P | WP-51 | Cap exists in text only; enforcement gap = WP-51. |
| M1-84 | Keep: progressive loading, `<load_first>`, refs one level deep (verify no reference chains) | P | WP-04 | Verification of no chain: add to WP-04 link checker. |
| M1-85 | Keep: tier by cognitive mode with lower effort for subagents | P | WP-63 | ALIGNED. |
| M1-86 | Keep: abstract tool language, one rule per item, no time-sensitive info | P | none needed | ALIGNED. Note: constitution tier table names model versions (time-sensitive) - mild tension. |
| M1-87 | Keep: default-fail gate with concrete criteria (Sonnet 5 concrete bar) | P | none needed | ALIGNED but see churn warning M1-34. |
| M1-88 | Probably unnecessary: byte-identical `<constitution>` in every agent is token cost; shrink to ~10 lines or load only at gates; enforce via validators/hooks | I | WP-62 | ADR 006 guardrail; needs new ADR to change. Cache-sharing benefit (constitution "Static Prefix") counters; ablation must measure cost net of cache hits (C-3). |
| M1-89 | Probably unnecessary: `<backstory>` persona prose; one sentence suffices | I | WP-62 | ADR 001/007; ablation. |
| M1-90 | Remove self-verify/double-check steps in Opus producers; keep independent gates | P | WP-64 | Repo: no Opus producers except gates; N/A mostly. |
| M1-91 | Replace "think step by step" with effort | P | WP-64 | Repo ALIGNED (0 matches). |
| M1-92 | Reduce repeated MUST/ALWAYS to 1-2 hard invariants | P | WP-64 | Repo CONTRADICTS (see M1-13). |
| M1-93 | Rigid 5-part structure for haiku recon may be overkill; goal + schema may suffice; test | I | WP-62 | Candidate ablation arm. |
| M1-94 | Harmful: `reasoning` fields | P | WP-61 | Same as M1-46. |
| M1-95 | Harmful: qualitative filtering in scanners | P | WP-50 | Same as M1-17. |
| M1-96 | EARS "never X" without rationale generalizes worse; EARS in output contracts fine | P | WP-64 | ADR 002 aligned for output contracts. |
| M1-97 | Harmful: gate-chaining that spawns reviewer subagents; harness owns spawning; "work directly unless X"; set depth/concurrency caps | P | WP-55 | Check agents' text for spawn instructions. |
| M1-98 | Harmful: reviewer-finds-something bias -> manufactured blockers looping to retry cap; require falsifiable evidence and correctness impact; "no findings" first-class pass | P | WP-50 | Same as M1-34. |
| M1-99 | Harmful: prompt tuned on one model tested on none of the others; pin effort per agent, re-sweep per generation | P | WP-63, WP-501 | |
| M1-100 | Harmful: mutating prompt/tool list between turns breaks cache; keep prompts static per agent | P | WP-66 | Repo ALIGNED (per-phase agents). |
| M1-101 | Tier check: Haiku/low recon may be fine for short prompts; raise to medium if recon misses files | P | WP-63 | Needs recon recall test. |
| M1-102 | Tier check: sonnet/medium scanners consistent with Sonnet 5.5 guidance | P | none needed | ALIGNED. |
| M1-103 | Tier check: Opus 5.5 gate start at medium and sweep; high/xhigh only where evals show gain; possible cost cut | P | WP-63 | Repo opus/high CONTRADICTS (C-4). |
| M1-104 | Test Fable 5.1 for hardest gate (architect/exit-gate) | P | WP-63 | Constitution forbids fable on gates; needs ADR/constitution amendment if trial wins. |
| M1-105 | Claude Code subagent `effort` frontmatter lets tiers be encoded natively | P | WP-509 | Repo already has `effort` field; verify it is honored by plugin agents. |
| M1-106 | Exploration: vague prompts fine when exploring; skip planning when exploratory; plan mode adds overhead | P | WP-10, WP-11 | Directly supports U1/U5. Repo has no exploratory mode (ADR 003/008 neighbors). |
| M1-107 | Sonnet 5.5: when user asks for ideas/options/plan, give that and stop; do not build until told | P | WP-11, WP-18 | Hard-stop rule for sketch. |
| M1-108 | Suggested sketch shape: no schemas, no gates, one agent, low/medium effort, "sketch not spec", assumptions list, promotion path to capture-need/draft-spec, non-binding label | I | WP-11, WP-14, WP-18 | Fully covered. |
| M1-109 | Fable 5 "report findings and stop" scope rule fits sketch | P | WP-11 | Covered. |
| M1-110 | Keep a deterministic guard: sketch mode may not write outside scratch dir (hook/permission) | I | WP-11, WP-512 | WP-11 has it; implementation mechanism (hook vs sandbox) in WP-512. |
| M1-111 | Gap: Anthropic engineering posts not fetched (multi-agent research, context engineering, effective harnesses, writing tools, skills) | U | WP-90 | Add explicit URL list to WP-90. |
| M1-112 | Gap: Claude Code skills/plugins/hooks/memory pages not read; plugin agent frontmatter specifics unverified | U | WP-90 | Blocks WP-509/WP-512. |
| M1-113 | Gap: model cards/release posts/migration guide not fetched; no benchmark numbers verified | U | WP-90 | Blocks WP-63 claims. |
| M1-114 | Gap: Claude Design article and github anthropics/claude-code frontend-design SKILL.md not read | U | WP-90 | Compare with muse; WP-511. |
| M1-115 | Gap: no Anthropic guidance on EARS or N-section prompts; claim that 5-part is unnecessary is inference | U | WP-62 | Ablation is the only evidence route. |
| M1-116 | Gap: no evidence on Haiku 5.5 vs 4.5 for recon accuracy | U | WP-63 | Needs test. |
| M1-117 | Gap: structured-outputs doc unread (schema feature limits e.g. additionalProperties, recursion) | U | WP-90, WP-505 | Repo schemas use additionalProperties false; verify compatibility. |
| M1-118 | Third-party summaries (mindstudio, claudefa.st, explainx, oh-my-fable) unread; non-authoritative | U | WP-90 | Do not cite. |
| M1-119 | Master page URL base and sub-URL list (platform.claude.com/docs/en/build-with-claude/prompt-engineering/, effort, agent-skills best-practices, code.claude.com best-practices, sub-agents, anthropic.com/engineering/harness-design-long-running-apps) | P | WP-90 | Source register; re-fetch for verbatim before quoting in constitution. |
| M2-01 | GPT-6 family: Astra (Sep 3 2026), Sol and Luna (Sep 22); GPT-6.1 Sol (Sep 29, gpt-6.1-sol) Codex default; launch pages 403 | S | WP-63, WP-90 | Unverified; browser verify. |
| M2-02 | latest-model guide ids: gpt-6-astra, gpt-6.1-sol, gpt-6-luna | P | WP-63 | |
| M2-03 | Astra and 6.1 Sol do not support `none` reasoning effort; use `low` | P | WP-70 | Repo SILENT (Codex counterparts carry no effort). |
| M2-04 | Responses API for tool calling with reasoning; remove temperature/top_p/top_logprobs when reasoning active | P | WP-70, WP-505 | Only relevant for API-based eval/runner; record. |
| M2-05 | prompt_cache_retention replaced by prompt_cache_options.ttl ("30m") | P | WP-502 | Record only. |
| M2-06 | Model guide (Oct 2 2026): five-part brief outcome, context, boundaries, definition of done, handoff; Codex start default effort, lower for simple, raise for deep | S | WP-70 | Repo CONTRADICTS ADR 001 shape for Codex? No: harness-authoring says do not mechanically translate; OK. Verify page. |
| M2-07 | Prompt guidance: concise paragraphs; lists only for parallel/sequential/comparable; avoid stock phrases | P | WP-70 | Informs Codex wording; Claude side no conflict. |
| M2-08 | Persist until intended goal complete; execute rather than propose unless destructive | P | WP-70, WP-18 | CONFLICTS with sketch hard-stop (C-6) unless boundary stated. |
| M2-09 | Complete authorized work before asking clarifying questions | P | WP-70 | Aligns with weaver:capture-need "no clarifying questions"; conflicts with weaver:clarifier one-question. Minor. |
| M2-10 | User instructions take precedence over skill guidelines; Astra context-sensitive: state hierarchy explicitly | P | WP-70 | Repo SILENT on instruction hierarchy (user > skill > agent). Add -> WP-509b? included in WP-70; flag as missing. |
| M2-11 | Do not write tests for reversible low-impact changes that mirror implementation; broaden tests only on new failures | P | WP-70, WP-46 | ALIGNED with ADR 008 and risk-based verification; supports U5. |
| M2-12 | "Can you..." requests = do the work | P | WP-70 | Boundaries needed in read-only/explore modes. |
| M2-13 | Codex docs moved: developers.openai.com/codex/* 308-redirects to learn.chatgpt.com/docs/* | P | WP-90 | Repo docs may link old URLs; add to WP-04 link check. |
| M2-14 | Codex prompting: optional blocks Goal, Context, Output, Boundaries; short prompt often works | P | WP-70 | |
| M2-15 | Describe process only when process matters; otherwise leave room to search; one or two hard rules | P | WP-64, WP-70 | Matches Anthropic Fable 5 brevity; contradicts constitution volume. |
| M2-16 | AGENTS.md: global ~/.codex then git root -> cwd concatenated root-down, closer overrides; cap 32 KiB project_doc_max_bytes; fallback filenames | P | WP-71 | Repo AGENTS.md 5.7K ALIGNED; but constitution is separate. Check Codex rendered size for generated files. |
| M2-17 | Subagents: TOML in ~/.codex/agents or .codex/agents; required name, description, developer_instructions; optional model, model_reasoning_effort (low..ultra); built-ins default/worker/explorer | P | WP-70 | Repo CONTRADICTS WP-70 as drafted: harness-authoring.md forbids TOML as plugin contract; uses markdown role cards. See C-7. |
| M2-18 | agents.max_concurrent_threads_per_session; subagents inherit parent sandbox/approval and cannot override; extra token cost | P | WP-55, WP-70 | Read-only enforcement for sketch must be parent sandbox. |
| M2-19 | Skills: open agent-skills standard; SKILL.md name+description; scripts/references/assets; repo/user/admin/system discovery; $skill explicit or implicit; progressive disclosure; plugins distribute; prefer instructions over scripts unless deterministic | P | WP-70, WP-72 | Repo ALIGNED; skills-routing key is dir name (AGENTS.md). |
| M2-20 | Sandbox/approvals: two layers; workspace-write disables network by default; cloud container setup online, agent offline, secrets removed | S | WP-70, WP-80 | Matters for Playwright/npm install in Codex (network off) -> add to WP-12/41. |
| M2-21 | Agents SDK April 2026 sandbox agents, MCP and AGENTS.md support, handoffs/manager patterns | S | WP-90 | Aggregator-sourced. |
| M2-22 | Changes: reasoning always on for Astra/Sol; sampling params removed; Responses API required with tools+reasoning; cache API changed | P | WP-70 | |
| M2-23 | Shift to outcome/definition-of-done briefs; fewer hard rules | P | WP-70, WP-64 | Convergent with Anthropic (M1-07). |
| M2-24 | Agentic by default; restraint stated as boundaries | P | WP-70 | Codex sketch skill needs explicit stop. |
| M2-25 | Skills/AGENTS.md/subagents first-class and standardized | P | WP-70, WP-71 | |
| M2-26 | OpenAI favors short outcome briefs, few hard rules; Claude/Wisp structured XML and contracts | I | WP-70, WP-62 | See C-10. |
| M2-27 | Codex agents TOML; sandbox not per-agent overridable vs Claude per-agent tools | I | WP-70, WP-55 | Repo ALIGNED re: not shipping TOML. |
| M2-28 | Carry over: structured outputs via Responses, default-fail gates, EARS in output contracts, tiers mapped gpt-6-luna/low recon, gpt-6.1-sol medium scanners, high/ultra exit-gate | I | WP-63, WP-70 | Mapping unverified; harness-authoring says never translate tiers mechanically (C-7). |
| M2-29 | Codex wording needs: avoid bloated 5-part bodies, outcome/DoD/handoff first, stop conditions, hierarchy user>skill>agent, no `none` effort, tests-only-when-risk | I | WP-70 | Covered; hierarchy item missing from WP-70 text. |
| M2-30 | AGENTS.md combined 32 KiB: keep constitution reference short, link not inline | I | WP-71 | ALIGNED. |
| M2-31 | Generate .codex/agents/*.toml with developer_instructions; explorer/worker built-ins or luna/low custom agent for sketch | I | WP-70 | CONTRADICTS repo policy (C-7). |
| M2-32 | Native features to use: skills, plugins, subagents with max_concurrent cap, cloud tasks for parallel, worktrees (unfetched) | I | WP-55, WP-70 | Cloud tasks/worktrees unverified -> WP-90. |
| M2-33 | Sketch mode fits "short prompt often works": low effort, Luna, no gate, non-binding | I | WP-11, WP-70 | |
| M2-34 | Gap: GPT-6 model guide, Sol/Luna launch, system cards 403 | U | WP-90 | |
| M2-35 | Gap: no OpenAI frontend/design/vision-in-loop guidance (URL 404); cookbook unsearched | U | WP-90 | Matters for Codex design ideation. |
| M2-36 | Gap: Codex plugin manifest, hooks, MCP config, worktrees, cloud docs unfetched; confirm dist/codex layout matches current .codex-plugin spec | U | WP-90, WP-70 | Direct risk to marketplace-sync output; verify. |
| M2-37 | Gap: Agents SDK docs unread; preamble behaviour unconfirmed | U | WP-90 | |
| M2-38 | Gap: is there still a "-codex" model variant | U | WP-90, WP-63 | |
| M2-39 | Fetcher summaries may paraphrase; re-fetch verbatim before citing in constitution | U | WP-90 | Applies to all M2 quotes. |
| M2-40 | Earlier GPT-5.x / 5.3-Codex / 5.5 exist (Wikipedia hits only) | U | WP-90 | Also NF cites "GPT-5.6 Sol" naming which conflicts with M2 lineup (GPT-6.1 Sol): see C-11. |
| X-U1 | User: plugin workflows too rigid for early/experimental work; want flexible vibe-coded iteration to flesh out ideas, see designs, validate tools without tests/specs | P | WP-10, WP-11, WP-15, WP-18 | Core requirement; ADR 003/008 neighbors; covered. |
| X-U2 | User wants understanding of work on techworx and orin-dx sites, plugin performance, gaps, for front-end and design ideation | P | WP-03, WP-56, WP-91 | Evaluation deliverable, not a plugin change; covered by baseline WP-03. |
| X-U3 | User wants industry practice survey: DESIGN.md, uSpec, Figma MCP, Claude Design, Shopify/Airbnb/Vercel/Atlassian/Netflix/IBM, Anthropic 5.5, GPT guidance, AGENTS.md, ICAO, caveman, TanStack Intent | P | WP-90 | Scope list; every named topic has rows below. DESIGN.md/Figma/Shopify etc. are in R/S notes, out of this map. |
| X-U4 | "Let's not cut things": every finding gets a work item or evidence-based disposition | P | all | This map is the response; items with "none needed" carry reason. |
| X-U5a | 2026-10-14 20:25: lean less on specs/tests while building; two phases: exploratory build quick, validate ideas; specs/tests come after narrowing, avoid regressions | P | WP-10, WP-11, WP-14, WP-19 | Core. Two-phase model = WP-18 router + WP-19 hardening. |
| X-U5b | 10-08 seo-geo: "stop with these tests. It's a waste of time" | P | WP-18, WP-46 | Evidence tests were overweight in exploratory work; verification should be mode-dependent (WP-18). |
| X-U5c | 10-14 16:49 "I said I wanted us to iterate first" | P | WP-18, WP-11 | Router must honor user's declared mode (declared-mode persistence) - add to WP-18 acceptance. |
| X-U5d | "We don't test our CSS per se... visual testing later" | P | WP-45, WP-42 | WP-45 "behavior-vs-CSS testing policy" covers; user preference should be default. |
| X-U5e | "I need actual examples of what is being approved" | P | WP-34 | Covered (show, don't describe). |
| X-U5f | "did you lose that decision. I'm frustrated now" | P | WP-13 | Decision-log "recorded but not applied" detection covers. |
| X-U5g | "Let's stop doing the claude artifacts, we can try locally" | P | WP-12 | Covered (Artifacts optional, local first). Note: this session's Artifact tool conflicts; default must be local. |
| X-UB1 | uSpec blog/docs/repo URLs; ownership and license of github.com/redongreen/uSpec NOT verified | U | WP-90 | Do not depend on it before license check. |
| X-UB2 | uSpec problem: 7 stacks, hundreds of spec pages; stale specs make engineering build from assumptions | P | WP-73 | Drift motivation; covered. |
| X-UB3 | Three layers: Agent Skills (six: Anatomy, API, Properties, Color annotation, Structure, Screen reader; Motion from After Effects), Figma Console MCP (local WebSocket), rendering script populating Figma templates | P | WP-35, WP-34 | Spec-render-in-Figma not covered; WP-34 renders in HTML boards; Figma render is out of scope unless WP-35. Disposition: record as optional adapter. |
| X-UB4 | Pipeline Extract -> Compile -> Render; Figma plugin captures deterministic evidence once; create-component-md produces schema-valid JSON + concise Markdown; create-* skills read Markdown not Figma ("save thousands of tokens per run") | P | WP-32, WP-31, WP-35 | WP-32 facts file ~ Component.MD. Missing: explicit "downstream reads compiled file not source" rule and token-saving claim measurement. |
| X-UB5 | Deterministic extraction (tokens, variants, structure, hierarchy, modes) vs LLM (a11y semantics, token mapping across states, organization, platform behavior) | P | WP-32 | Covered; keep boundary table in WP-32. |
| X-UB6 | Hallucination control: reference libraries loaded first, structured schemas, real-data grounding, local execution | P | WP-33, WP-32 | Covered; repo muse partly (schema); reference library absent. |
| X-UB7 | Human-in-loop: share link + optional context for non-inferrable states/platform behavior; results rendered for review | P | WP-34 | Covered. |
| X-UB8 | Results: screen-reader spec for 3 platforms under 2 minutes; months -> days | P | WP-03 | Vendor claim; use as expectation only; unverified. |
| X-UB9 | Limits: needs well-structured Figma files and accurate tokens; extract-once means initial capture must be accurate | P | WP-32, WP-35 | Add "input quality precondition" check to WP-35 adapter. |
| X-UB10 | Roadmap: drift detection, code-to-spec, new spec types; runs in Cursor, Claude Code, Codex | P | WP-73 | |
| X-UC1 | TanStack Intent: maintainers ship SKILL.md inside npm packages so skills version 1:1 with code; delivery vs maintenance problem | P | WP-72 | Repo ships skills in plugin (versioned); consumer-repo packaging of design skills not covered. Partial. |
| X-UC2 | `validate` compiles fenced JS/TS examples in SKILL.md with TypeScript compiler | P | WP-72 | Repo SILENT; no example-compile check in `just check`. |
| X-UC3 | `maintainer review` flags guidance affected by source changes, tied to source+skill versions ("has someone checked this against what changed?") | P | WP-72, WP-73 | |
| X-UC4 | `repair --write` mechanical frontmatter fixes only; code needs review | P | WP-72 | Covered. |
| X-UC5 | Reusable GitHub checks (validation, generated-file drift, pending source reviews) surface in Actions summary, never auto-apply fixes; agent hooks use local CLI | P | WP-72 | Repo has generated-file drift via marketplace-sync check (ALIGNED). Pending-review check missing. |
| X-UC6 | Skills "belong in the development process" | P | WP-72 | Principle. |
| X-IC1 | Standard words: affirm, negative, roger (received not yes), wilco, unable, standby, say again, verify, correction, disregard; avoid "OK" | K | WP-53, WP-90 | Unverified against ICAO Annex 10 / Doc 9432. Repo SILENT. |
| X-IC2 | Readback/hearback: pilot reads back safety-critical items; controller verifies and corrects; unchecked readback is theater | K | WP-52 | Covered; must define who verifies the readback (blocker echo checked by gate). |
| X-IC3 | SID/STAR: named published procedures referenced by name in clearance; pre-agreed details | K | UNMAPPED -> WP-513 | WP-53 vocabulary does not cover named standard procedures (e.g. "run HARDEN-A11y"). |
| X-IC4 | Lost-communications procedures; missed approach/go-around predefined at decision altitude | K | WP-54, WP-51 | Covered; mapping retry cap = missed approach. |
| X-IC5 | Pilot-in-command authority: may deviate in emergency but must declare and report afterward | K | WP-51 | Overrides declared/logged; covered. |
| X-IC6 | Urgency tiers (pan-pan/mayday) with fixed handling | K | WP-53 | P0-P3 definitions. |
| X-IC7 | IFR (controlled, clearance, controller responsible for separation) vs VFR with FIS/AFIS (information only, pilot responsible); IFR can be picked up in air and cancelled | K | WP-18 | Covered ("IFR/VFR framing"). Add explicit "cancel IFR" (leave gated mode) already in WP-18. |
| X-IC8 | Mapping: sketch=VFR+FIS; promote=pick up IFR; stall=lost-comms; retry cap=missed approach; override=declared deviation; closed vocabulary+readback for gate churn | K | WP-18, WP-14, WP-54, WP-51, WP-52, WP-53 | Fully distributed. |
| X-IC9 | Limits: phraseology exists for noisy voice and lives at stake; needs enforcement/training; agents follow prompts so vocabulary must be short | K | WP-53 | Condition: A/B eval whether vocabulary reduces gate rounds before adopting -> WP-514. |
| X-CV1 | Caveman skill github.com/JuliusBrussee/caveman, ~94k stars (enterprisedna) | S | WP-65 | Star count unverified. |
| X-CV2 | Repo eval: 3 arms (baseline, "Answer concisely", skill), 1 call/arm/prompt, Opus 5.5, tiktoken o200k_base, regex fidelity; claims 65% mean (22-87%) over 10 prompts; self-stated limits | P | WP-65 | Weak evidence (n=1). |
| X-CV3 | Independent dev.to nazecode: one C# task n=3: "Be concise." -28.7%, caveman -42.9%, ultra -63.6%; all correct; skill needs ~10 answers to break even vs two-word prompt | P | WP-65 | |
| X-CV4 | JetBrains caveman: Harbor 0.17, Claude Code 2.1.200, claude-sonnet-5 low, SkillsBench 86/87 tasks, 3 runs, ~240 trials, ~$106; Arm B forced activation | P | WP-60, WP-65 | |
| X-CV5 | Output tokens: smoke 10 tasks k=1 -29.5%; k=3 -6.7%; full 86 (82 pairs) k=1 -8.5% (592k->542k) | P | WP-60, WP-65 | Shows k=1 smoke misleads. |
| X-CV6 | Quality: 64 tied, 10 skill higher, 8 lower, sign test p=0.82; mean score 0.326 vs 0.311 | P | WP-60 | No quality effect. |
| X-CV7 | Cost: expected ~-10% but raw totals +11.6% ($40.60 vs $36.39) due to one task crossing 200k long-context tier ($8.29 vs $0.33). "Never trust a k=1 eval." | P | WP-60, WP-91 | Long-context tier cliff -> WP-515. |
| X-CV8 | Others: real coding tasks 14-21% (BetterStack); community reproductions 30-50%; agentic ~8.5%; "Be concise. Return JSON." handles ~60% of savings | S | WP-65 | Baseline arm "Be concise. Return JSON." mandatory in WP-65. |
| X-CV9 | Brevity paper arXiv 2604.00025: 31 models, 1,485 problems; brevity improves large-model accuracy up to 26 points on some benchmarks | S | WP-90, WP-65 | Verify arXiv id and claim; do not cite. |
| X-CV10 | Concise-CoT study showed GPT-3.5 -27.69% on math | U | WP-90 | Unverified; discard unless located. |
| X-RT1 | rtk JetBrains Part 2 (Jul 20 2026): Harbor 0.18, Claude Code 2.1.201, claude-sonnet-5 low and high, rtk v0.43.0 (`rtk init -g`: binary + PreToolUse hook + RTK.md), 425 trials, ~$320; claims -60-90% | P | WP-68 | |
| X-RT2 | Ceiling replay of 83 transcripts: 1,056 shell cmds, 349 rewritable, 525 no rule, 182 skipped; of 1.9M chars output 20% compressible, 46% shell no rule, 34% Read/Grep bypass hook; cap ~3% of input | P | WP-68, WP-03 | Replay-ceiling method = free first rung; WP-516 for tool. |
| X-RT3 | Measured low effort, 80 pairs: cost +7.6% median (p=0.004), turns +13.8% (p=0.03), cache reads +14.3% (p=0.008), fresh input +3.2% (p=0.23), output +6.7% ns; heavily rewritten +24% vs +5% | P | WP-68 | Directly relevant: the user's global config installs rtk; this agent runs under rtk hook. |
| X-RT4 | High effort: cost +0.1% (p=0.99). Quality: 151 pairs 10 better/8 worse/133 identical; sign p=1.0 | P | WP-68 | |
| X-RT5 | One glibc compatibility failure; one broken rewrite class (compound find predicates) | P | WP-68 | Repo constitution mandates fd/rg/bat/eza; with rtk rewriting, interplay unknown. |
| X-RT6 | `rtk gain` reported 96.2M tokens saved while bill rose; counterfactual counts raw output, chars/4, cached re-reads at a tenth | P | WP-68, WP-60 | Lesson: self-reported savings are claims. |
| X-RT7 | Lessons: paired analysis; per-task medians + Wilcoxon; exclude errored tasks from both arms; ladder replay -> wiring -> k=1 -> k=3 -> full at each effort; ~80 tasks rule out only large effects (~700 runs/side for subtle) | P | WP-60 | WP-60 covers ladder; add power note -> WP-514. |
| X-RT8 | User's ~/.claude/RTK.md installs rtk with same hook; own-workflow paired test open; do not change user config unasked | P | WP-68 | Constraint recorded. |
| X-NF1 | Netflix teams plugged JetBrains headless code-intelligence engine into Claude Code and Codex for Java/Kotlin (JAR boundaries); Netflix built daemon (warm index, session manager by project root, GraalVM) and CLI since LSP not agent-callable | P | WP-47 | Vendor-hosted case study. |
| X-NF2 | Eval: 2 codebases, navigation + end-to-end tasks; Opus 5, Sonnet 5, Codex GPT-5.6 Sol (medium/high); tokens + time; LLM judge vs reference change set; deterministic navigation scoring; outliers excluded both arms | P | WP-60 | "GPT-5.6 Sol" vs M2 "GPT-6.1 Sol": C-11. |
| X-NF3 | Results 20-30% more efficient typical, up to ~65% best case (strongest model, high effort, navigation); end-to-end ~21-30%; correctness held/improved; one time comparison unrepresentative | P | WP-47 | Snapshot; vendor. |
| X-NF4 | "Agents need a code engine, not a virtual editor"; "benefit to a deterministic intelligence layer alongside your agent"; Netflix plans Python/TS/JS/Go | P | WP-47 | TS/JS is Wisp front-end relevant but not yet shipped; dependency not available now. |
| X-NF5 | Commit f10e6b8 "feat(smith): add language-service evidence guidance" already points this direction | P | WP-47 | Repo ALIGNED. |
| X-NF6 | Not about design/front-end; no Netflix design-system answer (job posting hint of "design intelligence layer", per S2) | P | WP-47, WP-90 | Disposition: no design inference allowed. |
| X-PL1 | muse plugin.json, README:23, SKILL.md:11 cite "ranger's accessibility hazard taxonomy"; grep finds none in ranger | P | WP-01, WP-44 | Verified defect. |
| X-PL2 | 29/31 schemas have `reasoning`; 44 agents mention it; constitution L242 requires it | P | WP-61 | Same as M1-46. |
| X-PL3 | ADR index 001-010 with guardrails; decision-records.md: write ADR only when architectural and expensive/non-obvious | P | WP-10, WP-30, WP-40, WP-62 | Each ADR-needing WP must pass that test; WP-10 amends 003; WP-62 touches 001/006; WP-30 follows 004 (spec@2). |
| X-PL4 | `just check` = manifests test versions skills-doc reference-size marketplace-check mermaid; Codex via marketplace-sync; harness counterparts per harness-authoring.md | P | WP-04, WP-70 | New checks (WP-04, WP-508) join `just check`. |
| X-MI1 | Corpus correction: ~812 jsonl mostly subagent transcripts; ~7 real top-level sessions; plugin agents used in 2 (orin-dx b8d16e96 09-29..10-03; pages 24655582 10-05..10-16) + vanguard in e8f0978b (10-17) | P | WP-03, WP-56, WP-91 | Small n: any baseline stats are anecdotal; say so. |
| X-MI2 | ~/projects/orin-dx-site holds only brand/ HTML artifacts (no git, no docs); docs live in ~/projects/pages/docs | P | WP-80, WP-13 | Decision log location must account for non-git site folders. |

---

## (1) CONTRADICTIONS

C-1 (Anthropic vs Anthropic, by model): Opus 5 verifies unprompted and explicit verification instructions cause over-verification (M1-28), but Sonnet 5.5 and Haiku 5.5 at low/medium skip real checks and Anthropic supplies a "run a real check" paragraph (M1-29). Wisp agents mostly run on sonnet/medium, so the rule must be model-conditioned; WP-64 as drafted ("avoid over-verification in Opus producers") must be paired with WP-506.
C-2 (Anthropic internal): "do not use subagents to verify your own work" (M1-30) vs "fresh-context verifier subagents beat self-critique" (M1-31). Reconcile: orchestrator-owned independent gate yes; agent-spawned self-verification no. Matches WP-55.
C-3 (guidance vs repo): shrinking or removing the byte-identical constitution (M1-88) conflicts with ADR 006 and the Static Prompt Prefix Invariant, which exists for cache sharing. Cost benefit of removal must be measured net of cache hits; draft WP-62 does not state this.
C-4 (guidance vs repo): Opus 5.5 default medium and medium >= Opus 5 high (M1-19/20/103) vs constitution `opus / high` for gates. Fable 5.1 low competitive (M1-79) vs constitution "fable never gates".
C-5 (Anthropic vs caveman): Fable 5 says keep output short by selecting content, not by fragments or arrow chains (M1-51); caveman style is telegraphic. WP-65 must restrict to "Be concise." style, not caveman, and never on specs/handoffs.
C-6 (OpenAI vs sketch): OpenAI/Codex models persist and act on "can you..." (M2-08/12) while Anthropic Sonnet 5.5 says stop after giving ideas (M1-107). Sketch skill needs explicit boundary wording in both harnesses; enforcement via sandbox on Codex.
C-7 (draft WP vs repo): WP-70 says "TOML subagents" and M2-31 suggests generating .codex/agents/*.toml, but harness-authoring.md states TOML is host config, never a marketplace contract, with markdown role cards. Also "map tiers to GPT-6 models" conflicts with "never mechanically translate model tiers". WP-70/WP-63 text must be corrected.
C-8 (draft WP internal): WP-16 "~4 directions" vs WP-11 "~3 options". Pick one; Anthropic Sonnet 5 source says 4.
C-9 (guidance internal): Anthropic frontend blog warns against low-altitude hardcoded hex codes yet WP-31/DESIGN.md and Figma practice are token-exact. Resolve: tokens are system facts; direction/aesthetic guidance stays high-specific (named patterns), not hex lists.
C-10 (OpenAI vs Wisp style): OpenAI "few hard rules, outcome briefs" and Anthropic Fable 5 "too prescriptive" vs Wisp 290-line EARS constitution and 5-part skeleton; supported only by inference until ablation (M1-115).
C-11 (source inconsistency): X-NF2 reports Codex with "GPT-5.6 Sol" (Oct 15 JetBrains post), M2 lists GPT-6.1 Sol as Codex default (Sep 29). Either naming differs or one is wrong; resolve via WP-90.
C-12 (guidance vs repo): reasoning-extraction refusal risk vs constitution L242 mandatory `reasoning` field in every schema (M1-46). Also ADR 004 immutability forces @n+1 for 29 schemas.
C-13 (draft WP vs user): WP-12 keeps Artifacts optional; user said stop using Claude artifacts, try locally (X-U5g). WP-12 should default local and treat Artifacts as opt-in only.
C-14 (agent practice vs constitution): constitution mandates rg/fd/bat; rtk hook (global user config) rewrites shell commands; X-RT5 shows broken rewrite classes. Interplay unknown (WP-68).
C-15 (user vs repo): user wants fewer tests in exploration (X-U5a/b); repo ADR 008 dropped test-first only for features; verification mandatory elsewhere. Router (WP-18) must define which gates apply per mode.
C-16 (Anthropic vs repo): agent `description` should be short (M1-40); Wisp agent descriptions are multi-sentence routing text. Verify plugin spec before shortening (they also serve routing).

## (2) CLAIMS TO VERIFY before acting

1. reasoning_extraction refusal (M1-46): reproduce by running 3 agents (gate, scanner, drafter) on Fable/Opus 5.5/Sonnet 5.5 and counting refusals with `reasoning` field present vs renamed; fetch the exact doc text.
2. Opus 5.5 medium >= Opus 5 high; Fable 5.1 low competitive (M1-20, M1-79): mason:evaluate effort sweep; no vendor numbers verified.
3. Haiku 5.5 low skips searches (M1-27): recon recall vs ripgrep ground truth.
4. Sonnet 5.5 stopping reviewer subagents saved ~1/3 cost (M1-38): check against own transcripts (WP-91).
5. Plugin-agent frontmatter honors effort, maxTurns, tools, skills, memory; hooks/permissionMode in plugin agents (M1-39/105/112): read Claude Code plugin reference and test.
6. Codex: plugin manifest, hooks, MCP, role-card discovery, worktrees, cloud tasks (M2-32/36); `learn.chatgpt.com` AGENTS.md 32 KiB behavior with generated files: read pages in browser and run codex locally.
7. GPT-6 lineup, `none` unsupported, model ids, "-codex" variant, GPT-5.6 vs 6.1 naming (M2-01..03, C-11): browser fetch of 403 pages.
8. ICAO phraseology (X-IC1..8) from Annex 10 Vol II, Annex 11, Doc 4444, Doc 9432; FIS/AFIS rules vary by state. Only the analogy is needed, but do not cite normatively.
9. uSpec repo ownership/license/features (X-UB1) and the "under 2 minutes" claim (X-UB8): read repo LICENSE and docs.
10. Brevity paper arXiv 2604.00025 and Concise-CoT -27.69% (X-CV9/10); caveman star count (X-CV1).
11. Netflix numbers are vendor case study; TS/JS support is a plan (X-NF3/4).
12. Claude Design article, frontend-design SKILL.md (M1-75/114).
13. Structured-outputs schema limits vs Wisp schemas (M1-117): validate all 31 schemas.
14. Skill description length and SKILL.md line limits in current plugins (M1-64): script check.
15. WP-draft claim "29 of 31 schemas" and "44 agents" (X-PL2): re-count in WP-05.
16. rtk results are for claude-sonnet-5 on SkillsBench; no evidence for the user's workflow (WP-68).

## (3) PROPOSED NEW WPs (deduplicated)

- WP-501 Model-generation re-check policy: constitution/authoring rule that tier/effort pins carry the model version they were measured on, with a re-sweep trigger on new generations; reconcile tier table versioning. Target: shared/constitution.md (model tiers), shared/references/evaluation/.
- WP-502 Model/API facts reference (thinking always-on, budget_tokens 400, prefill gone, per-message effort beta, progress-as-thinking display, Codex `none`, cache TTL options): authoring-time notes. Target: shared/agent-best-practices.md.
- WP-503 Assumption ledger per harness component: each agent/constitution rule records the model weakness it compensates for, reviewed at model change. Target: shared/references/authoring/ and mason:audit-plugin.
- WP-504 Scope and literal-following audit: state instruction scope explicitly, request-is-deliverable rule (do not narrow/widen/swap), no "Want me to...?" in unattended runs. Target: constitution Autonomy section, skill orchestrators.
- WP-505 Structured-output adoption and JSON-only thinking caveat: use API structured outputs/Responses where available; test "Think the problem through" line and effort floor for JSON-only agents; verify schema compatibility. Target: shared/references/authoring, shared/schemas.
- WP-506 Real-check and claim-audit rules for producers on sonnet/haiku at low/medium: exercise-the-change check, syntax-only does not count, name unrun checks, audit each claim against a tool result before reporting. Target: smith implementer, constitution.
- WP-507 Positive examples and rationale: add one `<example>` per agent where format is error-prone; convert bare "never X" into reason-bearing rules; needs ADR 001/002 check. Target: agents, shared/references/authoring.
- WP-508 Skill/agent authoring conformance checks in `just check`: description <=1024 chars, third person, SKILL.md <500 lines, refs one level deep, >=3 evals present per skill, example code compiles (X-UC2). Target: scripts/ + mason:audit-plugin.
- WP-509 Native agent frontmatter adoption: evaluate `tools`, `maxTurns`, `skills`, `memory`, depth/concurrency caps for Claude; document Codex equivalents as role-card guidance only. Target: constitution frontmatter section, harness-authoring.md.
- WP-510 Reconcile Codex TOML policy: decide whether an optional, non-contract TOML generator (developer_instructions, model_reasoning_effort, sandbox) is allowed, and correct WP-70 wording; add hierarchy and stop-condition language. Target: shared/harness-authoring.md, harnesses/codex.
- WP-511 Claude Design / external canvas interop: handoff of options to and from Claude Design and Codex equivalents; verify tools first. Target: muse sketch skill reference.
- WP-512 Deterministic guard hooks: scratch-dir write guard for sketch, Stop-hook retry cap, pre-commit scoping; Codex sandbox equivalent. Target: plugins/muse + plugins/smith hooks, harnesses/codex.
- WP-513 Named standard procedures (SID/STAR analogue): short named routines (e.g., HARDEN-A11y, PROMOTE-SKETCH) referenced by name in dispatch. Target: shared/references/authoring, skills.
- WP-514 Evaluation methodology reference: ladder (replay, wiring, k=1, k=3, full), power/ceiling note (80 tasks only rule out large effects), paired medians + Wilcoxon, sign test, exclusion rule, bill-based cost; plus A/B of closed vocabulary and of "Be concise. Return JSON." baseline. Target: shared/references/evaluation/, mason:evaluate.
- WP-515 Cost-cliff monitoring: detect long-context (200k) tier crossings and single-task cost outliers in baseline and eval reporting. Target: WP-03/WP-91 script, mason:evaluate report.
- WP-516 Transcript-replay ceiling tool: estimate rewritable/compressible fraction of tool output before adopting any token saver. Target: tools/.
- WP-517 Native plugin-eval/skill-doctor assessment: evaluate Claude Code `claude plugin eval` and `/skill-doctor` (listed in session tooling, not in findings) as complements to mason:evaluate. Target: shared/references/evaluation/.
- WP-518 Promote WP-61 (reasoning field) to G0 defect with a costed plan (prompt-only reframe now, schema @n+1 later per ADR 004).
