// 多言語対応システム - 言語切り替え機能
// Language Switcher System for Multilingual Support

/**
 * 言語設定管理システム
 * LocalStorageを使用してユーザーの言語選択を保存し、
 * サイト内移動時に言語設定を維持します
 */

// 定数定義
const LANGUAGE_KEY = 'preferredLanguage'; // LocalStorageのキー
const SUPPORTED_LANGUAGES = ['ja', 'en']; // サポート言語
const DEFAULT_LANGUAGE = 'ja'; // デフォルト言語

/**
 * 現在のページの言語を検出
 * @returns {string} 'ja' または 'en'
 */
function detectCurrentLanguage() {
  const currentPath = window.location.pathname;

  // URLに '/en/' が含まれている場合は英語
  if (currentPath.includes('/en/')) {
    return 'en';
  }

  // それ以外は日本語
  return 'ja';
}

/**
 * 言語設定をLocalStorageに保存
 * @param {string} language - 保存する言語コード ('ja' または 'en')
 */
function saveLanguagePreference(language) {
  if (SUPPORTED_LANGUAGES.includes(language)) {
    localStorage.setItem(LANGUAGE_KEY, language);
    console.log(`言語設定を保存: ${language}`);
  }
}

/**
 * LocalStorageから言語設定を取得
 * @returns {string} 保存された言語コード、なければデフォルト言語
 */
function getLanguagePreference() {
  const saved = localStorage.getItem(LANGUAGE_KEY);
  return SUPPORTED_LANGUAGES.includes(saved) ? saved : DEFAULT_LANGUAGE;
}

/**
 * 現在のURLを指定言語版のURLに変換
 * @param {string} currentURL - 現在のURL
 * @param {string} targetLang - 変換先の言語 ('ja' または 'en')
 * @returns {string} 変換後のURL
 */
function getTranslatedURL(currentURL, targetLang) {
  const currentLang = detectCurrentLanguage();

  // 同じ言語の場合は変換不要
  if (currentLang === targetLang) {
    return currentURL;
  }

  // 日本語→英語
  if (currentLang === 'ja' && targetLang === 'en') {
    // Ohenro/xxx.html → Ohenro/en/xxx.html
    // Tokaido/xxx.html → Tokaido/en/xxx.html
    return currentURL.replace(
      /(Ohenro|Tokaido)\//,
      '$1/en/'
    );
  }

  // 英語→日本語
  if (currentLang === 'en' && targetLang === 'ja') {
    // Ohenro/en/xxx.html → Ohenro/xxx.html
    // Tokaido/en/xxx.html → Tokaido/xxx.html
    return currentURL.replace(
      /(Ohenro|Tokaido)\/en\//,
      '$1/'
    );
  }

  return currentURL;
}

/**
 * 指定された言語に切り替え
 * @param {string} targetLang - 切り替え先の言語
 */
function switchLanguage(targetLang) {
  if (!SUPPORTED_LANGUAGES.includes(targetLang)) {
    console.error(`サポートされていない言語: ${targetLang}`);
    return;
  }

  const currentURL = window.location.pathname;
  const translatedURL = getTranslatedURL(currentURL, targetLang);

  // 言語設定を保存
  saveLanguagePreference(targetLang);

  // 変換後のURLにリダイレクト
  if (translatedURL !== currentURL) {
    console.log(`言語切り替え: ${currentURL} → ${translatedURL}`);
    window.location.href = translatedURL;
  }
}

/**
 * ナビゲーションリンクを現在の言語に応じて更新
 */
function updateNavigationLinks() {
  const currentLang = detectCurrentLanguage();
  const navLinks = document.querySelectorAll('a[href]');

  navLinks.forEach(link => {
    const href = link.getAttribute('href');

    // 外部リンクやアンカーリンクはスキップ
    if (!href || href.startsWith('http') || href.startsWith('#')) {
      return;
    }

    // お遍路・東海道のページリンクを変換
    if (href.includes('Ohenro/') || href.includes('Tokaido/')) {
      let newHref = href;

      if (currentLang === 'en') {
        // 日本語版リンク→英語版リンクに変換
        if (!href.includes('/en/')) {
          newHref = href.replace(
            /(Ohenro|Tokaido)\//,
            '$1/en/'
          );
        }
      } else {
        // 英語版リンク→日本語版リンクに変換
        if (href.includes('/en/')) {
          newHref = href.replace(
            /(Ohenro|Tokaido)\/en\//,
            '$1/'
          );
        }
      }

      link.setAttribute('href', newHref);
    }
  });

  console.log(`ナビゲーションリンクを更新: ${currentLang}`);
}

