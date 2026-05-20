# R&D Synthesis: Wearable Energy Integration + Body Doubling

> **Статус:** Research / Future Architecture (v0.14+)
> **Источники:** `body_doubling_wearable_methodology.md` (3056 lines), `whoop_trainingpeaks_pattern.md` (1647 lines)
> **Дата синтеза:** 2026-05-20
> **Теги:** `[SKILL-READY]` — можно использовать в SKILL.md сейчас; `[APP-ONLY]` — требует mobile app / Telegram-бот

---

## 1. Пробел рынка (Market Gap)

**[RESEARCH]** Ни одна из 15+ проанализированных платформ не реализует полный цикл:
`multi-wearable recovery data → automatic calendar rescheduling → two-way sync → AI-powered explanation → cognitive (not just physical) recovery optimization`

| Платформа | Recovery Input | Adaptive Output | Calendar | AI Coach |
|-----------|---------------|-----------------|----------|----------|
| TrainingPeaks + WHOOP | HRV, RHR, Sleep | ❌ Display only | Metric Card | ❌ |
| Garmin → TrainingPeaks | Body Battery, HRV | ⚠️ Coach decides | ✅ Bidirectional | ❌ |
| SensAI | HRV, Sleep via HealthKit | ✅ AI workout | ❌ | ✅ |
| LifeStack.ai | Multi-wearable | ✅ Energy scheduling | ❌ No 2-way sync | ⚠️ |
| Focuzed.io | Generic wearable | ✅ Circadian scheduling | ✅ Google Calendar | ⚠️ |
| **life-planning-coach (target)** | Multi-source + self-report | ✅ Recovery-aware tasks | ✅ MCP 2-way | ✅ Claude |

**Конкурентные преимущества проекта:**
1. AI coach объясняет recovery data в контексте задач
2. MCP Calendar two-way integration (create/update/delete)
3. Body Doubling с recovery optimization
4. WOOP/MCII preemptive adaptation
5. Cognitive recovery (не только физическое)

---

## 2. 4-Layer Architecture

**[SKILL-READY]** Ментальная модель, применима к skill-формату:

```
┌─────────────────────────────────────────┐
│  LAYER 4: Adaptive Planning             │
│  Decision engine, optimal source sel.   │
│  [APP-ONLY]: Auto-rescheduling via MCP  │
│  [SKILL-READY]: Manual recommendations  │
└─────────────────────────────────────────┘
         ↑
┌─────────────────────────────────────────┐
│  LAYER 3: ML Correlation                │
│  Body Battery ↔ self-reported energy    │
│  [SKILL-READY]: Conversational patterns │
│  [APP-ONLY]: On-device TensorFlow Lite  │
└─────────────────────────────────────────┘
         ↑
┌─────────────────────────────────────────┐
│  LAYER 2: Wearable Recovery Data        │
│  Garmin Body Battery, Samsung Energy    │
│  [APP-ONLY]: Health Connect, HealthKit  │
│  [SKILL-READY]: User manually reports   │
└─────────────────────────────────────────┘
         ↑
┌─────────────────────────────────────────┐
│  LAYER 1: Self-Reported Energy          │
│  Morning: energy 1-10, focus 1-5        │
│  Post-task: actual energy, focus        │
│  End-of-day: reflection, patterns       │
│  [SKILL-READY]: Всегда доступно         │
└─────────────────────────────────────────┘
```

**State transitions:**
```
[New User] → Layer 1 only (self-report)
   ↓ (connect wearable — [APP-ONLY])
[Layer 1 + 2] → parallel collection
   ↓ (14+ days data)
[Layer 3] → correlation model built
   ↓ (confidence > threshold)
[Layer 4] → fully adaptive
```

---

## 3. Recovery Score Calculator (Composite)

**[SKILL-READY]** Адаптированный для ручного ввода (Layer 1):

| Компонент | Вес | Источник в skill |
|-----------|-----|-----------------|
| Self-reported energy (1-10) | 0.40 | Утренний чек-ин |
| Sleep quality (1-10) | 0.25 | Вопрос "Как спалось?" |
| Mental clarity (1-10) | 0.20 | Вопрос "Насколько ясно мыслишь?" |
| Motivation (1-10) | 0.10 | Вопрос "Есть ли желание делать дела?" |
| Stress level (1-10, инвертировано) | 0.05 | Вопрос "Насколько напряжён?" |

```
Recovery Score = (energy × 0.40 + sleep × 0.25 + clarity × 0.20 +
                  motivation × 0.10 + (10 - stress) × 0.05) × 10
Result: 0-100
```

**[APP-ONLY]** Full wearable version:

