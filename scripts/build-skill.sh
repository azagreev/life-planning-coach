#!/usr/bin/env bash
#
# ⚠ DEPRECATED in v1.0.0 — use `python scripts/build-skill.py build`.
# Will be removed in v1.1. See MIGRATION_v1.md §3.
#
# Build script for the life-planning-coach skill artifact.
# Creates a ZIP archive of the skill folder per Anthropic's official requirements:
# https://support.claude.com/en/articles/12512180-use-skills-in-claude
#
# The ZIP must contain the skill folder at the root level, not just SKILL.md.

echo "⚠ DEPRECATED: bash scripts/build-skill.sh — use 'python scripts/build-skill.py build' instead" >&2
echo "   See MIGRATION_v1.md §3. This wrapper will be removed in v1.1." >&2
echo "" >&2

set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_MD="${PROJECT_ROOT}/SKILL.md"
BUILD_DIR="${PROJECT_ROOT}/.build"
DIST_DIR="${PROJECT_ROOT}/dist"
SKILL_FOLDER="${BUILD_DIR}/life-planning-coach"

# ── 0. Generate platform-specific skills ─────────────────────────────────────
echo "Generating platform skills..."
# Detect python interpreter. On Windows, /WindowsApps/python3 is the MS Store
# stub launcher that returns exit 9009 with "Python " stderr — useless.
# Prefer real python that responds to --version.
pick_python() {
    for candidate in "${PYTHON:-}" python3 python py; do
        [ -z "$candidate" ] && continue
        if "$candidate" --version >/dev/null 2>&1; then
            echo "$candidate"
            return 0
        fi
    done
    echo "python3"  # last-resort fallback
}
PYTHON_BIN="$(pick_python)"
# Force UTF-8 stdio so emoji in build output don't crash cp1251 console (Windows).
PYTHONIOENCODING=utf-8 "$PYTHON_BIN" "${SCRIPT_DIR}/build-platform-skill.py" all

# ── 0.5. Sync Claude skill to root SKILL.md (backward compatibility) ──────────
cp "${PROJECT_ROOT}/platforms/claude/SKILL.md" "${SKILL_MD}"

# ── 1. Validate source file exists ─────────────────────────────────────────────
if [[ ! -f "${SKILL_MD}" ]]; then
    echo "Error: SKILL.md not found at ${SKILL_MD}" >&2
    exit 1
fi

# ── 2. Parse frontmatter ─────────────────────────────────────────────────────
frontmatter=$(sed -n '/^---$/,/^---$/p' "${SKILL_MD}" | sed '1d;$d')

if [[ -z "${frontmatter}" ]]; then
    echo "Error: SKILL.md is missing YAML frontmatter" >&2
    exit 1
fi

extract_value() {
    local key="$1"
    local raw
    raw=$(echo "${frontmatter}" | grep -E "^${key}:" | head -n 1)
    if [[ -z "${raw}" ]]; then
        echo ""
        return
    fi
    raw="${raw#*:}"
    raw="${raw# }"
    raw="${raw%\"}"
    raw="${raw#\"}"
    raw="${raw%\'}"
    raw="${raw#\'}"
    echo "${raw}"
}

skill_name=$(extract_value "name")
skill_version=$(extract_value "version")
requires_mcp=$(extract_value "requires_mcp")

# ── 3. Validate required frontmatter fields ──────────────────────────────────
errors=0

if [[ -z "${skill_name}" ]]; then
    echo "Error: Frontmatter is missing required field 'name'" >&2
    errors=$((errors + 1))
fi

if [[ -z "${skill_version}" ]]; then
    echo "Error: Frontmatter is missing required field 'version'" >&2
    errors=$((errors + 1))
fi

# requires_mcp is optional for non-Claude platforms, but required for Claude ZIP
# We keep validation for backward compatibility of the Claude artifact

if [[ ${errors} -gt 0 ]]; then
    exit 1
fi

# ── 4. Clean and create build directory ──────────────────────────────────────
rm -rf "${BUILD_DIR}"
mkdir -p "${SKILL_FOLDER}"

# ── 5. Copy skill contents ───────────────────────────────────────────────────
# Required: SKILL.md (the only file Anthropic requires)
cp "${SKILL_MD}" "${SKILL_FOLDER}/SKILL.md"

# Optional: references/ (methodologies, guides, templates)
# Exclude dev-only content: acceptance criteria, plans, checklists, research, tasks, archive
if [[ -d "${PROJECT_ROOT}/references" ]]; then
    mkdir -p "${SKILL_FOLDER}/references"
    rsync -a \
        --exclude='acceptance_criteria_*' \
        --exclude='plan_v*.md' \
        --exclude='release_checklist_*.md' \
        --exclude='persistence_research_plan.md' \
        --exclude='research/' \
        --exclude='research_*.md' \
        --exclude='tasks/' \
        --exclude='archive/' \
        "${PROJECT_ROOT}/references/" "${SKILL_FOLDER}/references/"
fi

# Optional: dashboard HTML (used by skill)
if [[ -f "${PROJECT_ROOT}/life-planning-dashboard.html" ]]; then
    cp "${PROJECT_ROOT}/life-planning-dashboard.html" "${SKILL_FOLDER}/life-planning-dashboard.html"
fi

