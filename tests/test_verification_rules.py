import unittest
from pathlib import Path

REFERENCES = Path(__file__).resolve().parents[1] / "shared/references"

# Each verification rule has exactly one owner phrase in the shared references; agents point to it.
OWNERS = {
    "verification/evidence.md": [
        "Run what CI runs, from a clean state",
        "exercise generated files",
        "A test double accepts only what the real tool accepts",
        "compare what the change declares",
        "is a defect until a cause is shown",
        "reports how many and why",
        "is a lead, not evidence",
    ],
    "verification/implementation-review.md": ["lists the sites searched"],
}


class VerificationRuleOwnerTests(unittest.TestCase):
    def test_each_rule_lives_in_exactly_one_reference(self):
        for owner, phrases in OWNERS.items():
            for phrase in phrases:
                with self.subTest(phrase=phrase):
                    homes = [p for p in REFERENCES.rglob("*.md") if phrase in p.read_text()]
                    self.assertEqual([REFERENCES / owner], homes)


if __name__ == "__main__":
    unittest.main()
