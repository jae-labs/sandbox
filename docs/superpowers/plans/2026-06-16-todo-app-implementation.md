# Todo Application Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a robust command-line Todo application in Python backed by SQLite with complete TDD coverage.

**Architecture:** A layered architecture separating CLI input/parsing (`cli.py`), SQLite CRUD operations (`db.py`), and the core dataclass model with validation (`models.py`).

**Tech Stack:** Python 3.x, standard library (`sqlite3`, `argparse`, `dataclasses`), and `pytest` for the testing framework.

---

### Task 1: Core Domain Model and Input Validation

**Files:**
* Create: `src/todo/models.py`
* Create: `tests/test_models.py`

- [ ] **Step 1: Write a failing test for models validation**
  
  Create file `tests/test_models.py` with:
  ```python
  import pytest
  from datetime import datetime
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
  ```

- [ ] **Step 2: Run the test to verify it fails**
  
  Run: `pytest tests/test_models.py`
  Expected output: `ModuleNotFoundError: No module named 'todo'` or import error.

- [ ] **Step 3: Write minimal implementation for models**
  
  Create file `src/todo/models.py` with:
  ```python
  from dataclasses import dataclass, field
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
  ```

- [ ] **Step 4: Run the test to verify it passes**
  
  Run: `pytest tests/test_models.py`
  Expected output: `1 passed` (Make sure PYTHONPATH includes `src/`)

- [ ] **Step 5: Commit changes**
  
  Run:
  ```bash
  git add src/todo/models.py tests/test_models.py
  git commit -m "feat: add TodoItem model with title, priority, and date validation"
  ```

---

### Task 2: Database Persistence Layer

**Files:**
* Create: `src/todo/db.py`
* Create: `tests/test_db.py`

- [ ] **Step 1: Write failing tests for SQLite CRUD operations**
  
  Create file `tests/test_db.py` with:
  ```python
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
  ```

- [ ] **Step 2: Run tests to verify failure**
  
  Run: `pytest tests/test_db.py`
  Expected output: `ImportError: cannot import name 'DatabaseManager'`

- [ ] **Step 3: Implement DatabaseManager logic**
  
  Create file `src/todo/db.py` with:
  ```python
  import sqlite3
  from typing import List, Optional
  from todo.models import TodoItem

  class DatabaseManager:
      def __init__(self, db_path: str):
          self.db_path = db_path

      def get_connection(self):
          return sqlite3.connect(self.db_path)

      def init_db(self):
          with self.get_connection() as conn:
              conn.execute("""
                  CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      description TEXT,
                      priority TEXT CHECK(priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
                      due_date TEXT,
                      completed INTEGER DEFAULT 0,
                      created_at TEXT DEFAULT CURRENT_TIMESTAMP
                  )
              """)
              conn.commit()

      def add_task(self, item: TodoItem) -> TodoItem:
          with self.get_connection() as conn:
              cursor = conn.cursor()
              cursor.execute(
                  "INSERT INTO tasks (title, description, priority, due_date, completed) VALUES (?, ?, ?, ?, ?)",
                  (item.title, item.description, item.priority, item.due_date, item.completed)
              )
              item.id = cursor.lastrowid
              conn.commit()
          return item

      def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None, sort: Optional[str] = None) -> List[TodoItem]:
          query = "SELECT id, title, description, priority, due_date, completed, created_at FROM tasks WHERE 1=1"
          params = []
          
          if status == "completed":
              query += " AND completed = 1"
          elif status == "pending":
              query += " AND completed = 0"
              
          if priority:
              query += " AND priority = ?"
              params.append(priority)
              
          if sort == "due":
              query += " ORDER BY due_date ASC"
          elif sort == "created":
              query += " ORDER BY created_at ASC"
          else:
              query += " ORDER BY id ASC"

          tasks = []
          with self.get_connection() as conn:
              cursor = conn.cursor()
              cursor.execute(query, params)
              for row in cursor.fetchall():
                  tasks.append(TodoItem(
                      id=row[0],
                      title=row[1],
                      description=row[2],
                      priority=row[3],
                      due_date=row[4],
                      completed=row[5],
                      created_at=row[6]
                  ))
          return tasks

      def _verify_task_exists(self, task_id: int):
          with self.get_connection() as conn:
              cursor = conn.cursor()
              cursor.execute("SELECT 1 FROM tasks WHERE id = ?", (task_id,))
              if not cursor.fetchone():
                  raise ValueError(f"Task with ID {task_id} not found")

      def complete_task(self, task_id: int, completed: int = 1):
          self._verify_task_exists(task_id)
          with self.get_connection() as conn:
              conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
              conn.commit()

      def delete_task(self, task_id: int):
          self._verify_task_exists(task_id)
          with self.get_connection() as conn:
              conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
              conn.commit()

      def edit_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, due_date: Optional[str] = None):
          self._verify_task_exists(task_id)
          updates = []
          params = []
          
          if title is not None:
              if not title.strip():
                  raise ValueError("Title cannot be empty")
              updates.append("title = ?")
              params.append(title)
          if description is not None:
              updates.append("description = ?")
              params.append(description)
          if priority is not None:
              if priority not in ("low", "medium", "high"):
                  raise ValueError("Invalid priority")
              updates.append("priority = ?")
              params.append(priority)
          if due_date is not None:
              updates.append("due_date = ?")
              params.append(due_date)
              
          if not updates:
              return
              
          query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
          params.append(task_id)
          
          with self.get_connection() as conn:
              conn.execute(query, params)
              conn.commit()
  ```

