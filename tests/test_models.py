import pytest
from todo.models import TodoItem

def test_todo_item_validation():
    # Valid case
    item = TodoItem(title="Buy milk", priority="medium")
    assert item.title == "Buy milk"
    assert item.completed == 0

    # Empty title validation
    with pytest.raises(ValueError, match="Title cannot be empty"):
        TodoItem(title="")

    # Invalid priority validation
    with pytest.raises(ValueError, match="Invalid priority"):
        TodoItem(title="Valid", priority="critical")

    # Invalid date format validation
    with pytest.raises(ValueError, match="Due date must be in YYYY-MM-DD format"):
        TodoItem(title="Valid", due_date="2026/06/16")
