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

def test_cli_list_empty(tmp_path, monkeypatch, capsys):
    db_file = str(tmp_path / "todo_empty.db")
    monkeypatch.setenv("TODO_DB_PATH", db_file)

    # Test listing tasks when database is empty
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main()
    captured = capsys.readouterr()
    assert "No tasks found." in captured.out

