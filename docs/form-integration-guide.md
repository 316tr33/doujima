# フォーム送信 JavaScript実装ガイド

## 概要

Cloudflare Pages Functionsで実装されたフォーム送信APIの呼び出し方法を説明します。

## 共通実装パターン

### 1. Turnstileウィジェット設定

```html
<!-- HTMLヘッダーにTurnstileスクリプトを追加 -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<!-- フォーム内にウィジェットを配置 -->
<div class="cf-turnstile"
     data-sitekey="YOUR_SITE_KEY"
     data-callback="onTurnstileSuccess"
     data-error-callback="onTurnstileError"
     data-theme="light">
</div>
```

### 2. ハニーポットフィールド

```html
<!-- CSS で非表示にするスパムボット対策フィールド -->
<input type="text"
       name="website"
       id="website"
       class="honeypot"
       tabindex="-1"
       autocomplete="off"
       aria-hidden="true">

<style>
  .honeypot {
    position: absolute;
    left: -9999px;
    width: 1px;
    height: 1px;
    opacity: 0;
    pointer-events: none;
  }
</style>
```

## お問い合わせフォーム実装

### HTML構造

```html
<form id="contact-form" class="contact-form">
  <!-- 会社名 -->
  <div class="form-group">
    <label for="company">会社名 <span class="required">*</span></label>
    <input type="text" id="company" name="company" required>
  </div>

  <!-- ご担当者名 -->
  <div class="form-group">
    <label for="name">ご担当者名 <span class="required">*</span></label>
    <input type="text" id="name" name="name" required>
  </div>

  <!-- メールアドレス -->
  <div class="form-group">
    <label for="email">メールアドレス <span class="required">*</span></label>
    <input type="email" id="email" name="email" required>
  </div>

  <!-- 電話番号 -->
  <div class="form-group">
    <label for="phone">電話番号</label>
    <input type="tel" id="phone" name="phone">
  </div>

  <!-- サービス選択 -->
  <div class="form-group">
    <label for="service">ご希望サービス <span class="required">*</span></label>
    <select id="service" name="service" required>
      <option value="">選択してください</option>
      <option value="お遍路事業">お遍路事業</option>
      <option value="東海道ウォーク事業">東海道ウォーク事業</option>
      <option value="その他">その他</option>
    </select>
  </div>

  <!-- 希望実施日 -->
  <div class="form-group">
    <label for="date">希望実施日</label>
    <input type="date" id="date" name="date">
  </div>

  <!-- 参加予定人数 -->
  <div class="form-group">
    <label for="participants">参加予定人数</label>
    <input type="number" id="participants" name="participants" min="1" max="10000">
  </div>

  <!-- ご要望・詳細 -->
  <div class="form-group">
    <label for="message">ご要望・詳細</label>
    <textarea id="message" name="message" rows="5"></textarea>
  </div>

  <!-- プライバシーポリシー同意 -->
  <div class="form-group">
    <label class="checkbox-label">
      <input type="checkbox" id="privacy" name="privacy" required>
      <a href="/privacy.html" target="_blank">プライバシーポリシー</a>に同意する
      <span class="required">*</span>
    </label>
  </div>

  <!-- ハニーポット -->
  <input type="text" name="website" id="website" class="honeypot" tabindex="-1" autocomplete="off">

  <!-- Turnstile -->
  <div class="cf-turnstile"
       data-sitekey="YOUR_SITE_KEY"
       data-callback="onContactTurnstileSuccess"
       data-error-callback="onTurnstileError">
  </div>

  <!-- 送信ボタン -->
  <button type="submit" id="contact-submit-btn" disabled>
    送信する
  </button>

  <!-- ローディング表示 -->
  <div id="contact-loading" class="loading" style="display: none;">
    送信中...
  </div>

  <!-- メッセージ表示エリア -->
  <div id="contact-message" class="message"></div>
</form>
```

### JavaScript実装

