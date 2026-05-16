"""
Менеджер задач Google Tasks.

Предоставляет CRUD-операции для задач, управление списками задач
и life-planning пресеты:
    - Daily Top-3 priorities
    - Weekly goal tasks
    - 12-week goal tasks

Все методы включают retry-логику и автоматическое обновление токена.

Example:
    >>> from calendar_integration.auth import CalendarAuth
    >>> from calendar_integration.tasks_manager import TasksManager
    >>> auth = CalendarAuth("credentials.json", "secret")
    >>> tasks_mgr = TasksManager(auth)
    >>> tasks = tasks_mgr.get_tasks()
    >>> new_task = tasks_mgr.create_task("Закончить отчёт", due=date(2025, 1, 20))
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta
from typing import Any, Optional

from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from .auth import CalendarAuth, with_retry
from .config import DEFAULT_TASKLIST_ID
from .exceptions import (
    AuthError,
    CalendarError,
    RateLimitError,
    TaskNotFoundError,
    ValidationError,
)
from .models import CalendarTask

logger = logging.getLogger(__name__)


class TasksManager:
    """
    Менеджер для работы с задачами Google Tasks.

    Управляет созданием, чтением, обновлением и удалением задач,
    управлением списками задач и life-planning пресетами.

    Attributes:
        _auth: Экземпляр CalendarAuth для аутентификации.
        _service: Lazy-initialized сервис Tasks API.

    Example:
        >>> tasks_mgr = TasksManager(auth)
        >>> # Получить активные задачи
        >>> tasks = tasks_mgr.get_tasks(show_completed=False)
        >>> # Создать daily top-3
        >>> top3 = tasks_mgr.create_daily_top3(
        ...     priorities=["Написать статью", "Подготовить презентацию", "Ответить на письма"],
        ...     due=date(2025, 1, 15),
        ... )
    """

    def __init__(self, auth: CalendarAuth) -> None:
        """
        Инициализировать TasksManager.

        Args:
            auth: Экземпляр CalendarAuth с настроенной аутентификацией.
        """
        self._auth = auth
        self._service: Optional[Resource] = None
        logger.debug("TasksManager инициализирован")

    # ------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------

    def _get_service(self) -> Resource:
        """
        Получить или создать сервис Tasks API.

        Returns:
            Экземпляр googleapiclient.discovery.Resource для Tasks API v1.
        """
        if self._service is None:
            self._service = self._auth.build_service("tasks", "v1")
        return self._service

    def _parse_task_response(self, data: dict[str, Any]) -> CalendarTask:
        """Преобразовать ответ API в CalendarTask."""
        return CalendarTask.from_api_response(data)

    @with_retry()
    def _execute_api_call(self, request: Any) -> Any:
        """Выполнить API-запрос с retry-логикой."""
        return request.execute()

    # ------------------------------------------------------------------
    # CRUD задач
    # ------------------------------------------------------------------

    def get_tasks(
        self,
        tasklist_id: str = DEFAULT_TASKLIST_ID,
        show_completed: bool = False,
        due_min: Optional[date] = None,
        due_max: Optional[date] = None,
        max_results: int = 100,
    ) -> list[CalendarTask]:
        """
        Получить список задач.

        Args:
            tasklist_id: ID списка задач. По умолчанию '@default'.
            show_completed: Включить выполненные задачи.
            due_min: Минимальный срок (фильтр).
            due_max: Максимальный срок (фильтр).
            max_results: Максимальное количество результатов.

        Returns:
            Список CalendarTask.

        Raises:
            AuthError: При ошибках аутентификации.

        Example:
            >>> from datetime import date, timedelta
            >>> tasks = tasks_mgr.get_tasks(
            ...     show_completed=False,
            ...     due_min=date.today(),
            ...     due_max=date.today() + timedelta(days=7),
            ... )
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        params: dict[str, Any] = {
            "tasklist": tasklist_id,
            "maxResults": max_results,
            "showCompleted": show_completed,
            "showDeleted": False,
            "showHidden": False,
        }

        if due_min:
            params["dueMin"] = self._format_due_date(due_min)
        if due_max:
            params["dueMax"] = self._format_due_date(due_max)

        logger.info(
            "Получение задач (list: %s, completed: %s)",
            tasklist_id, show_completed,
        )

        try:
            result = self._execute_api_call(service.tasks().list(**params))
            items = result.get("items", [])
            tasks = [self._parse_task_response(item) for item in items]
            logger.info("Получено %d задач", len(tasks))
            return tasks

        except HttpError as exc:
            self._handle_http_error(exc, f"get_tasks({tasklist_id})")
            raise  # для type checker

    def get_task(
        self, task_id: str, tasklist_id: str = DEFAULT_TASKLIST_ID
    ) -> CalendarTask:
        """
        Получить одну задачу по ID.

        Args:
            task_id: Идентификатор задачи.
            tasklist_id: ID списка задач.

        Returns:
            CalendarTask.

        Raises:
            TaskNotFoundError: Если задача не найдена.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.debug("Получение задачи %s из списка %s", task_id, tasklist_id)

        try:
            result = self._execute_api_call(
                service.tasks().get(tasklist=tasklist_id, task=task_id)
            )
            return self._parse_task_response(result)

        except HttpError as exc:
            if hasattr(exc, "resp") and exc.resp.status == 404:
                raise TaskNotFoundError(task_id, tasklist_id) from exc
            self._handle_http_error(exc, f"get_task({task_id})")
            raise  # для type checker

    def create_task(
        self,
        title: str,
        notes: str = "",
        due: Optional[date] = None,
        parent: Optional[str] = None,
        tasklist_id: str = DEFAULT_TASKLIST_ID,
    ) -> CalendarTask:
        """
        Создать задачу.

        Важно: Google Tasks API хранит ТОЛЬКО дату (без времени).

        Args:
            title: Название задачи (обязательное, макс. 8192 символа).
            notes: Описание / заметки.
            due: Срок выполнения (только дата).
            parent: ID родительской задачи (для подзадачи).
            tasklist_id: ID списка задач.

        Returns:
            Созданная CalendarTask с заполненным id.

        Raises:
            ValidationError: Если title пустой.
            AuthError: При ошибках аутентификации.

        Example:
            >>> from datetime import date
            >>> task = tasks_mgr.create_task(
            ...     title="Подготовить презентацию",
            ...     notes="Слайды + репетиция",
            ...     due=date(2025, 1, 20),
            ... )
        """
        if not title:
            raise ValidationError("Название задачи обязательно", field="title")

        self._auth.refresh_if_needed()
        service = self._get_service()

        task = CalendarTask(title=title, notes=notes, due=due, parent=parent)

        logger.info("Создание задачи '%s'", title)

        try:
            result = self._execute_api_call(
                service.tasks().insert(
                    tasklist=tasklist_id,
                    body=task.to_api_body(),
                    parent=parent,
                )
            )
            created = self._parse_task_response(result)
            logger.info("Задача создана: id=%s", created.id)
            return created

        except HttpError as exc:
            self._handle_http_error(exc, f"create_task({title})")
            raise  # для type checker

    def update_task(
        self,
        task_id: str,
        tasklist_id: str = DEFAULT_TASKLIST_ID,
        **kwargs: Any,
    ) -> CalendarTask:
        """
        Обновить существующую задачу.

        Args:
            task_id: Идентификатор задачи.
            tasklist_id: ID списка задач.
            **kwargs: Поля для обновления (title, notes, due, status).

        Returns:
            Обновлённая CalendarTask.

        Raises:
            TaskNotFoundError: Если задача не найдена.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.info("Обновление задачи %s: %s", task_id, kwargs)

        try:
            body: dict[str, Any] = {}
            for key, value in kwargs.items():
                if key == "due" and isinstance(value, date):
                    body["due"] = self._format_due_date(value)
                elif key == "title":
                    body["title"] = value
                elif key == "notes":
                    body["notes"] = value
                elif key == "status":
                    body["status"] = value
                else:
                    body[key] = value

            result = self._execute_api_call(
                service.tasks().patch(
                    tasklist=tasklist_id, task=task_id, body=body
                )
            )
            updated = self._parse_task_response(result)
            logger.info("Задача %s обновлена", task_id)
            return updated

        except HttpError as exc:
            if hasattr(exc, "resp") and exc.resp.status == 404:
                raise TaskNotFoundError(task_id, tasklist_id) from exc
            self._handle_http_error(exc, f"update_task({task_id})")
            raise  # для type checker

    def complete_task(
        self, task_id: str, tasklist_id: str = DEFAULT_TASKLIST_ID
    ) -> CalendarTask:
        """
        Отметить задачу как выполненную.

        Args:
            task_id: Идентификатор задачи.
            tasklist_id: ID списка задач.

        Returns:
            Обновлённая CalendarTask со статусом 'completed'.

        Raises:
            TaskNotFoundError: Если задача не найдена.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        completed_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

        logger.info("Отметка задачи %s как выполненной", task_id)

        try:
            result = self._execute_api_call(
                service.tasks().patch(
                    tasklist=tasklist_id,
                    task=task_id,
                    body={"status": "completed", "completed": completed_time},
                )
            )
            updated = self._parse_task_response(result)
            logger.info("Задача %s выполнена", task_id)
            return updated

        except HttpError as exc:
            if hasattr(exc, "resp") and exc.resp.status == 404:
                raise TaskNotFoundError(task_id, tasklist_id) from exc
            self._handle_http_error(exc, f"complete_task({task_id})")
            raise  # для type checker

    def uncomplete_task(
        self, task_id: str, tasklist_id: str = DEFAULT_TASKLIST_ID
    ) -> CalendarTask:
        """
        Вернуть задачу в статус 'нужно выполнить'.

        Args:
            task_id: Идентификатор задачи.
            tasklist_id: ID списка задач.

        Returns:
            Обновлённая CalendarTask со статусом 'needsAction'.
        """
        logger.info("Возврат задачи %s в активный статус", task_id)
        return self.update_task(
            task_id, tasklist_id=tasklist_id, status="needsAction", completed=None
        )

    def delete_task(
        self, task_id: str, tasklist_id: str = DEFAULT_TASKLIST_ID
    ) -> None:
        """
        Удалить задачу.

        Args:
            task_id: Идентификатор задачи.
            tasklist_id: ID списка задач.

        Raises:
            TaskNotFoundError: Если задача не найдена.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.info("Удаление задачи %s из списка %s", task_id, tasklist_id)

        try:
            self._execute_api_call(
                service.tasks().delete(tasklist=tasklist_id, task=task_id)
            )
            logger.info("Задача %s удалена", task_id)

        except HttpError as exc:
            if hasattr(exc, "resp") and exc.resp.status == 404:
                raise TaskNotFoundError(task_id, tasklist_id) from exc
            self._handle_http_error(exc, f"delete_task({task_id})")

    # ------------------------------------------------------------------
    # Управление списками задач
    # ------------------------------------------------------------------

    def get_task_lists(self) -> list[dict[str, Any]]:
        """
        Получить список всех списков задач пользователя.

        Returns:
            Список словарей с id и title каждого списка.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.debug("Получение списков задач")

        try:
            result = self._execute_api_call(service.tasklists().list())
            items = result.get("items", [])
            logger.info("Получено %d списков задач", len(items))
            return [{"id": item["id"], "title": item["title"]} for item in items]

        except HttpError as exc:
            self._handle_http_error(exc, "get_task_lists")
            raise  # для type checker

    def create_tasklist(self, title: str) -> str:
        """
        Создать новый список задач.

        Args:
            title: Название списка (макс. 1024 символа).

        Returns:
            ID созданного списка.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.info("Создание списка задач '%s'", title)

        try:
            result = self._execute_api_call(
                service.tasklists().insert(body={"title": title})
            )
            tasklist_id = result["id"]
            logger.info("Список задач создан: id=%s", tasklist_id)
            return tasklist_id

        except HttpError as exc:
            self._handle_http_error(exc, f"create_tasklist({title})")
            raise  # для type checker

    def get_or_create_tasklist(self, title: str) -> str:
        """
        Получить существующий список задач или создать новый.

        Args:
            title: Название списка.

        Returns:
            ID списка задач.
        """
        existing = self.get_task_lists()
        for tasklist in existing:
            if tasklist["title"] == title:
                logger.debug("Найден существующий список '%s': %s", title, tasklist["id"])
                return tasklist["id"]

        logger.info("Список '%s' не найден, создаём новый", title)
        return self.create_tasklist(title)

    def delete_tasklist(self, tasklist_id: str) -> None:
        """
        Удалить список задач.

        Args:
            tasklist_id: ID списка задач.
        """
        self._auth.refresh_if_needed()
        service = self._get_service()

        logger.info("Удаление списка задач %s", tasklist_id)

        try:
            self._execute_api_call(service.tasklists().delete(tasklist=tasklist_id))
            logger.info("Список задач %s удалён", tasklist_id)

        except HttpError as exc:
            self._handle_http_error(exc, f"delete_tasklist({tasklist_id})")

    # ------------------------------------------------------------------
    # Batch операции
    # ------------------------------------------------------------------

    def create_tasks_batch(
        self,
        tasks: list[CalendarTask],
        tasklist_id: str = DEFAULT_TASKLIST_ID,
    ) -> list[CalendarTask]:
        """
        Создать несколько задач пакетно.

        Args:
            tasks: Список CalendarTask для создания.
            tasklist_id: ID списка задач.

        Returns:
            Список созданных CalendarTask с заполненными id.
        """
        created: list[CalendarTask] = []
        for task in tasks:
            try:
                new_task = self.create_task(
                    title=task.title,
                    notes=task.notes,
                    due=task.due,
                    parent=task.parent,
                    tasklist_id=tasklist_id,
                )
                created.append(new_task)
            except Exception as exc:
                logger.error("Ошибка при создании задачи '%s': %s", task.title, exc)
                raise

        logger.info("Пакетно создано %d задач", len(created))
        return created

    def create_task_with_subtasks(
        self,
        parent_title: str,
        subtasks: list[str],
        notes: str = "",
        due: Optional[date] = None,
        tasklist_id: str = DEFAULT_TASKLIST_ID,
    ) -> tuple[str, list[str]]:
        """
        Создать задачу с подзадачами.

        Args:
            parent_title: Название родительской задачи.
            subtasks: Список названий подзадач.
            notes: Описание родительской задачи.
            due: Срок выполнения.
            tasklist_id: ID списка задач.

        Returns:
            Кортеж (parent_id, [subtask_id, ...]).

        Example:
            >>> parent_id, sub_ids = tasks_mgr.create_task_with_subtasks(
            ...     parent_title="Подготовить конференцию",
            ...     subtasks=["Написать доклад", "Создать слайды", "Репетиция"],
            ...     due=date(2025, 3, 15),
            ... )
        """
        # Создаём родительскую задачу
        parent = self.create_task(
            title=parent_title, notes=notes, due=due, tasklist_id=tasklist_id
        )
        parent_id = parent.id or ""

        # Создаём подзадачи
        created_ids: list[str] = []
        for sub_title in subtasks:
            sub = self.create_task(
                title=sub_title, parent=parent_id, tasklist_id=tasklist_id
            )
            created_ids.append(sub.id or "")

        logger.info(
            "Создана задача '%s' с %d подзадачами",
            parent_title, len(created_ids),
        )
        return parent_id, created_ids

    def clear_completed(self, tasklist_id: str = DEFAULT_TASKLIST_ID) -> int:
        """
        Удалить все выполненные задачи из списка.

        Google Tasks API предоставляет метод tasks.clear для этого,
        но он работает только для полной очистки выполненных задач.

        Args:
            tasklist_id: ID списка задач.

        Returns:
            Количество удалённых задач.
        """
        # Получаем выполненные задачи
        completed_tasks = self.get_tasks(
            tasklist_id=tasklist_id, show_completed=True
        )
        completed = [t for t in completed_tasks if t.is_completed()]

        # Удаляем каждую
        deleted_count = 0
        for task in completed:
            try:
                if task.id:
                    self.delete_task(task.id, tasklist_id)
                    deleted_count += 1
            except Exception as exc:
                logger.warning("Не удалось удалить задачу %s: %s", task.id, exc)

        logger.info("Удалено %d выполненных задач", deleted_count)
        return deleted_count

    # ------------------------------------------------------------------
    # Life Planning пресеты
    # ------------------------------------------------------------------

    def create_daily_top3(
        self,
        priorities: list[str],
        due: date,
        tasklist_id: str = DEFAULT_TASKLIST_ID,
    ) -> list[CalendarTask]:
        """
        Создать 3 приоритетных задачи на день (Daily Top-3).

        Метод productivity: каждый день определять 3 главных задачи,
        которые обязательно нужно выполнить.

        Args:
            priorities: Список из 1-3 приоритетных задач.
            due: Дата выполнения.
            tasklist_id: ID списка задач.

        Returns:
            Список созданных CalendarTask.

        Raises:
            ValidationError: Если priorities пустой или > 10 элементов.

        Example:
            >>> from datetime import date
            >>> top3 = tasks_mgr.create_daily_top3(
            ...     priorities=[
            ...         "Написать главу книги",
            ...         "Позвонить клиенту",
            ...         "30 минут спорт",
            ...     ],
            ...     due=date(2025, 1, 15),
            ... )
        """
        if not priorities:
            raise ValidationError(
                "Список приоритетов не может быть пустым", field="priorities"
            )
        if len(priorities) > 10:
            raise ValidationError(
                "Максимум 10 приоритетов за раз", field="priorities"
            )

        logger.info(
            "Создание Daily Top-3 на %s: %s",
            due, priorities,
        )

        # Создаём родительскую задачу "Top-3 [дата]"
        date_str = due.strftime("%d.%m.%Y")
        parent_task = self.create_task(
            title=f"Top-3 {date_str}",
            notes="Три главных приоритета на сегодня",
            due=due,
            tasklist_id=tasklist_id,
        )
        parent_id = parent_task.id

        # Создаём подзадачи-приоритеты
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        created: list[CalendarTask] = [parent_task]

        for i, priority in enumerate(priorities):
            emoji = emojis[i] if i < len(emojis) else "•"
            task = self.create_task(
                title=f"{emoji} {priority}",
                parent=parent_id,
                due=due,
                tasklist_id=tasklist_id,
            )
            created.append(task)

        logger.info("Создано %d задач Daily Top-3", len(created))
        return created

    def create_weekly_goal_tasks(
        self,
        goals: list[dict[str, Any]],
        tasklist_id: str = DEFAULT_TASKLIST_ID,
    ) -> list[CalendarTask]:
        """
        Создать задачи для недельных целей.

        Args:
            goals: Список словарей с ключами 'title', 'notes', 'due'.
            tasklist_id: ID списка задач.

        Returns:
            Список созданных CalendarTask.

        Example:
            >>> from datetime import date, timedelta
            >>> goals = [
            ...     {"title": "Завершить модуль auth", "due": date(2025, 1, 20)},
            ...     {"title": "Написать тесты", "due": date(2025, 1, 22)},
            ... ]
            >>> tasks = tasks_mgr.create_weekly_goal_tasks(goals)
        """
        created: list[CalendarTask] = []
        for goal in goals:
            task = self.create_task(
                title=goal["title"],
                notes=goal.get("notes", ""),
                due=goal.get("due"),
                tasklist_id=tasklist_id,
            )
            created.append(task)

        logger.info("Создано %d задач для недельных целей", len(created))
        return created

    def create_12week_goal_task(
        self,
        goal_title: str,
        target_date: date,
        subtasks: list[str],
        tasklist_id: str = DEFAULT_TASKLIST_ID,
    ) -> tuple[CalendarTask, list[CalendarTask]]:
        """
        Создать задачу 12-недельной цели с подзадачами.

        Методика 12 Week Year: большая цель разбивается
        на конкретные задачи со сроками.

        Args:
            goal_title: Название цели.
            target_date: Целевая дата достижения.
            subtasks: Список подзадач для достижения цели.
            tasklist_id: ID списка задач.

        Returns:
            Кортеж (parent_task, [subtask, ...]).
        """
        logger.info(
            "Создание 12-недельной цели '%s' (deadline: %s)",
            goal_title, target_date,
        )

        parent = self.create_task(
            title=f"12W: {goal_title}",
            notes=f"Цель на 12 недель. Дедлайн: {target_date}",
            due=target_date,
            tasklist_id=tasklist_id,
        )

        created_subs: list[CalendarTask] = []
        for sub_title in subtasks:
            sub = self.create_task(
                title=sub_title,
                parent=parent.id,
                due=target_date,
                tasklist_id=tasklist_id,
            )
            created_subs.append(sub)

        logger.info(
            "Создана цель '%s' с %d подзадачами",
            goal_title, len(created_subs),
        )
        return parent, created_subs

    # ------------------------------------------------------------------
    # Вспомогательные методы
    # ------------------------------------------------------------------

    @staticmethod
    def _format_due_date(due: date) -> str:
        """
        Форматировать дату для Google Tasks API.

        API принимает только дату (время игнорируется).

        Args:
            due: Дата срока выполнения.

        Returns:
            Строка в формате RFC 3339.
        """
        return due.strftime("%Y-%m-%dT00:00:00.000Z")

    @staticmethod
    def _handle_http_error(exc: HttpError, context: str) -> None:
        """
        Обработать HTTP ошибку от Google Tasks API.

        Args:
            exc: Исходное исключение HttpError.
            context: Контекст операции.

        Raises:
            RateLimitError: При 429.
            AuthError: При 401/403.
            CalendarError: При прочих ошибках.
        """
        status = exc.resp.status if hasattr(exc, "resp") else 0

        try:
            error_details = json.loads(exc.content) if exc.content else {}
        except Exception:
            error_details = {}

        logger.error(
            "Ошибка Tasks API в '%s' (HTTP %s): %s",
            context, status, exc,
        )

        if status == 429:
            raise RateLimitError(
                f"Превышен лимит запросов в '{context}'"
            ) from exc
        elif status == 401:
            raise AuthError(
                f"Ошибка авторизации в '{context}'", status_code=401
            ) from exc
        elif status == 403:
            raise AuthError(
                f"Доступ запрещён в '{context}'", status_code=403
            ) from exc
        else:
            raise CalendarError(
                f"Ошибка Tasks API в '{context}' (HTTP {status})",
                status_code=status,
                details=error_details,
            ) from exc
