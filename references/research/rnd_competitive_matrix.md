# Competitive Intelligence: Wearable + Productivity Integration

> **Статус:** [RESEARCH] — competitive intelligence, не для прямого применения в skill
> **Источники:** `whoop_trainingpeaks_pattern.md` §2, §6 + `body_doubling_wearable_methodology.md` §1.2, §2.2
> **Дата:** 2026-05-20
> **Платформ проанализировано:** 15+

---

## Summary: Market Gap Confirmed

Ни одна существующая платформа не реализует полный цикл:
`multi-wearable recovery → automatic calendar rescheduling → two-way sync → AI explanation → cognitive recovery optimization`

---

## Platform Comparison Matrix

| Платформа | Recovery Input | Calendar | Adaptive | AI Coach | 2-Way | Cognitive |
|-----------|---------------|----------|----------|----------|-------|-----------|
| **TrainingPeaks + WHOOP** | HRV, RHR, Sleep | ✅ Metric Card | ❌ Display only | ❌ | ❌ | ❌ |
| **Garmin → TrainingPeaks** | Body Battery, HRV, Stress | ✅ Bidirectional | ⚠️ Coach decides | ❌ | ✅ | ❌ |
| **WHOOP Strain Coach** | Internal sensors | ❌ | ✅ Auto strain | ✅ AI | ❌ | ❌ |
| **Oura → LifeStack.ai** | Sleep, HRV, Readiness | ✅ Energy scheduling | ✅ AI tasks | ⚠️ | ❌ | ✅ |
| **Oura → SensAI** | HRV, Sleep via HealthKit | ❌ | ✅ AI workout | ✅ LLM | ❌ | ❌ |
| **Oura → Strava** | Readiness, Sleep | ❌ Score stickers | ❌ | ❌ | ❌ | ❌ |
| **Apple HealthKit** | All health data | ✅ Via WorkoutKit | ❌ | ❌ | ❌ | ❌ |
| **Google Health Connect** | All connected | ❌ No calendar | ❌ | ❌ | ❌ | ❌ |
| **SensAI** | HRV, Sleep, RHR | ❌ Workout app | ✅ Full AI | ✅ LLM | ❌ | ❌ |
| **Vora** | 500+ sources | ✅ 2-way calendar | ✅ AI coach | ✅ | ✅ | ❌ |
| **Focuzed.io** | Generic wearable | ✅ Google Calendar | ✅ Circadian | ⚠️ | ❌ | ✅ |
| **HRV4Training** | Oura, WHOOP manual | ❌ | ⚠️ Readiness rec | ❌ | ❌ | ❌ |
| **Gentler Streak** | HealthKit HRV | ❌ | ✅ Rest-first | ❌ | ❌ | ❌ |
| **Focusmate** | Нет wearable | ❌ | ❌ | ❌ | ❌ | ❌ |
| **FLOWN** | Нет wearable | ❌ | ❌ | ⚠️ Facilitator | ❌ | ✅ |
| **life-planning-coach (target)** | Multi + self-report | ✅ MCP 2-way | ✅ Recovery-aware | ✅ Claude | ✅ | ✅ |

---

## Detailed Analysis

### TrainingPeaks + WHOOP

**Архитектура:** One-way sync через OAuth 2.0 REST API + Gateway pattern

**Что передаётся:**
- ✅ HRV (RMSSD), RHR, Sleep Hours, Times Woken, Deep/REM/Light Sleep
- ❌ Strain Score, Recovery Score, Sleep Performance %, Respiratory Rate, Skin Temp, SpO2

**Что делает TrainingPeaks:**
- Metric Card на календаре (read-only)
- Dashboard Charts (Premium)
- PMC Overlay — HRV на Performance Management Chart (mobile only)

**Чего НЕ делает (критический пробел):**
- ❌ Не автоматически переносит тренировки при низком Recovery
- ❌ Не отправляет рекомендации
- ❌ Не корректирует TSS-цели
- ❌ Не создаёт calendar events
- ❌ Не реализует two-way communication

**UserVoice:** 456+ голосов за Recovery/Strain scores с 2022 года — still pending.

---

### Garmin → TrainingPeaks (Bidirectional)

**Единственная двунаправленная интеграция** среди всех проанализированных.

**Garmin → TrainingPeaks:**
- Activities (GPS, HR, pace, power)
- Body Battery (daily high/low)
- HRV, Stress Level, RHR, Sleep
- Body Composition, Women's Health (май 2025)

**TrainingPeaks → Garmin:**
- Future workouts (structured training)
- Training plans, Calendar events
- Instant sync

**Ограничение:** Adaptive решения принимает coach, не AI. Нет cognitive recovery optimization.

---

### Oura Ecosystem

**Oura → Strava:** Bidirectional sync с "readiness stickers" на активностях. Косметическая интеграция.

**Oura → LifeStack.ai ($4.99/мес):**
- Energy Heatmap на основе Oura
- Smart Time-Blocking с AI templates
- Поддержка: Apple Watch, Oura, WHOOP, Fitbit, Garmin
- **Ограничение:** Нет two-way calendar integration, нет auto-rescheduling

