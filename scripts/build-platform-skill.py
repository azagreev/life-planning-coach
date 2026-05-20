#!/usr/bin/env python3
"""
Build platform-specific SKILL.md files from SKILL.master.md + platform overlays.

Usage:
    python3 scripts/build-platform-skill.py [claude|grok|kimi|all]

Outputs:
    platforms/{platform}/SKILL.md
"""

import os
import re
import sys
import yaml
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.resolve()
MASTER_PATH = PROJECT_ROOT / "SKILL.master.md"
OVERLAY_DIR = PROJECT_ROOT / "references" / "platforms"
OUTPUT_DIR = PROJECT_ROOT / "platforms"
REFERENCES_DIR = PROJECT_ROOT / "references"

PLATFORMS = ["claude", "grok", "kimi", "kimi-cli"]

# P0 critical references that must be inlined for single-file platforms
P0_REFS = [
    "diagnostic_methods.md",
    "communication_style.md",
    "authentic_goal_filter.md",
    "goal_architecture.md",
    "weekly_review.md",
    "habit_loop.md",
    "emotion_regulation.md",
    "dashboard_guide.md",
    "calendar_constants.md",
]


def detect_platform() -> str | None:
    """Auto-detect platform from environment.

    Checks (in order):
    1. Grok: /root/.grok/ exists or GROK_ENV is set
    2. Kimi: /app/.kimi/ exists or KIMI_ENV is set
    3. Claude: fallback if none detected
    """
    def _path_exists(path: str) -> bool:
        try:
            return Path(path).exists()
        except PermissionError:
            return False

    # Grok detection
    if _path_exists("/root/.grok") or os.environ.get("GROK_ENV"):
        return "grok"

    # Kimi detection
    if _path_exists("/app/.kimi") or os.environ.get("KIMI_ENV"):
        return "kimi"

    # Claude is default — no reliable env marker, but we can check for claude-specific paths
    if _path_exists("/tmp/claude") or os.environ.get("CLAUDE_ENV"):
        return "claude"

    return None


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


def demote_headings(text: str, levels: int = 2) -> str:
    """Demote all markdown headings by N levels (e.g., H1 -> H3)."""
    lines = text.split("\n")
    result = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("#"):
            # Count leading # characters
            hash_count = 0
            for ch in stripped:
                if ch == "#":
                    hash_count += 1
                else:
                    break
            new_level = hash_count + levels
            if new_level > 6:
                new_level = 6
            result.append("#" * new_level + stripped[hash_count:])
        else:
            result.append(line)
    return "\n".join(result)


def condense_markdown(text: str, aggressive: bool = False) -> str:
    """Condense a reference markdown file for inline inclusion."""
    lines = text.split("\n")
    result = []
    in_code = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Code blocks
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        # Tables
        if "|" in stripped and not stripped.startswith("#"):
            if "---" in stripped or "===" in stripped:
                continue
            if aggressive:
                continue
            if stripped.count("|") > 2:
                continue

        # Skip source/effect size/quotes/examples in aggressive mode
        if aggressive:
            if any(stripped.lower().startswith(x) for x in [
                "source:", "effect size:", "**source:**", "**effect size:**",
                "example:", "**example:**", "url:", "**url:**",
                "> **", '> "', "пример:", "примеры:",
                "исследования:", "research:", "научная база:"
            ]):
                continue
            if stripped.startswith(">"):
                continue
        else:
            if stripped.startswith("> **Source:**") or stripped.startswith("> **Effect size:**"):
                continue

        # Skip version/metainfo lines at top
        if stripped.startswith("> **Версия:**") or stripped.startswith("> **База:**") or stripped.startswith("> **Цель:**"):
            continue

        # Skip internal reference load instructions (these will be handled separately or are irrelevant when inlined)
        if re.search(r"(?i)(загрузи|прочитай|см\.?).*`references/[^`]+\.md`", stripped):
            continue

        result.append(line)

    return "\n".join(result)


def condense_dashboard(text: str) -> str:
    """Aggressively condense dashboard_guide.md for inline inclusion.

    Keep only:
    - Coaching Display Rules (how to present data)
    - JSON Data Contract (minimal example)
    - Integration notes with skill
    - Remove: CSS details, JS implementation, responsive design, a11y deep dives
    """
    lines = text.split("\n")
    result = []
    in_code = False
    keep_section = False
    section_name = ""

    for line in lines:
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            in_code = not in_code
            if not in_code:
                continue
            # Keep code blocks only if they contain JSON examples
            if "json" in stripped.lower():
                keep_section = True
            else:
                keep_section = False
            continue
        if in_code:
            if keep_section:
                result.append(line)
            continue

        # Identify sections to keep
        if stripped.startswith("#"):
            section_name = stripped.lower()
            # Keep sections related to coaching display, data contract, integration
            keep_section = any(kw in section_name for kw in [
                "display rule", "data contract", "json", "integration",
                "coaching", "skill integration", "how to use"
            ])
            if keep_section:
                result.append(line)
            continue

        if keep_section:
            # Skip CSS/JS implementation details
            if any(kw in stripped.lower() for kw in [
                "css", "javascript", "@media", "flexbox", "grid",
                "webkit", "moz-", "backdrop-filter", "echarts"
            ]):
                continue
            result.append(line)

    return "\n".join(result)


