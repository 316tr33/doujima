# Cloudflare Pages Functions セットアップガイド

## 概要

堂島フロント企画のフォーム送信処理をCloudflare Pages FunctionsとMailChannels APIで実装しています。

## 実装済みファイル

### 1. `/functions/submit-contact.js`
お問い合わせフォーム送信処理
- エンドポイント: `https://yourdomain.com/submit-contact`

### 2. `/functions/submit-recruit.js`
採用応募フォーム送信処理
- エンドポイント: `https://yourdomain.com/submit-recruit`

## 必要な環境変数

Cloudflare Pagesのダッシュボードで以下の環境変数を設定してください。

### 1. RECIPIENT_EMAIL（必須）
フォーム送信先のメールアドレス

```
例: contact@doujimafront.com
```

### 2. FROM_EMAIL（必須）
送信元メールアドレス

```
例: noreply@doujimafront.com
```

### 3. TURNSTILE_SECRET_KEY（必須）
Cloudflare Turnstileのシークレットキー

```
取得方法:
1. Cloudflareダッシュボード → Turnstile
2. サイト作成（またはExisting site）
3. Secret Keyをコピー
```

### 4. RATE_LIMIT（必須）
Workers KV Namespaceの設定

```
設定方法:
1. Cloudflareダッシュボード → Workers & Pages → KV
2. "Create a namespace"ボタンをクリック
3. Namespace name: "RATE_LIMIT"
4. Pagesプロジェクトの設定 → Functions → KV Namespace Bindings
5. Variable name: "RATE_LIMIT"、KV namespace: 作成したNamespaceを選択
```

## Cloudflare Pages 環境変数設定手順

### ステップ1: Pagesダッシュボードにアクセス

1. Cloudflareダッシュボードにログイン
2. **Workers & Pages** を選択
3. 該当のプロジェクトを選択
4. **Settings** タブをクリック
5. **Environment variables** セクションを開く

### ステップ2: 環境変数を追加

**Production（本番環境）:**

| Variable name | Value | Type |
|--------------|-------|------|
| RECIPIENT_EMAIL | contact@doujimafront.com | Plain text |
| FROM_EMAIL | noreply@doujimafront.com | Plain text |
| TURNSTILE_SECRET_KEY | [Turnstileから取得] | Secret |

**Preview（プレビュー環境）:**

開発・テスト用に別のメールアドレスを設定することを推奨

| Variable name | Value | Type |
|--------------|-------|------|
| RECIPIENT_EMAIL | dev@doujimafront.com | Plain text |
| FROM_EMAIL | noreply-dev@doujimafront.com | Plain text |
| TURNSTILE_SECRET_KEY | [Turnstileから取得] | Secret |

### ステップ3: KV Namespace Bindingを追加

1. **Settings** → **Functions** → **KV Namespace Bindings**
2. **Add binding** をクリック
3. Variable name: `RATE_LIMIT`
4. KV namespace: 事前に作成したNamespaceを選択
5. **Save** をクリック

## MailChannels設定（Cloudflare Pages専用）

Cloudflare PagesではMailChannels APIが無料で利用可能です。追加設定は不要ですが、送信元ドメインの設定が推奨されます。

### SPFレコード設定（推奨）

ドメインのDNS設定に以下のSPFレコードを追加:

```
Type: TXT
Name: @
Content: v=spf1 include:_spf.mx.cloudflare.net ~all
```

### DKIMレコード設定（推奨）

MailChannelsから提供されるDKIM設定を追加:

```
詳細: https://support.mailchannels.com/hc/en-us/articles/200262610-DKIM-Authentication
```

## Turnstile設定

### サイト作成

1. Cloudflareダッシュボード → **Turnstile**
2. **Add site** をクリック
3. サイト設定:
   - **Site name**: 堂島フロント企画フォーム
   - **Domain**: doujimafront.com（本番ドメイン）
   - **Widget Mode**: Managed
   - **Pre-Clearance**: Disabled

### HTMLへの実装

フォームに以下のスクリプトを追加:

```html
<!-- Turnstileスクリプト -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<!-- フォーム内 -->
<div class="cf-turnstile"
     data-sitekey="YOUR_SITE_KEY"
     data-callback="onTurnstileSuccess"
     data-error-callback="onTurnstileError">
</div>
```

### JavaScript実装例

