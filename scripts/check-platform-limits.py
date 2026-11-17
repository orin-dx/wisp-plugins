#!/usr/bin/env python3
"""Check authored plugin text against limits the host platforms enforce, and cross-references.

Checks (each a function taking the repository root, so tests can run it on a synthetic tree):

  cross-references   `plugin:name` and `plugin/name` mentions in plugin docs, prompts and Codex
                     skills must name an agent or skill that exists. A line that says "there is no
                     ..." or "no separate ..." is a deliberate negative statement and is skipped.
  description budget Claude Code warns when the combined name and description of all non-built-in
                     agents exceeds 15,000 tokens. This fails at 80% of that (4 characters per
                     token), so growth is caught before the warning.
  skill metadata     Agent Skills require the name to equal the directory name and the description
                     to be at most 1,024 characters (both Claude and Codex skills).
  codex budget       Codex lists skill descriptions within a budget of about 8,000 characters; this
                     fails above that and reports headroom.

Informational only (printed, never failing): frontmatter keys the host ignores at runtime
(agent `role`, skill `version`), recorded by the verification work.

Source for the limits: docs/evaluations/frontend-design/verification (Y1, Y3, Y4).

Usage: python3 scripts/check-platform-limits.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
AGENT_DESCRIPTION_BUDGET_TOKENS = 15_000
AGENT_BUDGET_FAIL_FRACTION = 0.8
CHARACTERS_PER_TOKEN = 4
SKILL_DESCRIPTION_LIMIT = 1_024
CODEX_DESCRIPTION_BUDGET_CHARACTERS = 8_000
NEGATIVE_MARKERS = ("there is no", "there's no", "no separate", "not several")


def parse_frontmatter(text: str) -> dict[str, str]:
    """Read the leading `---` block as flat keys, joining folded (`>`, `>-`, `|`) values."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    values: dict[str, str] = {}
    key: str | None = None
    for line in text[3:end].splitlines():
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match and not line.startswith(" "):
            key, value = match.group(1), match.group(2).strip()
            values[key] = "" if value in (">", ">-", "|", "|-") else value.strip("\"'")
        elif key is not None and line.strip():
            values[key] = (values[key] + " " + line.strip()).strip()
    return values


def plugin_ids(root: Path) -> list[str]:
    return sorted(path.name for path in (root / "plugins").iterdir() if path.is_dir())


def check_cross_references(root: Path) -> list[str]:
    plugins = plugin_ids(root)
    agents = {p: {a.stem for a in (root / "plugins" / p / "agents").glob("*.md")} for p in plugins}
    skills = {p: {s.parent.name for s in (root / "plugins" / p / "skills").glob("*/SKILL.md")} for p in plugins}
    names = "|".join(re.escape(p) for p in plugins)
    patterns = [
        re.compile(rf"(?<![\w/.-])({names}):([a-z][a-z-]*)\b"),
        re.compile(rf"(?<![\w/.:-])({names})/([a-z][a-z-]*)(?![\w/-]|\.\w)"),
    ]
    files = [
        *root.glob("plugins/*/README.md"),
        *root.glob("plugins/*/skills/*/SKILL.md"),
        *root.glob("plugins/*/agents/*.md"),
        *root.glob("harnesses/codex/plugins/*/skills/*/SKILL.md"),
        *(root / name for name in ("README.md", "ARCHITECTURE.md", "AGENTS.md") if (root / name).is_file()),
    ]
    failures: list[str] = []
    for path in sorted(files):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(marker in line.lower() for marker in NEGATIVE_MARKERS):
                continue
            for pattern in patterns:
                for match in pattern.finditer(line):
                    plugin, name = match.group(1), match.group(2)
                    if name == plugin or name in agents[plugin] or name in skills[plugin]:
                        continue
                    failures.append(f"{path.relative_to(root).as_posix()}:{number}: `{match.group(0)}` names no agent or skill of {plugin}")
    return failures


