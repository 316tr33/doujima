# 開発ドキュメント

このディレクトリには、堂島フロント企画ウェブサイトの開発・メンテナンスに関するドキュメントを格納しています。

## 📋 ドキュメント一覧

### フォーム機能実装ガイド（新規追加）

- [`deployment-guide.md`](./deployment-guide.md) - **デプロイ手順書**
  - Cloudflare Pages プロジェクト作成
  - 環境変数設定
  - Workers KV Namespace作成
  - Cloudflare Turnstile設定
  - デプロイ実行とトラブルシューティング

- [`dns-setup-guide.md`](./dns-setup-guide.md) - **DNS設定手順書**
  - DNS移行の概要と方式比較
  - 方式A: DNSをCloudflareに移行（推奨）
  - 方式B: お名前.comのDNSを継続使用
  - トラブルシューティング

- [`client-meeting-guide.md`](./client-meeting-guide.md) - **クライアント会議用資料**
  - 会議の目的と準備
  - 会議アジェンダ（90分）
  - デモシナリオとチェックリスト
  - 想定Q&A

- [`testing-guide.md`](./testing-guide.md) - **テスト手順書**
  - ローカルテスト（wrangler dev）
  - 機能テスト（フォーム送信、バリデーション、スパム対策）
  - レスポンシブテスト
  - ブラウザテスト
  - アクセシビリティテスト
  - セキュリティテスト
  - パフォーマンステスト
  - メール送信テスト

### Cloudflare設定

- [`cloudflare-setup.md`](./cloudflare-setup.md) - Cloudflare Pages Functions セットアップガイド
- [`form-integration-guide.md`](./form-integration-guide.md) - フォーム統合ガイド

### テスト・品質管理

- [`responsive-testing.md`](./responsive-testing.md) - レスポンシブ対応確認チェックリスト
- [`playwright-screenshot-guide.md`](./playwright-screenshot-guide.md) - Playwrightスクリーンショットガイド

## 📁 ディレクトリ構造との関係

```
doujima/
├── docs/              # 開発ドキュメント（このディレクトリ）
├── refactoring-docs/  # 特定リファクタリングプロジェクト用
├── CLAUDE.md          # Claude Code用プロジェクト設定
└── ...               # その他のプロジェクトファイル
```

## 🔄 メンテナンス

- ドキュメントは開発フローに応じて随時更新
- 新しい開発手順やガイドラインは適切なカテゴリに分類して追加