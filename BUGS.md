# Bug Tracker

> Живой список багов и известных проблем проекта life-planning-coach.
> Правило: каждый баг получает ID, приоритет, статус и owner.
> При закрытии бага — добавить resolution и дату закрытия.

---

## Формат бага

```markdown
### BUG-NNN: <Краткое название>
- **Приоритет:** P0/P1/P2
- **Статус:** open / in_progress / resolved / wont_fix
- **Найден:** YYYY-MM-DD
- **Версия:** vX.Y.Z
- **Owner:** @username
- **Файлы:** `path/to/file`

**Описание:**
<Что происходит>

**Expected:**
<Что должно быть>

**Actual:**
<Что происходит сейчас>

**Steps to reproduce:**
1. ...
2. ...

**Root cause (если известен):**
<Почему это происходит>

**Resolution (при закрытии):**
<Как исправлено>
```

---

## Открытые баги

### BUG-002: `grok.md` ссылается на 21 внешний reference-файл, недоступный при создании Grok Skill
- **Приоритет:** P0
- **Статус:** open
- **Найден:** 2026-05-18
- **Версия:** v0.10.0
- **Owner:** @azagreev
- **Файлы:** `platforms/grok/SKILL.md`, `dist/life-planning-coach-v0.10.0-grok.md`

**Описание:**
`platforms/grok/SKILL.md` содержит 21 ссылку на файлы из папки `references/*.md` (например: «Загрузи `references/diagnostic_methods.md` перед началом Stage 1»). При создании Grok Skill через веб-UI (вставка текста в поле Instruction) эти файлы не загружаются — Grok получает только 326 строк основного SKILL.md, но не 5879 строк детальных протоколов.

**Expected:**
Grok Skill содержит все необходимые инструкции для полноценной работы всех Stage (1-4), либо reference-файлы доступны через механизм загрузки дополнительных файлов.

**Actual:**
Grok получает только основные инструкции. Команды вида «Загрузи references/...» не выполняются, так как файлы отсутствуют в контексте скилла. Качество коучинга падает: нет детальных протоколов Emotional Landing, Wheel of Life, Authentic Goal Filter, Dashboard и др.

**Steps to reproduce:**
1. Скачать `life-planning-coach-v0.10.0-grok.md` из релиза v0.10.0
2. Создать Grok Project → Create Skill → вставить текст из файла в поле Instruction
3. Активировать скилл: `/life-planning-coach`
4. Попросить начать Stage 1 (Emotional Landing + Wheel of Life)
5. Grok не имеет доступа к `references/diagnostic_methods.md` — протоколы упрощаются или игнорируются

**Root cause:**
- Claude ZIP содержит папку `references/` со всеми файлами — Claude загружает ZIP целиком
- Grok Skills UI (веб) поддерживает только одно поле Instruction (один markdown-файл)
- Мы убрали Methods 1, 2, 4 и оставили только Grok Skills — но не адаптировали контент под single-file ограничение
- Progressive Disclosure предполагает, что тяжёлый контент в `references/` — но для Grok нет механизма подгрузки

**Affected references (21 files, 5879 lines):**
| Файл | Строк | Stage |
|------|-------|-------|
| `diagnostic_methods.md` | 436 | Stage 1 |
| `authentic_goal_filter.md` | 322 | Stage 1.5 |
| `dashboard_guide.md` | 2538 | Stage 4 |
| `goal_architecture.md` | 257 | Stage 2 |
| `communication_style.md` | 365 | Style Calibration |
| `weekly_review.md` | 256 | Stage 3 |
| `emotion_regulation.md` | 198 | ER Protocol |
| `habit_loop.md` | 254 | Привычки |
| `action_breakdown_template.md` | 128 | Действия |
| `calendar_constants.md` | 134 | Calendar |
| ... + 11 файлов | ... | ... |

**Potential solutions:**
1. **Inline critical refs** — встроить ~10 ключевых файлов в grok.md, урезав до минимума (риск: превысит лимит 500 строк)
2. **Self-contained grok.md** — переписать все «Загрузи X» на краткие inline-протоколы
3. **Multi-file upload** — проверить, поддерживает ли Grok Skills UI загрузку доп. файлов (Resources/Files)
4. **Separate grok ZIP** — создать ZIP-артефакт с SKILL.md + references/ для Grok (если Grok Build CLI поддерживает)