```javascript
// Turnstile検証成功コールバック
let contactTurnstileToken = null;

function onContactTurnstileSuccess(token) {
  contactTurnstileToken = token;
  document.getElementById('contact-submit-btn').disabled = false;
  console.log('Turnstile検証成功');
}

function onTurnstileError(error) {
  console.error('Turnstile検証失敗:', error);
  showMessage('contact-message', 'error', 'セキュリティ検証に失敗しました。ページを再読み込みしてください。');
}

// フォーム送信処理
document.getElementById('contact-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  // Turnstileトークンチェック
  if (!contactTurnstileToken) {
    showMessage('contact-message', 'error', 'セキュリティ検証を完了してください。');
    return;
  }

  // ローディング表示
  const submitBtn = document.getElementById('contact-submit-btn');
  const loading = document.getElementById('contact-loading');
  const messageDiv = document.getElementById('contact-message');

  submitBtn.disabled = true;
  loading.style.display = 'block';
  messageDiv.textContent = '';

  // フォームデータ収集
  const formData = {
    company: document.getElementById('company').value.trim(),
    name: document.getElementById('name').value.trim(),
    email: document.getElementById('email').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    service: document.getElementById('service').value,
    date: document.getElementById('date').value,
    participants: document.getElementById('participants').value,
    message: document.getElementById('message').value.trim(),
    privacy: document.getElementById('privacy').checked,
    website: document.getElementById('website').value, // ハニーポット
    'cf-turnstile-response': contactTurnstileToken,
  };

  try {
    // API呼び出し
    const response = await fetch('/submit-contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();

    if (response.ok && result.success) {
      // 成功時
      showMessage('contact-message', 'success', result.message);
      document.getElementById('contact-form').reset();

      // Turnstileリセット
      if (window.turnstile) {
        window.turnstile.reset();
      }
      contactTurnstileToken = null;
      submitBtn.disabled = true;

      // Google Analytics イベント送信（オプション）
      if (window.gtag) {
        gtag('event', 'form_submission', {
          form_name: 'contact',
          service: formData.service,
        });
      }
    } else {
      // エラー時
      showMessage('contact-message', 'error', result.error || 'エラーが発生しました。');

      // Turnstileリセット
      if (window.turnstile) {
        window.turnstile.reset();
      }
      contactTurnstileToken = null;
      submitBtn.disabled = true;
    }
  } catch (error) {
    console.error('送信エラー:', error);
    showMessage('contact-message', 'error', 'ネットワークエラーが発生しました。インターネット接続を確認してください。');
  } finally {
    loading.style.display = 'none';
    submitBtn.disabled = false;
  }
});

// メッセージ表示ヘルパー関数
function showMessage(elementId, type, message) {
  const messageDiv = document.getElementById(elementId);
  messageDiv.textContent = message;
  messageDiv.className = `message ${type}`;
  messageDiv.style.display = 'block';

  // 成功メッセージは5秒後に非表示
  if (type === 'success') {
    setTimeout(() => {
      messageDiv.style.display = 'none';
    }, 5000);
  }
}
```

### CSS スタイル

```css
/* フォームスタイル */
.contact-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.required {
  color: #d4af37;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  resize: vertical;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
}

/* 送信ボタン */
button[type="submit"] {
  width: 100%;
  padding: 1rem;
  background-color: #d4af37;
  color: #000;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"]:hover:not(:disabled) {
  background-color: #b8860b;
}

button[type="submit"]:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* ローディング */
.loading {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

/* メッセージ */
.message {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
  display: none;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* ハニーポット（非表示） */
.honeypot {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}
```

## 採用応募フォーム実装

### HTML構造

