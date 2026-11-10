# Evidence quality convention

How to tag and weigh evidence when research, an evaluation or a decision record cites it. The aim is that a reader can tell, at a glance, how far a claim can be trusted and what would change it.

## Source tags

| Tag | Meaning |
| :-- | :-- |
| `P` | The primary page, file or dataset was read in full |
| `P*` | The primary page was read through a summarizing fetch; quotes may be paraphrased, so re-fetch before quoting in a decision record or the constitution |
| `F` | Measured or observed first-hand, with the method and the command or script that reproduces it |
| `S` | A search-result summary only; never enough to act on |
| `K` | The author's own knowledge, not fetched |
| `I` | Inference from other evidence; say which evidence |
| `U` | Unverified |

## Risk flags

Add a flag whenever one applies. A flagged claim can inform a decision but is not established by itself.

| Flag | Use when |
| :-- | :-- |
| `vendor-run` | The vendor measured its own product or published the case study |
| `self-benchmark` | A tool reports its own savings (rtk's scoreboard reported 96.2M tokens saved while the measured bill rose) |
| `small-sample` | Fewer than about 30 paired tasks, or a single task, or one run per task (state n) |
| `preprint` | Not peer reviewed, or a single author |
| `testimonial` | A customer or team quote, not a controlled measurement (the 18- and 38-hour autonomous runs) |
| `version-drift` | The number depends on a model, tool or benchmark version that has since changed; name the version |
| `volatile` | A counter or ranking that changes quickly (stars, downloads, task counts that differ between benchmark versions) |
| `stale-readme` | The claim comes from documentation that the current behavior contradicts (Caveman's 65% against its own later 3% over a control) |
| `secondhand` | Reported by someone who attended or read the primary source, with no primary available |

## Rules

1. **Cite the source and the date.** A fact without both belongs in `docs/verified-facts.md` only after it has both.
2. **Do not average flagged claims into a conclusion.** Report the range and the flags.
3. **A null result needs its power.** State the number of pairs and the effect it could detect; "no difference" on 80 tasks excludes only large effects.
4. **Prefer the measured bill and a graded outcome** to a tool's own report (`docs/evaluation-methodology.md`).
5. **Record disagreement.** When two sources conflict, keep both, name the likely reason (version, sample, definition), and mark which one the decision uses.
6. **Say what you did not read.** An unread primary source, a 403, or a page seen only as a summary belongs in the "not verified" list, not in silence.
7. **Re-verify on the trigger** in the register row, not on a calendar.
