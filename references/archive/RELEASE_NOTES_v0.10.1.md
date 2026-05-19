# Release v0.10.1

## Кратко

Hotfix: инлайн 7 критичных reference-файлов в Grok и Kimi SKILL.md. Исправлены BUG-002 и BUG-003.

---

## Что исправлено

### BUG-002: Grok Web Chat — broken references
- **Проблема**: `platforms/grok/SKILL.md` (326 строк) содержал 21 ссылку "Загрузи `references/...`", которые не работали в Grok Web Chat (нет файловой системы).
- **Решение**: 7 критичных P0-файлов инлайнены через `<details>` tags:
  - `diagnostic_methods.md` (436 → 111 строк)
  - `communication_style.md` (365 → 156 строк)
  - `authentic_goal_filter.md` (322 → 147 строк)
  - `goal_architecture.md` (257 → 30 строк)
  - `weekly_review.md` (256 → 49 строк)
  - `habit_loop.md` (254 → 115 строк)
  - `emotion_regulation.md` (198 → 115 строк)
- Остальные 14 P1/P2 reference-файлов: инструкции "Загрузи" заменены на нейтральные "См."

### BUG-003: Kimi OK Computer — broken references
- **Проблема**: `platforms/kimi/SKILL.md` (312 строк) содержал те же 21 неработающую ссылку в single-file режиме OK Computer.
- **Решение**: Те же 7 файлов инлайнены в агрессивно сжатом виде (ultra-condensed):
  - `diagnostic_methods.md` (436 → 47 строк)
  - `communication_style.md` (365 → 69 строк)
  - `authentic_goal_filter.md` (322 → 68 строк)
  - `goal_architecture.md` (257 → 21 строк)
  - `weekly_review.md` (256 → 32 строк)
  - `habit_loop.md` (254 → 65 строк)
  - `emotion_regulation.md` (198 → 74 строк)

---

## Артефакты

| Файл | Платформа | Размер |
|---|---|---|
| `life-planning-coach-v0.10.1.skill` | Claude.ai | ~164K |
| `life-planning-coach-v0.10.1.zip` | Claude.ai | ~164K |
| `life-planning-coach-v0.10.1-grok.md` | Grok 4.3 | ~1270 строк |
| `life-planning-coach-v0.10.1-kimi.md` | Kimi K2.6 | ~740 строк |

---

## Установка

**Claude.ai:**
1. Settings → Capabilities → enable 'Code execution and file creation'
2. Customize → Skills → '+' → 'Upload a skill'
3. Select: `life-planning-coach-v0.10.1.skill`

**Grok 4.3:**
1. Скопируйте `-grok.md` в Direct Prompt или Grok Project
2. `<details>` tags позволяют сворачивать инлайн-протоколы для экономии контекста

**Kimi K2.6:**
1. Скопируйте `-kimi.md` в `/app/.kimi/skills/life-planning-coach/SKILL.md`

---

## Full Changelog

См. [CHANGELOG.md](https://github.com/azagreev/life-planning-coach/blob/main/CHANGELOG.md)
