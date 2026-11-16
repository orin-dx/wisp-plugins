"""Cover the pure parts of scripts/release.py: which tags it plans and which changelog entry it reads."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
specification = importlib.util.spec_from_file_location("release", REPOSITORY_ROOT / "scripts" / "release.py")
assert specification is not None and specification.loader is not None
release = importlib.util.module_from_spec(specification)
specification.loader.exec_module(release)


def tree(directory: str) -> Path:
    root = Path(directory)
    (root / "marketplace.json").write_text(json.dumps({"version": "4.6.0", "plugins": []}), encoding="utf-8")
    for plugin, version in (("alpha", "1.2.0"), ("beta", "2.0.1")):
        (root / "plugins" / plugin).mkdir(parents=True)
        (root / "plugins" / plugin / "plugin.json").write_text(json.dumps({"version": version}), encoding="utf-8")
    (root / "CHANGELOG.md").write_text("# Changelog\n\n## [4.6.0] - 2026-11-14 — Start by intent\n\n- One.\n- Two.\n\n## [4.5.0] - 2026-11-10 — Older\n\n- Old.\n", encoding="utf-8")
    return root


class ReleaseTests(unittest.TestCase):
    def test_every_untagged_version_gets_a_tag_and_existing_ones_are_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = tree(directory)
            self.assertEqual([tag for tag, _ in release.tags_to_create(root, set())], ["v4.6.0", "alpha--v1.2.0", "beta--v2.0.1"])
            self.assertEqual([tag for tag, _ in release.tags_to_create(root, {"v4.6.0", "alpha--v1.2.0"})], ["beta--v2.0.1"])

    def test_a_rerun_after_a_partial_push_only_pushes_what_the_remote_lacks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            planned = release.tags_to_create(tree(directory), set())
        local = {"v4.6.0", "alpha--v1.2.0", "beta--v2.0.1"}
        to_create, to_push = release.split_tags(planned, local, {"alpha--v1.2.0"})
        self.assertEqual(to_create, [])
        self.assertEqual(to_push, ["v4.6.0", "beta--v2.0.1"])
        to_create, to_push = release.split_tags(planned, set(), set())
        self.assertEqual([tag for tag, _ in to_create], ["v4.6.0", "alpha--v1.2.0", "beta--v2.0.1"])
        self.assertEqual(len(to_push), 3)

    def test_the_newest_changelog_entry_gives_the_version_name_and_body(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            version, name, body = release.changelog_top(tree(directory))
        self.assertEqual((version, name), ("4.6.0", "Start by intent"))
        self.assertEqual(body, "- One.\n- Two.")


if __name__ == "__main__":
    unittest.main()
