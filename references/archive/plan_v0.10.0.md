# Plan v0.10.0 — Polish & Infrastructure

**Кодовое имя:** Cleanup & Guardrails  
**Цель:** Закрыть техдолг, упростить релизный процесс, отполировать существующие фичи. Нет новых user-facing фич.

---

## Scope

### Входит

| # | Задача | Файл | Effort | AC |
|---|--------|------|--------|-----|
| 1 | **CI/CD через GitHub Actions** | `.github/workflows/ci.yml` | 3ч | Тесты запускаются автоматически при push/PR |
| 2 | **Ревизия текстов событий календаря** | `references/calendar_constants.md` | 2ч | Все тексты событий проходят tone check (нет «надо/должен») |
| 3 | **Единые Release Notes из CHANGELOG** | `scripts/extract-release-notes.py` + `release.sh` | 1ч | Release.sh генерирует notes из CHANGELOG, RELEASE_NOTES*.md удалены |
| 4 | **PDF экспорт дашборда** | `life-planning-dashboard.html` | 1ч | Кнопка "Печать/PDF" → вызов window.print() с оптимизированными стилями |
| 5 | **Архивация старых планов** | `references/archive/` | 30мин | Все plan_v*.md и release_checklist_v*.md перенесены в archive |

### Не входит
- Новые reference-файлы (фичи)
- Изменения SKILL.md инструкций
- Dashboard redesign (уже сделан в v0.9.1)

---

## Порядок работы

1. Архивация старых планов (быстро, разогрев)
2. CI/CD (инфраструктура первой — чтобы тесты проверяли остальное)
3. Ревизия текстов календаря (контент)
4. PDF экспорт (фронтенд)
5. Единые Release Notes (скрипты)

---

## Риски

| Риск | Митигация |
|------|-----------|
| CI/CD сломает существующие workflows | Тестировать в отдельной ветке |
| RELEASE_NOTES удалены, release.sh сломан | Держать backup до первого успешного релиза |
| PDF стили конфликтуют с dark mode | `@media print` отдельно от темы |

---

## Release checklist

- [ ] Все 5 задач выполнены
- [ ] Тесты проходят (190+ passed)
- [ ] ROADMAP обновлён автоматически release.sh
- [ ] CHANGELOG.md обновлён
