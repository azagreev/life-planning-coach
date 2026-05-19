# Release v0.10.2

## Кратко

Hotfix: исправлены 4 критических бага в build pipeline + добавлен behavioral testing framework.

---

## Что исправлено

### BUG-004: Оставшийся "Загрузи" в Grok
- **Проблема:** `platforms/grok/SKILL.md:469` содержал `**Загрузи \`references/authentic_goal_filter.md\`...**` внутри инлайненного `diagnostic_methods.md`
- **Решение:** Добавлен фильтр в `condense_markdown()` — удаление строк с "Загрузи/Прочитай/См. + references/"

### BUG-005: Missing required sections в Grok/Kimi
- **Проблема:** В Grok/Kimi отсутствовали Examples, Gotchas, Troubleshooting, Privacy & Data Handling, References
- **Решение:** Исправлен `parse_frontmatter()` — horizontal rules (`---`) внутри инлайненных refs больше не ломают парсинг body

### BUG-006: Сломанная heading hierarchy
- **Проблема:** Инлайненные reference-файлы содержали H1/H2 заголовки, которые "прорывались" в иерархию SKILL.md
- **Решение:** Добавлен `demote_headings()` — сдвиг всех заголовков на 2 уровня вниз (H1→H3, H2→H4)

### BUG-007: Dashboard guide не инлайнен
- **Проблема:** `references/dashboard_guide.md` (2538 строк) не был доступен в Grok/Kimi single-file режиме
- **Решение:** Добавлен `condense_dashboard()` — агрессивное сжатие до coaching display rules + JSON data contract (~100 строк). Инлайнен в Grok/Kimi.

---

## Что добавлено

### Behavioral Testing Framework
- `tests/e2e/golden_dataset.json` — 20 тест-кейсов для cross-platform behavioral testing
- `tests/e2e/evaluation_rubric.md` — 5 критериев LLM-as-a-Judge (Stage Adherence, Tone Check, Tool Invocation, Safety, Platform Compliance)
- `tests/e2e/MANUAL_TEST_RUN.md` — пошаговый протокол ручного прогона через Claude/Grok/Kimi

---

## Артефакты

| Файл | Платформа | Размер |
|---|---|---|
| `life-planning-coach-v0.10.2.skill` | Claude.ai | ~164K |
| `life-planning-coach-v0.10.2.zip` | Claude.ai | ~164K |
| `life-planning-coach-v0.10.2-grok.md` | Grok 4.3 | ~1190 строк |
| `life-planning-coach-v0.10.2-kimi.md` | Kimi K2.6 | ~815 строк |

---

## Установка

**Claude.ai:**
1. Settings → Capabilities → enable 'Code execution and file creation'
2. Customize → Skills → '+' → 'Upload a skill'
3. Select: `life-planning-coach-v0.10.2.skill`

**Grok 4.3:**
1. Скопируйте `-grok.md` в Direct Prompt или Grok Project
2. `<details>` tags позволяют сворачивать инлайн-протоколы для экономии контекста

**Kimi K2.6:**
1. Скопируйте `-kimi.md` в `/app/.kimi/skills/life-planning-coach/SKILL.md`
2. Для полной диагностики используйте OK Computer mode (kimi.com/agent)

---

## Full Changelog

См. [CHANGELOG.md](https://github.com/azagreev/life-planning-coach/blob/main/CHANGELOG.md)
