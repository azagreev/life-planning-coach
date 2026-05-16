# Contributing to Life Planning Coach

Спасибо за интерес к проекту! Это open-source скилл для Claude, и любые улучшения приветствуются.

## Как внести вклад

1. **Форкните** репозиторий
2. **Создайте ветку** для ваших изменений: `git checkout -b feature/название`
3. **Внесите изменения** и убедитесь, что:
   - Python-код проходит `py_compile`
   - Release-тесты проходят: `python -m unittest discover -s tests/release -v`
4. **Закоммитьте** с понятным сообщением
5. **Откройте Pull Request** с описанием изменений

## Что приветствуется

- Исправления ошибок в методиках или эффект sizes
- Улучшения dashboard (новые визуализации, accessibility)
- Дополнительные life-planning пресеты для Calendar Integration
- Переводы документации
- Тесты для Python-модуля

## Что НЕ приветствуется

- Изменения core-философии без обсуждения (Evidence-Based, Emotional Landing, Progressive Disclosure)
- Добавление зависимостей без явной необходимости
- Breaking changes в JSON-схеме Conversation State без миграции

## Соглашения

- Язык: русский для user-facing текста, английский для кода и комментариев
- Формат дат: `YYYY-MM-DD` в коде, `день месяц год` в changelog
- Версионирование: semver (`MAJOR.MINOR.PATCH`)

## Обратная связь

Telegram: [@zagreev](https://t.me/zagreev)
