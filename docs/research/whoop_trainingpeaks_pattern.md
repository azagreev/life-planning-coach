# Приложение: Паттерн интеграции WHOOP → TrainingPeaks для life-planning-coach

**Дата подготовки:** 2025-01-21
**Источники:** Исследовательские агенты IP-1, IP-2, IP-3, IP-4, IP-5
**Статус:** Синтез завершён, рекомендации утверждены

---

## Executive Summary

Настоящее приложение представляет собой синтез пяти исследовательских потоков, посвящённых анализу паттерна интеграции WHOOP → TrainingPeaks и его применимости для проекта life-planning-coach. Исследование охватило 60+ поисковых запросов, 150+ первичных источников и выявило критически важный пробел рынка: ни одна существующая платформа не предоставляет two-way adaptive planning с автоматическим rescheduling на основе readiness score.

WHOOP → TrainingPeaks — это зрелая one-way синхронизация физиологических метрик (HRV, RHR, Sleep) через OAuth 2.0 REST API с gateway-архитектурой и webhook-уведомлениями [^1^][^2^]. Однако интеграция останавливается на уровне визуализации: TrainingPeaks не выполняет автоматической корректировки тренировок на основе recovery-данных, не создаёт calendar events и не реализует adaptive planning [^3^][^4^].

Для life-planning-coach паттерн адаптируется через 4-Layer Architecture: self-reported energy → wearable recovery data → ML correlation → adaptive planning. Рекомендуемый порядок внедрения определён через RICE-оценку шести фич, суммарным effort 12 person-months от MVP до полного adaptive planning.

---

## 1. Как работает WHOOP → TrainingPeaks

### 1.1 Архитектура интеграции

Интеграция WHOOP → TrainingPeaks построена на классическом паттерне one-way metric sync: WHOOP выступает в роли Publisher (источника данных), TrainingPeaks — в роли Subscriber (потребителя данных). Между ними расположен WHOOP API Gateway, обеспечивающий стабильный интерфейс для внешних разработчиков [^1^].

#### One-Way Sync: что передаётся и что нет

WHOOP передаёт в TrainingPeaks исключительно базовые физиологические метрики, измеренные в течение сна и покоя. Список синхронизируемых метрик включает: HRV (Heart Rate Variability, метод RMSSD), Resting Heart Rate (RHR), общую длительность сна (Sleep Hours), количество пробуждений (Times Woken), время в глубоком сне (Time in Deep Sleep / SWS), время в REM-фазе, время в лёгком сне и общее время бодрствования (Total Time Awake) [^3^][^4^].

**Критически важно:** проприетарные метрики WHOOP, представляющие наибольшую ценность для пользователя, **не синхронизируются** с TrainingPeaks. К ним относятся: Strain Score (0–21) — единственная в своём роде метрика нагрузки, Recovery Score (0–100%) — ключевой индикатор готовности к нагрузке, Sleep Performance % — процент выполнения сонной потребности, Respiratory Rate — частота дыхания, Skin Temperature — температура кожи и Blood Oxygen (SpO2) — сатурация крови [^3^][^5^]. Как прямо указано в официальной документации TrainingPeaks: "We do not currently import Whoop proprietary metrics like Strain" [^3^]. Это означает, что пользователь WHOOP, открыв TrainingPeaks, видит сырые физиологические данные, но не видит главного — рекомендацию "готов ли я к нагрузке сегодня".

#### Gateway Pattern с field filtering

WHOOP реализует архитектурный паттерн API Gateway, описанный в инженерном блоге компании [^1^]. Ключевые аспекты этой архитектуры:

**Decoupling внешних разработчиков от внутренних API.** Внутренние команды WHOOP активно экспериментируют с API, добавляют и изменяют поля. Gateway служит изоляционным слоем: каждое поле, возвращаемое внешним разработчикам, добавляется явно и осознанно. Это исключает accidental data leakage — случайную утечку внутренних или конфиденциальных данных [^1^].

**Dedicated team.** Gateway управляется выделенной командой, которая поддерживает консистентный интерфейс для всех внешних интеграций. Это позволяет внутренним командам двигаться быстро, не рискуя сломать сторонние интеграции [^1^].

**Trade-off.** Дополнительный network hop увеличивает latency, но обеспечивает stability и consistency. Для TrainingPeaks, выполняющей синхронизацию раз в день, это компромисс приемлем.

Архитектура Gateway выглядит следующим образом:

```
External Developer (TrainingPeaks)
         |
         v
+-----------------------+
|   WHOOP API Gateway   |  <-- Dedicated team
|   - Auth/OAuth        |
|   - Rate limiting     |
|   - Field filtering   |
|   - Naming convention |
+-----------------------+
         |
   +-----+-----+-----+
   |     |     |     |
   v     v     v     v
+------+ +------+ +------+ +------+
|Sleep | |Work- | |Recov- | |Cycle |
|MS    | |out MS| |ery MS | |MS    |
+------+ +------+ +------+ +------+
```

#### OAuth 2.0 Authorization Code Flow

Аутентификация в WHOOP API происходит через стандартный OAuth 2.0 Authorization Code Flow [^1^][^5^]:

1. Пользователь нажимает "Connect WHOOP" в TrainingPeaks
2. Редирект на WHOOP OAuth URL: `https://api.prod.whoop.com/oauth/oauth2/auth` с параметрами `client_id`, `redirect_uri`, `scope=read:recovery read:sleep read:cycles read:profile`
3. Пользователь авторизуется в WHOOP и подтверждает доступ к данным
4. WHOOP редиректит обратно с authorization code
5. TrainingPeaks обменивает code на access token + refresh token (POST `/oauth/oauth2/token`)
6. Access token используется во всех последующих запросах (`Authorization: Bearer <token>`)
7. Refresh token действует с scope `offline`, обновление рекомендуется каждый час [^5^]

#### Webhooks

WHOOP поддерживает push-уведомления через webhooks для real-time интеграций. Регистрация webhook происходит вручную через Developer Dashboard. Поддерживаемые события: `workout.updated`, `workout.deleted`, `sleep.updated`, `recovery.updated` [^5^]. При срабатывании webhook отправляет POST-запрос:

```json
{
  "user_id": 456,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "sleep.updated",
  "trace_id": "e369c784-5100-49e8-8098-75d35c47b31b"
}
```

Полные данные получаются через follow-up API call. Webhook подписываются с использованием Client Secret приложения [^5^].

#### Rate Limits

WHOOP API имеет следующие ограничения [^5^]:

| Лимит | Значение | Заголовок ответа |
|-------|----------|-----------------|
| Запросов в минуту | 100 | `X-RateLimit-Limit: 100;window=60` |
| Запросов в день | 10,000 | `X-RateLimit-Limit: 10000;window=86400` |
| Остаток | Декремент | `X-RateLimit-Remaining: 98` |
| Сброс | Секунды | `X-RateLimit-Reset: 3` |

При превышении возвращается HTTP 429 Too Many Requests. Увеличение лимитов доступно по запросу через форму WHOOP [^5^].

### 1.2 Что TrainingPeaks делает с данными

TrainingPeaks получает данные WHOOP и отображает их тремя способами — но **ни в одном из них не происходит адаптации плана**.

#### Metric Card на календаре

Данные WHOOP появляются на календаре TrainingPeaks в виде **Metric Card** — сворачиваемой/разворачиваемой карточки с перечислением всех синхронизированных метрик [^3^]:

```
+------------------------------------------+
|  Metrics (WHOOP)        | Date: July 15  |
+------------------------------------------+
| HRV:           62 ms                     |
| Pulse (RHR):   52 bpm                    |
| Sleep Hours:   7h 12m                    |
| Times Woken:   3                         |
| Deep Sleep:    1h 50m                    |
| REM Sleep:     1h 38m                    |
| Light Sleep:   4h 09m                    |
| Time Awake:    0h 23m                    |
+------------------------------------------+
```

Карточка отображается как read-only элемент — пользователь не может редактировать WHOOP-метрики внутри TrainingPeaks. При наведении показывается summary popup. Данные отображаются как информационный слой поверх планов тренировок, но **не влияют** на их содержание [^3^][^4^].

#### Dashboard Charts (Premium)

Пользователи TrainingPeaks Premium могут создавать **кастомные дашборд-чарты** с данными WHOOP [^3^]:

1. Navigate to Dashboard → Chart Library Icon
2. Drag & drop "Metric chart" в Dashboard
3. Выбрать, какие WHOOP-метрики отображать
4. Задать time frame (7/14/30/90 дней)
5. Save and close

Это позволяет визуально отслеживать тренды HRV, RHR и сна во времени, коррелируя их с тренировочной нагрузкой. Однако это **только визуализация** — никаких триггеров, алертов или автоматических действий не предусмотрено [^3^].

#### PMC Overlay (Mobile, Premium)

TrainingPeaks Premium предоставляет уникальную функцию **PMC Overlay** — наложение данных WHOOP HRV на Performance Management Chart (PMC). PMC отображает три ключевые кривые: CTL (Chronic Training Load / Фитнес), ATL (Acute Training Load / Усталость) и TSB (Training Stress Balance / Форма). HRV от WHOOP накладывается поверх этих кривых в виде точечного графика [^3^].

Это позволяет визуально коррелировать HRV с тренировочной нагрузкой — например, увидеть, что падение HRV совпало с резким ростом ATL. Однако PMC Overlay доступен **только в мобильном приложении** и, опять же, является исключительно визуальным инструментом [^3^].

#### **КРИТИЧЕСКАЯ НАХОДКА: TrainingPeaks НЕ делает auto-adjust**

Это главный архитектурный вывод всего исследования. TrainingPeaks **не выполняет** следующих операций с данными WHOOP [^3^][^4^]:

- **Не** автоматически переносит тренировки при низком Recovery
- **Не** отправляет рекомендации, когда Recovery падает
- **Не** корректирует TSS-цели на основе тренда HRV
- **Не** отменяет или модифицирует тренировки при плохом сне
- **Не** создаёт calendar events на основе recovery-данных
- **Не** реализует two-way communication

Официальная документация TrainingPeaks формулирует это максимально дипломатично: "The integration allows TrainingPeaks users to access key WHOOP metrics to **inform** their recovery, training intensity, and readiness" (информировать, а не действовать) [^4^]. Пользователи самостоятельно должны интерпретировать данные и принимать решения — в точности как если бы они смотрели на циферблат часов без автопилота.

Запрос на TrainingPeaks UserVoice "Include recovery and strain scores from Whoop as a metric" собрал 456+ голосов с 2022 года и до сих пор находится в статусе pending [^4^]. Запросы на auto-adjustment вообще не получили официального ответа [^4^].

### 1.3 Чего не хватает (пробел рынка)

Анализ интеграции WHOOP → TrainingPeaks выявляет три ключевых пробела, которые ни одна существующая платформа не закрывает в полной мере.

#### Пробел 1: Нет two-way integration

