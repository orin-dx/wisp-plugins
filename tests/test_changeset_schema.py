"""Cover changeset@3 (layered summary, disposition) and release-artifact@3, and that the courier sources use them."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
specification = importlib.util.spec_from_file_location("validate_handback", REPOSITORY_ROOT / "shared" / "hooks" / "validate-handback.py")
assert specification is not None and specification.loader is not None
validator = importlib.util.module_from_spec(specification)
specification.loader.exec_module(validator)

CHANGESET = validator.load_schema("changeset@3")
RELEASE = validator.load_schema("release-artifact@3")

LAYERED = (
    "Links each change in the release PR to the pull request that added it.\n\n"
    "- Shown as `#123` next to the change, so you can open the review and discussion behind it.\n"
    "- A changeset added without a pull request (a direct push) gets no link.\n"
    "- For scripts: the `--emit-preview` file has an optional `pr` for each change."
)


def changeset(**changes) -> dict:
    document = {
        "summary": LAYERED,
        "disposition": "new",
        "consumer_impact": "new-capability",
        "semver_impact": "minor",
        "files_changed": ["src/release.rs"],
        "acceptance_criteria_met": ["unlinked"],
    }
    document.update(changes)
    return document


class ChangesetThreeTests(unittest.TestCase):
    def errors(self, document: dict) -> list[str]:
        return validator.validate(document, CHANGESET)

    def test_a_layered_summary_over_the_old_cap_is_valid(self) -> None:
        self.assertGreater(len(LAYERED), 200)
        self.assertEqual(self.errors(changeset()), [])

    def test_a_one_line_summary_is_valid(self) -> None:
        self.assertEqual(self.errors(changeset(summary="Fixes the crash when the config file is empty.", semver_impact="patch", consumer_impact="behavior-change")), [])

    def test_the_summary_may_not_be_empty(self) -> None:
        self.assertTrue(any("at least 1 characters" in error for error in self.errors(changeset(summary=""))))

    def test_disposition_is_required_and_bounded(self) -> None:
        missing = changeset()
        del missing["disposition"]
        self.assertTrue(any("disposition" in error for error in self.errors(missing)))
        self.assertTrue(any("expected one of" in error for error in self.errors(changeset(disposition="skip"))))

    def test_updating_an_existing_entry_names_it(self) -> None:
        self.assertTrue(any("updates" in error for error in self.errors(changeset(disposition="update-existing"))))
        self.assertEqual(self.errors(changeset(disposition="update-existing", updates=".changeset/release-pr-links.md")), [])

    def test_no_entry_needed_means_internal_only_and_no_bump(self) -> None:
        none = changeset(disposition="none", summary="Test-only change; no consumer sees it.", consumer_impact="internal-only", semver_impact="none")
        self.assertEqual(self.errors(none), [])
        self.assertTrue(any("expected 'none'" in error for error in self.errors(changeset(disposition="none"))))

    def test_unknown_fields_are_rejected_and_the_scratchpad_is_kept(self) -> None:
        self.assertTrue(any("unexpected property" in error for error in self.errors(changeset(extra=1))))
        self.assertIn("reasoning", CHANGESET["properties"])
        self.assertEqual(CHANGESET["$id"], "changeset@3")

    def test_the_published_previous_versions_are_untouched(self) -> None:
        previous = json.loads((REPOSITORY_ROOT / "shared" / "schemas" / "changeset@2.json").read_text(encoding="utf-8"))
        self.assertEqual(previous["properties"]["summary"]["maxLength"], 200)


class ReleaseArtifactThreeTests(unittest.TestCase):
    def test_a_layered_summary_is_carried_into_a_release(self) -> None:
        release = {
            "version": "0.19.0",
            "date": "2026-11-09",
            "changesets": [{"summary": LAYERED, "consumer_impact": "new-capability", "semver_impact": "minor"}],
        }
        self.assertEqual(validator.validate(release, RELEASE), [])
        self.assertEqual(RELEASE["$id"], "release-artifact@3")


class CourierSourcesUseTheNewContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def test_the_analyzer_and_skill_drop_the_length_rules(self) -> None:
        for relative in ("plugins/courier/agents/changeset-analyzer.md", "plugins/courier/skills/changeset/SKILL.md"):
            text = self.read(relative)
            with self.subTest(path=relative):
                self.assertNotIn("max 200", text)
                self.assertNotIn("one clause", text)
                self.assertNotIn("one sentence for minor", text)
                self.assertIn("changeset@3", text)

    def test_the_analyzer_keeps_limits_out_of_the_scratchpad(self) -> None:
        text = self.read("plugins/courier/agents/changeset-analyzer.md")
        self.assertIn("never forwarded", text)
        self.assertIn("disposition", text)

    def test_the_reference_covers_cli_and_serialized_file_changes(self) -> None:
        text = self.read("shared/references/delivery/changesets.md")
        for phrase in ("CLI flag", "exit code", "serialized file"):
            self.assertIn(phrase, text)

    def test_courier_skills_tell_the_assistant_to_use_them(self) -> None:
        for skill in ("changeset", "commit", "pr"):
            description = self.read(f"plugins/courier/skills/{skill}/SKILL.md").split("---")[1]
            with self.subTest(skill=skill):
                self.assertIn("Use this", description)

    def test_the_release_summarizer_consumes_the_new_schema(self) -> None:
        text = self.read("plugins/courier/agents/release-summarizer.md")
        self.assertIn("changeset@3", text)
        self.assertIn("release-artifact@3", text)
        self.assertNotIn("changeset@2", text)


class CommitAndPullRequestGuidanceTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def test_the_commit_analyzer_follows_the_repository_and_keeps_limits_out_of_the_scratchpad(self) -> None:
        text = self.read("plugins/courier/agents/commit-analyzer.md")
        self.assertIn("recent commit history", text)
        self.assertIn("never forwarded", text)
        self.assertIn("exit code", text)

    def test_the_pr_narrator_follows_the_template_and_links_the_changeset(self) -> None:
        text = self.read("plugins/courier/agents/pr-narrator.md")
        self.assertIn("pull request template", text)
        self.assertIn("courier/changeset", text)
        self.assertIn("what they see and where", text)
        self.assertIn("mark it as inferred", text)

    def test_the_references_carry_the_same_rules(self) -> None:
        self.assertIn("The scope table below applies only to this repository", self.read("shared/references/delivery/commits.md"))
        github = self.read("shared/references/delivery/github.md")
        self.assertIn("pull request template", github)
        self.assertIn("courier/changeset", github)


if __name__ == "__main__":
    unittest.main()
