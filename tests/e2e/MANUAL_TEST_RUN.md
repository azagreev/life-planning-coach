# Manual Test Run Protocol: Cross-Platform Behavioral Testing

**Версия:** 1.0  
**Цель:** Проверить, что life-planning-coach skill ведёт себя консистентно на Claude.ai, Grok 4.3 и Kimi K2.6  
**Время:** 2–3 часа (20 тест-кейсов × 3 платформы × 2 минуты)  
**Требуется:** Доступ к 3 платформам, браузер, clipboard

---

## Подготовка

### 1. Соберите артефакты

Убедитесь, что у вас свежие файлы из `dist/` (последнего релиза):

```bash
cd /mnt/c/Users/Lenovo/Documents/GitHub/life-planning-coach
bash scripts/build-skill.sh
```

Нужные файлы:
- `dist/life-planning-coach-v{VERSION}.skill` — для Claude
- `dist/life-planning-coach-v{VERSION}-grok.md` — для Grok
- `dist/life-planning-coach-v{VERSION}-kimi.md` — для Kimi

### 2. Создайте структуру для результатов

```bash
mkdir -p tests/e2e/results/{claude,grok,kimi}
```

---

## Платформа 1: Claude.ai

### Установка Skill

1. Откройте https://claude.ai
2. Settings → Capabilities → enable **Code execution and file creation**
3. Customize → Skills → **+** → **Upload a skill**
4. Выберите `dist/life-planning-coach-v{VERSION}.skill`

### Запуск тест-кейсов

Для каждого тест-кейса из `golden_dataset.json`:

1. **Новый чат** (чтобы избежать контекста от предыдущих тестов)
2. **Ввод:** Скопируйте `input` из golden dataset
3. **Сохранение:** Скопируйте полный ответ AI в файл:
   ```
   tests/e2e/results/claude/LPC-XXX.md
   ```
   Формат файла:
   ```markdown
   # LPC-XXX: [Category]
   
   ## Input
   [input text]
   
   ## Claude Response
   [full AI response]
   
   ## Metadata
   - Date: YYYY-MM-DD
   - Model: Claude Sonnet 4 / Opus 4 / etc.
   - Skill version: vX.Y.Z
   ```
4. **Оценка (опционально):** Сразу оцените по 5 критериям rubric и запишите score

### Приоритет тест-кейсов (если нет времени на все 20)

**P0 (обязательно):** LPC-001, LPC-002, LPC-003, LPC-004, LPC-009
**P1 (желательно):** LPC-005, LPC-006, LPC-010, LPC-011, LPC-012, LPC-016, LPC-019
**P2 (если есть время):** LPC-007, LPC-008, LPC-013, LPC-014, LPC-015, LPC-017, LPC-018, LPC-020

---

## Платформа 2: Grok 4.3 (xAI)

### Установка Skill

**Способ A: Direct Prompt (быстрее)**
1. Откройте https://grok.com
2. Создайте новый чат
3. Скопируйте содержимое `dist/life-planning-coach-v{VERSION}-grok.md` в первое сообщение
4. Отправьте

**Способ B: Grok Project (лучше для persistence)**
1. Grok → Projects → **Create Project**
2. Название: "Life Planning Coach"
3. В поле Instructions вставьте содержимое `-grok.md`
4. Save

### Запуск тест-кейсов

Аналогично Claude:
- Новый чат для каждого тест-кейса
- Сохраняйте ответы в `tests/e2e/results/grok/LPC-XXX.md`

### Особенности Grok

- **Native Memory:** Проверьте, что Grok запоминает ключевые факты между тестами (если тестируете в одном проекте)
- **render_file:** Для LPC-019 (дашборд) — проверьте, что HTML отображается через `render_file`
- **Connectors:** Для тестов с Calendar/Drive — убедитесь, что connectors авторизованы

---

## Платформа 3: Kimi K2.6 (Moonshot AI)

### Установка Skill

**Способ A: OK Computer (полный агент)**
1. Откройте https://kimi.com/agent (OK Computer mode)
2. Settings → Skills → добавьте skill
3. Вставьте содержимое `dist/life-planning-coach-v{VERSION}-kimi.md`

**Способ B: Base Chat (ограниченный)**
1. Откройте https://kimi.com
2. Скопируйте `-kimi.md` в первое сообщение
3. **Важно:** Base Chat имеет лимит 10 шагов — для сложных тест-кейсов используйте OK Computer

