from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app.schemas import TaskStatus
from app.service import complete_task, get_task, list_tasks


class TaskApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.data_file = Path(self.temporary_directory.name) / "tasks.json"
        self.data_file.write_text(
            json.dumps(
                [
                    {
                        "id": 1,
                        "title": "Open task",
                        "description": "",
                        "status": "open",
                        "priority": "medium",
                        "created_at": "2026-01-01T00:00:00+00:00",
                        "completed_at": None,
                    },
                    {
                        "id": 2,
                        "title": "Done LAUNCH task",
                        "description": "Contains a Report summary",
                        "status": "done",
                        "priority": "medium",
                        "created_at": "2026-01-01T00:00:00+00:00",
                        "completed_at": "2026-01-02T00:00:00+00:00",
                    },
                ]
            ),
            encoding="utf-8",
        )
        self.data_file_patch = patch("app.store.DATA_FILE", self.data_file)
        self.data_file_patch.start()

    def tearDown(self) -> None:
        self.data_file_patch.stop()
        self.temporary_directory.cleanup()

    def test_status_filter_uses_query_enum_value(self) -> None:
        tasks = list_tasks(status=TaskStatus.open)

        self.assertEqual([task["id"] for task in tasks], [1])

    def test_query_matches_title_case_insensitively(self) -> None:
        tasks = list_tasks(q="launch")

        self.assertEqual([task["id"] for task in tasks], [2])

    def test_query_matches_description_case_insensitively(self) -> None:
        tasks = list_tasks(q="report")

        self.assertEqual([task["id"] for task in tasks], [2])

    def test_query_works_with_status_filter(self) -> None:
        tasks = list_tasks(status=TaskStatus.open, q="task")

        self.assertEqual([task["id"] for task in tasks], [1])

    def test_complete_task_persists_to_storage(self) -> None:
        completed = complete_task(1)
        fetched = get_task(1)
        stored = json.loads(self.data_file.read_text(encoding="utf-8"))

        self.assertIsNotNone(completed)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["status"], "done")
        self.assertIsNotNone(fetched["completed_at"])
        self.assertEqual(stored[0]["status"], "done")
        self.assertIsNotNone(stored[0]["completed_at"])


if __name__ == "__main__":
    unittest.main()