def ultra_condense(text: str) -> str:
    """Keep only H1/H2 headers and bullet points under them."""
    lines = text.split("\n")
    result = []
    in_code = False
    keep_bullets = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Keep H1/H2
        if stripped.startswith("# ") or stripped.startswith("## "):
            result.append(line)
            keep_bullets = True
            continue
        # Keep bullet points under headers
        if keep_bullets and (stripped.startswith("- ") or stripped.startswith("* ") or stripped.startswith("1.")):
            result.append(line)
            continue
        # Keep H3 if aggressive
        if stripped.startswith("### ") and len(result) < 50:
            result.append(line)
            continue

    return "\n".join(result)


def inline_references(skill_text: str, platform: str) -> str:
    """Inline P0 critical references into a single-file platform skill."""
    ref_pattern = r"`references/([^`]+\.md)`"
    refs = set(re.findall(ref_pattern, skill_text))

    for ref in sorted(refs):
        ref_path = REFERENCES_DIR / ref
        if not ref_path.exists():
            continue

        # Only inline P0 critical refs
        if ref not in P0_REFS:
            # Replace "Загрузи" with neutral "См." for non-inlined refs
            # Handle markdown decoration around the keyword: **Загрузи** or _загрузи_
            skill_text = re.sub(
                rf"(?i)[*_]*\s*(загрузи|прочитай|см\.?)\s*[_*]*\s*`references/{re.escape(ref)}`",
                rf"См. `references/{ref}`",
                skill_text,
            )
            continue

        content = ref_path.read_text(encoding="utf-8")

        # Choose condensation level
        if ref == "dashboard_guide.md":
            # Custom condensation for dashboard: keep only coaching display rules + JSON contract
            condensed = condense_dashboard(content)
        elif platform == "kimi":
            condensed = ultra_condense(content)
        else:
            condensed = condense_markdown(content, aggressive=False)

        if not condensed.strip():
            continue

        # Demote headings to preserve hierarchy (H1 -> H3, H2 -> H4)
        condensed = demote_headings(condensed, levels=2)

        # Build inline block
        if platform == "grok":
            inline_block = (
                f"<!-- INLINED REF: {ref} -->\n"
                f"<details>\n"
                f"<summary>📄 {ref.replace('.md', '')} (полный протокол)</summary>\n\n"
                f"{condensed}\n\n"
                f"</details>\n"
                f"<!-- END INLINED REF: {ref} -->"
            )
        else:
            inline_block = (
                f"<!-- INLINED REF: {ref} -->\n"
                f"## 📄 {ref.replace('.md', '')}\n\n"
                f"{condensed}\n\n"
                f"<!-- END INLINED REF: {ref} -->"
            )

        # Replace the reference load instruction
        lines = skill_text.split("\n")
        new_lines = []
        replaced = False
        for line in lines:
            if f"`references/{ref}`" in line and not replaced:
                if any(kw in line.lower() for kw in ["загрузи", "see", "read", "прочитай"]):
                    new_lines.append(inline_block)
                    replaced = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        skill_text = "\n".join(new_lines)

    return skill_text


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

    # Inline references for single-file platforms (grok, kimi)
    if platform in ("grok", "kimi"):
        full_text = serialize_frontmatter(frontmatter) + "\n" + body
        full_text = inline_references(full_text, platform)
        # Remove platform-specific references (Claude, Anthropic) from inlined content
        full_text = full_text.replace("Claude предлагает", "AI предлагает")
        full_text = full_text.replace("(для Claude-чата)", "(для чата)")
        # Re-extract frontmatter and body
        frontmatter, body = parse_frontmatter(full_text)

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


def print_usage():
    print(f"Usage: {sys.argv[0]} [claude|grok|kimi|all|--detect]", file=sys.stderr)
    print("", file=sys.stderr)
    print("Options:", file=sys.stderr)
    print("  claude|grok|kimi    Build skill for specific platform", file=sys.stderr)
    print("  all                 Build skills for all platforms (default)", file=sys.stderr)
    print("  --detect            Auto-detect platform from environment", file=sys.stderr)
    print("", file=sys.stderr)
    print("Auto-detect heuristics:", file=sys.stderr)
    print("  Grok: /root/.grok exists or GROK_ENV is set", file=sys.stderr)
    print("  Kimi: /app/.kimi exists or KIMI_ENV is set", file=sys.stderr)
    print("  Claude: fallback (no reliable env marker)", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        # Default: build all
        targets = PLATFORMS
    elif sys.argv[1] in ("-h", "--help"):
        print_usage()
        sys.exit(0)
    elif sys.argv[1] == "--detect":
        detected = detect_platform()
        if detected:
            print(f"Detected platform: {detected}")
            targets = [detected]
        else:
            print("Could not auto-detect platform. Falling back to 'all'.", file=sys.stderr)
            targets = PLATFORMS
    elif sys.argv[1] == "all":
        targets = PLATFORMS
    else:
        targets = [p for p in sys.argv[1:] if p in PLATFORMS]
        if not targets:
            print_usage()
            sys.exit(1)

    for platform in targets:
        build_platform(platform)

    print("\nDone.")


if __name__ == "__main__":
    main()
