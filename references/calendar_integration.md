# Архитектура Google Calendar интеграции для Life Planning Skill

> **Документ**: Архитектурная спецификация
> **Версия**: 1.0
> **Дата**: 2025-07
> **Основание**: Исследование Google Calendar API v3 + Google Tasks API v1

---

## Содержание

1. [Структура модуля](#1-структура-модуля)
2. [Классовая диаграмма](#2-классовая-диаграмма)
3. [Data Models](#3-data-models)
4. [Sequence Diagrams](#4-sequence-diagrams)
5. [Configuration Schema](#5-configuration-schema)
6. [Error Handling Strategy](#6-error-handling-strategy)
7. [Примеры использования](#7-примеры-использования)
8. [requirements.txt](#8-requirementstxt)

---

## 1. Структура модуля

```
calendar_integration/
├── __init__.py              # Экспорт публичного API
├── auth.py                  # OAuth 2.0 flow, token management, Fernet encryption
├── calendar_manager.py      # CRUD событий, free/busy, recurring events
├── tasks_manager.py         # Google Tasks CRUD, subtasks
├── sync_engine.py           # Bidirectional sync, conflict resolution, sync tokens
├── config.py                # Color coding, reminders, settings schemas
├── models.py                # Data classes: Event, Task, TimeSlot, CalendarCredentials
├── exceptions.py            # Иерархия кастомных исключений
├── retry.py                 # Декоратор retry с exponential backoff
└── utils.py                 # Вспомогательные функции (timezone, RRULE builder)
```

---

## 2. Классовая диаграмма

### 2.1 Полная диаграмма (text-based UML)

```
+----------------------------------------------------------------------------------+
|                              <<module>> exceptions.py                             |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  CalendarIntegrationError (Base)                                                  |
|  ├── AuthenticationError                                                          |
|  │   ├── TokenExpiredError                                                        |
|  │   ├── TokenRefreshError                                                        |
|  │   └── CredentialsNotFoundError                                                 |
|  ├── CalendarAPIError                                                             |
|  │   ├── EventNotFoundError                                                       |
|  │   ├── CalendarNotFoundError                                                    |
|  │   ├── RateLimitExceededError                                                   |
|  │   └── QuotaExceededError                                                       |
|  ├── TasksAPIError                                                                |
|  │   ├── TaskNotFoundError                                                        |
|  │   └── TaskListNotFoundError                                                    |
|  ├── SyncError                                                                    |
|  │   ├── SyncTokenExpiredError                                                    |
|  │   └── ConflictResolutionError                                                  |
|  └── NetworkError                                                                 |
|      ├── OfflineModeError                                                         |
|      └── MaxRetriesExceededError                                                  |
|                                                                                   |
+----------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------+
|                                <<module>> models.py                                 |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  @dataclass                                                                       |
|  class CalendarCredentials:                                                       |
|      client_id: str                                                               |
|      client_secret: str                                                           |
|      refresh_token: str | None                                                    |
|      access_token: str | None                                                     |
|      scopes: list[str]                                                            |
|      expiry: datetime | None                                                      |
|      token_uri: str = "https://oauth2.googleapis.com/token"                       |
|      + is_valid() -> bool                                                         |
|      + is_expired() -> bool                                                       |
|      + to_google_credentials() -> Credentials                                       |
|                                                                                   |
|  @dataclass                                                                       |
|  class Event:                                                                     |
|      id: str | None                                                               |
|      title: str                                                                   |
|      start: datetime                                                              |
|      end: datetime                                                                |
|      description: str = ""                                                        |
|      location: str = ""                                                           |
|      color_id: str = "1"                                                          |
|      event_type: str = "personal"        # ключ из COLOR_MAP                      |
|      reminders: list[Reminder] = field(default_factory=list)                      |
|      recurrence: list[str] = field(default_factory=list)   # RRULE strings        |
|      attendees: list[str] = field(default_factory=list)                           |
|      calendar_id: str = "primary"                                                 |
|      html_link: str | None = None                                                 |
|      created: datetime | None = None                                              |
|      updated: datetime | None = None                                              |
|      status: str = "confirmed"          # confirmed, tentative, cancelled          |
|      recurring_event_id: str | None = None                                        |
|      + to_api_body() -> dict                                                      |
|      + from_api_response(data: dict) -> Event                                     |
|      + duration_minutes() -> int                                                  |
|                                                                                   |
|  @dataclass                                                                       |
|  class Reminder:                                                                  |
|      method: str          # "popup" | "email"                                     |
|      minutes: int         # 0..40320                                              |
|      + to_api_dict() -> dict                                                      |
|                                                                                   |
|  @dataclass                                                                       |
|  class Task:                                                                      |
|      id: str | None                                                               |
|      title: str                                                                   |
|      notes: str = ""                                                              |
|      due: date | None = None                                                      |
|      completed: datetime | None = None                                            |
|      status: str = "needsAction"      # needsAction | completed                    |
|      parent: str | None = None          # ID родительской задачи                  |
|      tasklist_id: str = "@default"                                                |
|      position: str = ""                                                           |
|      links: list[str] = field(default_factory=list)                               |
|      + to_api_body() -> dict                                                      |
|      + from_api_response(data: dict) -> Task                                      |
|      + is_completed() -> bool                                                     |
|      + is_overdue() -> bool                                                       |
|                                                                                   |
|  @dataclass                                                                       |
|  class TimeSlot:                                                                  |
|      start: datetime                                                              |
|      end: datetime                                                                |
|      is_free: bool = True                                                         |
|      + duration_minutes() -> int                                                  |
|      + overlaps(other: TimeSlot) -> bool                                          |
|      + split_at(boundary: datetime) -> tuple[TimeSlot, TimeSlot]                  |
|                                                                                   |
|  @dataclass                                                                       |
|  class SyncState:                                                                 |
|      calendar_sync_token: str | None = None                                       |
|      tasks_sync_token: str | None = None                                          |
|      last_sync_at: datetime | None = None                                         |
|      pending_changes: list[PendingChange] = field(default_factory=list)           |
|                                                                                   |
|  @dataclass                                                                       |
|  class PendingChange:                                                             |
|      id: str                                                                      |
|      operation: str              # "create" | "update" | "delete"                 |
|      entity_type: str            # "event" | "task"                               |
|      payload: dict | None = None                                                  |
|      timestamp: datetime = field(default_factory=datetime.utcnow)                 |
|      retry_count: int = 0                                                         |
|                                                                                   |
+----------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------+
|                                <<module>> config.py                                 |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  class CalendarConfig:                                                            |
|      + COLOR_MAP: dict[str, str]                                                  |
|      + REMINDER_PRESETS: dict[str, list[dict]]                                    |
|      + DEFAULT_TIMEZONE: str                                                      |
|      + WORK_HOURS: tuple[int, int]                                                |
|      + DEFAULT_REMINDER_MINUTES: int                                              |
|      + SYNC_INTERVAL_SECONDS: int                                                 |
|      + MAX_RETRIES: int                                                           |
|      + BASE_RETRY_DELAY: float                                                    |
|      + MAX_RETRY_DELAY: float                                                     |
|      + OFFLINE_QUEUE_MAX_SIZE: int                                                |
|      + _instance: CalendarConfig | None = None                                    |
|      + get_instance() -> CalendarConfig          # Singleton                       |
|      + get_color_id(event_type: str) -> str                                       |
|      + get_reminder_preset(name: str) -> list[Reminder]                           |
|      + load_from_file(path: str) -> CalendarConfig                                |
|                                                                                   |
|  Color map (Life Planning схема):                                                 |
|  +------------------+---------+-------------------------------------------------+ |
|  | deep_work        | "2"     | Sage green — фокусная работа по целям           | |
|  | woop             | "7"     | Peacock blue — WOOP-сессии                     | |
|  | weekly_review    | "5"     | Banana yellow — Weekly Review                  | |
|  | family           | "1"     | Lavender purple — семья / личное время          | |
|  | exercise         | "6"     | Tangerine orange — спорт / здоровье            | |
|  | reading          | "4"     | Flamingo pink — чтение / обучение              | |
|  | urgent           | "11"    | Tomato red — срочные / дедлайны                | |
|  | personal         | "3"     | Grape — личные задачи                          | |
|  +------------------+---------+-------------------------------------------------+ |
|                                                                                   |
+----------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------+
|                                <<module>> retry.py                                  |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  @dataclass                                                                       |
|  class RetryConfig:                                                               |
|      max_retries: int = 5                                                         |
|      base_delay: float = 1.0                                                      |
|      max_delay: float = 60.0                                                      |
|      retryable_status_codes: set[int] = field(default_factory=lambda: {429,500,   |
|                                                                      502,503,504})|
|      + get_delay(attempt: int) -> float       # exp backoff + jitter              |
|                                                                                   |
|  class Retryable:                                                                 |
|      + __init__(config: RetryConfig = RetryConfig())                              |
|      + __call__(func: Callable) -> Callable        # декоратор                  |
|      + execute(func: Callable, *args, **kwargs) -> T                              |
|      + execute_async(func: Callable, *args, **kwargs) -> T                        |
|                                                                                   |
+----------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------+
|                                 <<module>> auth.py                                  |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  class SecureTokenStorage:                                                        |
|      + __init__(encryption_key: str | None = None)                                |
|      - _cipher: Fernet                                                            |
|      + store(user_id: str, creds: CalendarCredentials, path: Path) -> None        |
|      + load(user_id: str, path: Path) -> CalendarCredentials                      |
|      + delete(user_id: str, path: Path) -> None                                   |
|      + exists(user_id: str, path: Path) -> bool                                   |
|      - _encrypt(data: str) -> str                                                 |
|      - _decrypt(token: str) -> str                                                |
|      - _derive_key(raw: str) -> bytes                                             |
|                                                                                   |
|  class GoogleAuthenticator:                                                       |
|      + __init__(client_id: str, client_secret: str,                               |
|                  storage: SecureTokenStorage, scopes: list[str])                  |
|      - _client_id: str                                                            |
|      - _client_secret: str                                                        |
|      - _storage: SecureTokenStorage                                               |
|      - _scopes: list[str]                                                         |
|      - _credentials: CalendarCredentials | None = None                            |
|      + authenticate() -> Credentials             # desktop flow                  |
|      + authenticate_headless(refresh_token: str) -> Credentials                   |
|      + refresh() -> Credentials                                                   |
|      + revoke() -> None                                                           |
|      + is_authenticated() -> bool                                                 |
|      + get_credentials() -> CalendarCredentials                                   |
|      - _run_oauth_flow() -> Credentials                                           |
|      - _build_google_credentials() -> Credentials                                 |
|                                                                                   |
|  <<decorator>>                                                                    |
|  @require_auth                                                                    |
|  +-- оборачивает методы, требующие авторизации                                   |
|                                                                                   |
+----------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------+
|                            <<module>> calendar_manager.py                           |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  class CalendarManager:                                                           |
|      + __init__(authenticator: GoogleAuthenticator, config: CalendarConfig)       |
|      - _auth: GoogleAuthenticator                                                 |
|      - _config: CalendarConfig                                                    |
|      - _service: Resource | None = None       # googleapiclient Resource          |
|      + _get_service() -> Resource                                                 |
|                                                                                   |
|      # --- CRUD событий ---                                                       |
|      + get_events(date_from: datetime, date_to: datetime,                         |
|                   calendar_id: str = "primary", query: str | None = None,         |
|                   max_results: int = 250) -> list[Event]                          |
|      + get_event(event_id: str, calendar_id: str = "primary") -> Event            |
|      + create_event(title: str, start: datetime, end: datetime,                   |
|                     description: str = "", color_id: str | None = None,           |
|                     reminders: list[Reminder] | None = None,                      |
|                     recurrence: list[str] | None = None,                          |
|                     attendees: list[str] | None = None,                           |
|                     calendar_id: str = "primary") -> Event                        |
|      + update_event(event_id: str, calendar_id: str = "primary",                  |
|                      **kwargs) -> Event                                           |
|      + delete_event(event_id: str, calendar_id: str = "primary") -> None          |
|      + move_event(event_id: str, destination_calendar: str,                       |
|                   source_calendar: str = "primary") -> Event                      |
|                                                                                   |
|      # --- Повторяющиеся события ---                                              |
|      + create_recurring_event(title: str, start: datetime, end: datetime,         |
|                               recurrence_rule: str, description: str = "",        |
|                               color_id: str | None = None,                        |
|                               reminders: list[Reminder] | None = None) -> Event   |
|      + get_event_instances(recurring_event_id: str,                               |
|                            calendar_id: str = "primary") -> list[Event]           |
|      + delete_event_series(recurring_event_id: str,                               |
|                             calendar_id: str = "primary") -> None                 |
|                                                                                   |
|      # --- Free / Busy ---                                                        |
|      + get_free_slots(date: date, duration_minutes: int,                          |
|                       work_start: int | None = None,                              |
|                       work_end: int | None = None,                                |
|                       calendar_id: str = "primary") -> list[TimeSlot]             |
|      + check_availability(start: datetime, end: datetime,                         |
|                            calendar_id: str = "primary") -> list[TimeSlot]        |
|      + is_slot_free(start: datetime, end: datetime,                               |
|                     calendar_id: str = "primary") -> bool                         |
|                                                                                   |
|      # --- Life Planning presets ---                                              |
|      + create_weekly_review_reminder(timezone: str | None = None,                 |
|                                      hour: int = 19, minute: int = 0) -> Event    |
|      + create_woop_reminder(timezone: str | None = None,                          |
|                              hour: int = 7, minute: int = 0) -> Event             |
|      + create_milestone_event(title: str, milestone_date: datetime,               |
|                                description: str = "",                             |
|                                advance_reminder_days: int = 7) -> Event           |
|      + create_time_block(title: str, start: datetime,                             |
|                          duration_hours: float, color: str = "deep_work",         |
|                          description: str = "") -> Event                          |
|      + create_12week_milestone_series(goal_title: str, start_date: date,          |
|                                        timezone: str | None = None) -> list[Event]|
|      + create_daily_schedule_blocks(schedule: list[dict]) -> list[Event]          |
|                                                                                   |
|      # --- Вспомогательные ---                                                    |
|      + get_available_colors() -> dict[str, dict]                                  |
|      + get_calendar_list() -> list[dict]                                          |
|      + search_events(query: str, days_ahead: int = 30) -> list[Event]             |
|                                                                                   |
+----------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------+
|                             <<module>> tasks_manager.py                             |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  class TasksManager:                                                              |
|      + __init__(authenticator: GoogleAuthenticator, config: CalendarConfig)       |
|      - _auth: GoogleAuthenticator                                                 |
|      - _config: CalendarConfig                                                    |
|      - _service: Resource | None = None                                           |
|      + _get_service() -> Resource                                                 |
|                                                                                   |
|      # --- Task Lists ---                                                         |
|      + get_task_lists() -> list[dict]                                             |
|      + get_or_create_tasklist(title: str) -> str        # возвращает tasklist_id  |
|      + create_tasklist(title: str) -> str                                         |
|      + delete_tasklist(tasklist_id: str) -> None                                  |
|                                                                                   |
|      # --- CRUD задач ---                                                         |
|      + get_tasks(tasklist_id: str = "@default",                                   |
|                   show_completed: bool = False,                                   |
|                   due_min: date | None = None,                                    |
|                   due_max: date | None = None,                                    |
|                   max_results: int = 100) -> list[Task]                           |
|      + get_task(task_id: str, tasklist_id: str = "@default") -> Task              |
|      + create_task(title: str, notes: str = "", due: date | None = None,          |
|                    parent: str | None = None,                                     |
|                    tasklist_id: str = "@default") -> Task                         |
|      + update_task(task_id: str, tasklist_id: str = "@default",                   |
|                     **kwargs) -> Task                                             |
|      + complete_task(task_id: str, tasklist_id: str = "@default") -> Task         |
|      + uncomplete_task(task_id: str, tasklist_id: str = "@default") -> Task       |
|      + delete_task(task_id: str, tasklist_id: str = "@default") -> None           |
|      + move_task(task_id: str, tasklist_id: str = "@default",                     |
|                   parent: str | None = None) -> Task                              |
|                                                                                   |
|      # --- Batch операции ---                                                     |
|      + create_tasks_batch(tasks: list[Task],                                      |
|                           tasklist_id: str = "@default") -> list[Task]            |
|      + create_task_with_subtasks(parent_title: str,                               |
|                                  subtasks: list[str],                             |
|                                  notes: str = "",                                 |
|                                  due: date | None = None,                         |
|                                  tasklist_id: str = "@default") -> tuple[str,     |
|                                                                  list[str]]       |
|                                                                                   |
|      # --- Life Planning presets ---                                              |
|      + create_daily_top3(priorities: list[str], due: date,                        |
|                          tasklist_id: str = "@default") -> list[Task]             |
|      + create_weekly_goal_tasks(goals: list[dict],                                |
|                                  tasklist_id: str = "@default") -> list[Task]     |
|      + create_12week_goal_task(goal_title: str, target_date: date,                 |
|                                subtasks: list[str],                               |
|                                tasklist_id: str = "@default") -> Task             |
|      + clear_completed(tasklist_id: str = "@default") -> int                      |
|                                                                                   |
+----------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------+
|                              <<module>> sync_engine.py                              |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  class SyncEngine:                                                                |
|      + __init__(calendar_manager: CalendarManager,                                |
|                  tasks_manager: TasksManager,                                     |
|                  storage: SecureTokenStorage, config: CalendarConfig)             |
|      - _calendar: CalendarManager                                                 |
|      - _tasks: TasksManager                                                       |
|      - _storage: SecureTokenStorage                                               |
|      - _config: CalendarConfig                                                    |
|      - _state: SyncState                                                          |
|      - _queue: ChangeQueue                                                        |
|      - _running: bool = False                                                     |
|      - _sync_thread: Thread | None = None                                         |
|                                                                                   |
|      # --- Синхронизация ---                                                      |
|      + full_sync() -> SyncResult                                                  |
|      + incremental_sync() -> SyncResult                                           |
|      + start_auto_sync(interval_seconds: int | None = None) -> None               |
|      + stop_auto_sync() -> None                                                   |
|      + force_sync() -> SyncResult                                                 |
|                                                                                   |
|      # --- Очередь изменений ---                                                  |
|      + queue_create(entity_type: str, payload: dict) -> str                       |
|      + queue_update(entity_type: str, entity_id: str, payload: dict) -> str       |
|      + queue_delete(entity_type: str, entity_id: str) -> str                      |
|      + process_queue() -> QueueResult                                             |
|      + get_pending_changes() -> list[PendingChange]                               |
|      + clear_queue() -> None                                                      |
|                                                                                   |
|      # --- Разрешение конфликтов ---                                              |
|      + resolve_conflict(local: Event | Task, remote: Event | Task,                |
|                         strategy: str = "last_write_wins") -> Event | Task        |
|      - _last_write_wins(local, remote) -> Event | Task                            |
|      - _local_wins(local, remote) -> Event | Task                                 |
|      - _remote_wins(local, remote) -> Event | Task                                |
|      - _merge(local, remote) -> Event | Task                                      |
|                                                                                   |
|      # --- Внутренние ---                                                         |
|      - _save_state() -> None                                                      |
|      - _load_state() -> SyncState                                                 |
|      - _run_sync_loop(interval: int) -> None                                      |
|      - _handle_sync_token_expired() -> None                                       |
|      - _notify_listeners(result: SyncResult) -> None                              |
|                                                                                   |
|  @dataclass                                                                       |
|  class SyncResult:                                                                |
|      events_created: int = 0                                                      |
|      events_updated: int = 0                                                      |
|      events_deleted: int = 0                                                      |
|      tasks_created: int = 0                                                       |
|      tasks_updated: int = 0                                                       |
|      tasks_deleted: int = 0                                                       |
|      conflicts_resolved: int = 0                                                  |
|      errors: list[str] = field(default_factory=list)                              |
|      sync_token_valid: bool = True                                                |
|      completed_at: datetime = field(default_factory=datetime.utcnow)              |
|                                                                                   |
|  class ChangeQueue:                                                               |
|      + __init__(max_size: int = 1000)                                             |
|      - _queue: deque[PendingChange]                                               |
|      + enqueue(change: PendingChange) -> str                                      |
|      + dequeue() -> PendingChange | None                                          |
|      + peek() -> PendingChange | None                                             |
|      + remove(change_id: str) -> bool                                             |
|      + get_all() -> list[PendingChange]                                           |
|      + size() -> int                                                              |
|      + is_empty() -> bool                                                         |
|      + is_full() -> bool                                                          |
|      + clear() -> None                                                            |
|                                                                                   |
+----------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------+
|                                <<module>> utils.py                                  |
+----------------------------------------------------------------------------------+
|                                                                                   |
|  class RRuleBuilder:                                                              |
|      + daily(count: int | None = None, until: date | None = None) -> str          |
|      + weekly(days: list[str], interval: int = 1,                                |
|               count: int | None = None, until: date | None = None) -> str         |
|      + monthly(day: int, count: int | None = None) -> str                         |
|      + weekdays(count: int | None = None, until: date | None = None) -> str       |
|      + weekends(count: int | None = None, until: date | None = None) -> str       |
|                                                                                   |
|  class TimezoneHelper:                                                            |
|      + now(tz: str) -> datetime                                                   |
|      + localize(dt: datetime, tz: str) -> datetime                                |
|      + to_utc(dt: datetime) -> datetime                                           |
|      + next_weekday(weekday: int, hour: int, minute: int, tz: str) -> datetime    |
|      + combine(date: date, time: time, tz: str) -> datetime                       |
|                                                                                   |
|  def find_free_intervals(boundaries: TimeSlot, busy: list[TimeSlot],              |
|                          min_duration: timedelta) -> list[TimeSlot]               |
|  def merge_adjacent_slots(slots: list[TimeSlot]) -> list[TimeSlot]                |
|  def filter_slots_by_duration(slots: list[TimeSlot],                              |
|                               min_duration: timedelta) -> list[TimeSlot]          |
|                                                                                   |
+----------------------------------------------------------------------------------+
```

### 2.2 Взаимосвязи между классами (relationships)

```
GoogleAuthenticator  *--  CalendarCredentials   (создаёт и управляет)
GoogleAuthenticator  *--  SecureTokenStorage    (использует для хранения)

CalendarManager      *--  GoogleAuthenticator   (получает service через auth)
CalendarManager      *--  CalendarConfig        (читает цвета, reminders)
CalendarManager  ..>  Event                    (создаёт, возвращает)
CalendarManager  ..>  TimeSlot                 (возвращает из free/busy)

TasksManager         *--  GoogleAuthenticator   (получает service через auth)
TasksManager         *--  CalendarConfig        (читает настройки)
TasksManager     ..>  Task                     (создаёт, возвращает)

SyncEngine           *--  CalendarManager       (синхронизирует события)
SyncEngine           *--  TasksManager          (синхронизирует задачи)
SyncEngine           *--  SecureTokenStorage    (хранит sync tokens)
SyncEngine           *--  CalendarConfig        (читает настройки)
SyncEngine           *--  SyncState             (управляет состоянием)
SyncEngine           *--  ChangeQueue           (управляет очередью)
SyncEngine       ..>  SyncResult               (возвращает результат)
SyncEngine       ..>  PendingChange            (обрабатывает из очереди)

Retryable        ..>  RetryConfig               (использует конфигурацию)
Retryable        ..>  CalendarAPIError          (бросает при исчерпании)

Event            ..>  Reminder                  (содержит список)
```

### 2.3 Публичный API (__init__.py)

```python
# calendar_integration/__init__.py

from .auth import GoogleAuthenticator, SecureTokenStorage
from .calendar_manager import CalendarManager
from .tasks_manager import TasksManager
from .sync_engine import SyncEngine, SyncResult
from .models import Event, Task, TimeSlot, Reminder, CalendarCredentials
from .config import CalendarConfig
from .exceptions import (
    CalendarIntegrationError,
    AuthenticationError,
    CalendarAPIError,
    TasksAPIError,
    SyncError,
    NetworkError,
)
from .retry import Retryable, RetryConfig

__all__ = [
    "GoogleAuthenticator",
    "SecureTokenStorage",
    "CalendarManager",
    "TasksManager",
    "SyncEngine",
    "CalendarConfig",
    "Event",
    "Task",
    "TimeSlot",
    "Reminder",
    "CalendarCredentials",
    "SyncResult",
    "Retryable",
    "RetryConfig",
    # exceptions
    "CalendarIntegrationError",
    "AuthenticationError",
    "CalendarAPIError",
    "TasksAPIError",
    "SyncError",
    "NetworkError",
]
```

---

## 3. Data Models

### 3.1 CalendarCredentials

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from google.oauth2.credentials import Credentials as GoogleCredentials


@dataclass
class CalendarCredentials:
    """
    Хранилище credentials для Google Calendar / Tasks API.

    Attributes:
        client_id: Client ID из Google Cloud Console.
        client_secret: Client secret из Google Cloud Console.
        refresh_token: Токен для обновления access token (долговременный).
        access_token: Краткосрочный access token (автоматически обновляется).
        scopes: Список OAuth scopes.
        expiry: Время истечения access token.
        token_uri: URI endpoint для обновления токена.
    """
    client_id: str
    client_secret: str
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    scopes: list[str] = field(default_factory=lambda: [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/tasks",
    ])
    expiry: Optional[datetime] = None
    token_uri: str = "https://oauth2.googleapis.com/token"

    def is_valid(self) -> bool:
        """Проверить, есть ли валидный access token."""
        return self.access_token is not None and not self.is_expired()

    def is_expired(self) -> bool:
        """Проверить, истёк ли access token (с запасом 60 секунд)."""
        if self.expiry is None:
            return True
        from datetime import timedelta
        return datetime.utcnow() >= (self.expiry - timedelta(seconds=60))

    def to_google_credentials(self) -> GoogleCredentials:
        """Конвертировать в google.oauth2.credentials.Credentials."""
        return GoogleCredentials(
            token=self.access_token,
            refresh_token=self.refresh_token,
            token_uri=self.token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes,
        )

    @classmethod
    def from_google_credentials(cls, creds: GoogleCredentials) -> "CalendarCredentials":
        """Создать CalendarCredentials из Google Credentials."""
        return cls(
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            refresh_token=creds.refresh_token,
            access_token=creds.token,
            scopes=list(creds.scopes) if creds.scopes else [],
            expiry=creds.expiry,
            token_uri=creds.token_uri,
        )
```

### 3.2 Event

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Reminder:
    """
    Напоминание о событии.

    Attributes:
        method: Метод доставки — "popup" (push) или "email".
        minutes: За сколько минут до события отправить напоминание (0..40320).
    """
    method: str = "popup"           # "popup" | "email"
    minutes: int = 15               # 0..40320 (4 недели)

    def __post_init__(self):
        if self.method not in ("popup", "email"):
            raise ValueError(f"Invalid reminder method: {self.method}")
        if not 0 <= self.minutes <= 40320:
            raise ValueError(f"Reminder minutes must be 0..40320, got {self.minutes}")

    def to_api_dict(self) -> dict:
        return {"method": self.method, "minutes": self.minutes}

    @classmethod
    def from_api_dict(cls, data: dict) -> "Reminder":
        return cls(method=data["method"], minutes=data["minutes"])


@dataclass
class Event:
    """
    Событие Google Calendar — центральная модуль life planning интеграции.

    Attributes:
        id: Уникальный идентификатор события (None при создании).
        title: Название события.
        start: Дата/время начала (timezone-aware).
        end: Дата/время окончания (timezone-aware).
        description: Описание / заметки.
        location: Место проведения.
        color_id: ID цвета (1-11), определяет визуальное оформление.
        event_type: Логический тип события (ключ из COLOR_MAP).
        reminders: Список кастомных напоминаний.
        recurrence: Правила повторения в формате RRULE (RFC 5545).
        attendees: Список email-адресов участников.
        calendar_id: ID календаря ("primary" по умолчанию).
        html_link: Публичная ссылка на событие.
        created: Дата создания.
        updated: Дата последнего обновления.
        status: Статус — confirmed, tentative, cancelled.
        recurring_event_id: ID родительского события (для экземпляра серии).
    """
    id: Optional[str] = None
    title: str = ""
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    description: str = ""
    location: str = ""
    color_id: str = "1"
    event_type: str = "personal"
    reminders: list[Reminder] = field(default_factory=lambda: [Reminder()])
    recurrence: list[str] = field(default_factory=list)
    attendees: list[str] = field(default_factory=list)
    calendar_id: str = "primary"
    html_link: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    status: str = "confirmed"
    recurring_event_id: Optional[str] = None

    def __post_init__(self):
        if not self.title:
            raise ValueError("Event title is required")
        if self.start and self.end and self.start >= self.end:
            raise ValueError(f"Event start ({self.start}) must be before end ({self.end})")

    def duration_minutes(self) -> int:
        """Длительность события в минутах."""
        if not self.start or not self.end:
            return 0
        return int((self.end - self.start).total_seconds() / 60)

    def to_api_body(self) -> dict:
        """Сериализовать в тело запроса Google Calendar API."""
        tz = str(self.start.tzinfo) if self.start and self.start.tzinfo else "UTC"
        body: dict[str, any] = {
            "summary": self.title,
            "description": self.description,
            "start": {"dateTime": self.start.isoformat(), "timeZone": tz},
            "end": {"dateTime": self.end.isoformat(), "timeZone": tz},
            "colorId": self.color_id,
            "reminders": {
                "useDefault": False,
                "overrides": [r.to_api_dict() for r in self.reminders],
            },
        }
        if self.location:
            body["location"] = self.location
        if self.recurrence:
            body["recurrence"] = self.recurrence
        if self.attendees:
            body["attendees"] = [{"email": e} for e in self.attendees]
        if self.recurring_event_id:
            body["recurringEventId"] = self.recurring_event_id
        return body

    @classmethod
    def from_api_response(cls, data: dict) -> "Event":
        """Десериализовать из ответа Google Calendar API."""
        start_data = data.get("start", {})
        end_data = data.get("end", {})

        def _parse_dt(dt_data: dict) -> Optional[datetime]:
            if "dateTime" in dt_data:
                return datetime.fromisoformat(dt_data["dateTime"].replace("Z", "+00:00"))
            if "date" in dt_data:
                from datetime import date as dt_date
                return datetime.combine(dt_date.fromisoformat(dt_data["date"]), datetime.min.time())
            return None

        reminders_raw = data.get("reminders", {}).get("overrides", [])
        reminders = [Reminder.from_api_dict(r) for r in reminders_raw] if reminders_raw else [Reminder()]

        return cls(
            id=data.get("id"),
            title=data.get("summary", ""),
            start=_parse_dt(start_data),
            end=_parse_dt(end_data),
            description=data.get("description", ""),
            location=data.get("location", ""),
            color_id=data.get("colorId", "1"),
            reminders=reminders,
            recurrence=data.get("recurrence", []),
            attendees=[a.get("email", "") for a in data.get("attendees", [])],
            calendar_id="primary",
            html_link=data.get("htmlLink"),
            created=_parse_dt({"dateTime": data["created"]}) if "created" in data else None,
            updated=_parse_dt({"dateTime": data["updated"]}) if "updated" in data else None,
            status=data.get("status", "confirmed"),
            recurring_event_id=data.get("recurringEventId"),
        )
```

### 3.3 Task

```python
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Task:
    """
    Задача Google Tasks — модель для daily priorities и goal tracking.

    Важно: Google Tasks API хранит ТОЛЬКО дату (без времени).
    Для задач с точным временем используйте Calendar Event.

    Attributes:
        id: Уникальный идентификатор задачи (None при создании).
        title: Название задачи (обязательное, макс. 8192 символа).
        notes: Описание / заметки (макс. 8192 символа).
        due: Срок выполнения (только дата, время игнорируется API).
        completed: Дата/время завершения (автоматически при complete_task).
        status: Статус — "needsAction" или "completed".
        parent: ID родительской задачи (для подзадач).
        tasklist_id: ID списка задач ("@default" — список по умолчанию).
        position: Позиция в списке (строка для сортировки).
        links: Связанные ссылки.
    """
    id: Optional[str] = None
    title: str = ""
    notes: str = ""
    due: Optional[date] = None
    completed: Optional[datetime] = None
    status: str = "needsAction"
    parent: Optional[str] = None
    tasklist_id: str = "@default"
    position: str = ""
    links: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.title:
            raise ValueError("Task title is required")

    def is_completed(self) -> bool:
        return self.status == "completed"

    def is_overdue(self) -> bool:
        if self.due is None or self.is_completed():
            return False
        return date.today() > self.due

    def to_api_body(self) -> dict:
        body: dict[str, any] = {"title": self.title}
        if self.notes:
            body["notes"] = self.notes
        if self.due:
            body["due"] = self.due.strftime("%Y-%m-%dT00:00:00.000Z")
        if self.status:
            body["status"] = self.status
        if self.completed:
            body["completed"] = self.completed.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        if self.parent:
            body["parent"] = self.parent
        if self.links:
            body["links"] = [{"link": link} for link in self.links]
        return body

    @classmethod
    def from_api_response(cls, data: dict) -> "Task":
        due_raw = data.get("due")
        due = datetime.fromisoformat(due_raw.replace("Z", "+00:00")).date() if due_raw else None

        completed_raw = data.get("completed")
        completed = datetime.fromisoformat(completed_raw.replace("Z", "+00:00")) if completed_raw else None

        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            notes=data.get("notes", ""),
            due=due,
            completed=completed,
            status=data.get("status", "needsAction"),
            parent=data.get("parent"),
            tasklist_id=data.get("tasklist_id", "@default"),
            position=data.get("position", ""),
            links=[l.get("link", "") for l in data.get("links", [])],
        )
```

### 3.4 TimeSlot

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class TimeSlot:
    """
    Временной слот — используется для free/busy анализа и планирования.

    Attributes:
        start: Начало слота.
        end: Окончание слота.
        is_free: True = свободный, False = занятый.
    """
    start: datetime
    end: datetime
    is_free: bool = True

    def __post_init__(self):
        if self.start >= self.end:
            raise ValueError("TimeSlot start must be before end")

    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() / 60)

    def overlaps(self, other: "TimeSlot") -> bool:
        """Проверить пересечение с другим слотом."""
        return self.start < other.end and other.start < self.end

    def contains(self, point: datetime) -> bool:
        """Проверить, содержит ли слот указанную точку во времени."""
        return self.start <= point < self.end

    def split_at(self, boundary: datetime) -> tuple[Optional["TimeSlot"], Optional["TimeSlot"]]:
        """Разделить слот по указанной границе."""
        if boundary <= self.start or boundary >= self.end:
            return (self, None) if boundary >= self.end else (None, self)
        left = TimeSlot(start=self.start, end=boundary, is_free=self.is_free)
        right = TimeSlot(start=boundary, end=self.end, is_free=self.is_free)
        return left, right

    def intersect(self, other: "TimeSlot") -> Optional["TimeSlot"]:
        """Вернуть пересечение двух слотов (None если не пересекаются)."""
        if not self.overlaps(other):
            return None
        return TimeSlot(
            start=max(self.start, other.start),
            end=min(self.end, other.end),
            is_free=self.is_free and other.is_free,
        )

    def __repr__(self) -> str:
        status = "FREE" if self.is_free else "BUSY"
        return f"TimeSlot({self.start:%H:%M}-{self.end:%H:%M}, {status})"
```

### 3.5 SyncState + PendingChange

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class PendingChange:
    """
    Отложенное изменение для офлайн-очереди.

    Attributes:
        id: Уникальный ID изменения.
        operation: Тип операции — create, update, delete.
        entity_type: Тип сущности — event, task.
        payload: Данные для операции.
        timestamp: Время постановки в очередь.
        retry_count: Количество попыток выполнения.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    operation: str = ""              # "create" | "update" | "delete"
    entity_type: str = ""            # "event" | "task"
    payload: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    retry_count: int = 0


@dataclass
class SyncState:
    """
    Состояние синхронизации — хранится между сессиями.

    Attributes:
        calendar_sync_token: Sync token для Calendar API инкрементальной синхронизации.
        tasks_sync_token: Sync token для Tasks API.
        last_sync_at: Время последней успешной синхронизации.
        pending_changes: Список отложенных изменений.
    """
    calendar_sync_token: Optional[str] = None
    tasks_sync_token: Optional[str] = None
    last_sync_at: Optional[datetime] = None
    pending_changes: list[PendingChange] = field(default_factory=list)
```

### 3.6 SyncResult + QueueResult

```python
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SyncResult:
    """
    Результат операции синхронизации.

    Attributes:
        events_created: Количество созданных событий.
        events_updated: Количество обновлённых событий.
        events_deleted: Количество удалённых событий.
        tasks_created: Количество созданных задач.
        tasks_updated: Количество обновлённых задач.
        tasks_deleted: Количество удалённых задач.
        conflicts_resolved: Количество разрешённых конфликтов.
        errors: Список текстовых описаний ошибок.
        sync_token_valid: True если sync token валиден.
        completed_at: Время завершения синхронизации.
    """
    events_created: int = 0
    events_updated: int = 0
    events_deleted: int = 0
    tasks_created: int = 0
    tasks_updated: int = 0
    tasks_deleted: int = 0
    conflicts_resolved: int = 0
    errors: list[str] = field(default_factory=list)
    sync_token_valid: bool = True
    completed_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def total_changes(self) -> int:
        return (
            self.events_created + self.events_updated + self.events_deleted +
            self.tasks_created + self.tasks_updated + self.tasks_deleted
        )

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def is_success(self) -> bool:
        return not self.has_errors and self.sync_token_valid


@dataclass
class QueueResult:
    """Результат обработки очереди изменений."""
    processed: int = 0
    succeeded: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)
```


---

## 4. Sequence Diagrams

### 4.1 Use Case 1: Weekly Review Reminder (создание повторяющегося события)

```
  Life Planning Skill          CalendarManager          GoogleAuthenticator   Google Calendar API
         |                           |                           |                    |
         |  create_weekly_review()   |                           |                    |
         |-------------------------->|                           |                    |
         |                           |  -- 1. _get_service() --  |                    |
         |                           |------------------------->|                    |
         |                           |                          | -- authenticate()  |
         |                           |                          |------(if needed)---|
         |                           |<-- service (Resource) ---|                    |
         |                           |                           |                    |
         |                           |  -- 2. build Event --     |                    |
         |                           |  title="Weekly Review"    |                    |
         |                           |  start=next_sunday_19:00  |                    |
         |                           |  end=+1h                  |                    |
         |                           |  color_id="5" (yellow)    |                    |
         |                           |  reminders=[email@1day,   |                    |
         |                           |            popup@1h]      |                    |
         |                           |  recurrence=[RRULE:FREQ=  |                    |
         |                           |    WEEKLY;BYDAY=SU]       |                    |
         |                           |                           |                    |
         |                           |  -- 3. POST /events/insert|                    |
         |                           |------------------------------------------------->|
         |                           |                           |                    |
         |                           |<-- 4. {id, htmlLink} -----|                    |
         |                           |     (201 Created)         |                    |
         |                           |                           |                    |
         |<-- 5. Event (with id) ---|                           |                    |
         |                           |                           |                    |

  [Retry: если 429/5xx -> exponential backoff до 5 попыток]
  [Offline: если нет сети -> поставить в очередь, sync при подключении]
```

### 4.2 Use Case 2: Find Available Slots (поиск свободного времени для Deep Work)

```
  Life Planning Skill          CalendarManager          GoogleAuthenticator   Google Calendar API
         |                           |                           |                    |
         |  get_free_slots(          |                           |                    |
         |    date=tomorrow,         |                           |                    |
         |    duration_minutes=180)  |                           |                    |
         |-------------------------->|                           |                    |
         |                           |  -- 1. _get_service() --  |                    |
         |                           |------------------------->|                    |
         |                           |<-- service --------------|                    |
         |                           |                           |                    |
         |                           |  -- 2. freebusy.query --  |                    |
         |                           |  timeMin=09:00            |------------------->|
         |                           |  timeMax=18:00            |                    |
         |                           |  items=[{id:"primary"}]   |                    |
         |                           |                           |                    |
         |                           |<-- 3. {calendars: {      |                    |
         |                           |     primary: {busy: [    |                    |
         |                           |       {start, end}, ...]}}|                    |
         |                           |                           |                    |
         |                           |  -- 4. Алгоритм поиска ---|                    |
         |                           |  work_hours=(9, 18)       |                    |
         |                           |  busy_periods -> invert   |                    |
         |                           |  filter >= 180 min        |                    |
         |                           |                           |                    |
         |<-- 5. list[TimeSlot] ----|                           |                    |
         |    [(09:00-10:30),      |                           |                    |
         |     (14:00-18:00)]      |                           |                    |
         |                           |                           |                    |

  Алгоритм поиска свободных слотов:
  1. Определить границы рабочего дня (work_start..work_end)
  2. Получить busy intervals из freebusy.query
  3. Инвертировать: busy -> свободные интервалы
  4. Отфильтровать по минимальной длительности (duration_minutes)
  5. Вернуть отсортированный список TimeSlot
```

### 4.3 Use Case 3: WOOP Morning Session (создание + ежедневная задача в Tasks)

```
  Life Planning Skill       CalendarManager    TasksManager    GoogleAuthenticator   Google APIs
         |                         |                  |                  |               |
         |  create_woop_reminder() |                  |                  |               |
         |------------------------>|                  |                  |               |
         |  create_daily_top3()    |                  |                  |               |
         |------------------------------------------->|                  |               |
         |                         |                  |                  |               |
         |                         | -- 1. Calendar event --             |               |
         |                         | title="WOOP Morning Session"        |               |
         |                         | start=weekday_07:00                 |               |
         |                         | end=+15min                          |               |
         |                         | color="7" (Peacock blue)            |               |
         |                         | recurrence=[RRULE:FREQ=WEEKLY;     |               |
         |                         |   BYDAY=MO,TU,WE,TH,FR]             |               |
         |                         |                  |                  |               |
         |                         |------------------------------------>|               |
         |                         |                  |         authenticate()          |
         |                         |                  |                  |               |
         |                         | POST /calendar/v3/events/insert    |               |
         |                         |----------------------------------------->|          |
         |                         |                  |                  |    (201)     |
         |                         |<-- {event_id} ---|                  |               |
         |                         |                  |                  |               |
         |<-- Event ---------------|                  |                  |               |
         |                         |                  | -- 2. Tasks ---  |               |
         |                         |                  | create_tasklist  |               |
         |                         |                  |   ("Daily Priorities")          |
         |                         |                  |                  |               |
         |                         |                  | POST /tasks/v1/tasklists/insert |
         |                         |                  |--------------------------------->|
         |                         |                  |<-- tasklist_id --|               |
         |                         |                  |                  |               |
         |                         |                  | create_task("Priority 1")       |
         |                         |                  | create_task("Priority 2")       |
         |                         |                  | create_task("Priority 3")       |
         |                         |                  |                  |               |
         |                         |                  | POST /tasks/v1/tasks/insert x3  |
         |                         |                  |--------------------------------->|
         |                         |                  |<-- [task_id x3] -|               |
         |                         |                  |                  |               |
         |<-- list[Task] ----------|------------------------------------|               |
         |                         |                  |                  |               |

  [Если Calendar API недоступен -> graceful degradation, лог warning, Task всё равно создаётся]
```

### 4.4 Use Case 4: 12-Week Milestone (множественное создание + advance reminder)

```
  Life Planning Skill       CalendarManager         Google Calendar API
         |                         |                          |
         | create_12week_milestone_series(                    |
         |   goal_title="Launch MVP",                         |
         |   start_date=2025-07-21)                           |
         |------------------------>|                          |
         |                         |                          |
         |                         | -- Генерация milestones --
         |                         | weeks = [2, 4, 6, 8, 10, 12]
         |                         | labels = [               |
         |                         |   "Checkpoint 1 - Found.",|
         |                         |   "Checkpoint 2 - 1/4",  |
         |                         |   ...                    |
         |                         |   "Goal Complete!"]      |
         |                         |                          |
         |                         | for week, label in pairs:|
         |                         |   event = Event(         |
         |                         |     title=f"12W: {label}"|
         |                         |     start=start_date +   |
         |                         |           timedelta(weeks=week) @ 9am
         |                         |     end=+2h              |
         |                         |     color="2" (deep_work)|
         |                         |     reminders=[          |
         |                         |       email@7days,       |
         |                         |       popup@1day]        |
         |                         |   )                      |
         |                         |                          |
         |                         | POST /events/insert x6   |
         |                         |------------------------->|
         |                         |<-- [{id, link} x6] ------|
         |                         |                          |
         |<-- list[Event] --------|                          |
         |   (6 milestone events)  |                          |
         |                         |                          |

  [Batch optimization: events создаются последовательно с retry для каждого]
  [При ошибке одного milestone -> retry 5x, затем log error, продолжить с остальными]
```

### 4.5 Use Case 5: Bidirectional Sync (инкрементальная синхронизация)

```
  Life Planning Skill       SyncEngine           CalendarManager      TasksManager    Google APIs
         |                      |                      |                  |               |
         |  start_auto_sync()   |                      |                  |               |
         |--------------------->|                      |                  |               |
         |                      | -- 1. _load_state() --                  |               |
         |                      |   (calendar_sync_token,                 |               |
         |                      |    tasks_sync_token)                    |               |
         |                      |                      |                  |               |
         |                      | -- 2. incremental_sync() every N sec    |               |
         |                      |                      |                  |               |
         |                      | ---- a) Calendar sync ----              |               |
         |                      |                      |                  |               |
         |                      | GET /events/list?    |                  |               |
         |                      |   syncToken=...      |                  |               |
         |                      |                      |---------------------------------->|
         |                      |                      |                  |    (200)      |
         |                      |<-- [changed_events] -|                  |    или        |
         |                      |                      |                  |    (410 Gone) |
         |                      |                      |                  |               |
         |                      | [if 410 Gone]:       |                  |               |
         |                      |   full_sync()        |                  |               |
         |                      |   (reset sync token) |                  |               |
         |                      |                      |                  |               |
         |                      | ---- b) Tasks sync ----                 |               |
         |                      |                      |                  |               |
         |                      |                      | GET /tasks/list? |               |
         |                      |                      |   syncToken=...  |-------------->|
         |                      |                      |                  |    (200)      |
         |                      |<-- [changed_tasks] --|                  |               |
         |                      |                      |                  |               |
         |                      | -- 3. Conflict Resolution --            |               |
         |                      |   for each changed entity:              |               |
         |                      |     if local.timestamp < remote.updated:|               |
         |                      |       apply remote                      |               |
         |                      |     else:                               |               |
         |                       |       keep local (last-write-wins)     |               |
         |                      |                      |                  |               |
         |                      | -- 4. Process Queue --                  |               |
         |                      |   for pending in queue:                 |               |
         |                      |     try:                                |               |
         |                      |       execute API call                  |               |
         |                      |       dequeue()                         |               |
         |                      |     except NetworkError:                |               |
         |                      |       retry_count++                     |               |
         |                      |       if retry_count > MAX:             |               |
         |                      |         log error, keep in queue        |               |
         |                      |                      |                  |               |
         |                      | -- 5. _save_state() --                  |               |
         |                      |   (new sync tokens,                     |               |
         |                      |    updated last_sync_at)                |               |
         |                      |                      |                  |               |
         |<-- SyncResult -------|                      |                  |               |
         |                      |                      |                  |               |
         |<-- (callback/notification о conflicts)      |                  |               |
         |                      |                      |                  |               |
         |  stop_auto_sync()    |                      |                  |               |
         |--------------------->|                      |                  |               |
         |                      | (graceful shutdown)  |                  |               |
         |                      |                      |                  |               |

  [Background thread: daemon thread с interval = SYNC_INTERVAL_SECONDS (default: 300)]
  [Offline mode: queue накапливает changes, sync при восстановлении соединения]
```

---

## 5. Configuration Schema

### 5.1 CalendarConfig — полная спецификация

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CalendarConfig:
    """
    Централизованная конфигурация модуля calendar_integration.
    Реализует паттерн Singleton для единого источника настроек.

    Attributes:
        COLOR_MAP: Маппинг типов событий life planning на Google Calendar colorId.
        REMINDER_PRESETS: Преднастроенные шаблоны напоминаний.
        DEFAULT_TIMEZONE: Часовой пояс по умолчанию (IANA, например "Europe/Moscow").
        WORK_HOURS: Рабочие часы (начало, конец) для поиска слотов.
        DEFAULT_REMINDER_MINUTES: Напоминание по умолчанию (минуты до события).
        SYNC_INTERVAL_SECONDS: Интервал авто-синхронизации.
        MAX_RETRIES: Максимальное число retry-попыток.
        BASE_RETRY_DELAY: Базовая задержка retry (секунды).
        MAX_RETRY_DELAY: Максимальная задержка retry (секунды).
        OFFLINE_QUEUE_MAX_SIZE: Максимальный размер офлайн-очереди.
        DEFAULT_TASKLIST_NAME: Название списка задач по умолчанию.
        ENABLE_AUTO_SYNC: Включить фоновую синхронизацию.
        CONFLICT_STRATEGY: Стратегия разрешения конфликтов.
    """

    # --- Color Coding ---
    COLOR_MAP: dict[str, str] = field(default_factory=lambda: {
        "deep_work":      "2",     # Sage green    — фокусная работа по целям
        "woop":           "7",     # Peacock blue  — WOOP-сессии
        "weekly_review":  "5",     # Banana yellow — Weekly Review
        "family":         "1",     # Lavender      — семья / личное время
        "exercise":       "6",     # Tangerine     — спорт / здоровье
        "reading":        "4",     # Flamingo pink — чтение / обучение
        "urgent":         "11",    # Tomato red    — срочные / дедлайны
        "personal":       "3",     # Grape         — личные задачи
        "meeting":        "9",     # Blueberry     — встречи
        "planning":       "10",    # Basil green   — планирование
    })

    # --- Reminder Presets ---
    REMINDER_PRESETS: dict[str, list[dict]] = field(default_factory=lambda: {
        "weekly_review": [
            {"method": "email",  "minutes": 10080},  # За неделю
            {"method": "email",  "minutes": 1440},   # За сутки
            {"method": "popup", "minutes": 60},      # За час
            {"method": "popup", "minutes": 15},      # За 15 минут
        ],
        "woop_morning": [
            {"method": "popup", "minutes": 5},       # За 5 минут
        ],
        "milestone": [
            {"method": "email",  "minutes": 10080},  # За неделю
            {"method": "popup", "minutes": 1440},    # За сутки
        ],
        "deep_work": [
            {"method": "popup", "minutes": 5},       # За 5 минут
        ],
        "time_block": [
            {"method": "popup", "minutes": 15},      # За 15 минут
        ],
        "daily_task": [
            {"method": "popup", "minutes": 0},       # В момент начала
        ],
    })

    # --- General Settings ---
    DEFAULT_TIMEZONE: str = "Europe/Moscow"
    WORK_HOURS: tuple[int, int] = (9, 18)           # (start_hour, end_hour)
    DEFAULT_REMINDER_MINUTES: int = 15

    # --- Sync Settings ---
    SYNC_INTERVAL_SECONDS: int = 300                 # 5 минут
    ENABLE_AUTO_SYNC: bool = True
    CONFLICT_STRATEGY: str = "last_write_wins"       # last_write_wins | local_wins | remote_wins | merge

    # --- Retry Settings ---
    MAX_RETRIES: int = 5
    BASE_RETRY_DELAY: float = 1.0
    MAX_RETRY_DELAY: float = 60.0

    # --- Offline Mode ---
    OFFLINE_QUEUE_MAX_SIZE: int = 1000

    # --- Tasks Settings ---
    DEFAULT_TASKLIST_NAME: str = "Life Planning"

    # --- Singleton ---
    _instance: Optional["CalendarConfig"] = field(default=None, repr=False, compare=False)

    @classmethod
    def get_instance(cls) -> "CalendarConfig":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def load_from_file(cls, path: str) -> "CalendarConfig":
        """Загрузить конфигурацию из JSON-файла."""
        import json
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        config = cls()
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        cls._instance = config
        return config

    def get_color_id(self, event_type: str) -> str:
        """Получить color_id по типу события."""
        return self.COLOR_MAP.get(event_type, "1")

    def get_reminder_preset(self, name: str) -> list[Reminder]:
        """Получить преднастроенные напоминания по имени."""
        from .models import Reminder
        presets = self.REMINDER_PRESETS.get(name, [])
        return [Reminder(method=r["method"], minutes=r["minutes"]) for r in presets]

    def save_to_file(self, path: str) -> None:
        """Сохранить конфигурацию в JSON-файл."""
        import json
        data = {
            "COLOR_MAP": self.COLOR_MAP,
            "REMINDER_PRESETS": self.REMINDER_PRESETS,
            "DEFAULT_TIMEZONE": self.DEFAULT_TIMEZONE,
            "WORK_HOURS": list(self.WORK_HOURS),
            "DEFAULT_REMINDER_MINUTES": self.DEFAULT_REMINDER_MINUTES,
            "SYNC_INTERVAL_SECONDS": self.SYNC_INTERVAL_SECONDS,
            "ENABLE_AUTO_SYNC": self.ENABLE_AUTO_SYNC,
            "CONFLICT_STRATEGY": self.CONFLICT_STRATEGY,
            "MAX_RETRIES": self.MAX_RETRIES,
            "BASE_RETRY_DELAY": self.BASE_RETRY_DELAY,
            "MAX_RETRY_DELAY": self.MAX_RETRY_DELAY,
            "OFFLINE_QUEUE_MAX_SIZE": self.OFFLINE_QUEUE_MAX_SIZE,
            "DEFAULT_TASKLIST_NAME": self.DEFAULT_TASKLIST_NAME,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
```

### 5.2 Пример JSON-конфигурации

```json
{
  "DEFAULT_TIMEZONE": "Europe/Moscow",
  "WORK_HOURS": [9, 18],
  "DEFAULT_REMINDER_MINUTES": 15,
  "SYNC_INTERVAL_SECONDS": 300,
  "ENABLE_AUTO_SYNC": true,
  "CONFLICT_STRATEGY": "last_write_wins",
  "MAX_RETRIES": 5,
  "BASE_RETRY_DELAY": 1.0,
  "MAX_RETRY_DELAY": 60.0,
  "OFFLINE_QUEUE_MAX_SIZE": 1000,
  "DEFAULT_TASKLIST_NAME": "Life Planning",
  "COLOR_MAP": {
    "deep_work": "2",
    "woop": "7",
    "weekly_review": "5",
    "family": "1",
    "exercise": "6",
    "reading": "4",
    "urgent": "11",
    "personal": "3",
    "meeting": "9",
    "planning": "10"
  },
  "REMINDER_PRESETS": {
    "weekly_review": [
      {"method": "email", "minutes": 10080},
      {"method": "email", "minutes": 1440},
      {"method": "popup", "minutes": 60},
      {"method": "popup", "minutes": 15}
    ],
    "woop_morning": [
      {"method": "popup", "minutes": 5}
    ],
    "milestone": [
      {"method": "email", "minutes": 10080},
      {"method": "popup", "minutes": 1440}
    ],
    "deep_work": [
      {"method": "popup", "minutes": 5}
    ],
    "time_block": [
      {"method": "popup", "minutes": 15}
    ]
  }
}
```

### 5.3 Таблица цветовой схемы Life Planning

| Тип события | colorId | Название | Hex background | Применение |
|-------------|---------|----------|----------------|------------|
| `deep_work` | 2 | Sage | `#33b679` | Фокусная работа, 12-недельные цели |
| `woop` | 7 | Peacock | `#039be5` | Утренние WOOP-сессии |
| `weekly_review` | 5 | Banana | `#f6c026` | Еженедельные обзоры |
| `family` | 1 | Lavender | `#7986cb` | Семья, личное время |
| `exercise` | 6 | Tangerine | `#f5511d` | Спорт, здоровье |
| `reading` | 4 | Flamingo | `#e67c73` | Чтение, обучение |
| `urgent` | 11 | Tomato | `#d50000` | Срочные дела, дедлайны |
| `personal` | 3 | Grape | `#8e24aa` | Личные задачи |
| `meeting` | 9 | Blueberry | `#3f51b5` | Встречи, звонки |
| `planning` | 10 | Basil | `#0b8043` | Планирование |

---

## 6. Error Handling Strategy

### 6.1 Иерархия исключений

```python
# exceptions.py

class CalendarIntegrationError(Exception):
    """Базовое исключение для всего модуля."""

    def __init__(self, message: str, status_code: int | None = None, 
                 details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


# === Аутентификация ===
class AuthenticationError(CalendarIntegrationError):
    """Базовое исключение аутентификации."""

class TokenExpiredError(AuthenticationError):
    """Access token истёк — требуется refresh."""
    STATUS_CODE = 401

class TokenRefreshError(AuthenticationError):
    """Не удалось обновить токен — возможно, refresh token revoked."""
    STATUS_CODE = 401

class CredentialsNotFoundError(AuthenticationError):
    """Credentials не найдены — требуется первичная авторизация."""


# === Calendar API ===
class CalendarAPIError(CalendarIntegrationError):
    """Базовое исключение Calendar API."""

class EventNotFoundError(CalendarAPIError):
    """Событие не найдено (404)."""
    STATUS_CODE = 404

class CalendarNotFoundError(CalendarAPIError):
    """Календарь не найден (404)."""
    STATUS_CODE = 404

class RateLimitExceededError(CalendarAPIError):
    """Превышен rate limit (429)."""
    STATUS_CODE = 429

class QuotaExceededError(CalendarAPIError):
    """Превышена квота проекта (403)."""
    STATUS_CODE = 403


# === Tasks API ===
class TasksAPIError(CalendarIntegrationError):
    """Базовое исключение Tasks API."""

class TaskNotFoundError(TasksAPIError):
    """Задача не найдена (404)."""
    STATUS_CODE = 404

class TaskListNotFoundError(TasksAPIError):
    """Список задач не найден (404)."""
    STATUS_CODE = 404


# === Синхронизация ===
class SyncError(CalendarIntegrationError):
    """Базовое исключение синхронизации."""

class SyncTokenExpiredError(SyncError):
    """Sync token устарел (410 Gone) — требуется полная ресинхронизация."""
    STATUS_CODE = 410

class ConflictResolutionError(SyncError):
    """Не удалось автоматически разрешить конфликт."""


# === Сеть / Offline ===
class NetworkError(CalendarIntegrationError):
    """Базовое исключение сети."""

class OfflineModeError(NetworkError):
    """Приложение в офлайн-режиме — изменения поставлены в очередь."""

class MaxRetriesExceededError(NetworkError):
    """Исчерпаны все попытки retry."""
```

### 6.2 Таблица обработки ошибок Google API

| HTTP Code | Google Error | Наше исключение | Стратегия | Retry |
|-----------|--------------|-----------------|-----------|-------|
| 400 | `badRequest` | `CalendarAPIError` | Проверить параметры запроса, логировать | No |
| 401 | `authError` | `TokenExpiredError` | Автоматический refresh token, повторить | Yes (1x) |
| 403 | `quotaExceeded` | `QuotaExceededError` | Ждать `Retry-After` секунд, повторить | Yes (exp backoff) |
| 403 | `forbidden` | `PermissionError` | Проверить scopes, логировать критическую ошибку | No |
| 404 | `notFound` | `EventNotFoundError` | Логировать, вернуть None | No |
| 409 | `conflict` | `CalendarAPIError` | Перечитать ресурс, применить изменения заново | Yes (2x) |
| 410 | `gone` | `SyncTokenExpiredError` | Запустить `full_sync()`, получить новый sync token | Yes (full sync) |
| 429 | `rateLimitExceeded` | `RateLimitExceededError` | Exponential backoff + jitter, повторить | Yes (до 5x) |
| 500 | `backendError` | `CalendarAPIError` | Exponential backoff, повторить | Yes (до 5x) |
| 502 | `badGateway` | `CalendarAPIError` | Exponential backoff, повторить | Yes (до 5x) |
| 503 | `serviceUnavailable` | `CalendarAPIError` | Exponential backoff, повторить | Yes (до 5x) |
| 504 | `gatewayTimeout` | `CalendarAPIError` | Exponential backoff, повторить | Yes (до 5x) |
| — | Timeout / Connection | `NetworkError` | Exponential backoff, повторить | Yes (до 5x) |
| — | DNS failure | `NetworkError` | Перейти в offline mode, поставить в очередь | No (queue) |

### 6.3 Retry декоратор (implementation)

```python
# retry.py
import time
import random
import logging
from functools import wraps
from dataclasses import dataclass, field
from typing import Callable, TypeVar, Any

from googleapiclient.errors import HttpError

from .exceptions import (
    MaxRetriesExceededError,
    TokenExpiredError,
    RateLimitExceededError,
    QuotaExceededError,
)

logger = logging.getLogger(__name__)
T = TypeVar("T")


@dataclass
class RetryConfig:
    """Конфигурация retry-стратегии."""
    max_retries: int = 5
    base_delay: float = 1.0
    max_delay: float = 60.0
    retryable_status_codes: set[int] = field(
        default_factory=lambda: {429, 500, 502, 503, 504}
    )
    # Статус-коды, при которых делаем только 1 retry (например, после refresh token)
    single_retry_codes: set[int] = field(default_factory=lambda: {401})

    def get_delay(self, attempt: int) -> float:
        """
        Вычислить задержку для attempt-ной попытки.
        Exponential backoff с полным jitter: delay = min(base * 2^attempt + jitter, max_delay).
        """
        delay = self.base_delay * (2 ** attempt)
        jitter = random.uniform(0, delay)
        return min(delay + jitter, self.max_delay)


class Retryable:
    """
    Декоратор/исполнитель с retry-логикой.
    Оборачивает вызовы Google API с exponential backoff.
    """

    def __init__(self, config: RetryConfig | None = None):
        self.config = config or RetryConfig()

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        """Использовать как декоратор: @Retryable() def my_func(): ..."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return self.execute(func, *args, **kwargs)
        return wrapper

    def execute(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """
        Выполнить функцию с retry-логикой.
        Обрабатывает HTTP ошибки от Google API.
        """
        last_exception: Exception | None = None

        for attempt in range(self.config.max_retries):
            try:
                return func(*args, **kwargs)

            except HttpError as e:
                status_code = e.resp.status
                last_exception = e
                error_reason = self._extract_reason(e)

                logger.warning(
                    "HTTP %d (%s) on attempt %d/%d: %s",
                    status_code, error_reason, attempt + 1,
                    self.config.max_retries, str(e)[:200]
                )

                # --- 401 Unauthorized -> refresh token + 1 retry ---
                if status_code in self.config.single_retry_codes:
                    if attempt == 0:
                        logger.info("Token expired, triggering refresh...")
                        raise TokenExpiredError(
                            "Access token expired, refresh required",
                            status_code=401
                        ) from e
                    raise TokenExpiredError(
                        "Token refresh failed after retry",
                        status_code=401
                    ) from e

                # --- 429 Too Many Requests -> exponential backoff ---
                if status_code == 429:
                    delay = self._get_retry_after(e) or self.config.get_delay(attempt)
                    logger.info("Rate limited, waiting %.1fs...", delay)
                    time.sleep(delay)
                    continue

                # --- 403 Quota Exceeded -> ждём максимальное время ---
                if status_code == 403 and error_reason == "quotaExceeded":
                    delay = self.config.max_delay
                    logger.warning("Quota exceeded, waiting %.1fs...", delay)
                    time.sleep(delay)
                    continue

                # --- 5xx Server Error -> exponential backoff ---
                if status_code in self.config.retryable_status_codes:
                    delay = self.config.get_delay(attempt)
                    logger.info("Server error, retrying in %.1fs...", delay)
                    time.sleep(delay)
                    continue

                # --- Non-retryable error -> пробрасываем сразу ---
                raise

            except (ConnectionError, TimeoutError) as e:
                last_exception = e
                delay = self.config.get_delay(attempt)
                logger.warning(
                    "Network error on attempt %d/%d: %s. Retrying in %.1fs...",
                    attempt + 1, self.config.max_retries, str(e)[:200], delay
                )
                time.sleep(delay)
                continue

        # Все попытки исчерпаны
        raise MaxRetriesExceededError(
            f"Failed after {self.config.max_retries} attempts: {last_exception}",
            details={"last_error": str(last_exception)}
        ) from last_exception

    @staticmethod
    def _extract_reason(error: HttpError) -> str:
        """Извлечь причину ошибки из ответа Google API."""
        try:
            content = error.content.decode("utf-8") if isinstance(error.content, bytes) else str(error.content)
            import json
            error_data = json.loads(content)
            errors = error_data.get("error", {}).get("errors", [])
            return errors[0].get("reason", "unknown") if errors else "unknown"
        except Exception:
            return "unknown"

    @staticmethod
    def _get_retry_after(error: HttpError) -> float | None:
        """Извлечь Retry-After из заголовков ответа."""
        retry_after = error.resp.get("retry-after")
        if retry_after:
            try:
                return float(retry_after)
            except (ValueError, TypeError):
                pass
        return None
```

### 6.4 Graceful Degradation Strategy

```
+---------------------+------------------+---------------------------------------------+
| Компонент           | Сбой             | Поведение                                   |
+---------------------+------------------+---------------------------------------------+
| Google Calendar API | 5xx / Timeout    | Retry 5x с backoff -> queue -> offline      |
| Google Calendar API | 429 Rate Limit   | Ждать Retry-After -> retry -> log warning   |
| Google Calendar API | 403 Quota        | Ждать 60s -> retry -> notify user           |
| Google Calendar API | 410 Gone         | Full sync (сброс sync token) -> retry       |
| Tasks API           | Любая ошибка     | Retry 5x -> queue -> продолжить без tasks   |
| Auth / Token        | Expired          | Авто-refresh -> retry (1x) -> redirect auth |
| Auth / Token        | Revoked          | Log error -> redirect to OAuth flow         |
| Network             | Полный offline   | Queue all changes -> sync при восстановлении|
| Sync Engine         | Конфликт         | last-write-wins -> log conflict details     |
| Sync Engine         | Token expired    | Full sync + notify user                     |
+---------------------+------------------+---------------------------------------------+

Критичность:
  HIGH: Calendar read/write (core функционал) -> retry + queue
  MEDIUM: Tasks sync -> retry + skip (не блокирует основной flow)
  LOW: Auto-sync background -> retry + reschedule
```

---

## 7. Примеры использования

### 7.1 Инициализация и аутентификация

```python
import os
from pathlib import Path
from dotenv import load_dotenv

from calendar_integration import (
    GoogleAuthenticator,
    SecureTokenStorage,
    CalendarManager,
    TasksManager,
    SyncEngine,
    CalendarConfig,
)

# --- Настройка окружения ---
load_dotenv()
ENCRYPTION_KEY = os.environ["CALENDAR_ENCRYPTION_KEY"]  # Fernet key
CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]

# --- Компоненты ---
storage = SecureTokenStorage(encryption_key=ENCRYPTION_KEY)
config = CalendarConfig.get_instance()

auth = GoogleAuthenticator(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    storage=storage,
    scopes=[
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/tasks",
    ],
)

# --- Авторизация (откроет браузер при первом запуске) ---
creds = auth.authenticate()  # Desktop OAuth flow

# --- Менеджеры ---
calendar = CalendarManager(auth, config)
tasks = TasksManager(auth, config)
sync = SyncEngine(calendar, tasks, storage, config)
```

### 7.2 Weekly Review Reminder (каждое воскресенье 19:00)

```python
from datetime import datetime, timedelta
import pytz

# --- Создать повторяющееся событие Weekly Review ---
event = calendar.create_weekly_review_reminder(
    timezone="Europe/Moscow",
    hour=19,
    minute=0,
)
# Результат:
# - Название: "Weekly Review - Life Planning"
# - Время: каждое воскресенье 19:00-20:00
# - Цвет: Banana yellow (5)
# - Напоминания: email за неделю, email за сутки, popup за час и 15 минут
# - Повторение: RRULE:FREQ=WEEKLY;BYDAY=SU
# - Описание содержит чек-лист:
#   1. Review completed tasks
#   2. Analyze incomplete items
#   3. Update 12-week goal progress
#   4. Plan top 3 priorities for next week
#   5. Schedule deep work blocks
#   6. Family/personal commitments check
#   7. Health/exercise review

# Ручное создание (для кастомизации):
tz = pytz.timezone("Europe/Moscow")
next_sunday = datetime(2025, 7, 27, 19, 0, tzinfo=tz)

event = calendar.create_event(
    title="Weekly Review - Life Planning",
    start=next_sunday,
    end=next_sunday + timedelta(hours=1),
    description="Custom review agenda here...",
    color_id=config.get_color_id("weekly_review"),
    reminders=config.get_reminder_preset("weekly_review"),
    recurrence=["RRULE:FREQ=WEEKLY;BYDAY=SU;COUNT=52"],
)
```

### 7.3 WOOP Morning Session (будни 7:00)

```python
# --- Создать WOOP напоминание на будни ---
event = calendar.create_woop_reminder(
    timezone="Europe/Moscow",
    hour=7,
    minute=0,
)
# Результат:
# - Название: "WOOP - Morning Visualization"
# - Время: пн-пт 7:00-7:15
# - Цвет: Peacock blue (7)
# - Напоминание: popup за 5 минут
# - Повторение: RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR
# - Описание:
#   W - Wish: What's your main wish for today?
#   O - Outcome: Visualize the best outcome
#   O - Obstacle: Identify the main internal obstacle
#   P - Plan: Create an if-then plan
```

### 7.4 Find Available Slots (поиск времени для Deep Work)

```python
from datetime import date

# --- Найти свободные слоты на завтра (минимум 3 часа) ---
tomorrow = date(2025, 7, 22)
free_slots = calendar.get_free_slots(
    date=tomorrow,
    duration_minutes=180,      # 3 часа
    work_start=9,              # с 9:00
    work_end=18,               # до 18:00
)

for slot in free_slots:
    print(f"{slot.start:%H:%M} - {slot.end:%H:%M} ({slot.duration_minutes()} min)")
# Вывод:
# 09:00 - 10:30 (90 min)
# 14:00 - 18:00 (240 min)

# --- Создать Deep Work блок в первом подходящем слоте ---
if free_slots:
    best_slot = free_slots[0]
    event = calendar.create_time_block(
        title="Deep Work - 12W Goal Project",
        start=best_slot.start,
        duration_hours=3,
        color="deep_work",
        description="Focused work on the main 12-week goal. No distractions.",
    )
```

### 7.5 12-Week Milestone Series

```python
from datetime import date

# --- Создать серию milestone-событий для 12-недельного цикла ---
start_date = date(2025, 7, 21)  # Начало цикла
milestones = calendar.create_12week_milestone_series(
    goal_title="Launch MVP Product",
    start_date=start_date,
    timezone="Europe/Moscow",
)

# Результат: 6 событий:
# Week 2:  "12W Milestone: Checkpoint 1 - Foundation Set"      + 7-day advance email
# Week 4:  "12W Milestone: Checkpoint 2 - First Quarter"       + 7-day advance email
# Week 6:  "12W Milestone: Checkpoint 3 - Halfway Review"      + 7-day advance email
# Week 8:  "12W Milestone: Checkpoint 4 - Three Quarters"     + 7-day advance email
# Week 10: "12W Milestone: Checkpoint 5 - Final Sprint"       + 7-day advance email
# Week 12: "12W Milestone: Goal Complete - Celebration!"      + 7-day advance email

# --- Ручное создание одного milestone ---
from datetime import datetime
import pytz

tz = pytz.timezone("Europe/Moscow")
milestone_date = tz.localize(datetime(2025, 8, 4, 9, 0))  # Week 2

event = calendar.create_milestone_event(
    title="Checkpoint 1 - Foundation Set",
    date=milestone_date,
    description="Review: API design complete, DB schema finalized.",
    advance_reminder_days=7,
)
```

### 7.6 Daily Top-3 Priorities as Tasks

```python
from datetime import date

# --- Создать ежедневные приоритеты как задачи ---
today = date.today()
daily_tasks = tasks.create_daily_top3(
    priorities=[
        "Deep work: Complete API integration module",
        "Review: Read 20 pages of 'Atomic Habits'",
        "Health: 30-min evening run",
    ],
    due=today,
)

for task in daily_tasks:
    print(f"- [{'x' if task.is_completed() else ' '}] {task.title}")
# - [ ] Deep work: Complete API integration module
# - [ ] Review: Read 20 pages of 'Atomic Habits'
# - [ ] Health: 30-min evening run

# --- Создать 12-недельную цель с подзадачами ---
goal_task, subtask_ids = tasks.create_task_with_subtasks(
    parent_title="12W Goal: Launch MVP",
    subtasks=[
        "Design database schema",
        "Set up CI/CD pipeline",
        "Implement core API endpoints",
        "Write integration tests",
        "Deploy to production",
    ],
    notes="Main 12-week goal for Q3 2025",
    due=date(2025, 10, 13),
)

# --- Отметить задачу выполненной ---
tasks.complete_task(subtask_ids[0])  # "Design database schema" -> done

# --- Очистить выполненные задачи ---
cleared_count = tasks.clear_completed()
print(f"Cleared {cleared_count} completed tasks")
```

### 7.7 Color-Coded Time Block

```python
from datetime import datetime
import pytz

tz = pytz.timezone("Europe/Moscow")
tomorrow_9am = tz.localize(datetime(2025, 7, 22, 9, 0))

# --- Создать time block для deep work ---
event = calendar.create_time_block(
    title="Deep Work - Architecture Design",
    start=tomorrow_9am,
    duration_hours=3,
    color="deep_work",        # Sage green (2)
    description="Design the microservices architecture. No meetings, no Slack.",
)

# --- Создать time block для спорта ---
event = calendar.create_time_block(
    title="Morning Workout",
    start=tz.localize(datetime(2025, 7, 22, 7, 0)),
    duration_hours=1,
    color="exercise",         # Tangerine orange (6)
    description="Cardio + strength training",
)

# --- Получить все события типа deep_work на неделю ---
from datetime import timedelta
now = datetime.now(tz)
week_events = calendar.get_events(
    date_from=now,
    date_to=now + timedelta(days=7),
)
deep_work_events = [e for e in week_events if e.event_type == "deep_work"]
print(f"Deep work hours this week: {sum(e.duration_minutes() for e in deep_work_events) / 60:.1f}h")
```

### 7.8 Full Daily Schedule Creation

```python
from datetime import datetime, timedelta
import pytz

tz = pytz.timezone("Europe/Moscow")
base_date = tz.localize(datetime(2025, 7, 22, 0, 0))

# --- Типичный распорядок дня (с цветовой кодировкой) ---
daily_schedule = [
    # (start_offset_h, duration_h, title, color_type, description)
    (7,  1,  "Morning Routine",       "exercise",       "Meditation + exercise"),
    (9,  3,  "Deep Work Block #1",    "deep_work",      "Focus on 12W goal project"),
    (12, 1,  "Lunch & Reading",       "reading",        "30-min reading + lunch"),
    (13, 3,  "Deep Work Block #2",    "deep_work",      "Focus on 12W goal project"),
    (16, 1,  "Admin & Planning",      "planning",       "Email, planning, review"),
    (17, 1,  "Family Time",           "family",         "Quality time with family"),
    (18, 1,  "Evening Walk",          "exercise",       "Active recovery walk"),
]

created_events = []
for start_h, duration_h, title, color, desc in daily_schedule:
    start = base_date.replace(hour=start_h, minute=0)
    event = calendar.create_time_block(
        title=title,
        start=start,
        duration_hours=duration_h,
        color=color,
        description=desc,
    )
    created_events.append(event)

print(f"Created {len(created_events)} scheduled events for {base_date:%A, %B %d}")
```

### 7.9 Bidirectional Sync

```python
# --- Запустить фоновую синхронизацию ---
sync.start_auto_sync(interval_seconds=300)  # каждые 5 минут

# --- Принудительная синхронизация ---
result = sync.force_sync()
print(f"Sync complete: {result.total_changes} changes, {result.conflicts_resolved} conflicts")
# SyncResult(events_created=2, events_updated=1, tasks_created=3, ...)

# --- Получить отложенные изменения (offline mode) ---
pending = sync.get_pending_changes()
print(f"Pending changes in queue: {len(pending)}")
for change in pending:
    print(f"  [{change.operation}] {change.entity_type}: {change.payload.get('title', 'N/A')}")

# --- Обработать очередь вручную ---
queue_result = sync.process_queue()
print(f"Processed: {queue_result.processed}, Succeeded: {queue_result.succeeded}")

# --- Остановить синхронизацию ---
sync.stop_auto_sync()
```

### 7.10 Headless / Server Mode (refresh token)

```python
# --- Headless mode: без браузера, через сохранённый refresh token ---
# (Для серверных деплоев, CI/CD, cron jobs)

# Шаг 1: Один раз получить refresh token (на desktop):
# creds = auth.authenticate()  # -> сохраняет в storage

# Шаг 2: На сервере использовать сохранённый refresh token:
from calendar_integration.auth import GoogleAuthenticator

server_auth = GoogleAuthenticator(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    storage=storage,
    scopes=["https://www.googleapis.com/auth/calendar"],
)

# Авторизация через refresh token без браузера
creds = server_auth.authenticate_headless(
    refresh_token="1//0dx..."  # или автоматически из storage
)

# Создание events из cron / Celery
calendar = CalendarManager(server_auth, config)
event = calendar.create_weekly_review_reminder()
print(f"Weekly review created from headless mode: {event.id}")
```

---

## 8. requirements.txt

```
# ============================================================
# Google Calendar Integration for Life Planning Skill
# Python >= 3.10
# ============================================================

# --- Google API Client Libraries ---
google-api-python-client>=2.140.0      # Google Calendar API v3, Tasks API v1
google-auth-oauthlib>=1.2.0            # OAuth 2.0 flow для desktop
google-auth-httplib2>=0.2.0            # HTTP transport layer
google-auth>=2.30.0                    # Core authentication library

# --- Timezone Handling ---
pytz>=2024.2                           # IANA timezone database

# --- Encryption ---
cryptography>=42.0.0                   # Fernet для шифрования токенов

# --- Configuration ---
python-dotenv>=1.0.0                   # Загрузка переменных окружения

# --- Logging ---
structlog>=24.1.0                      # Структурированное логирование (опционально)

# --- Dev / Testing ---
pytest>=8.0.0                          # Тестирование
pytest-asyncio>=0.23.0                 # Async тесты
pytest-mock>=3.14.0                    # Mocking
responses>=0.25.0                      # Mock HTTP для тестов
freezegun>=1.4.0                       # Мокинг времени в тестах

# --- Type Checking (dev) ---
mypy>=1.10.0                           # Статический анализ типов
types-pytz>=2024.1                     # Type stubs для pytz
```

### 8.1 Минимальный requirements.txt (production)

```
google-api-python-client>=2.140.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
google-auth>=2.30.0
pytz>=2024.2
cryptography>=42.0.0
python-dotenv>=1.0.0
```

---

## 9. Быстрый старт (Quick Start)

```python
# 1. Установить зависимости
# pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 pytz cryptography

# 2. Создать .env файл:
# GOOGLE_CLIENT_ID=your_client_id
# GOOGLE_CLIENT_SECRET=your_client_secret
# CALENDAR_ENCRYPTION_KEY=your_fernet_key  # base64-encoded, 32 bytes

# 3. Минимальный рабочий код:
from calendar_integration import (
    GoogleAuthenticator, SecureTokenStorage,
    CalendarManager, CalendarConfig,
)
import os
from dotenv import load_dotenv

load_dotenv()

storage = SecureTokenStorage(os.environ["CALENDAR_ENCRYPTION_KEY"])
auth = GoogleAuthenticator(
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    storage=storage,
)
calendar = CalendarManager(auth, CalendarConfig.get_instance())

# Создать Weekly Review
event = calendar.create_weekly_review_reminder()
print(f"Created: {event.title} at {event.start}")

# Найти свободные слоты
from datetime import date
slots = calendar.get_free_slots(date=date.today(), duration_minutes=120)
for s in slots:
    print(f"Free: {s.start:%H:%M} - {s.end:%H:%M}")
```

---

## 10. Метрики и наблюдаемость

```python
# Логирование всех API-вызовов
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calendar_integration")

# Рекомендуемые метрики для мониторинга:
# - calendar_api.calls_total        (Counter по endpoint)
# - calendar_api.call_duration      (Histogram)
# - calendar_api.errors_total       (Counter по status_code)
# - calendar_api.retry_total        (Counter)
# - sync.changes_processed          (Counter)
# - sync.conflicts_total            (Counter)
# - sync.queue_size                 (Gauge)
# - auth.token_refresh_total        (Counter)
# - auth.token_refresh_errors       (Counter)
```

---

*Документ подготовлен на основе исследования Google Calendar API v3 и Google Tasks API v1.*
*Все примеры кода используют Python 3.10+ с type hints и dataclasses.*
