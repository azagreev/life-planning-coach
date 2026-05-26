# Audit Report: Calendar Integration

> **Scope:** Полный аудит календарной интеграции в life-planning-coach v0.10.2
> **Дата:** 2026-05-19
> **Метод:** Статический анализ 4 платформенных SKILL.md + reference-файлов + тестов + CI/CD + build scripts
> **Режим:** Research Only — только отчёт, без реализации

---

## Executive Summary

| Метрика | Значение |
|---------|----------|
| Платформ с Calendar API | 3/4 (Claude MCP, Grok Connector, Kimi CLI MCP) |
| Платформ с **работающей** pre-flight проверкой | **0/4** |
| Платформ с conflict resolution | **0/4** |
| Платформ с density analysis | **0/4** |
| Функциональных тестов календаря | **0** |
| Тестов на tone/language | 3 (`test_calendar_tone.py`) |
| Заполненных PoC gates | 0/6 |
| Критических gaps | **4** |
| Высокорисковых gaps | **4** |
| Среднерисковых gaps | **6** |

**Главный вывод:** Календарная интеграция существует как **документация**, но не как **функциональность**. Все 4 платформы умеют создавать события, но ни одна не проверяет занятость пользователя перед созданием. Скилл предлагает время «вслепую» (`next_sunday_19:00`), не анализируя плотность календаря, не разрешая конфликты и не адаптируясь под загруженность пользователя.

---

## 1. Critical Gaps (Критические)

### GAP-1: Нет pre-flight проверки календаря перед созданием события

**Где найдено:** Все 4 `platforms/*/SKILL.md` (Phase 5)

**Что сейчас:**
```markdown
# Phase 5: Execution Backbone — Google Calendar Integration
# ...
create_event(
  summary="Weekly Review",
  start={next_sunday_19:00},   ← жёстко зашито, без проверки
  end={next_sunday_19:30},
  ...
)
```

**Чего нет:**
- Шага «проверь `list_events` на target дату/время»
- Вызова `suggest_time` перед `create_event`
- Использования Free Slot Algorithm (он описан в `calendar_constants.md`, но не вызывается из SKILL.md)

**Риск:** Пользователь получает событие в время, когда у него уже есть встреча. Конфликт не обнаруживается.

**Платформы:** Claude ❌ | Grok ❌ | Kimi Web ❌ | Kimi CLI ❌

---

### GAP-2: Нет conflict resolution (разрешения конфликтов)

**Где найдено:** Все 4 `platforms/*/SKILL.md`

**Что сейчас:** Если `create_event` падает из-за занятости — скилл не знает, что делать. В лучшем случае покажет text-only fallback.

**Чего нет:**
- Логики «время занято → найди ближайшее свободное → предложи пользователю"
- Обработки ошибки `409 Conflict` от Calendar API
- Smart rescheduling ("У тебя Team Standup в 19:00. Weekly Review перенести на 21:00?")

**Риск:** Скилл создаёт overlapping events или падает молча.

---

### GAP-3: Нет calendar density / busyness analysis

**Где найдено:** Все 4 `platforms/*/SKILL.md` + `references/calendar_integration.md`

**Что сейчас:** Free Slot Algorithm ищет 3 свободных окна, но не анализирует общую картину.

**Чего нет:**
- Подсчёта количества событий / день
- Оценки density: Low (<3) / Medium (3-6) / High (>6)
- Адаптации предложений под загруженность ("У тебя 8 встреч в понедельник — Deep Work лучше перенести на среду")
- Защиты от over-scheduling

**Риск:** Пользователь получает ещё одно событие в уже перегруженный день, что ведёт к выгоранию.

---

### GAP-4: Kimi Web — несостоятельный retry protocol

**Где найдено:** `platforms/kimi/SKILL.md` (lines 650–653)

**Что сейчас:**
```markdown
> **Prerequisites:** Kimi has no native calendar integration. Use text-only planning...
# ...
**Retry Protocol:**
1. Сохранить в очередь: `conversation_state.persistence_retry.calendar.pending_events`
2. В следующей сессии: Проверить доступность Calendar MCP
```

**Проблема:** Скилл заявляет, что у Kimi Web НЕТ calendar integration, но тут же копирует retry protocol от Claude, который предполагает Calendar MCP. `persistence_retry.calendar.pending_events` — бессмысленная переменная для платформы без API.

**Риск:** Противоречивые инструкции путают как пользователя, так и скилл.

---

### GAP-5: Dangling references в Grok/Kimi single-file skills

