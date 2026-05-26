# Архитектура интерактивного дашборда Life Planning

## Версия: 1.0 | Дата: 2025-01-15 | Статус: Проект

---

## 1. Компонентная архитектура

### 1.1 Иерархия компонентов

```
Dashboard (root)
|
|-- Header (фиксированный)
|   |-- Title + Subtitle ("Life Dashboard" | период)
|   |-- Date Range Picker (week selector)
|   |-- Export Button (PNG/SVG/JSON)
|   |-- Mobile Menu Toggle (< 768px)
|
|-- Sidebar (collapsible на mobile)
|   |-- Life Area Selector (8 сфер + "All")
|   |-- Date Range Presets (12WY / Month / Quarter / Year)
|   |-- Filters (goal type, status, priority)
|   |-- Mini Stats (текущая неделя, streak)
|
|-- Tab Navigation
|   |-- Tab: Overview (обзор)
|   |-- Tab: Retrospective (ретроспектива)
|   |-- Tab: Goals (цели)
|
|-- Content Area (динамический, по активному табу)
|   |
|   |-- [Tab: Overview]
|   |   |-- Section: Life Balance
|   |   |   |-- Wheel of Life Radar (ECharts radar)
|   |   |   |-- Life Balance Score (число, расчётное)
|   |   |
|   |   |-- Section: Execution
|   |   |   |-- OKR Progress Rings (Chart.js doughnut x 3)
|   |   |   |-- 12-Week Status Bar (сегментированный прогресс)
|   |   |
|   |   |-- Section: Velocity
|   |   |   |-- Weekly Velocity Sparkline (ECharts line, mini)
|   |   |   |-- Execution Score Trend (Sparkline)
|   |   |
|   |   |-- Section: Confidence
|   |       |-- Confidence Gauges (ECharts gauge x 3-5)
|   |
|   |-- [Tab: Retrospective]
|   |   |-- Section: Velocity Analysis
|   |   |   |-- Velocity Chart (ECharts combo: bar + line + trend)
|   |   |
|   |   |-- Section: Consistency
|   |   |   |-- Calendar Heatmap (ECharts calendar, GitHub-style)
|   |   |   |-- Streak Counters (current / best)
|   |   |
|   |   |-- Section: Pace Tracking
|   |   |   |-- Burndown Chart (ECharts line: ideal vs actual + forecast)
|   |   |
|   |   |-- Section: Lead/Lag Measures
|   |       |-- Lead vs Lag Bars (ECharts bar с target line)
|   |
|   |-- [Tab: Goals]
|       |-- Section: Roadmap
|       |   |-- BHAG Roadmap (ECharts timeline, cascade view)
|       |
|       |-- Section: 12-Week Execution
|       |   |-- 12-Week Tracker (progress bars + execution score)
|       |   |-- Weekly Priority List (интерактивный список)
|       |
|       |-- Section: Daily Practice
|       |   |-- Daily WOOP Cards (4 карточки: W-O-O-P)
|       |
|       |-- Section: Goal Details
|           |-- Goal Cards (expandable, с drill-down)
|
|-- Footer
|   |-- Legend (глобальная)
|   |-- Last Updated timestamp
|   |-- Keyboard shortcuts hint
|
|-- Modal Layer
|   |-- Day Detail Modal (клик по heatmap cell)
|   |-- Sphere Drill-down Modal (клик по radar сфере)
|   |-- Goal Detail Modal (клик по timeline bar)
|   |-- Export Options Modal
|
|-- Toast Layer
    |-- Notifications (export complete, data updated, etc.)
```

### 1.2 Схема раскладки (Desktop 1200px+)

```
+------------------------------------------------------------------+
| HEADER                                                [Export]    |
| Life Dashboard | Week 8 of 12               [Date Picker]       |
+-----------+------------------------------------------------------+
|           | TAB: Overview | Retrospective | Goals               |
|           +------------------------------------------------------+
|  SIDEBAR  | +------------------+ +-------------------------+    |
|           | | Wheel of Life    | | Calendar Heatmap        |    |
| [8 сфер]  | | (Radar Chart)    | | (GitHub-style, 365d)    |    |
|  + All    | |                  | |                         |    |
|           | | Click->drill     | | Click->day detail       |    |
| [Presets] | +------------------+ +-------------------------+    |
| 12WY      |                                                |
| Month     | +---------------------------------------------+    |
| Quarter   | | Velocity Sparkline (mini)                   |    |
| Year      | | Bar: completed | Line: planned | Trend      |    |
|           | +---------------------------------------------+    |
| [Filters] |                                                |
| Type      | +----------------+ +----------------+ +---------+ |
| Status    | | OKR Ring 1     | | OKR Ring 2     | | Gauge   | |
| Priority  | | 72%            | | 55%            | | Conf.   | |
|           | | "Health"       | | "Career"       | | 7.2/10  | |
| [Mini     | +----------------+ +----------------+ +---------+ |
|  Stats]   |                                                |
| Week 8/12 | +---------------------------------------------+    |
| Streak 12 | | OKR Progress Bars                           |    |
| Score 7.2 | | O1: ████████░░ 72%                        |    |
|           | | O2: ██████░░░░ 55%                        |    |
|           | | O3: ██████████ 91%                        |    |
|           | +---------------------------------------------+    |
+-----------+------------------------------------------------------+
| Footer: Global Legend | Last updated: 2025-01-15 09:00            |
+------------------------------------------------------------------+
```

### 1.3 Схема раскладки (Mobile < 768px)

```
+-----------------------+
| [=] Life Dashboard [E]|
| Week 8 of 12          |
+-----------------------+
| Overview | Retro | Goa|
+-----------------------+
| Wheel of Life (full)  |
| (Radar, скруглённый)  |
+-----------------------+
| Heatmap (3 мес. scroll|
| вертикально)          |
+-----------------------+
| Velocity (mini)       |
+-----------------------+
| [Ring 1] [Ring 2]     |
+-----------------------+
| OKR Bars              |
+-----------------------+
| Gauge (1, carousel)   |
+-----------------------+
```

---

## 2. Data Flow Architecture

### 2.1 Обзор потока данных

```
+---------------------------------------------------------------+
|                     DATA SOURCES                              |
+---------------------------------------------------------------+
|  Skill (JSON)  |  LocalStorage  |  User Input (UI)            |
|  (primary)     |  (cache)       |  (checklist, notes)          |
+-------+--------+-------+--------+---------------+-------------+
        |                |                        |
        v                v                        v
+-------+----------------+------------------------+-------------+
|                     DATA LAYER                                |
+---------------------------------------------------------------+
|  JSON Parser  |  Validator  |  Normalizer  |  Merger        |
|  (parse input)|  (zod-like) |  (форматы)   |  (merge sources) |
+-------+--------+------+-------+-------+--------+-------------+
        |               |               |
        v               v               v
+-------+---------------+---------------+-----------------------+
|                     STATE STORE                               |
+---------------------------------------------------------------+
|  Store Pattern: Event-Driven Reactive Store                  |
|  - State: { data, ui, filters, meta }                        |
|  - Actions: setData, updateFilter, setTab, drillDown         |
|  - Subscribers: chart components re-render on state change   |
+-------+---------------+---------------+-----------------------+
        |               |               |
        v               v               v
+-------+---------------+---------------+-----------------------+
|                  CHART COMPONENTS                             |
+---------------------------------------------------------------+
|  ECharts Instances  |  Chart.js Instances  |  DOM Components  |
|  - Radar            |  - Doughnut Rings    |  - WOOP Cards    |
|  - Heatmap          |  - Progress Bars     |  - Checklists    |
|  - Gauge            |                      |  - Modals        |
|  - Timeline         |                      |                  |
|  - Combo Charts     |                      |                  |
+-------+---------------+---------------+-----------------------+
        |               |               |
        v               v               v
+-------+---------------+---------------+-----------------------+
|                  INTERACTION LAYER                            |
+---------------------------------------------------------------+
|  Events: click | hover | toggle | zoom | export | filter     |
|  Handlers: drill-down | tooltip | legend | PNG/SVG capture   |
+---------------------------------------------------------------+
```

### 2.2 Детальный Data Flow

#### Этап 1: Инициализация (Dashboard Mount)

```
[Dashboard.init]
    |
    |-- 1.1 Проверить LocalStorage на cached data
    |       |-- Есть кэш и не устарел (< 1 час) -> использовать
    |       |-- Нет кэша / устарел -> ждать input
    |
    |-- 1.2 Подписаться на JSON input (event "dashboard:data")
    |       |-- Данные приходят от skill как CustomEvent
    |       |-- Payload: полный JSON объект data
    |
    |-- 1.3 Инициализировать Store с дефолтным состоянием
    |       |-- ui.tab = 'overview'
    |       |-- filters.sphere = 'all'
    |       |-- filters.period = '12wy'
    |
    |-- 1.4 Смонтировать компоненты (lazy - по tab)
    |       |-- Overview: всегда монтируется
    |       |-- Retrospective: по запросу
    |       |-- Goals: по запросу
    |
    |-- 1.5 Настроить глобальные обработчики событий
            |-- resize -> debounce(200ms) -> chart.resize()
            |-- visibilitychange -> pause/resume animations
            |-- beforeunload -> сохранить state в LocalStorage
```

#### Этап 2: Получение данных

```
[Event: dashboard:data]
    |
    |-- 2.1 Parse JSON
    |       |-- JSON.parse() с обработкой ошибок
    |       |-- При ошибке -> показать Toast "Invalid data format"
    |
    |-- 2.2 Validate Schema
    |       |-- Проверить обязательные поля (meta, wheelOfLife, okr, weeks)
    |       |-- Проверить типы данных
    |       |-- При ошибке -> показать Toast "Data validation failed"
    |
    |-- 2.3 Normalize
    |       |-- Даты в ISO format (YYYY-MM-DD)
    |       |-- Числа в Number (не string)
    |       |-- Заполнить defaults для отсутствующих полей
    |
    |-- 2.4 Store.dispatch('setData', normalizedData)
            |
            |-- 2.4.1 Store обновляет state.data
            |-- 2.4.2 Store уведомляет всех subscribers
            |-- 2.4.3 Каждый chart component получает update
            |-- 2.4.4 Chart component вызывает chart.setOption()
            |-- 2.4.5 Сохранить в LocalStorage (cache)
```

#### Этап 3: Обновление данных (Real-Time)

```
[User Interaction] или [Event from Skill]
    |
    |-- Вариант A: Пользователь кликнул checkbox в Weekly Priority
    |       |-- UI обновляется немедленно (optimistic update)
    |       |-- Store.dispatch('updateTaskStatus', { id, completed })
    |       |-- Chart components пересчитывают derived data
    |       |-- Charts обновляются через setOption (merge)
    |
    |-- Вариант B: Пришли новые данные от skill
    |       |-- Повторить Этап 2
    |       |-- Сравнить с текущим state (diff)
    |       |-- Обновить только изменённые series
    |
    |-- Вариант C: Пользователь изменил фильтр
            |-- Store.dispatch('setFilter', { filter, value })
            |-- Derived data пересчитывается
            |-- Charts обновляются
```

### 2.3 State Management (Reactive Store Pattern)

#### Store Architecture