---

### BUG-003: `kimi.md` ссылается на 21 внешний reference-файл, недоступный в Kimi OK Computer mode
- **Приоритет:** P0
- **Статус:** open
- **Найден:** 2026-05-18
- **Версия:** v0.10.0
- **Owner:** @azagreev
- **Файлы:** `platforms/kimi/SKILL.md`, `dist/life-planning-coach-v0.10.0-kimi.md`

**Описание:**
`platforms/kimi/SKILL.md` содержит те же 21 ссылку на `references/*.md`, что и grok.md. Kimi OK Computer mode (`kimi.com/agent`) загружает только `SKILL.md` из `/app/.kimi/skills/life-planning-coach/SKILL.md` — reference-файлы не подгружаются автоматически.

**Expected:**
Kimi Skill содержит все необходимые протоколы для работы всех Stage.

**Actual:**
Kimi получает только 312 строк основного SKILL.md. Команды «Загрузи references/...» не выполняются. Нет доступа к diagnostic_methods.md, authentic_goal_filter.md, dashboard_guide.md и др.

**Steps to reproduce:**
1. Скопировать `life-planning-coach-v0.10.0-kimi.md` в `/app/.kimi/skills/life-planning-coach/SKILL.md`
2. Открыть `kimi.com/agent` (OK Computer mode)
3. Активировать скилл
4. Попросить начать Stage 1 — Kimi не имеет доступа к детальным протоколам

**Root cause:**
Тот же, что и BUG-002: мульти-платформенная генерация (`build-platform-skill.py`) создаёт `SKILL.md` для каждой платформы, но не инлайнит reference-файлы. Клиентские платформы (Kimi, Grok) не имеют механизма авто-подгрузки `references/`.

**Affected references:**
Идентичны BUG-002: 21 файла, 5879 строк.

**Potential solutions:**
1. **Inline refs into kimi.md** — встроить протоколы прямо в SKILL.md
2. **Kimi-specific packaging** — проверить, поддерживает ли Kimi загрузку доп. файлов в skill-директорию
3. **Unified fix with BUG-002** — изменить генератор `build-platform-skill.py`, чтобы он инлайнил критичные refs для платформ без auto-load

---

---

## Закрытые баги

### BUG-001: Dashboard показывает 8 сфер Wheel of Life вместо 11
- **Приоритет:** P1
- **Статус:** resolved
- **Исправлено:** 2026-05-17
- **Найден:** 2026-05-17
- **Версия:** v0.6.1
- **Owner:** @azagreev
- **Файлы:** `life-planning-dashboard.html`

**Описание:**
HTML Dashboard (`life-planning-dashboard.html`) содержит старую реализацию Wheel of Life с 8 сферами. В v0.6.0 количество сфер было расширено до 11, но дашборд не обновлён.

**Expected:**
Дашборд отображает 11 сфер Wheel of Life, соответствующих AC-10 v0.7:
1. Здоровье и физическая форма
2. Финансы и материальное благополучие
3. Карьера и работа
4. Семья и близкие
5. Романтика и партнёрство
6. Дружба и социальные связи
7. Личностный рост и обучение
8. Духовность, смысл и ценности *(обязательный)*
9. Отдых, хобби и радость
10. Вклад в общество и наследие
11. Дом и окружение

**Actual (было):**
Дашборд отображал только 8 сфер.

**Root cause:**
Дашборд не обновлялся после расширения Wheel of Life с 8 до 11 сфер в v0.6.0. Константа `WHEEL_SPHERES` в JS содержала 8 элементов.

**Resolution:**
- `WHEEL_SPHERES` расширен с 8 до 11 элементов
- Разделён `family` → `family` (Семья) + `social` (Дружба)
- Добавлены `spirituality` (Духовность, смысл) и `contribution` (Вклад)
- Обновлён subtitle: "Баланс 8 сфер" → "Баланс 11 сфер"
- Обновлён делитель среднего: `/ 8` → `/ 11`
- Добавлены CSS-переменные для новых сфер
- Добавлен тест `test_wheel_has_11_domains`

---

## Статистика

| Метрика | Значение |
|---------|----------|
| Открыто | 2 |
| In Progress | 0 |
| P0 | 2 |
| P1 | 0 |
| P2 | 0 |
| Закрыто | 1 (BUG-001) |