**Где найдено:** `scripts/build-platform-skill.py` + `platforms/grok/SKILL.md` + `platforms/kimi/SKILL.md`

**Что сейчас:** `calendar_constants.md` и `calendar_integration.md` НЕ входят в `P0_REFS` (не инлайнятся в Grok/Kimi). Но в generated файлах остаются ссылки:
```markdown
См. `references/calendar_constants.md`
Загрузи `references/calendar_integration.md`
```

**Проблема:** Пользователь Grok/Kimi получает инструкцию открыть файл, которого нет в контексте.

**Риск:** Нерабочие ссылки = нерабочий coaching flow.

---

## 2. High-Risk Gaps (Высокорисковые)

### GAP-6: PoC MCP — полностью пустой

**Где найдено:** `references/research/mcp_poc_log.md`

**Статус:** Все 6 gates помечены ⏳ (не выполнены). Нет результатов OAuth, нет проверки `suggest_time`, нет latency data.

**Влияние:** Вся scope analysis (`references/research/scope_analysis.md`) — inferred из документации, не проверена экспериментально. Мы не знаем, работает ли recurrence в MCP, какие OAuth scopes реально нужны, работает ли `suggest_time`.

---

### GAP-7: 0 функциональных тестов календаря

**Где найдено:** `tests/`

**Что есть:**
- `test_calendar_tone.py` — 3 теста на tone/language
- `test_multi_platform.py` — проверка frontmatter

**Чего нет:**
- Тестов на Free Slot Algorithm
- Тестов на event creation patterns
- Тестов на conflict detection
- Тестов на COLOR_MAP / REMINDER_PRESETS / RRULE_PRESETS completeness
- Тестов на retry persistence protocol

**Риск:** Любое изменение `calendar_integration.md` может сломать календарную логику, и мы это не поймаем.

---

### GAP-8: `build-skill.yml` пропускает system tests

**Где найдено:** `.github/workflows/build-skill.yml`

**Что сейчас:**
```yaml
- name: Run release tests
  run: python3 -m unittest discover -s tests/release -v
```

**Проблема:** Release workflow НЕ гонит system tests. `test_calendar_tone.py` пропускается. Ошибка в tone/language пройдёт в релиз.

---

### GAP-9: Energy Scheduling — disconnected от календаря

**Где найдено:** `references/energy_scheduling.md`

**Что сейчас:** Файл описывает энергетическое планирование, но не интегрирован с чтением календаря. Нет алгоритма «пик энергии = 9:00 → найди свободный слот в 9:00–11:00».

**Риск:** Скилл предлагает Deep Work в 9:00, не зная, что у пользователя уже стоит встреча.

---

## 3. Medium-Risk Gaps (Среднерисковые)

### GAP-10: Work hours hardcoded (9:00–18:00)

**Где найдено:** `references/calendar_integration.md`

**Проблема:** Free Slot Algorithm ищет gaps в work_hours, но они не определены как параметр. Подразумевается 9:00–18:00 без учёта пользовательских предпочтений.

---

### GAP-11: Kimi-CLI не тестируется в multi-platform tests

**Где найдено:** `tests/system/test_multi_platform.py`

**Что сейчас:** `PLATFORMS = ["claude", "grok", "kimi"]` — нет `"kimi-cli"`.

---

### GAP-12: Нет JSON validation для calendar constants

**Где найдено:** `references/calendar_constants.md`

**Проблема:** `COLOR_MAP`, `REMINDER_PRESETS`, `RRULE_PRESETS` — JSON blocks без автоматической валидации.

---

### GAP-13: Нет artifact inclusion test для calendar files

**Где найдено:** `tests/release/test_skill_package.py`

**Проблема:** Тесты проверяют наличие `references/` в ZIP, но не конкретно `calendar_constants.md` и `calendar_integration.md`.

---

### GAP-14: Нет timezone intelligence

**Где найдено:** `references/calendar_integration.md`

**Проблема:** Поле `timeZone` есть в schema, но нет логики определения timezone пользователя или обработки DST.

---

### GAP-15: Tasks API — исследован, но не интегрирован

**Где найдено:** `references/research/tasks_api_research.md`

**Проблема:** Подробный research, но нет decision, integration plan или реализации. Daily Top-3 остаётся text-only.

---

## 4. Platform Matrix

