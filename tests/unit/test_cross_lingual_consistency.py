"""v0.19.0: Cross-lingual consistency audit.

Verifies:
- "Drive" used as proper noun consistently (no lowercase "drive" в user-facing text)
- No "Cloud Storage" lowercase variants (use "Drive" or "Google Drive")
- README positioning: promise/comparison BEFORE methodologies list

Notes:
- Code identifiers like `drive_connected`, `persistence_retry.drive.*` are excluded
  (these are JSON keys / pseudocode variables, not user-facing text).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MASTER = REPO_ROOT / "SKILL.master.md"
AI_INSTRUCTIONS = REPO_ROOT / "references" / "templates" / "AI_Instructions.md"
README = REPO_ROOT / "README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks and inline code (for prose-only checks)."""
    # Remove fenced ``` ... ``` blocks
    text = re.sub(r"```[\s\S]*?```", "", text)
    # Remove inline `code`
    text = re.sub(r"`[^`]+`", "", text)
    return text


class TestDriveTerminology(unittest.TestCase):
    """'Drive' used consistently as proper noun (no lowercase, no 'Cloud Storage')."""

    def test_master_no_cloud_storage_in_prose(self):
        body = _strip_code_blocks(_read(MASTER))
        self.assertNotIn(
            "Cloud Storage",
            body,
            "SKILL.master.md must not use 'Cloud Storage' in user-facing prose — use 'Drive'",
        )

    def test_ai_instructions_no_cloud_storage_in_prose(self):
        body = _strip_code_blocks(_read(AI_INSTRUCTIONS))
        self.assertNotIn(
            "Cloud Storage",
            body,
            "AI_Instructions.md must not use 'Cloud Storage' in prose",
        )

    def test_master_no_lowercase_drive_in_prose(self):
        """`drive_connected` and similar JSON/pseudocode keys are fine — they're in code blocks."""
        body = _strip_code_blocks(_read(MASTER))
        # Look for ' drive ' or 'drive.' or 'drive,' in prose, but not 'Drive' or 'drive_'
        # We allow `drive_connected` as variable name within prose only if backticked (stripped).
        # After stripping code blocks, lowercase 'drive' should NOT appear as standalone word.
        lowercase_drive = re.findall(r"(?<![_A-Za-z])drive(?![_A-Za-z])", body)
        self.assertEqual(
            lowercase_drive,
            [],
            f"SKILL.master.md prose contains {len(lowercase_drive)} 'drive' (lowercase) occurrences "
            f"outside code/variables. Use 'Drive' (proper noun).",
        )


class TestReadmePositioning(unittest.TestCase):
    """README first sections: promise → comparison → methodologies (not the reverse)."""

    def test_readme_has_comparison_table(self):
        body = _read(README)
        # Comparison table should mention Notion or Todoist + Generic AI-coach
        self.assertTrue(
            "Notion" in body or "Todoist" in body,
            "README must have comparison table mentioning Notion/Todoist",
        )
        self.assertIn(
            "AI-coach",
            body,
            "README must have comparison table mentioning generic AI-coaches",
        )

    def test_readme_positioning_promise_before_methodologies(self):
        body = _read(README)
        # "Чем отличается" (positioning) should come before "Что внутри" or "Wheel of Life"
        idx_diff = body.find("Чем отличается")
        idx_wheel = body.find("Wheel of Life")
        self.assertGreater(idx_diff, -1, "README must have 'Чем отличается' section")
        self.assertGreater(idx_wheel, -1, "README must have Wheel of Life mention")
        self.assertLess(
            idx_diff,
            idx_wheel,
            "README 'Чем отличается' section must come BEFORE 'Wheel of Life' methodology list",
        )

    def test_readme_promise_explicit(self):
        """First 30 lines must mention what the project DOES, not just what it has."""
        body = _read(README)
        first_30_lines = "\n".join(body.splitlines()[:30])
        # Promise keywords (one of): план, цели, привычки, ритм
        self.assertTrue(
            any(kw in first_30_lines for kw in ["план", "цели", "привычк", "ритм"]),
            "README first 30 lines must articulate promise (план / цели / привычки / ритм)",
        )


if __name__ == "__main__":
    unittest.main()
