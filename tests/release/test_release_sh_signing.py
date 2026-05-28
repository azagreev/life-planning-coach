"""
Regression tests for BUG-016: scripts/release.sh tag-signing robustness.

BUG-016 (v1.4.1 release): release.sh aborted at step 6 (`git tag -a`) AFTER the
irreversible step 4 (`git push origin main`), leaving a half-shipped release that
needed manual recovery. Cause: the repo's `tag.gpgSign=true` + a WSL signing-key
path (`/mnt/c/.../id_ed25519_github.pub`) that does NOT resolve under MSYS/
Git-Bash (where the key lives at `/c/.../id_ed25519_github.pub`).

Fix: `_resolve_tag_sign_args()` either remaps the signing-key path (WSL /mnt/c →
MSYS /c) or falls back to an UNSIGNED annotated tag, and is validated by a
throwaway-tag dry-run during PRECONDITIONS (before the push) so a signing/config
mismatch can never strand a release.

These tests guard:
  * the structural invariants of the fix (helpers present, override threaded into
    the real tag-create command, precondition runs before the push), and
  * the two behavioral mechanisms (path remap + unsigned fallback).
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASE_SH = PROJECT_ROOT / "scripts" / "release.sh"


def _find_bash():
    """Locate a bash that matches release.sh's runtime semantics.

    On Windows, `bash` on PATH may be WSL's System32 bash (where C:\\ lives at
    /mnt/c and env vars need WSLENV) — the wrong semantics for release.sh, which
    runs under Git-Bash/MSYS. Prefer Git-Bash's `bin/bash.exe`. Returns None if no
    suitable bash is found (→ behavioral tests skip). The behavioral tests invoke
    bash on a SCRIPT FILE (never `bash -c <str>`): under MSYS, args after `-c` are
    dropped and POSIX-looking literals in the `-c` string get path-mangled, whereas
    file content is read verbatim.
    """
    if os.name != "nt":
        return shutil.which("bash")
    candidates = []
    gitexe = shutil.which("git")
    if gitexe:
        p = Path(gitexe).resolve()
        # git may live at <Git>\cmd\git.exe or <Git>\mingw64\bin\git.exe
        for root in (p.parent.parent, p.parent.parent.parent):
            candidates.append(root / "bin" / "bash.exe")
    candidates += [
        Path(r"C:\Program Files\Git\bin\bash.exe"),
        Path(r"C:\Program Files (x86)\Git\bin\bash.exe"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    # Last resort: a PATH bash that is NOT WSL's System32 bash.
    w = shutil.which("bash")
    if w and "system32" not in w.lower():
        return w
    return None


BASH = _find_bash()


@pytest.fixture(scope="module")
def release_sh_text() -> str:
    assert RELEASE_SH.exists(), f"release.sh not found: {RELEASE_SH}"
    return RELEASE_SH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def release_sh_lines(release_sh_text) -> list:
    return release_sh_text.splitlines()


class TestBug016Presence:
    """Structural regression guards for the BUG-016 fix in release.sh."""

    def test_resolve_helper_defined(self, release_sh_text):
        assert "_resolve_tag_sign_args()" in release_sh_text, (
            "_resolve_tag_sign_args() helper missing — BUG-016 fix removed?"
        )

    def test_dry_run_helper_defined(self, release_sh_text):
        assert "_tag_dry_run()" in release_sh_text, (
            "_tag_dry_run() helper missing — tag creation is no longer pre-validated"
        )

    def test_wsl_to_msys_path_remap_present(self, release_sh_text):
        # WSL /mnt/c/... → MSYS /c/... via parameter expansion `/${key#/mnt/}`.
        assert "${key#/mnt/}" in release_sh_text, (
            "WSL→MSYS signing-key path remap removed"
        )

    def test_unsigned_fallback_present(self, release_sh_text):
        assert "tag.gpgSign=false" in release_sh_text, (
            "unsigned-annotated-tag fallback removed — the tag step can hard-fail again"
        )

    def test_dry_run_is_hang_guarded(self, release_sh_text):
        # A passphrase-protected SSH key must fail fast, not block on a prompt.
        assert "SSH_ASKPASS_REQUIRE=force" in release_sh_text, (
            "SSH askpass hang-guard removed from the tag dry-run"
        )
        assert "GIT_TERMINAL_PROMPT=0" in release_sh_text, (
            "terminal-prompt hang-guard removed from the tag dry-run"
        )

    def test_bug016_documented(self, release_sh_text):
        # Repo convention: keep the BUG-NNN comment-documentation in place.
        assert "BUG-016" in release_sh_text, (
            "BUG-016 documentation comment removed (repo convention: keep BUG-NNN notes)"
        )

    def test_sign_args_threaded_into_tag_create(self, release_sh_lines):
        # The resolved override MUST be on the actual annotated-tag create command,
        # otherwise step 6 ignores it and the original brittleness returns.
        create_lines = [
            line
            for line in release_sh_lines
            if 'tag -a "$TAG"' in line and "TAG_SIGN_ARGS" in line
        ]
        assert create_lines, (
            'TAG_SIGN_ARGS is not threaded into the `git ... tag -a "$TAG"` line; '
            "step 6 would ignore the resolved signing override"
        )


class TestBug016Ordering:
    """The signing precondition must run BEFORE the irreversible push (atomicity)."""

    def test_precondition_runs_before_push(self, release_sh_lines):
        def first_index(pred):
            return next(
                (i for i, line in enumerate(release_sh_lines) if pred(line)), None
            )

        # The *invocation* of the resolver: not its definition (`...() {`) and
        # not a comment line that merely mentions it.
        resolve_call = first_index(
            lambda line: "_resolve_tag_sign_args" in line
            and "()" not in line
            and not line.lstrip().startswith("#")
        )
        push_main = first_index(lambda line: line.strip() == "git push origin main")

        assert resolve_call is not None, "no _resolve_tag_sign_args invocation found"
        assert push_main is not None, "no `git push origin main` found"
        assert resolve_call < push_main, (
            "tag-signing precondition runs AFTER `git push origin main`; a signing/"
            "config mismatch could still strand a half-shipped release "
            f"(resolve@{resolve_call} push@{push_main})"
        )


@pytest.mark.skipif(BASH is None, reason="no Git-Bash/MSYS bash available")
class TestBug016Behavioral:
    """Exercise the two BUG-016 mechanisms via bash, not just by text matching.

    All bash is run on a SCRIPT FILE (never `bash -c <str>`): under Windows MSYS,
    args after `-c` are dropped and POSIX-looking literals in the `-c` string get
    path-mangled, whereas file content is read verbatim. Inputs that vary per run
    are interpolated into the script (single-quoted) rather than passed as args.
    """

    @staticmethod
    def _run_script(tmp_path, name, body):
        script = tmp_path / name
        script.write_text(body, encoding="utf-8")
        return subprocess.run(
            [BASH, str(script).replace("\\", "/")],
            capture_output=True,
            text=True,
            timeout=120,
        )

    def test_wsl_path_remap_micro(self, tmp_path):
        """`/${key#/mnt/}` turns a WSL signing-key path into its MSYS equivalent."""
        body = (
            'key="/mnt/c/Users/x/.ssh/id_ed25519_github.pub"\n'
            'printf "%s" "/${key#/mnt/}"\n'
        )
        result = self._run_script(tmp_path, "remap.sh", body)
        assert result.returncode == 0, result.stderr
        assert result.stdout == "/c/Users/x/.ssh/id_ed25519_github.pub"

    @pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
    def test_unsigned_fallback_creates_tag(self, tmp_path, release_sh_lines):
        """
        With a broken SSH signing config (signing key file does not exist),
        _resolve_tag_sign_args must fall back to an UNSIGNED annotated tag so the
        tag step still succeeds — never a hard-fail (the core BUG-016 property).
        """
        # Extract just the helper block (array init + the two functions) so that
        # running it has NO side effects — it must not run the release flow or
        # invoke _select_python. Anchors: the top-level `TAG_SIGN_ARGS=()`
        # assignment through the line just before `echo "=== Release ...`.
        start = next(
            i for i, line in enumerate(release_sh_lines) if line == "TAG_SIGN_ARGS=()"
        )
        end = next(
            i
            for i, line in enumerate(release_sh_lines)
            if line.startswith('echo "=== Release')
        )
        helpers = "\n".join(release_sh_lines[start:end]) + "\n"

        # Throwaway git repo with a single commit for the annotated tag to point at.
        repo = tmp_path / "repo"
        repo.mkdir()
        repo_posix = str(repo).replace("\\", "/")
        # A signing key that does NOT exist and is not /mnt/?/*, so the remap branch
        # is skipped and the dry-run drives _resolve_tag_sign_args to the fallback.
        signing_key = f"{repo_posix}/nonexistent_signing_key.pub"

        def git(*args):
            subprocess.run(
                ["git", *args],
                cwd=repo,
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
            )

        git("init", "-q")
        # Identity via LOCAL repo config so the annotated-tag tagger resolves without
        # depending on global/env config (`git tag -a` needs a tagger identity).
        git("config", "user.email", "test@example.com")
        git("config", "user.name", "Release Test")
        git("config", "tag.gpgSign", "true")
        git("config", "gpg.format", "ssh")
        git("config", "user.signingkey", signing_key)
        git("commit", "--allow-empty", "-q", "-m", "init")

        # Driver runs under `set -u` to mirror release.sh's `set -euo pipefail` and
        # to prove the `${arr[@]+"${arr[@]}"}` idiom is safe with the populated array.
        # The helper block is embedded directly; the repo path is single-quoted in.
        driver = (
            "set -u\n"
            + helpers
            + f"cd '{repo_posix}'\n"
            "if _resolve_tag_sign_args; then echo RESOLVE_OK; else echo RESOLVE_FAIL; fi\n"
            'echo "ARGS=${TAG_SIGN_ARGS[*]+${TAG_SIGN_ARGS[*]}}"\n'
            'git ${TAG_SIGN_ARGS[@]+"${TAG_SIGN_ARGS[@]}"} tag -a btag -m btag </dev/null '
            "&& echo TAG_OK\n"
            "git tag -l\n"
        )
        result = self._run_script(tmp_path, "driver.sh", driver)
        out = result.stdout

        assert "RESOLVE_OK" in out, (
            f"_resolve_tag_sign_args returned non-zero.\nSTDOUT:\n{out}\nSTDERR:\n{result.stderr}"
        )
        assert "TAG_OK" in out, (
            "annotated tag was NOT created despite a broken signing config — "
            f"BUG-016 hard-fail regression.\nSTDOUT:\n{out}\nSTDERR:\n{result.stderr}"
        )
        assert "btag" in out, (
            f"tag 'btag' missing from `git tag -l`.\nSTDOUT:\n{out}\nSTDERR:\n{result.stderr}"
        )
        assert "tag.gpgSign=false" in out, (
            "unsigned fallback was not engaged (expected `-c tag.gpgSign=false` in "
            f"TAG_SIGN_ARGS).\nSTDOUT:\n{out}\nSTDERR:\n{result.stderr}"
        )
