# Руководство пользователя — Kimi Code CLI (Terminal Agent)

> **Платформа:** Kimi Code CLI (терминальный AI-агент)
> **Формат:** Directory-based skill (`SKILL.md` + `references/`)
> **Размер файла:** ~90 KB (SKILL.md 28 KB + refs 62 KB)
> **Refs:** Загружаются через инструмент `read_file` (directory-based)
> **MCP:** Поддерживается (ручная конфигурация JSON)
> **Нет `memory_space`** — для персистентности используется файловая система

---

## 1. Системные требования

- Установленный **Kimi Code CLI** (`pip install kimi-cli` или через package manager)
- Терминал с поддержкой Unicode
- Python 3.10+
- Node.js (для MCP-серверов через npx)

### 1.1 Установка Kimi Code CLI

```bash
pip install kimi-cli
# Или через uv:
uv tool install kimi-cli
```

Проверка установки:
```bash
kimi --version
```

---

## 2. Установка

### 2.1 Создание директории скилла

```bash
mkdir -p ~/.kimi/skills/life-planning-coach
cd ~/.kimi/skills/life-planning-coach
```

### 2.2 Загрузка файлов

Из GitHub Releases:
```bash
# Загрузите и распакуйте директорию kimi-cli
wget https://github.com/azagreev/life-planning-coach/releases/download/vX.Y.Z/life-planning-coach-vX.Y.Z-kimi-cli.zip
unzip life-planning-coach-vX.Y.Z-kimi-cli.zip
# Или скопируйте из локальной сборки:
cp -r /path/to/platforms/kimi-cli/* ~/.kimi/skills/life-planning-coach/
```

Ожидаемая структура:
```
~/.kimi/skills/life-planning-coach/
├── SKILL.md
├── references/
│   ├── diagnostic_methods.md
│   ├── communication_style.md
│   ├── authentic_goal_filter.md
│   ├── goal_architecture.md
│   ├── weekly_review.md
│   ├── habit_loop.md
│   ├── emotion_regulation.md
│   └── dashboard_guide.md
└── life-planning-dashboard.html
```

### 2.3 Проверка установки

```bash
kimi skill list
# Должен отображаться: life-planning-coach
```

---

## 3. Конфигурация MCP (ручной JSON)

> ⚠️ **Предупреждение:** Настройка MCP в Kimi Code CLI — процесс "очень недружелюбный": требуется ручное редактирование JSON-файлов. В отличие от однокликовой установки в Claude, здесь необходимо напрямую редактировать конфигурационные файлы.

### 3.1 Определение директории конфигурации

```bash
ls ~/.config/kimi/mcp/  # или ~/.kimi/mcp/
```

### 3.2 Google Calendar MCP

Создайте файл `~/.config/kimi/mcp/google-calendar.json`:

```json
{
  "name": "google-calendar",
  "transport": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-gcalendar"]
  },
  "env": {
    "GOOGLE_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "your-client-secret"
  }
}
```

### 3.3 Google Drive MCP

Создайте файл `~/.config/kimi/mcp/google-drive.json`:

```json
{
  "name": "google-drive",
  "transport": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-gdrive"]
  },
  "env": {
    "GOOGLE_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "your-client-secret"
  }
}
```

### 3.4 Перезапуск Kimi CLI

```bash
kimi mcp reload
# Или перезапустите сессию kimi CLI
```

### 3.5 Проверка MCP-инструментов

```bash
kimi mcp list
# Должны отображаться: google-calendar, google-drive
```

### 3.6 Получение Google OAuth Credentials

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте проект → Включите **Google Calendar API** и **Google Drive API**
3. Перейдите в **Credentials** → **Create OAuth 2.0 Client ID** (Desktop app)
4. Скопируйте `Client ID` и `Client Secret` в JSON-конфиги выше
5. При первом использовании Kimi CLI запросит OAuth-авторизацию

---

## 4. Использование

### 4.1 Запуск сессии

```bash
kimi skill use life-planning-coach
```

Или в существующей сессии Kimi CLI:
```
@life-planning-coach проведи диагностику
```

### 4.2 Команды на естественном языке

| Что вы вводите | Что происходит |
|---------------|----------------|
| `Проведи диагностику` | Stage 1 — полная диагностика |
| `Построй цель на 6 месяцев` | Stage 2 — архитектура целей |
| `Как прошла неделя?` | Stage 3 — еженедельное ревью |
| `Сохрани в Drive` | Сохраняет в Google Drive (если MCP настроен) |
| `Добавь в календарь` | Создаёт событие в календаре (если MCP настроен) |
| `Покажи дашборд` | Открывает `life-planning-dashboard.html` |

### 4.3 Персистентность через файловую систему

В отличие от `memory_space` в Kimi OK Computer, Kimi CLI использует файловую систему:

```bash
# Коуч может создавать локальные файлы:
~/.kimi/skills/life-planning-coach/sessions/
├── session-2024-01-15.md
├── wheel-of-life-latest.json
└── goals-active.md
```

---

## 5. Ключевые отличия от Kimi OK Computer

| Фича | Code CLI | OK Computer |
|------|----------|-------------|
| Refs | `read_file` (директория) | Inlined (один файл) |
| MCP | ✅ Поддерживается (ручная конфигурация) | ❌ Не поддерживается |
| Память | Файловая система | `memory_space` |
| Календарь | Google Calendar MCP | Только текстовый экспорт |
| Drive | Google Drive MCP | ❌ Нет интеграции |
| Лимит шагов | Высокий (терминал) | ~10 шагов (Base Chat) |
| Установка | Терминал + JSON | Web UI (просто) |
| Окружение | Локальная файловая система | Только облако |

---

## 6. Устранение неполадок (Troubleshooting)

| Проблема | Решение |
|----------|---------|
| "Skill not found" | Проверьте путь `~/.kimi/skills/`; выполните `kimi skill list` |
| `read_file` fails | Убедитесь, что директория `references/` существует рядом с `SKILL.md` |
| MCP не загружается | Проверьте синтаксис JSON; убедитесь, что `npx` установлен; проверьте env vars |
| Ошибки OAuth | Пересоздайте credentials в Google Cloud Console |
| "Command not found" | Убедитесь, что `kimi` есть в PATH: `which kimi` |
| Вывод обрезается | У Kimi CLI высокие лимиты токенов; используйте `kimi --max-tokens` при необходимости |

---

## 7. Ограничения

- **Ручная настройка MCP** — нет GUI для конфигурации
- **Нет `memory_space`** — персистентность только через файловую систему
- **Требуется локальная установка** — не облачное решение, как OK Computer
- **Context window:** Зависит от модели (K2.6 ~200K tokens)
- **Terminal UI** — нет rich HTML rendering (дашборд открывается в браузере)

---

## 8. Приватность и обработка данных

- Коучинговые данные хранятся локально на вашей машине
- Доступ к Google Calendar/Drive осуществляется через ваши собственные OAuth credentials
- Никакие данные не отправляются в Moonshot AI, кроме содержимого разговора
- Полный контроль над MCP-серверами и их разрешениями
- Полное уведомление о приватности см. в `SKILL.md` → `## Privacy & Data Handling`
