"""
Иерархия кастомных исключений для модуля интеграции с Google Calendar.

Предоставляет структурированные исключения для различных сценариев ошибок:
- Ошибки аутентификации и авторизации
- Ошибки Calendar API (события, календари)
- Ошибки Tasks API (задачи, списки задач)
- Ошибки синхронизации
- Ошибки сети и превышения лимитов

Примеры использования:
    raise AuthError("Токен истёк, требуется повторная авторизация")
    raise EventNotFoundError("Событие с ID 'abc123' не найдено")
    raise RateLimitError("Превышен лимит запросов к API")
"""

from __future__ import annotations

from typing import Optional


class CalendarError(Exception):
    """
    Базовое исключение для всех ошибок интеграции с Google Calendar.

    Attributes:
        message: Описание ошибки.
        status_code: HTTP статус-код (если применимо).
        details: Дополнительные детали ошибки (тело ответа API и т.д.).
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[dict] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthError(CalendarError):
    """
    Ошибка аутентификации или авторизации.

    Возникает при:
    - Отсутствии credentials
    - Истечении токена без возможности refresh
    - Невалидном client_id / client_secret
    - Отказе пользователя в доступе (consent denied)
    """

    def __init__(
        self,
        message: str = "Ошибка аутентификации",
        status_code: Optional[int] = 401,
        details: Optional[dict] = None,
    ) -> None:
        super().__init__(message, status_code, details)


class TokenExpiredError(AuthError):
    """Access token истёк и требует обновления."""

    def __init__(self, message: str = "Access token истёк") -> None:
        super().__init__(message, status_code=401)


class TokenRefreshError(AuthError):
    """Не удалось обновить токен (refresh token невалиден или отозван)."""

    def __init__(
        self, message: str = "Не удалось обновить токен", details: Optional[dict] = None
    ) -> None:
        super().__init__(message, status_code=401, details=details)


class CredentialsNotFoundError(AuthError):
    """Credentials не найдены — требуется первичная аутентификация."""

    def __init__(self, message: str = "Credentials не найдены. Требуется аутентификация.") -> None:
        super().__init__(message, status_code=401)


class RateLimitError(CalendarError):
    """
    Превышен лимит запросов к API (429 Too Many Requests).

    Attributes:
        retry_after: Рекомендуемое время ожидания перед повторной попыткой (секунды).
    """

    def __init__(
        self,
        message: str = "Превышен лимит запросов к API",
        retry_after: Optional[int] = None,
        details: Optional[dict] = None,
    ) -> None:
        super().__init__(message, status_code=429, details=details)
        self.retry_after = retry_after


class QuotaExceededError(CalendarError):
    """Исчерпана дневная квота API (403 quotaExceeded)."""

    def __init__(self, message: str = "Исчерпана квота API") -> None:
        super().__init__(message, status_code=403)


class EventNotFoundError(CalendarError):
    """Событие не найдено в указанном календаре (404)."""

    def __init__(
        self,
        event_id: str = "",
        calendar_id: str = "primary",
        message: Optional[str] = None,
    ) -> None:
        msg = message or f"Событие '{event_id}' не найдено в календаре '{calendar_id}'"
        super().__init__(msg, status_code=404)
        self.event_id = event_id
        self.calendar_id = calendar_id


class TaskNotFoundError(CalendarError):
    """Задача не найдена в указанном списке (404)."""

    def __init__(
        self,
        task_id: str = "",
        tasklist_id: str = "@default",
        message: Optional[str] = None,
    ) -> None:
        msg = message or f"Задача '{task_id}' не найдена в списке '{tasklist_id}'"
        super().__init__(msg, status_code=404)
        self.task_id = task_id
        self.tasklist_id = tasklist_id


class CalendarNotFoundError(CalendarError):
    """Календарь не найден (404)."""

    def __init__(self, calendar_id: str = "", message: Optional[str] = None) -> None:
        msg = message or f"Календарь '{calendar_id}' не найден"
        super().__init__(msg, status_code=404)
        self.calendar_id = calendar_id


class SyncError(CalendarError):
    """Ошибка синхронизации данных с Google Calendar / Tasks."""

    def __init__(
        self,
        message: str = "Ошибка синхронизации",
        details: Optional[dict] = None,
    ) -> None:
        super().__init__(message, status_code=500, details=details)


class SyncTokenExpiredError(SyncError):
    """
    Sync token устарел (410 Gone) — требуется полная ресинхронизация.

    Возникает при инкрементальной синхронизации, когда sync token
    становится невалидным из-за длительного периода неактивности.
    """

    def __init__(self, message: str = "Sync token устарел. Требуется полная синхронизация.") -> None:
        super().__init__(message, details={"requires_full_sync": True})


class ConflictResolutionError(SyncError):
    """Не удалось разрешить конфликт между локальной и удалённой версиями."""

    def __init__(
        self,
        message: str = "Конфликт при синхронизации",
        local_version: Optional[dict] = None,
        remote_version: Optional[dict] = None,
    ) -> None:
        super().__init__(
            message,
            details={"local": local_version or {}, "remote": remote_version or {}},
        )


class NetworkError(CalendarError):
    """Сетевая ошибка при обращении к API."""

    def __init__(
        self,
        message: str = "Сетевая ошибка",
        status_code: Optional[int] = None,
        details: Optional[dict] = None,
    ) -> None:
        super().__init__(message, status_code=status_code or 503, details=details)


class MaxRetriesExceededError(NetworkError):
    """Исчерпаны все попытки retry — операция не выполнена."""

    def __init__(
        self,
        message: str = "Исчерпаны все попытки повторного выполнения",
        max_retries: int = 5,
        last_error: Optional[str] = None,
    ) -> None:
        full_message = f"{message} (попыток: {max_retries})"
        if last_error:
            full_message += f". Последняя ошибка: {last_error}"
        super().__init__(full_message, status_code=503)
        self.max_retries = max_retries
        self.last_error = last_error


class ValidationError(CalendarError):
    """Ошибка валидации входных данных."""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(message, status_code=400)
        self.field = field


class PermissionDeniedError(CalendarError):
    """Недостаточно прав для выполнения операции (403 forbidden)."""

    def __init__(
        self,
        message: str = "Недостаточно прав для выполнения операции",
        details: Optional[dict] = None,
    ) -> None:
        super().__init__(message, status_code=403, details=details)
