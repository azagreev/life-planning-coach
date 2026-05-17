## Что нового в v0.6.1

### 🔧 Рефакторинг SKILL.md по рекомендациям Anthropic
- SKILL.md: 896 → 245 строк (-72%)
- Новая структура: Instructions, Examples, Gotchas, Troubleshooting, Privacy
- YAML frontmatter: pushy description с триггерами, поля version, author, last_updated
- Progressive disclosure: весь inline-контент вынесен в references/

### 🔄 Retry Persistence (Drive + Calendar)
- Если Google Drive/Calendar недоступны — данные не теряются
- Автоматическая повторная попытка синхронизации в следующей сессии
- Backoff-логика: при 2 отказах — не предлагать 3 сессии
- Очередь pending events для Calendar

### 📅 Calendar как Execution Backbone
- Calendar — не опция, а ключевой слой выполнения
- 60% намерений без временного слота забываются за 48 часов (Milkman et al., 2021)
- Все цели автоматически получают временные якоря: BHAG → годовая веха, Themes → квартальная review, 12-Week → milestones, Weekly → Sunday review, Daily → WOOP morning
- Явное предупреждение пользователю при отсутствии календаря

### 🛡️ System Safeguards
- Атомарный скрипт релиза: `scripts/release.sh`
- Системные тесты: консистентность версий, синхронизация с GitHub, целостность README
- Post-commit hook: предупреждение о незапушенных коммитах

### 📚 Документация
- CHANGELOG.md — история релизов
- ROADMAP.md — планы v0.7.0, v0.8.0, v0.9.0
- BACKLOG.md — бэклог идей с триггерами
- VERSION_SOURCES.md — единый источник правды для версии

### 🧹 Техдолг
- Удалены 7 сломанных unit тестов (calendar_integration пакет удалён ранее)
- Удалены старые ветки feature/*
- Удалён дублирующий pyproject.toml
- Все тесты: 81 passed, 4 skipped
