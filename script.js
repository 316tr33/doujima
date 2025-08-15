// スライドショー機能
function initSlideshow() {
  let currentSlide = 0;
  const slides = document.querySelectorAll(".hero-slide");
  const dots = document.querySelectorAll(".slide-dot");
  const slideInfo = document.getElementById("slideInfo");
  const totalSlides = slides.length;

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

    // スライド情報を更新
    if (slideInfo && slides[index]) {
      const info = slides[index].getAttribute("data-info");
      if (info) {
        slideInfo.textContent = info;
        slideInfo.classList.remove("active");
        setTimeout(() => {
          slideInfo.classList.add("active");
        }, 100);
      }
    }

    currentSlide = index;
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

  function resetProgress() {
    const progressBar = document.querySelector(".slide-progress");
    if (progressBar) {
      progressBar.style.animation = "none";
      setTimeout(() => {
        progressBar.style.animation = "slideProgress 6s linear infinite";
      }, 10);
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

// 統合スクロールイベント管理
window.addEventListener("scroll", () => {
  // ヘッダー背景変更
  const header = document.querySelector("header");
  if (window.scrollY > 100) {
    header.style.background = "rgba(0, 0, 0, 0.95)";
  } else {
    header.style.background = "rgba(0, 0, 0, 0.9)";
  }

  // アクティブナビ更新
  updateActiveNav();
});

// 初期化
document.addEventListener("DOMContentLoaded", function () {
  try {
    initSlideshow();
    initializeAnimations();
    initSmoothScroll();
    initHoverNavigation();
    initParallaxAndDepth();
    updateActiveNav();

    console.log("Enhanced site with depth effects fully initialized");
  } catch (error) {
    console.error("Initialization error:", error);
  }
});
