# Анализ PRD v7.0 Reward Audit: что берём в skill, что откладываем

> **Дата анализа:** 2026-05-17
> **Аналитик:** Kimi Code CLI (на основе архитектуры life-planning-coach)
> **Исходный документ:** `references/research/prd_reward_audit.md` (PRD v7.0)
> **Вывод:** 80% PRD — standalone app scope. 20% — концентрированная killer-фича для skill.

---

## 1. Executive Summary → Резюме анализа

| Элемент PRD | В skill? | Решение |
|-------------|----------|---------|
| «Встроенный модуль» с логированием | ❌ Нет | Это standalone app, не conversational AI |
| Dopamine Load Score (0–10) | ❌ Нет | Требует daily tracking + persistence |
| Корреляция с completion rate | ⚠️ Частично | Только qualitative (в разговоре), не quant |
| Научный backing (весь раздел 4) | ✅ Да | Идёт в `references/reward_audit.md` как educational content |
| **Grayscale рекомендация** | ✅ **Killer** | Главный takeaway. Zero tracking, one-time action, strong evidence |
| Advanced Integrations (7.6) | ❌ Нет | Для standalone app v2+ |
| Custom MCP-сервер | ❌ Нет | Архитектура отдельного продукта |

**Итоговый scope для skill:** Grayscale Guide + conversational check-in + science backing. ~60–80 строк.

---

## 2. Problem Statement → Что берём

| Элемент | В skill? | Почему / Как использовать |
|---------|----------|---------------------------|
| «Сахар → дофамин → снижение мотивации» | ✅ | Educational framing в ответе скилла |
| «Соцсети → variable reward» | ✅ | Объяснение, почему grayscale работает |
| «Толерантность, effort-based decision making» | ✅ | Наука для reference-файла |
| **Боль пользователя** (цитата) | ✅ | Используем как trigger pattern для активации фичи |
| Research citations (Rada, Avena, Lembke, Kushlev) | ✅ | В `references/reward_audit.md` + упоминание в conversation |

**Вывод:** Весь Problem Statement — полезен. Перерабатываем в conversational framing.

---

## 3. Goals & Success Metrics → Что берём

| Метрика | В skill? | Комментарий |
|---------|----------|-------------|
| Completion rate +15–25% | ❌ Нет | Требует A/B тест, tracking, cohort analysis. Невозможно в skill. |
| Retention 30+ дней +20% | ❌ Нет | Product metric, не skill metric. |
| Logging ≥4 раза в неделю | ❌ Нет | Пользователь не «логирует» в skill — он разговаривает. |
| Dopamine Load Score | ❌ Нет | Требует daily input + calculation engine. |
| **Время до первого инсайта < 7 дней** | ✅ Да | Достигается за 1 сессию (grayscale рекомендация). |
| «Пользователь понимает связь» | ✅ Да | Качественная цель, достижима в conversation. |

**Вывод:** Все quant-метрики PRD — для standalone app. Для skill оставляем только качественные цели.

---

## 4. Research & Scientific Backing → Полностью берём

Весь раздел 4 (4.1–4.4) — **высококачественный контент**, который отличает продукт от конкурентов.

### 4.1 Сахар + дофамин (Rada, Avena, Jacques, UMich)
- ✅ **Берём всё.** Используем для объяснения «почему сахар мешает целям».
- 📎 **Конкретная цитата для conversation:** «Исследование Rada (2005) показало: повторяющийся сахар выбрасывает дофамин до 130% baseline. Мозг привыкает — и «обычная» мотивация перестаёт работать.»

### 4.2 Соцсети + экраны (Lembke, Kushlev, SDSU)
- ✅ **Берём всё.** Основа для grayscale рекомендации.
- 📎 **Конкретная цитата:** «Lembke из Stanford называет соцсети 'современным наркотиком' через variable rewards. Kushlev (2025): даже небольшой digital detox улучшает внимание.»

