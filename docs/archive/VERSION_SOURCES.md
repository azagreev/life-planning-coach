# Единый источник правды для версии

## Источник правды

**Git tag** — единственный источник правды для версии проекта.

```bash
git describe --tags --abbrev=0
# → v0.6.0
```

## Где используется версия

| Файл | Тип | Как обновляется | Примечание |
|------|-----|-----------------|------------|
| `setup.py` | Python package | `scripts/sync-version.sh` | Основной package metadata |
| `SKILL.md` | Skill frontmatter | `scripts/sync-version.sh` | Claude.ai использует для идентификации |
| `README.md` | Документация | `scripts/sync-version.sh` | Для пользователей |
| Git tag | Git | `git tag vX.Y.Z` | Источник правды |
| GitHub Release | GitHub | `gh release create` | Для пользователей, содержит ZIP |

## Архивные / не обновляемые

| Файл | Почему не обновляется |
|------|----------------------|
| `PLAN-FINAL.md` | Исторический документ планирования v0.2.0 |
| `references/release_checklist_v*.md` | Архивные чеклисты предыдущих релизов |
| `references/tasks/*.md` | Отчёты о тестировании конкретных версий |

## Удалённые / больше не используются

| Файл | Причина удаления |
|------|-----------------|
| `pyproject.toml` | Дублировал `setup.py`, никогда не обновлялся |

## Workflow обновления версии

1. Выполнить все фичи и тесты
2. `bash scripts/sync-version.sh 0.7.0`
3. Проверить `git diff`
4. `git add -A && git commit -m "release: bump version to 0.7.0"`
5. `git tag v0.7.0`
6. `git push origin main && git push origin v0.7.0`
7. Подготовить `RELEASE_NOTES_v0.7.md` на **русском языке**
8. `gh release create v0.7.0 --notes-file RELEASE_NOTES_v0.7.md --title "v0.7.0 — ..."`
9. Прикрепить ZIP и `.skill` к release
