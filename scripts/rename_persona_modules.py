"""One-shot migration script for v0.19.0: rename persona modules to mode_<short> convention.

Mapping:
    references/adhd_mode.md               → references/mode_adhd.md
    references/time_structure_unemployed.md → references/mode_unemployed.md
    references/elder_homebound_mode.md    → references/mode_elder.md
    references/planning_friction_audit.md → references/mode_planning_friction.md

Operations:
    1. `git mv` each file (preserves history).
    2. Find-and-replace each old path (and bare basename) across all
       .md, .py, .yaml, .yml, .json files in repo.
    3. Skip: .git/, dist/, .build/, docs/archive/.

Usage:
    python scripts/rename_persona_modules.py            # dry-run by default
    python scripts/rename_persona_modules.py --apply    # actually rename + replace
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = REPO_ROOT / "references"

# old → new (basename only; paths constructed below)
RENAMES = {
    "adhd_mode.md": "mode_adhd.md",
    "time_structure_unemployed.md": "mode_unemployed.md",
    "elder_homebound_mode.md": "mode_elder.md",
    "planning_friction_audit.md": "mode_planning_friction.md",
}

# Replacements to perform across the repo (both with and without `references/` prefix).
# Order: longer/more-specific paths first so we don't partially replace.
REPLACEMENTS: list[tuple[str, str]] = []
for old, new in RENAMES.items():
    REPLACEMENTS.append((f"references/{old}", f"references/{new}"))
    # Also handle bare basenames in case some file refs just the filename.
    REPLACEMENTS.append((old, new))

# File globs to search through
SEARCH_EXTENSIONS = {".md", ".py", ".yaml", ".yml", ".json", ".sh"}

# Directories to skip (incl. archive — historical refs should not be rewritten)
SKIP_DIRS = {".git", "dist", ".build", "node_modules", ".pytest_cache", "__pycache__", "archive"}

# Specific files to skip (e.g. self — script defines old names as data)
SKIP_FILES = {"rename_persona_modules.py"}


def find_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix not in SEARCH_EXTENSIONS:
            continue
        files.append(path)
    return files


def replace_in_file(path: Path, dry_run: bool) -> int:
    content = path.read_text(encoding="utf-8")
    new_content = content
    total_replacements = 0
    for old, new in REPLACEMENTS:
        if old not in new_content:
            continue
        # Skip exact "new" tokens already present (idempotence)
        count = new_content.count(old)
        new_content = new_content.replace(old, new)
        total_replacements += count
    if total_replacements > 0 and not dry_run:
        path.write_text(new_content, encoding="utf-8")
    return total_replacements


def git_mv(old: Path, new: Path, dry_run: bool) -> bool:
    if not old.exists():
        print(f"  ⚠ source not found: {old.relative_to(REPO_ROOT)}")
        return False
    if new.exists():
        print(f"  ⚠ target already exists: {new.relative_to(REPO_ROOT)}")
        return False
    if dry_run:
        print(f"  [dry-run] git mv {old.relative_to(REPO_ROOT)} → {new.relative_to(REPO_ROOT)}")
        return True
    result = subprocess.run(
        ["git", "mv", str(old), str(new)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ✗ git mv failed: {result.stderr.strip()}")
        return False
    print(f"  ✓ git mv {old.name} → {new.name}")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Actually rename + replace (default is dry-run)")
    args = parser.parse_args()
    dry_run = not args.apply

    mode_label = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== Persona Module Rename ({mode_label}) ===\n")

    # Step 1: git mv files
    print("Step 1: Rename files via git mv...")
    rename_ok = True
    for old_name, new_name in RENAMES.items():
        old_path = REFERENCES / old_name
        new_path = REFERENCES / new_name
        if not git_mv(old_path, new_path, dry_run):
            # If git mv fails AND new file already exists → maybe already renamed earlier
            if (REFERENCES / new_name).exists():
                print(f"  ℹ already renamed: {new_name}")
            else:
                rename_ok = False

    if not rename_ok and not dry_run:
        print("\n✗ Some renames failed. Aborting cross-ref replacement.")
        sys.exit(1)

    # Step 2: replace refs across repo
    print("\nStep 2: Replace cross-references...")
    files = find_files()
    print(f"Scanning {len(files)} files...")
    total_files_changed = 0
    total_replacements = 0
    for f in files:
        count = replace_in_file(f, dry_run)
        if count > 0:
            rel = f.relative_to(REPO_ROOT)
            print(f"  {'[dry-run] ' if dry_run else ''}{count:3d} refs in {rel}")
            total_files_changed += 1
            total_replacements += count

    print(f"\n{'[dry-run] ' if dry_run else ''}Summary:")
    print(f"  Files changed: {total_files_changed}")
    print(f"  Total replacements: {total_replacements}")
    print(f"  Renamed files: {len(RENAMES)}")
    if dry_run:
        print("\nRe-run with --apply to actually perform changes.")


if __name__ == "__main__":
    main()
