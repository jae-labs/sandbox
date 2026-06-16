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
