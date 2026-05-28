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

# ── Helper: resolve a working Python 3 interpreter ──
# BUG-013 (v1.4.0 release): plain `command -v python3` on Windows MSYS bash returns
# `/c/Users/.../Microsoft/WindowsApps/python3` — a Microsoft Store install-prompt
# stub, NOT a Python interpreter. Invoking it fails / opens Store UI. Probe each
# candidate с `--version` чтобы убедиться что это working Python 3.
_select_python() {
    for candidate in python3 python; do
        if command -v "$candidate" >/dev/null 2>&1; then
            local out
            out="$("$candidate" --version 2>&1 || true)"
            if [[ "$out" == "Python 3."* ]]; then
                command -v "$candidate"
                return 0
            fi
        fi
    done
    echo "❌ Не найден working Python 3 интерпретатор (проверены python3, python)" >&2
    echo "   На Windows: установить python.org Python и добавить в PATH ДО Microsoft Store stub" >&2
    return 1
}

PYTHON_BIN="$(_select_python)" || exit 1
echo "🐍 Python: $PYTHON_BIN"

# ── Helper: make `git tag -a` succeed in THIS environment ──
# BUG-016 (v1.4.1 release): release.sh aborted at step 6 (tag) AFTER the
# irreversible step 4 (push) → half-shipped release requiring manual recovery.
# Cause: the repo's tag.gpgSign=true + user.signingkey pointed at a WSL path
# (/mnt/c/Users/.../id_ed25519_github.pub) that does NOT resolve under MSYS/
# Git-Bash (MINGW64), where the key lives at /c/Users/.../id_ed25519_github.pub.
# `git tag -a` then failed: "Couldn't load public key … unable to sign the tag".
# Prior release tags (v1.3.1, v1.4.0) are UNSIGNED, so signing is not required.
#
# Fix: resolve the signing key per-environment (WSL /mnt/c → MSYS /c); if signing
# still can't work, fall back to an UNSIGNED annotated tag instead of hard-failing.
# The decision is validated by a throwaway-tag dry-run during preconditions
# (BEFORE the push), so a signing/config mismatch can never strand a release.
TAG_SIGN_ARGS=()

# Create+delete a throwaway annotated tag with the given `git -c` override args.
# Hang-guarded: SSH_ASKPASS_REQUIRE=force + </dev/null make a passphrase-protected
# SSH key fail fast rather than block on a prompt. Returns 0 if tagging worked.
_tag_dry_run() {
    local tmp="_release_signtest_$$"
    git tag -d "$tmp" >/dev/null 2>&1 || true
    local rc=0
    SSH_ASKPASS=/bin/false SSH_ASKPASS_REQUIRE=force DISPLAY="" GIT_TERMINAL_PROMPT=0 \
        git "$@" tag -a "$tmp" -m "release.sh signing dry-run" </dev/null >/dev/null 2>&1 || rc=1
    git tag -d "$tmp" >/dev/null 2>&1 || true
    return $rc
}

