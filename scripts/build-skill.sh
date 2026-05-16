#!/usr/bin/env bash
#
# Build script for the life-planning-coach.skill artifact.
# A .skill file is a renamed Markdown file with YAML frontmatter metadata.
#

set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_MD="${PROJECT_ROOT}/SKILL.md"
OUTPUT_FILE="${PROJECT_ROOT}/life-planning-coach.skill"

# ── 1. Validate source file exists ─────────────────────────────────────────────
if [[ ! -f "${SKILL_MD}" ]]; then
    echo "Error: SKILL.md not found at ${SKILL_MD}" >&2
    exit 1
fi

# ── 2. Parse frontmatter ─────────────────────────────────────────────────────
# Extract the YAML frontmatter block (content between the first two '---' lines)
frontmatter=$(sed -n '/^---$/,/^---$/p' "${SKILL_MD}" | sed '1d;$d')

if [[ -z "${frontmatter}" ]]; then
    echo "Error: SKILL.md is missing YAML frontmatter" >&2
    exit 1
fi

# Helper: extract a YAML key's value (handles quoted and unquoted values)
extract_value() {
    local key="$1"
    local raw
    raw=$(echo "${frontmatter}" | grep -E "^${key}:" | head -n 1)
    if [[ -z "${raw}" ]]; then
        echo ""
        return
    fi
    # Remove key and leading whitespace
    raw="${raw#*:}"
    raw="${raw# }"
    # Strip surrounding quotes if present
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

# ── 4. Build the artifact ────────────────────────────────────────────────────
cp "${SKILL_MD}" "${OUTPUT_FILE}"

# ── 5. Verify output ─────────────────────────────────────────────────────────
if [[ ! -f "${OUTPUT_FILE}" ]]; then
    echo "Error: Failed to create ${OUTPUT_FILE}" >&2
    exit 1
fi

# ── 6. Success ───────────────────────────────────────────────────────────────
echo "✓ Built life-planning-coach.skill (version ${skill_version})"