- [ ] **Step 4: Run tests to verify it passes**
  
  Run: `pytest tests/test_db.py`
  Expected output: `1 passed`

- [ ] **Step 5: Commit changes**
  
  Run:
  ```bash
  git add src/todo/db.py tests/test_db.py
  git commit -m "feat: add DatabaseManager with SQLite CRUD support"
  ```

---

### Task 3: CLI Parser and Argument Dispatcher

**Files:**
* Create: `src/todo/cli.py`
* Create: `tests/test_cli.py`

- [ ] **Step 1: Write integration tests for commands parsing and console output**
  
  Create file `tests/test_cli.py` with:
  ```python
  import sys
  import pytest
  from todo.cli import main

  def test_cli_add_and_list(tmp_path, monkeypatch, capsys):
      db_file = str(tmp_path / "todo.db")
      monkeypatch.setenv("TODO_DB_PATH", db_file)

      # Test adding a task
      monkeypatch.setattr(sys, "argv", ["todo", "add", "Task 1", "--priority", "high"])
      main()
      captured = capsys.readouterr()
      assert "added successfully" in captured.out

      # Test listing tasks
      monkeypatch.setattr(sys, "argv", ["todo", "list"])
      main()
      captured = capsys.readouterr()
      assert "Task 1" in captured.out
      assert "high" in captured.out

      # Test completing task
      monkeypatch.setattr(sys, "argv", ["todo", "complete", "1"])
      main()
      captured = capsys.readouterr()
      assert "completed successfully" in captured.out

      # Test error handling: invalid date
      monkeypatch.setattr(sys, "argv", ["todo", "add", "Task 2", "--due", "invalid-date"])
      with pytest.raises(SystemExit) as exc:
          main()
      assert exc.value.code == 1
      captured = capsys.readouterr()
      assert "Error" in captured.err

      # Test error handling: task not found
      monkeypatch.setattr(sys, "argv", ["todo", "complete", "999"])
      with pytest.raises(SystemExit) as exc:
          main()
      assert exc.value.code == 1
      captured = capsys.readouterr()
      assert "Error" in captured.err
  ```

- [ ] **Step 2: Run tests to verify failure**
  
  Run: `pytest tests/test_cli.py`
  Expected output: `ImportError: cannot import name 'main' from 'todo.cli'`

