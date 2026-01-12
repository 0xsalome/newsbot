# Handoff Document for Gemini

## Current Status: v2.0 Implemented (2026-01-11)

### ✅ Completed
- **Dual Selection Logic Implemented**:
  - `ai`: Dual Enhanced (2 Structural + 2 Trending)
  - `science`, `education`, `mycotech`, `curiosity`: Dual (1 Structural + 1 Trending)
  - `bigtech`, `devcommunity`: Trending Only (2 articles)
- **Diversity Mechanisms**:
  - `ensure_source_diversity`: Limits articles from the same domain.
  - `ensure_tag_diversity`: Ensures structural selections have distinct tag sets.
- **Infrastructure**:
  - All 7 categories configured in `config.py`.
  - GitHub Actions updated with new Webhook secrets (`BIGTECH`, `DEVCOMMUNITY`).
  - `state.json` structure updated and auto-maintained.

---

## Operational Notes

### State Management
- **Automatic Cleanup**: `curate.py` automatically removes:
  - Posted articles older than 7 days.
  - Pending articles older than 3 days.
- **Manual Cleanup**: `clean_state.py` is available as a utility to filter out specific noisy domains (e.g., GitHub Trending proxies) from the pending list if needed.

### Scoring & Selection
- **Dual Mode**:
  - **Structural Score**: Based on tag intensity (transformation, boundary crossing, etc.).
  - **Timeliness Score**: Based on source reliability and freshness (<24h = +3).
- **Diversity**:
  - Source limit: Max 2 articles per domain per day (configurable).
  - Pending list: Keeps top 10 candidates for future selection.

---

## Next Steps (Maintenance Phase)

1. **Monitor Scoring**:
   - Check if the "Structural vs Trending" balance is appropriate in the Discord posts.
   - Adjust weights in `config.py` if needed.

2. **Source Expansion**:
   - Add more high-quality RSS feeds to underrepresented categories if detected.

3. **Error Handling**:
   - Watch GitHub Actions logs for potential RSS parsing errors or translation API limits.