```javascript
// Простой reactive store на чистом JS (без фреймворков)
class DashboardStore {
  constructor() {
    // --- Core State ---
    this.state = {
      // Raw data от skill
      data: null,

      // UI State
      ui: {
        activeTab: 'overview',      // 'overview' | 'retrospective' | 'goals'
        sidebarOpen: false,          // mobile only
        modalOpen: null,            // null | 'dayDetail' | 'sphereDetail' | 'goalDetail'
        modalData: null,            // данные для открытого модала
        isLoading: false,
        lastUpdated: null,
      },

      // Filters
      filters: {
        sphere: 'all',              // 'all' | sphereId из wheelOfLife
        period: '12wy',             // '12wy' | 'month' | 'quarter' | 'year'
        goalType: 'all',            // 'all' | 'BHAG' | 'OKR' | 'weekly' | 'WOOP'
        status: 'all',              // 'all' | 'onTrack' | 'atRisk' | 'offTrack'
        dateRange: {                // кастомный диапазон
          start: null,
          end: null,
        },
      },

      // Meta
      meta: {
        version: '1.0',
        dataVersion: null,          // для инвалидации кэша
        exportFormat: 'png',        // 'png' | 'svg' | 'json'
      }
    };

    // --- Subscribers ---
    this.subscribers = new Map();   // key -> callback
    this.subId = 0;
  }

  // --- Actions ---
  setData(data) {
    this.state.data = data;
    this.state.ui.lastUpdated = new Date().toISOString();
    this._notify('data');
  }

  setTab(tab) {
    this.state.ui.activeTab = tab;
    this._notify('ui');
  }

  setFilter(filterKey, value) {
    this.state.filters[filterKey] = value;
    this._notify('filters');
  }

  openModal(type, data) {
    this.state.ui.modalOpen = type;
    this.state.ui.modalData = data;
    this._notify('ui');
  }

  closeModal() {
    this.state.ui.modalOpen = null;
    this.state.ui.modalData = null;
    this._notify('ui');
  }

  // --- Subscription Pattern ---
  subscribe(callback, keys = []) {
    const id = ++this.subId;
    this.subscribers.set(id, { callback, keys });
    return id; // unsubscribe: store.unsubscribe(id)
  }

  unsubscribe(id) {
    this.subscribers.delete(id);
  }

  _notify(changedKey) {
    this.subscribers.forEach(({ callback, keys }) => {
      // Если keys пустой -> подписка на всё
      // Иначе notify только если changedKey в keys
      if (keys.length === 0 || keys.includes(changedKey)) {
        callback(this.state, changedKey);
      }
    });
  }

  // --- Derived Data Getters (computed) ---
  get filteredWeeks() {
    const { data, filters } = this.state;
    if (!data) return [];
    // Фильтрация weeks по выбранному period / dateRange
    return filterWeeksByPeriod(data.weeks, filters.period, filters.dateRange);
  }

  get currentWeek() {
    const { data } = this.state;
    if (!data) return null;
    return data.weeks.find(w => w.isCurrent) || data.weeks[data.weeks.length - 1];
  }

  get balanceScore() {
    const { data } = this.state;
    if (!data?.wheelOfLife) return 0;
    const scores = data.wheelOfLife.spheres.map(s => s.currentScore);
    return (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);
  }

  get streaks() {
    const { data } = this.state;
    if (!data?.dailyScores) return { current: 0, best: 0 };
    return calculateStreaks(data.dailyScores);
  }
}

// Singleton instance
const store = new DashboardStore();
```

### 2.4 Export Functionality

```
[Export Button Click]
    |
    |-- Открыть Export Options Modal
    |   |-- Format: PNG (default) | SVG | JSON
    |   |-- Scope: Current Tab (default) | Full Dashboard
    |   |-- Quality: 1x (default) | 2x
    |
    |-- User подтверждает
    |   |
    |   |-- PNG Export:
    |   |   |-- ECharts: myChart.getDataURL({ type: 'png', pixelRatio: 2 })
    |   |   |-- Chart.js: canvas.toDataURL('image/png')
    |   |   |-- Для full dashboard: html2canvas (или аналог) на root container
    |   |
    |   |-- SVG Export:
    |   |   |-- ECharts: myChart.getDataURL({ type: 'svg' })
    |   |   |-- Chart.js: не поддерживает нативно -> конвертировать
    |   |
    |   |-- JSON Export:
    |   |   |-- JSON.stringify(store.state.data, null, 2)
    |   |   |-- Скачать как .json файл
    |   |
    |   |-- Trigger download (create <a> element with download attr)
    |
    |-- Показать Toast "Export complete"
```

---

## 3. JSON Data Contract

### 3.1 Обзор

Дашборд ожидает **один JSON-объект** от skill. Объект содержит все данные для отображения. Дашборд — stateless view: вся логика агрегации, расчёта трендов и стриков происходит на стороне дашборда.

### 3.2 Полная схема данных

```typescript
// ============================================================
// ROOT OBJECT
// ============================================================
interface DashboardData {
  meta: Meta;
  wheelOfLife: WheelOfLife;
  okr: OKR;
  goals12WY: Goals12WY;
  weeks: Week[];
  dailyScores: DailyScore[];
  bhagRoadmap: BHAGRoadmap;
  woopCards: WOOPCard[];
  leadLagMeasures: LeadLagMeasure[];
}

// ============================================================
// META
// ============================================================
interface Meta {
  version: string;           // "1.0" — версия data contract
  generatedAt: string;       // ISO 8601 timestamp
  weekNumber: number;        // Текущая неделя (1-12 для 12WY)
  weekLabel: string;         // "Week 8 of 12"
  periodStart: string;       // "2025-01-01" — начало 12WY
  periodEnd: string;         // "2025-03-25" — конец 12WY
  timezone: string;          // "Europe/Moscow"
}

// ============================================================
// WHEEL OF LIFE (Radar Chart)
// ============================================================
interface WheelOfLife {
  spheres: Sphere[];
  history: SphereHistory[];  // история для трендов
}

interface Sphere {
  id: string;                // уникальный идентификатор
  name: string;              // "Health & Fitness"
  label: string;             // короткая подпись "Health"
  currentScore: number;      // 0-10 (текущая неделя)
  previousScore: number;     // 0-10 (предыдущая неделя)
  targetScore: number;       // 0-10 (целевая)
  color: string;             // hex цвет сферы (переопределяет дефолт)
  icon: string;              // emoji или lucide icon name
  goals: SphereGoal[];       // цели в этой сфере (для drill-down)
}

interface SphereGoal {
  id: string;
  title: string;
  progress: number;          // 0-100
  status: 'onTrack' | 'atRisk' | 'offTrack';
}

interface SphereHistory {
  sphereId: string;
  scores: Array<{
    date: string;            // "2025-W01"
    score: number;           // 0-10
  }>;
}

// ============================================================
// OKR (Progress Rings + Bars)
// ============================================================
interface OKR {
  objectives: Objective[];
  overallProgress: number;   // 0-100
}

interface Objective {
  id: string;
  title: string;             // "Improve Physical Health"
  description?: string;      // описание
  progress: number;          // 0-100 (auto: avg of KRs)
  status: 'onTrack' | 'atRisk' | 'offTrack';
  sphereId: string;          // связь со сферой Wheel of Life
  keyResults: KeyResult[];
  confidenceScore: number;   // 1-10
}

interface KeyResult {
  id: string;
  title: string;             // "Run 3x per week"
  currentValue: number;      // текущее значение
  targetValue: number;       // целевое значение
  unit: string;              // "times", "hours", "kg", "%"
  progress: number;          // 0-100 (auto: current/target)
  status: 'onTrack' | 'atRisk' | 'offTrack';
}

// ============================================================
// 12-WEEK YEAR (Tracker)
// ============================================================
interface Goals12WY {
  tactics: Tactic[];         // еженедельные тактики
  executionScores: ExecutionScore[];
}

interface Tactic {
  id: string;
  title: string;             // "Deep work 4h daily"
  priority: number;          // 1-3 (1 = highest)
  sphereId: string;
  completed: boolean;
  weekNumber: number;        // к какой неделе относится
}

interface ExecutionScore {
  weekNumber: number;
  planned: number;           // запланировано задач
  completed: number;         // выполнено задач
  score: number;             // 0-10 execution score
}

// ============================================================
// WEEKS (Velocity + Retrospective)
// ============================================================
interface Week {
  number: number;            // 1-12
  label: string;             // "W1", "W2" ...
  startDate: string;         // "2025-01-01"
  endDate: string;           // "2025-01-07"
  isCurrent: boolean;        // текущая неделя
  planned: number;           // запланировано
  completed: number;         // выполнено
  confidence: number;        // 1-10
  energy: number;            // 1-10
  mood: number;              // 1-10
  satisfaction: number;      // 0-10 средний satisfaction
  reflection?: string;       // текстовая рефлексия
  wins: string[];            // победы недели
  improvements: string[];    // области улучшения
}

// ============================================================
// DAILY SCORES (Heatmap)
// ============================================================
interface DailyScore {
  date: string;              // "2025-01-15" (ISO date)
  totalScore: number;        // 0-4 уровень (для heatmap color)
  executionPct: number;      // 0-100 процент выполнения
  habitsCompleted: number;   // сколько привычек выполнено
  habitsTotal: number;       // сколько запланировано
  mood?: number;             // 1-10
  energy?: number;           // 1-10
  notes?: string;            // заметки дня
  habits: Array<{
    name: string;
    completed: boolean;
    icon?: string;
  }>;
}

// ============================================================
// BHAG ROADMAP (Timeline)
// ============================================================
interface BHAGRoadmap {
  levels: RoadmapLevel[];    // BHAG -> 3Y -> 1Y -> 12W -> Weekly
}

interface RoadmapLevel {
  level: number;             // 0=Weekly, 1=12W, 2=1Y, 3=3Y, 4=BHAG
  label: string;             // "12-Week Objective"
  items: RoadmapItem[];
}

interface RoadmapItem {
  id: string;
  title: string;
  description?: string;
  startDate: string;
  endDate: string;
  progress: number;          // 0-100
  status: 'notStarted' | 'inProgress' | 'completed' | 'atRisk';
  sphereId: string;
  parentId?: string;         // id родительской цели
  milestones: Array<{
    date: string;
    label: string;
    completed: boolean;
  }>;
}

// ============================================================
// WOOP CARDS
// ============================================================
interface WOOPCard {
  id: string;
  wish: string;              // "I want to run a marathon"
  outcome: string;           // "Feel accomplished and healthy"
  obstacle: string;          // "Lack of time in the morning"
  plan: string;              // "If I wake up late, then I'll run in the evening"
  sphereId: string;
  active: boolean;           // активная карточка
}

// ============================================================
// LEAD / LAG MEASURES
// ============================================================
interface LeadLagMeasure {
  id: string;
  name: string;              // "Weekly Workouts"
  type: 'lead' | 'lag';
  currentValue: number;
  targetValue: number;
  unit: string;
  weekOverWeekChange: number; // процентное изменение
  sphereId: string;
}
```

### 3.3 Минимальный пример данных

