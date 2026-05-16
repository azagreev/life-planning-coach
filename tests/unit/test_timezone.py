"""Unit tests for timezone handling in calendar reminder methods."""

import sys
import unittest
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

# Mock Google dependencies before importing calendar_integration modules.
_GOOGLE_MOCKS = {
    "google": MagicMock(),
    "google.auth": MagicMock(),
    "google.auth.transport": MagicMock(),
    "google.auth.transport.requests": MagicMock(),
    "google.oauth2": MagicMock(),
    "google.oauth2.credentials": MagicMock(),
    "googleapiclient": MagicMock(),
    "googleapiclient.discovery": MagicMock(),
    "googleapiclient.errors": MagicMock(),
    "google_auth_oauthlib": MagicMock(),
    "google_auth_oauthlib.flow": MagicMock(),
}

with patch.dict(sys.modules, _GOOGLE_MOCKS):
    from calendar_integration.calendar_manager import (
        CalendarManager,
        WEEKLY_REVIEW_RRULE,
        WOOP_RRULE,
    )


class TestTimezoneBug(unittest.TestCase):
    """Test that create_weekly_review_reminder and create_woop_reminder
    correctly apply the timezone parameter to start/end datetimes.
    """

    def setUp(self):
        mock_auth = MagicMock()
        self.manager = CalendarManager(auth=mock_auth)
        self.manager.create_event = MagicMock(return_value=MagicMock())

    def test_weekly_review_reminder_europe_moscow_timezone(self):
        """Weekly Review: start datetime should carry Europe/Moscow tzinfo."""
        self.manager.create_weekly_review_reminder(
            timezone="Europe/Moscow",
            hour=20,
            minute=0,
        )

        self.manager.create_event.assert_called_once()
        call_kwargs = self.manager.create_event.call_args.kwargs

        start = call_kwargs["start"]
        self.assertIsNotNone(
            start.tzinfo,
            "start datetime must have tzinfo when timezone is provided",
        )
        self.assertEqual(
            start.tzinfo,
            ZoneInfo("Europe/Moscow"),
        )
        self.assertEqual(call_kwargs["recurrence"], WEEKLY_REVIEW_RRULE)

    def test_weekly_review_reminder_utc_timezone(self):
        """Weekly Review: start datetime should carry UTC tzinfo."""
        self.manager.create_weekly_review_reminder(
            timezone="UTC",
            hour=19,
            minute=0,
        )

        self.manager.create_event.assert_called_once()
        call_kwargs = self.manager.create_event.call_args.kwargs

        start = call_kwargs["start"]
        self.assertIsNotNone(
            start.tzinfo,
            "start datetime must have tzinfo when timezone is provided",
        )
        self.assertEqual(
            start.tzinfo,
            ZoneInfo("UTC"),
        )
        self.assertEqual(call_kwargs["recurrence"], WEEKLY_REVIEW_RRULE)

    def test_woop_reminder_europe_moscow_timezone(self):
        """WOOP: start datetime should carry Europe/Moscow tzinfo."""
        self.manager.create_woop_reminder(
            timezone="Europe/Moscow",
            hour=7,
            minute=30,
        )

        self.manager.create_event.assert_called_once()
        call_kwargs = self.manager.create_event.call_args.kwargs

        start = call_kwargs["start"]
        self.assertIsNotNone(
            start.tzinfo,
            "start datetime must have tzinfo when timezone is provided",
        )
        self.assertEqual(
            start.tzinfo,
            ZoneInfo("Europe/Moscow"),
        )
        self.assertEqual(call_kwargs["recurrence"], WOOP_RRULE)

    def test_woop_reminder_utc_timezone(self):
        """WOOP: start datetime should carry UTC tzinfo."""
        self.manager.create_woop_reminder(
            timezone="UTC",
            hour=7,
            minute=0,
        )

        self.manager.create_event.assert_called_once()
        call_kwargs = self.manager.create_event.call_args.kwargs

        start = call_kwargs["start"]
        self.assertIsNotNone(
            start.tzinfo,
            "start datetime must have tzinfo when timezone is provided",
        )
        self.assertEqual(
            start.tzinfo,
            ZoneInfo("UTC"),
        )
        self.assertEqual(call_kwargs["recurrence"], WOOP_RRULE)


if __name__ == "__main__":
    unittest.main()
