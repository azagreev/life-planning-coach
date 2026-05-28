# Evidence Map — Доказательная база методов LPC skill

> **Tier:** 3 (lazy-load reference)
> **Загружается:** когда user спрашивает «на чём основано», «есть ли research», «откуда это», или при объяснении skill rationale.
> **Цель:** прозрачность evidence base. Не sales pitch, а honest assessment.

---

## Принцип честной оценки

Согласно PRD v0.15 core principle: **«Приоритет доказанной эффективности над популярностью инструментов. Честная оценка силы доказательной базы каждого метода.»**

Уровни доказательности:

| Уровень | Что означает |
|---------|--------------|
| 🟢 Очень высокий | Multiple meta-analyses, large samples, replicated. Effect size documented |
| 🔵 Высокий | Meta-analysis OR multiple RCTs, consistent results |
| 🟡 Средний (academic) | RCTs available, but fewer/smaller; or systematic review without meta-analysis |
| 🟠 Средний (practical) | Strong practical track record, fewer academic RCTs |
| 🔴 Слабый-средний | Growing clinical/practical base, limited rigorous studies |

---

## Goal-setting и planning

### WOOP (Wish-Outcome-Obstacle-Plan)

> **Evidence:** 🔵 Высокий
> **Sources:**
> - Wang, G. et al. (2021). A Meta-Analysis of Mental Contrasting With Implementation Intentions on Goal Attainment. *Frontiers in Psychology*. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8149892/) — g=0.336
> - Cross, A. & Sheffield, D. (2019). Mental Contrasting for Health Behaviour Change: A Systematic Review and Meta-analysis.
>
> **Used in:** `goal_architecture.md` §Layer 5, Phase 2 Goal Definition, daily morning template.

### Implementation Intentions (If-Then planning)

> **Evidence:** 🟢 Очень высокий — **d = 0.65** (medium-large effect)
> **Source:** Gollwitzer, P. M., & Sheeran, P. (2006). Implementation intentions and goal achievement: A meta-analysis of effects and processes. *Psychological Bulletin*, 119(2), 38–69.
> **Sample:** 94 independent studies, 8000+ participants.
>
> **Used in:** `implementation_intentions.md` (full deep ref), Phase 5 Execution, Calendar prompts (WHEN-type events), Habit Loop §1.2 anchor pattern.

### OKR (Objectives + Key Results)

> **Evidence:** 🟠 Средний (practical). Pioneered Intel (Grove 1970s), popularised Google. Limited academic RCTs.
> **Used in:** `goal_architecture.md` Layer 3, Phase 2.

### Premortem

