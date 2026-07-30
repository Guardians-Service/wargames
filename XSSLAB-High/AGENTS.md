<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-30 -->

# XSSLAB-High

## Purpose
A Flask app ("XSS Lab - High (Filter Bypass)") with a guestbook page whose `comment` query parameter is reflected into the page after passing through a naive sanitizer that strips `<script>...</script>` blocks and any `on<word>="..."`/`on<word>='...'` (quoted) event handler, but does not touch unquoted event handler attributes. The goal is a Reflected XSS filter bypass — e.g. `<img src=x onerror=alert(document.cookie)>` — to exfiltrate the `FLAG` cookie set on every visit.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `sanitize()` applies two regexes: `SCRIPT_TAG` strips `<script>` blocks (case-insensitive, dotall), `QUOTED_EVENT_HANDLER` strips `on[a-zA-Z]+=(["']).*?\1` (quoted only); `GET /` reflects `sanitize(request.args.get("comment"))` into the page and sets a fresh `FLAG` cookie on every response |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, set as the `FLAG` cookie value on every `/` response |
| `info.txt` | Korean challenge write-up: goal (bypass the filter to steal the FLAG cookie), difficulty (상/High), example unquoted-handler payloads |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to a filter-bypass Reflected XSS** — the entire point is that `QUOTED_EVENT_HANDLER` only matches quoted attribute values, leaving unquoted event handlers (`onerror=alert(1)`, no surrounding quotes) untouched. Do not "fix" the regex to also catch unquoted handlers, add a proper HTML sanitizer/escaper, or set a CSP — any of those breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd XSSLAB-High
docker build -t xsslab-high .
docker run -p 8000:8000 xsslab-high
```
Verify the filter still blocks the quoted form and lets the unquoted form through, e.g. via the Python REPL:
```python
from app import sanitize
sanitize('<img src=x onerror="alert(1)">')          # -> handler stripped
sanitize('<img src=x onerror=alert(document.cookie)>')  # -> handler intact (intended bypass)
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML f-string/`.format()` template, listens on `0.0.0.0:8000`.
- `FLAG` cookie pattern matches `XSSLAB-Cookie` (Medium) — this lab is the harder sibling, requiring an actual filter bypass rather than reflecting the payload with zero filtering.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`; stdlib `re`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
