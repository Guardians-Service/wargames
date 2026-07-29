<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-29 | Updated: 2026-07-29 -->

# SSRF-Medium

## Purpose
A Flask "URL preview" service demonstrating Server-Side Request Forgery. The server fetches whatever URL a user supplies (no allowlist) and echoes back a snippet of the response. A second, unlinked route only answers requests originating from loopback (`127.0.0.1`/`::1`), simulating an internal-only endpoint — the flag is only reachable by making the app request it on the player's behalf.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /?url=<url>` fetches the given URL server-side via `requests.get(...)` and returns the first ~1000 chars of the response, with no URL validation/allowlist. `GET /internal/flag` returns the flag only when `request.remote_addr` is a loopback address |
| `Dockerfile` | `python:3.11-slim`, installs `flask` + `requests`, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, served only by the loopback-gated `/internal/flag` route |
| `info.txt` | Korean challenge write-up: goal (SSRF to an internal-only path), difficulty (중/Medium), a suggestive (not fully explicit) hint about a loopback-only secret path |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to SSRF** — the `/` route's unrestricted server-side fetch of a user-supplied URL is the entire point. Do not add a URL allowlist/denylist, block loopback/private IP ranges, or otherwise validate the fetch target; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd SSRF-Medium
docker build -t ssrf-medium .
docker run -p 8000:8000 ssrf-medium
```
Verify the intended solve path still works:
```bash
curl "http://localhost:8000/internal/flag"          # should be 403/blocked from outside the container
curl "http://localhost:8000/?url=http://127.0.0.1:8000/internal/flag"   # should return the flag
```

### Common Patterns
- Single-file Flask app (`app.py`), listens on `0.0.0.0:8000`.
- The loopback check (`request.remote_addr`) is the entire access control for `/internal/flag` — this mirrors how the platform's real deployment gates the wargame pod's internal target, so keep the check exactly as-is rather than adding auth.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip packages `flask`, `requests`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
