import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/behavioral/fix-pass-misses.json"
REFERENCES = ROOT / "shared/references"

# Each fixture rule has exactly one owner phrase in the shared references.
OWNERS = {
    "ci-parity": ("verification/evidence.md", "Run what CI runs, from a clean state"),
    "generated-as-consumer": ("verification/evidence.md", "exercise generated files"),
    "fake-matches-real": ("verification/evidence.md", "A test double accepts only what the real tool accepts"),
    "sibling-search": ("verification/implementation-review.md", "lists the sites searched"),
    "declared-vs-actual": ("verification/evidence.md", "compare what the change declares"),
    "intermittent-is-defect": ("verification/evidence.md", "is a defect until a cause is shown"),
    "conservation": ("verification/evidence.md", "reports how many and why"),
    "claims-cite-proof": ("verification/evidence.md", "is a lead, not evidence"),
}


class FixPassFixtureTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(FIXTURE.read_text())

    def test_cases_are_complete(self):
        for case in self.fixture["cases"]:
            with self.subTest(case=case["id"]):
                self.assertIn(case["rule"], OWNERS)
                self.assertTrue(case["public_input"]["repro"])
                self.assertTrue(case["oracle"]["required_observations"])
                self.assertTrue(case["oracle"]["false_pass_if"])

    def test_every_rule_has_one_owner(self):
        for rule in {case["rule"] for case in self.fixture["cases"]}:
            owner, phrase = OWNERS[rule]
            with self.subTest(rule=rule):
                homes = [p for p in REFERENCES.rglob("*.md") if phrase in p.read_text()]
                self.assertEqual([REFERENCES / owner], homes)

    def test_every_owned_rule_is_exercised_by_a_fixture(self):
        used = {case["rule"] for case in self.fixture["cases"]}
        self.assertEqual(set(OWNERS), used)


if __name__ == "__main__":
    unittest.main()
