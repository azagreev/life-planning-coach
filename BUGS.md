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

_(no open bugs currently)_

---

## Закрытые баги

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
| Закрыто | 9 |
