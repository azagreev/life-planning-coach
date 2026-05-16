"""Unit tests for TasksManager."""

from __future__ import annotations

import json
import unittest
from datetime import date, datetime, timezone
from unittest.mock import MagicMock, patch

from googleapiclient.errors import HttpError

from calendar_integration.exceptions import RateLimitError, TaskNotFoundError, ValidationError
from calendar_integration.models import CalendarTask
from calendar_integration.tasks_manager import TasksManager


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
    """Build a chainable mock Google API service for Tasks."""
    service = MagicMock()
    service.tasks.return_value = service.tasks
    service.tasklists.return_value = service.tasklists
    return service


class TestTasksManager(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_auth = MagicMock()
        self.mock_service = make_mock_service()
        self.mock_auth.build_service.return_value = self.mock_service
        self.manager = TasksManager(self.mock_auth)

    # ------------------------------------------------------------------
    # get_tasks
    # ------------------------------------------------------------------
    def test_get_tasks_passes_filtering_params(self) -> None:
        self.mock_service.tasks.list.return_value.execute.return_value = {"items": []}
        due_min = date(2025, 1, 1)
        due_max = date(2025, 1, 31)

        tasks = self.manager.get_tasks(
            tasklist_id="@default",
            show_completed=True,
            due_min=due_min,
            due_max=due_max,
            max_results=25,
        )

        self.assertEqual(tasks, [])
        self.mock_service.tasks.list.assert_called_once_with(
            tasklist="@default",
            maxResults=25,
            showCompleted=True,
            showDeleted=False,
            showHidden=False,
            dueMin="2025-01-01T00:00:00.000Z",
            dueMax="2025-01-31T00:00:00.000Z",
        )
        self.mock_auth.refresh_if_needed.assert_called()

    def test_get_tasks_returns_parsed_tasks(self) -> None:
        self.mock_service.tasks.list.return_value.execute.return_value = {
            "items": [
                {
                    "id": "t1",
                    "title": "Task One",
                    "status": "needsAction",
                    "due": "2025-01-15T00:00:00.000Z",
                }
            ]
        }

        tasks = self.manager.get_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertIsInstance(tasks[0], CalendarTask)
        self.assertEqual(tasks[0].id, "t1")
        self.assertEqual(tasks[0].title, "Task One")

    # ------------------------------------------------------------------
    # create_task
    # ------------------------------------------------------------------
    def test_create_task_body_structure(self) -> None:
        due = date(2025, 1, 20)
        self.mock_service.tasks.insert.return_value.execute.return_value = {
            "id": "new_task",
            "title": "Write tests",
            "notes": "Unit tests for managers",
            "due": "2025-01-20T00:00:00.000Z",
            "parent": "parent_id",
        }

        task = self.manager.create_task(
            title="Write tests",
            notes="Unit tests for managers",
            due=due,
            parent="parent_id",
            tasklist_id="custom_list",
        )

        self.assertIsInstance(task, CalendarTask)
        call_kwargs = self.mock_service.tasks.insert.call_args.kwargs
        self.assertEqual(call_kwargs["tasklist"], "custom_list")
        self.assertEqual(call_kwargs["parent"], "parent_id")

        body = call_kwargs["body"]
        self.assertEqual(body["title"], "Write tests")
        self.assertEqual(body["notes"], "Unit tests for managers")
        self.assertEqual(body["due"], "2025-01-20T00:00:00.000Z")
        self.assertEqual(body["parent"], "parent_id")
        self.assertEqual(body["status"], "needsAction")

    def test_create_task_validation_error(self) -> None:
        with self.assertRaises(ValidationError):
            self.manager.create_task(title="")

    # ------------------------------------------------------------------
    # complete_task
    # ------------------------------------------------------------------
    def test_complete_task_patches_status(self) -> None:
        self.mock_service.tasks.patch.return_value.execute.return_value = {
            "id": "t1",
            "title": "Task One",
            "status": "completed",
            "completed": "2025-01-15T12:00:00.000Z",
        }

        task = self.manager.complete_task("t1", tasklist_id="mylist")

        self.assertIsInstance(task, CalendarTask)
        self.assertEqual(task.status, "completed")

        call_kwargs = self.mock_service.tasks.patch.call_args.kwargs
        self.assertEqual(call_kwargs["tasklist"], "mylist")
        self.assertEqual(call_kwargs["task"], "t1")
        body = call_kwargs["body"]
        self.assertEqual(body["status"], "completed")
        self.assertIn("completed", body)
        # Verify it's a UTC timestamp string
        self.assertTrue(body["completed"].endswith("Z") or "+00:00" in body["completed"])

    # ------------------------------------------------------------------
    # create_daily_top3
    # ------------------------------------------------------------------
    def test_create_daily_top3_creates_parent_and_subtasks(self) -> None:
        call_count = 0
        fake_ids = ["parent_1", "sub_1", "sub_2", "sub_3"]

        def fake_create_task(*, title, notes="", due=None, parent=None, tasklist_id="@default"):
            nonlocal call_count
            task_id = fake_ids[call_count]
            call_count += 1
            return CalendarTask(
                title=title,
                id=task_id,
                due=due,
                parent=parent,
            )

        with patch.object(self.manager, "create_task", side_effect=fake_create_task):
            tasks = self.manager.create_daily_top3(
                priorities=["Read", "Write", "Run"],
                due=date(2025, 6, 1),
                tasklist_id="mylist",
            )

        self.assertEqual(len(tasks), 4)  # parent + 3 subtasks
        self.assertEqual(tasks[0].id, "parent_1")
        self.assertEqual(tasks[0].title, "Top-3 01.06.2025")

        subtasks = tasks[1:]
        self.assertEqual(subtasks[0].title, "1️⃣ Read")
        self.assertEqual(subtasks[0].parent, "parent_1")
        self.assertEqual(subtasks[1].title, "2️⃣ Write")
        self.assertEqual(subtasks[1].parent, "parent_1")
        self.assertEqual(subtasks[2].title, "3️⃣ Run")
        self.assertEqual(subtasks[2].parent, "parent_1")

    def test_create_daily_top3_validation_error(self) -> None:
        with self.assertRaises(ValidationError):
            self.manager.create_daily_top3(priorities=[], due=date(2025, 1, 1))

        with self.assertRaises(ValidationError):
            self.manager.create_daily_top3(
                priorities=[str(i) for i in range(11)],
                due=date(2025, 1, 1),
            )

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------
    def test_404_raises_task_not_found(self) -> None:
        self.mock_service.tasks.patch.return_value.execute.side_effect = (
            make_http_error(404)
        )

        with self.assertRaises(TaskNotFoundError):
            self.manager.complete_task("missing_id")


if __name__ == "__main__":
    unittest.main()