```html
<form id="recruit-form" class="recruit-form">
  <!-- お名前 -->
  <div class="form-group">
    <label for="recruit-name">お名前 <span class="required">*</span></label>
    <input type="text" id="recruit-name" name="name" required>
  </div>

  <!-- フリガナ -->
  <div class="form-group">
    <label for="kana">フリガナ <span class="required">*</span></label>
    <input type="text" id="kana" name="kana" required placeholder="ヤマダタロウ">
  </div>

  <!-- メールアドレス -->
  <div class="form-group">
    <label for="recruit-email">メールアドレス <span class="required">*</span></label>
    <input type="email" id="recruit-email" name="email" required>
  </div>

  <!-- 電話番号 -->
  <div class="form-group">
    <label for="recruit-phone">電話番号 <span class="required">*</span></label>
    <input type="tel" id="recruit-phone" name="phone" required>
  </div>

  <!-- 年齢 -->
  <div class="form-group">
    <label for="age">年齢</label>
    <input type="number" id="age" name="age" min="15" max="100">
  </div>

  <!-- 住所 -->
  <div class="form-group">
    <label for="address">住所</label>
    <input type="text" id="address" name="address">
  </div>

  <!-- 希望職種（複数選択） -->
  <div class="form-group">
    <label>希望職種 <span class="required">*</span></label>
    <label class="checkbox-label">
      <input type="checkbox" name="position" value="先達（ガイド）"> 先達（ガイド）
    </label>
    <label class="checkbox-label">
      <input type="checkbox" name="position" value="事業企画"> 事業企画
    </label>
    <label class="checkbox-label">
      <input type="checkbox" name="position" value="営業"> 営業
    </label>
    <label class="checkbox-label">
      <input type="checkbox" name="position" value="事務"> 事務
    </label>
  </div>

  <!-- 関連経験・資格 -->
  <div class="form-group">
    <label for="experience">関連経験・資格</label>
    <textarea id="experience" name="experience" rows="4"></textarea>
  </div>

  <!-- 応募理由・自己PR -->
  <div class="form-group">
    <label for="motivation">応募理由・自己PR</label>
    <textarea id="motivation" name="motivation" rows="5"></textarea>
  </div>

  <!-- その他・ご質問 -->
  <div class="form-group">
    <label for="recruit-message">その他・ご質問</label>
    <textarea id="recruit-message" name="message" rows="4"></textarea>
  </div>

  <!-- プライバシーポリシー同意 -->
  <div class="form-group">
    <label class="checkbox-label">
      <input type="checkbox" id="recruit-privacy" name="privacy" required>
      <a href="/privacy.html" target="_blank">プライバシーポリシー</a>に同意する
      <span class="required">*</span>
    </label>
  </div>

  <!-- ハニーポット -->
  <input type="text" name="website" id="recruit-website" class="honeypot" tabindex="-1" autocomplete="off">

  <!-- Turnstile -->
  <div class="cf-turnstile"
       data-sitekey="YOUR_SITE_KEY"
       data-callback="onRecruitTurnstileSuccess"
       data-error-callback="onTurnstileError">
  </div>

  <!-- 送信ボタン -->
  <button type="submit" id="recruit-submit-btn" disabled>
    応募する
  </button>

  <!-- ローディング表示 -->
  <div id="recruit-loading" class="loading" style="display: none;">
    送信中...
  </div>

  <!-- メッセージ表示エリア -->
  <div id="recruit-message" class="message"></div>
</form>
```

### JavaScript実装

```javascript
// Turnstile検証成功コールバック
let recruitTurnstileToken = null;

function onRecruitTurnstileSuccess(token) {
  recruitTurnstileToken = token;
  document.getElementById('recruit-submit-btn').disabled = false;
  console.log('Turnstile検証成功');
}

// フォーム送信処理
document.getElementById('recruit-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  // Turnstileトークンチェック
  if (!recruitTurnstileToken) {
    showMessage('recruit-message', 'error', 'セキュリティ検証を完了してください。');
    return;
  }

  // ローディング表示
  const submitBtn = document.getElementById('recruit-submit-btn');
  const loading = document.getElementById('recruit-loading');
  const messageDiv = document.getElementById('recruit-message');

  submitBtn.disabled = true;
  loading.style.display = 'block';
  messageDiv.textContent = '';

  // 希望職種の収集（複数選択）
  const positionCheckboxes = document.querySelectorAll('input[name="position"]:checked');
  const positions = Array.from(positionCheckboxes).map(cb => cb.value);

  if (positions.length === 0) {
    showMessage('recruit-message', 'error', '希望職種を1つ以上選択してください。');
    loading.style.display = 'none';
    submitBtn.disabled = false;
    return;
  }

  // フォームデータ収集
  const formData = {
    name: document.getElementById('recruit-name').value.trim(),
    kana: document.getElementById('kana').value.trim(),
    email: document.getElementById('recruit-email').value.trim(),
    phone: document.getElementById('recruit-phone').value.trim(),
    age: document.getElementById('age').value,
    address: document.getElementById('address').value.trim(),
    position: positions,
    experience: document.getElementById('experience').value.trim(),
    motivation: document.getElementById('motivation').value.trim(),
    message: document.getElementById('recruit-message').value.trim(),
    privacy: document.getElementById('recruit-privacy').checked,
    website: document.getElementById('recruit-website').value, // ハニーポット
    'cf-turnstile-response': recruitTurnstileToken,
  };

  try {
    // API呼び出し
    const response = await fetch('/submit-recruit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();

    if (response.ok && result.success) {
      // 成功時
      showMessage('recruit-message', 'success', result.message);
      document.getElementById('recruit-form').reset();

      // Turnstileリセット
      if (window.turnstile) {
        window.turnstile.reset();
      }
      recruitTurnstileToken = null;
      submitBtn.disabled = true;

      // Google Analytics イベント送信（オプション）
      if (window.gtag) {
        gtag('event', 'form_submission', {
          form_name: 'recruit',
          position: positions.join(', '),
        });
      }
    } else {
      // エラー時
      showMessage('recruit-message', 'error', result.error || 'エラーが発生しました。');

      // Turnstileリセット
      if (window.turnstile) {
        window.turnstile.reset();
      }
      recruitTurnstileToken = null;
      submitBtn.disabled = true;
    }
  } catch (error) {
    console.error('送信エラー:', error);
    showMessage('recruit-message', 'error', 'ネットワークエラーが発生しました。インターネット接続を確認してください。');
  } finally {
    loading.style.display = 'none';
    submitBtn.disabled = false;
  }
});
```

