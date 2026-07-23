<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# SQLI-Medium

## Purpose
A Flask app ("SQLi Lab - Profile Lookup") with a `?id=` numeric parameter concatenated directly into a SQLite query with no parameterization or quoting, enabling UNION-based SQL injection. Unlike `SQLI-Easy`, output is minimal (only a username is echoed back), so the intended solve path is enumeration/exfiltration via `sqlmap` (`--dbs`, `--tables`, `--columns`, `--dump`) rather than a single crafted payload. The flag is stored in a `flag` column on a hidden row (`id=5`) of the same `users` table.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | On startup, creates a SQLite `users(id, username, email, flag)` table with 4 normal users and one flag-bearing row (`id=5`, empty username/email, `flag=FLAG`); `GET /` renders a lookup form; `GET /profile` builds `SELECT username FROM users WHERE id = {user_id}` via f-string (no quotes around the value — numeric context) and executes it |
| `Dockerfile` | `python:3.11-slim`, installs `sqlite3` CLI + Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, inserted as the hidden row's `flag` column value at startup |
| `info.txt` | Korean challenge write-up: goal (enumerate DB via SQLi, extract flag), difficulty (중/Medium), full `sqlmap` command sequence (`--dbs` → `--tables` → `--columns` → `--dump --where "id=5"`) |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to SQL injection** — the unquoted, unparameterized numeric `id` value spliced into the query is the entire point of the challenge, and the minimal output is deliberate (forces blind/UNION-based technique practice with `sqlmap`). Do not parameterize the query, cast/validate `id` as an integer before use, or add error suppression that would hide injectable behavior; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd SQLI-Medium
docker build -t sqli-medium .
docker run -p 8000:8000 sqli-medium
```
Verify the intended solve path still works, e.g.:
```bash
sqlmap -u "http://localhost:8000/profile?id=1" --batch --dbs
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS f-string, listens on `0.0.0.0:8000`.
- Uses `sqlite3.connect(..., check_same_thread=False)` with a single shared connection/cursor at module scope; DB rebuilt fresh on every process start.
- `/profile` wraps the query in `try/except`, returning a generic "Invalid input" page on SQL errors (rather than leaking a stack trace) — intentional, since error-based leakage isn't the intended technique here.
- Query is logged via `print("[DEBUG]", query)` for player debugging via container logs.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; OS package `sqlite3`; pip package `flask`; stdlib `sqlite3` module.
- Solve tooling (not part of the app itself): `sqlmap`, available in the `kali/` attacker container.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
