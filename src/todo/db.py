import sqlite3
from typing import List, Optional
from todo.models import TodoItem

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = None

    def get_connection(self):
        if self.db_path == ":memory:":
            if self._conn is None:
                self._conn = sqlite3.connect(self.db_path)
            return self._conn
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
