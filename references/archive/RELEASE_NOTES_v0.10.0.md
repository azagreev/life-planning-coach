# Release v0.10.0

## Кратко

Мульти-платформенная адаптация скилла и исправление критических ошибок в документации Grok 4.3.

---

## Что нового

### Multi-Platform Skill Adaptation
- **Claude.ai** (primary) — ZIP-архив `.skill`, MCP-интеграция, Claude Memory
- **Grok 4.3** (xAI) — plain `SKILL.md`, sandbox tools, native persistent memory, native connectors (Google Calendar, Google Drive, Outlook), `render_file` для дашборда
- **Kimi K2.6** (Moonshot AI) — plain `SKILL.md`, `memory_space` tool, `KIMI_REF` для артефактов
- Архитектура: `SKILL.master.md` + `references/platforms/{claude,grok,kimi}.overlay.yaml` + генератор `scripts/build-platform-skill.py`
- Поддержка cross-platform continuity — чтение существующей wiki из Google Drive при переходе между платформами

### Grok 4.3 — исправление 4 критических ошибок
- ✅ **Persistent Memory**: Grok имеет native memory (апрель 2025), Grok Projects, Skills, Collections
- ✅ **Calendar**: native Google Calendar + Outlook connectors (OAuth, CRUD, RSVP)
- ✅ **Drive**: native Google Drive connector (search/read/write/upload) — не MCP
- ✅ **`render_file`**: существует как render component (не API tool)

### Документация
- Полный user guide для Grok 4.3 с 4 методами установки: Direct Prompt, Grok Projects, Skills Directory, API + Collections
- Пошаговая настройка connectors и Persistent Memory
- Инструкция cross-platform continuity для перехода с Claude/Kimi

### Тесты
- 53 consistency tests (`+11` фактчек-тестов для Grok)
- Полная проверка: 249 passed, 5 skipped

---

## Артефакты

| Файл | Платформа | Размер |
|---|---|---|
| `life-planning-coach-v0.10.0.skill` | Claude.ai | ~164K |
| `life-planning-coach-v0.10.0.zip` | Claude.ai | ~164K |
| `life-planning-coach-v0.10.0-grok.md` | Grok 4.3 | ~2760 слов |
| `life-planning-coach-v0.10.0-kimi.md` | Kimi K2.6 | ~2612 слов |

---

## Установка

**Claude.ai:**
1. Settings → Capabilities → enable 'Code execution and file creation'
2. Customize → Skills → '+' → 'Upload a skill'
3. Select: `life-planning-coach-v0.10.0.skill`

**Grok 4.3:**
1. Создайте Grok Project или скопируйте `-grok.md` в Direct Prompt
2. Подключите Google Calendar и Google Drive через grok.com/connectors
3. Включите Persistent Memory в Settings → Data Controls

**Kimi K2.6:**
1. Скопируйте `-kimi.md` в `/app/.kimi/skills/life-planning-coach/SKILL.md`

---

## Full Changelog

См. [CHANGELOG.md](https://github.com/azagreev/life-planning-coach/blob/main/CHANGELOG.md)
