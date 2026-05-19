# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.
> **Как обновлять:** `release.sh` управляет статусом автоматически. Ручное редактирование таблицы запрещено.

---

## Текущий статус

> Факты о выпущенных версиях — в [CHANGELOG.md](CHANGELOG.md). Эта таблица содержит только будущее.

| Версия | Статус | Ожидаемая дата | Ключевая фича |
|--------|--------|----------------|---------------|

---

## История релизов

Полный список выпущенных версий — в [CHANGELOG.md](CHANGELOG.md).

<details>
<summary><strong>v0.7.0 — v0.9.1 (выпущено, кликни для деталей)</strong></summary>

### v0.9.1 — Apple-style Dashboard Redesign
- Activity Rings (SVG), Liquid Glass карточки, Dark/Light mode
- Размер: 1,403 KB → ~61 KB (23× уменьшение)
- Удалены внешние зависимости (ECharts, Chart.js, Font Awesome)

### v0.9.0 — Мобильная адаптация + Habit Tracker
- Habit streaks в дашборде, mobile responsive
- 5-Minute Micro-Sessions, Quick Decision Protocol
- Reward Audit (Dopamine Budget)

### v0.8.0 — Habit Loop Framework + Execution Layer v2
- Habit Loop (Cue-Routine-Reward, Tiny Habits, Habit Stacking)
- Task Breakdown with Checkpoints, Markdown Tables as UI
- Weak Goal Taxonomy + Sanity-Check

### v0.7.1 — Execution Layer Patch
- Win Alert Protocol, Recovery Protocol MVP, Energy-Based Scheduling

### v0.7.0 — Эмоциональная регуляция
- Emotion Regulation Protocol (cognitive reappraisal, grounding, self-compassion)
- Dashboard 8→11 доменов (BUG-001 fix)
</details>

---

## v0.10.0 — Polish & Infrastructure

**Цель:** Закрыть техдолг, упростить релизный процесс, отполировать существующие фичи.

**Scope:**
- [x] **Multi-Platform Skill Adaptation** — Claude.ai, Grok (xAI), Kimi OK Computer. `SKILL.master.md` + overlays + `build-platform-skill.py`. 42+ consistency tests.
- [x] **Kimi Code CLI support** — directory-based skill с `references/` + MCP (v0.10.2)
- [x] **README rewrite + USER_GUIDEs** — 4 platform guides + cross-platform comparison (v0.10.2)
- [x] **E2E behavioral testing** — golden dataset + evaluation rubric (v0.10.2)
- [ ] **CI/CD через GitHub Actions** — автоматический запуск тестов при push/PR
- [ ] **Ревизия текстов событий календаря** — tone check, нет «надо/должен»
- [ ] **Единые Release Notes из CHANGELOG** — генерация из CHANGELOG.md
- [ ] **PDF экспорт дашборда** — кнопка печати/PDF
- [ ] **Архивация старых планов** — перенос plan_v*.md в references/archive/

---

## v0.10.2 — README Rewrite & Kimi CLI (Released)

**Цель:** Исправить катастрофу README.md, добавить Kimi Code CLI как 4-ю платформу, создать полноценную документацию по платформам.

**Выполнено:**
- Полный rewrite README.md — value prop + quick-start + platform table
- Kimi Code CLI: `platforms/kimi-cli/SKILL.md` (323 lines), overlay, MCP support
- 4 USER_GUIDE: Claude, Grok, Kimi OK Computer, Kimi Code CLI
- `CROSS_PLATFORM_COMPARISON.md` — feature matrix + decision tree
- E2E framework: `golden_dataset.json` (20 cases), `evaluation_rubric.md`, `MANUAL_TEST_RUN.md`
- Исправлены BUG-002..BUG-007 (inline refs, heading demotion, dashboard condense)
- Удалён `RETRO_v091_v092.md` из публичного репозитория

---

## Advanced Patterns — Research Debt

Следующие паттерны сохранены как research direction в `references/communication_style.md`:

| Паттерн | Почему вынесено | Когда вернуть |
|---------|-----------------|---------------|
| Attachment Style Awareness (4 стиля) | Невозможно протестировать без реальных пользователей; требует психометрии | v0.11+ при расширении Emotional Regulation |
| Dynamic Adaptation Triggers (5+ triggers) | Мета-уровень, покрывается 4 квадранта; сложно измерить | v0.11+ при полноценном Habit Loop |
| Goal Ownership Language Rules | Дублирует Communication Style; лучше как style guide | Встроить в AC-6 как подпункт |

---

## Идеи без привязки к версии (см. BACKLOG.md)

| Идея | Триггер | Источник |
|------|---------|----------|
| Интеграция с Google Tasks MCP | Когда Tasks API станет доступен через MCP | Техническое ограничение |
| Голосовые напоминания | Когда Claude.ai добавит голос | Технологический тренд |
| Групповые сессии (парный коучинг) | Когда 5+ пользователей запросят | Пользовательский запрос |
| Интеграция Fitness API (Apple Health, Google Fit) | При расширении сферы «Здоровье» | Расширение Wheel of Life |
| Мультиязычность (EN/RU toggle) | 10+ запросов от англоязычных пользователей | Потенциал open source |

---

## Как предложить фичу

1. Проверьте `BACKLOG.md` — возможно, идея уже записана
2. Создайте GitHub Issue с тегом `enhancement`
3. Или напишите в Telegram: [@zagreev](https://t.me/zagreev)

---

## Баг-трекер

Активные баги и известные проблемы — в [BUGS.md](BUGS.md).
