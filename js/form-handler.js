/**
 * 堂島フロント企画 - フォーム送信処理
 * お問い合わせフォーム & 採用応募フォーム共通処理
 */

(function () {
  'use strict';

  // お問い合わせフォームの初期化
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    initializeForm(contactForm, '/submit-contact', 'contact');
  }

  // 採用応募フォームの初期化
  const recruitForm = document.getElementById('recruit-form');
  if (recruitForm) {
    initializeForm(recruitForm, '/submit-recruit', 'recruit');
  }

  /**
   * フォーム初期化
   */
  function initializeForm(form, endpoint, formType) {
    const submitButton = form.querySelector('button[type="submit"]');
    const messageContainer = document.getElementById(`${formType}-message`);
    let isSubmitting = false;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // 二重送信防止
      if (isSubmitting) {
        return;
      }

      // バリデーション
      if (!validateForm(form, formType)) {
        return;
      }

      isSubmitting = true;
      setSubmittingState(submitButton, true);
      clearMessage(messageContainer);

      try {
        // FormDataの作成
        const formData = new FormData(form);

        // 送信
        const response = await fetch(endpoint, {
          method: 'POST',
          body: formData,
        });

        const result = await response.json();

        if (result.success) {
          // 成功時
          showMessage(messageContainer, result.message || '送信が完了しました。', 'success');
          form.reset();
          resetTurnstile();
        } else {
          // エラー時
          showMessage(messageContainer, result.error || '送信に失敗しました。', 'error');
          resetTurnstile();
        }
      } catch (error) {
        console.error('フォーム送信エラー:', error);
        showMessage(
          messageContainer,
          'ネットワークエラーが発生しました。インターネット接続を確認してください。',
          'error'
        );
        resetTurnstile();
      } finally {
        isSubmitting = false;
        setSubmittingState(submitButton, false);
      }
    });
  }

  /**
   * フォームバリデーション
   */
  function validateForm(form, formType) {
    // プライバシーポリシー同意チェック
    const privacyCheckbox = form.querySelector('input[name="privacy"]');
    if (privacyCheckbox && !privacyCheckbox.checked) {
      alert('プライバシーポリシーに同意してください。');
      return false;
    }

    // Turnstileトークンチェック
    const turnstileResponse = form.querySelector('input[name="cf-turnstile-response"]');
    if (!turnstileResponse || !turnstileResponse.value) {
      alert('セキュリティ検証が完了していません。しばらくお待ちください。');
      return false;
    }

    // フォームタイプ別の追加バリデーション
    if (formType === 'contact') {
      return validateContactForm(form);
    } else if (formType === 'recruit') {
      return validateRecruitForm(form);
    }

    return true;
  }

  /**
   * お問い合わせフォームの個別バリデーション
   */
  function validateContactForm(form) {
    const email = form.querySelector('input[name="email"]').value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert('有効なメールアドレスを入力してください。');
      return false;
    }
    return true;
  }

  /**
   * 採用応募フォームの個別バリデーション
   */
  function validateRecruitForm(form) {
    // メールアドレスチェック
    const email = form.querySelector('input[name="email"]').value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert('有効なメールアドレスを入力してください。');
      return false;
    }

    // フリガナチェック(カタカナのみ)
    const kana = form.querySelector('input[name="kana"]').value;
    const kanaRegex = /^[ァ-ヶー\s]+$/;
    if (!kanaRegex.test(kana)) {
      alert('フリガナは全角カタカナで入力してください。');
      return false;
    }

    // 応募職種チェック(最低1つ選択)
    const positionCheckboxes = form.querySelectorAll('input[name="position"]:checked');
    if (positionCheckboxes.length === 0) {
      alert('応募職種を選択してください。');
      return false;
    }

    return true;
  }

  /**
   * メッセージ表示
   */
  function showMessage(container, message, type) {
    if (!container) return;

    container.textContent = message;
    container.className = `form-message ${type}`;
    container.style.display = 'block';

    // 成功メッセージは5秒後に自動非表示
    if (type === 'success') {
      setTimeout(() => {
        clearMessage(container);
      }, 5000);
    }
  }

  /**
   * メッセージクリア
   */
  function clearMessage(container) {
    if (!container) return;
    container.textContent = '';
    container.className = 'form-message';
    container.style.display = 'none';
  }

  /**
   * 送信中状態の設定
   */
  function setSubmittingState(button, isSubmitting) {
    if (!button) return;

    if (isSubmitting) {
      button.disabled = true;
      button.dataset.originalText = button.textContent;
      button.textContent = '送信中...';
    } else {
      button.disabled = false;
      button.textContent = button.dataset.originalText || '送信する';
    }
  }

  /**
   * Turnstileウィジェットのリセット
   */
  function resetTurnstile() {
    if (typeof turnstile !== 'undefined' && turnstile.reset) {
      try {
        turnstile.reset();
      } catch (error) {
        console.log('Turnstileリセットエラー:', error);
      }
    }
  }
})();
