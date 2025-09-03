// 採用情報ページ専用JavaScript - 堂島フロント企画

document.addEventListener('DOMContentLoaded', function() {
    // DOM要素の取得とキャッシュ
    const form = document.getElementById('recruitForm');
    const nameInput = document.getElementById('name');
    const kanaInput = document.getElementById('kana');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const positionCheckboxes = document.querySelectorAll('input[name="position"]');
    const privacyCheckbox = document.getElementById('privacy');

    // 初期化
    initFormValidation();
    initFormAnimations();
    initFormSubmission();

    // フォームバリデーション
    function initFormValidation() {
        // リアルタイムバリデーション
        nameInput.addEventListener('blur', validateName);
        kanaInput.addEventListener('blur', validateKana);
        emailInput.addEventListener('blur', validateEmail);
        phoneInput.addEventListener('blur', validatePhone);
        
        // 職種選択のバリデーション
        positionCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', validatePositions);
        });
        
        // プライバシーポリシー同意のバリデーション
        privacyCheckbox.addEventListener('change', validatePrivacy);
    }

    // フォームアニメーション
    function initFormAnimations() {
        // フォーカス時のアニメーション
        const formInputs = form.querySelectorAll('input, textarea, select');
        
        formInputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (!this.value.trim()) {
                    this.parentElement.classList.remove('focused');
                }
            });
        });
    }

    // フォーム送信処理
    function initFormSubmission() {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 全体バリデーション
            if (validateForm()) {
                submitForm();
            } else {
                showErrorMessage('入力内容に不備があります。エラー項目を確認してください。');
            }
        });
    }

    // 名前のバリデーション
    function validateName() {
        const name = nameInput.value.trim();
        if (!name) {
            showFieldError(nameInput, 'お名前を入力してください');
            return false;
        } else if (name.length < 2) {
            showFieldError(nameInput, 'お名前は2文字以上で入力してください');
            return false;
        } else {
            showFieldSuccess(nameInput);
            return true;
        }
    }

    // フリガナのバリデーション
    function validateKana() {
        const kana = kanaInput.value.trim();
        const kanaRegex = /^[\u30A1-\u30FC\u3041-\u3096\s]*$/;
        
        if (!kana) {
            showFieldError(kanaInput, 'フリガナを入力してください');
            return false;
        } else if (!kanaRegex.test(kana)) {
            showFieldError(kanaInput, 'フリガナはひらがな・カタカナで入力してください');
            return false;
        } else {
            showFieldSuccess(kanaInput);
            return true;
        }
    }

    // メールアドレスのバリデーション
    function validateEmail() {
        const email = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!email) {
            showFieldError(emailInput, 'メールアドレスを入力してください');
            return false;
        } else if (!emailRegex.test(email)) {
            showFieldError(emailInput, '正しいメールアドレスを入力してください');
            return false;
        } else {
            showFieldSuccess(emailInput);
            return true;
        }
    }

    // 電話番号のバリデーション
    function validatePhone() {
        const phone = phoneInput.value.trim();
        const phoneRegex = /^[\d\-]{10,}$/;
        
        if (!phone) {
            showFieldError(phoneInput, '電話番号を入力してください');
            return false;
        } else if (!phoneRegex.test(phone)) {
            showFieldError(phoneInput, '正しい電話番号を入力してください');
            return false;
        } else {
            showFieldSuccess(phoneInput);
            return true;
        }
    }

    // 職種選択のバリデーション
    function validatePositions() {
        const checkedPositions = document.querySelectorAll('input[name="position"]:checked');
        const errorElement = document.querySelector('.position-error');
        
        if (checkedPositions.length === 0) {
            if (!errorElement) {
                const error = document.createElement('div');
                error.className = 'position-error error-message';
                error.textContent = '希望職種を最低1つ選択してください';
                document.querySelector('.checkbox-group').parentElement.appendChild(error);
            }
            return false;
        } else {
            if (errorElement) {
                errorElement.remove();
            }
            return true;
        }
    }

    // プライバシーポリシー同意のバリデーション
    function validatePrivacy() {
        if (!privacyCheckbox.checked) {
            showFieldError(privacyCheckbox, '個人情報の取扱いに同意してください');
            return false;
        } else {
            showFieldSuccess(privacyCheckbox);
            return true;
        }
    }

    // 全体バリデーション
    function validateForm() {
        const validations = [
            validateName(),
            validateKana(),
            validateEmail(),
            validatePhone(),
            validatePositions(),
            validatePrivacy()
        ];
        
        return validations.every(result => result === true);
    }

    // フィールドエラー表示
    function showFieldError(field, message) {
        clearFieldMessages(field);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        field.parentElement.appendChild(errorDiv);
        field.classList.add('error');
    }

    // フィールド成功表示
    function showFieldSuccess(field) {
        clearFieldMessages(field);
        field.classList.add('success');
    }

    // フィールドメッセージクリア
    function clearFieldMessages(field) {
        const existingError = field.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        field.classList.remove('error', 'success');
    }

    // エラーメッセージ表示
    function showErrorMessage(message) {
        const existingError = form.querySelector('.form-error');
        if (existingError) {
            existingError.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error';
        errorDiv.textContent = message;
        
        form.insertBefore(errorDiv, form.firstChild);
        
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 5000);
    }

    // フォーム送信
    function submitForm() {
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        
        submitButton.disabled = true;
        submitButton.textContent = '送信中...';
        
        // フォームデータの収集
        const formData = new FormData(form);
        
        // 実際の送信処理（サンプル）
        setTimeout(() => {
            alert('応募を受け付けました。ありがとうございます。\n担当者より3営業日以内にご連絡いたします。');
            form.reset();
            
            // エラーメッセージをクリア
            form.querySelectorAll('.error-message').forEach(error => error.remove());
            form.querySelectorAll('.error, .success').forEach(field => {
                field.classList.remove('error', 'success');
            });
            
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }, 2000);
    }

    // フォームまでスクロール
    window.scrollToForm = function() {
        const formSection = document.querySelector('.application-form');
        if (formSection) {
            formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // 職種詳細表示機能
    window.scrollToDetails = function(positionId) {
        // 全ての詳細セクションを非表示
        const allDetails = document.querySelectorAll('.position-detail-section');
        allDetails.forEach(detail => {
            detail.style.display = 'none';
        });

        // 選択された詳細セクションを表示
        const targetElement = document.getElementById(positionId + '-details');
        const detailsSection = document.querySelector('.position-details-section');
        const sectionTitle = document.getElementById('detail-section-title');
        
        if (targetElement && detailsSection && sectionTitle) {
            // 詳細セクション全体を表示
            detailsSection.style.display = 'block';
            
            // 選択された職種の詳細を表示
            targetElement.style.display = 'block';
            
            // タイトルを更新
            const positionName = targetElement.querySelector('h4').textContent;
            sectionTitle.textContent = `${positionName} - 詳細情報`;

            // 詳細セクションまでスクロール
            const elementPosition = detailsSection.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - 80; // 80px上にマージンを取る

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });

            // 一時的にハイライトエフェクトを追加
            targetElement.style.transition = 'box-shadow 0.3s ease';
            targetElement.style.boxShadow = '0 8px 35px rgba(139, 115, 85, 0.3)';
            
            setTimeout(() => {
                targetElement.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)';
            }, 2000);
        }
    }

    // 全詳細を非表示にして職種一覧に戻る
    window.hideAllDetails = function() {
        const detailsSection = document.querySelector('.position-details-section');
        const cardsGrid = document.querySelector('.position-cards-grid');
        
        if (detailsSection && cardsGrid) {
            // 詳細セクションを非表示
            detailsSection.style.display = 'none';
            
            // 職種カードまでスクロール
            const elementPosition = cardsGrid.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - 100; // 100px上にマージンを取る

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    }
});