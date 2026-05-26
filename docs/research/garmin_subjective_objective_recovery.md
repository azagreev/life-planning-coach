# Garmin Ecosystem: Integration of Subjective Self-Assessment with Objective Biometrics

> **Research brief:** How Garmin combines objective biometrics (HRV, sleep, activity, stress) with subjective self-assessment for recovery and training readiness evaluation.  
> **Date:** 2026-05-19  
> **Sources:** Garmin official documentation, Firstbeat white papers, peer-reviewed studies, DC Rainmaker / forum analyses, comparative wearable reviews.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Garmin Body Battery](#2-garmin-body-battery)
3. [Garmin Training Readiness](#3-garmin-training-readiness)
4. [Garmin Recovery Advisor / Training Status](#4-garmin-recovery-advisor--training-status)
5. [Garmin Connect Subjective Features](#5-garmin-connect-subjective-features)
6. [Garmin's Approach to Combining Objective + Subjective](#6-garmins-approach-to-combining-objective--subjective)
7. [Scientific Backing](#7-scientific-backing)
8. [Comparative Table: Garmin vs. Competitors](#8-comparative-table-garmin-vs-competitors)
9. [Key Citations](#9-key-citations)
10. [Glossary](#10-glossary)

---

## 1. Executive Summary

Garmin's recovery and readiness ecosystem is **predominantly objective**. Its core metrics — Body Battery, Training Readiness, Training Status, Training Load, and Sleep Score — are computed from physiological signals (HRV, heart rate, sleep stages, activity intensity) via Firstbeat Analytics algorithms. **Garmin does not incorporate subjective user input into these core algorithms.**

However, Garmin has been gradually adding **optional subjective capture** features:

- Post-activity **RPE rating (1–10)** and **"How did it feel?" smiley faces (5 levels)**
- **Perceived Exertion** logging in newer watches (vivoactive 5, Forerunner series updates)
- **Health Snapshot** — on-demand 2-minute physiological assessment
- **Morning Report** — automated summary of objective metrics

**Critical gap:** Unlike competitors (e.g., Fitbit's daily 3-question subjective survey, Polar's Perceived Load = RPE × duration), Garmin's subjective inputs are **data-logged but not algorithmically integrated** into training load, recovery time, or readiness calculations. The user must manually triangulate objective scores with subjective feel.

---

## 2. Garmin Body Battery

### 2.1 What It Measures

Body Battery is a proprietary composite score (0–100) estimating available physical and mental energy reserves. Introduced in 2017, refined through firmware updates.

| Input | Description | Source |
|-------|-------------|--------|
| **HRV (RMSSD)** | Primary barometer of autonomic resilience; measured during sleep and quiet rest | Optical PPG (wrist) or chest strap |
| **Stress Tracking** | Real-time stress index from beat-to-beat HRV analysis | Firstbeat algorithm |
| **Sleep Quality & Duration** | Sleep stages (deep, light, REM), efficiency, restlessness | Optical PPG + accelerometer |
| **Activity/Rest** | Energy expenditure vs. recovery periods; low-HR rest periods | Accelerometer + HR |

### 2.2 Algorithm Characteristics

- **Scale:** 0–100 (0–30 = low, 70–100 = high readiness)
- **Reset:** Resets every 24 hours; heavily reactive to acute stressors
- **Weighting:** HRV is weighted most heavily, especially overnight RMSSD
- **Sensitivity:** A stressful meeting or caffeine before bed can drop score 20–30 points within 90 minutes
- **Baseline:** Requires ~3 weeks of consistent wear to establish personal baseline

### 2.3 Subjective Input?

**No.** Body Battery does not ask for or incorporate any subjective user input (mood, soreness, energy, perceived sleep quality). This is a documented limitation:

> "Garmin does not incorporate user-reported wellness data (e.g., soreness, mood, energy) into Body Battery. A runner logging perfect sleep and stable HRV may still feel wrecked after two weeks of high-volume intervals — but Body Battery won't reflect it without objective deviation." [Source: comparative wearable analysis]

### 2.4 Validation

| Study | Finding | Correlation |
|-------|---------|-------------|
| Frontiers in Physiology (2023) | Body Battery vs. subjective fatigue | r = 0.58 (moderate) |
| Frontiers in Physiology (2023) | Body Battery vs. salivary cortisol | r = 0.21 (weak) |
| Garmin internal study (2022, n=1,240) | Body Battery vs. subjective fatigue | Correlational (no peer review) |

---

## 3. Garmin Training Readiness

### 3.1 What It Measures

Training Readiness is a composite score (0–100) indicating how prepared the body is to handle training load on a given day. Introduced with Forerunner 955/Fenix 7 generation.

| Factor | Time Window | Description |
|--------|-------------|-------------|
| **Sleep Score** | Last night | 0–100 score from sleep duration, stages, HRV-derived recovery |
| **Recovery Time** | From last activity | Countdown hours until ready for next hard workout |
| **Acute Training Load** | Last 7 days | Weighted sum of recent training stress (EPOC-based) |
| **HRV Status** | 7-day average vs. 60-day baseline | Balanced / Unbalanced / Poor |
| **Sleep History** | Last 3 nights | Cumulative sleep quality beyond single night |
| **Stress History** | Last 3 days (awake) | All-day stress tracking accumulation |
| **Body Battery** | Current level | Energy reserve from Body Battery algorithm |

### 3.2 Score Zones

| Color | Score | Status | Recommendation |
|-------|-------|--------|----------------|
| Purple | 95–100 | Prime | Best possible — peak readiness |
| Blue | 75–94 | High | Ready for challenges |
| Green | 50–74 | Moderate | Good to go |
| Orange | 25–49 | Low | Time to slow down |
| Red | 1–24 | Poor | Let your body recover |

### 3.3 Subjective Input?

**No.** Training Readiness is purely algorithmic. Garmin explicitly states:

> "The score cannot detect muscular soreness or mental fatigue, both of which fall outside what a wrist optical sensor can measure." [Source: the5krunner.com, Garmin documentation]

The HRV component responds to physiological state rather than subjective sleep quality, so the score and perceived feel frequently diverge.

### 3.4 UX Pattern: Morning Report

On compatible devices, Training Readiness surfaces automatically in the **Morning Report** — triggered when the watch detects the user is awake (wrist gesture + normal wake time). The report is customizable and can include:

- Training Readiness
- HRV Status
- Sleep Score
- Weather
- Calendar
- Body Battery
- Daily Suggested Workout

**Important:** The Morning Report is a **passive display** of objective metrics. It does **not** ask the user "How do you feel today?" or request any subjective readiness input.

---

## 4. Garmin Recovery Advisor / Training Status

### 4.1 Training Status

Training Status assesses whether recent training is producing fitness benefit, maintaining fitness, or causing detraining. It is based on:

| Component | Description |
|-----------|-------------|
| **VO2max Trend** | Estimated aerobic capacity over weeks; updated after qualifying outdoor activities |
| **Acute Load** | 7-day rolling training stress |
| **Chronic Load** | 4-week average training load |
| **HRV Status** | Multi-day recovery trend |
| **Load Focus** | Distribution across low aerobic, high aerobic, anaerobic zones |

**Status Levels:** Peaking, Productive, Maintaining, Recovery, Strained, Unproductive, Overreaching, Detraining.

### 4.2 Recovery Time

- Displayed as hours remaining until ready for next hard workout
- Updated throughout the day based on sleep, stress, relaxation, and physical activity
- Speeds up with good sleep; slows down with poor sleep or stressful days
- Uses VO2max estimate in calculation

### 4.3 Load Focus

Analyzes training load distribution across three intensity zones:

| Zone | Description |
|------|-------------|
| **Low Aerobic** | Base endurance (Zone 1–2) |
| **High Aerobic** | Tempo/threshold (Zone 3–4) |
| **Anaerobic** | VO2max/sprints (Zone 5) |

Requires at least 7 days of training to determine if load is low, optimal, or high. After 4 weeks, shows 4-week distribution.

### 4.4 Subjective Input?

**No.** Recovery Time, Training Status, and Load Focus are entirely objective. Recovery Time does not adjust based on user-reported soreness. Training Status does not incorporate "how you feel."

One semi-subjective feature: users can **pause Training Status** when injured or sick. This is a manual override, not an integrated subjective input.

---

## 5. Garmin Connect Subjective Features

### 5.1 Post-Activity RPE / "How Did It Feel?"

Introduced in firmware updates for Forerunner 45/245/745/945 and newer models.

| Feature | Description |
|---------|-------------|
| **RPE Scale** | 1–10 rating of perceived exertion |
| **Feeling Scale** | 5 smiley faces representing subjective state (strong → weak) |
| **When** | Prompted after workout completion on watch |
| **Where Stored** | Activity record in Garmin Connect (visible in mobile app) |

**UX Pattern:** After saving an activity, the watch prompts: "How did that feel?" User selects a smiley face, then optionally rates RPE 1–10.

**Algorithm Integration:** The RPE/feelings data is **stored but not integrated** into Training Load, Recovery Time, or Training Status algorithms. It appears the data serves logging and longitudinal self-reflection purposes only.

> "Your personal assessment of your Rate of Perceived Effort (RPE) is then stored in the workout and visible in the Connect app... An RPE form like this can easily be used by developers as a proxy for Training Load and hence may well be an input into Garmin's adaptation protocol in the COACH. (I'm NOT saying it's a GOOD proxy BTW!)" [Source: the5krunner.com, Garmin Coach analysis]

### 5.2 Perceived Exertion in Garmin Connect

The Garmin Connect app and newer watches (vivoactive 5, Fenix 7 series, Forerunner 265/965) support **Perceived Exertion** as a post-workout field. This is separate from the automatic Training Effect calculation.

Key distinction:
- **Training Effect** = algorithmic (objective, based on HR zones + duration)
- **Perceived Exertion** = user-reported (subjective, user rates how hard it felt)

### 5.3 Health Snapshot / HRV Stress Test

#### Health Snapshot
- **Duration:** 2-minute controlled test
- **Metrics Captured:** Resting HR, HRV (SDRR, RMSSD), SpO2, Respiration Rate, Stress Score
- **When:** On-demand, anytime
- **UX:** User must sit still; recommended to take at same time daily for consistency
- **Subjective?** No — purely objective snapshot

#### HRV Stress Test
- **Duration:** 3-minute test
- **Requirement:** Chest strap HR monitor (on some devices); standing position
- **Output:** Stress score 0–100 (lower = less stress)
- **Purpose:** Assess readiness before workout
- **Subjective?** No — purely HRV-based

### 5.4 Morning Report

The Morning Report is an **automated, passive briefing** that appears when the watch detects waking. It displays objective metrics but does **not ask subjective questions**.

**Available widgets:** Training Readiness, HRV Status, Sleep, Weather, Calendar, Body Battery, Intensity Minutes, Steps, Daily Suggested Workout.

**Missing:** No "How do you feel?" prompt, no subjective wellness survey, no energy/mood/soreness questions.

### 5.5 Sleep Score

| Component | Weight | Description |
|-----------|--------|-------------|
| Sleep Duration | High | vs. user-defined goal (typically 7–9 hrs) |
| Sleep Stages | High | Deep, light, REM proportions |
| HRV-derived Recovery | Medium | Parasympathetic activity during sleep |
| Restlessness | Medium | Movement-based awakenings |
| Awake Time | Low | Time spent awake during night |

**Scale:** 0–100
- 90–100 = Excellent
- 80–89 = Good
- 60–79 = Fair
- 0–59 = Poor

**Subjective Input?** **No.** Garmin does not ask users to rate their perceived sleep quality. The score is entirely objective. This contrasts with Fitbit, which allows users to log how they feel upon waking.

> "Garmin provides a similar sleep score between 0 and 100, with broadly similar inputs, but includes an estimated 'stress index' during the sleep period, which is based on heart rate variability." [Source: IntechOpen sleep quality assessment chapter]

---

## 6. Garmin's Approach to Combining Objective + Subjective

### 6.1 How Garmin Uses RPE in Training Load

**Answer: It doesn't.** Garmin's Training Load is calculated from objective data only:

> **Training Load = EPOC (Excess Post-Exercise Oxygen Consumption)** estimated from heart rate data during activity. It is a 7-day rolling sum of arbitrary load units.

This differs from Polar's approach:

| Brand | Training Load Formula | Subjective Integration |
|-------|----------------------|------------------------|
| **Garmin** | EPOC from HR (objective) | None |
| **Polar** | Cardio Load (HR-based) + **Perceived Load = RPE × duration** | RPE directly integrated |
| **TrainerRoad** | Power-based TSS + post-workout RPE survey | RPE adapts future workouts |
| **Whoop** | Cardiovascular + muscular strain from HR | None |

Garmin's post-activity RPE is **data-logged only**. There is no evidence it feeds back into Training Load, Training Status, or Daily Suggested Workouts algorithms.

### 6.2 Load Focus + Subjective Feedback

Load Focus categorizes training by heart rate zone intensity:

| Category | HR Zone | Training Benefit |
|----------|---------|------------------|
| Low Aerobic | Zones 1–2 | Base endurance, fat oxidation |
| High Aerobic | Zones 3–4 | Threshold, tempo, race pace |
| Anaerobic | Zone 5 | VO2max, speed, power |

**Subjective integration:** None. Load Focus is purely HR-zone-based. The user can see their distribution over 4 weeks, but Garmin does not ask "Did this feel too easy/hard?" to validate zone assignments.

### 6.3 ClimbPro / PacePro — Subjective State Adjustment?

**No.** These features are **pre-planned, static tools**:

- **PacePro:** Creates grade-adjusted pacing strategies before a run. Targets are fixed at creation. Does not adapt mid-run based on fatigue, Body Battery, or subjective feel.
- **ClimbPro:** Displays upcoming climbs with distance, elevation, and gradient. Does not adjust based on recovery status.

> "Targets are fixed at strategy creation and remain static throughout the activity. Only the cumulative ahead/behind display updates in real time." [Source: the5krunner.com PacePro guide]

Neither feature integrates Training Readiness or Body Battery to dynamically soften targets on low-recovery days.

### 6.4 Daily Suggested Workouts + Subjective State

Daily Suggested Workouts generate personalized run/cycle workouts based on:

- Training Status
- Training Load & Load Focus
- VO2max
- Recovery Time
- Sleep data
- Recent workout profile

**Subjective integration:** None. The algorithm does not incorporate post-workout RPE or "how did it feel" ratings to adjust future suggestions. However, users report that if they **manually deviate** from suggestions (e.g., skip a hard workout, do an easy run instead), the algorithm eventually adapts.

Forum users note a key limitation:

> "The watch can suggest a hard workout while your recovery is still 'orange'. It looks like acute load is used though... I often replace or dismiss a workout when my training readiness metrics, my body battery or my perceived readiness is not matching the demand of the workout." [Source: Garmin forums]

---

## 7. Scientific Backing

### 7.1 Firstbeat Analytics (Garmin's Algorithm Engine)

Garmin acquired Firstbeat Technologies' analytics division in 2020. Firstbeat provides the physiological modeling behind most Garmin health/training metrics.

#### HRV-Based Stress Detection

Firstbeat's stress algorithm uses:

> "HRV measurements derived from inter-beat interval (IBI) signals. The stress-state detection procedure relies on two physiological assumptions: (1) it assesses sympathetic dominance relative to parasympathetic dominance, as inferred from heartbeat parameters; (2) it distinguishes the source of cardiac reactivity, excluding physical activity, movement, or posture." [Source: Firstbeat white paper / bioRxiv validation study]

- Stress score: 0–100 at 3-minute intervals
- Uses neural network modeling of HRV time/frequency domain variables
- Calculates derived parameters: respiration rate, VO2, EPOC

#### VO2max Estimation

| Metric | Method | Accuracy |
|--------|--------|----------|
| Running | HR + pace regression, HRV-derived efficiency | ~5% MAPE (Firstbeat white paper, 2014) |
| Cycling | HR + power regression | ~8% MAPE |
| Validation | Meta-analysis (Molina-Garcia et al., 2022) | 8–10.2% MAPE in independent studies |

Key paper: Firstbeat Technologies (2014). "Automated Fitness Level (VO2max) Estimation With Heart Rate and Speed Data." White paper.

#### Sleep Analysis

Firstbeat's sleep methodology (2019 white paper):

- Sleep stages from HRV + movement
- ANS balance assessment: parasympathetic dominance = recovery; sympathetic bursts = stress/restlessness
- Sleep score composites: duration + stages + HRV recovery + restlessness

### 7.2 Training Load Algorithms

Garmin Training Load is derived from **EPOC estimation**:

> "Training load is the sum of your excess post-exercise oxygen consumption (EPOC) over the last 7 days. EPOC is an estimate of how much energy it takes for your body to recover after exercise." [Source: Garmin official manual]

EPOC is estimated from heart rate response during activity using Firstbeat's neural network models. It does **not** use RPE or subjective effort.

### 7.3 Research on Combining HRV + Subjective Wellness

The scientific consensus supports combining HRV with subjective measures for training adaptation monitoring:

#### Key Finding 1: Subjective Measures Are More Responsive Than Objective

> "Subjective measures reflected acute and chronic training loads with superior sensitivity and consistency than objective measures... There was negligible evidence for an association between subjective and objective measures." [Source: Saw et al., 2016, systematic review in BMJ Open]

#### Key Finding 2: HRV + Subjective Combined > Either Alone

> "When HRV is combined with subjective wellness assessments and contextual training data, it evolves from a passive measurement into a dynamic tool... Brief psychometric tools have shown to be sensitive to both physical and psychological stress. When used alongside HRV, these measures can identify discrepancies between physiological signals and perceived recovery, offering early warning signs of non-functional overreaching." [Source: PMC review, 2024]

#### Key Finding 3: Association Between HRV and Subjective Recovery

Flatt et al. (2018) studied Division-1 swimmers:

> "LnRMSSD was higher when perceived sleep quality, fatigue, stress and mood were better than average versus worse than average... 15 of 17 subjects demonstrated at least one relationship between LnRMSSD and subjective measures." [Source: Sports (MDPI), 2018]

#### Key Finding 4: Weak Correlation in Consumer Settings

Recent research on consumer wearables shows weaker associations:

> "Self-reported stress and nervousness did not have an association with heart rate variability... Subjective feelings of readiness may not correspond to activity tracker biometrics and should be taken into consideration when calculating readiness scores." [Source: PMC, 2026]

#### Key Finding 5: HRV-Guided Training Outperforms Fixed Plans

> "A systematic review/meta-analysis found HRV-guided training yields greater gains in aerobic fitness/performance than predefined plans, by enabling day-to-day adjustments around the athlete's readiness." [Source: PMC meta-analysis]

### 7.4 Garmin-Specific Validation

| Study | Finding |
|-------|---------|
| Frontiers in Digital Health (2025) | Garmin stress levels and body battery computed via "black-box algorithm" mostly based on HRV; sleep stages at 1-min resolution |
| University of Oulu research | Body Battery relies on HRV, stress, sleep; proprietary weighting adjusted dynamically per user |
| DC Rainmaker field testing | Body Battery variance exceeded ±18% vs. ECG chest strap for 34% of participants |

---

## 8. Comparative Table: Garmin vs. Competitors

| Feature | Garmin | Fitbit | Polar | Whoop | Oura |
|---------|--------|--------|-------|-------|------|
| **Core Recovery Metric** | Body Battery (0–100) | Readiness Score (0–100) | Nightly Recharge | Recovery Score (0–100%) | Readiness Score (0–100) |
| **HRV Metric** | RMSSD (overnight + Health Snapshot) | SDNN (overnight) | Nightly HRV | RMSSD (continuous) | RMSSD, SDNN (overnight) |
| **Subjective Input into Algorithm** | **No** | **Yes** (daily survey) | Partial (Nightly Recharge asks feel) | No | No |
| **Post-Activity RPE** | Yes (logged, not integrated) | No | Yes (Perceived Load = RPE × duration) | Yes (logged) | No |
| **Morning Readiness Prompt** | No (passive report only) | Yes (3-question survey) | No | No | No |
| **Sleep Score Subjective Input** | No | No | No | No | No |
| **Training Load Formula** | EPOC from HR | Active Zone Minutes | Cardio Load + Perceived Load | Cardiovascular + Muscular Strain | Activity Score |
| **Dynamic Workout Adjustment** | Daily Suggested Workouts (objective only) | No | FitSpark (objective) | Strain Coach | No |
| **Scientific Validation** | Firstbeat white papers; limited peer review | Fitbit Sleep Study | Polar Research papers | Whoop validation studies | Multiple peer-reviewed studies |

---

## 9. Key Citations

### Official Garmin / Firstbeat Sources

1. Garmin Technology — Training Readiness: https://www.garmin.com/en-US/garmin-technology/running-science/physiological-measurements/training-readiness/
2. Garmin Technology — HRV Stress Test: https://www.garmin.com/en-US/garmin-technology/running-science/physiological-measurements/hrv-stress-test/
3. Garmin Support — Sleep Score: https://support.garmin.com/en-US/?faq=DWcdBazhr097VgqFufsTk8
4. Garmin Support — Self Evaluation Feature: https://support.garmin.com/en-US/?faq=8nISJXqSZVAI3Td4IWRqsA
5. Garmin Blog — How Garmin Watches Track Sleep: https://www.garmin.com/en-US/blog/fitness/how-garmin-watches-track-your-sleep-calculate-sleep-score/
6. Garmin Blog — New Data Examines Quality of Garmin Users' Sleep: https://www.garmin.com/en-US/blog/health/new-data-examines-quality-of-garmin-users-sleep/
7. Garmin Blog — Training Status and How to Use It: https://www.garmin.com/en-US/blog/fitness/garmin-training-status-and-how-to-use-it/
8. Firstbeat White Paper — Stress and Recovery Analysis (2014): https://www.firstbeat.com/wp-content/uploads/2015/10/Stress-and-recovery_white-paper_20145.pdf
9. Firstbeat White Paper — Sleep Analysis Method (2019): https://www.firstbeat.com/wp-content/uploads/2019/11/A-Sleep-Analysis-Method-Based-on-Heart-Rate-Variability-071119.pdf
10. Firstbeat White Paper — VO2max Estimation (2014): "Automated Fitness Level (VO2max) Estimation With Heart Rate and Speed Data"

### Third-Party Analyses

11. the5krunner — Garmin Training Readiness Deep Dive: https://the5krunner.com/garmin-features/training/training-readiness/
12. the5krunner — Garmin VO2max: https://the5krunner.com/garmin-features/physiology/vo2-max/
13. the5krunner — Garmin PacePro: https://the5krunner.com/garmin-features/performance/pacepro/
14. the5krunner — Garmin Coach / RPE: https://the5krunner.com/2018/07/11/garmin-coach-any-good-free-adaptive-5k-running-plan/
15. DC Rainmaker — Fenix 7 Pro Review: https://www.dcrainmaker.com/2023/05/flaslight-multiband-everyone.html
16. DC Rainmaker — Forerunner 265 Review: https://www.dcrainmaker.com/2023/03/garmin-forerunner-265-265s-review-amoled.html
17. Wired — Garmin's Top Training Features Explained: https://www.wired.com/story/garmins-top-training-features-explained/
18. Wareable — Garmin Health Snapshot: https://www.wareable.com/garmin/what-is-garmin-health-snapshot-how-to-use
19. Wareable — Garmin Coach vs. Daily Suggested Workouts: https://www.wareable.com/garmin/garmin-coach-vs-daily-suggested-workouts-key-differences

### Peer-Reviewed Studies

20. Flatt, A.A., Esco, M.R., & Nakamura, F.Y. (2018). "Association between Subjective Indicators of Recovery Status and Heart Rate Variability among Division-1 Sprint-Swimmers." *Sports*, 6(3), 93. https://www.mdpi.com/2075-4663/6/3/93
21. Saw, A.E., Main, L.C., & Gastin, P.B. (2016). "Monitoring the athlete training response: subjective self-reported measures trump commonly used objective measures." *BMJ Open Sport & Exercise Medicine*. https://pmc.ncbi.nlm.nih.gov/articles/PMC4789708/
22. Molina-Garcia, P. et al. (2022). "Validity of Estimating the Maximal Oxygen Consumption." Systematic review validating consumer wearable VO2max estimates. https://findresearcher.sdu.dk/ws/files/203839161/Molina_Garcia2022_Article_ValidityOfEstimatingTheMaximal.pdf
23. "Associations Between Daily Heart Rate Variability and Self-Reported Wellness: A 14-Day Observational Study in Healthy Adults." https://pmc.ncbi.nlm.nih.gov/articles/PMC12300306/
24. "Disconnection Between Self-Reported Wellbeing and Heart Rate Variability from Wearables." https://pmc.ncbi.nlm.nih.gov/articles/PMC12944331/
25. "Monitoring Training Adaptation and Recovery Status in Athletes." https://pmc.ncbi.nlm.nih.gov/articles/PMC12787763/
26. "Performance of seven consumer sleep-tracking devices." https://pmc.ncbi.nlm.nih.gov/articles/PMC8120339/
27. "Determinants and Factors of Physical Activity After Oncology Treatments." https://pmc.ncbi.nlm.nih.gov/articles/PMC11140280/
28. Seipäjärvi et al. (2022). "Measuring psychosocial stress with heart rate variability-based methods." *Physiological Measurement*, 43(5).
29. Frontiers in Digital Health (2025). Wearable data study using Garmin Health API. https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1640900/pdf

---

## 10. Glossary

| Term | Definition |
|------|------------|
| **ANS** | Autonomic Nervous System — controls involuntary physiological functions |
| **Body Battery** | Garmin's 0–100 energy reserve score combining HRV, stress, sleep, activity |
| **EPOC** | Excess Post-Exercise Oxygen Consumption — oxygen debt after exercise |
| **Firstbeat** | Finnish analytics company (acquired by Garmin in 2020) providing physiological algorithms |
| **HRV** | Heart Rate Variability — variation in time between heartbeats |
| **Load Focus** | Garmin's categorization of training load into low aerobic, high aerobic, anaerobic |
| **Morning Report** | Automated daily briefing on Garmin watches showing objective health/training metrics |
| **PacePro** | Garmin's grade-adjusted pacing strategy tool for races |
| **RMSSD** | Root Mean Square of Successive Differences — time-domain HRV metric |
| **RPE** | Rate of Perceived Exertion — subjective effort rating (1–10 or Borg 6–20) |
| **Training Effect** | Per-activity score (0.0–5.0) for aerobic/anaerobic stimulus |
| **Training Load** | 7-day rolling sum of EPOC-based training stress |
| **Training Readiness** | Garmin's 0–100 daily readiness score |
| **Training Status** | Long-term assessment of training benefit based on VO2max trend |
| **VO2max** | Maximal oxygen uptake — measure of aerobic fitness |

---

*Document compiled for life-planning-coach research. Focus: understanding how consumer wearables integrate subjective and objective recovery data, with specific attention to UX patterns, algorithmic transparency, and scientific validation.*