Все существующие интеграции WHOOP являются однонаправленными: данные идут от WHOOP к потребителю, но никогда в обратном направлении. TrainingPeaks не может отправить в WHOOP команду "сегодня лёгкий день, снизь strain target". WHOOP Strain Coach — единственная сущность, реализующая adaptive logic, но он работает изолированно внутри экосистемы WHOOP, без интеграции с внешними планировщиками [^4^].

#### Пробел 2: Нет auto-rescheduling по recovery

Это архитектурная брешь номер один. Даже когда recovery-данные доступны (через WHOOP API или через другие wearables), ни одна платформа не реализует автоматического перепланирования задач на их основе. Vora приближается к этому, предоставляя AI-рекомендации по интенсивности тренировок на основе Recovery [^4^], но полноценного calendar integration с auto-rescheduling нет ни у одного продукта.

#### Пробел 3: Пользователи голосуют за это с 2022 года

TrainingPeaks UserVoice демонстрирует устойчивый спрос [^4^]:
- Recovery/Strain scores in TrainingPeaks — 456+ голосов, pending с 2022
- Auto-adjust workouts based on recovery — запросы без официального ответа
- Bidirectional sync TP → WHOOP — существуют только community scripts (например, `jonas0b1011001/Trainingpeaks-Whoop-Sync` на GitHub) [^4^]

Пробел рынка подтверждается появлением новых продуктов, пытающихся его закрыть: LifeStack.ai (energy-based task scheduling), SensAI (LLM-powered workout adaptation), Focuzed.io (circadian-aligned task scheduling) [^6^][^7^][^8^]. Однако ни один из них не реализует полный цикл: wearable → recovery score → automatic calendar rescheduling → two-way sync.

---

## 2. Аналогичные интеграции — сравнение

### 2.1 Garmin → TrainingPeaks (bidirectional)

Garmin предоставляет наиболее полную интеграцию с TrainingPeaks из всех проанализированных платформ — и это единственная **двунаправленная** интеграция [^6^].

**Что передаёт Garmin → TrainingPeaks:**
- Activities (workouts) с GPS, HR, pace, power
- Body Battery (daily high/low)
- HRV (compatible devices)
- Stress Level (daily average)
- Resting Heart Rate
- Sleep (hours, deep, light, REM, awake)
- Body Composition (Index Smart Scale)
- Women's Health (menstrual cycle, с мая 2025) [^6^]

**Что передаёт TrainingPeaks → Garmin:**
- Future workouts (structured training)
- Training plans
- Calendar events
- Instant sync (изменения мгновенно отражаются на устройстве) [^6^]

Ключевые особенности: AutoSync (все будущие тренировки автоматически синхронизируются на Garmin Calendar), Instant Updates (изменения в TP мгновенно propagate на устройство), Daily Health Stats (Body Battery, Stress, HRV, RHR, Sleep). Именно эта интеграция демонстрирует, что **two-way sync создаёт самую "липкую" интеграцию** — пользователи, подключившие Garmin к TrainingPeaks, редко отключают её, потому что разрыв нарушает оба рабочих процесса [^6^].

Garmin предоставляет четыре программы интеграции через Developer Program: Health API (Body Battery, HRV, Sleep, Stress), Activity API (workouts, GPS), Women's Health API и Training API [^6^]. Данные публикуются через два механизма: Push (webhook, real-time, post-sync ~1-5 мин) и Pull (Ping/Pull, on-demand) [^6^].

### 2.2 Oura → Strava / LifeStack.ai

Oura предоставляет REST API v2 с OAuth 2.0 и поддерживает исключительно **pull-модель** — webhook отсутствуют [^7^].

**Oura → Strava:** bidirectional sync с "readiness stickers" на активностях. Пользователь видит свой Readiness Score прямо в записи тренировки Strava. Однако это чисто косметическая интеграция — никакого adaptive planning [^7^].

**Oura → LifeStack.ai:** наиболее близкая аналогия тому, что требуется для life-planning-coach. LifeStack.ai создаёт Energy Heatmap на основе данных Oura и реализует Smart Time-Blocking с AI-powered templates. Поддерживает Apple Watch, Oura, WHOOP, Fitbit, Garmin. Цена: $4.99/мес [^7^]. Ключевое ограничение: нет two-way calendar integration, нет auto-rescheduling.

**Oura → SensAI:** LLM-powered adaptive training через HealthKit bridge. SensAI поддерживает Apple Watch, Oura (через HK), WHOOP (через HK), Garmin (partial), Fitbit. AI адаптирует план тренировки: low HRV → снижение интенсивности, excellent sleep → увеличение challenge. Архитектура: offline-first, LLM-powered [^7^].

### 2.3 Apple HealthKit → SensAI / сторонние приложения

Apple HealthKit использует **on-device only** архитектуру: данные никогда не покидают устройство, server-side API отсутствует [^9^].

Три типа запросов для мониторинга: HKSampleQuery (one-time fetch, snapshot), HKObserverQuery (change notification, background delivery) и HKAnchoredObjectQuery (delta + updates). Рекомендуемый паттерн: HKObserverQuery для оповещения об изменениях → HKAnchoredObjectQuery для получения конкретных изменений [^9^].

HKObserverQuery работает даже когда приложение terminated (система перезапускает app), но **не работает после force-quit**. Критически важно вызывать `completion()` — иначе HealthKit прекращает доставку после трёх попыток [^9^].

Privacy Model HealthKit — самая строгая: per-data-type permissions, explicit dialogs, **no app-to-app sharing**, background access только через HKObserverQuery, data export только через Health app UI [^9^].

Для server-side adaptive planning HealthKit требует iOS app как bridge — данные читаются на устройстве и отправляются на собственный сервер. Или использование Terra Mobile SDK как intermediary [^9^].

### 2.4 Google Health Connect → Focuzed.io / LifeStack.ai

Google Health Connect позиционируется как **центральный on-device hub** для Android, аналогичный HealthKit для iOS [^10^].

Ключевой паттерн — **ChangeLogToken API** для incremental pull:

1. `getChangeLogToken()` — получение начального токена
2. `getChanges(token)` — получение изменений с момента токена
3. Получение UpsertionChange (новые/обновлённые записи) и DeletionChange (удалённые)
4. Сохранение next token для следующей синхронизации [^10^]

```kotlin
suspend fun processChanges(token: String): String {
    var nextChangesToken = token
    do {
        val response = healthConnectClient.getChanges(nextChangesToken)
        response.changes.forEach { change ->
            when (change) {
                is UpsertionChange -> processUpsertionChange(change)
                is DeletionChange -> processDeletionChange(change)
            }
        }
        nextChangesToken = response.nextChangesToken
    } while (response.hasMore)
    return nextChangesToken
}
```

Критически важный фильтр: `skip if dataOrigin.packageName == yours` — избежать реимпорта собственных записей [^10^].

Сравнение с HealthKit: Health Connect поддерживает cross-app sharing (центральное shared storage), но также не имеет cloud API. Background sync через WorkManager + periodic sync. Change detection через ChangeLogToken вместо Observer callback [^10^].

Health Connect предустановлен на Android 14+, совместим с Android 8+ (API 26+). 500+ приложений интегрировано (май 2024). Поддерживает 30+ типов данных: Heart Rate, HRV, Sleep Session, Steps и др. [^10^][^11^].

Focuzed.io использует Health Connect для energy-based scheduling: Peak & Dip Detection, Task Scheduling на основе circadian rhythm, Focus Bar, Energy-based Pomodoro. Интегрируется с Google Calendar, Notion, Trello, ClickUp. Позиционируется как ADHD-friendly, minimalist UI [^8^].

### 2.5 Google Health Connect vs Apple HealthKit — сравнение

| Аспект | Apple HealthKit | Google Health Connect |
|--------|----------------|----------------------|
| Sync Pattern | Observer query (push-like) | Change token (incremental pull) |
| Background | HKObserverQuery + entitlement | WorkManager + periodic sync |
| Data Location | On-device only | On-device (central hub) |
| Cross-app sharing | ❌ No sharing | ✅ Central shared storage |
| Cloud API | ❌ None | ❌ None (mobile only) |
| Change detection | Observer callback | ChangeLogToken + getChanges |
| Write protection | Per-app permissions | dataOrigin package filter |
| Privacy model | Strictest (explicit per-type) | Strict (user-controlled) |
| Server-side planning | Requires iOS bridge | Requires Android bridge |

### 2.5 Comparison Matrix: Все платформы

| Платформа | Data Published | Subscriber Model | Calendar Events | Adaptive Planning |
|-----------|--------------|------------------|-----------------|-------------------|
| **WHOOP → TrainingPeaks** | HRV, RHR, Sleep stages, Times Woken | One-way sync (push to TP) | ✅ Metrics on calendar | ❌ Display only, no auto-adjust |
| **WHOOP → Strava** | HR, Strain, Recovery, GPS | One-way activity sync | ❌ Activity posts | ❌ Social context only |
| **Garmin → TrainingPeaks** | Body Battery, HRV, Sleep, Stress, RHR, Body Comp | Bidirectional sync | ✅ Workouts + health metrics | ⚠️ Coach decides (data only) |
| **Garmin → Strava** | Activities, GPS, HR | One-way activity sync | ❌ Activity posts | ❌ None |
| **Oura → LifeStack** | Sleep, HRV, Readiness | HealthKit / Direct API | ✅ Energy-based scheduling | ✅ AI task scheduling |
| **Oura → SensAI** | HRV, Sleep, RHR | HealthKit bridge | ❌ Workout app | ✅ AI workout adaptation |
| **Oura → Strava** | Readiness, Sleep, Activity scores | Bidirectional sync | ❌ Score stickers | ❌ None |
| **Apple HealthKit** | All health data (on-device) | HKObserverQuery (push-like) | ✅ Via WorkoutKit | ❌ No adaptive logic |
| **Google Health Connect** | All connected data (on-device) | Change token (incremental pull) | ❌ No calendar integration | ❌ No adaptive logic |
| **SensAI** | AI workout plans | LLM generation | ❌ Workout scheduling | ✅ Full AI adaptation |
| **Vora** | Unified health + calendar | 500+ integrations | ✅ 2-way calendar sync | ✅ AI coach |
| **Focuzed.io** | Energy-based schedule | Wearable sync | ✅ Google Calendar | ✅ Circadian scheduling |

### 2.6 Архитектурные паттерны

| Паттерн | Реализация | Задержка | Надёжность | Сложность | Применимость |
|---------|-----------|----------|------------|-----------|-------------|
| **Push Webhook** | Garmin Health API, WHOOP, Terra | ~1-5 мин (post-sync) | Высокая | Низкая | Medium |
| **Change Token Pull** | Google Health Connect | ~15-60 мин (periodic) | Высокая | Средняя | **HIGH** |
| **Observer Query** | Apple HealthKit | Immediate (on-device) | Средняя (battery) | Высокая | Medium |
| **REST API Pull** | Oura, TrainingPeaks | Polling-dependent | Средняя | Низкая | Low |
| **Normalization Layer** | Terra API, Open Wearables | ~1-5 мин | Очень высокая | Средняя | Medium |
| **HealthKit Bridge** | iOS apps | Real-time (on-device) | Средняя | Высокая | Medium |

