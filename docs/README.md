# 開発ドキュメント

堂島フロント企画ウェブサイトの開発・保守・納品に関するドキュメント

---

## 📋 ドキュメント一覧

### 納品作業
- **[`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md)** - 現地納品作業チェックリスト（最重要）
  - 所要時間: 30-45分
  - Resend設定、DNS移管、環境変数設定、最終テスト
  - トラブルシューティング対応手順

### 技術リファレンス
- **[`FORM_TECHNICAL_REFERENCE.md`](./FORM_TECHNICAL_REFERENCE.md)** - フォーム機能の技術詳細
  - システム構成、環境変数、セキュリティ機能
  - API統合、バリデーションルール、エラーコード
  - カスタマイズ方法、トラブルシューティング

### 開発補助
- **[`responsive-testing.md`](./responsive-testing.md)** - レスポンシブ対応テストチェックリスト
  - デバイスサイズ別確認項目
  - 主要ブレークポイント（1024px, 768px, 480px, 375px）

- **[`playwright-screenshot-guide.md`](./playwright-screenshot-guide.md)** - スクリーンショット撮影ガイド
  - Playwright MCPを使用したスクリーンショット取得方法
  - JPEG形式推奨（5MB制限対策）

---

## 🎯 用途別ガイド

### クライアント先での納品作業時
→ **`DEPLOYMENT_CHECKLIST.md`** を印刷またはタブレットで表示

### トラブルシューティング時
→ **`FORM_TECHNICAL_REFERENCE.md`** のトラブルシューティング章を参照

### レスポンシブ修正時
→ **`responsive-testing.md`** で全デバイスサイズをテスト

### 機能拡張時
→ **`FORM_TECHNICAL_REFERENCE.md`** のカスタマイズ章を参照

---

## 📁 プロジェクト構造

```
doujima/
├── docs/                          # 開発ドキュメント（このディレクトリ）
│   ├── DEPLOYMENT_CHECKLIST.md   # 納品作業手順
│   ├── FORM_TECHNICAL_REFERENCE.md # 技術詳細
│   ├── responsive-testing.md      # レスポンシブテスト
│   └── playwright-screenshot-guide.md
│
├── functions/                     # Cloudflare Pages Functions
│   ├── submit-contact.js          # お問い合わせ処理
│   └── submit-recruit.js          # 採用応募処理
│
├── js/
│   └── form-handler.js            # フロントエンドフォーム処理
│
├── css/
│   ├── base/                      # 基盤CSS（変数、リセット、タイポグラフィ）
│   ├── components/                # コンポーネントCSS（ナビ、ボタン、カード等）
│   └── pages/                     # ページ別CSS
│
├── index.html                     # 企業ホームページ
├── recruit.html                   # 採用情報ページ
├── privacy-policy.html            # プライバシーポリシー
│
├── Ohenro/                        # お遍路事業サイト
│   ├── index.html
│   └── shikoku.html
│
├── Tokaido/                       # 東海道ウォーク事業サイト
│   └── index.html
│
├── wrangler.toml                  # Cloudflare Pages設定
├── .dev.vars                      # ローカル環境変数（Gitignore）
└── CLAUDE.md                      # Claude Code用プロジェクト設定
```

---

## 🔑 重要な技術情報

### フォーム機能の概要

**お問い合わせフォーム** (`index.html`)
- 企業・団体向けのサービス相談受付
- サービス種別選択（巡礼、東海道、その他）

**採用応募フォーム** (`recruit.html`)
- 添乗員、先達、アシスタント等の募集
- 複数職種の同時応募可能

### セキュリティ対策

1. **Cloudflare Turnstile**: ボット対策（CAPTCHA代替）
2. **Honeypot**: 非表示フィールドでスパム検出
3. **Rate Limiting**: IP単位で5分間に3回まで制限
4. **二重バリデーション**: フロントエンド + バックエンド

### 使用サービス

- **Cloudflare Pages**: ホスティング + サーバーレス関数
- **Cloudflare Turnstile**: ボット対策
- **Cloudflare Workers KV**: レート制限用ストレージ
- **Resend**: メール送信API（無料: 3,000通/月）

---

## 🚀 クイックスタート

### ローカル開発環境

```bash
# 1. Wranglerインストール（初回のみ）
npm install -g wrangler

# 2. 環境変数ファイル作成
cp .dev.vars.example .dev.vars
# 必要な値を設定（RESEND_API_KEY等）

# 3. ローカルサーバー起動
wrangler pages dev . --kv RATE_LIMIT

# 4. ブラウザでアクセス
open http://localhost:8788
```

### Production環境

- **URL**: https://doujimafront.com（納品後）
- **テストURL**: https://d92d129b.doujima.pages.dev
- **管理**: Cloudflare Dashboard

---

## 📞 サポート情報

### トラブル時の確認順序

1. **Cloudflare Pages Logs** でエラー詳細を確認
2. **FORM_TECHNICAL_REFERENCE.md** のトラブルシューティング章を参照
3. **環境変数** が正しく設定されているか確認
4. **DNS伝播** が完了しているか確認（最大24時間）

### よくある問題

| 症状 | 原因 | 対処 |
|------|------|------|
| メールが届かない | Resendドメイン未認証 | Resend Dashboardで確認 |
| Turnstile失敗 | ドメイン未登録 | Turnstile設定で追加 |
| 403エラー | Secret Key不正 | 環境変数を再確認 |
| レート制限誤動作 | KV未バインド | wrangler.toml確認 |

---

## 📝 メンテナンス履歴

| 日付 | 内容 |
|------|------|
| 2025-01-10 | フォーム機能実装（Resend API統合） |
| 2025-01-10 | ドキュメント整理（納品準備） |

---

## 🔗 関連リンク

- **GitHub**: https://github.com/316tr33/doujima
- **Cloudflare Dashboard**: https://dash.cloudflare.com/
- **Resend Dashboard**: https://resend.com/
