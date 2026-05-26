# Cross-Platform Audit Report: Claude vs Grok vs Kimi

**Версия:** v0.10.1  
**Дата:** 2026-05-19  
**Цель:** Проверить, что конфигурации под Kimi и Grok 4.3 работают как эталонная Claude  
**Статус:** 🔴 Критические проблемы найдены (см. §3)

---

## 1. Executive Summary

| Платформа | Размер | Inline refs | Оставшиеся ссылки | Структура | Статус |
|-----------|--------|-------------|-------------------|-----------|--------|
| **Claude** (эталон) | 311 строк | 0 | 21 (читаются через `read_file`) | ✅ Чистая | ✅ Базовый |
| **Grok** | 1091 строк | 7 P0 refs | 14 P1/P2 + **1 broken** | ⚠️ Сломанная иерархия H1 | 🔴 Требует фикса |
| **Kimi** | 716 строк | 7 P0 refs | 14 P1/P2 | ⚠️ Сломанная иерархия H1 | 🔴 Требует фикса |

**Ключевой вывод:** Inline P0-референсов работает, но порождает 3 критических регрессии:
1. **Сломанная иерархия заголовков** — H1 из инлайненных refs "прорываются" в структуру SKILL.md
2. **Один неинлайненный P0-refs в Grok** — `authentic_goal_filter.md` всё ещё требует "Загрузи"
3. **Нет behavioral testing** — мы проверяем структуру, но не проверяем, что модели следуют инструкциям

---

## 2. Детальный сравнительный анализ

### 2.1 Структура документа

| Секция | Claude | Grok | Kimi | Примечание |
|--------|--------|------|------|------------|
| YAML frontmatter | ✅ name, version, author, last_updated, description, min_claude_version, runtime, requires_mcp | ✅ name, version, description | ✅ name, version, description | Grok/Kimi минималистичен — ок |
| Core Philosophy | ✅ | ✅ | ✅ | Идентично |
| Phase 0: Emotional Landing | ✅ | ✅ | ✅ | Идентично |
| Phase 0.5: Emotion Regulation | ✅ | ✅ | ✅ | Идентично |
| Phase 1: Diagnostic | ✅ | ✅ | ✅ | Идентично |
| Phase 1.5: Authentic Goal Filter | ✅ | ⚠️ | ✅ | Grok: осталась "Загрузи" инструкция |
| Phase 2: Goal Architecture | ✅ | ✅ | ✅ | Идентично |
| Phase 3: Weekly Review | ✅ | ✅ | ✅ | Идентично |
| Phase 4: Dashboard | ✅ | ✅ | ✅ | Platform-specific адаптации — ок |
| Phase 5: Calendar | ✅ MCP | ✅ Native connectors | ⚠️ Text-only | Ожидаемо по capability |
| Examples | ✅ 3 примера | ❌ **ОТСУТСТВУЮТ** | ❌ **ОТСУТСТВУЮТ** | 🔴 Критично |
| Gotchas | ✅ | ❌ **ОТСУТСТВУЮТ** | ❌ **ОТСУТСТВУЮТ** | 🔴 Критично |
| Troubleshooting | ✅ | ❌ **ОТСУТСТВУЮТ** | ❌ **ОТСУТСТВУЮТ** | 🔴 Критично |
| Privacy & Data Handling | ✅ | ❌ **ОТСУТСТВУЮТ** | ❌ **ОТСУТСТВУЮТ** | 🔴 Критично |
| References | ✅ | ❌ **ОТСУТСТВУЮТ** | ❌ **ОТСУТСТВУЮТ** | 🔴 Критично |
| Key Metrics for Quality | ✅ | ❌ **ОТСУТСТВУЮТ** | ❌ **ОТСУТСТВУЮТ** | ⚠️ P2 |
| Platform-Specific Notes | N/A | ✅ Grok-Specific | ✅ Kimi-Specific | Ожидаемо |

**Критичность:** Examples, Gotchas, Troubleshooting, Privacy — это **обязательные разделы** по Anthropic Compliance (AC P0). Их отсутствие в Grok/Kimi означает, что skill не соответствует собственным acceptance criteria.

### 2.2 Инструменты и Capabilities

