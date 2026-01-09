# GEMINI.md

## Communication
- Respond in Japanese
- Explain in a way that is easy for non-engineers to understand
- Add brief explanations when using technical terms
- Briefly explain the reason ("why") for each change

## Workflow
- Prioritize security above all else
- Propose options as needed and explain briefly
- Explain what you will do before taking action, and proceed only after my approval
- When possible, show demo pages or previews as we progress
- Do not proceed based on assumptions; ask questions if anything is unclear
- Break down complex tasks and confirm each step
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
