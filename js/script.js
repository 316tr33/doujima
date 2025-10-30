// グローバル変数
let currentSlide = 0;
let totalSlides = 0;

// スライドショー機能（DOM キャッシュ最適化版）
function initSlideshow() {
  // DOM要素を初期化時に1回だけ取得してキャッシュ
  const slides = document.querySelectorAll(".hero-slide");
  const dots = document.querySelectorAll(".slide-dot");
  const slideInfo = document.getElementById("slideInfo");

  totalSlides = slides.length;
  let slideInterval = null;
  let fadeTimeouts = [];

  if (slides.length === 0) {
    console.log("No slides found, skipping slideshow initialization");
    return;
  }

  // 視認性監視でパフォーマンス最適化
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        startSlideshow();
      } else {
        pauseSlideshow();
      }
    });
  });

  if (slides[0]) {
    observer.observe(slides[0].parentElement);
  }

  function showSlide(index) {
    // 既存のタイムアウトをクリア（メモリリーク防止）
    fadeTimeouts.forEach((timeout) => clearTimeout(timeout));
    fadeTimeouts = [];

    // 全てのスライドを非アクティブに
    slides.forEach((slide) => slide.classList.remove("active"));
    dots.forEach((dot) => dot.classList.remove("active"));

    // 指定されたスライドをアクティブに
    if (slides[index]) {
      slides[index].classList.add("active");
    }
    if (dots[index]) {
      dots[index].classList.add("active");
    }

    // スライド情報を更新（最適化されたタイムアウト管理）
    if (slideInfo && slides[index]) {
      const info = slides[index].getAttribute("data-info");
      if (info) {
        const fadeOutTimeout = setTimeout(() => {
          slideInfo.style.transition = "opacity 1s ease-in-out";
          slideInfo.classList.remove("active");
        }, 300);

        const fadeInTimeout = setTimeout(() => {
          slideInfo.textContent = info;
          slideInfo.style.transition = "opacity 1.6s ease-in-out";
          slideInfo.classList.add("active");
        }, 1400);

        fadeTimeouts.push(fadeOutTimeout, fadeInTimeout);
      }
    }

    currentSlide = index;
  }

  function nextSlide() {
    const next = (currentSlide + 1) % totalSlides;
    showSlide(next);
  }

  function startSlideshow() {
    if (slideInterval || totalSlides <= 1) return;
    // 最初のスライドは3秒、その後は5.5秒で切り替え
    const firstSlideDelay = 2600; // 3秒
    const normalSlideDelay = 6300; // 6秒

    // 最初のスライドのタイマー（3秒）
    slideInterval = setTimeout(() => {
      nextSlide();
      // 通常のインターバル開始（5秒間隔）
      slideInterval = setInterval(nextSlide, normalSlideDelay);
    }, firstSlideDelay);
  }

  function pauseSlideshow() {
    if (slideInterval) {
      clearInterval(slideInterval);
      slideInterval = null;
    }
  }

  // ドットクリックイベント（最適化されたリセット）
  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      // クリック時のトランジション速度（調整可能）
      const clickTransitionTime = "1.5s"; // ここで速度調整（例: "0.5s", "0.8s", "1s", "1.2s", "1.5s"）
      const clickTransitionMs = parseFloat(clickTransitionTime) * 1000; // ミリ秒に変換

      // クリック時は調整可能な速度のトランジションを適用
      slides.forEach((slide) => {
        slide.style.transition = `opacity ${clickTransitionTime} ease-in-out`;
      });

      showSlide(index);

      // トランジション完了後に通常の速度に戻す
      setTimeout(() => {
        slides.forEach((slide) => {
          slide.style.transition = "opacity var(--transition-slow)";
        });
      }, clickTransitionMs);

      // 手動操作時はスライドショーをリスタート
      pauseSlideshow();

      // クリックされた場合は長めに表示（6.3秒）してから次のスライドへ
      slideInterval = setInterval(nextSlide, 6300);
    });
  });

  // ページ非表示時のリソース管理
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      pauseSlideshow();
    } else {
      startSlideshow();
    }
  });

  // 初期設定（最初のスライドは3秒）

  // メモリリーク防止のクリーンアップ関数を返す
  window.slideshowCleanup = () => {
    pauseSlideshow();
    fadeTimeouts.forEach((timeout) => clearTimeout(timeout));
    fadeTimeouts = [];
    observer.disconnect();

    // イベントリスナー削除
    dots.forEach((dot) => {
      const newDot = dot.cloneNode(true);
      dot.parentNode.replaceChild(newDot, dot);
    });

    console.log("Slideshow cleanup completed");
  };

  console.log("Optimized slideshow initialized with", totalSlides, "slides");
}

