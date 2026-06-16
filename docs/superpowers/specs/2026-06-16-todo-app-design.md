# CLI Todo Application Design Specification

**Status:** APPROVED
**Date:** 2026-06-16
**Author:** AIgile Agent

---

## 1. Overview & Goals
The CLI Todo application is a simple, command-line utility written in Python for managing personal tasks. The goals of this project are to provide a reliable task-tracking interface and serve as an E2E validation testbed for the AIgile SDLC workflow.

## 2. Requirements & Scope
The application must support the following operations:
* **Add Task:** Create a new task with a title (required), optional description, optional priority (low, medium, high), and optional due date (YYYY-MM-DD format).
* **List Tasks:** Display tasks in a formatted output. Supports filtering by completion status or priority, and sorting by due date or creation time.
* **Complete Task:** Mark a pending task as completed.
* **Uncomplete Task:** Mark a completed task as pending.
* **Delete Task:** Remove a task permanently from the database.
* **Edit Task:** Modify any attribute (title, description, priority, due date) of an existing task.

## 3. Technical Architecture
The application uses a layered architecture to isolate concerns:
1. **Presentation Layer (`cli.py`):** Parses command line arguments using Python's standard `argparse` module, validates basic input constraints, and renders success/error messages to stdout/stderr.
2. **Business & Domain Logic (`models.py`):** Defines the `TodoItem` data model and task validation rules.
3. **Data Access Layer (`db.py`):** Interacts with the SQLite database file to perform CRUD operations on the `tasks` table.

### 3.1 Database Schema
The database uses a single SQLite table:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT CHECK(priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
    due_date TEXT, -- YYYY-MM-DD format
    completed INTEGER DEFAULT 0, -- 0 for pending, 1 for completed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 4. Interface & Commands
All commands start with the executable name `todo` (or executing the script directly via `python src/todo/cli.py`).

* **Add:**
  ```bash
  todo add "Buy milk" --desc "Get 2% milk" --priority high --due 2026-06-20
  ```
* **List:**
  ```bash
  todo list --status pending --sort due
  ```
* **Complete/Uncomplete:**
  ```bash
  todo complete 1
  todo uncomplete 1
  ```
* **Delete:**
  ```bash
  todo delete 1
  ```
* **Edit:**
  ```bash
  todo edit 1 --title "Buy soy milk" --priority medium
  ```

## 5. Input Validation & Error Handling
* **Empty inputs:** Reject empty titles or whitespace-only inputs.
* **Invalid task IDs:** Show `Error: Task with ID <id> not found` and exit with status 1.
* **Invalid dates:** Validate date format against ISO 8601 (`YYYY-MM-DD`). Show `Error: Due date must be in YYYY-MM-DD format` and exit with status 1.
* **Database failure:** Gracefully catch SQLite connection errors, output `Error: Database file could not be accessed`, and exit with status 1.

## 6. Testing Strategy
* **Unit Tests (`tests/test_db.py`):** Use an in-memory SQLite database (`:memory:`) to verify insertion, deletion, query filters, and updates.
* **Integration Tests (`tests/test_cli.py`):** Mock inputs and standard streams to verify the argument parser, command routing, and console exit codes.