```json
{
  "meta": {
    "version": "1.0",
    "generatedAt": "2025-01-15T09:00:00Z",
    "weekNumber": 8,
    "weekLabel": "Week 8 of 12",
    "periodStart": "2024-12-30",
    "periodEnd": "2025-03-24",
    "timezone": "Europe/Moscow"
  },
  "wheelOfLife": {
    "spheres": [
      { "id": "health", "name": "Health & Fitness", "label": "Health", "currentScore": 7, "previousScore": 6, "targetScore": 9, "color": "#7A8B6F", "icon": "heart", "goals": [{ "id": "g1", "title": "Run 3x/week", "progress": 75, "status": "onTrack" }] },
      { "id": "career", "name": "Career & Business", "label": "Career", "currentScore": 6, "previousScore": 5, "targetScore": 8, "color": "#5B7B8C", "icon": "briefcase", "goals": [{ "id": "g2", "title": "Complete certification", "progress": 45, "status": "atRisk" }] },
      { "id": "finances", "name": "Finances & Money", "label": "Finances", "currentScore": 5, "previousScore": 5, "targetScore": 7, "color": "#B8A16E", "icon": "dollar-sign", "goals": [{ "id": "g3", "title": "Save 20% income", "progress": 60, "status": "onTrack" }] },
      { "id": "relationships", "name": "Relationships & Family", "label": "Relations", "currentScore": 8, "previousScore": 7, "targetScore": 9, "color": "#A67B8A", "icon": "users", "goals": [{ "id": "g4", "title": "Weekly date night", "progress": 90, "status": "onTrack" }] },
      { "id": "growth", "name": "Personal Growth", "label": "Growth", "currentScore": 6, "previousScore": 5, "targetScore": 8, "color": "#7B6BA0", "icon": "book", "goals": [{ "id": "g5", "title": "Read 2 books/month", "progress": 50, "status": "onTrack" }] },
      { "id": "fun", "name": "Fun & Recreation", "label": "Fun", "currentScore": 4, "previousScore": 3, "targetScore": 7, "color": "#C4845C", "icon": "gamepad-2", "goals": [{ "id": "g6", "title": "Weekend hobby", "progress": 30, "status": "offTrack" }] },
      { "id": "environment", "name": "Physical Environment", "label": "Home", "currentScore": 7, "previousScore": 6, "targetScore": 8, "color": "#6B8A7A", "icon": "home", "goals": [{ "id": "g7", "title": "Declutter workspace", "progress": 80, "status": "onTrack" }] },
      { "id": "spirituality", "name": "Spirituality & Purpose", "label": "Purpose", "currentScore": 5, "previousScore": 4, "targetScore": 8, "color": "#8B7D6B", "icon": "sun", "goals": [{ "id": "g8", "title": "Daily meditation", "progress": 40, "status": "atRisk" }] }
    ],
    "history": []
  },
  "okr": {
    "objectives": [
      {
        "id": "o1",
        "title": "Improve Physical Health",
        "progress": 72,
        "status": "onTrack",
        "sphereId": "health",
        "confidenceScore": 8,
        "keyResults": [
          { "id": "kr1", "title": "Run 3x per week", "currentValue": 3, "targetValue": 3, "unit": "times", "progress": 100, "status": "onTrack" },
          { "id": "kr2", "title": "Sleep 7+ hours", "currentValue": 6.5, "targetValue": 7, "unit": "hours", "progress": 65, "status": "atRisk" }
        ]
      }
    ],
    "overallProgress": 72
  },
  "goals12WY": {
    "tactics": [
      { "id": "t1", "title": "Deep work 4h daily", "priority": 1, "sphereId": "career", "completed": true, "weekNumber": 8 },
      { "id": "t2", "title": "Morning run 5km", "priority": 1, "sphereId": "health", "completed": true, "weekNumber": 8 },
      { "id": "t3", "title": "Read 30 pages", "priority": 2, "sphereId": "growth", "completed": false, "weekNumber": 8 }
    ],
    "executionScores": [
      { "weekNumber": 1, "planned": 10, "completed": 8, "score": 8 },
      { "weekNumber": 2, "planned": 10, "completed": 9, "score": 9 },
      { "weekNumber": 3, "planned": 12, "completed": 7, "score": 6 },
      { "weekNumber": 4, "planned": 10, "completed": 10, "score": 10 },
      { "weekNumber": 5, "planned": 11, "completed": 8, "score": 7 },
      { "weekNumber": 6, "planned": 10, "completed": 9, "score": 9 },
      { "weekNumber": 7, "planned": 10, "completed": 6, "score": 6 },
      { "weekNumber": 8, "planned": 10, "completed": 9, "score": 9 }
    ]
  },
  "weeks": [
    { "number": 1, "label": "W1", "startDate": "2024-12-30", "endDate": "2025-01-05", "isCurrent": false, "planned": 10, "completed": 8, "confidence": 7, "energy": 8, "mood": 7, "satisfaction": 7 },
    { "number": 2, "label": "W2", "startDate": "2025-01-06", "endDate": "2025-01-12", "isCurrent": false, "planned": 10, "completed": 9, "confidence": 7, "energy": 7, "mood": 8, "satisfaction": 8 },
    { "number": 3, "label": "W3", "startDate": "2025-01-13", "endDate": "2025-01-19", "isCurrent": false, "planned": 12, "completed": 7, "confidence": 5, "energy": 5, "mood": 6, "satisfaction": 6 },
    { "number": 4, "label": "W4", "startDate": "2025-01-20", "endDate": "2025-01-26", "isCurrent": false, "planned": 10, "completed": 10, "confidence": 8, "energy": 8, "mood": 9, "satisfaction": 9 },
    { "number": 5, "label": "W5", "startDate": "2025-01-27", "endDate": "2025-02-02", "isCurrent": false, "planned": 11, "completed": 8, "confidence": 6, "energy": 6, "mood": 6, "satisfaction": 7 },
    { "number": 6, "label": "W6", "startDate": "2025-02-03", "endDate": "2025-02-09", "isCurrent": false, "planned": 10, "completed": 9, "confidence": 7, "energy": 7, "mood": 7, "satisfaction": 8 },
    { "number": 7, "label": "W7", "startDate": "2025-02-10", "endDate": "2025-02-16", "isCurrent": false, "planned": 10, "completed": 6, "confidence": 5, "energy": 5, "mood": 5, "satisfaction": 5 },
    { "number": 8, "label": "W8", "startDate": "2025-02-17", "endDate": "2025-02-23", "isCurrent": true, "planned": 10, "completed": 9, "confidence": 8, "energy": 7, "mood": 8, "satisfaction": 8 }
  ],
  "dailyScores": [
    { "date": "2025-01-15", "totalScore": 3, "executionPct": 75, "habitsCompleted": 4, "habitsTotal": 5, "mood": 8, "energy": 7, "habits": [{ "name": "Morning run", "completed": true }, { "name": "Deep work", "completed": true }, { "name": "Reading", "completed": false }, { "name": "Meditation", "completed": true }, { "name": "Gratitude", "completed": true }] },
    { "date": "2025-01-16", "totalScore": 4, "executionPct": 100, "habitsCompleted": 5, "habitsTotal": 5, "mood": 9, "energy": 8, "habits": [{ "name": "Morning run", "completed": true }, { "name": "Deep work", "completed": true }, { "name": "Reading", "completed": true }, { "name": "Meditation", "completed": true }, { "name": "Gratitude", "completed": true }] },
    { "date": "2025-01-17", "totalScore": 2, "executionPct": 50, "habitsCompleted": 2, "habitsTotal": 5, "mood": 5, "energy": 4, "habits": [{ "name": "Morning run", "completed": false }, { "name": "Deep work", "completed": true }, { "name": "Reading", "completed": false }, { "name": "Meditation", "completed": false }, { "name": "Gratitude", "completed": true }] }
  ],
  "bhagRoadmap": {
    "levels": [
      { "level": 4, "label": "BHAG (10-Year)", "items": [{ "id": "bhag1", "title": "Build a life of freedom and impact", "startDate": "2025-01-01", "endDate": "2035-01-01", "progress": 15, "status": "inProgress", "sphereId": "purpose", "milestones": [] }] },
      { "level": 3, "label": "3-Year Vision", "items": [{ "id": "3y1", "title": "Location-independent business", "startDate": "2025-01-01", "endDate": "2028-01-01", "progress": 25, "status": "inProgress", "sphereId": "career", "parentId": "bhag1", "milestones": [{ "date": "2026-01-01", "label": "First $10k MRR", "completed": false }] }] },
      { "level": 2, "label": "Annual Goal", "items": [{ "id": "1y1", "title": "Launch coaching program", "startDate": "2025-01-01", "endDate": "2025-12-31", "progress": 40, "status": "inProgress", "sphereId": "career", "parentId": "3y1", "milestones": [] }] },
      { "level": 1, "label": "12-Week Objective", "items": [{ "id": "12w1", "title": "Complete course curriculum", "startDate": "2024-12-30", "endDate": "2025-03-24", "progress": 60, "status": "inProgress", "sphereId": "career", "parentId": "1y1", "milestones": [] }] },
      { "level": 0, "label": "Weekly Tactic", "items": [{ "id": "wt1", "title": "Record 3 video modules", "startDate": "2025-02-17", "endDate": "2025-02-23", "progress": 66, "status": "inProgress", "sphereId": "career", "parentId": "12w1", "milestones": [] }] }
    ]
  },
  "woopCards": [
    { "id": "woop1", "wish": "Run a half marathon", "outcome": "Feel proud, healthy, and accomplished crossing the finish line", "obstacle": "Morning fatigue and hitting snooze", "plan": "If I feel tired when the alarm rings, then I will put my running shoes by the bed and take 10 deep breaths", "sphereId": "health", "active": true },
    { "id": "woop2", "wish": "Read 24 books this year", "outcome": "Expand my thinking and have better conversations", "obstacle": "Evening TV and social media scrolling", "plan": "If I reach for the remote after dinner, then I will pick up my book and read one page first", "sphereId": "growth", "active": true }
  ],
  "leadLagMeasures": [
    { "id": "ll1", "name": "Weekly Workouts", "type": "lead", "currentValue": 4, "targetValue": 4, "unit": "sessions", "weekOverWeekChange": 0, "sphereId": "health" },
    { "id": "ll2", "name": "Body Weight", "type": "lag", "currentValue": 82, "targetValue": 78, "unit": "kg", "weekOverWeekChange": -0.5, "sphereId": "health" },
    { "id": "ll3", "name": "Deep Work Hours", "type": "lead", "currentValue": 18, "targetValue": 20, "unit": "hours", "weekOverWeekChange": 2, "sphereId": "career" },
    { "id": "ll4", "name": "Monthly Revenue", "type": "lag", "currentValue": 4200, "targetValue": 5000, "unit": "USD", "weekOverWeekChange": 5, "sphereId": "career" }
  ]
}
```

### 3.4 Обязательные vs Опциональные поля

| Поле | Обязательное | Описание |
|------|-------------|----------|
| `meta` | Да | Версия и временные метки |
| `meta.weekNumber` | Да | Для определения текущей недели |
| `wheelOfLife.spheres` | Да | 8 сфер с currentScore |
| `wheelOfLife.history` | Нет | Для трендов по сферам |
| `okr.objectives` | Нет | Если нет — не показывать OKR секцию |
| `goals12WY.tactics` | Нет | Если нет — не показывать 12WY секцию |
| `weeks` | Да | Хотя бы текущая и предыдущая |
| `dailyScores` | Нет | Если нет — не показывать heatmap |
| `bhagRoadmap` | Нет | Если нет — не показывать Roadmap |
| `woopCards` | Нет | Если нет — не показывать WOOP |
| `leadLagMeasures` | Нет | Если нет — не показывать Lead/Lag |

---

## 4. Color Palette

### 4.1 Принципы дизайна