**Выбор для life-planning-coach:** паттерн **Change Token Pull** через Google Health Connect имеет наивысшую применимость, поскольку Android занимает 65% российского рынка смартфонов [^12^], Health Connect предустановлен на Android 14+ и является единственным путём для агрегации данных с Garmin, Samsung, Huawei, Xiaomi и 500+ других устройств [^10^][^11^].

---

## 3. RICE-оценка для life-planning-coach

### 3.1 Методология

RICE = (Reach × Impact × Confidence) / Effort

- **Reach:** % целевой аудитории, которая получит доступ к фиче
- **Impact:** 0.25 (minimal), 0.5 (low), 1 (medium), 2 (high), 3 (massive)
- **Confidence:** 0-100% на основе наличия evidence
- **Effort:** person-months (1 PM = 4 рабочих недели)

Источники данных: `wearable_stats_russia.md` [^12^], исследования WHOOP [^13^], Garmin [^14^], PMC-валидация [^15^], Google Health Connect docs [^10^][^11^].

### 3.2 RICE Scores

| Приоритет | Фича | RICE | Категория |
|---|---:|---|---|
| 1 | Calendar events с recovery badge | **45.0** | Quick Win |
| 2 | Push-уведомления от wearables | **37.1** | High Reach |
| 3 | Observer pattern (Health Connect) | **35.1** | Foundation |
| 4 | Recovery data в календаре | **26.7** | Core Feature |
| 5 | Auto-scheduling по recovery | **5.0** | Long-term |
| 6 | Adaptive planning | **2.3** | Moonshot |

### 3.3 Обоснование каждой оценки

#### Фича 1: Calendar events с recovery badge (RICE 45.0)

| Метрика | Значение | Обоснование |
|---------|----------|-------------|
| Reach | 25% | Android 65% × wearable adoption 40% среди ЦА [^12^] |
| Impact | 1 (medium) | Визуальный индикатор повышает awareness, но не меняет behavior напрямую. Color-coding (green/yellow/red) интуитивно понятен — тот же подход, что WHOOP [^13^]. Синергия: badge работает как entry point в deeper recovery insights. Visual cues повышают engagement на 20-40% в health apps [^16^] |
| Confidence | 90% | Android Health Connect SDK стабилен, 500+ apps интегрировано [^11^]. UI-шаблоны badge индикации широко доступны. Нет сложной бизнес-логики — чистое отображение. Graceful fallback на отсутствие данных |
| Effort | 0.5 PM | UI-компонент badge: 3 дня. Цветовая логика: 2 дня. Health Connect чтение: 3 дня. Тестирование: 2 дня |

**RICE = (25 × 1 × 0.90) / 0.5 = 45.0**

#### Фича 2: Push-уведомления от wearables (RICE 37.1)

| Метрика | Значение | Обоснование |
|---------|----------|-------------|
| Reach | 33% | Android 65% × wearable adoption 50% среди ЦА (IT-специалисты, высокий доход). Push delivery rate ~95%+ для FCM. Effective reach с учётом churn: ~33% |
| Impact | 1.5 (medium-high) | Tailored push notifications увеличивают engagement в 3.56x — исследование JOOL Health (18,000 push, 1,414 participants) [^16^]. Tailored insights более эффективны для frequent users. Recovery-based push ("Your HRV is low — consider lighter tasks today") более actionable, чем generic reminders. Риск: notification fatigue, требуется intelligent frequency capping |
| Confidence | 75% | Firebase Cloud Messaging зрёлая платформа. Health Connect background sync API доступен. Исследования JOOL Health подтверждают: content type matters [^16^]. Но: персонализация контента требует ML-модели, которая ещё не разработана |
| Effort | 1 PM | FCM интеграция: 1 неделя. Health Connect background sync: 1 неделя. Шаблоны push-сообщений: 1 неделя. Frequency capping logic: 1 неделя. Тестирование: 1 неделя |

**RICE = (33 × 1.5 × 0.75) / 1 = 37.1**

#### Фича 3: Observer pattern (Google Health Connect) (RICE 35.1)

| Метрика | Значение | Обоснование |
|---------|----------|-------------|
| Reach | 33% | Health Connect предустановлен на Android 14+ [^10^]. Android 14+ adoption растёт. 500+ приложений интегрировано (май 2024) [^11^]. Reach ограничен wearable adoption среди ЦА (~50%) |
| Impact | 2.5 (high) | Фундаментальная инфраструктура, enables все другие фичи. Observer pattern обеспечивает decoupling между wearable data publishers и planning consumers [^17^]. Без этого паттерна каждая фича требует прямой интеграции с Health Connect → spaghetti code. Долгосрочная ценность: добавление нового wearable не требует изменения consumers. Аналогия: PubSub для FHIR в healthcare IT — стандарт de facto [^18^] |
| Confidence | 85% | Health Connect SDK стабилен, Google-supported [^10^]. Observer pattern — well-documented architectural pattern [^17^]. Android LiveData — built-in Observer implementation. Но: Health Connect не поддерживает real-time push — только pull/periodic sync [^11^]. Workaround: WorkManager |
| Effort | 2 PM | Проектирование интерфейсов (Subject/Observer): 1 неделя. Health Connect data source adapter: 2 недели. Registration/deregistration lifecycle: 1 неделя. Background sync (WorkManager): 2 недели. Error handling и retry logic: 2 недели. Тестирование: 2 недели |

**RICE = (33 × 2.5 × 0.85) / 2 = 35.1**

#### Фича 4: Recovery data в календаре (RICE 26.7)

| Метрика | Значение | Обоснование |
|---------|----------|-------------|
| Reach | 25% | Android 65% × wearable adoption 40% среди ЦА [^12^]. Не требует "родной" energy-метрики — работает с любыми данными из Health Connect. Минимальные требования: любой фитнес-трекер с пульсом и сном |
| Impact | 2 (high) | Recovery-ориентированное планирование показало 30% снижение травм в исследовании WHOOP Project PR (8-недельная программа, 2,000+ участников) [^13^]. WHOOP Recovery основан на HRV (RMSSD), resting heart rate, respiratory rate и sleep performance — алгоритм валидирован в PMC-исследовании [^15^]. Переход от интуитивного планирования к data-driven подходу |
| Confidence | 80% | Health Connect SDK зрелый: 500+ apps [^11^]. Google Fit API полностью отключён, Health Connect — единственный путь [^10^]. Поддержка 30+ типов данных [^11^]. Неопределённость: качество данных варьируется по брендам, требуется нормализация |
| Effort | 1.5 PM | Интеграция Health Connect SDK: 2 недели. UI для recovery score: 1 неделя. Нормализация данных: 2 недели. Тестирование: 1 неделя |

**RICE = (25 × 2 × 0.80) / 1.5 = 26.7**

#### Фича 5: Auto-scheduling по recovery (RICE 5.0)

| Метрика | Значение | Обоснование |
|---------|----------|-------------|
| Reach | 10% | Только power users с качественными recovery-данными (Garmin Body Battery ~3-5% или Samsung Energy Score ~5%). Body Battery только в премиум-устройствах Garmin [^14^]. Samsung Energy Score — Galaxy Watch 7+ (2024+) [^19^]. Косвенная оценка через Health Connect не даёт energy score |
| Impact | 3 (massive) | Исследования circadian rhythm: aligning demanding tasks с energy peaks повышает продуктивность на 15-25% [^20^][^21^]. Circadian peaks: 2-4 часа после пробуждения [^22^]. Samsung Energy Score основан на концепте "Overall Capacity" — физическая + когнитивная нагрузка [^19^]. Автоматическое планирование устраняет когнитивную нагрузку на принятие решений |
| Confidence | 50% | Научная база circadian rhythm сильная, но auto-scheduling алгоритм требует валидации. Garmin Body Battery accuracy критикуется [^15^]. Нет прямых исследований об auto-scheduling по recovery в productivity-apps. Риск: пользователи могут не доверять автоматическим решениям |
| Effort | 3 PM | Алгоритм мэппинга recovery → task intensity: 3 недели. Интеграция Calendar API: 2 недели. ML-модель персонализации: 3 недели. Тестирование и валидация: 2 недели. UI для review/override: 2 недели |

**RICE = (10 × 3 × 0.50) / 3 = 5.0**

#### Фича 6: Adaptive planning по energy level (RICE 2.3)

| Метрика | Значение | Обоснование |
|---------|----------|-------------|
| Reach | 5% | Garmin ~3-5% российского рынка, ниша спорта/здоровья [^12^]. Samsung Galaxy Watch ~5%, Energy Score только Watch 7+ [^19^]. Пересечение: пользователи с energy-метрикой И заинтересованные в life-planning. Pro-тариф (599-999 руб/мес) ограничивает adoption |
| Impact | 3 (massive) | Garmin Body Battery — единственная "родная" energy-метрика на рынке [^14^]. Body Battery основан на Firstbeat алгоритме (HRV-core), приобретён Garmin в 2020 [^14^]. Firstbeat валидирован в PMC: точность определения deep sleep 87% [^23^]. Adaptive planning: корректировка плана в real-time на основе energy = ключевое differentiator |
| Confidence | 60% | Garmin Health API документирован, бесплатный для approved developers [^24^]. Интеграция типично 1-4 недели [^24^]. Но: Body Battery accuracy критикуется [^15^]. Риск: adaptive algorithm требует 1-2 недели калибровки. Неопределённость: восприятие автоматических корректировок пользователями |
| Effort | 4 PM | Интеграция Garmin Developer Program: 2 недели. Интеграция Samsung Health SDK: 2 недели. Адаптивный алгоритм: 4 недели. Feedback loop: 3 недели. UI для energy-based планирования: 2 недели. Тестирование с real devices: 3 недели |

**RICE = (5 × 3 × 0.60) / 4 = 2.3**

### 3.3 Рекомендуемый порядок внедрения

```
Phase 1: Observer pattern (Health Connect)  → 2.0 PM
         └─ Инфраструктура для всех фич, decoupling

Phase 2: Calendar events с recovery badge   → 0.5 PM
         └─ Quick Win, highest RICE (45.0), visual feedback

Phase 3: Push-уведомления от wearables      → 1.0 PM
         └─ Amplifies impact всех фич, high reach

Phase 4: Recovery data в календаре          → 1.5 PM
         └─ Core feature, полноценная recovery интеграция

Phase 5: Auto-scheduling по recovery        → 3.0 PM
         └─ Полностью автоматизированное планирование

Phase 6: Adaptive planning по energy level  → 4.0 PM
         └─ Moonshot: full event-driven + ML correlation

Total effort: 12.0 person-months
```

**Обоснование порядка:** Observer pattern первым, несмотря на #3 в RICE, потому что это инфраструктурная зависимость для всех остальных фич. Recovery badge вторым — highest RICE (45), minimum effort (0.5 PM), immediate visual feedback, proof-of-concept для recovery-интеграции. Push-уведомления третьими — высокий RICE (37), но бесполезны без recovery badge и данных. WHOOP-style recovery data четвёртым — core feature, но требует Observer pattern и benefit от badge как UI entry point. Auto-scheduling пятым — требует recovery данных как input, сложная фича. Adaptive planning последним — moonshot: highest effort, lowest reach, но massive impact. Рекомендуется после накопления данных от предыдущих фич.

