# CLAUDE.md

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

## Safety Rules
- Do not directly touch production environments or production data
- Never commit or expose `.env` files or secrets
- Always confirm before deleting or overwriting files
- Break large changes into smaller steps and proceed incrementally
- Confirm with me before adding external packages
- Confirm with me before making API calls or sending data externally

## Project Information

- Project purpose: 構造的類似性に基づく自動ニュースキュレーションシステム（バズではなく学び / エンゲージメントではなく構造）
- Technologies used: Python / GitHub Actions / Discord Webhooks / feedparser / requests
- Main folder structure:
  - `.github/workflows/` - GitHub Actions設定
  - `curate.py` - メインスクリプト
  - `config.py` - RSS/タグ/スコア設定
  - `state.json` - 状態保存（Git管理）
  - `requirements.txt` - 依存ライブラリ
- Files/folders not to touch:
  - `state.json`（ボット自身が管理、手動編集は原則禁止）

## Development Commands

```bash
python curate.py           # ローカル実行（テスト用）
python curate.py --dry-run # 投稿せずにスコアリング確認
```

## Environment Variables (GitHub Secrets)

```
DISCORD_WEBHOOK_SCIENCE
DISCORD_WEBHOOK_AI
DISCORD_WEBHOOK_EDUCATION
DISCORD_WEBHOOK_MYCOTECH
DISCORD_WEBHOOK_CURIOSITY
DEEPL_API_KEY          # DeepL API Free（タイトル日本語翻訳用）
```

## Implementation Phases

### Phase 1: MVP
- RSS取得（1カテゴリのみ）
- 2タグ判定（transformation, boundary_crossing）
- 単純スコアリング
- Discord投稿
- state.json保存

### Phase 2: フル機能
- 5カテゴリ対応
- 6タグ完全実装
- タグ多様性チェック
- pending/posted管理

### Phase 3: 最適化
- スコア調整
- キーワード辞書拡充
- エラーハンドリング強化

## Security Guidelines

- Webhookは必ずGitHub Secretsで管理（コードに直書き禁止）
- state.jsonに機密情報を含めない
- 外部APIへのリクエストは最小限に
- User-Agentを適切に設定（ボット識別のため）
- エラーログに機密情報を出力しない

## Free Operation Constraints

- **GitHub Actions**: 月2,000分無料枠内で運用（1日5分 × 30日 = 150分）
- **外部API**: 無料枠のみ使用、有料APIは禁止
- **LLM**: 使用禁止（コスト発生のため）
- **ストレージ**: リポジトリ内のstate.jsonのみ使用
- **依存ライブラリ**: 最小限に抑える（feedparser, requests のみ）

## Notes

- 完全無料・全自動・LLMなし
- RSS礼儀: User-Agent設定、リクエスト間隔1秒以上
- Discord Rate Limit: 問題なし（10投稿/日）
