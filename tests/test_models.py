"""Tests for the Task dataclass and related models."""

import pytest
from task_manager.models import Task, VALID_PRIORITIES, VALID_STATUSES


def test_task_defaults():
    task = Task(title="Buy milk")
    assert task.title == "Buy milk"
    assert task.priority == "medium"
    assert task.status == "pending"
    assert task.id is None
    assert task.created_at is None
    assert task.completed_at is None


def test_task_is_done_pending():
    task = Task(title="Pending task", status="pending")
    assert task.is_done() is False


def test_task_is_done_completed():
    task = Task(title="Done task", status="done")
    assert task.is_done() is True


def test_priority_rank_ordering():
    low = Task(title="low", priority="low")
    medium = Task(title="medium", priority="medium")
    high = Task(title="high", priority="high")
    assert low.priority_rank() < medium.priority_rank() < high.priority_rank()


def test_from_row():
    row = {
        "id": 42,
        "title": "Test task",
        "priority": "high",
        "status": "done",
        "created_at": "2024-01-01 12:00:00",
        "completed_at": "2024-01-02 09:00:00",
    }
    task = Task.from_row(row)
    assert task.id == 42
    assert task.title == "Test task"
    assert task.priority == "high"
    assert task.status == "done"
    assert task.created_at == "2024-01-01 12:00:00"
    assert task.completed_at == "2024-01-02 09:00:00"
    assert task.is_done() is True