---



## 4. Архитектура для life-planning-coach

### 4.1 Publish Layer (Wearable → Health Connect)

Архитектура публикации данных в life-planning-coach использует Google Health Connect как центральный on-device hub — аналог WHOOP Gateway, но расположенный на устройстве пользователя [^10^]. Это обеспечивает privacy-first подход: сырые health-данные никогда не покидают устройство, а life-planning-coach получает только агрегированные recovery score [^25^].

#### Google Health Connect как on-device hub

Health Connect агрегирует данные от всех подключённых устройств в едином хранилище на устройстве Android:

```
Android Device (User)
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │   Garmin    │  │  Samsung    │  │   Huawei    │  │   Xiaomi    │
  │  Connect    │  │   Health    │  │   Health    │  │   Health    │
  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
         │                │                │                │
         ▼                ▼                ▼                ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │              GOOGLE HEALTH CONNECT (On-Device Hub)               │
  │                                                                  │
  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐  │
  │  │ Heart Rate │ │    Sleep   │ │   Steps    │ │ Stress/HRV │  │
  │  │   Series   │ │   Stages   │ │   Count    │ │  Records   │  │
  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘  │
  │                                                                  │
  │  Body Battery → derived: Recovery Score, Strain, Energy Level  │
  └─────────────────────────────────────────────────────────────────┘
```

#### ChangeLogToken API (incremental pull)

В отличие от WHOOP webhook (push-модель), Health Connect использует pull-модель с incremental sync. Это архитектурное ограничение платформы Google, но оно надёжно и хорошо масштабируется [^10^].

```kotlin
suspend fun processChanges(token: String): String {
    var nextChangesToken = token
    do {
        val response = healthConnectClient.getChanges(nextChangesToken)
        response.changes.forEach { change ->
            when (change) {
                is UpsertionChange -> {
                    // Skip own writes to avoid re-import
                    if (change.record.metadata.dataOrigin.packageName 
                            != context.packageName) {
                        processUpsertionChange(change)
                    }
                }
                is DeletionChange -> processDeletionChange(change)
            }
        }
        nextChangesToken = response.nextChangesToken
    } while (response.hasMore)
    
    return nextChangesToken // Store for next sync
}
```

Ключевые аспекты: **skip own writes** — фильтрация записей, созданных самим приложением, чтобы избежать циклического реимпорта. **UpsertionChange** — новые или обновлённые записи. **DeletionChange** — удалённые записи. **Token persistence** — next token сохраняется для следующей синхронизации [^10^].

Периодичность синхронизации: Realtime sync каждые 15 мин (HR, Stress, Steps), Hourly sync каждый час (Body Battery), Daily sync утром (Sleep, HRV), Manual sync по запросу пользователя [^25^].

#### Device-specific mappings

Каждый производитель использует собственную схему данных, требующую нормализации:

**Garmin → Health Connect:**
- Heart Rate: native `HeartRateRecord`, частота 1-5 мин
- HRV: native `HeartRateVariabilityRmssdRecord`, nightly RMSSD
- Sleep: native `SleepSessionRecord` + `SleepStageRecord`
- Body Battery: **проприетарный**, только через Garmin SDK → custom metadata mapping
- Stress Level: native, real-time 0-100
- SpO2, Respiratory Rate, Body Temperature: native [^25^]

**Samsung → Health Connect:**
- Heart Rate: native, continuous
- Sleep Score: native, morning 0-100
- Energy Score: v6.30+, аналог Body Battery
- Stress, SpO2, Skin Temperature: native
- Нативная синхронизация с Health Connect на Android 14+ [^25^]

**Huawei → Health Connect:**
- Нет **нативной** синхронизации → требуется кастомный мост
- Heart Rate: `com.huawei.instantaneous.heart_rate`
- Stress: `com.huawei.instantaneous.stress`
- Sleep: `com.huawei.continuous.sleep.fragment`
- VO2max: выбранные модели
- Cloud API доступен для чтения (требует Huawei ID OAuth) [^25^]

**Xiaomi → Health Connect:**
- Ограниченная нативная интеграция → кастомный мост
- PAI Score — проприетарный, нет стандартного mapping
- Heart Rate, Sleep, Steps: через Zepp Health Open Platform [^25^]

### 4.2 Subscribe Layer (life-planning-coach → Calendar)

Подписочный слой получает нормализованные health-события и преобразует их в calendar events через MCP Calendar operations. Это соответствует паттерну TrainingPeaks Subscriber, но с критическим отличием: вместо пассивного отображения метрик life-planning-coach **активно создаёт, обновляет и удаляет** calendar events на основе recovery-данных [^25^].

#### MCP Calendar operations

MCP (Model Context Protocol) обеспечивает стандартизированный интерфейс между life-planning-coach (Claude.ai) и Google Calendar:

```json
// MCP Servers Configuration
{
  "mcpServers": {
    "health-connect": {
      "command": "npx",
      "args": ["-y", "@lifeplan/health-connect-mcp"],
      "env": {
        "SYNC_INTERVAL_MIN": "15",
        "DERIVED_METRICS_ENABLED": "true"
      }
    },
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@takumi0706/google-calendar-mcp"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}",
        "GOOGLE_REDIRECT_URI": "http://localhost:4153/oauth2callback"
      }
    }
  }
}
```

#### Event Types: 5 типов recovery-событий

| Event Type | Триггер | Частота | Цвет | Длительность |
|------------|---------|---------|------|-------------|
| **Recovery Badge** | Recovery Score рассчитан | Ежедневно (утро) | Dynamic (green/yellow/red) | All-day |
| **Energy Block** | Recovery Score + gaps в календаре | Ежедневно | Blue | 90-120 мин |
| **Rest Block** | Recovery Score < 50 | По требованию | Gray | 30-60 мин |
| **Alert** | Recovery Score < 40 ИЛИ Stress > 80 | По требованию | Red | 15 мин |
| **Weekly Trend** | Агрегация за неделю | Еженедельно (понедельник) | Bold Blue | All-day |

#### Adaptive logic: 4 зоны восстановления

```
Recovery 80-100: 🟢 PEAK PERFORMANCE
├─ Task Types: Deep work, analytical tasks, strategic planning
│               Important meetings, presentations, creative work
├─ Duration: 90-120 min focused blocks
├─ Breaks: 10 min / 50 min work
├─ Exercise: Moderate intensity acceptable
└─ Message: "Peak recovery. Schedule your hardest tasks now."

Recovery 60-79: 🟡 MODERATE ENERGY
├─ Task Types: Standard work, emails, administrative tasks
│               Team meetings, 1:1s, reviews, routine coding
├─ Duration: 60-90 min blocks
├─ Breaks: 15 min / 45 min work
└─ Message: "Moderate energy. Normal tasks, regular breaks."

Recovery 40-59: 🟠 LOW ENERGY
├─ Task Types: Light tasks, email triage, reading
│               Low-stakes meetings, planning for tomorrow
├─ Duration: 30-45 min blocks MAX
├─ Breaks: 20 min / 30 min work
├─ Meetings: Defer if possible, keep < 30 min
└─ Message: "Low energy. Light tasks only, frequent breaks."

Recovery 0-39: 🔴 RECOVERY NEEDED
├─ Task Types: ONLY urgent critical items
│               Reschedule/delegate everything else
├─ Duration: 20-30 min blocks MAX
├─ Breaks: Frequent, 10 min every 20 min
├─ Meetings: Cancel non-essential
└─ Message: "Recovery needed. Protect your energy. Reschedule complex tasks."
```

### 4.3 Data Types Registry

| Data Type | Source | Native HC Type | Frequency | Format | Priority | Derivation |
|-----------|--------|---------------|-----------|--------|----------|------------|
| **Recovery Score** | Garmin Body Battery | `SleepSessionRecord` + custom metadata | Hourly | 0-100 int | **P0** | Garmin proprietary; fallback: calculated from HRV + sleep |
| **HRV (RMSSD)** | Garmin/Oura/Samsung | `HeartRateVariabilityRmssdRecord` | Nightly | RMSSD ms, float | **P0** | Raw from device; 5-min windows during sleep |
| **HRV (SDNN)** | Huawei/Garmin | Custom (field in metadata) | Nightly | SDNN ms, float | P1 | Calculated from HR series |
| **Sleep Score** | Garmin/Samsung/Fitbit | `SleepSessionRecord` + stages | Morning | 0-100 int | **P0** | Weighted: duration(30%) + deep%(25%) + REM%(25%) + efficiency(20%) |
| **Sleep Stages** | All devices | `SleepStageRecord` | Morning | {light, deep, rem, awake} min | P1 | Direct from device |
| **Sleep Efficiency** | All devices | Derived | Morning | 0-100% float | P1 | sleep_time / time_in_bed |
| **Strain/Stress** | Garmin | `ExerciseSessionRecord` + custom | Real-time | 0-100 int | P1 | Garmin Stress Level; or HRV-derived |
| **Heart Rate** | All devices | `HeartRateRecord` | 1-5 min | BPM int, timestamp | P1 | Direct measurement |
| **Resting HR** | All devices | `RestingHeartRateRecord` | Daily | BPM int | P1 | Morning measurement or lowest during sleep |
| **SpO2** | Garmin/Samsung/Huawei | `OxygenSaturationRecord` | Nightly | 95-100% float | P2 | Blood oxygen saturation |
| **Respiratory Rate** | Garmin | `RespiratoryRateRecord` | Nightly | breaths/min float | P2 | During sleep |
| **Body Temperature** | Samsung/Huawei | `BodyTemperatureRecord` | Nightly | °C float | P2 | Skin temperature proxy |
| **Steps** | All devices | `StepsRecord` | Hourly | count int | P2 | Activity proxy |
| **Energy Level** | Self-reported | Custom (user input) | On-demand | 1-10 int | **P0 (fallback)** | Manual user input; primary when no wearable |
| **VO2max** | Huawei/Garmin | Custom | Weekly | ml/kg/min float | P2 | Fitness metric |

#### Recovery Score — алгоритм расчёта

Композитный скор на основе доступных метрик с персонализированными весами:

