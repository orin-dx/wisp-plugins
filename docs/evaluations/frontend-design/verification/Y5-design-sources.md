# Y5: Primary-source verification of design-tooling claims (2026-10-17)

Method: raw files fetched with curl from raw.githubusercontent.com, registry.npmjs.org, vendor sites and read in full (cached under /Users/gabe/.claude/jobs/2d213021/tmp/y5/). WebFetch summaries were used only for directory listings. Tag [P] = read in the primary artifact. Tag [S] = secondary or conference writeup. All quotes are verbatim and 25 words or fewer.

## 0. CORRECTIONS vs R1-R4 and S1-S3 (read first)

| # | Earlier claim (file) | Verified fact | Impact |
|---|---|---|---|
| C1 | taste-skill "dials DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY" (S3) | Dials exist only in the older single-file variants. The default v2 skill: "v2 has no dials. Its direction comes from the draw and its limits from the inspector." v2 deals 3 of 20 researched directions, agent picks one, checks at 3 widths, up to 3 fix rounds. | WP-16 "taste dials" has no current precedent in the flagship skill. Replace with a direction draw plus an inspector. |
| C2 | Anthropic frontend-design "commit to extreme direction, bans Inter/Roboto/Arial, 4 pre-CSS questions" (S3, R4) | Current main SKILL.md is different: design-lead framing, a two-pass plan (4-6 named hex, type roles, layout with ASCII wireframes, principles), "review that plan against the brief" before code, five named AI-default clusters (cream #F4F1EA + terracotta #D97757 etc.), "Spend your boldness in one place", screenshot self-critique, a copywriting section. "the brief's own words always win". | WP-16 and WP-11 should cite the current text. The "extreme direction" framing is obsolete. |
| C3 | avoid-ai-design "67 deterministic patterns, exit codes" (S3) | 67 tells are in the catalog (references/ai-tells-catalog.md). `detect.mjs` implements 51 rule entries; the rest need a render. Severities are P0/P1/P2 ("who notices it": layperson, designer or developer, craft). Exit codes: 0 clean, 2 any P0 or P1, 1 error. Per-line ignore comment `avoid-ai-design-ignore: SD1`. | WP-16 scanner: only about 75% is code-certain. There is no P3. |
| C4 | Hallmark "57 slop-test gates" (S3) | README says 57; SKILL.md v1.1.0 says "58-gate" and "58 / 58". Both in the same repo. Plus 21 themes, 4 verbs, 6 cross-verb disciplines including a 1-5 pre-emit self-critique on Philosophy/Hierarchy/Execution/Specificity/Restraint/Variety (below 3 triggers revision). | Cite "57-58"; do not copy the count. |
| C5 | P0-P3 severity "from design-review agents" (WP-17 row; S3 TechNickAI) | TechNickAI design-reviewer uses Blockers / High / Medium / Nitpicks, not P-levels. The P0-P3 scheme with definitions is Vercel's product-design SKILL.md ("P0: blocks the primary task..."). | WP-17: cite Vercel for P0-P3. |
| C6 | Storybook MCP test tool `run-story-tests`, "Storybook 10.3+" (R4) | Tool is `test-run`. Full tool list is 9 tools in 3 toolsets (below). Whole feature banner: "Storybook's AI capabilities are in preview." Version gate not verified. The docs toolset needs `features.componentsManifest`. | WP-35 capability detection must key on tool names below. |
| C7 | Shopify MCP tool names (S1, brief item 14) | Current `shopify.dev/docs/api/polaris/using-mcp` lists NO tool names (config only; install via AI Toolkit). npm README for @shopify/dev-mcp 1.17.0 names `search_docs_chunks`, `validate_theme` (when `LIQUID_VALIDATION_MODE=full`) and a merged `validate` tool with an `api` enum. Older names (learn_shopify_api, introspect_graphql_schema) were not found in current docs. | Do not hard-code Shopify tool names; detect at runtime. |
| C8 | Adobe "audit rubric" is in spectrum-design-data AI docs (brief item 9) | The rubric is in React Spectrum S2's `/.well-known/skills/spectrum-audit/references/scoring-rubric.md`, not in spectrum-design-data (that page covers a design-data skill and MCP). | Source for WP-404 is react-spectrum.adobe.com. |
| C9 | Fluent "9 skills" (S2) | AGENTS.md table lists 12 skills (v9-component, headless-component, change, lint-check, token-lookup, package-info, visual-test, review-pr, triage-issues, dependabot-rollup, assign-prs, release-recovery). `visual-test` is `disable-model-invocation: true`, manual: launch per-component Storybook, `screenshot`, then Read the PNG. No baseline diff. | WP-17 manual screenshot loop is precedented; no pixel-diff precedent. |
| C10 | Primer MCP "20 tools; lint_css described as REQUIRED FINAL STEP" (S2) | primer.style MCP page lists 19 tools (init ... review_alt_text). The "CRITICAL: CALL THIS FIRST" wording is cited by Kaelig finding 4, not on the primer.style page. | Quote Kaelig as [S] for the wording. |
| C11 | Kaelig survey "20-21 systems, 187 affordances, 157 techniques, 17 MCP" (web snippet; S3) | Current: 21 systems, 6 platforms, 200 affordances, 165 techniques, data 26-28 Jul 2026, regenerated 2026-09-21. MCP: finding 1 says 18 of 21; the overview table footer says 20. Skills: 18 vs 19. The report is internally inconsistent by 1-2. | Use "about 18-20 of 21". |
| C12 | uSpec "NOT Uber-org; license unverified" (R1) | Confirmed and resolved. MIT, "Copyright (c) 2026 Ian Guisard". Repo owner is the personal account `redongreen`. Uber blog post (2026-03-11) is bylined Ian Guisard and describes uSpec as Uber's system. README itself never mentions Uber. | Treat as an Uber employee's personal MIT project. |
| C13 | uSpec skills "reference tables" only (R1) | Pipeline is much more specific. `_base.json` from a Figma plugin (Ajv schema-validated), 4 read-only extract skills (api, structure, color, voice), a reconcile step, a canonical JSON contract, then a rendered 5-section .md with Known gaps, Follow-ups, Cross-references, Provenance and a render-meta appendix. | WP-32/33: copy the template shape. |
| C14 | Atlassian "DESIGN.md ~92% more tokens" generalized (brief item 8) | 7.21M vs 3.75M (ADS MCP) tokens on one login-screen task. Atlassian: "these results should not be seen as conclusive; this blog is not a research paper." Run count and model not stated. | Never cite 92% without "one task, internal, MCP baseline". |
| C15 | Vercel "39 vs 91" (S1) | Count of known deterministic-check failures over 6 pages (3 desktop scenarios x with/without), Codex GPT-5.5 only, first attempts. Not a quality metric (below). | Use as evidence for encode-and-check, not for design quality. |
| C16 | R1 "Kiro/Spec Kit etc." and R1 DESIGN.md "lint rules 11" | 11 rules confirmed, but only `broken-ref` is an error. Contrast is a warning. Exit 1 only on errors. Four CLI commands (lint, diff, export, spec), not three. | WP-31 lint is advisory except refs. |
| C17 | Spotify first-party writeup (brief 13) | None found. All Spotify facts come from Into Design Systems posts (2026-02-22 meetup writeup; 2026-04-10 conference roundup). | Keep [S]. |

## 1. google-labs-code/design.md [P]

Repo files: README.md, PHILOSOPHY.md, docs/spec.md, examples/{atmospheric-glass,paws-and-paths,totality-festival}/{DESIGN.md,design_tokens.json,tailwind.config.js}, packages/cli/src/{commands,linter}. License: Apache-2.0. Status: alpha.

| Fact | Quote | URL |
|---|---|---|
| Purpose | "A format specification for describing a visual identity to coding agents." | https://raw.githubusercontent.com/google-labs-code/design.md/main/README.md |
| Two layers | "The tokens are the normative values. The prose provides context for how to apply them." | same |
| Front-matter keys | `version, name, description, omitted, colors, typography, rounded, spacing, components` (see section 9A) | https://raw.githubusercontent.com/google-labs-code/design.md/main/docs/spec.md |
| Reference syntax | "A token reference must be wrapped in curly braces" e.g. `{colors.primary}`; composite refs only inside `components` | spec.md |
| 8 sections, order | Overview (also Brand & Style), Colors, Typography, Layout (also Layout & Spacing), Elevation & Depth, Shapes, Components, Do's and Don'ts. "Sections can be omitted ... those present should appear in the sequence listed." | spec.md |
| Colors minimum | "At least the `primary` color palette must be defined" | spec.md |
| Component property tokens | backgroundColor, textColor, typography, rounded, padding, size, height, width. Unknown property: accepted with warning. | spec.md |
| Variants | States as sibling keys: `button-primary`, `button-primary-hover`, `button-primary-active` | spec.md |
| Unknown content | Unknown section heading: preserve. Duplicate section heading or duplicate top-level YAML key: "Error; reject the file". | spec.md |
| `omitted` | `- section: rounded` / `reason: "No rounded corners defined in brand book"` (declares intentional gaps) | spec.md |
| Lint rules (11) | error: `broken-ref`. warning: `missing-primary`, `contrast-ratio` (WCAG AA 4.5:1 on component bg/text pairs), `orphaned-tokens`, `missing-typography`, `section-order`, `unknown-key`, `token-like-ignored`. info: `token-summary`, `missing-sections`, `omitted-rules`. | README.md |
| CLI | `lint` (exit 1 on errors), `diff` (exit 1 on regression), `export --format json-tailwind \| css-tailwind \| tailwind \| dtcg` (exit 0 regardless of lint; 1 bad format; 2 unreadable), `spec [--rules] [--rules-only] [--format json]`. JSON output default; stdin via `-`. Library: `import { lint } from '@google/design.md/linter'`. | README.md |
| Agent integration | None in README or spec. The only agent-facing hook is `spec` ("useful for injecting spec context into agent prompts"). Repo `.agents/skills/` contains contributor skills (tdd, ink), not consumer skills. | README.md, tree |
| Example headings | paws-and-paths uses: Brand & Style, Colors, Typography, Layout & Spacing, Elevation & Depth, Shapes, Components (### Buttons & Inputs, Cards & Elevation, Lists & Navigation) | https://raw.githubusercontent.com/google-labs-code/design.md/main/examples/paws-and-paths/DESIGN.md |

## 2. redongreen/uSpec [P]

| Fact | Quote | URL |
|---|---|---|
| License and owner | "MIT License / Copyright (c) 2026 Ian Guisard" | https://raw.githubusercontent.com/redongreen/uSpec/main/LICENSE |
| Uber relation | Uber blog (2026-03-11), author Ian Guisard: "uSpec is an agentic system that connects an AI agent in Cursor to Figma through the open-source Figma Console MCP." Local only. | https://www.uber.com/us/en/blog/automate-design-specs/ |
| Install | `npx uspec-skills init`; works in "Cursor, Claude Code, or Codex" | README.md |
| Repo tree | skills/{create,extract}-{anatomy,api,color,component-md,motion,property,structure,voice}, firstrun; references/{anatomy,api,color,component-md,motion,property,screen-reader,structure}; figma-plugin/; packages/cli/; uspecs.config.json; docs/ | api.github.com tree |
| Contract | "`components/{componentSlug}.json` - the canonical, schema-valid machine contract" plus the sibling .md; `--view audit` gives an exhaustive `.audit.md` | https://raw.githubusercontent.com/redongreen/uSpec/main/docs/specs/component-md.mdx |
| Five sections | Overview, API, Structure, Color, Voice / Screen reader; plus "A Provenance block records the source identity and evidence coverage" | same |
| Pipeline | "The JSON contract is the machine source of truth." Prepare/validate (Ajv `_base.json`), 4 interpretation passes, reconcile typed disagreements, compile, render. Deterministic: "Given the same extraction, validated specialist caches, and render plan, contract compilation..." | https://raw.githubusercontent.com/redongreen/uSpec/main/docs/how-it-works.mdx, component-md.mdx |
| Skill structure | Orchestrator SKILL.md with a phase/token-cost table, parallel subagents "in a single batch", join-before-proceed, anti-pattern list (A2 "Type-based shortcutting", A3 "Copying child properties into the parent API"), classification table P1-P8 with a default ("default to referenced") | https://raw.githubusercontent.com/redongreen/uSpec/main/skills/create-component-md/SKILL.md |
| Reference tables | references/screen-reader/{aria,voiceover,talkback}.md. aria.md format: `| Role | Use When |` with Landmark/Widget/Structure role groups | https://raw.githubusercontent.com/redongreen/uSpec/main/references/screen-reader/aria.md |
| Template | `# {{COMPONENT_NAME}}`, Overview, Known gaps ("DEFECTS only"), Follow-ups ("NOT defects"), Cross-section invariants, API, Structure, Color, Voice, Cross-references, Provenance, render-meta appendix | https://raw.githubusercontent.com/redongreen/uSpec/main/references/component-md/component-md-template.md |
| Validation rule | "Validation error: _base.json does not match schema ... Ajv schema validation during the CLI prepare stage" | component-md.mdx |

## 3. mattpocock/skills [P] (MIT, Copyright 2026 Matt Pocock)

Layout: skills/engineering/prototype/{SKILL.md, LOGIC.md, UI.md, agents/openai.yaml}; skills/productivity/{grill-me, grilling, handoff, teach}; engineering also has research, retro, to-spec, to-tickets, implement-spec, tdd, triage, wayfinder, wizard, diagnosing-bugs.

| Fact | Quote | URL |
|---|---|---|
| Definition | "A prototype is **throwaway code that answers a question**. The question decides the shape." | https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/prototype/SKILL.md |
| Two branches | LOGIC.md ("Does this logic / state model feel right?": one shareable HTML file) vs UI.md ("What should this look like?") | SKILL.md |
| Shared rules (6) | Throwaway and marked; trivial to run (one command); no persistence by default; skip the polish; surface the state; capture it when done | SKILL.md |
| Capture | "commit it to a throwaway branch, out of main, and leave a context pointer to that branch on the implementation issue" | SKILL.md |
| UI variants | "Default to **3 variants**. More than 5 stops being radically different and starts being noise, so cap there." | https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/prototype/UI.md |
| Same-route | Variants on the existing page via `?variant=`; "strongly prefer sub-shape A"; new route only as last resort ("An empty route hides design problems") | UI.md |
| Switcher | Floating bottom bar, left/right arrows, label, keyboard arrows, hidden when `NODE_ENV === 'production'` | UI.md |
| Divergence | "Variants must be structurally different ... Three slightly-tweaked card grids isn't a UI prototype, it's wallpaper." | UI.md |
| Anti-patterns | Colour-only variants; sharing a `<Layout>`; real mutations (use stubs); promoting prototype to production | UI.md |
| grill-me | `disable-model-invocation: true`; body only: `Call the Skill tool with "grilling".` | https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/grill-me/SKILL.md |
| grilling | Design tree; ask "the whole frontier in one round: number each question and give your recommended answer"; "Word each question so 'yes' accepts your recommended answer"; facts are looked up by a sub-agent, decisions go to the user; done "when the frontier is empty" | https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/grilling/SKILL.md |

Conflict: grilling asks a batch of questions per round; Wisp's weaver rule is one question per invocation (K8). R3 said the "prototype" sits between grill-me and TDD; not stated in these files.

## 4. Anti-slop skills [P]

| Source | Fact | Quote | URL |
|---|---|---|---|
| Hallmark (Nutlope, Together AI; MIT) | Verbs, themes, gates | "twenty-one themes · four verbs"; "fifty-seven slop-test gates plus a pre-emit self-critique" (README) vs "58-gate slop test" (SKILL.md) | https://raw.githubusercontent.com/Nutlope/hallmark/main/README.md ; .../skills/hallmark/SKILL.md |
| Hallmark | Load order | slop-test.md is loaded only at step 7: "The 58 gates are a post-emit check, not a pre-emit reference." | SKILL.md |
| Hallmark | Disciplines | Honest copy ("If the user did not supply a metric, do not invent one"), locked tokens, no re-drawn chrome, mobile at 320/375/414/768, no italic headers | SKILL.md |
| avoid-ai-design (funboy322, MIT) | Scanner | "Exit code `2` when any P0 or P1 is found, `0` when clean, so it works as a CI gate." `--json`, `--min=P1`, `--rules`, `--hook` | https://raw.githubusercontent.com/funboy322/avoid-ai-design/main/README.md |
| avoid-ai-design | Rule IDs | Families SD (second-order defaults), T (type), C (color), L (layout), K (components), M (motion), I (icons), CP (copy), IM, F, plus K7 focus and M6 reduced-motion. Full list in 9C. | .../scripts/detect.mjs |
| avoid-ai-design | PostToolUse hook | `matcher: Edit|Write|MultiEdit` runs `detect.mjs --hook` so Claude sees tells in the same turn | README.md |
| avoid-ai-design | Honesty | "a tell is evidence of a default nobody chose, never proof that a model made the page" | README.md |
| taste-skill (Leonxlnx, MIT) | v2 flow | 6 steps from "a study of 247 curated sites"; "A build takes roughly 30 to 45 minutes and a few hundred thousand tokens." | https://raw.githubusercontent.com/Leonxlnx/taste-skill/main/README.md |
| taste-skill | Dials | "Both have three 1 to 10 dials ... v2 has no dials." (dials are in the experimental single-file variant) | same |
| TechNickAI design-reviewer v1.2.0 | Agent shape | Playwright; viewports 1440/768/375; touch targets under 44px; "Describe problems in terms of user impact"; tiers Blockers/High/Medium/Nitpicks; "Include screenshots"; handoff to an orchestrating LLM | https://raw.githubusercontent.com/TechNickAI/ai-coding-config/main/plugins/core/agents/design-reviewer.md |

## 5. anthropics/skills frontend-design [P]

URL: https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md (frontmatter `license: Complete terms in LICENSE.txt`).

| Fact | Quote |
|---|---|
| Brief wins | "Where the brief pins down a visual direction, follow it exactly - the brief's own words always win" |
| Named defaults | "AI-generated design right now clusters around some traits" then five numbered clusters (cream+terracotta, near-black+acid accent, broadsheet, SaaS card kit, template chrome) |
| Two passes | "Work in two passes. First, brainstorm a short design plan ... create a compact token system with color, type, layout, and principles." |
| Plan review | "review that plan against the brief before building: if any part ... reads like the generic default ... revise that part, say what you changed and why" |
| Restraint | "Spend your boldness in one place." |
| Verification | "taking screenshots to review if your environment supports it" |
| Memory | "if you have a space to quickly jot down notes about what you've tried, it can help you in future passes" |
| Copy | A "More on writing in design" section (active voice, "Save changes" not "Submit", errors never vague) |

## 6. shadcn/ui skill, MCP and evals [P]

Files: skills/shadcn/{SKILL.md, cli.md, mcp.md, design-system.md, design-system-page.md, customization.md, registry.md, rules/{styling,forms,composition,icons,chat,base-vs-radix}.md, scripts/showcase-coverage.mjs, assets/showcase/*, evals/evals.json}.

| Fact | Quote or detail | URL |
|---|---|---|
| Frontmatter | `user-invocable: false`; `allowed-tools: Bash(npx shadcn@latest *)...`; triggers include "applying a DESIGN.md or brand spec" | https://raw.githubusercontent.com/shadcn-ui/ui/main/skills/shadcn/SKILL.md |
| Context injection | Skill body embeds `npx shadcn@latest info --json` output as live project context | SKILL.md |
| Rules format | "Each links to a file with Incorrect/Correct code pairs." Critical Rules are short imperative lines naming the exact failure (e.g. "No `space-x-*` or `space-y-*`. Use `flex` with `gap-*`.") | SKILL.md |
| MCP tools (7) | get_project_registries, list_items_in_registries, search_items_in_registries, view_items_in_registries, get_item_examples_from_registries, get_add_command_for_items, get_audit_checklist. "there is no MCP equivalent" for project config (use CLI `info`). | https://raw.githubusercontent.com/shadcn-ui/ui/main/skills/shadcn/mcp.md |
| Evals | `evals/evals.json`: `{skill_name, evals[8]}`; each eval has `id, prompt, expected_output, files, expectations[]` (5-12 plain-sentence rubric items). Evals 1-5 test rules (forms, dialog, cards, chat); evals 6-8 test applying a DESIGN.md (e.g. "Implements the 2px outline focus with an offset instead of keeping the default ring"). No runner or pass thresholds in the file (runner not located). | https://raw.githubusercontent.com/shadcn-ui/ui/main/skills/shadcn/evals/evals.json |
| DESIGN.md workflow | 7 steps: scaffold, install every component, read DESIGN.md, map tokens to theme, map recipes to variants, build design system page, verify. "If the DESIGN.md path can't be read ... Don't guess its contents." | https://raw.githubusercontent.com/shadcn-ui/ui/main/skills/shadcn/design-system.md |
| Showcase page | Principles incl. "Pin states so reviewers can see them" and "Don't render every combination"; outline Foundations -> Components -> Compositions; "Turn its Do's and Don'ts into rendered do/don't pairs" | .../design-system-page.md |
| Coverage check | `showcase-coverage.mjs <ui-dir> <showcase-dir...>` lists installed components no showcase file imports (deterministic) | .../scripts/showcase-coverage.mjs |

## 7. Vercel posts [P]

### 7a. "Teaching agents product design at Vercel" (2026-06-25) https://vercel.com/blog/teaching-agents-product-design-at-vercel
| Fact | Quote or detail |
|---|---|
| Three parts | "An agent skill ... Linters that enforce clear rules automatically. A review loop that gathers evidence from Slack, Figma, and GitHub" |
| Tree | `.agents/skills/product-design/{AGENTS.md, SKILL.md, references/{product-judgment, interface-quality, resilience, surfaces, surfaces-{surface}, copy, rules, glossary, patterns, coverage-gaps}.md, exemplars/pr-{name}.md}` and `tooling/scripts/evals/{fixtures.json, rules-checklist.json, <fixture>/{before,after}}` |
| Mode list (5) | Shape, Implement, Review, Copy, Harden. "A URL, screenshot, route, or component identifies scope; it does not by itself authorize edits." |
| Decision authority (6) | User goal; verified evidence; repo-canonical guidance; accepted decisions and exemplars; adjacent shipped patterns; general heuristics |
| Severity | P0 blocks primary task or severe a11y failure; P1 likely task failure or major responsive/a11y defect; P2 meaningful friction; P3 minor craft. Each finding: "file/line or rendered location, verification status, canonical source, user consequence, and smallest concrete fix" |
| coverage-gaps.md | "coverage-gaps.md lists areas where we do not have a standard yet." |
| Rule promotion | "Add or change a rule only after current-source verification and human acceptance." "Never promote one screenshot, one shipped file, or one reviewer comment into a universal rule by itself." Destinations: "rule, reference, exemplar, lint rule, eval, coverage gap, or no change." |
| Linter vs guidance tree | "Can code identify the failure without rendering? No: use agent guidance. Yes: can the rule avoid likely false positives? ... concrete fix? Yes: use a linter." |
| Eval design | Agent edits a before state; a judge checks a rubric. "Holdouts hide their expected edits." Fixtures also run without the skill. "We score rule correctness separately from similarity to the shipped result." |
| Trigger finding | "In separate Next.js evals, agents failed to invoke an available skill in 56% of cases. Test the trigger separately from the guidance" |
| Evidence loop | Weekly: collector gathers, separate judge groups and verifies, human decides. "A collector gathers ... without proposing rules." |
| Verify | "Never claim visual verification from code alone." |
Copy rules have stable IDs: `rule/destructive-names-action ... Destructive CTAs follow Verb + Noun.` Templates for decision record and rule reference are in 9B.

### 7b. "How our agents build on-brand pages with design.md" (2026-08-31) https://vercel.com/blog/how-our-agents-build-on-brand-pages-with-design-md
| Fact | Quote or detail |
|---|---|
| Naive port failed | "every model reading it interpreted that description differently, generating vastly different pages from the same guidance" |
| 7 eval scenarios | Usage and performance report; Renewal proposal; Benchmark report; Interactive planning page; Build-versus-buy brief; Security governance brief; Presentation deck |
| Rounds | A round = fresh page from every scenario against the current file; full rounds on Claude Opus 4.8 and Codex with GPT-5.5; more than 200 runs total; local app with blind A/B comparisons; each stored run keeps prompt, inputs, model config, design.md version, screenshots, feedback |
| 3 parts | design.md (judgment), public stylesheet (bounded class and token vocabulary; "the agent never actually reads the stylesheet itself"), eval loop |
| Naming | "design.md also names the recurring generated-design patterns that we never want to see" |
| 39 vs 91 | "three desktop scenarios ... Codex with GPT-5.5 generate the page twice ... first attempt ... The pages generated with design.md had 39 of those failures. The pages generated without it had 91, which works out to 57% fewer." |
| Caveats | "The checks can only catch failures we have already seen"; "Six pages is also far too small a sample"; every page "still had at least one failure serious enough to block shipping" |
| Placement rule | "Judgment changes go into design.md as prose, reusable mechanics go into the stylesheet, and anything that we can check mechanically becomes a deterministic check in code." |
| Observable rewrite | "Let evidence tables use the full available width instead of Make the table feel less cramped" |
| Build-your-own | Pick one artifact; write a rubric; save baseline first; last ten corrections; constrain mechanics; one matched comparison with blind shuffle; encode; keep a hidden holdout; record model and guidance versions |
| Metric | Count recurrence of each complaint class over time; "When it does not [fall], something about the fix is wrong." |
Counter-point vs Atlassian: Vercel's file is judgment prose (not tokens) paired with a stylesheet; it is used for one-off pages outside repos.

## 8. Atlassian posts [P]

| Post | Facts | URL |
|---|---|---|
| DESIGN.md (2026-06-15, Kylor Hall, Andrew Campbell) | Same login-screen task; table: No context ~5% DS context, 4.20M tokens, 6m19s, 43 turns; ADS MCP ~80%, 3.75M, 5m01s, 35.1; ADS skill ~80%, 4.43M, 5m23s, 36; DESIGN.md ~30%, 7.21M, 6m46s, 45.3. Text: "~92% more tokens ... ~2.7x the variance". Model and run count not stated. "this blog is not a research paper." File is 80 KB, about 19,800 tokens; MCP and skills carry about 2.5 MB fetched on demand. DESIGN.md "was more likely to re-create components rather than use the existing system". Useful for: art direction, blue-sky prototyping, tool interoperability, customer theming. Generated from the same structured-content pipeline; non-standard properties and a separate dark-mode variant. | https://www.atlassian.com/blog/how-we-build/atlassians-design-md-is-here-what-we-learned-testing-portable-design-context-in-practice |
| Teaching AI (2026-06-02) | Structured content schemas in TypeScript generate "the ADS MCP server, the design system skill, DESIGN.md files". Vs agents without MCP: 4.9% more accurate, 11% fewer errors, 34% faster, 16% fewer tokens, 26% fewer tool calls. Self-healing docs via skills that run evals. MCP tool example `ads_plan` (named in the DESIGN.md post). | https://www.atlassian.com/blog/ai-at-work/teaching-ai-to-speak-our-design-language |
| CLI (2026-09-16) | Internal agent benchmark of real front-end tasks, auto-graded; only the fetch route changed (MCP, CLI, wrapper scripts, bundled reference files). Records pass rate, time, tokens, tool calls, kept transcripts ("a benchmark tells you whether the agent succeeded, whereas the transcript tells you whether it succeeded the way you intended"). Results: 352s to 325s (8%), 218k to 201k tokens (8%), "CLI usage surpassing MCP by 60%". npx added "more than 15 seconds of overhead"; moved to pre-installed plugin (95% less); `batch` command. Skill routes to CLI first, MCP fallback. Commands: `search`, `component`, `token`, `docs`, `batch`, `--json`. Model and run count not stated. | https://www.atlassian.com/blog/ai-at-work/giving-ai-agents-design-system-context-from-the-terminal-what-we-learned-building-a-cli |

## 9. Other vendors [P unless marked]

| Source | Fact | Quote or detail | URL |
|---|---|---|---|
| Adobe React Spectrum S2 | Skills and MCP | `npx skills add https://react-spectrum.adobe.com`; MCP `@react-spectrum/mcp@latest`; every doc page has `.md` twin and "Copy for LLM"; llms.txt | https://react-spectrum.adobe.com/ai.md |
| Adobe | Skills manifest | `/.well-known/skills/index.json` lists 3: react-spectrum-s2 (263 files), migrate-react-spectrum-v3-to-s2 (9), spectrum-audit (9: 6 check files, report-template.md, scoring-rubric.md) | https://react-spectrum.adobe.com/.well-known/skills/index.json |
| Adobe | Audit | "report-only", "The score is arithmetic over counted findings - do not estimate it." Weights Critical 10, High 5, Medium 2, Low 1; `categoryScore = 100 - min(100, sum)`; category weights Setup 25, Component usage 20, Styling 20, Accessibility 20, Versioning 10, Testing 5; grades A 90+, B 80, C 70, D 60, F below; dedupe by root cause per file:line | https://react-spectrum.adobe.com/.well-known/skills/spectrum-audit/references/scoring-rubric.md |
| Adobe spectrum-design-data | Skill vs MCP | Table: skill context cost "Description only, until invoked"; MCP "All tools loaded every session". "It does not generate component code". | https://opensource.adobe.com/spectrum-design-data/ai/ |
| Salesforce SLDS | 3 skills | design-systems-slds-validate / -apply / -slds2-migrate. "Agents can still skip an SLDS Linter step even when it's indicated as mandatory in the skill." Linter parses only HTML and CSS. | https://developer.salesforce.com/docs/platform/slds-linter/guide/get-started-linter-AI-skills.html |
| Salesforce | Scorecard | Weights: Linter 30, Theming 20, Accessibility 20, Code Quality 15, Component Usage 15; category score `100 - critical*10 - warnings*3 - info*1`; grades A/B/C/D/F at 90/80/70/60; manual gate Pass / Advisory / Blocking; "Blocking ... not ready for production, regardless of automated grade"; recommendation table (Ready / Ready with follow-ups / Needs work / Failing). Docs page formula (100 - 10E - 5W) differs from SKILL.md (100 - 10 per violation). | https://raw.githubusercontent.com/forcedotcom/sf-skills/main/skills/design-systems-slds-validate/SKILL.md |
| Microsoft Fluent | AGENTS.md | "Instructions in this file are the source of truth, not existing code." 5 Critical Rules ("Never hardcode colors, spacing, or typography values"); Legacy Anti-Patterns; architecture and workflow routing tables; quality-grades.md and tech-debt-tracker.md. | https://raw.githubusercontent.com/microsoft/fluentui/master/AGENTS.md |
| Fluent | visual-test | `disable-model-invocation: true`; per-component Storybook only; `npx -y @playwright/cli@0.1.1`; screenshot to /tmp then "View the screenshot using the Read tool"; use `snapshot` for the accessibility tree | https://raw.githubusercontent.com/microsoft/fluentui/master/.agents/skills/visual-test/SKILL.md |
| GitHub Primer | MCP page | `@primer/mcp` local stdio, 19 tools: init, list_components, get_component, get_component_examples, get_component_usage_guidelines, get_component_accessibility_guidelines, list_patterns, get_pattern, find_tokens, get_token_group_bundle, get_design_token_specs, get_token_usage_patterns, lint_css, get_color_usage, get_typography_usage, list_icons, get_icon, primer_coding_guidelines, review_alt_text | https://primer.style/product/getting-started/foundations/mcp/ |
| Spotify Encore [S] | Facts | MCP server; 3 layers (foundation, style, behavior) plus headless on React ARIA and Base UI; test framework scoring generated components on "Lint errors - Similarity scores - Visual output". Stats 220,000+ style uses and 93% satisfaction come from the conference roundup. No first-party Spotify post found. | https://www.intodesignsystems.com/blog/how-spotify-design-system-ai-ready ; https://www.intodesignsystems.com/blog/design-system-not-ready-for-ai-agents |
| Indeed [S] | JSON vs Markdown | 77 components, 8 MCP configs, 1,056 prompts; JSON "80% fewer tokens"; "JSON for MCP, Markdown for LLM" | design-system-not-ready-for-ai-agents |
| Shopify | Dev MCP | `npx -y @shopify/dev-mcp@latest` (v1.17.0, published 2026-10-16); tools named in npm README: `search_docs_chunks`, `validate_theme`, `validate` (api enum); telemetry on by default with opt-out file `~/.config/shopify-ai-toolkit/opt-out` | https://registry.npmjs.org/@shopify/dev-mcp ; https://shopify.dev/docs/api/polaris/using-mcp |
| Storybook MCP | Tools | development: stories-changed, get-storybook-story-instructions, stories-preview, stories-find-by-component, review-create. docs: docs-show, docs-show-story, docs-list. testing: test-run ("including any accessibility issues (if configured)"). Install `npx storybook add @storybook/addon-mcp`; endpoint localhost:6006/mcp. | https://storybook.js.org/docs/ai/mcp/overview |
| Playwright MCP | Snapshot vs screenshot | `browser_snapshot`: "Capture accessibility snapshot of the current page, this is better than screenshot". `browser_take_screenshot`: "You can't perform actions based on the screenshot". `--snapshot-boxes` adds `[box=x,y,width,height]` (CSS px, viewport-relative). Also browser_find, browser_resize, browser_emulate_media, browser_evaluate, browser_network_requests, browser_run_code_unsafe, browser_tabs; caps `vision, pdf, devtools`. README prefers CLI+SKILLS for coding agents: "more token-efficient". | https://raw.githubusercontent.com/microsoft/playwright-mcp/main/README.md |
| Chrome DevTools MCP | Tools | 59 tools in 11 groups. Relevant: take_snapshot, take_screenshot, emulate (colorScheme, forcedColors, cpu throttling), resize_page, get_css_styles ("authoritative and complete", cascade layers, `[overloaded]`), evaluate_script, list_console_messages, `lighthouse_audit` ("accessibility, SEO, best practices, and agentic browsing"; excludes performance; mode navigation or snapshot; device desktop or mobile), performance_start_trace, screencast_start. | https://raw.githubusercontent.com/ChromeDevTools/chrome-devtools-mcp/main/docs/tool-reference.md |
| Kaelig survey | Method and findings | Agents gathered data 26-28 Jul 2026 (researchers "Claude Opus 5", lead "Claude Fable 5"); "Every claim was checked against its primary source before publication" (self-reported); CC BY 4.0; five caveats incl. "Maturity ratings are my judgment". Findings: 18/21 official MCP; 2026 "year of the agent skill"; frontier = portable design context and published evals (Astryx: "The baseline has won 50 of 91 nights"); tool-gating beats prohibition (28 prohibition vs 22 gating techniques); best context files are compiled; validation loops make guidelines gates; skills are "a compact SKILL.md router plus lazy-loaded reference files" (Carbon 24KB SKILL.md + 12 refs). Data as JSON/MD twins with llms.txt. | https://state-of-ai-in-design-systems.netlify.app/insights.md ; https://github.com/kaelig/state-of-ai-in-design-systems |

## 10. Concrete formats worth copying verbatim

### 10A. DESIGN.md front matter (adopt as the token layer of design-intent)
```yaml
---
version: alpha
name: <string>
description: <string>            # optional
omitted:                          # optional; declares intentional gaps
  - spacing
  - section: rounded
    reason: "No rounded corners defined in brand book"
colors:      { primary: "#1A1C1E", secondary: "#6C7278", tertiary: "#B8422E", neutral: "#F7F5F2" }
typography:
  h1: { fontFamily: Public Sans, fontSize: 48px, fontWeight: 600, lineHeight: 1.1, letterSpacing: -0.02em }
rounded:     { sm: 4px, md: 8px, full: 9999px }
spacing:     { sm: 8px, md: 16px }
components:
  button-primary:       { backgroundColor: "{colors.primary-60}", textColor: "{colors.primary-20}", rounded: "{rounded.md}", padding: 12px }
  button-primary-hover: { backgroundColor: "{colors.primary-70}" }
---
```
Body: `## Overview | Colors | Typography | Layout | Elevation & Depth | Shapes | Components | Do's and Don'ts`, in that order, each unique. Do/Don't line style from spec: "Do use the primary color only for the single most important action per screen".
Gate: `npx @google/design.md lint --format json DESIGN.md` (exit 1 only on `broken-ref`), `diff` for regression, `export --format dtcg`.

### 10B. Vercel templates (adopt for decision log, rules, modes, severity)
```
SKILL modes:  Shape | Implement | Review | Copy | Harden   (resolve from the user's verb and artifact; narrowest wins)
# Decision: {name}
Status: proposed | accepted | rejected
Scope: / Decision: / Rationale: / Evidence: / Exceptions: / Bad example: / Good example: / Assumptions: / Open decisions:

# {Surface}
Load when: / Canonical owner:
## rule/{stable-id}
Scope: / Rule: / Why: / Exceptions: / Source:
## Examples  (Bad: / Good:)
## Coverage gaps
- {missing decision or evidence}

Severity: P0 blocks primary task or severe a11y failure; P1 likely task failure or major responsive/a11y defect;
          P2 meaningful friction or weak hierarchy; P3 minor craft.
Finding fields: file/line or rendered location, verification status, canonical source, user consequence, smallest concrete fix.
Promotion destination: rule | reference | exemplar | lint rule | eval | coverage gap | no change   (human approver required)
Collector prompt: "Write raw artifacts only. Do not score candidates or propose rules."
Judge prompt: "Separate verified facts, inferences, and open questions. Keep every candidate pending."
```

### 10C. avoid-ai-design rule IDs and severities (seed for a scanner reference; MIT, keep attribution)
P0: T1 Inter as primary face; C1 purple/indigo gradient; C6 gradient-filled headline text; L1 pill badge + centered hero; L2 three identical icon-topped cards; K1 untouched shadcn base theme.
P1: SD1 cream+terracotta; SD2 near-black + one acid accent; SD4 tracked ALL-CAPS labels; SD5 one word accented in headline; SD6 decorative 01/02/03; T2 "tasteful free font" cluster; T4 Geist untouched; T7 typeface declared never shipped; C2 indigo primary buttons; C9 muted text below WCAG AA; L4 round-number stat strip; L6 default page shell; L7 three tiers with "Most Popular" ring; L8 four-column footer; L9 cookie-cutter section order; K2 one radius + soft shadow everywhere; K3 glassmorphism; K4 colored side-stripe; K6 icon in tinted rounded square; K7 no visible focus; K8 default --radius; K9 default dark SaaS card; K10 stock Aceternity/Magic UI; M6 no prefers-reduced-motion; I2 emoji as icons; I3 worn Lucide / sparkle; CP1 vague aspirational headline; CP3 arrow welded to CTA; IM4 placeholder avatars; F1 generator signature.
P2: SD4m mono data labels; SD4d middle-dot meta strings; SD4w "WORD - fragment" labels; SD7 fake window dots; SD8 emerald fallback; C5 glow shadows; C8 one hue pretending to be two; K5 sparkle pill; M1 same fade-up; M4 bounce easing; M5 count-up stats; CP2 beige superlatives; CP4 tricolon slogan; CP6 generic CTA label.
Exit: 0 clean, 2 any P0/P1, 1 error. Ignore: `avoid-ai-design-ignore: SD1` / `avoid-ai-design-ignore-file: SD1, SD4`.

### 10D. Deterministic audit rubric (Adobe S2, adopt for WP-404)
severity weights Critical 10 / High 5 / Medium 2 / Low 1; `categoryScore = 100 - min(100, sum)`; weighted average; A-F at 90/80/70/60; "do not estimate it"; dedupe per root cause per file:line; N/A category scores 100 and is labelled; always show raw counts. Pair with Salesforce's separate manual gate Pass / Advisory / Blocking that overrides the grade.

### 10E. Component.MD section skeleton (uSpec; for muse spec companion or design-intent facts file)
Overview, Known gaps (defects only), Follow-ups (not defects), Cross-section invariants, API, Structure, Color, Voice / Screen reader, Cross-references, Provenance (source id, extractors, generated-by), machine appendix `render-meta`.

### 10F. mattpocock prototype rules (for sketch and spike)
Throwaway and marked; one command to run; no persistence; no polish; surface full state on every switch; capture verdict and keep the prototype on a throwaway branch. UI: 3 variants default, cap 5, structurally different, `?variant=` on the real route, dev-only switcher.

### 10G. frontend-design plan block (for muse sketch anchor brief)
Color: 4-6 named hex values. Type: faces and roles. Layout: one-sentence prose plus ASCII wireframes, with alignment. Principles. Then review against the brief; revise any default; state what changed and why.

## 11. PLAN IMPACT on CATALOG.md

| WP | Impact | Specific change |
|---|---|---|
| WP-11 sketch | Strengthen, adjust | Pocock UI.md supplies the missing numbers and shape: 3 default, cap 5, structurally different, same-route `?variant=` host preferred over a blank page. Resolves K1 for options-per-round (3, cap 5). Note Pocock keeps the full variant set on a throwaway branch, not deleted, which differs from the scratch-dir guard; decide explicitly. Add frontend-design's two-pass plan with ASCII wireframes as the anchor brief format (10G). |
| WP-15 spike | Supported | Pocock LOGIC/UI split and six shared rules (10F) match. Add a required "question answered" and captured verdict. No new dependency. |
| WP-16 direction and anti-slop | Change | Drop "taste dials" (C1: v2 has none; dials only in an experimental variant). Replace with a direction draw (taste v2: 3 of 20, agent picks) plus named-cluster ban list taken from current frontend-design (five clusters, "brief wins"). Scanner: avoid-ai-design shows 51 of 67 tells are code-certain, exit 2 on P0/P1; build ours as a small vendored list with attribution (MIT) and an ignore-comment escape. Add the honesty line: tells are evidence of unchosen defaults. |
| WP-17 visual critic | Adjust | Cite Vercel for P0-P3 with definitions and finding fields; TechNickAI for viewports 1440/768/375, 44px touch targets and user-impact wording. Fluent visual-test is a manual screenshot-and-Read loop; Playwright MCP says snapshot is better than screenshot for actions; use screenshot for judgment, snapshot (with `--snapshot-boxes`) for geometry. |
| WP-31 design-intent | Adjust | Make token layer DESIGN.md-compatible (10A) and add `omitted` with reasons as the home for coverage gaps. Evidence limits: Atlassian measured DESIGN.md at +92% tokens and ~30% context on one production task, so position it for greenfield, prototyping and theming, never as the sole source in a repo with a design system (point recon at the real components instead). Vercel's failed single-file port confirms "lookup not monolith". Spec is alpha; pin `version: alpha`. |
| WP-32 recon facts | Supported, add sources | Deterministic extraction first, LLM only for semantics (uSpec `_base.json` + Ajv). Concrete extractors: Playwright `--snapshot-boxes`, DevTools `get_css_styles`, shadcn `info --json`, Storybook manifest. Atlassian and Kaelig finding 5: generate context from one source. |
| WP-33 reference tables | Supported, ready to copy | uSpec ships the table format (`| Role | Use When |`) for ARIA, VoiceOver, TalkBack. Primer exposes `get_component_accessibility_guidelines` as a tool. License MIT, attribution needed. |
| WP-35 design-source adapter | Adjust | Use verified tool names for capability detection: Storybook (docs-list, docs-show, test-run, stories-preview ...), Primer (19 tools), shadcn (7 tools). Treat Storybook MCP as preview and the docs toolset as manifest-dependent. Do not hard-code Shopify names (C7). Skill vs MCP context cost (Adobe) favors skill-first with MCP optional. |
| WP-43 copy provenance | Supported | Hallmark discipline 2 ("do not invent one"), avoid-ai-design CP rules, frontend-design copy section, Vercel copy mode with stable-ID rules. Vercel's copywriting-eval tests copy only. |
| WP-106 brittleness guard | Supported | Vercel's rewrite test (observable, checkable wording), DESIGN.md "tokens are the normative values", Hallmark locked tokens. Route hex and px to token refs. |
| WP-402 benchmark | Redesign the method | No source gives a general none/skill/MCP/CLI/DESIGN.md result. Atlassian is one internal task set, model unstated; Vercel's 39/91 counts known failures only. Adopt: fixed scenarios, saved baseline, matched first attempts, blind A/B, version recording, transcripts read, holdout, trigger tested separately (56% skill non-invocation), metrics = tokens, time, turns, variance, pass rate. |
| WP-404 weighted rubric | Ready to specify | Two real rubrics (10D). Adopt arithmetic scoring, report-only, dedupe rule, N/A handling, plus a separate Pass/Advisory/Blocking manual gate that overrides the grade. Beware the Salesforce internal formula inconsistency. |
| WP-409 coercion catalog | Source identified | Kaelig's 165 techniques in 11 categories (CC BY 4.0, JSON twins) is the catalog to cite; key findings: tool-gating over prohibition; "name the hallucination". Do not re-derive. Add the SLDS caveat that agents skip "mandatory" steps, so pair with a hook (WP-512). |
| WP-412 promotion ladder | Adjust | Replace guidance -> exemplar -> lint -> eval with Vercel's: destinations rule | reference | exemplar | lint | eval | coverage gap | no change; add decision tree (lint only if no false positives and a concrete fix), collector/judge/human separation, "never promote one screenshot ... by itself", evidence per candidate, and a recurrence count to test that a fix worked. |
