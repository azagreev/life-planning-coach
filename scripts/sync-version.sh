#!/bin/bash
# ⚠ DEPRECATED in v1.0.0 — use `python scripts/build-skill.py version X.Y.Z`.
# Will be removed in v1.1. See MIGRATION_v1.md §3.
#
# sync-version.sh — Единый источник правды для версии проекта
#
# Источник правды: git tag (git describe --tags --abbrev=0)
# Этот скрипт синхронизирует версию во все файлы, где она должна совпадать.
#
# Использование:
#   bash scripts/sync-version.sh 0.7.0
#
# После запуска проверьте diff и закоммитьте изменения.

echo "⚠ DEPRECATED: bash scripts/sync-version.sh — use 'python scripts/build-skill.py version X.Y.Z' instead" >&2
echo "   See MIGRATION_v1.md §3. This wrapper will be removed in v1.1." >&2
echo "" >&2

set -euo pipefail

NEW_VERSION="${1:-}"

if [ -z "$NEW_VERSION" ]; then
    echo "Ошибка: не указана версия"
    echo "Использование: bash scripts/sync-version.sh 0.7.0"
    exit 1
fi

# Убираем префикс v если есть
NEW_VERSION="${NEW_VERSION#v}"

echo "=== Синхронизация версии $NEW_VERSION ==="

# 1. setup.py
echo "→ setup.py"
sed -i "s/version=\"[^\"]*\"/version=\"$NEW_VERSION\"/" setup.py

# 2. SKILL.md frontmatter (root and master)
echo "→ SKILL.md"
sed -i "s/^version: .*/version: $NEW_VERSION/" SKILL.md

echo "→ SKILL.master.md"
sed -i "s/^version: .*/version: $NEW_VERSION/" SKILL.master.md

# 3. README.md
echo "→ README.md"
sed -i "s/\*\*Версия:\*\* [0-9.]*/**Версия:** $NEW_VERSION/" README.md

# 4. AGENTS.md
echo "→ AGENTS.md"
sed -i "s/life-planning-coach v[0-9.]*/life-planning-coach v$NEW_VERSION/" AGENTS.md
sed -i "s/Title = только тег (\`v[0-9.]*\`)/Title = только тег (\`v$NEW_VERSION\`)/" AGENTS.md
sed -i "s/\*\*Версия:\*\* v[0-9.]*/**Версия:** v$NEW_VERSION/" AGENTS.md

# 5. ROADMAP.md «Текущая версия» line.
# Without this, tests/system/test_planning_docs_guardrails.py
# `test_roadmap_version_matches_latest_git_tag` fails right after release.sh
# creates the new tag (ROADMAP would still point to the previous version).
TODAY=$(date +%Y-%m-%d)
echo "→ ROADMAP.md (Текущая версия → v$NEW_VERSION, released $TODAY)"
sed -i "s/\*\*Текущая версия:\*\* \`v[0-9.]*\`/**Текущая версия:** \`v$NEW_VERSION\`/" ROADMAP.md
sed -i "s/(released [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\})/(released $TODAY)/" ROADMAP.md

# 6. Проверка: нет stale версий в других файлах
echo "→ Проверка на stale версии..."
STALE=$(grep -rn "version.*0\.[0-9]\+\.\?[0-9]*" --include="*.py" --include="*.md" --include="*.toml" . \
    | grep -v "node_modules" \
    | grep -v ".git/" \
    | grep -v "docs/archive/release/release_checklist_" \
    | grep -v "docs/archive/release/acceptance_criteria_" \
    | grep -v "docs/tasks/" \
    | grep -v "docs/planning/plan_" \
    | grep -v "docs/archive/PLAN" \
    | grep -v "docs/archive/plan_v" \
    | grep -v "docs/archive/VERSION_SOURCES.md" \
    | grep -v "docs/archive/RELEASE_NOTES_" \
    | grep -v "test_" \
    | grep -v "sync-version.sh" \
    | grep -v "$NEW_VERSION" \
    || true)

if [ -n "$STALE" ]; then
    echo "⚠️  Найдены stale версии (требуют проверки):"
    echo "$STALE"
else
    echo "✅ Stale версий не найдено"
fi

echo ""
echo "=== Синхронизация завершена ==="
echo "Проверьте изменения: git diff"
echo "Закоммитьте: git add -A && git commit -m 'bump version to $NEW_VERSION'"
