# Bug Tracker

> Живой список багов и известных проблем проекта life-planning-coach.
> Правило: каждый баг получает ID, приоритет, статус и owner.
> При закрытии бага — добавить resolution и дату закрытия.

---

## Формат бага

```markdown
### BUG-NNN: <Краткое название>
- **Приоритет:** P0/P1/P2
- **Статус:** open / in_progress / resolved / wont_fix
- **Найден:** YYYY-MM-DD
- **Версия:** vX.Y.Z
- **Owner:** @username
- **Файлы:** `path/to/file`

**Описание:**
<Что происходит>

**Expected:**
<Что должно быть>

**Actual:**
<Что происходит сейчас>

**Steps to reproduce:**
1. ...
2. ...

**Root cause (если известен):**
<Почему это происходит>

**Resolution (при закрытии):**
<Как исправлено>
```

---

## Открытые баги

_Открытых багов нет._

---

## Закрытые баги

### BUG-017: full test suite мутирует tracked `ROADMAP.md` (test isolation)
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-29 (`test_cmd_version_accepts_semver` → tmp_path + monkeypatch `PROJECT_ROOT`)
- **Найден:** 2026-05-29 (во время работы над BUG-016)
- **Версия:** v1.4.1 → исправлено в v1.4.2+
- **Owner:** @azagreev
- **Файлы:** `tests/unit/test_build_skill_cli.py::test_cmd_version_accepts_semver`

**Описание:**
Полный прогон `python -m pytest` на чистом дереве оставлял `git status` грязным: `modified: ROADMAP.md`. Изолированный прогон `tests/release/` это НЕ триггерил — нужен был именно весь suite (тест живёт в `tests/unit/`).

**Expected:**
Тесты гермитичны: `python -m pytest` на чистом дереве оставляет `git status` чистым — ни один tracked-файл не мутируется как side effect.

**Actual:**
`git diff -- ROADMAP.md` показывал единственное изменение — строку `**Текущая версия:**`:
`- **Текущая версия:** `v1.4.1` 🎉 (released 2026-05-28)`
`+ **Текущая версия:** `v1.4.1` 🎉 (released <сегодняшняя дата>)`

**Root cause:**
`test_cmd_version_accepts_semver` вызывал `cmd_version(version=current)` напрямую, без изоляции. `cmd_version` (`scripts/build-skill.py` ~429-440) пишет в файлы по hardcoded `PROJECT_ROOT` и штампует ROADMAP-строку `(released <today>)` через `today = datetime.date.today().isoformat()`. Даже «no-op» sync на текущую версию переписывает release-дату на сегодняшнюю, когда она отличается от сохранённой → мутация tracked working-copy `ROADMAP.md`. Остальные synced-файлы diff не показывали (версия не менялась → `_replace_in_file` писал идентичный контент).

**Resolution:**
Тест теперь гермитичен: копирует все 6 файлов, которые трогает `cmd_version` (`setup.py`, `SKILL.md`, `SKILL.master.md`, `README.md`, `AGENTS.md`, `ROADMAP.md`), в `tmp_path` и делает `monkeypatch.setattr(mod, "PROJECT_ROOT", tmp_path)` — sync (+ `_scan_stale_versions`, который тоже читает `PROJECT_ROOT.rglob`) гоняется только против tmp-копии. Добавлен regression-guard: snapshot реального `ROADMAP.md` до вызова + assert байт-идентичности после (падает, если monkeypatch когда-нибудь уберут). Production-код `cmd_version` не менялся — это чисто test-isolation fix; стэмп `(released <build-date>)` в реальном релизе корректен, т.к. sync и tag создаются в один день.

**Test coverage:** сам `test_cmd_version_accepts_semver` теперь содержит guard (реальный `ROADMAP.md` не мутируется); `tests/system/test_github_sync.py::test_working_tree_is_clean` ловит любую будущую suite-wide regression.

---

