"""
News Curation Bot - Configuration
セキュリティ: Webhook URLはここに書かない（GitHub Secretsで管理）
"""

# =============================================================================
# CATEGORY DEFINITIONS
# =============================================================================

CATEGORIES = {
    "bigtech": {
        "name": "Big Tech",
        "emoji": "🏢",
        "description": "グローバルテック、トレンド、ビジネス",
        "posts_per_day": 2,
        "selection_mode": "trending_only",  # 話題性のみ
        "weights": {"structural": 0.3, "timeliness": 0.7}
    },
    "devcommunity": {
        "name": "Dev Community",
        "emoji": "💬",
        "description": "開発者議論、トレンド、実践知",
        "posts_per_day": 2,
        "selection_mode": "trending_only",
        "weights": {"structural": 0.3, "timeliness": 0.7}
    },
    "ai": {
        "name": "AI",
        "emoji": "🤖",
        "description": "境界侵犯、人間観の揺らぎ",
        "posts_per_day": 4,
        "selection_mode": "dual_enhanced",  # 構造2 + 話題2
        "weights_structural": {"structural": 0.8, "timeliness": 0.2},
        "weights_trending": {"structural": 0.2, "timeliness": 0.8}
    },
    "science": {
        "name": "Science",
        "emoji": "🔬",
        "description": "観測可能性の拡張、理論と実証",
        "posts_per_day": 2,
        "selection_mode": "dual",  # 構造1 + 話題1
        "weights_structural": {"structural": 0.7, "timeliness": 0.3},
        "weights_trending": {"structural": 0.3, "timeliness": 0.7}
    },
    "education": {
        "name": "Education",
        "emoji": "📚",
        "description": "価値の再定義、評価軸の移動",
        "posts_per_day": 2,
        "selection_mode": "dual",
        "weights_structural": {"structural": 0.7, "timeliness": 0.3},
        "weights_trending": {"structural": 0.3, "timeliness": 0.7}
    },
    "mycotech": {
        "name": "Mycotech",
        "emoji": "🍄",
        "description": "生物×機械、境界侵犯の象徴領域",
        "posts_per_day": 2,
        "selection_mode": "dual",
        "weights_structural": {"structural": 0.7, "timeliness": 0.3},
        "weights_trending": {"structural": 0.3, "timeliness": 0.7}
    },
    "curiosity": {
        "name": "Curiosity",
        "emoji": "🌍",
        "description": "スケール錯誤、本来そこにないもの",
        "posts_per_day": 2,
        "selection_mode": "dual",
        "weights_structural": {"structural": 0.7, "timeliness": 0.3},
        "weights_trending": {"structural": 0.3, "timeliness": 0.7}
    }
}

# =============================================================================
# RSS SOURCES
# =============================================================================

RSS_SOURCES = {
    "bigtech": [
        # グローバルテックメディア
        "https://techcrunch.com/feed/",
        "https://www.wired.com/feed/rss",
        "https://arstechnica.com/feed/",
        # 中国テック（英語版）
        "https://www.scmp.com/rss/91/feed",
        "https://kr-asia.com/feed",
        "https://technode.com/feed/",
        "https://pandaily.com/feed/",
        # トレンド
        "https://news.ycombinator.com/rss",
        "https://www.producthunt.com/feed",
    ],
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
        # 実践知
        "https://www.indiehackers.com/feed",
        "https://increment.com/feed.xml",
        # 日本語
        "https://qiita.com/popular-items/feed",
        "https://zenn.dev/feed",
    ],
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
    ],
    "science": [
        # 深掘り科学
        "https://www.sciencedaily.com/rss/all.xml",
        "https://phys.org/rss-feed/",
        "https://www.quantamagazine.org/feed/",
        "https://nautil.us/feed/",
        "https://www.earth.com/feed/",
        # 科学報道
        "https://feeds.arstechnica.com/arstechnica/science",
        "https://theconversation.com/articles.atom",
        # コミュニティ
        "https://www.reddit.com/r/science/.rss",
        "https://news.ycombinator.com/rss",
    ],
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
    ],
    "mycotech": [
        # 生物学研究
        "https://phys.org/rss-feed/biology-news/",
        "https://www.sciencedaily.com/rss/plants_animals.xml",
        "https://journals.plos.org/plosbiology/feed/atom",
        "https://www.earth.com/feed/",
        # 環境×技術
        "https://www.anthropocenemagazine.org/feed/",
        "https://grist.org/feed/",
        "https://therevelator.org/feed/",
        # テックトレンド
        "https://www.reddit.com/r/biology/.rss",
    ],
    "curiosity": [
        # 珍奇・深掘り
        "https://www.atlasobscura.com/feeds/latest",
        "https://www.bbc.com/future/feed.rss",
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
}

