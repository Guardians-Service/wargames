<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# BruteForceLAB-Easy

## Purpose
A Flask-based login form ("Brute Force Lab") with no authentication protections (no rate limiting, no lockout, no CAPTCHA). The correct password is chosen at random at container startup from a 100-entry candidate list in `passwords.txt`; the username is fixed to `admin`. The goal is to brute-force the correct password via `/login` and retrieve the flag returned on success.

## Key Files
| File | Description |
|------|--------------|
| `app.py` | Flask app: `GET /` renders the login form; `POST /login` compares submitted `username`/`password` against `admin` + a randomly-chosen entry from `passwords.txt`, returning `flag.txt` contents on success or an "Unauthorized" page otherwise |
| `Dockerfile` | `python:3.11-slim`, installs Flask, copies `app.py`/`flag.txt`/`passwords.txt`, exposes port 8000, runs `python app.py` |
| `passwords.txt` | 100-line candidate password list; one random line is chosen as the correct password each run |
| `flag.txt` | The challenge flag, returned as `text/plain`-style content on successful login |
| `info.txt` | Korean challenge write-up: goal, difficulty (Easy), and example Hydra/`curl` brute-force commands |
| `.upload-include` | Files bundled for distribution to trainees (does not include `flag.txt`) |

## For AI Agents

### Working In This Directory
**This app is intentionally unprotected against brute-force login attempts** — that is the entire challenge. Do not add rate limiting, account lockout, CAPTCHA, delays, or other anti-brute-force protections; doing so breaks the lab. Only touch this code for unrelated fixes (e.g., Docker build issues) explicitly requested.

### Testing Requirements
```bash
cd BruteForceLAB-Easy
docker build -t bruteforce-easy .
docker run -p 8000:8000 bruteforce-easy
```
Verify the intended solve path still works, e.g.:
```bash
hydra -l admin -P passwords.txt <host> -s 8000 http-post-form "/login:username=^USER^&password=^PASS^:Unauthorized"
```

### Common Patterns
- Single-file Flask app (`app.py`), inline HTML/CSS returned as an f-string/triple-quoted string, listens on `0.0.0.0:8000`.
- Password is picked with `random.choice()` once at process start (module load time), so it is stable for the container's lifetime but changes on restart/redeploy.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `python:3.11-slim`; pip package `flask`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
