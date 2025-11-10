# フォーム機能 技術リファレンス

トラブルシューティングや機能拡張時の技術参考資料

---

## システム構成

```
フロントエンド (index.html, recruit.html)
    ↓ FormData POST
form-handler.js (バリデーション)
    ↓ /submit-contact, /submit-recruit
Cloudflare Pages Functions (submit-*.js)
    ├→ Turnstile検証
    ├→ Honeypot検証
    ├→ Rate Limiting (KV)
    └→ Resend API (メール送信)
```

---

## 主要ファイル

### フロントエンド
- `index.html` - お問い合わせフォーム（`id="contact-form"`）
- `recruit.html` - 採用応募フォーム（`id="recruit-form"`）
- `js/form-handler.js` - フォーム送信処理（共通）
- `css/components/form-message.css` - メッセージ表示スタイル

### バックエンド
- `functions/submit-contact.js` - お問い合わせ送信処理
- `functions/submit-recruit.js` - 採用応募送信処理

### 設定
- `wrangler.toml` - Cloudflare Pages Functions設定
- `.dev.vars` - ローカル開発用環境変数（Gitignore済み）

---

## 環境変数

### 必須設定（Cloudflare Pages Environment Variables）

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `RESEND_API_KEY` | Resend APIキー | `re_...` |
| `FROM_EMAIL` | 送信元アドレス | `noreply@doujimafront.com` |
| `RECIPIENT_EMAIL` | 受信先アドレス | `info@doujimafront.com` |
| `TURNSTILE_SECRET_KEY` | Turnstile秘密鍵 | `0x4AAAAAAB_1ya...` |

### KV Namespace

| Binding | ID | 用途 |
|---------|-----|------|
| `RATE_LIMIT` | `b17668227fe14cd28bf6ff52f1f81ba1` | レート制限用ストレージ |

---

## セキュリティ機能

### 1. Cloudflare Turnstile
- **目的**: ボット対策（CAPTCHA代替）
- **Site Key**: `0x4AAAAAAB_1yaGfdV_epdP4`
- **検証**: フロントエンド（表示）+ バックエンド（検証）

### 2. Honeypot
- **目的**: スパムボット検出
- **実装**: 非表示フィールド `name="website"`
- **動作**: 入力があれば即座に403エラー

### 3. Rate Limiting
- **制限**: 同一IPから5分間に3回まで
- **ストレージ**: Workers KV（TTL: 300秒）
- **キー形式**: `ratelimit:contact:${clientIP}`

### 4. データバリデーション
- **フロントエンド**: HTML5 + JavaScript（即時フィードバック）
- **バックエンド**: 正規表現 + 型チェック（二重検証）

---

## API統合

### Resend API

**エンドポイント**: `https://api.resend.com/emails`

**リクエスト形式:**
```javascript
{
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${RESEND_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: {
    from: "堂島フロント企画 お問い合わせフォーム <noreply@doujimafront.com>",
    to: ["info@doujimafront.com"],
    subject: "【お問い合わせ】会社名 - サービス種別",
    html: "<html>...</html>"
  }
}
```

**レスポンス:**
```javascript
// 成功
{ "id": "email_id_here" }

// エラー
{ "message": "error description", "statusCode": 422 }
```

---

## バリデーションルール

### お問い合わせフォーム

| フィールド | 必須 | ルール |
|-----------|------|--------|
| 会社名 | ✓ | 1文字以上 |
| お名前 | ✓ | 1文字以上 |
| メールアドレス | ✓ | `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` |
| サービス | ✓ | ohenro/tokaido/consultation |
| 電話番号 | - | `/^[0-9\-\+\(\)\s]{10,20}$/` |
| 参加人数 | - | 1〜10000 |
| プライバシー同意 | ✓ | true |

### 採用応募フォーム

| フィールド | 必須 | ルール |
|-----------|------|--------|
| お名前 | ✓ | 1文字以上 |
| フリガナ | ✓ | `/^[ァ-ヶー\s]+$/`（全角カタカナのみ） |
| メールアドレス | ✓ | `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` |
| 電話番号 | ✓ | `/^[0-9\-\+\(\)\s]{10,20}$/` |
| 応募職種 | ✓ | 配列（1つ以上選択） |
| 年齢 | - | 15〜100 |
| プライバシー同意 | ✓ | true |

---

## エラーコード

### HTTP Status Codes

