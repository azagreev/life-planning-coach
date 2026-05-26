# Composite Readiness Model — Objective + Subjective Recovery for Life Planning Coach

> **Research synthesis:** How Polar, Garmin, and sports science combine objective biometrics with subjective self-assessment for adaptive planning.
>
> **Date:** 2026-05-20
> **Sources:** Polar official docs, Garmin/Firstbeat white papers, peer-reviewed sports science (Foster, Saw, Kiviniemi, Plews)
> **Status:** Ready for implementation in v0.15.0+

---

## 1. Executive Summary

**The problem:** Consumer wearables (Garmin, Fitbit, Oura) provide objective recovery scores, but these correlate poorly with how the user actually feels (r = 0.21–0.58). A runner with "perfect" HRV may feel wrecked after a stressful week. An unemployed person may have good sleep metrics but report zero energy due to existential fatigue.

**The solution:** A **Composite Readiness Index** that weights both objective biometrics (from Google Health API / wearables) and subjective self-assessment (energy, mood, soreness, sleep quality). Neither alone is sufficient. Together they capture what algorithms miss.

**Key insight from research:**
- **Polar** integrates RPE algorithmically: `Perceived Load = RPE × duration`
- **Garmin** logs RPE but **does not use it** in Body Battery / Training Readiness — a documented gap
- **Sports science consensus:** Subjective wellness detects overreaching earlier than HRV (Saw et al., 2016)
- **MI-aligned principle:** The user owns their data. Subjective self-report is not "less valid" — it captures dimensions no sensor can measure (meaning, grief, anxiety, hope).

---

## 2. What Wearables Actually Measure (And What They Miss)

### 2.1 Objective Biometrics — What Sensors Capture

| Signal | What It Actually Measures | What It Misses |
|--------|--------------------------|----------------|
| **HRV (RMSSD)** | Parasympathetic tone, autonomic recovery | Mental fatigue, emotional distress, existential emptiness |
| **Sleep stages** | Time in REM / deep / light (accelerometer + PPG) | Perceived sleep quality, dreams, nighttime anxiety |
| **Resting HR** | Cardiovascular fitness trend | Overtraining in non-cardio domains (cognitive, emotional) |
| **Steps / activity** | Mechanical movement | Quality of movement, purpose of activity, social context |
| **Stress (HRV-derived)** | Sympathetic activation | Cause of stress (work vs. grief vs. conflict), coping resources |

### 2.2 The "False Green" Problem

> *Example:* A user has Body Battery 85 (high), Sleep Score 88, HRV Status "Balanced." But they report energy 2/10, feel "empty," and cannot start any task.
>
> *Why:* Objective metrics reflect physiological recovery. They do not reflect **purpose**, **meaning**, **grief**, **burnout**, or **learned helplessness**.

### 2.3 The "False Red" Problem

> *Example:* A user has Body Battery 25 (low), HRV "Poor." But they report energy 8/10, feel motivated, and want to tackle a challenging project.
>
> *Why:* Physiological metrics lag behind subjective state. A "bad" HRV day may follow a single poor night, but the user may be mentally recovered from a breakup, new medication, or simply wired from caffeine.

---

## 3. How Leaders Do It: Polar vs Garmin vs Fitbit

### 3.1 Polar — The Gold Standard for Integration

| Feature | Objective Input | Subjective Input | Integration |
|---------|----------------|------------------|-------------|
| **Training Load Pro** | TRIMP (HR-based), Muscle Load (power) | RPE (1–10) post-workout | **Perceived Load = RPE × duration** — algorithmically integrated |
| **Recovery Pro** | Orthostatic HRV test (morning) | 3 daily questions (soreness, strain, sleep) | Both feed into **training recommendation** |
| **Nightly Recharge** | ANS Charge (−10 to +10), Sleep Charge | Sleep quality rating (optional) | Shown side-by-side, not blended |
| **Sleep Score** | Accelerometer + optical HR | Subjective rating (1–5) | **Kept separate** for user comparison |

**Polar's design pattern:**
1. **Measure both** — objective and subjective are captured independently
2. **Show comparison** — user sees objective Sleep Score AND subjective rating side-by-side
3. **Use both for recommendations** — Recovery Pro combines HRV + subjective answers for daily advice
4. **Preserve scientific validity** — subjective ratings never corrupt objective scores

### 3.2 Garmin — Strong Objective, Weak Subjective

| Feature | Objective Input | Subjective Input | Integration |
|---------|----------------|------------------|-------------|
| **Body Battery** | HRV, stress, sleep, activity | None | N/A |
| **Training Readiness** | Sleep, HRV, load, stress, Body Battery | None | N/A |
| **Training Status** | VO2max, acute/chronic load, HRV | None | N/A |
| **Post-activity** | EPOC-based load | RPE (1–10), "How did it feel?" (5 smileys) | **Logged only, not used in algorithms** |

**Garmin's design pattern:**
1. **Purely objective** core metrics — no subjective input feeds into algorithms
2. **Optional logging** — RPE and "feelings" are captured but treated as annotations
3. **User must triangulate** — the skill/device expects the user to manually compare objective score with subjective state
4. **Morning Report is passive** — displays objective data, asks no questions