### BUG-016: `scripts/release.sh` tag step (signing) env-brittle + validated too late → half-shipped release
- **Приоритет:** P1
- **Статус:** resolved
- **Исправлено:** 2026-05-29 (release.sh `_resolve_tag_sign_args` + `_tag_dry_run` precondition)
- **Найден:** 2026-05-28 (v1.4.1 release flow)
- **Версия:** v1.4.1 (наблюдаемо во время ship) → исправлено в v1.4.2+
- **Owner:** @azagreev
- **Файлы:** `scripts/release.sh` (helpers ~56-117, precondition ~194-206, step 6 create ~307), `tests/release/test_release_sh_signing.py`

**Описание:**
Во время релиза v1.4.1 release.sh упал на шаге 6 (`git tag -a "$TAG"`) ПОСЛЕ необратимого шага 4 (`git push origin main`). Получился half-shipped релиз: main уже запушен, но тега и GitHub Release нет → потребовалось ручное восстановление (ручной signed tag + создание Release через REST API, т.к. `gh release` subcommand отдавал 401).

**Expected:**
Релиз атомарен: если создание тега в этом окружении невозможно — скрипт прерывается ДО push, а не оставляет main запушенным без тега.

**Actual:**
`git tag -a` падал с `Couldn't load public key … unable to sign the tag` (exit 128) уже ПОСЛЕ push.

**Root cause:**
Два независимых дефекта:
1. **Signing env-brittle.** Репо имеет `tag.gpgSign=true` + `gpg.format=ssh` + `user.signingkey=/mnt/c/Users/.../id_ed25519_github.pub` (WSL-путь, выставлен под WSL). Под MSYS/Git-Bash (MINGW64, где репо реально собирается) ключ лежит по `/c/Users/.../id_ed25519_github.pub`, а `/mnt/c/...` не резолвится → подпись падает. Прошлые теги (v1.3.1, v1.4.0) UNSIGNED — подпись исторически не требуется.
2. **Validated too late.** Создание тега не входило в preconditions (шаг 1); фактическая попытка была только на шаге 6, ПОСЛЕ push. Любой signing/config mismatch делал релиз неатомарным.

**Resolution:**
Добавлены helper'ы `_tag_dry_run()` и `_resolve_tag_sign_args()` (по аналогии с `_select_python()` из BUG-013):
- `_resolve_tag_sign_args` при `tag.gpgSign=true` + ssh + ключ-как-путь: если файл не найден и путь вида `/mnt/?/*`, ремапит WSL→MSYS (`local alt="/${key#/mnt/}"`) и пробрасывает `-c user.signingkey=<alt>`. Если подпись всё равно невозможна → fallback на UNSIGNED annotated tag (`-c tag.gpgSign=false`) вместо hard-fail.
- Решение валидируется `_tag_dry_run` (throwaway annotated tag, hang-guarded: `SSH_ASKPASS_REQUIRE=force` + `</dev/null` + `GIT_TERMINAL_PROMPT=0` — passphrase-ключ падает быстро, а не виснет на prompt) среди preconditions ДО push. Если даже unsigned tag создать нельзя → релиз прерывается ДО необратимого шага.
- Результат (`TAG_SIGN_ARGS`) пробрасывается в команду шага 6: `git ${TAG_SIGN_ARGS[@]+"${TAG_SIGN_ARGS[@]}"} tag -a "$TAG" -m "$TAG"`.
Подход не обходит политику подписи (root-cause fix — резолв ключа per-environment); unsigned — только если подпись объективно невозможна, что согласуется с unsigned-историей тегов.

**Test coverage:** `tests/release/test_release_sh_signing.py` — presence/ordering guards (helpers есть; override проброшен в строку `tag -a "$TAG"`; precondition-вызов идёт ДО `git push origin main`) + поведенческие тесты на Git-Bash (WSL→MSYS ремап `/${key#/mnt/}`; end-to-end: при битом ssh-signing config `_resolve_tag_sign_args` создаёт UNSIGNED tag, не падая). Тесты гоняют bash на script-FILE (не `bash -c`), т.к. под MSYS аргументы после `-c` теряются, а POSIX-литералы в `-c`-строке path-mangle'ятся.