// アクティブナビゲーション管理（DOM キャッシュ最適化版）
let cachedSections = null;
let cachedNavLinks = null;

function initNavigationCache() {
  // DOM要素を初期化時に1回だけ取得してキャッシュ
  cachedSections = document.querySelectorAll("section[id]");
  cachedNavLinks = document.querySelectorAll(".nav-links a");
}

function updateActiveNav() {
  // キャッシュされた要素を使用（DOM検索なし）
  if (!cachedSections || !cachedNavLinks) {
    initNavigationCache();
  }

  let currentSection = "";
  const scrollPos = window.scrollY + 200;

  cachedSections.forEach((section) => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.offsetHeight;

    if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
      currentSection = section.getAttribute("id");
    }
  });

  // メインナビゲーションのアクティブ状態更新
  cachedNavLinks.forEach((link) => {
    const wasActive = link.classList.contains("active");
    link.classList.remove("active");
    const href = link.getAttribute("href");

    if (href === "#" + currentSection) {
      link.classList.add("active");
      // スムーズなアクティブ状態変更エフェクト
      if (!wasActive) {
        link.style.transform = "scale(1.05)";
        setTimeout(() => {
          link.style.transform = "";
        }, 200);
      }
    }
  });
}

// 改善されたナビゲーションハイライト効果
function initEnhancedNavEffects() {
  const navLinks = document.querySelectorAll(".nav-links > li > a");

  navLinks.forEach((link) => {
    link.addEventListener("mouseenter", function () {
      // 他のリンクを少し薄くする効果
      navLinks.forEach((otherLink) => {
        if (otherLink !== this) {
          otherLink.style.opacity = "0.6";
        }
      });
    });

    link.addEventListener("mouseleave", function () {
      // 透明度をリセット
      navLinks.forEach((otherLink) => {
        otherLink.style.opacity = "";
      });
    });
  });

  // 完璧版ドロップダウンシステム - フェイルセーフ対応
  const dropdownParents = document.querySelectorAll(".nav-links li");
  let currentOpenDropdown = null;
  let globalCheckInterval = null;

  // 全てのドロップダウンを閉じる関数
  function hideAllDropdowns() {
    dropdownParents.forEach((parent) => {
      const dropdown = parent.querySelector(".dropdown");
      if (dropdown) {
        dropdown.style.opacity = "0";
        dropdown.style.visibility = "hidden";
        dropdown.style.pointerEvents = "none";
      }
    });
    currentOpenDropdown = null;

    // グローバルチェックを停止
    if (globalCheckInterval) {
      clearInterval(globalCheckInterval);
      globalCheckInterval = null;
    }
  }

  // グローバルマウス位置監視（フェイルセーフ）
  function startGlobalCheck() {
    if (globalCheckInterval) return;

    globalCheckInterval = setInterval(() => {
      if (!currentOpenDropdown) return;

      // マウスの現在位置を取得
      document.addEventListener(
        "mousemove",
        function checkGlobalMouse(e) {
          document.removeEventListener("mousemove", checkGlobalMouse);

          const dropdown = currentOpenDropdown.querySelector(".dropdown");
          if (!dropdown) return;

          const parentRect = currentOpenDropdown.getBoundingClientRect();
          const dropdownRect = dropdown.getBoundingClientRect();

          const mouseX = e.clientX;
          const mouseY = e.clientY;

          // より厳密な境界判定
          const inParentArea =
            mouseX >= parentRect.left - 2 &&
            mouseX <= parentRect.right + 2 &&
            mouseY >= parentRect.top - 2 &&
            mouseY <= parentRect.bottom + 10;

          const inDropdownArea =
            mouseX >= dropdownRect.left - 2 &&
            mouseX <= dropdownRect.right + 2 &&
            mouseY >= dropdownRect.top - 2 &&
            mouseY <= dropdownRect.bottom + 2;

          // どちらのエリアにもない場合は強制非表示
          if (!inParentArea && !inDropdownArea) {
            hideAllDropdowns();
          }
        },
        { once: true }
      );
    }, 150); // 150ms間隔でチェック
  }

  dropdownParents.forEach((parent) => {
    const dropdown = parent.querySelector(".dropdown");

    // ドロップダウンがない要素（ホーム、企業トップページ）の場合
    if (!dropdown) {
      parent.addEventListener("mouseenter", function () {
        // ドロップダウンのない要素にホバーした場合、全てのドロップダウンを即座に閉じる
        hideAllDropdowns();
      });
      return;
    }

    // ドロップダウン表示関数
    function showDropdown() {
      if (currentOpenDropdown === parent) return; // 既に開いている場合

      // 他のドロップダウンを即座に閉じる
      hideAllDropdowns();

      // 現在のドロップダウンを表示
      currentOpenDropdown = parent;
      dropdown.style.opacity = "1";
      dropdown.style.visibility = "visible";
      dropdown.style.transform = "translateX(-50%) translateY(0)";
      dropdown.style.pointerEvents = "all";

      // グローバル監視開始
      startGlobalCheck();
    }

    // ドロップダウン非表示関数（即座実行）
    function hideDropdown() {
      if (currentOpenDropdown === parent) {
        dropdown.style.opacity = "0";
        dropdown.style.visibility = "hidden";
        dropdown.style.transform = "translateX(-50%) translateY(0)";
        dropdown.style.pointerEvents = "none";
        currentOpenDropdown = null;

        // グローバルチェック停止
        if (globalCheckInterval) {
          clearInterval(globalCheckInterval);
          globalCheckInterval = null;
        }
      }
    }

    // 親要素イベント
    parent.addEventListener("mouseenter", function (e) {
      showDropdown();
    });

    parent.addEventListener("mouseleave", function (e) {
      // 即座にエリア判定
      const parentRect = parent.getBoundingClientRect();
      const dropdownRect = dropdown.getBoundingClientRect();

      const mouseX = e.clientX;
      const mouseY = e.clientY;

      const inParentArea =
        mouseX >= parentRect.left - 2 &&
        mouseX <= parentRect.right + 2 &&
        mouseY >= parentRect.top - 2 &&
        mouseY <= parentRect.bottom + 10;

      const inDropdownArea =
        mouseX >= dropdownRect.left - 2 &&
        mouseX <= dropdownRect.right + 2 &&
        mouseY >= dropdownRect.top - 2 &&
        mouseY <= dropdownRect.bottom + 2;

      if (!inParentArea && !inDropdownArea) {
        hideDropdown();
      }
    });

    // ドロップダウン要素イベント
    dropdown.addEventListener("mouseenter", function (e) {
      showDropdown();
    });

    dropdown.addEventListener("mouseleave", function (e) {
      // ドロップダウンから出た場合の判定
      const parentRect = parent.getBoundingClientRect();
      const dropdownRect = dropdown.getBoundingClientRect();

      const mouseX = e.clientX;
      const mouseY = e.clientY;

      const inParentArea =
        mouseX >= parentRect.left - 2 &&
        mouseX <= parentRect.right + 2 &&
        mouseY >= parentRect.top - 2 &&
        mouseY <= parentRect.bottom + 10;

      const inDropdownArea =
        mouseX >= dropdownRect.left - 2 &&
        mouseX <= dropdownRect.right + 2 &&
        mouseY >= dropdownRect.top - 2 &&
        mouseY <= dropdownRect.bottom + 2;

      if (!inParentArea && !inDropdownArea) {
        hideDropdown();
      }
    });
  });

  // 最終フェイルセーフ: ページ全体でのクリックで全ドロップダウンを閉じる
  document.addEventListener("click", function (e) {
    // ナビゲーション要素外でのクリックの場合
    const isNavClick = e.target.closest(".nav-links");
    if (!isNavClick && currentOpenDropdown) {
      hideAllDropdowns();
    }
  });

  console.log(
    "Perfect navigation effects initialized with failsafe dropdown management"
  );
}