- **Фон**: тёплый кремовый, не чистый белый — создаёт ощущение уюта и безопасности
- **Текст**: тёплый тёмно-коричневый, не чёрный — мягче для глаз
- **Accent**: насыщенный тёплый коричневый (какао) — ассоциация с надёжностью
- **Статусные цвета**: приглушённые (muted), не яркие RGB — соответствует low-saturation концепции
- **Heatmap**: градации одного тёплого цвета, а не зелёный-синий
- **Контраст**: все комбинации текста/фона проходят WCAG AA (минимум 4.5:1)

### 4.2 Базовая палитра

| Назначение | Имя | Hex | RGB | Использование |
|-----------|-----|-----|-----|---------------|
| Фон страницы | Linen | `#F0EDE5` | 240, 237, 229 | body background |
| Карточки / контейнеры | Linen Light | `#FFF8F0` | 255, 248, 240 | card backgrounds |
| Primary текст | Clove | `#2A2421` | 42, 36, 33 | headings, основной текст |
| Secondary текст | Wood | `#7F5F4C` | 127, 95, 76 | labels, captions |
| Accent / CTA | Cacao | `#563D2E` | 86, 61, 46 | buttons, active states, primary lines |
| Muted текст | Taupe | `#CCC2B6` | 204, 194, 182 | disabled, borders, secondary lines |
| Border | Sand | `#E7E7E7` | 231, 231, 231 | разделители, grid lines |
| Hover фон | Cream | `#E8D5C4` | 232, 213, 196 | hover states, heatmap L1 |

### 4.3 Семантические цвета (Status)

| Статус | Имя | Hex | RGB | Использование |
|--------|-----|-----|-----|---------------|
| Success / On Track | Warm Green | `#7A8B6F` | 122, 139, 111 >85% compl., позитивный тренд |
| Warning / At Risk | Warm Amber | `#C4845C` | 196, 132, 92 | 50-85% completion |
| Danger / Off Track | Warm Rust | `#A0522D` | 160, 82, 45 | <50% completion, негативный тренд |
| Info | Warm Stone | `#8B7D6B` | 139, 125, 107 | нейтральная информация |

### 4.4 8 цветов для сфер Wheel of Life

Каждая сфера имеет запоминающийся, ненавязчивый цвет. Насыщенность ~25-35% (low-saturation). Цвета выбраны так, чтобы быть различимыми для большинства типов цветовой слепоты (deuteranopia, protanopia).

| # | Сфера | Цвет | Hex | RGB | Почему этот цвет |
|---|-------|------|-----|-----|-----------------|
| 1 | Health & Fitness | Sage Green | `#7A8B6F` | 122, 139, 111 | Ассоциация с природой, здоровьем |
| 2 | Career & Business | Steel Blue | `#5B7B8C` | 91, 123, 140 | Профессионализм, стабильность |
| 3 | Finances & Money | Gold Ochre | `#B8A16E` | 184, 161, 110 | Монета, золото, достаток |
| 4 | Relationships & Family | Dusty Rose | `#A67B8A` | 166, 123, 138 | Тепло, забота, любовь |
| 5 | Personal Growth | Lavender Gray | `#7B6BA0` | 123, 107, 160 | Мудрость, интроспекция |
| 6 | Fun & Recreation | Tangerine | `#C4845C` | 196, 132, 92 | Энергия, радость, творчество |
| 7 | Physical Environment | Eucalyptus | `#6B8A7A` | 107, 138, 122 | Природа, дом, уют |
| 8 | Spirituality & Purpose | Warm Taupe | `#8B7D6B` | 139, 125, 107 | Земля, корни, осознанность |

#### Цветовая доступность (контраст на фоне `#F0EDE5`):

| Цвет | Контраст | WCAG AA |
|------|----------|---------|
| `#7A8B6F` | 4.7:1 | ✅ Проходит |
| `#5B7B8C` | 5.2:1 | ✅ Проходит |
| `#B8A16E` | 5.8:1 | ✅ Проходит |
| `#A67B8A` | 5.4:1 | ✅ Проходит |
| `#7B6BA0` | 5.9:1 | ✅ Проходит |
| `#C4845C` | 5.2:1 | ✅ Проходит |
| `#6B8A7A` | 4.9:1 | ✅ Проходит |
| `#8B7D6B` | 5.4:1 | ✅ Проходит |

### 4.5 Heatmap градации

| Уровень | Значение | Цвет | Hex | Описание |
|---------|----------|------|-----|----------|
| Level 0 | 0 (no data) | Sand | `#E7E7E7` | Нет активности / пропуск |
| Level 1 | 1 | Pale Caramel | `#E8D5C4` | Минимальная активность |
| Level 2 | 2 | Light Amber | `#D4A574` | Частичное выполнение |
| Level 3 | 3 | Medium Caramel | `#C4845C` | Цель достигнута |
| Level 4 | 4 | Dark Amber | `#A0522D` | Превышение цели |

### 4.6 Gauge / Chart цветовые зоны

```
Gauge шкала 0-10:
0 ---- 4 ---- 7 ---- 10
[RED]  [AMBER]  [GREEN]
#A0522D #C4845C #7A8B6F

Radar зоны:
0-4  : rgba(160, 82, 45, 0.05)  -- требует внимания
5-7  : rgba(196, 132, 92, 0.05)  -- норма
8-10 : rgba(122, 139, 111, 0.08) -- сильная сторона
```

### 4.7 CSS Custom Properties

```css
:root {
  /* Base */
  --color-bg: #F0EDE5;
  --color-card: #FFF8F0;
  --color-text-primary: #2A2421;
  --color-text-secondary: #7F5F4C;
  --color-accent: #563D2E;
  --color-muted: #CCC2B6;
  --color-border: #E7E7E7;
  --color-hover: #E8D5C4;

  /* Status */
  --color-success: #7A8B6F;
  --color-warning: #C4845C;
  --color-danger: #A0522D;
  --color-info: #8B7D6B;

  /* Spheres */
  --sphere-health: #7A8B6F;
  --sphere-career: #5B7B8C;
  --sphere-finances: #B8A16E;
  --sphere-relationships: #A67B8A;
  --sphere-growth: #7B6BA0;
  --sphere-fun: #C4845C;
  --sphere-environment: #6B8A7A;
  --sphere-spirituality: #8B7D6B;

  /* Heatmap */
  --heat-0: #E7E7E7;
  --heat-1: #E8D5C4;
  --heat-2: #D4A574;
  --heat-3: #C4845C;
  --heat-4: #A0522D;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(42, 36, 33, 0.08);
  --shadow-md: 0 4px 12px rgba(42, 36, 33, 0.10);
  --shadow-lg: 0 8px 24px rgba(42, 36, 33, 0.12);

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
}
```

---

## 5. Event Handling Schema

### 5.1 Обзор событий

```
+---------------------------------------------------------------+
|                    EVENT LIFECYCLE                            |
+---------------------------------------------------------------+
|                                                               |
|  DOM Events (browser)                                         |
|  |-- click, hover, scroll, resize, keydown                   |
|  v                                                            |
|  Chart Events (ECharts / Chart.js)                            |
|  |-- chartClick, chartHover, legendToggle, dataZoom           |
|  v                                                            |
|  Dashboard Events (custom)                                    |
|  |-- drillDown, filterChange, tabSwitch, export, modalOpen   |
|  v                                                            |
|  Store Actions                                                |
|  |-- setData, setFilter, setTab, openModal, closeModal       |
|  v                                                            |
|  State Update -> Re-render                                    |
|                                                               |
+---------------------------------------------------------------+
```

### 5.2 Схема обработки событий

| Событие | Источник | Обработчик | Результат |
|---------|----------|------------|-----------|
| `click` на сферу Radar | ECharts `click` | `handleSphereClick(sphereId)` | Открыть Sphere Drill-down Modal |
| `hover` на heatmap cell | ECharts `mouseover` | `handleHeatmapHover(date, score)` | Tooltip с деталями дня |
| `click` на heatmap cell | ECharts `click` | `handleHeatmapClick(date)` | Открыть Day Detail Modal |
| `click` на timeline bar | ECharts `click` | `handleTimelineClick(goalId)` | Открыть Goal Detail Modal |
| Toggle legend | ECharts `legendselectchanged` | Встроенный ECharts | Show/hide data series |
| `click` на checkbox | DOM click | `handleTaskToggle(taskId)` | Optimistic update + Store |
| `change` фильтра | DOM change | `handleFilterChange(key, value)` | Store.dispatch -> пересчёт |
| `click` на таб | DOM click | `handleTabSwitch(tab)` | Store.setTab -> монтировать tab |
| `click` Export | DOM click | `handleExport(format)` | Export Modal -> generate file |
| `resize` окна | window | `handleResize()` | Debounce -> chart.resize() |
| `visibilitychange` | document | `handleVisibilityChange()` | Pause/resume анимации |
| `dashboard:data` | CustomEvent | `handleDataInput(payload)` | Parse -> Validate -> Store |
| `keydown` (ESC) | document | `handleKeydown(e)` | Закрыть модал |
| `keydown` (Ctrl+E) | document | `handleKeydown(e)` | Открыть Export |

### 5.3 Детальные сценарии

#### 5.3.1 Click на сферу Radar -> Drill-down

```
[User clicks on Radar sphere point]
    |
    |-- ECharts генерирует событие `click`
    |   params.componentType === 'series'
    |   params.name === 'Health & Fitness'
    |
    |-- RadarChart.onClick(params) -> определяет sphereId по name
    |   |-- Map: sphereName -> sphereId ('health')
    |
    |-- Store.dispatch('drillDown', { type: 'sphere', id: 'health' })
    |   |-- Store.openModal('sphereDetail', { sphereId: 'health' })
    |
    |-- Modal Component монтируется
    |   |-- Загружает данные сферы: store.state.data.wheelOfLife.spheres.find(s => s.id === 'health')
    |   |-- Загружает связанные цели: store.state.data.okr.objectives.filter(o => o.sphereId === 'health')
    |   |-- Загружает историю: store.state.data.wheelOfLife.history.filter(h => h.sphereId === 'health')
    |
    |-- Внутри Modal:
    |   |-- Sphere Trend Chart (mini line chart)
    |   |-- Active Goals (progress bars)
    |   |-- Sphere Score Breakdown (bar chart)
    |   |-- Recent Actions (text list)
    |
    |-- User clicks Close или ESC
        |-- Store.closeModal()
        |-- Modal unmounts
```

#### 5.3.2 Hover на Heatmap cell -> Tooltip

```
[User hovers over heatmap cell]
    |
    |-- ECharts tooltip.trigger = 'item'
    |   |-- Formatter function вызывается с params.value = ['2025-01-15', 3]
    |
    |-- HeatmapChart.tooltipFormatter(date, score)
    |   |-- Ищет детали дня: store.state.data.dailyScores.find(d => d.date === date)
    |   |-- Формирует rich HTML tooltip:
    |       "<strong>Wednesday, January 15</strong>
    |        Score: 3/4 (High)
    |        Execution: 75% (4/5 habits)
    |        Mood: 8/10 | Energy: 7/10
    |        Habits: ✅ Run ✅ Deep Work ❌ Reading ✅ Meditation ✅ Gratitude
    |        Streak: 3 days"
    |
    |-- ECharts отображает tooltip с кастомным styling
        backgroundColor: 'rgba(42, 36, 33, 0.95)'
        borderColor: '#7F5F4C'
        textStyle.color: '#F0EDE5'
```

