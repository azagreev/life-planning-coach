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

# ── 0. HOOK INSTALLATION ──
echo ""
echo "[0/7] Проверка git hooks..."

HOOK_SRC=".github/hooks/pre-push-release-guard"
HOOK_DST=".git/hooks/pre-push"

if [ -f "$HOOK_SRC" ]; then
    if [ ! -f "$HOOK_DST" ]; then
        echo "→ Установка pre-push hook..."
        cp "$HOOK_SRC" "$HOOK_DST"
        chmod +x "$HOOK_DST"
        echo "✅ pre-push hook установлен"
    elif ! diff -q "$HOOK_SRC" "$HOOK_DST" >/dev/null 2>&1; then
        echo "→ Обновление pre-push hook..."
        cp "$HOOK_SRC" "$HOOK_DST"
        chmod +x "$HOOK_DST"
        echo "✅ pre-push hook обновлён"
    else
        echo "✅ pre-push hook актуален"
    fi
else
    echo "⚠️  Шаблон hook'а не найден: $HOOK_SRC"
fi

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
# Используем git diff (porcelain) вместо git diff-index (plumbing), потому что
# porcelain с diff.autoRefreshIndex=true (default) корректно обрабатывает stat cache
# mismatch при core.filemode=false (типично для WSL/Windows).
# diff-index видит stat mismatch как dirty, даже если content идентичен.
if ! git diff --quiet HEAD; then
    echo "❌ Есть незакоммиченные изменения:"
    git status --short
    git diff --stat HEAD
    exit 1
fi
echo "✅ Рабочая директория чиста"

# Пересобираем артефакты после тестов, чтобы ZIP был свежим
# (pytest TestBuildScript может перезаписать platforms/*/SKILL.md, делая ZIP "устаревшим")
echo "→ Пересборка артефактов..."
bash scripts/build-skill.sh >/dev/null 2>&1 || true

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

# ── 2.5. UPDATE ROADMAP STATUS TABLE ──
echo ""
echo "[2.5/7] Обновление ROADMAP..."
ROADMAP_FILE="ROADMAP.md"
# Remove released version from status table (Option B: no Released rows in ROADMAP)
if grep -q "| v${VERSION} |" "$ROADMAP_FILE"; then
    sed -i "/| v${VERSION} |/d" "$ROADMAP_FILE"
    echo "✅ Удалена строка v${VERSION} из 'Текущий статус'"
else
    echo "ℹ️  Версия v${VERSION} не найдена в таблице статуса"
fi

# ── 3. COMMIT ──
echo ""
echo "[3/7] Коммит..."
if git diff --quiet HEAD; then
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
    echo "⚠️  Тег $TAG уже существует локально"
    git push origin "$TAG"
    echo "✅ Тег $TAG запушен"
else
    git tag -a "$TAG" -m "$TAG"
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
        ZIP_FILE="dist/life-planning-coach-v${VERSION}.zip"
        SKILL_FILE="dist/life-planning-coach-v${VERSION}.skill"
        GROK_FILE="dist/life-planning-coach-v${VERSION}-grok.md"
        KIMI_FILE="dist/life-planning-coach-v${VERSION}-kimi.md"
        if [ ! -f "$ZIP_FILE" ] || [ ! -f "$SKILL_FILE" ]; then
            echo "❌ Build artifacts not found. Run: bash scripts/build-skill.sh"
            exit 1
        fi
        UPLOAD_ARGS=("$ZIP_FILE" "$SKILL_FILE")
        [ -f "$GROK_FILE" ] && UPLOAD_ARGS+=("$GROK_FILE")
        [ -f "$KIMI_FILE" ] && UPLOAD_ARGS+=("$KIMI_FILE")
        gh release create "$TAG" \
            --title "$TAG" \
            --notes-file "$RELEASE_NOTES_FILE" \
            "${UPLOAD_ARGS[@]}"
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