# Populate TAG_SIGN_ARGS so step 6 tagging is guaranteed to work. Returns 1 only
# if even an unsigned annotated tag cannot be created (git fundamentally broken).
_resolve_tag_sign_args() {
    TAG_SIGN_ARGS=()
    local sign fmt key
    sign="$(git config --type=bool --get tag.gpgSign 2>/dev/null || true)"

    if [ "$sign" = "true" ]; then
        fmt="$(git config --get gpg.format 2>/dev/null || true)"
        key="$(git config --get user.signingkey 2>/dev/null || true)"
        # Brittle case: SSH key given as a FILE PATH. A literal key (ssh-… / sk-…)
        # needs no file, so config is left untouched there.
        if [ "$fmt" = "ssh" ] && [ -n "$key" ] && [[ "$key" != ssh-* ]] && [[ "$key" != sk-* ]]; then
            if [ ! -f "$key" ] && [[ "$key" == /mnt/?/* ]]; then
                local alt="/${key#/mnt/}"   # WSL /mnt/c/… → MSYS /c/…
                if [ -f "$alt" ]; then
                    echo "ℹ️  signing key не найден по '$key' — использую MSYS-путь '$alt'"
                    TAG_SIGN_ARGS=(-c "user.signingkey=$alt")
                fi
            fi
        fi
    fi

    # Validate; on failure fall back to an unsigned annotated tag.
    if _tag_dry_run ${TAG_SIGN_ARGS[@]+"${TAG_SIGN_ARGS[@]}"}; then
        return 0
    fi
    if [ "$sign" = "true" ]; then
        echo "⚠️  Подписанный тег невозможен в этом окружении — fallback на UNSIGNED annotated tag"
        TAG_SIGN_ARGS=(-c tag.gpgSign=false)
        _tag_dry_run ${TAG_SIGN_ARGS[@]+"${TAG_SIGN_ARGS[@]}"} && return 0
    fi
    echo "❌ git tag dry-run упал даже для unsigned тега — прерываю ДО push (release atomic)." >&2
    return 1
}

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

# ── 0.5. PRE-TEST ARTIFACT REBUILD ──
# BUG-014 (v1.4.0 release): `test_zip_is_fresh` (tests/release/test_skill_package.py)
# fails if ZIP older than SKILL.md. Between releases прошлые v1.X.Y artifacts в dist/
# become stale relative к main's SKILL.md (которая накопила PR'ы). Rebuild с CURRENT
# version СНАЧАЛА чтобы tests видели fresh ZIP. Step 2.6 (post-sync) rebuild later
# regenerates с NEW version — both rebuilds legitimate, each для своей цели.
echo ""
echo "[0.5/7] Pre-test artifact rebuild (current version, для test_zip_is_fresh)..."
if ! "$PYTHON_BIN" scripts/build-skill.py build >/dev/null; then
    echo "❌ Pre-test build упал. Запустите вручную для diagnostics:"
    echo "   python scripts/build-skill.py build"
    exit 1
fi
echo "✅ Артефакты пересобраны (current version)"

# ── 1. PRECONDITION CHECKS ──
echo ""
echo "[1/7] Проверка preconditions..."

# Проверка: все тесты проходят
echo "→ Запуск тестов..."
if ! "$PYTHON_BIN" -m pytest tests/release/ tests/system/ -q --tb=short; then
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

# Проверка: мы на main
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "❌ Не на ветке main (сейчас: $CURRENT_BRANCH)"
    exit 1
fi
echo "✅ На ветке main"

# Проверка: создание тега возможно в этом окружении (BUG-016).
# Делаем ДО шага 4 (push) — необратимого — чтобы signing/config mismatch не
# оставил half-shipped релиз. _resolve_tag_sign_args резолвит signing key
# (WSL→MSYS) или fallback'ит на unsigned, и валидирует throwaway-tag dry-run'ом.
echo "→ Проверка возможности создания тега (signing)..."
if ! _resolve_tag_sign_args; then
    exit 1
fi
if [ "${#TAG_SIGN_ARGS[@]}" -gt 0 ]; then
    echo "✅ Тег создаваем (override: ${TAG_SIGN_ARGS[*]})"
else
    echo "✅ Тег создаваем (signing по умолчанию из git config)"
fi

# ── 2. VERSION SYNC ──
echo ""
echo "[2/7] Синхронизация версии..."
bash scripts/sync-version.sh "$VERSION"

# ── 2.5. ROADMAP CLEANUP (released-version section + status row) ──
# BUG-015 (v1.4.0 release): step 2.5 ранее удаляла ТОЛЬКО legacy status-table
# row через `sed -i "/| v${VERSION} |/d"`, оставляя `## v${VERSION} (planned) …`
# detail section в ROADMAP → post-release CI падал на test_roadmap_integrity
# (ROADMAP должен содержать только future scope). Bash sed multi-line хрупкий
# (BUG-015 note), поэтому delegate в build-skill.py (pure-Python, robust
# heading→next-`## ` section removal + orphan `---` cleanup). Exit code
# propagates чтобы failure halt'ил release атомарно.
echo ""
echo "[2.5/7] Очистка ROADMAP (released-version section/row)..."
if ! "$PYTHON_BIN" scripts/build-skill.py roadmap-cleanup "$VERSION"; then
    echo "❌ ROADMAP cleanup упал. Запустите вручную для diagnostics:"
    echo "   python scripts/build-skill.py roadmap-cleanup $VERSION"
    exit 1
fi

# ── 2.6. REBUILD ARTIFACTS WITH NEW VERSION ──
# Previously step 1.5: `bash scripts/build-skill.sh` BEFORE version sync — but
# (a) build-skill.sh uses rsync which is absent on Windows MSYS bash → silent
# failure under `>/dev/null 2>&1 || true`, and (b) running BEFORE sync produces
# artifacts with the OLD version (step 7 then can't find v${VERSION} files).
# Fix: rebuild AFTER sync via build-skill.py (pure-Python, no rsync), let exit
# code propagate so failure halts the release atomically.
echo ""
echo "[2.6/7] Пересборка артефактов (build-skill.py, после version sync)..."
# PYTHON_BIN уже resolved в top-of-script header (BUG-013 fix).
if ! "$PYTHON_BIN" scripts/build-skill.py build >/dev/null; then
    echo "❌ Сборка артефактов упала. Запустите вручную для diagnostics:"
    echo "   python scripts/build-skill.py build"
    exit 1
fi
echo "✅ Артефакты пересобраны c версией $VERSION"

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

# Проверяем версию в README на GitHub.
# BUG-008 fix (v1.3.0): использовали `sys.stdout.buffer.write(bytes)` вместо
# `print(content.decode('utf-8'))`. Старый print() крашился на Windows cp1251
# default encoding при попытке записать UTF-8 README (с emoji 🧭, кириллицей)
# в stdout — UnicodeEncodeError + pipe error. Binary write bypass'ит encoding
# entirely.
#
# BUG-010 fix (v1.3.2+): после BUG-008 fix остаётся вторая pipe-related issue —
# `grep -oP '...'` находит match рано и закрывает upstream pipe, пока Python
# ещё не закончил writing → BrokenPipeError → empty result → проверка падает
# даже когда GitHub README correct. Replay v1.3.1 release: «Python write
# /dev/stdout: The pipe is being closed». Fix: decode в temp-file, потом grep
# на файл — никакого pipe, никакого early-exit issue.
# PYTHON_BIN уже resolved в top-of-script header (BUG-013 fix).
TMP_README=$(mktemp)
trap 'rm -f "$TMP_README"' EXIT
gh api "repos/$REPO/contents/README.md" --jq '.content' \
    | "$PYTHON_BIN" -c "import sys, base64; sys.stdout.buffer.write(base64.b64decode(sys.stdin.read()))" \
    > "$TMP_README"
GITHUB_README=$(grep -oP '\*\*Версия:\*\*\s*\K[0-9.]+' "$TMP_README" | head -n 1 || true)
rm -f "$TMP_README"
trap - EXIT

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
    git ${TAG_SIGN_ARGS[@]+"${TAG_SIGN_ARGS[@]}"} tag -a "$TAG" -m "$TAG"
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
    RELEASE_NOTES_FILE="docs/archive/RELEASE_NOTES_$TAG.md"
    if [ ! -f "$RELEASE_NOTES_FILE" ]; then
        echo "→ Генерация release notes из CHANGELOG.md..."
        "$PYTHON_BIN" scripts/extract-release-notes.py "$VERSION"
    fi

    if [ -f "$RELEASE_NOTES_FILE" ]; then
        # Title = tag only (minimalist format, as React/Node.js do)
        # Release notes contain the full description
        ZIP_FILE="dist/life-planning-coach-v${VERSION}.zip"
        SKILL_FILE="dist/life-planning-coach-v${VERSION}.skill"
        GROK_FILE="dist/life-planning-coach-v${VERSION}-grok.md"
        KIMI_FILE="dist/life-planning-coach-v${VERSION}-kimi.md"
        KIMI_CLI_FILE="dist/life-planning-coach-v${VERSION}-kimi-cli.zip"
        if [ ! -f "$ZIP_FILE" ] || [ ! -f "$SKILL_FILE" ]; then
            echo "❌ Build artifacts not found. Run: python scripts/build-skill.py build"
            exit 1
        fi
        UPLOAD_ARGS=("$ZIP_FILE" "$SKILL_FILE")
        [ -f "$GROK_FILE" ] && UPLOAD_ARGS+=("$GROK_FILE")
        [ -f "$KIMI_FILE" ] && UPLOAD_ARGS+=("$KIMI_FILE")
        [ -f "$KIMI_CLI_FILE" ] && UPLOAD_ARGS+=("$KIMI_CLI_FILE")
        gh release create "$TAG" \
            --title "$TAG" \
            --notes-file "$RELEASE_NOTES_FILE" \
            "${UPLOAD_ARGS[@]}"
        echo "✅ Release $TAG создан из $RELEASE_NOTES_FILE"
    else
        echo "❌ Файл $RELEASE_NOTES_FILE не найден и не удалось сгенерировать"
        exit 1
    fi
fi

echo ""
echo "=== Релиз $TAG завершён ==="
echo "Проверьте: https://github.com/$REPO/releases/tag/$TAG"
