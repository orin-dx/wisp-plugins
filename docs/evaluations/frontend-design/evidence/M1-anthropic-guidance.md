# M1: Anthropic current guidance (Claude 5 family) and implications for Wisp
Date: 2026-10-17. Tags: [P] fetched primary page, [S] search summary only, [U] unverified.
Base URL: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/

## A. Landscape [P]
- Master page claude-prompting-best-practices lists: Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 5, Opus 4.8/4.7/4.6, Sonnet 5.5, Sonnet 5, Sonnet 4.6, **Haiku 5.5**, Haiku 4.5. Haiku 5.5 exists and is the first Haiku with effort levels (default medium). Wisp's "haiku recon" tier should be re-evaluated against it.
- Each model has its own page: prompting-claude-fable-5-1, -fable-5, -opus-5-5, -opus-5, -sonnet-5-5, -sonnet-5, -haiku-5-5. Doc says "Where a technique names a specific model, treat it as measured on that model and re-check it against your own evals."
- Effort doc https://platform.claude.com/docs/en/build-with-claude/effort : levels low/medium/high/xhigh/max. Defaults: high everywhere except Opus 5.5 and Haiku 5.5 = medium. "Effort level names don't correspond to the same amount of thinking across models." low = "Simpler tasks that need the best speed and lowest costs, such as subagents".
- Thinking: Fable 5.1, Fable 5, Opus 5.5 are thinking always-on, adaptive only. Sonnet 5.5 lowest setting `between_tools`. budget_tokens returns 400 on 4.7+. Prefill unsupported since 4.6.

## B. What changed vs 4.x (direct quotes)
1. Scaffolding/prescriptiveness is now a liability [P]
 - Fable 5: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality. Review and consider removing older instructions if default performance is better." (prompting-claude-fable-5)
 - Fable 5: "Capability improvements at this level are also a good prompt to re-evaluate which instructions, tools, and guardrails are still needed."
 - Fable 5: "Instruction-following is improved enough that you can steer most behaviors with a brief instruction rather than enumerating each behavior by name."
 - Master: "Prefer general instructions over prescriptive steps. A prompt like 'think thoroughly' often produces better reasoning than a hand-written step-by-step plan. Claude's reasoning frequently exceeds what a human would prescribe."
 - Harness blog https://www.anthropic.com/engineering/harness-design-long-running-apps : "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing"; Opus 4.6 "required significantly less scaffolding than 4.5" (paraphrase by fetch tool).
2. ALL-CAPS/emphasis [P]
 - Master: "If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'." (stated for 4.5/4.6, still in the current master page).
 - Claude Code best practices https://code.claude.com/docs/en/best-practices : "If you emphasize many lines, none of them stands out." and "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
 - Caveat: Sonnet 5's own frontend snippet still uses "NEVER". Emphasis is not banned, it is rationed.
3. Literal instruction following [P]
 - Sonnet 5: "interprets prompts literally and explicitly... does not silently generalize an instruction from one item to another... If you need Claude to apply an instruction broadly, state the scope explicitly."
 - Opus 5 / Sonnet 5 review harnesses: "If your review prompt says 'only report high-severity issues' or 'be conservative,' the model may follow that instruction literally and report less; ask it to report everything and filter in a separate pass instead." Sonnet 5: "Report every issue you find, including ones you are uncertain about... a separate verification step will do that... include your confidence level and an estimated severity". STRONGLY SUPPORTS Wisp's scanner (recall) -> adversary/gate (filter) split.
4. Effort replaces prompt-level thinking control [P]
 - Opus 5.5: "Effort is the main control for how much Claude Opus 5.5 thinks... Start at medium, the default... set it explicitly, and test several levels against your own evals". "In Anthropic's testing, Claude Opus 5.5 at medium matches or exceeds Claude Opus 5 at high on coding and knowledge-work evaluations, and on several coding evaluations low comes close".
 - Opus 5.5: "To get less thinking, lower the effort level first. Lowering effort reduces thinking... more reliably than prompt instructions do." Sonnet 5.5: "Asking it in the system prompt to think less doesn't reliably reduce its thinking." Haiku 5.5: telling it to answer directly "didn't stop it from thinking".
 - Opus 5.5: remove "think carefully" lines in chat prompts. Sonnet 5.5 does allow one line "Think the problem through before you answer." for JSON-output reasoning tasks, which lifts high-effort accuracy to near xhigh.
 - Effort also scales tool calls: "Lower effort levels tend to... Make fewer tool calls... Proceed directly to action without preamble" (effort doc).
 - Per-message effort change (beta, header mid-conversation-output-config-2026-07-01) preserves cache.
 - Sonnet 5.5 at low: "can skip verifying a change"; at low/medium "more likely to stop and check in with the user before it finishes". Haiku 5.5 at low: "more likely to skip a search, stop early, or skip a check"; low->medium "roughly halved early stopping".
