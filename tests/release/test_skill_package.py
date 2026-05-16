"""
Tests for the life-planning-coach skill package (ZIP artifact).

Per Anthropic's official requirements:
https://support.claude.com/en/articles/12512180-use-skills-in-claude

Rules verified:
1. Skill must be packaged as a ZIP archive
2. ZIP must contain the skill folder at the root level (not just SKILL.md)
3. Folder name must be kebab-case
4. SKILL.md must exist with valid YAML frontmatter
5. No forbidden files (.git/, README.md at skill root, etc.)
"""

import os
import re
import zipfile
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
ZIP_PATH = PROJECT_ROOT / "life-planning-coach.zip"
SKILL_PATH = PROJECT_ROOT / "life-planning-coach.skill"
SKILL_MD_PATH = PROJECT_ROOT / "SKILL.md"

# Maximum ZIP size (10 MB) — Anthropic may have limits
MAX_ZIP_SIZE_BYTES = 10 * 1024 * 1024

# Files that must NOT be inside the skill folder
FORBIDDEN_FILES = {
    ".git",
    ".gitattributes",
    ".gitignore",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "RELEASE_NOTES.md",
    "RELEASE_NOTES_v0.4.md",
    "setup.py",
    "pyproject.toml",
    "PLAN.md",
    "PLAN-FINAL.md",
    "PLAN-MIGRATION.md",
    "QA_CHECKLIST.md",
    "TESTING_ALTERNATIVES.md",
    "AGENTS.md",
    ".github",
    "tests",
    "scripts",             # build scripts are not part of the skill
    "domain",
    "research",
}

# Required files inside the skill folder
REQUIRED_FILES = {
    "SKILL.md",
}

# Optional but expected files/directories
EXPECTED_CONTENT = {
    "references",
    "life-planning-dashboard.html",
}


class TestZipArtifactExists:
    """Verify the ZIP artifact is built."""

    def test_zip_file_exists(self):
        assert ZIP_PATH.exists(), f"ZIP artifact not found: {ZIP_PATH}"

    def test_zip_file_is_readable(self):
        assert zipfile.is_zipfile(ZIP_PATH), f"File is not a valid ZIP: {ZIP_PATH}"

    def test_zip_size_under_limit(self):
        size = ZIP_PATH.stat().st_size
        assert size <= MAX_ZIP_SIZE_BYTES, (
            f"ZIP size {size} bytes exceeds limit {MAX_ZIP_SIZE_BYTES} bytes"
        )

    def test_skill_file_exists_for_backward_compatibility(self):
        """.skill file is kept for backward compatibility."""
        assert SKILL_PATH.exists(), f".skill file not found: {SKILL_PATH}"

    def test_zip_integrity_crc32(self):
        """Verify ZIP is not corrupted — check CRC32 of every entry."""
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            bad_file = zf.testzip()
            assert bad_file is None, (
                f"ZIP is corrupted, failed CRC32 check on file: {bad_file}"
            )

    def test_zip_extracts_without_errors(self, tmp_path):
        """Unpack ZIP to temp dir and verify all files extract cleanly."""
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            zf.extractall(tmp_path)

        extracted_folder = tmp_path / "life-planning-coach"
        assert extracted_folder.exists(), "Extracted folder not found after unzip"
        assert (extracted_folder / "SKILL.md").exists(), "SKILL.md missing after extraction"

        # Verify every file from ZIP manifest exists on disk and is readable
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                extracted_file = tmp_path / info.filename
                assert extracted_file.exists(), f"File missing after extraction: {info.filename}"
                assert extracted_file.stat().st_size == info.file_size, (
                    f"Size mismatch for {info.filename}: "
                    f"expected {info.file_size}, got {extracted_file.stat().st_size}"
                )
                # Try reading the file
                content = extracted_file.read_bytes()
                assert len(content) == info.file_size, (
                    f"Read size mismatch for {info.filename}"
                )


class TestZipStructure:
    """Verify ZIP contains folder at root level (Anthropic requirement)."""

    @pytest.fixture(scope="class")
    def zip_contents(self):
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            return zf.namelist()

    def test_root_contains_folder_not_flat_files(self, zip_contents):
        """
        Anthropic: "the ZIP must contain the folder itself at the root,
        not just the SKILL.md file"
        """
        root_entries = [name for name in zip_contents if name.count("/") <= 1]
        folders_at_root = [name for name in root_entries if name.endswith("/")]

        assert len(folders_at_root) >= 1, (
            "ZIP must contain a folder at the root level. "
            f"Root entries: {root_entries}"
        )

    def test_root_has_exactly_one_skill_folder(self, zip_contents):
        """There should be exactly one skill folder at root."""
        root_folders = [
            name.rstrip("/")
            for name in zip_contents
            if name.count("/") == 1 and name.endswith("/")
        ]
        assert root_folders == ["life-planning-coach"], (
            f"Expected exactly one root folder 'life-planning-coach', got: {root_folders}"
        )

    def test_folder_name_is_kebab_case(self, zip_contents):
        """Anthropic: folder name must be kebab-case."""
        root_folders = [
            name.rstrip("/")
            for name in zip_contents
            if name.count("/") == 1 and name.endswith("/")
        ]
        for folder in root_folders:
            assert re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", folder), (
                f"Folder name '{folder}' is not kebab-case. "
                "Use lowercase letters, numbers, and hyphens only."
            )

    def test_no_forbidden_files_in_skill_folder(self, zip_contents):
        """Verify no dev/repo files leaked into the skill package."""
        skill_files = [
            name.replace("life-planning-coach/", "")
            for name in zip_contents
            if name.startswith("life-planning-coach/")
        ]
        found_forbidden = []
        for forbidden in FORBIDDEN_FILES:
            for skill_file in skill_files:
                if skill_file == forbidden or skill_file.startswith(forbidden + "/"):
                    found_forbidden.append(skill_file)

        assert not found_forbidden, (
            f"Forbidden files found in skill package: {found_forbidden}"
        )


