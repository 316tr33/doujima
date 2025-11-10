# フォーム統合ガイド

堂島フロント企画サイトのフォーム機能の実装詳細と統合方法を説明します。

## アーキテクチャ概要

```
┌─────────────────┐
│  HTML Form      │
│  (Frontend)     │
└────────┬────────┘
         │
         │ FormData (POST)
         ▼
┌─────────────────┐
│  form-handler.js│
│  (Validation)   │
└────────┬────────┘
         │
         │ POST /submit-contact
         ▼
┌─────────────────┐
│ Cloudflare Pages│
│   Functions     │
└────────┬────────┘
         │
         ├─► Turnstile 検証
         ├─► Honeypot 検証
         ├─► Rate Limiting (KV)
         ├─► Data Validation
         │
         ▼
┌─────────────────┐
│   Resend API    │
│  (Email送信)    │
└─────────────────┘
```

---

## 1. フロントエンド実装

### 1.1 お問い合わせフォーム (`index.html`)

**必須要素:**

```html
<!-- フォーム ID -->
<form id="contact-form">

  <!-- 必須フィールド -->
  <input type="text" name="company" required />
  <input type="text" name="name" required />
  <input type="email" name="email" required />
  <select name="service" required>
    <option value="ohenro">巡礼・先達手配</option>
    <option value="tokaido">ウォーキングガイド手配</option>
    <option value="consultation">サービス相談</option>
  </select>

  <!-- 任意フィールド -->
  <input type="tel" name="phone" />
  <input type="date" name="date" />
  <input type="number" name="participants" />
  <textarea name="message"></textarea>

  <!-- ハニーポット（非表示） -->
  <input type="text" name="website" style="display: none;" />

  <!-- プライバシーポリシー同意 -->
  <input type="checkbox" name="privacy" value="true" required />

  <!-- Turnstile ウィジェット -->
  <div class="cf-turnstile" data-sitekey="0x4AAAAAAB_1yaGfdV_epdP4"></div>

  <button type="submit">送信</button>
</form>

<!-- メッセージ表示エリア -->
<div id="contact-message" class="form-message"></div>
```

**スクリプト読み込み:**

```html
<head>
  <!-- Turnstile SDK -->
  <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
  <!-- CSS -->
  <link rel="stylesheet" href="css/components/form-message.css" />
</head>

<body>
  <!-- フォームハンドラー -->
  <script src="js/form-handler.js"></script>
</body>
```

### 1.2 採用応募フォーム (`recruit.html`)

**必須要素:**

```html
<form id="recruit-form">
  <!-- 必須フィールド -->
  <input type="text" name="name" required />
  <input type="text" name="kana" required />
  <input type="email" name="email" required />
  <input type="tel" name="phone" required />

  <!-- 応募職種（複数選択可能） -->
  <input type="checkbox" name="position" value="添乗員" />
  <input type="checkbox" name="position" value="アシスタント" />
  <input type="checkbox" name="position" value="先達" />
  <input type="checkbox" name="position" value="街道ウォークリーダー" />

  <!-- 任意フィールド -->
  <input type="number" name="age" />
  <input type="text" name="address" />
  <textarea name="experience"></textarea>
  <textarea name="motivation"></textarea>
  <textarea name="message"></textarea>

  <!-- ハニーポット、プライバシー、Turnstile -->
  <!-- (お問い合わせフォームと同様) -->
</form>

<div id="recruit-message" class="form-message"></div>
```

---

## 2. フロントエンド JavaScript (`js/form-handler.js`)

### 2.1 初期化処理

```javascript
// DOMContentLoaded 後に自動初期化
const contactForm = document.getElementById('contact-form');
const recruitForm = document.getElementById('recruit-form');

if (contactForm) {
  initializeForm(contactForm, '/submit-contact', 'contact');
}

if (recruitForm) {
  initializeForm(recruitForm, '/submit-recruit', 'recruit');
}
```

### 2.2 フォーム送信フロー

1. **クライアント側バリデーション**
   - 必須フィールドチェック
   - メールアドレス形式チェック
   - フリガナ（カタカナ）チェック
   - Turnstile トークン存在チェック

2. **FormData 作成**
   - `new FormData(form)` で全フィールドを取得
   - 応募職種は配列として処理

