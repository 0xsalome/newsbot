# News Curation Bot

**構造的類似性に基づく自動ニュースキュレーションシステム**

[![GitHub Actions](https://img.shields.io/badge/automation-GitHub%20Actions-2088FF?logo=github-actions)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/python-3.11-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 概要

このbotは、ニュース記事を**トピックではなく認識論的構造**で分類・キュレーションします。

「AI関連ニュース」や「科学ニュース」という従来の分類ではなく、記事が持つ**構造的パターン**（変容、境界横断、スケールの逆説など）を検出し、異なる分野の記事を同じ構造軸で並べます。

**設計思想**:
- 人気度やバイラル性ではなく、記事が持つ認識論的構造を優先
- LLMを使わず、ヒューリスティックとパターンマッチングで透明性を確保
- 完全無料で運用可能（GitHub Actions + Discord Webhook + DeepL API Free）

---

## 主な特徴

### 🏗️ 構造ベースのタグ付け

6つの構造タグで記事を分類：

| タグ | 説明 | 例 |
|------|------|-----|
| `transformation` | 価値の反転（毒→薬、失敗→発見） | 「がん治療の副作用が認知症予防に効果」 |
| `boundary_crossing` | 領域横断（生物×機械、科学×芸術） | 「菌糸体がコンピュータ回路として機能」 |
| `visibility_gain` | 観測不能→可能 | 「ブラックホール内部を初めて可視化」 |
| `value_redefinition` | 評価軸の移動 | 「ADHDは病気でなく認知スタイルの多様性」 |
| `scale_shift` | スケールの逆説 | 「1個の細胞が全身の炎症を引き起こす」 |
| `ontology_shift` | 人間観の揺らぎ | 「AIに著作権、創造性の再定義」 |

### 🌐 日本語翻訳

DeepL API Free を使用して記事タイトルを日本語に翻訳：
- 選択された記事のみ翻訳（API節約）
- 月50万文字無料枠（十分な余裕）

### 📊 透明なスコアリング

```python
最終スコア = 構造強度 × 0.5 + 話題性 × 0.5

構造強度 = Σ(タグスコア)
話題性 = ソース信頼度 + 鮮度
```

すべての判定基準は`config.py`で編集可能。

### 🔄 完全自動化

- **実行**: GitHub Actions（毎日UTC 0:00 / JST 9:00）
- **保存**: `state.json`（Git管理、7日間保持）
- **投稿**: Discord Webhook（5カテゴリ × 2記事/日）

---

## アーキテクチャ

```
┌─────────────────┐
│  GitHub Actions │ ← cron: 毎日実行
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RSS Fetcher    │ ← 20+ フィード取得
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Tagger         │ ← キーワード/パターンマッチ
│  (Heuristic)    │    ドメイン辞書、対義語ペア
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Scorer         │ ← 構造強度 × 話題性
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Selector       │ ← タグ多様性チェック
│  (Top 2/day)    │    pending管理
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Translator     │ ← DeepL API Free
│  (JA)           │    選択記事のみ翻訳
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Discord Poster │ ← Webhook経由で投稿
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  state.json     │ ← 重複防止、優先度管理
│  (Git commit)   │
└─────────────────┘
```

---

## セットアップ

### 1. 前提条件

- GitHubアカウント
- Discordサーバー（管理者権限）
- DeepLアカウント（無料）
- Python 3.11+（ローカルテスト用）

### 2. リポジトリのクローン

```bash
git clone https://github.com/0xsalome/newsbot.git
cd newsbot
```

### 3. Discord Webhook作成

各カテゴリ用に5つのWebhookを作成：

1. Discordサーバー設定 → 連携サービス → ウェブフック
2. チャンネルごとにWebhook作成（`#science`, `#ai`, `#education`, `#mycotech`, `#curiosity`）
3. Webhook URLをコピー

### 4. DeepL API Key取得

1. https://www.deepl.com/pro-api にアクセス
2. 無料アカウント作成
3. APIキーをコピー

### 5. GitHub Secrets設定

リポジトリの`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

```
DISCORD_WEBHOOK_SCIENCE=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_AI=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_EDUCATION=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_MYCOTECH=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_CURIOSITY=https://discord.com/api/webhooks/...
DEEPL_API_KEY=your_deepl_api_key
```

### 6. 初期化

```bash
# 依存関係インストール（ローカルテスト用）
pip install -r requirements.txt

# ドライラン（投稿せずにテスト）
python curate.py --dry-run --category science
```

### 7. 手動実行（テスト）

GitHub Actionsタブ → `Daily News Curation` → `Run workflow`

---

## ディレクトリ構成

```
newsbot/
├── .github/
│   └── workflows/
│       └── daily-curate.yml     # Cron設定
├── config.py                     # RSS/タグ/スコア定義
├── curate.py                     # メインスクリプト
├── state.json                    # 状態管理（Git追跡）
├── requirements.txt              # 依存ライブラリ
├── CLAUDE.md                     # AI設定（Claude用）
├── GEMINI.md                     # AI設定（Gemini用）
└── README.md
```

---

## 技術スタック

| 用途 | 技術 | 理由 |
|------|------|------|
| 実行環境 | GitHub Actions | 完全無料、cron対応 |
| RSS解析 | feedparser | 軽量、高速 |
| 翻訳 | DeepL API Free | 高品質、月50万文字無料 |
| タグ判定 | 正規表現 + 辞書 | 透明性、デバッグ容易 |
| 投稿 | Discord Webhook | 認証不要、シンプル |
| 状態管理 | JSON + Git | データベース不要 |

**依存ライブラリ**:
```txt
feedparser==6.0.10
requests==2.31.0
```

---

## RSS ソース（全て無料・ペイウォールなし）

### Science (5 feeds)
- Science Daily
- Phys.org
- EurekAlert
- arXiv (CS, Biology)

### AI (4 feeds)
- Hacker News
- The Verge AI
- VentureBeat AI
- TechCrunch AI

### Education (3 feeds)
- EdSurge
- Edsource
- The Hechinger Report

### Mycotech (4 feeds)
- Phys.org Biology
- Hacker News
- Anthropocene Magazine
- Science Daily Plants/Animals

### Curiosity (4 feeds)
- Atlas Obscura
- BBC Future
- Aeon
- Smithsonian Magazine

---

## タグ判定の仕組み

### 例: `transformation` タグ

**キーワード検出**:
```python
keywords = ["unexpectedly", "repurposed", "turned out", "paradoxically"]
if any(kw in title.lower() for kw in keywords):
    score += 3
```

**対義語ペア検出**:
```python
pairs = [("poison", "medicine"), ("failure", "success"), ("waste", "resource")]
if "poison" in text and "medicine" in text:
    score += 5
```

**スコアリング**:
- キーワード1つ: +3点
- 対義語ペア: +5点
- 否定→肯定パターン: +4点

### 例: `boundary_crossing` タグ

**ドメイン辞書**:
```python
domains = {
    "biology": ["protein", "DNA", "fungi", "mycelium"],
    "machine": ["algorithm", "AI", "circuit", "neural network"]
}
```

**判定**:
```python
detected_domains = []
for domain, keywords in domains.items():
    if any(kw in text for kw in keywords):
        detected_domains.append(domain)

if len(detected_domains) >= 2:
    score += 4  # 2ドメイン横断
```

---

## 投稿フォーマット

```
🔬 **Science** | 2026-01-07

**[transformation × visibility_gain]**
有害藻類ブルームの副産物が次世代太陽電池に電力を供給

🔗 https://sciencedaily.com/releases/2026/01/algae-solar.htm
📰 Science Daily | Score: 14.2
```

**要素**:
- カテゴリ絵文字（🔬🤖📚🍄🌍）
- タグの組み合わせ
- 記事タイトル（日本語翻訳済み）
- 元記事リンク
- ソース名 + スコア（透明性）

---

## 選択ロジック

### 1日2投稿/カテゴリの選び方

1. **新規 + pending記事をマージ**
2. **スコアソート**（降順）
3. **タグ多様性チェック**:
   ```python
   # 上位2件が同じタグ → 3位以降で異なるタグを探す
   if top1.tags == top2.tags:
       find_different_tag_from(rank_3_to_10)
   ```
4. **重複除外**（過去7日の投稿済みURL）
5. **pending更新**（3-10位を保存、3日以上古いものは削除）

---

## 設定のカスタマイズ

### スコア比率の変更

`config.py`:
```python
STRUCTURAL_WEIGHT = 0.5
TIMELINESS_WEIGHT = 0.5
# ← 構造重視なら 0.7 / 0.3 に変更
```

### タグキーワードの追加

`config.py`:
```python
TRANSFORMATION_KEYWORDS = [
    "unexpectedly", "repurposed", "turned out",
    "your_new_keyword"  # ← 追加
]
```

### ソース信頼度の調整

`config.py`:
```python
SOURCE_WEIGHT = {
    "arxiv.org": 5,
    "sciencedaily.com": 4,
    "your-favorite-source.com": 5  # ← 追加
}
```

---

## トラブルシューティング

### RSS取得に失敗

**症状**: GitHub Actionsログに `HTTP 403` や `Timeout`

**解決策**:
1. User-Agentを確認（`config.py`）
2. リトライ設定を確認（デフォルト3回）
3. 問題のあるフィードを一時的にコメントアウト

### Discord投稿が届かない

**症状**: Actionsは成功するが投稿されない

**解決策**:
1. Webhook URLが正しいか確認（Secretsを再設定）
2. Discord側のWebhookが削除されていないか確認
3. Rate limitに引っかかっていないか確認（1秒間隔を守る）

### 重複投稿が発生

**症状**: 同じ記事が複数回投稿される

**解決策**:
1. `state.json`が正しくcommitされているか確認
2. Git pushが失敗していないか確認（Actionsログ）
3. URL正規化処理を確認

### 翻訳されない

**症状**: タイトルが英語のまま

**解決策**:
1. `DEEPL_API_KEY`がSecretsに設定されているか確認
2. DeepL API Freeの月間制限を確認
3. Actionsログで翻訳エラーを確認

---

## パフォーマンス

### 実行時間
- RSS取得: 約2分（20フィード、1秒間隔）
- タグ判定: 約30秒（100記事）
- スコアリング: 約10秒
- 翻訳: 約5秒（10記事）
- Discord投稿: 約10秒（10投稿、1秒間隔）
- **合計: 約3-5分/日**

### コスト
- GitHub Actions: **0円**（2,000分/月の無料枠、月間150分使用）
- Discord Webhook: **0円**
- DeepL API Free: **0円**（月50万文字無料枠）
- RSS取得: **0円**
- **総コスト: 0円**

---

## 拡張のアイデア

### 短期（実装が容易）
- [ ] ログ記録（タグ判定の詳細）
- [ ] 週次サマリー投稿（タグの統計）
- [ ] カテゴリの追加（環境、宇宙など）
- [ ] キーワード辞書の自動拡張

### 中期（要設計）
- [ ] Web UI（記事一覧、タグ統計）
- [ ] ペイウォール検出（有料記事を除外）
- [ ] 記事のクラスタリング（同一構造の複数ソース）
- [ ] タグごとの RSS フィード生成

### 長期（有料化が必要）
- [ ] LLM統合（Claude/GPT-4でタグ精度向上）
- [ ] 記事要約生成
- [ ] ユーザーフィードバック学習

---

## 貢献

Issue、Pull Request歓迎です。

特に以下の貢献を求めています：
- タグ判定精度の向上（キーワード追加、パターン改善）
- 新しいRSSソースの提案（無料・ペイウォールなし必須）
- ドメイン辞書の拡充
- バグ報告

---

## ライセンス

MIT License

---

## 謝辞

このプロジェクトは、「ニュースをトピックではなく認識論的構造で分類する」という編集思想に基づいて設計されました。

エンゲージメント指標に依存しない、透明で検証可能なキュレーションシステムを目指しています。

---

## 関連リンク

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Discord Webhooks Guide](https://discord.com/developers/docs/resources/webhook)
- [DeepL API Documentation](https://www.deepl.com/docs-api)
- [feedparser Documentation](https://feedparser.readthedocs.io/)

---

**質問・提案**: [Issues](https://github.com/0xsalome/newsbot/issues)
