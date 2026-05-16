# Release Checklist v0.6.0

> **Кодовое имя:** Authentic Goals + Portfolio + Adaptive Style
> **Дата релиза:** 2026-05-16
> **Статус:** ✅ Завершён

---

## 1. Подготовка кода

- [x] Все фичи реализованы и протестированы
- [x] Все тесты проходят (`pytest` — зелёный)
- [x] SKILL.md не превышает лимит токенов (< 5000 слов)
- [x] Нет запрещённых слов в SKILL.md ("надо", "должен", "провал")

## 2. Синхронизация версий

- [x] `setup.py` — версия обновлена
- [x] `SKILL.md` frontmatter — версия обновлена
- [x] `README.md` — версия обновлена
- [x] `pyproject.toml` — удалён (дубль setup.py)
- [x] `PLAN-FINAL.md` — помечен как архивный
- [x] Скрипт `scripts/sync-version.sh` проверяет консистентность

## 3. Документация

- [x] README.md отражает актуальные фичи (11 сфер, Stage 1.5, стиль коммуникации)
- [x] Все references существуют и актуальны
- [x] Новые references добавлены в структуру проекта в README

## 4. Release Notes

- [x] Файл `RELEASE_NOTES_v0.6.md` подготовлен **на русском языке**
- [x] Release notes описывают все пользовательские изменения
- [x] Язык release notes проверен: содержит кириллицу

## 5. Git

- [x] Все изменения закоммичены
- [x] Commit message описывает суть изменений
- [x] **`git push origin main` выполнен**
- [x] **Проверка на GitHub: README.md показывает актуальную версию**
- [x] Тег `v0.6.0` создан (`git tag v0.6.0`)
- [x] Тег запушен на GitHub (`git push origin v0.6.0`)

## 6. GitHub Release

- [x] Release создан на GitHub через `gh release create`
- [x] Release notes **на русском языке**
- [x] ZIP-архив `life-planning-coach.zip` приложен к release
- [x] Legacy `.skill` файл приложен (backward compatibility)

## 7. Пост-релиз

- [x] PR создан и влит в `main`
- [x] Feature branch удалён
- [x] Тесты на `main` проходят
- [x] **Проверка: `git status` показывает `nothing to commit, working tree clean` и `Your branch is up to date with 'origin/main'`**
- [x] Release checklist заархивирован в `references/`

---

## Известные проблемы (исправлены ретроспективно)

| Проблема | Когда обнаружено | Как исправлено |
|----------|-----------------|----------------|
| README.md содержал версию 0.4.0 | После релиза | Обновлено до 0.6.0 |
| GitHub Release v0.6.0 был на английском | После релиза | Перезаписан на русский через `gh release edit` |
| pyproject.toml содержал версию 0.1.0 | Аудит версий | Удалён как дублирующий |

---

## Системные меры для будущих релизов

1. **Обязательный pre-release тест:** `pytest tests/system/` проверяет консистентность версий
2. **RELEASE_NOTES.md шаблон** — готовится заранее на русском
3. **Скрипт sync-version.sh** — единая команда для обновления всех версий
4. **Файл VERSION_SOURCES.md** — список всех мест с версией