> **Evidence:** 🟡 Средний (academic). Theoretical base: cognitive bias literature on outcome reasoning + prospective hindsight (Mitchell, Russo & Pennington 1989).
> **Source:** Klein, G. (2007). Performing a Project Premortem. *Harvard Business Review*. [Article](https://hbr.org/2007/09/performing-a-project-premortem)
>
> **Used in:** `premortem.md` (full deep ref), Phase 2 trigger для важных OKR (`confidence_score ≤ 6` / horizon ≥ 1y / `partner_coordination` block / explicit request / mid-quarter stagnation). Mitigation pipeline через `implementation_intentions.md` §Coping plans (top-3 risks → if-then plans). State persistence: `goals.premortem_assessments[]` (schema v2.2.3+).

---

## Habits и поведение

### Tiny Habits (B=MAP)

> **Evidence:** 🟠 Средний (practical strong). Fewer academic meta-analyses than Implementation Intentions.
> **Sources:**
> - Fogg, BJ (2019). Tiny Habits: The Small Changes That Change Everything.
> - Fogg Behavior Model: B = MAP (Behavior = Motivation × Ability × Prompt)
>
> **Used in:** `habit_loop.md` §1 (primary for new habit creation), Phase 5 Execution.

### Cue-Routine-Reward (Classical Habit Loop)

> **Evidence:** 🔵 Высокий. Neurological basis well-established.
> **Sources:**
> - Duhigg, C. (2012). The Power of Habit.
> - Wood, W. & Neal, D. T. (2007). A new look at habits and the habit-goal interface. *Psychological Review*.
> - Wood, W., Quinn, J. M., & Kashy, D. A. (2002). Habits в everyday life: 43% поведения автоматическое.
>
> **Used in:** `habit_loop.md` §2 (diagnostic для existing habits).

### Habit Stacking (anchor habits)

> **Evidence:** 🟠 Средний (practical) — 64% higher adoption с anchor habits.
> **Source:** Clear, J. (2018). Atomic Habits.
> **Used in:** `habit_loop.md` §3, `habit_stack_builder.md`.

### Habit Timeline (66 days median)

> **Evidence:** 🔵 Высокий.
> **Source:** Lally, P., et al. (2010). How are habits formed: Modelling habit formation in the real world. *European Journal of Social Psychology*.
> **Sample:** 96 participants, real-world habit tracking.
> **Used in:** `habit_loop.md` §5; corrects 21-day myth.

### Environment Design (friction asymmetry, cue design, choice architecture)

> **Evidence:** 🔵 Высокий. Combines Lally habit-context research, Fogg B=MAP Prompt component, Thaler & Sunstein nudge theory, Wood et al. context-dependent automaticity.
> **Sources:** Lally 2010 (habits need stable context); Fogg 2019 (Prompt = environmental trigger в B=MAP); Thaler & Sunstein 2008 (*Nudge* — default switching, choice architecture); Wood, Quinn & Kashy 2002 (43% поведения автоматическое в стабильном контексте).
> **Used in:** `environment_design.md` (full deep ref, NEW в v1.2); primary intervention для COM-B Opportunity gap; secondary в `habit_loop.md` §1.2 anchor pattern.

---

## Diagnostics и self-regulation

### COM-B Model (Capability + Opportunity + Motivation → Behavior)

> **Evidence:** 🔵 Высокий. Foundational для UK Behaviour Change Wheel.
> **Source:** Michie, S., van Stralen, M. M., & West, R. (2011). The behaviour change wheel: A new method for characterising and designing behaviour change interventions. *Implementation Science*, 6(42). [Source](https://doi.org/10.1186/1748-5908-6-42)
>
> **Used in:** `com_b_diagnostic.md` (full deep ref), Phase 0 / Phase 1 opt-in diagnostic, Phase 3 Weekly Review escalation. Routing к targeted interventions: Capability → `habit_loop.md` §1 Tiny Habits + `action_breakdown_template.md`; Opportunity → `environment_design.md`; Motivation → `module_phase2_goal_architecture.md` §Layer 5 WOOP + `module_phase1_5_goal_filter.md` Compass Mode.

### After Action Review — Runtime pattern (v1.3.0)

> **Source:** US Army TC 25-20 (1993) — original AAR doctrine.
> **Used in:** `module_phase3_weekly_review.md` Step 9 Lessons Learned (v1.3.0). Pattern matching через skill-instruction (NOT Python algorithm): при write нового lesson skill loads last 4 weekly_reviews, оценивает semantic similarity (same `category` + общая тема) с previous lessons, increments `sighted_count` существующего OR appends new с `sighted_count: 1`. Surface threshold `sighted_count ≥ 3` → quarterly OKR / Habits / Environment adjustment via Phase 2 или Phase 1.5. Schema 2.2.4+, см. `state_v2_schema.md` §3.5.2.

### Wheel of Life (life balance assessment)

> **Evidence:** 🟠 Средний (practical). Coaching tool с decades of use. No strong academic RCTs.
> **Source:** [The Wheel of Life as a Coaching Tool to Audit Life Priorities (2022)](https://www.researchgate.net/publication/365375169_The_Wheel_of_Life_as_a_Coaching_Tool_to_Audit_Life_Priorities) — улучшение self-insight, motivation, habit-change support.
> **Used in:** Phase 1 diagnostic (`module_phase1_diagnostic.md` § WoL Frequency Gate), frequency-gated к 1×/30 days (PRD v0.15 §5). State: `diagnosis.wheel_of_life.last_assessed_at` (schema 2.2.5+, v1.3.0).

### WoL Health Sub-segments (multidimensional wellness, v1.4.0)

> **Evidence:** 🟠 Средний (practical). Multi-dimensional wellness self-assessment повышает targeted change effectiveness vs single-score.
> **Source:** Schultchen et al. (2019) — bidirectional relationship of stress and physical activity (subjective stress/energy/recovery scores correlate с adherence behavior).
> **Used in:** Phase 1 diagnostic при `health` ≤ 6 ИЛИ explicit interest (`module_phase1_diagnostic.md` + `wol_health_subsegments.md`). State: `diagnosis.wheel_of_life.current.health_subsegments` (6-segment object, schema 2.2.6+, v1.4.0 Sub-feature A). Не дублирует `track_health_metabolism.md` (v0.19.0 deep 7-рычаговый трек) — это light pre-screening (≤ 6 вопросов).

### Schwartz Values Theory

> **Evidence:** 🟢 Очень высокий. Cross-cultural validation.
> **Source:** Schwartz, S. H. (1992). Universals в the content and structure of values. *Advances в Experimental Social Psychology*.
> **Used in:** `authentic_goal_filter.md`, Phase 1.5 values discovery, Compass Mode.

### Adaptive Communication (Big Five × TTM × Motivational Interviewing)

> **Evidence:**
> - Big Five — 🟢 (DeYoung et al. 2007, many meta-analyses)
> - TTM (stages of change) — 🔵 (Prochaska & DiClemente 1983)
> - Motivational Interviewing — 🟢 (Miller & Rollnick, Hettema et al. 2005 meta-analysis)
>
> **Used in:** `communication_style.md`.

---

## Эмоциональная регуляция

### DBT-informed techniques

> **Evidence:** 🔵 Высокий для DBT (Linehan et al. multiple RCTs для BPD).
> **LPC применяет:** Cognitive Reappraisal, Grounding, Self-Compassion (Neff), Conflict Reappraisal (Gottman).
> **Used in:** `emotion_regulation.md`, Phase 0.5.

### Self-Compassion

> **Evidence:** 🟢 Очень высокий.
> **Source:** Neff, K. D. (2003). The development and validation of a scale to measure self-compassion. *Self and Identity*.
> **Used in:** `emotion_regulation.md`.

---

## Retrospective и review

### Weekly Review (GTD-derived)

> **Evidence:** 🟠 Средний (practical). David Allen GTD methodology.
> **Source:** Allen, D. (2001). Getting Things Done.
> **Used in:** `module_phase3_weekly_review.md`.

### Scrum Retrospective (continuous improvement)

> **Evidence:** 🟠 Средний (practical, software engineering origin).
> **Sources:** Sutherland & Schwaber (1995) Scrum guide; Derby & Larsen (2006) Agile Retrospectives.
> **Used in:** `module_phase3_weekly_review.md`.

### After Action Review (AAR)

> **Evidence:** 🟠 Средний (practical strong). US Army developed, decades of organizational use.
> **Sources:** US Army TC 25-20 (1993); Garvin, D. (2000). *Learning in Action: A Guide to Putting the Learning Organization to Work*. Harvard Business School Press.
>
> **Used in:** `module_phase3_weekly_review.md` шаги 8–9 (Lean AAR integration: 7-step → 9-step). Step 8 Gap Analysis (Three Whys + категория internal/external/both, повтор ≥ 2 недели → COM-B escalation). Step 9 Lessons Learned (`sighted_count ≥ 3` → quarterly systemic adjustment). Skip при `execution_score ≥ 70%`. ADHD/elder persona opt-out. State: `weekly_reviews[].gap_analysis[]` + `lessons_learned[]` (schema v2.2.4+).

---

## Health и body

### Sleep, stress, protein, fiber — metabolism levers

> **Evidence:** 🔵-🟢 Высокий для main 4 (sleep, stress, protein, fiber).
> **Sources:** см. `track_health_metabolism.md` для full citations (Walker, Sapolsky, Layman, multiple nutrition meta-analyses).

### Chewing, chlorogenic acid

> **Evidence:** 🟡 Средний-слабый.
> **Note:** Honest disclosure в `track_health_metabolism.md`.

---

## Goal Concordance (партнёрство)

### Transactive Goal Dynamics

> **Evidence:** 🔵 Высокий.
> **Source:** Fitzsimons, G. M., Finkel, E. J., & vanDellen, M. R. (2015). Transactive Goal Dynamics. *Psychological Review*.
> **Used in:** Phase 1.5/2/ER partner_coordination block.

### Gottman Couples Research

> **Evidence:** 🟢 Очень высокий (longitudinal, 40+ years).
> **Source:** Gottman, J. M. (1994+). Multiple books и papers.
> **Used in:** `emotion_regulation.md` conflict reappraisal.

---

## Calendar и time management

### Implementation Intentions via Calendar

> **Evidence:** 🟢 (via Gollwitzer 2006).
> **Used in:** Calendar events as WHEN-type triggers.

### Time-blocking (deep work)

> **Evidence:** 🟠 Средний (practical strong).
> **Sources:** Newport, C. (2016) Deep Work; Csikszentmihalyi flow research (🔵).
> **Used in:** `module_phase5_execution.md`.

### Chronotype-aware scheduling

> **Evidence:** 🔵 Высокий. Roenneberg et al. multiple studies on chronotype distribution.
> **Used in:** `chronotype_native_planning.md`.

---

## Когда **не** утверждать что "research-backed"

Skill следует honest framing:
- **Parts Work (IFS)** — 🔴 (clinical growing, RCT base тонкая). НЕ говорить "proven".
- **Body doubling** — 🟠 (anecdotal strong, formal research thin).
- **Wheel of Life** — 🟠 (decades of coaching use, no strong RCTs).

Для этих методов skill говорит «practice показывает» или «coaches используют» — не «research shows».

---

## Cross-references

- `implementation_intentions.md` — deep dive on strongest single method
- `habit_loop.md` — habits framework hierarchy
- `goal_architecture.md` — BHAG → OKR → WOOP hierarchy
- `track_health_metabolism.md` — health levers с individual evidence calls
- PRD v0.15 в `docs/research/prd_v0.15_methodology_upgrade.md` — full methodology rationale

---

## Update cadence

Re-audit evidence base каждые 12 месяцев. Новые meta-analyses или significant studies могут update уровни. Next review: 2027-05.