## エラーハンドリングパターン

### レート制限エラー（429）

```javascript
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After') || '300';
  showMessage(
    'contact-message',
    'error',
    `送信回数が制限を超えました。${Math.ceil(retryAfter / 60)}分後に再度お試しください。`
  );
}
```

### バリデーションエラー（400）

```javascript
if (response.status === 400) {
  showMessage('contact-message', 'error', result.error);
  // 特定フィールドのハイライト（オプション）
  highlightInvalidField(result.field);
}
```

### セキュリティエラー（403）

```javascript
if (response.status === 403) {
  showMessage(
    'contact-message',
    'error',
    'セキュリティ検証に失敗しました。ページを再読み込みしてください。'
  );
  // ページリロード推奨
  setTimeout(() => {
    if (confirm('ページを再読み込みしますか?')) {
      window.location.reload();
    }
  }, 3000);
}
```

## アクセシビリティ対応

### aria-live属性でスクリーンリーダー対応

```html
<div id="contact-message"
     class="message"
     role="alert"
     aria-live="polite"
     aria-atomic="true">
</div>
```

### フォームバリデーション改善

```javascript
// リアルタイムバリデーション
document.getElementById('email').addEventListener('blur', (e) => {
  const email = e.target.value;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (email && !emailRegex.test(email)) {
    e.target.setCustomValidity('有効なメールアドレスを入力してください');
    e.target.reportValidity();
  } else {
    e.target.setCustomValidity('');
  }
});
```

## テスト用モックデータ

### お問い合わせフォームテストデータ

```javascript
const mockContactData = {
  company: 'テスト株式会社',
  name: '山田太郎',
  email: 'test@example.com',
  phone: '090-1234-5678',
  service: 'お遍路事業',
  date: '2025-12-01',
  participants: 10,
  message: 'テストメッセージです。',
  privacy: true,
};
```

### 採用応募フォームテストデータ

```javascript
const mockRecruitData = {
  name: '山田太郎',
  kana: 'ヤマダタロウ',
  email: 'recruit-test@example.com',
  phone: '090-9876-5432',
  age: 30,
  address: '東京都渋谷区',
  position: ['先達（ガイド）', '営業'],
  experience: '旅行業界5年、ガイド経験3年',
  motivation: '日本の伝統文化に興味があります。',
  message: 'よろしくお願いします。',
  privacy: true,
};
```

## まとめ

このガイドに従って実装すれば、以下の機能を備えたフォーム送信システムが完成します:

- ✅ Turnstileによるボット対策
- ✅ ハニーポットによるスパム対策
- ✅ レート制限によるDoS対策
- ✅ クライアントサイドバリデーション
- ✅ アクセシビリティ対応
- ✅ エラーハンドリング
- ✅ ローディング表示
- ✅ Google Analytics連携（オプション）
