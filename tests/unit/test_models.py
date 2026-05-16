"""Unit tests for calendar_integration/models.py dataclasses."""

from __future__ import annotations

import sys
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# Load models.py directly to avoid triggering calendar_integration/__init__.py
# which imports auth modules with heavy external dependencies.
import importlib.util

_project_root = Path(__file__).resolve().parents[2]
_models_path = _project_root / "calendar_integration" / "models.py"
_spec = importlib.util.spec_from_file_location("calendar_integration.models_standalone", _models_path)
_models = importlib.util.module_from_spec(_spec)
sys.modules["calendar_integration.models_standalone"] = _models
_spec.loader.exec_module(_models)

CalendarEvent = _models.CalendarEvent
CalendarTask = _models.CalendarTask
FreeBusyWindow = _models.FreeBusyWindow
Reminder = _models.Reminder
TimeSlot = _models.TimeSlot


class TestReminder(unittest.TestCase):
    """Tests for Reminder dataclass."""

    def test_default_values(self) -> None:
        r = Reminder()
        self.assertEqual(r.method, "popup")
        self.assertEqual(r.minutes, 15)

    def test_valid_email_method(self) -> None:
        r = Reminder(method="email", minutes=30)
        self.assertEqual(r.method, "email")
        self.assertEqual(r.minutes, 30)

    def test_invalid_method_raises(self) -> None:
        with self.assertRaises(ValueError):
            Reminder(method="sms", minutes=10)

    def test_minutes_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            Reminder(method="popup", minutes=-1)

    def test_minutes_too_large_raises(self) -> None:
        with self.assertRaises(ValueError):
            Reminder(method="popup", minutes=40321)

    def test_minutes_boundary_zero(self) -> None:
        r = Reminder(minutes=0)
        self.assertEqual(r.minutes, 0)

    def test_minutes_boundary_max(self) -> None:
        r = Reminder(minutes=40320)
        self.assertEqual(r.minutes, 40320)

    def test_to_api_dict(self) -> None:
        r = Reminder(method="email", minutes=45)
        self.assertEqual(r.to_api_dict(), {"method": "email", "minutes": 45})

    def test_from_api_dict(self) -> None:
        data = {"method": "email", "minutes": 20}
        r = Reminder.from_api_dict(data)
        self.assertEqual(r.method, "email")
        self.assertEqual(r.minutes, 20)

    def test_from_api_dict_defaults(self) -> None:
        r = Reminder.from_api_dict({})
        self.assertEqual(r.method, "popup")
        self.assertEqual(r.minutes, 15)


