# Evaluation methodology

How to decide whether a plugin, a skill, a prompt change or a token-saving tool actually helps. It applies to `mason:evaluate`, `claude plugin eval` and any ad hoc A/B run. The rules come from paired benchmarks of agent add-ons (the Caveman and rtk tests by JetBrains, the Netflix code-intelligence study) and from what went wrong in this repository's own sessions; the evidence is in `docs/evaluations/frontend-design/`.

## Rules

1. **Compare against a fair control.** Use at least three arms: no treatment, a plain control that gets the cheap version of the idea (for a brevity skill, "answer concisely"), and the treatment. A treatment compared only with an unconstrained baseline measures the idea, not your implementation of it.
2. **Pair by task and repeat.** Every arm runs the same tasks with the same model, effort, settings and budget. Run each task more than once; reduce repeats to a per-task median. A single run per task misleads: a first 10-task run reported a 30% token saving that fell to 8.5% at 86 tasks, and a +36% cost penalty fell to noise at three runs.
3. **Exclude a crashed task from every arm.** If a task has no successful trial in any arm, drop it from all arms and report how many were dropped. Never score a crash as zero in one arm only.
4. **Climb the ladder, cheapest first.** (a) Replay existing transcripts to bound what the idea could possibly touch, at no cost (`tools/transcript-metrics.py outputs`). (b) A one-trial wiring check that the treatment actually fires. (c) A small slice, one run. (d) The same slice with three runs. (e) The full set at each effort level you will use. Stop when a rung shows nothing.
5. **Measure the bill and the outcome, not the tool's own scoreboard.** A tool's self-reported saving is a claim about its counterfactual. rtk's scoreboard reported 96.2 million tokens saved while the measured cost went up. Use measured cost, turns and tokens, and a graded outcome.
6. **Grade outcomes mechanically where you can.** Task verifiers and hidden-oracle fixtures (`mason:evaluate`) come first. When an LLM judge is unavoidable, calibrate it: label at least 20 items by hand, run the judge on them, and report raw agreement and Cohen's kappa (`tools/paired-analysis.py agreement`). Treat a kappa below about 0.6 as a judge you cannot rely on; this threshold is a convention, not a measured result.
7. **Test at the effort you will run.** Effects reversed with effort: rtk cost +7.6% at low effort and no difference at high effort. Pin the model and effort in every arm and run each effort you intend to use.
8. **Watch the cost cliff.** A single long session can cross a long-context pricing tier and flip a total (one task billed $8.29 against $0.33). Report per-task medians and totals with and without outliers, and flag tasks above 200,000 reported tokens (`tools/transcript-metrics.py agents --cliff`).
9. **State the power.** About 80 paired tasks can only rule out large effects; catching a few-point shift needs on the order of hundreds of runs per arm. A null result is not proof of no effect. Say so in the report.
10. **Record provenance.** Model ids and versions, effort, plugin versions, source revision, the harness and its version, task set, number of runs, and the dates.

## Statistics

`tools/paired-analysis.py compare <trials> --baseline <arm>` implements rules 2, 3 and 9: per-task medians, an exact two-sided Wilcoxon signed-rank test on paired differences (normal approximation above 60 pairs), the median relative change, and for the quality score an exact two-sided sign test with the counts of better, worse and tied tasks. It reads a JSON list or JSON Lines of trials with `task`, `arm`, `run`, optional `error`, and numeric fields such as `score`, `cost`, `turns`, `tokens`.

## Which tool for which question

| Question | Use |
| :-- | :-- |
| Does a plugin change behavior against no plugin, cheaply and in CI? | `claude plugin eval`: cases run with and without the plugin; it never fails on the difference, so read the difference yourself |
| Does a workflow find defects it should, with answers hidden from the agent, across harnesses? | `mason:evaluate` with hidden-oracle fixtures |
| What could a token-saving tool possibly reach? | Transcript replay first, then the ladder above |
| Did a change make agents cost more or run longer? | `tools/transcript-metrics.py agents` before and after, then a paired run |

See `docs/evaluations/frontend-design/investigations/plugin-eval-assessment.md` for how the two evaluation tools combine and for a first suite design.

## Report template

State the question, the arms, the tasks and runs, the model and effort, how crashes were handled, the paired medians with p-values, the outcome counts, the cost with and without outliers, the power note, and what would change the conclusion.
