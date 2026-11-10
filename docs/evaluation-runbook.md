# Evaluation runbook

How to run the paired design in `docs/evaluation-methodology.md` on real work, for three task kinds. The question each time: does the treatment reduce turns and tokens, and does the first result need less rework? Single-run pilots and anecdotes cannot answer that. Pairs can, within the limits below.

`tools/transcript-metrics.py turns`, `agents`, `context` and `gates` measure; `tools/paired-analysis.py compare` and `agreement` analyse. `tests/test_transcript_metrics.py` (`DryRunTests`) runs this pipeline on synthetic sessions.

## Before any run

1. **Write the task list and the checklists first.** Take 6 to 10 real tasks from the backlog, each with a blinded checklist (see Scoring). Nothing is edited after the first run.
2. **Pin everything but the treatment.** Same model id, effort, repo commit, permission mode, and CLAUDE.md and memory. Record plugin versions and dates (methodology rule 10). Start each run in a fresh session from a clean checkout of the repo state.
3. **Randomize order.** Flip a coin per task for which arm runs first, so fatigue and your own learning do not fall on one arm. Run each pair on the same day.
4. **Run each arm per task once, then repeat** when you can: two to three runs, reduced to the median per task.
5. **One person drives, another scores.** The driver answers the agent's questions the same way in both arms (write the answers down on the first run and reuse them). Stop when the driver would accept the result; that is "acceptance".

## Capturing a session

The transcript is `~/.claude/projects/<encoded-project-dir>/<session-id>.jsonl` (read only; never copy it into the repo). For each finished run:

```
python3 tools/transcript-metrics.py turns --file <transcript> --trial task=T1,arm=control,run=1,score=0.7,defects=2 >> trials.jsonl
python3 tools/transcript-metrics.py context --match '<project-dir-suffix>$'
python3 tools/transcript-metrics.py agents --match '<project-dir-suffix>$'
python3 tools/transcript-metrics.py gates <directory holding <spec>-verdict[-n].json>
```

Add `gate_rounds=N` to `--trial` for the spec task and `ctx_chars=N` from `context`'s total. The `turns` fields: `prompts` (human prompts, the turns to acceptance), `turns` (assistant messages), `tool_calls`, `subagents`, `retries` (a call right after a failure, same tool, changed input; rework signal, defined in the tool docstring), `subagent_tokens` (as reported by subagents, not a bill). `context` is cumulative over the matched sessions, so match one session per run or use a dedicated project directory per arm.

Then:

```
python3 tools/paired-analysis.py compare trials.jsonl --baseline control --metrics score,prompts,turns,retries,subagent_tokens,gate_rounds
```

## Task kinds

### A. Design ideation (muse or sketch against an ad hoc session)

- **Statement**: "Explore <N=3> directions for <screen or component> in <repo>. Constraints: <list>. Stop when I can pick one."
- **Control**: plain session, no plugin, the same statement. **Treatment**: `muse:sketch` with the plugin installed.
- **Fixed**: model, effort, repo commit, design tokens and brief, the driver's selection rule (pick the option meeting the constraints; ties go to the first).
- **Primary metrics**: prompts to acceptance, `subagent_tokens`, `context` characters by origin, quality score, and whether the chosen direction survives promotion to a spec without being redone.
- **Defects found later**: constraint violations a reviewer finds in the accepted option within one week.

### B. Spec drafting and gating (gated pipeline now versus before gate hygiene)

- **Statement**: "Draft and gate a spec for <requirement>" with a requirement of fixed text.
- **Control**: the plugins at commit `50bdcf1b^` (before the gate-hygiene change), checked out in a separate worktree and loaded as the plugin source. **Treatment**: the plugins at the commit under test. Disable the installed marketplace copy in both so only one version loads, and record the commit in each trial.
- **Fixed**: requirement text, model, effort, a prewritten set of answers to clarifying questions, retry cap.
- **Primary metrics**: `gate_rounds` (from `gates`), blockers per round, `subagent_tokens` from `agents`, prompts to a passed gate, long summaries and escalations.
- **Defects found later**: criteria that a reviewer who has not seen the gate verdicts finds untestable, missing an error case or contradicting the requirement; and spec contradictions raised when the spec is implemented.

### C. Changeset and PR text (courier with layered `changeset@3` guidance versus freehand)

- **Statement**: "Write the changeset and PR description for this diff" with a stored diff (`gh pr diff <n>` saved outside the repo, or a branch to check out).
- **Control**: freehand, no courier skills, no changeset guidance in context. **Treatment**: `courier:changeset` then `courier:pr`.
- **Fixed**: diff, repo conventions file and PR template, model, effort.
- **Primary metrics**: prompts to acceptance, `retries`, tokens (`agents` plus main-thread `context`), characters of text produced, quality score.
- **Defects found later**: a release reader's questions the text did not answer, wrong semver impact, missing limits or breaking-change marks, found by someone who did not write either text.

## Scoring

A scorer who did not run the sessions scores both outputs **blind**: strip arm names, plugin names and agent-specific markers, and shuffle. The checklist is written before the first run and frozen. Each item is yes, no or not applicable, with a one-line evidence note. Score = yes / (yes + no).

```
Task: ___  Output id (shuffled): ___  Scorer: ___  Date: ___
| # | Checklist item (observable, yes or no)        | Yes/No/NA | Evidence |
| 1 | <task-specific, written before the run>        |           |          |
Defects found in later review (count, with one line each): ___
Score: ___ / ___ = ___     Would accept as-is? yes / no
```

Calibration: for task kind B and C, have a second scorer (or an LLM judge) score at least 20 items, then run `python3 tools/paired-analysis.py agreement labels.json` with `[{"a": ..., "b": ...}]`. Use an LLM judge only at kappa of about 0.6 or above (convention, not measured). Below that, score by hand.

## How many pairs, and what a null shows

- The exact Wilcoxon test cannot reach p < 0.05 with fewer than 6 non-tied pairs, whatever the effect. Run **at least 6 pairs per task kind**; aim for 10, with repeats.
- With 6 to 10 pairs only large effects (on the order of a third of turns or tokens, or most items flipping in the checklist) can reach significance. A smaller real effect will look like noise.
- **A null result shows**: no large effect on that task kind, for that model and effort, on those tasks. **It does not show**: no effect, no effect at other efforts, or no effect on other repositories. Report the pair count, the median relative change with its direction, and the better, worse and tied counts. A consistent direction across tasks at n = 8 (say 7 of 8 better) is evidence worth following up, not proof.
- Do not mix kinds. Do not drop a task because the treatment lost. A crashed task is dropped from every arm and counted.
- Tag the write-up with `small-sample` and `self-benchmark` where they apply (`docs/evidence-quality.md`).

## Results table

```
| Task kind | Pairs | Prompts (median delta) | Turns | Retries | Subagent tokens | Gate rounds | Score (better/worse/tied) | Defects later | Verdict |
| A ideation |  |  |  |  |  | n/a |  |  |  |
| B spec gate |  |  |  |  |  |  |  |  |  |
| C changeset/PR |  |  |  |  | n/a |  |  |  |
Provenance: model ___, effort ___, plugin commits ___ / ___, repo commit ___, dates ___, runs per task ___, excluded ___.
Power note and what would change the conclusion: ___
```

## Limits

Turn counts depend on how the driver answers. Subagent tokens are reported, not billed, and the main thread's tokens are not in them; `context` counts characters, not tokens, and ignores caching. Retries include legitimate progress. Treat the numbers as a comparison between arms on the same driver, not as absolute costs.
