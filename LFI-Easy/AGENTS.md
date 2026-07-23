<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# LFI-Easy

## Purpose
A Flask app ("LFI Lab - Easy") that reads and returns a file from the `pages/` directory based on a user-controlled `?page=` query parameter, with no filtering or path sanitization. The goal is to use directory traversal (`../`) to escape `pages/` and read `flag.txt` from the app's working directory.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | Single route `GET /` opens `pages/{page}` (from `?page=`, default `home`) and inlines its contents into the response; any exception falls back to a 404 "Page not found" |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`, `flag.txt`, and `pages/`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, readable via path traversal out of `pages/` |
| `info.txt` | Korean challenge write-up: goal (read `flag.txt` via LFI), difficulty (하/Easy), hint `?page=../flag` |
| `.upload-include` | Files bundled for distribution: `pages/`, `app.py`, `Dockerfile` (excludes `flag.txt`) |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| [pages/AGENTS.md](pages/AGENTS.md) | Legitimate in-app pages (`home.html`, `about.html`) served by the `?page=` router; also the directory an attacker traverses out of |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to Local File Inclusion / path traversal** — the unsanitized `open(f"pages/{page}")` call is the entire point of the challenge. Do not add path canonicalization, an allowlist of page names, or `os.path.normpath`/`realpath` containment checks; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd LFI-Easy
docker build -t lfi-easy .
docker run -p 8000:8000 lfi-easy
```
Verify the intended solve path still works, e.g.:
```bash
curl "http://localhost:8000/?page=../flag.txt"
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS f-string, listens on `0.0.0.0:8000`.
- File path is built via plain string formatting (`f"pages/{page}"`) with no validation — the canonical unsafe LFI pattern.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
