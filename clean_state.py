
import json
import config
from urllib.parse import urlparse

def clean_state():
    with open("state.json", "r", encoding="utf-8") as f:
        state = json.load(f)

    cleaned_count = 0
    
    # 全カテゴリについてチェック
    for category in config.CATEGORIES:
        allowed_sources = []
        # RSS URLからドメインを抽出して許可リストを作成
        for rss_url in config.RSS_SOURCES.get(category, []):
            domain = urlparse(rss_url).netloc
            allowed_sources.append(domain)
            
        # pendingリストをクリーニング
        if category in state["pending"]:
            original_len = len(state["pending"][category])
            # 許可されたソースを含むか、ソース情報がない（念のため残す）記事のみ保持
            # ただし、GitHub Trendingなどの特定ドメインは明示的に排除
            
            new_pending = []
            for article in state["pending"][category]:
                source = article.get("source", "")
                # 明示的に削除したいドメイン
                if "mshibanami.github.io" in source or "hackernews" in source or "ycombinator" in source:
                    continue
                new_pending.append(article)
            
            state["pending"][category] = new_pending
            cleaned_count += original_len - len(new_pending)

    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f"Cleaned {cleaned_count} items from pending state.")

if __name__ == "__main__":
    clean_state()
