<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# RSA-High

## Purpose
A Flask app ("Crypto Lab - Weak RSA Key") that serves a public RSA key (`public.pem`, low exponent `e = 3`) and a ciphertext (`ciphertext.txt`) produced by encrypting a very short, unpadded plaintext. Because the message is short relative to the modulus and no PKCS#1 padding is used, the flag can be recovered via a cube-root / low-exponent RSA attack (e.g., `RsaCtfTool --attack cube_root`).

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `GET /` renders a download page; `GET /public.pem` and `GET /ciphertext.txt` serve the two challenge files via `send_file` |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`public.pem`/`ciphertext.txt`, exposes port 8000, runs `python app.py` |
| `public.pem` | RSA public key with `e = 3` and a modulus small/weak enough for a cube-root attack |
| `ciphertext.txt` | Base64-encoded RSA ciphertext of the (short, unpadded) flag plaintext |
| `flag.txt` | The plaintext flag that was encrypted to produce `ciphertext.txt` (not served by the app; kept for reference/regeneration) |
| `info.txt` | Korean challenge write-up: goal (cube-root attack on `e=3` RSA), difficulty (상/High), `RsaCtfTool` setup + attack commands |
| `.upload-include` | Files bundled for distribution: `app.py`, `ciphertext.txt`, `Dockerfile`, `public.pme` — **note**: this entry has a typo (`public.pme` instead of `public.pem`), meaning the actual public key file may not be included in the distributable ZIP; this looks like a pre-existing bug, not something to silently "fix" as part of unrelated work |

## For AI Agents

### Working In This Directory
**This lab is intentionally cryptographically weak** — the low public exponent (`e = 3`) and lack of OAEP/PKCS#1 padding on a short plaintext are the entire point of the challenge (they enable a cube-root attack). Do not regenerate `public.pem`/`ciphertext.txt` with a larger exponent or add padding; doing so breaks the lab. The `.upload-include` typo (`public.pme`) is a separate, likely-unintentional bug — only fix it if explicitly asked, since correcting it changes what gets shipped to trainees.

### Testing Requirements
```bash
cd RSA-High
docker build -t rsa-high .
docker run -p 8000:8000 rsa-high
```
Verify the intended solve path still works (see `info.txt` for full `RsaCtfTool` setup):
```bash
curl -O http://localhost:8000/public.pem
curl -O http://localhost:8000/ciphertext.txt
base64 -d ciphertext.txt > ciphertext.raw
python3 -m RsaCtfTool.main --publickey public.pem --attack cube_root --decryptfile ciphertext.raw
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS, listens on `0.0.0.0:8000`, serves static crypto artifacts via `send_file`.
- Unlike most other labs, the vulnerability lives in the pre-generated crypto artifacts (`public.pem`/`ciphertext.txt`), not in application logic.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`.
- Solve tooling (not part of the app itself): `RsaCtfTool` or `SageMath`, referenced in `info.txt` and available in the `kali/` attacker container.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
