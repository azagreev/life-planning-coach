"""Unit tests for CalendarManager."""

from __future__ import annotations

import json
import unittest
from datetime import date, datetime, timedelta, timezone
from unittest.mock import MagicMock, Mock, patch

import pytest
from googleapiclient.errors import HttpError

from calendar_integration.calendar_manager import CalendarManager
from calendar_integration.config import COLOR_MAP, REMINDER_PRESETS, WEEKLY_REVIEW_RRULE
from calendar_integration.exceptions import EventNotFoundError, MaxRetriesExceededError, RateLimitError, ValidationError
from calendar_integration.models import CalendarEvent, TimeSlot


def make_http_error(status: int, content: dict | None = None) -> HttpError:
    """Factory for mock HttpError exceptions."""
    class FakeResp:
        def __init__(self, status_code: int) -> None:
            self.status = status_code
            self.reason = "Fake Reason"

        def get(self, key: str, default=None):
            return default

    body = json.dumps(content or {}).encode("utf-8")
    return HttpError(FakeResp(status), body)


def make_mock_service() -> MagicMock:
    """Build a chainable mock Google API service."""
    service = MagicMock()
    # events().list/insert/get/... all return a request with .execute()
    service.events.return_value = service.events
    service.freebusy.return_value = service.freebusy
    return service