// スムーススクロール（DOM キャッシュ最適化版）
function initSmoothScroll() {
  // DOM要素を初期化時に1回だけ取得してキャッシュ
  const nav = document.getElementById("verticalNav");
  const indicator = document.getElementById("navIndicator");

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });

        // クリック後にナビを閉じる（キャッシュした要素を使用）
        setTimeout(() => {
          nav.classList.remove("show");
          indicator.classList.remove("hover");
        }, 300);
      }
    });
  });
}

// スクロールアニメーション
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, observerOptions);

// アニメーション要素の初期設定
function initializeAnimations() {
  document
    .querySelectorAll(".card, .section-title, .section-intro")
    .forEach((el) => {
      el.style.opacity = "0";
      el.style.transform = "translateY(30px)";
      el.style.transition = "all 0.8s ease-out";
      observer.observe(el);
    });
}

// 動画ギャラリー機能
function initVideoGallery() {
  const tabButtons = document.querySelectorAll(".tab-button");
  const videoGrids = document.querySelectorAll(".video-grid");
  const videoItems = document.querySelectorAll(".video-item");

  // タブ切り替え機能
  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // アクティブタブを変更
      tabButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");

      // 対応する動画グリッドを表示
      const prefecture = button.getAttribute("data-prefecture");
      videoGrids.forEach((grid) => {
        grid.classList.remove("active");
        if (grid.id === prefecture + "-videos") {
          grid.classList.add("active");
        }
      });
    });
  });

  // 動画アイテムクリックでYouTube再生
  videoItems.forEach((item) => {
    item.addEventListener("click", () => {
      const youtubeId = item.getAttribute("data-youtube-id");
      if (youtubeId) {
        // 新しいタブでYouTube動画を開く
        window.open(`https://www.youtube.com/watch?v=${youtubeId}`, "_blank");
      }
    });
  });

  console.log("Video gallery initialized with", videoItems.length, "videos");
}