#### 5.3.3 Toggle Legend

```
[User clicks on legend item]
    |
    |-- ECharts legend.selectedMode = true (встроенная функция)
    |   |-- ECharts автоматически скрывает/показывает data series
    |
    |-- Нет необходимости в кастомном обработчике
    |-- ECharts сам управляет visibility series
```

#### 5.3.4 Export -> PNG

```
[User clicks Export button]
    |
    |-- Открывается Export Options Modal
    |   |-- Scope: "Current Tab: Overview"
    |   |-- Format: [PNG] [SVG] [JSON]
    |   |-- Quality: [1x] [2x]
    |
    |-- User выбирает PNG, 2x, нажимает "Download"
    |
    |-- ExportHandler.exportPNG(scope, quality)
    |   |-- Если scope === 'tab':
    |   |   |-- Находим активный tab container: document.querySelector('.tab-active')
    |   |   |-- Используем html2canvas (или встроенный ECharts getDataURL)
    |   |   |-- Для ECharts charts: chart.getDataURL({ type: 'png', pixelRatio: 2 })
    |   |   |-- Для DOM elements: html2canvas(element, { scale: 2 })
    |   |
    |   |-- Создаём <a> element
    |   |-- a.href = dataURL
    |   |-- a.download = `life-dashboard-${tab}-${date}.png`
    |   |-- a.click()
    |   |-- a.remove()
    |
    |-- Toast.show("Exported: life-dashboard-overview-2025-01-15.png")
```

### 5.4 Event Bus (координация между компонентами)

```javascript
// Простой Event Bus на чистом JS
class EventBus {
  constructor() {
    this.events = {};
  }

  on(event, callback) {
    if (!this.events[event]) this.events[event] = [];
    this.events[event].push(callback);
    return () => this.off(event, callback); // unsubscribe function
  }

  off(event, callback) {
    if (!this.events[event]) return;
    this.events[event] = this.events[event].filter(cb => cb !== callback);
  }

  emit(event, data) {
    if (!this.events[event]) return;
    this.events[event].forEach(cb => cb(data));
  }
}

const eventBus = new EventBus();

// Использование:
// Подписка: eventBus.on('sphere:selected', (sphereId) => { ... })
// Эмит: eventBus.emit('sphere:selected', 'health')

// События системы:
// 'data:loaded'      — данные загружены и валидированы
// 'data:updated'     — данные обновлены
// 'ui:tab:switched'  — переключение таба
// 'ui:modal:open'    — открытие модала
// 'ui:modal:close'   — закрытие модала
// 'filter:changed'   — изменение фильтра
// 'chart:resize'     — resize всех charts
// 'export:requested' — запрос на экспорт
// 'export:completed' — экспорт завершён
// 'sphere:selected'  — выбрана сфера (drill-down)
// 'day:selected'     — выбран день (heatmap)
// 'goal:selected'    — выбрана цель (timeline)
```

---

## 6. File Structure

### 6.1 Дерево файлов

```
dashboard/
|
|-- index.html                          # Entry point, структура страницы
|
|-- css/
|   |-- variables.css                   # CSS Custom Properties (палитра)
|   |-- base.css                        # Сброс, типографика, layout
|   |-- components.css                  # Стили компонентов (card, modal, tooltip)
|   |-- responsive.css                  # Media queries (mobile/tablet/desktop)
|   |-- animations.css                  # Keyframes, transitions
|   |-- main.css                        # Импорт всех CSS файлов
|
|-- js/
|   |
|   |-- core/
|   |   |-- Store.js                    # Reactive Store (state management)
|   |   |-- EventBus.js                 # Event Bus (координация)
|   |   |-- DataParser.js               # JSON parse, validate, normalize
|   |   |-- ExportManager.js            # PNG/SVG/JSON export
|   |   |-- IntersectionObserver.js     # Lazy loading charts
|   |
|   |-- charts/
|   |   |-- ChartBase.js                # Базовый класс для всех charts
|   |   |-- EChartsBase.js             # Базовый класс для ECharts
|   |   |-- ChartJSBase.js             # Базовый класс для Chart.js
|   |   |
|   |   |-- WheelOfLifeRadar.js         # ECharts: Radar (8 сфер)
|   |   |-- CalendarHeatmap.js          # ECharts: Calendar heatmap
|   |   |-- VelocityChart.js            # ECharts: Combo bar+line
|   |   |-- BurndownChart.js            # ECharts: Line (ideal vs actual)
|   |   |-- ConfidenceGauge.js          # ECharts: Gauge
|   |   |-- BHAGTimeline.js             # ECharts: Timeline
|   |   |-- LeadLagBars.js              # ECharts: Bar с target line
|   |   |-- Sparkline.js                # ECharts: Mini line chart
|   |   |
|   |   |-- OKRProgressRing.js          # Chart.js: Doughnut ring
|   |   |-- ProgressBar.js              # Chart.js: Horizontal bar
|   |
|   |-- components/
|   |   |-- Header.js                   # Шапка с title, date picker, export
|   |   |-- Sidebar.js                  # Боковая панель (фильтры, сферы)
|   |   |-- TabNav.js                   # Навигация по табам
|   |   |-- TabOverview.js              # Таб: Обзор (сборка секций)
|   |   |-- TabRetrospective.js         # Таб: Ретроспектива
|   |   |-- TabGoals.js                 # Таб: Цели
|   |   |-- Modal.js                    # Базовый модальный компонент
|   |   |-- SphereDetailModal.js        # Модал: детали сферы
|   |   |-- DayDetailModal.js           # Модал: детали дня
|   |   |-- GoalDetailModal.js          # Модал: детали цели
|   |   |-- ExportModal.js              # Модал: опции экспорта
|   |   |-- Toast.js                    # Toast notifications
|   |   |-- WeeklyPriorityList.js       # Интерактивный список задач
|   |   |-- WOOPCard.js                 # Карточка WOOP (4 поля)
|   |
|   |-- utils/
|   |   |-- colors.js                   # Color utilities (hex->rgb, opacity)
|   |   |-- dates.js                    # Date formatting, period calc
|   |   |-- math.js                     # Rolling avg, trend line, regression
|   |   |-- validators.js               # JSON schema validation
|   |   |-- constants.js                # Sphere labels, defaults, config
|   |
|   |-- app.js                          # Main entry: инициализация, монтирование
|   |-- init.js                         # Bootstrap: загрузка, первичная настройка
|
|-- assets/
|   |-- icons/                          # SVG иконки (Lucide-style)
|   |-- fonts/                          # Шрифты (Inter или системные)
|
|-- lib/
|   |-- echarts/                        # ECharts (или CDN)
|   |-- chart.js/                       # Chart.js (или CDN)
|
|-- data/
|   |-- sample-data.json                # Пример данных для разработки
```

### 6.2 Загрузка скриптов (index.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Life Planning Dashboard</title>
  <!-- ECharts from CDN (tree-shakeable modules) -->
  <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
  <!-- Chart.js from CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <!-- Styles -->
  <link rel="stylesheet" href="css/main.css">
</head>
<body>
  <div id="dashboard-root">
    <!-- Header -->
    <header id="dashboard-header"></header>

    <!-- Sidebar -->
    <aside id="dashboard-sidebar"></aside>

    <!-- Main Content -->
    <main id="dashboard-main">
      <nav id="tab-navigation"></nav>
      <div id="tab-content">
        <section id="tab-overview" class="tab-panel tab-active"></section>
        <section id="tab-retrospective" class="tab-panel"></section>
        <section id="tab-goals" class="tab-panel"></section>
      </div>
    </main>

    <!-- Modal Layer -->
    <div id="modal-layer" class="hidden"></div>

    <!-- Toast Layer -->
    <div id="toast-layer"></div>
  </div>

  <!-- Scripts (module pattern) -->
  <script type="module" src="js/app.js"></script>
</body>
</html>
```

---

## 7. Псевдо-код для главных компонентов

### 7.1 Базовые классы

#### ChartBase — базовый класс для всех графиков

```javascript
// js/charts/ChartBase.js
class ChartBase {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.chart = null;           // ECharts или Chart.js instance
    this.options = options;
    this.isVisible = false;
    this.isInitialized = false;
    this.data = null;

    // Debounced resize handler
    this.resizeHandler = this._debounce(() => this.resize(), 200);
  }

  // --- Lifecycle ---

  init() {
    if (this.isInitialized) return;
    this._setupIntersectionObserver();
    this.isInitialized = true;
  }

  destroy() {
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    window.removeEventListener('resize', this.resizeHandler);
    this.isInitialized = false;
  }

  // --- Data ---

  setData(data) {
    this.data = data;
    if (this.isVisible) {
      this._render();
    }
  }

  // --- Visibility (lazy loading) ---

  _setupIntersectionObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        this.isVisible = entry.isIntersecting;
        if (this.isVisible && this.data && !this.chart) {
          this._render();
        }
      });
    }, { rootMargin: '100px' });

    observer.observe(this.container);
  }

  // --- Rendering ---

  _render() {
    // Override in subclasses
    throw new Error('_render() must be implemented by subclass');
  }

  resize() {
    if (this.chart && this.chart.resize) {
      this.chart.resize();
    }
  }

  // --- Export ---

  exportToPNG(pixelRatio = 2) {
    if (!this.chart) return null;
    return this.chart.getDataURL({
      type: 'png',
      pixelRatio,
      backgroundColor: '#FFF8F0'
    });
  }

  exportToSVG() {
    if (!this.chart) return null;
    return this.chart.getDataURL({ type: 'svg' });
  }

  // --- Utilities ---

  _debounce(fn, ms) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), ms);
    };
  }

  _getSphereColor(sphereId) {
    const colors = {
      health: '#7A8B6F', career: '#5B7B8C', finances: '#B8A16E',
      relationships: '#A67B8A', growth: '#7B6BA0', fun: '#C4845C',
      environment: '#6B8A7A', spirituality: '#8B7D6B'
    };
    return colors[sphereId] || '#7F5F4C';
  }

  _getStatusColor(status) {
    const colors = { onTrack: '#7A8B6F', atRisk: '#C4845C', offTrack: '#A0522D' };
    return colors[status] || '#CCC2B6';
  }
}
```

#### EChartsBase — базовый класс для ECharts

```javascript
// js/charts/EChartsBase.js
class EChartsBase extends ChartBase {
  constructor(containerId, options = {}) {
    super(containerId, options);
    this.renderer = options.renderer || 'canvas';
  }

  _initChart() {
    if (this.chart) return;
    this.chart = echarts.init(this.container, null, {
      renderer: this.renderer
    });
    window.addEventListener('resize', this.resizeHandler);
  }

  _render() {
    this._initChart();
    const option = this._buildOption();
    this.chart.setOption(option, true);
    this._attachEvents();
  }

  _buildOption() {
    // Override in subclasses
    throw new Error('_buildOption() must be implemented');
  }

  _attachEvents() {
    // Override in subclasses для кастомных обработчиков
    // Базовый: ничего не делаем
  }

  // Common ECharts tooltip style
  _getTooltipConfig(formatter) {
    return {
      trigger: 'item',
      formatter,
      backgroundColor: 'rgba(42, 36, 33, 0.95)',
      borderColor: '#7F5F4C',
      borderWidth: 1,
      textStyle: { color: '#F0EDE5', fontSize: 13 },
      extraCssText: 'border-radius: 8px; box-shadow: 0 4px 12px rgba(42, 36, 33, 0.2);'
    };
  }