| Status | 意味 | 原因 |
|--------|------|------|
| 200 | 成功 | 正常処理 |
| 400 | Bad Request | バリデーションエラー |
| 403 | Forbidden | Turnstile失敗、Honeypot検出 |
| 405 | Method Not Allowed | POST以外のリクエスト |
| 429 | Too Many Requests | レート制限超過 |
| 500 | Internal Server Error | サーバーエラー |

### Turnstile Error Codes

| Code | 意味 | 対処 |
|------|------|------|
| `missing-input-secret` | Secret Key未設定 | 環境変数確認 |
| `invalid-input-secret` | Secret Key不正 | 値を再確認 |
| `missing-input-response` | トークン未送信 | フロントエンド確認 |
| `invalid-input-response` | トークン不正 | 期限切れの可能性 |
| `timeout-or-duplicate` | タイムアウト/重複 | ページ再読み込み |
| `hostname-mismatch` | ドメイン未登録 | Turnstile設定確認 |

---

## ローカル開発

### セットアップ

1. **環境変数ファイル作成** (`.dev.vars`)
```bash
RESEND_API_KEY=re_test_key
FROM_EMAIL=onboarding@resend.dev
RECIPIENT_EMAIL=test@example.com
TURNSTILE_SECRET_KEY=0x4AAAAAAB_1ya3SKxlzd7HV3dbnIFgKRdM
```

2. **ローカルサーバー起動**
```bash
wrangler pages dev . --kv RATE_LIMIT
```

3. **アクセス**
```
http://localhost:8788
```

### テスト用メールアドレス

Resendのテストドメイン `onboarding@resend.dev` を使用することで、
ドメイン認証なしでテスト可能。

---

## カスタマイズ

### フォームフィールド追加

1. **HTML修正** (`index.html` または `recruit.html`)
```html
<input type="text" name="new_field" />
```

2. **バリデーション追加** (`functions/submit-*.js`)
```javascript
const requiredFields = {
  // 既存フィールド...
  new_field: '新フィールド名'
};
```

3. **メールテンプレート追加** (`functions/submit-*.js`)
```html
<div class="field">
  <div class="label">新フィールド名</div>
  <div class="value">${data.new_field || '未入力'}</div>
</div>
```

### レート制限変更

`functions/submit-*.js` の定数を変更：
```javascript
const maxAttempts = 3;      // 回数
const windowSeconds = 300;  // 秒（5分）
```

---

## トラブルシューティング

### メール送信失敗

**症状**: 「メール送信に失敗しました」

**原因と対処:**
1. **RESEND_API_KEY未設定**
   - Cloudflare Pages環境変数を確認
   - Production環境に設定されているか確認

2. **FROM_EMAIL未認証**
   - Resend Dashboardでドメイン認証確認
   - Status: Verified になっているか

3. **RECIPIENT_EMAIL形式エラー**
   - 空白文字が含まれていないか確認
   - 正しいメール形式か確認

### Turnstile検証失敗

**症状**: 「セキュリティ検証に失敗しました」

**原因と対処:**
1. **ドメイン未登録**
   - Cloudflare Turnstile設定確認
   - 該当ドメインが登録されているか

2. **Secret Key不一致**
   - 環境変数のTURNSTILE_SECRET_KEY確認
   - Site Keyと対応する秘密鍵か確認

3. **トークン期限切れ**
   - ページを再読み込みして再送信

### レート制限誤動作

**症状**: 制限に達していないのに「送信回数が制限を超えました」

**原因と対処:**
1. **KV Namespace未バインド**
   - `wrangler.toml` のKV設定確認
   - Cloudflare DashboardでBinding確認

2. **キーが削除されない**
   - TTL設定（300秒）を確認
   - 手動でKVキーを削除

---

## 制限事項

### Resend無料プラン
- **月間送信数**: 3,000通まで
- **1日の送信数**: 100通まで
- **送信レート**: 10通/秒

### Workers KV
- **読み取り**: 1日100,000回まで（無料枠）
- **書き込み**: 1日1,000回まで（無料枠）
- **ストレージ**: 1GB まで（無料枠）

### Cloudflare Pages Functions
- **実行時間**: 最大10秒（CPU時間）
- **メモリ**: 128MB
- **リクエスト**: 1日100,000回まで（無料枠）

---

## 参考リンク

- **Resend API**: https://resend.com/docs/api-reference/emails/send-email
- **Cloudflare Turnstile**: https://developers.cloudflare.com/turnstile/
- **Workers KV**: https://developers.cloudflare.com/kv/
- **Pages Functions**: https://developers.cloudflare.com/pages/functions/

---

## 変更履歴

| 日付 | 変更内容 |
|------|---------|
| 2025-01-10 | 初版作成（Resend API統合） |
