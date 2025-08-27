// グローバル変数
let currentSlide = 0;
let totalSlides = 0;

// スライドショー機能（DOM キャッシュ最適化版）
function initSlideshow() {
  // DOM要素を初期化時に1回だけ取得してキャッシュ
  const slides = document.querySelectorAll(".hero-slide");
  const dots = document.querySelectorAll(".slide-dot");
  const slideInfo = document.getElementById("slideInfo");
  const progressFill = document.querySelector(".progress-line-fill");

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

    // プログレスバー更新（requestAnimationFrameで最適化）
    requestAnimationFrame(() => {
      updateHorizontalProgress(index + 1, totalSlides);
    });

    currentSlide = index;
  }

  function updateHorizontalProgress(current, total) {
    if (progressFill) {
      const progressWidth = current / total;
      progressFill.style.transform = `scaleX(${progressWidth})`;
    }
  }

  function nextSlide() {
    const next = (currentSlide + 1) % totalSlides;
    showSlide(next);
  }

  function startSlideshow() {
    if (slideInterval || totalSlides <= 1) return;
    slideInterval = setInterval(nextSlide, 6000);
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
      showSlide(index);
      resetProgress();
      // 手動操作時はスライドショーをリスタート
      pauseSlideshow();
      startSlideshow();
    });
  });

  // 進行バーのリセット機能
  function resetProgress() {
    if (progressFill) {
      progressFill.style.animation = "none";
      progressFill.style.transform = "scaleX(0)";

      requestAnimationFrame(() => {
        progressFill.style.animation = "horizontalProgress 6s linear infinite";
      });
    }
  }

  // ページ非表示時のリソース管理
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      pauseSlideshow();
    } else {
      startSlideshow();
    }
  });

  // 初期設定
  resetProgress();
  updateHorizontalProgress(1, totalSlides);

  // クリーンアップ関数を返す（必要に応じて使用）
  window.slideshowCleanup = () => {
    pauseSlideshow();
    fadeTimeouts.forEach((timeout) => clearTimeout(timeout));
    observer.disconnect();
  };

  console.log("Optimized slideshow initialized with", totalSlides, "slides");
}

// 軽量化：パララックス機能を無効化
function initParallaxAndDepth() {
  console.log("Parallax disabled for performance optimization");
}

// 軽量化：パーティクル生成を無効化
function createFloatingParticles() {
  console.log("Particles disabled for performance optimization");
}

// 改良されたホバーナビゲーション制御（パララックス考慮）
function initHoverNavigation() {
  const nav = document.getElementById("verticalNav");
  const trigger = document.getElementById("navTrigger");
  const indicator = document.getElementById("navIndicator");

  let isNavOpen = false;
  let hoverTimeout;

  // トリガーエリアにマウスが入った時
  trigger.addEventListener("mouseenter", () => {
    clearTimeout(hoverTimeout);
    isNavOpen = true;
    nav.classList.add("show");
    indicator.classList.add("hover");
  });

  // トリガーエリアからマウスが離れた時
  trigger.addEventListener("mouseleave", () => {
    hoverTimeout = setTimeout(() => {
      if (!nav.matches(":hover")) {
        closeNavigation();
      }
    }, 150);
  });

  // ナビゲーションにマウスが入った時
  nav.addEventListener("mouseenter", () => {
    clearTimeout(hoverTimeout);
    isNavOpen = true;
  });

  // ナビゲーションからマウスが離れた時
  nav.addEventListener("mouseleave", () => {
    closeNavigation();
  });

  function closeNavigation() {
    isNavOpen = false;
    nav.classList.remove("show");
    indicator.classList.remove("hover");
  }
}

// アクティブナビゲーション管理（DOM キャッシュ最適化版）
let cachedSections = null;
let cachedNavLinks = null;

function initNavigationCache() {
  // DOM要素を初期化時に1回だけ取得してキャッシュ
  cachedSections = document.querySelectorAll("section[id]");
  cachedNavLinks = document.querySelectorAll(".vertical-nav a");
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

  cachedNavLinks.forEach((link) => {
    link.classList.remove("active");
    const href = link.getAttribute("href");
    if (href === "#" + currentSection) {
      link.classList.add("active");
    }
  });
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

// アコーディオン機能の初期化
function initAccordion() {
  setTimeout(() => {
    const accordionHeaders = document.querySelectorAll(".accordion-header");

    console.log("Found accordion headers:", accordionHeaders.length);

    if (accordionHeaders.length === 0) {
      console.log(
        "No accordion headers found, skipping accordion initialization"
      );
      return;
    }

    // 各アコーディオンヘッダーにクリックイベントを設定
    for (let i = 0; i < accordionHeaders.length; i++) {
      const header = accordionHeaders[i];
      const targetId = header.getAttribute("data-target");

      console.log(`Setting up accordion header ${i}:`, targetId);

      header.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        console.log("Accordion header clicked:", targetId);

        const targetContent = document.getElementById(targetId);
        const isCurrentlyActive = header.classList.contains("active");

        if (!targetContent) {
          console.error("Target content not found:", targetId);
          return;
        }

        if (isCurrentlyActive) {
          // 現在アクティブなアコーディオンを閉じる
          header.classList.remove("active");
          targetContent.classList.remove("active");
          console.log("Accordion closed:", targetId);
        } else {
          // 他のアコーディオンを全て閉じる
          for (let j = 0; j < accordionHeaders.length; j++) {
            accordionHeaders[j].classList.remove("active");
            const otherTargetId =
              accordionHeaders[j].getAttribute("data-target");
            const otherContent = document.getElementById(otherTargetId);
            if (otherContent) {
              otherContent.classList.remove("active");
            }
          }

          // クリックされたアコーディオンを開く
          header.classList.add("active");
          targetContent.classList.add("active");
          console.log("Accordion opened:", targetId);
        }
      });
    }

    console.log("Accordion functionality initialized successfully");
  }, 100);
}