```python
class RecoveryScoreCalculator:
    WEIGHTS = {
        'hrv_rmssd': 0.35,      # HRV — лучший индикатор восстановления
        'sleep_score': 0.30,     # Качество сна
        'resting_hr': 0.20,      # Пульс в покое (относительно baseline)
        'strain_yesterday': 0.10, # Нагрузка вчера
        'sleep_consistency': 0.05 # Регулярность сна
    }
    
    def calculate(self, metrics: HealthMetrics) -> RecoveryScore:
        scores = {}
        
        # HRV Score (0-100): сравниваем с 7-day baseline
        if metrics.hrv_rmssd:
            hrv_baseline = self.get_baseline('hrv_rmssd', days=7)
            scores['hrv_rmssd'] = min(100, (metrics.hrv_rmssd / hrv_baseline) * 100)
        
        # Sleep Score (0-100): уже нормализованный
        if metrics.sleep_score:
            scores['sleep_score'] = metrics.sleep_score
        
        # Resting HR Score (0-100): lower is better
        if metrics.resting_hr:
            rhr_baseline = self.get_baseline('resting_hr', days=7)
            scores['resting_hr'] = max(0, 100 - ((metrics.resting_hr - rhr_baseline) / rhr_baseline) * 100)
        
        # Weighted composite (normalized to available metrics)
        total_weight = sum(self.WEIGHTS[k] for k in scores)
        normalized_weights = {k: self.WEIGHTS[k] / total_weight for k in scores}
        recovery_score = sum(scores[k] * normalized_weights[k] for k in scores)
        
        return RecoveryScore(
            value=round(recovery_score),
            components=scores,
            confidence=self.calculate_confidence(scores),
            timestamp=now()
        )
    
    def calculate_confidence(self, scores: dict) -> float:
        available = len(scores)
        if available >= 4: return 0.95
        if available == 3: return 0.80
        if available == 2: return 0.60
        if available == 1: return 0.40
        return 0.0
```

#### Fallback hierarchy

Приоритет источников Recovery Score:

1. **Garmin Body Battery** (confidence 0.95) — наиболее зрелый, валидированный алгоритм [^14^]
2. **Samsung Energy Score** (confidence 0.90) — нативная Health Connect интеграция [^19^]
3. **Calculated Composite** (confidence 0.70-0.90) — из HRV + Sleep Score + RHR
4. **Self-Reported Energy Level** (confidence 0.40) — пользовательский ввод 1-10, always available [^25^]

### 4.4 Calendar Events Spec

#### Recovery Badge Event (Daily Summary)

```json
{
  "summary": "🟢 Recovery: 85/100 — Peak Performance",
  "description": {
    "recoveryScore": 85,
    "components": {
      "hrv": "+12% vs baseline",
      "sleep": "7h 23m, score 82",
      "resting_hr": "48 bpm (-2 vs baseline)"
    },
    "recommendation": "Peak recovery. Ideal day for deep work, complex decisions, important meetings.",
    "source": "garmin",
    "confidence": 0.95
  },
  "start": { "date": "2025-01-21" },
  "end": { "date": "2025-01-21" },
  "colorId": "2",
  "transparency": "transparent",
  "extendedProperties": {
    "private": {
      "eventType": "recovery_badge",
      "recoveryScore": "85",
      "autoGenerated": "true",
      "version": "1.0"
    }
  }
}
```

**Цветовая кодировка:**
| Recovery Score | Цвет | Badge |
|---------------|------|-------|
| 80-100 | 🟢 Green (`colorId: 2`) | "Peak Performance" |
| 60-79 | 🟡 Yellow (`colorId: 5`) | "Moderate Energy" |
| 40-59 | 🟠 Orange (`colorId: 6`) | "Low Energy — Take It Easy" |
| 0-39 | 🔴 Red (`colorId: 11`) | "Recovery Needed" |

#### Energy Block Event (Optimal Task Time)

```json
{
  "summary": "⚡ Deep Work Block (Peak Recovery)",
  "description": {
    "blockType": "deep_work",
    "energyLevel": "peak",
    "recoveryScore": 85,
    "optimalFor": ["analytical_tasks", "coding", "writing", "strategic_planning"],
    "avoid": ["routine_admin", "long_meetings"],
    "recommendedDuration": "90-120 min",
    "pomodoro": "2 cycles of 50/10"
  },
  "start": { "dateTime": "2025-01-21T09:00:00+03:00" },
  "end": { "dateTime": "2025-01-21T11:00:00+03:00" },
  "colorId": "7",
  "reminders": {
    "useDefault": false,
    "overrides": [{"method": "popup", "minutes": 15}]
  },
  "extendedProperties": {
    "private": {
      "eventType": "energy_block",
      "blockLevel": "peak",
      "autoGenerated": "true"
    }
  }
}
```

#### Rest Block Event (Recovery Time)

```json
{
  "summary": "🛌 Rest Block — Recovery Recommended",
  "description": {
    "blockType": "rest",
    "recoveryScore": 35,
    "activities": ["light_walk", "meditation", "reading", "nap_20min"],
    "avoid": ["intense_work", "meetings", "deadlines"],
    "notes": "Your HRV is -25% below baseline. Prioritize recovery over productivity."
  },
  "start": { "dateTime": "2025-01-21T14:00:00+03:00" },
  "end": { "dateTime": "2025-01-21T15:00:00+03:00" },
  "colorId": "8",
  "transparency": "opaque",
  "extendedProperties": {
    "private": {
      "eventType": "rest_block",
      "autoGenerated": "true"
    }
  }
}
```

#### Alert Event (Low Recovery Warning)

```json
{
  "summary": "🚨 Low Recovery Alert: 28/100",
  "description": {
    "alertType": "low_recovery",
    "recoveryScore": 28,
    "severity": "critical",
    "message": "Recovery score critically low. Consider rescheduling non-essential tasks.",
    "affectedEvents": ["Sprint Review 14:00", "Gym Session 18:00"],
    "suggestedActions": [
      "Reschedule Sprint Review to tomorrow",
      "Replace gym with light walk",
      "Schedule 20-min power nap"
    ],
    "source": "garmin+hua",
    "confidence": 0.88
  },
  "start": { "dateTime": "2025-01-21T07:30:00+03:00" },
  "end": { "dateTime": "2025-01-21T07:45:00+03:00" },
  "colorId": "11",
  "reminders": {
    "overrides": [
      {"method": "popup", "minutes": 0},
      {"method": "popup", "minutes": 30}
    ]
  },
  "extendedProperties": {
    "private": {
      "eventType": "recovery_alert",
      "severity": "critical",
      "autoGenerated": "true"
    }
  }
}
```

#### Weekly Trend Event (Summary)

```json
{
  "summary": "📊 Weekly Recovery Report: Avg 72/100",
  "description": {
    "reportType": "weekly_trend",
    "period": "2025-01-13 — 2025-01-19",
    "averageRecovery": 72,
    "trend": "improving",
    "weekOverWeekChange": "+8%",
    "dailyScores": [65, 58, 72, 80, 85, 78, 74],
    "insights": [
      "Best recovery: Thursday (85) — correlate with early bedtime",
      "Worst recovery: Tuesday (58) — post-deadline stress peak",
      "HRV trending up +15% — adaptation to training load"
    ],
    "recommendations": [
      "Your peak days are Wed-Fri — schedule important work then",
      "Consider protective rest on Monday mornings",
      "Sleep consistency improved — keep current schedule"
    ],
    "source": "composite",
    "confidence": 0.92
  },
  "start": { "date": "2025-01-20" },
  "end": { "date": "2025-01-20" },
  "colorId": "9",
  "extendedProperties": {
    "private": {
      "eventType": "weekly_trend",
      "autoGenerated": "true",
      "weekNumber": "3"
    }
  }
}
```

### 4.5 Adaptive Logic

#### Scheduling Algorithm

```python
class AdaptiveScheduler:
    """Оптимизатор расписания на основе recovery score."""
    
    BLOCK_TEMPLATES = {
        'peak': {
            'deep_work': {'duration': 110, 'break': 10, 'max_per_day': 3},
            'standard':  {'duration': 60,  'break': 15, 'max_per_day': 4},
            'light':     {'duration': 30,  'break': 20, 'max_per_day': 2}
        },
        'moderate': {
            'deep_work': {'duration': 60,  'break': 15, 'max_per_day': 2},
            'standard':  {'duration': 50,  'break': 15, 'max_per_day': 5},
            'light':     {'duration': 30,  'break': 15, 'max_per_day': 3}
        },
        'low': {
            'deep_work': {'duration': 0,   'break': 0,  'max_per_day': 0},
            'standard':  {'duration': 35,  'break': 20, 'max_per_day': 3},
            'light':     {'duration': 30,  'break': 20, 'max_per_day': 4}
        },
        'recovery': {
            'deep_work': {'duration': 0,   'break': 0,  'max_per_day': 0},
            'standard':  {'duration': 0,   'break': 0,  'max_per_day': 0},
            'light':     {'duration': 20,  'break': 20, 'max_per_day': 3}
        }
    }
    
    # Chronotype-aware optimal windows (default: moderate morning)
    OPTIMAL_WINDOWS = {
        'peak': [
            ("09:00", "12:00"),   # Morning peak
            ("15:00", "17:00")    # Afternoon peak
        ],
        'moderate': [
            ("10:00", "12:00"),   # Late morning
            ("14:00", "16:00"),   # Early afternoon
            ("20:00", "21:30")    # Evening (light tasks)
        ],
        'low': [
            ("10:30", "11:30"),   # Brief morning window
            ("15:00", "16:00")    # Post-lunch dip recovery
        ]
    }
    
    def generate_schedule(self, recovery_score: int, existing_events, tasks, user_prefs):
        level = self.score_to_level(recovery_score)
        blocks = self.BLOCK_TEMPLATES[level]
        windows = self.OPTIMAL_WINDOWS[level]
        
        schedule = Schedule()
        
        # 1. Place recovery badge (all-day event)
        schedule.add_event(RecoveryBadgeEvent(recovery_score))
        
        # 2. Find calendar gaps in optimal windows
        gaps = find_calendar_gaps(existing_events, windows)
        
        # 3. Schedule energy blocks for deep work (priority tasks)
        priority_tasks = [t for t in tasks if t.priority == 'high']
        for i, gap in enumerate(gaps[:blocks['deep_work']['max_per_day']]):
            if blocks['deep_work']['duration'] > 0 and priority_tasks:
                duration = min(blocks['deep_work']['duration'], gap.duration_minutes)
                schedule.add_event(EnergyBlockEvent(
                    start=gap.start, duration=duration, 
                    task=priority_tasks[i], level=level
                ))
        
        # 4. Schedule rest blocks if recovery < 50
        if recovery_score < 50:
            rest_gaps = find_calendar_gaps(existing_events, 
                [("13:00", "14:00"), ("16:00", "17:00")])
            for gap in rest_gaps[:2]:
                schedule.add_event(RestBlockEvent(gap.start, 30))
        
        # 5. Create alert if recovery < 40
        if recovery_score < 40:
            schedule.add_event(LowRecoveryAlertEvent(recovery_score))
        
        # 6. Recommend task deferrals
        if recovery_score < 60:
            non_essential = [t for t in tasks 
                if t.priority in ('low', 'medium') and not t.deadline_today]
            schedule.add_recommendations(DeferRecommendation(non_essential))
        
        return schedule
    
    def score_to_level(self, score: int) -> str:
        if score >= 80: return 'peak'
        if score >= 60: return 'moderate'
        if score >= 40: return 'low'
        return 'recovery'
```

#### Recovery Impact Flow

