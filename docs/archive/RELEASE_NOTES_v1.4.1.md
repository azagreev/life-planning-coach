## Что нового в v1.4.1

**Тема:** Patch release. Post-v1.4.0 project-wide audit fixes — корректность данных в docs, устранение overlap категорий Health Index на границе 5.0, и hardening release-тулинга (BUG-015, `--clean-prev`, release.sh pytest). Без новых features; поведение методологии не меняется, кроме disambiguation границы 5.0.

### Fixed

- **Health Index / Snapshot Index — overlap категорий на границе 5.0** (#37). «Низкий» был определён как `≤ 5.0`, тогда как «Средний» начинался с `5.0` (диапазон 5.0–6.4) — счёт, округлённый ровно до 5.0, попадал в обе категории, давая ambiguous routing Health Track (strongly-offer vs soft-offer). Теперь «Низкий» строго `< 5.0` (1.0–4.9); 5.0 → только «Средний». Исправлено во всех source-локациях: `references/state_v2_schema.md` (§3.4.5 / §3.4.6 / §12), `references/wol_health_subsegments.md`, `references/health_snapshot.md`, `references/evidence_map.md`. НЕ schema bump (prose/categorization correction; stored doc байт-совместим). Добавлен parametrized regression guard `TestHealthIndexBoundaryNoOverlap` по всем reference-докам. Пороги `≤ 5.5` (launch trigger) и `≤ 3` (safety escalation) не затронуты.
- **`scripts/release.sh` step 2.5 оставлял released-version section в ROADMAP** (BUG-015, #39). Step 2.5 удалял только legacy `| vX.Y.Z |` status-row, оставляя `## vX.Y.Z (planned) …` detail section → post-tag CI падал на `test_roadmap_integrity`, требуя ручной cleanup PR после каждого релиза. Новый subcommand `build-skill.py roadmap-cleanup` (pure-Python helper `_strip_roadmap_version`) robustly удаляет секцию + row, с cleanup orphaned `---` separator; `cmd_release` получил parity. 6 unit-тестов.
- **`scripts/build-skill.py --clean-prev` был no-op** (#38). Inverted `continue` guard без `unlink`/`rmtree` → флаг ничего не удалял. Реализован `_clean_prev_artifacts()`; argparse help исправлен. Добавлены регрессионные тесты.
- **`scripts/release.sh` precondition tests использовали bare `pytest`** (#38) — заменено на `"$PYTHON_BIN" -m pytest` (consistency с BUG-013 interpreter resolution; bare `pytest` может отсутствовать / resolve'иться неверно на Windows MSYS).
- **Stale данные в docs** (#36): test counts → `900+` (фактически 920+ collected), таблица статистики в `BUGS.md`, dead link в `ROADMAP.md` (`references/` → `docs/planning/`), устаревшая ссылка в `BACKLOG.md` (`[Unreleased]` → `[1.3.1]`).

### Changed (Tests — integrity)

- De-vacuoused `test_master_does_not_have_phase0_com_b_trigger` (#38): premise-assert вместо silently-skipped `if idx != -1` wrapper.
- Version-checks в `test_methodology_v1_3.py` (#38) scoped к §12 Changelog (history-preservation guard вместо global substring match).
