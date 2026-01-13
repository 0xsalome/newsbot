# GEMINI.md

## Communication Rules
- **Language:** Always respond in Japanese.
- Explain in a way that is easy for non-engineers to understand
- Add brief explanations when using technical terms
- Briefly explain the reason ("why") for each change

## Git Workflow

**Default Process:**
1. **Implementation (Gemini/Docker):** I handle all file editing, testing, `git add`, and `git commit`.
2. **Review (User or Claude):** You or Claude will review the generated code and commits for any issues.
3. **Approval & Push (User/Host):** Once the changes are approved, you will run `git push` from your host machine's terminal.

**Protocol:**
- After committing, I will request a review and push.
- I will not attempt to push from within the Docker environment.
- If revisions are needed during review, I will make the corrections within Docker.

**Reason:** Docker sandbox does not have GitHub authentication configured. The host machine has SSH keys configured for git@github.com.

## Security & Secrets

**Critical Rule: Never Expose Secrets**
- Never read, print, or expose any API keys, secrets, private keys, or credentials from .env files, config files, or environment variables. If asked to show them, refuse.

**Strict rules:**
- Never hardcode secrets (API keys, private keys, tokens, passwords) in code, tests, or logs.
- Assume secrets are supplied via:
  - environment variables,
  - secret managers (e.g. 1Password, cloud secrets),
  - local config files ignored by git.

**Do NOT:**
- read `.env` or similar files without explicit approval,
- print environment variables or full config contents into chat, logs, or comments.

**For destructive operations** (dropping data, wiping queues, etc.):
- always ask for explicit confirmation,
- document backup/rollback steps before proceeding.

## Prohibited Commands

Never execute:
- Disk operations: `dd`, `diskutil`, `mkfs`, `fdisk`, `parted`
- Root permission changes: `chmod -R /`, `chown -R /`
- Destructive deletion: `rm -rf /`
- Destructive git: `git reset --hard`, `git clean -fdx`, `git push --force`
- Docker cleanup: `docker system prune`

## Workflow

- Prioritize security above all else
- Propose options as needed and explain briefly
- Explain what you will do before taking action, and proceed only after my approval
- When possible, show demo pages or previews as we progress
- Do not proceed based on assumptions; ask questions if anything is unclear
- Break down complex tasks and confirm each step
- Always confirm with user before executing commands that modify or delete files
- Break large changes into smaller steps
- Confirm before adding external packages or making API calls
- If you seem to have forgotten previous instructions, confirm with me before continuing

## Safety Rules

- Do not directly touch production environments or production data
- Never commit or expose `.env` files or secrets
- Always confirm before deleting or overwriting files
- Break large changes into smaller steps and proceed incrementally
- Confirm with me before adding external packages
- Confirm with me before making API calls or sending data externally

## Project Information

- Project purpose: Automated news curation system based on structural similarity (learning over buzz / structure over engagement)
- Technologies used: Python / GitHub Actions / Discord Webhooks / feedparser / requests
- Main folder structure:
  - `.github/workflows/` - GitHub Actions configuration
  - `curate.py` - Main script
  - `config.py` - RSS/tags/scoring configuration
  - `state.json` - State storage (Git managed)
  - `requirements.txt` - Dependencies
- Files/folders not to touch:
  - `state.json` (managed by bot, manual editing prohibited)

## Development Commands

```bash
python curate.py           # Local execution (for testing)
python curate.py --dry-run # Check scoring without posting
```

## Environment Variables (GitHub Secrets)

```
DISCORD_WEBHOOK_SCIENCE
DISCORD_WEBHOOK_AI
DISCORD_WEBHOOK_EDUCATION
DISCORD_WEBHOOK_MYCOTECH
DISCORD_WEBHOOK_CURIOSITY
DEEPL_API_KEY          # DeepL API Free (for Japanese title translation)
```

## Implementation Phases

### Phase 1: MVP
- RSS fetching (single category)
- 2-tag detection (transformation, boundary_crossing)
- Simple scoring
- Discord posting
- state.json persistence

### Phase 2: Full Features
- 5 categories support
- Full 6-tag implementation
- Tag diversity check
- pending/posted management

### Phase 3: Optimization
- Score tuning
- Keyword dictionary expansion
- Error handling improvements

## Security Guidelines

- Webhooks must be managed via GitHub Secrets (no hardcoding)
- No sensitive data in state.json
- Minimize external API requests
- Set appropriate User-Agent (for bot identification)
- No sensitive data in error logs

## Free Operation Constraints

- **GitHub Actions**: Stay within 2,000 min/month free tier (5 min/day × 30 days = 150 min)
- **External APIs**: Free tier only, paid APIs prohibited
- **LLM**: Prohibited (cost reasons)
- **Storage**: state.json in repository only
- **Dependencies**: Keep minimal (feedparser, requests only)

## Skills

### Agent Memory
- Location: `.claude/skills/agent-memory/`
- Purpose: Persistent memory space for storing knowledge that survives across conversations
- Usage: Save research findings, codebase patterns, architectural decisions, and in-progress work
- See `.claude/skills/agent-memory/SKILL.md` for detailed instructions

## Notes

- Fully free, fully automated, no LLM
- RSS etiquette: User-Agent set, 1+ second between requests
- Discord Rate Limit: No issues (10 posts/day)