// 動画切り替え機能の初期化
function initVideoSelector() {
  setTimeout(() => {
    const videoButtons = document.querySelectorAll(".video-btn");
    const mainVideo = document.getElementById("main-video");

    console.log("Found video buttons:", videoButtons.length);

    if (videoButtons.length === 0 || !mainVideo) {
      console.log(
        "No video buttons or main video found, skipping video selector initialization"
      );
      return;
    }

    for (let i = 0; i < videoButtons.length; i++) {
      const button = videoButtons[i];
      const videoId = button.getAttribute("data-video");
      const videoTitle = button.getAttribute("data-title");

      console.log(`Setting up video button ${i}:`, videoId);

      button.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        console.log("Video button clicked:", videoId);

        // 全てのボタンからactiveクラスを削除
        for (let j = 0; j < videoButtons.length; j++) {
          videoButtons[j].classList.remove("active");
        }

        // クリックされたボタンにactiveクラスを追加
        button.classList.add("active");

        // 動画を切り替え
        if (videoId && videoId !== "REPLACE_WITH_ACTUAL_ID") {
          const newSrc = `https://www.youtube.com/embed/${videoId}`;
          mainVideo.src = newSrc;
          mainVideo.title = `お遍路入門 - ${videoTitle}`;
          console.log("Video switched to:", newSrc);
        } else {
          console.log("Video ID not available yet:", videoId);
        }
      });
    }

    console.log("Video selector functionality initialized successfully");
  }, 100);
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

// タブ機能の初期化
function initTabs() {
  // 少し遅延して確実にDOMが読み込まれてから実行
  setTimeout(() => {
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    console.log("Found tab buttons:", tabButtons.length);
    console.log("Found tab contents:", tabContents.length);

    if (tabButtons.length === 0) {
      console.log("No tab buttons found, skipping tab initialization");
      return;
    }

    // 各タブボタンにクリックイベントを設定
    for (let i = 0; i < tabButtons.length; i++) {
      const button = tabButtons[i];
      const targetTab = button.getAttribute("data-tab");

      console.log(`Setting up tab button ${i}:`, targetTab);

      button.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        console.log("Tab button clicked:", targetTab);

        // 全てのタブボタンからactiveクラスを削除
        for (let j = 0; j < tabButtons.length; j++) {
          tabButtons[j].classList.remove("active");
        }

        // 全てのタブコンテンツからactiveクラスを削除
        for (let k = 0; k < tabContents.length; k++) {
          tabContents[k].classList.remove("active");
        }

        // クリックされたボタンにactiveクラスを追加
        button.classList.add("active");

        // 対応するコンテンツにactiveクラスを追加
        const targetContent = document.getElementById(targetTab);
        if (targetContent) {
          targetContent.classList.add("active");
          console.log("Successfully activated tab:", targetTab);
        } else {
          console.error("Target content not found:", targetTab);
        }
      });
    }

    console.log("Tab functionality initialized successfully");
  }, 100);
}

// 初期化
document.addEventListener("DOMContentLoaded", function () {
  try {
    initSlideshow();
    initializeAnimations();
    initSmoothScroll();
    initHoverNavigation();
    initParallaxAndDepth();
    initVideoGallery();
    initTabs(); // タブ機能を追加
    initAccordion(); // アコーディオン機能を追加
    initVideoSelector(); // 動画切り替え機能を追加
    initNavigationCache(); // DOM キャッシュ初期化
    initHeaderCache(); // ヘッダーキャッシュ初期化
    initYoutubeLazyLoading(); // YouTube遅延読み込み初期化
    updateActiveNav();

    console.log("Enhanced site with YouTube lazy loading fully initialized");
  } catch (error) {
    console.error("Initialization error:", error);
  }
});

// スクロールイベントに進捗更新を追加（DOM キャッシュ最適化版）
let cachedHeader = null;

function initHeaderCache() {
  cachedHeader = document.querySelector("header");
}

let scrollTicking = false;

function handleScroll() {
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

window.addEventListener(
  "scroll",
  () => {
    if (!scrollTicking) {
      requestAnimationFrame(handleScroll);
      scrollTicking = true;
    }
  },
  { passive: true }
);