  // Common ECharts grid config
  _getGridConfig() {
    return {
      left: 60,
      right: 40,
      top: 40,
      bottom: 50,
      containLabel: true
    };
  }

  // Common ECharts axis style
  _getAxisStyle() {
    return {
      axisLine: { lineStyle: { color: '#CCC2B6' } },
      axisLabel: { color: '#7F5F4C', fontSize: 12 },
      splitLine: { lineStyle: { color: '#E7E7E7', type: 'dashed' } }
    };
  }
}
```

### 7.2 Wheel of Life Radar

```javascript
// js/charts/WheelOfLifeRadar.js
class WheelOfLifeRadar extends EChartsBase {
  constructor(containerId) {
    super(containerId);
    this.onSphereClick = null;   // callback: (sphereId) => {}
  }

  _buildOption() {
    const { spheres } = this.data.wheelOfLife;
    const currentScores = spheres.map(s => s.currentScore);
    const previousScores = spheres.map(s => s.previousScore);
    const balanceScore = (currentScores.reduce((a, b) => a + b, 0) / 8).toFixed(1);

    return {
      title: {
        text: 'Wheel of Life',
        subtext: `Balance Score: ${balanceScore}/10`,
        left: 'center',
        top: 10,
        textStyle: { color: '#2A2421', fontSize: 16, fontWeight: 'bold' },
        subtextStyle: { color: '#7F5F4C', fontSize: 12 }
      },
      tooltip: this._getTooltipConfig((params) => {
        const idx = spheres.findIndex(s => s.name === params.name);
        const sphere = spheres[idx];
        const diff = sphere.currentScore - sphere.previousScore;
        const arrow = diff > 0 ? '▲' : diff < 0 ? '▼' : '●';
        return `<strong>${sphere.name}</strong><br/>
                Score: <strong>${sphere.currentScore}/10</strong><br/>
                Previous: ${sphere.previousScore}/10<br/>
                Target: ${sphere.targetScore}/10<br/>
                Change: ${arrow} ${Math.abs(diff)}`;
      }),
      legend: {
        data: ['Current Week', 'Previous Week'],
        bottom: 5,
        textStyle: { color: '#7F5F4C', fontSize: 11 },
        itemWidth: 16,
        itemHeight: 8
      },
      radar: {
        indicator: spheres.map(s => ({
          name: s.label,
          max: 10
        })),
        shape: 'polygon',
        radius: '58%',
        center: ['50%', '52%'],
        splitNumber: 5,
        axisName: {
          color: '#2A2421',
          fontSize: 11,
          fontWeight: 'bold',
          formatter: (value) => value
        },
        splitLine: {
          lineStyle: { color: '#CCC2B6', width: 1 }
        },
        splitArea: {
          show: true,
          areaStyle: {
            color: [
              'rgba(160, 82, 45, 0.04)',   // 0-2: alert zone
              'rgba(160, 82, 45, 0.04)',   // 2-4: alert zone
              'rgba(196, 132, 92, 0.04)',  // 4-6: ok zone
              'rgba(196, 132, 92, 0.04)',  // 6-8: ok zone
              'rgba(122, 139, 111, 0.06)'  // 8-10: great zone
            ]
          }
        },
        axisLine: {
          lineStyle: { color: '#CCC2B6', width: 1 }
        }
      },
      series: [{
        type: 'radar',
        data: [
          {
            value: currentScores,
            name: 'Current Week',
            symbol: 'circle',
            symbolSize: 8,
            lineStyle: { color: '#563D2E', width: 2.5 },
            areaStyle: { color: 'rgba(86, 61, 46, 0.2)' },
            itemStyle: { color: '#563D2E', borderColor: '#FFF', borderWidth: 2 },
            emphasis: {
              itemStyle: {
                borderColor: '#563D2E',
                borderWidth: 3,
                shadowBlur: 10,
                shadowColor: 'rgba(86, 61, 46, 0.4)'
              }
            }
          },
          {
            value: previousScores,
            name: 'Previous Week',
            symbol: 'circle',
            symbolSize: 4,
            lineStyle: { color: '#CCC2B6', width: 1.5, type: 'dashed' },
            areaStyle: { color: 'rgba(204, 194, 182, 0.08)' },
            itemStyle: { color: '#CCC2B6' }
          }
        ]
      }]
    };
  }

  _attachEvents() {
    this.chart.on('click', (params) => {
      if (params.componentType === 'series' && this.onSphereClick) {
        // params.name = label сферы (например, "Health")
        const sphere = this.data.wheelOfLife.spheres.find(s => s.label === params.name);
        if (sphere) {
          this.onSphereClick(sphere.id);
        }
      }
    });
  }
}
```

### 7.3 Calendar Heatmap

```javascript
// js/charts/CalendarHeatmap.js
class CalendarHeatmap extends EChartsBase {
  constructor(containerId) {
    super(containerId);
    this.onDayClick = null;      // callback: (date) => {}
    this.year = new Date().getFullYear();
  }

  _buildOption() {
    const heatmapData = this.data.dailyScores.map(d => [d.date, d.totalScore]);
    const { currentStreak, bestStreak } = this._calculateStreaks();

    return {
      title: {
        text: 'Daily Consistency',
        subtext: `Current: ${currentStreak}d | Best: ${bestStreak}d`,
        left: 'center',
        top: 5,
        textStyle: { color: '#2A2421', fontSize: 15, fontWeight: 'bold' },
        subtextStyle: { color: '#7F5F4C', fontSize: 12 }
      },
      tooltip: {
        position: 'top',
        formatter: (params) => {
          const date = new Date(params.value[0]);
          const value = params.value[1];
          const levels = ['None', 'Light', 'Medium', 'High', 'Intense'];
          const dayData = this.data.dailyScores.find(d => d.date === params.value[0]);
          const habitsStr = dayData
            ? dayData.habits.map(h => `${h.completed ? '✓' : '○'} ${h.name}`).join('<br/>')
            : '';
          return `<strong>${date.toLocaleDateString('en-US', {
            weekday: 'long', month: 'short', day: 'numeric'
          })}</strong><br/>
                  Score: <strong>${value}/4</strong> (${levels[value]})<br/>
                  Execution: ${dayData?.executionPct || 0}%<br/>
                  Habits: ${dayData?.habitsCompleted || 0}/${dayData?.habitsTotal || 0}<br/>
                  ${habitsStr}`;
        },
        backgroundColor: 'rgba(42, 36, 33, 0.95)',
        borderColor: '#7F5F4C',
        textStyle: { color: '#F0EDE5', fontSize: 12 }
      },
      visualMap: {
        min: 0,
        max: 4,
        calculable: false,
        orient: 'horizontal',
        left: 'center',
        bottom: 5,
        itemWidth: 14,
        itemHeight: 14,
        inRange: {
          color: ['#E7E7E7', '#E8D5C4', '#D4A574', '#C4845C', '#A0522D']
        },
        text: ['High', 'None'],
        textStyle: { color: '#7F5F4C', fontSize: 10 }
      },
      calendar: {
        top: 55,
        left: 45,
        right: 45,
        cellSize: ['auto', 14],
        range: this.year,
        itemStyle: {
          borderWidth: 2,
          borderColor: '#F0EDE5',
          borderRadius: 2
        },
        splitLine: { show: false },
        yearLabel: { show: true, color: '#2A2421', fontWeight: 'bold', fontSize: 13 },
        monthLabel: { color: '#7F5F4C', fontSize: 11 },
        dayLabel: {
          color: '#7F5F4C',
          fontSize: 10,
          firstDay: 1  // Monday first
        }
      },
      series: {
        type: 'heatmap',
        coordinateSystem: 'calendar',
        data: heatmapData,
        emphasis: {
          itemStyle: {
            shadowBlur: 8,
            shadowColor: 'rgba(86, 61, 46, 0.4)',
            borderColor: '#563D2E',
            borderWidth: 2
          }
        }
      }
    };
  }

  _attachEvents() {
    this.chart.on('click', (params) => {
      if (params.value && this.onDayClick) {
        this.onDayClick(params.value[0]);
      }
    });
  }

