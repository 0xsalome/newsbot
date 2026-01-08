# Handoff Document for Gemini

## Current Status

### Completed
- Basic RSS fetching, tagging, scoring, and Discord posting is operational
- Japanese translation via DeepL API
- GitHub Actions auto-execution (daily at UTC 0:00)
- 7 categories (bigtech, devcommunity, ai, science, education, mycotech, curiosity)

### Current File Structure
```
newsbot/
├── .github/workflows/daily-curate.yml
├── config.py          # RSS/tag/scoring settings
├── curate.py          # Main script (all features in one file)
├── state.json         # State management
├── requirements.txt   # feedparser, requests only
├── CLAUDE.md
├── GEMINI.md
└── README.md
```

---

## Implementation Specs (v2.0)

### 1. Category Configuration (7 categories)

| Category | Posts/Day | Scoring |
|----------|-----------|---------|
| **bigtech** | 2 | structural 30% + timeliness 70% |
| **devcommunity** | 2 | structural 30% + timeliness 70% |
| **ai** | 4 | structural-focused 2 (80/20) + timeliness-focused 2 (20/80) |
| **science** | 2 | structural-focused 1 (70/30) + timeliness-focused 1 (30/70) |
| **education** | 2 | structural-focused 1 (70/30) + timeliness-focused 1 (30/70) |
| **mycotech** | 2 | structural-focused 1 (70/30) + timeliness-focused 1 (30/70) |
| **curiosity** | 2 | structural-focused 1 (70/30) + timeliness-focused 1 (30/70) |

### 2. Dual Selection System

**Big Tech / Dev Community:**
```python
# Select 2 articles based on timeliness only
final_score = structural_score * 0.3 + timeliness_score * 0.7
```

**AI (4 articles):**
```python
# First, select 2 with structural focus
structural_score = structural * 0.8 + timeliness * 0.2
top_2_structural = select_top(2)

# Then, select 2 from remaining with timeliness focus
timeliness_score = structural * 0.2 + timeliness * 0.8
top_2_trending = select_top(2, exclude=top_2_structural)
```

**Other 4 categories (2 articles each):**
```python
# 1 with structural focus
structural_score = structural * 0.7 + timeliness * 0.3
top_1_structural = select_top(1)

# 1 from remaining with timeliness focus
timeliness_score = structural * 0.3 + timeliness * 0.7
top_1_trending = select_top(1, exclude=top_1_structural)
```

---

## 3. Complete RSS Source List

### Big Tech
```python
"bigtech": [
    # Global tech media
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://arstechnica.com/feed/",
    # China tech (English)
    "https://www.scmp.com/rss/91/feed",
    "https://kr-asia.com/feed",
    "https://technode.com/feed/",
    "https://pandaily.com/feed/",
    # Trends
    "https://news.ycombinator.com/rss",
    "https://www.producthunt.com/feed",
]
```

### Dev Community
```python
"devcommunity": [
    # GitHub
    "https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml",
    "https://mshibanami.github.io/GitHubTrendingRSS/weekly/all.xml",
    # Discussion platforms
    "https://news.ycombinator.com/rss",
    "https://lobste.rs/rss",
    "https://www.reddit.com/r/programming/.rss",
    "https://www.reddit.com/r/compsci/.rss",
    "https://www.reddit.com/r/webdev/.rss",
    "https://www.reddit.com/r/devops/.rss",
    # Developer blogs
    "https://dev.to/feed",
    # Practical knowledge
    "https://www.indiehackers.com/feed",
    "https://increment.com/feed.xml",
    # Japanese
    "https://qiita.com/popular-items/feed",
    "https://zenn.dev/feed",
]
```

### AI
```python
"ai": [
    # Research to implementation
    "https://paperswithcode.com/feed.atom",
    "https://export.arxiv.org/rss/cs.AI",
    "https://export.arxiv.org/rss/cs.LG",
    # AI news
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://venturebeat.com/category/ai/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    # AI ethics & social impact
    "https://www.aisnakeoil.com/feed",
    "https://www.anthropocenemagazine.org/feed/",
    # Community
    "https://www.reddit.com/r/MachineLearning/.rss",
    "https://www.reddit.com/r/artificial/.rss",
    "https://news.ycombinator.com/rss",
]
```

### Science
```python
"science": [
    # Deep science
    "https://www.sciencedaily.com/rss/all.xml",
    "https://phys.org/rss-feed/",
    "https://www.quantamagazine.org/feed/",
    "https://nautil.us/feed/",
    "https://www.earth.com/feed/",
    # Science news
    "https://feeds.arstechnica.com/arstechnica/science",
    "https://theconversation.com/articles.atom",
    # Community
    "https://www.reddit.com/r/science/.rss",
    "https://news.ycombinator.com/rss",
]
```