### 4.3 Dopamine detox backlash (The Scientist, Northwestern)
- ✅ **Берём.** Важно для фрейминга «Reward Management» вместо «detox».
- 📎 **Конкретная цитата:** «Сам термин 'dopamine detox' критикуют учёные (Northwestern, 2025) за oversimplification. Мы используем 'Reward Audit' — это про осознанность, не про запреты.»

### 4.4 Grayscale mode (Holte, Wickord, Myers, NYT) — ⭐ ГЛАВНОЕ
- ✅ **Берём ВСЁ.** Это ядро фичи.
- 📎 **Конкретные цифры для conversation:**
  - Holte (2021): –37.9 мин/день screen time
  - Wickord (2023): –21.76 мин/день (репликация)
  - Myers (2022): уменьшение «allure» телефона + лучше сон
  - NYT (2025): –40% за 2 недели
- 📎 **Механизм для объяснения:** «Цвет в apps — визуальный допаминовый триггер. Grayscale убирает его → scrolling становится скучным.»

---

## 5. Competitive Landscape → Частично берём

| Элемент | В skill? | Комментарий |
|---------|----------|-------------|
| Elqi, Opal, BePresent, Liven | ✅ | Используем для positioning: «Мы не блокируем apps — мы объясняем механизм» |
| Habitica, Habitify и т.д. | ❌ Не нужно | Не конкуренты для coaching skill |
| **Gap: «никто не связывает cheap dopamine с completion rate»** | ✅ | Уникальное позиционирование. Но в skill — qualitative, не quantitative correlation. |

**Вывод:** Конкурентный анализ полезен для понимания positioning, но не идёт напрямую в skill.

---

## 6. User Personas → Берём

| Persona | В skill? | Как использовать |
|---------|----------|------------------|
| Андрей, 32, PM, 3–4 часа в соцсетях | ✅ | Trigger pattern: жалобы на прокрастинацию + high screen time |
| Фаундер, 28–40, высокий стресс | ✅ | Trigger pattern: «нет мотивации», «выгорание» |

**Вывод:** Personas помогают определить trigger phrases для активации фичи.

---

## 7. Functional Requirements → Разбор по пунктам

### 7.1 Логирование (MVP) → ❌ НЕ берём
- Экран «Сегодняшний Dopamine Load» → ❌ Нет экранов в skill
- 5 категории + слайдеры → ❌ Нет UI элементов
- Быстрые пресеты → ❌ Нет
- Screen Time API → ❌ Нет доступа

**Alternative для skill:** Conversational question: «Что из этого было чаще обычного на этой неделе?» + список категорий.

### 7.2 Расчёт и визуализация → ❌ НЕ берём
- Dopamine Load Score → ❌ Нет calculation engine
- Графики (Scatter, Bar, Trend) → ❌ Нет рендеринга
- Weekly report → ⚠️ Только conversational (без визуализации)

### 7.3 Insights & Рекомендации → ⚠️ Частично
- «Снижение скролла на 30 мин/день → +15% completion» → ❌ Нет персональных данных для такой корреляции
- **Предложение low-dopamine режима** → ✅ Можно предложить grayscale
- **Список effortful активностей** → ✅ Можно дать как recommendation

### 7.4 Интеграция с core → ⚠️ Частично
- Weekly planning: блок «Dopamine Budget» → ❌ Нет UI блоков
- Badge «Low Dopamine Week» → ❌ Нет badge system
- **В Weekly Review спросить про distractions** → ✅ Conversational integration

### 7.5 Геймификация → ❌ НЕ берём
- Streaks, очки, уровни → Всё требует persistence

### 7.6 Advanced Integrations → ❌ НЕ берём (но сохраняем для будущего)

