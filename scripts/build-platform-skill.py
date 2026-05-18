#!/usr/bin/env python3
"""
Build platform-specific SKILL.md files from SKILL.master.md + platform overlays.

Usage:
    python3 scripts/build-platform-skill.py [claude|grok|kimi|all]

Outputs:
    platforms/{platform}/SKILL.md
"""

import re
import sys
import yaml
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.resolve()
MASTER_PATH = PROJECT_ROOT / "SKILL.master.md"
OVERLAY_DIR = PROJECT_ROOT / "references" / "platforms"
OUTPUT_DIR = PROJECT_ROOT / "platforms"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown text."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found in master file")
    frontmatter = yaml.safe_load(match.group(1)) or {}
    body = match.group(2)
    return frontmatter, body


def serialize_frontmatter(frontmatter: dict) -> str:
    """Serialize dict to YAML frontmatter string."""
    # Custom serialization to preserve order and avoid anchors
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, str) and (":" in value or value.startswith("[") or "\n" in value):
            lines.append(f'{key}: >-')
            for line in value.splitlines():
                lines.append(f"  {line}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def apply_replacements(body: str, replacements: list[dict]) -> str:
    """Apply ordered string replacements to body."""
    for rep in replacements:
        old = rep["old"]
        new = rep["new"]
        if old in body:
            body = body.replace(old, new)
        else:
            print(f"  ⚠ Warning: replacement target not found: {old[:60]}...", file=sys.stderr)
    return body


def apply_frontmatter_changes(frontmatter: dict, overlay: dict) -> dict:
    """Apply frontmatter additions and removals from overlay."""
    result = dict(frontmatter)

    # Remove fields
    for key in overlay.get("frontmatter_remove", []):
        result.pop(key, None)

    # Add/override fields
    for key, value in overlay.get("frontmatter_add", {}).items():
        result[key] = value

    return result


def build_platform(platform: str) -> Path:
    """Build SKILL.md for a single platform."""
    print(f"Building {platform}...")

    # Read master
    master_text = MASTER_PATH.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(master_text)

    # Read overlay
    overlay_path = OVERLAY_DIR / f"{platform}.overlay.yaml"
    if not overlay_path.exists():
        raise FileNotFoundError(f"Overlay not found: {overlay_path}")
    overlay = yaml.safe_load(overlay_path.read_text(encoding="utf-8")) or {}

    # Apply frontmatter changes
    frontmatter = apply_frontmatter_changes(frontmatter, overlay)

    # Apply body replacements
    body = apply_replacements(body, overlay.get("replacements", []))

    # Append extra sections
    append_text = overlay.get("append_after_privacy", "")
    if append_text:
        body = body.rstrip() + "\n\n" + append_text.strip() + "\n"

    # Ensure output dir
    platform_dir = OUTPUT_DIR / platform
    platform_dir.mkdir(parents=True, exist_ok=True)

    # Write output
    output_path = platform_dir / "SKILL.md"
    output_text = serialize_frontmatter(frontmatter) + "\n" + body
    output_path.write_text(output_text, encoding="utf-8")

    # Stats
    line_count = len(output_text.splitlines())
    word_count = len(output_text.split())
    print(f"  ✓ {output_path} ({line_count} lines, {word_count} words)")

    return output_path


def main():
    platforms = ["claude", "grok", "kimi"]

    if len(sys.argv) < 2 or sys.argv[1] == "all":
        targets = platforms
    else:
        targets = [p for p in sys.argv[1:] if p in platforms]
        if not targets:
            print(f"Usage: {sys.argv[0]} [claude|grok|kimi|all]", file=sys.stderr)
            sys.exit(1)

    for platform in targets:
        build_platform(platform)

    print("\nDone.")


if __name__ == "__main__":
    main()
