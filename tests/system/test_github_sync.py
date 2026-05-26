"""
System test for GitHub synchronization.

Ensures local repository is in sync with origin before declaring "done".
Root cause of: README.md shows 0.4.0 on GitHub while local was 0.6.0
"""

import subprocess

import pytest

from test_version_consistency import PROJECT_ROOT


class TestGitHubSync:
    """Ensure local repository is synchronized with GitHub."""

    def test_local_main_matches_origin_main(self):
        """Local main branch must be in sync with origin/main.

        This test prevents the scenario where:
        1. Developer commits locally
        2. Declares "done"
        3. GitHub still shows old version because push was forgotten
        """
        # Fetch latest from origin
        subprocess.run(
            ["git", "fetch", "origin", "main"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        # Get local and remote HEAD
        local = subprocess.run(
            ["git", "rev-parse", "main"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        remote = subprocess.run(
            ["git", "rev-parse", "origin/main"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        local_sha = local.stdout.strip()
        remote_sha = remote.stdout.strip()

        assert local_sha == remote_sha, (
            f"Local main ({local_sha[:8]}) ≠ origin/main ({remote_sha[:8]}). "
            f"Run: git push origin main"
        )

    def test_no_unpushed_commits(self):
        """There must be no unpushed commits on main."""
        result = subprocess.run(
            ["git", "rev-list", "origin/main..main", "--count"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        count = int(result.stdout.strip())

        assert count == 0, (
            f"{count} unpushed commit(s) on main. "
            f"Run: git push origin main"
        )

    def test_working_tree_is_clean(self):
        """Working tree must have no uncommitted changes."""
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        assert result.stdout.strip() == "", (
            "Working tree has uncommitted changes:\n"
            f"{result.stdout}"
            f"Run: git add -A && git commit"
        )

    @pytest.mark.skip(
        reason="Optional: requires network. Run manually before release."
    )
    def test_github_readme_version_matches_local(self):
        """README.md version on GitHub must match local version."""
        import base64

        # Get local version
        readme_local = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        import re
        local_match = re.search(r'\*\*Версия:\*\*\s*([0-9.]+)', readme_local)
        assert local_match, "Version not found in local README.md"
        local_version = local_match.group(1)

        # Get GitHub version
        gh_result = subprocess.run(
            ["gh", "api", "repos/azagreev/life-planning-coach/contents/README.md", "--jq", ".content"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        github_content = base64.b64decode(gh_result.stdout).decode("utf-8")
        github_match = re.search(r'\*\*Версия:\*\*\s*([0-9.]+)', github_content)
        assert github_match, "Version not found in GitHub README.md"
        github_version = github_match.group(1)

        assert local_version == github_version, (
            f"GitHub README version ({github_version}) ≠ local ({local_version}). "
            f"Push required: git push origin main"
        )

    def test_release_notes_generation(self, tmp_path):
        """extract-release-notes.py must create RELEASE_NOTES file from CHANGELOG.

        Regression test for: release.sh no longer generating RELEASE_NOTES file
        after commit 507ad1f, causing pre-push hook to deadlock.
        """
        # Use current version from git tag to test with real CHANGELOG data
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        current_tag = result.stdout.strip()
        current_version = current_tag.lstrip("v")

        # Output location moved from references/archive/ → docs/archive/ in v0.15.x
        expected_file = PROJECT_ROOT / "docs/archive" / f"RELEASE_NOTES_{current_tag}.md"
        file_existed_before = expected_file.exists()

        try:
            # Use sys.executable for cross-platform (Windows MS Store stub for python3
            # returns exit 9009; sys.executable is always the actual interpreter).
            # Force UTF-8 stdio so the script's ✅ output doesn't crash cp1251 console.
            import os
            import sys
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(
                [sys.executable, "scripts/extract-release-notes.py", current_version],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env,
                check=True,
            )

            assert expected_file.exists(), (
                f"RELEASE_NOTES file not created: {expected_file}\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

            content = expected_file.read_text(encoding="utf-8")
            assert f"## Что нового в {current_tag}" in content, (
                f"Expected header not found in {expected_file}"
            )
        finally:
            # Cleanup: remove only if we created it
            if not file_existed_before and expected_file.exists():
                expected_file.unlink()