class TestCalendarEvent(unittest.TestCase):
    """Tests for CalendarEvent dataclass."""

    def _make_dt(self, hour: int = 9) -> datetime:
        return datetime(2025, 1, 15, hour, 0, tzinfo=timezone.utc)

    def test_empty_title_raises(self) -> None:
        with self.assertRaises(ValueError):
            CalendarEvent(title="", start=self._make_dt(9), end=self._make_dt(11))

    def test_start_equals_end_raises(self) -> None:
        with self.assertRaises(ValueError):
            CalendarEvent(title="Test", start=self._make_dt(10), end=self._make_dt(10))

    def test_start_after_end_raises(self) -> None:
        with self.assertRaises(ValueError):
            CalendarEvent(title="Test", start=self._make_dt(11), end=self._make_dt(9))

    def test_no_start_end_ok(self) -> None:
        event = CalendarEvent(title="Draft")
        self.assertIsNone(event.start)
        self.assertIsNone(event.end)

    def test_duration_minutes(self) -> None:
        event = CalendarEvent(
            title="Work",
            start=self._make_dt(9),
            end=self._make_dt(11),
        )
        self.assertEqual(event.duration_minutes(), 120)

    def test_duration_minutes_none_times(self) -> None:
        event = CalendarEvent(title="Draft")
        self.assertEqual(event.duration_minutes(), 0)

    def test_to_api_body_basic(self) -> None:
        event = CalendarEvent(
            title="Deep Work",
            start=self._make_dt(9),
            end=self._make_dt(11),
            color_id="2",
        )
        body = event.to_api_body()
        self.assertEqual(body["summary"], "Deep Work")
        self.assertEqual(body["colorId"], "2")
        self.assertEqual(body["start"]["timeZone"], "UTC")
        self.assertEqual(body["end"]["timeZone"], "UTC")
        self.assertIn("dateTime", body["start"])
        self.assertIn("dateTime", body["end"])

    def test_to_api_body_missing_times_raises(self) -> None:
        event = CalendarEvent(title="Draft")
        with self.assertRaises(ValueError):
            event.to_api_body()

    def test_to_api_body_optional_fields(self) -> None:
        event = CalendarEvent(
            title="Meeting",
            start=self._make_dt(9),
            end=self._make_dt(10),
            description="Desc",
            location="Room A",
            recurrence=["RRULE:FREQ=DAILY"],
            attendees=["a@example.com"],
        )
        body = event.to_api_body()
        self.assertEqual(body["description"], "Desc")
        self.assertEqual(body["location"], "Room A")
        self.assertEqual(body["recurrence"], ["RRULE:FREQ=DAILY"])
        self.assertEqual(body["attendees"], [{"email": "a@example.com"}])

    def test_to_api_body_reminders(self) -> None:
        event = CalendarEvent(
            title="Reminder Test",
            start=self._make_dt(9),
            end=self._make_dt(10),
            reminders=[Reminder(method="email", minutes=30)],
        )
        body = event.to_api_body()
        self.assertFalse(body["reminders"]["useDefault"])
        self.assertEqual(
            body["reminders"]["overrides"],
            [{"method": "email", "minutes": 30}],
        )

    def test_from_api_response_datetime_format(self) -> None:
        data = {
            "summary": "Event",
            "id": "evt1",
            "start": {"dateTime": "2025-01-15T09:00:00+00:00"},
            "end": {"dateTime": "2025-01-15T10:00:00+00:00"},
            "description": "Desc",
            "location": "Office",
            "colorId": "3",
            "status": "confirmed",
            "htmlLink": "http://example.com",
            "recurringEventId": "parent1",
            "attendees": [{"email": "user@example.com"}],
            "reminders": {"overrides": [{"method": "popup", "minutes": 10}]},
            "recurrence": ["RRULE:FREQ=WEEKLY"],
        }
        event = CalendarEvent.from_api_response(data)
        self.assertEqual(event.title, "Event")
        self.assertEqual(event.id, "evt1")
        self.assertEqual(event.start, datetime(2025, 1, 15, 9, 0, tzinfo=timezone.utc))
        self.assertEqual(event.end, datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc))
        self.assertEqual(event.description, "Desc")
        self.assertEqual(event.location, "Office")
        self.assertEqual(event.color_id, "3")
        self.assertEqual(event.status, "confirmed")
        self.assertEqual(event.html_link, "http://example.com")
        self.assertEqual(event.recurring_event_id, "parent1")
        self.assertEqual(event.attendees, ["user@example.com"])
        self.assertEqual(len(event.reminders), 1)
        self.assertEqual(event.reminders[0].method, "popup")
        self.assertEqual(event.reminders[0].minutes, 10)
        self.assertEqual(event.recurrence, ["RRULE:FREQ=WEEKLY"])

    def test_from_api_response_date_format(self) -> None:
        data = {
            "summary": "All Day",
            "start": {"date": "2025-01-15"},
            "end": {"date": "2025-01-16"},
        }
        event = CalendarEvent.from_api_response(data)
        self.assertEqual(event.start, datetime(2025, 1, 15, 0, 0, 0))
        self.assertEqual(event.end, datetime(2025, 1, 16, 0, 0, 0))

    def test_from_api_response_z_suffix(self) -> None:
        data = {
            "summary": "Z Event",
            "start": {"dateTime": "2025-01-15T09:00:00Z"},
            "end": {"dateTime": "2025-01-15T10:00:00Z"},
        }
        event = CalendarEvent.from_api_response(data)
        self.assertEqual(event.start, datetime(2025, 1, 15, 9, 0, tzinfo=timezone.utc))
        self.assertEqual(event.end, datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc))

    def test_from_api_response_defaults(self) -> None:
        data = {"summary": "Minimal"}
        event = CalendarEvent.from_api_response(data)
        self.assertEqual(event.title, "Minimal")
        self.assertIsNone(event.start)
        self.assertIsNone(event.end)
        self.assertEqual(event.color_id, "1")
        self.assertEqual(event.status, "confirmed")
        self.assertEqual(event.reminders, [Reminder()])

    def test_from_api_response_empty_reminders(self) -> None:
        data = {
            "summary": "Default Reminder",
            "start": {"dateTime": "2025-01-15T09:00:00+00:00"},
            "end": {"dateTime": "2025-01-15T10:00:00+00:00"},
            "reminders": {"overrides": []},
        }
        event = CalendarEvent.from_api_response(data)
        self.assertEqual(event.reminders, [Reminder()])


