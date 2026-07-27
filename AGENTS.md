<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# Guardians-wargames (GitHub remote rename pending)

## Purpose
This is the **Guardians Wargames** repository (an independent git repo nested inside the larger `guardians-service` workspace). The folder/repo name `Guaridnas-wargames` was an unintentional typo of `Guardians-wargames`; the local folder has been corrected, but the GitHub remote has not yet — see "Working In This Directory" below for current status. It is a collection of ~15 self-contained, containerized CTF-style security training challenges ("wargames") built by the BeeGuardians team, plus a `kali` attacker/tooling container and a GitHub Actions CI/CD pipeline that builds each lab's Docker image, pushes it to Amazon Public ECR, and uploads a zipped copy of its distributable files to S3.

## Key Files
| File | Description |
|------|--------------|
| `README.md` | Korean-language repo overview: lab list, CI/CD pipeline explanation, how to run a lab via Docker, contribution steps |
| `.gitignore` | Ignores `.idea/`, `.DS_Store`, `.venv` |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| [.github/workflows/AGENTS.md](.github/workflows/AGENTS.md) | CI/CD workflow (`deploy.yaml`) that builds/pushes each changed lab's Docker image and uploads its `.upload-include` files to S3 |
| [BruteForceLAB-Easy/AGENTS.md](BruteForceLAB-Easy/AGENTS.md) | Flask login form vulnerable to password brute-forcing (no rate limiting) |
| [CRYPTOLAB-Caesar/AGENTS.md](CRYPTOLAB-Caesar/AGENTS.md) | Classic Caesar cipher decryption challenge |
| [CRYPTOLAB-XOR/AGENTS.md](CRYPTOLAB-XOR/AGENTS.md) | Base64 + single-byte XOR cipher decryption challenge |
| [FileUpload-Webshell/AGENTS.md](FileUpload-Webshell/AGENTS.md) | PHP file upload with no extension/content validation → webshell RCE |
| [FormatStringLAB-Easy/AGENTS.md](FormatStringLAB-Easy/AGENTS.md) | C program with `printf(buf)` format-string vulnerability, served over a raw TCP socket via `socat` |
| [kali/AGENTS.md](kali/AGENTS.md) | Kali Linux attacker/tooling container (nmap, hydra, sqlmap, gdb, etc.) exposed via `ttyd` web terminal |
| [LFI-Easy/AGENTS.md](LFI-Easy/AGENTS.md) | Flask app with unsanitized `?page=` parameter → local file inclusion / path traversal |
| [RCELAB-Easy/AGENTS.md](RCELAB-Easy/AGENTS.md) | Flask app that shells out to `ping` with unsanitized input → OS command injection |
| [RSA-High/AGENTS.md](RSA-High/AGENTS.md) | Weak RSA parameters (small `e=3`, no padding) vulnerable to a cube-root / low-exponent attack |
| [SQLI-Easy/AGENTS.md](SQLI-Easy/AGENTS.md) | Login form with string-concatenated SQL query → classic SQL injection auth bypass |
| [SQLI-Medium/AGENTS.md](SQLI-Medium/AGENTS.md) | `?id=` numeric parameter concatenated into SQL query → UNION-based SQL injection, sqlmap-friendly |
| [SSTILAB-Medium/AGENTS.md](SSTILAB-Medium/AGENTS.md) | Flask `render_template_string` with unsanitized user input → server-side template injection (Jinja2 RCE) |
| [STEGANO-Easy/AGENTS.md](STEGANO-Easy/AGENTS.md) | PNG image with a flag hidden in trailing bytes → steganography / file-forensics challenge |
| [XSSLAB-Cookie/AGENTS.md](XSSLAB-Cookie/AGENTS.md) | Reflected XSS used to steal a `FLAG` cookie via `document.cookie` |
| [XSSLAB-Easy/AGENTS.md](XSSLAB-Easy/AGENTS.md) | Reflected XSS that pops a JS global `flag` variable via `alert()` |
| [XSSLAB-Medium/AGENTS.md](XSSLAB-Medium/AGENTS.md) | Reflected XSS used to `fetch()` a same-origin `/flag` JSON API and exfiltrate the result |

## For AI Agents

### Working In This Directory
**Repo rename partially complete:** the correct name is `Guardians-wargames` (not `Guaridnas`). Status: the local folder has been renamed to `Guardians-wargames`, but the GitHub remote (`github.com/BeeGuardians/Guaridnas-wargames`) still has the old typo'd name and needs renaming (via `gh repo rename` or the GitHub web UI, then update this repo's `origin` remote URL). Once the GitHub-side rename lands, update this note (see `../AGENTS.md`).

**This entire repository is a deliberately vulnerable security-training platform.** Every lab under this directory contains an intentional vulnerability (SQL injection, XSS, RCE, LFI, format-string bugs, weak crypto, insecure file upload, brute-forceable auth, etc.) that is the entire point of the challenge. **Never "fix," sanitize, patch, or harden these vulnerabilities** — doing so breaks the lab. Only make changes that are explicitly requested (e.g., adjusting difficulty, fixing an unrelated build/deploy bug, updating the flag, improving the CI pipeline). If a change is ambiguous about whether it would remove the intended vulnerability, ask before proceeding or leave the vulnerable code path untouched.

Each lab directory is fully independent — it has its own `Dockerfile`, source files, `flag.txt`, `info.txt` (Korean-language challenge write-up shown to players), and `.upload-include` (list of files bundled into the distributable ZIP uploaded to S3; secrets like `flag.txt` inside a container image are fine, but avoid ever adding `flag.txt` to `.upload-include` for a solved lab).

### Testing Requirements
Each lab builds and runs standalone via its own `Dockerfile` (all labs listen internally on port 8000):
```bash
cd <LabName>
docker build -t <lab-name> .
docker run -p 8000:8000 <lab-name>
```
There is no repo-wide test suite or linter; verification is "does the container build and does the intended exploit path work against it."

### Common Patterns
- Most labs are single-file Flask (`app.py`) apps on `python:3.11-slim` or `python:3.9-slim`, listening on `0.0.0.0:8000`, with inline HTML/CSS returned as f-strings.
- Each lab ships `flag.txt` (the challenge secret) and `info.txt` (a Korean write-up with hints/example solve commands shown to trainees) — treat these as content, not code to refactor.
- `.upload-include` lists exactly which files get zipped and uploaded to S3 by CI; it typically excludes `flag.txt`.
- Difficulty is encoded in directory names (`-Easy`, `-Medium`, `-High`) and mirrored in each `info.txt`'s "난이도" (difficulty) field.

## Dependencies

### Internal
- The CI pipeline in `.github/workflows/deploy.yaml` depends on every lab directory having a `Dockerfile` and a `.upload-include` file at its root.
- `kali/` is a standalone attacker toolbox container, not built by or dependent on the other labs.

### External
- Base images: `python:3.11-slim`, `python:3.9-slim`, `php:8.2-apache`, `debian:bookworm-slim`, `kalilinux/kali-rolling`.
- Deploy target: Amazon Public ECR (`public.ecr.aws/i7t0x0a1/gaurdians/wargames:<dir-name>`) and S3 bucket `s3-guardians-dev/wargame_zips/`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