class TestSkillMdContent:
    """Verify SKILL.md inside ZIP is valid."""

    @pytest.fixture(scope="class")
    def skill_md_from_zip(self):
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            return zf.read("life-planning-coach/SKILL.md").decode("utf-8")

    @pytest.fixture(scope="class")
    def skill_md_from_repo(self):
        return SKILL_MD_PATH.read_text(encoding="utf-8")

    def test_skill_md_matches_repo_version(self, skill_md_from_zip, skill_md_from_repo):
        """The ZIP's SKILL.md must be identical to the repo's."""
        assert skill_md_from_zip == skill_md_from_repo, (
            "SKILL.md in ZIP does not match repo version. "
            "Run scripts/build-skill.sh to rebuild."
        )

    def test_has_yaml_frontmatter(self, skill_md_from_zip):
        match = re.search(r"^---\s*\n(.*?)\n---\s*\n", skill_md_from_zip, re.DOTALL)
        assert match, "SKILL.md missing YAML frontmatter"

    def test_frontmatter_has_required_fields(self, skill_md_from_zip):
        match = re.search(r"^---\s*\n(.*?)\n---\s*\n", skill_md_from_zip, re.DOTALL)
        frontmatter = match.group(1)

        required_fields = ["name", "version", "requires_mcp"]
        for field in required_fields:
            pattern = rf"^{field}\s*:"
            assert re.search(pattern, frontmatter, re.MULTILINE), (
                f"Frontmatter missing required field: '{field}'"
            )

    def test_frontmatter_version_matches_expected(self, skill_md_from_zip):
        match = re.search(r"^---\s*\n(.*?)\n---\s*\n", skill_md_from_zip, re.DOTALL)
        frontmatter = match.group(1)

        version_match = re.search(r"^version\s*:\s*['\"]?(.*?)['\"]?\s*$", frontmatter, re.MULTILINE)
        assert version_match, "Frontmatter missing 'version' field"
        version = version_match.group(1).strip('"').strip("'")
        assert version == "0.6.0", f"Expected version 0.6.0, got: {version}"

    def test_skill_md_is_under_token_limit(self, skill_md_from_zip):
        """
        Anthropic recommends keeping SKILL.md under 5,000 words.
        This is a soft limit — we warn if exceeded.
        """
        word_count = len(skill_md_from_zip.split())
        max_words = 5000
        assert word_count <= max_words, (
            f"SKILL.md has {word_count} words, exceeds recommended {max_words}. "
            "Consider moving content to references/."
        )


class TestRequiredFiles:
    """Verify required and expected files are present."""

    @pytest.fixture(scope="class")
    def zip_contents(self):
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            return zf.namelist()

    @pytest.mark.parametrize("required_file", REQUIRED_FILES)
    def test_required_file_exists(self, zip_contents, required_file):
        path = f"life-planning-coach/{required_file}"
        assert path in zip_contents, f"Required file missing: {required_file}"

    @pytest.mark.parametrize("expected_file", EXPECTED_CONTENT)
    def test_expected_content_exists(self, zip_contents, expected_file):
        """These are optional but strongly recommended."""
        # ZIP entries for directories end with '/'
        path = f"life-planning-coach/{expected_file}"
        if not path.endswith("/"):
            path_dir = path + "/"
            assert path in zip_contents or path_dir in zip_contents, (
                f"Expected content missing: {expected_file}"
            )
        else:
            assert path in zip_contents, f"Expected content missing: {expected_file}"

    def test_references_directory_has_content(self, zip_contents):
        ref_files = [
            name for name in zip_contents
            if name.startswith("life-planning-coach/references/") and not name.endswith("/")
        ]
        assert len(ref_files) > 0, (
            "references/ directory is empty. It should contain methodologies and guides."
        )


class TestBuildScriptIntegrity:
    """Verify the build script is executable and produces correct output."""

    def test_build_script_exists(self):
        script = PROJECT_ROOT / "scripts" / "build-skill.sh"
        assert script.exists(), f"Build script not found: {script}"

    def test_build_script_is_executable(self):
        script = PROJECT_ROOT / "scripts" / "build-skill.sh"
        assert os.access(script, os.X_OK), (
            f"Build script is not executable: {script}. Run: chmod +x {script}"
        )

    def test_zip_is_fresh(self):
        """
        ZIP should be newer than SKILL.md.
        If not, the build script may not have been run after the last edit.
        """
        zip_mtime = ZIP_PATH.stat().st_mtime
        skill_mtime = SKILL_MD_PATH.stat().st_mtime
        assert zip_mtime >= skill_mtime, (
            "ZIP is older than SKILL.md. Run scripts/build-skill.sh to rebuild."
        )
