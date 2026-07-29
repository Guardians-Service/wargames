<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-29 | Updated: 2026-07-29 -->

# NOSQLI-Easy

## Purpose
A Flask login API backed by `mongomock` (in-memory MongoDB-compatible store) demonstrating NoSQL injection. The login endpoint builds a query directly from the JSON request body (`{"username": ..., "password": ...}`) with no type/operator validation, so a MongoDB query operator like `{"$ne": null}` in place of a literal password string bypasses authentication.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | Seeds a `users` collection (mongomock) with one `admin` document holding a real password and a `secret` field containing the flag. `POST /login` calls `collection.find_one({"username": body["username"], "password": body["password"]})` directly on the raw JSON values and returns the matched document (including `secret`) on success |
| `Dockerfile` | `python:3.11-slim`, installs `flask` + `mongomock`, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, embedded as the admin document's `secret` field at startup |
| `info.txt` | Korean challenge write-up: goal (NoSQL operator injection), difficulty (하/Easy) |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to NoSQL injection** — passing raw JSON body values straight into `find_one(...)` without validating they're strings (rather than dict operators like `$ne`) is the entire point of the challenge. Do not add type checking/sanitization on the query inputs; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd NOSQLI-Easy
docker build -t nosqli-easy .
docker run -p 8000:8000 nosqli-easy
```
Verify the intended solve path still works, e.g.:
```bash
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" \
  -d '{"username":"admin","password":{"$ne":null}}'
```

### Common Patterns
- Single-file Flask app (`app.py`), listens on `0.0.0.0:8000`.
- Uses `mongomock` (pure-Python, no real MongoDB server) so the container has no external DB dependency — keep it that way, don't swap in a real `pymongo`/MongoDB connection.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip packages `flask`, `mongomock`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