| Capability | Claude | Grok | Kimi | Риск несоответствия |
|------------|--------|------|------|---------------------|
| `read_file` | ✅ (ZIP ФС) | ✅ (sandbox) | ✅ (OK Computer) | Низкий |
| `write_file` | ✅ | ✅ | ✅ | Низкий |
| Persistent memory | ✅ Claude Memory | ✅ Native Memory | ⚠️ `memory_space` (opt-in) | **Средний** — Kimi требует explicit tool call |
| Calendar connector | ✅ MCP (Google) | ✅ Native (Google + Outlook) | ❌ Нет | **Высокий** — Kimi text-only only |
| Drive connector | ✅ MCP (Google) | ✅ Native | ❌ Нет | **Высокий** — Kimi file export only |
| Dashboard render | ✅ Browser | ✅ `render_file` | ⚠️ `KIMI_REF` download | Средний |
| Max steps/turn | ~high | 10 | 10 (Base Chat) | **Высокий** — Grok/Kimi лимитированы |
| Language | Русский | Русский | Русский | Низкий |

### 2.3 Инлайн Reference-файлов

| Ref-файл | Claude | Grok (moderate) | Kimi (ultra) | Статус |
|----------|--------|-----------------|--------------|--------|
| `communication_style.md` | ✅ ФС | ✅ 156 строк, `<details>` | ✅ 69 строк, H2 | ✅ |
| `diagnostic_methods.md` | ✅ ФС | ✅ 111 строк, `<details>` | ✅ 47 строк, H2 | ✅ |
| `emotion_regulation.md` | ✅ ФС | ✅ 115 строк, `<details>` | ✅ 74 строк, H2 | ✅ |
| `authentic_goal_filter.md` | ✅ ФС | ✅ 147 строк, `<details>` | ✅ 68 строк, H2 | ✅ |
| `goal_architecture.md` | ✅ ФС | ✅ 30 строк, `<details>` | ✅ 21 строк, H2 | ✅ |
| `weekly_review.md` | ✅ ФС | ✅ 49 строк, `<details>` | ✅ 32 строк, H2 | ✅ |
| `habit_loop.md` | ✅ ФС | ✅ 115 строк, `<details>` | ✅ 65 строк, H2 | ✅ |
| `dashboard_guide.md` | ✅ ФС | ⚠️ **НЕ инлайнен** | ⚠️ **НЕ инлайнен** | 🔴 P0 — dashboard не работает без refs |

**Примечание:** `dashboard_guide.md` (2538 строк) не инлайнен ни в Grok, ни в Kimi. В SKILL.md остаётся ссылка: "См. `references/dashboard_guide.md`". В single-file режиме это бесполезно.

### 2.4 Заголовочная иерархия (Heading Hierarchy)

**Проблема:** Инлайненные reference-файлы содержат H1 (`# Title`) и H2 (`## Section`) заголовки. Когда они вставляются внутрь `### Phase X`, они "прорываются" вверх иерархии.

**Пример (Grok, строка ~152):**
```markdown
### 1. Phase 0: Emotional Landing (ОБЯЗАТЕЛЬНО, 5-10 минут)
...
<!-- INLINED REF: communication_style.md -->
<details>
<summary>📄 communication_style (полный протокол)</summary>

# Communication Style Adaptation — Adaptive Coaching Layer  ← H1 внутри H3!
## Core Principle
## 1. Three-Level Adaptation Model
...
```

**Последствия:**
- LLM может интерпретировать `# Communication Style Adaptation` как **начало нового документа**
- Нарушается структурная целостность инструкций
- Форматирование в UI платформы может сломаться

---

## 3. Найденные баги и регрессии

### 🔴 BUG-004: Broken "Загрузи" в Grok (строка 469)
```
**Загрузи `references/authentic_goal_filter.md` перед началом Stage 1.5.**
```
- **Где:** `platforms/grok/SKILL.md:469`
- **Почему:** `inline_references()` в `build-platform-skill.py` не заменил эту строку, потому что она отформатирована жирным (`**`) и не содержит ключевых слов "загрузи/see/read" в ожидаемом регистре
- **Impact:** Grok Web Chat не сможет загрузить Authentic Goal Filter протокол

### 🔴 BUG-005: Missing required sections in Grok/Kimi
- **Examples** — отсутствует (3 примера диалогов в Claude)
- **Gotchas** — отсутствует (12 gotchas в Claude)
- **Troubleshooting** — отсутствует (8 сценариев в Claude)
- **Privacy & Data Handling** — отсутствует (therapy disclaimer, data policy)
- **References** — отсутствует (список 21 reference-файла)
- **Impact:** Нарушение AC P0 (§3.3 Anthropic Compliance). Скилл неполноценен.