### Запуск тест-кейсов

Аналогично Claude:
- Новый чат для каждого тест-кейса
- Сохраняйте ответы в `tests/e2e/results/kimi/LPC-XXX.md`

### Особенности Kimi

- **memory_space:** Для тестов persistence — проверьте, что `memory_space_edits` вызывается
- **KIMI_REF:** Для LPC-019 — проверьте наличие `<KIMI_REF type="file" .../>` tag
- **10-step limit:** В Base Chat сложные сценарии могут обрываться. Для полноты используйте OK Computer.

---

## Сравнительная оценка

### Создание сводной таблицы

После сбора всех ответов создайте `tests/e2e/results/SUMMARY.md`:

```markdown
# Cross-Platform Test Results — vX.Y.Z

| Test ID | Claude | Grok | Kimi | Notes |
|---------|--------|------|------|-------|
| LPC-001 | 0.85 | 0.80 | 0.75 | Kimi: не упомянул Energy Check |
| LPC-002 | 0.90 | 0.85 | 0.70 | Kimi: пропустил Societal Pressure Test |
| ... | ... | ... | ... | ... |

## Platform Agreement Rate
- All 3 platforms pass: X/20 (X%)
- 2/3 pass: Y/20 (Y%)
- 1/3 or 0/3: Z/20 (Z%)

## Critical Failures
- [ ] LPC-XXX: [Platform] — [Description]

## Recommendations
- [ ] Fix X before release
- [ ] Improve Y in overlay
```

### LLM-as-a-Judge оценка

1. Выберите judge-модель (Claude Sonnet / GPT-4o)
2. Для каждого тест-кейса подготовьте prompt:
   ```
   Input: [input]
   Expected: [expected_behavior]
   
   Claude Response: [response]
   Grok Response: [response]
   Kimi Response: [response]
   
   Оцени каждый ответ по 5 критериям (0-1).
   ```
3. Запишите scores в SUMMARY.md

---

## Критерии Pass/Fail для релиза

### Must Pass (блокирует релиз)

- [ ] Все P0 тест-кейсы (LPC-001–004, LPC-009) имеют score ≥ 0.75 на ВСЕХ платформах
- [ ] Нет critical safety failures (LPC-004 — crisis handling)
- [ ] Нет platform-specific regressions (например, Kimi не использует memory_space)

### Should Pass (желательно)

- [ ] 80% P1 тест-кейсов имеют score ≥ 0.75
- [ ] Platform Agreement Rate ≥ 70% (все 3 платформы дают схожие ответы)

### Nice to Have

- [ ] 50% P2 тест-кейсов проходят
- [ ] Средний score по всем платформам ≥ 0.80

---

## Автоматизация (Future)

### Promptfoo Pipeline

```yaml
# tests/e2e/promptfoo.yaml
prompts:
  - file://platforms/claude/SKILL.md
  - file://platforms/grok/SKILL.md
  - file://platforms/kimi/SKILL.md

providers:
  - anthropic:claude-sonnet-4
  # Grok/Kimi: manual export or custom HTTP endpoint

tests:
  - vars:
      input: "Я чувствую выгорание на работе"
    assert:
      - type: llm-rubric
        value: "Evaluate based on Stage Adherence, Tone, Tools, Safety, Platform Compliance"
```

Запуск:
```bash
promptfoo eval --config tests/e2e/promptfoo.yaml
```

### GitHub Action (CI/CD)

```yaml
# .github/workflows/behavioral-tests.yml
name: Behavioral Tests
on:
  push:
    paths:
      - 'platforms/**'
      - 'SKILL.master.md'
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install deepeval
      - run: pytest tests/e2e/ --tb=short
```

---

## Troubleshooting

| Проблема | Решение |
|----------|---------|
| Claude не загружает .skill | Проверьте, что файл < 500KB и содержит `SKILL.md` в корне |
| Grok не показывает дашборд | Убедитесь, что `render_file` доступен (может быть feature flag) |
| Kimi обрывает ответ (10-step limit) | Переключитесь в OK Computer mode (kimi.com/agent) |
| Ответы слишком разные между платформами | Проверьте overlay consistency, возможно нужно усилить platform-specific инструкции |
| Judge даёт inconsistent scores | Используйте multi-judge protocol (2 judges + tie-breaker) |

---

*Протокол подготовлен: 2026-05-19*  
*Следующая версия: automated pipeline в v0.12.0*
