"""Tests for database CRUD operations using real temp SQLite files."""

import pytest
from task_manager import database as db


@pytest.fixture
def db_path(tmp_path):
    """Provide a fresh temp SQLite file path for each test."""
    return str(tmp_path / "test.db")


def test_init_db_creates_table(db_path):
    db.init_db(db_path)
    import sqlite3
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'"
        ).fetchone()
    assert row is not None


def test_add_task_returns_task(db_path):
    task = db.add_task("Test task", "high", db_path)
    assert task.id == 1
    assert task.title == "Test task"
    assert task.priority == "high"
    assert task.status == "pending"


def test_add_task_default_priority(db_path):
    task = db.add_task("Default priority task", db_path=db_path)
    assert task.priority == "medium"


def test_get_task_exists(db_path):
    added = db.add_task("Find me", "low", db_path)
    found = db.get_task(added.id, db_path)
    assert found is not None
    assert found.id == added.id
    assert found.title == "Find me"


def test_get_task_not_found(db_path):
    db.init_db(db_path)
    result = db.get_task(999, db_path)
    assert result is None


def test_list_tasks_empty(db_path):
    tasks = db.list_tasks(db_path)
    assert tasks == []


def test_list_tasks_multiple(db_path):
    db.add_task("Task A", "high", db_path)
    db.add_task("Task B", "low", db_path)
    db.add_task("Task C", "medium", db_path)
    tasks = db.list_tasks(db_path)
    assert len(tasks) == 3
    assert tasks[0].title == "Task A"
    assert tasks[2].title == "Task C"


def test_complete_task(db_path):
    task = db.add_task("To complete", "medium", db_path)
    assert task.status == "pending"
    completed = db.complete_task(task.id, db_path)
    assert completed.status == "done"
    assert completed.completed_at is not None


def test_delete_task(db_path):
    task = db.add_task("To delete", "low", db_path)
    result = db.delete_task(task.id, db_path)
    assert result is True
    assert db.get_task(task.id, db_path) is None


def test_get_stats(db_path):
    db.add_task("High 1", "high", db_path)
    db.add_task("High 2", "high", db_path)
    task = db.add_task("Low 1", "low", db_path)
    db.complete_task(task.id, db_path)

    stats = db.get_stats(db_path)
    assert stats["total"] == 3
    assert stats["pending"] == 2
    assert stats["done"] == 1
    assert stats["by_priority"]["high"] == 2
    assert stats["by_priority"]["low"] == 1