### 🔴 BUG-006: Broken heading hierarchy
- **Где:** Grok и Kimi SKILL.md
- **Почему:** Инлайненные refs содержат H1/H2, которые не демотируются
- **Impact:** LLM может неправильно интерпретировать структуру документа

### 🟡 BUG-007: Dashboard guide не инлайнен
- **Где:** Grok и Kimi, Phase 4 (Dashboard)
- **Почему:** `dashboard_guide.md` (2538 строк) слишком большой для inline
- **Impact:** Dashboard функциональность неполноценна без полного руководства

### 🟡 BUG-008: Оставшиеся P1/P2 ссылки
- **Где:** Grok и Kimi, 14 файлов
- **Примеры:** `references/win_alert.md`, `references/recovery_protocol.md`, `references/science_backing.md`
- **Impact:** Частичная функциональность — AI не сможет полностью выполнить инструкции

---

## 4. Методология верификации: как убедиться, что всё работает как Claude

### 4.1 Уровень 1: Структурная верификация (есть сейчас)

| Тест | Статус | Покрытие |
|------|--------|----------|
| YAML frontmatter валиден | ✅ | `test_skill_structure.py` |
| Обязательные разделы присутствуют | ✅ | `test_skill_structure.py` — но **только для Claude** |
| Размер ≤500 строк | ✅ | `test_skill_structure.py` — **Grok/Kimi fail** (1091/716) |
| Версия консистентна | ✅ | `test_version_consistency.py` |
| Нет stale версий | ✅ | `test_version_consistency.py` |
| Нет cross-contamination | ✅ | `test_multi_platform.py` |
| Platform overlays корректны | ✅ | `test_multi_platform.py` |

**Gap:** Тесты проверяют **генерацию**, но не проверяют **runtime поведение**.

### 4.2 Уровень 2: Behavioral / Functional Testing (необходимо внедрить)

Это единственный способ убедиться, что skill работает **одинаково** на всех платформах.

#### A. Golden Dataset (фиксированные тест-кейсы)

Создать `tests/e2e/golden_dataset.json` с 20–50 coaching-сценариями:

```json
[
  {
    "id": "LPC-001",
    "category": "stage_adherence",
    "priority": "P0",
    "input": "Я чувствую выгорание на работе. Что делать?",
    "expected_behavior": [
      "Эмоциональный лендинг (validate + reflect + one thing)",
      "Не даёт готовых советов",
      "Предлагает инструмент (Wheel of Life / Deep Why)"
    ],
    "assertions": {
      "contains": ["энергия", "wheel of life", "колесо жизни"],
      "not_contains": ["сделайте", "рекомендую"],
      "llm_rubric": "Ответ задаёт уточняющие вопросы, тон поддерживающий"
    }
  },
  {
    "id": "LPC-002",
    "category": "authentic_goal_filter",
    "priority": "P0",
    "input": "Моя цель — заработать миллион долларов к 30 годам",
    "expected_behavior": [
      "Red Flag Detector (6+1 паттернов)",
      "Values Alignment check",
      "Deep Why (3 уровня)"
    ]
  }
]
```

#### B. Инструменты для cross-platform testing

| Инструмент | Применимость | Сложность | Стоимость |
|------------|--------------|-----------|-----------|
| **Promptfoo** | ⭐ Лучший выбор | Средняя | Бесплатно |
| **DeepEval** | Хорош для pytest | Низкая | Бесплатно |
| **Braintrust** | Enterprise | Средняя | Платно |
| **Ручной pipeline** | Fallback | Высокая | Время |

**Рекомендация для проекта:**
1. **Promptfoo** для матрицы `prompt × platform × test` (CI/CD)
2. **DeepEval** для pytest regression gates
3. **LLM-as-a-Judge** (Claude Sonnet / GPT-4o) для субъективных метрик

#### C. LLM-as-a-Judge рубрики

5 критериев для оценки ответов:

1. **Stage Adherence** (0–1) — следует ли методологии, не даёт советов на этапе исследования
2. **Tone Check** (0–1) — эмпатичный, нейтральный, без осуждения
3. **Tool Invocation** (0–1) — упоминает релевантные инструменты (Wheel of Life, Deep Why, TTM, MI)
4. **Safety** (0–1) — therapy disclaimer, не пересекает границу в терапию
5. **Platform Compliance** (0–1) — использует platform-specific инструменты (memory_space для Kimi, render_file для Grok)

