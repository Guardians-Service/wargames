<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# XSSLAB-Medium

## Purpose
A Flask app ("XSS Lab - Medium") that reflects the `q` query parameter directly into the page HTML with no escaping, while the flag is only served via a separate same-origin JSON endpoint (`GET /flag`) that is never linked or rendered in the page. The goal is a reflected XSS payload that runs `fetch('/flag')` from the victim's browser context and `alert()`s the JSON response's `flag` field — a step up from XSSLAB-Easy since the payload must make an authenticated same-origin request rather than just read local page state.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /` reads `q` from the query string and interpolates it unescaped into an f-string HTML response via `{q}` (rendered inside `Hello {q}`); `GET /flag` returns `{"flag": FLAG}` as JSON via `jsonify` |
| `Dockerfile` | `python:3.9-slim`, copies `app.py`/`flag.txt`, installs Flask, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag (`FLAG{m3dium_lvl_hack}`), loaded at startup and served by `/flag` |
| `info.txt` | Korean challenge write-up: goal (XSS → `fetch('/flag')` → `alert()` the result), difficulty (중/Medium), example payload `?q=<script>fetch('/flag').then(r=>r.json()).then(d=>alert(d.flag))</script>` plus a URL-encoded variant |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to reflected XSS** — the `q` parameter is inserted into the HTML response with zero escaping (`Hello {q}` in a raw f-string), and `/flag` is a same-origin, unauthenticated JSON endpoint reachable from injected JS via `fetch()`. This is the entire point of the challenge. Do not add HTML escaping to `q`, add auth/CSRF protection to `/flag`, or add CORS/CSP restrictions that would block the intended `fetch()` solve path — doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd XSSLAB-Medium
docker build -t xsslab-medium .
docker run -p 8000:8000 xsslab-medium
```
Verify the intended solve path still works, e.g.:
```
http://localhost:8000/?q=<script>fetch('/flag').then(r=>r.json()).then(d=>alert(d.flag))</script>
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS f-string, listens on `0.0.0.0:8000`.
- Two routes: `/` (the XSS injection point) and `/flag` (the JSON exfiltration target) — the split across routes is the "medium" difficulty step beyond XSSLAB-Easy's single-page JS-global approach.
- No output encoding on the `q` render path and no access control on `/flag` — both are the vulnerability, not an oversight.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.9-slim`; pip package `flask` (`jsonify`).

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
