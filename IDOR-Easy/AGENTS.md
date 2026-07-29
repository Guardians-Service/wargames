<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-29 | Updated: 2026-07-29 -->

# IDOR-Easy

## Purpose
A Flask app ("IDOR Lab - Easy") demonstrating Insecure Direct Object Reference. A guest account can log in and view its own profile via `/profile?id=<n>`, but the endpoint never checks that the requested `id` belongs to the logged-in session. The goal is to change the `id` parameter from the guest's own id (`2`) to the admin's id (`1`) and read the flag embedded in the admin's profile data.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | Hardcoded users dict (`id=1` admin holding the flag, `id=2` guest/guest). `GET /login` sets a cookie with the numeric user id on valid guest credentials. `GET /profile?id=<n>` returns whatever profile matches `id`, with no check that it equals the session's own id |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, embedded in the admin (`id=1`) profile's bio field |
| `info.txt` | Korean challenge write-up: goal (IDOR — change the id parameter), difficulty (하/Easy) |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to IDOR** — `/profile` never verifies that the requesting session owns the requested `id`. Do not add an ownership check, session-to-id binding, or authorization middleware; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd IDOR-Easy
docker build -t idor-easy .
docker run -p 8000:8000 idor-easy
```
Verify the intended solve path still works, e.g.:
```bash
curl -c cookies.txt "http://localhost:8000/login?username=guest&password=guest"
curl -b cookies.txt "http://localhost:8000/profile?id=1"
```

### Common Patterns
- Single-file Flask app (`app.py`), listens on `0.0.0.0:8000`.
- Session is a plain cookie holding the numeric user id — no signing/encryption, kept intentionally simple to isolate the IDOR concept from unrelated auth-hardening concerns.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
