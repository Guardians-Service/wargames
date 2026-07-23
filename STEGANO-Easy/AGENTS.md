<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# STEGANO-Easy

## Purpose
A Flask app ("Steganography Challenge") that serves a single PNG image (`stego.png`) with a flag hidden as plain text appended after the image's normal PNG data (trailing-bytes steganography). The goal is to download the image and extract the flag with a file-forensics tool (`strings`, `tail`, `binwalk`, etc.) rather than through the web app itself.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /` renders a page with an embedded `<img>` and a download link; `GET /stego.png` serves `stego.png` via `send_file` |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`stego.png`, exposes port 8000, runs `python app.py` |
| `stego.png` | A valid PNG image with the flag appended as trailing text after the image data ends |
| `flag.txt` | The plaintext flag matching the one embedded in `stego.png` (not served by the app; kept for reference/regeneration) |
| `info.txt` | Korean challenge write-up: goal (extract hidden flag from PNG), difficulty (하/Easy), hint commands `strings stego.png \| grep FLAG` / `tail -n 10 stego.png` |
| `.upload-include` | Files bundled for distribution: `app.py`, `stego.png` |

## For AI Agents

### Working In This Directory
**This lab's vulnerability is embedded in the image asset, not the app logic** — the flag hidden in `stego.png`'s trailing bytes is the entire point of the challenge. Do not "clean up," re-compress, or re-save `stego.png` (image tooling that re-encodes the file will strip the appended flag data and break the lab). The Flask app itself (`app.py`) has no injectable vulnerability and is just a static file server — do not add unrelated hardening to it either, to stay consistent with the rest of the repo's "don't touch challenge content" policy.

### Testing Requirements
```bash
cd STEGANO-Easy
docker build -t stegano-easy .
docker run -p 8000:8000 stegano-easy
```
Verify the intended solve path still works, e.g.:
```bash
curl -O http://localhost:8000/stego.png
strings stego.png | grep FLAG
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS, listens on `0.0.0.0:8000`, serves the static image via `send_file`.
- No `.upload-include` entry for `Dockerfile` or `flag.txt` — only `app.py` and `stego.png` are distributed to trainees (the app can be inspected, but the flag lives solely inside the binary asset).

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`.
- Solve tooling (not part of the app itself): `strings`, `binwalk`, `exiftool`, available in the `kali/` attacker container.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