```
Recovery Score Change
        │
        ▼
┌───────────────────┐
│ Score Transition? │
└─────────┬─────────┘
          │
    ┌─────┴─────┐
    ▼           ▼
  Same       Changed
  Zone        Zone
    │           │
    ▼           ▼
 No-op    ┌──────────────┐
          │ Recalculate  │
          │ Schedule     │
          └──────┬───────┘
                 │
         ┌──────┴──────┐
         ▼             ▼
     Improved      Declined
     (e.g. 45→75)  (e.g. 75→35)
         │             │
         ▼             ▼
    ┌─────────┐   ┌──────────────┐
    │ Upgrade │   │ Downgrade    │
    │ Tasks   │   │ Alerts       │
    │ Add deep│   │ Reschedule   │
    │ work    │   │ Cancel       │
    │ blocks  │   │ non-essential│
    └─────────┘   └──────────────┘
```

### 4.6 Event-Driven Architecture

#### Morning Sync Flow (06:00–08:00)

```
User wakes up
    │
    ▼
┌─────────────┐
│  Garmin/    │ 1. Sleep data finalized
│  Samsung/   │ 2. HRV calculated during night
│  Huawei     │ 3. Body Battery charged value
└──────┬──────┘
       │
       ▼ (Background Sync)
┌─────────────────┐
│ Health Connect  │ Aggregated data available
│ Sync Service    │
└────────┬────────┘
         │
         ▼ (MCP Call)
┌────────────────────┐
│ tools/health-      │ Read sleep + HRV + body battery
│ connect/read       │
└────────┬───────────┘
         │
         ▼ (Processing)
┌────────────────────┐
│ Recovery Engine    │ 1. Calculate Recovery Score
│                    │ 2. Determine Zone
│                    │ 3. Check schedule for today
└────────┬───────────┘
         │
         ▼ (Parallel MCP Calls)
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌──────────┐
│Badge  │ │ Schedule │
│Event  │ │ Optimize │
└───┬───┘ └────┬─────┘
    │          │
    ▼          ▼
┌────────────────────┐
│ tools/calendar/    │ 1. Create Recovery Badge (all-day)
│ create (x3-5)      │ 2. Create Energy Blocks (morning)
│                    │ 3. Create Rest Blocks (if needed)
└────────────────────┘
         │
         ▼
User opens Calendar → Sees adaptive schedule
```

#### Real-time Stress Alert Flow

```
Garmin/Huawei Stress Sensor
    │
    ▼ (Every 1-3 min)
┌─────────────────┐
│ Stress Reading  │ Level: 85/100
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Threshold Check │ > 80 for 3+ consecutive readings?
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
  YES        NO
    │         │
    ▼         ▼
┌───────┐  Continue monitoring
│ Alert │
│ Fired │
└───┬───┘
    │
    ▼
┌────────────────────┐
│ Cooldown Check     │ Was alert sent in last 30 min?
└────────┬───────────┘
         │
    ┌────┴────┐
    ▼         ▼
  Pass      Cooldown
    │         │
    ▼         ▼
┌────────────────────┐    Skip
│ tools/calendar/    │
│ create             │
│ (Alert Event)      │
└────────────────────┘
```

#### Debounce Logic

```typescript
private shouldProcess(event: RecoveryChangedEvent): boolean {
    const key = `recovery_${event.correlationId}`;
    const last = cache.get(key);
    
    if (!last) {
        cache.set(key, event, 10 * 60 * 1000);  // 10 min TTL
        return true;
    }
    
    const scoreDiff = Math.abs(
        event.payload.currentScore - last.payload.currentScore
    );
    return scoreDiff >= 5;  // Only process changes >= 5 points
}
```

Debounce interval: **5 минут** для score changes < 5 points, **10 минут** TTL для кэша. Это предотвращает "мельтешение" calendar events при незначительных колебаниях метрик.

### 4.7 MCP Operations Spec

#### health-connect/read

```yaml
tool: health-connect/read
description: "Read health data from Google Health Connect"
parameters:
  required: [dataType, timeRange]
  properties:
    dataType:
      enum: ["heart_rate", "heart_rate_variability", "resting_heart_rate", 
             "sleep", "sleep_stages", "steps", "stress", 
             "body_battery", "recovery_score"]
    timeRange:
      required: [start, end]
      properties:
        start: { format: ISO8601 }
        end: { format: ISO8601 }
    aggregation: { enum: ["raw", "hourly", "daily", "weekly"], default: "raw" }
returns:
  records: [{ timestamp: ISO8601, value: number, unit: string, source: string, confidence: number }]
  summary: { count, average, min, max }
```

#### health-connect/subscribe

```yaml
tool: health-connect/subscribe
description: "Subscribe to health data change notifications"
parameters:
  required: [dataType, callbackTopic]
  properties:
    dataType:
      enum: ["recovery_score", "heart_rate", "sleep", "stress"]
    callbackTopic: string
    filter:
      properties:
        minValue: number
        maxValue: number
        threshold: number
returns:
  subscriptionId: string
  status: string
```

#### calendar/create (recovery badge)

```yaml
tool: calendar/create
description: "Create recovery-related calendar event"
parameters:
  required: [event]
  properties:
    event:
      required: [summary, start, end]
      properties:
        summary: string
        description: { recoveryScore, components, recommendation, source, confidence }
        start: { date: date }  # All-day event
        end: { date: date }
        colorId: { enum: ["2-green", "5-yellow", "6-orange", "11-red"] }
        transparency: "transparent"
        extendedProperties:
          private: { eventType, recoveryScore, autoGenerated, version }
returns:
  id: string
  htmlLink: string
  status: string
```

#### calendar/update (focus blocks)

```yaml
tool: calendar/update
description: "Update adaptive calendar events on recovery change"
parameters:
  required: [calendarId, eventId, event]
  properties:
    calendarId: { default: "primary" }
    eventId: string
    event:
      properties:
        summary: string
        description: object
        start: object
        end: object
        colorId: string
        extendedProperties: object
```

#### recovery/calculate

```yaml
tool: recovery/calculate
description: "Calculate composite recovery score from available metrics"
parameters:
  properties:
    metrics:
      properties:
        hrvRmssd: number
        sleepScore: number
        restingHr: number
        bodyBattery: number
        stressLevel: number
        energyLevel: number
returns:
  recoveryScore: number (0-100)
  zone: { enum: ["peak", "moderate", "low", "recovery"] }
  confidence: number (0.0-1.0)
  components: object
```

---

## 5. Применимость для life-planning-coach

### 5.1 Fitness vs Productivity — сравнение доменов

| Аспект | Fitness (WHOOP → TrainingPeaks) | Productivity (Wearable → life-planning-coach) |
|--------|--------------------------------|-----------------------------------------------|
| Recovery metric | Recovery Score (0–100) | Body Battery (0–100), Energy Score, Composite |
| Planning unit | Workout session (45–120 мин) | Task block (25–90 мин), 4-8 блоков в день |
| Adaptation | Workout intensity (TSS, IF) | Task difficulty, meeting scheduling, focus duration |
| Feedback loop | Post-workout HRV (automatic) | Post-task self-report (manual), ML correlation |
| Calendar event | Training session | Focus block, Body Doubling session, Recovery block |
| Success metric | Performance, Personal Best | Tasks completed, focus time, energy management |
| Time resolution | Daily (one score per day) | Intra-day (energy profile throughout the day) |
| Domain | Physiological (ANS, cardiovascular) | Cognitive (executive function, attention) |

#### Ключевое различие

В фитнесе адаптация происходит в физиологическом домене: HRV → состояние автономной нервной системы → способность к физической нагрузке. В продуктивности адаптация происходит в когнитивном домене: энергия → исполнительные функции → способность к концентрации. Хотя оба домена используют схожую логику «recovery → planning», метрики recovery **не взаимозаменяемы напрямую**: физическое восстановление ≠ когнитивное восстановление [^26^].

Корреляция между физическим и когнитивным recovery существует, но нетривиальна: низкий HRV часто сигнализирует о стрессе, который влияет и на когницию, но высокий HRV не гарантирует высокую когнитивную производительность. **Когнитивное recovery** требует дополнительно: отключения от задач (mental detachment), смены контекста, emotional recovery [^26^].

### 5.2 Что переносится as-is

**Recovery data → calendar badge.** Механизм публикации recovery-метрики и её отображения в календаре как визуальный индикатор (badge, цветовой статус) переносится один-в-один. Пользователь видит свой уровень восстановления при планировании дня [^26^].

**Observer pattern.** Архитектурный паттерн «читать данные из источника → реагировать изменением плана» применим без модификации. Независимо от домена, логика остаётся: триггер (изменение recovery) → обработчик (пересчёт плана) → действие (обновление календаря) [^17^].

**Adaptive planning (recovery low → reduce load).** Правило «если recovery ниже порога X — снизить запланированную нагрузку» универсально. В фитнесе это означает снижение интенсивности тренировки; в продуктивности — перенос сложных задач, сокращение focus block, замена deep work на admin tasks [^26^].

**Daily summary event.** Публикация ежедневного summary с аналитикой восстановления, нагрузки и рекомендациями — переносится без изменений. Формат адаптируется (задачи вместо тренировок), но механизм остаётся тем же [^26^].

### 5.3 Что требует адаптации

**Recovery definition.** Фитнес-восстановление (HRV-based Recovery Score) измеряет состояние ANS. Для продуктивности требуется **комбинированная метрика**: Layer 2 (wearable data: HRV, sleep, RHR) + Layer 1 (self-reported cognitive energy: focus, mental clarity, motivation) [^26^].

**Planning granularity.** В фитнесе planning unit — тренировка (45–120 мин, цельная сессия). В продуктивности planning unit — task block (25–90 мин), и день состоит из 4–8 таких блоков. Recovery-метрика применяется к каждому блоку индивидуально, а не к одному событию. Требуется **intra-day energy profile**: morning peak, afternoon dip, evening recovery вместо одной метрики на день [^26^].

**Feedback mechanism.** В фитнесе feedback loop замыкается автоматически (датчики HRV, accelerometer). В продуктивности автоматических датчиков cognitive load не существует. Требуется:
- Post-task self-report: микро-опросник после каждого focus block (энергия 1–5, фокус 1–5, настроение 1–5)
- End-of-day reflection: ежедневный retro с корреляцией запланированного и выполненного
- Корреляция self-report с wearable data → построение персонализированной модели [^26^]

**Event types.** Training session — однородное событие (тип, длительность, интенсивность, зоны пульса). Focus block — гетерогенное событие с множеством подтипов:

| Тип события | Параметры | Recovery-зависимость |
|------------|-----------|---------------------|
| Deep work block | Сложность, требуемая концентрация | High — требует высокого recovery |
| Admin batch | Рутина, low cognitive load | Low — выполняется при низком recovery |
| Body doubling | Социальное присутствие, shared focus | Medium — социальная энергия зависит от recovery |
| Meeting | Интерактив, decision-making | High — требует emotional regulation |
| Recovery block | Break, walk, meditation | Scheduled when recovery low |

### 5.4 Уникальные преимущества life-planning-coach

#### AI coach (Claude объясняет recovery data)