### Education
```python
"education": [
    # Education practice
    "https://www.edsurge.com/news.rss",
    "https://edsource.org/feed",
    "https://hechingerreport.org/feed/",
    "https://blog.khanacademy.org/feed/",
    # Educational resources
    "https://www.openculture.com/feed",
    "https://news.mit.edu/rss/topic/education",
    "https://theconversation.com/articles.atom",
    # Education trends
    "https://www.reddit.com/r/education/.rss",
    "https://news.ycombinator.com/rss",
]
```

### Mycotech
```python
"mycotech": [
    # Biology research
    "https://phys.org/rss-feed/biology-news/",
    "https://www.sciencedaily.com/rss/plants_animals.xml",
    "https://journals.plos.org/plosbiology/feed/atom",
    "https://www.earth.com/feed/",
    # Environment x Technology
    "https://www.anthropocenemagazine.org/feed/",
    "https://grist.org/feed/",
    "https://therevelator.org/feed/",
    # Community
    "https://www.reddit.com/r/biology/.rss",
]
```

### Curiosity
```python
"curiosity": [
    # Unusual & deep-dive
    "https://www.atlasobscura.com/feeds/latest",
    "https://www.bbc.com/future/feed.rss",
    "https://aeon.co/feed.rss",
    "https://nautil.us/feed/",
    "https://www.quantamagazine.org/feed/",
    # Art x Science
    "https://www.thisiscolossal.com/feed/",
    "https://www.creativeapplications.net/feed/",
    # Design & Culture
    "https://www.wired.com/feed/category/design/latest/rss",
    "https://www.smithsonianmag.com/rss/latest_articles/",
    # Trends
    "https://www.producthunt.com/feed",
    "https://www.reddit.com/r/interestingasfuck/.rss",
]
```

---

## 4. Source Reliability (SOURCE_WEIGHT)

```python
SOURCE_WEIGHT = {
    # Highest quality (academic/research)
    "arxiv.org": 5,
    "quantamagazine.org": 5,
    "paperswithcode.com": 5,

    # High quality science media
    "sciencedaily.com": 4,
    "phys.org": 3,
    "eurekalert.org": 4,
    "earth.com": 4,
    "nautil.us": 4,

    # Tech media (major)
    "techcrunch.com": 4,
    "theverge.com": 3,
    "wired.com": 4,
    "arstechnica.com": 4,
    "technologyreview.com": 5,

    # Tech media (mid-tier)
    "venturebeat.com": 3,
    "engadget.com": 2,
    "mashable.com": 2,

    # China tech
    "scmp.com": 3,
    "kr-asia.com": 3,
    "technode.com": 3,
    "pandaily.com": 3,

    # General media
    "bbc.com": 4,
    "smithsonianmag.com": 4,

    # Community
    "news.ycombinator.com": 3,
    "lobste.rs": 4,
    "reddit.com": 2,
    "producthunt.com": 2,

    # Developer platforms
    "dev.to": 2,
    "hashnode.com": 2,
    "qiita.com": 2,
    "zenn.dev": 2,
    "github.com": 3,

    # Culture & Education
    "aeon.co": 4,
    "atlasobscura.com": 3,
    "openculture.com": 3,
    "edsurge.com": 3,
    "edsource.org": 3,
    "hechingerreport.org": 3,

    # Environment
    "anthropocenemagazine.org": 4,
    "grist.org": 3,
    "therevelator.org": 3,

    # Default
    "default": 1
}
```

---

## 5. Discord Post Format

```
{emoji} **{category_name}** | {date}

**[{tags}]**
{title_ja}

{url}
{source} | Score: {final_score}
```

---

## 6. GitHub Secrets

Existing:
- DISCORD_WEBHOOK_SCIENCE
- DISCORD_WEBHOOK_AI
- DISCORD_WEBHOOK_EDUCATION
- DISCORD_WEBHOOK_MYCOTECH
- DISCORD_WEBHOOK_CURIOSITY
- DEEPL_API_KEY

Added:
- DISCORD_WEBHOOK_BIGTECH
- DISCORD_WEBHOOK_DEVCOMMUNITY

---

## 7. GitHub Actions

`.github/workflows/daily-curate.yml` includes:
```yaml
DISCORD_WEBHOOK_BIGTECH: ${{ secrets.DISCORD_WEBHOOK_BIGTECH }}
DISCORD_WEBHOOK_DEVCOMMUNITY: ${{ secrets.DISCORD_WEBHOOK_DEVCOMMUNITY }}
```

---

## Important Notes

1. **Security**: Never write webhook URLs in code (use GitHub Secrets)
2. **Free operation**: No LLM, stay within DeepL free tier (500k chars/month)
3. **RSS etiquette**: Set User-Agent, 1 second interval
4. **Testing**: Always run `python curate.py --dry-run` before production

---

## Implementation Priority

1. Add categories and RSS sources to config.py
2. Implement dual selection logic in curate.py
3. Add new webhook environment variables to GitHub Actions
4. Add new categories to state.json
5. Test with dry-run
6. Deploy to production
