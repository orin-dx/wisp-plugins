# Draft work packages (WP) — v0, to be extended by unmapped findings

Plugins: courier, mason, muse, navigator, ranger, scribe, sentinel, smith, vanguard, weaver (+ shared/, docs/adr, harnesses/codex).

## G0 Defects and baselines
- WP-01 Fix muse's dangling "ranger accessibility hazard taxonomy" references (plugin.json, README, SKILL.md) — either build the pack (WP-44) or correct the docs.
- WP-02 Migrate muse from verdict@1 to verdict@3 (version bump, Codex counterpart).
- WP-03 Baseline metrics script over transcripts: gate rounds per spec, blocker types (wording vs substantive), time-to-first-visual, post-gate defects, stalls/failed agent tasks, tokens/cost per phase.
- WP-04 Cross-reference link checker in `just check` / mason:audit-plugin (plugin docs referencing things that don't exist).
- WP-05 Correct/verify factual claims in repo docs touched by this evaluation (counts, tier tables).

## G1 Exploration and ideation
- WP-10 ADR(s): exploratory/divergent cognitive mode (amends ADR 003), mode routing, non-binding artifacts.
- WP-11 muse `sketch` skill: option files with stable IDs + status (open/parked/chosen/rejected) + one-line reason; anchor brief re-derived each round; ~3 options default; TBDs allowed; no gate; visibly low-fidelity marker; assumptions list; hard stop before implementation; scratch-dir-only write guard.
- WP-12 Sketch rendering medium and option matrix: local dev server/static pages, Playwright screenshots, side-by-side option boards, brand × theme × viewport matrix from tokens; Artifacts as optional; how sketches land in a repo.
- WP-13 Decision log + cross-session persistence: format, where it lives in consumer repos, surfaced through AGENTS.md routing, retrieval of prior-session decisions, "recorded but not applied" detection, rule candidates pending until human accepts (never promote a single screenshot/comment), conflict with ADR table.
- WP-14 `promote` skill: prototype/sketch → requirement@1 → spec@2; prototype/screenshots kept as visual oracle; change-delta specs; carry decision_ref; resolve TBDs or move to non_goals.
- WP-15 smith `spike` skill: validate that a tool/library/approach works in the stack; throwaway marker; skip plan/spec/mutator/reviewer/exit-gate; report verified vs unverified; smoke-check evidence recipe; promote or discard.
- WP-16 Direction-commit and anti-slop controls: propose ~4 distinct directions → user picks; named aesthetic; ban lists; rejection clauses; second-order slop patterns; taste dials (variance/motion/density); deterministic slop scanner.
- WP-17 Visual critique / design-review agent: Playwright multi-viewport critic, severity tiers (P0–P3), user-impact language with screenshots, hierarchy/contrast checks; distinct from spec audit.
- WP-18 Mode router: shape / sketch / spike / implement / review / copy / harden / promote; exploration modes read-only or sketch-only; explicit authority labeling ("cleared by"); IFR/VFR framing; ability to enter/leave gated mode explicitly.
- WP-19 Exploration → hardening handoff: characterization tests, pin behavior, hardening checklist (empty/loading/error states, a11y, copy truth, responsive), "harden" mode keeps direction and fixes state/a11y.
- WP-20 Copy/voice workflow: copy review agent/skill, case-study truth audit, voice consistency, content provenance (see WP-43).
- WP-21 Research for design (vanguard): visual/competitive sourcing, prior-art boards, keep the recon→reader→synthesizer path that worked; framing questions sharply.

## G2 Spec and visual intent
- WP-30 ADR + `spec@2`: token references `{path}`, visual references (Figma node, Storybook story id, screenshot path), per-state render references, decision_ref, supersedes links; keep falsifiable criteria; no TBD in spec (TBD only in sketch).
- WP-31 Design-intent artifact: small routed files (DESIGN.md-compatible front matter tokens + prose + Do/Don't + rejection clauses), lint/export via optional CLI, `coverage-gaps` file, exemplar good/bad PRs; component facts via lookup not monolith.
- WP-32 Ground-truth extraction step (recon): tokens, props, measured geometry from repo/running page/prototype → facts file consumed by drafter/planner/verifier; compile examples (validate); version-tied reviews.
- WP-33 Reference tables loaded before drafting: ARIA APG patterns, keyboard maps, platform a11y APIs; "never write from memory" hard rule.
- WP-34 Human-reviewable spec rendering and approval evidence: dual format (JSON + readable), rendered approval boards, "show, don't describe" before approval.
- WP-35 Optional design-source adapter: design-source@1 (figma|screenshot|html|description|none); capability-detected Figma MCP adapter (metadata first, then node), Storybook MCP, Code Connect-equivalent checks (token use, component reuse), rules-file generator.
- WP-36 Spec/plan size and stall guards: size caps, chunked writes, split specs, supersession handling and stale-spec cleanup.

## G3 Verification evidence
- WP-40 ADR + workspace-manifest@2: capability kinds browser/visual/a11y/storybook/e2e; unrendered UI is a coverage gap, never a pass; keeps ADR 005 (artifact-agnostic gate).
- WP-41 render-evidence artifact: screenshots per viewport/theme/state, axe/Lighthouse JSON, console errors, a11y-tree snapshots; baseline approval before it becomes a baseline.
- WP-42 Deterministic UI checks: token lint (hardcoded values), computed-style checks, contrast/target-size/reflow probes, landmarks, JS size budget; state that automated a11y coverage is partial.
- WP-43 Copy-provenance check: rendered text vs source copy; invented stats/names/testimonials; quoted evidence + location per finding.
- WP-44 ranger accessibility hazard pack for TSX/CSS (or removal of references, see WP-01).
- WP-45 Visual-regression + CI placement policy: Playwright/Storybook/axe in CI, behavior-vs-CSS testing policy, baseline approval, Chromatic/Percy/Lost Pixel options.
- WP-46 smith UI verification recipe: component/DOM testing, Storybook interaction/a11y tests, Playwright; mutation limits for markup/CSS; sibling review for UI.
- WP-47 UI "code intelligence" query layer (computed styles, a11y tree, token usage, component usage) extending the language-service evidence guidance (commit f10e6b8).

## G4 Gates and orchestration
- WP-50 Gate-hygiene constitution amendment: evidence-citing blockers, "no findings" is a valid pass, mechanical fixes outside the gate, convergence control for wording-only blockers, scanners report all with confidence/severity then filter separately.
- WP-51 Retry-cap enforcement with real human escalation; overrides declared and logged (no silent "owner-directed gate pass").
- WP-52 Readback in the correction loop; shared-contract-first step for sibling specs; cross-spec contradiction checks up front.
- WP-53 Standard vocabulary and fixed urgency tiers (affirm/negative/unable/standby/verify/correction/wilco/say again; P0–P3 definitions).
- WP-54 Stall/lost-contact procedures: per-agent timeouts, fallbacks, go-around, chunked writes.
- WP-55 Orchestrator owns subagent spawning; no agent spawns its own verifiers; spawn caps; file-ownership declaration in plans; single writer for shared tokens/config; merge one branch at a time; post-merge render check; ceiling 3–5 parallel agents.
- WP-56 Investigate why smith reviewer/mutator/exit-gate/recon and sentinel were never used in either project; integrate or simplify.
- WP-57 Repo-wide pre-commit gate cost during parallel smith runs: scoped checks guidance.
- WP-58 Plan quality: stale geometry, plan amendment when spec changes, challenger checks for contradictions with live code.

## G5 Prompt and agent design (model guidance)
- WP-60 mason:evaluate paired-eval harness: transcript replay first, then smoke, k=3, full; per-task medians + Wilcoxon; exclude failures from both arms; bill-based; outcome-graded; at actual effort.
- WP-61 `reasoning` field refusal test and decision (rename vs keep; 29 of 31 schemas; ADR 004 versioning).
- WP-62 Ablations of constitution/backstory/5-part skeleton (ADR 001/006).
- WP-63 Tier re-check: Haiku 5.5 recon, Opus 5.5 gates starting medium, Fable 5.1 trial, effort sweep, GPT-6 mapping.
- WP-64 Prescriptiveness audit: ration MUST/ALWAYS, explain "never X", remove "think carefully", remove qualitative filtering in producers, avoid over-verification in Opus producers, each harness component encodes an assumption.
- WP-65 Narration brevity ("be concise" for status/rationale/reports) evaluated vs baseline; not for specs/handoffs.
- WP-66 Context management: structured JSON state + progress notes + git; fresh context vs compaction; append-only history; no mid-session prompt/tool edits.
- WP-67 Skill-rule evals for the new design skills (hidden expected edits on unseen interfaces; shadcn/Vercel style).
- WP-68 Token-saver stance: paired test of rtk on the user's own workflow (optional, user config untouched).

## G6 Harness, Codex, AGENTS.md, distribution
- WP-70 Codex counterparts for every new skill/agent: outcome-first wording, boundaries, stop conditions, hierarchy, no effort `none`, TOML subagents, sandbox-enforced read-only, `just marketplace-sync`.
- WP-71 AGENTS.md strategy: short router, ≤32 KiB for Codex, one-line CLAUDE.md importing AGENTS.md, closest-file override, three layers (rules / lookup tool / AGENTS.md), constitution pointer.
- WP-72 Skills versioning and maintenance à la TanStack Intent: validate examples by compiling, review tied to source versions, mechanical repair vs judgment, CI checks that surface without auto-fixing, generate skills from source.
- WP-73 Drift: spec-drift extended to intent files, facts files and decision logs; docs freshness.
- WP-74 Lookup interface for design-system facts: CLI vs MCP, JSON over Markdown, llms.txt, component manifests.

## G7 Consumer-repo follow-ups (not plugin changes; recorded so they are not lost)
- WP-80 Add Playwright/Storybook/axe to CI, restore visual/a11y checks deferred on 13 Oct, screenshot assertions.
- WP-81 Duplicate/competing abstractions (orin vs twx packages, foundations/ui vs components, css() usage, brand branches), unported packages/rules.
- WP-82 Decision-status staleness, spec supersession cleanup, copy truth audit follow-ups, SEO checks.

## G8 Open research / verification items
- WP-90 Verify unverified claims and unread primary sources (OpenAI model pages 403, unfetched Anthropic engineering/Claude Code pages, uSpec repo, DESIGN.md agent integration docs, Figma specifics, ICAO documents).
- WP-91 Measure gate cost (tokens/time) from transcripts.
