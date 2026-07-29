<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-29 | Updated: 2026-07-29 -->

# JWTLAB-Medium

## Purpose
A Flask app issuing HS256 JWTs (`PyJWT`) signed with a deliberately weak, dictionary-crackable secret. `/login` only ever issues `role: user` tokens; `/admin` requires a `role: admin` claim and returns the flag. There's no legitimate path to an admin token — the intended solve is cracking the weak signing secret offline (small wordlist/brute force against a captured token), then forging a `role: admin` token with the recovered secret.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | `POST /login` issues an HS256 JWT with `{"username": ..., "role": "user"}`, signed with a short/common secret. `GET /admin` decodes the presented token and returns the flag only if `role == "admin"` |
| `Dockerfile` | `python:3.11-slim`, installs `flask` + `pyjwt`, copies `app.py`/`flag.txt`, exposes port 8000, runs `python app.py` |
| `flag.txt` | The challenge flag, returned by `/admin` on a forged admin-role token |
| `info.txt` | Korean challenge write-up: goal (crack the weak JWT secret, forge an admin token), difficulty (중/Medium), hints that the secret is short/weak without revealing it |
| `.upload-include` | Files bundled for distribution: `app.py`, `Dockerfile` (excludes `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally vulnerable via a weak JWT signing secret** — do not strengthen the secret, add secret rotation, or switch to an asymmetric algorithm (RS256); any of those breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested. If the secret string itself ever needs to change, it must remain genuinely crackable by a short wordlist/brute force (a handful of common, short dictionary words) — don't "fix" it into something strong.

### Testing Requirements
```bash
cd JWTLAB-Medium
docker build -t jwtlab-medium .
docker run -p 8000:8000 jwtlab-medium
```
Verify the intended solve path still works: log in to get a `role: user` token, confirm `/admin` rejects it, crack the secret offline, forge a `role: admin` token with the same `PyJWT`/HS256 scheme, confirm `/admin` now returns the flag.

### Common Patterns
- Single-file Flask app (`app.py`), listens on `0.0.0.0:8000`.
- Weak secret is a private constant in `app.py`, not read from `flag.txt` or an env var — keep it that way so the crack target is fixed and reproducible per image build.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip packages `flask`, `pyjwt`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
