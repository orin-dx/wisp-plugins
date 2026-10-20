#!/usr/bin/env python3
"""Claude Code hook that validates a gate subagent's handback against its verdict schema.

Spike for the deterministic-enforcement work (WP-602, WP-624); not registered by any plugin.

Why a PreToolUse hook on `SubagentHandback`: in auto mode (Claude Code 2.1.271 and later) a
subagent delivers its report through the `SubagentHandback` tool, so a `SubagentStop` hook's
`last_assistant_message` holds only the closing text. The delivered report is
`tool_input.message`. Denying the call returns the reason to the subagent, which can correct
and hand back again.

Wire it (plugin `hooks/hooks.json`), scoped so it only inspects gate agents:

  {"hooks": {"PreToolUse": [{"matcher": "SubagentHandback", "hooks": [
    {"type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/../../tools/validate-handback.py"}]}]}}

Behavior
  - Reads the hook JSON from stdin. Acts only for `agent_type` values in ROUTES (the exit-gate
    agents); every other agent passes untouched.
  - Extracts the first JSON object from `tool_input.message` (bare, fenced, or after prose) and
    validates it against the routed schema, including its conditional rules (a `pass` carries no
    blockers; a `fail` names at least one).
  - On a violation it denies the handback with the first few errors. After MAX_DENIALS denials
    for one `agent_id` it lets the handback through, so the invalid artifact reaches the
    orchestrator, which owns human escalation. This is the retry cap of 3, enforced here and
    not in a prompt.
  - Fails open: an internal error exits 1, which does not block (only exit code 2 or a deny
    decision blocks). A broken validator therefore cannot stall every subagent.

Limits recorded by the verification work: a failing or timed-out hook does not block by default
(`onFailure: "block"` needs Claude Code 2.1.295), plugin hooks fire for every subagent, and
`SubagentHandback` exists only in auto mode and for locally run, non-fork subagents.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIRECTORY = REPOSITORY_ROOT / "shared" / "schemas"
MAX_DENIALS = 3
MAX_REPORTED_ERRORS = 5

# A handback passes when it conforms to any listed schema. The muse gate documents verdict@1 but
# 35 of the 45 verdicts recorded in the pages project are verdict@3-shaped, so both are accepted
# until muse moves to verdict@3 (WP-02).
ROUTES = {
    "muse:exit-gate": ("verdict@1", "verdict@3"),
    "ranger:exit-gate": ("verdict@3",),
    "scribe:exit-gate": ("verdict@3",),
    "sentinel:exit-gate": ("verdict@3",),
    "smith:exit-gate": ("verdict@3",),
}

TYPE_CHECKS = {
    "object": lambda value: isinstance(value, dict),
    "array": lambda value: isinstance(value, list),
    "string": lambda value: isinstance(value, str),
    "boolean": lambda value: isinstance(value, bool),
    "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
    "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
    "null": lambda value: value is None,
}


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the JSON-Schema keywords the verdict schemas use. No third-party dependency."""
    expected = schema.get("type")
    allowed = [expected] if isinstance(expected, str) else expected if isinstance(expected, list) else []
    if allowed and not any(TYPE_CHECKS.get(kind, lambda value: True)(instance) for kind in allowed):
        return [f"{path}: expected {' or '.join(allowed)}"]
    errors: list[str] = []
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}")
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected {schema['const']!r}")
    if isinstance(instance, str):
        if isinstance(schema.get("minLength"), int) and len(instance) < schema["minLength"]:
            errors.append(f"{path}: expected at least {schema['minLength']} characters")
        if isinstance(schema.get("maxLength"), int) and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: expected at most {schema['maxLength']} characters")
    if isinstance(instance, int) and not isinstance(instance, bool):
        if isinstance(schema.get("minimum"), int) and instance < schema["minimum"]:
            errors.append(f"{path}: expected at least {schema['minimum']}")
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in instance:
                errors.append(f"{path}: missing required property {name!r}")
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}: unexpected property {name!r}" for name in instance if name not in properties)
        for name, value in instance.items():
            if isinstance(properties.get(name), dict):
                errors.extend(validate(value, properties[name], f"{path}.{name}"))
    if isinstance(instance, list):
        if isinstance(schema.get("minItems"), int) and len(instance) < schema["minItems"]:
            errors.append(f"{path}: expected at least {schema['minItems']} items")
        if isinstance(schema.get("maxItems"), int) and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: expected at most {schema['maxItems']} items")
        if isinstance(schema.get("items"), dict):
            for index, value in enumerate(instance):
                errors.extend(validate(value, schema["items"], f"{path}[{index}]"))
    for rule in schema.get("allOf", []):
        condition = rule.get("if")
        if isinstance(condition, dict) and not validate(instance, condition, path):
            if isinstance(rule.get("then"), dict):
                errors.extend(validate(instance, rule["then"], path))
    return errors


