#!/usr/bin/env python3
"""Generate each plugin's Claude Code manifest from its shared plugin manifest.

Claude Code reads a plugin's manifest only from `.claude-plugin/plugin.json`. This repo's
authoritative per-plugin manifest is `plugins/<id>/plugin.json`, which also carries
repository-level fields (`id`, `consumes`, `produces`, `skills`, `agents`) that Claude Code
ignores and `claude plugin validate` reports as unknown. Validating a plugin directory
without a `.claude-plugin/plugin.json` checks nothing, so this tool writes one containing only
the fields Claude Code defines: name, version, description and author.

Usage:
  python3 tools/sync-claude-manifests.py          write the generated manifests
  python3 tools/sync-claude-manifests.py --check  fail if any generated manifest is missing or stale

Generated files are never edited by hand; change `plugins/<id>/plugin.json` and re-run.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_FIELDS = ("name", "version", "description", "author")


def expected_manifest(shared_manifest: dict) -> dict:
    missing = [field for field in CLAUDE_FIELDS if field not in shared_manifest]
    if missing:
        raise SystemExit(f"plugin manifest is missing {', '.join(missing)}")
    return {field: shared_manifest[field] for field in CLAUDE_FIELDS}


def render(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="fail on missing or stale output instead of writing")
    args = parser.parse_args()

    problems: list[str] = []
    sources = sorted(REPOSITORY_ROOT.glob("plugins/*/plugin.json"))
    if not sources:
        raise SystemExit("no plugins/*/plugin.json found")
    for source in sources:
        target = source.parent / ".claude-plugin" / "plugin.json"
        wanted = render(expected_manifest(json.loads(source.read_text(encoding="utf-8"))))
        relative = target.relative_to(REPOSITORY_ROOT).as_posix()
        if args.check:
            if not target.is_file():
                problems.append(f"{relative}: missing")
            elif target.read_text(encoding="utf-8") != wanted:
                problems.append(f"{relative}: stale")
        else:
            target.parent.mkdir(exist_ok=True)
            target.write_text(wanted, encoding="utf-8")
    if problems:
        print("FAIL: generated Claude manifests are out of date. Run: python3 tools/sync-claude-manifests.py")
        for problem in problems:
            print(f"    {problem}")
        return 1
    print(f"OK: {len(sources)} Claude manifest(s) {'match' if args.check else 'written from'} their plugin manifests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