5. Verification / self-checking is model-dependent [P]
 - Opus 5: "verifies its own work without being told... If your prompt contains explicit verification instructions... remove them: instructions like these cause over-verification... The same applies to legacy harness scaffolding that adds separate verification steps." Also "do not use subagents to verify or double-check your own work" (sample damping prompt) and "Avoid instructing re-checks it already performs".
 - But Sonnet 5.5 and Haiku 5.5 at low/medium: report done without a real check; Anthropic supplies a paragraph: "run a real check that exercises the change before reporting it done... A syntax-only check, or a check command that failed to start, does not count... Only if no real check can run here, say which one you did not run and why".
 - Fable 5: "Separate, fresh-context verifier subagents tend to outperform self-critique." and "Before reporting progress, audit each claim against a tool result from this session... nearly eliminated fabricated status reports".
 - Harness blog: "Separating the agent doing the work from the agent judging it proves to be a strong lever"; self-grading agents "confidently praising the work". Claude Code best practices: independent subagent reviewer in fresh context, plus a warning: "A reviewer prompted to find gaps will usually report some, even when the work is sound... Chasing every finding leads to over-engineering... Tell the reviewer to flag only gaps that affect correctness or the stated requirements".
 - Claude Code: "Give Claude a check it can run" and deterministic gates via Stop hook / /goal. Tests/commands beat LLM judgment where possible.
6. Subagents [P]
 - Opus 4.6 / Opus 5: "delegates to subagents more readily than prior models... multiplies cost and time when applied to small tasks"; sample: "Delegate to a subagent only for large tasks that are genuinely independent and parallelizable... Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work."
 - Fable 5 / 5.1: more dependable parallel subagents; "Delegate independent subtasks to subagents and keep working while they run."; let lead continue while subagents run.
 - Sonnet 5.5 at xhigh/max can "launch reviewer subagents"; instruction to stop that "cut session cost by about a third, with no change in quality".
 - Claude Code subagents https://code.claude.com/docs/en/sub-agents : frontmatter supports `model` (sonnet/opus/haiku/fable), `effort`, `tools`, `skills`, `memory`, `maxTurns`; "Use Haiku for Exploration" for read-only search; description should be short ("kept brief"), detailed logic goes in body; depth cap default 3, concurrency 20, env CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH / _MAX_CONCURRENT_SUBAGENTS.
7. XML tags, roles, examples [P]
 - Master page still recommends XML tags ("reduces misinterpretation"), a one-sentence role ("Even a single sentence makes a difference"), 3-5 examples in <example> tags. None of this is deprecated. Note: no guidance requires a fixed N-part tag skeleton; XML is for separating instruction/context/input types.
 - Examples caveat on Fable 5.1: one complete example fixed unmarked quoting. Sonnet 5: "Positive examples... tend to be more effective than negative examples or instructions that tell the model what not to do."
 - Tell Claude what to do rather than what not to do; give the reason ("Claude is smart enough to generalize from the explanation"). Fable 5: "performs better when it understands the intent behind a request".
8. reasoning_extraction refusals: DIRECT RISK TO WISP SCHEMAS [P]
 - Fable 5, Fable 5.1, Opus 5, Opus 5.5, Sonnet 5.5: "Prompts, skills, and tool descriptions that ask the model to write out its thinking or reasoning may be declined with the reasoning_extraction category." Fix: "Ask for a short explanation of the answer or a summary of the actions taken instead", or read summarized thinking blocks. Server-side fallback does not retry these.
 - Wisp schemas carry a "reasoning scratchpad field" and agent frontmatter says "reasoning is a private scratchpad". Must be audited and reframed as `rationale`/`evidence_summary`/`actions_taken`, not "your reasoning/thinking".
9. Verbosity, format, narration [P]
 - Opus 5 longer by default; effort does not shorten visible output; prompt for length. Written deliverables also longer: "do not pad with filler sections, redundant summaries, or boilerplate".
 - Fable 5.1 formats less; "If your prompt contains anti-formatting language, remove it". Sonnet 5.5/Opus 5.5/Fable 5.1 progress text comes as thinking blocks with empty text unless display "updates". Remove "hold all findings for the final response".
 - Fable 5: "The way to keep output short is to be selective about what you include..., not to compress the writing into fragments, abbreviations, arrow chains".
