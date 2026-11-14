#!/usr/bin/env python3
"""Generate every copy of a plugin's version and metadata from its shared plugin manifest.

`plugins/<id>/plugin.json` is the one source for a plugin's version. From it this tool writes:

  - `plugins/<id>/.claude-plugin/plugin.json` (name, version, description, author: the only
    fields Claude Code defines; it reads a plugin's manifest only from there)
  - the plugin's entry in `marketplace.json` (version and description) and its description in
    `.claude-plugin/marketplace.json`
  - the `**Version:**` line of `plugins/<id>/README.md`
  - the `version` of `harnesses/codex/plugins/<id>/.codex-plugin/plugin.json`

The ecosystem version has no manifest of its own, so the top-level `version` in `marketplace.json`
is its source. From it the tool writes the Marketplace badge in `README.md`.

The one deliberate human edit is the CHANGELOG: it carries the release notes. Add the top
`## [x.y.z]` entry to `plugins/<id>/CHANGELOG.md` (and to `CHANGELOG.md` for the ecosystem)
to match the version you set. The tool never writes a changelog; it fails when the top entry
disagrees with the source version.

Usage:
  python3 tools/sync-claude-manifests.py          write the generated copies, then check the changelogs
  python3 tools/sync-claude-manifests.py --check  fail if any generated copy is missing or stale, or a changelog disagrees

Generated copies are never edited by hand; change the source and re-run. Run
`python3 tools/build-codex-marketplace.py` afterwards so `dist/codex/` picks up the Codex version.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_FIELDS = ("name", "version", "description", "author")
SEMVER = r"\d+\.\d+\.\d+"
# (file, entry key naming the plugin, whether the file escapes non-ASCII as it is committed)
MARKETPLACES = (
    ("marketplace.json", "id", True),
    (".claude-plugin/marketplace.json", "name", False),
)
CHANGELOG_TOP_ENTRY = re.compile(rf"^## \[({SEMVER})", re.MULTILINE)
README_VERSION_LINE = re.compile(rf"(\*\*Version:\*\* *)({SEMVER})")
CODEX_VERSION_FIELD = re.compile(rf'("version": *")({SEMVER})(")')
README_BADGE = re.compile(rf"(Marketplace[-\s]v)({SEMVER})")


def expected_manifest(shared_manifest: dict) -> dict:
    missing = [field for field in CLAUDE_FIELDS if field not in shared_manifest]
    if missing:
        raise SystemExit(f"plugin manifest is missing {', '.join(missing)}")
    return {field: shared_manifest[field] for field in CLAUDE_FIELDS}


def render(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def render_marketplace(path: Path, key: str, ascii_only: bool, plugins: dict[str, dict]) -> str:
    """The marketplace file with each plugin entry's description (and version, where the entry has one)
    taken from its plugin manifest. The top-level version is the ecosystem source and stays as authored."""
    marketplace = json.loads(path.read_text(encoding="utf-8"))
    for entry in marketplace["plugins"]:
        source = plugins.get(entry[key])
        if source is None:
            continue
        entry["description"] = source["description"]
        if "version" in entry:
            entry["version"] = source["version"]
    return json.dumps(marketplace, indent=2, ensure_ascii=ascii_only) + "\n"


def replace_version(text: str, pattern: re.Pattern[str], version: str) -> str | None:
    """`text` with the first version matched by `pattern` set to `version`, or None when nothing matches.
    Every other byte is kept, so hand-authored layout in the file survives."""
    match = pattern.search(text)
    if match is None:
        return None
    return text[: match.start(2)] + version + text[match.end(2) :]


def replace_badge(text: str, version: str) -> str | None:
    """README text with every Marketplace badge version (the image URL and its alt text) set to `version`."""
    if README_BADGE.search(text) is None:
        return None
    return README_BADGE.sub(lambda match: match.group(1) + version, text)


def changelog_problem(path: Path, version: str, label: str) -> str | None:
    if not path.is_file():
        return f"{label}: missing"
    match = CHANGELOG_TOP_ENTRY.search(path.read_text(encoding="utf-8"))
    if match is None:
        return f"{label}: no `## [x.y.z]` entry found; add `## [{version}] - <date>` with the release notes"
    if match.group(1) != version:
        return f"{label}: top entry is {match.group(1)} but the source version is {version}; edit the changelog to match"
    return None


def sync(root: Path, check: bool) -> tuple[list[str], int]:
    """Write (or, with `check`, only compare) every generated copy. Returns the problems found and the plugin count."""
    problems: list[str] = []

    def emit(path: Path, wanted: str | None, problem_when_missing: str, stale: str) -> None:
        relative = path.relative_to(root).as_posix()
        if wanted is None:
            problems.append(f"{relative}: {problem_when_missing}")
        elif check:
            if not path.is_file():
                problems.append(f"{relative}: missing")
            elif path.read_text(encoding="utf-8") != wanted:
                problems.append(f"{relative}: {stale}")
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(wanted, encoding="utf-8")

    sources = sorted(root.glob("plugins/*/plugin.json"))
    if not sources:
        raise SystemExit("no plugins/*/plugin.json found")
    plugins = {source.parent.name: json.loads(source.read_text(encoding="utf-8")) for source in sources}
    for plugin_id, manifest in plugins.items():
        if not re.fullmatch(SEMVER, str(manifest.get("version", ""))):
            raise SystemExit(f"plugins/{plugin_id}/plugin.json: version must be x.y.z, found {manifest.get('version')!r}")

    for relative, key, ascii_only in MARKETPLACES:
        path = root / relative
        emit(path, render_marketplace(path, key, ascii_only, plugins), "unreadable", "plugin descriptions or versions are stale")

    for source in sources:
        plugin_dir = source.parent
        manifest = plugins[plugin_dir.name]
        version = manifest["version"]
        emit(plugin_dir / ".claude-plugin" / "plugin.json", render(expected_manifest(manifest)), "unreadable", "stale")

        readme = plugin_dir / "README.md"
        wanted = replace_version(readme.read_text(encoding="utf-8"), README_VERSION_LINE, version) if readme.is_file() else None
        emit(readme, wanted, "no `**Version:**` line found", f"`**Version:**` is not {version}")

        codex = root / "harnesses" / "codex" / "plugins" / plugin_dir.name / ".codex-plugin" / "plugin.json"
        if codex.is_file():
            wanted = replace_version(codex.read_text(encoding="utf-8"), CODEX_VERSION_FIELD, version)
            emit(codex, wanted, "no `version` field found", f"version is not {version}")
        else:
            problems.append(f"{codex.relative_to(root).as_posix()}: missing")

        found = changelog_problem(plugin_dir / "CHANGELOG.md", version, f"plugins/{plugin_dir.name}/CHANGELOG.md")
        if found:
            problems.append(found)

    ecosystem_version = json.loads((root / "marketplace.json").read_text(encoding="utf-8")).get("version")
    if not re.fullmatch(SEMVER, str(ecosystem_version)):
        raise SystemExit(f"marketplace.json: top-level version must be x.y.z, found {ecosystem_version!r}")
    readme = root / "README.md"
    wanted = replace_badge(readme.read_text(encoding="utf-8"), ecosystem_version)
    emit(readme, wanted, "no Marketplace version badge found", f"Marketplace badge is not v{ecosystem_version}")
    found = changelog_problem(root / "CHANGELOG.md", ecosystem_version, "CHANGELOG.md")
    if found:
        problems.append(found)
    return problems, len(sources)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="fail on missing, stale or disagreeing output instead of writing")
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    problems, count = sync(args.root.resolve(), args.check)
    if problems:
        print("FAIL: versions and generated manifests disagree with their sources. Run: python3 tools/sync-claude-manifests.py")
        print("      (a changelog line below is the one hand edit: add or fix the top entry yourself)")
        for problem in problems:
            print(f"    {problem}")
        return 1
    print(
        f"OK: {count} plugin(s) and the ecosystem: versions {'match' if args.check else 'written from'} "
        "their sources and every top changelog entry agrees."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
