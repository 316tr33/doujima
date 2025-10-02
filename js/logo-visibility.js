/*
   logo-visibility.js - ロゴ企業名の動的表示制御
   nav要素の幅に応じて企業名の表示/非表示を自動切り替え
*/

(function() {
    'use strict';

    // 設定
    const MIN_GAP = 50; // 企業名とnav-linksの最小空白（px）
    const DESKTOP_BREAKPOINT = 1024; // デスクトップ判定ブレークポイント
    const THROTTLE_DELAY = 100; // リサイズイベントのthrottle遅延（ms）

    let resizeTimer = null;

    // 企業名表示/非表示の判定と更新
    function updateLogoTextVisibility() {
        const windowWidth = window.innerWidth;
        const logoText = document.querySelector('.logo-text');

        if (!logoText) {
            console.log('logo-text not found');
            return;
        }

        // モバイル・タブレット（〜1023px）は常に表示
        if (windowWidth < DESKTOP_BREAKPOINT) {
            logoText.style.display = 'inline';
            logoText.setAttribute('data-visibility-reason', 'mobile');
            return;
        }

        // デスクトップ（1024px〜）は幅計算に基づいて判定
        const nav = document.querySelector('nav');
        const logo = document.querySelector('.logo');
        const logoImg = logo ? logo.querySelector('img') : null;
        const navLinks = document.querySelector('.nav-links');

        if (!nav || !logoImg || !navLinks) {
            console.log('Required elements not found');
            return;
        }

        // 各要素の幅を取得
        const navWidth = nav.offsetWidth;
        const navPadding = parseFloat(getComputedStyle(nav).paddingLeft) +
                          parseFloat(getComputedStyle(nav).paddingRight);
        const availableWidth = navWidth - navPadding;

        // ロゴ画像の幅
        const logoImgWidth = logoImg.offsetWidth;

        // 企業名の幅を取得（一時的に表示して測定）
        logoText.style.display = 'inline';
        logoText.style.visibility = 'hidden';
        const logoTextWidth = logoText.offsetWidth;
        logoText.style.visibility = '';

        // nav-linksの幅
        const navLinksWidth = navLinks.offsetWidth;

        // 必要な合計幅 = ロゴ画像 + 企業名 + 最小空白 + nav-links
        const totalRequired = logoImgWidth + logoTextWidth + MIN_GAP + navLinksWidth;

        // 判定と表示切り替え
        if (totalRequired <= availableWidth) {
            logoText.style.display = 'inline';
            logoText.setAttribute('data-visibility-reason', 'space-available');
            console.log(`✓ 企業名表示: ${availableWidth}px（必要: ${totalRequired}px、余裕: ${availableWidth - totalRequired}px）`);
        } else {
            logoText.style.display = 'none';
            logoText.setAttribute('data-visibility-reason', 'space-insufficient');
            console.log(`✗ 企業名非表示: ${availableWidth}px（必要: ${totalRequired}px、不足: ${totalRequired - availableWidth}px）`);
        }
    }

    // Throttle処理付きリサイズハンドラ
    function handleResize() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            updateLogoTextVisibility();
        }, THROTTLE_DELAY);
    }

    // 初期化
    function init() {
        // 初期表示判定
        updateLogoTextVisibility();

        // リサイズイベント
        window.addEventListener('resize', handleResize);

        // オリエンテーション変更
        window.addEventListener('orientationchange', () => {
            setTimeout(updateLogoTextVisibility, 200);
        });

        console.log('Logo visibility controller initialized');
    }

    // DOMロード完了後に初期化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // グローバル関数として公開（デバッグ用）
    window.logoVisibility = {
        update: updateLogoTextVisibility,
        getStatus: function() {
            const logoText = document.querySelector('.logo-text');
            return {
                display: logoText ? logoText.style.display : 'not found',
                reason: logoText ? logoText.getAttribute('data-visibility-reason') : null,
                windowWidth: window.innerWidth
            };
        }
    };

})();