3. **POST リクエスト送信**
   ```javascript
   const response = await fetch(endpoint, {
     method: 'POST',
     body: formData
   });
   ```

4. **レスポンス処理**
   - 成功: メッセージ表示 + フォームリセット + Turnstile リセット
   - エラー: エラーメッセージ表示 + Turnstile リセット

5. **二重送信防止**
   - `isSubmitting` フラグで制御
   - ボタン無効化 + テキスト変更（「送信中...」）

---

## 3. バックエンド実装

### 3.1 お問い合わせフォーム (`functions/submit-contact.js`)

**処理フロー:**

1. **CORS 設定**
   - 同一オリジンのみ許可
   - OPTIONS リクエスト対応

2. **FormData パース**
   ```javascript
   const formData = await request.formData();
   const data = {};
   for (const [key, value] of formData.entries()) {
     data[key] = value;
   }
   ```

3. **ハニーポット検証**
   - `data.website` が空でない場合は403エラー

4. **Turnstile 検証**
   ```javascript
   const response = await fetch(
     'https://challenges.cloudflare.com/turnstile/v0/siteverify',
     {
       method: 'POST',
       body: JSON.stringify({
         secret: env.TURNSTILE_SECRET_KEY,
         response: turnstileToken,
         remoteip: clientIP
       })
     }
   );
   ```

5. **レート制限チェック**
   - KV に `ratelimit:contact:${clientIP}` をキーとして保存
   - 5分間に3回まで許可
   - TTL: 300秒

6. **データバリデーション**
   - 必須フィールド: company, name, email, service, privacy
   - メールアドレス形式: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
   - 電話番号形式: `/^[0-9\-\+\(\)\s]{10,20}$/`
   - 参加人数範囲: 1〜10000

7. **Resend API メール送信**
   ```javascript
   const response = await fetch('https://api.resend.com/emails', {
     method: 'POST',
     headers: {
       'Authorization': `Bearer ${env.RESEND_API_KEY}`,
       'Content-Type': 'application/json'
     },
     body: JSON.stringify({
       from: `堂島フロント企画 お問い合わせフォーム <${fromEmail}>`,
       to: [recipientEmail],
       subject: `【お問い合わせ】${data.company} - ${data.service}`,
       html: htmlBody
     })
   });
   ```

### 3.2 採用応募フォーム (`functions/submit-recruit.js`)

お問い合わせフォームとほぼ同様ですが、以下の違いがあります：

**バリデーション:**
- 必須フィールド: name, kana, email, phone, position, privacy
- フリガナチェック: `/^[ァ-ヶー\s]+$/`（全角カタカナのみ）
- 年齢範囲: 15〜100

**応募職種の処理:**
```javascript
// 複数選択対応
if (key === 'position') {
  if (!data.position) {
    data.position = [];
  }
  data.position.push(value);
}

// メール件名に使用
const positionText = Array.isArray(data.position)
  ? data.position.join('、')
  : data.position;
```

---

## 4. セキュリティ実装

### 4.1 多層防御

1. **Cloudflare Turnstile**
   - ボット検証（CAPTCHA 代替）
   - フロントエンド + バックエンドで二重検証

2. **ハニーポット**
   - 人間には見えない隠しフィールド
   - ボットが入力すると即座に403エラー

3. **レート制限**
   - IP ベース、5分間に3回まで
   - KV Namespace で状態管理
   - KV エラー時は処理継続（可用性優先）

4. **データバリデーション**
   - フロントエンド + バックエンドで二重チェック
   - 正規表現による形式検証
   - 数値範囲チェック

### 4.2 エラーハンドリング

**環境変数未設定:**
```javascript
if (!env.RESEND_API_KEY) {
  return { success: false, error: 'メール送信システムが正しく設定されていません' };
}
```

**KV エラー:**
```javascript
try {
  // KV 操作
} catch (error) {
  console.error('[レート制限] KVエラー:', error);
  return { allowed: true, count: 0 }; // 処理継続
}
```

**Resend API エラー:**
```javascript
if (!response.ok) {
  const errorText = await response.text();
  console.error('[Resend] APIエラー:', { status, error: errorText });
  return { success: false, error: 'メール送信に失敗しました' };
}
```

---

