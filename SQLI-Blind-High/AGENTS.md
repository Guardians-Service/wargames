<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-30 -->

# SQLI-Blind-High

## Purpose
A Flask app ("Blind SQL Injection Lab - High") whose `/api/check?id=` endpoint concatenates the `id` parameter directly into a SQL query with no parameterization, but only ever returns a boolean `{"exists": true/false}` — no query results, no error messages. The goal is boolean-based blind SQL injection to extract the flag (stored in a separate `secrets` table, never joined by the normal query path) one character at a time via conditions like `id=1 AND (SELECT substr(flag,1,1) FROM secrets)='F'`.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | On startup, creates an in-memory SQLite `users` table (5 rows) and a `secrets` table holding the flag; `GET /` renders a description page; `GET /api/check?id=` builds `SELECT id, username FROM users WHERE id = {id}` via f-string and executes it, catching all `sqlite3.Error` and always returning `{"exists": false}` on error (never leaks error text) |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, inserted as the sole row of the `secrets` table at startup |
| `info.txt` | Korean challenge write-up: goal (boolean-blind SQLi flag extraction), difficulty (상/High), example payloads and an sqlmap `--technique=B` invocation |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to blind SQL injection** — the f-string-built query in `/api/check` with no parameterization, and the fact that the endpoint only ever returns a boolean with no data/error leakage, are the entire point of the challenge. Do not switch to parameterized queries, add input sanitization, or leak more information in error responses — any of those breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd SQLI-Blind-High
docker build -t sqli-blind-high .
docker run -p 8000:8000 sqli-blind-high
```
Verify the intended solve path still works, e.g.:
```bash
curl "http://localhost:8000/api/check?id=1"                      # {"exists": true}
curl "http://localhost:8000/api/check?id=999"                     # {"exists": false}
curl --get "http://localhost:8000/api/check" --data-urlencode "id=1 AND (SELECT substr(flag,1,1) FROM secrets)='F'"  # {"exists": true} if flag starts with F
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML f-string for `/`, listens on `0.0.0.0:8000`.
- Uses `sqlite3.connect(":memory:", check_same_thread=False)` with a single shared connection/cursor at module scope; DB is rebuilt fresh on every process start.
- Query is logged via `print("[DEBUG]", query)` — intentional, aids players debugging their payloads via container logs.
- Distinguishing feature vs. `SQLI-Easy`/`SQLI-Medium`: those leak visible row data or DB structure directly; this one is purely boolean-blind, requiring iterative/scripted extraction.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`; stdlib `sqlite3`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
