"""
Примеры использования модуля интеграции с Google Calendar.

Демонстрирует основные сценарии:
    1. Инициализация и аутентификация
    2. Создание Weekly Review reminder
    3. Создание WOOP reminder
    4. Чтение встреч на неделю
    5. Создание daily top-3 задач
    6. Поиск свободных слотов

Перед запуском:
    1. Создайте проект в Google Cloud Console
    2. Включите Google Calendar API и Google Tasks API
    3. Создайте OAuth 2.0 credentials (Desktop app)
    4. Скачайте client_secret.json
    5. Установите зависимости: pip install -r requirements.txt

Запуск:
    CALENDAR_ENCRYPTION_KEY="your-secret-key" python example_usage.py
"""

from __future__ import annotations

import logging
import os
from datetime import date, datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# Настройка логирования
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("example_usage")


# ---------------------------------------------------------------------------
# Пример 1: Инициализация
# ---------------------------------------------------------------------------
def example_initialization():
    """
    Инициализация аутентификации и менеджеров.

    Создаёт экземпляры CalendarAuth, CalendarManager и TasksManager.
    При первом запуске откроется браузер для OAuth авторизации.
    """
    from calendar_integration import CalendarAuth, CalendarManager, TasksManager

    # Путь к файлу с client secrets (скачан из Google Cloud Console)
    client_secrets = "credentials.json"

    # Ключ для шифрования токенов (можно через env: CALENDAR_ENCRYPTION_KEY)
    encryption_key = os.environ.get("CALENDAR_ENCRYPTION_KEY", "my-secret-key")

    logger.info("=" * 60)
    logger.info("Пример 1: Инициализация")
    logger.info("=" * 60)

    # Создаём объект аутентификации
    auth = CalendarAuth(
        client_secrets_file=client_secrets,
        encryption_key=encryption_key,
    )

    # Запускаем аутентификацию (OAuth flow)
    # При первом запуске откроется браузер
    credentials = auth.authenticate()
    logger.info("Аутентификация успешна! User: %s", credentials.client_id)

    # Создаём менеджеры
    calendar = CalendarManager(auth)
    tasks = TasksManager(auth)

    logger.info("Менеджеры созданы")
    return auth, calendar, tasks


# ---------------------------------------------------------------------------
# Пример 2: Создание Weekly Review reminder
# ---------------------------------------------------------------------------
def example_weekly_review(calendar: "CalendarManager") -> None:
    """
    Создать еженедельное напоминание о Weekly Review.

    Создаёт повторяющееся событие каждое воскресенье в 19:00
    для ретроспективы прошедшей недели.
    """
    logger.info("=" * 60)
    logger.info("Пример 2: Weekly Review Reminder")
    logger.info("=" * 60)

    try:
        event = calendar.create_weekly_review_reminder(
            timezone="Europe/Moscow",
            hour=19,
            minute=0,
        )
        logger.info("Weekly Review создан: %s", event.id)
        logger.info("  Название: %s", event.title)
        logger.info("  Начало: %s", event.start)
        logger.info("  Ссылка: %s", event.html_link)
    except Exception as exc:
        logger.error("Ошибка создания Weekly Review: %s", exc)


# ---------------------------------------------------------------------------
# Пример 3: Создание WOOP reminder
# ---------------------------------------------------------------------------
def example_woop_reminder(calendar: "CalendarManager") -> None:
    """
    Создать ежедневное напоминание о WOOP-сессии.

    WOOP (Wish, Outcome, Obstacle, Plan) — техника ментального контрастирования.
    Создаёт повторяющееся событие ежедневно в 7:00 утра.
    """
    logger.info("=" * 60)
    logger.info("Пример 3: WOOP Reminder")
    logger.info("=" * 60)

    try:
        event = calendar.create_woop_reminder(
            timezone="Europe/Moscow",
            hour=7,
            minute=0,
        )
        logger.info("WOOP reminder создан: %s", event.id)
        logger.info("  Название: %s", event.title)
        logger.info("  Начало: %s", event.start)
        logger.info("  Повторение: ежедневно")
    except Exception as exc:
        logger.error("Ошибка создания WOOP reminder: %s", exc)


