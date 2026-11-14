"""Enforce concern-first shared references, valid paths, and runtime callers."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = REPOSITORY_ROOT / "shared/references"
REFERENCE_PATH = re.compile(r"shared/references/[A-Za-z0-9@._/-]+\.md")
SCHEMA_PATH = re.compile(r"shared/schemas/[A-Za-z0-9@._/-]+\.json")
SHARED_FILE_PATH = re.compile(r"shared/(?:constitution|harness-authoring|agent-best-practices)\.md")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s+(\S+)", re.MULTILINE)
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
RETIRED_REFERENCE_NAME = re.compile(
    r"(?:\*|rust|typescript|python|go)-hazards(?:-t7-t10)?\.md|(?<!/)changesets\.md"
)
TEXT_SUFFIXES = {".json", ".md", ".py", ".sh", ".yaml", ".yml"}
EXCLUDED_PARTS = {".git", ".agents", "dist", "node_modules"}
AUTHORING_ONLY = {
    "shared/references/README.md",
    "shared/references/authoring/diagrams.md",
    "shared/references/tooling/cli.md",
}
CONCERN_DIRECTORIES = {
    "architecture",
    "authoring",
    "delivery",
    "evaluation",
    "hazards",
    "tooling",
    "verification",
    "workspace",
}
# Published schemas are byte-immutable. Keep narrow exceptions for exact paths
# embedded before a reference move; live skill and agent routes must still use
# current paths and pass the checks below.
IMMUTABLE_PATH_EXCEPTIONS = {
    (
        "shared/schemas/changeset@2.json",
        "shared/references/" "changesets" ".md",
    ): "shared/references/delivery/changesets.md",
}


def authored_text_files() -> list[Path]:
    return [
        path
        for path in REPOSITORY_ROOT.rglob("*")
        if path.is_file()
        and path.suffix in TEXT_SUFFIXES
        and path.name != "CHANGELOG.md"
        and not EXCLUDED_PARTS.intersection(path.relative_to(REPOSITORY_ROOT).parts)
    ]


def is_runtime_caller(path: Path) -> bool:
    relative = path.relative_to(REPOSITORY_ROOT)
    parts = relative.parts
    if parts[:2] == ("shared", "references"):
        return path != REFERENCE_ROOT / "README.md"
    if parts[:2] == ("shared", "hooks"):
        return True
    if parts and parts[0] == "plugins":
        return "agents" in parts or "skills" in parts
    if parts[:3] == ("harnesses", "codex", "agent-roles"):
        return path.name != "README.md"
    return parts[:3] == ("harnesses", "codex", "plugins") and "skills" in parts


def local_markdown_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    if not target or target.startswith("#") or "://" in target or target.startswith("mailto:"):
        return None
    return unquote(target.split("#", 1)[0].split("?", 1)[0])


class ReferenceIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = {
            path: path.read_text(encoding="utf-8")
            for path in authored_text_files()
        }

    def test_exact_reference_paths_exist(self) -> None:
        broken: list[str] = []
        for source, contents in self.sources.items():
            for reference in REFERENCE_PATH.findall(contents):
                source_name = source.relative_to(REPOSITORY_ROOT).as_posix()
                if (source_name, reference) in IMMUTABLE_PATH_EXCEPTIONS:
                    continue
                if not (REPOSITORY_ROOT / reference).is_file():
                    broken.append(f"{source_name} -> {reference}")
        self.assertEqual(broken, [])

    def test_exact_schema_paths_exist(self) -> None:
        broken = [
            f"{source.relative_to(REPOSITORY_ROOT).as_posix()} -> {schema}"
            for source, contents in self.sources.items()
            if source.suffix in {".json", ".md", ".yaml", ".yml"}
            for schema in SCHEMA_PATH.findall(contents)
            if not (REPOSITORY_ROOT / schema).is_file()
        ]
        self.assertEqual(broken, [])

    def test_immutable_path_exceptions_have_live_replacements(self) -> None:
        invalid: list[str] = []
        for (source_name, historical), replacement in IMMUTABLE_PATH_EXCEPTIONS.items():
            source = REPOSITORY_ROOT / source_name
            if historical not in source.read_text(encoding="utf-8"):
                invalid.append(f"{source_name} no longer contains {historical}")
            if not (REPOSITORY_ROOT / replacement).is_file():
                invalid.append(f"replacement missing: {replacement}")
            live_callers = [
                path.relative_to(REPOSITORY_ROOT).as_posix()
                for path, contents in self.sources.items()
                if path != source and is_runtime_caller(path) and historical in contents
            ]
            if live_callers:
                invalid.append(f"live callers still use {historical}: {live_callers}")
        self.assertEqual(invalid, [])

    def test_local_markdown_links_resolve(self) -> None:
        broken: list[str] = []
        for source, contents in self.sources.items():
            if source.suffix != ".md":
                continue
            raw_targets = (
                MARKDOWN_LINK.findall(contents)
                + REFERENCE_LINK.findall(contents)
                + HTML_LINK.findall(contents)
            )
            for raw_target in raw_targets:
                target = local_markdown_target(raw_target)
                if target is None:
                    continue
                resolved = (source.parent / target).resolve()
                if not resolved.exists():
                    source_name = source.relative_to(REPOSITORY_ROOT).as_posix()
                    broken.append(f"{source_name} -> {target}")
        self.assertEqual(broken, [])

    def test_retired_or_ambiguous_reference_names_are_absent(self) -> None:
        stale = [
            f"{source.relative_to(REPOSITORY_ROOT).as_posix()} -> {match.group(0)}"
            for source, contents in self.sources.items()
            for match in RETIRED_REFERENCE_NAME.finditer(contents)
        ]
        self.assertEqual(stale, [])

    def test_reference_paths_are_concern_first(self) -> None:
        misplaced = [
            path.relative_to(REFERENCE_ROOT).as_posix()
            for path in REFERENCE_ROOT.rglob("*.md")
            if path != REFERENCE_ROOT / "README.md"
            and path.relative_to(REFERENCE_ROOT).parts[0] not in CONCERN_DIRECTORIES
        ]
        self.assertEqual(misplaced, [])

    def test_each_runtime_reference_has_a_runtime_caller(self) -> None:
        missing: list[str] = []
        for reference_file in REFERENCE_ROOT.rglob("*.md"):
            reference = reference_file.relative_to(REPOSITORY_ROOT).as_posix()
            if reference in AUTHORING_ONLY:
                continue
            callers = [
                source
                for source, contents in self.sources.items()
                if source != reference_file and is_runtime_caller(source) and reference in contents
            ]
            if not callers:
                missing.append(reference)
        self.assertEqual(missing, [])

    def test_codex_runtime_paths_are_shipped_with_the_plugins_that_load_them(self) -> None:
        catalog = json.loads((REPOSITORY_ROOT / "harnesses/codex/catalog.json").read_text(encoding="utf-8"))
        shipped = {
            entry["id"]: [
                item if isinstance(item, str) else item["source"] for item in entry.get("runtime_files", [])
            ]
            for entry in catalog["plugins"]
        }

        def is_shipped(plugin: str, path: str) -> bool:
            return any(path == item or path.startswith(item.rstrip("/") + "/") for item in shipped[plugin])

        missing: list[str] = []
        roles_used: dict[str, set[str]] = {}
        for source, contents in self.sources.items():
            parts = source.relative_to(REPOSITORY_ROOT).parts
            if parts[:3] != ("harnesses", "codex", "plugins") or "skills" not in parts:
                continue
            plugin = parts[3]
            for role in re.findall(r"`(recon|tracer|research|author|implementer|adversary|reviewer|judge)`", contents):
                roles_used.setdefault(role, set()).add(plugin)
            for path in REFERENCE_PATH.findall(contents) + SCHEMA_PATH.findall(contents) + SHARED_FILE_PATH.findall(contents):
                if not is_shipped(plugin, path):
                    missing.append(f"{source.relative_to(REPOSITORY_ROOT).as_posix()} -> {path}")
        # Role cards ship to every plugin; a path a card names must be shipped with at least
        # one plugin whose skills use that role, since the card applies it only where relevant.
        for card in (REPOSITORY_ROOT / "harnesses/codex/agent-roles").glob("*.md"):
            if card.name == "README.md":
                continue
            users = roles_used.get(card.stem, set())
            for path in REFERENCE_PATH.findall(card.read_text(encoding="utf-8")):
                if not any(is_shipped(plugin, path) for plugin in users):
                    missing.append(f"harnesses/codex/agent-roles/{card.name} -> {path}")
        self.assertEqual(missing, [])

    def test_adr_index_matches_records(self) -> None:
        index = REPOSITORY_ROOT / "docs/adr/README.md"
        rows: dict[str, list[str]] = {}
        problems: list[str] = []
        for line in index.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| ["):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) != 5 or not cells[4].startswith("Do not "):
                problems.append(f"malformed row: {line[:40]}")
                continue
            rows[cells[0][1:4]] = cells
        records = {record.name[:3]: record for record in index.parent.glob("[0-9][0-9][0-9]-*.md")}
        self.assertEqual(sorted(rows), sorted(records))
        for number, record in records.items():
            _, status, _, relation, _ = rows[number]
            meta = [
                line
                for line in record.read_text(encoding="utf-8").splitlines()
                if re.match(r"\*\*(Status|Supersedes|Extended by):\*\*", line)
            ]
            superseded = any("superseded" in line.lower() for line in meta if line.startswith("**Status:"))
            if status not in {"Accepted", "Partially superseded", "Superseded"} or superseded == (status == "Accepted"):
                problems.append(f"{number}: index status {status!r} disagrees with the record")
            for other in re.findall(r"ADR-(\d{3})", " ".join(meta)):
                if other not in rows or other not in relation:
                    problems.append(f"{number}: Relation omits or misnames {other}")
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
