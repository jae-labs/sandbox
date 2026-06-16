from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class TodoItem:
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[str] = None
    completed: int = 0
    id: Optional[int] = None
    created_at: Optional[str] = None

    @staticmethod
    def validate_title(title: str):
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

    @staticmethod
    def validate_priority(priority: str):
        if priority not in ("low", "medium", "high"):
            raise ValueError("Invalid priority: must be low, medium, or high")

    @staticmethod
    def validate_due_date(due_date: Optional[str]):
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format")

    def __post_init__(self):
        self.validate_title(self.title)
        self.validate_priority(self.priority)
        self.validate_due_date(self.due_date)
