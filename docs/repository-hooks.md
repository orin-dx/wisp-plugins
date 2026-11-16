# Hooks

Use this page to find which hook is firing, turn it off, or test it. Two kinds exist: hooks that apply only while working in `orin-dx/wisp-plugins`, and hooks the plugins ship to their users. Why each rule is a hook, and where hooks do not run, is in [`ARCHITECTURE.md` section 5](../ARCHITECTURE.md#5-hooks-and-where-they-run).

| Kind | Hook | Event | Turn off | Test |
| :--- | :--- | :--- | :--- | :--- |
| Repository | `scripts/authoring-integrity-hook.py` | `PreToolUse` on `Bash` for `git commit` (Claude Code and Codex) | Remove it from `.claude/settings.json` or `.codex/hooks.json` | `tests/test_authoring_integrity_hook.py` |
| Plugin (`wisp`) | `shared/hooks/validate-handback.py` | `PreToolUse` on `SubagentHandback` | Not switchable; fails open | `tests/test_handback_validator.py` |
| Plugin (`wisp`) | `shared/hooks/stop-check.py` | `Stop` | `WISP_STOP_CHECK=off` | `tests/test_wisp_core.py` |
| Plugin (`wisp-packs`) | `shared/hooks/pack-inject.py` | `SessionStart` | Remove the `Packs:` line from `AGENTS.md` | `tests/test_wisp_packs.py` |

Plugin hooks run only in Claude Code, are registered in `plugins/<id>/hooks/hooks.json`, and fail open. Codex has none of them and Antigravity's support is unverified. The routing guard (`route-guard.py`) is removed: `wisp` has a single entry point.

## Repository hooks

### Commit-time integrity guard

Claude and Codex run `scripts/authoring-integrity-hook.py` before a shell command that invokes `git commit`. It is silent unless it blocks a commit for one of two hard invariants:

- A tracked `shared/schemas/<name>@<version>.json` file is modified, deleted, renamed or copied instead of adding a new version.
- The generated Codex marketplace artifacts (`.agents/plugins/marketplace.json` and `dist/codex`) do not exactly match the authored Codex sources and catalog.

It does not run tests, rewrite files, add context, inspect ordinary edits or act outside this repository. It permits new schema files and reports the one corrective action when it blocks. Both harness adapters invoke the same standard-library check and accept its shared `{"decision":"block","reason":"..."}` output; they stay separate because each harness resolves project-root paths and hook configuration independently.

| Harness | Configuration | Hook command |
| :--- | :--- | :--- |
| Claude Code | `.claude/settings.json` | `PreToolUse` for `Bash` |
| Codex | `.codex/hooks.json` | `PreToolUse` for `Bash` |

To inspect or trust a hook, use `/hooks` in either harness.

## Plugin hooks

### `validate-handback.py` (`wisp`)

- **Checks:** a `wisp:verifier` handback is a valid `verdict@3`, and a fail at the second round or later carries an `escalation_required` blocker (ADR 012, 015).
- **On a violation:** denies the handback with the first few errors so the verifier can correct it. After three denials for one agent it passes the report on and the orchestrator escalates.
- **Limits:** only in auto mode, for locally run subagents. Other agents pass untouched.
- **Debug:** set `WISP_HANDBACK_TRACE` to a file path to append one JSON line per inspected event.

### `stop-check.py` (`wisp`)

- **Checks:** with uncommitted changes in a work tree, the final message contains a `Not verified:` line (any case).
- **On a miss:** blocks once and asks for the line. The next stop carries `stop_hook_active` and passes. A clean tree, or a non-git directory, passes.
- **Turn off:** `WISP_STOP_CHECK=off`.

### `pack-inject.py` (`wisp-packs`)

- **Reads:** `Packs: name, name` lines in `AGENTS.md` at the working directory, in the directories above it up to the repository root, and in directories up to four levels below it.
- **Injects:** each named pack once, as session context, within 64 files and 60,000 characters. An unknown name or a line inside a fenced code block is ignored.
- **Adopt a pack:** [`ARCHITECTURE.md` section 6](../ARCHITECTURE.md#6-packs).

## Verification

```bash
python3 -m unittest tests/test_authoring_integrity_hook.py tests/test_handback_validator.py tests/test_wisp_core.py tests/test_wisp_packs.py -v
```
