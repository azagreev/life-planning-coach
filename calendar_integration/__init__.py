"""
Google Calendar интеграция для Life Planning.

Модуль предоставляет удобный Python API для работы с Google Calendar
и Google Tasks: CRUD операции, life-planning пресеты, поиск свободных
слотов, зашифрованное хранение токенов.

Основные компоненты:
    - CalendarAuth: OAuth2 аутентификация с Fernet-шифрованием
    - CalendarManager: CRUD событий, free/busy, life-planning пресеты
    - TasksManager: CRUD задач, daily top-3, weekly goals
    - CalendarEvent / CalendarTask: Data models
    - CalendarError и наследники: иерархия исключений

Quick Start:
    >>> from calendar_integration import CalendarAuth, CalendarManager, TasksManager
    >>> auth = CalendarAuth("credentials.json", "my-secret-key")
    >>> auth.authenticate()
    >>> cal = CalendarManager(auth)
    >>> events = cal.get_events(datetime.now(), datetime.now() + timedelta(days=7))
    >>> tasks = TasksManager(auth)
    >>> tasks.create_daily_top3(["Задача 1", "Задача 2", "Задача 3"], date.today())
"""

from .auth import CalendarAuth, SecureTokenStorage, require_auth, with_retry
from .calendar_manager import CalendarManager
from .config import CalendarConfig, COLOR_MAP, REMINDER_PRESETS
from .exceptions import (
    AuthError,
    CalendarError,
    ConflictResolutionError,
    CredentialsNotFoundError,
    EventNotFoundError,
    MaxRetriesExceededError,
    NetworkError,
    PermissionDeniedError,
    RateLimitError,
    SyncError,
    SyncTokenExpiredError,
    TaskNotFoundError,
    TokenExpiredError,
    TokenRefreshError,
    ValidationError,
)
from .models import CalendarEvent, CalendarTask, FreeBusyWindow, Reminder, TimeSlot
from .tasks_manager import TasksManager

__version__ = "1.0.0"
__author__ = "Life Planning Skill"

__all__ = [
    # Auth
    "CalendarAuth",
    "SecureTokenStorage",
    "require_auth",
    "with_retry",
    # Managers
    "CalendarManager",
    "TasksManager",
    # Config
    "CalendarConfig",
    "COLOR_MAP",
    "REMINDER_PRESETS",
    # Models
    "CalendarEvent",
    "CalendarTask",
    "FreeBusyWindow",
    "Reminder",
    "TimeSlot",
    # Exceptions
    "CalendarError",
    "AuthError",
    "CredentialsNotFoundError",
    "TokenExpiredError",
    "TokenRefreshError",
    "RateLimitError",
    "EventNotFoundError",
    "TaskNotFoundError",
    "SyncError",
    "SyncTokenExpiredError",
    "ConflictResolutionError",
    "MaxRetriesExceededError",
    "NetworkError",
    "PermissionDeniedError",
    "ValidationError",
]
