<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# kali

## Purpose
Builds a Kali Linux container preloaded with common offensive-security tooling and exposes an interactive `bash` shell over the web via `ttyd`, so trainees can attack the other wargame labs from a browser without installing tools locally. This is the "attacker box," not a challenge with its own flag.

## Key Files
| File | Description |
|------|--------------|
| `Dockerfile` | `FROM kalilinux/kali-rolling`; installs recon/exploitation tools (nmap, netcat, hydra, john, sqlmap, nikto, whatweb, gdb, radare2, binwalk, tcpdump, dig/whois, python3); builds `ttyd` from source (pinned to listen on port 8000); `CMD` runs `ttyd --writable -p 8000 bash` |
| `.upload-include` | Lists `Dockerfile` as the only file bundled for distribution |

## For AI Agents

### Working In This Directory
This is infrastructure/tooling, not a vulnerable challenge app — there's no flag here and no vulnerability to preserve. Changes here are about keeping the attacker toolchain useful (adding/removing tools, fixing the `ttyd` build) rather than about lab design. Note `ttyd --writable` exposes a fully interactive root shell to whoever can reach port 8000 with no authentication — that is intentional for a training environment but would be a serious issue anywhere else; do not port this pattern into other labs without flagging it.

### Testing Requirements
```bash
cd kali
docker build -t kali-attacker .
docker run -p 8000:8000 kali-attacker
```
Then open `http://localhost:8000` in a browser to confirm the `ttyd` terminal loads and tools (e.g. `nmap -V`, `sqlmap --version`) run.

### Common Patterns
- Single multi-tool `apt-get install` layer followed by a from-source build of `ttyd` (cloned via `git`, built with `cmake`/`make`), then the git clone and build tree are removed to shrink the final image.

## Dependencies

### Internal
- None — used alongside the other lab containers on the same Docker network/host during training exercises, but has no build-time dependency on them.

### External
- Base image `kalilinux/kali-rolling`; upstream tool source `https://github.com/tsl0922/ttyd`; Kali/Debian `apt` package repositories.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
