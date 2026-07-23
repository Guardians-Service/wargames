<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# XSSLAB-Cookie

## Purpose
A Flask app ("XSS Lab - Cookie Stealer") that reflects the `q` query parameter directly into the page HTML with no escaping, while also setting a `FLAG` cookie on every response. The goal is a reflected XSS payload (e.g., `<script>alert(document.cookie)</script>`) that reads `document.cookie` to reveal the `FLAG` cookie value.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /` reads `q` from the query string and interpolates it unescaped into an f-string HTML response via `{q}`; sets `resp.set_cookie("FLAG", FLAG)` on every response |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag (`FLAG{xss_cookie_steal_success}`), loaded at startup and set as the `FLAG` cookie value |
| `info.txt` | Korean challenge write-up: goal (steal `document.cookie` via reflected XSS), difficulty (중/Medium), example payload `?q=<script>alert(document.cookie)</script>` |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to reflected XSS** — the `q` parameter is inserted into the HTML response with zero escaping (`{q}` in a raw f-string, not `markupsafe.escape`/Jinja2 autoescaping), and the `FLAG` cookie is set without `HttpOnly`, making it readable via `document.cookie` from injected JS. This is the entire point of the challenge. Do not add HTML escaping, a Content-Security-Policy, or `HttpOnly`/`Secure` cookie flags — doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd XSSLAB-Cookie
docker build -t xsslab-cookie .
docker run -p 8000:8000 xsslab-cookie
```
Verify the intended solve path still works, e.g.:
```
http://localhost:8000/?q=<script>alert(document.cookie)</script>
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS f-string, listens on `0.0.0.0:8000`.
- Uses `flask.make_response()` + `resp.set_cookie(...)` rather than Flask's default response, specifically so the `FLAG` cookie is attached to every request.
- No output encoding anywhere in the render path — this is the vulnerability, not an oversight.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
