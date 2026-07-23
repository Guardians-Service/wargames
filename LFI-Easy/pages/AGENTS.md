<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# pages

## Purpose
Static HTML fragments served by `LFI-Easy/app.py`'s `?page=` router under normal (non-exploit) use. These are the "legitimate" pages a player sees before attempting the LFI traversal.

## Key Files
| File | Description |
|------|--------------|
| `home.html` | Default page (`?page=home`): `<h2>Welcome to the Home Page</h2>` |
| `about.html` | Alternate page (`?page=about`): `<h2>This is the About Page</h2>` |

## For AI Agents

### Working In This Directory
Part of the **LFI-Easy** deliberately vulnerable lab (see [../AGENTS.md](../AGENTS.md)). These files are just content served by the vulnerable route — the vulnerability itself lives in `app.py`, not here. Don't add files here that would change the intended traversal depth needed to reach `flag.txt` (currently one level up: `../flag.txt`).

### Testing Requirements
No standalone tests; verified indirectly by loading `LFI-Easy` (see parent AGENTS.md).

### Common Patterns
Minimal static HTML snippets, no styling, no scripts.

## Dependencies

### Internal
Consumed only by `LFI-Easy/app.py`.

### External
None.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
