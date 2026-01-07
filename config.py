"""
News Curation Bot - Configuration
セキュリティ: Webhook URLはここに書かない（GitHub Secretsで管理）
"""

# =============================================================================
# CATEGORY DEFINITIONS
# =============================================================================

CATEGORIES = {
    "science": {
        "name": "Science",
        "emoji": "🔬",
        "description": "観測可能性の拡張、理論と実証"
    },
    "ai": {
        "name": "AI",
        "emoji": "🤖",
        "description": "境界侵犯、人間観の揺らぎ"
    },
    "education": {
        "name": "Education",
        "emoji": "📚",
        "description": "価値の再定義、評価軸の移動"
    },
    "mycotech": {
        "name": "Mycotech",
        "emoji": "🍄",
        "description": "生物×機械、境界侵犯の象徴領域"
    },
    "curiosity": {
        "name": "Curiosity",
        "emoji": "🌍",
        "description": "スケール錯誤、本来そこにないもの"
    }
}

# =============================================================================
# RSS SOURCES
# =============================================================================

RSS_SOURCES = {
    "science": [
        "https://www.nature.com/nature.rss",
        "https://www.sciencedaily.com/rss/all.xml",
        "https://phys.org/rss-feed/",
        "https://www.eurekalert.org/rss/news_releases.xml",
    ],
    "ai": [
        "https://news.ycombinator.com/rss",
        "https://www.technologyreview.com/feed/",
        "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "https://venturebeat.com/category/ai/feed/",
    ],
    "education": [
        "https://www.edsurge.com/news.rss",
        "https://edsource.org/feed",
        "https://hechingerreport.org/feed/",
    ],
    "mycotech": [
        "https://phys.org/rss-feed/biology-news/",
        "https://news.ycombinator.com/rss",
        "https://www.sciencedaily.com/rss/plants_animals/mycology.xml",
        "https://www.anthropocenemagazine.org/feed/",
    ],
    "curiosity": [
        "https://www.atlasobscura.com/feeds/latest",
        "https://www.bbc.com/future/rss",
        "https://aeon.co/feed.rss",
        "https://www.smithsonianmag.com/rss/latest_articles/",
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

# ソース格付け
SOURCE_WEIGHT = {
    "nature.com": 5,
    "science.org": 5,
    "cell.com": 5,
    "nytimes.com": 3,
    "bbc.com": 3,
    "technologyreview.com": 4,
    "theverge.com": 2,
    "sciencedaily.com": 3,
    "phys.org": 2,
    "default": 1
}

# スコア比率
STRUCTURAL_WEIGHT = 0.7
TIMELINESS_WEIGHT = 0.3

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

# 1日あたりの投稿数（カテゴリごと）
POSTS_PER_DAY = 2

# 保存期限（日）
POSTED_RETENTION_DAYS = 7
PENDING_RETENTION_DAYS = 3

# RSS取得設定
USER_AGENT = "NewsCurationBot/1.0 (+https://github.com/YOUR_REPO)"
REQUEST_INTERVAL_SECONDS = 1
MAX_RETRIES = 3

# タイムゾーン
TIMEZONE = "Asia/Tokyo"