// YouTube遅延読み込み機能
function initYoutubeLazyLoading() {
  // グローバルイベント監視 - 動画プレースホルダーのクリックを処理
  document.addEventListener(
    "click",
    (e) => {
      // .video-placeholderの親要素である.card-imageもしくは.video-placeholder自体をチェック
      let placeholder = e.target.closest(".video-placeholder");

      // もし.video-placeholderが見つからない場合、.card-image内の.video-placeholderを探す
      if (!placeholder && e.target.classList.contains("card-image")) {
        placeholder = e.target.querySelector(".video-placeholder");
      }

      // クリックされた要素が.card-imageの場合もチェック
      if (!placeholder) {
        const cardImage = e.target.closest(".card-image");
        if (cardImage) {
          placeholder = cardImage.querySelector(".video-placeholder");
        }
      }

      if (placeholder) {
        const videoId = placeholder.dataset.videoId;
        if (videoId) {
          e.preventDefault();
          e.stopImmediatePropagation();
          loadYouTubeVideo(placeholder, videoId);
        }
      }
    },
    true
  );

  // 全ての動画プレースホルダーを取得してスタイル設定
  const videoPlaceholders = document.querySelectorAll(".video-placeholder");

  videoPlaceholders.forEach((placeholder) => {
    const videoId = placeholder.dataset.videoId;
    if (videoId) {
      placeholder.style.cursor = "pointer";
    }
  });
}

function loadYouTubeVideo(placeholder, videoId) {
  // iframe要素を作成
  const iframe = document.createElement("iframe");
  iframe.style.cssText =
    "z-index: 2; position: relative; width: 100%; height: 100%;";
  iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
  iframe.setAttribute("frameborder", "0");
  iframe.allow =
    "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
  iframe.allowFullscreen = true;

  // プレースホルダーをiframeに置き換え
  placeholder.parentNode.replaceChild(iframe, placeholder);
}

