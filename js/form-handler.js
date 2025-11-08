/**
 * フォーム送信処理 - Cloudflare Turnstile + ハニーポット統合
 * お問い合わせフォームと採用応募フォームの送信を管理
 */

// DOMContentLoaded時の初期化
document.addEventListener('DOMContentLoaded', function() {
  initContactForm();
  initRecruitForm();
});

/**
 * お問い合わせフォーム初期化
 */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    await handleContactSubmit(form);
  });
}

/**
 * 採用応募フォーム初期化
 */
function initRecruitForm() {
  const form = document.getElementById('recruitForm');
  if (!form) return;

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    await handleRecruitSubmit(form);
  });
}

/**
 * お問い合わせフォーム送信処理
 */
async function handleContactSubmit(form) {
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalBtnText = submitBtn.innerHTML;

  try {
    // バリデーション
    if (!validateContactForm(form)) {
      showMessage('必須項目を入力してください', 'error');
      return;
    }

    // ハニーポットチェック
    const honeypot = form.querySelector('input[name="website"]');
    if (honeypot && honeypot.value !== '') {
      console.log('ハニーポット検出: スパムの可能性');
      showMessage('送信に失敗しました。ページを再読み込みしてください', 'error');
      return;
    }

    // Turnstileトークン取得
    const turnstileResponse = getTurnstileToken(form);
    if (!turnstileResponse) {
      showMessage('ボット検証に失敗しました。ページを再読み込みしてください', 'error');
      return;
    }

    // ローディング状態
    submitBtn.disabled = true;
    submitBtn.setAttribute('aria-busy', 'true');
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 送信中...';

    // FormData作成
    const formData = new FormData(form);
    formData.append('cf-turnstile-response', turnstileResponse);

    // API送信
    const response = await fetch('/submit-contact', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `サーバーエラー: ${response.status}`);
    }

    const result = await response.json();

    // 成功処理
    showMessage('お問い合わせを受け付けました。担当者より折り返しご連絡いたします', 'success');
    form.reset();

    // Turnstileリセット（再送信用）
    if (window.turnstile) {
      window.turnstile.reset();
    }

  } catch (error) {
    console.error('フォーム送信エラー:', error);

    // エラーメッセージ判定
    let errorMessage = 'サーバーエラーが発生しました。しばらくしてから再度お試しください';

    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      errorMessage = '送信に失敗しました。インターネット接続を確認してください';
    } else if (error.message.includes('429') || error.message.includes('レート制限')) {
      errorMessage = '送信回数が制限されています。しばらくしてから再度お試しください';
    }

    showMessage(errorMessage, 'error');

  } finally {
    // ボタン復元
    submitBtn.disabled = false;
    submitBtn.removeAttribute('aria-busy');
    submitBtn.innerHTML = originalBtnText;
  }
}

/**
 * 採用応募フォーム送信処理
 */
async function handleRecruitSubmit(form) {
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalBtnText = submitBtn.textContent;

  try {
    // バリデーション
    if (!validateRecruitForm(form)) {
      showMessage('必須項目を入力してください', 'error');
      return;
    }

    // ハニーポットチェック
    const honeypot = form.querySelector('input[name="website"]');
    if (honeypot && honeypot.value !== '') {
      console.log('ハニーポット検出: スパムの可能性');
      showMessage('送信に失敗しました。ページを再読み込みしてください', 'error');
      return;
    }

    // Turnstileトークン取得
    const turnstileResponse = getTurnstileToken(form);
    if (!turnstileResponse) {
      showMessage('ボット検証に失敗しました。ページを再読み込みしてください', 'error');
      return;
    }

    // ローディング状態
    submitBtn.disabled = true;
    submitBtn.setAttribute('aria-busy', 'true');
    submitBtn.textContent = '送信中...';

    // FormData作成（複数選択対応）
    const formData = new FormData(form);
    const positions = formData.getAll('position'); // チェックボックス配列取得

    // FormDataをJSONに変換
    const jsonData = {
      name: formData.get('name'),
      kana: formData.get('kana'),
      email: formData.get('email'),
      phone: formData.get('phone'),
      age: formData.get('age'),
      address: formData.get('address'),
      position: positions, // 配列
      experience: formData.get('experience'),
      motivation: formData.get('motivation'),
      message: formData.get('message'),
      'cf-turnstile-response': turnstileResponse
    };

    // API送信
    const response = await fetch('/submit-recruit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(jsonData)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `サーバーエラー: ${response.status}`);
    }

    const result = await response.json();

    // 成功処理
    showMessage('応募を受け付けました。選考結果は後日ご連絡いたします', 'success');
    form.reset();

    // Turnstileリセット（再送信用）
    if (window.turnstile) {
      window.turnstile.reset();
    }

  } catch (error) {
    console.error('フォーム送信エラー:', error);

    // エラーメッセージ判定
    let errorMessage = 'サーバーエラーが発生しました。しばらくしてから再度お試しください';

    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      errorMessage = '送信に失敗しました。インターネット接続を確認してください';
    } else if (error.message.includes('429') || error.message.includes('レート制限')) {
      errorMessage = '送信回数が制限されています。しばらくしてから再度お試しください';
    }

    showMessage(errorMessage, 'error');

  } finally {
    // ボタン復元
    submitBtn.disabled = false;
    submitBtn.removeAttribute('aria-busy');
    submitBtn.textContent = originalBtnText;
  }
}

