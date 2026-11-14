#!/usr/bin/env python3
"""Claude Code hook that sends direct calls to a plugin's pipeline agents through one of its skills.

Usage (in a plugin's hooks/hooks.json): route-guard.py <plugin-id>, registered for
UserPromptSubmit and for PreToolUse with matcher "Skill|Agent|Task".

Why: sessions called pipeline agents (for example smith:reviewer) directly, so the checks their
skill runs (recon, review, mutation, the exit gate) never ran. A hook sees what a prompt cannot
enforce: a skill started with a slash command arrives as a UserPromptSubmit prompt such as
"/smith:implement", a skill the model starts arrives as a PreToolUse Skill call, and a subagent
call arrives as a PreToolUse Agent call with `subagent_type`, all with the same `session_id`.

Behavior
  - Records, per session, that a skill of this plugin started. Each fact is its own file created
    atomically, so parallel hook calls cannot lose each other's state.
  - Denies a direct call to one of this plugin's agents when none of its skills has started in the
    session, once per agent type; the reason names the skill to use. A second call goes through,
    so a deliberate direct use still works and the guard cannot deadlock a session.
  - Ignores other plugins, calls made inside a subagent, and everything when WISP_ROUTE_GUARD=off.
  - Fails open: an internal error exits 1, which does not block.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

SUGGEST = {
    "smith": "`smith:implement`, or `/guide:fix` or `/guide:build`",
    "scribe": "`scribe:draft-spec` or `scribe:gate-spec`, or `/guide:build`",
    "muse": "`muse:component` or `muse:sketch`, or `/guide:explore`",
    "navigator": "`navigator:plan`, or `/guide:build`",
    "ranger": "`ranger:audit`, or `/guide:check`",
    "sentinel": "`sentinel:gate`, or `/guide:check`",
}
COMMAND = re.compile(r"^\s*/([a-z0-9-]+):[a-z0-9-]+")


def record_path(state_directory: Path, session: str, kind: str, name: str) -> Path:
    """One empty file per fact, so concurrent hook calls never read-modify-write shared state."""
    safe = lambda value: re.sub(r"[^A-Za-z0-9_-]", "_", value) or "unknown"
    return state_directory / safe(session) / f"{kind}-{safe(name)}"


def has(path: Path) -> bool:
    return path.exists()


def mark(path: Path) -> bool:
    """Create the record; True only for the caller that created it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.touch(exist_ok=False)
    except FileExistsError:
        return False
    return True


def decide(event: dict[str, Any], plugin: str, state_directory: Path) -> dict[str, Any] | None:
    """Return a deny decision, or None to let the event through."""
    if os.environ.get("WISP_ROUTE_GUARD", "").lower() == "off":
        return None
    session = str(event.get("session_id", "unknown"))
    started = record_path(state_directory, session, "skill", plugin)
    name = event.get("hook_event_name")
    if name == "UserPromptSubmit":
        match = COMMAND.match(str(event.get("prompt", "")))
        if match and match.group(1) == plugin:
            mark(started)
        return None
    if name != "PreToolUse":
        return None
    tool_input = event.get("tool_input") or {}
    tool = event.get("tool_name")
    if tool == "Skill":
        if str(tool_input.get("skill", "")).startswith(f"{plugin}:"):
            mark(started)
        return None
    if tool not in ("Agent", "Task") or event.get("agent_id"):
        return None
    agent_type = str(tool_input.get("subagent_type", ""))
    if not agent_type.startswith(f"{plugin}:"):
        return None
    if has(started) or not mark(record_path(state_directory, session, "denied", agent_type)):
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"{agent_type} is a step inside a {plugin} skill. Start through {SUGGEST.get(plugin, f'a {plugin} skill')} "
                "so the checks it relies on run. If calling it directly is deliberate, say why and call it again."
            ),
        }
    }


def main() -> int:
    try:
        plugin = sys.argv[1]
        event = json.load(sys.stdin)
        state_directory = Path(os.environ.get("WISP_ROUTE_STATE_DIR", Path(tempfile.gettempdir()) / "wisp-route"))
        decision = decide(event, plugin, state_directory)
    except Exception as error:  # fail open: only exit code 2 or a deny decision blocks
        print(f"route-guard: internal error, not blocking: {error}", file=sys.stderr)
        return 1
    if decision is not None:
        print(json.dumps(decision))
    return 0


if __name__ == "__main__":
    sys.exit(main())
