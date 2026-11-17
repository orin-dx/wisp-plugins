# Pilots of the exploration modes

Date: 2026-10-20. Question: do the new `sketch`, `promote` and `spike` skills and the `explorer` agent behave as their instructions say when a model runs them, and do their artifacts conform to their schemas? This is a smoke pilot, not an evaluation: one run per scenario, one model, no comparison against the gated path or against ad hoc work.

## Method

Each run used `claude -p --model claude-sonnet-5-5 --plugin-dir <plugin under test> --no-session-persistence` in a throwaway project directory outside `~/.claude` (a directory under it is treated as sensitive and blocks writes), with a budget cap and `--permission-mode acceptEdits` or `auto`. The prompt was a plain request, never naming the skill. Artifacts were validated against the real schemas with `shared/hooks/validate-handback.py`. The throwaway directories were deleted afterwards, so only the numbers and findings below are kept.

## Runs

| # | Skill | Request | Result | Cost |
| :-- | :-- | :-- | :-- | :-- |
| 1 | `sketch` | "Show me some options for the hero section", brand file given, no direction | Wrote a brief with stated assumptions, proposed four distinct named directions, asked two optional questions (the skill allows three), and stopped for a pick. Did not open with the mode line | $0.14 |
| 2 | `sketch` | Same, direction chosen, inside `~/.claude` | Every write was blocked as a sensitive path; it said so, did not try another location, planned three structurally different options and ended with the skipped-gates line | $0.21 |
| 3 | `sketch` | Same, direction chosen, temporary directory | Opened with the mode line, said no render was seen, built three static pages and a board, and wrote a record that **failed the schema with 22 violations**: it could not read the schema file and followed the skill's loose prose (wrong id formats, wrong field names, missing required fields) | $0.25 |
| 4 | `sketch` | Same prompt after the record shape was added inline to the skill | Opened with the mode line, same honesty about renders, and the record **validated with zero errors** | $0.22 |
| 5 | `spike` | "Can we rely on the standard library alone for an exact Wilcoxon p-value for about 30 pairs?" | Opened with the mode line, ran real code, caught a bug in its own first version by brute-force checking, listed what was verified and what was not (including that scipy was absent), wrote only to scratch; the `spike-report@1` **validated with zero errors** | $0.18 |
| 6 | `promote` | A decided sketch fixture (valid against `option-set@1`), "promote the chosen option" | Wrote a `requirement@1` that **validated with zero errors**: eight `done_when` items including a labeled owner review of the approved render, unverified items carried forward as conditions to confirm, rejected and parked options in `out_of_scope` with their reasons quoted, the decision reason copied word for word; named the next stage without starting it | $0.15 |
| 7 | `explorer` | A delegation packet for one option | One `muse:explorer` subagent ran, built and rendered its option under the scratch path, differentiated it from the named siblings, flagged that the mobile render was captured but not viewed, and returned an `option-set@1` that **validated with zero errors** | $0.33 |

Total about $1.49.

## What changed because of the pilots

- **Schema files are not reliably readable at run time**, so each skill now carries the record or report shape inline, with the required fields and id formats (22 violations became 0 on the same prompt; one run each). The same limit applies to every existing skill that points at `shared/schemas/...`; whether the references resolve after install is WP-621.
- **The mode line** is now an explicit instruction in the first workflow step. Runs 4 and 5 opened with it; run 1 did not.
- **The board preview frames were clipped** in the page the model built, hiding the diagrams; the skill now says to make frames at least 640px tall and let the board scroll.
- **The explorer used absolute paths and the `file` kind for screenshots**; its output rules now ask for workspace-relative paths and the `screenshot` kind. This change was not re-run.

## What the pilots do not show

- One run per scenario on one model; the variation between runs is unknown.
- They ran headless, so the user's direction pick and the decision round were supplied by the prompt, not by a person choosing from the board.
- Nothing measured whether exploration is faster or produces fewer defects found later than the ad hoc work it replaces; that needs the paired design in `docs/evaluation-methodology.md`.
- The sketch pilots had no browser permission and fell back to the documented "not rendered" path; only the explorer rendered. The rendered quality of the options was seen once, on a board from run 4: three structurally different layouts with placeholder copy, with the diagram previews clipped (now addressed).
- `spike` pointed at `smith/implement` and not `muse/promote` for the next step because only the `smith` plugin was loaded.
- The Codex counterparts were not run; they are checked only by the repository's native-source tests.
