"""Invariant test for v0.15.1 cleanup.

After dev-only cleanup, references/ must contain ONLY runtime artefacts.
Dev-only содержимое (research, tasks, audit, archive, legacy plans/checklists/
acceptance criteria, shadow research files) живёт в docs/.

Каноничный allow-list ниже фиксирует то, что грузится в runtime skill.
Любой новый файл в references/ должен быть либо в allow-list, либо переехать в docs/.
"""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCES = REPO_ROOT / "references"
DOCS = REPO_ROOT / "docs"


# Dev-only directories that MUST NOT exist under references/.
FORBIDDEN_REFERENCES_SUBDIRS = {"research", "tasks", "audit", "archive"}


# Legacy filename patterns that MUST NOT exist directly under references/.
FORBIDDEN_REFERENCES_PATTERNS = (
    "acceptance_criteria_v",
    "release_checklist_v",
    "plan_v",                       # plan_v0.5.0.md etc.
    "plan_roadmap_backlog_cleanup",
    "research_diagnostic_",         # shadow files
    "research_communication_style_",
    "research_stage_",
    "competitive_research_",
    "persistence_research_",
)


# Directories that MUST exist under docs/ (cleanup destinations).
REQUIRED_DOCS_SUBDIRS = {"research", "tasks", "audit", "archive"}


class TestReferencesRuntimeOnly(unittest.TestCase):
    """references/ contains only runtime artefacts after v0.15.1 cleanup."""

    def test_no_dev_only_subdirs_in_references(self):
        for name in FORBIDDEN_REFERENCES_SUBDIRS:
            subdir = REFERENCES / name
            self.assertFalse(
                subdir.is_dir(),
                f"references/{name}/ must not exist (moved to docs/{name}/ in v0.15.1)",
            )

    def test_no_legacy_files_in_references_root(self):
        offenders = []
        for entry in REFERENCES.iterdir():
            if not entry.is_file():
                continue
            name = entry.name.lower()
            for pattern in FORBIDDEN_REFERENCES_PATTERNS:
                if name.startswith(pattern):
                    offenders.append(entry.name)
                    break
        self.assertFalse(
            offenders,
            f"Legacy files still in references/ (move to docs/): {offenders}",
        )

    def test_required_docs_dirs_exist(self):
        for name in REQUIRED_DOCS_SUBDIRS:
            subdir = DOCS / name
            self.assertTrue(
                subdir.is_dir(),
                f"docs/{name}/ must exist (cleanup destination)",
            )

    def test_release_notes_live_in_docs_archive(self):
        archive = DOCS / "archive"
        notes = list(archive.glob("RELEASE_NOTES_v*.md"))
        self.assertGreater(
            len(notes),
            0,
            "docs/archive/ must contain RELEASE_NOTES_v*.md (used by release.sh + pre-push hook)",
        )

    def test_state_v2_schema_lives_in_references(self):
        """state_v2_schema.md is runtime — must stay in references/ root."""
        self.assertTrue(
            (REFERENCES / "state_v2_schema.md").exists(),
            "references/state_v2_schema.md must exist (canonical runtime schema)",
        )

    def test_dashboard_guide_lives_in_references(self):
        """Thin runtime dashboard_guide.md stays in references/."""
        self.assertTrue(
            (REFERENCES / "dashboard_guide.md").exists(),
            "references/dashboard_guide.md must exist (thin runtime guide)",
        )

    def test_dashboard_architecture_lives_in_docs(self):
        """Heavy dashboard architecture doc moved to docs/research/ in v0.15.0."""
        self.assertTrue(
            (DOCS / "research" / "dashboard_architecture_v1.md").exists(),
            "Heavy dashboard architecture doc must live in docs/research/",
        )


if __name__ == "__main__":
    unittest.main()