class TestCalendarTask(unittest.TestCase):
    """Tests for CalendarTask dataclass."""

    def test_empty_title_raises(self) -> None:
        with self.assertRaises(ValueError):
            CalendarTask(title="")

    def test_is_completed_true(self) -> None:
        task = CalendarTask(title="Done", status="completed")
        self.assertTrue(task.is_completed())

    def test_is_completed_false(self) -> None:
        task = CalendarTask(title="Todo", status="needsAction")
        self.assertFalse(task.is_completed())

    def test_is_overdue_true(self) -> None:
        past_due = date.today() - timedelta(days=1)
        task = CalendarTask(title="Late", due=past_due)
        self.assertTrue(task.is_overdue())

    def test_is_overdue_false_no_due(self) -> None:
        task = CalendarTask(title="No Due")
        self.assertFalse(task.is_overdue())

    def test_is_overdue_false_completed(self) -> None:
        past_due = date.today() - timedelta(days=1)
        task = CalendarTask(title="Late Done", due=past_due, status="completed")
        self.assertFalse(task.is_overdue())

    def test_is_overdue_false_future(self) -> None:
        future_due = date.today() + timedelta(days=1)
        task = CalendarTask(title="Future", due=future_due)
        self.assertFalse(task.is_overdue())

    def test_to_api_body_basic(self) -> None:
        task = CalendarTask(title="Basic")
        self.assertEqual(task.to_api_body(), {"title": "Basic", "status": "needsAction"})

    def test_to_api_body_all_fields(self) -> None:
        dt = datetime(2025, 1, 15, 12, 0, tzinfo=timezone.utc)
        task = CalendarTask(
            title="Full",
            notes="Note",
            due=date(2025, 1, 20),
            status="completed",
            completed=dt,
            parent="parent1",
        )
        body = task.to_api_body()
        self.assertEqual(body["title"], "Full")
        self.assertEqual(body["notes"], "Note")
        self.assertEqual(body["due"], "2025-01-20T00:00:00.000Z")
        self.assertEqual(body["status"], "completed")
        self.assertEqual(body["completed"], "2025-01-15T12:00:00.000Z")
        self.assertEqual(body["parent"], "parent1")

    def test_from_api_response(self) -> None:
        data = {
            "title": "API Task",
            "id": "task1",
            "notes": "Notes",
            "due": "2025-01-20T00:00:00.000Z",
            "completed": "2025-01-18T10:30:00.000Z",
            "status": "completed",
            "parent": "parent1",
            "tasklist_id": "list1",
            "position": "0001",
        }
        task = CalendarTask.from_api_response(data)
        self.assertEqual(task.title, "API Task")
        self.assertEqual(task.id, "task1")
        self.assertEqual(task.notes, "Notes")
        self.assertEqual(task.due, date(2025, 1, 20))
        self.assertEqual(task.completed, datetime(2025, 1, 18, 10, 30, tzinfo=timezone.utc))
        self.assertEqual(task.status, "completed")
        self.assertEqual(task.parent, "parent1")
        self.assertEqual(task.tasklist_id, "list1")
        self.assertEqual(task.position, "0001")

    def test_from_api_response_defaults(self) -> None:
        data = {"title": "Minimal"}
        task = CalendarTask.from_api_response(data)
        self.assertEqual(task.title, "Minimal")
        self.assertIsNone(task.due)
        self.assertIsNone(task.completed)
        self.assertEqual(task.status, "needsAction")


