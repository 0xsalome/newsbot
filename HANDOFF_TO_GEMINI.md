# Gemini への引き継ぎ文書

## 現在の状態

### 完了済み
- 基本的なRSS取得・タグ付け・スコアリング・Discord投稿が動作中
- DeepL APIによる日本語翻訳機能
- GitHub Actions自動実行（毎日UTC 0:00）
- 5カテゴリ（science, ai, education, mycotech, curiosity）

### 現在のファイル構成
```
newsbot/
├── .github/workflows/daily-curate.yml
├── config.py          # RSS/タグ/スコア設定
├── curate.py          # メインスクリプト（全機能が1ファイル）
├── state.json         # 状態管理
├── requirements.txt   # feedparser, requests のみ
├── CLAUDE.md
├── GEMINI.md
└── README.md
```

---

## 実装してほしいこと（v2.0）

### 1. カテゴリを5→7に拡張

| カテゴリ | 投稿数 | スコアリング |
|---------|--------|-------------|
| **bigtech** (新規) | 2 | 構造30% + 話題70% |
| **devcommunity** (新規) | 2 | 構造30% + 話題70% |
| **ai** | 4 | 構造重視2件(80/20) + 話題重視2件(20/80) |
| **science** | 2 | 構造重視1件(70/30) + 話題重視1件(30/70) |
| **education** | 2 | 構造重視1件(70/30) + 話題重視1件(30/70) |
| **mycotech** | 2 | 構造重視1件(70/30) + 話題重視1件(30/70) |
| **curiosity** | 2 | 構造重視1件(70/30) + 話題重視1件(30/70) |

### 2. 二刀流選択システム

**Big Tech / Dev Community:**
```python
# 話題性のみで2件選出
final_score = structural_score * 0.3 + timeliness_score * 0.7
```

**AI（4件選出）:**
```python
# まず構造重視で2件選出
structural_score = structural * 0.8 + timeliness * 0.2
top_2_structural = select_top(2)

# 残りから話題性重視で2件選出
timeliness_score = structural * 0.2 + timeliness * 0.8
top_2_trending = select_top(2, exclude=top_2_structural)
```

**他4カテゴリ（各2件選出）:**
```python
# 構造重視で1件
structural_score = structural * 0.7 + timeliness * 0.3
top_1_structural = select_top(1)

# 残りから話題性重視で1件
timeliness_score = structural * 0.3 + timeliness * 0.7
top_1_trending = select_top(1, exclude=top_1_structural)
```

---

## 3. 完全版RSSソースリスト

### 🏢 Big Tech（新規カテゴリ）
```python
"bigtech": [
    # グローバルテックメディア
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://arstechnica.com/feed/",
    "https://www.engadget.com/rss.xml",
    "https://mashable.com/feeds/rss/all",
    # 中国テック（英語版）
    "https://www.scmp.com/rss/91/feed",
    "https://kr-asia.com/feed",
    "https://technode.com/feed/",
    "https://pandaily.com/feed/",
    # トレンド
    "https://news.ycombinator.com/rss",
    "https://www.producthunt.com/feed",
]
```

### 💬 Dev Community（新規カテゴリ）
```python
"devcommunity": [
    # GitHub
    "https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml",
    "https://mshibanami.github.io/GitHubTrendingRSS/weekly/all.xml",
    # 議論プラットフォーム
    "https://news.ycombinator.com/rss",
    "https://lobste.rs/rss",
    "https://www.reddit.com/r/programming/.rss",
    "https://www.reddit.com/r/compsci/.rss",
    "https://www.reddit.com/r/webdev/.rss",
    "https://www.reddit.com/r/devops/.rss",
    # 開発者ブログ
    "https://dev.to/feed",
    "https://hashnode.com/rss",
    "https://daily.dev/blog/feed",
    # 実践知
    "https://www.indiehackers.com/feed",
    "https://increment.com/feed.xml",
    # 日本語
    "https://qiita.com/popular-items/feed",
    "https://zenn.dev/feed",
]
```

### 🤖 AI（既存カテゴリ、ソース拡張）
```python
"ai": [
    # 研究→実装
    "https://paperswithcode.com/feed.atom",
    "https://export.arxiv.org/rss/cs.AI",
    "https://export.arxiv.org/rss/cs.LG",
    # AI報道
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://venturebeat.com/category/ai/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    # AI倫理・社会影響
    "https://www.aisnakeoil.com/feed",
    "https://www.anthropocenemagazine.org/feed/",
    # コミュニティ
    "https://www.reddit.com/r/MachineLearning/.rss",
    "https://www.reddit.com/r/artificial/.rss",
    "https://news.ycombinator.com/rss",
]
```

