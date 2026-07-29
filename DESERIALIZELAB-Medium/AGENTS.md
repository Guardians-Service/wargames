<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-29 | Updated: 2026-07-29 -->

# DESERIALIZELAB-Medium

## Purpose
A Flask "load saved settings" feature demonstrating insecure deserialization. `POST /load` accepts a base64-encoded blob and calls `pickle.loads()` on the decoded bytes with no validation, the classic Python pickle RCE sink. The intended solve is crafting a payload locally with a `__reduce__` method that runs a shell command (e.g. `cat flag.txt`), base64-encoding it, and POSTing it — the command's output comes back in the response.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `POST /load` reads a `data` field (form or JSON), base64-decodes it, and calls `pickle.loads()` directly on the bytes, returning `str(result)` in the JSON response |
| `Dockerfile` | `python:3.11-slim`, installs `flask`, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, readable from the container filesystem by whatever command the crafted pickle payload executes |
| `info.txt` | Korean challenge write-up: goal (craft a malicious pickle payload for RCE), difficulty (중/Medium) |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to insecure deserialization** — calling `pickle.loads()` directly on user-controlled bytes with no validation/sandboxing is the entire point. Do not switch to `json`/a restricted unpickler/an allowlist-based deserializer; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested. Keep any executed commands confined to this container's own filesystem — do not add network tools or capabilities that would let a payload reach outside the container.

### Testing Requirements
```bash
cd DESERIALIZELAB-Medium
docker build -t deserializelab-medium .
docker run -p 8000:8000 deserializelab-medium
```
Verify the intended solve path still works: craft a pickle payload with `__reduce__` returning `(subprocess.check_output, (["cat", "flag.txt"],))`, base64-encode it, and confirm `POST /load` with that as `data` returns the flag text in the response.

### Common Patterns
- Single-file Flask app (`app.py`), listens on `0.0.0.0:8000`.
- No sandboxing/validation on `pickle.loads()` input by design — this is the standard, well-understood pattern for this class of lab (same "arbitrary command execution confined to the container" philosophy as `RCELAB-Easy`'s OS command injection).

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`; stdlib `pickle`, `base64`, `subprocess`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