class TestTimeSlot(unittest.TestCase):
    """Tests for TimeSlot dataclass."""

    def _make(self, start_h: int, end_h: int, is_free: bool = True) -> TimeSlot:
        return TimeSlot(
            start=datetime(2025, 1, 15, start_h, 0, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, end_h, 0, tzinfo=timezone.utc),
            is_free=is_free,
        )

    def test_start_equals_end_raises(self) -> None:
        t = datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc)
        with self.assertRaises(ValueError):
            TimeSlot(start=t, end=t)

    def test_start_after_end_raises(self) -> None:
        t1 = datetime(2025, 1, 15, 11, 0, tzinfo=timezone.utc)
        t2 = datetime(2025, 1, 15, 9, 0, tzinfo=timezone.utc)
        with self.assertRaises(ValueError):
            TimeSlot(start=t1, end=t2)

    def test_duration_minutes(self) -> None:
        slot = self._make(9, 11)
        self.assertEqual(slot.duration_minutes(), 120)

    def test_overlaps_true_partial(self) -> None:
        a = self._make(9, 11)
        b = self._make(10, 12)
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

    def test_overlaps_true_contained(self) -> None:
        a = self._make(9, 12)
        b = self._make(10, 11)
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

    def test_overlaps_false(self) -> None:
        a = self._make(9, 10)
        b = self._make(10, 11)
        self.assertFalse(a.overlaps(b))
        self.assertFalse(b.overlaps(a))

    def test_contains_true(self) -> None:
        slot = self._make(9, 11)
        point = datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc)
        self.assertTrue(slot.contains(point))

    def test_contains_at_start(self) -> None:
        slot = self._make(9, 11)
        point = datetime(2025, 1, 15, 9, 0, tzinfo=timezone.utc)
        self.assertTrue(slot.contains(point))

    def test_contains_at_end_false(self) -> None:
        slot = self._make(9, 11)
        point = datetime(2025, 1, 15, 11, 0, tzinfo=timezone.utc)
        self.assertFalse(slot.contains(point))

    def test_contains_outside(self) -> None:
        slot = self._make(9, 11)
        point = datetime(2025, 1, 15, 8, 0, tzinfo=timezone.utc)
        self.assertFalse(slot.contains(point))

    def test_split_at_before_start(self) -> None:
        slot = self._make(9, 11)
        boundary = datetime(2025, 1, 15, 8, 0, tzinfo=timezone.utc)
        left, right = slot.split_at(boundary)
        self.assertIsNone(left)
        self.assertEqual(right, slot)

    def test_split_at_after_end(self) -> None:
        slot = self._make(9, 11)
        boundary = datetime(2025, 1, 15, 12, 0, tzinfo=timezone.utc)
        left, right = slot.split_at(boundary)
        self.assertEqual(left, slot)
        self.assertIsNone(right)

    def test_split_at_inside(self) -> None:
        slot = self._make(9, 12)
        boundary = datetime(2025, 1, 15, 10, 30, tzinfo=timezone.utc)
        left, right = slot.split_at(boundary)
        self.assertIsNotNone(left)
        self.assertIsNotNone(right)
        self.assertEqual(left.start, slot.start)
        self.assertEqual(left.end, boundary)
        self.assertEqual(right.start, boundary)
        self.assertEqual(right.end, slot.end)
        self.assertEqual(left.is_free, slot.is_free)
        self.assertEqual(right.is_free, slot.is_free)

    def test_intersect_overlapping(self) -> None:
        a = self._make(9, 12)
        b = self._make(10, 14, is_free=False)
        result = a.intersect(b)
        self.assertIsNotNone(result)
        self.assertEqual(result.start, datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc))
        self.assertEqual(result.end, datetime(2025, 1, 15, 12, 0, tzinfo=timezone.utc))
        self.assertFalse(result.is_free)

    def test_intersect_no_overlap(self) -> None:
        a = self._make(9, 10)
        b = self._make(10, 11)
        self.assertIsNone(a.intersect(b))

    def test_intersect_free_and_free(self) -> None:
        a = self._make(9, 12, is_free=True)
        b = self._make(10, 11, is_free=True)
        result = a.intersect(b)
        self.assertTrue(result.is_free)


class TestFreeBusyWindow(unittest.TestCase):
    """Tests for FreeBusyWindow dataclass."""

    def test_is_available_true(self) -> None:
        window = FreeBusyWindow(email="user@example.com")
        self.assertTrue(window.is_available)

    def test_is_available_false(self) -> None:
        busy = TimeSlot(
            start=datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, 11, 0, tzinfo=timezone.utc),
            is_free=False,
        )
        window = FreeBusyWindow(email="user@example.com", busy_slots=[busy])
        self.assertFalse(window.is_available)


if __name__ == "__main__":
    unittest.main()
