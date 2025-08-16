// グローバル変数
let currentSlide = 0;
let totalSlides = 0;

// スライドショー機能
function initSlideshow() {
  const slides = document.querySelectorAll(".hero-slide");
  const dots = document.querySelectorAll(".slide-dot");
  const slideInfo = document.getElementById("slideInfo");
  totalSlides = slides.length;

  if (slides.length === 0) {
    console.log("No slides found, skipping slideshow initialization");
    return;
  }

  function showSlide(index) {
    // 全てのスライドを非アクティブに
    slides.forEach((slide) => {
      slide.classList.remove("active");
    });
    dots.forEach((dot) => {
      dot.classList.remove("active");
    });

    // 指定されたスライドをアクティブに
    if (slides[index]) {
      slides[index].classList.add("active");
    }
    if (dots[index]) {
      dots[index].classList.add("active");
    }

    // スライド情報を更新（画像を見てもらってから説明を表示）
    if (slideInfo && slides[index]) {
      const info = slides[index].getAttribute("data-info");
      if (info) {
        // 少し遅れてフェードアウト（現在の文字をもう少し読める時間を確保）
        setTimeout(() => {
          // フェードアウト用のトランジション時間を設定
          slideInfo.style.transition = "opacity 1s ease-in-out";
          slideInfo.classList.remove("active");
        }, 300);

        // 画像をじっくり見てもらってからテキストを更新・表示
        setTimeout(() => {
          slideInfo.textContent = info;
          // フェードイン用のトランジション時間を設定
          slideInfo.style.transition = "opacity 1.6s ease-in-out";
          slideInfo.classList.add("active");
        }, 1400);
      }
    }

    // 水平プログレスバーを更新
    updateHorizontalProgress(index + 1, totalSlides);

    currentSlide = index;
  }

  function updateHorizontalProgress(current, total) {
    const progressFill = document.querySelector(".progress-line-fill");

    if (progressFill) {
      const progressWidth = (current / total) * 100;
      progressFill.style.width = progressWidth + "%";
    }
  }

  function nextSlide() {
    const next = (currentSlide + 1) % totalSlides;
    showSlide(next);
  }

  // ドットクリックイベント
  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      showSlide(index);
      resetProgress();
    });
  });

  // 自動スライド（6秒間隔）
  if (totalSlides > 1) {
    setInterval(nextSlide, 6000);
  }

  // 進行バーのリセット機能
  resetProgress();

  // 初期状態でプログレスを設定
  updateHorizontalProgress(1, totalSlides);

  function resetProgress() {
    const progressFill = document.querySelector(".progress-line-fill");
    if (progressFill) {
      // アニメーションをリセット
      progressFill.style.animation = "none";
      progressFill.style.width = "0%";

      // 少し遅延してからアニメーションを再開
      setTimeout(() => {
        progressFill.style.animation = "horizontalProgress 6s linear infinite";
      }, 50);
    }
  }

  console.log("Slideshow initialized with", totalSlides, "slides");
}

// パララックス効果と粒子生成
function initParallaxAndDepth() {
  const parallaxLayers = {
    mountainsFar: document.getElementById("mountainsFar"),
    mountainsMid: document.getElementById("mountainsMid"),
    mountainsNear: document.getElementById("mountainsNear"),
    fogLayer: document.getElementById("fogLayer"),
    lightRays: document.getElementById("lightRays"),
  };

  // 浮遊粒子を生成
  createFloatingParticles();

  // パララックススクロール
  function handleParallax() {
    const scrollY = window.pageYOffset;

    if (parallaxLayers.mountainsFar) {
      parallaxLayers.mountainsFar.style.transform = `translateY(${
        scrollY * 0.1
      }px)`;
    }
    if (parallaxLayers.mountainsMid) {
      parallaxLayers.mountainsMid.style.transform = `translateY(${
        scrollY * 0.3
      }px)`;
    }
    if (parallaxLayers.mountainsNear) {
      parallaxLayers.mountainsNear.style.transform = `translateY(${
        scrollY * 0.6
      }px)`;
    }
    if (parallaxLayers.fogLayer) {
      parallaxLayers.fogLayer.style.transform = `translateY(${
        scrollY * 0.2
      }px) translateX(${Math.sin(scrollY * 0.001) * 20}px)`;
    }
    if (parallaxLayers.lightRays) {
      parallaxLayers.lightRays.style.transform = `translateY(${
        scrollY * 0.1
      }px) rotate(${scrollY * 0.01}deg)`;
    }
  }

  // スクロールイベントにパララックスを追加
  let ticking = false;
  function updateParallax() {
    if (!ticking) {
      requestAnimationFrame(() => {
        handleParallax();
        ticking = false;
      });
      ticking = true;
    }
  }

  window.addEventListener("scroll", updateParallax);

  console.log("Parallax and depth effects initialized");
}

// 浮遊粒子生成
function createFloatingParticles() {
  const container = document.getElementById("floatingParticles");
  if (!container) return;

  const particleCount = 15;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.className = "particle-float";
    particle.style.left = Math.random() * 100 + "%";
    particle.style.animationDelay = Math.random() * 12 + "s";
    particle.style.animationDuration = Math.random() * 8 + 10 + "s";

    // ランダムな色調
    const hue = Math.random() * 60 + 30; // 30-90の範囲で暖色系
    particle.style.background = `radial-gradient(circle, hsla(${hue}, 70%, 70%, 0.8) 0%, transparent 70%)`;

    container.appendChild(particle);
  }
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

// アクティブナビゲーション管理
function updateActiveNav() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".vertical-nav a");

  let currentSection = "";
  const scrollPos = window.scrollY + 200;

  sections.forEach((section) => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.offsetHeight;

    if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
      currentSection = section.getAttribute("id");
    }
  });

  navLinks.forEach((link) => {
    link.classList.remove("active");
    const href = link.getAttribute("href");
    if (href === "#" + currentSection) {
      link.classList.add("active");
    }
  });
}

// スムーススクロール
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });

        // クリック後にナビを閉じる
        const nav = document.getElementById("verticalNav");
        const indicator = document.getElementById("navIndicator");
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

// 初期化
document.addEventListener("DOMContentLoaded", function () {
  try {
    initSlideshow();
    initializeAnimations();
    initSmoothScroll();
    initHoverNavigation();
    initParallaxAndDepth();
    initVideoGallery();
    updateActiveNav();

    console.log(
      "Enhanced site with horizontal progress indicator fully initialized"
    );
  } catch (error) {
    console.error("Initialization error:", error);
  }
});

// スクロールイベントに進捗更新を追加
window.addEventListener("scroll", () => {
  // 既存のスクロール処理
  const header = document.querySelector("header");
  if (window.scrollY > 100) {
    header.style.background = "rgba(0, 0, 0, 0.95)";
  } else {
    header.style.background = "rgba(0, 0, 0, 0.9)";
  }

  updateActiveNav();
});