class TestCalendarManager(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_auth = MagicMock()
        self.mock_service = make_mock_service()
        self.mock_auth.build_service.return_value = self.mock_service
        self.manager = CalendarManager(self.mock_auth)

    # ------------------------------------------------------------------
    # get_events
    # ------------------------------------------------------------------
    def test_get_events_passes_correct_params(self) -> None:
        dt_from = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
        dt_to = datetime(2025, 1, 2, 0, 0, tzinfo=timezone.utc)
        self.mock_service.events.list.return_value.execute.return_value = {
            "items": []
        }

        events = self.manager.get_events(
            date_from=dt_from,
            date_to=dt_to,
            calendar_id="primary",
            query="standup",
            max_results=50,
        )

        self.assertEqual(events, [])
        self.mock_service.events.list.assert_called_once_with(
            calendarId="primary",
            timeMin=dt_from.isoformat(),
            timeMax=dt_to.isoformat(),
            maxResults=50,
            singleEvents=True,
            orderBy="startTime",
            q="standup",
        )
        self.mock_auth.refresh_if_needed.assert_called()

    def test_get_events_returns_parsed_events(self) -> None:
        dt_from = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
        dt_to = datetime(2025, 1, 2, 0, 0, tzinfo=timezone.utc)
        self.mock_service.events.list.return_value.execute.return_value = {
            "items": [
                {
                    "id": "evt1",
                    "summary": "Meeting",
                    "start": {"dateTime": "2025-01-01T10:00:00+00:00"},
                    "end": {"dateTime": "2025-01-01T11:00:00+00:00"},
                }
            ]
        }

        events = self.manager.get_events(date_from=dt_from, date_to=dt_to)

        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], CalendarEvent)
        self.assertEqual(events[0].id, "evt1")
        self.assertEqual(events[0].title, "Meeting")

    def test_get_events_validation_error(self) -> None:
        dt = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
        with self.assertRaises(ValidationError):
            self.manager.get_events(date_from=dt, date_to=dt)

    # ------------------------------------------------------------------
    # create_event
    # ------------------------------------------------------------------
    def test_create_event_body_structure(self) -> None:
        start = datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc)
        end = datetime(2025, 1, 15, 11, 0, tzinfo=timezone.utc)
        self.mock_service.events.insert.return_value.execute.return_value = {
            "id": "new_evt",
            "summary": "Test Event",
            "start": {"dateTime": start.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": end.isoformat(), "timeZone": "UTC"},
            "colorId": "9",
        }

        event = self.manager.create_event(
            title="Test Event",
            start=start,
            end=end,
            description="A description",
            color_id="9",
            reminders=[{"method": "popup", "minutes": 10}],
            recurrence=["RRULE:FREQ=DAILY"],
            attendees=["a@example.com"],
        )

        self.assertIsInstance(event, CalendarEvent)
        call_kwargs = self.mock_service.events.insert.call_args.kwargs
        self.assertEqual(call_kwargs["calendarId"], "primary")
        self.assertEqual(call_kwargs["sendUpdates"], "all")

        body = call_kwargs["body"]
        self.assertEqual(body["summary"], "Test Event")
        self.assertEqual(body["start"]["dateTime"], start.isoformat())
        self.assertEqual(body["end"]["dateTime"], end.isoformat())
        self.assertEqual(body["colorId"], "9")
        self.assertEqual(body["description"], "A description")
        self.assertEqual(body["recurrence"], ["RRULE:FREQ=DAILY"])
        self.assertEqual(body["attendees"], [{"email": "a@example.com"}])
        self.assertEqual(
            body["reminders"]["overrides"],
            [{"method": "popup", "minutes": 10}],
        )
        self.assertFalse(body["reminders"]["useDefault"])

    def test_create_event_validation_errors(self) -> None:
        start = datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc)
        end = datetime(2025, 1, 15, 11, 0, tzinfo=timezone.utc)

        with self.assertRaises(ValidationError):
            self.manager.create_event(title="", start=start, end=end)

        with self.assertRaises(ValidationError):
            self.manager.create_event(title="X", start=end, end=start)

    # ------------------------------------------------------------------
    # get_free_slots
    # ------------------------------------------------------------------
    def test_get_free_slots_calculates_correctly(self) -> None:
        target = date(2025, 1, 15)
        self.mock_service.freebusy.query.return_value.execute.return_value = {
            "calendars": {
                "primary": {
                    "busy": [
                        {
                            "start": "2025-01-15T10:00:00+00:00",
                            "end": "2025-01-15T11:00:00+00:00",
                        },
                        {
                            "start": "2025-01-15T14:00:00+00:00",
                            "end": "2025-01-15T15:00:00+00:00",
                        },
                    ]
                }
            }
        }

        slots = self.manager.get_free_slots(
            target_date=target,
            duration_minutes=60,
            work_start=9,
            work_end=18,
        )

        self.assertTrue(all(slot.is_free for slot in slots))
        # Expected free intervals: 09:00-10:00, 11:00-14:00, 15:00-18:00
        self.assertEqual(len(slots), 3)
        self.assertEqual(slots[0].start.hour, 9)
        self.assertEqual(slots[0].end.hour, 10)
        self.assertEqual(slots[1].start.hour, 11)
        self.assertEqual(slots[1].end.hour, 14)
        self.assertEqual(slots[2].start.hour, 15)
        self.assertEqual(slots[2].end.hour, 18)

        # Verify freebusy body
        call_kwargs = self.mock_service.freebusy.query.call_args.kwargs
        body = call_kwargs["body"]
        self.assertEqual(body["timeZone"], "UTC")
        self.assertEqual(body["items"], [{"id": "primary"}])

    def test_get_free_slots_validation_error(self) -> None:
        with self.assertRaises(ValidationError):
            self.manager.get_free_slots(
                target_date=date(2025, 1, 15),
                duration_minutes=0,
            )

    # ------------------------------------------------------------------
    # create_weekly_review_reminder
    # ------------------------------------------------------------------
    def test_create_weekly_review_reminder_calls_create_event(self) -> None:
        with patch.object(self.manager, "create_event") as mock_create:
            mock_create.return_value = CalendarEvent(
                title="Weekly Review",
                start=datetime(2025, 1, 1, 19, 0),
                end=datetime(2025, 1, 1, 19, 30),
                id="evt123",
            )
            event = self.manager.create_weekly_review_reminder(
                timezone="Europe/Moscow", hour=20, minute=30
            )

        self.assertEqual(event.id, "evt123")
        mock_create.assert_called_once()
        call_kwargs = mock_create.call_args.kwargs
        self.assertEqual(call_kwargs["title"], "Weekly Review")
        self.assertEqual(call_kwargs["color_id"], COLOR_MAP["weekly_review"])
        self.assertEqual(call_kwargs["reminders"], REMINDER_PRESETS["weekly_review"])
        self.assertEqual(call_kwargs["recurrence"], WEEKLY_REVIEW_RRULE)
        self.assertIn("Weekly Review", call_kwargs["description"])
        self.assertEqual(call_kwargs["start"].hour, 20)
        self.assertEqual(call_kwargs["start"].minute, 30)
        self.assertEqual(call_kwargs["end"], call_kwargs["start"] + timedelta(minutes=30))

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------
    def test_404_raises_event_not_found(self) -> None:
        self.mock_service.events.get.return_value.execute.side_effect = (
            make_http_error(404)
        )

        with self.assertRaises(EventNotFoundError):
            self.manager.get_event(event_id="missing_evt")

    def test_get_event_404_not_found(self) -> None:
        self.mock_service.events.get.return_value.execute.side_effect = (
            make_http_error(404)
        )

        with self.assertRaises(EventNotFoundError) as ctx:
            self.manager.get_event(event_id="evt123", calendar_id="primary")

        self.assertEqual(ctx.exception.event_id, "evt123")
        self.assertEqual(ctx.exception.calendar_id, "primary")

    def test_429_raises_max_retries_exceeded(self) -> None:
        self.mock_service.events.insert.return_value.execute.side_effect = (
            make_http_error(429)
        )

        with self.assertRaises(MaxRetriesExceededError):
            self.manager.create_event(
                title="Test",
                start=datetime(2025, 1, 1, 10, 0, tzinfo=timezone.utc),
                end=datetime(2025, 1, 1, 11, 0, tzinfo=timezone.utc),
            )


if __name__ == "__main__":
    unittest.main()