### 🔬 Science（既存カテゴリ、ソース拡張）
```python
"science": [
    # 深掘り科学
    "https://www.sciencedaily.com/rss/all.xml",
    "https://phys.org/rss-feed/",
    "https://www.quantamagazine.org/feed/",
    "https://nautil.us/feed/",
    "https://www.earth.com/news/feed/",
    # プレスリリース
    "https://www.eurekalert.org/rss/news_releases.xml",
    # 科学報道
    "https://feeds.arstechnica.com/arstechnica/science",
    "https://theconversation.com/articles.atom",
    # コミュニティ
    "https://www.reddit.com/r/science/.rss",
    "https://news.ycombinator.com/rss",
]
```

### 📚 Education（既存カテゴリ、ソース拡張）
```python
"education": [
    # 教育実践
    "https://www.edsurge.com/news.rss",
    "https://edsource.org/feed",
    "https://hechingerreport.org/feed/",
    "https://blog.khanacademy.org/feed/",
    # 教育リソース
    "https://www.openculture.com/feed",
    "https://news.mit.edu/rss/topic/education",
    "https://theconversation.com/articles.atom",
    # 教育トレンド
    "https://www.reddit.com/r/education/.rss",
    "https://news.ycombinator.com/rss",
]
```

### 🍄 Mycotech（既存カテゴリ、ソース拡張）
```python
"mycotech": [
    # 生物学研究
    "https://phys.org/rss-feed/biology-news/",
    "https://www.sciencedaily.com/rss/plants_animals.xml",
    "https://journals.plos.org/plosbiology/feed/atom",
    "https://www.earth.com/news/feed/",
    # 環境×技術
    "https://www.anthropocenemagazine.org/feed/",
    "https://grist.org/feed/",
    "https://therevelator.org/feed/",
    # テックトレンド
    "https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml",
    "https://news.ycombinator.com/rss",
    "https://www.reddit.com/r/biology/.rss",
]
```

### 🌍 Curiosity（既存カテゴリ、ソース拡張）
```python
"curiosity": [
    # 珍奇・深掘り
    "https://www.atlasobscura.com/feeds/latest",
    "https://www.bbc.com/future/rss",
    "https://aeon.co/feed.rss",
    "https://nautil.us/feed/",
    "https://www.quantamagazine.org/feed/",
    # アート×科学
    "https://www.thisiscolossal.com/feed/",
    "https://www.creativeapplications.net/feed/",
    # デザイン・文化
    "https://www.wired.com/feed/category/design/latest/rss",
    "https://www.smithsonianmag.com/rss/latest_articles/",
    # トレンド
    "https://www.producthunt.com/feed",
    "https://www.reddit.com/r/interestingasfuck/.rss",
]
```

---

## 4. ソース信頼度（SOURCE_WEIGHT追加）

```python
SOURCE_WEIGHT = {
    # 最高品質（学術・研究）
    "arxiv.org": 5,
    "quantamagazine.org": 5,
    "paperswithcode.com": 5,

    # 高品質科学メディア
    "sciencedaily.com": 4,
    "phys.org": 3,
    "eurekalert.org": 4,
    "earth.com": 4,
    "nautil.us": 4,

    # テックメディア（大手）
    "techcrunch.com": 4,
    "theverge.com": 3,
    "wired.com": 4,
    "arstechnica.com": 4,
    "technologyreview.com": 5,

    # テックメディア（中堅）
    "venturebeat.com": 3,
    "engadget.com": 2,
    "mashable.com": 2,

    # 中国テック
    "scmp.com": 3,
    "kr-asia.com": 3,
    "technode.com": 3,
    "pandaily.com": 3,

    # 一般メディア
    "bbc.com": 4,
    "smithsonianmag.com": 4,

    # コミュニティ
    "news.ycombinator.com": 3,
    "lobste.rs": 4,
    "reddit.com": 2,
    "producthunt.com": 2,

    # 開発者プラットフォーム
    "dev.to": 2,
    "hashnode.com": 2,
    "qiita.com": 2,
    "zenn.dev": 2,
    "github.com": 3,

    # 文化・教育
    "aeon.co": 4,
    "atlasobscura.com": 3,
    "openculture.com": 3,
    "edsurge.com": 3,
    "edsource.org": 3,
    "hechingerreport.org": 3,

    # 環境
    "anthropocenemagazine.org": 4,
    "grist.org": 3,
    "therevelator.org": 3,

    # デフォルト
    "default": 1
}
```