def agent_description_size(root: Path) -> tuple[int, int]:
    """Return (agents, characters) for the combined name and description of every agent."""
    count = characters = 0
    for path in root.glob("plugins/*/agents/*.md"):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        count += 1
        characters += len(meta.get("name", "")) + len(meta.get("description", ""))
    return count, characters


def check_description_budget(root: Path) -> tuple[list[str], str]:
    count, characters = agent_description_size(root)
    tokens = characters // CHARACTERS_PER_TOKEN
    limit = int(AGENT_DESCRIPTION_BUDGET_TOKENS * AGENT_BUDGET_FAIL_FRACTION)
    summary = (
        f"{count} agent descriptions, about {tokens} tokens of the {AGENT_DESCRIPTION_BUDGET_TOKENS}-token budget "
        f"(fails above {limit})"
    )
    failures = [f"agent descriptions total about {tokens} tokens, above {limit}: shorten descriptions or move detail into the agent body"] if tokens > limit else []
    return failures, summary


def skill_files(root: Path) -> list[Path]:
    return sorted([*root.glob("plugins/*/skills/*/SKILL.md"), *root.glob("harnesses/codex/plugins/*/skills/*/SKILL.md")])


def check_skill_metadata(root: Path) -> list[str]:
    failures = []
    for path in skill_files(root):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        relative = path.relative_to(root).as_posix()
        if not meta.get("description"):
            failures.append(f"{relative}: missing description")
        elif len(meta["description"]) > SKILL_DESCRIPTION_LIMIT:
            failures.append(f"{relative}: description is {len(meta['description'])} characters, above {SKILL_DESCRIPTION_LIMIT}")
        if meta.get("name") != path.parent.name:
            failures.append(f"{relative}: name {meta.get('name')!r} must equal its directory name {path.parent.name!r}")
    return failures


def check_codex_budget(root: Path) -> tuple[list[str], str]:
    total = sum(
        len(parse_frontmatter(path.read_text(encoding="utf-8")).get("description", ""))
        for path in root.glob("harnesses/codex/plugins/*/skills/*/SKILL.md")
    )
    summary = f"Codex skill descriptions total {total} of about {CODEX_DESCRIPTION_BUDGET_CHARACTERS} characters"
    failures = [f"Codex skill descriptions total {total} characters, above {CODEX_DESCRIPTION_BUDGET_CHARACTERS}"] if total > CODEX_DESCRIPTION_BUDGET_CHARACTERS else []
    return failures, summary


def ignored_keys(root: Path) -> list[str]:
    agents = sum(1 for path in root.glob("plugins/*/agents/*.md") if "role" in parse_frontmatter(path.read_text(encoding="utf-8")))
    skills = sum(1 for path in root.glob("plugins/*/skills/*/SKILL.md") if "version" in parse_frontmatter(path.read_text(encoding="utf-8")))
    return [f"note: `role` in {agents} agent files and `version` in {skills} skill files have no runtime effect in Claude Code"]


def main() -> int:
    root = REPOSITORY_ROOT
    problems: list[str] = []
    for title, failures in (
        ("cross-references", check_cross_references(root)),
        ("skill metadata", check_skill_metadata(root)),
    ):
        problems.extend(f"[{title}] {failure}" for failure in failures)
    budget_failures, budget_summary = check_description_budget(root)
    codex_failures, codex_summary = check_codex_budget(root)
    problems.extend(f"[description budget] {failure}" for failure in budget_failures)
    problems.extend(f"[codex budget] {failure}" for failure in codex_failures)
    print(budget_summary)
    print(codex_summary)
    for note in ignored_keys(root):
        print(note)
    if problems:
        print(f"FAIL: {len(problems)} platform-limit or cross-reference problem(s):")
        for problem in problems:
            print(f"    {problem}")
        return 1
    print("OK: cross-references resolve, skill metadata is valid, and description budgets have headroom.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
