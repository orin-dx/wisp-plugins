# courier — Ship Tooling

**Stage:** Ship · **Output:** `release-artifact@3` · **Version:** 3.1.0

Handles everything after implementation: commit messages, PR descriptions, changeset extraction, review triage, posting a review, and release notes. Courier is not a linear pipeline — six independently-triggered skills, each dispatching to the subagent that matches the task. It reads the staged diff, linked spec, and linked requirement at runtime to produce meaningful, context-aware output, not mechanical templates.

Courier does not critique code quality or spec conformance — that's the built-in `code-review` skill and `sentinel`'s job respectively. Courier consumes their findings when relevant (e.g. `courier/post-review` can post an already-drafted `code-review` finding) rather than re-implementing them.

---

## When to Use

- You need a commit message that explains *why*, not just *what*
- You're opening a PR and want a description a reviewer with zero context can act on
- You need full context (diff, spec, tests, open questions) before responding to PR review comments
- You have an already-drafted review or reply and want it posted to GitHub
- You're cutting a release and need user-facing release notes
- You want to extract a `changeset@3` from a git diff for semantic versioning, classified from a consumer's perspective

**Invoke with:** `"Commit this"`, `"Write a commit message"`, `"Open a PR"`, `"Write the PR description"`, `"Address the feedback"`, `"Respond to review comments"`, `"Post this review"`, `"Cut a release"`, `"What's in this release"`, `"Add a changeset"`

### Use the skill, not freehand text

When a commit, a PR description or a changeset needs writing, invoke the matching skill before drafting it yourself. Each skill carries rules that freehand text skips.

| Writing | Use | Why |
| :--- | :--- | :--- |
| A commit message | `courier/commit` | Explains why, in conventional form |
| A PR title or description | `courier/pr` | Written for a reviewer with no context; reports observed verification and gaps |
| A changeset or changelog entry | `courier/changeset` | One entry per user-visible outcome, layered, with limits stated; can update an entry or recommend none |
| Release notes | `courier/release` | Aggregates changesets without rewriting them |

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/wisp-plugins
/plugin install courier
```

**AGY** — installs the full repo; see the [root README](../../README.md#install) for instructions.

**Codex** — see the [root Codex setup](../../README.md#codex), then run `codex plugin add courier@wisp-plugins`.

---

## Skills

| Skill | What it does | Subagent |
| :--- | :--- | :--- |
| `courier/commit` | Reads staged diff, produces a conventional commit message explaining the *why* | `commit-analyzer` |
| `courier/pr` | Produces a PR title and body a reviewer with zero prior context can understand, opens the PR after confirmation | `pr-narrator` |
| `courier/changeset` | Splits a diff into independent topics if it has more than one, classifies consumer_impact and semver_impact per topic, and writes a changeset whose detail scales with that classification | `changeset-analyzer` |
| `courier/receive-feedback` | Assembles the review package (diff, linked spec, test results, open questions) for feedback received on the user's own PR | `review-preprocessor` |
| `courier/post-review` | Posts an already-drafted review or reply via `gh pr review`/`gh pr comment`, gated by explicit confirmation | none — mechanical orchestration only |
| `courier/release` | Aggregates changesets since the last release; version is `max(semver_impact)` across included changesets | `release-summarizer` |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `commit-analyzer` | Commit Author | haiku / low | Reads staged diff and produces a conventional commit message explaining why, not what. |
| `changeset-analyzer` | Changeset Extractor | sonnet / medium | Classifies `consumer_impact` and `semver_impact` from a git diff per `shared/references/delivery/changesets.md`, then produces a `changeset@3` whose summary detail scales with that classification. |
| `pr-narrator` | PR Author | sonnet / medium | Writes a PR title and body from the reviewer's perspective — zero prior context assumed. |
| `review-preprocessor` | Review Package Assembler | haiku / low | Bundles the diff, linked spec, test results, and open questions into a structured review package. Does not categorize comments — that's the caller's call, made with `shared/references/delivery/github.md`'s vocabulary. |
| `release-summarizer` | Release Author | haiku / low | Aggregates `changeset@3` entries into a `release-artifact@3`, computing the version as `max(semver_impact)` and filtering `internal-only` entries. |

`courier/post-review` has no subagent — posting is mechanical execution of already-drafted content, gated by user confirmation, not a judgment task.

---

## Pipeline

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart TD
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10px,ry:10px,font-weight:600;

    Diff["Git diff"] --> Changeset["<b>changeset</b><br/>changeset-analyzer"] --> CS(["changeset@3"])
    Diff --> PR["<b>pr</b><br/>pr-narrator"] --> PROut(["PR opened"])
    CS --> Release["<b>release</b><br/>release-summarizer"] --> RelOut(["release-artifact@3"])

    Staged["Staged diff"] --> Commit["<b>commit</b><br/>commit-analyzer"] --> CommitOut(["conventional commit"])

    Comments["PR comments"] --> Receive["<b>receive-feedback</b><br/>review-preprocessor"]
    Receive -->|"review package"| Draft["Caller drafts response"] --> Post["<b>post-review</b><br/>confirmed delivery"] --> Reply(["posted reply"])

    class Diff,Staged,Comments source
    class Changeset,PR,Release,Commit,Receive,Draft,Post engine
    class CS,PROut,RelOut,CommitOut,Reply output
```

`fix code` is the one step courier doesn't do — a human or `smith` closes that gap before `courier/post-review` picks back up.

---

## Output Schemas

- `changeset@3` — see `shared/schemas/changeset@3.json` (supersedes `changeset@2`: the summary has no length cap and may be layered, and `disposition` lets the analyzer update an existing entry or recommend none)
- `release-artifact@3` — see `shared/schemas/release-artifact@3.json` (supersedes `release-artifact@1`)

---

## References

Agents read these at runtime — they are not injected at startup:

- `shared/references/delivery/commits.md` — type/scope conventions, commit message rules, voice
- `shared/references/delivery/github.md` — PR template, label conventions, review-comment vocabulary, voice
- `shared/references/delivery/changesets.md` — changeset format, consumer/semver classification tables, voice
- `shared/references/authoring/voice.md` — the full voice standard these three embed a subset of

---

## Previous Stage

Consumes smith's per-task `criteria_evidence` from **[smith](../smith/)** (aggregated across the implementation run) as the precise input to `courier/changeset`, or produces `changeset@3` directly from a staged git diff when no smith run backs the change.