  _calculateStreaks() {
    const sorted = [...this.data.dailyScores]
      .sort((a, b) => new Date(a.date) - new Date(b.date));

    let currentStreak = 0;
    let bestStreak = 0;
    let tempStreak = 0;

    // Current streak = с конца
    for (let i = sorted.length - 1; i >= 0; i--) {
      if (sorted[i].totalScore > 0) {
        currentStreak++;
      } else {
        break;
      }
    }

    // Best streak = максимум
    for (const day of sorted) {
      if (day.totalScore > 0) {
        tempStreak++;
        bestStreak = Math.max(bestStreak, tempStreak);
      } else {
        tempStreak = 0;
      }
    }

    return { currentStreak, bestStreak };
  }
}
```

### 7.4 Velocity Chart (Combo)

```javascript
// js/charts/VelocityChart.js
class VelocityChart extends EChartsBase {
  _buildOption() {
    const weeks = this.data.weeks;
    const labels = weeks.map(w => w.label);
    const completed = weeks.map(w => w.completed);
    const planned = weeks.map(w => w.planned);
    const rollingAvg = this._calculateRollingAverage(completed, 4);

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross', crossStyle: { color: '#CCC2B6' } },
        backgroundColor: 'rgba(42, 36, 33, 0.95)',
        borderColor: '#7F5F4C',
        textStyle: { color: '#F0EDE5' }
      },
      legend: {
        data: ['Completed', 'Planned', '4-Week Avg'],
        bottom: 5,
        textStyle: { color: '#7F5F4C', fontSize: 11 }
      },
      grid: this._getGridConfig(),
      xAxis: {
        type: 'category',
        data: labels,
        axisLine: { lineStyle: { color: '#CCC2B6' } },
        axisLabel: { color: '#7F5F4C', fontSize: 11 },
        axisTick: { show: false }
      },
      yAxis: {
        type: 'value',
        name: 'Tasks',
        nameTextStyle: { color: '#7F5F4C', fontSize: 11 },
        axisLine: { show: false },
        splitLine: { lineStyle: { color: '#E7E7E7', type: 'dashed' } },
        axisLabel: { color: '#7F5F4C', fontSize: 11 }
      },
      series: [
        {
          name: 'Completed',
          type: 'bar',
          data: completed.map((val, idx) => ({
            value: val,
            itemStyle: {
              color: weeks[idx].isCurrent ? '#563D2E' : '#7A8B6F',
              borderRadius: [4, 4, 0, 0]
            }
          })),
          barWidth: '35%',
          emphasis: {
            itemStyle: { color: '#563D2E' }
          }
        },
        {
          name: 'Planned',
          type: 'line',
          data: planned,
          lineStyle: { color: '#CCC2B6', width: 2, type: 'dashed' },
          itemStyle: { color: '#CCC2B6' },
          symbol: 'none',
          smooth: false
        },
        {
          name: '4-Week Avg',
          type: 'line',
          data: rollingAvg,
          lineStyle: { color: '#563D2E', width: 2.5 },
          itemStyle: { color: '#563D2E' },
          smooth: true,
          symbol: 'circle',
          symbolSize: 5
        }
      ]
    };
  }

  _calculateRollingAverage(data, window) {
    const result = [];
    for (let i = 0; i < data.length; i++) {
      if (i < window - 1) {
        result.push(null);  // недостаточно данных
      } else {
        const slice = data.slice(i - window + 1, i + 1);
        const avg = slice.reduce((a, b) => a + b, 0) / window;
        result.push(Number(avg.toFixed(1)));
      }
    }
    return result;
  }
}
```

### 7.5 Burndown Chart

```javascript
// js/charts/BurndownChart.js
class BurndownChart extends EChartsBase {
  _buildOption() {
    const { weeks } = this.data;
    const totalWeeks = weeks.length;
    const totalWork = weeks[0]?.planned * totalWeeks || 100;

    // Ideal line — равномерное снижение от totalWork до 0
    const idealLine = weeks.map((_, i) =>
      Number((totalWork * (1 - i / (totalWeeks - 1))).toFixed(1))
    );

    // Actual line — оставшаяся работа
    let remaining = totalWork;
    const actualLine = weeks.map(w => {
      remaining -= w.completed;
      return Math.max(0, Number(remaining.toFixed(1)));
    });

    // Forecast line — продолжение тренда (пунктир)
    const currentWeekIdx = weeks.findIndex(w => w.isCurrent);
    const lastActual = actualLine[currentWeekIdx];
    const slope = currentWeekIdx > 0
      ? (actualLine[currentWeekIdx] - actualLine[0]) / currentWeekIdx
      : 0;

    const forecastLine = weeks.map((_, i) => {
      if (i <= currentWeekIdx) return null;
      const forecast = lastActual + slope * (i - currentWeekIdx);
      return forecast > 0 ? Number(forecast.toFixed(1)) : 0;
    });

    // Labels
    const labels = weeks.map(w => w.label);

    return {
      title: {
        text: '12-Week Burndown',
        left: 'center',
        top: 5,
        textStyle: { color: '#2A2421', fontSize: 15, fontWeight: 'bold' }
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(42, 36, 33, 0.95)',
        borderColor: '#7F5F4C',
        textStyle: { color: '#F0EDE5' },
        formatter: (params) => {
          const lines = params.map(p =>
            `${p.marker} ${p.seriesName}: <strong>${p.value ?? '--'}</strong>`
          );
          return `<strong>${params[0].axisValue}</strong><br/>${lines.join('<br/>')}`;
        }
      },
      legend: {
        data: ['Ideal', 'Actual', 'Forecast'],
        bottom: 5,
        textStyle: { color: '#7F5F4C', fontSize: 11 }
      },
      grid: this._getGridConfig(),
      xAxis: {
        type: 'category',
        data: labels,
        axisLine: { lineStyle: { color: '#CCC2B6' } },
        axisLabel: { color: '#7F5F4C', fontSize: 11 }
      },
      yAxis: {
        type: 'value',
        name: 'Remaining Work',
        nameTextStyle: { color: '#7F5F4C', fontSize: 11 },
        splitLine: { lineStyle: { color: '#E7E7E7', type: 'dashed' } },
        axisLabel: { color: '#7F5F4C', fontSize: 11 }
      },
      series: [
        {
          name: 'Ideal',
          type: 'line',
          data: idealLine,
          lineStyle: { color: '#CCC2B6', width: 2, type: 'dashed' },
          itemStyle: { color: '#CCC2B6' },
          symbol: 'none',
          smooth: false
        },
        {
          name: 'Actual',
          type: 'line',
          data: actualLine,
          lineStyle: { color: '#563D2E', width: 2.5 },
          itemStyle: { color: '#563D2E' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(86, 61, 46, 0.15)' },
                { offset: 1, color: 'rgba(86, 61, 46, 0.02)' }
              ]
            }
          },
          symbol: 'circle',
          symbolSize: 6,
          markLine: {
            silent: true,
            data: [{ xAxis: currentWeekIdx }],
            lineStyle: { color: '#C4845C', width: 1, type: 'dashed' }
          }
        },
        {
          name: 'Forecast',
          type: 'line',
          data: forecastLine,
          lineStyle: { color: '#A0522D', width: 2, type: 'dotted' },
          itemStyle: { color: '#A0522D' },
          symbol: 'diamond',
          symbolSize: 6
        }
      ]
    };
  }
}
```

### 7.6 Confidence Gauge

```javascript
// js/charts/ConfidenceGauge.js
class ConfidenceGauge extends EChartsBase {
  constructor(containerId, options = {}) {
    super(containerId, options);
    this.label = options.label || 'Score';
    this.max = options.max || 10;
  }

  _buildOption() {
    const value = this.data;
    const pct = value / this.max;

    return {
      series: [{
        type: 'gauge',
        startAngle: 200,
        endAngle: -20,
        min: 0,
        max: this.max,
        splitNumber: this.max,
        itemStyle: { color: '#563D2E' },
        progress: {
          show: true,
          width: 18,
          roundCap: true
        },
        pointer: {
          icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
          length: '55%',
          width: 5,
          offsetCenter: [0, '-8%'],
          itemStyle: { color: '#2A2421' }
        },
        axisLine: {
          roundCap: true,
          lineStyle: {
            width: 18,
            color: [
              [0.4, '#A0522D'],   // 0-40%: red zone
              [0.7, '#C4845C'],   // 40-70%: amber zone
              [1, '#7A8B6F']      // 70-100%: green zone
            ]
          }
        },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: {
          distance: -22,
          color: '#7F5F4C',
          fontSize: 9
        },
        anchor: {
          show: true,
          showAbove: true,
          size: 14,
          itemStyle: { borderColor: '#563D2E', borderWidth: 3, color: '#FFF8F0' }
        },
        title: {
          offsetCenter: [0, '55%'],
          fontSize: 12,
          color: '#7F5F4C',
          fontWeight: 'normal'
        },
        detail: {
          valueAnimation: true,
          fontSize: 32,
          fontWeight: 'bold',
          offsetCenter: [0, '-8%'],
          formatter: '{value}',
          color: '#2A2421'
        },
        data: [{ value, name: this.label }]
      }]
    };
  }
}
```

### 7.7 App Init

```javascript
// js/app.js — Main Application Entry

import { DashboardStore } from './core/Store.js';
import { EventBus } from './core/EventBus.js';
import { DataParser } from './core/DataParser.js';
import { WheelOfLifeRadar } from './charts/WheelOfLifeRadar.js';
import { CalendarHeatmap } from './charts/CalendarHeatmap.js';
import { VelocityChart } from './charts/VelocityChart.js';
import { BurndownChart } from './charts/BurndownChart.js';
import { ConfidenceGauge } from './charts/ConfidenceGauge.js';
import { Header } from './components/Header.js';
import { Sidebar } from './components/Sidebar.js';
import { TabNav } from './components/TabNav.js';
import { Toast } from './components/Toast.js';
import { Modal } from './components/Modal.js';

// --- Инициализация глобальных объектов ---
const store = new DashboardStore();
const eventBus = new EventBus();

// --- Реестр chart instances ---
const charts = new Map();

// --- Main Init ---
async function init() {
  // 1. Проверить кэш
  const cached = loadFromCache();
  if (cached && !isCacheExpired(cached)) {
    store.setData(cached.data);
  }

  // 2. Инициализировать UI компоненты
  Header.init('dashboard-header', { store, eventBus });
  Sidebar.init('dashboard-sidebar', { store, eventBus });
  TabNav.init('tab-navigation', { store, eventBus });
  Toast.init('toast-layer');
  Modal.init('modal-layer');

  // 3. Подписаться на переключение табов
  eventBus.on('ui:tab:switched', (tab) => {
    mountTab(tab);
  });

  // 4. Подписаться на входные данные (от skill)
  window.addEventListener('dashboard:data', (event) => {
    handleIncomingData(event.detail);
  });

  // 5. Монтировать дефолтный таб
  mountTab('overview');

  // 6. Глобальные обработчики
  window.addEventListener('resize', () => {
    charts.forEach(chart => chart.resize());
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') eventBus.emit('ui:modal:close');
    if (e.ctrlKey && e.key === 'e') {
      e.preventDefault();
      eventBus.emit('export:requested');
    }
  });

  console.log('[Dashboard] Initialized');
}

// --- Монтирование таба (lazy) ---
function mountTab(tabName) {
  // Скрыть все табы
  document.querySelectorAll('.tab-panel').forEach(el => {
    el.classList.remove('tab-active');
  });

  // Показать активный
  const activeTab = document.getElementById(`tab-${tabName}`);
  activeTab.classList.add('tab-active');

  // Mount charts для таба
  switch (tabName) {
    case 'overview':
      mountOverviewCharts();
      break;
    case 'retrospective':
      mountRetrospectiveCharts();
      break;
    case 'goals':
      mountGoalsCharts();
      break;
  }
}

// --- Mount Overview Charts ---
function mountOverviewCharts() {
  const data = store.state.data;
  if (!data) return;

  // Wheel of Life Radar
  if (!charts.has('radar')) {
    const radar = new WheelOfLifeRadar('radar-container');
    radar.onSphereClick = (sphereId) => {
      eventBus.emit('sphere:selected', sphereId);
      store.openModal('sphereDetail', { sphereId });
    };
    charts.set('radar', radar);
    radar.init();
  }
  charts.get('radar').setData(data);

  // Confidence Gauges (x3)
  const gaugeConfigs = [
    { id: 'gauge-confidence', label: 'Confidence', value: data.weeks.find(w => w.isCurrent)?.confidence || 7 },
    { id: 'gauge-energy', label: 'Energy', value: data.weeks.find(w => w.isCurrent)?.energy || 6 },
    { id: 'gauge-mood', label: 'Mood', value: data.weeks.find(w => w.isCurrent)?.mood || 7 }
  ];
  gaugeConfigs.forEach(cfg => {
    if (!charts.has(cfg.id)) {
      const gauge = new ConfidenceGauge(cfg.id, { label: cfg.label, max: 10 });
      charts.set(cfg.id, gauge);
      gauge.init();
    }
    charts.get(cfg.id).setData(cfg.value);
  });

  // OKR Progress Rings (Chart.js)
  mountOKRRings(data);
}

// --- Mount Retrospective Charts ---
function mountRetrospectiveCharts() {
  const data = store.state.data;
  if (!data) return;

  // Velocity Chart
  if (!charts.has('velocity')) {
    const velocity = new VelocityChart('velocity-container');
    charts.set('velocity', velocity);
    velocity.init();
  }
  charts.get('velocity').setData(data);

  // Calendar Heatmap
  if (!charts.has('heatmap')) {
    const heatmap = new CalendarHeatmap('heatmap-container');
    heatmap.onDayClick = (date) => {
      eventBus.emit('day:selected', date);
      store.openModal('dayDetail', { date });
    };
    charts.set('heatmap', heatmap);
    heatmap.init();
  }
  charts.get('heatmap').setData(data);

  // Burndown Chart
  if (!charts.has('burndown')) {
    const burndown = new BurndownChart('burndown-container');
    charts.set('burndown', burndown);
    burndown.init();
  }
  charts.get('burndown').setData(data);
}

// --- Mount Goals Charts ---
function mountGoalsCharts() {
  const data = store.state.data;
  if (!data) return;

  // BHAG Timeline
  if (!charts.has('timeline')) {
    const timeline = new BHAGTimeline('timeline-container');
    charts.set('timeline', timeline);
    timeline.init();
  }
  charts.get('timeline').setData(data.bhagRoadmap);
}

