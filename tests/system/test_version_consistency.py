"""
System tests for version consistency across project files.

These tests prevent version desynchronization — the root cause of:
- README.md showing stale version
- pyproject.toml never being updated
- Multiple sources of truth
"""

import subprocess
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestVersionConsistency:
    """Ensure all version sources point to the same version."""

    @pytest.fixture(scope="class")
    def git_tag_version(self):
        """Get version from git tag (source of truth)."""
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        tag = result.stdout.strip()
        # Remove 'v' prefix if present
        return tag.lstrip("v")

    def test_setup_py_version_matches_git_tag(self, git_tag_version):
        """setup.py version must match git tag."""
        setup_py = PROJECT_ROOT / "setup.py"
        content = setup_py.read_text(encoding="utf-8")
        match = re.search(r'version="([^"]+)"', content)
        assert match, "Version not found in setup.py"
        assert match.group(1) == git_tag_version, (
            f"setup.py version {match.group(1)} != git tag {git_tag_version}"
        )

    def test_skill_md_version_matches_git_tag(self, git_tag_version):
        """SKILL.md frontmatter version must match git tag."""
        skill_md = PROJECT_ROOT / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        match = re.search(r'^version:\s*([0-9.]+)', content, re.MULTILINE)
        assert match, "Version not found in SKILL.md frontmatter"
        assert match.group(1) == git_tag_version, (
            f"SKILL.md version {match.group(1)} != git tag {git_tag_version}"
        )

    def test_readme_version_matches_git_tag(self, git_tag_version):
        """README.md version badge must match git tag."""
        readme = PROJECT_ROOT / "README.md"
        content = readme.read_text(encoding="utf-8")
        match = re.search(r'\*\*Версия:\*\*\s*([0-9.]+)', content)
        assert match, "Version not found in README.md"
        assert match.group(1) == git_tag_version, (
            f"README.md version {match.group(1)} != git tag {git_tag_version}"
        )

    def test_agents_md_version_matches_git_tag(self, git_tag_version):
        """AGENTS.md version must match git tag."""
        agents_md = PROJECT_ROOT / "AGENTS.md"
        content = agents_md.read_text(encoding="utf-8")
        match = re.search(r'\*\*Версия:\*\*\s*v?([0-9.]+)', content)
        assert match, "Version not found in AGENTS.md"
        assert match.group(1) == git_tag_version, (
            f"AGENTS.md version {match.group(1)} != git tag {git_tag_version}"
        )

    def test_no_pyproject_toml_exists(self):
        """pyproject.toml must not exist (was removed as duplicate)."""
        pyproject = PROJECT_ROOT / "pyproject.toml"
        assert not pyproject.exists(), (
            "pyproject.toml exists but was removed as duplicate of setup.py. "
            "Use setup.py as single source for package metadata."
        )

    def test_no_stale_versions_in_source_files(self, git_tag_version):
        """No source file should contain a version different from git tag."""
        # Files to check (excluding archives, tests, docs)
        source_files = [
            PROJECT_ROOT / "setup.py",
            PROJECT_ROOT / "SKILL.md",
            PROJECT_ROOT / "README.md",
        ]

        for filepath in source_files:
            content = filepath.read_text(encoding="utf-8")
            # Find all version-like strings (X.Y or X.Y.Z)
            versions = re.findall(r'[\"\']?([0-9]+\.[0-9]+(?:\.[0-9]+)?)[\"\']?', content)
            for v in versions:
                if v != git_tag_version:
                    # Allow references to historical versions in comments
                    if "# bump:" in content or "архив" in content.lower():
                        continue
                    # Allow Python version requirements (e.g. python_requires>=3.9)
                    if v.startswith("3.") or v.startswith("2."):
                        continue
                    pytest.fail(
                        f"Stale version {v} found in {filepath.name} "
                        f"(expected {git_tag_version})"
                    )


class TestReleaseIntegrity:
    """Ensure release artifacts meet quality standards."""

    @pytest.mark.skip(
        reason="Post-release verification: run after creating GitHub Release"
    )
    def test_github_release_exists_for_tag(self):
        """GitHub Release must exist for current git tag."""
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        tag = result.stdout.strip()

        gh_result = subprocess.run(
            ["gh", "release", "view", tag, "--json", "tagName"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert gh_result.returncode == 0, (
            f"GitHub Release for {tag} does not exist. "
            f"Create it with: gh release create {tag} --notes-file RELEASE_NOTES.md"
        )

    @pytest.mark.skip(
        reason="Optional: requires gh CLI and network. Run manually before release."
    )
    def test_github_release_contains_russian(self):
        """GitHub Release body should contain Cyrillic characters (Russian)."""
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        tag = result.stdout.strip()

        gh_result = subprocess.run(
            ["gh", "release", "view", tag, "--json", "body"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        body = gh_result.stdout
        # Check for Cyrillic characters
        has_cyrillic = bool(re.search(r'[\u0400-\u04FF]', body))
        assert has_cyrillic, (
            f"GitHub Release {tag} body does not contain Russian text. "
            f"Release notes must be in Russian."
        )
