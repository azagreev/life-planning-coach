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

### BUG-008: `scripts/release.sh` падает на step 5 (verification) на Windows
- **Приоритет:** P2
- **Статус:** open
- **Найден:** 2026-05-27
- **Версия:** v1.2.0 (release flow)
- **Owner:** @azagreev
- **Файлы:** `scripts/release.sh` (step 5), вероятно `scripts/build-skill.py` или sync-version subprocess

**Описание:**
`release.sh` шаг 5 «Проверка на GitHub» падает с ошибкой `Python write /dev/stdout: The pipe is being closed.`. Steps 1-4 (preconditions / version sync / commit / push) проходят успешно — commit и push на GitHub выполняются. Падение на verification = step 5+ (создание тега + GitHub Release) **не выполняются автоматически**.

**Expected:**
Полный flow: build → version sync → commit → push → **verify on GitHub** → tag → GitHub Release без ошибок.

**Actual:**
Steps 1-4 ok, step 5 крашится с pipe error, далее release.sh exits. Tag + GitHub Release нужно делать вручную:
```
git -c tag.gpgSign=false tag -a v1.2.0 <commit> -m "..."
git push origin v1.2.0
gh release create v1.2.0 ...
```

**Steps to reproduce:**
1. На Windows (PowerShell или Git Bash через MSYS)
2. `PYTHONIOENCODING=utf-8 bash scripts/release.sh 1.2.0`
3. Дождаться step 5 «Проверка на GitHub» → pipe error

**Root cause (предполагаемый):**
Step 5 видимо использует Python subprocess (через bash → python pipe) с PIPE stdout/stderr. Windows MSYS bash + Python 3.12 + cp1251 default encoding + subprocess pipe — где-то комбинация ломает stdout flush. Возможно проблема в `scripts/sync-version.sh` или другом subprocess который step 5 запускает.

**Workaround (текущий):**
Выполнить tag + GitHub release вручную после release.sh падения. См. сессию v1.2.0 release log как пример.

---

### BUG-009: `scripts/extract-release-notes.py` крашится на финальном print под Windows cp1251
- **Приоритет:** P2
- **Статус:** open
- **Найден:** 2026-05-27
- **Версия:** v1.2.0 (release prep)
- **Owner:** @azagreev
- **Файлы:** `scripts/extract-release-notes.py` (строка 73)

**Описание:**
`extract-release-notes.py` корректно генерирует файл `docs/archive/RELEASE_NOTES_vX.Y.Z.md`, но крашится на финальном `print(f"✅ Release notes сохранены: {output_path}")` под Windows default encoding (cp1251).

**Expected:**
```
$ python scripts/extract-release-notes.py 1.2.0
✅ Release notes сохранены: docs/archive/RELEASE_NOTES_v1.2.0.md
$ echo $?
0
```

**Actual:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '✅' in position 0: character maps to <undefined>
```
Exit code 1 (несмотря на то, что файл успешно создан).

**Steps to reproduce:**
1. На Windows (PowerShell / cmd / Git Bash) без `PYTHONIOENCODING=utf-8`
2. `python scripts/extract-release-notes.py 1.2.0`
3. UnicodeEncodeError на финальном print

**Root cause:**
Python 3 на Windows по default использует cp1251 для stdout. ✅ emoji (`✅`) и кириллица в print не encode'ятся. Файл записывается через `open(..., encoding="utf-8")` — нормально; проблема только на print stdout.

**Workaround (текущий):**
`PYTHONIOENCODING=utf-8 python scripts/extract-release-notes.py 1.2.0`

**Resolution (предлагаемый):**
В начале `scripts/extract-release-notes.py` добавить:
```python
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
```
(Тот же pattern уже использован в `scripts/build-platform-skill.py` строки 17-20 — see BUG-007 era.)

Альтернатива — убрать emoji из print, заменить на ASCII (`[OK]`).

---

---

## Закрытые баги

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
| Открыто | 2 |
| In Progress | 0 |
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |
| Закрыто | 7 |