/**
 * 言語切り替えボタンの表示テキストを更新
 */
function updateLanguageButtonText() {
  const currentLang = detectCurrentLanguage();
  const desktopButton = document.getElementById('languageToggle');
  const mobileButton = document.getElementById('mobileLangToggle');

  const buttonText = currentLang === 'ja' ? 'English' : '日本語';

  if (desktopButton) {
    const textSpan = desktopButton.querySelector('.lang-text');
    if (textSpan) {
      textSpan.textContent = buttonText;
    }
  }

  if (mobileButton) {
    // モバイルボタンのテキストを更新（アイコンは維持）
    const icon = mobileButton.querySelector('i');
    if (icon) {
      mobileButton.innerHTML = '';
      mobileButton.appendChild(icon);
      mobileButton.append(` ${buttonText}`);
    } else {
      mobileButton.innerHTML = `<i class="fas fa-globe"></i> ${buttonText}`;
    }
  }
}

/**
 * 言語切り替えシステムを初期化
 */
function initLanguageSwitcher() {
  const currentLang = detectCurrentLanguage();
  const savedLang = getLanguagePreference();

  console.log(`現在の言語: ${currentLang}, 保存された設定: ${savedLang}`);

  // ボタンテキストを更新
  updateLanguageButtonText();

  // ナビゲーションリンクを更新
  updateNavigationLinks();

  // デスクトップ用言語切り替えボタンのイベントリスナー
  const desktopButton = document.getElementById('languageToggle');
  if (desktopButton) {
    desktopButton.addEventListener('click', function(e) {
      e.preventDefault();
      const targetLang = currentLang === 'ja' ? 'en' : 'ja';
      switchLanguage(targetLang);
    });
  }

  // モバイル用言語切り替えボタンのイベントリスナー
  const mobileButton = document.getElementById('mobileLangToggle');
  if (mobileButton) {
    mobileButton.addEventListener('click', function(e) {
      e.preventDefault();
      const targetLang = currentLang === 'ja' ? 'en' : 'ja';
      switchLanguage(targetLang);
    });
  }

  console.log('言語切り替えシステムを初期化完了');
}

/**
 * ページ読み込み時の言語チェックと自動リダイレクト
 * 注: 企業トップページ（index.html）は日本語のみのため除外
 */
function checkLanguageOnLoad() {
  const currentPath = window.location.pathname;

  // 企業トップページまたはrecruitページの場合はスキップ
  if (currentPath.includes('index.html') &&
      !currentPath.includes('Ohenro') &&
      !currentPath.includes('Tokaido')) {
    console.log('企業トップページ: 言語チェックをスキップ');
    return;
  }

  if (currentPath.includes('recruit.html')) {
    console.log('採用ページ: 言語チェックをスキップ');
    return;
  }

  const currentLang = detectCurrentLanguage();
  const savedLang = getLanguagePreference();

  // お遍路・東海道ページで、保存された言語と現在の言語が異なる場合
  if ((currentPath.includes('Ohenro') || currentPath.includes('Tokaido')) &&
      currentLang !== savedLang) {
    console.log(`言語設定不一致: 現在=${currentLang}, 設定=${savedLang}`);
    const translatedURL = getTranslatedURL(currentPath, savedLang);

    if (translatedURL !== currentPath) {
      console.log(`自動リダイレクト: ${currentPath} → ${translatedURL}`);
      window.location.href = translatedURL;
    }
  }
}

// DOMContentLoaded時の初期化
document.addEventListener('DOMContentLoaded', function() {
  // 言語チェックと自動リダイレクト
  checkLanguageOnLoad();

  // 言語切り替えシステム初期化
  initLanguageSwitcher();
});

// グローバルスコープに公開（必要に応じて）
window.switchLanguage = switchLanguage;
window.detectCurrentLanguage = detectCurrentLanguage;
