# План релиза v0.7.0 — Minimal Scope

> **Статус:** Draft  
> **Дата планирования:** 2026-05-17  
> **Ожидаемая дата релиза:** TBD  
> **Scope:** Minimal — 3 задачи, ~6-7 часов

---

## Задачи

| # | Задача | Приоритет | Объём | Файлы |
|---|--------|-----------|-------|-------|
| 1 | **BUG-001: Dashboard 8→11 доменов** | P1 | 1-2ч | `life-planning-dashboard.html` |
| 2 | **Emotion Regulation Protocol** | P1 | 3-4ч | `SKILL.md`, `references/emotion_regulation.md` |
| 3 | **Фикс зависших тестов** | P1 | 1ч | `tests/release/test_metadata.py`, `tests/unit/test_dashboard.py`, `tests/system/test_version_consistency.py` |

---

## 1. BUG-001: Dashboard 8→11 доменов

### Что меняем
- `WHEEL_SPHERES` в `life-planning-dashboard.html`: 8 → 11 элементов
- Разделяем `family` → `family` (Семья) + `social` (Дружба)
- Добавляем `spirituality` (Духовность, смысл)
- Добавляем `contribution` (Вклад)
- Обновляем subtitle: "Баланс 8 сфер" → "Баланс 11 сфер"
- Обновляем делитель в `avg`: `/ 8` → `/ 11`

### 11 доменов (по AC-10 v0.7)
1. Здоровье и физическая форма
2. Финансы и материальное благополучие
3. Карьера и работа
4. Семья и близкие
5. Романтика и партнёрство
6. Дружба и социальные связи
7. Личностный рост и обучение
8. Духовность, смысл и ценности
9. Отдых, хобби и радость
10. Вклад в общество и наследие
11. Дом и окружение

### Критерий приёмки
- [ ] Дашборд открывается без ошибок в консоли
- [ ] Радарная диаграмма показывает 11 секторов
- [ ] Все 11 меток читаемы (не перекрываются)
- [ ] Средний счёт считается как сумма/11

---

## 2. Emotion Regulation Protocol

### Что добавляем
Новый reference-файл `references/emotion_regulation.md` с 3 техниками:
1. **Cognitive Reappraisal** — переосмысление ситуации (Gross, 1998)
2. **Grounding** — техники заземления (5-4-3-2-1 senses)
3. **Self-Compassion Break** — 3 шага Neff (mindfulness, common humanity, kindness)

### Интеграция в SKILL.md
- Новый раздел в Stage 0 (Emotional Landing) или отдельный Stage?
- Триггер активации: пользователь говорит о стрессе, тревоге, выгорании
- Не заменяет Emotional Landing, а дополняет

### Критерий приёмки
- [ ] Техники описаны с эффект-сайзами (Gross d=0.45, Neff r=0.47)
- [ ] SKILL.md содержит триггеры для активации
- [ ] Не нарушает правило «без давления» (нет «надо»/«должен»)
- [ ] Интегрирован с Communication Style (адаптация под Big Five)

---

## 3. Фикс зависших тестов

### test_skill_archive_structure
- [ ] Путь: `dist/life-planning-coach-v*.zip` вместо корня
- [ ] Required: только `SKILL.md` + `references/` + `life-planning-dashboard.html`
- [ ] Убрать README.md, LICENSE, CONTRIBUTING.md, SECURITY.md из required

### test_dashboard.py
- [ ] Добавить `test_wheel_has_11_domains`
- [ ] Проверить `WHEEL_SPHERES.length === 11`
- [ ] Проверить наличие всех 11 id: health, finances, career, family, romance, social, growth, spirituality, fun, contribution, environment

### test_github_release_exists_for_tag
- [ ] Добавить whitelist: `v0.2.0` — тег без релиза (ожидаемо)
- [ ] Или: проверять только если тег === `v0.6.1` (latest)

---

## Не входит в v0.7.0 (отложено)

| Задача | Почему отложено | Когда |
|--------|-----------------|-------|
| Resilience Assessment | Требует психометрии, сложно валидировать | v0.7.1 |
| Failure Recovery Protocol | Связано с Resilience | v0.7.1 |
| Energy Management | Отдельная большая фича | v0.7.1 |
| Recovery Protocol для сессий | Не критично для v0.7.0 | v0.7.1 или v0.8.0 |
| Calendar Event Copy Review | UX-улучшение, не блокер | v0.7.1 |
| Dashboard Self-Contained | Большой рефакторинг, риск затягивания | v0.8.0 |

---

## Чеклист перед релизом

- [ ] Все 3 задачи выполнены
- [ ] Тесты проходят (включая новые)
- [ ] SKILL.md обновлён (version: 0.7.0)
- [ ] CHANGELOG.md обновлён
- [ ] `bash scripts/build-skill.sh` собирает ZIP
- [ ] `bash scripts/release.sh 0.7.0` проходит
