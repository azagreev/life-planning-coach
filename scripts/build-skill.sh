#!/usr/bin/env bash
#
# Build script for the life-planning-coach skill artifact.
# Creates a ZIP archive of the skill folder per Anthropic's official requirements:
# https://support.claude.com/en/articles/12512180-use-skills-in-claude
#
# The ZIP must contain the skill folder at the root level, not just SKILL.md.

set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_MD="${PROJECT_ROOT}/SKILL.md"
BUILD_DIR="${PROJECT_ROOT}/.build"
DIST_DIR="${PROJECT_ROOT}/dist"
SKILL_FOLDER="${BUILD_DIR}/life-planning-coach"
OUTPUT_ZIP="${DIST_DIR}/life-planning-coach-v${skill_version}.zip"
OUTPUT_SKILL="${DIST_DIR}/life-planning-coach-v${skill_version}.skill"
mkdir -p "${DIST_DIR}"

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

if [[ -z "${requires_mcp}" ]]; then
    echo "Error: Frontmatter is missing required field 'requires_mcp'" >&2
    errors=$((errors + 1))
fi

if [[ ${errors} -gt 0 ]]; then
    exit 1
fi

# ── 4. Clean and create build directory ──────────────────────────────────────
rm -rf "${BUILD_DIR}"
mkdir -p "${SKILL_FOLDER}"

# ── 5. Copy skill contents ───────────────────────────────────────────────────
# Required: SKILL.md
cp "${SKILL_MD}" "${SKILL_FOLDER}/SKILL.md"

# Required: README.md
cp "${PROJECT_ROOT}/README.md" "${SKILL_FOLDER}/README.md"

# Required: LICENSE
cp "${PROJECT_ROOT}/LICENSE" "${SKILL_FOLDER}/LICENSE"

# Required: CONTRIBUTING.md
cp "${PROJECT_ROOT}/CONTRIBUTING.md" "${SKILL_FOLDER}/CONTRIBUTING.md"

# Required: SECURITY.md
cp "${PROJECT_ROOT}/SECURITY.md" "${SKILL_FOLDER}/SECURITY.md"

# Optional: references/ (methodologies, guides, templates)
if [[ -d "${PROJECT_ROOT}/references" ]]; then
    cp -r "${PROJECT_ROOT}/references" "${SKILL_FOLDER}/references"
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

# ── 7. Create ZIP archive ────────────────────────────────────────────────────
rm -f "${OUTPUT_ZIP}"
(cd "${BUILD_DIR}" && zip -r "${OUTPUT_ZIP}" "life-planning-coach" >/dev/null)

# ── 8. Also create .skill file (same ZIP, alternative extension) ─────────────
cp "${OUTPUT_ZIP}" "${OUTPUT_SKILL}"

# ── 9. Verify outputs ────────────────────────────────────────────────────────
if [[ ! -f "${OUTPUT_ZIP}" ]]; then
    echo "Error: Failed to create ${OUTPUT_ZIP}" >&2
    exit 1
fi

zip_size=$(du -h "${OUTPUT_ZIP}" | cut -f1)

# ── 10. Success ──────────────────────────────────────────────────────────────
echo "✓ Built ${OUTPUT_ZIP} (version ${skill_version}, size: ${zip_size})"
echo "✓ Built ${OUTPUT_SKILL} (ZIP archive, same content)"
echo ""
echo "Upload to Claude.ai:"
echo "  1. Settings → Capabilities → enable 'Code execution and file creation'"
echo "  2. Customize → Skills → '+' → 'Upload a skill'"
echo "  3. Select: ${OUTPUT_ZIP} (or ${OUTPUT_SKILL})"
echo ""
echo "Or attach to GitHub Release:"
echo "  gh release upload v${skill_version} ${OUTPUT_ZIP} ${OUTPUT_SKILL}"
