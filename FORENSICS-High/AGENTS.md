<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-30 -->

# FORENSICS-High

## Purpose
A Flask app ("Forensics Lab - Layered Evidence (High)") serving a single static file, `evidence.bin`, whose real format is deliberately mismatched with its extension. The flag is encoded through four layers — hex → single-byte XOR → base64 → gzip — and the player must peel each one off in reverse to recover it. No live exploitation is involved; this is a pure file-analysis/decode-chain challenge, matching the static-file pattern of `RSA-High`/`STEGANO-Easy` rather than the app-vulnerability pattern of most other labs.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /` renders a description page with a download link; `GET /evidence.bin` serves the pre-generated `evidence.bin` via `send_file` |
| `evidence.bin` | `gzip.compress(base64.b64encode(bytes(b ^ key for b in flag.hex().encode())))` for a fixed single-byte `key` — i.e. gunzip → base64-decode → XOR-bruteforce (256 keys) → hex-decode recovers the flag |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`evidence.bin`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag in plaintext — kept for reference/verification only; the actual encoded flag lives inside `evidence.bin`, not read by `app.py` at runtime |
| `info.txt` | Korean challenge write-up: goal (peel 4 encoding layers), difficulty (상/High), a full Python decode script (gunzip → b64-decode → XOR-bruteforce → hex-decode) |
| `.upload-include` | Files bundled for distribution: `app.py`, `evidence.bin` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This is an encoding puzzle, not a running-app vulnerability** — `app.py` never reads `flag.txt`; regenerating `evidence.bin` requires re-deriving it from the flag text with the exact encode order (hex → XOR → base64 → gzip) and updating `flag.txt` to match. If you ever need to regenerate `evidence.bin` (e.g., changing the flag), use this encode script and keep `flag.txt` in sync:
```python
import base64, gzip
flag = b"FLAG{...}"
hex_str = flag.hex().encode()
key = <single byte 0-255>
xored = bytes(b ^ key for b in hex_str)
open("evidence.bin", "wb").write(gzip.compress(base64.b64encode(xored)))
```
Do not add more layers, remove the XOR-bruteforce step (e.g. by hardcoding a "hint" that reveals `key` directly in `info.txt`), or otherwise make the puzzle materially easier without being asked.

### Testing Requirements
```bash
cd FORENSICS-High
docker build -t forensics-high .
docker run -p 8000:8000 forensics-high
```
Verify the intended decode path still recovers the exact `flag.txt` contents:
```python
import gzip, base64
data = open("evidence.bin", "rb").read()  # or fetch via curl http://localhost:8000/evidence.bin
decoded = base64.b64decode(gzip.decompress(data))
for k in range(256):
    cand = bytes(b ^ k for b in decoded)
    try:
        result = bytes.fromhex(cand.decode("ascii"))
    except (ValueError, UnicodeDecodeError):
        continue
    if result.startswith(b"FLAG{"):
        print(k, result)
        break
```

### Common Patterns
- Single-file Flask app (`app.py`) purely for description + file download, listens on `0.0.0.0:8000` — same shape as `RSA-High`/`STEGANO-Easy`.
- Reuses the single-byte-XOR + brute-force-256-keys technique already taught in `CRYPTOLAB-XOR`, layered with gzip/base64/hex on top for a harder, multi-step version.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`; stdlib `gzip`, `base64`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
