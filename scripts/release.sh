#!/bin/bash
# release.sh — Атомарный скрипт релиза
#
# Выполняет полный цикл релиза в правильном порядке:
# 1. Проверка preconditions
# 2. Синхронизация версии
# 3. Коммит
# 4. Push на GitHub
# 5. Проверка на GitHub
# 6. Создание тега
# 7. Создание GitHub Release
#
# Использование:
#   bash scripts/release.sh 0.7.0

set -euo pipefail

VERSION="${1:-}"
REPO="azagreev/life-planning-coach"

if [ -z "$VERSION" ]; then
    echo "Ошибка: не указана версия"
    echo "Использование: bash scripts/release.sh 0.7.0"
    exit 1
fi

# Убираем префикс v если есть
VERSION="${VERSION#v}"
TAG="v$VERSION"

echo "=== Release $TAG ==="

# ── 1. PRECONDITION CHECKS ──
echo ""
echo "[1/7] Проверка preconditions..."

# Проверка: все тесты проходят
echo "→ Запуск тестов..."
if ! pytest tests/release/ tests/system/ -q --tb=short; then
    echo "❌ Тесты не проходят. Исправьте перед релизом."
    exit 1
fi
echo "✅ Тесты проходят"

# Проверка: нет незакоммиченных изменений
if ! git diff-index --quiet HEAD --; then
    echo "❌ Есть незакоммиченные изменения:"
    git status --short
    exit 1
fi
echo "✅ Рабочая директория чиста"

# Проверка: мы на main
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "❌ Не на ветке main (сейчас: $CURRENT_BRANCH)"
    exit 1
fi
echo "✅ На ветке main"

# ── 2. VERSION SYNC ──
echo ""
echo "[2/7] Синхронизация версии..."
bash scripts/sync-version.sh "$VERSION"

# ── 3. COMMIT ──
echo ""
echo "[3/7] Коммит..."
if git diff-index --quiet HEAD --; then
    echo "ℹ️  Нет изменений для коммита (версия уже синхронизирована)"
else
    git add -A
    git commit -m "release: bump version to $VERSION"
    echo "✅ Коммит создан"
fi

# ── 4. PUSH ──
echo ""
echo "[4/7] Push на GitHub..."
git push origin main
echo "✅ Push выполнен"

# ── 5. GITHUB VERIFICATION ──
echo ""
echo "[5/7] Проверка на GitHub..."
# Ждём 3 секунды для репликации GitHub
sleep 3

# Проверяем версию в README на GitHub
GITHUB_README=$(gh api "repos/$REPO/contents/README.md" --jq '.content' | python3 -c "import sys, base64; print(base64.b64decode(sys.stdin.read()).decode('utf-8'))" | grep -oP '\*\*Версия:\*\*\s*\K[0-9.]+' || true)

if [ "$GITHUB_README" != "$VERSION" ]; then
    echo "❌ Версия на GitHub ($GITHUB_README) ≠ ожидаемой ($VERSION)"
    echo "   Возможно, push не успел примениться. Подождите и проверьте вручную."
    exit 1
fi
echo "✅ Версия на GitHub проверена: $GITHUB_README"

# ── 6. TAG ──
echo ""
echo "[6/7] Создание тега..."
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "⚠️  Тег $TAG уже существует"
else
    git tag "$TAG"
    git push origin "$TAG"
    echo "✅ Тег $TAG создан и запушен"
fi

# ── 7. GITHUB RELEASE ──
echo ""
echo "[7/7] GitHub Release..."

# Проверяем, существует ли release
if gh release view "$TAG" >/dev/null 2>&1; then
    echo "⚠️  Release $TAG уже существует"
else
    RELEASE_NOTES_FILE="references/archive/RELEASE_NOTES_$TAG.md"
    if [ -f "$RELEASE_NOTES_FILE" ]; then
        # Title = tag only (minimalist format, as React/Node.js do)
        # Release notes contain the full description
        gh release create "$TAG" \
            --title "$TAG" \
            --notes-file "$RELEASE_NOTES_FILE" \
            life-planning-coach.zip \
            life-planning-coach.skill
        echo "✅ Release $TAG создан из $RELEASE_NOTES_FILE"
    else
        echo "⚠️  Файл $RELEASE_NOTES_FILE не найден"
        echo "   Создайте его на русском языке и запустите:"
        echo "   gh release create $TAG --notes-file $RELEASE_NOTES_FILE"
        exit 1
    fi
fi

echo ""
echo "=== Релиз $TAG завершён ==="
echo "Проверьте: https://github.com/$REPO/releases/tag/$TAG"