**Critical gap:** Garmin's subjective features exist but are "data graveyards" — they are collected but never used to adapt training plans. This is a major UX flaw that life-planning-coach can avoid.

### 3.3 Fitbit — Simple Subjective Integration

| Feature | Objective Input | Subjective Input | Integration |
|---------|----------------|------------------|-------------|
| **Daily Readiness** | HRV, sleep, recent activity | Daily 3-question survey (energy, mood, soreness) | **Both feed into Readiness Score** |

**Fitbit's design pattern:**
1. **Lightweight daily survey** — 3 quick questions each morning
2. **Algorithmic blending** — subjective answers directly influence the score
3. **Simple UX** — minimal friction, high adherence

---

## 4. Scientific Backing

### 4.1 sRPE — The Foundation of Subjective Load

**Session-RPE (Foster et al., 2001):**
```
sRPE = RPE (1–10) × Duration (minutes)
```

- Validated against HR-based TRIMP (r = 0.75–0.85)
- Superior for strength training, team sports, and any activity where HR lags
- Rated ~30 min post-session to avoid recency bias

**Modified Borg CR-10 Scale:**

| Score | Verbal Anchor | For Life Planning |
|-------|--------------|-------------------|
| 0 | Rest | No effort at all |
| 1 | Very, very easy | Light routine task |
| 3 | Moderate | Standard work session |
| 5 | Heavy | Challenging but manageable |
| 7 | Very heavy | Near limit, requires recovery |
| 10 | Maximal | Absolute maximum effort |

### 4.2 Subjective Wellness vs Objective Biomarkers

**Saw et al. (2016) systematic review:**
- Subjective wellness questionnaires detect overreaching **earlier** than HRV
- HRV responds to acute stressors (sleep, alcohol, illness)
- Subjective measures capture cumulative fatigue, mental load, motivation
- **Combined use is superior** to either alone

**Plews et al. (2017) — HRV-guided training:**
- Daily HRV measurement enables training adaptation
- But HRV alone misses non-physiological stressors
- Adding subjective wellness improves prediction of performance

### 4.3 Why Subjective Measures Matter for Life Planning

Life planning is **not sports training.** The stressors are different:

| Sports Stressor | Life Planning Stressor | Measurable By |
|-----------------|----------------------|---------------|
| Training volume | Workload / deadlines | Partially objective |
| Intensity | Emotional intensity | Subjective only |
| Recovery sleep | Restorative rest | Both |
| Muscle soreness | Decision fatigue | Subjective only |
| Overreaching | Burnout / meaning crisis | Subjective only |
| Tapering | Sabbatical / transition | Both |

**Key insight:** For life planning, subjective measures are arguably **more important** than for sports. Sensors cannot measure existential fatigue, grief, or loss of purpose.

---

## 5. Proposed Composite Readiness Model for Life Planning Coach

### 5.1 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           COMPOSITE READINESS INDEX (CRI)                   │
│                      Scale: 0–100                           │
├─────────────────────────────────────────────────────────────┤
│  Objective Recovery (OR)    │   Subjective Recovery (SR)    │
│  Weight: 40%                │   Weight: 60%                 │
│  Source: Google Health API  │   Source: Self-report         │
│        / Wearables          │        (conversation)         │
├─────────────────────────────┼───────────────────────────────┤
│  • Sleep score (0–100)      │  • Energy (1–10)              │
│  • HRV status (0–100)       │  • Mood / mental strain (1–10)│
│  • Resting HR trend (0–100) │  • Muscle soreness (1–10)     │
│  • Activity load (0–100)    │  • Sleep quality (1–10)       │
│  • Stress index (0–100)     │  • Meaning / purpose (1–10)   │
└─────────────────────────────┴───────────────────────────────┘
```

**Why 40/60 weighting?**
- For life planning (not sports), subjective state is more predictive of capacity
- Sensors miss meaning, grief, burnout, anxiety
- But objective data anchors subjective reports (prevents catastrophizing)

### 5.2 Component Formulas

#### Objective Recovery (OR) — 0 to 100

```
OR = (Sleep_Score × 0.30) + (HRV_Score × 0.30) + (Activity_Balance × 0.20) + (Stress_Score × 0.20)

Where:
  Sleep_Score      = normalized sleep quality from Google Health API (0–100)
  HRV_Score        = RMSSD vs personal baseline (0 = far below, 100 = above baseline)
  Activity_Balance = steps / goal + active minutes / goal (capped at 100)
  Stress_Score     = inverted stress index (0 = high stress, 100 = low stress)
```

#### Subjective Recovery (SR) — 0 to 100

```
SR = (Energy × 10 + Mood × 10 + Soreness × 10 + Sleep_Quality × 10 + Purpose × 10) / 5

Where each is self-reported 1–10:
  Energy       = "How much energy do you have?" (1 = none, 10 = peak)
  Mood         = "How is your mental state?" (1 = overwhelmed, 10 = calm/focused)
  Soreness     = "Any physical tension or soreness?" (1 = severe, 10 = none)
  Sleep_Quality= "How did you sleep?" (1 = terrible, 10 = excellent)
  Purpose      = "Do you feel sense of meaning today?" (1 = empty, 10 = fulfilled)
