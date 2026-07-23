<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# RCELAB-Easy

## Purpose
A Flask app ("RCE Lab - Easy") that shells out to the system `ping` command using a user-controlled `host` query parameter concatenated directly into the shell string, with no sanitization. The goal is OS command injection (e.g., `8.8.8.8 && cat flag.txt`) to read `flag.txt`.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /` and `GET /ping` both run `os.popen(f"ping -c 1 {host}").read()` on the `host` query param and inline the raw output into the response |
| `Dockerfile` | `python:3.11-slim`, installs `iputils-ping` (for `ping`) and Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, readable via injected shell commands (e.g., `; cat flag.txt`) |
| `info.txt` | Korean challenge write-up: goal (OS command injection via `ping`), difficulty (하/Easy), example `curl` payload using `;` |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to OS command injection** — `os.popen(f"ping -c 1 {host}")` with no shell-metacharacter filtering, no `shlex.quote`, and no use of `subprocess` with an argument list is the entire point of the challenge. Do not sanitize `host`, switch to `subprocess.run([...], shell=False)`, or add a hostname/IP allowlist; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd RCELAB-Easy
docker build -t rce-easy .
docker run -p 8000:8000 rce-easy
```
Verify the intended solve path still works, e.g.:
```bash
curl "http://localhost:8000/ping?host=127.0.0.1;cat%20flag.txt"
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS f-string, listens on `0.0.0.0:8000`.
- Two nearly-identical vulnerable routes (`/` renders a form + result; `/ping` returns raw `<pre>` output) — both share the same unsafe `os.popen` call.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; OS package `iputils-ping`; pip package `flask`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
