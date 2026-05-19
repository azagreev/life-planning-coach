#!/bin/bash
# sync-version.sh — Единый источник правды для версии проекта
#
# Источник правды: git tag (git describe --tags --abbrev=0)
# Этот скрипт синхронизирует версию во все файлы, где она должна совпадать.
#
# Использование:
#   bash scripts/sync-version.sh 0.7.0
#
# После запуска проверьте diff и закоммитьте изменения.

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

# 4. Проверка: нет stale версий в других файлах
echo "→ Проверка на stale версии..."
STALE=$(grep -rn "version.*0\.[0-9]\+\.\?[0-9]*" --include="*.py" --include="*.md" --include="*.toml" . \
    | grep -v "node_modules" \
    | grep -v ".git/" \
    | grep -v "references/release_checklist_" \
    | grep -v "references/tasks/" \
    | grep -v "PLAN-FINAL.md" \
    | grep -v "VERSION_SOURCES.md" \
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
