---
name: receive-feedback
description: >-
  Trigger when the user asks to process or triage incoming review feedback on their own PR: "address the feedback", "respond to review comments", "what do these comments mean", "triage this review". Assembles a review package (diff summary, linked spec, test results, open questions). Reviewing someone else's PR is code-review's job.
version: 3.0.0
---

# Courier — Receive Feedback

<overview>
Bundles a review package (diff summary, linked spec, test results, open questions) so the author can respond without re-reading the whole thread. The assembly is mechanical, so it runs in the primary agent and has no subagent. It does not judge the change: whether the underlying code is right is what produced the comments, so triage is the author's call, made with `${CLAUDE_PLUGIN_ROOT}/shared/references/delivery/github.md`'s vocabulary.
</overview>

<dispatch>
None. This skill runs in the primary agent. Do not delegate it.
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/references/delivery/github.md` — the Conventional Comments / Google review-label vocabulary (`praise:`/`nitpick:`/`issue:`/`suggestion:`/`question:` or `Nit:`/`Optional:`/`FYI:`) the author applies when triaging the assembled package.
</references>

<io>
**Consumes**: PR diff, optionally a linked `spec@1` or `requirement@1`, test results, incoming review comments
**Produces**: a review package: `diff_summary`, `linked_spec` (`null` when none is linked), `test_results` (counts and a summary, or "not provided"), `open_questions`. The author triages the incoming comments against it.
</io>

<workflow>
1. **Gather what exists.** Read the PR diff, the incoming comments, any linked spec or requirement, and the test results from the last run. Run the project's checks only if the user asks; otherwise report results as "not provided" and set the counts to 0.
2. **Summarize the diff** in a few lines of what changed and why, from the author's side.
3. **List open questions** the author knew about, plus questions the comments raise that the diff and spec do not answer. Do not invent any.
4. **Present the package**, then offer to draft replies. Replies are posted through `courier/post-review` after the user confirms.
</workflow>

<rules>
- Assemble only what is given or can be read; do not judge change quality and do not rank the comments.
- Never omit the linked spec field: use `null` when there is none.
</rules>