**Oura → SensAI:**
- LLM-powered adaptive training через HealthKit bridge
- Low HRV → снижение интенсивности
- Excellent sleep → увеличение challenge
- **Ограничение:** Fitness-only, нет calendar integration

---

### Apple HealthKit

**Архитектура:** On-device only. Данные никогда не покидают устройство.

**API:**
- HKSampleQuery (one-time fetch)
- HKObserverQuery (change notification, background delivery)
- HKAnchoredObjectQuery (delta + updates)

**Критически:** HKObserverQuery **не работает после force-quit**. Нужно вызывать `completion()`.

**Privacy:** Per-data-type permissions, no app-to-app sharing.

**Ограничение:** Для server-side adaptive planning требуется iOS app как bridge.

---

### Google Health Connect

**Архитектура:** Central on-device hub для Android. Аналог HealthKit.

**Ключевой паттерн:** ChangeLogToken API для incremental pull

**Сравнение с HealthKit:**
- ✅ Cross-app sharing (central shared storage)
- ❌ Нет cloud API
- Background sync через WorkManager
- 500+ приложений интегрировано (май 2024)
- 30+ типов данных

**Focuzed.io** использует Health Connect для:
- Peak & Dip Detection
- Task Scheduling на основе circadian rhythm
- Focus Bar, Energy-based Pomodoro
- Интеграция: Google Calendar, Notion, Trello, ClickUp

---

### SensAI

**Архитектура:** Offline-first, LLM-powered

**Поддержка:** Apple Watch, Oura (via HK), WHOOP (via HK), Garmin (partial), Fitbit

**Функционал:**
- AI адаптирует план тренировки
- Low HRV → снижение интенсивности
- Excellent sleep → увеличение challenge

**Ограничение:** Fitness-only, нет calendar integration, нет cognitive recovery.

---

### Vora

**Наиболее близкий аналог** полного цикла.

**Функционал:**
- 500+ integrations
- 2-way calendar sync
- AI coach
- Training intensity + recovery recommendations

**Ограничение:** Fitness-focused, нет cognitive recovery optimization.

---

### Body Doubling Platforms

| Платформа | Модель | Effect Size | AI | Wearable |
|-----------|--------|-------------|-----|----------|
| **Focusmate** | Human-human pairing | 143% productivity | ❌ | ❌ |
| **FLOWN** | Facilitated virtual co-working | +41% sustained focus (ADHD) | ⚠️ Human facilitator | ❌ |
| **Flown.com** | Deep Work Cohorts | N/A | ❌ | ❌ |
| **AI Body Double** (Ara et al. 2025) | AI companion | dz = -0.90 vs alone | ✅ | ❌ |

**Ключевое исследование:** Ara et al. 2025 (N=12 ADHD):
- AI body double статистически неотличим от человеческого (p = 1.000)
- Task efficiency: +30% vs alone
- Sustained attention: +25% vs alone
- AI felt "less pressure, more comfortable"

---

## Competitive Positioning for life-planning-coach

### Unique Differentiators

1. **AI Coach Explains Recovery Data**
   - Не dashboard, а разговор: "Ваш HRV на 15% ниже — я перенёс презентацию"
   - Personalized recommendations в контексте задач
   - Coached reflection

2. **MCP Calendar Two-Way Integration**
   - Чтение существующих событий
   - Создание focus blocks
   - Обновление при изменении recovery
   - Удаление low-priority events

3. **Body Doubling + Recovery**
   - Recovery-aware scheduling социальных сессий
   - Social recovery через co-working
   - Mutual adaptation участников

4. **WOOP/MCII Preemptive Adaptation**
   - План B до наступления low recovery
   - IF-THEN планы для obstacles

5. **Cognitive Recovery (не только физическое)**
   - Mental detachment (Sonnentag)
   - Emotional recovery
   - Context switching optimization

---

## Risk: Hardware Dependency

| Wearable | Recovery Metric | API | Availability in RF |
|----------|----------------|-----|-------------------|
| Garmin | Body Battery | Health API | ⚠️ Niche (3.2% market) |
| Apple Watch | Нет native | HealthKit | ❌ Нет recovery metric |
| Fitbit | Daily Readiness | Web API (Premium) | ⚠️ Limited |
| Oura | Readiness Score | Cloud API (subscription) | ⚠️ Limited |
| WHOOP | Recovery Score | Developer API (membership) | ⚠️ Niche |
| Samsung | Energy Score | Samsung Health SDK | ✅ Galaxy Store |
| Huawei | Stress only | HMS Health Kit | ✅ AppGallery |
| Xiaomi | Нет | ❌ Нет API | ❌ |

**RF-specific priority:**
1. Huawei Health Kit (17% market, полная доступность)
2. Google Health Connect (универсальный агрегатор)
3. Samsung Health SDK (13.8% market)
4. Garmin Health API (niche, фитнес-энтузиасты)

---

*Исследование подготовлено: 2026-05-20*
*Источники: whoop_trainingpeaks_pattern.md, body_doubling_wearable_methodology.md*