/**
 * お問い合わせフォームバリデーション
 */
function validateContactForm(form) {
  const company = form.querySelector('#company');
  const name = form.querySelector('#name');
  const email = form.querySelector('#email');
  const service = form.querySelector('#service');
  const privacy = form.querySelector('input[name="privacy"]');

  // 必須フィールドチェック
  if (!company.value.trim() || !name.value.trim() || !email.value.trim() || !service.value || !privacy.checked) {
    return false;
  }

  // メールアドレス形式チェック
  if (!isValidEmail(email.value)) {
    showMessage('正しいメールアドレスを入力してください', 'error');
    return false;
  }

  // 電話番号チェック（任意フィールドだが入力されている場合）
  const phone = form.querySelector('#phone');
  if (phone.value.trim() && !isValidPhone(phone.value)) {
    showMessage('正しい電話番号を入力してください（ハイフンなしの数字10-11桁）', 'error');
    return false;
  }

  return true;
}

/**
 * 採用応募フォームバリデーション
 */
function validateRecruitForm(form) {
  const name = form.querySelector('#name');
  const kana = form.querySelector('#kana');
  const email = form.querySelector('#email');
  const phone = form.querySelector('#phone');
  const positions = form.querySelectorAll('input[name="position"]:checked');
  const privacy = form.querySelector('#privacy');

  // 必須フィールドチェック
  if (!name.value.trim() || !kana.value.trim() || !email.value.trim() || !phone.value.trim() || positions.length === 0 || !privacy.checked) {
    return false;
  }

  // メールアドレス形式チェック
  if (!isValidEmail(email.value)) {
    showMessage('正しいメールアドレスを入力してください', 'error');
    return false;
  }

  // 電話番号チェック
  if (!isValidPhone(phone.value)) {
    showMessage('正しい電話番号を入力してください（ハイフンなしの数字10-11桁）', 'error');
    return false;
  }

  return true;
}

/**
 * メールアドレス形式チェック
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * 電話番号形式チェック（ハイフンなしの数字10-11桁）
 */
function isValidPhone(phone) {
  const phoneRegex = /^[0-9]{10,11}$/;
  const cleanedPhone = phone.replace(/[-\s]/g, ''); // ハイフンとスペースを除去
  return phoneRegex.test(cleanedPhone);
}

/**
 * Turnstileトークン取得
 */
function getTurnstileToken(form) {
  const turnstileElement = form.querySelector('.cf-turnstile');
  if (!turnstileElement) {
    console.warn('Turnstile要素が見つかりません');
    return null;
  }

  // Turnstile APIからトークンを取得
  const response = turnstileElement.querySelector('input[name="cf-turnstile-response"]');
  if (response && response.value) {
    return response.value;
  }

  console.warn('Turnstileトークンが見つかりません');
  return null;
}

/**
 * メッセージ表示（成功/エラー）
 */
function showMessage(message, type) {
  // 既存のメッセージを削除
  const existingMessage = document.querySelector('.form-message');
  if (existingMessage) {
    existingMessage.remove();
  }

  // メッセージ要素作成
  const messageDiv = document.createElement('div');
  messageDiv.className = `form-message ${type}`;
  messageDiv.textContent = message;
  messageDiv.setAttribute('role', 'alert');

  // フォームの送信ボタンの直前に挿入
  const forms = document.querySelectorAll('#contactForm, #recruitForm');
  forms.forEach(form => {
    if (form) {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.parentElement.insertBefore(messageDiv, submitBtn);
      }
    }
  });

  // フェードイン
  setTimeout(() => {
    messageDiv.style.opacity = '1';
  }, 10);

  // 3秒後に自動非表示
  setTimeout(() => {
    messageDiv.style.animation = 'fadeOut 0.3s ease-in-out';
    setTimeout(() => {
      messageDiv.remove();
    }, 300);
  }, 3000);
}