```javascript
// Turnstile検証成功時
function onTurnstileSuccess(token) {
  console.log('Turnstile検証成功');
  document.getElementById('submit-btn').disabled = false;
}

// Turnstile検証エラー時
function onTurnstileError(error) {
  console.error('Turnstile検証失敗:', error);
  alert('セキュリティ検証に失敗しました。ページを再読み込みしてください。');
}
```

## テスト手順

### 1. ローカルテスト（Wrangler CLI使用）

```bash
# Cloudflare Wranglerインストール
npm install -g wrangler

# ローカル開発サーバー起動
wrangler pages dev .

# テストリクエスト送信
curl -X POST http://localhost:8788/submit-contact \
  -H "Content-Type: application/json" \
  -d '{
    "company": "テスト株式会社",
    "name": "山田太郎",
    "email": "test@example.com",
    "phone": "090-1234-5678",
    "service": "お遍路事業",
    "date": "2025-12-01",
    "participants": 10,
    "message": "テストメッセージ",
    "privacy": true,
    "cf-turnstile-response": "test-token"
  }'
```

### 2. プレビュー環境テスト

1. Gitにプッシュしてプレビューデプロイ作成
2. プレビューURL経由でフォーム送信テスト
3. 環境変数が正しく設定されているか確認

### 3. 本番環境テスト

1. mainブランチにマージして本番デプロイ
2. 本番ドメイン経由でフォーム送信テスト
3. メール受信確認

## トラブルシューティング

### メール送信失敗（500エラー）

**原因:**
- MailChannels APIエラー
- 環境変数の設定ミス
- FROM_EMAILドメイン不一致

**対処法:**
1. Cloudflare Pagesのログを確認
2. 環境変数が正しく設定されているか確認
3. FROM_EMAILのドメインがデプロイドメインと一致しているか確認

### Turnstile検証失敗（403エラー）

**原因:**
- TURNSTILE_SECRET_KEYが間違っている
- サイトキーとシークレットキーの不一致
- ドメイン制限設定ミス

**対処法:**
1. Turnstileダッシュボードでサイトキーとシークレットキーを再確認
2. ドメイン設定を確認（本番/プレビュー両方許可）

### レート制限エラー（429エラー）

**原因:**
- 5分間に3回以上の送信
- KV Namespace設定ミス

**対処法:**
1. 5分待ってから再試行
2. KV Namespace Bindingsが正しく設定されているか確認
3. テスト時は一時的にレート制限を無効化（コード修正）

### CORS エラー

**原因:**
- 異なるオリジンからのリクエスト
- プリフライトリクエストの失敗

**対処法:**
1. フォームとAPIが同一ドメインにあるか確認
2. ブラウザのコンソールでCORSエラー詳細を確認
3. 必要に応じてcorsHeadersを調整

## セキュリティ考慮事項

### 実装済みセキュリティ機能

1. **Turnstile検証**: ボット対策
2. **ハニーポット**: スパムボット検出
3. **レート制限**: DoS攻撃対策（5分間に3回まで）
4. **データバリデーション**: インジェクション攻撃対策
5. **CORS制限**: 同一オリジンのみ許可

### 追加推奨事項

1. **CSP（Content Security Policy）設定**
   - HTMLヘッダーにCSPを追加

2. **HTTPS強制**
   - Cloudflare Pagesはデフォルトで有効

3. **ログ監視**
   - Cloudflare Logsで異常なトラフィックを監視

4. **定期的なシークレットキーローテーション**
   - TURNSTILE_SECRET_KEYを定期的に更新

## 監視とメンテナンス

### ログ確認方法

1. Cloudflareダッシュボード → Workers & Pages
2. 該当プロジェクト → **Logs** タブ
3. Functionsのログをリアルタイム確認

### アラート設定（推奨）

1. Cloudflare Analytics → Workers Analyticsを有効化
2. エラー率が一定値を超えたらアラート通知
3. メール通知やSlack連携を設定

### 定期メンテナンス項目

- [ ] 月次: KV Namespaceの使用量確認
- [ ] 月次: メール送信成功率の確認
- [ ] 四半期: Turnstileシークレットキーのローテーション
- [ ] 四半期: ログの異常パターン分析

## サポート情報

### 公式ドキュメント

- **Cloudflare Pages Functions**: https://developers.cloudflare.com/pages/functions/
- **MailChannels API**: https://mailchannels.zendesk.com/hc/en-us/articles/4565898358413
- **Cloudflare Turnstile**: https://developers.cloudflare.com/turnstile/
- **Workers KV**: https://developers.cloudflare.com/kv/

### 問題報告

プロジェクト固有の問題は開発チームに連絡してください。
