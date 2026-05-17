# Conversation State JSON Schema

> **Для Claude:** Используй эту схему для отслеживания состояния пользователя между сессиями. Состояние хранится в памяти разговора (conversation state) или в Claude Memory.

## Полная схема

```json
{
  "user_id": "uuid",
  "stage": "1|1.5|2|3",
  "phase": "wheel_of_life|values|designing_life|ikigai|goal_filter|goal_architecture|weekly_review",
  "diagnostic_track": "quick|deep",
  "completed_phases": ["wheel_of_life", "values"],
  "current_question": 3,
  "readiness_gates": [
    {"phase": "wheel_of_life", "score": 8, "timestamp": "2026-05-16T10:00:00Z"},
    {"phase": "values", "score": 7, "timestamp": "2026-05-16T10:15:00Z"}
  ],
  "life_wheel": {
    "health": 7,
    "finances": 6,
    "career": 4,
    "family": 8,
    "romance": 7,
    "social": 6,
    "personal_growth": 5,
    "meaning": 6,
    "fun_recreation": 3,
    "contribution": 5,
    "physical_environment": 6
  },
  "values": {
    "self_direction": 0.85,
    "achievement": 0.72,
    "benevolence": 0.91,
    "...": "..."
  },
  "goals": {
    "bhag": "...",
    "themes": [{"objective": "...", "key_results": []}],
    "twelve_week": {"objectives": [], "key_results": []},
    "weekly": ["..."],
    "daily_woop": [{"wish": "...", "outcome": "...", "obstacle": "...", "plan": "..."}]
  },
  "goal_filter": {
    "active_goals": [{"goal": "...", "radar": {"values": 9, "energy": 8, "impact": 9, "feasibility": 7, "authenticity": 8}}],
    "paused_goals": [{"goal": "...", "red_flags": ["RF3"], "insight": "..."}],
    "patterns": [{"red_flag": "RF3", "count": 2, "insight": "..."}]
  },
  "communication_style": {
    "baseline": {"softness": "soft|neutral|direct", "structure": "high|medium|low"},
    "current_intensity": "nurturing|exploratory|collaborative|challenging"
  },
  "weekly_reviews": [
    {
      "date": "2026-05-16",
      "format": "gtd_scrum",
      "worked": ["..."],
      "didnt_work": ["..."],
      "changes": ["..."],
      "lead_measures": {},
      "lag_measures": {},
      "adjustments": []
    }
  ]
}
```

## Описание полей

| Поле | Тип | Описание |
|------|-----|----------|
| `user_id` | string | UUID пользователя (генерируется при первой сессии) |
| `stage` | string | Текущий Stage: 1 (Diagnostic), 1.5 (Goal Filter), 2 (Goal Architecture), 3 (Weekly Review) |
| `phase` | string | Текущая фаза внутри Stage |
| `diagnostic_track` | string | "quick" (20-30 мин) или "deep" (65-105 мин, 2-4 сессии) |
| `completed_phases` | array | Список завершённых фаз |
| `current_question` | number | Номер текущего вопроса в фазе |
| `readiness_gates` | array | Оценки комфорта (1-10) после каждой фазы |
| `life_wheel` | object | Оценки 11 сфер Wheel of Life (1-10) |
| `values` | object | Веса ценностей Schwartz PVQ (0-1) |
| `goals` | object | Иерархия целей: BHAG → Themes → 12-Week → Weekly → Daily WOOP |
| `goal_filter` | object | Результаты Stage 1.5: Active, Paused, Patterns |
| `communication_style` | object | Базовый профиль и текущая интенсивность |
| `weekly_reviews` | array | История еженедельных ревью |

## Протокол checkpoint-and-resume

- Каждая сессия сохраняет прогресс (checkpoint)
- При возобновлении: 2-предложенный recap + "Где остановились?"
- Максимум 8-10 вопросов за сессию, затем предложить перерыв
- Поддерживать микро-сессии (2-3 минуты)
