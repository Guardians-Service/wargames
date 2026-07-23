<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# SSTILAB-Medium

## Purpose
A Flask app ("SSTI Lab") that passes a user-controlled `name` query parameter directly into an f-string that is then rendered with `render_template_string`, causing the value to be interpreted as Jinja2 template syntax rather than plain text. This enables Server-Side Template Injection leading to RCE (e.g., via the classic `cycler.__init__.__globals__.os.popen(...)` sandbox-escape gadget) to read `flag.txt`.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /` builds an f-string HTML template embedding the raw `name` query param, then calls `render_template_string(template)` on it (double vulnerability: the value is both f-string-interpolated *and* Jinja2-rendered); `GET /source` additionally leaks the app's own source code via `open(__file__).read()` |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, readable via an SSTI-driven `os.popen("cat flag.txt")` gadget |
| `info.txt` | Korean challenge write-up: goal (SSTI → RCE), difficulty (중/Medium), hints `{{7*7}}` and the full `cycler.__init__.__globals__.os.popen(...)` payload |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to Server-Side Template Injection** — passing untrusted input into `render_template_string` (instead of `render_template` with a fixed template + `name=name` context variable) is the entire point of the challenge, and the `/source` endpoint's source disclosure is also intentional (helps players confirm the vuln class). Do not switch to `render_template`/Jinja2 autoescaping-safe patterns, sandbox the Jinja2 environment, or remove `/source`; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd SSTILAB-Medium
docker build -t ssti-medium .
docker run -p 8000:8000 ssti-medium
```
Verify the intended solve path still works, e.g.:
```bash
curl "http://localhost:8000/?name=%7B%7B7*7%7D%7D"   # expect 49 reflected
curl "http://localhost:8000/?name=%7B%7Bcycler.__init__.__globals__.os.popen(%27cat%20flag.txt%27).read()%7D%7D"
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS f-string wrapping user input, listens on `0.0.0.0:8000`.
- Vulnerability is "double-layered": Python f-string interpolation embeds `name` into the template text, then `render_template_string` interprets that text as Jinja2 — both layers are needed for full RCE, distinguishing this from a simpler reflected-only SSTI.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask` (Jinja2 ships as a Flask dependency).

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
