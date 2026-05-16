# Release Notes v0.4.0 — Foundation

**Дата:** 2026-05-16  
**Кодовое имя:** Foundation  
**Статус:** Stable

---

## What's New

### 🧠 Двухуровневая система персистентности

Раньше все данные хранились только в контексте разговора — при закрытии вкладки или длинном диалоге данные терялись. Теперь скилл поддерживает два режима:

**Уровень 1: Zero-Setup (по умолчанию)**
- Работает сразу, без настройки
- Ключевые факты автоматически сохраняются в Claude Memory
- При возвращении — естественный диалог восстановления контекста
- Никаких state-dump'ов, копирования или вставки

**Уровень 2: Google Drive + LLM Wiki (opt-in)**
- Подключение в 1 клик после 1-2 сессий
- Полная структура wiki на вашем Google Drive
- Hot_Cache, Index, Dashboard — всё автоматически
- 60-75% экономия токенов на длинных сессиях
- Данные в вашем облаке, доступны с любого устройства

### 📁 Структура LLM Wiki

При подключении Google Drive скилл автоматически создаёт:

```
Life Planning Coach Wiki/
├── 00_Raw/              ← История всех сессий
├── 01_Wiki/
│   ├── Hot_Cache.md     ← Актуальный контекст (~500 слов)
│   ├── Index.md         ← Оглавление
│   ├── User_Progress/   ← Цели, Wheel of Life, инсайты
│   └── ...
├── 03_Dashboard/
│   └── Progress_Dashboard.md  ← Ваш прогресс (русский, emoji)
└── README.md            ← Что это и зачем
```

### 🔄 Graceful Degradation

Если Google Drive временно недоступен (гео-блокировка, отозван доступ, ошибка) — скилл мягко переключается на Memory-режим без потери данных текущей сессии.

---

## Breaking Changes

**Нет.** Обновление обратно совместимо.

- Существующие пользователи продолжат работу в режиме Memory
- Google Drive — опционально, не требуется для работы
- Методология коучинга не изменилась

---

## Migration Guide

### Для существующих пользователей (v0.2.0 → v0.4.0)

1. Удалите старый скилл: Settings → Capabilities → Skills → Remove
2. Загрузите новый `life-planning-coach.skill`
3. Начните разговор — скилл распознает вас через Memory
4. (Опционально) Подключите Google Drive после 1-2 сессий для автосохранения

**Ваши данные не пропадут** — Claude Memory сохранит ключевые факты.

---

## Known Issues

| Issue | Статус | Workaround |
|-------|--------|------------|
| Google Drive connector требует approval на каждую запись | By design | Batch-запись в конце сессии, ≤5 approval'ов |
| Claude Memory может "забыть" детали при большом объёме | Known limitation | Подключите Google Drive для надёжности |
| Google OAuth может быть недоступен в некоторых регионах | External | Скилл автоматически переключится на Memory |
| Токен-экономия на web Claude ниже, чем на Claude Code | Platform limitation | Всё равно 60-75% экономии vs полный контекст |

---

## Full Changelog

### Added
- Двухуровневая система персистентности (Memory + Drive Wiki)
- Протокол End-of-Session (emotional summary + auto-save)
- Graceful Degradation при отказе Drive
- Шаблоны файлов wiki: Hot_Cache, Index, Dashboard, Raw
- Инструкции для Claude Memory ("запомни это")
- Естественный диалог восстановления контекста (cold start recovery)

### Changed
- Onboarding: теперь zero-setup, без технических требований
- FAQ: обновлены ответы про сохранение данных
- README: добавлена информация о persistence

### Deprecated
- Ручной экспорт state-dump'ов (ещё работает, но не рекомендуется)

### Removed
- Требование настраивать Google Drive перед началом работы

---

## Благодарности

- Andrej Karpathy — за LLM Wiki pattern
- MindStudio — за адаптацию pattern для production
- Сообщество Claude — за фидбек по friction в onboarding'е