# =============================================================================
# TAG DETECTION - TRANSFORMATION
# =============================================================================

TRANSFORMATION_KEYWORDS = [
    "originally", "unexpectedly", "turned out", "repurposed",
    "paradoxically", "serendipitous", "accident", "accidental",
    "waste", "byproduct", "side effect", "unintended",
    "failure", "defect", "error", "mistake",
    "thought to be useless", "considered waste", "deemed failure"
]

ANTONYM_PAIRS = [
    ("poison", "medicine"), ("poison", "cure"), ("toxic", "therapeutic"),
    ("failure", "success"), ("failure", "discovery"),
    ("defect", "feature"), ("bug", "innovation"),
    ("waste", "resource"), ("trash", "treasure"),
    ("side effect", "main effect"), ("accident", "breakthrough")
]

# =============================================================================
# TAG DETECTION - BOUNDARY CROSSING
# =============================================================================

DOMAINS = {
    "biology": [
        "protein", "DNA", "cell", "organism", "evolution", "gene",
        "bacteria", "virus", "tissue", "membrane", "enzyme",
        "fungus", "fungi", "mycelium", "spore", "mushroom"
    ],
    "machine": [
        "algorithm", "robot", "AI", "circuit", "neural network",
        "computer", "software", "hardware", "sensor", "automation"
    ],
    "art": [
        "paint", "painting", "sculpture", "aesthetic", "creative",
        "artist", "gallery", "exhibition", "design", "visual"
    ],
    "military": [
        "weapon", "defense", "surveillance", "drone", "army",
        "combat", "warfare", "missile", "radar"
    ],
    "medicine": [
        "therapy", "diagnosis", "treatment", "patient", "clinical",
        "hospital", "doctor", "cure", "disease", "symptom"
    ],
    "game": [
        "game", "play", "VR", "virtual reality", "simulation",
        "player", "gaming", "interactive"
    ],
    "religion": [
        "ritual", "meditation", "spirituality", "sacred", "prayer",
        "belief", "faith", "ceremony"
    ],
    "food": [
        "food", "cooking", "cuisine", "ingredient", "recipe",
        "edible", "nutrition", "flavor"
    ],
    "material": [
        "material", "fabric", "textile", "composite", "polymer",
        "leather", "packaging", "insulation", "biodegradable"
    ]
}

BOUNDARY_KEYWORDS = [
    "combines", "merges", "intersection", "hybrid", "fusion",
    "cross", "interdisciplinary", "bridge", "between"
]

# =============================================================================
# TAG DETECTION - VISIBILITY GAIN
# =============================================================================

VISIBILITY_KEYWORDS = [
    "first time", "newly observable", "previously invisible",
    "now detectable", "breakthrough", "revealed", "discovered",
    "measured for the first time", "visualized", "imaged",
    "mapped", "sequenced", "quantified", "detected",
    "microscopy", "imaging", "sensor", "telescope", "spectroscopy",
    "scanner", "camera", "detector"
]

# =============================================================================
# TAG DETECTION - VALUE REDEFINITION
# =============================================================================

VALUE_KEYWORDS = [
    "once considered", "traditionally seen as", "previously thought",
    "now understood", "rethinking", "reconsidered", "redefine",
    "challenge", "question", "reconsider",
    "no longer seen as", "shift from", "move away from"
]

CATEGORY_SHIFT_PAIRS = [
    ("disease", "diversity"), ("disease", "variation"),
    ("waste", "efficient"), ("waste", "valuable"),
    ("irrational", "rational"), ("nonsense", "meaningful"),
    ("useless", "essential"), ("primitive", "sophisticated")
]