# ---------------------------------------------------------------------------
# Пример 4: Чтение встреч на неделю
# ---------------------------------------------------------------------------
def example_read_week_events(calendar: "CalendarManager") -> None:
    """
    Получить список встреч на ближайшую неделю.

    Демонстрирует фильтрацию по датам и текстовый поиск.
    """
    logger.info("=" * 60)
    logger.info("Пример 4: Встречи на неделю")
    logger.info("=" * 60)

    now = datetime.now(timezone.utc)
    week_later = now + timedelta(days=7)

    try:
        # Получаем все события на неделю
        events = calendar.get_events(date_from=now, date_to=week_later)
        logger.info("Всего событий на неделю: %d", len(events))

        for event in events:
            duration = event.duration_minutes()
            logger.info(
                "  %s | %s — %s (%d мин) | %s",
                event.id[:12] if event.id else "N/A",
                event.start.strftime("%d.%m %H:%M") if event.start else "?",
                event.end.strftime("%H:%M") if event.end else "?",
                duration,
                event.title[:50],
            )

        # Поиск по тексту
        search_results = calendar.search_events(query="standup", days_ahead=7)
        logger.info("Результаты поиска 'standup': %d", len(search_results))

    except Exception as exc:
        logger.error("Ошибка чтения событий: %s", exc)


# ---------------------------------------------------------------------------
# Пример 5: Создание Daily Top-3 задач
# ---------------------------------------------------------------------------
def example_daily_top3(tasks: "TasksManager") -> None:
    """
    Создать 3 главных приоритета на день.

    Метод productivity: каждый день определять 3 главных задачи.
    Создаёт родительскую задачу с 3 подзадачами.
    """
    logger.info("=" * 60)
    logger.info("Пример 5: Daily Top-3")
    logger.info("=" * 60)

    today = date.today()

    priorities = [
        "Написать главу 3 книги (45 мин фокуса)",
        "Позвонить потенциальному клиенту",
        "30 минут йоги",
    ]

    try:
        top3 = tasks.create_daily_top3(
            priorities=priorities,
            due=today,
        )
        logger.info("Daily Top-3 создано: %d задач", len(top3))
        for task in top3:
            logger.info("  %s: %s", task.id[:12] if task.id else "N/A", task.title)
    except Exception as exc:
        logger.error("Ошибка создания Daily Top-3: %s", exc)


# ---------------------------------------------------------------------------
# Пример 6: Поиск свободных слотов
# ---------------------------------------------------------------------------
def example_find_free_slots(calendar: "CalendarManager") -> None:
    """
    Найти свободные временные слоты на сегодня.

    Ищет свободные окна длительностью 60 минут
    в рабочее время (9:00-18:00).
    """
    logger.info("=" * 60)
    logger.info("Пример 6: Свободные слоты")
    logger.info("=" * 60)

    today = date.today()

    try:
        free_slots = calendar.get_free_slots(
            target_date=today,
            duration_minutes=60,
            work_start=9,
            work_end=18,
        )

        logger.info(
            "Свободные слоты на %s (60+ мин):", today.strftime("%d.%m.%Y")
        )
        for slot in free_slots:
            logger.info(
                "  %s — %s (%d мин)",
                slot.start.strftime("%H:%M"),
                slot.end.strftime("%H:%M"),
                slot.duration_minutes(),
            )

    except Exception as exc:
        logger.error("Ошибка поиска свободных слотов: %s", exc)


# ---------------------------------------------------------------------------
# Пример 7: Создание time block (бонус)
# ---------------------------------------------------------------------------
def example_time_block(calendar: "CalendarManager") -> None:
    """
    Создать временной блок для глубокой работы.

    Time blocking — выделение конкретного времени для фокусной работы.
    """
    logger.info("=" * 60)
    logger.info("Пример 7: Time Block (Deep Work)")
    logger.info("=" * 60)

    tomorrow = date.today() + timedelta(days=1)
    start = datetime.combine(tomorrow, datetime.min.time().replace(hour=9))

    try:
        event = calendar.create_time_block(
            title="Deep Work — Разработка архитектуры",
            start=start,
            duration=120,  # 2 часа
            color="deep_work",
            description="Фокусное время без перерывов. Телефон в режиме 'Не беспокоить'.",
        )
        logger.info("Time block создан: %s", event.id)
        logger.info("  Название: %s", event.title)
        logger.info("  Длительность: %d мин", event.duration_minutes())
    except Exception as exc:
        logger.error("Ошибка создания time block: %s", exc)


# ---------------------------------------------------------------------------
# Главная функция
# ---------------------------------------------------------------------------
def main() -> None:
    """
    Запуск всех примеров.

    Выполняет последовательно все сценарии использования модуля.
    Для пропуска примеров закомментируйте соответствующие вызовы.
    """
    logger.info("Начало демонстрации модуля Google Calendar интеграции")
    logger.info("")

    # Шаг 1: Инициализация
    auth, calendar, tasks = example_initialization()

    # Шаг 2-7: Примеры использования
    example_weekly_review(calendar)
    example_woop_reminder(calendar)
    example_read_week_events(calendar)
    example_daily_top3(tasks)
    example_find_free_slots(calendar)
    example_time_block(calendar)

    logger.info("")
    logger.info("=" * 60)
    logger.info("Все примеры выполнены!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
