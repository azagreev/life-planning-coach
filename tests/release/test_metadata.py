"""Release tests for life-planning-coach metadata consistency."""

import json
import unittest
import zipfile
from pathlib import Path


class TestVersionConsistency(unittest.TestCase):
    """SKILL.md, README.md, setup.py and __init__.py versions must match."""

    def test_skill_md_has_version(self):
        text = Path("SKILL.md").read_text(encoding="utf-8")
        self.assertIn("version:", text, "SKILL.md must have version in frontmatter")

    def test_skill_version_matches_setup_py(self):
        skill_text = Path("SKILL.md").read_text(encoding="utf-8")
        setup_text = Path("setup.py").read_text(encoding="utf-8")

        skill_version = ""
        for line in skill_text.splitlines():
            if line.startswith("version:"):
                skill_version = line.split(":", 1)[1].strip()
                break

        setup_version = ""
        for line in setup_text.splitlines():
            if 'version=' in line:
                setup_version = line.split('="')[1].split('"')[0]
                break

        self.assertTrue(skill_version, "Could not parse version from SKILL.md")
        self.assertTrue(setup_version, "Could not parse version from setup.py")
        self.assertEqual(
            skill_version, setup_version,
            f"SKILL.md version ({skill_version}) != setup.py version ({setup_version})"
        )

    def test_init_version_matches_setup_py(self):
        init_text = Path("calendar_integration/__init__.py").read_text(encoding="utf-8")
        setup_text = Path("setup.py").read_text(encoding="utf-8")

        init_version = ""
        for line in init_text.splitlines():
            if '__version__' in line:
                # Handle both single and double quotes
                parts = line.split("=")
                if len(parts) >= 2:
                    init_version = parts[1].strip().strip('"\'')
                break

        setup_version = ""
        for line in setup_text.splitlines():
            if 'version=' in line:
                setup_version = line.split('="')[1].split('"')[0]
                break

        self.assertTrue(init_version, "Could not parse __version__ from __init__.py")
        self.assertTrue(setup_version, "Could not parse version from setup.py")
        self.assertEqual(
            init_version, setup_version,
            f"__init__.py version ({init_version}) != setup.py version ({setup_version})"
        )


class TestRequiredFiles(unittest.TestCase):
    """Required release files must exist."""

    def test_license_exists(self):
        self.assertTrue(Path("LICENSE").exists(), "LICENSE file must exist")

    def test_contributing_exists(self):
        self.assertTrue(Path("CONTRIBUTING.md").exists(), "CONTRIBUTING.md must exist")

    def test_security_exists(self):
        self.assertTrue(Path("SECURITY.md").exists(), "SECURITY.md must exist")

    def test_skill_md_exists(self):
        self.assertTrue(Path("SKILL.md").exists(), "SKILL.md must exist")

    def test_references_dir_exists(self):
        self.assertTrue(Path("references").is_dir(), "references/ directory must exist")


class TestSkillArchive(unittest.TestCase):
    """.skill archive must contain required files."""

    def test_skill_archive_structure(self):
        skill_path = Path("life-planning-coach.skill")
        if not skill_path.exists():
            self.skipTest("life-planning-coach.skill not built yet")

        with zipfile.ZipFile(skill_path, "r") as zf:
            names = zf.namelist()
            prefix = "life-planning-coach/"
            required = [
                f"{prefix}SKILL.md",
                f"{prefix}README.md",
                f"{prefix}LICENSE",
                f"{prefix}CONTRIBUTING.md",
                f"{prefix}SECURITY.md",
            ]
            for req in required:
                self.assertIn(
                    req, names,
                    f"Required file {req} missing from .skill archive"
                )


class TestProjectMetadata(unittest.TestCase):
    """Project metadata consistency tests."""

    def test_requirements_txt_no_leading_space(self):
        req_path = Path("calendar_integration/requirements.txt")
        self.assertTrue(req_path.exists(), "requirements.txt must exist")
        lines = req_path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines, start=1):
            self.assertFalse(
                line.startswith(" "),
                f"Line {i} in requirements.txt starts with a space: {line!r}"
            )

    def test_setup_py_name_matches_repo(self):
        setup_text = Path("setup.py").read_text(encoding="utf-8")
        name_value = ""
        for line in setup_text.splitlines():
            if line.strip().startswith("name="):
                name_value = line.split("=", 1)[1].strip().strip('"\'')
                break
        self.assertTrue(name_value, "Could not parse name from setup.py")
        self.assertIn(
            "life-planning-coach", name_value,
            f"setup.py name ({name_value}) should contain 'life-planning-coach', not 'life-planning-calendar'"
        )


if __name__ == "__main__":
    unittest.main()
