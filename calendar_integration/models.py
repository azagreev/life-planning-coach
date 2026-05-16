"""
Data models для модуля интеграции с Google Calendar.

Определяет dataclasses для представления событий, задач,
временных слотов и окон занятости.

Все модели поддерживают сериализацию в/из формата Google API.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, time as dt_time
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class Reminder:
    """
    Напоминание о событии.

    Attributes:
        method: Метод доставки — 'popup' (всплывающее) или 'email'.
        minutes: За сколько минут до события отправить напоминание (0..40320).

    Raises:
        ValueError: Если method не 'popup'/'email' или minutes вне диапазона.

    Example:
        >>> r = Reminder(method="popup", minutes=15)
        >>> r.to_api_dict()
        {'method': 'popup', 'minutes': 15}
    """

    method: str = "popup"
    minutes: int = 15

    def __post_init__(self) -> None:
        if self.method not in ("popup", "email"):
            raise ValueError(
                f"Некорректный метод напоминания: {self.method}. "
                f"Допустимые значения: 'popup', 'email'"
            )
        if not 0 <= self.minutes <= 40320:
            raise ValueError(
                f"Напоминание должно быть в диапазоне 0..40320 минут, "
                f"получено: {self.minutes}"
            )

    def to_api_dict(self) -> dict[str, Any]:
        """Сериализовать в формат Google Calendar API."""
        return {"method": self.method, "minutes": self.minutes}

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> "Reminder":
        """Создать Reminder из ответа Google Calendar API."""
        return cls(method=data.get("method", "popup"), minutes=data.get("minutes", 15))


@dataclass
class CalendarEvent:
    """
    Событие Google Calendar — центральная модель life planning интеграции.

    Attributes:
        title: Название события (обязательное).
        start: Дата/время начала (timezone-aware).
        end: Дата/время окончания (timezone-aware).
        id: Уникальный идентификатор события (None при создании).
        description: Описание / заметки.
        location: Место проведения.
        color_id: ID цвета (1-11).
        reminders: Список кастомных напоминаний.
        recurrence: Правила повторения в формате RRULE (RFC 5545).
        attendees: Список email-адресов участников.
        calendar_id: ID календаря.
        html_link: Публичная ссылка на событие.
        status: Статус — confirmed, tentative, cancelled.
        recurring_event_id: ID родительского события (для экземпляра серии).

    Raises:
        ValueError: Если title пустой или start >= end.

    Example:
        >>> from datetime import datetime, timezone
        >>> event = CalendarEvent(
        ...     title="Deep Work",
        ...     start=datetime(2025, 1, 15, 9, 0, tzinfo=timezone.utc),
        ...     end=datetime(2025, 1, 15, 11, 0, tzinfo=timezone.utc),
        ...     color_id="2",
        ... )
    """

    title: str = ""
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    id: Optional[str] = None
    description: str = ""
    location: str = ""
    color_id: str = "1"
    reminders: list[Reminder] = field(default_factory=lambda: [Reminder()])
    recurrence: list[str] = field(default_factory=list)
    attendees: list[str] = field(default_factory=list)
    calendar_id: str = "primary"
    html_link: Optional[str] = None
    status: str = "confirmed"
    recurring_event_id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("Название события (title) обязательно")
        if self.start and self.end and self.start >= self.end:
            raise ValueError(
                f"Время начала ({self.start}) должно быть раньше "
                f"времени окончания ({self.end})"
            )

    def duration_minutes(self) -> int:
        """Длительность события в минутах."""
        if not self.start or not self.end:
            return 0
        return int((self.end - self.start).total_seconds() / 60)

    def to_api_body(self) -> dict[str, Any]:
        """Сериализовать в тело запроса Google Calendar API."""
        if not self.start or not self.end:
            raise ValueError("start и end должны быть заданы для сериализации")

        tz = str(self.start.tzinfo) if self.start.tzinfo else "UTC"
        body: dict[str, Any] = {
            "summary": self.title,
            "start": {"dateTime": self.start.isoformat(), "timeZone": tz},
            "end": {"dateTime": self.end.isoformat(), "timeZone": tz},
            "colorId": self.color_id,
            "reminders": {
                "useDefault": False,
                "overrides": [r.to_api_dict() for r in self.reminders],
            },
        }
        if self.description:
            body["description"] = self.description
        if self.location:
            body["location"] = self.location
        if self.recurrence:
            body["recurrence"] = self.recurrence
        if self.attendees:
            body["attendees"] = [{"email": e} for e in self.attendees]
        return body

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> "CalendarEvent":
        """Создать CalendarEvent из ответа Google Calendar API."""

        def _parse_dt(dt_data: dict[str, str]) -> Optional[datetime]:
            if "dateTime" in dt_data:
                return datetime.fromisoformat(
                    dt_data["dateTime"].replace("Z", "+00:00")
                )
            if "date" in dt_data:
                return datetime.combine(
                    date.fromisoformat(dt_data["date"]), dt_time.min
                )
            return None

        start_data = data.get("start", {})
        end_data = data.get("end", {})

        reminders_raw = data.get("reminders", {}).get("overrides", [])
        reminders = (
            [Reminder.from_api_dict(r) for r in reminders_raw]
            if reminders_raw
            else [Reminder()]
        )

        return cls(
            title=data.get("summary", ""),
            start=_parse_dt(start_data),
            end=_parse_dt(end_data),
            id=data.get("id"),
            description=data.get("description", ""),
            location=data.get("location", ""),
            color_id=data.get("colorId", "1"),
            reminders=reminders,
            recurrence=data.get("recurrence", []),
            attendees=[a.get("email", "") for a in data.get("attendees", [])],
            calendar_id="primary",
            html_link=data.get("htmlLink"),
            status=data.get("status", "confirmed"),
            recurring_event_id=data.get("recurringEventId"),
        )

    def __repr__(self) -> str:
        if self.start and self.end:
            return (
                f"CalendarEvent('{self.title}', "
                f"{self.start:%Y-%m-%d %H:%M}-{self.end:%H:%M})"
            )
        return f"CalendarEvent('{self.title}')"


@dataclass
class CalendarTask:
    """
    Задача Google Tasks — модель для daily priorities и goal tracking.

    Важно: Google Tasks API хранит ТОЛЬКО дату (без времени).
    Для задач с точным временем используйте CalendarEvent.

    Attributes:
        title: Название задачи (обязательное, макс. 8192 символа).
        id: Уникальный идентификатор задачи (None при создании).
        notes: Описание / заметки (макс. 8192 символа).
        due: Срок выполнения (только дата).
        completed: Дата/время завершения.
        status: Статус — 'needsAction' или 'completed'.
        parent: ID родительской задачи (для подзадач).
        tasklist_id: ID списка задач.
        position: Позиция в списке.

    Raises:
        ValueError: Если title пустой.

    Example:
        >>> from datetime import date
        >>> task = CalendarTask(title="Закончить отчёт", due=date(2025, 1, 20))
    """

    title: str = ""
    id: Optional[str] = None
    notes: str = ""
    due: Optional[date] = None
    completed: Optional[datetime] = None
    status: str = "needsAction"
    parent: Optional[str] = None
    tasklist_id: str = "@default"
    position: str = ""

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("Название задачи (title) обязательно")

    def is_completed(self) -> bool:
        """Проверить, выполнена ли задача."""
        return self.status == "completed"

    def is_overdue(self) -> bool:
        """Проверить, просрочена ли задача."""
        if self.due is None or self.is_completed():
            return False
        return date.today() > self.due

    def to_api_body(self) -> dict[str, Any]:
        """Сериализовать в тело запроса Google Tasks API."""
        body: dict[str, Any] = {"title": self.title}
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
        return body

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> "CalendarTask":
        """Создать CalendarTask из ответа Google Tasks API."""
        due_raw = data.get("due")
        due: Optional[date] = None
        if due_raw:
            due = datetime.fromisoformat(due_raw.replace("Z", "+00:00")).date()

        completed_raw = data.get("completed")
        completed: Optional[datetime] = None
        if completed_raw:
            completed = datetime.fromisoformat(completed_raw.replace("Z", "+00:00"))

        return cls(
            title=data.get("title", ""),
            id=data.get("id"),
            notes=data.get("notes", ""),
            due=due,
            completed=completed,
            status=data.get("status", "needsAction"),
            parent=data.get("parent"),
            tasklist_id=data.get("tasklist_id", "@default"),
            position=data.get("position", ""),
        )

    def __repr__(self) -> str:
        status_mark = "✓" if self.is_completed() else "○"
        due_str = f", due={self.due}" if self.due else ""
        return f"CalendarTask({status_mark} '{self.title}'{due_str})"


@dataclass
class TimeSlot:
    """
    Временной слот — используется для free/busy анализа и планирования.

    Attributes:
        start: Начало слота.
        end: Окончание слота.
        is_free: True = свободный, False = занятый.

    Raises:
        ValueError: Если start >= end.

    Example:
        >>> from datetime import datetime, timezone
        >>> slot = TimeSlot(
        ...     start=datetime(2025, 1, 15, 9, 0, tzinfo=timezone.utc),
        ...     end=datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc),
        ... )
        >>> slot.duration_minutes()
        60
    """

    start: datetime
    end: datetime
    is_free: bool = True

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError(
                f"Начало слота ({self.start}) должно быть раньше окончания ({self.end})"
            )

    def duration_minutes(self) -> int:
        """Длительность слота в минутах."""
        return int((self.end - self.start).total_seconds() / 60)

    def overlaps(self, other: "TimeSlot") -> bool:
        """Проверить пересечение с другим слотом."""
        return self.start < other.end and other.start < self.end

    def contains(self, point: datetime) -> bool:
        """Проверить, содержит ли слот указанную точку во времени."""
        return self.start <= point < self.end

    def split_at(self, boundary: datetime) -> tuple[Optional["TimeSlot"], Optional["TimeSlot"]]:
        """Разделить слот по указанной границе."""
        if boundary <= self.start:
            return None, self
        if boundary >= self.end:
            return self, None
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


@dataclass
class FreeBusyWindow:
    """
    Окно занятости — результат freeBusy запроса к Google Calendar API.

    Attributes:
        email: Email пользователя / ID календаря.
        busy_slots: Список занятых интервалов.
        errors: Список ошибок (если календарь недоступен).

    Example:
        >>> from datetime import datetime, timezone
        >>> window = FreeBusyWindow(
        ...     email="user@example.com",
        ...     busy_slots=[
        ...         TimeSlot(
        ...             start=datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc),
        ...             end=datetime(2025, 1, 15, 11, 0, tzinfo=timezone.utc),
        ...             is_free=False,
        ...         )
        ...     ],
        ... )
    """

    email: str = ""
    busy_slots: list[TimeSlot] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def is_available(self) -> bool:
        """Проверить, есть ли занятые слоты."""
        return len(self.busy_slots) == 0

    def __repr__(self) -> str:
        status = "available" if self.is_available else f"{len(self.busy_slots)} busy"
        return f"FreeBusyWindow({self.email}: {status})"