```

**Note:** For elder homebound and unemployed personas, the "Purpose" dimension is weighted higher (see §6.3).

### 5.3 Composite Readiness Index (CRI)

```
CRI = (OR × 0.40) + (SR × 0.60)
```

| Zone | CRI | Color | Planning Adaptation |
|------|-----|-------|---------------------|
| **Prime** | 80–100 | 🟢 | Full load — challenging goals, deep work, social activities |
| **Moderate** | 60–79 | 🟡 | Standard plan — maintain routine, no new stressors |
| **Low** | 40–59 | 🟠 | Rain plan — reduce ambitions 20–30%, fewer decisions |
| **Poor** | 0–39 | 🔴 | Recovery mode — micro-anchors only, no output goals, rest |

### 5.4 The Gap Detection Protocol

When objective and subjective scores diverge significantly (|OR − SR| > 30), trigger a **Gap Exploration**:

| Pattern | Interpretation | Coaching Response |
|---------|---------------|-------------------|
| OR high, SR low ("False Green") | Sensor says recovered, user feels drained | Explore: burnout? grief? meaning crisis? emotional labor? |
| OR low, SR high ("False Red") | Sensors show fatigue, user feels motivated | Acknowledge: physiological lag; suggest light activity, monitor |
| Both low ("True Red") | Genuine need for recovery | Full recovery mode — no guilt |
| Both high ("True Green") | Optimal window for growth | Challenge zone — suggest stretch goals |

---

## 6. UX Patterns — How to Ask

### 6.1 When to Ask (Timing)

| Time | Question Type | Context |
|------|--------------|---------|
| **Morning (7–10 AM)** | Subjective Recovery (5 questions) | After waking, before planning |
| **Mid-day check-in** | Energy re-rating (1 question) | Optional, if user reports low energy |
| **Post-activity** | sRPE (1–2 questions) | After completing a significant task/session |
| **Evening (8–10 PM)** | Quick reflection (3 questions) | Before shutdown ritual |

### 6.2 How to Ask (MI-Aligned Framing)

**❌ Avoid:**
- "Rate your energy 1–10" (clinical, detached)
- "You should feel better — your sleep was good" (invalidating)
- "Your HRV is low, so you must rest" (dictating)

**✅ Use:**
- "Как вы себя чувствуете сегодня — не по цифрам, а по ощущениям?"
- "Ваши данные показывают хороший сон, но я слышу, что энергии мало. Давайте разберёмся, что происходит."
- "Если захотите — могу предложить лёгкий план на сегодня. Или можем просто поговорить."

### 6.3 Persona Adaptations

| Persona | Objective Weight | Subjective Weight | Key Dimension |
|---------|-----------------|-------------------|---------------|
| **Standard** | 40% | 60% | Energy + Purpose |
| **ADHD** | 30% | 70% | Energy + Mental strain + Task initiation |
| **Unemployed** | 30% | 70% | Purpose + Mood + Social connection |
| **Elder Homebound** | 25% | 75% | Purpose + Meaning + Micro-achievement |

---

## 7. Implementation Path for v0.15.0+

### Phase 1: Subjective Foundation (v0.15.0)
- [ ] Add 5 daily subjective questions to `references/energy_scheduling.md`
- [ ] Create `references/composite_readiness.md` (this file as reference)
- [ ] Add CRI calculation to `references/calendar_intelligence.md`
- [ ] Test with 3 personas

### Phase 2: Objective Integration (v0.16.0)
- [ ] Implement MCP connector for Google Health API v4
- [ ] Add `get_recovery_context` tool (sleep, HRV, steps, stress)
- [ ] Blend objective + subjective in Phase 5 (Calendar)

### Phase 3: Adaptive Intelligence (v0.17.0)
- [ ] Learn user-specific baselines (28-day rolling average)
- [ ] Detect divergence patterns (False Green / False Red)
- [ ] Suggest planning adaptations automatically
- [ ] A/B test: objective-only vs composite model

---

## 8. Key References

1. **Foster et al. (2001)** — *A new approach to monitoring exercise training.* J Strength Cond Res. sRPE validation.
2. **Saw et al. (2016)** — *Monitoring the athlete training response: subjective self-reported measures trump commonly used objective measures.* Br J Sports Med. Systematic review.
3. **Plews et al. (2017)** — *Heart rate variability and training intensity distribution in elite endurance athletes.* Int J Sports Physiol Perform.
4. **Kiviniemi et al. (2007)** — *Daily exercise prescription based on heart rate variability.* Eur J Appl Physiol.
5. **Borg (1998)** — *Borg's Perceived Exertion and Pain Scales.* Human Kinetics.
6. **Polar White Paper** — *Training Load Pro: Science behind the metrics.* Polar Electro Oy.
7. **Firstbeat Analytics (Garmin)** — *Body Battery white paper.* Firstbeat Technologies.
8. **Google Health API v4** — *Developers documentation.* Google for Developers.

---

*Research synthesis completed. Ready for planning phase.*
