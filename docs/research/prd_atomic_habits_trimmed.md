# PRD (trimmed): Atomic Habits — точечное усиление, без пивота идентичности

**Версия:** 2.0 (trimmed) · **Дата:** 2026-06-03 · **Статус:** 📋 Candidate — gated к v1.5.0
**Заменяет:** `life-planning-coach_Prd_Atomic_Habits_Extension.md` v1.0 (8 фич, отклонён по итогам аудита кодовой базы)
**Источник усечения:** independent review 2026-06-03 — fact-check предпосылок против `references/`

---

## 1. Почему trimmed (1 абзац)

Исходный PRD (8 фич, «пивот goal-coaching → identity-coaching») **переоценивает пробел**: ~⅔ предложенного уже в продукте, причём на **более сильных первоисточниках**, чем Клир. `habit_loop.md §3.2` уже содержит identity-voting Клира дословно; `authentic_goal_filter.md` уже работает на уровне аутентичного «я» через Self-Concordance (Sheldon & Elliot 1999); 2-min rule, friction, celebration, habit stacking, нелинейная кривая Lally — всё на месте; Clear (2018) уже цитируется в `evidence_map.md:82`. При этом проект **оценивает качество доказательств** (`science_backing.md:15` — grit помечен `LOW/CONTESTED`), поэтому долив поп-науки Клира (метафоры «1.01³⁶⁵=37.8×», «кубик льда / плато скрытого потенциала») **снижает** evidence-positioning, а не усиливает. Чистой новой ценности ≈ **1 модуль + набор reframing-prompts**.

---

## 2. Что УЖЕ покрыто → НЕ делаем

| Исходная фича | Уже в репозитории | Решение |
|---|---|---|
| F2 Identity Architecture | `habit_loop.md §3.2` (голосование за идентичность, Clear) + `authentic_goal_filter.md` (Self-Concordance, «чей голос?») | ❌ Cut — есть, глубже, на primary-источнике |
| F1 4 Laws (как контент) | Тактики под Fogg (B=MAP), Wood (friction/context), Duhigg (loop), Clear (stacking) + `implementation_intentions.md`, `environment_design.md`, `reward_audit.md` | ❌ Cut как модуль (опц. coach-индекс — см. §7) |
| F4 Plateau of Latent Potential (как модуль) | `habit_loop.md §5` — реальная кривая Lally (66 дн, 18–254, «миф 21 дня») + `recovery_protocol.md` «пропуск = данные» | ⚠️ Reframe (см. RP), не строить |
| F5 Goldilocks selector | Fogg B=MAP (Ability) + Tiny Habits «чувствуешь сопротивление — уменьши вдвое» (`habit_loop §1.1`) | ❌ Cut — избыточно |
| F8 Personality-aligned design | Big Five в `communication_style.md` (калибровка коммуникации) | ❌ Cut — слабая доказательность matching личность→дизайн привычки; против evidence-дисциплины |
| F6 Enhanced reflection | Weekly Review + AAR (Gap Analysis + Lessons, schema v2.2.4) + readiness gates | ⏸️ Defer — риск перекрыть AAR/AGF; пересмотреть по сигналу |

---

## 3. Scope (IN) — 1 модуль + reframing-prompts

### M1 — Bad Habit Inversion Toolkit (новый Tier-3 модуль)

**Файл:** `references/bad_habit_inversion.md` (Tier 3, lazy-load, бюджет ≤ 2.5K токенов).

**Реальный пробел:** работа с *вредными* привычками сейчас — один абзац (`habit_loop.md §2` Golden Rule: cue+reward оставить, routine заменить, Duhigg). Структурированного flow нет, хотя значимая доля запросов — именно «бросить X».

**Содержание (заземлено на primary, не только на инверсии Клира):**
- Инверсия 4 законов как мнемоника flow: **незаметным** (убрать cue — Wood: context-cue removal), **непривлекательным** (reframe reward, reward_audit), **сложным** (повысить friction — Wood), **неудовлетворяющим** (immediate cost / accountability).
- Интеграция, а не дубль: расширяет `habit_loop.md §2` Golden Rule + ссылается на `environment_design.md` (friction) и `recovery_protocol.md` (срыв = данные).
- Accountability (habit contract / партнёр) — **опционально**, с явной privacy-оговоркой (consent, как в SKILL.master §Safety).
- Routing: добавить строку в Routing Map SKILL.master + `module_phase5_execution.md` («бросить привычку» → этот ref).
- Guardrails: НЕ для зависимостей/клиники (→ safety-эскалация), honor autonomy.

**State:** без изменений схемы (переиспользует `habits[]` / recovery). **Тесты:** pattern `test_methodology_v1_*` (presence + routing + token budget). **Платформы:** rebuild (deep-ref, в master не инлайнится).

### RP — Reframing-prompts (БЕЗ нового модуля — правки существующих файлов)

