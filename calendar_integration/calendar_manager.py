"""
Менеджер событий Google Calendar.

Предоставляет CRUD-операции для событий, поиск свободных слотов,
управление повторяющимися событиями и life-planning пресеты:
    - Weekly Review reminder
    - WOOP сессия
    - Milestone события
    - Time blocks (deep work и др.)

Все методы включают retry-логику с exponential backoff и
автоматическое обновление токена.

Example:
    >>> from calendar_integration.auth import CalendarAuth
    >>> from calendar_integration.calendar_manager import CalendarManager
    >>> auth = CalendarAuth("credentials.json", "secret")
    >>> manager = CalendarManager(auth)
    >>> events = manager.get_events(date_from=datetime.now(), date_to=datetime.now() + timedelta(days=7))
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, time as dt_time
from zoneinfo import ZoneInfo
from typing import Any, Optional

from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from .auth import CalendarAuth, with_retry
from .config import (
    COLOR_MAP,
    DEFAULT_CALENDAR_ID,
    DEFAULT_WORK_HOURS_START,
    DEFAULT_WORK_HOURS_END,
    REMINDER_PRESETS,
    WEEKLY_REVIEW_RRULE,
    WOOP_RRULE,
)
from .exceptions import (
    AuthError,
    CalendarError,
    EventNotFoundError,
    RateLimitError,
    ValidationError,
)
from .models import CalendarEvent, Reminder, TimeSlot

logger = logging.getLogger(__name__)


class CalendarManager:
    """
    Менеджер для работы с событиями Google Calendar.

    Управляет созданием, чтением, обновлением и удалением событий,
    а также предоставляет вспомогательные методы для планирования
    (свободные слоты, life-planning пресеты).

    Attributes:
        _auth: Экземпляр CalendarAuth для аутентификации.
        _service: Lazy-initialized сервис Calendar API.

    Example:
        >>> manager = CalendarManager(auth)
        >>> # Получить встречи на неделю
        >>> events = manager.get_events(
        ...     date_from=datetime(2025, 1, 13),
        ...     date_to=datetime(2025, 1, 20),
        ... )
        >>> # Создать событие deep work
        >>> event = manager.create_time_block(
        ...     title="Фокусная работа",
        ...     start=datetime(2025, 1, 15, 9, 0),
        ...     duration=120,
        ...     color="deep_work",
        ... )
    """

    def __init__(self, auth: CalendarAuth) -> None:
        """
        Инициализировать CalendarManager.

        Args:
            auth: Экземпляр CalendarAuth с настроенной аутентификацией.
        """
        self._auth = auth
        self._service: Optional[Resource] = None
        logger.debug("CalendarManager инициализирован")

    # ------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------

    def _get_service(self) -> Resource:
        """
        Получить или создать сервис Calendar API.

        Returns:
            Экземпляр googleapiclient.discovery.Resource для Calendar API v3.

        Raises:
            AuthError: Если не удалось создать сервис.
        """
        if self._service is None:
            self._service = self._auth.build_service("calendar", "v3")
        return self._service

    def _parse_event_response(self, data: dict[str, Any]) -> CalendarEvent:
        """Преобразовать ответ API в CalendarEvent."""
        return CalendarEvent.from_api_response(data)

    def _execute_api_call(self, request: Any) -> Any:
        """
        Выполнить API-запрос с retry-логикой.

        Args:
            request: Объект запроса Google API.

        Returns:
            Результат выполнения запроса.
        """
        @with_retry(auth_instance=self._auth)
        def _do_execute() -> Any:
            return request.execute()

        return _do_execute()

    # ------------------------------------------------------------------
    # CRUD событий
    # ------------------------------------------------------------------

    def get_events(
        self,
        date_from: datetime,
        date_to: datetime,
        calendar_id: str = DEFAULT_CALENDAR_ID,
        query: Optional[str] = None,
        max_results: int = 250,
    ) -> list[CalendarEvent]:
        """
        Получить список событий за указанный период.

        Args:
            date_from: Начало периода (включительно).
            date_to: Конец периода (включительно).
            calendar_id: ID календаря (по умолчанию 'primary').
            query: Текстовый поиск (опционально).
            max_results: Максимальное количество результатов.

        Returns:
            Список CalendarEvent, отсортированных по времени начала.

        Raises:
            AuthError: При ошибках аутентификации.
            ValidationError: Если date_from >= date_to.

        Example:
            >>> from datetime import datetime, timedelta
            >>> events = manager.get_events(
            ...     date_from=datetime.now(),
            ...     date_to=datetime.now() + timedelta(days=7),
            ...     query="standup",
            ... )
        """
        if date_from >= date_to:
            raise ValidationError(
                "date_from должен быть раньше date_to",
                field="date_from",
            )

        self._auth.refresh_if_needed()
        service = self._get_service()

        time_min = date_from.isoformat()
        time_max = date_to.isoformat()

        logger.info(
            "Получение событий: %s — %s (calendar: %s)",
            time_min, time_max, calendar_id,
        )

        try:
            result = self._execute_api_call(
                service.events().list(
                    calendarId=calendar_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    maxResults=max_results,
                    singleEvents=True,  # Развернуть повторяющиеся события
                    orderBy="startTime",
                    q=query,
                )
            )

            items = result.get("items", [])
            events = [self._parse_event_response(item) for item in items]
            logger.info("Получено %d событий", len(events))
            return events

        except HttpError as exc:
            self._handle_http_error(exc, f"get_events({calendar_id})")
            raise  # для type checker

    def get_event(
        self, event_id: str, calendar_id: str = DEFAULT_CALENDAR_ID
    ) -> CalendarEvent:
        """
        Получить одно событие по ID.

        Args:
            event_id: Идентификатор события.
            calendar_id: ID календаря.

        Returns:
            CalendarEvent.

        Raises:
            EventNotFoundError: Если событие не найдено.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.debug("Получение события %s из календаря %s", event_id, calendar_id)

        try:
            result = self._execute_api_call(
                service.events().get(calendarId=calendar_id, eventId=event_id)
            )
            return self._parse_event_response(result)

        except HttpError as exc:
            if hasattr(exc, "resp") and exc.resp.status == 404:
                raise EventNotFoundError(event_id, calendar_id) from exc
            self._handle_http_error(exc, f"get_event({event_id})")
            raise  # для type checker

    def create_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        description: str = "",
        color_id: Optional[str] = None,
        reminders: Optional[list[dict[str, Any]]] = None,
        recurrence: Optional[list[str]] = None,
        attendees: Optional[list[str]] = None,
        calendar_id: str = DEFAULT_CALENDAR_ID,
    ) -> CalendarEvent:
        """
        Создать событие в календаре.

        Args:
            title: Название события.
            start: Дата/время начала (timezone-aware).
            end: Дата/время окончания.
            description: Описание.
            color_id: ID цвета (1-11). Если None — используется цвет по умолчанию.
            reminders: Список напоминаний [{'method': 'popup', 'minutes': 15}, ...].
            recurrence: Правила повторения RRULE.
            attendees: Список email участников.
            calendar_id: ID календаря.

        Returns:
            Созданное CalendarEvent с заполненным id.

        Raises:
            ValidationError: Если title пустой или start >= end.
            AuthError: При ошибках аутентификации.

        Example:
            >>> from datetime import datetime, timezone
            >>> event = manager.create_event(
            ...     title="Встреча с командой",
            ...     start=datetime(2025, 1, 15, 14, 0, tzinfo=timezone.utc),
            ...     end=datetime(2025, 1, 15, 15, 0, tzinfo=timezone.utc),
            ...     color_id="9",
            ...     reminders=[{"method": "popup", "minutes": 15}],
            ... )
        """
        if not title:
            raise ValidationError("Название события обязательно", field="title")
        if start >= end:
            raise ValidationError(
                "Время начала должно быть раньше времени окончания",
                field="start",
            )

        self._auth.refresh_if_needed()
        service = self._get_service()

        # Формируем reminders
        reminder_list = [Reminder(**r) for r in (reminders or [{"method": "popup", "minutes": 15}])]

        event = CalendarEvent(
            title=title,
            start=start,
            end=end,
            description=description,
            color_id=color_id or COLOR_MAP["default"],
            reminders=reminder_list,
            recurrence=recurrence or [],
            attendees=attendees or [],
            calendar_id=calendar_id,
        )

        logger.info(
            "Создание события '%s' (%s — %s)", title, start.isoformat(), end.isoformat()
        )

        try:
            result = self._execute_api_call(
                service.events().insert(
                    calendarId=calendar_id,
                    body=event.to_api_body(),
                    sendUpdates="all",
                )
            )
            created = self._parse_event_response(result)
            logger.info("Событие создано: id=%s", created.id)
            return created

        except HttpError as exc:
            self._handle_http_error(exc, f"create_event({title})")
            raise  # для type checker

    def update_event(
        self,
        event_id: str,
        calendar_id: str = DEFAULT_CALENDAR_ID,
        **kwargs: Any,
    ) -> CalendarEvent:
        """
        Обновить существующее событие.

        Args:
            event_id: Идентификатор события.
            calendar_id: ID календаря.
            **kwargs: Поля для обновения (title, start, end, description,
                color_id, reminders и т.д.).

        Returns:
            Обновлённое CalendarEvent.

        Raises:
            EventNotFoundError: Если событие не найдено.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.info("Обновление события %s: %s", event_id, kwargs)

        try:
            # Получаем текущее событие
            current = self._execute_api_call(
                service.events().get(calendarId=calendar_id, eventId=event_id)
            )

            # Обновляем переданные поля
            for key, value in kwargs.items():
                if key in ("start", "end") and isinstance(value, datetime):
                    tz = str(value.tzinfo) if value.tzinfo else "UTC"
                    current[key] = {"dateTime": value.isoformat(), "timeZone": tz}
                elif key == "title":
                    current["summary"] = value
                elif key == "reminders" and isinstance(value, list):
                    current["reminders"] = {
                        "useDefault": False,
                        "overrides": value,
                    }
                elif key == "attendees" and isinstance(value, list):
                    current["attendees"] = [{"email": e} for e in value]
                else:
                    current[key] = value

            result = self._execute_api_call(
                service.events().update(
                    calendarId=calendar_id,
                    eventId=event_id,
                    body=current,
                    sendUpdates="all",
                )
            )
            updated = self._parse_event_response(result)
            logger.info("Событие %s обновлено", event_id)
            return updated

        except HttpError as exc:
            if hasattr(exc, "resp") and exc.resp.status == 404:
                raise EventNotFoundError(event_id, calendar_id) from exc
            self._handle_http_error(exc, f"update_event({event_id})")
            raise  # для type checker

    def delete_event(
        self, event_id: str, calendar_id: str = DEFAULT_CALENDAR_ID
    ) -> None:
        """
        Удалить событие из календаря.

        Args:
            event_id: Идентификатор события.
            calendar_id: ID календаря.

        Raises:
            EventNotFoundError: Если событие не найдено.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.info("Удаление события %s из календаря %s", event_id, calendar_id)

        try:
            self._execute_api_call(
                service.events().delete(
                    calendarId=calendar_id,
                    eventId=event_id,
                    sendUpdates="all",
                )
            )
            logger.info("Событие %s удалено", event_id)

        except HttpError as exc:
            if hasattr(exc, "resp") and exc.resp.status == 404:
                raise EventNotFoundError(event_id, calendar_id) from exc
            self._handle_http_error(exc, f"delete_event({event_id})")

    # ------------------------------------------------------------------
    # Free / Busy — свободные слоты
    # ------------------------------------------------------------------

    def get_free_slots(
        self,
        target_date: date,
        duration_minutes: int,
        work_start: Optional[int] = None,
        work_end: Optional[int] = None,
        calendar_id: str = DEFAULT_CALENDAR_ID,
        timezone: str = "UTC",
    ) -> list[TimeSlot]:
        """
        Найти свободные временные слоты на указанную дату.

        Args:
            target_date: Дата для поиска.
            duration_minutes: Минимальная длительность слота (минуты).
            work_start: Начало рабочего дня (час, 0-23). По умолчанию 9.
            work_end: Конец рабочего дня (час, 0-23). По умолчанию 18.
            calendar_id: ID календаря.
            timezone: Часовой пояс.

        Returns:
            Список свободных TimeSlot подходящей длительности.

        Raises:
            ValidationError: Если duration_minutes <= 0.

        Example:
            >>> from datetime import date
            >>> slots = manager.get_free_slots(
            ...     target_date=date(2025, 1, 15),
            ...     duration_minutes=60,
            ...     work_start=9,
            ...     work_end=18,
            ... )
            >>> for slot in slots:
            ...     print(f"Свободно: {slot.start:%H:%M} - {slot.end:%H:%M}")
        """
        if duration_minutes <= 0:
            raise ValidationError(
                "duration_minutes должен быть положительным", field="duration_minutes"
            )

        work_start = work_start or DEFAULT_WORK_HOURS_START
        work_end = work_end or DEFAULT_WORK_HOURS_END

        self._auth.refresh_if_needed()
        service = self._get_service()

        # Формируем границы рабочего дня
        day_start = datetime.combine(target_date, dt_time(work_start, 0))
        day_end = datetime.combine(target_date, dt_time(work_end, 0))

        logger.info(
            "Поиск свободных слотов на %s (%d мин, %02d:00-%02d:00)",
            target_date, duration_minutes, work_start, work_end,
        )

        try:
            # Запрос freeBusy
            body = {
                "timeMin": day_start.isoformat(),
                "timeMax": day_end.isoformat(),
                "timeZone": timezone,
                "items": [{"id": calendar_id}],
            }

            result = self._execute_api_call(service.freebusy().query(body=body))

            # Извлекаем занятые слоты
            calendars = result.get("calendars", {})
            cal_data = calendars.get(calendar_id, {})
            busy_raw = cal_data.get("busy", [])

            # Преобразуем в TimeSlot
            busy_slots: list[TimeSlot] = []
            for b in busy_raw:
                b_start = datetime.fromisoformat(b["start"].replace("Z", "+00:00")).replace(tzinfo=None)
                b_end = datetime.fromisoformat(b["end"].replace("Z", "+00:00")).replace(tzinfo=None)
                busy_slots.append(TimeSlot(start=b_start, end=b_end, is_free=False))

            # Ищем свободные слоты
            free_slots = self._find_free_intervals(
                day_start, day_end, busy_slots, duration_minutes
            )

            logger.info(
                "Найдено %d свободных слотов (занято: %d)",
                len(free_slots), len(busy_slots),
            )
            return free_slots

        except HttpError as exc:
            self._handle_http_error(exc, "get_free_slots")
            raise  # для type checker

    @staticmethod
    def _find_free_intervals(
        day_start: datetime,
        day_end: datetime,
        busy_slots: list[TimeSlot],
        min_duration_minutes: int,
    ) -> list[TimeSlot]:
        """
        Найти свободные интервалы между занятыми слотами.

        Args:
            day_start: Начало рабочего дня.
            day_end: Конец рабочего дня.
            busy_slots: Список занятых слотов.
            min_duration_minutes: Минимальная длительность свободного слота.

        Returns:
            Список свободных TimeSlot.
        """
        min_duration = timedelta(minutes=min_duration_minutes)
        free_slots: list[TimeSlot] = []

        # Сортируем занятые слоты
        sorted_busy = sorted(busy_slots, key=lambda s: s.start)

        # Объединяем пересекающиеся занятые слоты
        merged_busy: list[TimeSlot] = []
        for slot in sorted_busy:
            if not merged_busy:
                merged_busy.append(slot)
            elif slot.start <= merged_busy[-1].end:
                # Пересечение — расширяем текущий
                merged_busy[-1] = TimeSlot(
                    start=merged_busy[-1].start,
                    end=max(merged_busy[-1].end, slot.end),
                    is_free=False,
                )
            else:
                merged_busy.append(slot)

        # Ищем свободные промежутки
        current = day_start
        for busy in merged_busy:
            if current + min_duration <= busy.start:
                free_slots.append(
                    TimeSlot(start=current, end=busy.start, is_free=True)
                )
            current = max(current, busy.end)

        # Проверяем остаток дня
        if current + min_duration <= day_end:
            free_slots.append(TimeSlot(start=current, end=day_end, is_free=True))

        return free_slots

    # ------------------------------------------------------------------
    # Life Planning пресеты
    # ------------------------------------------------------------------

    def create_weekly_review_reminder(
        self,
        timezone: str = "UTC",
        hour: int = 19,
        minute: int = 0,
        calendar_id: str = DEFAULT_CALENDAR_ID,
    ) -> CalendarEvent:
        """
        Создать еженедельное повторяющееся напоминание о Weekly Review.

        Напоминание создаётся на каждое воскресенье в указанное время.
        Используется цвет weekly_review (Banana yellow).

        Args:
            timezone: Часовой пояс.
            hour: Час начала (0-23). По умолчанию 19.
            minute: Минута начала (0-59). По умолчанию 0.
            calendar_id: ID календаря.

        Returns:
            Созданное CalendarEvent с правилом повторения.

        Example:
            >>> event = manager.create_weekly_review_reminder(
            ...     timezone="Europe/Moscow", hour=20, minute=0
            ... )
        """
        # Находим ближайшее воскресенье
        today = date.today()
        days_until_sunday = (6 - today.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7  # Если сегодня воскресенье — берём следующее

        sunday = today + timedelta(days=days_until_sunday)
        start = datetime.combine(sunday, dt_time(hour, minute), tzinfo=ZoneInfo(timezone))
        end = start + timedelta(minutes=30)

        description = (
            "Weekly Review — ретроспектива недели:\n"
            "1. Что прошло хорошо?\n"
            "2. Что можно улучшить?\n"
            "3. Какие уроки извлечены?\n"
            "4. Приоритеты на следующую неделю"
        )

        logger.info(
            "Создание Weekly Review reminder (воскресенье %s %02d:%02d)",
            sunday, hour, minute,
        )

        return self.create_event(
            title="Weekly Review",
            start=start,
            end=end,
            description=description,
            color_id=COLOR_MAP["weekly_review"],
            reminders=REMINDER_PRESETS["weekly_review"],
            recurrence=WEEKLY_REVIEW_RRULE,
            calendar_id=calendar_id,
        )

    def create_woop_reminder(
        self,
        timezone: str = "UTC",
        hour: int = 7,
        minute: int = 0,
        calendar_id: str = DEFAULT_CALENDAR_ID,
    ) -> CalendarEvent:
        """
        Создать ежедневное повторяющееся напоминание о WOOP-сессии.

        WOOP = Wish, Outcome, Obstacle, Plan.
        Используется цвет woop (Peacock blue).

        Args:
            timezone: Часовой пояс.
            hour: Час начала (0-23). По умолчанию 7 (утро).
            minute: Минута начала. По умолчанию 0.
            calendar_id: ID календаря.

        Returns:
            Созданное CalendarEvent с ежедневным правилом повторения.

        Example:
            >>> event = manager.create_woop_reminder(
            ...     timezone="Europe/Moscow", hour=7, minute=30
            ... )
        """
        tomorrow = date.today() + timedelta(days=1)
        start = datetime.combine(tomorrow, dt_time(hour, minute), tzinfo=ZoneInfo(timezone))
        end = start + timedelta(minutes=15)

        description = (
            "WOOP-сессия (Wish, Outcome, Obstacle, Plan):\n"
            "1. Wish — Какое желание хочешь реализовать сегодня?\n"
            "2. Outcome — Какой лучший результат представляешь?\n"
            "3. Obstacle — Какое главное препятствие?\n"
            "4. Plan — Если X, то Y (implementation intention)"
        )

        logger.info(
            "Создание WOOP reminder (ежедневно %02d:%02d)", hour, minute
        )

        return self.create_event(
            title="WOOP Сессия",
            start=start,
            end=end,
            description=description,
            color_id=COLOR_MAP["woop"],
            reminders=REMINDER_PRESETS["woop"],
            recurrence=WOOP_RRULE,
            calendar_id=calendar_id,
        )

    def create_milestone_event(
        self,
        title: str,
        milestone_date: datetime,
        description: str = "",
        advance_reminder_days: int = 7,
        calendar_id: str = DEFAULT_CALENDAR_ID,
    ) -> CalendarEvent:
        """
        Создать событие-веху (milestone) с предварительным напоминанием.

        Используется цвет urgent (Tomato red) для визуальной важности.

        Args:
            title: Название вехи.
            milestone_date: Дата и время вехи.
            description: Описание.
            advance_reminder_days: За сколько дней предупредить. По умолчанию 7.
            calendar_id: ID календаря.

        Returns:
            Созданное CalendarEvent.

        Example:
            >>> from datetime import datetime
            >>> event = manager.create_milestone_event(
            ...     title="Завершить проект Alpha",
            ...     milestone_date=datetime(2025, 3, 31, 18, 0),
            ...     description="Финальный дедлайн проекта Alpha",
            ... )
        """
        end_time = milestone_date + timedelta(minutes=30)

        full_description = description or f"Milestone: {title}"

        reminders = [
            {"method": "popup", "minutes": advance_reminder_days * 24 * 60},
            {"method": "popup", "minutes": 60},
        ]

        logger.info(
            "Создание milestone '%s' на %s (напоминание за %d дней)",
            title, milestone_date.isoformat(), advance_reminder_days,
        )

        return self.create_event(
            title=f"Milestone: {title}",
            start=milestone_date,
            end=end_time,
            description=full_description,
            color_id=COLOR_MAP["urgent"],
            reminders=reminders,
            calendar_id=calendar_id,
        )

    def create_time_block(
        self,
        title: str,
        start: datetime,
        duration: int,
        color: str = "deep_work",
        description: str = "",
        calendar_id: str = DEFAULT_CALENDAR_ID,
    ) -> CalendarEvent:
        """
        Создать временной блок (time block) для фокусной работы.

        Time blocking — техника управления временем, при которой
        выделяются конкретные блоки времени для конкретных задач.

        Args:
            title: Название блока.
            start: Время начала.
            duration: Длительность в минутах.
            color: Тип блока (deep_work, exercise, family и т.д.).
            description: Описание.
            calendar_id: ID календаря.

        Returns:
            Созданное CalendarEvent.

        Example:
            >>> from datetime import datetime
            >>> event = manager.create_time_block(
            ...     title="Глубокая работа — написание статьи",
            ...     start=datetime(2025, 1, 15, 9, 0),
            ...     duration=120,
            ...     color="deep_work",
            ...     description="Фокусное время для написания",
            ... )
        """
        end = start + timedelta(minutes=duration)
        color_id = COLOR_MAP.get(color, COLOR_MAP["default"])
        reminder_preset = REMINDER_PRESETS.get(color, REMINDER_PRESETS["default"])

        logger.info(
            "Создание time block '%s' (%d мин, цвет: %s)",
            title, duration, color,
        )

        return self.create_event(
            title=title,
            start=start,
            end=end,
            description=description,
            color_id=color_id,
            reminders=reminder_preset,
            calendar_id=calendar_id,
        )

    def create_recurring_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        recurrence_rule: list[str],
        description: str = "",
        color_id: Optional[str] = None,
        reminders: Optional[list[dict[str, Any]]] = None,
        calendar_id: str = DEFAULT_CALENDAR_ID,
    ) -> CalendarEvent:
        """
        Создать повторяющееся событие.

        Args:
            title: Название события.
            start: Время начала первого экземпляра.
            end: Время окончания первого экземпляра.
            recurrence_rule: Правила RRULE (например, ['RRULE:FREQ=WEEKLY;BYDAY=MO']).
            description: Описание.
            color_id: ID цвета.
            reminders: Список напоминаний.
            calendar_id: ID календаря.

        Returns:
            Созданное CalendarEvent.

        Example:
            >>> from datetime import datetime
            >>> event = manager.create_recurring_event(
            ...     title="Ежедневный standup",
            ...     start=datetime(2025, 1, 15, 10, 0),
            ...     end=datetime(2025, 1, 15, 10, 30),
            ...     recurrence_rule=["RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"],
            ...     color_id="9",
            ... )
        """
        return self.create_event(
            title=title,
            start=start,
            end=end,
            description=description,
            color_id=color_id or COLOR_MAP["default"],
            reminders=reminders,
            recurrence=recurrence_rule,
            calendar_id=calendar_id,
        )

    def get_event_instances(
        self, recurring_event_id: str, calendar_id: str = DEFAULT_CALENDAR_ID
    ) -> list[CalendarEvent]:
        """
        Получить все экземпляры повторяющегося события.

        Args:
            recurring_event_id: ID родительского события.
            calendar_id: ID календаря.

        Returns:
            Список CalendarEvent — экземпляры серии.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.debug(
            "Получение экземпляров повторяющегося события %s", recurring_event_id
        )

        try:
            result = self._execute_api_call(
                service.events().instances(
                    calendarId=calendar_id, eventId=recurring_event_id
                )
            )
            items = result.get("items", [])
            events = [self._parse_event_response(item) for item in items]
            logger.info("Получено %d экземпляров", len(events))
            return events

        except HttpError as exc:
            self._handle_http_error(exc, f"get_event_instances({recurring_event_id})")
            raise  # для type checker

    def delete_event_series(
        self, recurring_event_id: str, calendar_id: str = DEFAULT_CALENDAR_ID
    ) -> None:
        """
        Удалить серию повторяющихся событий.

        Args:
            recurring_event_id: ID родительского события серии.
            calendar_id: ID календаря.
        """
        self.delete_event(recurring_event_id, calendar_id)
        logger.info("Серия событий %s удалена", recurring_event_id)

    # ------------------------------------------------------------------
    # Вспомогательные методы
    # ------------------------------------------------------------------

    def get_available_colors(self) -> dict[str, dict[str, str]]:
        """
        Получить палитру доступных цветов Google Calendar.

        Returns:
            Словарь {color_id: {background, foreground}}.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.debug("Получение палитры цветов")

        try:
            result = self._execute_api_call(service.colors().get())
            event_colors = result.get("event", {})
            return {
                color_id: {
                    "background": info.get("background", ""),
                    "foreground": info.get("foreground", ""),
                }
                for color_id, info in event_colors.items()
            }
        except HttpError as exc:
            self._handle_http_error(exc, "get_available_colors")
            raise  # для type checker

    def get_calendar_list(self) -> list[dict[str, Any]]:
        """
        Получить список доступных календарей пользователя.

        Returns:
            Список словарей с информацией о календарях.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.debug("Получение списка календарей")

        try:
            result = self._execute_api_call(service.calendarList().list())
            calendars = result.get("items", [])
            logger.info("Получено %d календарей", len(calendars))
            return [
                {
                    "id": cal.get("id"),
                    "summary": cal.get("summary"),
                    "primary": cal.get("primary", False),
                    "accessRole": cal.get("accessRole"),
                    "backgroundColor": cal.get("backgroundColor"),
                }
                for cal in calendars
            ]
        except HttpError as exc:
            self._handle_http_error(exc, "get_calendar_list")
            raise  # для type checker

    def search_events(
        self, query: str, days_ahead: int = 30, max_results: int = 50
    ) -> list[CalendarEvent]:
        """
        Поиск событий по текстовому запросу.

        Args:
            query: Поисковый запрос.
            days_ahead: На сколько дней вперёд искать.
            max_results: Максимальное количество результатов.

        Returns:
            Список найденных CalendarEvent.
        """
        now = datetime.now()
        date_to = now + timedelta(days=days_ahead)
        return self.get_events(
            date_from=now, date_to=date_to, query=query, max_results=max_results
        )

    # ------------------------------------------------------------------
    # Обработка ошибок
    # ------------------------------------------------------------------

    @staticmethod
    def _handle_http_error(exc: HttpError, context: str) -> None:
        """
        Обработать HTTP ошибку от Google Calendar API.

        Преобразует HttpError в специфичные исключения модуля.

        Args:
            exc: Исходное исключение HttpError.
            context: Контекст операции (для логирования).

        Raises:
            RateLimitError: При 429 Too Many Requests.
            AuthError: При 401/403 ошибках.
            CalendarError: При прочих ошибках.
        """
        status = exc.resp.status if hasattr(exc, "resp") else 0

        try:
            error_details = json.loads(exc.content) if exc.content else {}
        except Exception:
            error_details = {}

        reason = ""
        if error_details:
            errors = error_details.get("error", {}).get("errors", [])
            if errors:
                reason = errors[0].get("reason", "")

        logger.error(
            "Ошибка Calendar API в '%s' (HTTP %s, reason: %s): %s",
            context, status, reason, exc,
        )

        if status == 429:
            retry_after = exc.resp.get("retry-after") if hasattr(exc, "resp") else None
            raise RateLimitError(
                f"Превышен лимит запросов в '{context}'",
                retry_after=int(retry_after) if retry_after else None,
            ) from exc
        elif status == 401:
            raise AuthError(
                f"Ошибка авторизации в '{context}'", status_code=401
            ) from exc
        elif status == 403:
            raise AuthError(
                f"Доступ запрещён в '{context}' (reason: {reason})",
                status_code=403,
                details=error_details,
            ) from exc
        else:
            raise CalendarError(
                f"Ошибка Calendar API в '{context}' (HTTP {status})",
                status_code=status,
                details=error_details,
            ) from exc


# json нужен для обработки ошибок
import json