# ── 6. Validate skill folder structure ───────────────────────────────────────
if [[ ! -f "${SKILL_FOLDER}/SKILL.md" ]]; then
    echo "Error: SKILL.md not found in build folder" >&2
    exit 1
fi

# ── 7. Define output filenames (after version is parsed) ─────────────────────
OUTPUT_ZIP="${DIST_DIR}/life-planning-coach-v${skill_version}.zip"
OUTPUT_SKILL="${DIST_DIR}/life-planning-coach-v${skill_version}.skill"
mkdir -p "${DIST_DIR}"

# ── 8. Create ZIP archive ────────────────────────────────────────────────────
rm -f "${OUTPUT_ZIP}"
(cd "${BUILD_DIR}" && zip -r "${OUTPUT_ZIP}" "life-planning-coach" >/dev/null)

# ── 9. Also create .skill file (same ZIP, alternative extension) ─────────────
cp "${OUTPUT_ZIP}" "${OUTPUT_SKILL}"

# ── 9.5. Copy Grok and Kimi plain SKILL.md files to dist ─────────────────────
cp "${PROJECT_ROOT}/platforms/grok/SKILL.md" "${DIST_DIR}/life-planning-coach-v${skill_version}-grok.md"
cp "${PROJECT_ROOT}/platforms/kimi/SKILL.md" "${DIST_DIR}/life-planning-coach-v${skill_version}-kimi.md"

# ── 9.6. Copy Kimi CLI skill directory to dist ───────────────────────────────
KIMI_CLI_DIR="${DIST_DIR}/life-planning-coach-v${skill_version}-kimi-cli"
mkdir -p "${KIMI_CLI_DIR}"
cp "${PROJECT_ROOT}/platforms/kimi-cli/SKILL.md" "${KIMI_CLI_DIR}/SKILL.md"
if [[ -d "${PROJECT_ROOT}/references" ]]; then
    mkdir -p "${KIMI_CLI_DIR}/references"
    rsync -a \
        --exclude='acceptance_criteria_*' \
        --exclude='plan_v*.md' \
        --exclude='release_checklist_*.md' \
        --exclude='persistence_research_plan.md' \
        --exclude='research/' \
        --exclude='research_*.md' \
        --exclude='tasks/' \
        --exclude='archive/' \
        "${PROJECT_ROOT}/references/" "${KIMI_CLI_DIR}/references/"
fi
if [[ -f "${PROJECT_ROOT}/life-planning-dashboard.html" ]]; then
    cp "${PROJECT_ROOT}/life-planning-dashboard.html" "${KIMI_CLI_DIR}/life-planning-dashboard.html"
fi

# ── 9.7. Create Kimi CLI ZIP ─────────────────────────────────────────────────
KIMI_CLI_ZIP="${DIST_DIR}/life-planning-coach-v${skill_version}-kimi-cli.zip"
rm -f "${KIMI_CLI_ZIP}"
(cd "${DIST_DIR}" && zip -r "${KIMI_CLI_ZIP}" "life-planning-coach-v${skill_version}-kimi-cli" >/dev/null)

# ── 10. Verify outputs ───────────────────────────────────────────────────────
if [[ ! -f "${OUTPUT_ZIP}" ]]; then
    echo "Error: Failed to create ${OUTPUT_ZIP}" >&2
    exit 1
fi

zip_size=$(du -h "${OUTPUT_ZIP}" | cut -f1)

# ── 11. Success ──────────────────────────────────────────────────────────────
echo "✓ Built ${OUTPUT_ZIP} (version ${skill_version}, size: ${zip_size})"
echo "✓ Built ${OUTPUT_SKILL} (ZIP archive, same content)"
echo "✓ Built ${DIST_DIR}/life-planning-coach-v${skill_version}-grok.md (Grok xAI)"
echo "✓ Built ${DIST_DIR}/life-planning-coach-v${skill_version}-kimi.md (Kimi OK Computer)"
echo ""
echo "Upload to Claude.ai:"
echo "  1. Settings → Capabilities → enable 'Code execution and file creation'"
echo "  2. Customize → Skills → '+' → 'Upload a skill'"
echo "  3. Select: ${OUTPUT_ZIP} (or ${OUTPUT_SKILL})"
echo ""
echo "✓ Built ${DIST_DIR}/life-planning-coach-v${skill_version}-kimi-cli.zip (Kimi Code CLI)"
echo ""
echo "Upload to Claude.ai:"
echo "  1. Settings → Capabilities → enable 'Code execution and file creation'"
echo "  2. Customize → Skills → '+' → 'Upload a skill'"
echo "  3. Select: ${OUTPUT_ZIP} (or ${OUTPUT_SKILL})"
echo ""
echo "Grok (xAI): Copy SKILL.md content to /root/.grok/skills/life-planning-coach/SKILL.md"
echo "Kimi OK Computer: Copy SKILL.md content to /app/.kimi/skills/life-planning-coach/SKILL.md"
echo "Kimi Code CLI: Copy directory to ~/.kimi/skills/life-planning-coach/"
echo ""
echo "Or attach to GitHub Release:"
echo "  gh release upload v${skill_version} ${OUTPUT_ZIP} ${OUTPUT_SKILL} ${DIST_DIR}/life-planning-coach-v${skill_version}-grok.md ${DIST_DIR}/life-planning-coach-v${skill_version}-kimi.md"
