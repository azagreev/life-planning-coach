# Чеклист релиза: Персистентность данных v0.4.0

## Версия: v0.4.0
## Кодовое имя: Foundation
## Дата планируемого релиза: [YYYY-MM-DD]

---

## Фаза 1: Подготовка (Pre-Release)

### Разработка
- [ ] Разработчик завершил работу по `developer_task_v0.4.md`
- [ ] SKILL.md обновлён (Уровень 1 + Уровень 2)
- [ ] README.md обновлён
- [ ] RELEASE_NOTES_v0.4.md создан
- [ ] Все файлы прошли self-review

### Код-ревью
- [ ] SKILL.md — review на непротиворечивость
- [ ] SKILL.md — review на понятность для Claude
- [ ] README.md — review на точность информации
- [ ] Нет breaking changes без migration guide

---

## Фаза 2: Тестирование (QA)

### Инспекция (Review-based)
- [ ] Тестировщик назначен
- [ ] Тестировщик прочитал `acceptance_criteria_v0.4.md`
- [ ] Тестировщик прочитал обновлённый `SKILL.md`
- [ ] Тестовый отчёт создан: `references/tasks/test_report_v0.4.md`

### Результаты тестирования
- [ ] Все P0-критерии: PASS (11/11)
- [ ] ≥80% P1-критериев: PASS (≥5/6)
- [ ] Нет critical bugs
- [ ] Нет блокирующих issues

### Решение по релизу
- [ ] **GO** — если все P0 пройдены
- [ ] **NO-GO** — если есть непройденные P0
- [ ] **CONDITIONAL GO** — если есть P1-failures, но есть план hotfix'а

---

## Фаза 3: Документация (Documentation)

### Release Notes
- [ ] Файл `RELEASE_NOTES_v0.4.md` создан и проверен
- [ ] Содержит: What's New, Breaking Changes, Migration, Known Issues

### README
- [ ] Обновлена секция "Возможности" (features)
- [ ] Обновлена секция "FAQ"
- [ ] Обновлена секция "Установка" (если изменилась)
- [ ] Версия в README актуальна

### CHANGELOG (проектный)
- [ ] Файл `CHANGELOG.md` обновлён (если есть)
- [ ] Запись о v0.4.0 добавлена

---

## Фаза 4: Git-операции (Release)

### Коммиты
- [ ] Все изменения закоммичены
- [ ] Коммит-сообщение содержит: `feat(persistence): v0.4.0 — two-tier persistence`
- [ ] Нет uncommitted changes

### Тег
- [ ] Тег `v0.4.0` создан: `git tag -a v0.4.0 -m "Release v0.4.0: Two-tier persistence (Memory + Drive Wiki)"`
- [ ] Тег запушен: `git push origin v0.4.0`

### Версия
- [ ] Версия в SKILL.md обновлена: `version: 0.4.0`
- [ ] Версия в README.md обновлена (если указана)

---

## Фаза 5: Пост-релиз (Post-Release)

### Проверка
- [ ] Тег `v0.4.0` доступен на GitHub
- [ ] Release notes опубликованы (GitHub Release)
- [ ] README отображается корректно на GitHub

### Коммуникация
- [ ] (Опционально) Обновить описание проекта
- [ ] (Опционально) Поделиться в соцсетях / с тестировщиками

---

## Артефакты релиза

| Артефакт | Путь | Статус |
|----------|------|--------|
| SKILL.md | `SKILL.md` | |
| README.md | `README.md` | |
| Release Notes | `RELEASE_NOTES_v0.4.md` | |
| Test Report | `references/tasks/test_report_v0.4.md` | |
| Research Plan | `references/persistence_research_plan.md` | (уже есть) |
| Acceptance Criteria | `references/acceptance_criteria_v0.4.md` | (уже есть) |

---

## Решение

| Поле | Значение |
|------|----------|
| Релиз одобрен | [ ] Да / [ ] Нет |
| Дата релиза | |
| Ответственный за релиз | |
| Примечания | |