---

### BUG-015: `scripts/release.sh` step 2.5 does NOT remove released-version scope section from ROADMAP
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-28 (build-skill.py `roadmap-cleanup` + release.sh step 2.5)
- **Найден:** 2026-05-28 (v1.4.0 release flow)
- **Версия:** v1.4.0 (наблюдаемо post-ship) → исправлено в v1.4.1+
- **Owner:** @azagreev
- **Файлы:** `scripts/build-skill.py` (`_strip_roadmap_version` + `roadmap-cleanup` subcommand + `cmd_release` parity), `scripts/release.sh` (step 2.5), `tests/unit/test_build_skill_cli.py`

**Описание:**
После v1.4.0 ship CI failed на `test_roadmap_integrity.py` because ROADMAP всё ещё содержал `## v1.4.0 (planned) — WoL Health Assessment Methodology` section с full sub-feature scope. Released-version detail belongs в CHANGELOG.md, не ROADMAP.md (per planning guardrails).

release.sh step 2.5 ТОЛЬКО removes a status-table row (`| v${VERSION} | ... |`) — это legacy pattern от earlier release format. Современный ROADMAP convention использует `## v${VERSION} (planned)` headings instead of table rows. release.sh не обновился под этот convention.

**Resolution:**
Step 2.5 теперь delegates в `python scripts/build-skill.py roadmap-cleanup "$VERSION"`. Pure-Python helper `_strip_roadmap_version()` удаляет `## v${VERSION} …` detail section (от heading до следующего `## ` heading / EOF) + legacy `| v${VERSION} |` status row, с cleanup orphaned `---` separator если section была последней. Version-boundary lookahead (`(?![\w.])`) не даёт v1.4.1 матчить v1.4.10. Хрупкий bash sed multi-line (см. оригинальный note) заменён robust Python. `cmd_release` (Python release path) получил тот же шаг для parity. Exit code propagates → failure halt'ит release атомарно.

**Test coverage:** `tests/system/test_roadmap_integrity.py` ловит regression post-release; `tests/unit/test_build_skill_cli.py::test_strip_roadmap_version_*` (6 тестов: middle/last section, status-row, no-op, idempotent, longer-version preservation) проверяют removal logic напрямую.

---

### BUG-014: `scripts/release.sh` step 1 tests падает на `test_zip_is_fresh` если dist/ZIP stale
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-28 (тот же PR что BUG-013)
- **Найден:** 2026-05-28 (v1.4.0 release attempt)
- **Версия:** v1.4.0 release flow → исправлено в v1.4.1+
- **Owner:** @azagreev
- **Файлы:** `scripts/release.sh` (новый step 0.5)

**Описание:**
v1.4.0 release attempt halted at step 1 «Запуск тестов» с `AssertionError: ZIP is older than SKILL.md. Run scripts/build-skill.sh to rebuild.` Между релизами `dist/life-planning-coach-v${PREVIOUS_VERSION}.zip` хранит timestamp от предыдущего release; main's SKILL.md накапливает изменения от promotion PRs (regenerated platforms/* в methodology PRs). В момент следующего release ZIP становится stale relative к SKILL.md.

**Root cause:**
- `tests/release/test_skill_package.py::TestBuildScriptIntegrity::test_zip_is_fresh` enforces `ZIP.mtime >= SKILL.md.mtime`
- Step 1 release.sh runs tests BEFORE any rebuild → ZIP not refreshed since last release
- Step 2.6 (BUG-011 fix) rebuilds AFTER sync, but it's POST-tests — uselessly for step 1's freshness check
- В v1.3.0/v1.3.1 the issue был masked by silent BUG-011 (build attempted в old step 1.5 but failed) → test_zip_is_fresh was using stale data, but other failures stopped flow before this surfaced

**Resolution:**
Added step 0.5 BEFORE step 1: `python scripts/build-skill.py build` rebuilds artifacts с CURRENT version. Now tests see fresh ZIP. Step 2.6 (post-sync) STILL exists — produces NEW-version artifacts after sync. Two builds в одном release flow, each для своей цели:

