<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-30 -->

# JWTLAB-High

## Purpose
A Flask app ("JWT Lab - High (kid Injection)") that issues HS256-signed JWTs carrying a `kid` (key id) header naming which key file under `keys/` was used to sign it. `/admin` re-derives the verification key by reading the unverified header's `kid` value and joining it onto `keys/` with no path sanitization, so a `kid` of `../app.py` escapes the `keys/` directory entirely and uses the app's own source file as the HMAC secret — a file the player already has, byte-for-byte, from the challenge's own distributable ZIP. The goal is to forge a `role: admin` token using that known key.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `/login` issues a token signed with `keys/default.key`, header `{"kid": "default.key"}`; `/admin` reads `jwt.get_unverified_header(token)["kid"]`, builds `key_path = os.path.normpath(os.path.join(KEYS_DIR, kid))` with no containment check, reads that file's bytes as the HMAC key, then calls `jwt.decode(token, key=verify_key, algorithms=["HS256"])` |
| `keys/default.key` | Container-only random 64-hex-char secret used for legitimate low-privilege tokens — **not** shipped to players (excluded from `.upload-include`) |
| `Dockerfile` | `python:3.11-slim`, installs `flask pyjwt`, copies `app.py`/`flag.txt`/`keys/`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, returned by `/admin` once a forged admin-role token is accepted |
| `info.txt` | Korean challenge write-up: goal (forge an admin token via `kid` path traversal), difficulty (상/High), a full Python/PyJWT example forging the token with `app.py`'s own bytes as the key |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` — deliberately includes `app.py` because the exploit itself depends on the player having byte-identical source to use as the forged signing key; excludes `flag.txt` and `keys/` |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable to JWT `kid`-header path traversal / key confusion.** The vulnerability is entirely in `/admin`'s unsanitized `os.path.join(KEYS_DIR, kid)` — do not add `os.path.basename(kid)`, an allow-list of known `kid` values, or `os.path.realpath` containment checks, any of which breaks the lab. Do not switch back to an "algorithm confusion" (RS256→HS256) design either — that was tried first and confirmed **not exploitable** against current PyJWT (both 2.x and even 1.7.1 raise `InvalidKeyError` when an RSA/PEM-shaped key is used as an HMAC secret, and `alg=none` requires `key=None` exactly, which this app never passes) — verified locally before landing on the `kid`-injection design actually shipped here. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd JWTLAB-High
docker build -t jwtlab-high .
docker run -p 8000:8000 jwtlab-high
```
Verify the intended solve path still works:
```python
import jwt
app_py_bytes = open("app.py", "rb").read()
forged = jwt.encode({"username": "attacker", "role": "admin"}, app_py_bytes, algorithm="HS256", headers={"kid": "../app.py"})
```
```bash
curl http://localhost:8000/admin -H "Authorization: Bearer <forged>"
```
Should return `{"flag": "FLAG{...}", ...}`. Also confirm a normal `/login`-issued user-role token still gets `403` from `/admin`.

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML f-string for `/`, listens on `0.0.0.0:8000`.
- Distinguishing feature vs. `JWTLAB-Medium` (weak/guessable HS256 secret, brute-forced offline): this lab's secret is strong and never brute-forceable — the bug is in key *selection* (path traversal via `kid`), not key *strength*.

## Dependencies

### Internal
None — fully self-contained (does not depend on any other lab directory), though the exploit does depend on `app.py` itself being part of the distributed `.upload-include` bundle.

### External
- Base image `python:3.11-slim`; pip packages `flask`, `pyjwt`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