// 初期化
document.addEventListener("DOMContentLoaded", function () {
  try {
    initSlideshow();
    initializeAnimations();
    initSmoothScroll();
    initMobileNavigation(); // モバイルナビゲーション初期化
    initEnhancedNavEffects(); // デスクトップナビゲーション強化エフェクト
    initVideoGallery();
    initNavigationCache(); // DOM キャッシュ初期化
    initHeaderCache(); // ヘッダーキャッシュ初期化
    initYoutubeLazyLoading(); // YouTube遅延読み込み初期化
    initTempleFilter(); // 重要霊場フィルター初期化
    initFAQFunctionality(); // FAQ機能初期化

    // Tokaido専用機能の初期化（routes.htmlでのみ実行）
    if (typeof initRouteDetails === "function") {
      initRouteDetails();
      console.log("Route details system initialized");
    }

    updateActiveNav();

    // パフォーマンス監視初期化（開発環境のみ）
    if (
      typeof PerformanceMonitor === "function" &&
      (location.hostname === "localhost" || location.hostname === "127.0.0.1")
    ) {
      console.log("Performance monitoring enabled");

      // 5秒後にメモリ使用量チェック
      setTimeout(() => {
        window.performanceMonitor.checkMemoryUsage();
        console.log(
          "Performance Stats:",
          window.performanceMonitor.getPerformanceStats()
        );
      }, 5000);

      // FPS測定開始
      window.performanceMonitor.measureFPS();
    }

    console.log(
      "Enhanced site with improved desktop and mobile navigation fully initialized"
    );
  } catch (error) {
    console.error("Initialization error:", error);
  }
});

// モバイルナビゲーション
function initMobileNavigation() {
  const mobileMenuToggle = document.getElementById("mobileMenuToggle");
  const mobileMenuClose = document.getElementById("mobileMenuClose");
  const mobileMenu = document.getElementById("mobileMenu");
  const mobileMenuOverlay = document.getElementById("mobileMenuOverlay");
  const mobileMenuLinks = document.querySelectorAll(".mobile-menu-link");

  if (
    !mobileMenuToggle ||
    !mobileMenuClose ||
    !mobileMenu ||
    !mobileMenuOverlay
  ) {
    console.log("Mobile navigation elements not found");
    return;
  }

  // メニューを開く
  function openMobileMenu() {
    mobileMenu.classList.add("active");
    mobileMenuOverlay.classList.add("active");
    mobileMenuToggle.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  // メニューを閉じる
  function closeMobileMenu() {
    mobileMenu.classList.remove("active");
    mobileMenuOverlay.classList.remove("active");
    mobileMenuToggle.classList.remove("active");
    document.body.style.overflow = "";
  }

  // イベントリスナー追加
  mobileMenuToggle.addEventListener("click", function (e) {
    e.preventDefault();
    if (mobileMenu.classList.contains("active")) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  });

  mobileMenuClose.addEventListener("click", function (e) {
    e.preventDefault();
    closeMobileMenu();
  });

  mobileMenuOverlay.addEventListener("click", function (e) {
    e.preventDefault();
    closeMobileMenu();
  });

  // メニューリンククリック時にメニューを閉じる
  mobileMenuLinks.forEach((link) => {
    link.addEventListener("click", function () {
      // どちらのリンクタイプでも即座にメニューを閉じる
      closeMobileMenu();
    });
  });

  // ESCキーでメニューを閉じる
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && mobileMenu.classList.contains("active")) {
      closeMobileMenu();
    }
  });

  // ウィンドウリサイズ時にメニューを閉じる
  window.addEventListener("resize", function () {
    if (window.innerWidth > 768 && mobileMenu.classList.contains("active")) {
      closeMobileMenu();
    }
  });

  console.log("Mobile navigation initialized");
}

// スクロールイベントに進捗更新を追加（DOM キャッシュ最適化版）
let cachedHeader = null;

function initHeaderCache() {
  cachedHeader = document.querySelector("header");
}

let scrollTicking = false;
let lastScrollTime = 0;

function handleScroll() {
  // スクロール頻度制限（GPU負荷削減）
  const now = performance.now();
  if (now - lastScrollTime < 32) {
    // 30FPSに制限
    scrollTicking = false;
    return;
  }
  lastScrollTime = now;

  // 既存のスクロール処理（キャッシュした要素を使用）
  if (!cachedHeader) {
    initHeaderCache();
  }

  if (cachedHeader) {
    if (window.scrollY > 100) {
      cachedHeader.style.background = "rgba(0, 0, 0, 0.95)";
    } else {
      cachedHeader.style.background = "rgba(0, 0, 0, 0.9)";
    }
  }

  updateActiveNav();
  scrollTicking = false;
}