- Step 0.5 (NEW): pre-test, CURRENT version, satisfies `test_zip_is_fresh`
- Step 2.6 (PR #28): post-sync, NEW version, produces `dist/life-planning-coach-v${NEW_VERSION}.{zip,skill,...}` для step 7 (gh release create)

См. также BUG-013 (тот же session — оба fixes в одном PR).

---

### BUG-013: `scripts/release.sh` `$PYTHON_BIN` resolves к Microsoft Store stub на Windows
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-28
- **Найден:** 2026-05-28 (v1.4.0 release attempt, step 2.6 silent failure)
- **Версия:** v1.4.0 release flow → исправлено в v1.4.1+
- **Owner:** @azagreev
- **Файлы:** `scripts/release.sh` (top-of-script `_select_python` helper + sites где PYTHON_BIN использовался)

**Описание:**
v1.4.0 release attempt step 2.6 «Пересборка артефактов (build-skill.py)» упал silently с непонятным error message:
```
[2.6/7] Пересборка артефактов (build-skill.py, после version sync)...
Python ❌ Сборка артефактов упала.
```

«Python» в выводе — отрывок Microsoft Store error message «Python was not found; install via Microsoft Store».

**Root cause:**
release.sh использовал:
```bash
PYTHON_BIN="$(command -v python3 || command -v python || echo python3)"
```

На Windows MSYS bash `command -v python3` resolves к `/c/Users/<name>/AppData/Local/Microsoft/WindowsApps/python3` — это **symlink к `AppInstallerPythonRedirector.exe`** (Microsoft Store install-prompt stub). НЕ Python interpreter. Invoking его с args → exits non-zero с install prompt text в stderr.

Тот же fallback на `python` (без `3`) resolved к real Python at `/c/Users/<name>/AppData/Local/Programs/Python/Python312/python`, но `command -v python3` уже succeeded → real Python никогда не probed.

**Resolution:**
Helper function `_select_python()` at top of release.sh probes each candidate с `--version` чтобы убедиться что это working Python 3:

```bash
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
    return 1
}
PYTHON_BIN="$(_select_python)" || exit 1
```

Resolved once at top, used throughout (step 0.5, 2.6, 5). Eliminates stub-trap on Windows. Linux/macOS поведение не меняется (working python3 returns matching `--version`, picked first).

См. также BUG-014 (тот же session — оба fixes в одном PR).

---

### BUG-012: `scripts/sync-version.sh` install-refs sed падает с «unknown option to s'»
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-28 (PR #34)
- **Найден:** 2026-05-28 (v1.4.0 release attempt, step 2)
- **Версия:** v1.4.0 release flow → исправлено перед re-attempt
- **Owner:** @azagreev
- **Файлы:** `scripts/sync-version.sh` (install-refs sed line)

**Описание:**
v1.4.0 release attempt step 2 «Синхронизация версии» upal с:
```
=== Синхронизация версии 1.4.0 ===
→ setup.py
→ SKILL.md
→ SKILL.master.md
→ README.md
sed: -e expression #1, char 48: unknown option to `s'
```

Pre-PR-#27 sync-version.sh не trogal install refs. PR #27 (v1.3.1 leftovers) added a sed для install refs (`life-planning-coach-v${V}.zip|-grok.md|-kimi.md|-kimi-cli.zip|-kimi-cli/`).

**Root cause:**
Added sed использовал `|` как BOTH delimiter AND regex alternation operator:
```bash
sed -i -E "s|life-planning-coach-v[0-9.]+(\.zip|-grok\.md|-kimi\.md|-kimi-cli\.zip|-kimi-cli/)|life-planning-coach-v${NEW_VERSION}\1|g"
        ^                            ^                  ^                  ^
        open                    first alternation   sed sees как close
```

sed parser reads first inner `|` as delimiter close → tries to parse rest of pattern as flags → unknown «s'» option.

**Resolution:**
Switched delimiter к `#` (absent from pattern AND version strings):
```bash
sed -i -E "s#life-planning-coach-v[0-9.]+(\.zip|-grok\.md|-kimi\.md|-kimi-cli\.zip|-kimi-cli/)#life-planning-coach-v${NEW_VERSION}\1#g"
```

Regression tests: `tests/unit/test_sync_version_sh.py` (5 tests). Verified manually на live README content. Также regression guard `test_install_refs_sed_uses_hash_delimiter` ensures the fix не regress.

---

### BUG-011: `scripts/release.sh` step 1.5 «Пересборка артефактов» молча падает на Windows (rsync missing)
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-28 (тот же commit что BUG-010)
- **Найден:** 2026-05-28 (v1.3.1 release)
- **Версия:** v1.3.1 release flow → исправлено в v1.3.2+ (через release.sh обновление)
- **Owner:** @azagreev
- **Файлы:** `scripts/release.sh` (бывшая строка 86; перемещён на step 2.6)

**Описание:**
release.sh шаг 1.5 пересобирал артефакты через `bash scripts/build-skill.sh >/dev/null 2>&1 || true`. build-skill.sh использует `rsync` для копирования references/templates — на Windows MSYS bash rsync отсутствует. Команда падала с `rsync: command not found`, но stderr был перенаправлен в /dev/null + `|| true` глотал exit code → молчаливый провал. Результат: артефакты в dist/ оставались со старой версией ПЛЮС платформы (platforms/{claude,grok,kimi,kimi-cli}/SKILL.md) не регенерировались после version sync, что требовало retroactive cleanup PR после каждого release (v1.2 → v1.3, v1.3.0 → v1.3.1).

**Root cause:**
1. `bash scripts/build-skill.sh` depends on rsync → не работает на Windows MSYS bash (rsync не входит в Git for Windows by default).
2. Step 1.5 (rebuild) выполнялся ДО step 2 (version sync) — даже если build успешно проходил, артефакты получали СТАРУЮ версию, а step 7 (gh release create) ожидал `dist/life-planning-coach-v${VERSION}.{zip,skill,...}` с НОВОЙ версией.
3. Suppressed output + `|| true` маскировали failure: release.sh продолжался как если всё было ОК.

**Resolution:**
- Step 1.5 удалён.
- Новый step 2.6 после version sync, вызывает `python scripts/build-skill.py build` (pure-Python, без rsync) — работает кросс-платформенно. Exit code пропагируется (без `|| true`), failure halts release.
- Step 3 commit теперь включает регенерированные platforms/* SKILL.md вместе с source-file sync.

См. также BUG-010 (тот же session, обе fixes в одном PR).

---

### BUG-010: `scripts/release.sh` step 5 (verification) — BrokenPipeError при grep early-exit
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-28
- **Найден:** 2026-05-28 (v1.3.1 release flow — рецидив после BUG-008 fix)
- **Версия:** v1.3.1 release flow → исправлено в v1.3.2+
- **Owner:** @azagreev
- **Файлы:** `scripts/release.sh` (бывшая строка 143; рефакторено на temp-file approach)

**Описание:**
Step 5 «Проверка на GitHub» снова упал с `Python write /dev/stdout: The pipe is being closed.` — несмотря на BUG-008 fix (v1.3.0 PR #14) который заменил `print(content.decode('utf-8'))` на `sys.stdout.buffer.write(bytes)`. Версия на GitHub была correct (1.3.1), но release.sh не смог её захватить → exit 1 → tag + GH release не сделаны автоматически (пришлось руками).

**Root cause:**
BUG-008 fix решил **encoding** issue (UTF-8 vs cp1251), но не **pipe-lifecycle** issue:

```bash
gh api ... | python -c "...sys.stdout.buffer.write(base64.b64decode(...))" | grep -oP '...\K[0-9.]+'
```

`grep -oP` находит match в первой строке (или там где `**Версия:**` встречается), выводит result и **завершается**. Python всё ещё writing bytes (decoded README ~3-5 KB) в свой stdout, который теперь закрыт → BrokenPipeError → Python exits non-zero → bash subshell capture видит pipefail (если включён) ИЛИ empty result → variable GITHUB_README пустая → `[ "$GITHUB_README" != "$VERSION" ]` true → exit 1.

Не воспроизводился стабильно: depending on timing/OS pipe buffer size, иногда Python успевал отписать всё ДО grep'а early-exit, иногда нет. На Linux/CI с большим pipe buffer чаще проходит; на Windows MSYS bash с меньшим — чаще падает.

**Resolution:**
Заменили pipe-to-grep на temp-file approach:

```bash
TMP_README=$(mktemp)
trap 'rm -f "$TMP_README"' EXIT
gh api ... | python -c "...write bytes..." > "$TMP_README"
GITHUB_README=$(grep -oP '...' "$TMP_README" | head -n 1 || true)
rm -f "$TMP_README"; trap - EXIT
```

Python пишет полный output в файл (нет downstream pipe → нет early-exit issue → нет BrokenPipeError). Grep читает с диска — операции последовательные, не concurrent. `head -n 1` ограничивает output одной строкой. `trap EXIT` cleanup гарантирует удаление temp-file даже при failure mid-step.

**Regression test:** `tests/unit/test_release_sh_step5.py` (расширен — было 3 теста для BUG-008, теперь +N для BUG-010 pattern).

---

### BUG-008: `scripts/release.sh` падает на step 5 (verification) на Windows
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-27
- **Найден:** 2026-05-27
- **Версия:** v1.2.0 (release flow) → исправлено в v1.3.0
- **Owner:** @azagreev
- **Файлы:** `scripts/release.sh` (line 138)

**Описание:**
`release.sh` шаг 5 «Проверка на GitHub» падал с ошибкой `Python write /dev/stdout: The pipe is being closed.`. Steps 1-4 (preconditions / version sync / commit / push) проходили успешно. Step 5+ (tag + GitHub Release) **не выполнялись автоматически** — приходилось делать вручную.

**Root cause:**
Step 5 line 138 содержал inline pipe: `gh api ... | python -c "print(base64.b64decode(...).decode('utf-8'))" | grep -oP "..."`. Python decode'ил README в UTF-8 + print() → stdout, но Windows cp1251 default encoding не может encode emoji (`🧭` на первой строке README) и кириллицу. UnicodeEncodeError на Python side → pipe close → MSYS bash repackag'ил error как «The pipe is being closed.»

Та же root cause что BUG-009 (cp1251 vs UTF-8 на Windows), но в другом scope (inline `-c` script внутри release.sh, не отдельный .py файл).

**Resolution:**
Заменили `print(content.decode('utf-8'))` на `sys.stdout.buffer.write(bytes)`:
```bash
# Было (BROKEN):
... | "$PYTHON_BIN" -c "import sys, base64; print(base64.b64decode(sys.stdin.read()).decode('utf-8'))" | grep ...
# Стало (FIXED):
... | "$PYTHON_BIN" -c "import sys, base64; sys.stdout.buffer.write(base64.b64decode(sys.stdin.read()))" | grep ...
```

`sys.stdout.buffer.write(bytes)` bypass'ит text encoding entirely — pipe несёт raw UTF-8 bytes, grep их обрабатывает без проблем. Работает на любом OS / encoding. Более robust чем PYTHONIOENCODING=utf-8 (не зависит от env var).

**Regression test:** `tests/unit/test_release_sh_step5.py::test_step5_uses_binary_stdout_write` — проверяет что `release.sh` содержит `sys.stdout.buffer.write` (не `print(...decode...)`).

**Verification:**
```
$ gh api repos/azagreev/life-planning-coach/contents/README.md --jq .content \
    | python -c "import sys, base64; sys.stdout.buffer.write(base64.b64decode(sys.stdin.read()))" \
    | grep -oP '\*\*Версия:\*\*\s*\K[0-9.]+'
1.2.0
$ echo $?
0
```
(На Windows MSYS без PYTHONIOENCODING=utf-8 prefix.)

---

### BUG-009: `scripts/extract-release-notes.py` крашится на финальном print под Windows cp1251
- **Приоритет:** P2
- **Статус:** resolved
- **Исправлено:** 2026-05-27
- **Найден:** 2026-05-27
- **Версия:** v1.2.0 (release prep) → исправлено в v1.3.0
- **Owner:** @azagreev
- **Файлы:** `scripts/extract-release-notes.py`

**Описание:**
`extract-release-notes.py` корректно генерирует файл `docs/archive/RELEASE_NOTES_vX.Y.Z.md`, но крашился на финальном `print(f"✅ Release notes сохранены: {output_path}")` под Windows default encoding (cp1251).

**Root cause:**
Python 3 на Windows по default использует cp1251 для stdout. ✅ emoji и кириллица в print не encode'ятся. Файл записывается через `open(..., encoding="utf-8")` — это работало нормально; проблема была только на print → stdout.

**Resolution:**
В начале `scripts/extract-release-notes.py` (после `import sys`) добавлен guard:
```python
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
```
Тот же pattern уже использован в `scripts/build-platform-skill.py` (строки 17-20). `hasattr()` guard сохраняет совместимость с Python < 3.7 (no-op там). Defensive regression test добавлен в `tests/unit/test_extract_release_notes.py::test_stdout_reconfigure_present_for_windows_safety`.

**Verification:**
```
$ python scripts/extract-release-notes.py 1.2.0
✅ Release notes сохранены: docs/archive/RELEASE_NOTES_v1.2.0.md
$ echo $?
0
```
(На Windows без `PYTHONIOENCODING=utf-8` prefix.)

### BUG-007: `dashboard_guide.md` (2538 строк) невозможно инлайнить полностью в Grok/Kimi
- **Приоритет:** P0
- **Статус:** resolved
- **Исправлено:** 2026-05-19
- **Найден:** 2026-05-18
- **Версия:** v0.10.1
- **Owner:** @azagreev
- **Файлы:** `scripts/build-platform-skill.py`, `references/dashboard_guide.md`

**Описание:**
`dashboard_guide.md` содержит 2538 строк HTML/CSS/JS спецификации дашборда. Полный inline в Grok/Kimi SKILL.md невозможен из-за ограничений контекста.

**Resolution:**
Добавлена функция `condense_dashboard()` в `build-platform-skill.py`. Агрессивное сжатие до ~100 строк: coaching rules + JSON contract + CSS variable map. Инлайнится как `<details>` в Grok и аналогично в Kimi.

---

### BUG-006: Заголовки инлайненных refs не демотируются — ломают структуру SKILL.md
- **Приоритет:** P0
- **Статус:** resolved
- **Исправлено:** 2026-05-19
- **Найден:** 2026-05-18
- **Версия:** v0.10.1
- **Owner:** @azagreev
- **Файлы:** `scripts/build-platform-skill.py`

**Описание:**
При inline reference-файлов в Grok/Kimi их H1/H2 заголовки конфликтуют с заголовками основного SKILL.md, нарушая структуру документа.

**Resolution:**
Добавлена функция `demote_headings(text, levels=2)` — сдвигает H1→H3, H2→H4. Применяется ко всем инлайненным refs.

---

### BUG-005: Пропавшие секции (Examples, Gotchas, Troubleshooting, Privacy) в Grok/Kimi SKILL.md
- **Приоритет:** P0
- **Статус:** resolved
- **Исправлено:** 2026-05-19
- **Найден:** 2026-05-18
- **Версия:** v0.10.1
- **Owner:** @azagreev
- **Файлы:** `scripts/build-platform-skill.py`, `platforms/grok/SKILL.md`, `platforms/kimi/SKILL.md`

**Описание:**
После inline reference-файлов секции Examples, Gotchas, Troubleshooting, Privacy исчезали из Grok/Kimi SKILL.md.

**Root cause:**
Функция `parse_frontmatter()` ломалась на `---` внутри body (inline refs используют `<details>` с markdown, где `---` встречались). Секции после inline блока отбрасывались.

**Resolution:**
Секции восстановились после inline + rebuild. `parse_frontmatter()` не менялся — root cause был в порядке операций inline vs body assembly.

---

### BUG-004: Оставшийся `Загрузи `references/...`` в Grok SKILL.md не ловится regex
- **Приоритет:** P0
- **Статус:** resolved
- **Исправлено:** 2026-05-19
- **Найден:** 2026-05-18
- **Версия:** v0.10.1
- **Owner:** @azagreev
- **Файлы:** `scripts/build-platform-skill.py`

**Описание:**
После BUG-002 осталась одна ссылка вида `**Загрузи \u0060references/...\u0060**` (с markdown decoration **), которую regex не ловил.

**Resolution:**
Regex обновлён — теперь ловит markdown decoration вокруг ссылки. Все оставшиеся "Загрузи" заменены на "См.".

---

### BUG-003: `kimi.md` ссылается на 21 внешний reference-файл, недоступный в Kimi OK Computer mode
- **Приоритет:** P0
- **Статус:** resolved
- **Исправлено:** 2026-05-19
- **Найден:** 2026-05-18
- **Версия:** v0.10.0
- **Owner:** @azagreev
- **Файлы:** `platforms/kimi/SKILL.md`, `scripts/build-platform-skill.py`

**Описание:**
`platforms/kimi/SKILL.md` содержит 21 ссылку на `references/*.md`. Kimi OK Computer mode (`kimi.com/agent`) загружает только `SKILL.md` — reference-файлы не подгружаются.

**Resolution:**
7 критичных P0 reference-файлов инлайнены в `platforms/kimi/SKILL.md` в агрессивно сжатом виде (`ultra_condense()` + `demote_headings()`). P1/P2 refs заменены на нейтральные "См. `references/...`". Остальные оставлены как ссылки (Kimi OK Computer игнорирует, но не ломается).

---

### BUG-002: `grok.md` ссылается на 21 внешний reference-файл, недоступный при создании Grok Skill
- **Приоритет:** P0
- **Статус:** resolved
- **Исправлено:** 2026-05-19
- **Найден:** 2026-05-18
- **Версия:** v0.10.0
- **Owner:** @azagreev
- **Файлы:** `platforms/grok/SKILL.md`, `scripts/build-platform-skill.py`

**Описание:**
`platforms/grok/SKILL.md` содержит 21 ссылку на файлы из папки `references/*.md`. При создании Grok Skill через веб-UI (вставка текста в поле Instruction) эти файлы не загружаются — Grok получает только основной SKILL.md без детальных протоколов.

**Resolution:**
7 критичных P0 reference-файлов инлайнены в `platforms/grok/SKILL.md` через `<details>` tags (`condense_markdown()` + `demote_headings()`). P1/P2 refs заменены на нейтральные "См. `references/...`". Остальные оставлены как ссылки (Grok игнорирует, но не ломается).

---

### BUG-001: Dashboard показывает 8 сфер Wheel of Life вместо 11
- **Приоритет:** P1
- **Статус:** resolved
- **Исправлено:** 2026-05-17
- **Найден:** 2026-05-17
- **Версия:** v0.6.1
- **Owner:** @azagreev
- **Файлы:** `life-planning-dashboard.html`

**Описание:**
HTML Dashboard содержит старую реализацию Wheel of Life с 8 сферами. В v0.6.0 количество сфер было расширено до 11, но дашборд не обновлён.

**Resolution:**
- `WHEEL_SPHERES` расширен с 8 до 11 элементов
- Разделён `family` → `family` (Семья) + `social` (Дружба)
- Добавлены `spirituality` (Духовность, смысл) и `contribution` (Вклад)
- Обновлён subtitle: "Баланс 8 сфер" → "Баланс 11 сфер"
- Обновлён делитель среднего: `/ 8` → `/ 11`
- Добавлены CSS-переменные для новых сфер
- Добавлен тест `test_wheel_has_11_domains`

---

## Статистика

| Метрика | Значение |
|---------|----------|
| Открыто | 0 |
| In Progress | 0 |
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |
| Закрыто | 17 |