10. Autonomy defaults, scope, finishing [P]
 - Sonnet 5.5 / Haiku 5.5 sample: "Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step. When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for."
 - Fable 5.1: "The user's request... sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it." Unattended: "The user is not watching in real time... asking 'Want me to…?' will block the work."
 - Opus 5.5 unattended: treat text-only end_turn as a report; keep a checklist; "stop after two or three automatic continuations on the same task rather than repeating them indefinitely". This is retry-cap guidance, consistent with Wisp's cap of 3.
 - Master: balancing autonomy/safety prompt (confirm destructive/irreversible/externally visible actions) remains.
11. Context and memory [P]
 - Master: multi-window workflows: first window sets up framework (tests.json, init.sh), later windows iterate; use JSON for structured state, free text for progress notes, git for state; "consider starting with a brand new context window rather than using compaction. Claude's latest models are extremely effective at discovering state from the local filesystem."
 - Fable 5: memory = markdown notes, "Store one lesson per file with a one-line summary at the top... delete notes that turn out to be wrong."
 - Claude Code: context is the fundamental constraint; subagents for investigation; "If you've corrected Claude more than twice on the same issue... /clear".
 - Fable 5.1 / Opus 5.5: keep history append-only; changing system/tools mid-session invalidates thinking blocks and cache. Relevant to any Wisp harness that edits prompts per phase: use a fresh agent per phase (which Wisp does).
12. Skills authoring [P] https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
 - "Default assumption: Claude is already very smart. Only add context Claude doesn't already have."
 - Degrees of freedom: low freedom (exact scripts) only for "Operations are fragile and error-prone / Consistency is critical"; high freedom for heuristics. "Narrow bridge with cliffs" vs "open field".
 - Description: third person, what + when; <=1024 chars; SKILL.md body <500 lines; references one level deep; validation feedback loops ("Run validator -> fix errors -> repeat"); plan-validate-execute with machine-verifiable intermediate files for "Batch operations, destructive changes, complex validation rules, high-stakes operations".
 - Eval-driven: "Create evaluations BEFORE writing extensive documentation", >=3 evals, "Tested with Haiku, Sonnet, and Opus". Use Claude A/Claude B iteration. Gerund names suggested (Wisp deliberately uses single lifecycle words; acceptable, doc lists noun/action forms as acceptable).
 - Template strictness: "ALWAYS use this exact template" appropriate for strict data formats; flexible otherwise.
