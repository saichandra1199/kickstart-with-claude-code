"""Task dataclass and related constants."""

from dataclasses import dataclass, field
from typing import Optional

VALID_PRIORITIES = ("low", "medium", "high")
VALID_STATUSES = ("pending", "done")

PRIORITY_RANK = {"low": 0, "medium": 1, "high": 2}


@dataclass
class Task:
    title: str
    priority: str = "medium"
    status: str = "pending"
    id: Optional[int] = field(default=None)
    created_at: Optional[str] = field(default=None)
    completed_at: Optional[str] = field(default=None)

    def is_done(self) -> bool:
        return self.status == "done"

    def priority_rank(self) -> int:
        return PRIORITY_RANK.get(self.priority, 1)

    @classmethod
    def from_row(cls, row: dict) -> "Task":
        return cls(
            id=row["id"],
            title=row["title"],
            priority=row["priority"],
            status=row["status"],
            created_at=row["created_at"],
            completed_at=row["completed_at"],
        )
