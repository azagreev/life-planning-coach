# Backlog

> **Для кого:** Внутреннее планирование, идеи без committed версии, research debt и техдолг.  
> **Принцип:** Каждая активная идея имеет триггер и RICE score.  
> **Баги:** Активные баги — в [BUGS.md](BUGS.md).  
> **История:** Выпущенные версии — в [CHANGELOG.md](CHANGELOG.md). Старый backlog сохранён в [references/archive/BACKLOG_before_cleanup_2026-05-21.md](references/archive/BACKLOG_before_cleanup_2026-05-21.md).

---

## Формат RICE

```
RICE = (Reach × Impact × Confidence) / Effort

Reach: % целевой аудитории (0-100) [GUESS, если нет данных]
Impact: 0.25 minimal → 3.0 massive
Confidence: 0-100%
Effort: Estimated AI Sessions (EAS) + Context Pressure
```

| RICE | Категория | Действие |
|------|-----------|----------|
| > 30 | Quick Win | Немедленно |
| 10-30 | High Priority | Следующий спринт |
| 3-10 | Medium Priority | Backlog |
| < 3 | Moonshot | Исследовать позже |

---

## Active Candidates

### Быстрый онбординг через микроцель (Track 0: Micro-Goal)

- **Описание:** Быстрый путь от первого сообщения до одной маленькой SMART-цели на сегодня: Best Hopes → Scaling → One Small Step → if-then цель.
- **Триггер:** Решение автора после аудита онбординга и research validation.
- **Статус:** 💡 Идея, исследование завершено, ждёт отдельного plan mode.
- **RICE:** Reach 70 [GUESS] × Impact 2.0 × Confidence 75% / Effort M=2 EAS, Context Pressure High = **52.5** (Quick Win).
- **Артефакты:** `references/research/track0_micro_goal_research.md`; предстоит создать `references/track0_micro_goal.md`.
- **Риск:** Нужно решить, Track 0 заменяет Phase 0 или дополняет её.

### Переписать позиционирование README.md

- **Описание:** Первые 30 строк README должны объяснять promise и отличие от Notion/Todoist/AI-коучей, а не перечислять методологии.
- **Триггер:** UX-аудит позиционирования.
- **Статус:** 💡 Идея, ждёт plan mode.
- **RICE:** Reach 100 × Impact 1.5 × Confidence 80% / Effort S=1 EAS, Context Pressure Low = **120.0** (Quick Win).
- **Артефакты:** Переписанный hero/quick-start, таблица "в чём отличие", сокращённый блок "Что это?".
- **Риск:** Не потерять credibility при снижении академичности.

### QA Hardening — надёжность, edge cases, безопасность

- **Описание:** Input validation, MCP timeout handling, prompt-injection reinforcement, human-friendly errors.
- **Триггер:** Внешнее QA-ревью или перед расширением MCP.
- **Статус:** 💡 Идея, аудит завершён.
- **RICE:** Reach 100 × Impact 2.0 × Confidence 70% / Effort M=2 EAS, Context Pressure Medium = **70.0** (Quick Win).
- **Артефакты:** Обновления `SKILL.master.md`, `references/calendar_integration.md`, тесты на invalid input/prompt injection/timeouts.
- **Риск:** Не превратить text-only skill в over-engineered runtime.

### UX Hardening — tone of voice, cognitive load, empty states

- **Описание:** Tone guide, quick-add путь для целей, empty states для первого входа/0 целей/0 привычек/0 прогресса.
- **Триггер:** Внешнее UX-ревью или жалобы на тяжёлый onboarding.
- **Статус:** 💡 Идея, аудит завершён.
- **RICE:** Reach 80 [GUESS] × Impact 1.5 × Confidence 70% / Effort M=2 EAS, Context Pressure Medium = **42.0** (Quick Win).
- **Артефакты:** `references/tone_of_voice_guide.md`, `references/empty_states.md`, tests for forbidden words/tone consistency.
- **Риск:** Слишком жёсткий tone guide может конфликтовать с adaptive communication style.

### Интеграция с Google Tasks MCP

- **Описание:** Синхронизация Daily Top-3 с Google Tasks через MCP.
- **Триггер:** Tasks API становится доступен через MCP в целевой платформе.
- **Статус:** ⏳ Ожидание внешнего события.
- **RICE:** Reach 45 [GUESS] × Impact 1.5 × Confidence 40% / Effort L=3 EAS, Context Pressure High = **9.0** (Medium Priority).
- **Риск:** Зависимость от внешней платформы и OAuth scope.

### Групповой коучинг

- **Описание:** Парный или групповой coaching flow для 2+ участников.
- **Триггер:** 5+ пользователей запросят групповой формат.
- **Статус:** 💡 Идея.
- **RICE:** Reach 20 [GUESS] × Impact 1.0 × Confidence 30% / Effort XL=5 EAS, Context Pressure High = **1.2** (Moonshot).
- **Риск:** Сложность privacy, consent и conflict handling.

### Мультиязычность

- **Описание:** Поддержка английского языка или EN/RU toggle.
- **Триггер:** 10+ запросов от англоязычных пользователей.
- **Статус:** 💡 Идея.
- **RICE:** Reach 35 [GUESS] × Impact 1.5 × Confidence 45% / Effort XL=5 EAS, Context Pressure High = **4.7** (Medium Priority).
- **Риск:** Cross-lingual consistency и удвоение тестовой матрицы.

### Social accountability

