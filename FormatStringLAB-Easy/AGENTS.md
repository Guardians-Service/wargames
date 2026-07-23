<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# FormatStringLAB-Easy

## Purpose
A C program compiled without stack protection and served as a raw TCP service (via `socat`, not HTTP) that reads a line of user input and passes it directly to `printf(buf)` instead of `printf("%s", buf)`. This is a classic format-string vulnerability: the flag is loaded into a global buffer and passed to the vulnerable function's stack frame, and the trainee uses `%x`/`%s`-style format specifiers to leak stack memory (including the flag) back over the socket.

## Key Files
| File | Description |
|------|--------------|
| `vulnerable.c` | The vulnerable C program: reads `flag.txt` into a global `char flag[100]`, calls `vuln(flag)` which `fgets`s user input into a 256-byte stack buffer and passes it unsanitized to `printf(buf)` |
| `Dockerfile` | `debian:bookworm-slim`; installs `gcc`, `libc6-dev`, `socat`; compiles `vulnerable.c` with `-no-pie -fno-stack-protector` (intentionally disabling ASLR-of-binary and stack canaries) into `./vuln`; `flag.txt` made read-only; exposes port 8000; runs `start.sh` |
| `start.sh` | `socat TCP-LISTEN:8000,reuseaddr,fork EXEC:./vuln` — spawns a fresh `./vuln` process per TCP connection |
| `flag.txt` | The challenge flag, loaded into the vulnerable binary's memory at startup |
| `info.txt` | Korean challenge write-up: goal, difficulty (Easy), and example `nc`-based format-string probing (`%x.%x.%x...`, `%N$s`) |
| `.upload-include` | Files bundled for distribution to trainees (does not include `flag.txt`) |

## For AI Agents

### Working In This Directory
**The `printf(buf)` call (instead of `printf("%s", buf)`), and the `-no-pie -fno-stack-protector` compile flags, are all intentional** — together they make the format-string leak reliable and exploitable. Do not "fix" the format string, re-enable stack protection/PIE, or otherwise harden this binary unless explicitly asked; doing so defeats the lab. This is the only non-Python/PHP/web lab in the collection — it is a raw binary exposed over a TCP socket via `socat`, not an HTTP service.

### Testing Requirements
```bash
cd FormatStringLAB-Easy
docker build -t formatstring-easy .
docker run -p 8000:8000 formatstring-easy
```
Verify the leak still works, e.g.:
```bash
for i in $(seq 1 20); do printf '%%%d$s\n' "$i" | nc localhost 8000; done
```
looking for output containing `FLAG{`.

### Common Patterns
- Minimal, single-source-file C program; compiled with debug-hostile-but-exploit-friendly flags on purpose.
- Networking is handled entirely by `socat` wrapping the compiled binary (`EXEC:./vuln`) rather than any in-program socket code — the C program itself just does stdin/stdout I/O.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `debian:bookworm-slim`; `apt` packages `gcc`, `libc6-dev`, `socat`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