---

## 5. カテゴリ定義（CATEGORIES更新）

```python
CATEGORIES = {
    "bigtech": {
        "name": "Big Tech",
        "emoji": "🏢",
        "posts_per_day": 2,
        "selection_mode": "trending_only",  # 話題性のみ
        "weights": {"structural": 0.3, "timeliness": 0.7}
    },
    "devcommunity": {
        "name": "Dev Community",
        "emoji": "💬",
        "posts_per_day": 2,
        "selection_mode": "trending_only",
        "weights": {"structural": 0.3, "timeliness": 0.7}
    },
    "ai": {
        "name": "AI",
        "emoji": "🤖",
        "posts_per_day": 4,
        "selection_mode": "dual_enhanced",  # 構造2 + 話題2
        "weights_structural": {"structural": 0.8, "timeliness": 0.2},
        "weights_trending": {"structural": 0.2, "timeliness": 0.8}
    },
    "science": {
        "name": "Science",
        "emoji": "🔬",
        "posts_per_day": 2,
        "selection_mode": "dual",  # 構造1 + 話題1
        "weights_structural": {"structural": 0.7, "timeliness": 0.3},
        "weights_trending": {"structural": 0.3, "timeliness": 0.7}
    },
    "education": {
        "name": "Education",
        "emoji": "📚",
        "posts_per_day": 2,
        "selection_mode": "dual",
        "weights_structural": {"structural": 0.7, "timeliness": 0.3},
        "weights_trending": {"structural": 0.3, "timeliness": 0.7}
    },
    "mycotech": {
        "name": "Mycotech",
        "emoji": "🍄",
        "posts_per_day": 2,
        "selection_mode": "dual",
        "weights_structural": {"structural": 0.7, "timeliness": 0.3},
        "weights_trending": {"structural": 0.3, "timeliness": 0.7}
    },
    "curiosity": {
        "name": "Curiosity",
        "emoji": "🌍",
        "posts_per_day": 2,
        "selection_mode": "dual",
        "weights_structural": {"structural": 0.7, "timeliness": 0.3},
        "weights_trending": {"structural": 0.3, "timeliness": 0.7}
    }
}
```

---

## 6. Discord投稿フォーマット（ラベル不要版）

```
{emoji} **{category_name}** | {date}

**[{tags}]**
{title_ja}

🔗 {url}
📰 {source} | Score: {final_score}
```

---

## 7. GitHub Secrets追加

既存:
- DISCORD_WEBHOOK_SCIENCE
- DISCORD_WEBHOOK_AI
- DISCORD_WEBHOOK_EDUCATION
- DISCORD_WEBHOOK_MYCOTECH
- DISCORD_WEBHOOK_CURIOSITY
- DEEPL_API_KEY

**新規追加:**
- DISCORD_WEBHOOK_BIGTECH
- DISCORD_WEBHOOK_DEVCOMMUNITY

---

## 8. GitHub Actions更新

`.github/workflows/daily-curate.yml` に追加:
```yaml
DISCORD_WEBHOOK_BIGTECH: ${{ secrets.DISCORD_WEBHOOK_BIGTECH }}
DISCORD_WEBHOOK_DEVCOMMUNITY: ${{ secrets.DISCORD_WEBHOOK_DEVCOMMUNITY }}
```

---

## 注意事項

1. **セキュリティ**: Webhook URLはコードに書かない（GitHub Secrets使用）
2. **無料運用**: LLM禁止、DeepL無料枠内（月50万文字）
3. **RSS礼儀**: User-Agent設定、1秒間隔
4. **テスト**: `python curate.py --dry-run` で確認してから本番

---

## 実装の優先順位

1. config.pyにカテゴリとRSSソース追加
2. curate.pyに二刀流選択ロジック実装
3. GitHub Actionsに新しいWebhook環境変数追加
4. state.jsonに新カテゴリ追加
5. dry-runでテスト
6. 本番デプロイ

---

## 参考：仕様書

ユーザーが作成した完全仕様書（タグ定義、キーワードリスト詳細）は会話履歴にあります。
