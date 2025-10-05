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
  const currentPath = window.location.pathname.toLowerCase();

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
    // ohenro/xxx.html → ohenro/en/xxx.html
    // tokaido/xxx.html → tokaido/en/xxx.html
    // 大文字小文字を区別しない（case-insensitive）
    return currentURL.replace(
      /(ohenro|tokaido)\//i,
      '$1/en/'
    );
  }

  // 英語→日本語
  if (currentLang === 'en' && targetLang === 'ja') {
    // ohenro/en/xxx.html → ohenro/xxx.html
    // tokaido/en/xxx.html → tokaido/xxx.html
    // 大文字小文字を区別しない（case-insensitive）
    return currentURL.replace(
      /(ohenro|tokaido)\/en\//i,
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
  const currentLang = detectCurrentLanguage();
  const translatedURL = getTranslatedURL(currentURL, targetLang);

  console.log(`🌐 言語切り替え開始:`);
  console.log(`  現在の言語: ${currentLang}`);
  console.log(`  切り替え先: ${targetLang}`);
  console.log(`  現在のURL: ${currentURL}`);
  console.log(`  変換後URL: ${translatedURL}`);

  // 言語設定を保存
  saveLanguagePreference(targetLang);

  // 変換後のURLにリダイレクト
  if (translatedURL !== currentURL) {
    console.log(`✅ リダイレクト実行: ${currentURL} → ${translatedURL}`);
    window.location.href = translatedURL;
  } else {
    console.warn(`⚠️ URLが同じため、リダイレクトをスキップしました`);
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

    // お遍路・東海道のページリンクを変換（大文字小文字を区別しない）
    if (href.toLowerCase().includes('ohenro/') || href.toLowerCase().includes('tokaido/')) {
      let newHref = href;

      if (currentLang === 'en') {
        // 日本語版リンク→英語版リンクに変換
        if (!href.toLowerCase().includes('/en/')) {
          newHref = href.replace(
            /(ohenro|tokaido)\//i,
            '$1/en/'
          );
        }
      } else {
        // 英語版リンク→日本語版リンクに変換
        if (href.toLowerCase().includes('/en/')) {
          newHref = href.replace(
            /(ohenro|tokaido)\/en\//i,
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
      console.log('🖱️ デスクトップ言語切り替えボタンがクリックされました');
      const targetLang = currentLang === 'ja' ? 'en' : 'ja';
      switchLanguage(targetLang);
    });
    console.log('✅ デスクトップボタンのイベントリスナーを設定');
  } else {
    console.warn('⚠️ デスクトップ言語切り替えボタン (#languageToggle) が見つかりません');
  }

  // モバイル用言語切り替えボタンのイベントリスナー
  const mobileButton = document.getElementById('mobileLangToggle');
  if (mobileButton) {
    mobileButton.addEventListener('click', function(e) {
      e.preventDefault();
      console.log('📱 モバイル言語切り替えボタンがクリックされました');
      const targetLang = currentLang === 'ja' ? 'en' : 'ja';
      switchLanguage(targetLang);
    });
    console.log('✅ モバイルボタンのイベントリスナーを設定');
  } else {
    console.warn('⚠️ モバイル言語切り替えボタン (#mobileLangToggle) が見つかりません');
  }

  console.log('言語切り替えシステムを初期化完了');
}

/**
 * ページ読み込み時の言語チェック
 * 注: 自動リダイレクトは行わず、現在のページの言語をそのまま表示
 * ユーザーの明示的な言語選択のみをLocalStorageに記憶
 */
function checkLanguageOnLoad() {
  const currentPath = window.location.pathname;
  const currentPathLower = currentPath.toLowerCase();

  // 企業トップページまたはrecruitページの場合はスキップ
  if (currentPathLower.includes('index.html') &&
      !currentPathLower.includes('ohenro') &&
      !currentPathLower.includes('tokaido')) {
    console.log('企業トップページ: 言語チェックをスキップ');
    return;
  }

  if (currentPathLower.includes('recruit.html')) {
    console.log('採用ページ: 言語チェックをスキップ');
    return;
  }

  const currentLang = detectCurrentLanguage();

  // 現在のページの言語をLocalStorageに保存
  // これにより、次のページ遷移時に言語が継承される
  saveLanguagePreference(currentLang);

  console.log(`現在のページ言語を保存: ${currentLang}`);
}

// DOMContentLoaded時の初期化
// ページが既に読み込まれている場合は即座に実行、そうでなければDOMContentLoadedを待つ
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    // 言語チェックと自動リダイレクト
    checkLanguageOnLoad();

    // 言語切り替えシステム初期化
    initLanguageSwitcher();
  });
} else {
  // DOMが既に読み込まれている場合は即座に実行
  checkLanguageOnLoad();
  initLanguageSwitcher();
}

// グローバルスコープに公開（必要に応じて）
window.switchLanguage = switchLanguage;
window.detectCurrentLanguage = detectCurrentLanguage;