def extract_json_object(message: str) -> Any:
    """Return the first JSON object in a report: bare, in a code fence, or after prose."""
    decoder = json.JSONDecoder()
    candidates = [message.strip()]
    candidates.extend(match.group(1).strip() for match in re.finditer(r"```(?:json)?\s*(.*?)```", message, re.S))
    for candidate in candidates:
        try:
            value, _ = decoder.raw_decode(candidate)
            if isinstance(value, dict):
                return value
        except ValueError:
            pass
    for match in re.finditer(r"\{", message):
        try:
            value, _ = decoder.raw_decode(message[match.start():])
            if isinstance(value, dict):
                return value
        except ValueError:
            continue
    return None


def load_schema(schema_name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIRECTORY / f"{schema_name}.json").read_text(encoding="utf-8"))


def denial_count(state_directory: Path, agent_id: str) -> int:
    path = state_directory / "denials.json"
    try:
        return int(json.loads(path.read_text(encoding="utf-8")).get(agent_id, 0))
    except (OSError, ValueError):
        return 0


def record_denial(state_directory: Path, agent_id: str) -> None:
    state_directory.mkdir(parents=True, exist_ok=True)
    path = state_directory / "denials.json"
    try:
        counts = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        counts = {}
    counts[agent_id] = int(counts.get(agent_id, 0)) + 1
    path.write_text(json.dumps(counts), encoding="utf-8")


def decide(event: dict[str, Any], state_directory: Path, max_denials: int = MAX_DENIALS) -> dict[str, Any] | None:
    """Return a hook decision to deny the handback, or None to let it through."""
    if event.get("tool_name") != "SubagentHandback":
        return None
    schema_names = ROUTES.get(str(event.get("agent_type", "")))
    if schema_names is None:
        return None
    agent_id = str(event.get("agent_id", "unknown"))
    message = (event.get("tool_input") or {}).get("message", "")
    report = extract_json_object(message) if isinstance(message, str) else None
    if report is None:
        errors = ["no JSON object found in the handback"]
    else:
        results = [validate(report, load_schema(name)) for name in schema_names]
        if any(not result for result in results):
            return None
        errors = min(results, key=len)
    schema_name = " or ".join(schema_names)
    if not errors:
        return None
    if denial_count(state_directory, agent_id) >= max_denials:
        print(f"validate-handback: cap of {max_denials} denials reached for {agent_id}; passing the report on", file=sys.stderr)
        return None
    record_denial(state_directory, agent_id)
    shown = "; ".join(errors[:MAX_REPORTED_ERRORS])
    more = f" (+{len(errors) - MAX_REPORTED_ERRORS} more)" if len(errors) > MAX_REPORTED_ERRORS else ""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Your handback does not conform to {schema_name}: {shown}{more}. "
                "Correct the JSON object and hand back again."
            ),
        }
    }


def main() -> int:
    try:
        event = json.load(sys.stdin)
        state_directory = Path(os.environ.get("WISP_HANDBACK_STATE_DIR", Path(tempfile.gettempdir()) / "wisp-handback"))
        decision = decide(event, state_directory)
    except Exception as error:  # fail open: only exit code 2 or a deny decision blocks
        print(f"validate-handback: internal error, not blocking: {error}", file=sys.stderr)
        return 1
    if decision is not None:
        print(json.dumps(decision))
    return 0


if __name__ == "__main__":
    sys.exit(main())
