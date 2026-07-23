<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# XSSLAB-Easy

## Purpose
A Flask app ("XSS Lab - Easy") that reflects the `q` query parameter directly into the page HTML with no escaping. The flag is embedded as a JavaScript global variable (`var flag = ...;`) that is never rendered on screen, so the goal is a reflected XSS payload (e.g., `<script>alert(flag)</script>`) that pops the flag via `alert()`.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /` reads `q` from the query string, interpolates it unescaped into an f-string HTML response via `{q}`; also embeds the flag as a JS global using `json.dumps(FLAG)` (`flag_js`) inside an inline `<script>` block |
| `Dockerfile` | `python:3.9-slim`, copies `app.py`/`flag.txt`, installs Flask, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag (`FLAG{e4sy_xss_win}`), loaded at startup and exposed as the JS global `flag` |
| `info.txt` | Korean challenge write-up: goal (pop `alert(flag)` via reflected XSS), difficulty (하/Easy), example payload `?q=<script>alert(flag)</script>` |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to reflected XSS** — the `q` parameter is inserted into the HTML response with zero escaping (`{q}` in a raw f-string). Note `json.dumps(FLAG)` is used only to safely embed the flag string as a JS literal (preventing it from breaking out of the `<script>` block) — it is *not* a mitigation for the `q` injection point, which remains wide open. Do not add HTML escaping to `q`, remove the `flag` global, or otherwise close the injection path — doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd XSSLAB-Easy
docker build -t xsslab-easy .
docker run -p 8000:8000 xsslab-easy
```
Verify the intended solve path still works, e.g.:
```
http://localhost:8000/?q=<script>alert(flag)</script>
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS f-string, listens on `0.0.0.0:8000`.
- `json.dumps()` is used deliberately to embed the flag as a JS literal — this is a JS-string-escaping technique for `flag`, distinct from (and not a substitute for) HTML-escaping `q`.
- No output encoding on the `q` render path — this is the vulnerability, not an oversight.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.9-slim`; pip package `flask`; stdlib `json`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
