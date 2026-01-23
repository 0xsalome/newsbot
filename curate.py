#!/usr/bin/env python3
"""
News Curation Bot - Main Script
構造的類似性に基づく自動ニュースキュレーション

Usage:
    python curate.py              # 通常実行
    python curate.py --dry-run    # 投稿せずにスコアリング確認
    python curate.py --category science  # 特定カテゴリのみ
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime, timedelta
from urllib.parse import urlparse

import feedparser
import requests

import config


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

def load_state(filepath="state.json"):
    """state.jsonを読み込む"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            state = json.load(f)
            # 新規カテゴリの初期化
            for category in config.CATEGORIES:
                if category not in state["posted"]:
                    state["posted"][category] = []
                if category not in state["pending"]:
                    state["pending"][category] = []
            return state
    except FileNotFoundError:
        return create_initial_state()


def save_state(state, filepath="state.json"):
    """state.jsonを保存する"""
    state["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def create_initial_state():
    """初期状態を作成"""
    return {
        "meta": {
            "last_updated": None,
            "retention_days": config.POSTED_RETENTION_DAYS
        },
        "posted": {cat: [] for cat in config.CATEGORIES},
        "pending": {cat: [] for cat in config.CATEGORIES}
    }


def cleanup_old_entries(state):
    """古いエントリを削除"""
    now = datetime.utcnow()

    # posted: 7日以上古いものを削除
    for category in state["posted"]:
        state["posted"][category] = [
            entry for entry in state["posted"][category]
            if _is_within_days(entry.get("posted_at"), config.POSTED_RETENTION_DAYS, now)
        ]

    # pending: 3日以上古いものを削除
    for category in state["pending"]:
        state["pending"][category] = [
            entry for entry in state["pending"][category]
            if _is_within_days(entry.get("fetched_at"), config.PENDING_RETENTION_DAYS, now)
        ]

    return state


def _is_within_days(date_str, days, now):
    """日付が指定日数以内かチェック"""
    if not date_str:
        return False
    try:
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return (now - date.replace(tzinfo=None)).days <= days
    except (ValueError, AttributeError):
        return False


# =============================================================================
# RSS FETCHING
# =============================================================================

def fetch_rss(url):
    """RSSフィードまたはReddit JSON APIを取得"""
    try:
        headers = {"User-Agent": config.USER_AGENT}

        # Reddit URLの場合はJSON APIを使用
        if "reddit.com" in url:
            # .rss を .json に置換（なければそのまま .json 追加）
            json_url = url.replace(".rss", ".json") if ".rss" in url else url + ".json"
            response = requests.get(json_url, headers=headers, timeout=30)
            response.raise_for_status()
            return {"reddit_json": response.json(), "url": url}

        # 通常のRSS
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return feedparser.parse(response.content)
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def fetch_all_feeds(category):
    """カテゴリのすべてのRSSフィードを取得"""
    articles = []
    sources = config.RSS_SOURCES.get(category, [])

    for url in sources:
        feed = fetch_rss(url)
        if not feed:
            continue

        # Reddit JSON APIの場合
        if isinstance(feed, dict) and "reddit_json" in feed:
            reddit_data = feed["reddit_json"]
            if reddit_data.get("data", {}).get("children"):
                for child in reddit_data["data"]["children"]:
                    post_data = child.get("data", {})
                    article = parse_reddit_post(post_data, url)
                    if article:
                        articles.append(article)
        # 通常のRSS
        elif hasattr(feed, 'entries') and feed.entries:
            for entry in feed.entries:
                article = parse_feed_entry(entry, url)
                if article:
                    articles.append(article)

        time.sleep(config.REQUEST_INTERVAL_SECONDS)

    return articles


def parse_feed_entry(entry, source_url):
    """RSSエントリを記事オブジェクトに変換"""
    try:
        return {
            "url": entry.get("link", ""),
            "title": entry.get("title", ""),
            "summary": entry.get("summary", entry.get("description", "")),
            "source": urlparse(source_url).netloc,
            "published": entry.get("published", ""),
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "tags": [],
            "structural_score": 0,
            "timeliness_score": 0,
            "final_score": 0,
            # Reddit以外は人気度情報なし
            "reddit_score": None,
            "reddit_comments": None,
        }
    except Exception as e:
        print(f"[ERROR] Failed to parse entry: {e}")
        return None


def parse_reddit_post(post_data, source_url):
    """Reddit投稿を記事オブジェクトに変換"""
    try:
        # 人気度フィルター：最低基準を満たさない投稿を除外
        score = post_data.get("score", 0)
        num_comments = post_data.get("num_comments", 0)

        # 条件: upvotes < 10 かつ comments < 3 の場合は除外
        if score < config.REDDIT_MIN_UPVOTES and num_comments < config.REDDIT_MIN_COMMENTS:
            return None

        # upvote_ratioが低すぎる（賛否が分かれすぎ）投稿も除外
        upvote_ratio = post_data.get("upvote_ratio", 1.0)
        if upvote_ratio < config.REDDIT_MIN_UPVOTE_RATIO:
            return None

        # 投稿時刻をISO形式に変換
        created_utc = post_data.get("created_utc", 0)
        published_date = datetime.utcfromtimestamp(created_utc).isoformat() + "Z" if created_utc else ""

        # selftext（本文）またはリンク先URLを取得
        url = post_data.get("url", "")
        # Reddit内部リンクの場合は絶対URLに変換
        if url.startswith("/r/"):
            url = f"https://www.reddit.com{url}"

        return {
            "url": url,
            "title": post_data.get("title", ""),
            "summary": post_data.get("selftext", "")[:500],  # 本文の最初の500文字
            "source": "reddit.com",
            "published": published_date,
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "tags": [],
            "structural_score": 0,
            "timeliness_score": 0,
            "final_score": 0,
            # Reddit人気度情報
            "reddit_score": score,
            "reddit_comments": num_comments,
            "reddit_upvote_ratio": upvote_ratio,
        }
    except Exception as e:
        print(f"[ERROR] Failed to parse Reddit post: {e}")
        return None


# =============================================================================
# TRANSLATION (DeepL API Free)
# =============================================================================

def translate_to_japanese(text):
    """DeepL APIで日本語に翻訳"""
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        return None

    try:
        response = requests.post(
            "https://api-free.deepl.com/v2/translate",
            data={
                "auth_key": api_key,
                "text": text,
                "target_lang": "JA"
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result["translations"][0]["text"]
    except Exception as e:
        error_details = str(e)
        # レスポンス本文があれば詳細を追加（認証エラーや制限超過の理由がわかる）
        if 'response' in locals() and hasattr(response, 'text') and response.text:
            error_details += f" | Details: {response.text}"
        
        print(f"[WARN] Translation failed: {error_details}")
        return None


def translate_articles(articles):
    """記事のタイトルを日本語に翻訳"""
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        print("[INFO] DEEPL_API_KEY not set, skipping translation")
        return articles

    print(f"Translating {len(articles)} article titles...")
    for article in articles:
        title_ja = translate_to_japanese(article["title"])
        article["title_ja"] = title_ja if title_ja else article["title"]
        time.sleep(0.1)  # Rate limit対策

    return articles


def strip_html(text):
    """HTMLタグを除去"""
    return re.sub(r'<[^>]+>', '', text)


# =============================================================================
# TAG DETECTION
# =============================================================================

def detect_tags(article):
    """記事にタグを付与"""
    # HTML除去と正規化
    raw_text = f"{article['title']} {article['summary']}"
    text = strip_html(raw_text).lower()
    
    tags = []

    # transformation
    score = detect_transformation(text)
    if score > 0:
        tags.append({"name": "transformation", "score": score})

    # boundary_crossing
    score = detect_boundary_crossing(text)
    if score > 0:
        tags.append({"name": "boundary_crossing", "score": score})

    # visibility_gain
    score = detect_visibility_gain(text)
    if score > 0:
        tags.append({"name": "visibility_gain", "score": score})

    # value_redefinition
    score = detect_value_redefinition(text)
    if score > 0:
        tags.append({"name": "value_redefinition", "score": score})

    # scale_shift
    score = detect_scale_shift(text)
    if score > 0:
        tags.append({"name": "scale_shift", "score": score})

    # ontology_shift (他タグとの組み合わせでのみ付与)
    if tags:  # 他のタグがある場合のみチェック
        score = detect_ontology_shift(text, tags)
        if score > 0:
            tags.append({"name": "ontology_shift", "score": score})

    article["tags"] = tags
    return article


def count_matches(text, keywords):
    """キーワードの出現回数をカウント（単語境界を考慮）"""
    count = 0
    for keyword in keywords:
        # エスケープ処理（キーワードに記号が含まれる場合用）
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text):
            count += 1
    return count


def detect_transformation(text):
    """transformation タグの検出"""
    score = 0

    # キーワード検出
    matches = count_matches(text, config.TRANSFORMATION_KEYWORDS)
    if matches > 0:
        score += config.TAG_SCORES["transformation_keyword"] * matches

    # 対義語ペア検出
    for word1, word2 in config.ANTONYM_PAIRS:
        pattern1 = r'\b' + re.escape(word1) + r'\b'
        pattern2 = r'\b' + re.escape(word2) + r'\b'
        if re.search(pattern1, text) and re.search(pattern2, text):
            score += config.TAG_SCORES["transformation_antonym_pair"]

    return score


def detect_boundary_crossing(text):
    """boundary_crossing タグの検出"""
    score = 0
    detected_domains = []

    # ドメイン検出
    for domain, keywords in config.DOMAINS.items():
        if count_matches(text, keywords) > 0:
            detected_domains.append(domain)

    # 2ドメイン以上で検出
    if len(detected_domains) >= 3:
        score += config.TAG_SCORES["boundary_crossing_3_domains"]
    elif len(detected_domains) >= 2:
        score += config.TAG_SCORES["boundary_crossing_2_domains"]

    # 境界語検出
    if count_matches(text, config.BOUNDARY_KEYWORDS) > 0:
        score += config.TAG_SCORES["boundary_crossing_keyword"]

    return score


def detect_visibility_gain(text):
    """visibility_gain タグの検出"""
    score = 0
    
    matches = count_matches(text, config.VISIBILITY_KEYWORDS)
    if matches > 0:
        score += config.TAG_SCORES["visibility_gain_keyword"] * matches

    return min(score, config.TAG_SCORES["visibility_gain_combo"])  # 上限設定


def detect_value_redefinition(text):
    """value_redefinition タグの検出"""
    score = 0

    matches = count_matches(text, config.VALUE_KEYWORDS)
    if matches > 0:
        score += config.TAG_SCORES["value_redefinition_keyword"] * matches

    for word1, word2 in config.CATEGORY_SHIFT_PAIRS:
        pattern1 = r'\b' + re.escape(word1) + r'\b'
        pattern2 = r'\b' + re.escape(word2) + r'\b'
        if re.search(pattern1, text) and re.search(pattern2, text):
            score += config.TAG_SCORES["value_redefinition_pair"]

    return score


def detect_scale_shift(text):
    """scale_shift タグの検出"""
    score = 0

    for word1, word2 in config.SCALE_PAIRS:
        pattern1 = r'\b' + re.escape(word1) + r'\b'
        pattern2 = r'\b' + re.escape(word2) + r'\b'
        if re.search(pattern1, text) and re.search(pattern2, text):
            score += config.TAG_SCORES["scale_shift_pair"]

    matches = count_matches(text, config.SCALE_KEYWORDS)
    if matches > 0:
        score += config.TAG_SCORES["scale_shift_paradox"]

    return score


def detect_ontology_shift(text, existing_tags):
    """ontology_shift タグの検出（他タグとの組み合わせでのみ）"""
    has_ontology_keyword = count_matches(text, config.ONTOLOGY_KEYWORDS) > 0
    has_questioning = count_matches(text, config.QUESTIONING_KEYWORDS) > 0

    if not has_ontology_keyword:
        return 0

    # transformation または boundary_crossing と組み合わせ
    relevant_tags = ["transformation", "boundary_crossing"]
    has_relevant = any(t["name"] in relevant_tags for t in existing_tags)

    if has_relevant and has_questioning:
        return config.TAG_SCORES["ontology_shift"]

    return 0


# =============================================================================
# SCORING
# =============================================================================

def calculate_base_scores(article):
    """記事の基本スコア（構造・話題性）を計算"""
    # 構造強度スコア
    structural_score = sum(tag["score"] for tag in article["tags"])

    # 話題性スコア
    timeliness_score = calculate_timeliness_score(article)

    article["structural_score"] = structural_score
    article["timeliness_score"] = timeliness_score
    return article

def calculate_weighted_score(article, weights):
    """指定された重みで最終スコアを計算"""
    final_score = (
        article["structural_score"] * weights["structural"] +
        article["timeliness_score"] * weights["timeliness"]
    )
    return final_score

def calculate_timeliness_score(article):
    """話題性スコアを計算"""
    import math
    score = 0

    # ソース格付け
    source = article.get("source", "")
    for domain, weight in config.SOURCE_WEIGHT.items():
        if domain in source:
            score += weight
            break
    else:
        score += config.SOURCE_WEIGHT["default"]

    # 鮮度スコア
    published = article.get("published", "")
    if published:
        try:
            # feedparserの日付形式に対応
            pub_date = feedparser._parse_date(published)
            if pub_date:
                pub_datetime = datetime(*pub_date[:6])
                age_hours = (datetime.utcnow() - pub_datetime).total_seconds() / 3600

                if age_hours <= 24:
                    score += 3
                elif age_hours <= 48:
                    score += 2
                elif age_hours <= 168:  # 7 days
                    score += 1
        except Exception:
            pass

    # Reddit人気度スコア（エンゲージメント）
    reddit_score = article.get("reddit_score")
    reddit_comments = article.get("reddit_comments")

    if reddit_score is not None and reddit_comments is not None:
        # 対数スケールでエンゲージメントを評価（大きな数値差を緩和）
        # log(upvotes + 1) + log(comments + 1) を正規化
        engagement = math.log(reddit_score + 1) + math.log(reddit_comments + 1)
        # エンゲージメントスコアを0-5の範囲に正規化
        # 典型的な人気投稿: upvotes=100, comments=20 → log(101)+log(21) ≈ 4.6+3.0 = 7.6
        # スコア化: engagement / 2 (最大値を5程度に抑える)
        engagement_score = min(engagement / 2, 5)
        score += engagement_score

    return score


# =============================================================================
# UTILS
# =============================================================================

def normalize_url(url):
    """URLを正規化（重複チェック用）"""
    if not url:
        return ""
    try:
        parsed = urlparse(url.strip())
        # スキームとネットロックを小文字化
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        path = parsed.path
        # 末尾のスラッシュを除去
        if path.endswith("/"):
            path = path[:-1]
        
        # クエリパラメータはそのまま（記事IDなどが含まれる場合があるため）
        # ただし、特定のトラッキングパラメータは削除してもいいかもしれないが、今回はシンプルに
        
        return f"{scheme}://{netloc}{path}"
    except Exception:
        return url.strip()


# =============================================================================
# SELECTION LOGIC
# =============================================================================

def filter_bigtech_products(articles):
    """BigTechカテゴリで製品販売情報を除外"""
    filtered = []
    for article in articles:
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

        # 除外キーワードをチェック
        has_product_keyword = False
        for keyword in config.BIGTECH_PRODUCT_EXCLUDE_KEYWORDS:
            if keyword.lower() in text:
                has_product_keyword = True
                break

        # キーワードが含まれていない記事のみ追加
        if not has_product_keyword:
            filtered.append(article)

    return filtered


def select_articles(articles, state, category):
    """カテゴリ設定に基づいて記事を選出"""
    # 1. すべての候補を正規化URLでユニークにする
    unique_candidates_map = {}
    for a in articles:
        norm_url = normalize_url(a["url"])
        if norm_url not in unique_candidates_map:
            unique_candidates_map[norm_url] = a
    
    # 2. 既に投稿済みのURLを除外（正規化して比較）
    posted_entries = state["posted"].get(category, [])
    posted_urls = {normalize_url(entry["url"]) for entry in posted_entries}
    
    new_articles = []
    for url, a in unique_candidates_map.items():
        if url not in posted_urls:
            new_articles.append(a)
    
    # 3. pending記事とマージ
    pending = state["pending"].get(category, [])
    # すでにnew_articlesにあるものはpendingから除外
    new_urls = {normalize_url(a["url"]) for a in new_articles}
    
    # pending内の重複も排除
    unique_pending = []
    seen_pending_urls = set()
    for p in pending:
        p_url = normalize_url(p["url"])
        if p_url not in new_urls and p_url not in posted_urls and p_url not in seen_pending_urls:
            unique_pending.append(p)
            seen_pending_urls.add(p_url)

    all_candidates = new_articles + unique_pending

    # BigTechカテゴリ: 製品販売情報を除外
    if category == "bigtech":
        all_candidates = filter_bigtech_products(all_candidates)

    cat_config = config.CATEGORIES[category]
    mode = cat_config["selection_mode"]

    selected = []

    if mode == "trending_only":
        # 話題性重視のみ
        weights = cat_config["weights"]
        for a in all_candidates:
            a["final_score"] = round(calculate_weighted_score(a, weights), 2)

        sorted_articles = sorted(all_candidates, key=lambda x: x["final_score"], reverse=True)
        # ソース多様性を考慮して選出
        # BigTechカテゴリは1ソース1記事のみ
        max_per_source = 1 if category in ["bigtech", "ai"] else 2
        selected = ensure_source_diversity(sorted_articles, cat_config["posts_per_day"], max_per_source=max_per_source)

    elif mode == "dual":
        # 構造重視1 + 話題重視1
        
        # 1. 構造重視
        weights_struct = cat_config["weights_structural"]
        for a in all_candidates:
            a["temp_score_struct"] = calculate_weighted_score(a, weights_struct)
        
        sorted_struct = sorted(all_candidates, key=lambda x: x["temp_score_struct"], reverse=True)
        struct_candidates = [a for a in sorted_struct if a["tags"]]
        
        top_structural = struct_candidates[:1]
        
        # 2. 話題重視
        weights_trend = cat_config["weights_trending"]
        # 重複排除（オブジェクトIDベースだと危険なのでURLベースで）
        selected_urls = {normalize_url(a["url"]) for a in top_structural}
        remaining = [a for a in all_candidates if normalize_url(a["url"]) not in selected_urls]
        
        for a in remaining:
            a["temp_score_trend"] = calculate_weighted_score(a, weights_trend)
            
        sorted_trend = sorted(remaining, key=lambda x: x["temp_score_trend"], reverse=True)
        
        # ソース重複チェック（構造枠と同じソースばかりにならないように）
        top_trending = []
        if sorted_trend:
            # 構造枠のソースを確認
            struct_sources = [urlparse(a["url"]).netloc for a in top_structural]
            
            # 可能な限り異なるソースを選ぶ
            for a in sorted_trend:
                if urlparse(a["url"]).netloc not in struct_sources:
                    top_trending.append(a)
                    break
            
            # 見つからなければスコア1位を選ぶ
            if not top_trending and sorted_trend:
                top_trending.append(sorted_trend[0])
        
        # 統合
        selected = top_structural + top_trending
        
        # final_score更新
        for a in top_structural:
            a["final_score"] = round(a.get("temp_score_struct", 0), 2)
        for a in top_trending:
            a["final_score"] = round(a.get("temp_score_trend", 0), 2)


    elif mode == "dual_enhanced":
        # 構造重視2 + 話題重視2 (AI)

        # Reddit投稿数の上限を取得
        reddit_max = config.REDDIT_MAX_POSTS.get(category, config.REDDIT_MAX_POSTS["default"])
        reddit_count = 0

        # 1. 構造重視
        weights_struct = cat_config["weights_structural"]
        for a in all_candidates:
            a["temp_score_struct"] = calculate_weighted_score(a, weights_struct)

        sorted_struct = sorted(all_candidates, key=lambda x: x["temp_score_struct"], reverse=True)
        struct_candidates = [a for a in sorted_struct if a["tags"]]

        # ソース多様性を確保しつつ2つ選ぶ（AIカテゴリは1ソース1記事）
        max_per_source = 1 if category == "ai" else 2

        # Reddit上限を考慮しながら選出
        top_structural = []
        source_counts = Counter()
        for article in struct_candidates:
            if len(top_structural) >= 2:
                break

            domain = urlparse(article["url"]).netloc
            # Reddit投稿はreddit_scoreフィールドで判定（URLではなく）
            is_reddit = article.get("reddit_score") is not None

            # Reddit上限チェック
            if is_reddit and reddit_count >= reddit_max:
                continue

            # ソース多様性チェック
            if source_counts[domain] < max_per_source:
                top_structural.append(article)
                source_counts[domain] += 1
                if is_reddit:
                    reddit_count += 1

        # タグ多様性チェック（Reddit制限も考慮）
        if category == "ai":
            # Reddit制限を考慮したタグ多様性チェック
            top_structural = ensure_tag_diversity_with_reddit_limit(
                top_structural, struct_candidates, reddit_count, reddit_max
            )
            # reddit_countを再計算（reddit_scoreフィールドで判定）
            reddit_count = sum(1 for a in top_structural if a.get("reddit_score") is not None)
        else:
            top_structural = ensure_tag_diversity(top_structural, struct_candidates)

        # 2. 話題重視
        weights_trend = cat_config["weights_trending"]
        selected_urls = {normalize_url(a["url"]) for a in top_structural}
        remaining = [a for a in all_candidates if normalize_url(a["url"]) not in selected_urls]

        for a in remaining:
            a["temp_score_trend"] = calculate_weighted_score(a, weights_trend)

        sorted_trend = sorted(remaining, key=lambda x: x["temp_score_trend"], reverse=True)

        # こちらもソース多様性を確保（全体でのバランスも考慮したいが、まずはこの枠内で）
        # 構造枠ですでに選ばれたソースは優先度を下げるロジックを入れるとより良い
        struct_sources = Counter([urlparse(a["url"]).netloc for a in top_structural])

        top_trending = []
        for a in sorted_trend:
            if len(top_trending) >= 2:
                break

            domain = urlparse(a["url"]).netloc
            # Reddit投稿はreddit_scoreフィールドで判定
            is_reddit = a.get("reddit_score") is not None

            # Reddit上限チェック
            if is_reddit and reddit_count >= reddit_max:
                continue

            # AIカテゴリは全体で同じドメインは最大1つまで（構造枠ですでに選ばれたソースは除外）
            max_allowed = 1 if category == "ai" else 2
            if struct_sources.get(domain, 0) + 1 <= max_allowed: # ここでの+1は今回選ぶ分
                 top_trending.append(a)
                 struct_sources[domain] = struct_sources.get(domain, 0) + 1
                 if is_reddit:
                     reddit_count += 1
        
        # もし厳しすぎて埋まらなかった場合、制限を緩めて埋める
        if len(top_trending) < 2:
            current_trending_urls = {normalize_url(a["url"]) for a in top_trending}
            remaining_trend = [a for a in sorted_trend if normalize_url(a["url"]) not in current_trending_urls]
            needed = 2 - len(top_trending)

            # AIカテゴリの場合は、フォールバック時もソース重複を避ける
            if category == "ai":
                for candidate in remaining_trend:
                    if len(top_trending) >= 2:
                        break
                    candidate_domain = urlparse(candidate["url"]).netloc
                    # Reddit投稿はreddit_scoreフィールドで判定
                    is_reddit_fallback = candidate.get("reddit_score") is not None

                    # Reddit上限チェック
                    if is_reddit_fallback and reddit_count >= reddit_max:
                        continue

                    if struct_sources.get(candidate_domain, 0) == 0:
                        top_trending.append(candidate)
                        struct_sources[candidate_domain] = 1
                        if is_reddit_fallback:
                            reddit_count += 1
            else:
                top_trending.extend(remaining_trend[:needed])

        # 統合
        selected = top_structural + top_trending

        # final_score更新
        for a in top_structural:
            a["final_score"] = round(a.get("temp_score_struct", 0), 2)
        for a in top_trending:
            a["final_score"] = round(a.get("temp_score_trend", 0), 2)

    return selected


def ensure_source_diversity(candidates, limit, max_per_source=2):
    """同一ソースからの選出を制限して記事を選ぶ"""
    selected = []
    source_counts = Counter()
    
    for article in candidates:
        if len(selected) >= limit:
            break
            
        domain = urlparse(article["url"]).netloc
        if source_counts[domain] < max_per_source:
            selected.append(article)
            source_counts[domain] += 1
            
    return selected



def ensure_tag_diversity(current_top, candidates):
    """タグの多様性を確保（構造重視枠用）"""
    if len(current_top) < 2:
        return current_top

    top1 = current_top[0]
    top2 = current_top[1]

    tags1 = {t["name"] for t in top1.get("tags", [])}
    tags2 = {t["name"] for t in top2.get("tags", [])}

    # 同じタグセットなら、候補リストの3番目以降から異なるタグを持つものを探す
    if tags1 == tags2 and len(candidates) > 2:
        for article in candidates[2:10]:  # 上位10件まで探索
            article_tags = {t["name"] for t in article.get("tags", [])}
            if article_tags != tags1:
                return [top1, article]

    return current_top


def ensure_tag_diversity_with_reddit_limit(current_top, candidates, current_reddit_count, reddit_max):
    """タグの多様性を確保（Reddit制限も考慮）"""
    if len(current_top) < 2:
        return current_top

    top1 = current_top[0]
    top2 = current_top[1]

    tags1 = {t["name"] for t in top1.get("tags", [])}
    tags2 = {t["name"] for t in top2.get("tags", [])}

    # 同じタグセットなら、候補リストの3番目以降から異なるタグを持つものを探す
    if tags1 == tags2 and len(candidates) > 2:
        for article in candidates[2:10]:  # 上位10件まで探索
            article_tags = {t["name"] for t in article.get("tags", [])}
            if article_tags != tags1:
                # Reddit制限チェック（reddit_scoreフィールドで判定）
                is_reddit = article.get("reddit_score") is not None
                is_top2_reddit = top2.get("reddit_score") is not None

                # top2がRedditで、新しい記事もRedditの場合、Reddit数は変わらない
                # top2がRedditでなく、新しい記事がRedditの場合、Reddit数が増える
                if is_reddit and not is_top2_reddit:
                    # Reddit上限をチェック
                    if current_reddit_count >= reddit_max:
                        continue  # この記事はスキップして次を探す

                return [top1, article]

    return current_top


def update_pending(articles, selected, state, category):
    """pending記事を更新"""
    selected_urls = {a["url"] for a in selected}
    
    # 選択されなかった記事
    remaining = [a for a in articles if a["url"] not in selected_urls]
    
    # 簡易スコア（デフォルトウェイト）でソートして上位を保持
    # ※ 次回実行時に適切なモードで再計算されるため、ここでは暫定的に保持
    default_weights = {"structural": 0.5, "timeliness": 0.5}
    for a in remaining:
        if "final_score" not in a or a["final_score"] == 0:
             a["final_score"] = calculate_weighted_score(a, default_weights)

    sorted_pending = sorted(remaining, key=lambda x: x.get("final_score", 0), reverse=True)
    
    state["pending"][category] = sorted_pending[:10]  # 上位10件保持

    return state


# =============================================================================
# DISCORD POSTING
# =============================================================================

def post_to_discord(article, category, dry_run=False):
    """Discordに投稿"""
    webhook_env = f"DISCORD_WEBHOOK_{category.upper()}"
    webhook_url = os.environ.get(webhook_env)

    # メッセージ作成（dry-run時も表示するため先に作成）
    cat_info = config.CATEGORIES[category]
    tag_names = " × ".join(t["name"] for t in article["tags"]) if article["tags"] else "no tags"
    date_str = datetime.utcnow().strftime("%Y-%m-%d")

    # 日本語タイトルがあれば使用
    title = article.get('title_ja', article['title'])

    message = f"""{cat_info['emoji']} **{cat_info['name']}** | {date_str}

**[{tag_names}]**
{title}

🔗 {article['url']}
📰 {article['source']} | Score: {article['final_score']}"""

    if dry_run:
        print(f"\n[DRY-RUN] Would post to {category}:")
        print(message)
        print("-" * 50)
        return True

    # Webhook URLチェック（実投稿時のみ）
    if not webhook_url:
        print(f"[WARN] {webhook_env} not set, skipping post")
        return False

    # 実際に投稿
    try:
        response = requests.post(
            webhook_url,
            json={"content": message},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        print(f"[OK] Posted to {category}: {article['title'][:50]}...")
        return True
    except requests.RequestException as e:
        print(f"[ERROR] Failed to post to Discord: {e}")
        return False


# =============================================================================
# MAIN
# =============================================================================

def process_category(category, state, dry_run=False):
    """1カテゴリを処理"""
    print(f"\n{'='*50}")
    print(f"Processing: {category}")
    print(f"{'='*50}")

    # RSS取得
    articles = fetch_all_feeds(category)
    print(f"Fetched {len(articles)} articles")

    if not articles:
        return state

    # タグ付与と基本スコア計算
    for article in articles:
        detect_tags(article)
        calculate_base_scores(article)

    # 記事選択（カテゴリごとのロジックで）
    selected = select_articles(articles, state, category)
    print(f"Selected {len(selected)} articles for posting")

    # 選択された記事のみ翻訳（API節約）
    selected = translate_articles(selected)

    # 投稿
    for article in selected:
        if post_to_discord(article, category, dry_run):
            # 投稿成功したらpostedに追加
            if not dry_run:
                state["posted"][category].append({
                    "url": article["url"],
                    "posted_at": datetime.utcnow().strftime("%Y-%m-%d"),
                    "score": article["final_score"],
                    "tags": [t["name"] for t in article["tags"]]
                })

    # pending更新
    # selectedに入らなかった記事の中からpending候補を選ぶ
    state = update_pending(articles, selected, state, category)

    return state


def main():
    parser = argparse.ArgumentParser(description="News Curation Bot")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually post")
    parser.add_argument("--category", type=str, help="Process specific category only")
    args = parser.parse_args()

    print("News Curation Bot starting...")
    print(f"Dry run: {args.dry_run}")

    # 状態読み込み
    state = load_state()
    state = cleanup_old_entries(state)

    # カテゴリ処理
    categories = [args.category] if args.category else list(config.CATEGORIES.keys())

    for category in categories:
        if category not in config.CATEGORIES:
            print(f"[ERROR] Unknown category: {category}")
            continue
        state = process_category(category, state, args.dry_run)

    # 状態保存
    if not args.dry_run:
        save_state(state)
        print("\nState saved.")

    print("\nDone!")


if __name__ == "__main__":
    main()