// スクロールイベントをthrottleでGPU負荷削減
let scrollTimeout;
window.addEventListener(
  "scroll",
  () => {
    if (!scrollTicking) {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        requestAnimationFrame(handleScroll);
      }, 16);
      scrollTicking = true;
    }
  },
  { passive: true }
);

// 重要霊場フィルター機能
function initTempleFilter() {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".card, .station-card");

  if (!filterButtons.length || !cards.length) {
    return;
  }

  filterButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const filter = this.getAttribute("data-filter");

      // アクティブボタンの切り替え
      filterButtons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");

      // カードのフィルタリング
      cards.forEach((card) => {
        const cardCategory = card.getAttribute("data-category");
        const shouldShow =
          filter === "all" ||
          (filter === "special" && cardCategory === "special") ||
          card.classList.contains(filter) ||
          card.querySelector('[data-prefecture="' + filter + '"]');

        if (shouldShow) {
          card.style.display = "block";
          card.style.opacity = "1";
        } else {
          card.style.display = "none";
          card.style.opacity = "0";
        }
      });
    });
  });

  console.log("Temple filter system initialized");
}

// FAQ機能
function initFAQFunctionality() {
  const faqQuestions = document.querySelectorAll(".faq-question");
  const faqItems = document.querySelectorAll(".faq-item");
  const searchInput = document.querySelector(".faq-search");
  const categoryButtons = document.querySelectorAll(".category-btn");
  const noResults = document.querySelector(".no-results");

  if (!faqQuestions.length) {
    console.log("FAQ elements not found");
    return;
  }

  // FAQ項目の開閉
  faqQuestions.forEach((question) => {
    question.addEventListener("click", function () {
      const faqItem = this.closest(".faq-item");
      const faqAnswer = faqItem.querySelector(".faq-answer");
      const isActive = faqItem.classList.contains("active");

      // 他のFAQ項目を閉じる
      faqItems.forEach((item) => {
        if (item !== faqItem) {
          item.classList.remove("active");
          const answer = item.querySelector(".faq-answer");
          if (answer) {
            answer.style.maxHeight = "0";
          }
        }
      });

      // 現在の項目をトグル
      if (isActive) {
        faqItem.classList.remove("active");
        faqAnswer.style.maxHeight = "0";
      } else {
        faqItem.classList.add("active");
        // scrollHeightに余裕を持たせて全文が表示されるようにする
        const contentHeight = faqAnswer.scrollHeight + 50;
        faqAnswer.style.maxHeight = contentHeight + "px";
      }
    });
  });

  // 検索機能
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase();
      let visibleCount = 0;

      faqItems.forEach((item) => {
        const questionText = item
          .querySelector(".faq-question span")
          .textContent.toLowerCase();
        const answerText = item
          .querySelector(".faq-answer p")
          .textContent.toLowerCase();

        if (
          questionText.includes(searchTerm) ||
          answerText.includes(searchTerm)
        ) {
          item.style.display = "block";
          visibleCount++;
        } else {
          item.style.display = "none";
        }
      });

      // 検索結果なしメッセージの表示/非表示
      if (noResults) {
        noResults.style.display =
          visibleCount === 0 && searchTerm !== "" ? "block" : "none";
      }
    });
  }

  // カテゴリフィルター
  categoryButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const category = this.getAttribute("data-category");

      // アクティブボタンの切り替え
      categoryButtons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");

      // 検索ボックスをクリア
      if (searchInput) {
        searchInput.value = "";
      }

      let visibleCount = 0;

      // カテゴリフィルタリング
      faqItems.forEach((item) => {
        const itemCategory = item.getAttribute("data-category");

        if (category === "all" || itemCategory === category) {
          item.style.display = "block";
          visibleCount++;
        } else {
          item.style.display = "none";
        }

        // アクティブ状態をリセット
        item.classList.remove("active");
        const answer = item.querySelector(".faq-answer");
        if (answer) {
          answer.style.maxHeight = "0";
        }
      });

      // 検索結果なしメッセージを隠す
      if (noResults) {
        noResults.style.display = "none";
      }
    });
  });

  console.log("FAQ functionality initialized with", faqItems.length, "items");
}