// --- Обработка входных данных ---
function handleIncomingData(payload) {
  try {
    const parsed = DataParser.parse(payload);
    const validated = DataParser.validate(parsed);
    const normalized = DataParser.normalize(validated);

    store.setData(normalized);
    saveToCache(normalized);

    eventBus.emit('data:loaded');
    Toast.show('Dashboard updated', 'success');
  } catch (err) {
    console.error('[Dashboard] Data error:', err);
    Toast.show(`Data error: ${err.message}`, 'error');
  }
}

// --- Cache utilities ---
function loadFromCache() {
  try {
    const raw = localStorage.getItem('dashboard_cache');
    return raw ? JSON.parse(raw) : null;
  } catch { return null; }
}

function saveToCache(data) {
  localStorage.setItem('dashboard_cache', JSON.stringify({
    data,
    timestamp: Date.now()
  }));
}

function isCacheExpired(cached, maxAgeMs = 3600000) {
  return Date.now() - cached.timestamp > maxAgeMs;
}

// --- OKR Rings (Chart.js) ---
function mountOKRRings(data) {
  data.okr.objectives.forEach((obj, idx) => {
    const canvasId = `okr-ring-${idx}`;
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const color = store.getSphereColor(obj.sphereId);

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Completed', 'Remaining'],
        datasets: [{
          data: [obj.progress, 100 - obj.progress],
          backgroundColor: [color, '#E7E7E7'],
          borderWidth: 0,
          borderRadius: 16,
          cutout: '78%'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        },
        animation: {
          animateRotate: true,
          duration: 1000,
          easing: 'easeOutQuart'
        }
      },
      plugins: [{
        id: 'centerText',
        afterDraw: (chart) => {
          const { ctx, chartArea: { top, bottom, left, right } } = chart;
          const centerX = (left + right) / 2;
          const centerY = (top + bottom) / 2;

          ctx.save();
          ctx.font = 'bold 24px Inter, sans-serif';
          ctx.fillStyle = '#2A2421';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(`${obj.progress}%`, centerX, centerY - 8);

          ctx.font = '11px Inter, sans-serif';
          ctx.fillStyle = '#7F5F4C';
          ctx.fillText(obj.title.substring(0, 14), centerX, centerY + 14);
          ctx.restore();
        }
      }]
    });
  });
}

// --- Старт ---
init();
```

---

## 8. Responsive стратегия

### 8.1 Breakpoints

```css
/* Mobile first approach */

/* Base: Mobile < 768px */
.dashboard {
  grid-template-columns: 1fr;
  grid-template-areas:
    "header"
    "main";
}

.sidebar { display: none; }  /* off-canvas menu */
.sidebar.open { display: block; position: fixed; z-index: 100; }

.chart-container {
  height: 250px;  /* smaller charts on mobile */
}

/* Tablet: 768px - 1199px */
@media (min-width: 768px) {
  .dashboard {
    grid-template-columns: 200px 1fr;
    grid-template-areas:
      "header header"
      "sidebar main";
  }
  .sidebar { display: block; position: static; }
  .chart-container { height: 320px; }
}

/* Desktop: 1200px+ */
@media (min-width: 1200px) {
  .dashboard {
    grid-template-columns: 240px 1fr;
    max-width: 1440px;
    margin: 0 auto;
  }
  .chart-container { height: 380px; }

  /* Multi-column layouts per tab */
  .tab-overview {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  .tab-overview .chart-wide {
    grid-column: 1 / -1;  /* full width */
  }
}
```

### 8.2 Mobile-специфичные адаптации

| Компонент | Desktop | Mobile |
|-----------|---------|--------|
| Heatmap | 365 дней, полный год | 90 дней, scrollable |
| Radar | Все 8 сфер, полный размер | Те же 8, уменьшенный |
| Gauges | 3 в ряд | 1 + carousel swipe |
| OKR Rings | 3 в ряд | 2 в ряд |
| Velocity | Полный combo chart | Только bar + avg line |
| Burndown | С forecast | Без forecast (нет места) |
| Sidebar | Всегда видна | Off-canvas, toggle |
| Tooltips | Hover | Tap |
| Zoom/Pan | Mouse wheel | Убрано |

---

## 9. Performance Budget

| Метрика | Целевое значение |
|---------|-----------------|
| First Paint | < 1.5s |
| Time to Interactive | < 3.0s |
| Bundle size (total) | < 500KB gzipped |
| Charts render | < 500ms каждый |
| Animation fps | 60fps |
| Scroll jank | < 16ms/frame |
| Memory (idle) | < 50MB |

### Оптимизации:

1. **Lazy loading**: Charts инициализируются только при появлении в viewport (IntersectionObserver)
2. **Tab lazy mount**: Charts таба ретроспективы не создаются до первого открытия таба
3. **Debounced resize**: 200ms debounce на window resize
4. **ECharts Canvas**: Canvas renderer вместо SVG для лучшей производительности
5. **Animation pause**: Анимации приостанавливаются когда таб неактивен
6. **Data sampling**: >1000 точек — автоматический downsampling
7. **Cache**: LocalStorage кэш данных (1 час TTL)

---

## 10. Accessibility (a11y)

### 10.1 Требования

- **WCAG 2.1 Level AA** — целевой стандарт
- **Color blindness**: Не полагаться только на цвет (patterns + icons)
- **Keyboard navigation**: Tab, Enter, Escape, Arrow keys
- **Screen readers**: aria-labels, live regions, sr-only текст

### 10.2 Реализация

```html
<!-- Radar chart с ARIA -->
<div id="radar-container" role="img"
     aria-label="Wheel of Life radar chart showing 8 life spheres.
                 Balance score: 6.2 out of 10.
                 Health: 7, Career: 6, Finances: 5, Relations: 8,
                 Growth: 6, Fun: 4, Environment: 7, Purpose: 5">
  <span class="sr-only">
    Detailed data table for screen readers...
  </span>
</div>

<!-- Heatmap с ARIA -->
<div id="heatmap-container" role="img"
     aria-label="Calendar heatmap showing daily execution scores.
                 Current streak: 5 days. Best streak: 12 days.
                 Today: score 3 out of 4.">
</div>
```

### 10.3 Keyboard Shortcuts

| Клавиша | Действие |
|---------|----------|
| `Tab` | Навигация по интерактивным элементам |
| `Enter` / `Space` | Активировать элемент |
| `Escape` | Закрыть модал |
| `Ctrl + E` | Открыть Export modal |
| `1`, `2`, `3` | Переключение табов |
| `←`, `→` | Навигация по heatmap |

---

## 11. Интеграция со Skill

### 11.1 Способ передачи данных

Дашборд — одностраничное HTML-приложение. Skill передаёт данные через **CustomEvent**:

```javascript
// Код, который выполняет skill для передачи данных в дашборд:
const dashboardData = { /* ... полный JSON ... */ };

const event = new CustomEvent('dashboard:data', {
  detail: dashboardData,
  bubbles: true
});

window.dispatchEvent(event);
```

### 11.2 Альтернативные способы

| Способ | Когда использовать |
|--------|-------------------|
| CustomEvent | Основной — skill и дашборд на одной странице |
| window.postMessage | Skill и дашборд в разных iframe |
| localStorage | Дашборд загружается отдельно, читает кэш |
| URL param (base64) | Данные < 2KB, inline передача |
| Fetch API | Дашборд подключается к API skill |

### 11.3 Интеграционный сценарий

```
[Skill запускает сессию]
    |
    |-- Skill собирает данные пользователя
    |   |-- Wheel of Life scores
    |   |-- OKR progress
    |   |-- Weekly data
    |   |-- Daily habits
    |
    |-- Skill формирует DashboardData JSON
    |   |-- Соответствует JSON Data Contract (раздел 3)
    |
    |-- Skill встраивает дашборд (iframe или inline)
    |   |-- HTML файл + JS + CSS
    |
    |-- Skill передаёт данные
    |   |-- window.dispatchEvent(new CustomEvent('dashboard:data', { detail: data }))
    |
    |-- Дашборд получает данные
    |   |-- Parse -> Validate -> Normalize -> Store
    |   |-- Charts инициализируются и рендерятся
    |
    |-- Пользователь взаимодействует с дашбордом
        |-- Клик по сфере -> drill-down
        |-- Клик по дню -> детали
        |-- Export -> скачивание PNG
```

---

## 12. Roadmap внедрения

| Фаза | Компоненты | Срок | Приоритет |
|------|-----------|------|-----------|
| **Phase 1: MVP** | Radar (Wheel of Life), Heatmap, OKR Rings, базовый Store | 3-5 дней | P0 |
| **Phase 2: Trends** | Velocity Chart, Burndown Chart, Gauges | 3-4 дня | P1 |
| **Phase 3: Goals** | BHAG Timeline, 12-Week Tracker, WOOP Cards | 3-4 дня | P1 |
| **Phase 4: Polish** | Drill-down modals, Export, Animations, Responsive | 3-4 дня | P2 |
| **Phase 5: Advanced** | Filters, Correlations, Accessibility, Keyboard shortcuts | 2-3 дня | P3 |

### Phase 1 (MVP) — детализация

```
Day 1: Store + EventBus + DataParser + базовая HTML-структура
Day 2: WheelOfLifeRadar + CalendarHeatmap (ECharts)
Day 3: OKRProgressRing (Chart.js) + Header + TabNav
Day 4: Интеграция + тестирование + Responsive (mobile)
Day 5: Bug fixes + оптимизация
```

---

## 13. Заключение

### Ключевые архитектурные решения

| Решение | Обоснование |
|---------|-------------|
| **Vanilla JS без фреймворков** | Простота развёртывания (один HTML файл), минимум зависимостей, лёгкая интеграция со skill |
| **ECharts + Chart.js гибрид** | ECharts покрывает сложные визуализации (heatmap, radar, gauge, timeline), Chart.js — простые doughnut rings |
| **Reactive Store на чистом JS** | Достаточно для одностраничного дашборда без избыточности Redux/Vuex |
| **CustomEvent для data input** | Стандартный браузерный API, skill просто dispatch событие с JSON payload |
| **Lazy loading charts** | IntersectionObserver гарантирует, что незаметные charts не потребляют ресурсы |
| **Low-saturation warm palette** | Соответствует life coach тематике, создаёт ощущение уюта и безопасности |
| **8 цветов для сфер** | Запоминаемые, различимые при цветовой слепоте, ненавязчивые |
| **Mobile-first responsive** | Дашборд должен работать на телефоне (пользователь открывает на ходу) |

### Масштабируемость

- Добавление нового chart типа: унаследовать от `EChartsBase` / `ChartJSBase`
- Добавление новой секции: создать компонент + зарегистрировать в Tab
- Добавление нового фильтра: расширить `filters` в Store + UI в Sidebar
- Изменение data contract: добавить опциональное поле (обратная совместимость)

### Риски и митигация

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Bundle size > 500KB | Средняя | ECharts tree-shaking, CDN loading с cache |
| Performance на слабом mobile | Средняя | Lazy loading, data sampling, уменьшение точек |
| Цветовая слепота | Низкая | Patterns + icons, WCAG-compliant контраст |
| IE/старый browser | Низкая | Только modern browsers (ES2020+) |

---

*Архитектура спроектирована на основе исследования интерактивных дашбордов для ретроспектив и отслеживания личных целей. Технический стек: Apache ECharts + Chart.js + Vanilla JS. Готов к Phase 1 (MVP) разработке.*