- [ ] **Step 3: Implement main CLI entrypoint**
  
  Create file `src/todo/cli.py` with:
  ```python
  import argparse
  import os
  import sys
  from todo.db import DatabaseManager
  from todo.models import TodoItem

  def get_db_manager() -> DatabaseManager:
      db_path = os.getenv("TODO_DB_PATH", "todo.db")
      manager = DatabaseManager(db_path)
      manager.init_db()
      return manager

  def main():
      parser = argparse.ArgumentParser(description="CLI Todo Application")
      subparsers = parser.add_subparsers(dest="command")

      # Add subcommand
      parser_add = subparsers.add_parser("add", help="Add a new task")
      parser_add.add_argument("title", type=str, help="Task title")
      parser_add.add_argument("--desc", type=str, default=None, help="Task description")
      parser_add.add_argument("--priority", type=str, choices=["low", "medium", "high"], default="medium", help="Task priority")
      parser_add.add_argument("--due", type=str, default=None, help="Task due date (YYYY-MM-DD)")

      # List subcommand
      parser_list = subparsers.add_parser("list", help="List tasks")
      parser_list.add_argument("--status", type=str, choices=["all", "completed", "pending"], default="all", help="Filter by status")
      parser_list.add_argument("--priority", type=str, choices=["low", "medium", "high"], default=None, help="Filter by priority")
      parser_list.add_argument("--sort", type=str, choices=["due", "created"], default=None, help="Sort parameter")

      # Complete subcommand
      parser_complete = subparsers.add_parser("complete", help="Complete a task")
      parser_complete.add_argument("id", type=int, help="Task ID")

      # Uncomplete subcommand
      parser_uncomplete = subparsers.add_parser("uncomplete", help="Uncomplete a task")
      parser_uncomplete.add_argument("id", type=int, help="Task ID")

      # Delete subcommand
      parser_delete = subparsers.add_parser("delete", help="Delete a task")
      parser_delete.add_argument("id", type=int, help="Task ID")

      # Edit subcommand
      parser_edit = subparsers.add_parser("edit", help="Edit a task")
      parser_edit.add_argument("id", type=int, help="Task ID")
      parser_edit.add_argument("--title", type=str, default=None, help="New task title")
      parser_edit.add_argument("--desc", type=str, default=None, help="New task description")
      parser_edit.add_argument("--priority", type=str, choices=["low", "medium", "high"], default=None, help="New priority")
      parser_edit.add_argument("--due", type=str, default=None, help="New due date (YYYY-MM-DD)")

      args = parser.parse_args()
      if not args.command:
          parser.print_help()
          return

      db = get_db_manager()

      try:
          if args.command == "add":
              item = TodoItem(
                  title=args.title,
                  description=args.desc,
                  priority=args.priority,
                  due_date=args.due
              )
              inserted = db.add_task(item)
              print(f"Task {inserted.id} added successfully.")

          elif args.command == "list":
              status = None if args.status == "all" else args.status
              tasks = db.list_tasks(status=status, priority=args.priority, sort=args.sort)
              if not tasks:
                  print("No tasks found.")
                  return
              print(f"{'ID':<4} | {'Title':<20} | {'Priority':<8} | {'Due Date':<10} | {'Completed':<9}")
              print("-" * 60)
              for t in tasks:
                  status_str = "Yes" if t.completed == 1 else "No"
                  due_str = t.due_date if t.due_date else "None"
                  print(f"{t.id:<4} | {t.title:<20} | {t.priority:<8} | {due_str:<10} | {status_str:<9}")

          elif args.command == "complete":
              db.complete_task(args.id, completed=1)
              print(f"Task {args.id} marked completed successfully.")

          elif args.command == "uncomplete":
              db.complete_task(args.id, completed=0)
              print(f"Task {args.id} marked pending successfully.")

          elif args.command == "delete":
              db.delete_task(args.id)
              print(f"Task {args.id} deleted successfully.")

          elif args.command == "edit":
              db.edit_task(
                  task_id=args.id,
                  title=args.title,
                  description=args.desc,
                  priority=args.priority,
                  due_date=args.due
              )
              print(f"Task {args.id} updated successfully.")

      except ValueError as e:
          print(f"Error: {e}", file=sys.stderr)
          sys.exit(1)
      except Exception as e:
          print(f"Unexpected Error: {e}", file=sys.stderr)
          sys.exit(1)

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 4: Run tests to verify it passes**
  
  Run: `pytest tests/test_cli.py`
  Expected output: `1 passed`

- [ ] **Step 5: Commit changes**
  
  Run:
  ```bash
  git add src/todo/cli.py tests/test_cli.py
  git commit -m "feat: add CLI parser and command dispatcher interface"
  ```
