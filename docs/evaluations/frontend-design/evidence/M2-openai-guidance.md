# M2: OpenAI current guidance (as of 2026-10-17)
Caveat: WebFetch returns small-model summaries, not verbatim pages; "quotes" below are as returned by the fetcher. [P]=fetched, [S]=search summary, [U]=unverified.

## Model lineup
- [S] GPT-6 family: Astra (Sep 3 2026), Sol and Luna (Sep 22); GPT-6.1 Sol (Sep 29, API id gpt-6.1-sol) is Codex default. https://openai.com/index/introducing-gpt-6-sol-and-luna/ (403 on fetch), https://openai.com/index/practical-guide-building-gpt-6/ (403)
- [P] https://developers.openai.com/api/docs/guides/latest-model : model ids gpt-6-astra, gpt-6.1-sol, gpt-6-luna. "GPT-6 Astra and GPT-6.1 Sol do not support `none`; use `low` instead". Responses API for tool calling with reasoning; remove temperature/top_p/top_logprobs when reasoning active; prompt_cache_retention replaced by prompt_cache_options.ttl ("30m").
- [S] Model guide (Oct 2 2026): five-part brief: outcome, context, boundaries, definition of done, handoff. Codex: start at default effort, lower for simple, raise for deep.
- [U] Earlier GPT-5.x / 5.3-Codex / 5.5 exist (Wikipedia hits only); not read.

## Prompting (API) [P] https://developers.openai.com/api/docs/guides/prompt-guidance (fetcher summary)
- "Default to using clear, concise paragraphs... Use lists only when the information is genuinely parallel, sequential, or easier to compare"; avoid stock phrases.
- Eagerness: "When the user expresses intent to perform new work or fix an existing issue, persist until the user's intended goal is complete." Execute, don't just propose, unless clearly destructive.
- "Before asking the user clarifying questions, you should complete the work that is already authorized from context..."
- "The user's instructions take precedence over guidelines provided in a skill." Astra is more context-sensitive: state instruction hierarchy explicitly.
- "Do not write tests for reversible, low-impact changes that mirror the implementation." Broaden tests only on new failures.
- Prompting for requests like "can you..." = do the work.

## Codex docs (moved: developers.openai.com/codex/* 308-redirects to learn.chatgpt.com/docs/*)
- [P] Prompting https://learn.chatgpt.com/docs/prompting : optional blocks Goal, Context, Output, Boundaries; "a short prompt often works"; (via the-decoder [P-secondary]) "describe a process when the process itself matters. Otherwise, leave ... room to search"; "one or two hard rules to block unwanted behavior". Consumer-oriented, unified ChatGPT+Codex. https://the-decoder.com/openais-new-prompting-guide-tells-users-to-stop-overthinking-and-start-with-the-result/
- [P] AGENTS.md https://learn.chatgpt.com/docs/agent-configuration/agents-md : global ~/.codex/AGENTS.override.md or AGENTS.md, then git root -> cwd, concatenated root-down, closer overrides; cap 32 KiB (project_doc_max_bytes), stops adding past cap; fallback filenames configurable.
- [P] Subagents https://learn.chatgpt.com/docs/agent-configuration/subagents : TOML files in ~/.codex/agents/ or .codex/agents/; required name, description, developer_instructions; optional model, model_reasoning_effort (low..ultra); built-ins default/worker/explorer; agents.max_concurrent_threads_per_session; subagents inherit parent sandbox/approval and cannot override it; extra token cost.
- [P] Skills https://learn.chatgpt.com/docs/build-skills : open agent-skills standard; SKILL.md with name+description, optional scripts/references/assets; discovered from repo/user/admin/system; explicit `$skill` or implicit by description; progressive disclosure; distribute via plugins (skills + MCP + assets). "prefer instructions over scripts unless deterministic".
- [S] Sandbox/approvals https://learn.chatgpt.com/docs/agent-approvals-security : two layers, sandbox mode + approval policy; workspace-write disables network by default; cloud = isolated container, setup phase online, agent phase offline, secrets removed.
- [S] Agents SDK: April 2026 sandbox agents + model-native harness, MCP and AGENTS.md support; Responses API default; handoffs/manager patterns. (aggregator blogs; GPT-6-specific SDK guidance not found)

## Changes vs GPT-4/o-series
- Reasoning always on for Astra/Sol (no `none`); sampling params removed; Responses API required with tools+reasoning; cache API changed.
- Shift from step-by-step scripts to outcome/definition-of-done briefs; fewer, hard rules.
- Agentic by default (acts on "can you"), so restraint must be stated as boundaries.
- Skills/AGENTS.md/subagents are first-class and standardized.

## Versus Claude guidance (my inference [U-as-comparison])
- OpenAI now pushes short outcome briefs and few hard rules; Claude/Wisp style is structured XML sections and explicit contracts. OpenAI says explicit user instruction beats skill text; hierarchy should be stated.
- Codex subagents are TOML, not markdown frontmatter; sandbox not per-agent overridable (Claude agents can restrict tools per agent).

## Implications for Wisp [analysis]
Carry over: schema-first JSON handoffs (use Responses structured outputs), default-fail gates, EARS in output contracts, model/effort tiers (map to gpt-6-luna/low for recon, gpt-6.1-sol medium scanners, high/ultra for exit-gate), skills with progressive disclosure, AGENTS.md as shared constitution pointer.
Need Codex wording: avoid the 5-part rigid agent bodies bloating prompts; lead with outcome/definition of done/handoff; state stop conditions and boundaries because model is eager; state hierarchy (user > skill > agent); no `none` effort; tests-only-when-risk wording matches existing risk-based verification. AGENTS.md combined 32 KiB cap: keep constitution reference short, link not inline. Agent files: generate .codex/agents/*.toml (developer_instructions); exploration/sketch mode can use `explorer`/`worker` built-ins or a luna/low custom agent; sandbox inherited so read-only enforcement must be via parent sandbox/approval config, not agent file.
Native features to use: skills (SKILL.md, $invoke), plugins for distribution, subagents with max_concurrent_threads cap, cloud tasks for long parallel work, worktrees [U: not fetched].
Sketch mode: fits "short prompt often works"; low effort + Luna; no gate; output labelled non-binding.

## Gaps
- No primary read of GPT-6 model guide, Sol/Luna launch, system cards (403). Verify directly in a browser.
- Frontend/design/vision-in-the-loop guidance not found (frontend-guidance URL 404); cookbook not searched.
- Codex plugin manifest format, hooks, MCP config, worktrees, cloud task docs not fetched; confirm how dist/codex layout matches current .codex-plugin spec.
- Agents SDK current docs (openai.github.io/openai-agents-python) not read; preamble behaviour unconfirmed.
- Codex-tuned variant status (is there still a "-codex" model?) unverified.
- Fetcher summaries may paraphrase; re-fetch for verbatim quotes before citing in constitution.