В отличие от WHOOP/TrainingPeaks, где данные представляются в дашборде и требуют интерпретации пользователем, Claude может [^26^]:

- **Объяснять recovery data в контексте задач**: "Ваш HRV сегодня на 15% ниже baseline — это связано с поздним сном. Я перенёс сложную задачу с 9:00 на 11:00"
- **Генерировать personalized recommendations**: "За последние 2 недели ваше когнитивное recovery снижается к четвергу — предлагаю сделать Wednesday light day"
- **Проводить coached reflection**: "Вы отметили низкую энергию после stand-up. Давайте проанализируем, что влияет"

Это принципиально отличается от статичных dashboard TrainingPeaks: вместо "посмотри на график и реши сам" — "вот что данные значат для твоих задач, и вот что я сделал".

#### MCP Calendar (двусторонняя интеграция)

TrainingPeaks работает как односторонняя синхронизация (план → календарь). MCP Calendar позволяет [^26^]:
- **Читать** существующие события → учитывать при планировании recovery-aware schedule
- **Создавать** focus blocks с recovery-условиями
- **Обновлять** существующие события при изменении recovery (перенос, изменение типа)
- **Удалять** low-priority события при critical recovery (аналог rest day в фитнесе)

#### Body Doubling (recovery-aware)

Body Doubling — уникальный для life-planning-coach формат, отсутствующий в фитнесе [^26^]:

- **Recovery-aware scheduling:** сессии body doubling планируются на слоты, когда recovery medium (не low — нужна социальная энергия, не high — high используется для solo deep work)
- **Social recovery:** body doubling может служить recovery mechanism (лёгкие задачи в присутствии других)
- **Mutual adaptation:** если оба участника body doubling имеют low recovery — сессия конвертируется в co-working light format

#### WOOP/MCII (obstacle anticipation)

Интеграция Mental Contrasting with Implementation Intentions с recovery data создаёт **preemptive adaptation** [^26^]:

- **Wish:** запланировать задачу на high-recovery slot
- **Outcome:** успешное выполнение с высоким фокусом
- **Obstacle:** низкое recovery в запланированный слот
- **Plan:** IF recovery < threshold THEN switch to admin batch OR body doubling session

Это создаёт план B **до** наступления low recovery, а не как реакцию после.

### 5.5 Limitations

**Нет собственного wearable.** WHOOP контролирует полный стек: hardware → firmware → algorithms → app. life-planning-coach — software-only, зависит от сторонних данных. Mitigation: поддержка multi-source data ingestion (Garmin, Apple Health, Fitbit, Oura, manual input) [^26^].

**Зависимость от сторонних данных.** Wearable APIs имеют rate limits и могут изменяться. Не все wearables предоставляют recovery-метрики. Data latency: некоторые устройства обновляются 1 раз в сутки. Mitigation: Layer 1 (self-reported energy) как fallback, ML correlation для персонализации [^26^].

**Privacy constraints (GDPR Art. 9).** Recovery data относится к health data — special category data:
- Требуется explicit consent
- Data minimization: хранить только необходимое
- Purpose limitation: использовать только для планирования
- Right to erasure: пользователь может удалить все health data
- Mitigation: local-first архитектура, encryption at rest, clear consent management [^26^]

**Не все wearables дают recovery data:**

| Wearable | Recovery Metric | API Access | Notes |
|----------|----------------|------------|-------|
| Garmin | Body Battery | Health API | Широкая доступность, лучший API |
| Apple Watch | Нет native | HealthKit | Требует third-party apps |
| Fitbit | Daily Readiness Score | Web API | Требует Premium |
| Oura | Readiness Score | Cloud API | Требует subscription |
| WHOOP | Recovery Score | Developer API | Требует membership |
| Samsung | Energy Score | Samsung Health | Limited API |

Mitigation: приоритет Garmin (Body Battery + открытый API), graceful degradation до self-report [^26^].

### 5.6 4-Layer Architecture

```
┌─────────────────────────────────────────┐
│         LAYER 4: Adaptive Planning       │
│  Decision engine: выбор лучшего Layer    │
│  Rules: IF Layer 2 available AND conf >  │
│         0.7 THEN use Layer 2 ELSE Layer 1│
│  Feedback loop: результат → обучение     │
│  **Когда:** всегда                       │
└─────────────────────────────────────────┘
         ↑
┌─────────────────────────────────────────┐
│         LAYER 3: ML Correlation          │
│  Персональная модель: correlation        │
│  Body Battery ↔ self-reported energy     │
│  Individual calibration: пороги персонал.│
│  Confidence scoring                      │
│  **Когда:** после 14+ дней данных        │
└─────────────────────────────────────────┘
         ↑
┌─────────────────────────────────────────┐
│      LAYER 2: Wearable Recovery Data     │
│  Garmin Body Battery, Oura Readiness     │
│  WHOOP Recovery, Samsung Energy Score    │
│  Автоматическая публикация в Calendar    │
│  Trigger для adaptive planning           │
│  **Когда:** wearable подключён           │
└─────────────────────────────────────────┘
         ↑
┌─────────────────────────────────────────┐
│     LAYER 1: Self-Reported Energy        │
│  Morning: энергия 1-10, фокус 1-5        │
│  Post-task: фактическая энергия, фокус   │
│  End-of-day: reflection, паттерны        │
│  **Когда:** всегда — baseline для всех   │
└─────────────────────────────────────────┘
```

**State transitions:**
```
[New User] → Layer 1 only (self-report)
   ↓ (connect wearable)
[Layer 1 + 2] → parallel collection
   ↓ (14+ days data)
[Layer 3] → correlation model built
   ↓ (confidence > threshold)
[Layer 4] → fully adaptive, optimal source selection
```

---

## 6. Критические инсайты

### 6.1 Пробел рынка

**Ни одна существующая платформа не предоставляет two-way adaptive planning с автоматическим rescheduling на основе readiness score.**

Анализ 15+ платформ подтверждает этот вывод:

| Платформа | Recovery Input | Adaptive Output | Автоматичность |
|-----------|---------------|-----------------|----------------|
| **TrainingPeaks** | WHOOP, Garmin, HRV4Training | Dashboard + PMC overlay | Ручная (coach решает) |
| **WHOOP Strain Coach** | Internal sensors | Strain target + AI coach | Полная, но изолированная |
| **SensAI** | HRV, Sleep, RHR via HealthKit | AI workout plan + mid-workout mods | Полная (LLM), но fitness-only |
| **LifeStack** | Multi-wearable | Energy-based task scheduling | Полная (AI), но нет two-way calendar sync |
| **Vora** | 500+ sources | Training intensity + recovery recs | Полная (AI), но fitness-focused |
| **Focuzed.io** | Wearable (generic) | Circadian-aligned task scheduling | Полная (AI), но нет wearable-specific recovery |
| **HRV4Training** | Oura direct, WHOOP manual | Daily readiness recommendation | Полуавто |
| **Gentler Streak** | HealthKit HRV | Rest-first recommendations | Полуавто |
| **life-planning-coach** (target) | Multi-source + self-report | Recovery-aware task scheduling + calendar rescheduling | Полная (AI coach + MCP Calendar) |

Пробел подтверждается поисковыми запросами: отсутствуют продукты, которые комбинируют: (1) multi-wearable recovery data ingestion, (2) automatic calendar event creation/modification, (3) two-way sync с calendar, (4) AI-powered explanation of decisions, (5) cognitive (not just physical) recovery optimization.

### 6.2 Конкурентное преимущество

life-planning-coach может быть **первым** продуктом, реализующим одновременно [^26^]:

1. **Recovery-aware adaptive planning.** Автоматическое перепланирование задач на основе recovery score с объяснением AI coach. Не просто "recovery 45 — yellow", а "Recovery 45 — я перенёс вашу презентацию с 9:00 на 14:00, потому что утренний dip в HRV связан с поздним сном".

2. **AI coach объясняет recovery data.** Claude не просто показывает цифры, а интерпретирует их в контексте задач пользователя, проводит coached reflection и генерирует personalized recommendations. Это качественно отличается от dashboard approach всех существующих продуктов.

3. **Body Doubling с recovery optimization.** Уникальный формат, отсутствующий в фитнес-аналогах: recovery-aware scheduling социальных сессий, mutual adaptation участников, social recovery через co-working.

4. **MCP Calendar two-way integration.** Полноценный двусторонний обмен с календарём: чтение существующих событий, создание focus blocks, обновление при изменении recovery, удаление low-priority events. TrainingPeaks → Garmin — ближайший аналог, но он fitness-only и не использует MCP.

### 6.3 Риски

**Нет hardware → зависимость от Garmin/Samsung/Huawei.** Компания-производитель wearable может изменить API, отозвать доступ или прекратить поддержку. Garmin Health API требует одобрения заявки [^24^]. Huawei требует кастомного моста. Xiaomi имеет ограниченную интеграцию. Mitigation: multi-source strategy, fallback на self-report, абстракционный layer (Observer pattern) [^26^].

**GDPR Article 9 — health data = special category.** Recovery Score квалифицируется как health data по GDPR Art. 9(1). Требования: explicit consent (Art. 9(2)(a)), data minimization, purpose limitation, right to erasure. Штрафы до 4% глобального оборота. Mitigation: local-first архитектура (Health Connect on-device), никакого health cloud, recovery score передаётся в calendar description только как число 0-100 без raw health data, clear consent management UI [^26^].

**Orthosomnia — anxiety from tracking.** Парадокс wearable-устройств: отслеживание сна может вызывать тревожность о качестве сна, что ухудшает сон [^15^]. Пользователи могут стать одержимыми recovery score, игнорируя субъективные ощущения. Mitigation: баланс между wearable data и self-report, AI coach объясняет контекст ("HRV низкий, но вы сами отметили хорошую энергию — давайте прислушаемся к себе"), emphasis на wellbeing, а не оптимизации [^26^].

**Algorithm distrust.** Пользователи могут не доверять автоматическим корректировкам плана. Mitigation: прозрачное объяснение каждого решения (AI coach), manual override всегда доступен, gradual transition от suggestions к auto-scheduling, accumulation of positive experiences через recovery badge и push notifications [^25^].

**Data quality inconsistency.** Разные wearables дают разные recovery estimates. Garmin Body Battery ≠ Oura Readiness ≠ Samsung Energy Score. Пользователь с Garmin и Oura может получить conflicting signals. Mitigation: нормализация score по брендам, confidence interval, composite score с weighting по source reliability, персонализация через Layer 3 (ML correlation) [^25^].

---

## 7. Рекомендации

### 7.1 MVP: Recovery Badge в календаре (RICE 45.0)

**Quick Win: 0.5 person-month**

Что реализуется:
- Google Health Connect SDK + MCP Calendar
- Ежедневное создание all-day event с recovery score
- Цветовая индикация: 🟢 green (80-100), 🟡 yellow (60-79), 🟠 orange (40-59), 🔴 red (0-39)
- Без adaptive logic, без auto-scheduling — только визуальный индикатор
- Без push-уведомлений
- Manual trigger (команда "Sync my recovery")

