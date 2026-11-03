# Review and slop learnings: plugin improvements

Evaluation date: 2026-11-02. Status: proposal, nothing implemented. No plugin version, schema or constitution text changed.

## Verdict

Add less than first proposed. Most of what Entire's reviewer caught is plain logic bugs that no rule prevents. The rule-addressable remainder fits in four one-line additions to existing reference files. A new schema, agent, reference pack or `entire` dependency is not justified by this evidence.

## Evidence

- All Entire trail findings for `orin-dx/caliper` and `orin-dx/callisto`, pulled with `entire trail finding list` for open, resolved and dismissed: **167 changes, 37 findings** (19 open, 18 resolved, 0 dismissed). Findings exist on 7 changes (3 Caliper, 4 Callisto). Open and resolved findings were read in full.
- Transcripts of 126 sessions harvested (71 MB) but **not read in bulk**. Reading them would add volume, not signal. They stay available for targeted lookup.
- Session-level learnings from earlier lanes: Caliper `ad4b3461`, Callisto `01a16130`, `01a0e02c`, `01a0e02f-*`, `a33915af`, `15c732d1`. Callisto reported no local `entire review` runs, yet its trail has 14 findings on changes 37 to 40. The finding author was not checked. Its adversarial review (`01a16130`) came from Codex.
- Entire's reviewer had false positives: 4 Caliper findings on caliper/65 were already fixed and still show as open. Reproduce on current main before acting.
- Two projects, one author. Patterns are plausible, not proven general.

## What the 37 findings were

| Group | Count | Examples | A rule helps? |
|---|---|---|---|
| Logic and behavior bugs | 13 | `memo(forwardRef())` panic that drops a file's components; `less_precise` vs `less precise` key; substring PID filter reporting the wrong RSS; `errexit` disabled by `\|\|` leading to a duplicate comment; failure note in a job that never runs on the usual failures | No. Found by reading the diff adversarially. |
| Tests that cannot fail or leave a path untested | 7 | Asserts only `!success()` where an E-code is specified; stub ignores `--jq`, so a broken filter passes; new call has no test; `--list` path never exercised | Yes |
| Duplication, hand-copied values, hardcoded names | 5 | Helpers copied between two oracles; `report_name` hardcodes strings that exist as `Report::COMMAND`; local `stderr` helper duplicates `stderr_of` | Yes |
| Harness differs from the real consumer | 4 | Benchmark uses the NAPI default instead of the addon's `collapseInheritedProps: 'none'`; `pgrep` inside the timed loop; `sleep` inside `wall_ms`; "first 50" over 12 components | Yes |
| Docs and comments that misstate behavior | 4 | Module docstring describes the wrong scoring; stale comment on a removed field; `alias_expanded` is a text-length guess stated as fact | Yes |
| Dead code | 2 | Unused field and parameters | Weakly |
| Error swallowed or contract bent | 2 | `run_json` discards the exit code; spec now permits stray stderr before JSON | Weakly |

13 of 37 findings are logic bugs. The reviewer found them because it read each change independently, not because a rule told it what to look for. The Caliper agent did not look at the review output until the user relayed it, so the gap is that the pass was not consulted.

## Proposed changes

Each is one or two lines added to an existing file, justified by at least four findings. None adds a file, schema, agent or constitution text.

1. **Specific assertions** (7 findings). In `shared/references/verification/evidence.md`: a test for a specified error asserts that error's code or message, not only failure; a stub applies the logic it stands in for.
2. **Single source** (5 findings). In `shared/references/verification/implementation-review.md`, next to the existing sibling search: before adding a helper, string or list, check whether the codebase already defines it, and reuse it.
3. **Harness fidelity** (4 findings). In `evidence.md`: a measurement uses the consumer's configuration and times only the measured work; the report states the configuration and sample size.
4. **Claims match code** (4 findings). In `shared/references/authoring/comments.md`: a comment or doc states what the code does today; a heuristic is labeled as one.

Process, not plugin code: run the independent review pass and read its output before declaring work done. This is the largest gap in the evidence and no plugin text fixes it.

## Held back

Each needs a second source before it earns a place.

- **Failure-as-absence and projection-as-authority hazards for `ranger`.** Evidence is one Codex adversarial review on Callisto. Zero of the 37 Entire findings are this class.
- **Docs-versus-code checking in `scribe:drift-checker`.** 4 findings are doc errors, but they were caught inside a normal review. Not shown to need a new capability.
- **Judge-style consolidation, new schema, slop-review pack, `entire` dependency.** Entire's reviewer already has a judge. The plugins would duplicate it.
- **Constitution change to extend API grounding to briefs.** One Callisto incident (`redact_native_output`). Revisit on a second.
- **The 14-class sweep from the Callisto-to-Caliper prompt.** Useful as a one-off script-first audit. It is prescriptive for a plugin default, and its own rules (hotspot table, shards, verifier per finding) cost more than the 37 findings it would reproduce.

## Next step before adding anything

Audit the plugins' current instruction cost. The inventory found a constitution plus per-agent rules, schemas and hazard packs already in place, and both source projects complained about over-engineering and unrequested gates. Each addition above should displace a line, and the audit identifies which lines. Proposed as a separate evaluation using `mason:audit-plugin`'s instruction-economy check.

## Open decisions

- Approve the four one-line additions, or hold all additions until the cost audit.
- Whether to run the cost audit first.