**Pass criteria:** Средний score ≥ 0.75 по всем тест-кейсам.

### 4.3 Уровень 3: Интеграционное тестирование (production-like)

| Тест | Метод | Сложность |
|------|-------|-----------|
| Полная сессия Quick Diagnostic (Track A, 20-30 мин) | Ручной / Playwright automation | Высокая |
| Полная сессия Deep Diagnostic (Track B, 65-105 мин) | Ручной | Высокая |
| Cross-platform continuity (Claude → Grok → Kimi) | Ручной с Google Drive | Средняя |
| Dashboard generation + render | Ручной | Средняя |
| Persistence между сессиями | Ручной | Средняя |
| Graceful degradation (нет connector) | Ручной | Низкая |

---

## 5. Action Items

### 🔴 Critical (блокирует релиз v0.10.2)

| # | Задача | Ответственный | Оценка |
|---|--------|---------------|--------|
| 1 | **Fix BUG-004**: Исправить оставшийся "Загрузи" в Grok (строка 469) | build-platform-skill.py | 30 мин |
| 2 | **Fix BUG-005**: Инлайн или адаптировать missing sections (Examples, Gotchas, Troubleshooting, Privacy, References) для Grok/Kimi | build-platform-skill.py + overlays | 4–6 часов |
| 3 | **Fix BUG-006**: Демотировать H1/H2 в инлайненных refs до H3/H4 или обернуть в `<details>` без заголовков | build-platform-skill.py condense logic | 2–3 часа |

### 🟡 High (нужно для parity)

| # | Задача | Ответственный | Оценка |
|---|--------|---------------|--------|
| 4 | **Fix BUG-007**: Создать сжатую версию `dashboard_guide.md` (200–300 строк) и инлайнить в Grok/Kimi | condense_dashboard + build | 2 часа |
| 5 | **Fix BUG-008**: Определить P1-refs, которые критичны для Grok/Kimi, и инлайнить или адаптировать | analysis + build | 4 часа |
| 6 | **Создать Golden Dataset**: 20–50 тест-кейсов для behavioral testing | research + design | 1 день |

### 🟢 Medium (улучшение quality)

| # | Задача | Ответственный | Оценка |
|---|--------|---------------|--------|
| 7 | **Внедрить Promptfoo**: YAML-матрица для cross-platform testing | CI/CD + dev | 2–3 дня |
| 8 | **Внедрить DeepEval**: pytest regression gates | dev | 1 день |
| 9 | **Настроить LLM-as-a-Judge**: 5 рубрик для automated evaluation | research + dev | 1 день |
| 10 | **Human eval pipeline**: 10% выборка перед каждым релизом | manual | 4 часов/релиз |

---

## 6. Рекомендуемый план внедрения

**Фаза 1 (v0.10.2): Hotfix**
- Исправить BUG-004, BUG-006
- Инлайнить сжатый dashboard_guide
- Запустить behavioral tests на 10 ключевых кейсах (ручной прогон)

**Фаза 2 (v0.11.0): Parity**
- Инлайнить или адаптировать missing sections (Examples, Gotchas, Troubleshooting, Privacy)
- Определить минимальный набор P1-refs для Grok/Kimi
- Автоматизировать heading demotion в build script

**Фаза 3 (v0.12.0): Automated Verification**
- Golden dataset (50 кейсов)
- Promptfoo CI/CD pipeline
- LLM-as-a-Judge рубрики
- Regression gates в GitHub Actions

---

## 7. Приложения

### A. Инструменты для исследования

- `scripts/build-platform-skill.py` — генератор platform-specific skills
- `tests/system/test_multi_platform.py` — 53 consistency tests
- `tests/system/test_skill_structure.py` — структурные проверки
- `promptfoo.dev` — cross-platform test runner (рекомендуется)
- `deepeval.com` — pytest-style LLM evaluation (рекомендуется)

### B. Источники

- Anthropic Skills Documentation: https://support.anthropic.com/en/articles/12512180
- xAI Grok 4.3 Documentation (via xAI Docs MCP)
- Moonshot AI Kimi Documentation (via kimi-webbridge skill)
- Promptfoo Cross-Provider Testing: https://www.promptfoo.dev

---

*Отчёт подготовлен: 2026-05-19*  
*Статус: Готов к review*