| Интеграция | В skill? | Комментарий |
|------------|----------|-------------|
| **A. Grayscale** | ✅ **Да, но по-другому** | Не «трекинг включения», а **one-time recommendation** с инструкцией |
| B. Digital Wellbeing / Screen Time | ❌ Нет | Требует доступа к системе |
| C. Freestyle Libre | ❌ Нет | Медицинские данные, API, consent — standalone app |
| D. Claude Health via MCP | ❌ Нет | Это про Claude mobile app, не про skill. Skill не имеет доступа к MCP. |
| E. Custom MCP-сервер | ❌ Нет | Архитектура отдельного продукта |

**⚠️ Важное уточнение:** MCP Health интеграции (раздел 7.6D) работают в **Claude mobile app** (iOS/Android), но **НЕ в skill**. Skill — это prompt + references, у него нет доступа к внешним API, HealthKit или MCP. Это критическое ограничение, которое PRD игнорирует.

### 7.7 Приватность → ⚠️ Не применимо
- Локальное хранение → В skill данные не хранятся (только в Claude Memory или Drive wiki, opt-in)
- GDPR-like → Не применимо к conversational skill

---

## 8–10. NFR, Success Metrics, Roadmap → ❌ НЕ берём

Всё это — standalone app product management. Для skill неактуально.

---

## 11. Risks & Mitigations → Частично берём

| Риск | В skill? | Митигация для skill |
|------|----------|---------------------|
| Guilt-trip | ✅ | Opt-in + framing «Reward Management» + positive tone |
| Dopamine detox backlash | ✅ | Термин «Reward Audit» + научные ссылки |
| Низкий adoption | ❌ Не применимо | В skill нет «adoption» — есть conversational trigger |
| Приватность | ⚠️ Не критично | Skill не собирает данные без согласия |

---

## 12. Open Questions → Ответы для skill

| Вопрос | Ответ для skill |
|--------|-----------------|
| Порно / азарт? | ❌ Не спрашивать. Только если пользователь сам упомянул. |
| Вес сахара vs скролла? | ❌ Не считать. Нет scoring. |
| MyFitnessPal? | ❌ Нет интеграций. |
| Геймификация? | ❌ Нет. |

---

## Appendix A (ссылки) → Полностью берём

Все 11 источников — в `references/reward_audit.md`.

## Appendix B (Grayscale research) → Полностью берём

Весь мини-отчёт — в `references/reward_audit.md` как основа killer feature.

---

## Итог: Что идёт в `references/reward_audit.md`

```
1. When to use (triggers)
2. Opt-in script
3. Grayscale Experiment:
   - Why it works (mechanism)
   - Data (Holte –37.9 min, Wickord –21.76 min, Myers allure, NYT –40%)
   - Instructions (iOS + Android)
   - Framing: «Make your phone boring»
4. Optional conversational check-in:
   - 4 categories (digital, food, shopping, other)
   - Qualitative connection to goals
5. Safety guardrails (opt-in, no guilt, not for crisis)
6. Science backing (Rada, Avena, Lembke, Kushlev + grayscale studies)
```

**Оценка:** ~70–90 строк. Вписывается в лимит ≤120.

---

## Что откладываем в архив (для standalone app v2+)

| Идея | Почему отложена | Когда вернуть |
|------|-----------------|---------------|
| Dopamine Load Score | Требует daily tracking + calculation engine | Standalone app |
| Screen Time API | Требует native app permissions | Standalone app |
| Freestyle Libre | Требует medical API + consent | Standalone app v2+ |
| Claude Health MCP | Только для Claude mobile app, не skill | Если продукт вырастет в standalone |
| Custom MCP-сервер | Архитектура отдельного продукта | v2.5+ standalone |
| Геймификация, streaks | Требует persistence + game design | Standalone app |
| Корреляционные графики | Требует data visualization engine | Standalone app |
| Digital Wellbeing integration | Требует OS-level access | Standalone app |

---

*Анализ завершён. Рекомендация: реализовать сфокусированный Grayscale Guide в skill, всё остальное — в архив для potential standalone product.*
