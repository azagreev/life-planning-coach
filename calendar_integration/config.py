"""
Конфигурация модуля интеграции с Google Calendar.

Содержит цветовую схему для life planning, пресеты напоминаний,
константы и настройки по умолчанию.

Цветовая схема (Life Planning):
    - deep_work (Sage green)     — фокусная работа по целям
    - woop (Peacock blue)        — WOOP-сессии
    - weekly_review (Banana yellow) — Weekly Review
    - family (Lavender purple)   — семья / личное время
    - exercise (Tangerine orange) — спорт / здоровье
    - reading (Flamingo pink)    — чтение / обучение
    - urgent (Tomato red)        — срочные / дедлайны
    - personal (Grape)           — личные задачи

Примеры:
    from calendar_integration.config import COLOR_MAP, REMINDER_PRESETS
    color_id = COLOR_MAP["deep_work"]
    reminders = REMINDER_PRESETS["weekly_review"]
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Цветовая карта Google Calendar event colors
# ---------------------------------------------------------------------------
# ID цвета -> hex-код (background)
_GOOGLE_EVENT_COLORS: dict[str, str] = {
    "1": "#7986cb",  # Lavender
    "2": "#33b679",  # Sage
    "3": "#8e24aa",  # Grape
    "4": "#e67c73",  # Flamingo
    "5": "#f6c026",  # Banana
    "6": "#f5511d",  # Tangerine
    "7": "#039be5",  # Peacock
    "8": "#616161",  # Graphite
    "9": "#3f51b5",  # Blueberry
    "10": "#0b8043",  # Basil
    "11": "#d50000",  # Tomato
}

# ---------------------------------------------------------------------------
# Life Planning цветовая схема: тип события -> ID цвета Google Calendar
# ---------------------------------------------------------------------------
COLOR_MAP: dict[str, str] = {
    "deep_work": "2",      # Sage green — фокусная работа по целям
    "woop": "7",           # Peacock blue — WOOP-сессии / визуализация
    "weekly_review": "5",  # Banana yellow — Weekly Review
    "family": "1",         # Lavender purple — семья / личное время
    "exercise": "6",       # Tangerine orange — спорт / здоровье
    "reading": "4",        # Flamingo pink — чтение / обучение
    "urgent": "11",        # Tomato red — срочные / дедлайны
    "personal": "3",       # Grape — личные задачи
    "meeting": "9",        # Blueberry — встречи
    "planning": "10",      # Basil — планирование
    "default": "8",        # Graphite — значение по умолчанию
}

# Обратное отображение: ID цвета -> тип события
COLOR_NAME_BY_ID: dict[str, str] = {
    color_id: name for name, color_id in COLOR_MAP.items()
}

# ---------------------------------------------------------------------------
# Пресеты напоминаний
# ---------------------------------------------------------------------------
REMINDER_PRESETS: dict[str, list[dict[str, Any]]] = {
    "default": [
        {"method": "popup", "minutes": 15},
    ],
    "weekly_review": [
        {"method": "popup", "minutes": 60},
        {"method": "popup", "minutes": 15},
    ],
    "woop": [
        {"method": "popup", "minutes": 5},
    ],
    "milestone": [
        {"method": "popup", "minutes": 1440},   # за сутки
        {"method": "popup", "minutes": 60},     # за час
    ],
    "deep_work": [
        {"method": "popup", "minutes": 5},
    ],
    "exercise": [
        {"method": "popup", "minutes": 30},
    ],
    "urgent": [
        {"method": "popup", "minutes": 60},
        {"method": "popup", "minutes": 15},
        {"method": "popup", "minutes": 0},
    ],
    "morning_routine": [
        {"method": "popup", "minutes": 10},
    ],
}

# ---------------------------------------------------------------------------
# Константы
# ---------------------------------------------------------------------------
DEFAULT_CALENDAR_ID: str = "primary"
DEFAULT_TASKLIST_ID: str = "@default"
DEFAULT_TIMEZONE: str = "UTC"
DEFAULT_WORK_HOURS_START: int = 9
DEFAULT_WORK_HOURS_END: int = 18
DEFAULT_REMINDER_MINUTES: int = 15

# Retry конфигурация
MAX_RETRIES: int = 5
BASE_RETRY_DELAY: float = 1.0
MAX_RETRY_DELAY: float = 60.0
RETRYABLE_STATUS_CODES: set[int] = {429, 500, 502, 503, 504}

# Google API endpoints / constants
GOOGLE_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
GOOGLE_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_REVOKE_URI: str = "https://oauth2.googleapis.com/revoke"

# Scopes
DEFAULT_SCOPES: list[str] = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
]

MINIMAL_SCOPES: list[str] = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/tasks",
]

# WOOP recurring rule: ежедневно в 07:00
WOOP_RRULE: list[str] = ["RRULE:FREQ=DAILY"]

# Weekly Review recurring rule: каждое воскресенье в 19:00
WEEKLY_REVIEW_RRULE: list[str] = ["RRULE:FREQ=WEEKLY;BYDAY=SU"]


# ---------------------------------------------------------------------------
# Configuration class
# ---------------------------------------------------------------------------
@dataclass
class CalendarConfig:
    """
    Конфигурация модуля интеграции с Google Calendar.

    Attributes:
        timezone: Часовой пояс по умолчанию.
        work_hours_start: Начало рабочего дня (час, 0-23).
        work_hours_end: Конец рабочего дня (час, 0-23).
        default_reminder_minutes: Стандартное напоминание (минуты до события).
        max_retries: Максимальное количество повторных попыток при ошибке API.
        base_retry_delay: Базовая задержка для exponential backoff (секунды).
        max_retry_delay: Максимальная задержка между попытками (секунды).
        calendar_id: ID календаря по умолчанию.
        tasklist_id: ID списка задач по умолчанию.
        scopes: Список OAuth scopes.
    """

    timezone: str = DEFAULT_TIMEZONE
    work_hours_start: int = DEFAULT_WORK_HOURS_START
    work_hours_end: int = DEFAULT_WORK_HOURS_END
    default_reminder_minutes: int = DEFAULT_REMINDER_MINUTES
    max_retries: int = MAX_RETRIES
    base_retry_delay: float = BASE_RETRY_DELAY
    max_retry_delay: float = MAX_RETRY_DELAY
    calendar_id: str = DEFAULT_CALENDAR_ID
    tasklist_id: str = DEFAULT_TASKLIST_ID
    scopes: list[str] = field(default_factory=lambda: list(DEFAULT_SCOPES))

    def get_color_id(self, event_type: str) -> str:
        """
        Получить ID цвета Google Calendar по типу события.

        Args:
            event_type: Тип события (например, 'deep_work', 'meeting').

        Returns:
            ID цвета (строка '1'-'11').

        Example:
            >>> config = CalendarConfig()
            >>> config.get_color_id("deep_work")
            '2'
            >>> config.get_color_id("unknown_type")
            '8'
        """
        color_id = COLOR_MAP.get(event_type, COLOR_MAP["default"])
        logger.debug("Цвет для типа '%s': %s", event_type, color_id)
        return color_id

    def get_color_name(self, color_id: str) -> str:
        """
        Получить название типа события по ID цвета.

        Args:
            color_id: ID цвета Google Calendar.

        Returns:
            Название типа события или 'unknown'.
        """
        return COLOR_NAME_BY_ID.get(color_id, "unknown")

    def get_reminder_preset(self, preset_name: str) -> list[dict[str, Any]]:
        """
        Получить пресет напоминаний по имени.

        Args:
            preset_name: Имя пресета (например, 'weekly_review', 'woop').

        Returns:
            Список словарей с напоминаниями. Возвращает 'default' если пресет не найден.

        Example:
            >>> config = CalendarConfig()
            >>> config.get_reminder_preset("woop")
            [{'method': 'popup', 'minutes': 5}]
        """
        preset = REMINDER_PRESETS.get(preset_name, REMINDER_PRESETS["default"])
        logger.debug("Пресет напоминаний '%s': %s", preset_name, preset)
        return preset

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CalendarConfig":
        """
        Создать конфигурацию из словаря.

        Args:
            data: Словарь с настройками.

        Returns:
            Экземпляр CalendarConfig.
        """
        return cls(
            timezone=data.get("timezone", DEFAULT_TIMEZONE),
            work_hours_start=data.get("work_hours_start", DEFAULT_WORK_HOURS_START),
            work_hours_end=data.get("work_hours_end", DEFAULT_WORK_HOURS_END),
            default_reminder_minutes=data.get(
                "default_reminder_minutes", DEFAULT_REMINDER_MINUTES
            ),
            max_retries=data.get("max_retries", MAX_RETRIES),
            base_retry_delay=data.get("base_retry_delay", BASE_RETRY_DELAY),
            max_retry_delay=data.get("max_retry_delay", MAX_RETRY_DELAY),
            calendar_id=data.get("calendar_id", DEFAULT_CALENDAR_ID),
            tasklist_id=data.get("tasklist_id", DEFAULT_TASKLIST_ID),
            scopes=data.get("scopes", list(DEFAULT_SCOPES)),
        )