**RP-a — Нормализация нелинейности** (`habit_loop.md §5` поверх Lally + Phase 3 Weekly Review):
- 2–3 prompt'а: «прогресс копится в системе, даже если видимого результата пока нет — кривая Lally: автоматизм 18–254 дня». Заземление на **данных Lally**, без метафоры «кубика льда».
- Цель: перехватить срыв в первые 3–6 недель «нет результата».

**RP-b — Systems / consistency mindset** (1 prompt, опционально):
- Reframe «фокус на улучшении системы, не только на цели; маленькие действия складываются». **Без** «1.01³⁶⁵ = 37.8×» (метафора, не данные) — заземлить на consistency/behavioral momentum.
- Самый низкоприоритетный; включать только если бесплатно в рамках RP-a.

---

## 4. RICE (по конвенции `BACKLOG.md`)

> RICE = (Reach × Impact × Confidence) / Effort · Reach 0–100% · Impact 0.25→3.0 · Conf 0–100% · Effort = EAS + Context Pressure

| Item | Reach | Impact | Conf | Effort (EAS) | RICE | Категория |
|---|---|---|---|---|---|---|
| **RP — Reframing-prompts** (a+b) | 50 | 0.75 | 60% | 1.0 (Low) | **22.5** | High Priority |
| **M1 — Bad Habit Inversion** | 45 | 1.0 | 65% | 2.0 (Medium) | **14.6** | High Priority |
| ~~RP-b отдельно (compounding)~~ | 40 | 0.4 | 40% | 0.5 (Low) | 12.8 | Medium (только в связке с RP-a) |

**Порядок исполнения по RICE:** сначала RP (дёшево, широкий reach, на существующих данных), затем M1 (новый модуль). Совокупный Effort ≈ **3 EAS**, Context Pressure Medium.

---

## 5. Привязка к гейту v1.5.0

Статус — **Candidate**, НЕ committed. По правилу ROADMAP: *revisit after 30d usage signal, ≥ 2026-06-27*. Перед переносом в committed scope пройти gate-вопросы:

- [ ] **M1:** есть ≥ 2 сигнала (user feedback / session-транскрипты), где запрос «бросить вредную привычку» и текущий Golden Rule (`habit_loop §2`) оказался недостаточен?
- [ ] **RP-a:** есть сигнал, что пользователи бросают привычки в первые 3–6 недель из-за «нет видимого результата», и Lally-таймлайн (`§5`) это не перехватывает?
- [ ] **Бюджет:** cold-load остаётся в норме (master ≤ 4K; новый ref ≤ 2.5K) — проверить перед commit.
- [ ] **Evidence:** новый контент сохраняет primary-grounding (Wood/Duhigg/Lally), инверсия Клира помечена как mnemonic-framing, не как доказательство.

Если ни один сигнал не подтверждён к 2026-06-27 — остаётся в BACKLOG, не блокирует релизы.

---

## 6. Success signal (качественный — телеметрии нет)

Скилл stateless / prompt-based, persistence opt-in, **аналитики нет** → метрики вида «снижение начал→бросил» / «рост удовлетворённости» из v1.0 PRD **неизмеримы**. Вместо них — качественные сигналы:
- В session-транскриптах при запросе «бросить X» коуч выдаёт структурированный inversion-flow (а не разовый Golden Rule).
- Тесты `test_methodology_*` фиксируют presence + routing + бюджет (объективно проверяемо).
- Обратная связь: меньше «не вижу прогресса → бросаю» в первые недели (qualitative, через feedback issues).

---

## 7. Риски и границы

- **Therapy-boundary:** trimmed-версия СНИМАЕТ главный риск v1.0 — НЕ делает «пивот в трансформацию идентичности». Identity-работа остаётся на текущем безопасном уровне (AGF/Self-Concordance + habit_loop §3.2).
- **Token budget:** 1 модуль вместо 8 — дисциплина cold-load сохранена.
- **Evidence dilution:** инверсия и reframing заземлены на Wood/Duhigg/Lally; поп-метафоры Клира («37.8×», «кубик льда») исключены.
- **Опционально (не в scope):** F1 «4 закона» — только как coach-facing *индекс-мнемоника* (1 экран поверх существующих тактик), если возникнет сигнал о несистемности рекомендаций; не контент-модуль.

---

## 8. Audit trail: судьба 8 фич v1.0

| F | Фича v1.0 | Решение |
|---|---|---|
| 1 | 4 Laws framework | Cut как модуль (опц. индекс — §7) |
| 2 | Identity Architecture | Cut — уже есть (habit_loop §3.2 + AGF) |
| 3 | Compounding / 1% | → RP-b (только grounded часть, без «37.8×») |
| 4 | Plateau of Latent Potential | → RP-a (reframe поверх Lally) |
| 5 | Goldilocks selector | Cut — избыточно (Fogg/Tiny Habits) |
| 6 | Enhanced reflection | Defer — риск перекрыть AAR |
| 7 | **Bad Habits Inversion** | **→ M1 (единственный новый модуль)** |
| 8 | Personality-aligned design | Cut — слабая доказательность |

---

*Trimmed PRD. Реализация — только после прохождения гейта v1.5.0 (§5). RICE и приоритеты — §4.*
