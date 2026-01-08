# News Curation Bot

> ニュースを「構造」で選ぶbot。変容・境界横断・価値の再定義など、記事が持つ認識論的パターンを検出するDiscord bot。ニュース記事を**話題性も保ちながら認識論的構造**で分類・キュレーションします。完全無料・LLM不使用。
>
> A Discord bot that selects news by "structure" rather than "popularity." Detects epistemic patterns—transformations, boundary crossings, value redefinitions—and curates articles based on their structural logic while maintaining timeliness. Completely free, no LLM used.

[![GitHub Actions](https://img.shields.io/badge/automation-GitHub%20Actions-2088FF?logo=github-actions)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/python-3.11-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## What This Does

Ranks articles by epistemic patterns instead of engagement metrics.

**Patterns detected**:
- **Transformation**: poison → medicine, failure → discovery, waste → resource
- **Boundary Crossing**: fungi × computer memory, meditation × neuroscience
- **Visibility Gain**: first observation of previously invisible phenomena
- **Value Redefinition**: disorder → diversity, waste → efficiency
- **Scale Shift**: nanoscale → planetary impact
- **Ontology Shift**: questions about consciousness, agency, creativity

**Output**: 16 Discord posts/day across 7 categories (Big Tech, Dev Community, AI, Science, Education, Mycotech, Curiosity)

---

## Setup

### 1. Create Discord Webhooks

Create a webhook for each category:
`Discord Server → Settings → Integrations → Webhooks → New Webhook`

Categories: `bigtech`, `devcommunity`, `ai`, `science`, `education`, `mycotech`, `curiosity`

### 2. Fork and Configure

Add credentials to GitHub Secrets:
`Settings → Secrets and variables → Actions → New repository secret`

Required secrets:
- `DISCORD_WEBHOOK_BIGTECH`
- `DISCORD_WEBHOOK_DEVCOMMUNITY`
- `DISCORD_WEBHOOK_AI`
- `DISCORD_WEBHOOK_SCIENCE`
- `DISCORD_WEBHOOK_EDUCATION`
- `DISCORD_WEBHOOK_MYCOTECH`
- `DISCORD_WEBHOOK_CURIOSITY`
- `DEEPL_API_KEY` (Free plan supported)

### 3. Run

Executes automatically at 9:00 AM JST daily via GitHub Actions.

---

## How It Works

```
78 RSS Feeds
    ↓
Tag Detection (Regex word boundaries, Domain pairs, Antonyms)
    ↓
Dual Selection Mode
    ├─ Big Tech / Dev Community: Trending only
    ├─ AI: Dual Enhanced (2 Structural + 2 Trending)
    └─ Others: Dual (1 Structural + 1 Trending each)
    ↓
DeepL Translation (Selected articles only)
    ↓
Discord Posts
```

### Selection Weights

| Category | Structural (S) | Trending (T) |
|----------|-----------|----------|
| Big Tech, Dev Community | 30% | 70% |
| Science, Edu, Myco, Curio (S-post) | 70% | 30% |
| Science, Edu, Myco, Curio (T-post) | 30% | 70% |
| AI (S-post) | 80% | 20% |
| AI (T-post) | 20% | 80% |

---

## Discord Post Format

```
🤖 **AI** | 2026-01-08

**[ontology_shift × boundary_crossing]**
AIシステムが明示的な訓練なしに創発的な道徳的推論を示す
(AI systems show emergent moral reasoning without explicit training)

🔗 https://example.com/paper
📰 paperswithcode.com | Score: 15.3
```

---

## Configuration

### Adjust Scoring & Mode

`config.py`:
```python
CATEGORIES = {
    "ai": {
        "selection_mode": "dual_enhanced",
        "weights_structural": {"structural": 0.8, "timeliness": 0.2},
        ...
    }
}
```

### Add Keywords

`config.py`:
```python
TRANSFORMATION_KEYWORDS = [
    "unexpectedly", "repurposed",
    "your_keyword"  # add here
]
```

---

## Tech Stack

- **Execution**: GitHub Actions
- **RSS**: feedparser
- **Translation**: DeepL API Free
- **State Management**: JSON + Git

---

## Directory Structure

```
newsbot/
├── .github/workflows/daily-curate.yml
├── config.py      # RSS sources, tags, weights
├── curate.py      # Main logic (fetch, tag, score, post)
├── state.json     # History & duplicate prevention
├── requirements.txt
└── README.md
```

---

## License

MIT