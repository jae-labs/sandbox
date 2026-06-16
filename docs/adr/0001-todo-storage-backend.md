# ADR 0001: Storage Backend for CLI Todo Application

## Status
ACCEPTED

## Context
The Todo application requires a storage backend to persist tasks (such as title, description, priority, due date, completion status, and timestamps) across multiple terminal sessions.
We considered two primary storage options:
1. **JSON file storage:** Simpler to read and write directly using Python's standard `json` module, human-readable on disk, and has no database engine overhead.
2. **SQLite database storage:** A lightweight, single-file relational database engine included with standard Python, supporting complex filtering, indexing, schema constraints, and transactional safety.

## Decision
We will use **SQLite** as the storage backend.

## Rationale
* **Data Integrity & Schema Constraints:** SQLite allows us to enforce column-level types (e.g. integer completion flags) and constraints (e.g. `CHECK` statements for priority values `low|medium|high` and `NOT NULL` for titles).
* **Robust Filtering and Sorting:** Implementing sorting (by due date, creation time) and filtering (by status, priority) is clean and robust using standard SQL query clauses (`WHERE`, `ORDER BY`). With JSON, this would require custom in-memory parsing, sorting, and filtering logic in Python.
* **Transactional Safety:** SQLite provides ACID compliance, preventing corruption if the process is terminated mid-write.
* **Standard Library:** No external dependencies are needed since the `sqlite3` module is built into Python.

## Consequences
* **File format:** The database will be stored as a single binary file (`.db`).
* **Migrations:** Any schema modifications in the future will require executing SQLite migration scripts or running `ALTER TABLE` operations.
* **Testing:** We can use an in-memory SQLite database (`:memory:`) for fast unit tests without writing to the disk.