# =============================================================================
# TAG DETECTION - SCALE SHIFT
# =============================================================================

SCALE_PAIRS = [
    ("nano", "global"), ("nano", "planetary"), ("nano", "worldwide"),
    ("atom", "universe"), ("atom", "cosmic"),
    ("single", "entire"), ("one", "all"),
    ("individual", "species"), ("personal", "civilization"),
    ("tiny", "massive"), ("trace", "profound"), ("minimal", "critical"),
    ("small", "catastrophic"), ("slight", "dramatic")
]

SCALE_KEYWORDS = [
    "nanoscale", "microscopic", "molecular", "atomic",
    "global", "planetary", "universal", "cosmic",
    "tiny amount", "trace amount", "minimal dose"
]

# =============================================================================
# TAG DETECTION - ONTOLOGY SHIFT
# =============================================================================

ONTOLOGY_KEYWORDS = [
    "consciousness", "free will", "intelligence", "creativity",
    "self", "identity", "agency", "responsibility", "personhood",
    "sentience", "awareness", "mind", "soul"
]

QUESTIONING_KEYWORDS = [
    "what is", "redefine", "challenge notion", "blur boundary",
    "question", "reconsider", "rethink"
]

# =============================================================================
# SCORING
# =============================================================================

# ソース信頼度
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

# デフォルトのスコア比率（カテゴリ設定で上書きされるため、バックアップとしてのみ使用）
STRUCTURAL_WEIGHT = 0.5
TIMELINESS_WEIGHT = 0.5

# 各タグのスコア
TAG_SCORES = {
    "transformation_keyword": 3,
    "transformation_antonym_pair": 5,
    "transformation_negation_pattern": 4,
    "boundary_crossing_2_domains": 4,
    "boundary_crossing_3_domains": 7,
    "boundary_crossing_keyword": 2,
    "visibility_gain_keyword": 4,
    "visibility_gain_combo": 5,
    "value_redefinition_keyword": 4,
    "value_redefinition_pair": 5,
    "scale_shift_pair": 4,
    "scale_shift_paradox": 5,
    "ontology_shift": 8,
}

# =============================================================================
# OPERATIONAL SETTINGS
# =============================================================================

# 保存期限（日）
POSTED_RETENTION_DAYS = 7
PENDING_RETENTION_DAYS = 3

# RSS取得設定
USER_AGENT = "NewsCurationBot/1.0 (+https://github.com/0xsalome/newsbot)"
REQUEST_INTERVAL_SECONDS = 1
MAX_RETRIES = 3

# Reddit人気度フィルター
# 最低基準：upvotes < 10 かつ comments < 3 の投稿は除外
REDDIT_MIN_UPVOTES = 10
REDDIT_MIN_COMMENTS = 3
REDDIT_MIN_UPVOTE_RATIO = 0.6  # 60%未満の賛成率は除外（賛否両論すぎる投稿）

# Reddit投稿の上限（カテゴリごと）
REDDIT_MAX_POSTS = {
    "ai": 1,  # AIカテゴリはReddit最大1記事
    "education": 2,
    "default": 2  # その他のカテゴリはデフォルト2記事まで
}

# BigTech: 製品販売情報の除外キーワード
BIGTECH_PRODUCT_EXCLUDE_KEYWORDS = [
    # 販売・発売関連
    "launches", "launch", "unveiled", "unveils", "introduces", "announced", "announces",
    "available now", "now available", "on sale", "pre-order", "preorder",
    "coming soon", "releasing", "released",
    # レビュー・スペック関連
    "review", "hands-on", "unboxing", "specs", "specifications", "features",
    "price", "pricing", "costs", "$", "€", "£", "¥",
    # 製品カテゴリ
    "drone", "camera", "phone", "smartphone", "tablet", "laptop", "notebook",
    "watch", "smartwatch", "earbuds", "headphones", "speaker",
    "tv", "television", "monitor", "display",
    "car", "vehicle", "ev", "electric vehicle", "suv",
    "bike", "scooter", "motorcycle",
    "gadget", "device", "wearable"
]

# タイムゾーン
TIMEZONE = "Asia/Tokyo"