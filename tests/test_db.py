import os
import sqlite3
import pytest
from todo.db import DatabaseManager
from todo.models import TodoItem

@pytest.fixture
def db():
    # Use an in-memory database for testing
    manager = DatabaseManager(":memory:")
    manager.init_db()
    return manager

def test_db_operations(db):
    # Create task
    item = TodoItem(title="Test task", description="Test desc", priority="high", due_date="2026-06-20")
    inserted = db.add_task(item)
    assert inserted.id is not None
    assert inserted.completed == 0

    # Retrieve tasks
    tasks = db.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test task"

    # Complete task
    db.complete_task(inserted.id)
    tasks = db.list_tasks(status="completed")
    assert len(tasks) == 1
    assert tasks[0].completed == 1

    # Edit task
    db.edit_task(inserted.id, title="Updated task", priority="low")
    tasks = db.list_tasks()
    assert tasks[0].title == "Updated task"
    assert tasks[0].priority == "low"

    # Delete task
    db.delete_task(inserted.id)
    assert len(db.list_tasks()) == 0
