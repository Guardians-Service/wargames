<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# CRYPTOLAB-Caesar

## Purpose
A static, single-page Flask app that displays a Caesar-cipher-encrypted string (`IURG{fdhvdu_flskhu_lv_ixq}`, shift 3, decoding to `FLAG{caesar_cipher_is_fun}`) and challenges the trainee to decrypt it by hand or with a script. There is no server-side interaction beyond rendering the page — the "attack" happens entirely off-server.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | Flask app: `GET /` renders a page showing the hardcoded Caesar-ciphertext and a hint about the shift concept |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The plaintext flag (for reference/verification; not served by the app) |
| `info.txt` | Korean challenge write-up: ciphertext, difficulty (Easy), and shift-cipher hints |
| `.upload-include` | Files bundled for distribution to trainees |

## For AI Agents

### Working In This Directory
**The ciphertext is intentionally weak (classical Caesar cipher, trivially brute-forceable across 25 shifts)** — this is the entire point of the "Easy" crypto challenge. Do not strengthen the cipher, add server-side decryption protections, or otherwise change the crypto scheme unless explicitly asked.

### Testing Requirements
```bash
cd CRYPTOLAB-Caesar
docker build -t crypto-caesar .
docker run -p 8000:8000 crypto-caesar
```
Confirm the page at `http://localhost:8000/` displays the ciphertext, and that shifting it by -3 yields `FLAG{caesar_cipher_is_fun}` (matching `flag.txt`).

### Common Patterns
- Single-file Flask app, ciphertext hardcoded as a Python string constant in `app.py`, listens on `0.0.0.0:8000`.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
