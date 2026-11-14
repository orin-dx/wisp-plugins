"""Black-box tests for the version and manifest generator in tools/sync-claude-manifests.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "tools" / "sync-claude-manifests.py"

CODEX_MANIFEST = """{
  "name": "alpha",
  "version": "1.2.3",
  "skills": "./skills/",
  "interface": {
    "capabilities": ["skills", "agent-teams-optional"]
  }
}
"""


class SyncClaudeManifestsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.write_json(
            "plugins/alpha/plugin.json",
            {
                "id": "alpha",
                "name": "alpha",
                "version": "1.2.3",
                "description": "Alpha source description.",
                "author": {"name": "Orin DX"},
                "skills": "./skills/",
            },
        )
        self.write("plugins/alpha/README.md", "# alpha\n\n**Stage:** Code · **Version:** 1.2.3\n")
        self.write("plugins/alpha/CHANGELOG.md", "# Changelog\n\n## [1.2.3] - 2026-01-01\n\n- Notes.\n\n## [1.2.2] - 2025-12-01\n")
        self.write("harnesses/codex/plugins/alpha/.codex-plugin/plugin.json", CODEX_MANIFEST)
        self.write_json(
            "marketplace.json",
            {
                "name": "wisp",
                "version": "4.0.0",
                "plugins": [{"id": "alpha", "version": "1.2.3", "path": "./plugins/alpha", "description": "stale"}],
            },
        )
        self.write_json(".claude-plugin/marketplace.json", {"name": "wisp", "plugins": [{"name": "alpha", "description": "stale"}]})
        self.write("README.md", '<img src="https://img.shields.io/badge/Marketplace-v4.0.0-success.svg" alt="Marketplace v4.0.0" />\n')
        self.write("CHANGELOG.md", "# Changelog\n\n## [4.0.0] - 2026-01-01 — Name\n")
        self.sync()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_json(self, relative: str, value: object) -> None:
        self.write(relative, json.dumps(value, indent=2) + "\n")

    def read(self, relative: str) -> str:
        return (self.root / relative).read_text(encoding="utf-8")

    def run_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--root", str(self.root), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def sync(self) -> subprocess.CompletedProcess[str]:
        return self.run_tool()

    def check(self) -> subprocess.CompletedProcess[str]:
        return self.run_tool("--check")

    def set_plugin_version(self, version: str) -> None:
        path = self.root / "plugins/alpha/plugin.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["version"] = version
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    def test_a_consistent_repository_passes_the_check(self) -> None:
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_plugin_missing_from_a_marketplace_or_without_a_root_version_fails(self) -> None:
        for relative, key in (('marketplace.json', 'id'), ('.claude-plugin/marketplace.json', 'name')):
            with self.subTest(file=relative):
                original = self.read(relative)
                data = json.loads(original)
                data['plugins'] = [entry for entry in data['plugins'] if entry[key] != 'alpha']
                self.write_json(relative, data)
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('no entry for plugin `alpha`', result.stdout)
                self.write(relative, original)
        root = json.loads(self.read('marketplace.json'))
        del root['plugins'][0]['version']
        self.write_json('marketplace.json', root)
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('has no version', result.stdout)

    def test_a_marketplace_entry_without_a_plugin_fails(self) -> None:
        data = json.loads(self.read('marketplace.json'))
        data['plugins'].append({'id': 'ghost', 'version': '1.0.0', 'path': './plugins/ghost', 'description': 'x'})
        self.write_json('marketplace.json', data)
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('entry `ghost` has no plugins/ghost/plugin.json', result.stdout)

    def test_a_plugin_bump_reaches_every_copy_and_leaves_other_text_alone(self) -> None:
        self.set_plugin_version("1.3.0")
        self.assertNotEqual(self.check().returncode, 0)
        self.write("plugins/alpha/CHANGELOG.md", "## [1.3.0] - 2026-02-01\n")
        self.sync()
        self.assertEqual(self.check().returncode, 0)
        self.assertEqual(json.loads(self.read("plugins/alpha/.claude-plugin/plugin.json"))["version"], "1.3.0")
        self.assertEqual(json.loads(self.read("marketplace.json"))["plugins"][0]["version"], "1.3.0")
        self.assertEqual(self.read("plugins/alpha/README.md"), "# alpha\n\n**Stage:** Code · **Version:** 1.3.0\n")
        self.assertEqual(self.read("harnesses/codex/plugins/alpha/.codex-plugin/plugin.json"), CODEX_MANIFEST.replace("1.2.3", "1.3.0"))

    def test_descriptions_come_from_the_plugin_manifest(self) -> None:
        self.assertEqual(json.loads(self.read("marketplace.json"))["plugins"][0]["description"], "Alpha source description.")
        self.assertEqual(json.loads(self.read(".claude-plugin/marketplace.json"))["plugins"][0]["description"], "Alpha source description.")
        self.assertNotIn("version", json.loads(self.read(".claude-plugin/marketplace.json"))["plugins"][0])

    def test_a_stale_copy_fails_the_check_and_names_the_file(self) -> None:
        stale = {
            "plugins/alpha/README.md": "# alpha\n\n**Version:** 1.2.2\n",
            "harnesses/codex/plugins/alpha/.codex-plugin/plugin.json": CODEX_MANIFEST.replace("1.2.3", "1.2.2"),
        }
        for relative, content in stale.items():
            with self.subTest(file=relative):
                original = self.read(relative)
                self.write(relative, content)
                result = self.check()
                self.assertEqual(result.returncode, 1)
                self.assertIn(relative, result.stdout)
                self.write(relative, original)
        for relative in ("plugins/alpha/.claude-plugin/plugin.json", "marketplace.json"):
            with self.subTest(file=relative):
                original = self.read(relative)
                self.write(relative, original.replace("1.2.3", "1.2.2"))
                result = self.check()
                self.assertEqual(result.returncode, 1)
                self.assertIn(relative, result.stdout)
                self.write(relative, original)

    def test_a_disagreeing_changelog_fails_both_check_and_sync_and_is_never_rewritten(self) -> None:
        self.write("plugins/alpha/CHANGELOG.md", "## [1.2.2] - 2025-12-01\n")
        for result in (self.check(), self.sync()):
            self.assertEqual(result.returncode, 1)
            self.assertIn("plugins/alpha/CHANGELOG.md", result.stdout)
        self.assertEqual(self.read("plugins/alpha/CHANGELOG.md"), "## [1.2.2] - 2025-12-01\n")

    def test_a_missing_changelog_entry_fails(self) -> None:
        self.write("plugins/alpha/CHANGELOG.md", "# Changelog\n")
        self.assertEqual(self.check().returncode, 1)

    def test_a_readme_without_a_version_line_fails_because_it_cannot_be_generated(self) -> None:
        self.write("plugins/alpha/README.md", "# alpha\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("no `**Version:**` line", result.stdout)

    def test_the_ecosystem_version_comes_from_marketplace_json_and_rewrites_both_badge_spots(self) -> None:
        marketplace = json.loads(self.read("marketplace.json"))
        marketplace["version"] = "4.1.0"
        self.write_json("marketplace.json", marketplace)
        self.assertEqual(self.check().returncode, 1)
        self.write("CHANGELOG.md", "## [4.1.0] - 2026-02-01\n")
        self.sync()
        self.assertEqual(self.check().returncode, 0)
        self.assertEqual(
            self.read("README.md"),
            '<img src="https://img.shields.io/badge/Marketplace-v4.1.0-success.svg" alt="Marketplace v4.1.0" />\n',
        )

    def test_a_disagreeing_ecosystem_changelog_or_badge_fails(self) -> None:
        self.write("CHANGELOG.md", "## [3.9.0] - 2025-01-01\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("CHANGELOG.md", result.stdout)
        self.write("CHANGELOG.md", "## [4.0.0] - 2026-01-01\n")
        self.write("README.md", "no badge\n")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("README.md", result.stdout)

    def test_a_malformed_plugin_version_is_refused(self) -> None:
        self.set_plugin_version("1.2")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("version must be x.y.z", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