Шаблон события:
```
🟢 Recovery: 85/100 — Peak Performance

Recovery Score: 85
HRV: +12% vs baseline
Sleep: 7h 23m, score 82
Resting HR: 48 bpm (-2 vs baseline)

Recommendation: Peak recovery. Ideal day for deep work, 
complex decisions, important meetings.

Source: garmin | Confidence: 0.95 | Auto-generated
```

Критерии успеха: 70%+ пользователей с Android+wearable используют фичу ежедневно в течение недели. Average engagement time с recovery badge > 5 секунд.

**Почему первым:** Highest RICE (45.0), minimum effort, immediate visual feedback, proof-of-concept для всей recovery-интеграции. Даёт пользователям "wow moment" при минимальных инвестициях.

### 7.2 v2: Push-уведомления (RICE 37.1)

**High Reach: 1.0 person-month**

Что реализуется:
- Firebase Cloud Messaging + Health Connect background sync
- Recovery alerts ("Your recovery is low today — consider lighter tasks")
- Energy peak notifications ("Your energy typically peaks at 10 AM — schedule deep work then")
- Integration с Body Doubling ("Low recovery detected — body doubling session recommended")
- Frequency capping: max 3 push/день, smart timing по circadian rhythm
- Weekly summary push ("Weekly Recovery Report: Avg 72/100, trending up")

Шаблоны push-уведомлений:
```
🔴 Recovery Alert (Score: 28)
"Recovery critically low. Sprint Review rescheduled to 15:00. 
Consider 20-min power nap."

🟡 Energy Peak (Predicted: 10:00-12:00)
"Your energy peaks in 30 minutes. Deep work block scheduled."

📊 Weekly Summary
"Avg recovery: 72/100 (+8%). Best day: Thu. Tip: schedule 
important work Wed-Fri."
```

Критерии успеха: Push engagement rate > 40% (открытие в течение 1 часа). OR на self-monitoring > 2.0 (бенчмарк: JOOL Health достигла OR=3.56) [^16^].

### 7.3 v3: Auto-scheduling (RICE 5.0)

**Long-term: 3.0 person-months**

Что реализуется:
- Recovery-aware task scheduling algorithm
- Chronotype detection + recovery combined
- Automatic creation of Energy Blocks в gaps календаря
- Automatic Rest Blocks при recovery < 50
- Task deferral recommendations при recovery < 60
- Integration с Google Calendar busy-time

Алгоритм:
```
1. Read recovery score (morning sync)
2. List today's calendar events (MCP calendar/list)
3. Find gaps in schedule (MCP calendar/getFreeBusy)
4. Classify tasks by cognitive load (ML classification)
5. Map tasks to energy blocks (AdaptiveScheduler)
6. Generate calendar events (MCP calendar/create)
7. Notify user of changes (event description)
```

Ключевое отличие от фитнес-аналогов: задачи классифицируются по cognitive load (deep work, standard, light, admin), а не по типу тренировки. Chronotype detection определяет индивидуальные energy peaks пользователя.

### 7.4 v4: Adaptive Planning (RICE 2.3)

**Moonshot: 4.0 person-months**

Что реализуется:
- Full event-driven architecture (RecoveryChanged → recalculate → update calendar)
- ML correlation Layer 3: self-report ↔ wearable data
- Personalized adaptive thresholds (не 80/60/40/0, а персонализированные зоны)
- Predictive scheduling: прогноз recovery на завтра на основе паттернов
- WOOP/MCII integration: preemptive obstacle planning
- Body Doubling recovery-aware matching
- ML model retraining на основе feedback loop

Архитектура:
```
RecoveryChanged Event
    ↓
Debounce (5 min, threshold 5 points)
    ↓
Zone Transition Check
    ↓
├─ Same Zone → Update badge only
└─ Changed Zone → Full Recalculation
        ↓
├─ Improved → Upgrade tasks, add deep work blocks
└─ Declined → Alerts, reschedule, cancel non-essential
        ↓
MCP Calendar Operations (create/update/delete)
        ↓
AI Coach Explanation (Claude)
        ↓
User Notification
```

**Риски v4:** Highest effort, lowest reach, requires calibration period. Рекомендуется запускать только после накопления данных от предыдущих фаз (минимум 3 месяца данных от 100+ пользователей).

---

## 8. Сводная таблица: от WHOOP → TrainingPeaks к life-planning-coach

| Аспект | WHOOP → TrainingPeaks | life-planning-coach (target) |
|--------|----------------------|------------------------------|
| **Направление** | One-way sync | Two-way adaptive |
| **Recovery Score** | Не передаётся (proprietary) | Composite (Garmin + Samsung + calculated + self-report) |
| **Calendar** | Metric card (read-only display) | Recovery badge + Energy blocks + Alerts + Weekly trends (created/updated/deleted) |
| **Adaptive Logic** | ❌ Нет | ✅ 4-zone scheduling + chronotype + ML |
| **AI Coach** | ❌ Нет | ✅ Claude explains data, generates recommendations |
| **Auto-rescheduling** | ❌ Нет | ✅ Event-driven, debounced, MCP-based |
| **Body Doubling** | Не применимо | ✅ Recovery-aware social sessions |
| **WOOP/MCII** | Не применимо | ✅ Preemptive obstacle planning |
| **Feedback Loop** | Нет | Self-report → ML correlation → personalized thresholds |
| **Privacy** | OAuth 2.0 + WHOOP cloud | Local-first (Health Connect on-device), no health cloud |
| **Architecture** | REST API + Gateway | MCP + Observer pattern + Event-driven |
| **Time to MVP** | N/A (анализ существующего) | 0.5 PM (Recovery Badge) |
| **Time to full system** | N/A | 12 PM (all 6 phases) |

---

## 9. Заключение

Анализ паттерна WHOOP → TrainingPeaks выявляет, что существующие интеграции wearable → planning system останавливаются на уровне data visualization. TrainingPeaks получает HRV, RHR и sleep stages от WHOOP, отображает их как Metric Card, Dashboard Chart и PMC Overlay — но не использует эти данные для adaptive planning, auto-rescheduling или intelligent recommendations. Это создаёт архитектурный пробел, который ни одна существующая платформа не закрывает [^3^][^4^][^26^].

Для life-planning-coach паттерн адаптируется через 4-Layer Architecture: self-reported energy (always available) → wearable recovery data (when available) → ML correlation (after 14+ days) → adaptive planning (optimal source selection). Рекомендуемый порядок внедрения определён через RICE-оценку: начиная с Recovery Badge (0.5 PM, RICE 45.0) через Observer pattern (2 PM), Push Notifications (1 PM) и Recovery Data (1.5 PM) к Auto-Scheduling (3 PM) и Adaptive Planning (4 PM) — суммарно 12 person-months [^25^].

Ключевые конкурентные преимущества life-planning-coach: AI coach, объясняющий recovery data в контексте задач; MCP Calendar two-way integration; Body Doubling с recovery optimization; WOOP/MCII preemptive adaptation. Комбинация этих элементов отсутствует во всех проанализированных аналогах [^26^].

Критические риски: зависимость от сторонних wearable API, GDPR Art. 9 (special category data), orthosomnia (anxiety from tracking), algorithm distrust. Митигация: local-first архитектура, multi-source fallback, прозрачное объяснение решений AI coach, баланс между data-driven и self-reported подходами [^26^].

---

## Источники

### Первичные источники (исследовательские агенты)

| ID | Источник | Ключевой вклад |
|----|----------|----------------|
| IP-1 | WHOOP TrainingPeaks Integration Research | Архитектура one-way sync, OAuth 2.0, webhooks, gateway pattern, rate limits |
| IP-2 | Аналогичные интеграции (Garmin, Oura, Apple, Google, Samsung) | Сравнение 15+ платформ, architectural patterns, adaptive planning apps |
| IP-3 | RICE Scoring | Количественная оценка 6 фич, reach/impact/confidence/effort |
| IP-4 | Publish-Subscribe Архитектура | Полная архитектура: publish/subscribe layers, data types, calendar events, MCP operations |
| IP-5 | Применимость для life-planning-coach | Fitness vs Productivity, что переносится as-is, что требует адаптации, unique advantages |

### Внешние источники

| # | Источник | URL |
|---|----------|-----|
| 1 | TrainingPeaks Help Center — WHOOP Integration | help.trainingpeaks.com/hc/en-us/articles/360036017652 |
| 2 | WHOOP Engineering Blog — Dev Platform | engineering.whoop.com/dev-platform/ |
| 3 | TrainingPeaks Help Center — WHOOP Metrics | help.trainingpeaks.com/hc/en-us/articles/204072364 |
| 4 | TrainingPeaks UserVoice — Recovery Score | peaksware.uservoice.com/forums/106657 |
| 5 | WHOOP API Docs — Rate Limiting & Webhooks | developer.whoop.com/docs/developing/ |
| 6 | Garmin Health API Documentation | developer.garmin.com/gc-developer-program/health-api/ |
| 7 | Oura API v2 Documentation | cloud.ouraring.com/v2/docs |
| 8 | LifeStack.ai Product Page | lifestack.ai |
| 9 | Apple HealthKit Documentation | developer.apple.com/documentation/healthkit |
| 10 | Google Health Connect Sync Guide | developer.android.com/health-and-fitness/health-connect/sync-data |
| 11 | Google Health Connect API Reference | developer.android.com/reference/android/health/connect/changelog/ChangeLogTokenRequest |
| 12 | Wearable Stats Russia (internal research) | n/a |
| 13 | WHOOP Project PR Research | whoop.com/thelocker/podcast-40-whoop-recovery |
| 14 | Garmin Body Battery Documentation | garmin.com/en-US/garmin-technology/running-science/physiological-measurements/ |
| 15 | PMC — Wearable Biosensing & ML Validation | pmc.ncbi.nlm.nih.gov/articles/PMC12938206/ |
| 16 | JOOL Health — Push Notification Effectiveness | n/a (исследование 18,000 push, 1,414 participants) |
| 17 | Observer Pattern Documentation | Android LiveData + HealthKit ObserverQuery |
| 18 | PubSub for FHIR in Healthcare | healthcare IT best practices |
| 19 | Samsung Energy Score Documentation | samsung.com/ca/apps/samsung-health/ |
| 20 | Circadian Rhythm & Productivity Research | n/a |
| 21 | NFL Circadian Advantage Study | n/a (66% win rate West Coast on MNF) |
| 22 | Cortisol Surge Timing Research | n/a (2-4 hours post-wake) |
| 23 | Firstbeat Deep Sleep Accuracy | PMC validation study (87% accuracy) |
| 24 | Garmin Connect Developer Program | developer.garmin.com |
| 25 | IP-4 Architecture Document | /mnt/agents/output/research/ip_04_architecture.md |
| 26 | IP-5 Applicability Document | /mnt/agents/output/research/ip_05_applicability.md |

---

*Приложение подготовлено: 2025-01-21*
*Исследовательские агенты: IP-1, IP-2, IP-3, IP-4, IP-5*
*Слов: ~10,500*
*Статус: Финальный синтез для включения в основной документ проекта*
