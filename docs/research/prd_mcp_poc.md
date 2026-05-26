# PRD: PoC MCP — End-to-End Verification of Calendar & Drive Integration

**Версия документа:** 1.0
**Дата:** 2026-05-28
**Автор:** life-planning-coach team
**Статус:** ✅ **Выполнено 2026-05-26** — Decision: **MCP-first**. См. [mcp_poc_log.md](mcp_poc_log.md).
**RICE:** Reach 70 × Impact 1.5 × Confidence 60% / Effort M=2 EAS, Context Pressure High = **31.5** (Quick Win)

---

## ✅ Outcome Summary (post-execution, 2026-05-26)

| Gate | Status | Result |
|------|--------|--------|
| 0 — Platform audit | ✅ PASSED | Claude Max plan supports Calendar + Drive MCP |
| 1 — OAuth + CRUD | ✅ PASSED | 7/7 ops functional; 6 critical findings |
| 2 — Advanced features | ✅ PASSED | 7/7 ops functional; 13 schema deviations documented |
| 3 — Tasks API | ✅ RESOLVED | Google Tasks NOT in MCP directory → conversational fallback |
| 4 — UX | ✅ PASSED | 4.0/5 avg; persistence ⭐, error handling ⭐ |
| 5 — Domain mapping | ✅ RESOLVED | Bare Claude doesn't apply LPC defaults → skill value validated |
| 6 — Decision | ✅ **MCP-FIRST** | Documented в [mcp_poc_log.md §Gate 6](mcp_poc_log.md#gate-6-decision) |

**Method actually used (vs PRD §14 plan):** AI-assisted hybrid через `Claude_in_Chrome` extension — Chrome Claude (Opus 4.7, "Act without asking") выполнял browser navigation + sent prompts в claude.ai chat, current session (this Claude) orchestrated и filled log. ~3 часа real time vs PRD's 10 hours human-driven estimate.

**Re-audit cadence:** Per NFR-10, re-run каждые 6 месяцев — next check **2026-11-26**.

---

## 1. Обзор и проблема

### 1.1 Контекст

`life-planning-coach` v1.0 **декларирует** интеграцию с Google Calendar и Google Drive через [MCP (Model Context Protocol)](https://modelcontextprotocol.io/):

- `references/calendar_integration.md` — 8 MCP tools (`list_calendars`, `create_event`, `suggest_time`, etc.)
- `references/calendar_constants.md` — COLOR_MAP, REMINDER_PRESETS, RRULE_PRESETS
- `references/module_phase5_execution.md` Mode A: «Calendar Connected (default if available) → Skill создаёт реальные события через connector с подтверждением»
- `references/templates/AI_Instructions.md` §Bootstrap + §Backfill — Drive Wiki через MCP file system

### 1.2 Проблема

**Никто не проверил end-to-end**, что заявленные MCP операции реально работают на целевых платформах.

Конкретные неизвестные:
1. **Платформенная поддержка:** доступен ли Google Calendar MCP в Claude.ai (Free / Pro / Team / Enterprise plans)? В Claude Desktop? Через Claude Code CLI?
2. **OAuth flow:** какие scopes запрашивает Claude.ai при подключении Google Calendar? Какие user steps требуются? Можно ли revoke и переподключить?
3. **CRUD latency и limits:** Сколько событий можно создать за сессию? Rate limits (429 Too Many Requests)? Обработка failures (network, OAuth revoke, permission denied)?
4. **`suggest_time`:** Есть ли в official Google MCP, или только в community connectors? Какой формат запроса/ответа?
5. **Recurring events (RRULE):** Поддерживаются ли в MCP, или нужен fallback на individual events?
6. **Drive integration:** MCP file system access работает ли для пользовательских Drive folders? Что с `wiki_bootstrapped` flow?
7. **Tasks API:** Доступен ли через MCP — для Daily Top-3 synchronization?
8. **Cross-platform parity:** что с Kimi Code CLI (MCP support claimed) vs Claude.ai? Идентичны ли scopes/flows?

### 1.3 Что произойдёт без PoC

- **Risk:** Пользователь следует quick-start, подключает Calendar — flow ломается на первом `create_event` (no MCP support в Free plan / другая ошибка) → confidence в skill падает.
- **Risk:** Skill говорит «создам recurring weekly review» — MCP не поддерживает recurrence → создаются 50 одиночных events → user spam.
- **Risk:** `suggest_time` не работает → free slot algorithm в `module_phase5_execution.md` выдаёт ошибку → пользователь застревает в Mode A не понимая, что fallback на Paper Coach Mode.
- **Risk:** Документация устаревает быстрее чем используется — реальный API меняется в обновлениях Claude.ai, мы не отслеживаем.

### 1.4 Решение

**Proof of Concept** — controlled end-to-end test всех заявленных MCP интеграций на реальных платформах. Выход = **decision document** + обновлённые runtime refs с фактическими scopes/latency/error handling.

---

## 2. Цели и Non-goals

### 2.1 Цели (Goals)

1. **Verify platform coverage:** определить какие plans/clients поддерживают MCP для Calendar и Drive.
2. **Document OAuth contract:** зафиксировать запрашиваемые scopes, user-facing steps, revocation/reconnect flow.
3. **Benchmark CRUD operations:** измерить latency (p50/p95), rate limits, batch limits для каждой операции.
4. **Identify gaps:** выявить функции, которые declared но не работают (или работают иначе).
5. **Update refs:** обновить `calendar_integration.md`, `calendar_constants.md`, `module_phase5_execution.md`, `templates/AI_Instructions.md` фактами.
6. **Decision:** continue с MCP-first / pivot на Paper Coach Mode default / гибрид.

### 2.2 Non-goals (Что в PoC НЕ входит)

- ❌ **Production-grade error recovery** — это уже product feature, не research.
- ❌ **MCP server implementation** — мы тестируем existing Google Calendar MCP server, не пишем свой.
- ❌ **Grok / Kimi OK Computer** — они используют native OAuth (Grok) или text-only (Kimi web), не MCP. Отдельный PoC при необходимости.
- ❌ **Health/wearable MCP** — отдельный PRD `prd_health_metabolism.md` + research `google_health_mcp_integration_research.md`.
- ❌ **Performance optimization** — измеряем baseline, не оптимизируем.
- ❌ **MCP servers Hardening** — out of scope: security review, fuzzing, adversarial testing.

---

## 3. Целевая аудитория PoC

### 3.1 Tester profile

- 1-2 пользователя (или maintainer) с:
  - Claude.ai Free + Pro accounts (для plan comparison)
  - Google Workspace или personal Google account с Calendar + Drive
  - Windows / macOS / Linux test environments
  - Готовность создать test calendar / test Drive folder
  - 4-6 часов на gate execution

### 3.2 PoC user (после реализации)

Пользователь life-planning-coach, который:
- Подключает Google Calendar при первом запуске Phase 5 Execution
- Ожидает что Weekly Review автоматически создаётся в календаре с правильным цветом
- Ожидает что Daily WOOP появится утром как recurring reminder
- Ожидает graceful degradation если что-то не работает

---

## 4. User Stories

### 4.1 PoC Stories (для tester)

**US-PoC-1.** Как tester, я хочу проверить что MCP Calendar доступен в моём текущем plan, чтобы зафиксировать requirement в Quick-start guide.

**US-PoC-2.** Как tester, я хочу пройти полный OAuth flow и documentать scopes/steps, чтобы пользователь knew what permissions он даёт.

**US-PoC-3.** Как tester, я хочу выполнить каждую из 8 MCP operations с realistic данными, чтобы убедиться они работают и измерить latency.

**US-PoC-4.** Как tester, я хочу попытаться вызвать advanced features (recurrence, suggest_time, multi-calendar), чтобы найти gaps между declared и actual.

**US-PoC-5.** Как tester, я хочу симулировать failure scenarios (network drop, OAuth revoke, rate limit), чтобы verify failure modes из `calendar_constants.md` действительно срабатывают.

### 4.2 Downstream Stories (после PoC)

**US-Skill-1.** Как пользователь, я хочу запланировать Weekly Review через skill, и увидеть событие в моём Google Calendar с правильным цветом + reminder.

**US-Skill-2.** Как пользователь, я хочу что skill корректно сказал мне «Google Calendar требует Claude Pro» если я в Free plan — а не падал silent.

**US-Skill-3.** Как пользователь без Drive подключения, я хочу что Phase 5 переключается в Paper Coach Mode без error spam.

---

## 5. Функциональные требования

### 5.1 Verification Coverage

PoC должен покрыть:

#### Connector Discovery
- **FR-1.1** Определить какие MCP servers доступны через Claude.ai Settings → Connectors (Google Calendar, Drive, Tasks, Health).
- **FR-1.2** Зафиксировать UI flow для подключения (screenshots или text describe).

#### OAuth Flow
- **FR-2.1** Запустить OAuth подключение, capture запрашиваемые scopes.
- **FR-2.2** Запросить scopes минимально необходимые (read-only first, then write).
- **FR-2.3** Revoke access в Google Account settings, verify что skill детектирует disconnect.
- **FR-2.4** Reconnect, verify resume.

#### CRUD Operations (Calendar)
Для каждой операции из `calendar_integration.md`:
- **FR-3.1** `list_calendars` — получить список календарей.
- **FR-3.2** `list_events` — query с `calendarId`, `timeMin`, `timeMax`.
- **FR-3.3** `get_event` — read single event by ID.
- **FR-3.4** `create_event` (simple) — title + start + end.
- **FR-3.5** `create_event` (full) — + `colorId`, `reminders`, `description`.
- **FR-3.6** `update_event` — modify title, time, color.
- **FR-3.7** `delete_event`.
- **FR-3.8** Verify event visible в Google Calendar UI (Web/mobile).

#### Advanced Features
- **FR-4.1** `create_event` с `recurrence: ["RRULE:FREQ=WEEKLY;BYDAY=SU"]` — проверить что создаётся recurring series.
- **FR-4.2** `create_event` с `recurrence` для всех 3 RRULE_PRESETS из `calendar_constants.md`.
- **FR-4.3** `suggest_time(duration, timeMin, timeMax)` — если функция существует.
- **FR-4.4** `respond_to_event` — accept/decline invite.
- **FR-4.5** Multi-calendar — `create_event` в non-primary calendar.
- **FR-4.6** Free/busy queries — могут ли заменить `suggest_time` если он отсутствует.

#### Drive Operations
- **FR-5.1** Verify Drive MCP позволяет создать folder structure `Life Planning Coach Wiki/`.
- **FR-5.2** Bootstrap protocol (`templates/AI_Instructions.md §Bootstrap`) — пройти full sequence.
- **FR-5.3** Write to `Hot_Cache.md`, `Goals.md`, `Wheel_of_Life_History.md` через MCP.
- **FR-5.4** Read existing Drive Wiki в новой сессии (persistence).
- **FR-5.5** Verify что MCP write использует UTF-8 (русский контент сохраняется корректно).

#### Tasks API (gate 3, may skip)
- **FR-6.1** Проверить доступность Google Tasks MCP (official или community).
- **FR-6.2** Если доступен — verify create_task / list_tasks для Daily Top-3.
- **FR-6.3** Если нет — подтвердить, что fallback на conversational в `calendar_constants.md §Daily Top-3` корректен.

#### Error Handling
- **FR-7.1** Verify failure mode «Calendar not connected» — error message пользователю.
- **FR-7.2** Симулировать rate limit (создать 10+ events подряд) — обработка 429.
- **FR-7.3** Permission denied (revoke во время сессии) — graceful degradation.
- **FR-7.4** Recurrence not supported (если RRULE failed) — fallback на individual events.
- **FR-7.5** Verify все 5 failure modes из `calendar_constants.md` покрыты.

---

## 6. Test Plan — Gate-by-Gate

PoC проходит через **6 sequential gates**. Каждый gate имеет clear pass/fail criteria. Останавливаемся на первом failed gate с blocker severity и пересматриваем architecture.

### Gate 0: Платформенный аудит (1 час)

**Goal:** Понять surface area MCP support до глубокого тестирования.

| Проверка | Method | Pass criteria |
|---|---|---|
| MCP доступен в claude.ai web (Free plan) | Login → Settings → check Connectors | Google Calendar item present |
| MCP доступен в claude.ai web (Pro plan) | Login Pro → check Connectors | Same или extended set |
| MCP доступен в Claude Desktop | Install → check Settings | Same set or different? |
| MCP доступен в Claude Code CLI | `claude mcp list` | Google Calendar MCP listed |
| Plan requirements | Cross-reference Anthropic docs | Document min plan для MCP |

**Output:** Заполнить `mcp_poc_log.md §Gate 0`. Decision: если Free plan не поддерживает — update README Quick-start.

**Exit criteria:** ≥ 1 платформа поддерживает Google Calendar MCP.

### Gate 1: OAuth & CRUD (1.5 часа)

**Goal:** Verify базовые операции работают и зафиксировать scopes/latency.

**Setup:**
- Создать test Google Calendar `LPC_TEST_CALENDAR`
- Создать test Drive folder `LPC_TEST_WIKI`

**Test sequence:**
1. **OAuth:** Подключить Google Calendar в Claude.ai. Capture экран запроса permissions. Зафиксировать scopes.
2. **list_calendars:** запрос → expect список calendars including `LPC_TEST_CALENDAR`. Measure latency.
3. **create_event** (minimal): create test event 30 min from now → verify в Google Calendar UI.
4. **list_events** для test calendar, timeMin=today, timeMax=today+1 → expect ≥ 1 event.
5. **get_event** by ID → expect full event details.
6. **update_event**: change title → verify в UI.
7. **delete_event** → verify removed from UI.

| Операция | Pass criteria | Latency target |
|---|---|---|
| OAuth flow | Success, scopes documented | ≤ 60s включая user clicks |
| list_calendars | ≥ 1 calendar returned | ≤ 2s |
| create_event | Event appears в UI | ≤ 3s |
| get_event | Event details match input | ≤ 2s |
| update_event | Change visible в UI | ≤ 3s |
| delete_event | Event removed from UI | ≤ 2s |
| list_events | Correct count, sorted by start | ≤ 3s |

**Output:** `mcp_poc_log.md §Gate 1` + screenshots + sample requests/responses.

**Exit criteria:** All 6 CRUD operations работают, latency ≤ 5s p95.

### Gate 2: Advanced Features (1.5 часа)

**Goal:** Проверить features за пределами basic CRUD.

| Фича | Test | Pass criteria |
|---|---|---|
| Recurring (RRULE) | `create_event(recurrence=["RRULE:FREQ=WEEKLY;BYDAY=SU"])` | Series created, 4+ instances visible в UI |
| All 3 RRULE presets | `weekly_sunday`, `daily`, `weekdays` | Each creates correct series |
| `suggest_time` | `suggest_time(duration=60, timeMin=today, timeMax=today+7)` | Returns ≥ 1 available slot |
| Free/busy fallback | `list_events` + manual algorithm если suggest_time нет | Slots calculated correctly |
| Multi-calendar | `create_event(calendarId="secondary")` | Event в правильном календаре |
| Pagination | `list_events` для 30 дней с 50+ events | All events returned (no truncation) |
| `respond_to_event` | Create invite → respond_to_event(accept) | Status changes |
| Reminders | `create_event(reminders=...)` | Reminders configured per spec |
| Color codes | All 11 colors из COLOR_MAP | Visual verification |

**Output:** `mcp_poc_log.md §Gate 2` + matrix фич с pass/fail/N-A.

**Exit criteria:** ≥ 70% advanced features работают. `suggest_time` либо работает либо есть viable fallback.

### Gate 3: Tasks API (30 минут — может skip)

**Goal:** Решить — использовать ли Tasks API для Daily Top-3.

| Проверка | Pass criteria |
|---|---|
| Tasks MCP в official set | Yes/No |
| Community Tasks MCP available | Yes/No |
| Если yes — basic CRUD | create_task, list_tasks работают |

**Output:** `mcp_poc_log.md §Gate 3`.

**Exit criteria:** Decision: использовать Tasks MCP / оставить Daily Top-3 conversational.

### Gate 4: UX (1 час)

**Goal:** Сравнить user-facing flow MCP vs hypothetical Python-only module.

| Метрика | MCP | Python module (hypothetical) |
|---|---|---|
| Time-to-setup (first user) | Measure | Hypothetical: setup.py install + OAuth |
| Onboarding сложность | 1-5 scale + qualitative | — |
| Graceful degradation | Test 3 failure modes | — |
| Persistence между сессиями | Verify через 2-3 сессии | — |
| Cross-platform parity | Claude.ai web vs Desktop vs CLI | — |

**Output:** `mcp_poc_log.md §Gate 4`.

**Exit criteria:** UX MCP comparable или better than Python alternative.

### Gate 5: Domain Logic Mapping (30 минут)

**Goal:** Verify что operational concepts skill (Daily Top-3, WOOP, Weekly Review, Habit Loop) корректно маппятся в MCP вызовы.

| Domain concept | MCP вызов | Notes |
|---|---|---|
| Weekly Review reminder | `create_event` recurring | colorId=5, weekly_review preset |
| Daily WOOP morning prompt | `create_event` recurring daily | colorId=7, woop preset |
| Time Block (Deep Work) | `create_event` single | colorId=2, deep_work preset |
| Milestone | `create_event` single + reminders 24h+1h | colorId=11 |
| Habit micro-event | `create_event` recurring daily | habit_loop preset |
| BHAG annual reminder | `create_event` yearly | — |

**Output:** Confirm все 6+ patterns создают correct events. Update `calendar_integration.md §Prompt Patterns` if needed.

**Exit criteria:** All domain → MCP mappings работают.

### Gate 6: Decision (30 минут)

**Goal:** Зафиксировать решение и план обновления refs.

Решение **MCP-first / Paper-first / Hybrid**:

| Outcome | Trigger | Action |
|---|---|---|
| **MCP-first** | Gates 1-2 ≥ 90% pass, UX good | Mode A остаётся default в Phase 5. Update refs с фактами. |
| **Paper-first с MCP opt-in** | Gates 1-2 ~70-90% pass | Default → Paper Coach Mode. MCP — opt-in для advanced users. |
| **Hybrid** | Gate 2 < 70% (advanced features broken) | Mode A для basic CRUD; Mode B (Paper) для advanced. |
| **Drop MCP** | Gate 0/1 fail полностью | Удалить calendar_integration.md, переписать Phase 5 на Paper Coach only. |

**Output:** `mcp_poc_log.md §Gate 6 Decision` + PR обновляющий runtime refs.

---

## 7. Acceptance Criteria (P0)

PoC считается **завершённым** когда:

- ✅ Все 6 gates пройдены (или explicit skip с rationale)
- ✅ `docs/research/mcp_poc_log.md` заполнен полностью (все ⏳ → ✅/❌/N-A)
- ✅ Принято explicit decision из 4 опций (Gate 6)
- ✅ Если decision = MCP-first/Hybrid: `references/calendar_integration.md` обновлён с:
  - Зафиксированными OAuth scopes
  - Latency benchmarks (p50/p95)
  - Confirmed working MCP tools (vs declared)
  - Updated failure modes если реальные отличаются от документированных
- ✅ Если decision = Paper-first/Drop MCP: `references/module_phase5_execution.md` Mode A/B порядок изменён
- ✅ README Quick-start обновлён с plan requirements (если Pro/Team нужен для MCP)
- ✅ Updates committed в repo с commit message `feat: mcp poc results (decision: X)`

---

## 8. Метрики успеха

### 8.1 Quantitative

| Метрика | Target | Measurement |
|---|---|---|
| MCP CRUD success rate | ≥ 95% | (passed ops / total ops) × 100 |
| OAuth flow completion | 100% | Setup completed без manual workarounds |
| Latency p95 | ≤ 5s per operation | Measured during Gate 1 |
| Documented gaps | All identified | Compare declared (refs) vs actual |
| Refs update accuracy | 100% | All MCP claims в refs либо verified либо removed |

### 8.2 Qualitative

- Maintainer (или tester) уверен в Mode A claim в Phase 5
- README quick-start не вводит пользователя в заблуждение (правильные plan requirements)
- Failure modes в calendar_constants.md покрывают реальные observed errors

---

## 9. Нефункциональные требования

### 9.1 Privacy & Security

- **NFR-1** PoC использует test account (не personal data). После tests — revoke OAuth access.
- **NFR-2** No credentials в commit history. `.env` или env variables only.
- **NFR-3** Test events не должны содержать PII (real names, addresses).
- **NFR-4** Drive PoC использует isolated folder, не пересекается с real user data.

### 9.2 Reproducibility

- **NFR-5** PoC steps must be runnable повторно (idempotent): re-running на новом test account даёт same results.
- **NFR-6** Все captured screenshots в `docs/research/screenshots/mcp_poc/` (если используются).
- **NFR-7** Sample MCP requests/responses сохранены как JSON для regression reference.

### 9.3 Documentation

- **NFR-8** Каждый Gate имеет structured Markdown в `mcp_poc_log.md` (consistent with template).
- **NFR-9** Любой maintainer может прочитать PoC log и понять что было проверено + результат за 10 минут.
- **NFR-10** Update history: при изменении MCP API через 6+ месяцев — re-run PoC и update log с new date.

---

## 10. Зависимости

### 10.1 External

- **Google account** с Calendar + Drive access (test или dedicated PoC account)
- **Claude.ai account** (Free + Pro для plan comparison) — может требоваться $20/мес × 1 месяц для Pro
- **Claude Desktop** (optional, для Gate 0)
- **Anthropic API key** (optional, если хотим программно тестировать через Claude API)

### 10.2 Internal

- `references/calendar_integration.md` — source of declared MCP tools
- `references/calendar_constants.md` — COLOR_MAP / REMINDER_PRESETS / RRULE_PRESETS
- `references/module_phase5_execution.md` — Mode A/B definitions
- `references/templates/AI_Instructions.md` — Bootstrap/Backfill protocols
- `docs/research/mcp_poc_log.md` — empty template для заполнения
- `docs/research/google_health_mcp_integration_research.md` — adjacent research (Health MCP)

---

## 11. Риски

| Risk | Severity | Mitigation |
|---|---|---|
| MCP Calendar не доступен в Free plan → many users blocked | High | Document explicitly в README; Mode B (Paper Coach) — robust default |
| `suggest_time` отсутствует → free slot algorithm в Phase 5 broken | Medium | Fallback на manual free/busy через `list_events` + Python algorithm |
| MCP API меняется без notice → existing tests/refs обsolete | Medium | NFR-10 — re-run PoC каждые 6 месяцев; subscribe Anthropic changelog |
| Tester использует personal account → privacy concern | High | NFR-1 — only test accounts; explicit list of test data |
| Rate limits в MCP server ниже expected → batch creation breaks | Medium | Gate 2 measure rate limits explicitly; implement exponential backoff в skill |
| Drive integration требует другой OAuth flow than Calendar | Medium | Gate 1 separate Drive sub-tests; document oddities |
| Грtenz: разные результаты на different OS (Win/Mac/Linux) | Low | Multi-platform testing в Gate 0 |
| Drive write requires user confirm каждый раз → batch impossible | Low | Если так — pivot batch-writes на end-of-session prompt |

---

## 12. Open Questions

Эти вопросы остаются для discussion ДО старта PoC:

- **OQ-1** Использовать ли личный Google account maintainer'а, или создавать dedicated test account? (Privacy vs setup cost.)
- **OQ-2** Тестировать ли все 4 platforms (claude/grok/kimi/kimi-cli) или только Claude.ai (где MCP first-class)?
- **OQ-3** Включать ли в PoC любые Slack / Notion / Asana MCP integrations, или только Google ecosystem?
- **OQ-4** Если Gate 1 fails — стоит ли continue с Gate 2 advanced features? (Думаем что нет, экономия времени.)
- **OQ-5** Если decision = Drop MCP — что делать с уже написанными `calendar_integration.md`, `calendar_constants.md`? Архивировать в `docs/archive/`?
- **OQ-6** Кого считать «tester»? Maintainer (Андрей)? Один из early adopters? Или external paid tester?
- **OQ-7** Какие failure modes из `calendar_constants.md` обязательно тестировать (FR-7.5)? Все 5 или selective?

---

## 13. Артефакты (Deliverables)

После завершения PoC:

### 13.1 Updated documents

- `docs/research/mcp_poc_log.md` — заполненный лог (6 gates × структурированные таблицы)
- `references/calendar_integration.md` — обновлённые scopes, latency numbers, confirmed tools
- `references/calendar_constants.md` — обновлённые failure modes (если differs)
- `references/module_phase5_execution.md` — Mode A/B порядок если decision требует
- `references/templates/AI_Instructions.md` — обновлённые Bootstrap/Backfill steps (если Drive PoC требует)
- `README.md` — plan requirements в Quick-start (если Pro plan нужен)
- `CHANGELOG.md` — секция «PoC MCP completed» в Unreleased или next minor
- `BACKLOG.md` — переместить PoC MCP item в Archived/Done

### 13.2 New documents (optional)

- `docs/research/screenshots/mcp_poc/` — visual evidence для Gates 0-2 (если screenshots)
- `docs/research/mcp_poc_decision_summary.md` — 1-page summary решения для future contributors

### 13.3 Code changes (если applicable)

- Updated `module_phase5_execution.md` если Mode A/B порядок changed
- New helper в `scripts/` если нужен programmatic free slot algorithm (fallback для отсутствующего suggest_time)
- New tests в `tests/system/test_mcp_integration.py` если PoC создаёт smoke tests для MCP claims

---

## 14. Schedule & Phases

PoC = **~2 EAS = 10-15 рабочих часов** распределённых:

| Phase | Duration | Owner | Output |
|---|---|---|---|
| **Pre-PoC setup** | 1 час | Maintainer | Test accounts, environments ready |
| **Gate 0** | 1 час | Tester | Platform audit complete |
| **Gate 1** | 1.5 часа | Tester | CRUD verified |
| **Gate 2** | 1.5 часа | Tester | Advanced features mapped |
| **Gate 3** | 30 мин | Tester | Tasks decision |
| **Gate 4** | 1 час | Tester | UX comparison |
| **Gate 5** | 30 мин | Tester | Domain mapping verified |
| **Gate 6** | 30 мин | Maintainer | Decision document |
| **Refs update PR** | 2 часа | Maintainer | All artifacts updated |
| **Total** | **~10 часов** | — | — |

---

## 15. Definition of Done

PoC считается **done** когда:

1. ✅ Все 6 gates имеют статус ✅/❌/N-A (нет ⏳ в `mcp_poc_log.md`)
2. ✅ Explicit decision (Gate 6) committed в repo
3. ✅ Все referenced docs обновлены под decision (Section 13.1)
4. ✅ BACKLOG.md item PoC MCP перенесён в Archived/Done
5. ✅ Если MCP-first decision: smoke test `tests/system/test_mcp_integration.py` создан и passes на CI (или explicitly skipped с reason)
6. ✅ README plan requirements consistent с reality
7. ✅ Maintainer signs off: «Skill теперь честно описывает MCP integration capabilities»

---

## 16. Связанные документы

- [BACKLOG.md](../../BACKLOG.md) — research debt entry для PoC MCP (RICE 31.5)
- [ROADMAP.md](../../ROADMAP.md) — post-v1.0 trajectory
- [references/calendar_integration.md](../../references/calendar_integration.md) — MCP tools declared в runtime
- [references/calendar_constants.md](../../references/calendar_constants.md) — COLOR_MAP, presets, failure modes
- [references/module_phase5_execution.md](../../references/module_phase5_execution.md) — Mode A/B definitions
- [docs/research/mcp_poc_log.md](mcp_poc_log.md) — empty template для заполнения
- [docs/research/google_health_mcp_integration_research.md](google_health_mcp_integration_research.md) — adjacent (Health MCP research)
- [MCP Protocol Spec](https://modelcontextprotocol.io/) — внешняя ссылка

---

## Подпись

- **Подготовлен:** life-planning-coach team, 2026-05-28
- **Pending:** owner assignment, scheduling, OQ-1..7 resolution

---

*Документ готов к использованию. Перед стартом PoC — провести discussion на OQ-1..7 и зафиксировать owner.*