- **Описание:** Permission-based напоминания партнёру/другу или accountability check-in.
- **Триггер:** 3+ пользователя запросят социальную ответственность.
- **Статус:** 💡 Идея.
- **RICE:** Reach 25 [GUESS] × Impact 1.0 × Confidence 35% / Effort L=3 EAS, Context Pressure High = **2.9** (Moonshot).
- **Риск:** Privacy, consent, эмоциональное давление.

---

## Research Debt

### Token Optimization Audit

- **Описание:** Найти и уменьшить token overhead в русском skill-контенте, references и examples.
- **Триггер:** Жалобы на скорость/стоимость или перед крупным расширением references.
- **Статус:** 🔬 Research, запланировано.
- **RICE:** Reach 100 × Impact 1.5 × Confidence 40% / Effort XL=5 EAS, Context Pressure Medium = **12.0** (High Priority).
- **Deliverable:** `references/research/token_audit_report.md`, рекомендации и PR с оптимизациями при значимой экономии.

### Cross-Lingual Consistency

- **Описание:** Проверить code-switching артефакты между README, frontmatter, SKILL instructions и platform files.
- **Триггер:** Обнаружена пользователем 2026-05-20.
- **Статус:** 🔍 Идентифицирована проблема.
- **RICE:** Reach 100 × Impact 1.0 × Confidence 70% / Effort S=1 EAS, Context Pressure Medium = **70.0** (Quick Win).
- **TODO:** Retrieval accuracy tests, platform-файлы, решение по языку README.

### Google Health MCP integration research

- **Описание:** Выбрать безопасный путь интеграции health/wearable data: hosted MCP, local bridge или custom connector.
- **Триггер:** v0.16 candidate decision.
- **Статус:** 🔬 Research completed, implementation не утверждена.
- **RICE:** Reach 40 [GUESS] × Impact 2.0 × Confidence 45% / Effort XL=5 EAS, Context Pressure Crit = **7.2** (Medium Priority).
- **Артефакт:** `references/research/google_health_mcp_integration_research.md`.
- **Риск:** Высокая privacy/security нагрузка.

### Body Doubling via AI

- **Описание:** AI-assisted body doubling prompts/session flow для удержания внимания и начала действий.
- **Триггер:** Retention проблема становится критичной.
- **Статус:** 🔬 Research direction.
- **RICE:** Reach 35 [GUESS] × Impact 1.5 × Confidence 35% / Effort L=3 EAS, Context Pressure High = **6.1** (Medium Priority).

### Wearable Energy Integration

- **Описание:** Подключение wearable signals для energy-aware planning.
- **Триггер:** Wearable MCP servers становятся stable.
- **Статус:** 🔬 Research direction.
- **RICE:** Reach 30 [GUESS] × Impact 2.0 × Confidence 30% / Effort XL=5 EAS, Context Pressure Crit = **3.6** (Medium Priority).

---

## Tech Debt

| Задача | Приоритет | Триггер | RICE | Примечание |
|--------|-----------|---------|------|------------|
| Функциональные тесты календаря | P0 | v0.15.0 | 100 × 2.0 × 80% / M=2, CP Med = **80.0** | Free Slot Algorithm, event patterns, conflict detection, JSON validation |
| Тесты целостности `SKILL.master.md` | P0 | v0.15.0 | 100 × 2.0 × 80% / M=2, CP Med = **80.0** | Structure, cross-reference validation, platform sync |
| Coverage report + badge | P1 | v0.15.0 | 80 × 1.0 × 75% / S=1, CP Low = **60.0** | `pytest-cov`, минимум 85%, badge в README |
| Pre-commit hooks | P1 | v0.15.0 | 80 × 1.0 × 70% / S=1, CP Med = **56.0** | `ruff`, `mypy`, whitespace |
| PoC MCP | P1 | v0.15.0 | 70 × 1.5 × 60% / M=2, CP High = **31.5** | OAuth + CRUD + `suggest_time` |
| Универсальный скрипт сборки | P2 | v0.15.0+ | 60 × 1.0 × 70% / M=2, CP Med = **21.0** | Единый `build-skill.py` |
| Planning docs guardrails | P2 | v0.15.0+ | 80 × 0.5 × 80% / XS=0.5, CP Low = **64.0** | Проверка, что roadmap не превращается в changelog |
| Timezone edge-case hardening | P2 | v0.16 candidate | 60 × 1.0 × 60% / M=2, CP Med = **18.0** | Travel, DST, смена рабочей зоны |

---

## Archived / Done

Детальные completed specs больше не хранятся в активном backlog. Источники:

- [CHANGELOG.md](CHANGELOG.md) — факты по выпущенным версиям.
- [ROADMAP.md](ROADMAP.md) — будущий committed scope.
- [references/archive/BACKLOG_before_cleanup_2026-05-21.md](references/archive/BACKLOG_before_cleanup_2026-05-21.md) — архив старого backlog.

Ключевые статусы, зафиксированные при чистке:

| Item | Статус |
|------|--------|
| Habit Loop | Реализовано в v0.8.0 |
| PDF export dashboard | Реализовано: `window.print()` + print CSS в `life-planning-dashboard.html` |
| Timezone intelligence | Базовая schema/preset support есть; edge-case hardening вынесен в tech debt |
| README rewrite + platform guides | Реализовано в v0.10.2 |
| Inclusive coaching references | Реализовано в v0.14.0 |

---

## Как работать с backlog

1. Новая идея попадает в `Active Candidates` или `Research Debt`.
2. У каждой активной записи должны быть триггер, статус и RICE.
3. Когда триггер сработал, задача переносится в `ROADMAP.md` с версией, приоритетом и acceptance criteria.
4. После релиза детали уходят в `CHANGELOG.md`; backlog хранит только активное и research debt.
