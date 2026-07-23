<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# SQLI-Easy

## Purpose
A Flask app ("SQL Injection Lab - Easy") with a login form whose `username`/`password` query params are concatenated directly into a SQLite query string with no parameterization. The goal is a classic SQL injection auth bypass (e.g., `username=admin' --`) to log in and reveal the flag, which is stored as the `admin` user's password in the `users` table.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | On startup, creates an in-memory-backed SQLite `users` table with one row (`admin`, `FLAG`); `GET /` renders the login form; `GET /login` builds `SELECT * FROM users WHERE username = '{username}' AND password = '{password}'` via f-string and executes it, returning the flag on any matching row |
| `Dockerfile` | `python:3.9-slim`, installs Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, inserted as the `admin` row's password value at startup |
| `info.txt` | Korean challenge write-up: goal (SQLi login bypass), difficulty (하/Easy), example payload `username=admin' --` |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to SQL injection** — the f-string-built query in `/login` with no parameterized query (`?`/`sqlite3.connect(...).execute(query, params)`) and no input escaping is the entire point of the challenge. Do not switch to parameterized queries, add input sanitization, or use an ORM; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd SQLI-Easy
docker build -t sqli-easy .
docker run -p 8000:8000 sqli-easy
```
Verify the intended solve path still works, e.g.:
```bash
curl "http://localhost:8000/login?username=admin'%20--&password="
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS f-string, listens on `0.0.0.0:8000`.
- Uses `sqlite3.connect(..., check_same_thread=False)` with a single shared connection/cursor at module scope; DB is rebuilt fresh (`DROP TABLE IF EXISTS` + `CREATE`) on every process start, so it is not persisted across restarts.
- Query is logged via `print("[DEBUG]", query)` — intentional, aids players debugging their payloads via container logs.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.9-slim`; pip package `flask`; stdlib `sqlite3`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
