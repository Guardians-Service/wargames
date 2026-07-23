<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-07-23 | Updated: 2026-07-23 -->

# workflows

## Purpose
GitHub Actions workflow(s) that automate building and distributing the wargame labs whenever changes are pushed.

## Key Files
| File | Description |
|------|--------------|
| `deploy.yaml` | "Deploy CTF Problems" workflow. On push, diffs changed top-level folders against the commit-message's comma-separated folder list (lines after the first), then for each matched folder: builds its `Dockerfile` and pushes to `public.ecr.aws/i7t0x0a1/gaurdians/wargames:<folder>`, and zips the files listed in that folder's `.upload-include` and uploads to `s3://s3-guardians-dev/wargame_zips/<folder>.zip` |

## For AI Agents

### Working In This Directory
This workflow drives deployment of the intentionally-vulnerable labs (see the repo-root [AGENTS.md](../../AGENTS.md)) — the vulnerabilities in the labs themselves are out of scope here; only touch this file for CI/CD logic changes (trigger conditions, build/push steps, secrets, S3/ECR targets). The deploy step only runs for a folder if it appears in **both** the git diff and the second-line-onward comma-separated list in the triggering commit message — that's the intentional (if unusual) publish-gating mechanism; don't "simplify" it away without checking with the user, since it's how maintainers avoid rebuilding every lab on every push.

### Testing Requirements
No local test harness — this is a `push`-triggered GitHub Actions workflow requiring `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` repo secrets. Validate syntax with `actionlint` or a YAML linter, and dry-run logic changes to the bash steps locally where possible.

### Common Patterns
- Two-job pipeline: `detect-changes` (bash + `jq`, computes an intersection of changed and commit-message-mentioned folders, emits a JSON array) → `deploy` (matrix job over that array, one ECR push + one S3 upload per folder).
- Uses `actions/checkout@v3` and `aws-actions/configure-aws-credentials@v2`; AWS region is hardcoded to `us-east-1`.

## Dependencies

### Internal
- Every top-level lab directory in this repo (currently on disk as `Guaridnas-wargames/`, pending rename to `Guardians-wargames/` — see repo-root AGENTS.md) must have a `Dockerfile` and a `.upload-include` file for this workflow to succeed against it.

### External
- Amazon Public ECR (`public.ecr.aws/i7t0x0a1/gaurdians/wargames`) and S3 bucket `s3-guardians-dev` (external AWS resources, not part of this repo).

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
