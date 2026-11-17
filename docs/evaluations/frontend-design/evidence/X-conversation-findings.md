# X — Findings captured from the conversation (not in other notes files)

Confidence tags: [P] primary page read in full or via Playwright; [S] search summary; [K] author's own knowledge, not fetched; [U] unverified.

## U. User guidance (verbatim intent, from this session)
- U1: "the plugin workflows are too rigid for early/experimental and idea work where we might be more flexible to vibe-coded iffiness but we want to flush ideas out, see designs, validate that tools work without worrying about tests, specs, etc."
- U2: Wants to understand the work done on two brands/sites (techworx, orin-dx), how well the plugins did, and where the gaps were — for front-end work AND design ideation.
- U3: Wants industry practice: DESIGN.md, Uber uSpec, Figma + Figma MCP, Claude Design, other tools; then Shopify/Airbnb/Vercel/Atlassian/Netflix/IBM etc.; then Anthropic 5.5 and latest GPT guidance; AGENTS.md; ICAO/SID-STAR/FIS-AFIS phraseology; caveman guidance and evals; TanStack Intent.
- U4: "Let's not cut things please, why be lazy?" — nothing from the evidence may be silently dropped; every finding gets a work item or an explicit, evidence-based disposition.
- U5 (from transcripts, user's own words in the sessions): 2026-10-14 20:25 "Let's lean less on the specs and tests as we build this… two phases of work, exploratory build quick, validate ideas and iterate… Ideation like this shouldn't be so strict about specs and tests. Those come when we narrow it down… avoid regressions." Also 10-08 seo-geo "stop with these tests. It's a waste of time"; 10-14 16:49 "I said I wanted us to iterate first"; "We don't test our CSS per se… We'll worry about visual testing later"; "I need actual examples of what is being approved"; "did you lose that decision. I'm frustrated now"; "Let's stop doing the claude artifacts, we can try locally".

## UB. Uber uSpec — blog + docs fetched [P, LLM-summarized fetch]
- Blog https://www.uber.com/us/en/blog/automate-design-specs/ ; docs https://docs.uspec.design/ ; repo https://github.com/redongreen/uSpec (ownership and license NOT verified).
- Problem: Base design system, 7 stacks (UIKit, SwiftUI, Android XML/Compose, Web React, Go, SDUI); "hundreds of spec pages that all need to stay accurate"; "When those specs fall behind, engineering builds from assumptions".
- Three layers: (1) Agent Skills = domain instruction files with validation rules and reference docs, six specialized skills (Anatomy, API, Properties, Color annotation, Structure, Screen reader; Motion from After Effects); (2) Figma Console MCP, open source, local WebSocket bridge; (3) rendering layer: script populates templates in Figma.
- Pipeline per docs: Extract → Compile → Render. uSpec Extract Figma plugin captures "deterministic evidence" once; `create-component-md` interprets and validates it into a schema-valid JSON contract + concise Markdown ("Component.MD"); `create-*` skills read the generated Markdown, not Figma again ("save thousands of tokens per run").
- Deterministic extraction: token names, variant values, component structure, parent-child, variable modes, layer hierarchy. LLM: a11y semantics classification, token mapping across states, spec organization, platform behavior from provided context.
- Hallucination control: reference libraries loaded first ("the agent doesn't guess at property names — it selects from documented APIs"), structured schemas, real-data grounding, local execution.
- Human-in-the-loop: share link + optional context for non-inferrable states/platform behavior; results render in Figma for review.
- Results: screen-reader spec for 3 platforms "under 2 minutes"; months → days.
- Limits: needs well-structured Figma files, accurate tokens/variables; extract-once means initial capture must be accurate. Roadmap: drift detection, code-to-spec, new spec types.
- Runs in Cursor, Claude Code, Codex.

## UC. TanStack Intent 0.5 — https://tanstack.com/blog/intent-0.5-skills-you-can-maintain [P, summarized fetch]
- Library maintainers ship SKILL.md inside npm packages so skills version 1:1 with code. "It helps to solve the delivery problem. It doesn't, by itself, solve the maintenance problem."
- 0.5 additions: `validate` compiles fenced JS/TS examples in SKILL.md with the TypeScript compiler (missing exports, invalid options, type mismatches); `maintainer review` identifies guidance affected by source changes, tied to specific source+skill versions ("has someone checked this guidance against what changed?" not "is this file old?"); `repair --write` applies mechanical frontmatter fixes only, code changes need review; reusable GitHub checks for validation, generated-file drift, pending source reviews — surface in Actions summary, never auto-apply fixes; agent hooks use local CLI when installed. Skills "belong in the development process".

## IC. ICAO / aviation phraseology analogy [K — from author knowledge, NOT fetched; verify against ICAO Annex 10/11, Doc 4444, Doc 9432 before any normative use]
- Standard words with fixed meanings: affirm, negative, roger (received, not yes), wilco, unable, standby, say again, verify, correction, disregard; avoid "OK".
- Readback/hearback: pilot reads back safety-critical items; controller must verify and correct. A readback nobody checks is theater.
- SID/STAR: published named procedures referenced by name in the clearance; reduce workload, pre-agreed details.
- Lost-communications procedures: predefined behavior when contact is lost. Missed approach/go-around: predefined at decision altitude, not improvised.
- Pilot-in-command authority: may deviate in emergency but must declare and report afterwards.
- Urgency tiers (pan-pan/mayday) with fixed handling.
- IFR (controlled, clearance, controller responsible for separation) vs VFR with FIS/AFIS (information only, no clearances, pilot responsible); IFR can be picked up in the air and cancelled.
- Mapping proposed: sketch = VFR+FIS; promote = pick up IFR clearance; stall/timeouts = lost-comms; retry cap = missed approach; override = declared deviation; closed vocabulary + readback for gate churn. Limits: phraseology exists for noisy voice; rigidity is justified by lives at stake; needs enforcement/training; agents follow prompts so vocabulary must be short.

## CV. "Caveman" prompting — measured
- Skill: https://github.com/JuliusBrussee/caveman (~94k stars per https://enterprisedna.co/resources/ai-pulse/ai-pulse-2026-07-28-a-claude-code-skill-called-caveman-respond-in-terse-fragment/ ). Repo eval [P]: 3 arms (baseline, "Answer concisely", skill), 1 call/arm/prompt on Opus 5.5, tiktoken o200k_base output tokens, fidelity regex checks; claims 65% mean (22–87%) over 10 prompts; self-stated limits: tokenizer approximation, n=1, regex-only fidelity, no cross-model.
- Independent [P, summarized]: https://dev.to/nazecode/i-measured-the-viral-talk-like-a-caveman-token-saver-a-two-word-prompt-got-most-of-it-118a — one C# debugging task, n=3/variant: "Be concise." −28.7%, caveman −42.9%, ultra −63.6%; all correct; skill needs ~10 answers to break even vs two-word prompt.
- JetBrains [P, full page via Playwright]: https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/ (Denis Shiryaev). Harbor 0.17, Claude Code 2.1.200, claude-sonnet-5 effort low, SkillsBench 86/87 tasks, 3 runs, ~240 trials, ~$106. Arm B forced activation (ceiling). Output tokens: smoke 10 tasks k=1 −29.5%; 10 tasks k=3 −6.7%; full 86 (82 clean pairs) k=1 −8.5% (592k→542k). Quality: 64 tied, 10 skill higher, 8 lower, sign test p=0.82; mean score 0.326 vs 0.311. Cost: expected ~−10% but raw totals +11.6% ($40.60 vs $36.39) due to single task crossing 200k long-context tier ($8.29 vs $0.33). Lesson: "Never trust a k=1 eval."
- Others [S]: real coding tasks 14–21% (BetterStack); community reproductions 30–50%; agentic ~8.5%; "Be concise. Return JSON." handles ~60% of savings.
- Brevity paper [S]: arXiv 2604.00025 "Brevity Constraints Reverse Performance Hierarchies in Language Models" — 31 models, 1,485 problems; brevity improves large-model accuracy up to 26 points on some benchmarks; Concise-CoT study [S, unverified] showed GPT-3.5 −27.69% on math.

## RT. rtk (Rust Token Killer) — JetBrains test [P, full page via Playwright]
- https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/ (Part 2, Jul 20 2026). Harbor 0.18, Claude Code 2.1.201, claude-sonnet-5 at low and high effort, rtk v0.43.0 as `rtk init -g` ships (binary + PreToolUse hook + RTK.md), 425 trials, ~$320.
- Claimed −60–90%. Ceiling analysis from replay of 83 transcripts: of 1,056 shell commands, 349 rewritable, 525 no rule (python3, project scripts, loops), 182 skipped on purpose; of 1.9M chars tool output, 20% compressible, 46% shell without rule, 34% Read/Grep bypassing hook; total cap ≈3% of input.
- Measured: low effort, 80 clean pairs: cost +7.6% median (p=0.004), turns +13.8% (p=0.03), cache reads +14.3% (p=0.008), fresh input +3.2% (p=0.23), output +6.7% (ns); heavily-rewritten pairs +24% vs +5%. High effort: cost +0.1% (p=0.99). Quality: 151 paired tasks 10 better/8 worse/133 identical; sign test p=1.0 both efforts. One compatibility failure (glibc) and one broken rewrite class (compound find predicates). `rtk gain` reported 96.2M tokens saved while the bill rose: counterfactual counts raw output (1.2MB cat = 320k "saved"), chars÷4 estimate, cached re-reads at a tenth of price.
- Lessons: "a tool's self-reported savings are a claim about its counterfactual, not about your bill"; paired analysis only; per-task medians + Wilcoxon; exclude errored tasks from both arms; ladder: free transcript replay → wiring check → k=1 smoke → k=3 → full run at each effort. ~80 tasks can only rule out large effects (~700 runs/side for subtle shifts). User's global config (~/.claude/RTK.md) installs rtk with the same hook — an own-workflow paired test is an open item; do not change user config without being asked.

## NF. Netflix + JetBrains IDE intelligence — https://blog.jetbrains.com/ai/2026/10/how-netflix-made-ai-coding-agents-more-efficient/ (Oct 15 2026) [P, full page; vendor-hosted case study]
- Netflix ADP, GenAI Platform and Agentic SDLC teams plugged JetBrains' headless code-intelligence engine into Claude Code and Codex for Java/Kotlin (esp. JAR boundaries). Netflix built the daemon (keeps index warm, session manager by project root, GraalVM executable) and CLI because the LSP alone isn't callable by an agent.
- Eval: 2 codebases (internal Spring Boot 4/Gradle service; open-source DGS Framework), navigation tasks + end-to-end tasks; models Opus 5, Sonnet 5, Codex with GPT-5.6 Sol (medium/high effort); metrics tokens + time, LLM-as-judge vs reference change set for end-to-end, deterministic scoring for navigation; outlier tasks excluded from both arms; multiple runs.
- Results: typically 20–30% more efficient, up to ~65% best case (strongest model, high effort, navigation); end-to-end ~21–30%; correctness held or improved; one config's time comparison unrepresentative due to batched search. Numbers are a snapshot.
- Quote: JetBrains' Stukalov: "Agents need a code engine, not a virtual editor" — operations in terms of symbols, diagnostics, test relations, runtime behavior, not cursor positions. Netflix: "there is a benefit to having a deterministic intelligence layer alongside your agent". Netflix plans Python/TS/JS/Go.
- Repo link: commit f10e6b8 "feat(smith): add language-service evidence guidance" already points this direction.
- Not about design/front-end; does not answer Netflix design-system question (only job posting hints at a "design intelligence layer", per S2).

## PL. Repo facts verified in this session
- muse plugin.json, README.md:23, skills/component/SKILL.md:11 all point to "ranger's accessibility hazard taxonomy"; grep for "accessib" finds nothing in plugins/ranger; only shared/references/verification/interface-coverage.md mentions accessibility. [verified by grep]
- 29 of 31 shared/schemas/*.json have a "reasoning" field; all 44 agents mention reasoning/scratchpad; constitution L242 requires `reasoning: string` scratchpad in every schema. [verified by grep]
- ADR index (docs/adr/README.md): 001 four-part structure, 002 EARS output only, 003 cognitive-mode separation ("Do not combine enumeration and judgment in one agent without a new ADR"), 004 immutable schemas (new @n+1), 005 artifact-agnostic gate, 006 byte-identical constitution, 007 persona naming, 008 drop test-first, 009 implementer shape latitude, 010 Wisp Plugins brand. decision-records.md says: write an ADR only when architectural AND expensive-to-reverse/non-obvious; one-line "Do not X without a new ADR" index entry.
- Validation: `just check` = manifests test versions skills-doc reference-size marketplace-check mermaid; Codex files generated via `just marketplace-sync`; harness counterparts per shared/harness-authoring.md.

## MISC. Earlier conversation facts
- Session corpus correction: ~812 jsonl files are mostly subagent transcripts; only ~7 real top-level sessions across the projects; plugin agents used in 2 (orin-dx b8d16e96 09-29..10-03; pages 24655582 10-05..10-16) + vanguard in pages writing-candidates e8f0978b (2026-10-17).
- ~/projects/orin-dx-site holds only brand/ HTML artifacts (no git, no docs); the docs live in ~/projects/pages/docs.