13. Frontend / design / "AI slop" [P]
 - Master (frontend_aesthetics block): "You tend to converge toward generic, 'on distribution' outputs... 'AI slop' aesthetic"; vary fonts/themes; "You still tend to converge on common choices (Space Grotesk, for example)".
 - Opus 5.5 page: "a general instruction such as 'avoid a generic AI look' mostly swaps one default for another. It responds well to instructions that name specific patterns to avoid... Work iteratively: check which styles the first result used instead, and extend the list". Sample bans: cream/off-white background, italic accent words, numbered 01/02/03 labels, monospace labels, pill buttons.
 - Sonnet 5: "Generic instructions... tend to shift the model to a different fixed palette rather than producing variety. Two approaches work reliably: 1. Specify a concrete alternative... 2. Have the model propose options before building": "propose 4 distinct visual directions... Ask the user to pick one, then implement only that direction."
 - Blog https://www.claude.com/blog/improving-frontend-design-through-skills : four vectors (typography, themes, motion, backgrounds); avoid "low-altitude hardcoded logic like specifying exact hex codes and vague high-altitude guidance" [P via fetch summary].
 - Harness blog evaluator criteria for design: design quality, originality, craft, functionality [P, summarized].
 - Claude Design (https://support.claude.com/en/articles/14604416-get-started-with-claude-design) is linked from master page as a canvas for interactive design iteration [S: link only, page not fetched].

## C. Per-model quick table (for tiering) [P]
- Haiku 5.5: default medium, thinking on by default, 128k max_tokens, can disable thinking at <=high. low: skips search/stops early/skips checks in long agent prompts. Compare against Sonnet 5.5 at xhigh/max.
- Sonnet 5.5: default high; for agentic coding start medium (well-specified) -> high. Self-reported tendency to add tests/docs unprompted; verifies less at low.
- Opus 5.5: default medium; medium >= Opus 5 high; xhigh/max only where measured. Thinks more per turn than Opus 5 at same level. Better code review ("more bugs caught... fewer false alarms").
- Fable 5.1: default high; low is "often competitive with Claude Opus and Claude Sonnet models on cost per task while scoring higher". Strongest long-horizon; "Longer turns by default" (minutes to hours).

## D. Assessment of Wisp practices

### Still right (keep)
1. Separate scanner/recon (recall, enumerate) from adversary/gate (filter, judge). Directly backed by Sonnet 5 / Opus 5 review-harness advice and harness blog generator/evaluator split. [P]
2. Gate in a fresh context from the producer; do not self-grade. [P]
3. Schema-first JSON handoffs between agents: matches skills guidance on "verifiable intermediate outputs", "plan-validate-execute", and "Use structured formats for state data". [P] Use structured outputs where available (docs: structured outputs; Sonnet 5.5 caveat: with JSON-only output the model can only reason in thinking, so keep adaptive thinking on and effort >= high or add "Think the problem through before you answer.").
4. Retry caps on gates: Opus 5.5 "stop after two or three automatic continuations"; Claude Code Stop-hook "cap on consecutive blocks". Wisp's cap of 3 is consistent. [P]
5. Progressive loading of references (one `<load_first>`), tight SKILL.md, refs one level deep: matches skills best practices. Verify no reference-of-reference chains. [P]
6. Tier by cognitive mode, with lower effort for subagents: effort doc literally lists "such as subagents" under low. [P]
7. XML sections for separating content types and a one-line role: still endorsed. [P]
8. Abstract tool language, single actionable rule per item, no time-sensitive info: consistent with skills guidance. [P]
9. Default-fail gate with concrete criteria: matches "be concrete about where the bar is rather than qualitative terms" (Sonnet 5). [P]

### Probably unnecessary (candidates to delete, after eval)
1. Byte-identical `<constitution>` copied into every agent: pure token cost on every spawn; Fable 5 says rules/guardrails should be re-evaluated; Claude Code says prune anything where "removing this would not cause mistakes". Alternative: load shared/constitution.md only at gates, or shrink to ~10 lines and enforce the rest with validators (just check) and hooks (deterministic). Needs an ablation eval. [P-derived inference]
2. `<backstory>` persona prose: one-sentence role suffices ("Even a single sentence"). Long backstories are not endorsed anywhere; flag as probably noise. [P-derived inference]
3. Explicit "verify your work" / "double-check" steps inside agents running on Opus 5.x: documented over-verification. Keep verification as an independent gate and as deterministic commands, remove self-check chatter in producers. [P]
4. "Think step by step / think carefully" style lines and step-by-step reasoning prescriptions: replace with effort setting. [P]
5. Any "do not forget / MUST / ALWAYS" repeated emphasis; reserve for 1-2 hard invariants. [P]
6. Fixed rigid 5-part structure applied to haiku recon agents that do deterministic enumeration: small tasks may only need goal + output schema. Test. [inference]

### Potentially harmful (fix first)
1. "reasoning" scratchpad fields and any agent text that tells the model to write out its reasoning: refusal risk (`reasoning_extraction`) on Fable/Opus 5.5/Sonnet 5.5, and not retried by fallback. Rename to `rationale` / `evidence` / `actions_taken`, cap length, and never say "show your reasoning/thinking". Highest priority. [P]
2. Qualitative filtering instructions in scanners ("only report real/high-severity/confident issues") under literal following lower recall; scanner must emit everything with confidence+severity fields and let adversary/gate filter. Wisp's scanner already says "emit every matching candidate"; audit other agents. [P]
3. EARS WHEN/IF/WHILE in prose rules: not harmful per se, but docs prefer positive framing + reason. Rules written only as "never X" with no rationale generalize worse than explained rules ("Claude is smart enough to generalize from the explanation"). EARS in output contracts is fine (precise, testable). [P-derived]
4. Gate-chaining that spawns reviewer subagents from agents: Opus 5/Sonnet 5.5 spawn more readily and gates that ask "use a subagent to verify" add cost; the harness (skill orchestrator) should own spawning, agents should state "work directly unless X". Also set depth/concurrency caps. [P]
5. Reviewer-finds-something bias: "A reviewer prompted to find gaps will usually report some, even when the work is sound" (Claude Code docs) -> default-fail gate + adversary asked to find problems can manufacture blockers and loop to retry cap. Mitigate: blockers must cite falsifiable evidence and correctness/requirement impact; allow explicit "no findings" as first-class pass. [P]
6. Same prompt tuned on one model tested on none of the others: skills guidance says test on Haiku, Sonnet, Opus; effort names are not comparable across models. Pin effort per agent and re-sweep per model generation. [P]
7. Mutating the system prompt or tool list between turns of one session (per-phase injection) breaks cache and thinking blocks: keep prompts static per agent. Wisp's one-agent-per-phase design is fine; avoid orchestrator edits mid-conversation. [P]

### Tier mapping check
- Haiku/low recon: Haiku 5.5 at low skips searches/checks in long prompts, and Anthropic suggests medium as default. Recon is deterministic enumeration with short prompts, so low may be fine, but raise to medium if recon misses files; keep prompts short ("With a short system prompt, Claude Haiku 5.5 rarely stops before the work is done"). [P]
- Sonnet/medium scanners: Sonnet 5.5 recommendation for agentic multi-step tool use is medium for well-specified tasks, high for harder. Scanner is pattern matching over bounded hazard packs: medium is consistent. [P]
- Opus/high gates: Opus 5.5 medium >= Opus 5 high. A binding gate on Opus 5.5 should start at medium and sweep up; high/xhigh only where evals show gain. Cost-saving with no quality drop is plausible. Also Fable 5.1 low is "competitive with Opus/Sonnet on cost per task while scoring higher" -> test Fable for the hardest gate (architect/exit-gate). [P]
- Claude Code subagent frontmatter supports `effort`, so tiers can be encoded natively. [P]

## E. Lightweight exploratory / sketch mode: what Anthropic guidance supports
- Anthropic itself says vague prompts are fine for exploration: "Vague prompts can be useful when you're exploring and can afford to course-correct" and "Sometimes you should skip planning and let Claude figure it out because the task is exploratory" (Claude Code best practices) [P]. Plan mode "adds overhead... If you could describe the diff in one sentence, skip the plan." [P]
- Design: Sonnet 5.5 "When the user asks for ideas, options or a plan, give them that and stop. Don't start building or changing anything until they say to go ahead." Sonnet 5 design: "propose 4 distinct visual directions... Ask the user to pick one, then implement only that direction." This is the sketch pattern [P].
- Suggested shape: no schema handoffs, no gates, one agent (or none), effort low/medium, explicit output: "sketch, not spec", hard stop before implementation, a short "what I assumed / what would need a spec" list, and a promotion path that feeds into weaver:capture-need or scribe:draft-spec. Fable 5 "Navigating ambiguity... asked to determine next steps" and scope rule ("deliverable is your assessment. Report your findings and stop") fit. Do not run default-fail gates on sketches; label output non-binding. [inference grounded in P]
- Keep a cheap deterministic guard: sketch mode may not write outside a scratch dir (hook/permission), since autonomy-with-no-gate needs reversibility ("local, reversible actions"). [P]

## F. Research gaps
1. Anthropic engineering posts NOT fetched: multi-agent research system, effective context engineering, "effective harnesses for long-running agents", writing tools for agents, equipping agents with skills (only [S] via search listing). Relevant to orchestrator-worker costs and handoff formats.
2. Claude Code docs for skills/plugins/hooks/memory pages not read in full (only best-practices and subagents' first 100k chars). Plugin manifest/agent frontmatter specifics (e.g., whether plugin agents ignore hooks/permissionMode) unverified.
3. Model cards / release blog posts and "What's new" pages for Fable 5.1, Opus 5.5, Sonnet 5.5 not fetched; no benchmark numbers verified. Migration guide not read.
4. Claude Design support article not fetched; frontend-design SKILL.md at github.com/anthropics/claude-code not read (could be compared to muse).
5. No Anthropic guidance found on EARS or on rigid N-section agent prompts; statements about 5-part structure being unnecessary are inference, not Anthropic claims. Need an in-repo ablation (mason:evaluate) to decide constitution/backstory removal.
6. No primary evidence on Haiku 5.5 vs Haiku 4.5 for enumeration/recon accuracy; test needed. Structured-outputs doc not read (constraints on JSON schema features, e.g. additionalProperties, recursive schemas).
7. Third-party summaries (mindstudio, claudefa.st, explainx, oh-my-fable) surfaced in search were not read and are [U]; treat as non-authoritative.
