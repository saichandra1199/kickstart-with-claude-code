"""SQLite CRUD operations for tasks."""

import sqlite3
from typing import Optional

from task_manager.models import Task

DEFAULT_DB_PATH = "./tasks.db"


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
            """
        )


def add_task(title: str, priority: str = "medium", db_path: str = DEFAULT_DB_PATH) -> Task:
    init_db(db_path)
    with _connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, priority) VALUES (?, ?)",
            (title, priority),
        )
        task_id = cursor.lastrowid
    return get_task(task_id, db_path)


def get_task(task_id: int, db_path: str = DEFAULT_DB_PATH) -> Optional[Task]:
    init_db(db_path)
    with _connect(db_path) as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return None
    return Task.from_row(dict(row))


def list_tasks(db_path: str = DEFAULT_DB_PATH) -> list[Task]:
    init_db(db_path)
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY id ASC"
        ).fetchall()
    return [Task.from_row(dict(row)) for row in rows]


def complete_task(task_id: int, db_path: str = DEFAULT_DB_PATH) -> Optional[Task]:
    init_db(db_path)
    with _connect(db_path) as conn:
        conn.execute(
            "UPDATE tasks SET status = 'done', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
            (task_id,),
        )
    return get_task(task_id, db_path)


def delete_task(task_id: int, db_path: str = DEFAULT_DB_PATH) -> bool:
    init_db(db_path)
    with _connect(db_path) as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return cursor.rowcount > 0


def get_stats(db_path: str = DEFAULT_DB_PATH) -> dict:
    init_db(db_path)
    with _connect(db_path) as conn:
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        pending = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'pending'"
        ).fetchone()[0]
        done = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'done'"
        ).fetchone()[0]
        by_priority = conn.execute(
            "SELECT priority, COUNT(*) as count FROM tasks GROUP BY priority"
        ).fetchall()

    return {
        "total": total,
        "pending": pending,
        "done": done,
        "by_priority": {row["priority"]: row["count"] for row in by_priority},
    }