## 5. メールテンプレート

### 5.1 HTML メール構造

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <style>
    body { font-family: 'Noto Sans JP', sans-serif; }
    .header { background-color: #b8860b; color: white; }
    .field { margin-bottom: 15px; }
    .label { font-weight: bold; color: #b8860b; }
    .value { background-color: white; border-left: 3px solid #b8860b; }
  </style>
</head>
<body>
  <div class="header"><h2>堂島フロント企画 お問い合わせフォーム</h2></div>
  <div class="content">
    <!-- フィールド表示 -->
    <div class="field">
      <div class="label">会社名</div>
      <div class="value">${data.company}</div>
    </div>
    <!-- 繰り返し -->
  </div>
  <div class="footer">
    送信日時: ${timestamp}<br>
    送信元IP: ${clientIP}
  </div>
</body>
</html>
```

### 5.2 件名フォーマット

- **お問い合わせ**: `【お問い合わせ】${会社名} - ${サービス種別}`
- **採用応募**: `【採用応募】${氏名} - ${応募職種}`

---

## 6. トラブルシューティング

### 6.1 よくあるエラー

**"セキュリティ検証が完了していません"**
- Turnstile ウィジェットが読み込まれていない
- Site Key が正しくない
- ネットワークエラーで Turnstile API に接続できない

**"メール送信に失敗しました"**
- Resend API キーが設定されていない
- FROM_EMAIL が認証済みドメインでない
- Resend の送信制限（3,000通/月）を超過

**"送信回数が制限を超えました"**
- 同一 IP から5分間に3回以上送信
- 5分待つか、KV の該当キーを削除

### 6.2 デバッグ方法

**ローカル開発:**
```bash
# Wrangler でローカル実行
wrangler pages dev . --kv RATE_LIMIT

# ログ確認
# Console に詳細なログが出力されます
```

**本番環境:**
```bash
# Cloudflare ログ確認
wrangler pages deployment tail

# または Dashboard の「Logs」セクション
```

---

## 7. カスタマイズ方法

### 7.1 フォームフィールド追加

1. **HTML に追加**
   ```html
   <input type="text" name="new_field" />
   ```

2. **バリデーション追加** (`functions/submit-*.js`)
   ```javascript
   const requiredFields = {
     // ...既存
     new_field: '新しいフィールド'
   };
   ```

3. **メールテンプレート追加**
   ```javascript
   <div class="field">
     <div class="label">新しいフィールド</div>
     <div class="value">${data.new_field || '未入力'}</div>
   </div>
   ```

### 7.2 レート制限変更

`functions/submit-*.js` の定数を変更：

```javascript
const maxAttempts = 5; // 3 → 5 に変更
const windowSeconds = 600; // 5分 → 10分 に変更
```

### 7.3 メールテンプレート変更

`functions/submit-*.js` の `htmlBody` 変数を編集：

```javascript
const htmlBody = `
  <!-- カスタム HTML -->
`;
```

---

## 8. テストチェックリスト

### 8.1 フロントエンド

- [ ] 必須フィールド未入力で送信できないこと
- [ ] メールアドレス形式が正しくない場合エラーになること
- [ ] フリガナがカタカナ以外の場合エラーになること（採用フォーム）
- [ ] Turnstile チェック前は送信できないこと
- [ ] プライバシーポリシー未同意で送信できないこと

### 8.2 バックエンド

- [ ] ハニーポットに入力した場合403エラーになること
- [ ] Turnstile トークンが無効な場合403エラーになること
- [ ] レート制限（5分間に3回）が機能すること
- [ ] 必須フィールド未入力で400エラーになること
- [ ] メール送信が成功すること
- [ ] 受信先メールアドレスにメールが届くこと

### 8.3 セキュリティ

- [ ] CORS が同一オリジンのみ許可されていること
- [ ] API キーが環境変数から読み込まれていること
- [ ] エラーメッセージに機密情報が含まれていないこと

---

## 次のステップ

- [Cloudflare セットアップガイド](./cloudflare-setup.md) - Cloudflare の設定方法
- [デプロイガイド](./deployment-guide.md) - 本番環境へのデプロイ手順
- [クライアント引き継ぎガイド](./client-meeting-guide.md) - クライアントへの説明資料
