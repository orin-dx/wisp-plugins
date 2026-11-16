"""Cover the pack injection hook (declaration parsing, nested files, inject once, fail open) and the wisp-packs plugin's packs."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "shared" / "hooks" / "pack-inject.py"
PLUGIN = REPOSITORY_ROOT / "plugins" / "wisp-packs"
specification = importlib.util.spec_from_file_location("pack_inject", TOOL)
assert specification is not None and specification.loader is not None
inject = importlib.util.module_from_spec(specification)
specification.loader.exec_module(inject)


class DeclarationParsingTests(unittest.TestCase):
    def test_reads_names_from_a_comma_separated_line(self) -> None:
        self.assertEqual(inject.declared_in("# Guide\n\nPacks: rust-house, ts-house\n"), ["rust-house", "ts-house"])

    def test_accepts_a_list_item_bold_label_and_backticked_names(self) -> None:
        text = "- Packs: `rust-house`, ts-house.\n* **Packs:** ui-house\n"
        self.assertEqual(inject.declared_in(text), ["rust-house", "ts-house", "ui-house"])

    def test_ignores_lines_that_only_mention_packs(self) -> None:
        text = "Add a Packs: line to opt in.\nThe Packs: line is optional here\nUnpacks: x\n"
        self.assertEqual(inject.declared_in(text), [])

    def test_ignores_a_line_inside_a_fenced_code_block(self) -> None:
        text = "Example:\n\n```\nPacks: rust-house\n```\n\nPacks: ts-house\n"
        self.assertEqual(inject.declared_in(text), ["ts-house"])

    def test_a_longer_fence_is_not_closed_by_a_shorter_one_inside_it(self) -> None:
        text = "````markdown\n```\nPacks: rust-house\n```\nPacks: ui-house\n````\n\nPacks: ts-house\n"
        self.assertEqual(inject.declared_in(text), ["ts-house"])
        self.assertEqual(inject.declared_in("~~~\n```\nPacks: rust-house\n~~~\n"), [])

    def test_drops_names_that_are_not_pack_names(self) -> None:
        self.assertEqual(inject.declared_in("Packs: ../etc/passwd, Rust_House, ok-1\n"), ["ok-1"])


class HookRunTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.packs = self.root / "plugin-packs"
        self.packs.mkdir()
        (self.packs / "alpha.md").write_text("Applies to alpha.\n\nALPHA-MARKER\n", encoding="utf-8")
        (self.packs / "beta.md").write_text("Applies to beta.\n\nBETA-MARKER\n", encoding="utf-8")
        self.repo = self.root / "repo"
        self.repo.mkdir()
        (self.repo / ".git").mkdir()

    def write(self, relative: str, text: str) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_hook(self, cwd: Path | None = None) -> dict | None:
        payload = json.dumps({"hook_event_name": "SessionStart", "cwd": str(cwd or self.repo)})
        output = inject.main([str(self.packs)], payload)
        return json.loads(output) if output else None

    def context(self, cwd: Path | None = None) -> str:
        result = self.run_hook(cwd)
        self.assertIsNotNone(result)
        assert result is not None
        specific = result["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "SessionStart")
        return specific["additionalContext"]

    def test_injects_the_packs_the_root_file_declares(self) -> None:
        self.write("AGENTS.md", "# Repo\n\nPacks: alpha\n")
        context = self.context()
        self.assertIn("ALPHA-MARKER", context)
        self.assertNotIn("BETA-MARKER", context)

    def test_injects_nothing_without_a_declaration(self) -> None:
        self.write("AGENTS.md", "# Repo\n\nNo packs here.\n")
        self.assertIsNone(self.run_hook())

    def test_injects_nothing_without_an_agents_file(self) -> None:
        self.assertIsNone(self.run_hook())

    def test_finds_nested_files_below_the_working_directory(self) -> None:
        self.write("AGENTS.md", "Packs: alpha\n")
        self.write("packages/web/AGENTS.md", "Packs: beta\n")
        context = self.context()
        self.assertIn("ALPHA-MARKER", context)
        self.assertIn("BETA-MARKER", context)

    def test_reads_the_root_file_from_a_subdirectory(self) -> None:
        self.write("AGENTS.md", "Packs: alpha\n")
        (self.repo / "crates" / "core").mkdir(parents=True)
        self.assertIn("ALPHA-MARKER", self.context(self.repo / "crates" / "core"))

    def test_does_not_read_above_the_repository_root(self) -> None:
        (self.root / "AGENTS.md").write_text("Packs: alpha\n", encoding="utf-8")
        self.write("AGENTS.md", "Packs: beta\n")
        context = self.context()
        self.assertIn("BETA-MARKER", context)
        self.assertNotIn("ALPHA-MARKER", context)

    def test_skips_dependency_and_hidden_directories(self) -> None:
        self.write("AGENTS.md", "Packs: beta\n")
        self.write("node_modules/dep/AGENTS.md", "Packs: alpha\n")
        self.write(".hidden/AGENTS.md", "Packs: alpha\n")
        self.assertNotIn("ALPHA-MARKER", self.context())

    def test_injects_a_pack_once_when_several_files_name_it(self) -> None:
        self.write("AGENTS.md", "Packs: alpha, alpha\n")
        self.write("a/AGENTS.md", "Packs: alpha\n")
        self.write("b/AGENTS.md", "Packs: alpha, beta\n")
        context = self.context()
        self.assertEqual(context.count("ALPHA-MARKER"), 1)
        self.assertEqual(context.count("BETA-MARKER"), 1)

    def test_skips_a_declared_pack_that_has_no_file(self) -> None:
        self.write("AGENTS.md", "Packs: missing, alpha\n")
        context = self.context()
        self.assertIn("ALPHA-MARKER", context)
        self.assertNotIn("missing", context)

    def test_a_declared_pack_with_no_file_alone_injects_nothing(self) -> None:
        self.write("AGENTS.md", "Packs: missing\n")
        self.assertIsNone(self.run_hook())


class FailOpenTests(unittest.TestCase):
    def run_script(self, stdin: str, *arguments: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        environment = {key: value for key, value in os.environ.items() if key != "CLAUDE_PLUGIN_ROOT"}
        environment.update(env or {})
        return subprocess.run(
            [sys.executable, str(TOOL), *arguments], input=stdin, capture_output=True, text=True, env=environment, check=False
        )

    def test_malformed_input_prints_nothing_and_exits_zero(self) -> None:
        done = self.run_script("{not json", str(PLUGIN / "packs"))
        self.assertEqual((done.returncode, done.stdout), (0, ""))

    def test_a_missing_packs_directory_prints_nothing_and_exits_zero(self) -> None:
        done = self.run_script("{}", "/nonexistent/packs")
        self.assertEqual((done.returncode, done.stdout), (0, ""))

    def test_no_packs_directory_at_all_prints_nothing_and_exits_zero(self) -> None:
        done = self.run_script("{}")
        self.assertEqual((done.returncode, done.stdout), (0, ""))

    def test_a_nonexistent_working_directory_exits_zero(self) -> None:
        done = self.run_script(json.dumps({"cwd": "/nonexistent/project"}), str(PLUGIN / "packs"))
        self.assertEqual(done.returncode, 0)

    def test_the_script_emits_the_documented_json_for_a_declared_pack(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory).resolve()
            (project / ".git").mkdir()
            (project / "AGENTS.md").write_text("Packs: rust-house\n", encoding="utf-8")
            done = self.run_script(json.dumps({"cwd": str(project)}), env={"CLAUDE_PLUGIN_ROOT": str(PLUGIN)})
        self.assertEqual(done.returncode, 0)
        specific = json.loads(done.stdout)["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "SessionStart")
        self.assertIn("rust-house", specific["additionalContext"])


class ShippedPackTests(unittest.TestCase):
    def test_pack_names_match_what_the_hook_accepts(self) -> None:
        for pack in (PLUGIN / "packs").glob("*.md"):
            with self.subTest(pack=pack.name):
                self.assertRegex(pack.stem, inject.PACK_NAME)

    def test_the_hook_is_registered_for_session_start(self) -> None:
        hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
        commands = [entry["command"] for group in hooks["SessionStart"] for entry in group["hooks"]]
        self.assertEqual(commands, ['python3 "${CLAUDE_PLUGIN_ROOT}/shared/hooks/pack-inject.py"'])

    def test_both_harnesses_ship_the_same_skills(self) -> None:
        claude = {path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md")}
        codex = {path.parent.name for path in (REPOSITORY_ROOT / "harnesses" / "codex" / "plugins" / "wisp-packs" / "skills").glob("*/SKILL.md")}
        self.assertEqual(claude, {"load", "list", "suggest"})
        self.assertEqual(claude, codex)


if __name__ == "__main__":
    unittest.main()