| Capability | Claude (MCP) | Grok (Connector) | Kimi Web | Kimi CLI (MCP) |
|------------|-------------|------------------|----------|----------------|
| **API available** | ✅ | ✅ | ❌ | ✅ (opt-in) |
| **Auto-detect availability** | ✅ | ✅ | ❌ | ✅ |
| **Check before create** | ❌ | ❌ | N/A | ❌ |
| **Conflict resolution** | ❌ | ❌ | N/A | ❌ |
| **Density analysis** | ❌ | ❌ | N/A | ❌ |
| **Smart time proposal** | ❌ | ❌ | N/A | ❌ |
| **Recurring events** | ✅ (RRULE) | ✅ (RRULE) | ❌ | ✅ (RRULE) |
| **Free slot search** | ✅ (tool exists) | ✅ (tool exists) | ❌ | ✅ (tool exists) |
| **Retry protocol** | ✅ | ✅ | ❌* | ✅ |
| **Text-only fallback** | ✅ | ✅ | ✅ | ✅ |

\* Retry protocol copy-pasted from Claude, inconsistent with no-API reality.

---

## 5. Тестовое покрытие

| Что тестируется | Файл | Статус |
|-----------------|------|--------|
| Tone/language (forbidden words) | `test_calendar_tone.py` | ✅ 3 теста |
| Tone/language (scary statistics) | `test_calendar_tone.py` | ✅ 1 тест |
| Tone/language (positive framing) | `test_calendar_tone.py` | ✅ 1 тест |
| Frontmatter `requires_mcp` | `test_multi_platform.py` | ✅ |
| Platform-specific calendar claims | `test_multi_platform.py` | ✅ |
| **Free Slot Algorithm** | — | ❌ **Нет** |
| **Event creation patterns** | — | ❌ **Нет** |
| **Conflict detection** | — | ❌ **Нет** |
| **COLOR_MAP completeness** | — | ❌ **Нет** |
| **REMINDER_PRESETS validity** | — | ❌ **Нет** |
| **RRULE_PRESETS validity** | — | ❌ **Нет** |
| **Retry Persistence Protocol** | — | ❌ **Нет** |
| **Artifact inclusion (calendar files)** | — | ❌ **Нет** |
| **Broken references in single-file** | — | ❌ **Нет** |
| **JSON validation (constants)** | — | ❌ **Нет** |

---

## 6. CI/CD

| Workflow | Calendar Tests | Артефакты | Gaps |
|----------|---------------|-----------|------|
| `release-checks.yml` (PR/push) | ✅ Полный pytest suite | Dry-run ZIP | Нет calendar-specific проверок |
| `build-skill.yml` (tag push) | ❌ Только `tests/release` | Релизные артефакты | **Пропускает system tests** |
| `release-guard.yml` (release) | N/A | N/A | Только title check |

---

## 7. Recommendations (Приоритизированные)

### P0 (Блокирует релиз v0.11.0)
1. **GAP-1 + GAP-2 + GAP-3:** Создать `references/calendar_intelligence.md` — обязательный pre-flight protocol: `list_events` → density check → conflict detection → smart proposal → `create_event`
2. **GAP-4:** Удалить несостоятельный retry protocol из `platforms/kimi/SKILL.md`, заменить на честный text-only flow
3. **GAP-5:** Добавить `calendar_constants.md` + `calendar_integration.md` в `P0_REFS` для Grok/Kimi, или убрать ссылки

### P1 (Должно быть в v0.11.0)
4. **GAP-7:** Добавить функциональные тесты календаря
5. **GAP-8:** Обновить `build-skill.yml` — гонить ВСЕ тесты
6. **GAP-6:** Провести PoC MCP (Gate 0–2)

### P2 (Можно отложить)
7. **GAP-9:** Интегрировать `energy_scheduling.md` с calendar reading
8. **GAP-10:** Добавить user preference для work hours
9. **GAP-11–15:** Kimi-CLI tests, JSON validation, artifact tests, timezone, Tasks API

---

## 8. Что НЕ является проблемой

| То, что может показаться проблемой | Почему это OK |
|-----------------------------------|---------------|
| Text-only Daily Top-3 | Ожидаемо — Google Tasks API недоступен через Calendar MCP |
| `requires_mcp` optional | Ожидаемо — скилл работает без календаря, это feature |
| Отсутствие Tasks API | Ожидаемо — техническое ограничение, задокументировано в v0.2.0 |
| Kimi Web без API | Ожидаемо — platform limitation, не bug скилла |

---

*Audit completed. 15 gaps found: 5 Critical, 4 High-risk, 6 Medium-risk.*
*Рекомендуется: Plan Mode → `references/calendar_intelligence.md` + обновление 4 SKILL.md + тесты.*
