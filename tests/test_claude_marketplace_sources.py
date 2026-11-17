"""Keep installed Claude plugins able to read the shared schemas and references.

Every plugin has a `shared` symlink to the repository's `shared/` directory. Claude Code copies a
plugin into its cache and dereferences a symlink whose target is elsewhere in the same marketplace,
so the installed plugin gets real schema and reference files. A `git-subdir` source fetches only one
subdirectory with a sparse checkout, so the target is absent and the installed `shared` is a dangling
link: the plugin loads but cannot read any schema or reference. For plugins in this repository the
marketplace entry must therefore be a relative path. Verified by installing every plugin into an isolated
Claude config (see docs/evaluations/frontend-design/verification/VERIFY-3.md).
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json"


class ClaudeMarketplaceSourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.entries = json.loads(MARKETPLACE.read_text(encoding="utf-8"))["plugins"]

    def test_every_plugin_directory_has_a_marketplace_entry_and_the_reverse(self) -> None:
        directories = {path.name for path in (REPOSITORY_ROOT / "plugins").iterdir() if path.is_dir()}
        self.assertEqual({entry["name"] for entry in self.entries}, directories)

    def test_entries_use_relative_path_sources_not_git_subdir(self) -> None:
        for entry in self.entries:
            with self.subTest(plugin=entry["name"]):
                self.assertIsInstance(
                    entry["source"],
                    str,
                    "a git-subdir source sparse-checks-out one directory, so the plugin's shared symlink dangles after install",
                )
                self.assertEqual(entry["source"], f"./plugins/{entry['name']}")
                self.assertTrue((REPOSITORY_ROOT / entry["source"]).is_dir())

    def test_each_plugin_shares_files_through_a_symlink_that_stays_inside_the_repository(self) -> None:
        for entry in self.entries:
            with self.subTest(plugin=entry["name"]):
                link = REPOSITORY_ROOT / "plugins" / entry["name"] / "shared"
                self.assertTrue(link.is_symlink(), "shared must be a symlink so the installer can dereference it")
                target = link.resolve()
                self.assertEqual(target, (REPOSITORY_ROOT / "shared").resolve())
                self.assertTrue((target / "schemas").is_dir())

    def test_each_plugin_has_the_manifest_claude_reads(self) -> None:
        for entry in self.entries:
            with self.subTest(plugin=entry["name"]):
                manifest = REPOSITORY_ROOT / "plugins" / entry["name"] / ".claude-plugin" / "plugin.json"
                self.assertTrue(manifest.is_file())
                self.assertEqual(json.loads(manifest.read_text(encoding="utf-8"))["name"], entry["name"])


if __name__ == "__main__":
    unittest.main()
