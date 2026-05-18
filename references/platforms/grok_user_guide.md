# User Guide: Life Planning Coach на Grok 4.3 (xAI)

> **Важно:** Grok 4.3 не имеет официального Skill Store. Этот гайд описывает 4 проверенных способа загрузки скилла в Grok — от простого к продвинутому.

---

## Предварительные требования

| Что нужно | Зачем |
|-----------|-------|
| Аккаунт xAI (grok.com) | Доступ к Grok 4.3 |
| Скачанный `life-planning-coach-vX.Y.Z-grok.md` | Файл скилла для Grok |
| Любой текстовый редактор | Для копирования содержимого |

**Возможности Grok 4.3:** ✅ Persistent memory • ✅ Native Google Calendar connector • ✅ Native Google Drive connector • ✅ Sandbox file I/O (`read_file`, `write_file`, `edit_file`, `bash`) • ✅ Web search и image generation • ✅ Grok Projects • ✅ Skills (forthcoming, leaked UI: Name/Description/Instruction + .md import) • ✅ Collections • ✅ `render_file` component

---

## Способ 1. Direct Prompt (простой, 2 минуты)

**Лучше для:** быстрого знакомства, тестирования, одноразовых сессий.

### Шаг 1. Открыть Grok
1. Перейди на [grok.com](https://grok.com) или открой мобильное приложение
2. Убедись, что выбрана модель **Grok 4.3**

### Шаг 2. Вставить скилл
1. Открой `life-planning-coach-vX.Y.Z-grok.md`, скопируй всё содержимое (Ctrl+A → Ctrl+C)
2. Вставь в первое сообщение:

```
Ниже — инструкции для тебя как AI-ассистента. Следуй им во всём разговоре.

---
[вставь сюда всё содержимое SKILL.md]
---

Начни с Emotional Landing. Пользователь говорит: "Я чувствую, что жизнь проходит мимо, помоги разобраться"
```

### Шаг 3. Начать диалог
Grok прочитает инструкции и начнёт с Emotional Landing Protocol.

**💡 Совет:** С включённой Persistent Memory контекст сохраняется между сессиями даже при Direct Prompt.

---

## Способ 2. Grok Projects (рекомендуемый)

**Лучше для:** регулярного использования, workspace-specific контекст, постоянный доступ к файлам.

### Шаг 1. Создать Project
1. В Grok нажми **New Project** (или «+» рядом с Projects)
2. Название: **Life Planning Coach**, описание: «Коучинг по жизненному планированию»

### Шаг 2. Добавить инструкции
1. Открой `life-planning-coach-vX.Y.Z-grok.md`, скопируй содержимое
2. В Project → **Context** (или «Instructions») вставь текст скилла → сохрани

### Шаг 3. Загрузить reference-файлы
В Project → **Files** нажми **Upload**, загрузи файлы из папки `references/`.

### Шаг 4. Активировать
Открывай Project **Life Planning Coach** — скилл применяется автоматически.

---

## Способ 3. Grok Skills (реюзабельный скилл)

**Лучше для:** постоянный доступ к скиллу через slash command во всех сессиях.

> ⚠️ **Статус:** Grok Skills — forthcoming feature. Leaked UI mockups (TestingCatalog, апр 2026) подтверждают поля Name / Description / Instruction и импорт `.md`, но feature flag пока False. Может быть недоступен для всех пользователей.

### Шаг 1. Создать Project
1. В Grok нажми **New Project** → название: **Life Planning Coach**
2. Включи connectors: **Google Calendar** и **Google Drive**

### Шаг 2. Создать Skill
1. В Project нажми **Create Skill** (или набери `/skill-create`)
2. Название: **life-planning-coach**
3. В поле **Instruction** вставь содержимое `life-planning-coach-vX.Y.Z-grok.md`
4. Сохрани — Grok предложит сохранить скилл

### Шаг 3. Активация
В любом чате набери slash command:
```
/life-planning-coach
```

**💡 Совет:** Если Skills UI недоступен — используй **Способ 2 (Grok Projects)**. Тот же результат через Project context.

---

## Способ 4. API + Collections (продвинутый)

**Лучше для:** автоматизации, persistent document storage через Collections API.

### Шаг 1. API-ключ
[console.x.ai](https://console.x.ai) → создай API Key с доступом к Grok 4.3 + tool use.

### Шаг 2. Создать Collection
Collections — persistent хранилище документов между сессиями:

```python
import openai
client = openai.OpenAI(api_key="YOUR_KEY", base_url="https://api.x.ai/v1")
with open("life-planning-coach-v0.9.2-grok.md") as f:
    skill = f.read()
client.chat.completions.create(
    model="grok-4.3",
    messages=[{"role": "user", "content": f"""
Создай Collection "Life Planning Coach" и добавь документ "SKILL.md":
```\n{skill}\n```
"""}],
)
```

### Шаг 3. Использовать Collection
```
Загрузи документ "SKILL.md" из Collection "Life Planning Coach".
Начни с Emotional Landing.
```

---

## Как включить connectors

Grok поддерживает встроенные connectors для внешних сервисов:

### Google Calendar
[grok.com/connectors](https://grok.com/connectors) → **New Connector** → **Google Calendar** → OAuth (разреши create/update/delete/search/RSVP).

### Google Drive
Там же → **Google Drive** → OAuth (разреши search/read/write/create/upload).

> **Важно:** Google Drive connector — нативный, НЕ MCP. Работает напрямую через OAuth.

### Другие connectors
Outlook Calendar, OneDrive, SharePoint, Salesforce, Teams — тот же OAuth-флоу.

---

## Настройка Persistent Memory

Grok запоминает контекст между сессиями через Memory.

### Включить
Settings → Data Controls → Memory → **ON**

### Управление
- **Просмотр:** Settings → Data Controls → Memory → «View Memories»
- **Удалить одно:** 🗑️ рядом с воспоминанием
- **Удалить все:** Settings → Data Controls → Memory → «Clear All Memories»

### Приватный режим (Private Chat)
Иконка 👻 в чате — для чувствительных разговоров. В этом режиме Grok **не сохраняет** воспоминания.

---

## Кросс-платформенная непрерывность

Переход с другого AI-ассистента на Grok? Всё остаётся на месте.

Grok имеет нативный Google Drive connector — все файлы wiki доступны без пересоздания. Вставь в первое сообщение:

```
Найди в моём Google Drive папку "Life Planning Coach Wiki".
Прочитай файлы Index.md и Hot_Cache.md.
Продолжи с того места, где мы остановились.
```

Grok найдёт папку, прочитает состояние и продолжит диагностику.

---

## Сравнение способов

| Способ | Сложность | Persistent | Calendar | Drive | Лучше для |
|--------|-----------|------------|----------|-------|-----------|
| Direct Prompt | ⭐ Лёгкий | ⚠️ Только с Memory ON | ✅ Native | ✅ Native | Тестирование, быстрый старт |
| Grok Projects | ⭐⭐ Средний | ✅ Да (Project context) | ✅ Native | ✅ Native | Регулярное использование |
| Grok Skills | ⭐⭐ Средний | ✅ Да (slash command) | ✅ Native | ✅ Native | Reusable во всех сессиях |
| API + Collections | ⭐⭐⭐ Сложный | ✅ Да (Collections API) | ✅ Native | ✅ Native | Разработчики, автоматизация |

---

## Первый запуск (общий флоу)

### 1. Триггер-фраза
- «Я чувствую, что жизнь проходит мимо, помоги разобраться»
- «Не знаю, куда двигаться»
- «Хочу поставить цели на год»
- «Сделай Wheel of Life»

### 2. Emotional Landing (5-10 мин)
Grok начнёт с валидации:
> «Это знакомо многим — чувство, что время уходит, а ты не туда движешься...»

### 3. Style Calibration (1 мин, опционально)
Два вопроса о предпочтительном стиле коммуникации.

### 4. Диагностика
- **Track A** (20-30 мин): Wheel of Life + Values + одно действие
- **Track B** (65-105 мин, 2-4 сессии): полная диагностика

---

## Особенности Grok 4.3 (важно понимать)

### Persistent Memory
Grok **запоминает** контекст между сессиями через Memory (Settings → Data Controls → Memory).
- Включи Memory для автоматического сохранения контекста
- Используй Private Chat (👻), когда не хочешь запоминать
- Для полного контроля сохраняй `conversation_state.json` в sandbox

### Native Calendar Connector
Grok **может** создавать, обновлять и удалять события в Google Calendar через OAuth.
- Подключи Calendar в grok.com/connectors
- Скилл создаст события автоматически: «Понедельник 19:00 — Weekly Review»
- Также доступен Outlook Calendar

### Dashboard
Grok генерирует HTML-дашборд через sandbox:
1. Скажи: «Покажи дашборд»
2. Grok создаст HTML через `write_file`
3. Используй `render_file` для отображения в чате
4. **Скачай файл** — sandbox очищается при закрытии сессии

### Tool Limit
Максимум **10 tool calls** за один turn. Grok автоматически batch'ит операции.

---

## Troubleshooting

| Проблема | Решение |
|----------|---------|
| «Я не вижу скилл в списке» | Grok 4.3 не имеет Skill Store. Используй Direct Prompt, Projects или Skills Directory. |
| «Данные пропали после закрытия вкладки» | Включи Persistent Memory (Settings → Data Controls → Memory). Дополнительно сохраняй `conversation_state.json`. |
| «Grok не начинает с Emotional Landing» | Убедись, что загружен именно Grok-вариант (`-grok.md`), не универсальный. |
| «Не могу подключить Google Calendar» | Перейди на grok.com/connectors → New Connector → Google Calendar → пройди OAuth. |
| «Дашборд не отображается» | Попроси Grok использовать `render_file` component для отображения HTML из sandbox. |
| «Слишком длинный скилл, не влезает» | Разбей на части: сначала Phase 0-2, потом Phase 3-5. Или используй Grok Projects. |

---

## Quick Start (минимальный путь)

```
1. Скачай life-planning-coach-v0.9.2-grok.md
2. Открой grok.com → выбери Grok 4.3
3. Включи Persistent Memory: Settings → Data Controls → Memory → ON
4. Подключи Google Drive: grok.com/connectors → Google Drive → OAuth
5. Скопируй содержимое файла скилла
6. Вставь в чат: "Следуй этим инструкциям. Начни с Emotional Landing."
7. Напиши: "Я чувствую, что жизнь проходит мимо"
```

---

*Документация основана на Grok 4.3 leaked system prompt, sandbox capabilities и native connectors.*
*Обновлено: 2026-05-18*
