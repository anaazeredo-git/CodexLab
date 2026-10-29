import json
from pathlib import Path
from typing import Any


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def load_tasks() -> list[dict[str, Any]]:
    """Read all task records from the local JSON data file."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    """Persist task records back to disk."""
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(tasks, handle, indent=2)


def update_task(task_id: int, changes: dict[str, Any]) -> dict[str, Any] | None:
    """Apply changes to one task and persist the updated collection."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task.update(changes)
            save_tasks(tasks)
            return task

    return None


def next_task_id(tasks: list[dict[str, Any]]) -> int:
    """Generate the next numeric ID based on the existing records."""
    return max((task["id"] for task in tasks), default=0) + 1