```python
WEIGHTS = {
    'hrv_rmssd': 0.35,
    'sleep_score': 0.30,
    'resting_hr': 0.20,
    'strain_yesterday': 0.10,
    'sleep_consistency': 0.05
}
```

**Fallback hierarchy:**
1. Garmin Body Battery (confidence 0.95) — [APP-ONLY]
2. Samsung Energy Score (confidence 0.90) — [APP-ONLY]
3. Calculated Composite from HRV + Sleep + RHR (confidence 0.70-0.90) — [APP-ONLY]
4. **Self-Reported Energy Level (confidence 0.40) — [SKILL-READY], always available**

---

## 4. Privacy Architecture

**[APP-ONLY]** Production-ready framework для mobile app:

| Принцип | Реализация | Стандарт |
|---------|-----------|----------|
| Zero-knowledge | Health-данные не покидают устройство | Privacy-by-design |
| GDPR Art. 9 | Explicit consent, granular, revocable | Art. 9(2)(a) |
| Data minimization | Собираем только нужное для корреляции | Art. 5(1)(c) |
| Purpose limitation | Только energy-productivity correlation | Art. 5(1)(b) |
| Storage limitation | Автоудаление после 365 дней | Art. 5(1)(e) |

**[SKILL-READY]** Для text-based skill:
- Все данные остаются в conversation history
- Нет persistent storage (кроме user-provided context)
- Никаких health-данных не передаётся третьим лицам
- Medical disclaimer обязателен

---

## 5. Critical Risks

| Риск | Severity | Митигация |
|------|----------|-----------|
| Effect size оказался overestimated | 🔴 High | Buffer: d = 0.5 вместо 0.9 |
| Privacy breach / GDPR | 🔴 High | [APP-ONLY]: Zero-knowledge; [SKILL-READY]: No data storage |
| Orthosomnia (anxiety from tracking) | 🟡 Medium | 6 prevention measures; digital detox option |
| API deprecation / sanctions | 🟡 Medium | [APP-ONLY]: Abstraction layer; Huawei Health Kit для РФ |
| High churn post-first session | 🟡 Medium | Soft recovery + Two-Day Rule + shame-free messaging |
| Algorithm distrust | 🟡 Medium | Transparent explanations, manual override always available |
| No wearable API (Xiaomi) | 🟡 Medium | Google Fit bridge → Health Connect |

---

## 6. RICE-оценка (полная версия — [APP-ONLY])

| Приоритет | Фича | RICE | Effort | Статус |
|---|---:|---|---|---|
| 1 | Calendar events с recovery badge | **45.0** | 0.5 PM | [APP-ONLY] |
| 2 | Push-уведомления от wearables | **37.1** | 1.0 PM | [APP-ONLY] |
| 3 | Observer pattern (Health Connect) | **35.1** | 2.0 PM | [APP-ONLY] |
| 4 | Recovery data в календаре | **26.7** | 1.5 PM | [APP-ONLY] |
| 5 | Auto-scheduling по recovery | **5.0** | 3.0 PM | [APP-ONLY] |
| 6 | Adaptive planning по energy | **2.3** | 4.0 PM | [APP-ONLY] |

**[SKILL-READY]** Эквиваленты для skill-формата:
- Recovery badge → Energy indicator в плане дня (text-based)
- Push → Morning check-in prompt в начале сессии
- Auto-scheduling → Recommendations при планировании

---

## 7. Архитектурные паттерны ([APP-ONLY])

### Gateway Pattern
- Decoupling внешних разработчиков от внутренних API
- Field filtering, dedicated team
- Rate limits: 100/min, 10,000/day

### Observer Pattern (Google Health Connect)
- ChangeLogToken API для incremental pull
- `skip own writes` — фильтрация реимпорта
- WorkManager для background sync

### MCP Operations
```yaml
# [APP-ONLY] Полная спецификация в whoop_trainingpeaks_pattern.md §4.7
- health-connect/read
- health-connect/subscribe
- calendar/create (recovery badge)
- calendar/update (focus blocks)
- recovery/calculate
```

---

## 8. Ссылки

- Исходный документ Body Doubling: `references/research/body_doubling_wearable_methodology.md`
- Исходный документ WHOOP Pattern: `references/research/whoop_trainingpeaks_pattern.md`
- Адаптированный Energy Score: `references/research/rnd_energy_score_manual.md`
- Adaptive Zones: `references/research/rnd_adaptive_zones.md`
- Body Doubling Scripts: `references/research/rnd_body_doubling_scripts.md`
- Competitive Matrix: `references/research/rnd_competitive_matrix.md`

---

*Синтез подготовлен: 2026-05-20*
*Статус: Research, не интегрировано в SKILL.md*
