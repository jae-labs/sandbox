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

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        
        if self.priority not in ("low", "medium", "high"):
            raise ValueError("Invalid priority: must be low, medium, or high")
        
        if self.due_date:
            try:
                datetime.strptime(self.due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format")
