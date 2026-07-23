<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# CRYPTOLAB-XOR

## Purpose
A static Flask page that displays a Base64-encoded, single-byte-XOR-encrypted ciphertext (loaded from `cipher.txt`) and challenges the trainee to brute-force the 256 possible single-byte keys to recover a `FLAG{...}`-shaped plaintext. Like `CRYPTOLAB-Caesar`, all "solving" happens client-side/offline — the server just serves the ciphertext.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | Flask app: `GET /` reads `cipher.txt` at startup and renders a page showing the ciphertext plus a XOR/Base64 hint |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py` and `cipher.txt`, exposes port 8000, runs `python app.py` |
| `cipher.txt` | The Base64-encoded XOR-ciphertext served on the page |
| `flag.txt` | The plaintext flag (for reference; not served by the app) |
| `info.txt` | Korean challenge write-up: difficulty (Medium/중), hints, and a full Python brute-force snippet (`base64.b64decode` + XOR loop over 256 keys) |
| `.upload-include` | Files bundled for distribution to trainees |

## For AI Agents

### Working In This Directory
**Single-byte XOR is intentionally weak and trivially brute-forceable (256 keys)** — that weakness is the entire challenge. Do not switch to a stronger cipher or multi-byte key, or add server-side protections, unless explicitly asked.

### Testing Requirements
```bash
cd CRYPTOLAB-XOR
docker build -t crypto-xor .
docker run -p 8000:8000 crypto-xor
```
Verify the solve script in `info.txt` (Base64-decode `cipher.txt`, XOR against keys 0–255, look for `FLAG{`) recovers a plaintext matching `flag.txt`.

### Common Patterns
- Single-file Flask app, ciphertext loaded from a sibling text file (`cipher.txt`) rather than hardcoded, listens on `0.0.0.0:8000`.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
