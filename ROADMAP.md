# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.
> **Как обновлять:** После каждого релиза переносить `In Progress` → `Done`, а `Planned` → `In Progress`.

---

## Текущий статус

| Версия | Статус | Ожидаемая дата | Ключевая фича |
|--------|--------|----------------|---------------|
| v0.6.0 | ✅ Released | 2026-05-16 | Authentic Goals + Portfolio + Adaptive Style |
| v0.7.0 | 🚧 Planned | TBD | Эмоциональная регуляция + Resilience |
| v0.8.0 | 📋 Planned | TBD | Интеграция привычек (Habit Loop) |
| v0.9.0 | 📋 Planned | TBD | Мобильная адаптация + краткие сессии |

---

## v0.7.0 — Эмоциональная регуляция + Resilience

**Цель:** Дать пользователю инструменты для управления эмоциональным состоянием на пути к целям.

**Планируемые фичи:**
- [ ] **Emotion Regulation Protocol** — 3 техники (cognitive reappraisal, breathing, grounding)
- [ ] **Resilience Assessment** — опросник на устойчивость к стрессу (Connor-Davidson или аналог)
- [ ] **Failure Recovery Protocol** — что делать, когда цель провалилась (не «провал», а «данные»)
- [ ] **Energy Management** — отслеживание энергии (не только времени)

**Методики:**
- Cognitive Reappraisal (Gross, 1998) — d = 0.45
- Self-Compassion (Neff) — связь с мотивацией
- Post-Traumatic Growth

**Детали планирования:** `references/plan_v0.7.0.md` (будет создан при старте разработки)

---

## v0.8.0 — Интеграция привычек (Habit Loop)

**Цель:** Мост между целями и ежедневными действиями через привычки.

**Планируемые фичи:**
- [ ] **Habit Loop Framework** — Cue-Routine-Reward + Implementation Intentions
- [ ] **Habit Tracker** — визуализация цепочек (streaks) в Dashboard
- [ ] **Tiny Habits** — методика BJ Fogg (начинать с 30 секунд)
- [ ] **Habit Stacking** — привязка к существующим рутинам

**Методики:**
- Tiny Habits (Fogg, 2019)
- Habit Stacking (Clear, 2018)
- Implementation Intentions (Gollwitzer) — уже используется в WOOP

---

## v0.9.0 — Мобильная адаптация + краткие сессии

**Цель:** Скилл должен работать эффективно на мобильных устройствах и в режиме нехватки времени.

**Планируемые фичи:**
- [ ] **5-Minute Micro-Sessions** — быстрые чек-ины (эмоция → 1 действие)
- [ ] **Voice-Optimized Output** — ответы, удобные для голосового чтения
- [ ] **Mobile Dashboard** — адаптивная версия HTML Dashboard
- [ ] **Quick Decision Protocol** — 2-3 вопроса для принятия решения «здесь и сейчас»

---

## Advanced Patterns — Research Debt (из AC v0.6, вынесено в v0.7)

Следующие паттерны были удалены из формальных Acceptance Criteria v0.7 как over-engineering для текущей версии, но сохранены как research direction в `references/communication_style.md`:

| Бывший AC | Паттерн | Почему вынесено | Когда вернуть |
|-----------|---------|-----------------|---------------|
| AC-13 | Attachment Style Awareness (4 стиля) | Невозможно протестировать без реальных пользователей; требует психометрии | v0.7+ при расширении Emotional Regulation |
| AC-14 | Dynamic Adaptation Triggers (5+ triggers) | Мета-уровень, покрывается AC-6 (4 квадранта); сложно измерить | v0.8+ при полноценном Habit Loop |
| AC-15 | Goal Ownership Language Rules | Дублирует AC-6/AC-7; лучше как style guide, не AC | Встроить в AC-6 как подпункт при рефакторинге Communication Style |

---

## Идеи без привязки к версии (см. BACKLOG.md)

| Идея | Триггер | Источник |
|------|---------|----------|
| Интеграция с Google Tasks MCP | Когда Tasks API станет доступен через MCP | Пользовательский запрос |
| Голосовые напоминания | Когда Claude.ai добавит голос | Технологический тренд |
| Групповые сессии (парный коучинг) | Когда 5+ пользователей запросят | Пользовательский запрос |
| Интеграция Fitness API (Apple Health, Google Fit) | При расширении сферы «Здоровье» | Расширение Wheel of Life |

---

## Как предложить фичу

1. Проверьте `BACKLOG.md` — возможно, идея уже записана
2. Создайте GitHub Issue с тегом `enhancement`
3. Или напишите в Telegram: [@zagreev](https://t.me/zagreev)

---

## Баг-трекер

Активные баги и известные проблемы — в [BUGS.md](BUGS.md).

## История изменений

Полный список изменений — в [CHANGELOG.md](CHANGELOG.md).
